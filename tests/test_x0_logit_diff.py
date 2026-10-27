"""Batch 39's logit-difference split (scripts/x0_logit_diff.py) reads planted effects."""

from scripts import x0_logit_diff as L


def _model(n=90, lk_keep=1.0, rc_keep=0.0, switched=1):
    """Two readers; whole shift 2 + (i % 3); without J++ the shift keeps lk_keep / rc_keep of it; without random all."""
    model = {}
    for w, keep in (("PP", lk_keep), ("PM", rc_keep)):
        by = {}
        for i in range(n):
            whole = 2.0 + i % 3
            by[f"s{i}"] = {"entity": f"e{i % 15}",
                           "ld": {"none": -1.0, "whole": -1.0 + whole, "no_part": -1.0 + keep * whole,
                                  "no_rand": -1.0 + whole},
                           "sw": {"whole": switched, "no_part": int(keep > 0.5) * switched, "no_rand": switched}}  # fmt: skip
        model[w] = by
    return model


def test_ld_gap_reads_a_planted_split():
    g = L.gap_of(_model(), 200)
    assert abs(g["recall"]["extra"][0] - 1.0) < 1e-9 and abs(g["lookup"]["extra"][0]) < 1e-9
    assert abs(g["gap"][0] - 1.0) < 1e-9 and g["n_common"] == 90


def test_terciles_count_and_answer():
    t = L.terciles(_model(n=300), 100)
    assert t["counted"] == 3 and t["answer"] == "yes"
    assert all(abs(r["gap"] - 1.0) < 1e-9 for r in t["terciles"])


def test_terciles_cant_tell_without_switches():
    t = L.terciles(_model(n=120, switched=0), 100)
    assert t["counted"] == 0 and t["answer"] == "can't tell"
