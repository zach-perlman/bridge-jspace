"""Toy-tensor tests for bridge_jspace.ablate (CPU, no model). Run: python tests/test_ablate.py"""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace.ablate import (
    LensDictionary,
    MatrixDictionary,
    RotatedDictionary,
    RowSettings,
    omp_fit,
    removal_edit,
    rotation,
    top_span_removal,
)
from scripts.exp04_brew_parts import signed_omp


def _setup(n=300, d=48, seed=0):
    g = torch.Generator().manual_seed(seed)
    wg = torch.randn(n, d, generator=g, dtype=torch.float64).float()
    J = torch.randn(d, d, generator=g, dtype=torch.float64).float() / d**0.5
    explicit = torch.nn.functional.normalize(wg @ J, dim=-1)
    x = torch.randn(20, d, generator=g, dtype=torch.float64).float() * 2
    return LensDictionary(wg, J), explicit, x


def test_lens_dictionary_matches_explicit_unit_vectors():
    dic, explicit, x = _setup()
    assert torch.allclose(dic.scores(x), x @ explicit.T, atol=1e-4)
    idx = torch.tensor([[0, 5], [7, 299]])
    assert torch.allclose(dic.atoms(idx), explicit[idx], atol=1e-5)
    assert torch.equal(dic.logits(x).argsort(dim=1)[:, -3:], (x @ (dic.wg @ dic.J).T).argsort(dim=1)[:, -3:])


def test_omp_matches_v1_signed_omp():
    dic, explicit, x = _setup()
    assert torch.allclose(omp_fit(dic, x, 8), signed_omp(explicit, x, 8), atol=1e-4)
    assert torch.allclose(omp_fit(MatrixDictionary(explicit), x, 8), signed_omp(explicit, x, 8), atol=1e-5)


def test_omp_never_chooses_banned_atoms():
    dic, _, x = _setup()
    _, chosen_free = omp_fit(dic, x, 6, return_chosen=True)
    banned = chosen_free[:5].flatten().unique()
    _, chosen = omp_fit(dic, x, 6, banned=[(torch.arange(5), banned)], return_chosen=True)
    assert not torch.isin(chosen[:5], banned).any()
    assert torch.equal(chosen[5:], chosen_free[5:])  # other rows unaffected


def test_top_span_removal_projects_out_the_top_atoms_and_spares_protected():
    dic, explicit, x = _setup()
    proj, top = top_span_removal(dic, x, 10, return_chosen=True)
    resid = x - proj
    assert (resid.unsqueeze(1) * explicit[top]).sum(-1).abs().max() < 1e-3  # orthogonal to every removed atom
    protected = top[:, :3].flatten().unique()
    _, top2 = top_span_removal(dic, x, 10, protected=[(torch.arange(20), protected)], return_chosen=True)
    assert not torch.isin(top2, protected).any()


def test_rotated_dictionary_is_the_rotated_atoms():
    dic, explicit, x = _setup()
    R = rotation(48, 7, device="cpu")
    rot = RotatedDictionary(dic, R)
    assert torch.allclose(rot.scores(x), x @ (explicit @ R).T, atol=1e-4)
    assert torch.allclose(rot.atoms(torch.tensor([3])), (explicit @ R)[[3]], atol=1e-5)


def test_removal_edit_skips_positions_and_rotation_keeps_size():
    dic, _, _ = _setup()
    g = torch.Generator().manual_seed(1)
    h = torch.randn(2, 6, 48, generator=g)
    rows = [RowSettings(skip=[0, 1]), RowSettings()]
    out = removal_edit("omp", dic, rows, k=4)(h)
    assert torch.equal(out[0, :2], h[0, :2])  # skipped positions untouched
    assert not torch.allclose(out[1], h[1])
    R = rotation(48, 3, device="cpu")
    out_rot = removal_edit("omp", dic, rows, rotation=R, k=4)(h)
    assert torch.allclose((h - out).norm(dim=-1), (h - out_rot).norm(dim=-1), atol=1e-4)  # same size everywhere
    out_top = removal_edit("top", dic, [RowSettings(protected=torch.tensor([1, 2])), RowSettings()], k=3)(h)
    assert out_top.shape == h.shape


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
