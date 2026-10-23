"""d1_verdict's late-switch and rest-size rules: the pure verdicts and runs on a synthetic map and parts run (no
model)."""

import argparse
import json

from scripts import d1_verdict as V


def cell(lk: dict, rc: dict) -> dict:
    """lookup / recall part -> (switched, n) as [rate, lo, hi, n]."""
    return {f: {p: [*V.wilson(k, n), n] for p, (k, n) in d.items()} for f, d in (("lookup", lk), ("recall", rc))}


SPLIT = {"jspace": (0, 100), "not_jspace": (50, 100), "rand_sub": (0, 100)}  # lens part silent, the rest moves
RECALL_OK = {"jspace": (60, 100), "not_jspace": (40, 100), "rand_sub": (5, 100)}
MOVES = {"jspace": (35, 100), "not_jspace": (70, 100), "rand_sub": (2, 100)}


def test_late_switch_verdict_branches():
    late = V.late_switch_verdict({"context:30": cell(MOVES, RECALL_OK), "context:33": cell(SPLIT, RECALL_OK)})
    assert late["verdict"] == "late switch holds at context:33" and late["late_cells"] == ["context:33"]
    fails = V.late_switch_verdict({"context:30": cell(MOVES, RECALL_OK), "context:33": cell(MOVES, RECALL_OK)})
    assert fails["verdict"].startswith("finding 2 fails")
    weak_recall = {**RECALL_OK, "jspace": (20, 100)}  # the recall control fails at the split cell
    v = V.late_switch_verdict({"context:33": cell(SPLIT, weak_recall)})["verdict"]
    assert v.startswith("inconclusive: the split holds at context:33")
    no_beat = {**RECALL_OK, "rand_sub": (55, 100)}  # on recalls the lens part does no better than its size
    assert V.late_switch_verdict({"context:33": cell(SPLIT, no_beat)})["verdict"].startswith("inconclusive")
    size = {**MOVES, "rand_sub": (30, 100)}  # the lens part moves lookups, but so does a random subspace of its size
    v = V.late_switch_verdict({"context:30": cell(MOVES, RECALL_OK), "context:33": cell(size, RECALL_OK)})["verdict"]
    assert v.startswith("inconclusive: the lens part moves >= 20%") and v.endswith("context:33")
    upper = {**SPLIT, "jspace": (4, 100)}  # 4% but its upper bound is above 5%: no late switch, not moving
    assert V.late_switch_verdict({"context:33": cell(upper, RECALL_OK)})["verdict"] == "inconclusive"
    assert V.late_switch_verdict({})["verdict"].startswith("not interpretable")
    old_run = {**SPLIT, "rand_sub": (0, 0)}  # a parts run from before rand_sub
    assert V.late_switch_verdict({"context:33": cell(old_run, RECALL_OK)})["verdict"].startswith("not interpretable")


def test_late_switch_needs_the_lens_part_to_stay_quiet():
    """Dan's amendment (23 Oct 12:30): once quiet at a decisive cell, the lens part stays quiet (Wilson upper bound
    <= 10% of lookups) at every later decisive cell of the same position set."""
    back = V.late_switch_verdict({"context:30": cell(SPLIT, RECALL_OK), "context:33": cell(MOVES, RECALL_OK)})
    assert back["late_cells"] == [] and not back["checks"]["context:30"]["stays_quiet"]
    assert back["verdict"] == "inconclusive: the split holds at context:30 but fails there: context:30 stays_quiet"
    six = {**SPLIT, "jspace": (6, 100)}  # 6%: upper bound 12.5% > 10%, so it has come back
    assert V.wilson(6, 100)[2] > V.LATE_STAYS_HI
    v = V.late_switch_verdict({"context:30": cell(SPLIT, RECALL_OK), "context:36": cell(six, RECALL_OK)})
    assert v["late_cells"] == []
    four = {**SPLIT, "jspace": (4, 100)}  # 4%: upper bound 9.8% <= 10%, still quiet
    assert V.wilson(4, 100)[2] <= V.LATE_STAYS_HI
    v = V.late_switch_verdict({"context:30": cell(SPLIT, RECALL_OK), "context:33": cell(four, RECALL_OK),
                               "context:36": cell(SPLIT, RECALL_OK)})  # fmt: skip
    assert v["late_cells"] == ["context:30", "context:36"]
    other_set = V.late_switch_verdict({"context:30": cell(SPLIT, RECALL_OK), "bind_bridge:33": cell(MOVES, RECALL_OK)})
    assert other_set["verdict"] == "late switch holds at context:30"  # the sentence's cells do not bind the context's
    earlier = V.late_switch_verdict({"context:30": cell(MOVES, RECALL_OK), "context:36": cell(SPLIT, RECALL_OK)})
    assert earlier["late_cells"] == ["context:36"]  # only later cells count: moving before going quiet is a late switch


