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
