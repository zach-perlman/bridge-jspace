"""Batch 51, test 51.6 (scripts/x51_lightning.py): the dev / test split, step 1's layer pick on planted rates, both
steps' reads on a tiny fake causal model (CPU), the sealed run stage (a layer passes; no layer passes; the gate fails),
step 2's rule and the verdict on planted runs, the verify-pack view, and the seal. No real model."""

import json
from types import SimpleNamespace

import pytest
import torch

from scripts import statement_positions as SP
from scripts import x0_necessity as X
from scripts import x51_lightning as L6
from tests.test_x49_gain import FakeLens, FakeModel

LK, RC = X.LOOKUP, X.RECALL
N_LAYERS = 52
LAST = max(L6.LAYERS)


class Lens51(FakeLens):
    source_layers = tuple(range(LAST + 1))


def _case(i: int) -> dict:
    """A main-test case as build_cases writes it: both readers' prompts agree through the bridge word (position 4); S
    changes only the bridge word here."""
    org = [1 + i % 7, 2, 3, 4, 20 + i % 5, 6]
    alt = [*org[:4], 40 + i % 5, 6]
    rd = {"id": f"PP-{i}", "question": "Which locker belongs to Iris's pick?", "answer": "5", "cf_answer": "3",
          "ids": {"org": [*org, 7], "alt": [*alt, 7]}, "tok_A": 5, "tok_b": 3}  # fmt: skip
    rc = {**rd, "id": f"PM-{i}", "question": "How many legs?", "ids": {"org": [*org, 8, 9], "alt": [*alt, 8, 9]}}
    return {"scene": f"P2-L0-{i:04d}", "rendering": "chat", "domain": "animals", "bridge": f"e{i % 4}", "cf_bridge": "bee",
            "pos": 4, "space": [11], "readers": {LK: rd, RC: rc}}  # fmt: skip


# ---- the split and the layer pick ----------------------------------------------------------------------------------


def test_split_is_seeded_disjoint_and_in_scene_order():
    cases = [_case(i) for i in range(300)]
    dev, test = L6.split_scenes(cases)
    assert len(dev) == 60 and len(test) == 200
    ids = [c["scene"] for c in cases]
    d, t = [c["scene"] for c in dev], [c["scene"] for c in test]
    assert not set(d) & set(t) and d == sorted(d) and t == sorted(t)
    assert t == [s for s in ids if s not in set(d)][:200]  # the first 200 not in dev
    assert L6.split_scenes(cases)[0] == dev  # seeded
    assert [c["scene"] for c in L6.split_scenes(cases, seed=1)[0]] != d
    small_dev, small_test = L6.split_scenes(cases[:70])
    assert len(small_dev) == 60 and len(small_test) == 10
    assert L6.split_scenes([]) == ([], [])


def _rates(**by_layer):
    return {int(k[1:]): {LK: v[0], RC: v[1]} for k, v in by_layer.items()}


def test_pick_layer_is_the_earliest_where_both_switch():
    rates = _rates(L2=(0.2, 0.9), L4=(0.3, 0.3), L6=(0.8, 0.9), L8=(0.1, 0.2))
    assert L6.pick_layer(rates) == 4  # inclusive at the bar
    assert L6.passing_layers(rates) == [4, 6]
    assert L6.pick_layer(_rates(L2=(0.29, 1.0), L4=(1.0, 0.2999))) is None  # never both
    assert L6.pick_layer({}) is None
    assert L6.pick_layer({2: {LK: 1.0}}) is None  # a reader missing


def test_step1_rates_from_rows():
    rows = [{"arm": "whole", "layer": la, "reader": w, "switched": s} for la, w, s in
            [(2, LK, 1), (2, LK, 0), (2, RC, 1), (2, RC, 1), (4, LK, 0), (4, RC, 0)]]  # fmt: skip
    rows.append({"arm": "none", "layer": None, "reader": LK, "switched": 1})
    assert L6.step1_rates(rows) == {2: {LK: 0.5, RC: 1.0}, 4: {LK: 0.0, RC: 0.0}}


