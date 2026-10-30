"""scripts/story_b47b.py: each batch-47 README figure drawn from a PLANTED verdict folder (the verdict stage itself run on
each script's test fixtures: tests/test_x47_*.py's planted runs; no real result is read), and 47.0's on a planted
verbal.json. Per figure: the PNG and SVG are written, the default title reads the verdict's own outcome, every plotted
number is recorded with the verdict file as its source, and the drawn text keeps docs/glossary.md's words and no
retired term (tests/test_readme_build.banned, scripts/check_figure_terms.retired). CPU, no model."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from matplotlib.figure import Figure
from matplotlib.text import Text

from scripts import story_b47b as B
from scripts import story_style as S
from scripts import x0_necessity as X
from scripts import x47_cumulative as C
from scripts import x47_depthmap as D
from scripts import x47_edges as E
from scripts import x47_value as V
from scripts.check_figure_terms import retired
from tests import test_x47_cumulative as TC
from tests import test_x47_depthmap as TD
from tests import test_x47_edges as TE
from tests.test_readme_build import banned

LK, RC = X.LOOKUP, X.RECALL


# ---- planted verdict folders (each script's own verdict stage on its tests' planted runs) ---------------------------


def planted_d1(root: Path, mp) -> Path:
    """x47_depthmap's verdict on test_x47_depthmap's planted maps (9B and Muse; the 27B pending): the lookup's bridge
    word hot to layer 8 and the recall's to 16 in locker-first scenes."""
    mp.setattr(D, "RESULTS", root)
    mp.setattr(D, "dan_answer", lambda rev="HEAD": "planted")
    TD.write_planted(root, "r9", "qwen3.5-9b")
    TD.write_planted(root, "rm", "muse-glimmer-30b")
    return D.stage_verdict(["r9", "rm"], n_boot=100)


def planted_47_4(root: Path, mp) -> Path:
    """x47_cumulative's verdict on test_x47_cumulative's planted runs (9B, 27B; Muse pending): in the main test's
    locker-first items the change at L switches 20%, the bridge word before L adds 40%, the pick sentence 10%."""
    mp.setattr(C, "RESULTS", root)
    mp.setattr(C, "dan_answer", lambda rev="HEAD": "planted")
    TC.write_planted(root, "r9", "qwen3.5-9b")
    TC.write_planted(root, "r27", "qwen3.6-27b")
    return C.stage_verdict(["r9", "r27"], n_boot=100)


def planted_47_6(root: Path, mp) -> Path:
    """x47_edges' verdict on test_x47_edges' planted (b) rows: on Muse the block removes position answers and keeps the
    rest (formation holds), on the 9B position stays at 30% (it does not)."""
    mp.setattr(E, "RESULTS", root)
    mp.setattr(E, "dan_answer", lambda rev="HEAD": "planted")
    TE.write_b(
        root, "muse30_x47_6_b", "muse-glimmer-30b", TE.b_rows(60, {"position": 0.0, "identity": 0.5, "recall": 0.9}), 26
    )
    TE.write_b(
        root, "qwen35_9b_x47_6_b", "qwen3.5-9b", TE.b_rows(60, {"position": 0.3, "identity": 0.5, "recall": 0.9}), 12
    )
    return E.stage_verdict(n_boot=100)


def _value_rows(n: int, spec: dict[str, dict[str, tuple[float, float]]], fmt: str = "prose") -> list[dict]:
    """Lookup rows: per rendering and arm the (value, position) shares, the rest identity; C2 and C0 alike."""
    rows = []
    for i in range(n):
        for r, arms in spec.items():
            for a, (v, p) in arms.items():
                route = "value" if i / n < v else "position" if i / n < v + p else "identity"
                for cond in ("C2", "C0"):
                    rows.append({"scene": f"{cond}-{fmt}-{i:04d}", "condition": cond, "entity": f"e{i % 20}", "reader": LK,
                                 "rendering": r, "arm": a, "route": route, "switched": 0, "format": fmt})  # fmt: skip
    return rows


