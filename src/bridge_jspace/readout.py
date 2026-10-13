"""Lens readouts that keep only the ranks of chosen tokens.

A reader is a fitted `JacobianLens` (J-lens or J++, same file format) or `None` for the logit
lens (raw residual straight into final norm + unembed). Full [layers x positions x vocab] logits
are never kept: on Qwen3.6-27B that is gigabytes per prompt.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import torch
from jlens import ActivationRecorder, JacobianLens, LensModel

Reader = JacobianLens | None


@dataclass(frozen=True)
class WordTokens:
    """Token ids that count as the lens "saying" `word`.

    Surface variants are `" word"` and `"word"`. If any variant is a single token, only the
    single-token variants count; otherwise the first non-whitespace token of each variant counts and
    `single_token` is False (a fragment like "Port" or the digit "2" for "26" is weak evidence).
    Whitespace-only pieces are skipped: Qwen splits " 26" into " ", "2", "6", and the rank of a bare
    " " says nothing about the number.
    """

    word: str
    ids: tuple[int, ...]
    pieces: tuple[str, ...]  # decoded `ids`, for a human to check
    single_token: bool


def word_tokens(tokenizer, word: str) -> WordTokens:
    encoded = [tokenizer.encode(v, add_special_tokens=False) for v in (" " + word, word)]
    encoded = [e for e in encoded if e]
    if not encoded:
        raise ValueError(f"{word!r} encodes to no tokens")
    single = [e[0] for e in encoded if len(e) == 1]
    ids = tuple(dict.fromkeys(single or [_first_content_token(tokenizer, e) for e in encoded]))
    pieces = tuple(tokenizer.decode([i]) for i in ids)
    return WordTokens(word=word, ids=ids, pieces=pieces, single_token=bool(single))


def _first_content_token(tokenizer, ids: list[int]) -> int:
    return next((i for i in ids if tokenizer.decode([i]).strip()), ids[0])


def continuation_first_token(tokenizer, prompt: str, word: str) -> int:
    """First token of `word` as the continuation of `prompt`: with a leading space unless the prompt
    already ends in whitespace (then e.g. "Portuguese" -> "Port", not " Portuguese")."""
    text = word if prompt[-1:].isspace() else " " + word
    return tokenizer.encode(text, add_special_tokens=False)[0]


@torch.no_grad()
def residuals(model: LensModel, input_ids: torch.Tensor, layers: Sequence[int]) -> dict[int, torch.Tensor]:
    """Block outputs `{layer: [seq, d_model]}` for a single prompt (`input_ids` is [1, seq])."""
    with ActivationRecorder(model.layers, at=layers) as rec:
        model.forward(input_ids)
        return {layer: rec.activations[layer][0].detach() for layer in layers}


@torch.no_grad()
def readout_logits(model: LensModel, reader: Reader, residual: torch.Tensor, layer: int) -> torch.Tensor:
    """`[..., vocab]` float logits of `reader` applied to `residual` taken at `layer`."""
    h = residual.float()
    if reader is not None:
        h = reader.transport(h, layer)
    return model.unembed(h).float()


def ranks_of(logits: torch.Tensor, token_ids: Sequence[int]) -> torch.Tensor:
    """`[n, len(token_ids)]` ranks of `token_ids` in `logits` [n, vocab]; 0 = top-1.

    Rank = number of tokens with a strictly larger logit (ties count in the target's favour).
    """
    return torch.stack([(logits > logits[:, [t]]).sum(-1) for t in token_ids], dim=-1)


@torch.no_grad()
def rank_grid(
    model: LensModel,
    reader: Reader,
    resid: dict[int, torch.Tensor],
    layers: Sequence[int],
    token_ids: Sequence[int],
    positions: Sequence[int] | None = None,
) -> torch.Tensor:
    """`[len(layers), n_positions, len(token_ids)]` ranks on CPU (all positions if `positions` is None)."""
    out = []
    for layer in layers:
        h = resid[layer] if positions is None else resid[layer][list(positions)]
        out.append(ranks_of(readout_logits(model, reader, h, layer), token_ids).cpu())
    return torch.stack(out)