# ---- the reads on a fake model -------------------------------------------------------------------------------------


def test_step1_writes_the_whole_change_at_each_layer():
    model = FakeModel(n_layers=N_LAYERS)
    cases = [_case(i) for i in range(3)]
    layers = (2, 10, 50)
    delta = L6.deltas(model, cases, layers)
    assert delta.shape == (3, 3, 48)
    rows = L6.step1_reads(model, cases, layers, delta, torch.arange(10))
    assert len(rows) == 3 * 2 * (1 + len(layers))
    assert {(r["arm"], r["layer"]) for r in rows} == {("none", None), *(("whole", la) for la in layers)}
    assert all(r["switched"] == int(r["top"] == 3) for r in rows)
    prompt, edits = model.calls[0]
    c = cases[0]
    assert prompt == c["readers"][LK]["ids"]["org"] + c["space"] and edits[0] == {}
    assert [list(e) for e in edits[1:]] == [[la] for la in layers]
    # under the whole change at l, O's bridge state at l is S's
    ids = c["readers"][LK]["ids"]
    for li, la in enumerate(layers):
        h_s = model.run(torch.tensor([ids["alt"]]), record=(la,))[1][la][c["pos"]]
        h_e = model.run(torch.tensor([ids["org"]]), edits=edits[1 + li], record=(la,))[1][la][c["pos"]]
        assert torch.allclose(h_e, h_s, atol=1e-4)


def test_step2_arms_are_x0s():
    model = FakeModel(n_layers=N_LAYERS)
    cases = [_case(i) for i in range(12)]
    la = 26
    rows, shares, greedy = L6.step2_reads(model, Lens51(), cases, la, torch.arange(10))
    assert len(rows) == 12 * 2 * 4 and len(shares) == 12 and len(greedy) == X.K_EXAMPLES * 2 * 4
    assert [r["arm"] for r in rows[:4]] == list(L6.ARMS2)
    assert {(r["dict"], r["k"], r["omp"]) for r in rows if r["arm"] in ("no_part", "no_rand")} == {
        ("jpp", 25, "signed")
    }
    # the edits: whole = Δ, no_part = Δ - X0's J++ part, no_rand = Δ - X0's random part of its share
    c = cases[0]
    ids = c["readers"][LK]["ids"]
    h = {v: model.run(torch.tensor([ids[v]]), record=(la,))[1][la][c["pos"]] for v in ("org", "alt")}
    delta = (h["alt"] - h["org"])[None]
    jdic = Lens51().vectors(la, torch.arange(100))
    part = X.fit(jdic, delta, 25, "signed")
    share = part.norm(dim=-1) ** 2 / delta.norm(dim=-1) ** 2
    rand = SP.random_subspace_part(delta, share, SP.random_basis(48, torch.Generator().manual_seed(888 + la)))
    edits = model.calls[0][1]  # case 0's lookup read (Δ comes from model.run, not generate_batch)
    assert edits[0] == {}
    assert torch.allclose(edits[1][la].delta, delta, atol=1e-5)
    assert torch.allclose(edits[2][la].delta, delta - part, atol=1e-4)
    assert torch.allclose(edits[3][la].delta, delta - rand, atol=1e-4)
    assert shares[0]["share"] == pytest.approx(float(share[0]), abs=1e-4)
    # X0's cells read these rows as its own
    cells = X.cells_of(rows, n_boot=50)
    assert set(cells) == {("chat", la, w, "jpp", 25, "signed") for w in X.READERS}


# ---- the run stage -------------------------------------------------------------------------------------------------


