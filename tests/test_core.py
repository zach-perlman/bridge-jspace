"""Toy-tensor tests for the OMP, the clamp and the statistics (CPU, no model). Run: python tests/test_core.py"""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace.clamp import SwapClamp
from bridge_jspace.data import _derived_forms, _words
from bridge_jspace.omp import nonneg_omp
from bridge_jspace.stats import ledoit_wolf, paired_bootstrap_diff, wilson


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
    x = -dictionary[7] + 0.5 * dictionary[9]  # atom 7 can only enter negatively
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


def test_clamp_positions_edit_only_those_positions():
    atoms, clean_h, full = _toy_clamp(3)
    some = SwapClamp(atoms, clean_h, positions=[2, 5])
    out, ref = some(clean_h), full(clean_h)
    torch.testing.assert_close(out[[2, 5]], ref[[2, 5]])  # the same edit where it applies
    torch.testing.assert_close(out[[0, 1, 3, 4]], clean_h[[0, 1, 3, 4]])  # nothing elsewhere
    null = SwapClamp(
        atoms, clean_h, null_direction=torch.nn.functional.normalize(torch.randn(64), dim=0), positions=[5]
    )
    assert (null.delta(clean_h)[:4] == 0).all()
    assert some.edit_ratio_last == full.edit_ratio_last  # position 5 is the last, edited in both


def test_cue_regimes_split_the_earlier_positions():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.exp02_swaps import regime_positions, span_positions

    # "The capital of the country where Naples is located is": Naples = characters 33-39
    offsets = [(0, 3), (3, 11), (11, 14), (14, 18), (18, 26), (26, 32), (32, 39), (39, 42), (42, 50), (50, 53)]
    cue = span_positions(offsets, 33, 39)
    assert cue == [6]
    seq_len = len(offsets)
    cue_pos = regime_positions("cue", seq_len, cue)
    rest = regime_positions("earlier_noncue", seq_len, cue)
    assert cue_pos == [6]
    assert cue_pos is not None
    assert rest is not None
    assert sorted(cue_pos + rest) == regime_positions("earlier", seq_len)  # they partition "earlier"


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


def test_ledoit_wolf_matches_definition_and_limits():
    g = torch.Generator().manual_seed(3)
    z = torch.randn(30, 12, generator=g, dtype=torch.float64) * torch.linspace(0.2, 3.0, 12, dtype=torch.float64)
    cov, a = ledoit_wolf(z)
    n, d = z.shape
    s = z.T @ z / n
    mu = torch.trace(s) / d
    d2 = ((s - mu * torch.eye(d, dtype=s.dtype)) ** 2).sum() / d
    b2 = sum(((zi[:, None] * zi[None] - s) ** 2).sum() for zi in z) / n**2 / d
    expected = float(min(b2, d2) / d2)
    assert abs(a - expected) < 1e-10
    torch.testing.assert_close(cov, (1 - a) * s + a * mu * torch.eye(d, dtype=s.dtype))
    _, a_isotropic = ledoit_wolf(torch.randn(20, 200, generator=g))  # n << d, no structure: shrink a lot
    _, a_structured = ledoit_wolf(torch.randn(5000, 10, generator=g) * torch.logspace(-1, 1, 10))  # n >> d
    assert a_isotropic > 0.8 and a_structured < 0.05


def test_name_derived_words_count_as_naming_the_entity():
    def leaks(entity, text):
        return any(w.startswith(_derived_forms(entity)) for w in _words(text))

    assert leaks("Brazil", "the Brazilian real") and leaks("drums", "a drummer") and leaks("China", "Chinese tea")
    assert leaks("nitrogen", "nitrates in soil") and leaks("Saturn", "on Saturday")
    assert not leaks("heart", "sounds heard through a stethoscope") and not leaks("ant", "an antenna")


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")]
    for name, fn in tests:
        fn()
        print("ok", name)
    print(f"{len(tests)} tests passed")


def test_matched_direction_has_the_jpart_cosine_to_the_probe():
    import pytest

    if not torch.cuda.is_available():
        pytest.skip("Probes live on the GPU")
    from scripts.exp02_swaps import Probes

    g = torch.Generator().manual_seed(0)
    probe, jpart = torch.randn(3, 2, 32, generator=g), torch.randn(3, 2, 32, generator=g)
    probes = Probes.__new__(Probes)
    probes.index, probes.layer_index = {"a": 0, "b": 1, "c": 2}, {10: 0, 11: 1}
    probes.parts = {"full_probe": probe.cuda(), "jpart": jpart.cuda()}
    for entity in "abc":
        for layer in (10, 11):
            u = probes.matched(entity, layer)
            p, j = probes.unit("full_probe", entity, layer), probes.unit("jpart", entity, layer)
            torch.testing.assert_close(u.norm(), torch.tensor(1.0, device="cuda"))
            torch.testing.assert_close(u @ p, j @ p)
            torch.testing.assert_close(probes.matched(entity, layer), u)  # seeded
