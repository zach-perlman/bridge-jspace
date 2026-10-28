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


# ---- 3. the recall under the address swap ---------------------------------------------------------------------------

LEGS = {"frog": 4, "goose": 2, "spider": 8, "snake": 0}
CTX = "The locker of the frog is 5. The locker of the goose is 3. The locker of the spider is 7."


def _x8_rows(top_by_k: dict[int, int], kind: str = "write", s: float = 1, scene: str = "C2-1", entity: str = "frog",
             look: str = "target") -> list[dict]:  # fmt: skip
    """O's answer is the frog's legs (4); the token id is the digit itself (decode = str)."""
    rows = []
    for k, top in top_by_k.items():
        rows.append({"scene": scene, "entity": entity, "reader": "PM", "kind": kind, "j": 0, "k": k, "s": s,
                     "top": top, "changed": int(top != 4)})  # fmt: skip
        rows.append({"scene": scene, "entity": entity, "reader": "PP", "kind": kind, "j": 0, "k": k, "s": s,
                     "top": 0, "class": look})  # fmt: skip
    return rows


def test_recall_units_planted():
    cases = {"C2-1": {"bridge": "frog", "context": CTX}}
    # k = 1 (goose, 2 legs): the recall names the goose; k = 2 (spider, 8): unchanged
    units = C.recall_units(_x8_rows({1: 2, 2: 4}), cases, LEGS, str)
    by_k = {u["k"]: u for u in units}
    assert by_k[1]["changed"] == 1 and by_k[1]["names_target"] == 1 and by_k[1]["informative"] == 1
    assert by_k[2]["changed"] == 0 and by_k[2]["names_target"] == 0 and by_k[2]["lookup_target"] == 1
    # a changed recall naming the third item is a change, not the target
    u = C.recall_units(_x8_rows({1: 8}), cases, LEGS, str)[0]
    assert u["changed"] == 1 and u["names_target"] == 0
    # the bridge must be the case's and sit at slot j
    with pytest.raises(AssertionError):
        C.recall_units(_x8_rows({1: 2}, entity="goose"), cases, LEGS, str)


def test_recall_informative_flag():
    cases = {"C2-1": {"bridge": "frog", "context": CTX.replace("goose", "snake")}}
    legs = {**LEGS, "snake": 4}  # the slot-1 item has as many legs as the frog
    u = C.recall_units(_x8_rows({1: 4}), cases, legs, str)[0]
    assert u["informative"] == 0 and u["changed"] == 0


def test_dose_cells_planted():
    units = []
    for i in range(10):
        for s, n_named in ((1, 2), (2, 5), (4, 9)):
            units.append({"entity": f"e{i % 4}", "kind": "write", "s": s, "changed": int(i < n_named + 1),
                          "names_target": int(i < n_named), "informative": int(i < 8), "lookup_target": 1})  # fmt: skip
        units.append({"entity": f"e{i % 4}", "kind": "random", "s": 1, "changed": 0, "names_target": 0,
                      "informative": 1, "lookup_target": 0})  # fmt: skip
    cells = {(c["kind"], c["s"]): c for c in C.dose_cells(units, NB)}
    assert set(cells) == {("write", 1), ("write", 2), ("write", 4), ("random", 1)}
    assert cells[("write", 2)]["all"]["names_target"][0] == pytest.approx(0.5)
    assert cells[("write", 2)]["all"]["changed"][0] == pytest.approx(0.6)
    assert cells[("write", 4)]["informative"]["n"] == 8
    assert cells[("write", 4)]["informative"]["names_target"][0] == pytest.approx(1.0)
    assert cells[("random", 1)]["all"]["changed"][0] == 0
    lo, hi = cells[("write", 2)]["all"]["names_target"][1:]
    assert lo <= 0.5 <= hi


# ---- 4. concatenation probe -----------------------------------------------------------------------------------------