def _stage(monkeypatch, tmp_path, n: int = 30, gate_ok: bool = True, switch_min: float = 0.0):
    from bridge_jspace import lens as LN
    from bridge_jspace import model as M
    from bridge_jspace import pins

    cases = [_case(i) for i in range(n)]
    monkeypatch.setattr(M, "load_model", lambda: FakeModel(n_layers=N_LAYERS))
    monkeypatch.setattr(LN, "JLens", Lens51)
    monkeypatch.setattr(L6, "RESULTS", tmp_path / "x51")
    monkeypatch.setattr(L6, "TARGET", pins.TARGET)
    monkeypatch.setattr(L6, "preflight", lambda: None)
    monkeypatch.setattr(L6, "build", lambda tok: (cases, {"scenes": n, "cases": {"chat": n}, "dropped": {}}))
    monkeypatch.setattr(L6, "N_DEV", 6)
    monkeypatch.setattr(L6, "N_TEST", 12)
    monkeypatch.setattr(L6, "SWITCH_MIN", switch_min)
    monkeypatch.setattr(X, "N_MIN", 10)
    monkeypatch.setattr(X, "whitespace_mask", lambda model: None)
    monkeypatch.setattr(X, "digit_ids", lambda tok: list(range(10)))
    monkeypatch.setattr(X, "RENDERINGS", ("chat",))

    def competence(model, cs, digits, ws):
        return [{"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "right": True,
                 "read_right": gate_ok or w == LK, "cand_right": True} for c in cs for w in X.READERS
                for v in ("org", "alt")]  # fmt: skip

    monkeypatch.setattr(X, "competence", competence)
    return cases


def test_stage_run_end_to_end_sealed(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path)
    n_items = X.N_ITEMS
    out = L6.stage_run(f"{pins.RUN_PREFIX}x51_6_test", "test")
    assert n_items == X.N_ITEMS  # restored
    m = json.loads((out / "manifest.json").read_text())
    assert m["test"] == "51.6" and m["layers"] == list(L6.LAYERS) and "sealed" in m and "switches" in m
    assert m["question"].startswith("Q51.6") and m["lens"]["name"] == "jpp"
    gate = json.loads((out / "gate.json").read_text())
    assert gate["tested"] and gate["eligible"] == 30 and len(gate["dev"]) == 6 and len(gate["test"]) == 12
    assert not set(gate["dev"]) & set(gate["test"])
    s1 = json.loads((out / "step1.json").read_text())
    assert s1["layer"] == 2  # every layer passes a bar of 0: the earliest
    assert len(X.read_jsonl(out / "step1_outcomes.jsonl")) == 6 * 2 * (1 + len(L6.LAYERS))
    s2 = json.loads((out / "step2.json").read_text())
    assert s2 == {"status": "done", "layer": 2, "n": 12}
    rows2 = X.read_jsonl(out / "step2_outcomes.jsonl")
    assert len(rows2) == 12 * 2 * 4 and {r["scene"] for r in rows2} == set(gate["test"])
    assert not (set(p.name for p in out.iterdir()) & {"verdict.md", "verdict.json"})


def test_stage_run_stops_when_no_layer_passes(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, switch_min=1.01)
    out = L6.stage_run(f"{pins.RUN_PREFIX}x51_6_none", "test")
    assert json.loads((out / "step1.json").read_text())["layer"] is None
    assert json.loads((out / "step2.json").read_text()) == {"status": "no layer passes step 1", "label": L6.NO_LAYER}
    assert not (out / "step2_outcomes.jsonl").exists()


def test_stage_run_without_the_gate_reads_nothing(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, gate_ok=False)
    out = L6.stage_run(f"{pins.RUN_PREFIX}x51_6_gate", "test")
    gate = json.loads((out / "gate.json").read_text())
    assert gate["tested"] is False and gate["gate"]["pass"] is False and gate["dev"] == []
    assert json.loads((out / "step1.json").read_text())["status"] == "not tested"
    assert not (out / "step1_outcomes.jsonl").exists()


# ---- batch 52: the prerequisite (gate on 60 scenes, the layer by the published rule) -------------------------------


