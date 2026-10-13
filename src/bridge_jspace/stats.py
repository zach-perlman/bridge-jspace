"""Rates with Wilson intervals and paired bootstrap differences."""

import math

import numpy as np


def wilson(hits: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """(rate, lower, upper) of the Wilson score interval; nan for n = 0."""
    if n == 0:
        return (math.nan, math.nan, math.nan)
    p = hits / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (p, centre - half, centre + half)


def paired_bootstrap_diff(a, b, n_boot: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """(mean(a) - mean(b), 2.5th, 97.5th percentile) resampling items with replacement; a and b are per-item 0/1
    outcomes on the same items."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(a), size=(n_boot, len(a)))
    diffs = a[idx].mean(1) - b[idx].mean(1)
    return (float(a.mean() - b.mean()), float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5)))
