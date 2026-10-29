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
