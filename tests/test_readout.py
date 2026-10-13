"""Readout on a tiny from-scratch LensModel: no download, checks the math against jlens itself."""

from typing import ClassVar

import pytest
import torch
from jlens import JacobianLens
from torch import nn

from bridge_jspace.readout import (
    continuation_first_token,
    rank_grid,
    ranks_of,
    readout_logits,
    residuals,
    word_tokens,
)

D, V, L, SEQ = 8, 32, 4, 5


class TinyModel:
    """Minimal jlens LensModel: residual blocks h + tanh(W h), unembed = LayerNorm + Linear."""

    def __init__(self, seed: int = 0):
        g = torch.Generator().manual_seed(seed)
        self.n_layers, self.d_model, self.tokenizer = L, D, None
        self.embed = nn.Embedding(V, D)
        self.layers = nn.ModuleList(_Block(g) for _ in range(L))
        self.norm = nn.LayerNorm(D)
        self.head = nn.Linear(D, V, bias=False)
        for p in [*self.embed.parameters(), *self.head.parameters()]:
            p.data = torch.randn(p.shape, generator=g)

    def encode(self, text: str, *, max_length: int = 512) -> torch.Tensor:
        return torch.tensor([[ord(c) % V for c in text[:max_length]]])

    def forward(self, input_ids):
        h = self.embed(input_ids)
        for block in self.layers:
            h = block(h)
        return h

    def unembed(self, residual):
        return self.head(self.norm(residual))


class _Block(nn.Module):
    def __init__(self, g):
        super().__init__()
        self.w = nn.Parameter(torch.randn(D, D, generator=g) / D**0.5)

    def forward(self, h):
        return h + torch.tanh(h @ self.w.T)


@pytest.fixture
def model():
    return TinyModel()


@pytest.fixture
def lens():
    g = torch.Generator().manual_seed(1)
    return JacobianLens({i: torch.randn(D, D, generator=g) for i in range(L - 1)}, n_prompts=1, d_model=D)


def _naive_ranks(logits, ids):
    order = logits.argsort(-1, descending=True)
    full = torch.empty_like(order)
    full.scatter_(1, order, torch.arange(logits.shape[1]).expand_as(order))
    return full[:, ids]


def test_ranks_of_matches_argsort():
    logits = torch.randn(7, 100, generator=torch.Generator().manual_seed(0))  # continuous: no ties
    ids = [0, 5, 99, 42]
    assert torch.equal(ranks_of(logits, ids), _naive_ranks(logits, ids))


def test_ranks_of_ties_count_in_target_favour():
    logits = torch.tensor([[1.0, 1.0, 0.0]])
    assert ranks_of(logits, [0, 1, 2]).tolist() == [[0, 0, 2]]


def test_readout_matches_jlens_apply(model, lens):
    prompt = "abcde"
    ref, model_logits, ids = lens.apply(model, prompt)
    resid = residuals(model, ids, [*lens.source_layers, L - 1])
    for layer in lens.source_layers:
        torch.testing.assert_close(readout_logits(model, lens, resid[layer], layer), ref[layer])
    torch.testing.assert_close(readout_logits(model, None, resid[L - 1], L - 1), model_logits)


def test_logit_lens_matches_jlens_without_jacobian(model, lens):
    ref, _, ids = lens.apply(model, "abcde", use_jacobian=False)
    resid = residuals(model, ids, lens.source_layers)
    for layer in lens.source_layers:
        torch.testing.assert_close(readout_logits(model, None, resid[layer], layer), ref[layer])


def test_rank_grid_shape_and_positions(model, lens):
    ids = model.encode("abcde")
    resid = residuals(model, ids, lens.source_layers)
    full = rank_grid(model, lens, resid, lens.source_layers, [3, 7])
    last = rank_grid(model, lens, resid, lens.source_layers, [3, 7], positions=[-1])
    assert full.shape == (L - 1, SEQ, 2)
    assert torch.equal(last[:, 0], full[:, -1])


class _Tok:
    """Word-level fake tokenizer: known words are one token, the rest split per character."""

    vocab: ClassVar[dict[str, int]] = {" Brazil": 1, "Brazil": 2, " Portuguese": 3}

    def encode(self, text, add_special_tokens=False):
        if text in self.vocab:
            return [self.vocab[text]]
        return [100 + ord(c) for c in text]

    def decode(self, ids):
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv[i] if i in inv else chr(i - 100) for i in ids)


def test_word_tokens_both_single():
    w = word_tokens(_Tok(), "Brazil")
    assert w.ids == (1, 2) and w.single_token


def test_word_tokens_keeps_only_single_token_variants():
    w = word_tokens(_Tok(), "Portuguese")  # "Portuguese" alone would split into "P", "o", ...
    assert w.ids == (3,) and w.pieces == (" Portuguese",) and w.single_token


def test_continuation_first_token_respects_trailing_space():
    tok = _Tok()
    assert continuation_first_token(tok, "spoken is", "Portuguese") == 3  # " Portuguese"
    assert continuation_first_token(tok, "spoken is ", "Portuguese") == 100 + ord("P")  # "Port..." split


def test_word_tokens_falls_back_to_first_token():
    w = word_tokens(_Tok(), "Hungary")
    assert w.ids == (100 + ord(" "), 100 + ord("H")) and not w.single_token
