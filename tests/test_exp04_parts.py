"""exp04_brew_parts: the parts of a copy, signed OMP, and the edits (no model)."""

import torch

from scripts.exp04_brew_parts import AddRows, lens2_part, null_rows, signed_omp


def test_signed_omp_recovers_a_sparse_signed_combination():
    g = torch.Generator().manual_seed(0)
    dictionary = torch.nn.functional.normalize(torch.randn(400, 64, generator=g), dim=-1)
    x = torch.stack([2.0 * dictionary[3] - 1.5 * dictionary[17], -dictionary[5] + 0.5 * dictionary[300]])
    approx = signed_omp(dictionary, x, k=4)
    assert torch.allclose(approx, x, atol=1e-4)


def test_lens2_part_is_the_projection_onto_the_two_vectors():
    g = torch.Generator().manual_seed(1)
    v = torch.nn.functional.normalize(torch.randn(2, 16, generator=g), dim=-1)
    delta = torch.randn(5, 16, generator=g)
    part = lens2_part(delta, v)
    assert torch.allclose(lens2_part(part, v), part, atol=1e-5)  # idempotent
    assert torch.allclose((delta - part) @ v.T, torch.zeros(5, 2), atol=1e-5)  # the rest is orthogonal to v


def test_add_rows_and_null_rows():
    g = torch.Generator().manual_seed(2)
    h, delta = torch.randn(6, 8, generator=g), torch.randn(2, 8, generator=g)
    out = AddRows(delta, [1, 4])(h)
    assert torch.allclose(out[[1, 4]], h[[1, 4]] + delta)
    assert torch.equal(out[[0, 2, 3, 5]], h[[0, 2, 3, 5]])
    noise = null_rows(delta, g)
    assert torch.allclose(noise.norm(dim=-1), delta.norm(dim=-1), atol=1e-5)
