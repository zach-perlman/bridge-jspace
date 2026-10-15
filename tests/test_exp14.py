"""exp14's pure helpers (no model)."""

import json
import math

import pytest
import torch

import scripts.exp14_cue_answer_swaps.experiment as exp14


def test_diff_cosine_and_share_in_span():
    e = torch.eye(4)
    bridge = torch.stack([e[0], e[1]])
    answer = torch.stack([e[0], e[2]])  # shares the first atom: difference vectors (1,-1,0,0) and (1,0,-1,0)
    assert exp14.diff_cosine(bridge, answer) == pytest.approx(0.5)
    delta = torch.tensor([[1.0, -1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]])  # a bridge-swap edit at one position
    assert exp14.share_in_span(delta, bridge) == pytest.approx(1.0)
    assert exp14.share_in_span(delta, torch.stack([e[2], e[3]])) == pytest.approx(0.0)
    assert exp14.share_in_span(delta, answer) == pytest.approx(math.sqrt(0.5))  # its e0 half lies in the answer span
    assert math.isnan(exp14.share_in_span(torch.zeros(2, 4), bridge))


def _o(name, kind, flip, null=False, positions="cue", band="24-40", lens="jpp", kept=None):
    kept = (not flip) if kept is None else kept
    return {"name": name, "lens": lens, "positions": positions, "band": band, "kind": kind, "null": null,
            "flip": flip, "kept_clean": kept, "edit_ratio": 0.02, "layers_skipped": []}  # fmt: skip


def test_rates_and_paired_difference_use_questions_with_both_swaps():
    outcomes = [
        _o("a", "bridge", True), _o("a", "answer", False),
        _o("b", "bridge", True), _o("b", "answer", True),
        _o("c", "bridge", False),  # c has no single-token answer: no answer swap
        _o("a", "bridge", False, null=True),
    ]  # fmt: skip
    r = {(x["kind"], x["null"]): x for x in exp14.rates(outcomes)}
    assert r[("bridge", False)]["n"] == 3 and r[("bridge", False)]["flip"][0] == pytest.approx(2 / 3)
    assert r[("answer", False)]["n"] == 2 and r[("bridge", True)]["n"] == 1
    (d,) = exp14.bridge_minus_answer(outcomes, n_boot=200, seed=0)
    assert d["n"] == 2 and d["bridge"] == 1.0 and d["answer"] == 0.5 and d["diff"][0] == pytest.approx(0.5)


def test_positive_control_takes_the_best_last_token_band():
    outcomes = [_o("a", "answer", f, positions="last", band=b) for b, f in (("24-40", False), ("40-56", True))]
    outcomes += [_o("b", "answer", True, positions="last", band="40-56"), _o("b", "answer", False, positions="last")]
    pc = exp14.positive_control(outcomes, min_flip=0.3)["jpp"]
    assert pc["band"] == "40-56" and pc["flip"][0] == 1.0 and pc["works"]


def test_eligibility_check(tmp_path):
    labels = tmp_path / "labels.csv"
    labels.write_text("name,status\na,eligible\nb,clean_wrong\nc,eligible\n")
    assert exp14.eligibility_check(["a", "c"], labels, None)["same"]
    check = exp14.eligibility_check(["a"], labels, 2)  # a smoke run that looked at the first two only
    assert check["same"] and check["n_part_b"] == 1


def test_replication_check_reads_part_b_raw_jlens(tmp_path, monkeypatch):
    run = tmp_path / "exp02_swaps" / "ref"
    run.mkdir(parents=True)
    theirs = [
        {"name": "a", "band": "24-40", "condition": "raw_jlens", "null": False, "flip": True},
        {"name": "a", "band": "24-40", "condition": "raw_jlens", "null": True, "flip": False},
        {"name": "a", "band": "24-40", "condition": "jpart", "null": False, "flip": False},
    ]
    (run / "outcomes.jsonl").write_text("\n".join(json.dumps(o) for o in theirs))
    monkeypatch.setattr(exp14, "RESULTS_DIR", tmp_path)
    ours = [_o("a", "bridge", True), _o("a", "bridge", False, null=True), _o("a", "answer", False)]
    rep = exp14.replication_check(ours, {"jpp": {"cue/24-40": "ref"}})["jpp cue/24-40"]
    assert (rep["agree"], rep["of"], rep["flip_ours"], rep["flip_part_b"]) == (2, 2, 1.0, 1.0)
