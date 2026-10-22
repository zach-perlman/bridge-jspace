"""primacy_noise: the answer classes, the observed / expected ratios and the pre-registered decision (no model)."""

import pytest

from scripts import primacy_noise as PN

CASE = {
    "ids": [10, 5, 11, 3, 12, 7, 13, 9, 14, 1, 15],
    "tok_A": 7,
    "conf_toks": [1, 3, 5, 9],
}  # digits 5 3 7 9 1 in order


def test_classify_by_place_in_the_prompt():
    assert PN.classify(7, CASE) == ("right", 3)
    assert PN.classify(5, CASE) == ("list", 1)
    assert PN.classify(1, CASE) == ("list", 5)
    assert PN.classify(99, CASE) == ("off", None)


def test_ratios_uniform_and_first_heavy():
    uniform = [(i, 3, j) for i, j in enumerate([1, 2, 4, 5] * 10)]
    assert all(r == pytest.approx(1.0) for k, r in PN.ratios(uniform).items() if k != 3)
    first = [(i, 3, 1) for i in range(40)]
    assert PN.ratios(first)[1] == pytest.approx(4.0)


@pytest.mark.parametrize(("chosen", "verdict"), [
    ([1] * 60, "generic"),
    ([1, 2, 4, 5] * 15, "specific to blocking"),
    ([1] * 10, "not testable"),
])  # fmt: skip
def test_decide(chosen, verdict):
    acc = {0.05: 0.9, 0.1: 0.5, 0.2: 0.12, 0.4: 0.02}
    items = [(i, 3, j) for i, j in enumerate(chosen)]
    wrong = {s: (items if s == 0.2 else []) for s in acc}
    d = PN.decide(acc, wrong, blocked_acc=0.09)
    assert d["sigma_star"] == 0.2
    assert d["verdict"].startswith(verdict)
