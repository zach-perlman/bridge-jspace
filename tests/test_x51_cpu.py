"""Batch 51 CPU items (scripts/x51_cpu.py, scripts/x51_fit.py): each computation on planted rows. No model, no stored
results."""

import math

import numpy as np
import pytest

from scripts import x51_cpu as C

NB = 200  # bootstrap resamples in tests


# ---- 1. Z1 ----------------------------------------------------------------------------------------------------------


def _z1_rows(n: int, k_sw: dict[str, int], m_sw: dict[str, int], stratum: str = "fact-first", set_="jsuite_v2_test_chat",
             relation: str = "cities", start: int = 0) -> list[dict]:  # fmt: skip
    """n passages; per reader and arm the first k passages switch."""
    rows = []
    for i in range(start, start + n):
        for w, sw in (("K", k_sw), ("M", m_sw)):
            for a in C.Z1_ARMS:
                rows.append({"set": set_, "scene": f"s{i}", "reader": w, "arm": a, "stratum": stratum,
                             "relation": relation, "layer": 12, "switched": int(i - start < sw.get(a, 0))})  # fmt: skip
    return rows


def test_z1_cell_planted_split():
    # lookup: removing J++ costs nothing beyond random; recall: J++ removal kills every switch, random keeps all
    rows = _z1_rows(20, {"whole": 10, "no_jpp": 10, "no_jpp_rand": 10}, {"whole": 20, "no_jpp": 0, "no_jpp_rand": 20})
    c = C.z1_cell(rows, NB)
    assert c["n"] == 20
    assert c["K"]["share"]["whole"][0] == pytest.approx(0.5) and c["K"]["share"]["none"][0] == 0
    assert c["K"]["excess"][0] == pytest.approx(0.0)
    assert c["M"]["Jdep"][0] == pytest.approx(1.0) and c["M"]["Rdep"][0] == pytest.approx(0.0)
    assert c["M"]["excess"][0] == pytest.approx(1.0)
    assert c["gap"][0] == pytest.approx(1.0)
    assert c["gap"][1] <= c["gap"][0] <= c["gap"][2]


def test_z1_cell_no_switch_is_undefined():
    c = C.z1_cell(_z1_rows(5, {}, {"whole": 5, "no_jpp": 5, "no_jpp_rand": 5}), NB)
    assert math.isnan(c["K"]["excess"][0]) and math.isnan(c["gap"][0])
    assert C.fmt(c["K"]["excess"]) == "-"


def test_z1_groups_and_strata(tmp_path):
    rows = (_z1_rows(6, {"whole": 6}, {"whole": 6}, "fact-first")
            + _z1_rows(4, {"whole": 0}, {"whole": 4}, "fact-after", "jsuite_v2nb_test_chat", start=6))  # fmt: skip
    groups = C.z1_groups(rows)
    assert set(groups) == {"all", "v2", "v2nb"} and len(groups["v2nb"]) == 4 * 2 * len(C.Z1_ARMS)
    first = C.z1_cell([r for r in rows if r["stratum"] == "fact-first"], NB)
    after = C.z1_cell([r for r in rows if r["stratum"] == "fact-after"], NB)
    assert first["K"]["share"]["whole"][0] == 1.0 and after["K"]["share"]["whole"][0] == 0.0
    assert C.z1_groups(_z1_rows(3, {}, {})).keys() == {"all"}


def test_z1_is_sealed(monkeypatch):
    from scripts import x50_zach as Z

    monkeypatch.setattr(Z, "dan_answer", lambda q, rev="HEAD": "")
    with pytest.raises(AssertionError, match="sealed"):
        C.item_z1(NB)


def test_ci3_and_strip():
    assert all(math.isnan(v) for v in C.ci3(math.nan, np.zeros(3)))
    assert C.strip({"a": 1, "_d": np.zeros(2), "b": [{"_x": 1, "y": 2}]}) == {"a": 1, "b": [{"y": 2}]}