FORM = {"jspace": (0, 100), "not_jspace": (60, 100), "not_jspace_matched": (30, 100), "rand_sub": (0, 100)}
SIZE = {"jspace": (0, 100), "not_jspace": (60, 100), "not_jspace_matched": (3, 100), "rand_sub": (0, 100)}


def test_rest_size_verdict_branches():
    assert V.wilson(30, 100)[1] >= V.FORM_REST_LO and V.wilson(3, 100)[2] <= V.SIZE_REST_HI
    assert V.rest_size_verdict(cell(FORM, RECALL_OK)).startswith("H-form")
    assert V.rest_size_verdict(cell(SIZE, RECALL_OK)).startswith("H-size")
    loud = {**FORM, "jspace": (30, 100)}  # the lens part is not quiet: no H-form, and the shrunk rest moves
    assert V.rest_size_verdict(cell(loud, RECALL_OK)) == "inconclusive"
    middle = {**FORM, "not_jspace_matched": (10, 100)}  # 10%: lower bound 5.5% < 20%, upper bound 17% > 10%
    assert V.rest_size_verdict(cell(middle, RECALL_OK)) == "inconclusive"
    size_loud = {**SIZE, "jspace": (30, 100)}  # H-size does not need a quiet lens part
    assert V.rest_size_verdict(cell(size_loud, RECALL_OK)).startswith("H-size")
    assert V.rest_size_verdict(cell({**FORM, "not_jspace_matched": (0, 0)}, RECALL_OK)).startswith("not interpretable")


def fake_runs(tmp_path, monkeypatch, rates: list[tuple], plan: dict) -> tuple:
    """A map (rates: set, layer, transit, flips) and a parts run (plan: (family, set, layer) -> part -> switched of
    100 items) under tmp_path; returns the statement_positions and d1_verdict folders."""
    sp, out = tmp_path / "statement_positions", tmp_path / "d1_verdict"
    monkeypatch.setattr(V, "SP", sp)
    (sp / "M").mkdir(parents=True)
    rows_map = [{"family": "PP", "set": s, "layer": la, "transit": tr, "cf": {"flips": [f, f - 0.05, f + 0.03]}}
                for s, la, tr, f in rates]  # fmt: skip
    (sp / "M" / "summary.json").write_text(json.dumps({"rates": rows_map}))
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
    return sp, out


def hits(d: dict, full: int) -> dict:
    return {"full": full, **{p: k for p, (k, _) in d.items()}}