def test_prereq_layers_are_every_4th_with_lens_maps():
    assert L6.LAYERS4 == (2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50) and set(L6.LAYERS4) <= set(L6.LAYERS)
    assert L6.N_GATE == 60 and L6.PREREQ_RUN.startswith("nem35l_")


def test_gate_first_reads_the_first_n_scenes_only():
    cases = [_case(i) for i in range(10)]
    comp = [{"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "right": True,
             "read_right": not (w == RC and i < 3), "cand_right": True}
            for i, c in enumerate(cases) for w in X.READERS for v in ("org", "alt")]  # fmt: skip
    g = L6.gate_first(cases, comp, n=5)  # recall right on 2 of the first 5
    assert g["cases"] == 5 and g["org_accuracy"] == {LK: 1.0, RC: 0.4} and g["pass"] is False
    assert L6.gate_first(cases[3:], comp, n=5)["pass"] is True  # all right from scene 3 on
    assert L6.gate_first(cases[:4], comp[: 4 * 4], n=5)["pass"] is False  # fewer than n scenes


def test_stage_prereq_writes_the_layer_and_no_step_2(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, switch_min=0.0)
    monkeypatch.setattr(L6, "N_GATE", 10)
    out = L6.stage_prereq(f"{pins.RUN_PREFIX}x52_layer_test", "test", n_boot=50)
    m = json.loads((out / "manifest.json").read_text())
    assert m["batch"] == 52 and m["layers"] == list(L6.LAYERS4) and m["question"] == L6.NO_PREDICTION
    gate = json.loads((out / "gate.json").read_text())
    assert gate["gate60"]["pass"] and gate["gate60"]["cases"] == 10 and len(gate["dev"]) == 6
    rec = json.loads((out / "layer.json").read_text())
    assert rec["layer"] == 2 and rec["label"] == "L2" and rec["passing_layers"] == list(L6.LAYERS4)
    assert set(rec["rates_ci"]) == {str(la) for la in L6.LAYERS4} and rec["prediction"] == L6.NO_PREDICTION
    rows = X.read_jsonl(out / "step1_outcomes.jsonl")
    assert len(rows) == 6 * 2 * (1 + len(L6.LAYERS4)) and {r["scene"] for r in rows} == set(gate["dev"])
    names = {p.name for p in out.iterdir()}
    assert not names & {"step2_outcomes.jsonl", "step2.json", "verdict.md"} and "prereq.md" in names
    assert "**Layer: L2**" in (out / "prereq.md").read_text()


def test_stage_prereq_no_layer_and_failed_gate(tmp_path, monkeypatch):
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, switch_min=1.01)
    monkeypatch.setattr(L6, "N_GATE", 10)
    rec = json.loads((L6.stage_prereq(f"{pins.RUN_PREFIX}x52_none", "t", n_boot=20) / "layer.json").read_text())
    assert rec["layer"] is None and rec["label"] == L6.NO_LAYER and rec["status"] == "no layer passes"
    _stage(monkeypatch, tmp_path / "g", gate_ok=False)
    monkeypatch.setattr(L6, "N_GATE", 10)
    out = L6.stage_prereq(f"{pins.RUN_PREFIX}x52_gate", "t", n_boot=20)
    rec = json.loads((out / "layer.json").read_text())
    assert rec["layer"] is None and rec["status"] == "prerequisite failed" and "60 main-test" in rec["label"]
    assert not (out / "step1_outcomes.jsonl").exists()


