"""Toy tests (CPU) for the attention-sink variant (docs/breadth/prereg_sink_1021.md) and the sink verdict rule."""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace.ablate import LensDictionary, RowSettings, removal_edit
from scripts.ablate_v2 import top_k
from scripts.sink_decision import verdict


def test_nosink_leaves_position_zero_and_massive_positions():
    g = torch.Generator().manual_seed(0)
    wg = torch.randn(40, 8, generator=g)
    h = torch.randn(1, 6, 8, generator=g)
    h[0, 3] *= 100.0  # a massive-norm position
    dic = LensDictionary(wg, torch.eye(8))
    plain = removal_edit("top", dic, [RowSettings()], k=2)(h.clone())
    nosink = removal_edit("top", dic, [RowSettings()], k=2, skip_sinks=True)
    out = nosink(h.clone())
    assert torch.equal(out[0, 0], h[0, 0]) and torch.equal(out[0, 3], h[0, 3])  # sinks unedited
    assert torch.allclose(out[0, [1, 2, 4, 5]], plain[0, [1, 2, 4, 5]])  # every other position as before
    assert nosink.sinks == [2, 6]


def test_condition_names():
    assert top_k("paper10_nosink") == 10 and top_k("paper10_nosink_rot") == 10 and top_k("unembed10_nosink") == 10
    assert top_k("top5_nosink_rot") == 5 and top_k("top5_rot") == 5 and top_k("omp25") is None


def _t(acc_pp, acc_mp, acc_pm, acc_mm, rot=1.0):
    k = {
        w: {"acc": a, "unedited": 1.0, "n": 100}
        for w, a in zip(("PP", "MP", "PM", "MM"), (acc_pp, acc_mp, acc_pm, acc_mm), strict=True)
    }
    kr = {w: {"acc": rot, "unedited": 1.0, "n": 100} for w in ("PP", "MP", "PM", "MM")}
    return {"paper10_nosink": k, "paper10_nosink_rot": kr}


def test_verdicts():
    base = {b: _t(0.2, 0.2, 0.1, 0.1) for b in ("L30-38", "L40-48", "L48-56")}
    assert verdict(base)[0] == "NOT ARTIFACT"
    assert verdict({**base, "L40-48": _t(0.95, 0.9, 0.5, 0.4)})[0] == "ARTIFACT"
    assert verdict({**base, "L40-48": _t(0.95, 0.9, 0.5, 0.4, rot=0.85)})[0] == "MIXED"  # control too weak
    assert verdict({**base, "L40-48": _t(0.95, 0.9, 0.9, 0.9)})[0] == "MIXED"  # lookups back but no gap
