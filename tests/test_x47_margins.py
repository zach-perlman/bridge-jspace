"""Batch 47, test 47.0b (scripts/x47_margins.py): the unedited margins of switchers vs stayers on planted data."""

from __future__ import annotations

import math

import numpy as np
import pytest

from scripts import x0_necessity as X
from scripts import x47_margins as M


def planted(n_ent: int = 20, per: int = 5, shift: float = 2.0, seed: int = 1):
    """Items in n_ent entities; every other item switches; stayers' margins are switchers' + shift (plus noise)."""
    rng = np.random.default_rng(seed)
    margin, switched, ents = [], [], []
    for e in range(n_ent):
        for i in range(per):
            sw = (e + i) % 2
            margin.append(3.0 + rng.normal(0, 0.3) + (0 if sw else shift))
            switched.append(sw)
            ents.append(f"e{e}")
    return margin, switched, ents


def test_planted_difference_is_recovered_with_an_interval_around_it():
    c = M.margin_cell(*planted(shift=2.0), n_boot=2000)
    assert c["n_switch"] + c["n_stay"] == c["n"] == 100
    assert c["diff"][0] == pytest.approx(2.0, abs=0.2)
    assert c["diff"][1] < c["diff"][0] < c["diff"][2]
    assert c["diff"][1] > 1.5  # far from 0
    assert c["auc"] > 0.99  # every stayer above every switcher


def test_no_difference_gives_an_interval_over_zero_and_auc_near_half():
    c = M.margin_cell(*planted(shift=0.0), n_boot=2000)
    assert c["diff"][1] < 0 < c["diff"][2]
    assert 0.35 < c["auc"] < 0.65


def test_sign_stayers_minus_switchers():
    c = M.margin_cell(*planted(shift=-1.0), n_boot=500)
    assert c["diff"][0] < 0 and c["mean_stay"][0] < c["mean_switch"][0]
    assert c["auc"] < 0.05


def test_auc_ties_count_half():
    assert M.auc(np.array([1.0, 1.0]), np.array([1.0])) == pytest.approx(0.5)
    assert M.auc(np.array([2.0]), np.array([1.0, 3.0])) == pytest.approx(0.5)
    assert math.isnan(M.auc(np.array([]), np.array([1.0])))


def test_an_empty_group_is_nan_not_an_error():
    c = M.margin_cell([1.0, 2.0, 3.0], [1, 1, 1], ["a", "b", "c"], n_boot=100)
    assert c["n_stay"] == 0 and math.isnan(c["mean_stay"][0]) and math.isnan(c["diff"][0])
    assert not math.isnan(c["mean_switch"][0])


def test_one_entity_with_many_items_widens_the_interval():
    """Cluster bootstrap: the same items as one entity per item vs a few big entities -> wider interval."""
    margin, switched, _ = planted(shift=1.0)
    narrow = M.margin_cell(margin, switched, [f"i{i}" for i in range(len(margin))], n_boot=2000)
    # stayers' margins vary by cluster: 4 clusters carry the signal, so resampling them is noisier
    margin2 = [m + (2.0 * (i // 25) if not s else 0.0) for i, (m, s) in enumerate(zip(margin, switched, strict=True))]
    wide = M.margin_cell(margin2, switched, [f"c{i // 25}" for i in range(len(margin))], n_boot=2000)
    assert (wide["diff"][2] - wide["diff"][1]) > (narrow["diff"][2] - narrow["diff"][1])


def test_items_reads_the_unedited_margin_as_minus_ld_and_the_whole_switch():
    base = {"rendering": "chat", "layer": 12, "reader": X.LOOKUP, "entity": "frog"}
    rows = [
        {**base, "scene": "s1", "arm": "none", "ld": -4.5, "p_org": 0.9, "p_alt": 0.01, "switched": 0},
        {**base, "scene": "s1", "arm": "whole", "ld": 4.0, "p_org": 0.01, "p_alt": 0.9, "switched": 1},
        {**base, "scene": "s2", "arm": "none", "ld": -2.0, "p_org": 0.7, "p_alt": 0.1, "switched": 0},
        {**base, "scene": "s2", "arm": "whole", "ld": -1.0, "p_org": 0.6, "p_alt": 0.2, "switched": 0},
        {**base, "scene": "s2", "layer": 14, "arm": "none", "ld": -9.0, "p_org": 0.7, "p_alt": 0.1, "switched": 0},
        {**base, "scene": "s2", "reader": X.RECALL, "arm": "none", "ld": -9.0, "p_org": 0.7, "p_alt": 0.1,
         "switched": 0},
    ]  # fmt: skip
    its = M.items(rows, 12, X.LOOKUP)
    assert [(i["scene"], i["margin"], i["switched"]) for i in its] == [("s1", 4.5, 1), ("s2", 2.0, 0)]
    with pytest.raises(AssertionError):
        M.items([*rows, rows[0]], 12, X.LOOKUP)
    assert M.none_stable(rows, X.LOOKUP) == pytest.approx(7.0)
