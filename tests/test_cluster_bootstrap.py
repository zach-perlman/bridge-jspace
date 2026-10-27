"""stats.cluster_bootstrap: the entity-cluster bootstrap (items of one entity are correlated)."""

import numpy as np
import pytest

from bridge_jspace.stats import bootstrap_mean, cluster_bootstrap


def test_constant_values_give_a_point_interval():
    m, lo, hi = cluster_bootstrap([1.0] * 20, [i % 4 for i in range(20)])
    assert m == lo == hi == 1.0


def test_correlated_clusters_widen_the_interval():
    # 10 entities, each answered all-right or all-wrong: the effective n is 10, not 100
    clusters = [i // 10 for i in range(100)]
    values = [float((i // 10) % 2) for i in range(100)]
    _, lo_c, hi_c = cluster_bootstrap(values, clusters, n_boot=4000, seed=0)
    _, lo_i, hi_i = bootstrap_mean(values, 4000, 0)
    assert hi_c - lo_c > 2 * (hi_i - lo_i)


def test_independent_items_match_the_item_bootstrap():
    rng = np.random.default_rng(1)
    values = rng.integers(0, 2, 400).astype(float)
    _, lo_c, hi_c = cluster_bootstrap(values, list(range(400)), n_boot=4000, seed=0)
    _, lo_i, hi_i = bootstrap_mean(values, 4000, 0)
    assert hi_c - lo_c == pytest.approx(hi_i - lo_i, abs=0.02)


def test_strata_keep_their_share():
    # stratum a: all 1 (5 clusters); stratum b: all 0 (5 clusters), 10 items each: every resample has mean 0.5
    values = [1.0] * 50 + [0.0] * 50
    clusters = [f"a{i % 5}" for i in range(50)] + [f"b{i % 5}" for i in range(50)]
    strata = ["a"] * 50 + ["b"] * 50
    m, lo, hi = cluster_bootstrap(values, clusters, strata)
    assert m == lo == hi == 0.5


def test_deterministic_and_empty():
    v, c = [0, 1, 1, 0, 1, 1], ["x", "x", "y", "y", "z", "z"]
    assert cluster_bootstrap(v, c, seed=3) == cluster_bootstrap(v, c, seed=3)
    with pytest.raises(ValueError):
        cluster_bootstrap([], [])
    with pytest.raises(ValueError):
        cluster_bootstrap([0, 1], ["x"])