def test_stage_prereq_main_gate_decides_with_the_60_scene_check_beside(tmp_path, monkeypatch):
    """r2: the first 10 scenes fail the recall (pre-check fails) while X0's all-scene gate passes: --gate main sweeps,
    the default stops."""
    from bridge_jspace import pins

    _stage(monkeypatch, tmp_path, switch_min=0.0)
    monkeypatch.setattr(L6, "N_GATE", 10)

    def competence(model, cs, digits, ws):
        return [{"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "right": True,
                 "read_right": not (w == RC and i < 3), "cand_right": True}
                for i, c in enumerate(cs) for w in X.READERS for v in ("org", "alt")]  # fmt: skip

    monkeypatch.setattr(X, "competence", competence)
    out = L6.stage_prereq(f"{pins.RUN_PREFIX}x52_main", "t", n_boot=20, gate_mode="main")
    gate = json.loads((out / "gate.json").read_text())
    assert gate["prereq_gate"] == "main" and gate["gate_passes"] and not gate["gate60"]["pass"]
    assert gate["gate"]["pass"] and gate["eligible"] == 27 and len(gate["dev"]) == 6
    assert not set(gate["dev"]) & {f"P2-L0-{i:04d}" for i in range(3)}  # the scenes the recall misses are not eligible
    rec = json.loads((out / "layer.json").read_text())
    assert rec["layer"] == 2 and rec["prereq_gate"] == "main" and rec["gate60_pass"] is False
    m = json.loads((out / "manifest.json").read_text())
    assert m["prereq_gate"]["mode"] == "main"
    assert "pre-check" in (out / "prereq.md").read_text()
    rec1 = json.loads((L6.stage_prereq(f"{pins.RUN_PREFIX}x52_60", "t", n_boot=20) / "layer.json").read_text())
    assert rec1["layer"] is None and rec1["status"] == "prerequisite failed"
    with pytest.raises(AssertionError, match="not one of"):
        L6.stage_prereq(f"{pins.RUN_PREFIX}x52_bad", "t", gate_mode="bad")


def test_committed_layer_refuses_until_committed(monkeypatch):
    def fake(code: int, text: str):
        return lambda *a, **k: SimpleNamespace(returncode=code, stdout=text)

    monkeypatch.setattr(L6.subprocess, "run", fake(128, ""))
    with pytest.raises(AssertionError, match="not committed"):
        L6.committed_layer()
    monkeypatch.setattr(L6.subprocess, "run", fake(0, json.dumps({"layer": None, "status": "no layer passes"})))
    with pytest.raises(AssertionError, match="cancelled"):
        L6.committed_layer()
    monkeypatch.setattr(L6.subprocess, "run", fake(0, json.dumps({"layer": 14})))
    assert L6.committed_layer() == 14


# ---- the rule and the verdict on planted runs ----------------------------------------------------------------------

SPLIT = {LK: {"whole": 0.5, "no_part": 0.5, "no_rand": 0.5}, RC: {"whole": 0.8, "no_part": 0.2, "no_rand": 0.8}}
FOLLOWS = {LK: {"whole": 0.5, "no_part": 0.3, "no_rand": 0.5}, RC: SPLIT[RC]}


def _rows2(rates: dict, n: int = 60, layer: int = 4) -> list[dict]:
    """Step-2 rows: n scenes over 10 bridge items; per reader and arm the first round(rate * n) scenes switch."""
    rows = []
    for i in range(n):
        for w in X.READERS:
            for a in L6.ARMS2:
                s = 0 if a == "none" else int(i < round(rates[w][a] * n))
                rows.append({"scene": f"P2-L0-{i:04d}", "entity": f"e{i % 10}", "domain": "animals", "rendering": "chat",
                             "step": 2, "layer": layer, "reader": w, "arm": a, "switched": s, "top": 3 if s else 5,
                             "role": "b" if s else "A", "p_org": 0.1, "p_alt": 0.9})  # fmt: skip
    return rows