def test_late_switch_run_and_figure(tmp_path, monkeypatch):
    rates = [("context", 24, True, 0.99), ("context", 33, True, 0.98), ("bind_bridge", 36, False, 0.35)]
    plan = {("PP", "context", 33): hits(SPLIT, 100), ("PM", "context", 33): hits(RECALL_OK, 97),
            ("PP", "bind_bridge", 36): hits(MOVES, 30), ("PM", "bind_bridge", 36): hits(RECALL_OK, 80),
            ("PP", "context", 24): hits(MOVES, 99), ("PM", "context", 24): hits(RECALL_OK, 97)}  # fmt: skip
    _, out = fake_runs(tmp_path, monkeypatch, rates, plan)
    a = argparse.Namespace(map="M", parts="P", lookup="PP", recall="PM", tasks_set=None, out=str(out), rule="late-switch",
                           cells=["bind_bridge:36", "context:33"], reference=["context:24"], decisive=None, figures=False)  # fmt: skip
    assert V.by_cell(a) == 0
    (d,) = out.glob("P_*")
    v = json.loads((d / "verdict.json").read_text())
    assert v["rule"] == "late-switch" and v["decisive_cells"] == ["context:33"]  # bind_bridge:36 not in transit
    assert v["verdict"] == "late switch holds at context:33"
    assert v["cells"]["bind_bridge:36"]["role"] == "not in transit" and v["cells"]["context:24"]["role"] == "reference"
    assert v["cells"]["context:33"]["lookup"]["not_jspace"][0] == 0.5
    assert v["cells"]["context:33"]["recall"]["jspace"][3] == 100
    assert v["cells"]["context:33"]["lookup"]["jspace_null"][3] == 100
    assert v["cells"]["context:33"]["lookup"]["not_jspace_matched"][3] == 0  # a run without it: reported as missing
    assert v["cells"]["context:33"]["median_share"] == {"jspace": 0.3, "rand_sub": 0.3, "rand_omp": 0.05}
    assert "late switch holds" in (d / "verdict.md").read_text()
    a.figures = True
    assert V.rule_figures(a) == 0
    assert list(d.glob("analysis-*-figures/late_switch.png"))


def test_rest_size_run_and_figure(tmp_path, monkeypatch):
    rates = [("context", 32, True, 0.99), ("bind_bridge", 32, False, 0.4), ("context", 36, True, 0.97)]
    recall = {**RECALL_OK, "not_jspace_matched": (25, 100)}
    plan = {("PP", "context", 32): hits(FORM, 100), ("PM", "context", 32): hits(recall, 97),
            ("PP", "bind_bridge", 32): hits(SIZE, 40), ("PM", "bind_bridge", 32): hits(recall, 90),
            ("PP", "context", 36): hits(SIZE, 97), ("PM", "context", 36): hits(recall, 95)}  # fmt: skip
    _, out = fake_runs(tmp_path, monkeypatch, rates, plan)
    a = argparse.Namespace(map="M", parts="P", lookup="PP", recall="PM", tasks_set=None, out=str(out), rule="rest-size",
                           cells=["context:32", "bind_bridge:32", "context:36"], reference=[], decisive="context:32",
                           figures=False)  # fmt: skip
    assert V.by_cell(a) == 0
    (d,) = out.glob("P_*")
    v = json.loads((d / "verdict.json").read_text())
    assert v["rule"] == "rest-size" and v["decisive_cells"] == ["context:32"]
    assert v["verdict"].startswith("H-form")  # decided at the decisive cell; context:36 says H-size, reported only
    assert v["cells"]["context:36"]["verdict"].startswith("H-size") and v["cells"]["context:36"]["role"] == "reported"
    assert v["cells"]["bind_bridge:32"]["role"] == "not in transit"
    assert v["cells"]["context:32"]["recall"]["not_jspace_matched"][3] == 100  # recalls reported for the shrunk rest
    a.figures = True
    assert V.rule_figures(a) == 0
    assert list(d.glob("analysis-*-figures/rest_size.png"))
    out2 = tmp_path / "d1_verdict_2"  # a decisive cell the map does not have in transit: not interpretable
    b = argparse.Namespace(**{**vars(a), "out": str(out2), "decisive": "bind_bridge:32", "figures": False})
    assert V.by_cell(b) == 0
    (d2,) = out2.glob("P_*")
    assert json.loads((d2 / "verdict.json").read_text())["verdict"].startswith("not interpretable")
