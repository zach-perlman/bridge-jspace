"""x0_massmean: the mass-mean basis spans the centred class means, is orthonormal, and has rank classes - 1."""

import numpy as np

from scripts import x0_massmean as MM


def test_mass_mean_spans_the_class_means():
    rng = np.random.default_rng(0)
    d, n, k = 30, 400, 5
    centres = rng.normal(size=(k, d)) * 2.0
    labels = [int(v) for v in rng.integers(0, k, n)]
    x = centres[labels] + rng.normal(size=(n, d)) * 0.5
    q = MM.mass_mean(x, labels)
    assert q.shape == (d, k - 1)
    assert np.allclose(q.T @ q, np.eye(k - 1), atol=1e-8)
    mu = x.mean(0)
    means = np.stack([x[[i for i, v in enumerate(labels) if v == c]].mean(0) - mu for c in range(k)])
    resid = means.T - q @ (q.T @ means.T)
    assert np.linalg.norm(resid) / np.linalg.norm(means) < 1e-8


def _two_routes_rows(lost: dict[str, dict[str, float]], n: int = 60, ents: int = 20) -> list[dict]:
    """Synthetic batch-45g rows: every item switches with the whole change; without a part, the share lost[order][arm]
    of items no longer switches (the first ones), for both readers."""
    rows = []
    for order in ("before", "after"):
        for i in range(n):
            scene = f"{order}-{i}"
            for w in ("PP", "PM"):
                for arm in (
                    "whole",
                    *(f"no_{p}" for p in MM.TWO_ROUTES_PARTS),
                    *(f"no_{p}_rand" for p in MM.TWO_ROUTES_PARTS),
                ):
                    drop = lost[order].get(arm, 0.0) if w == "PM" else 0.0
                    rows.append({"scene": scene, "entity": f"e{i % ents}", "reader": w, "arm": arm, "org_order": order,
                                 "switched": int(i >= round(drop * n))})  # fmt: skip
    return rows


def test_two_routes_rule_a_needs_the_union_above_each_part():
    # recall, locker before: J++ alone and the pointer alone cost 0.1 each, both together 0.6; random parts nothing
    yes = MM.two_routes_cells(
        _two_routes_rows({"before": {"no_jpp": 0.1, "no_Alf": 0.1, "no_jppAlf": 0.6}, "after": {}}), 500
    )
    assert abs(yes["PM|before"]["jppAlf"][0] - 0.6) < 1e-9 and yes["PM|before"]["both_minus_larger"][0] > 0.49
    assert MM.rule_45g(yes)["a"]
    # the union no better than J++ alone: (a) fails
    no = MM.two_routes_cells(
        _two_routes_rows({"before": {"no_jpp": 0.5, "no_Alf": 0.1, "no_jppAlf": 0.55}, "after": {}}), 500
    )
    assert not MM.rule_45g(no)["a"]
    assert no["PM|before"]["larger_single"] == "jpp"


def test_two_routes_rule_b_and_the_random_part():
    # locker after: J++ alone 0.5, the union 0.55 (adds < 0.1) -> (b); random parts subtract
    rows = _two_routes_rows({"before": {}, "after": {"no_jpp": 0.5, "no_jppAlf": 0.55, "no_jpp_rand": 0.1}})
    c = MM.two_routes_cells(rows, 500)
    assert abs(c["PM|after"]["jpp"][0] - 0.4) < 1e-9  # 0.5 lost minus 0.1 lost to the random part
    assert c["PM|after"]["n"] == 60 and c["PM|all"]["n"] == 120
    assert MM.rule_45g(c)["b"] is False  # J++ 0.4 >= 0.3, but the union adds 0.55 - 0.4 = 0.15 >= 0.1
    rows = _two_routes_rows({"before": {}, "after": {"no_jpp": 0.5, "no_jppAlf": 0.55}})
    assert MM.rule_45g(MM.two_routes_cells(rows, 500))["b"] is True
