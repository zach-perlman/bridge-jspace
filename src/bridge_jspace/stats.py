from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np

Z95 = 1.959963984540054


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float, float]:
    """Proportion k/n with its Wilson score interval: (p, lo, hi)."""
    if n <= 0:
        raise ValueError("wilson needs n > 0")
    if not 0 <= k <= n:
        raise ValueError(f"need 0 <= k <= n, got k={k}, n={n}")
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return p, max(0.0, centre - half), min(1.0, centre + half)


def bootstrap_mean(values: Sequence[float], n_boot: int, seed: int, alpha: float = 0.05) -> tuple[float, float, float]:
    """Mean with a percentile bootstrap CI over items: (mean, lo, hi).

    For paired comparisons pass the per-item differences.
    """
    x = np.asarray(values, dtype=float)
    if x.size == 0:
        raise ValueError("bootstrap_mean needs at least one value")
    rng = np.random.default_rng(seed)
    means = x[rng.integers(0, x.size, size=(n_boot, x.size))].mean(axis=1)
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return float(x.mean()), float(lo), float(hi)