def test_step2_rule_on_planted_rows():
    r = L6.step2_result(_rows2(SPLIT), n_boot=200)
    assert r["holds"] and r["n"] == 60 and r["x0_verdict"] == "confirmed"
    assert r["cells"]["lookup"]["excess"][0] == pytest.approx(0.0)
    assert r["cells"]["gap"][0] == pytest.approx(0.75)
    f = L6.step2_result(_rows2(FOLLOWS), n_boot=200)
    assert not f["holds"] and f["cells"]["lookup"]["excess"][0] == pytest.approx(0.4)
    # the bars are inclusive: lookup extra loss exactly 0.10 and a gap exactly 0.3
    at = {LK: {"whole": 0.5, "no_part": 0.45, "no_rand": 0.5}, RC: {"whole": 0.5, "no_part": 0.25, "no_rand": 0.45}}
    a = L6.step2_result(_rows2(at), n_boot=200)
    assert a["cells"]["lookup"]["excess"][0] == pytest.approx(0.1) and a["cells"]["gap"][0] == pytest.approx(0.3)
    assert a["holds"]


def write_planted(root, run: str, kind: str):
    """A planted 51.6 run: 'holds' / 'follows' (step 2 at L4), 'none' (no layer passes), 'gate' (not tested)."""

    src = root / run
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"model": {"target": L6.TARGET}}))
    cases = [{**_case(i), "bridge": f"e{i % 10}"} for i in range(60)]
    X.write_jsonl(src / "cases.jsonl", cases)
    g = {"cases": 516, "org_accuracy": {LK: 0.95, RC: 0.82}, "pass": kind != "gate", "eligible": 120}
    (src / "gate.json").write_text(json.dumps({"gate": g, "tested": kind != "gate", "eligible": 120,
                                              "dev": [c["scene"] for c in cases[:20]],
                                              "test": [c["scene"] for c in cases], "kernel_check": {"pass": True}}))  # fmt: skip
    if kind == "gate":
        (src / "step1.json").write_text(json.dumps({"status": "not tested", "why": "gate"}))
        return
    good = {2: (0.9, 0.2), 4: (0.4, 0.6), 6: (0.3, 0.3), 8: (0.1, 0.5)}
    bad = {2: (0.9, 0.2), 4: (0.2, 0.6)}
    rows1 = []
    for la, (lk, rc) in (bad if kind == "none" else good).items():
        for i in range(20):
            for w, rate in ((LK, lk), (RC, rc)):
                s = int(i < round(rate * 20))
                rows1.append({"scene": cases[i]["scene"], "entity": f"e{i % 10}", "step": 1, "reader": w, "arm": "whole",
                              "layer": la, "switched": s, "top": 3 if s else 5, "role": "b" if s else "A",
                              "p_org": 0.1, "p_alt": 0.9})  # fmt: skip
    X.write_jsonl(src / "step1_outcomes.jsonl", rows1)
    layer = None if kind == "none" else 4
    (src / "step1.json").write_text(json.dumps({"status": "done", "n": 20, "layer": layer}))
    if kind == "none":
        (src / "step2.json").write_text(json.dumps({"status": "no layer passes step 1", "label": L6.NO_LAYER}))
        return
    X.write_jsonl(src / "step2_outcomes.jsonl", _rows2(SPLIT if kind == "holds" else FOLLOWS))
    X.write_jsonl(src / "step2_shares.jsonl", [{"scene": c["scene"], "share": 0.1} for c in cases])
    X.write_jsonl(
        src / "step2_examples.jsonl", [{"scene": cases[0]["scene"], "reader": LK, "arm": "whole", "greedy": "3"}]
    )
    (src / "step2.json").write_text(json.dumps({"status": "done", "layer": 4, "n": 60}))


def test_run_name_takes_the_pins_live_prefix_and_layers_have_lens_maps():
    from bridge_jspace import pins

    assert pins.TARGETS[L6.TARGET]["run_prefix"] + "x51_6" == L6.RUN
    assert pins.TARGETS[L6.TARGET]["n_layers"] - 2 == LAST == 50 and len(L6.LAYERS) == 25


