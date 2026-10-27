"""pointer_fair's pure helpers (no model): token groups, the suite's locker order, the overshoot analysis."""

import math
from typing import Any

import pytest

import scripts.pointer_fair as PFA


def test_after_group_is_the_last_question_token_and_everything_after():
    assert PFA.after_group([10, 11, 12], [13, 14, 15]) == [12, 13, 14, 15]
    assert PFA.after_group([], [3]) == [3]


def test_locker_order_reads_the_statements_in_context_order():
    ctx = (
        "Jack's pet is a cow. Mia's pet is a dog. The dog's locker is 3. The cow's locker is 5. The pig's locker is 7."
    )
    assert PFA.locker_order(ctx) == [("dog", "3"), ("cow", "5"), ("pig", "7")]


def test_beyond_and_the_uniform_expectation():
    # asked 1, target 3 of 5: off-target statements 0, 2, 4; beyond the target (far side from 1): 4 only
    assert [PFA.beyond(1, 3, k) for k in (0, 2, 4)] == [False, False, True]
    assert PFA.overshoot_expectation(1, 3, 5) == pytest.approx(1 / 3)
    # target below the asked statement: beyond means lower
    assert PFA.beyond(3, 1, 0) and not PFA.beyond(3, 1, 2)
    assert PFA.overshoot_expectation(3, 1, 5) == pytest.approx(1 / 3)
    assert PFA.overshoot_expectation(0, 4, 5) == 0.0  # nothing lies beyond the last statement
    assert math.isnan(PFA.overshoot_expectation(0, 1, 2))


def test_answer_slot_and_overshoot_counts():
    assert PFA.answer_slot("7", ["1", "7", "9"]) == 1
    assert PFA.answer_slot(None, ["1"]) is None and PFA.answer_slot("4", ["1"]) is None
    rows = {
        f"x{i}": {"domain": "animals", "query": q, "asked": 1, "target_slot": 3, "n_statements": 5, "answer_slot": s}
        for i, (q, s) in enumerate([("cow", 4), ("dog", 4), ("pig", 0), ("cow", 3), ("dog", 1), ("pig", None)])
    }
    o = PFA.overshoot(rows)
    assert o["n_off_target"] == 3  # target, answer org and non-statement answers are not off-target
    assert o["beyond"] == 2 and o["expected_uniform"] == pytest.approx(1.0)


def test_window_key_keeps_the_earlier_runs_label():
    assert PFA.window_key([32, 36, 40]) == "32-40"
    assert PFA.window_key((12, 8, 10)) == "8-12"


def test_widen_takes_the_wider_bound_and_keeps_the_rate():
    assert PFA.widen([0.3, 0.25, 0.35], [0.3, 0.26, 0.36]) == [0.3, 0.25, 0.36]
    # 0 hits: every resample gives 0, the Wilson upper bound stands (the memory → memory control needs it)
    assert PFA.widen([0.0, 0.0, 0.0], [0.0, 0.0, 0.03]) == [0.0, 0.0, 0.03]
    assert all(math.isnan(v) for v in PFA.widen([math.nan] * 3, [math.nan] * 3))


def test_topic_verdict_needs_rate_margin_and_both_controls():
    ok: dict[str, Any] = dict(
        ptr_lo=0.31, d_lens=[0.25, 0.1, 0.4], d_rand=[0.3, 0.2, 0.4], shuf_hi=0.08, shuf_n=100, rr_hi=0.09, rr_n=100
    )
    assert PFA.topic_verdict(**ok) == (True, True)
    assert PFA.topic_verdict(**{**ok, "ptr_lo": 0.29})[0] is False
    assert PFA.topic_verdict(**{**ok, "d_lens": [0.19, 0.1, 0.3]})[0] is False  # margin is a point estimate >= 20
    assert PFA.topic_verdict(**{**ok, "d_rand": [0.3, 0.0, 0.5]})[0] is False  # lower bound must be > 0
    assert PFA.topic_verdict(**{**ok, "rr_hi": 0.11}) == (True, False)
    assert PFA.topic_verdict(**{**ok, "shuf_n": 34}) == (True, False)


def _rows(topic: str, p_hit: float, rr_changed: float, n: int = 40, k: int = 8) -> list[dict]:
    """Synthetic outcome rows of one topic: n memory → prompt and n memory → memory items over k entities."""
    out = []
    for fam in ("RL", "RR"):
        for i in range(n):
            base = {"family": fam, "domain": topic, "name": f"{topic}-{fam}-{i}", "query": f"{topic}{i % k}",
                    "template": f"{i % 3}/{i % 3}", "cut": "entity", "asked": 0, "target_slot": 2, "n_statements": 5,
                    "group": "after", "layer": "32-40", "scale": 1.0}  # fmt: skip
            out.append({**base, "cond": "unedited", "group": None, "layer": None, "scale": None, "role": "org",
                        "changed": False, "answer_slot": 0})  # fmt: skip
            for cn in PFA.CONDS:
                hit = fam == "RL" and cn == "pointer" and i < p_hit * n
                changed = fam == "RR" and cn == "pointer" and i < rr_changed * n
                out.append({**base, "cond": cn, "role": "target" if hit else "org", "changed": hit or changed,
                            "answer_slot": 2 if hit else 0})  # fmt: skip
    return out


