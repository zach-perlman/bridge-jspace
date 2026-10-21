"""Exact edge knock-out on Qwen3.5-family hybrid decoders (D2, Dan's depth track, 2026-10-20): "destinations D cannot
read sources S directly at layer l", per batch row, at any set of layers.

At every layer l in a row's layer set, everything else in the model untouched:
- full (gated softmax) attention: the logits of the pairs (d, s), d in D, s in S, are -inf in every head, so d's
  softmax renormalises over the keys it may still read; every other pair, and the output gate (a function of d's own
  input), as is.
- Gated DeltaNet: the token mixer runs a second time and that run's output replaces the normal one at D only (every
  other position keeps the normal output). The gated delta rule, state_t = a_t state_{t-1} (I - b_t k_t k_t^T) +
  b_t v_t k_t^T, is linear in the values: o_t = sum_j w_tj v_j, with weights w_tj that depend on queries, keys, betas
  and decays but not on values. mode="value" (default) removes exactly the s -> t terms: in the second run
    (i)  v_s = 0 for s in S (the value after the short conv), every key, beta and decay unchanged, so no weight w_tj
         changes (beta_s = 0 instead would also drop s's erase of earlier writes, which can restore an earlier,
         template-identical statement: not an edge removal);
    (ii) S's conv taps are dropped from the value channels: the depthwise causal conv (kernel 4) mixes x_s into the
         values of the next 3 tokens, which write to the state D reads; the conv's value-channel input is zeroed at S
         (the conv is linear and bias-free before its SiLU), so those values lose exactly x_s's terms and keep the rest.
  What S keeps in "value" mode: its weights, i.e. its own key, beta and decay (how much it erases and decays what came
  before it) and its taps in the next 3 tokens' keys and queries. No content (value) of S reaches D directly.
  mode="absent" (the positive control) removes S from the recurrence altogether: conv input zeroed at S in every
  channel, beta_s = 0 and decay a_s = 1 (g_s = 0). S then has no influence at all on D's layer-l output, as if its
  tokens were not in this layer's mixer (which also undoes S's erase of earlier writes).

Not blocked (by design): indirect routes. S -> p -> D through any position p outside D (later context sentences, the
instruction, ...) at the same or an earlier layer, and whatever S wrote into D's residual stream at a layer outside the
set. MLPs and norms act per position and carry nothing across positions; but the DeltaNet's per-head output RMSNorm
rescales D's output after the knock-out (it normalises each head's o_d): `norm_log` records ||o_d|| knocked / normal.

Never blocked: the first token (an attention sink; asserted). The second DeltaNet run is the module's own forward, with
the two kernel functions it calls (causal_conv1d_fn and torch_chunk_gated_delta_rule: flash-linear-attention's kernels
when installed, else transformers' torch reference) wrapped to change their inputs; per-token values, beta and g are
ordinary inputs of both paths. Only full, uncached forwards (prefill) are supported.
"""

from __future__ import annotations

import contextlib
import importlib.util
import sys
from collections.abc import Callable, Collection, Iterator, Sequence
from typing import Any

import torch
from torch import nn

MODES = ("value", "absent")
FULL, LINEAR = "full_attention", "linear_attention"


def decoder_layers(model: Any) -> nn.ModuleList:
    """The decoder blocks of a bridge_jspace Model (`.hf`), an HF causal LM, or a multimodal model's language model."""
    hf = getattr(model, "hf", model)
    inner = hf.model
    return getattr(inner, "language_model", inner).layers


def layer_kind(layer: nn.Module) -> str:
    """FULL for a block with softmax attention (`self_attn`), LINEAR for a Gated DeltaNet block (`linear_attn`)."""
    if hasattr(layer, "linear_attn"):
        return LINEAR
    if hasattr(layer, "self_attn"):
        return FULL
    raise TypeError(f"{type(layer).__name__}: neither self_attn nor linear_attn")


def layer_kinds(model: Any) -> list[str]:
    return [layer_kind(layer) for layer in decoder_layers(model)]


def kernel_path() -> str:
    """Which gated-delta-rule implementation transformers dispatches to: 'fla' when flash-linear-attention imports,
    else 'torch' (the reference). Mirrors transformers' own choice (import the package, else fall back)."""
    return "fla" if importlib.util.find_spec("fla") is not None else "torch"