@pytest.mark.parametrize(("kind", "label", "i", "ii"), [
    ("holds", "L4: the split holds", "yes", "yes"),
    ("follows", "L4: the split does not hold", "yes", "no"),
    ("none", f"no layer passes step 1: {L6.NO_LAYER}", "no", None),
    ("gate", "not tested", None, None),
])  # fmt: skip
def test_verdict_on_planted_runs(tmp_path, monkeypatch, kind, label, i, ii):
    monkeypatch.setattr(L6, "RESULTS", tmp_path)
    monkeypatch.setattr(L6, "dan_answer", lambda rev="HEAD": "planted")
    write_planted(tmp_path, L6.RUN, kind)
    out = L6.stage_verdict(n_boot=200)
    blob = json.loads((out / "verdict.json").read_text())
    r = blob["result"]
    assert r["label"] == label and blob["dan"] == "planted"
    assert r.get("q51_6_i") == i and r.get("q51_6_ii") == ii
    md = (out / "verdict.md").read_text()
    assert f"**Label: {label}**" in md and "Dan: planted" in md
    if kind in ("holds", "follows"):
        assert r["passing_layers"] == [4, 6] and r["n_test"] == 60 and "| L4 |" in md and "Gap" in md
        rate, lo, hi = r["step1"]["4"][LK]  # JSON keys
        assert rate == pytest.approx(0.4) and lo <= 0.4 <= hi


def test_view_on_a_planted_run(tmp_path, monkeypatch):
    monkeypatch.setattr(L6, "RESULTS", tmp_path)
    monkeypatch.setattr(L6, "dan_answer", lambda rev="HEAD": "planted")
    write_planted(tmp_path, L6.RUN, "holds")
    out = L6.stage_view(decode=lambda ids: "".join(f"<{int(t)}>" for t in ids))
    md = (out / "view.md").read_text()
    assert md.count("```") == 2 * 2 * L6.N_PROMPTS and "⟦<2" in md  # the bridge token (20-24) marked
    for a in L6.ARMS2:
        assert f"## Step 2: arm {a}, 10 random rows" in md
    assert md.count("| P2-L0-") >= 10 * (1 + len(L6.ARMS2))


# ---- the seal ------------------------------------------------------------------------------------------------------


def test_sealed_until_dans_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(L6, "RESULTS", tmp_path)
    monkeypatch.setattr(L6, "dan_answer", lambda rev="HEAD": "")
    write_planted(tmp_path, L6.RUN, "holds")
    for stage in (L6.stage_verdict, L6.stage_view):
        with pytest.raises(AssertionError, match="sealed"):
            stage()
    assert sorted(p.name for p in tmp_path.iterdir()) == [L6.RUN]


def test_dan_answer_reads_only_the_q51_6_block(monkeypatch):
    def fake_git(text: str):
        return lambda *a, **k: SimpleNamespace(stdout=text)

    blocks = ("**Q51.5** x\n\nDan: yes\n\n**Q51.6** (51.6, optional) Lightning, the main test.\n- (i) A layer passes\n"
              "- (ii) If yes, the split\n\n{}\n\n**Q51.7** (51.7) Z1\n\nDan: (a)\n")  # fmt: skip
    monkeypatch.setattr(L6.subprocess, "run", fake_git(blocks.format("Dan:")))
    assert L6.dan_answer() == ""
    monkeypatch.setattr(L6.subprocess, "run", fake_git(blocks.format("Dan: (i) 70%; (ii) 55%")))
    assert L6.dan_answer() == "(i) 70%; (ii) 55%"
    monkeypatch.setattr(L6.subprocess, "run", fake_git(blocks.format("Dan (Lightning): (i) 70%\n- (ii) 55%")))
    assert L6.dan_answer() == "(i) 70%\n- (ii) 55%"


def test_the_committed_predictions_file_has_the_q51_6_block():
    text = L6.subprocess.run(["git", "show", f"HEAD:{L6.PREDICTIONS}"], cwd=L6.pins.REPO_ROOT, capture_output=True,
                             text=True, check=False).stdout  # fmt: skip
    if not text:
        pytest.skip("the predictions file is not in this checkout's HEAD")
    assert f"**{L6.QUESTION}**" in text and isinstance(L6.dan_answer(), str)
