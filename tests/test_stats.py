import math

import pytest

from bridge_jspace.stats import bootstrap_mean, wilson


def test_wilson_reference_value():
    # 55/90 ~ 61%, the paper's J-space swap rate: textbook Wilson interval.
    p, lo, hi = wilson(55, 90)
    assert p == pytest.approx(0.6111, abs=1e-4)
    assert lo == pytest.approx(0.5079, abs=1e-3)
    assert hi == pytest.approx(0.7050, abs=1e-3)


def test_wilson_edges():
    assert wilson(0, 10)[1] == pytest.approx(0.0, abs=1e-12)
    assert wilson(10, 10)[2] == pytest.approx(1.0)
    assert wilson(0, 10)[2] > 0.0  # unlike the Wald interval, not degenerate at 0


def test_wilson_empty_is_nan():
    assert all(math.isnan(v) for v in wilson(3, 0))


def test_bootstrap_deterministic_and_brackets_mean():
    x = [0, 1, 1, 0, 1, 1, 1, 0, 0.5, 1]
    a = bootstrap_mean(x, n_boot=2000, seed=0)
    assert a == bootstrap_mean(x, n_boot=2000, seed=0)
    mean, lo, hi = a
    assert mean == pytest.approx(0.65)
    assert lo < mean < hi


def test_bootstrap_constant_has_zero_width():
    assert bootstrap_mean([1.0] * 20, n_boot=500, seed=0) == (1.0, 1.0, 1.0)
