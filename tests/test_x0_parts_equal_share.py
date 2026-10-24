"""x0_parts.equal_share: on orthonormal atoms it is signed OMP's part, with k per row matching a target share."""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x0_parts as XP
from scripts.exp04_brew_parts import signed_omp


def setup(n=6, d=64, atoms=40, seed=0):
    g = torch.Generator().manual_seed(seed)
    q, _ = torch.linalg.qr(torch.randn(d, atoms, generator=g))
    return q.T.contiguous(), torch.randn(n, d, generator=g)  # [atoms, d] orthonormal rows, [n, d]


def share(part, x):
    return part.norm(dim=-1) ** 2 / x.norm(dim=-1) ** 2


def test_matches_signed_omp_at_its_k():
    top, x = setup()
    target = torch.tensor([0.05, 0.1, 0.2, 0.3, 0.4, 0.5])
    part, k = XP.equal_share(top, x, target)
    for i in range(len(x)):
        ref = signed_omp(top, x[i : i + 1], int(k[i]))[0] if k[i] else torch.zeros_like(x[i])
        assert torch.allclose(part[i], ref, atol=1e-4)


def test_share_is_closest_to_the_target():
    top, x = setup()
    target = torch.tensor([0.05, 0.1, 0.2, 0.3, 0.4, 0.5])
    part, k = XP.equal_share(top, x, target)
    got = share(part, x)
    for i in range(len(x)):
        # one atom fewer or more is never closer to the target
        for kk in (int(k[i]) - 1, int(k[i]) + 1):
            if 0 < kk <= top.shape[0]:
                other = share(signed_omp(top, x[i : i + 1], kk), x[i : i + 1])[0]
                assert abs(float(got[i] - target[i])) <= abs(float(other - target[i])) + 1e-6


def test_zero_target_gives_an_empty_part():
    top, x = setup()
    part, k = XP.equal_share(top, x, torch.zeros(len(x)))
    assert (k == 0).all() and torch.count_nonzero(part) == 0
