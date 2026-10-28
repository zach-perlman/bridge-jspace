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


# ---- 2. route split -------------------------------------------------------------------------------------------------


def _route_rows(spec: list[tuple[str, str, str]], part: str = "no_jpp", rand: str = "no_jpp_rand") -> list[dict]:
    """One scene per (whole route, route without the part, route without its random twin); entity per scene."""
    rows = []
    for i, routes in enumerate(spec):
        for a, rt in zip(("whole", part, rand), routes, strict=True):
            rows.append({"scene": f"C2-{i}", "entity": f"e{i % 7}", "arm": a, "route": rt, "reader": "PP",
                         "condition": "C2"})  # fmt: skip
    return rows


def test_route_split_planted():
    # 10 identity items: J++ removal sends 8 to 'original', random keeps all -> extra loss 0.8
    # 5 position items: both keep 4 of 5 -> extra loss 0; 3 'other' items ignored
    spec = ([("identity", "original", "identity")] * 8 + [("identity", "identity", "identity")] * 2
            + [("position", "position", "position")] * 4 + [("position", "other", "other")]
            + [("other", "other", "other")] * 3)  # fmt: skip
    c = C.route_split(_route_rows(spec), "no_jpp", "no_jpp_rand", NB)
    assert c["n"] == 18 and c["whole_routes"] == {"identity": 10, "position": 5, "other": 3}
    assert c["identity"]["n"] == 10 and c["position"]["n"] == 5
    assert c["identity"]["keep_without_part"][0] == pytest.approx(0.2)
    assert c["identity"]["keep_without_rand"][0] == pytest.approx(1.0)
    assert c["identity"]["extra_loss"][0] == pytest.approx(0.8)
    assert c["position"]["extra_loss"][0] == pytest.approx(0.0)
    assert c["identity_minus_position"][0] == pytest.approx(0.8)
    assert c["identity"]["without_part_goes_to"] == {"original": 8, "identity": 2}
    lo, hi = c["identity"]["extra_loss"][1:]
    assert lo <= 0.8 <= hi


def test_route_split_missing_route_and_other_arms():
    spec = [("identity", "identity", "original")] * 4
    c = C.route_split(_route_rows(spec, "no_J", "no_J_rand"), "no_J", "no_J_rand", NB)
    assert c["identity"]["extra_loss"][0] == pytest.approx(-1.0)
    assert c["position"]["n"] == 0 and math.isnan(c["position"]["extra_loss"][0])
    assert math.isnan(c["identity_minus_position"][0])
    assert C.route_split([], "no_J", "no_J_rand", NB) == {"n": 0}


def test_ci3_and_strip():
    assert all(math.isnan(v) for v in C.ci3(math.nan, np.zeros(3)))
    assert C.strip({"a": 1, "_d": np.zeros(2), "b": [{"_x": 1, "y": 2}]}) == {"a": 1, "b": [{"y": 2}]}
