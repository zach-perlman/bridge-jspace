"""exp07_step_code: the code fit, its reading and the edit sizes (no model)."""

import random

import torch

from scripts.exp07_step_code import COLOURS, CodeFit, code_of, decode_intermediate, design_row, resized, scaled


def test_design_row_is_an_intercept_and_three_one_hot_blocks():
    x = design_row("blue", "teal", "red")
    k = len(COLOURS)
    assert x[0] == 1 and x.sum() == 4
    assert x[1 + COLOURS.index("blue")] == 1
    assert x[1 + k + COLOURS.index("teal")] == 1
    assert x[1 + 2 * k + COLOURS.index("red")] == 1


def planted(seed: int, n_positions: int = 3, d: int = 16):
    g = torch.Generator().manual_seed(seed)
    k = len(COLOURS)
    codes = {role: torch.randn(k, n_positions, d, generator=g, dtype=torch.float64) for role in "SIA"}
    codes = {role: c - c.mean(dim=0, keepdim=True) for role, c in codes.items()}  # each block sums to zero
    return torch.randn(n_positions, d, generator=g, dtype=torch.float64), codes


def test_code_fit_recovers_planted_codes():
    intercept, codes = planted(0)
    rng, g = random.Random(0), torch.Generator().manual_seed(1)
    fit = CodeFit((36,), n_positions=3, d=16, device="cpu")
    for _ in range(1500):
        s, i, a = rng.sample(COLOURS, 3)
        h = intercept + sum(codes[r][COLOURS.index(c)] for r, c in zip("SIA", (s, i, a), strict=True))
        fit.add(s, i, a, {36: h + 0.05 * torch.randn(h.shape, generator=g, dtype=torch.float64)})
    w = fit.solve(1.0)[36]
    k = len(COLOURS)
    assert torch.allclose(w[1 + k : 1 + 2 * k].sum(dim=0), torch.zeros(3, 16, dtype=torch.float64), atol=1e-6)
    for x, i in (("gold", "blue"), ("white", "pink")):
        want = codes["I"][COLOURS.index(x)] - codes["I"][COLOURS.index(i)]
        assert torch.allclose(code_of(w, x) - code_of(w, i), want, atol=0.06)


def test_decode_intermediate_reads_the_planted_colour():
    intercept, codes = planted(2)
    k = len(COLOURS)
    w = torch.cat([intercept[None], codes["S"], codes["I"], codes["A"]]).float()
    assert w.shape[0] == 1 + 3 * k
    h = (intercept + codes["S"][COLOURS.index("red")] + codes["I"][COLOURS.index("teal")] + codes["A"][0]).float()
    assert decode_intermediate(w, h, "red", COLOURS[0]) == "teal"


def test_scaled_rows_and_resized_total():
    g = torch.Generator().manual_seed(3)
    norms = torch.tensor([1.0, 2.0, 0.5])
    rows = scaled(torch.randn(3, 8, generator=g), norms)
    assert torch.allclose(rows.norm(dim=-1), norms, atol=1e-6)
    one = scaled(torch.randn(8, generator=g), norms)  # one direction for every position
    assert torch.allclose(torch.nn.functional.cosine_similarity(one[0], one[2], dim=0), torch.tensor(1.0), atol=1e-6)
    edit, like = torch.randn(3, 8, generator=g), torch.randn(3, 8, generator=g)
    out = resized(edit, like)
    assert torch.allclose(out.norm(), like.norm(), atol=1e-5)
    assert torch.allclose(out / out.norm(), edit / edit.norm(), atol=1e-6)  # same spread over positions
