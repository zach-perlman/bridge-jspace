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
