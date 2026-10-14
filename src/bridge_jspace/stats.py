"""Rates with Wilson intervals, bootstrap CIs (means and paired differences), and a shrunk covariance."""

import math

import numpy as np
import torch


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


def bootstrap_mean(values, n_boot: int, seed: int, alpha: float = 0.05) -> tuple[float, float, float]:
    """(mean, lo, hi): percentile bootstrap CI of the mean over items. For paired comparisons pass per-item
    differences."""
    x = np.asarray(values, dtype=float)
    if x.size == 0:
        raise ValueError("bootstrap_mean needs at least one value")
    rng = np.random.default_rng(seed)
    means = x[rng.integers(0, x.size, size=(n_boot, x.size))].mean(axis=1)
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return float(x.mean()), float(lo), float(hi)


def ledoit_wolf(z: torch.Tensor) -> tuple[torch.Tensor, float]:
    """Ledoit-Wolf (2004) shrunk covariance of already-centred rows z [n, d]: (1 - a) S + a (tr S / d) I with
    S = z^T z / n and the analytic intensity a = min(b2, d2) / d2, where (Frobenius norms divided by d)
    d2 = |S - (tr S / d) I|^2 and b2 = (1 / n^2) sum_i |z_i z_i^T - S|^2. Returns (cov [d, d] float64, a)."""
    z = z.double()
    n, d = z.shape
    # Aligned derivation comments: keep the formatter out.
    # fmt: off
    sq_norms = z.pow(2).sum(1)                                   # |z_i|^2
    mu = float(sq_norms.sum()) / (n * d)                         # tr(S) / d
    s_fro2 = float((z @ z.T).pow(2).sum()) / n ** 2              # |S|_F^2, via the n x n Gram matrix
    d2 = (s_fro2 - d * mu ** 2) / d
    b2 = (float(sq_norms.pow(2).sum()) / n - s_fro2) / (n * d)   # sum_i |z_i z_i^T - S|^2 = sum|z_i|^4 - n|S|^2
    a = min(b2, d2) / d2
    # fmt: on
    cov = (1 - a) * (z.T @ z / n) + a * mu * torch.eye(d, dtype=z.dtype, device=z.device)
    return cov, a
