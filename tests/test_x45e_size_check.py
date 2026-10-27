"""45e size check: which scenes count as matched, and the zero-direction summary. Planted rows; no GPU."""

from scripts import x45e_size_check as S


def _norm(scene, cond, idout, wrong, k=3, pool=30):
    return {"scene": scene, "condition": cond, "share_idout": idout, "share_wrong": wrong, "k_wrong": k,
            "n_wrong_pool": pool}  # fmt: skip


def test_matched_keeps_the_control_at_or_above_the_bar():
    norms = [_norm("C0-1", "C0", 0.10, 0.09), _norm("C0-2", "C0", 0.10, 0.0899), _norm("C0-3", "C0", 0.10, 0.25),
             _norm("C2-1", "C2", 0.0, 0.0, k=0), _norm("C2-2", "C2", 0.2, 0.0, k=0)]  # fmt: skip
    # exactly 0.9 counts; an overshoot counts; idout's share 0 and a zero-direction control do not
    assert S.matched(norms) == {"C0-1", "C0-3"}


def test_zero_directions_reports_pool_and_idout_share():
    norms = [_norm("C0-1", "C0", 0.001, 0.0, k=0), _norm("C0-2", "C0", 0.08, 0.08), _norm("C0-3", "C0", 0.06, 0.06),
             _norm("C2-1", "C2", 0.05, 0.05)]  # fmt: skip
    cases = {r["scene"]: {"domain": "animals"} for r in norms}
    z = S.zero_directions(norms, cases)
    assert z["C0"]["k0"] == 1 and z["C0"]["k0_pools"] == [30] and z["C0"]["k0_domains"] == ["animals"]
    assert z["C0"]["k0_idout_median"] == 0.001 and z["C0"]["all_idout_median"] == 0.06
    assert z["C2"]["k0"] == 0 and z["C2"]["k0_idout_median"] is None