def test_key_order_and_concat_states():
    trows = [{"row": 0, "key": "w:The"}, {"row": 0, "key": "item"}, {"row": 0, "key": "number"},
             {"row": 1, "key": "w:The"}, {"row": 1, "key": "w:the"}, {"row": 1, "key": "item"},
             {"row": 1, "key": "number"}]  # fmt: skip
    keys = C.key_order(trows)
    assert keys[0] == "w:The" and keys[-1] == "number" and set(keys) == {"w:The", "w:the", "item", "number"}
    th = np.arange(7 * 2, dtype=float).reshape(7, 2) + 1
    h = C.concat_states(trows, th, 2, keys)
    assert h.shape == (2, 8)
    col = {k: 2 * i for i, k in enumerate(keys)}
    assert list(h[0, col["item"] : col["item"] + 2]) == list(th[1])
    assert list(h[0, col["w:the"] : col["w:the"] + 2]) == [0, 0]  # the role row 0 lacks: zero
    assert list(h[1, col["w:the"] : col["w:the"] + 2]) == list(th[4])
    with pytest.raises(AssertionError, match="twice"):
        C.concat_states([*trows, {"row": 0, "key": "item"}], np.vstack([th, th[:1]]), 2, keys)


def _probe_res(i: float, ii: float, ci: float = 0.3, cii: float = 0.5) -> dict:
    return {"picker": {"after": {"accuracy": [i, i, i]}, "before": {"accuracy": [ci, ci, ci]}},
            "asked": {"after": {"accuracy": [ii, ii, ii]}, "before": {"accuracy": [cii, cii, cii]}}}  # fmt: skip


def test_concat_label_planted():
    assert C.concat_label(_probe_res(0.90, 0.5))["label"] == "person"
    assert C.concat_label(_probe_res(0.85, 0.5))["label"] == "person"  # at the bar counts
    assert C.concat_label(_probe_res(0.40, 0.90))["label"] == "flag"
    assert C.concat_label(_probe_res(0.60, 0.90))["label"] == "between"  # (ii) high but (i) above 0.5
    assert C.concat_label(_probe_res(0.30, 0.55))["label"] == "chance"
    assert C.concat_label(_probe_res(0.30, 0.65))["label"] == "between"
    bad = C.concat_label(_probe_res(0.90, 0.5, ci=0.6))
    assert bad["label"] == "uninterpretable" and bad["raw"] == "person" and not bad["control_ok"]
    assert C.concat_model_label({"6": {"label": "chance"}, "12": {"label": "person"}}) == "person"
    assert C.concat_model_label({"6": {"label": "chance"}, "12": {"label": "chance"}}) == "chance"
    assert C.concat_model_label({"6": {"label": "chance"}, "12": {"label": "between"}}) == "between"


def test_concat_probe_reads_a_planted_joint_code():
    """The picker is written half into the item token and half into the number token: the concatenation reads it
    in locker-after sentences; locker-first sentences carry noise only (the control at chance)."""
    from scripts import x49_probe as P

    rng = np.random.default_rng(0)
    names, d, rows, trows, states = ["Ann", "Bob", "Cy"], 6, [], [], []
    code = {n: rng.normal(size=d) * 3 for n in names}
    for i in range(240):
        st = "after" if i % 2 == 0 else "before"
        picker = names[i % 3]
        rows.append({"picker": picker, "names": names, "locker_item": f"it{i % 24}", "stratum": st, "group": st,
                     "asked": i % 4 < 2, "scene_items": []})  # fmt: skip
        for key in ("w:The", "item", "number"):
            x = rng.normal(size=d)
            if st == "after" and key != "w:The":
                x = x + code[picker] / 2
            trows.append({"row": i, "key": key})
            states.append(x)
    h = C.concat_states(trows, np.array(states), len(rows), C.key_order(trows))
    res = {p: P.probe_view(h, rows, p, 50) for p in C.CONCAT_PROBES}
    assert res["picker"]["after"]["accuracy"][0] >= 0.85
    assert res["picker"]["before"]["accuracy"][0] <= 1 / 3 + 0.15
    assert C.concat_label(res)["label"] == "person"


# ---- 5. the gain fit (scripts/x51_fit.py) ---------------------------------------------------------------------------

GAINS = (0.0, 0.5, 1.0, 1.5, 2.0)


def _gain_rows(a0: float, a: float, b: float, c: float, n_items: int, seed: int = 0) -> list[dict]:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_items):
        for al in GAINS:
            for be in GAINS:
                p = 1 / (1 + np.exp(-(a0 + a * al + b * be + c * al * be)))
                rows.append({"scene": f"s{i}", "entity": f"e{i % 40}", "reader": "PM", "arm": f"J({al:g},{be:g})",
                             "switched": int(rng.random() < p)})  # fmt: skip
        rows.append({"scene": f"s{i}", "entity": f"e{i % 40}", "reader": "PM", "arm": "R(2,0)", "switched": 1})
    return rows