def plant_value_ab(root: Path, run: str, target: str, value: dict[str, float], probe_qf: bool, ql_arms: bool) -> None:
    """A 47.7 (a) or (b) run folder (test_x47_value's planted run, per model): the whole change's value share per
    rendering, the arms question-first (and question-last for (b)); the digit decodable question-first iff probe_qf."""
    src = root / run
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12}))
    (src / "plan.json").write_text("{}")
    (src / "gate.json").write_text(
        json.dumps({"gate": {c: {"pass": True, "org_read_accuracy": {}} for c in ("C2", "C0")}})
    )
    (src / "c0_check.json").write_text(json.dumps({"qf": {"ok": True}}))

    def arms(v: float) -> dict[str, tuple[float, float]]:
        return {
            "whole": (v, 0.4),
            "no_jpp": (0.0, 0.4),
            "no_jpp_rand": (v, 0.4),
            "no_alf": (v, 0.0),
            "no_alf_rand": (v, 0.4),
        }

    spec = {"qf": arms(value["qf"]), "ql": arms(value["ql"]) if ql_arms else {"whole": (value["ql"], 0.5)}}
    X.write_jsonl(src / "outcomes.jsonl", _value_rows(100, spec))
    rng = np.random.default_rng(1)
    items, h, rends, readout = [], [], [], []
    for r in ("ql", "qf"):
        for i in range(100):
            ans = str(1 + i % 9)
            items.append({"scene": f"C2-{i:04d}", "condition": "C2", "rendering": r, "entity": f"e{i % 20}", "answer": ans,
                          "slot": i % 3, "context": f"ctx {i}", "format": "prose"})  # fmt: skip
            v = rng.standard_normal(16)
            if r == "qf" and probe_qf:
                v[int(ans)] += 6.0
            h.append(v)
            rends.append(r)
            readout.append({"scene": f"C2-{i:04d}", "condition": "C2", "rendering": r, "entity": f"e{i % 20}", "answer": ans,
                            "rank": 3, "top": "1", "n_candidates": 10})  # fmt: skip
    np.savez_compressed(src / "states.npz", h=np.stack(h).astype(np.float16), scene=np.array([it["scene"] for it in items]),
                        rendering=np.array(rends))  # fmt: skip
    X.write_jsonl(src / "items.jsonl", items)
    X.write_jsonl(src / "readout.jsonl", readout)


def plant_value_c(root: Path, run: str, target: str, value: dict[str, float], refit: bool) -> None:
    """A 47.7 (c) run folder: per format the whole change's value share, question-last; the refit-pointer arms iff
    refit (the 27B has none)."""
    src = root / run
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": 12}))
    (src / "plan.json").write_text("{}")
    (src / "gate.json").write_text(
        json.dumps({"gate": {f: {"pass": True, "org_read_accuracy": {}} for f in V.FORMATS}})
    )
    rows = []
    for f, v in value.items():
        arms = {
            "whole": (v, 0.3),
            "no_jpp": (v, 0.3),
            "no_jpp_rand": (v, 0.3),
            "no_alf": (v, 0.3),
            "no_alf_rand": (v, 0.3),
        }
        if refit:
            arms |= {"no_pcf": (v, 0.0), "no_pcf_rand": (v, 0.3)}
        rows += [r for r in _value_rows(60, {"ql": arms}, f) if r["condition"] == "C2"]
    X.write_jsonl(src / "outcomes.jsonl", rows)


def planted_47_7(root: Path, mp) -> Path:
    """x47_value's three verdicts on planted runs: (a) the 9B prefetches (value 30% question-first, the probe reads the
    digit), the 27B and Muse keep the address; (c) value 0-3% in every format but Muse's JSON (10%); (b) the 9B and Muse,
    no value question-last. Returns (a)'s folder; (c)'s and (b)'s are its siblings."""
    mp.setattr(V, "RESULTS", root)
    mp.setattr(V, "dan_answer", lambda: "planted")
    mp.setattr(V, "example_lines", lambda run: [])
    runs = V.RUNS
    for t, (qf, probe) in {
        "qwen3.5-9b": (0.3, True),
        "qwen3.6-27b": (0.0, False),
        "muse-glimmer-30b": (0.02, False),
    }.items():
        plant_value_ab(root, runs["a"][t], t, {"qf": qf, "ql": 0.0}, probe, ql_arms=False)
    for t, json_v in {"qwen3.5-9b": 0.0, "qwen3.6-27b": 0.03, "muse-glimmer-30b": 0.1}.items():
        plant_value_c(root, runs["c"][t], t, {"prose": 0.0, "json": json_v, "table": 0.02}, refit=t != "qwen3.6-27b")
    for t in runs["b"]:
        plant_value_ab(root, runs["b"][t], t, {"qf": 0.05, "ql": 0.0}, False, ql_arms=True)
    out = V.stage_verdict("a", list(runs["a"].values()), n_boot=100)
    V.stage_verdict("c", list(runs["c"].values()), n_boot=100)
    V.stage_verdict("b", list(runs["b"].values()), n_boot=100)
    return out


