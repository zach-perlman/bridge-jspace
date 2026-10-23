"""d1_verdict's late-binding rule: the pure verdict and a run on a synthetic map and parts run (no model)."""

import argparse
import json

from scripts import d1_verdict as V


def cell(lk: dict, rc: dict) -> dict:
    """lookup / recall part -> (switched, n) as [rate, lo, hi, n]."""
    return {f: {p: [*V.wilson(k, n), n] for p, (k, n) in d.items()} for f, d in (("lookup", lk), ("recall", rc))}


SPLIT = {"jspace": (0, 100), "not_jspace": (50, 100), "rand_sub": (0, 100)}  # lens part silent, the rest moves
RECALL_OK = {"jspace": (60, 100), "not_jspace": (40, 100), "rand_sub": (5, 100)}
MOVES = {"jspace": (35, 100), "not_jspace": (70, 100), "rand_sub": (2, 100)}


def test_late_binding_verdict_branches():
    late = V.late_binding_verdict({"context:30": cell(MOVES, RECALL_OK), "context:33": cell(SPLIT, RECALL_OK)})
    assert late["verdict"] == "late binding holds at context:33" and late["late_cells"] == ["context:33"]
    fails = V.late_binding_verdict({"context:30": cell(MOVES, RECALL_OK), "context:33": cell(MOVES, RECALL_OK)})
    assert fails["verdict"].startswith("finding 2 fails")
    weak_recall = {**RECALL_OK, "jspace": (20, 100)}  # the recall control fails at the split cell
    v = V.late_binding_verdict({"context:33": cell(SPLIT, weak_recall)})["verdict"]
    assert v.startswith("inconclusive: the split holds at context:33")
    no_beat = {**RECALL_OK, "rand_sub": (55, 100)}  # on recalls the lens part does no better than its size
    assert V.late_binding_verdict({"context:33": cell(SPLIT, no_beat)})["verdict"].startswith("inconclusive")
    size = {**MOVES, "rand_sub": (30, 100)}  # the lens part moves lookups, but so does a random subspace of its size
    v = V.late_binding_verdict({"context:30": cell(MOVES, RECALL_OK), "context:33": cell(size, RECALL_OK)})["verdict"]
    assert v.startswith("inconclusive: the lens part moves >= 20%") and v.endswith("context:33")
    upper = {**SPLIT, "jspace": (4, 100)}  # 4% but its upper bound is above 5%: not late binding, not moving
    assert V.late_binding_verdict({"context:33": cell(upper, RECALL_OK)})["verdict"] == "inconclusive"
    assert V.late_binding_verdict({})["verdict"].startswith("not interpretable")
    old_run = {**SPLIT, "rand_sub": (0, 0)}  # a parts run from before rand_sub
    assert V.late_binding_verdict({"context:33": cell(old_run, RECALL_OK)})["verdict"].startswith("not interpretable")


def test_late_binding_run_and_figure(tmp_path, monkeypatch):
    sp, out = tmp_path / "statement_positions", tmp_path / "d1_verdict"
    monkeypatch.setattr(V, "SP", sp)
    rates = [{"family": "PP", "set": s, "layer": la, "transit": tr, "cf": {"flips": [f, f - 0.05, f + 0.03]}}
             for s, la, tr, f in (("context", 24, True, 0.99), ("context", 33, True, 0.98), ("bind_bridge", 36, False, 0.35))]  # fmt: skip
    (sp / "M").mkdir(parents=True)
    (sp / "M" / "summary.json").write_text(json.dumps({"rates": rates}))
    plan = {("PP", "context", 33): {"full": 100, **{p: k for p, (k, _) in SPLIT.items()}},
            ("PM", "context", 33): {"full": 97, **{p: k for p, (k, _) in RECALL_OK.items()}},
            ("PP", "bind_bridge", 36): {"full": 30, **{p: k for p, (k, _) in MOVES.items()}},
            ("PM", "bind_bridge", 36): {"full": 80, **{p: k for p, (k, _) in RECALL_OK.items()}},
            ("PP", "context", 24): {"full": 99, **{p: k for p, (k, _) in MOVES.items()}},
            ("PM", "context", 24): {"full": 97, **{p: k for p, (k, _) in RECALL_OK.items()}}}  # fmt: skip
    rows, fve = [], []
    for (fam, s, la), hits in plan.items():
        for i in range(100):
            base = {"family": fam, "name": f"item{i}", "scene": f"s{i}", "set": s, "layer": la, "source": "cf"}
            for p, k in hits.items():
                rows.append({**base, "part": p, "null": False, "role": "b" if i < k else "A"})
            rows.append({**base, "part": "jspace", "null": True, "role": "A"})
            fve += [
                {**base, "what": w, "share": sh} for w, sh in (("jspace", 0.3), ("rand_sub", 0.3), ("rand_omp", 0.05))
            ]
    (sp / "P").mkdir()
    (sp / "P" / "outcomes.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    (sp / "P" / "fve.jsonl").write_text("\n".join(json.dumps(r) for r in fve) + "\n")
    a = argparse.Namespace(map="M", parts="P", lookup="PP", recall="PM", tasks_set=None, out=str(out),
                           cells=["bind_bridge:36", "context:33"], reference=["context:24"], figures=False)  # fmt: skip
    assert V.late_binding(a) == 0
    (d,) = out.glob("P_*")
    v = json.loads((d / "verdict.json").read_text())
    assert v["decisive_cells"] == ["context:33"]  # bind_bridge:36 is not in transit on the map: reported only
    assert v["verdict"] == "late binding holds at context:33"
    assert v["cells"]["bind_bridge:36"]["role"] == "not in transit" and v["cells"]["context:24"]["role"] == "reference"
    assert (
        v["cells"]["context:33"]["lookup"]["not_jspace"][0] == 0.5
        and v["cells"]["context:33"]["recall"]["jspace"][3] == 100
    )
    assert v["cells"]["context:33"]["lookup"]["jspace_null"][3] == 100
    assert v["cells"]["context:33"]["median_share"] == {"jspace": 0.3, "rand_sub": 0.3, "rand_omp": 0.05}
    assert "late binding holds" in (d / "verdict.md").read_text()
    a.figures = True
    assert V.late_figures(a) == 0
    assert list(d.glob("analysis-*-figures/late_binding.png"))