def reference_chunk_rule(gdn: nn.Module) -> Callable:
    """transformers' torch reference of the chunked gated delta rule, unwrapped from the kernels-hub dispatcher (which
    sends calls to fla when it is installed): for comparing the two paths."""
    func = sys.modules[type(gdn).__module__].torch_chunk_gated_delta_rule
    for cell in type(func).forward.__closure__ or ():
        ref = getattr(cell.cell_contents, "__wrapped__", None)
        if ref is not None and ref.__name__ == "torch_chunk_gated_delta_rule":
            return ref
    raise RuntimeError("could not find the torch reference behind torch_chunk_gated_delta_rule")


def _per_row(layers: Collection[int] | Sequence[Collection[int]], n_rows: int) -> list[frozenset[int]]:
    items: list[Any] = list(layers)
    if all(isinstance(x, int) for x in items):  # one set for every row (an empty collection included)
        return [frozenset(int(x) for x in items)] * n_rows
    assert len(items) == n_rows, f"{len(items)} layer sets for {n_rows} rows"
    return [frozenset(int(x) for x in row) for row in items]


class _Masks:
    """Per-row boolean masks [rows, T] of the source and destination positions, built once per sequence length."""

    def __init__(self, src: list[list[int]], dst: list[list[int]]):
        self.src, self.dst = src, dst
        self._cache: dict[tuple[int, str], tuple[torch.Tensor, torch.Tensor]] = {}

    def get(self, length: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
        key = (length, str(device))
        if key not in self._cache:
            masks = []
            for positions in (self.src, self.dst):
                m = torch.zeros(len(positions), length, dtype=torch.bool)
                for row, pos in enumerate(positions):
                    assert not pos or max(pos) < length, f"row {row}: position {max(pos)} >= sequence length {length}"
                    m[row, pos] = True
                masks.append(m.to(device))
            self._cache[key] = (masks[0], masks[1])
        return self._cache[key]


@contextlib.contextmanager
def knock_out(
    model: Any,
    layers: Collection[int] | Sequence[Collection[int]],
    src_positions: Sequence[Collection[int]],
    dst_positions: Sequence[Collection[int]],
    mode: str = "value",
    norm_log: list[dict] | None = None,
    heads: Sequence[Collection[int] | None] | None = None,
) -> Iterator[None]:
    """Within the block, in every forward of a batch with len(src_positions) rows: for row r, at each layer in its set,
    positions dst_positions[r] cannot read src_positions[r] directly (module docstring). `layers` is one collection of
    layer indices for every row, or one per row. A row with an empty source or destination set is left as is (its
    forward is bit-for-bit the unhooked one, except that sdpa may pick another kernel for the batch's full-attention
    layers when another row is knocked out there). Sources and destinations of a row must be disjoint, and position 0
    is never a source. With `norm_log`, each knocked DeltaNet layer appends {"layer", "rows", "ratio"}: per knocked row,
    the mean over D and heads of ||o_d|| (second run) / ||o_d|| (normal run), before the per-head output RMSNorm.

    `heads` (one entry per row, None = every head): the query heads whose (D, S) logits are masked, in full-attention
    layers only (a row with heads may list no DeltaNet layer). The unit is the query head: with grouped-query attention
    several query heads share one key/value head, and masking one query head's logits leaves its group partners
    reading S; blocking a key/value group means listing all its query heads."""
    assert mode in MODES, mode
    n_rows = len(src_positions)
    assert len(dst_positions) == n_rows, "one destination set per source set"
    head_sets = [None if h is None else sorted({int(x) for x in h}) for h in (heads or [None] * n_rows)]
    assert len(head_sets) == n_rows, "one head set (or None) per row"
    src = [sorted({int(p) for p in s}) for s in src_positions]
    dst = [sorted({int(p) for p in d}) for d in dst_positions]
    for row, (s, d) in enumerate(zip(src, dst, strict=True)):
        assert not set(s) & set(d), f"row {row}: a position is both source and destination"
        assert all(p >= 0 for p in s + d), f"row {row}: negative position"
        assert 0 not in s, f"row {row}: the first token (attention sink) is never blocked"
    per_row = _per_row(layers, n_rows)
    blocks: Any = decoder_layers(model)
    for row, ls in enumerate(per_row):
        assert all(0 <= la < len(blocks) for la in ls), f"row {row}: layer outside 0..{len(blocks) - 1}"
        if head_sets[row] is not None:
            assert all(layer_kind(blocks[la]) == FULL for la in ls), f"row {row}: heads apply to full attention only"
            n_heads = blocks[next(iter(ls))].self_attn.config.num_attention_heads if ls else 0
            assert all(0 <= h < n_heads for h in head_sets[row] or []), f"row {row}: head outside 0..{n_heads - 1}"
    masks = _Masks(src, dst)
    handles = []
    try:
        for la, block in enumerate(blocks):
            rows = [r for r in range(n_rows) if la in per_row[r] and src[r] and dst[r]]
            if not rows:
                continue
            if layer_kind(block) == FULL:
                hook = _attention_hook(rows, masks, {r: head_sets[r] for r in rows})
                handles.append(block.self_attn.register_forward_pre_hook(hook, with_kwargs=True))
            else:
                gdn = block.linear_attn
                seen: dict[str, torch.Tensor] = {}
                if norm_log is not None:
                    handles.append(gdn.norm.register_forward_pre_hook(_keep_norm_input(seen)))
                hook = _deltanet_hook(la, rows, masks, mode, seen if norm_log is not None else None, norm_log)
                handles.append(gdn.register_forward_hook(hook, with_kwargs=True))
        yield
    finally:
        for handle in handles:
            handle.remove()


def _attention_hook(rows: list[int], masks: _Masks, head_sets: dict[int, list[int] | None]):
    per_head = any(h is not None for h in head_sets.values())

    def hook(module, args, kwargs):
        hs = kwargs["hidden_states"] if "hidden_states" in kwargs else args[0]
        batch, length = hs.shape[:2]
        src, dst = masks.get(length, hs.device)
        assert batch == src.shape[0], f"batch of {batch} rows, knock-out set up for {src.shape[0]}"
        if not per_head:
            idx = torch.tensor(rows, device=hs.device)
            block = torch.zeros(batch, 1, length, length, dtype=torch.bool, device=hs.device)
            block[idx, 0] = dst[idx, :, None] & src[idx, None, :]
        else:  # one mask per query head
            block = torch.zeros(batch, module.config.num_attention_heads, length, length, dtype=torch.bool,
                                device=hs.device)  # fmt: skip
            for r in rows:
                pair = dst[r, :, None] & src[r, None, :]
                which = head_sets[r]
                if which is None:
                    block[r] = pair
                else:
                    block[r, which] = pair
        kwargs["attention_mask"] = _blocked_mask(kwargs.get("attention_mask"), block, hs.dtype, module)
        return args, kwargs

    return hook


def _blocked_mask(mask: torch.Tensor | None, block: torch.Tensor, dtype: torch.dtype, module: Any):
    """The layer's attention mask with the blocked pairs removed: boolean (True = may attend) for sdpa, additive for
    eager. With no incoming mask (sdpa's causal fast path) the causal mask is built here."""
    length = block.shape[-1]
    impl = module.config._attn_implementation
    assert impl in ("sdpa", "eager"), f"knock_out needs sdpa or eager attention, not {impl}"
    if mask is None:
        keep = torch.ones(length, length, dtype=torch.bool, device=block.device).tril() & ~block
        if impl == "sdpa":
            return keep
        return torch.zeros(keep.shape, dtype=dtype, device=block.device).masked_fill(~keep, torch.finfo(dtype).min)
    assert mask.shape[-1] == mask.shape[-2] == length, "knock_out supports uncached forwards only"
    if mask.dtype == torch.bool:
        return mask & ~block
    return mask.expand(block.shape[0], block.shape[1], -1, -1).masked_fill(block, torch.finfo(mask.dtype).min)


def _keep_norm_input(seen: dict[str, torch.Tensor]):
    def hook(_module, args):
        seen["x"] = args[0]

    return hook


def _deltanet_hook(layer: int, rows: list[int], masks: _Masks, mode: str, seen: Any, norm_log: Any):
    def hook(module, args, kwargs, out):
        assert not args, "Gated DeltaNet called with positional arguments"
        assert kwargs.get("cache_params") is None, "knock_out supports uncached forwards only"
        hs = kwargs["hidden_states"]
        batch, length = hs.shape[:2]
        src, dst = masks.get(length, hs.device)
        assert batch == src.shape[0], f"batch of {batch} rows, knock-out set up for {src.shape[0]}"
        idx = torch.tensor(rows, device=hs.device)
        normal = seen["x"].reshape(batch, length, -1, module.head_v_dim)[idx] if seen is not None else None
        sub = dict(kwargs, hidden_states=hs[idx])
        if kwargs.get("attention_mask") is not None:  # a 2D padding mask
            sub["attention_mask"] = kwargs["attention_mask"][idx]
        with _without_sources(module, src[idx], mode):
            out2 = module.forward(**sub)
        if normal is not None and seen is not None:
            knocked = seen["x"].reshape(len(rows), length, -1, module.head_v_dim)
            ratio = knocked.float().norm(dim=-1) / normal.float().norm(dim=-1).clamp_min(1e-12)  # [rows, T, heads]
            d = dst[idx].float()
            per_row = (ratio.mean(-1) * d).sum(-1) / d.sum(-1)
            norm_log.append({"layer": layer, "rows": rows, "ratio": per_row.tolist()})
        merged = out.clone()
        merged[idx] = torch.where(dst[idx, :, None], out2, out[idx])
        return merged

    return hook


@contextlib.contextmanager
def _without_sources(gdn: Any, src: torch.Tensor, mode: str) -> Iterator[None]:
    """While active, the Gated DeltaNet module's kernels see S removed (module docstring). src: [rows, T] bool."""
    ns: Any = sys.modules[type(gdn).__module__]
    conv, rule = ns.causal_conv1d_fn, ns.torch_chunk_gated_delta_rule
    first_value_channel = 2 * gdn.key_dim  # mixed_qkv's channels: queries, keys, values
    calls = {"conv": 0, "rule": 0}

    def conv_without(x: torch.Tensor, *args, **kwargs):  # x: [rows, channels, T], the conv's input
        calls["conv"] += 1
        drop = src[:, None, :].expand(-1, x.shape[1], -1).clone()
        if mode == "value":
            drop[:, :first_value_channel] = False
        return conv(x.masked_fill(drop, 0), *args, **kwargs)

    def rule_without(query, key, value, *args, g: torch.Tensor, beta: torch.Tensor, **kwargs):
        calls["rule"] += 1  # query, key: [rows, T, heads, dk]; value: [rows, T, heads, dv]; g, beta: [rows, T, heads]
        if mode == "value":
            value = value.masked_fill(src[:, :, None, None], 0)
        else:
            g, beta = g.masked_fill(src[:, :, None], 0.0), beta.masked_fill(src[:, :, None], 0)
        return rule(query, key, value, *args, g=g, beta=beta, **kwargs)

    ns.causal_conv1d_fn, ns.torch_chunk_gated_delta_rule = conv_without, rule_without
    try:
        yield
    finally:
        ns.causal_conv1d_fn, ns.torch_chunk_gated_delta_rule = conv, rule
    assert calls == {"conv": 1, "rule": 1}, f"the Gated DeltaNet forward did not call its kernels once each: {calls}"


@torch.no_grad()
def attention_probs(model: Any, input_ids: torch.Tensor, layers: Collection[int], q_positions: Sequence[int]):
    """Each listed full-attention layer's softmax attention, per query head, from the query positions to every key
    position, in one unedited forward: {layer: [batch, heads, len(q_positions), T]} (fp32). Recomputed from the layer's
    own inputs (query projection without its gate half, per-head norms, rotary embedding, the scaling, causal softmax),
    so the forward itself keeps its attention implementation; tests check it against eager attention weights."""
    hf = getattr(model, "hf", model)
    out: dict[int, torch.Tensor] = {}
    with capture_attention(model, layers, q_positions, out):
        hf(input_ids=input_ids, use_cache=False, logits_to_keep=1)
    return out


@contextlib.contextmanager
def capture_attention(
    model: Any, layers: Collection[int], q_positions: Sequence[int], out: dict[int, torch.Tensor]
) -> Iterator[None]:
    """While active, every forward fills `out` as attention_probs returns it, for whatever else the forward does
    (e.g. residual edits by other hooks: the attention is then the edited forward's)."""
    blocks: Any = decoder_layers(model)

    def hook_for(la: int):
        def hook(module, args, kwargs):
            hs = kwargs["hidden_states"] if "hidden_states" in kwargs else args[0]
            cos, sin = kwargs["position_embeddings"]
            ns: Any = sys.modules[type(module).__module__]
            shape = (*hs.shape[:-1], -1, module.head_dim)
            q, _gate = torch.chunk(module.q_proj(hs).view(*hs.shape[:-1], -1, module.head_dim * 2), 2, dim=-1)
            q = module.q_norm(q.reshape(shape)).transpose(1, 2)
            k = module.k_norm(module.k_proj(hs).view(shape)).transpose(1, 2)
            q, k = ns.apply_rotary_pos_emb(q, k, cos, sin)
            k = ns.repeat_kv(k, module.num_key_value_groups)
            qp = torch.tensor(list(q_positions), device=hs.device)
            scores = (q[:, :, qp].float() @ k.float().transpose(-1, -2)) * module.scaling
            future = torch.arange(hs.shape[1], device=hs.device)[None, :] > qp[:, None]
            out[la] = scores.masked_fill(future, float("-inf")).softmax(-1)

        return hook

    handles = []
    for la in layers:
        assert layer_kind(blocks[la]) == FULL, f"layer {la} is not a full-attention layer"
        handles.append(blocks[la].self_attn.register_forward_pre_hook(hook_for(la), with_kwargs=True))
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()
