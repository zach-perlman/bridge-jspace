"""Batch 52, Dan's morning queue (29 Oct) item 1: Lightning's below-gate exploratory runs. Each script's --below-gate path
reads Lightning's clean-design source below its gate (x45b_binding.FRESH_BELOW) and labels its verdict 'below gate
(exploratory)'; the default paths (FRESH_RUN, the design's verdicts and batch counts) are unchanged."""

import pytest

LT = "nemotron-3.5-lightning"


def test_45q_default_path_unchanged_and_below_gate_lookup():
    from scripts import x45b_binding as B

    assert set(B.FRESH_RUN) == {"qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b"} == set(B.Q_MODELS)
    assert B.fresh_of("qwen3.5-9b") == B.FRESH_RUN["qwen3.5-9b"] and B.fresh_of(LT, below=True) == "nem35l_x52_fresh"
    with pytest.raises(KeyError):
        B.fresh_of(LT)
    with pytest.raises(AssertionError, match="below gate"):
        B.fresh_of("qwen3.5-9b", below=True)
    assert "below gate (exploratory)" in B.BELOW_GATE and "0.751" in B.BELOW_GATE


def test_45q_below_gate_verdict(tmp_path, monkeypatch):
    """q-verdict --below-gate: Lightning's run alone, the rule per model, no batch count, no seal, x52_45q_below-<UTC>/."""
    from scripts import x45b_binding as B

    monkeypatch.setattr(B, "RESULTS", tmp_path)
    monkeypatch.setattr(B, "unsealed", lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    out = B.stage_q_verdict(["nem35l_x52_45q_below"], 10, below=True)
    text = (out / "x45q.md").read_text()
    assert out.name.startswith("x52_45q_below-") and B.BELOW_GATE in text and "no batch count" in text


def test_ladder_gate_refuses_a_failed_source_unless_below_gate(tmp_path, monkeypatch):
    """49.2 reads the 45m source's gate: a failed gate stops the run unless --below-gate (BELOW); the verdict below
    gate reads the given run alone, writes the below-gate note, x52_ladder_below-<UTC>/."""
    import json

    from scripts import x49_ladder as LD

    src = tmp_path / "src"
    src.mkdir()
    (src / "gate.json").write_text(json.dumps({"gate": {"chat": {"pass": False, "org_accuracy": {"PM": 0.75}}}}))
    assert LD.BELOW is False
    with pytest.raises(AssertionError, match="did not pass"):
        LD.gate_of(src)
    monkeypatch.setattr(LD, "BELOW", True)
    assert LD.gate_of(src)["pass"] is False
    monkeypatch.setattr(LD, "RESULTS", tmp_path)
    out = LD.stage_verdict({LT: "nem35l_x52_ladder_below"}, n_boot=10, coverage=True)
    text = (out / "x49_2.md").read_text()
    assert out.name.startswith("x52_ladder_below-") and "below gate (exploratory)" in text and "Dan:" not in text


def test_45p_below_gate_verdict(tmp_path, monkeypatch):
    from scripts import x45p as P

    monkeypatch.setattr(P, "RESULTS", tmp_path)
    monkeypatch.setattr(P, "dan_answer", lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    out = P.stage_verdict(["nem35l_x52_45p_below"], 10, below=True)
    text = (out / "x45p.md").read_text()
    assert out.name.startswith("x52_45p_below-") and "below gate (exploratory)" in text and ", Dan:" not in text
    assert "qwen3.5-9b" not in text
    with pytest.raises(AssertionError, match="45p runs on"):
        P.stage_verdict([P.RUNS["qwen3.5-9b"]], 10, below=True)


def test_bind_and_route2_below_gate(tmp_path, monkeypatch):
    """48.3 and 48.5: the 45m source extended by Lightning's below-gate run only with --below-gate; the below-gate
    verdicts read Lightning alone, no seal, x52_bind_below-<UTC>/ and x52_route2_below-<UTC>/."""
    from scripts import x45b_binding as B
    from scripts import x48_bind as BD
    from scripts import x48_route2 as R2

    assert BD.BELOW is False and BD.sources() is BD.SOURCES and LT not in BD.SOURCES["45m"]
    monkeypatch.setattr(BD, "BELOW", True)
    assert BD.sources()["45m"][LT] == B.FRESH_BELOW[LT] and BD.sources()["main"] is B.MAIN_RUN
    monkeypatch.setattr(BD, "RESULTS", tmp_path)
    monkeypatch.setattr(BD, "dan_answer", lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    monkeypatch.setattr(
        BD, "model_result", lambda r, n: {"run": r, "target": LT, "status": "pending", "holds": False, "why": "x"}
    )
    out = BD.stage_verdict(["nem35l_x52_bind_below"], 10, coverage=True)
    assert out.name.startswith("x52_bind_below-") and "below gate (exploratory)" in (out / "x48_bind.md").read_text()
    monkeypatch.setattr(R2, "RESULTS", tmp_path)
    monkeypatch.setattr(R2, "dan_answer", lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    out = R2.stage_verdict(["nem35l_x52_route2_below"], 10, below=True)
    text = (out / f"{R2.EXP}.md").read_text()
    assert out.name.startswith("x52_route2_below-") and "below gate (exploratory)" in text and ", Dan:" not in text


def test_cue_and_answer_cue_below_gate(tmp_path, monkeypatch):
    """47.3 below its own gate: a failed gate reads 'not tested' unless the run was made --below-gate (its manifest
    says so); 51.12's cue set below gate reads the below-gate 47.3 run and writes its own below-gate runs."""
    import json

    from scripts import x47_cue as CUE
    from scripts import x51_answer as AN

    assert CUE.BELOW is False and AN.BELOW is False
    run = tmp_path / "r"
    run.mkdir()
    (run / "cues.json").write_text(json.dumps({"status": "ok"}))
    gate = {"pass": False, "chosen": 300, "org_read_accuracy": {"PP": 0.72}, "eligible": 301}
    (run / "gate.json").write_text(json.dumps(gate))
    (run / "manifest.json").write_text(json.dumps({"model": {"target": LT}, "layer": 14}))
    monkeypatch.setattr(CUE, "RESULTS", tmp_path)
    assert CUE.model_result("r", 10)["status"] == "not tested"
    (run / "manifest.json").write_text(json.dumps({"model": {"target": LT}, "layer": 14, "below_gate": CUE.BELOW_GATE}))
    got = CUE.model_result("r", 10)
    assert got["status"] == "pending" and got.get("below_gate") == CUE.BELOW_GATE  # no outcomes yet, but read below
    assert AN.source_of("cue", LT).name == "nem35l_x52_cue"  # default unchanged
    monkeypatch.setattr(AN, "BELOW", True)
    assert AN.source_of("cue", LT).name == CUE.BELOW_RUNS[LT]
    assert AN.all_runs(("cue",), coverage=True) == [("cue", LT, "nem35l_x52_cue_answer_below")]


def test_natural_below_gate_verdict_carries_the_note(tmp_path, monkeypatch):
    """x5_natural --below-gate: the run's manifest carries BELOW_GATE and the verdict prints it first."""
    import json

    from scripts import x0_necessity as X
    from scripts import x5_natural as N

    run = tmp_path / "r"
    run.mkdir()
    (run / "manifest.json").write_text(
        json.dumps({"model": {"target": LT}, "layer": 14, "rule": "r", "below_gate": N.BELOW_GATE})
    )
    rows = [
        {
            "scene": f"s{i}",
            "entity": f"e{i % 3}",
            "relation": "countries",
            "half": "A",
            "reader": w,
            "arm": a,
            "dict": "jpp",
            "switched": int(a == "whole" or (w == X.RECALL and a == "no_rand")),
            "lure_alt": 0,
        }
        for i in range(6)
        for w in X.READERS
        for a in ("whole", "no_part", "no_rand")
    ]
    X.write_jsonl(run / "outcomes.jsonl", rows)
    monkeypatch.setattr(N, "RESULTS", tmp_path)
    out = N.stage_verdict("r", 10)
    assert N.BELOW_GATE in (out / "verdict.md").read_text()


def test_report49_design_from_lightning(tmp_path, monkeypatch):
    """49.6 on Lightning with the 9B / 27B spec's design: its run and its 47.10 reference looked up; the verdict
    --design-from reads it alone, no seal, x52_report49-<UTC>/; the design's verdict unchanged."""
    from scripts import x49_report as R

    assert (
        R.DESIGN_RUNS == {LT: "nem35l_x52_report49"} and LT not in R.MODELS and R.REFERENCE[LT] == "nem35l_x52_report"
    )
    monkeypatch.setattr(R, "RESULTS", tmp_path)
    monkeypatch.setattr(R, "dan_answer", lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    out = R.stage_verdict(["nem35l_x52_report49"], 10, design_from=True)
    text = (out / "x49_6.md").read_text()
    assert out.name.startswith("x52_report49-") and "design from the 9B / 27B spec" in text and ", Dan:" not in text


def test_depth51_design_from_lightning(tmp_path, monkeypatch):
    """51.5 on Lightning with the 9B / 27B spec's design: 47.8's Lightning grid, Z1's Lightning run, ours from
    Lightning's 47.8 sweep (L22 / L22); verdict --design-from alone, no seal, x52_depth51-<UTC>/."""
    from scripts import x47_anatomy as A
    from scripts import x51_depth as D

    assert D.LAYERS[LT] == A.LAYERS[LT] and D.REFERENCE[LT] == {"lookup": 22, "recall": 22}
    assert D.z1_run(LT).name == "nem35l_x52_z1" and D.z1_run("qwen3.5-9b").name == "qwen35_9b_x50_z1"
    assert LT not in D.TARGETS and LT not in D.RUNS
    ref = D.reference(LT)
    assert (ref["lookup"], ref["recall"]) == (22, 22)  # the constant is the function's value on the stored sweep
    monkeypatch.setattr(D, "RESULTS", tmp_path)
    monkeypatch.setattr(D, "unsealed", lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    out = D.stage_verdict(["nem35l_x52_depth51"], 10, design_from=True)
    text = (out / "verdict.md").read_text()
    assert out.name.startswith("x52_depth51-") and "design from the 9B / 27B spec" in text and ", Dan:" not in text


def test_probe49_below_gate(tmp_path, monkeypatch):
    """49.3: the 45m source is Lightning's below-gate run only with --below-gate; the verdict below gate reads the
    below-gate run alone, x52_probe49_below-<UTC>/."""
    from scripts import x49_probe as P

    assert P.BELOW is False and LT not in P.COVERAGE_RUNS
    monkeypatch.setattr(P, "BELOW", True)
    monkeypatch.setattr(P, "RESULTS", tmp_path)
    monkeypatch.setattr(P, "dan_answer", lambda: (_ for _ in ()).throw(AssertionError("the seal guard ran")))
    out = P.stage_verdict([P.BELOW_RUNS[LT]], 10, coverage=True)
    assert out.name.startswith("x52_probe49_below-") and "below gate (exploratory)" in (out / "x49_3.md").read_text()
    with pytest.raises(AssertionError, match=r"49\.3 runs on"):
        P.stage_verdict([P.COVERAGE_RUNS["qwen3.6-27b"]], 10, coverage=True)


def test_d1_and_474_clean_below_gate(tmp_path, monkeypatch):
    """D1 and 47.4: the clean design's source is Lightning's below-gate run only below gate; the coverage verdicts
    below gate write the note, x52_depthmap_below-<UTC>/ and x52_cumulative_below-<UTC>/."""
    from scripts import x45b_binding as B
    from scripts import x47_cumulative as C
    from scripts import x47_depthmap as DM

    assert C.BELOW is False and DM.BELOW is False and C.sources() is C.SOURCES and LT not in C.SOURCES["clean"]
    assert C.sources(True)["clean"][LT] == B.FRESH_BELOW[LT] and C.sources(True)["main"] is C.SOURCES["main"]
    monkeypatch.setattr(C, "BELOW", True)
    monkeypatch.setattr(C, "RESULTS", tmp_path)
    out = C.stage_verdict(["nem35l_x52_cumulative_clean_below"], 10, coverage=True)
    assert out.name.startswith("x52_cumulative_below-") and "below gate (exploratory)" in (out / "x47_4.md").read_text()
    monkeypatch.setattr(DM, "BELOW", True)
    monkeypatch.setattr(DM, "RESULTS", tmp_path)
    monkeypatch.setattr(DM, "model_result", lambda r, n_boot: {"run": r, "target": LT, "status": "pending", "why": "x"})
    out = DM.stage_verdict(["nem35l_x52_depthmap_clean_below"], 10, coverage=True)
    assert out.name.startswith("x52_depthmap_below-")
    assert "below gate (exploratory)" in "".join(p.read_text() for p in out.glob("*.md"))