def test_decide_v4_counts_topics_and_sets_the_flags():
    rows = _rows("countries", 0.7, 0.0) + _rows("animals", 0.7, 0.0) + _rows("body", 0.7, 0.4)
    cfg = {"primary_scale": 1.0, "layers": [32, 36, 40], "domains": ["countries", "animals", "body"]}
    d = PFA.decide_v4(rows, cfg)["after"]
    assert [(d["topics"][t]["passes"], d["topics"][t]["valid"]) for t in cfg["domains"]] == [
        (True, True),
        (True, True),
        (True, False),
    ]
    assert d["topics_passing"] == 2 and d["flags"]["pointer_at_lens_depth"]
    assert not d["flags"]["not_lookup_specific"] and not d["flags"]["pointer_later_only"]
    assert (
        d["topics"]["countries"]["pointer"]["k_entities"] == 8
        and d["topics"]["countries"]["pointer"]["t_wordings"] == 3
    )
    # two topics with a weak pointer: the claim fails and "pointer only later" is flagged
    weak = _rows("countries", 0.1, 0.0) + _rows("animals", 0.05, 0.0) + _rows("body", 0.7, 0.0)
    d = PFA.decide_v4(weak, cfg)["after"]
    assert d["topics_passing"] == 1 and not d["flags"]["pointer_at_lens_depth"] and d["flags"]["pointer_later_only"]


def test_transit_and_c2_rules():
    assert (
        PFA.in_transit(0.03, 0.02, 0.6) and not PFA.in_transit(0.05, 0.02, 0.6) and not PFA.in_transit(0.0, 0.02, 0.4)
    )
    assert PFA.c2_layer([0.02, 0.0, 0.06], [0.0, 0.0, 0.02], 0.01) == "holds"  # >= 3x random but negligible
    assert PFA.c2_layer([0.05, 0.02, 0.12], [0.02, 0.0, 0.05], 0.0) == "holds"  # < 3x random
    assert PFA.c2_layer([0.2, 0.13, 0.28], [0.01, 0.0, 0.04], 0.12) == "killed"
    assert PFA.c2_layer([0.08, 0.0, 0.2], [0.0, 0.0, 0.05], -0.01) == "unclear"
    assert PFA.c2_topic([]) == "not testable" and PFA.c2_topic(["holds", "killed"]) == "killed"
    assert PFA.c2_topic(["holds", "holds"]) == "holds" and PFA.c2_topic(["holds", "unclear"]) == "undecided"


def _transit_rows(topic: str, spec: dict[int, tuple[float, float, float]], n: int = 100, k: int = 20) -> list[dict]:
    """Synthetic transit rows: spec[layer] = (memory → memory lens hits, memory → prompt copy changed, memory → prompt
    lens hits) as shares; random pushes never hit."""
    out = []
    for fam in ("RL", "RR"):
        for i in range(n):
            base = {"family": fam, "domain": topic, "name": f"{topic}-{fam}-{i}", "query": f"{topic}{i % k}",
                    "group": PFA.TRANSIT}  # fmt: skip
            for la, (rr_lens, copy, rl_lens) in spec.items():
                lens_hit = i < (rl_lens if fam == "RL" else rr_lens) * n
                out.append({**base, "layer": la, "scale": 1.0, "cond": "lens", "role": "target" if lens_hit else "org",
                            "changed": lens_hit})  # fmt: skip
                out.append({**base, "layer": la, "scale": 1.0, "cond": "random", "role": "org", "changed": False})
                ch = fam == "RL" and i < copy * n
                out.append({**base, "layer": la, "scale": None, "cond": "patch", "role": "org", "changed": ch})
    return out


def test_decide_transit_finds_transit_layers_and_c2_per_topic():
    rows = (
        _transit_rows("a", {28: (0.5, 0.9, 0.3), 40: (0.0, 0.8, 0.02), 52: (0.0, 0.2, 0.0)})  # transit at 40, holds
        + _transit_rows("b", {28: (0.5, 0.9, 0.3), 40: (0.0, 0.8, 0.3), 52: (0.0, 0.2, 0.0)})  # transit at 40, killed
        + _transit_rows("c", {28: (0.5, 0.9, 0.3), 40: (0.4, 0.8, 0.3), 52: (0.3, 0.6, 0.0)})  # no transit
    )
    cfg = {"domains": ["a", "b", "c"], "transit_layers": [28, 40, 52], "transit_scales": [1.0], "primary_scale": 1.0}
    tr = PFA.decide_transit(rows, cfg)["by_scale"]["1"]
    assert [tr["topics"][t]["transit_layers"] for t in "abc"] == [[40], [40], []]
    assert [tr["topics"][t]["c2"] for t in "abc"] == ["holds", "killed", "not testable"]
    assert tr["flags"] == {"c2_transit": False, "no_transit": True, "c2_killed": True}


def test_v4_items_are_held_out_of_the_fit_only():
    cfg = {
        "data": "pointer_v4",
        "domains": ["countries", "body"],
        "n": {"RL": 30, "DL": 0, "RR": 10},
        "competence": None,
    }
    items = PFA.v1_items(cfg)
    assert {it["family"] for it in items} == {"RL", "RR"}
    assert all(it["cut"] != "neither" for it in items)
    assert sum(it["family"] == "RL" for it in items) == 60 and sum(it["family"] == "RR" for it in items) == 20