def _against(median: float, cut: float, mid: float) -> dict:
    return {"median": median, "null_cut": cut, "null_median_of_medians": mid, "beyond": False, "null_pct": 5.0,
            "case_share_beyond": [0.05, 0.02, 0.1]}  # fmt: skip


def planted_47_0(root: Path) -> Path:
    """A planted verbal.json in x47_verbal's shape (summary stage's keys), three models."""
    models = {}
    for i, t in enumerate(("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")):
        models[t] = {"target": t, "layer": 12, "n_cases": 200, "n_items": 100, "n_identity_cases": 200,
                     "a": {"write|best_ordinal": _against(30 + i, 20, 35), "identity|alt_name": _against(20, 2000, 4000)},
                     "b": {"all|25": {"pointer": 0.05, "random_mean": 0.045, "random_p95": 0.06, "identity_mean": 0.2,
                                      "ratio": 1.1}},
                     "c": {"write": _against(0.1, 0.2, 0.08), "identity": _against(0.5 + i, 0.2, 0.08)},
                     "reading": {"label": "not verbalizable"}}  # fmt: skip
    out = root / "summary-planted"
    out.mkdir(parents=True)
    (out / "verbal.json").write_text(json.dumps({"models": models, "overall": "not verbalizable"}))
    return out


# ---- the figures ----------------------------------------------------------------------------------------------------


@pytest.fixture
def drawn(monkeypatch, tmp_path):
    """Every text each saved figure draws, by file stem, the title first (the figure is still written);
    story_style.ROWS emptied."""
    texts: dict[str, list[str]] = {}
    save = Figure.savefig

    def grab(fig, fname, *args, **kwargs):
        texts[Path(str(fname)).stem] = [fig.get_suptitle()] + [t.get_text() for t in fig.findobj(Text)
                                                                if t.get_text().strip()]  # fmt: skip
        return save(fig, fname, *args, **kwargs)

    monkeypatch.setattr(Figure, "savefig", grab)
    monkeypatch.setattr(S, "ROWS", [])
    return texts


def check(name: str, out: Path, drawn: dict[str, list[str]], source: str) -> list[str]:
    """The files exist, every recorded row of the figure cites the verdict file, and the drawn words are canonical."""
    assert (out / f"{name}.png").exists()  # PNG only (Dan, 30 Oct)
    rows = [r for r in S.ROWS if r["figure"] == name]
    assert rows and all(r["source"].endswith(source) for r in rows), {r["source"] for r in rows}
    flat = [(name, t) for t in drawn[name]]
    assert not banned(flat), banned(flat)
    assert not retired(flat), retired(flat)
    return drawn[name]


def said(texts: list[str]) -> str:
    """The drawn texts as one line (the subtitle wraps anywhere)."""
    return " ".join(" ".join(texts).split())


def test_d1_map(tmp_path, monkeypatch, drawn):
    v = planted_d1(tmp_path / "v", monkeypatch)
    name = B.build_d1(v, "fig16", out_dir=tmp_path / "out")
    texts = check(name, tmp_path / "out", drawn, "depth.json")
    assert texts[0] == "The lookup reads the bridge word to layer 8, the recall to layer 16"
    rows = {r["quantity"]: r["value"] for r in S.ROWS}
    assert rows["D1 clean, locker-first, lookup: gbridge@8 switched"] == 1.0
    assert rows["D1 clean, locker-first, lookup: gbridge@12 switched"] == 0.0
    assert rows["D2 clean, locker-first, lookup: l_R"] == 24 and rows["D2 clean, locker-first, recall: l_R"] == 12
    assert "bridge word, every layer ≥ l" in texts
    B.build_d1(v, "fig16b", "A title from the caller", target="qwen3.6-27b", out_dir=tmp_path / "out")  # pending
    assert drawn["fig16b"][0] == "A title from the caller" and "not run" in drawn["fig16b"]


