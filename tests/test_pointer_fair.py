"""pointer_fair's pure helpers (no model): token groups, the suite's locker order, the overshoot analysis."""

import math

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
