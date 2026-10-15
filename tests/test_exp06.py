"""exp06_sigma_writes: Σ_λ products and covariance draws on a small synthetic covariance (no model)."""

import torch

from scripts.exp06_sigma_writes import Sigma


def fake_sigma(cov: torch.Tensor) -> Sigma:
    s = Sigma.__new__(Sigma)
    s.cov, s._root, s.n_positions = {0: cov.double()}, {}, 0
    return s


def test_lambda_one_keeps_the_direction_and_zero_applies_sigma():
    a = torch.randn(6, 6, dtype=torch.float64)
    cov = a @ a.T
    s, u = fake_sigma(cov), torch.randn(6)
    one = s.apply(0, u, 1.0)
    assert torch.allclose(one / one.norm(), u / u.norm(), atol=1e-5)
    assert torch.allclose(s.apply(0, u, 0.0), (cov @ u.double()).float(), atol=1e-4)


def test_draws_have_the_covariance():
    a = torch.randn(4, 4, dtype=torch.float64)
    cov = a @ a.T + torch.eye(4, dtype=torch.float64)
    s, g = fake_sigma(cov), torch.Generator().manual_seed(0)
    x = torch.stack([s.draw(0, g).double() for _ in range(20000)])
    assert torch.allclose(x.T @ x / len(x), cov, atol=0.1 * float(cov.diag().mean()))