@pytest.mark.parametrize("coverage", [False, True])
def test_47_4_cumulative(tmp_path, monkeypatch, drawn, coverage):
    v = planted_47_4(tmp_path / "v", monkeypatch)
    kw = {} if coverage else {"coverage": None}  # default: the batch-52 coverage file (27B, Lightning)
    name = B.build_47_4(v, "fig17", out_dir=tmp_path / "out", **kw)
    texts = check(name, tmp_path / "out", drawn, "x47_4.json")
    # planted 9B and 27B; with the coverage file Lightning's main test is drawn too (hollow)
    assert (
        texts[0]
        == f"Lookups the change misses sit mostly at the bridge word before L (2 of {3 if coverage else 2} models)"
    )
    rows = {(r["model"], r["quantity"]): r["value"] for r in S.ROWS}
    assert rows[("qwen3.5-9b", "47.4 main, locker-first, lookup: a")] == pytest.approx(0.2)
    assert rows[("qwen3.5-9b", "47.4 main, locker-first, lookup: outside")] == pytest.approx(0.3)
    assert "not run" in texts  # Muse
    # four model slots, in order, always (Dan's figures brief, 29 Oct 10:00)
    slots = list(dict.fromkeys(t.split(" ")[0] for t in texts if t.endswith((" lookup", " recall"))))
    assert slots == ["9B", "27B", "Muse", "Lightning"], slots
    lt_rows = [r for r in S.ROWS if r["model"] == "nemotron-3.5-lightning"]
    if coverage:  # Lightning's clean design has no run past its gate: a grey slot
        assert lt_rows and "not tested: gate" in texts
    else:  # no coverage file: Lightning keeps its slot, grey
        assert not lt_rows and texts.count("not run") >= 2 and "Lightning: not run" in said(texts)
    assert not any("BUG" in t for t in texts)


def test_47_6_formation(tmp_path, monkeypatch, drawn):
    v = planted_47_6(tmp_path / "v", monkeypatch)
    name = B.build_47_6(v, "fig18", out_dir=tmp_path / "out")
    texts = check(name, tmp_path / "out", drawn, "verdict.json")
    assert texts[0] == "Position answers survive when the pick sentence cannot read the lockers"
    assert "Holds on: 9B no, Muse yes." in said(texts)
    rows = {(r["model"], r["quantity"]): r["value"] for r in S.ROWS}
    assert rows[("qwen3.5-9b", f"47.6 (b) {B.DECISIVE_B}: lookup position share")] == pytest.approx(0.3)
    assert rows[("muse-glimmer-30b", "47.6 (b): the formation rule holds")] == 1


def test_47_7_value(tmp_path, monkeypatch, drawn):
    v = planted_47_7(tmp_path / "v", monkeypatch)
    name = B.build_47_7(v, "fig19", out_dir=tmp_path / "out")
    texts = check(name, tmp_path / "out", drawn, ".json")
    assert texts[0] == "Even with the question first, the lookup keeps the address"
    assert "(a) address regardless; (c) does not generalize; (b) never the value for a word value too: yes" in said(
        texts
    )
    srcs = {r["source"].rsplit("/", 1)[-1] for r in S.ROWS}
    assert srcs == {"x47_7a.json", "x47_7c.json", "x47_7b.json"}
    rows = {(r["model"], r["quantity"]): r["value"] for r in S.ROWS}
    assert rows[("qwen3.5-9b", "47.7(a) qf: value share (whole change)")] == pytest.approx(0.3)
    assert rows[("muse-glimmer-30b", "47.7(c) json: value share (whole change)")] == pytest.approx(0.1)
    assert "not run" in texts  # (b) has no 27B run


def test_47_0_verbal(tmp_path, drawn, monkeypatch):
    v = planted_47_0(tmp_path / "v")
    name = B.build_47_0(v, "fig20", out_dir=tmp_path / "out")
    texts = check(name, tmp_path / "out", drawn, "verbal.json")
    assert texts[0] == "Read through the J++ lens, the pointer looks like a random direction"
    assert "200 cases per model" in said(texts)
    assert len([r for r in S.ROWS if r["figure"] == "fig20"]) == 3 * 7


def test_tests_table_names_each_build():
    assert set(B.TESTS) == {"D1", "47.4", "47.6", "47.7", "47.0"}
    for script, f, fig in B.TESTS.values():
        assert (S.REPO / script).exists() and callable(f) and fig.startswith("fig")
