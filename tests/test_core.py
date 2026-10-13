"""Toy-tensor tests for the OMP, the clamp and the statistics (CPU, no model). Run: python tests/test_core.py"""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace.clamp import SwapClamp  # noqa: E402
from bridge_jspace.omp import nonneg_omp  # noqa: E402
from bridge_jspace.stats import paired_bootstrap_diff, wilson  # noqa: E402


def test_omp_recovers_planted_code():
    g = torch.Generator().manual_seed(0)
    dictionary = torch.nn.functional.normalize(torch.randn(2000, 256, generator=g), dim=-1)
    planted = torch.tensor([3, 70, 512, 1024, 1999])
    weights = torch.tensor([2.0, 1.5, 1.0, 0.8, 0.5])
    x = weights @ dictionary[planted]
    indices, coefs = nonneg_omp(dictionary, x, k=25)
    assert set(planted.tolist()) <= set(indices.tolist())
    recon = coefs @ dictionary[indices]
    assert (x - recon).norm() / x.norm() < 1e-4
    assert (coefs > 0).all()


def test_omp_never_uses_negative_coefficients():
    g = torch.Generator().manual_seed(1)
    dictionary = torch.nn.functional.normalize(torch.randn(500, 64, generator=g), dim=-1)
    x = -dictionary[7] + 0.5 * dictionary[9]   # atom 7 can only enter negatively
    indices, coefs = nonneg_omp(dictionary, x, k=10)
    assert (coefs > 0).all() and len(indices) <= 10


def _toy_clamp(n_atoms: int):
    g = torch.Generator().manual_seed(2)
    atoms = torch.randn(n_atoms, 64, generator=g)
    clean_h = torch.randn(6, 64, generator=g)
    return atoms, clean_h, SwapClamp(atoms, clean_h)


def test_clamp_hits_swapped_targets_and_keeps_the_rest():
    atoms, clean_h, clamp = _toy_clamp(5)
    out = clamp(clean_h)
    clean_c = clean_h[1:] @ torch.linalg.pinv(atoms)
    new_c = out[1:] @ torch.linalg.pinv(atoms)
    torch.testing.assert_close(new_c[:, 0], clean_c[:, 1], atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(new_c[:, 1], clean_c[:, 0], atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(new_c[:, 2:], clean_c[:, 2:], atol=1e-4, rtol=1e-4)
    # Nothing orthogonal to span(atoms) changes, and position 0 is untouched.
    q, _ = torch.linalg.qr(atoms.T)
    ortho = lambda h: h - (h @ q) @ q.T  # noqa: E731
    torch.testing.assert_close(ortho(out), ortho(clean_h), atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(out[0], clean_h[0])


def test_clamp_is_idempotent():
    _, clean_h, clamp = _toy_clamp(3)
    once = clamp(clean_h)
    torch.testing.assert_close(clamp(once), once, atol=1e-4, rtol=1e-4)


def test_null_direction_matches_edit_norm():
    atoms, clean_h, clamp = _toy_clamp(2)
    u = torch.nn.functional.normalize(torch.randn(64), dim=0)
    null = SwapClamp(atoms, clean_h, null_direction=u)
    torch.testing.assert_close(null.delta(clean_h).norm(dim=-1), clamp.delta(clean_h).norm(dim=-1))
    cos = torch.nn.functional.cosine_similarity(null.delta(clean_h), u[None], dim=-1)
    torch.testing.assert_close(cos, torch.ones_like(cos))


def test_wilson_known_values():
    rate, lo, hi = wilson(5, 10)
    assert abs(rate - 0.5) < 1e-12 and abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3
    _, lo0, hi0 = wilson(0, 10)
    assert lo0 < 1e-12 and abs(hi0 - 0.2775) < 1e-3


def test_paired_bootstrap():
    a = [1, 0, 1, 1, 0, 1, 0, 0]
    diff, lo, hi = paired_bootstrap_diff(a, a)
    assert diff == lo == hi == 0
    diff, lo, hi = paired_bootstrap_diff([1] * 8, [0] * 8)
    assert diff == lo == hi == 1


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")]
    for name, fn in tests:
        fn()
        print("ok", name)
    print(f"{len(tests)} tests passed")