def test_parse_arm_and_grid_counts():
    from scripts import x51_fit as F

    assert F.parse_arm("J(0.5,2)") == (0.5, 2.0) and F.parse_arm("J(0,0)") == (0.0, 0.0)
    assert F.parse_arm("R(2,0)") is None and F.parse_arm("J(0,2)-U") is None and F.parse_arm("J100(2,0)") is None
    g = F.grid_counts(_gain_rows(0, 1, 1, 0, 6))
    assert g["succ"].shape == (6, 25) and g["rows"] == 6 * 25 and g["trials"].sum() == 150
    assert list(g["alpha"][:5]) == [0.0] * 5 and list(g["beta"][:5]) == list(GAINS)


def test_fit_recovers_planted_coefficients():
    from scripts import x51_fit as F

    g = F.grid_counts(_gain_rows(-3.0, 0.5, 2.0, 0.0, 400))
    s, n = g["succ"].sum(0), g["trials"].sum(0)
    f = F.fit_gain(g["alpha"], g["beta"], s, n, interaction=False, intercept=True)
    assert f["converged"]
    assert f["a0"] == pytest.approx(-3.0, abs=0.25) and f["a"] == pytest.approx(0.5, abs=0.15)
    assert f["b"] == pytest.approx(2.0, abs=0.2) and f["b_over_a"] == pytest.approx(f["b"] / f["a"])
    assert float(f["predict"](0.0, 0.0)[0]) == pytest.approx(1 / (1 + np.exp(-f["a0"])))
    # as written (no intercept): P = 0.5 at the origin by construction
    f0 = F.fit_gain(g["alpha"], g["beta"], s, n, interaction=False, intercept=False)
    assert float(f0["predict"](0.0, 0.0)[0]) == pytest.approx(0.5) and "a0" not in f0
    assert not F.lr_test(g["alpha"], g["beta"], s, n, intercept=True)["c_needed"]


def test_lr_test_finds_a_planted_interaction():
    from scripts import x51_fit as F

    g = F.grid_counts(_gain_rows(-4.0, 0.2, 0.2, 2.0, 200))  # "together only": neither part alone switches
    lrt = F.lr_test(g["alpha"], g["beta"], g["succ"].sum(0), g["trials"].sum(0), intercept=True)
    assert lrt["c_needed"] and lrt["p"] < 1e-6 and lrt["df"] == 1
    f1 = F.fit_gain(g["alpha"], g["beta"], g["succ"].sum(0), g["trials"].sum(0), interaction=True, intercept=True)
    assert f1["c"] == pytest.approx(2.0, abs=0.4)


def test_separated_data_do_not_converge():
    from scripts import x51_fit as F

    al = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    be = np.zeros(5)
    f = F.fit_gain(al, be, np.array([0, 0, 10, 10, 10]), np.full(5, 10), interaction=False, intercept=True)
    assert not f["converged"]


def test_gain_fit_bootstrap_intervals():
    from scripts import x51_fit as F

    res = F.gain_fit(_gain_rows(-3.0, 0.5, 2.0, 0.0, 200, seed=1), n_boot=60, seed=0, intercept=True)
    assert res["n_clusters"] == 40 and res["n_rows"] == 200 * 25 and len(res["cells"]) == 25
    lo, hi = res["ci"]["b"]
    assert lo < res["additive"]["b"] < hi and lo < 2.0 < hi
    assert res["nonconverged_resamples"] == {"additive": 0, "with_c": 0}
    cell = next(c for c in res["cells"] if c["alpha"] == 0 and c["beta"] == 2)
    assert cell["share_ci"][0] <= cell["share"] <= cell["share_ci"][1]


def test_ci3_and_strip():
    assert all(math.isnan(v) for v in C.ci3(math.nan, np.zeros(3)))
    assert C.strip({"a": 1, "_d": np.zeros(2), "b": [{"_x": 1, "y": 2}]}) == {"a": 1, "b": [{"y": 2}]}
