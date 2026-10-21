"""bridge_jspace.knockout: the exact edge knock-out (D2).

Unit tests run on a tiny random Qwen3.5 hybrid (8 layers: 3 Gated DeltaNet + 1 full attention, twice; fp32, no
download) against naive fp64 references written from the equations, not from transformers' code. Model tests
(`pytest -m model`) run on Qwen3.5-0.8B in fp32 (CUDA if available, where the DeltaNet kernels are fla's; CPU otherwise,
torch reference kernels).

Tolerances (fp32 throughout): untouched rows/positions are compared bit for bit where the code path is the same. With
flash-linear-attention installed (the GPU box) every model runs on CUDA (fla's triton kernels need it), where fla's
chunked kernels and sdpa's masked-vs-causal kernels differ from exact fp32 at ~1e-3: ABS (absolute, logits of
positions the knock-out cannot reach, context independence) is 1e-5 on CPU and 1e-2 on CUDA; REL (relative, knocked
outputs vs the fp64 references) is 1e-4 on CPU and 5e-3 on CUDA. Every test also asserts the effect it checks against
is far above these (knocked D outputs move by > 1e-3 relative, logits at D by > 0.1).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pytest
import torch
import torch.nn.functional as F
import yaml

from bridge_jspace.knockout import FULL, LINEAR, attention_probs, decoder_layers, knock_out, layer_kinds

TYPES = [LINEAR, LINEAR, LINEAR, FULL] * 2
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
ABS = 1e-5 if DEVICE == "cpu" else 1e-2
REL = 1e-4 if DEVICE == "cpu" else 5e-3


def tiny_model(impl: str = "sdpa", seed: int = 0):
    from transformers import Qwen3_5TextConfig
    from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5ForCausalLM

    cfg = Qwen3_5TextConfig(
        vocab_size=61,
        hidden_size=32,
        intermediate_size=48,
        num_hidden_layers=len(TYPES),
        layer_types=TYPES,
        num_attention_heads=4,
        num_key_value_heads=2,
        head_dim=8,
        linear_num_key_heads=2,
        linear_num_value_heads=4,
        linear_key_head_dim=8,
        linear_value_head_dim=6,
        linear_conv_kernel_dim=4,
        max_position_embeddings=128,
    )
    cfg._attn_implementation = impl
    torch.manual_seed(seed)
    model = Qwen3_5ForCausalLM(cfg).eval()
    # Default init leaves activations tiny; scale every weight so that each part of the layer matters numerically.
    g = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        for name, p in model.named_parameters():
            if name.endswith(("A_log", "dt_bias")):
                continue
            noise = torch.randn(p.shape, generator=g)
            if p.ndim >= 2:
                p.copy_(noise / math.sqrt(p.shape[-1]))
            else:
                p.copy_((1.0 if name.endswith("linear_attn.norm.weight") else 0.0) + 0.3 * noise)
    moved: Any = model
    return moved.to(DEVICE)


def ids_for(seed: int, length: int, batch: int = 1) -> torch.Tensor:
    return torch.randint(0, 61, (batch, length), generator=torch.Generator().manual_seed(seed)).to(DEVICE)


def cpu64(t: torch.Tensor) -> torch.Tensor:
    return t.detach().double().cpu()


def naive_deltanet(mod, x: torch.Tensor, src: set[int], mode: str = "value") -> torch.Tensor:
    """One Gated DeltaNet token mixer in fp64, step by step, from its equations: x [T, d] (the block's normed input)
    -> [T, d]. mode 'value': S's values are zero (v_s = 0 after the conv; its key, beta and decay kept, so it still
    erases) and S's conv taps are dropped from the value channels only; mode 'absent': S's conv input is zero in
    every channel and S neither writes, erases nor decays."""

    def f(t):
        return cpu64(t)

    x = f(x)
    length = x.shape[0]
    u = x @ f(mod.in_proj_qkv.weight).T
    first = 2 * mod.key_dim if mode == "value" else 0
    u[sorted(src), first:] = 0
    w = f(mod.conv1d.weight).squeeze(1)
    k_size = w.shape[1]
    c = torch.zeros_like(u)
    for t in range(length):
        for j in range(k_size):
            p = t - (k_size - 1 - j)
            if p >= 0:
                c[t] += w[:, j] * u[p]
    c = F.silu(c)
    q, k, v = c.split([mod.key_dim, mod.key_dim, mod.value_dim], dim=-1)
    rep = mod.num_v_heads // mod.num_k_heads
    q = q.reshape(length, mod.num_k_heads, mod.head_k_dim).repeat_interleave(rep, dim=1)
    k = k.reshape(length, mod.num_k_heads, mod.head_k_dim).repeat_interleave(rep, dim=1)
    v = v.reshape(length, mod.num_v_heads, mod.head_v_dim).clone()
    if mode == "value":
        v[sorted(src)] = 0

    def l2(z):
        return z / torch.sqrt((z * z).sum(-1, keepdim=True) + 1e-6)

    q, k = l2(q) * mod.head_k_dim**-0.5, l2(k)
    beta = torch.sigmoid(x @ f(mod.in_proj_b.weight).T)
    g = -f(mod.A_log).exp() * F.softplus(x @ f(mod.in_proj_a.weight).T + f(mod.dt_bias))
    if mode == "absent":
        g[sorted(src)] = 0
    o = torch.zeros(length, mod.num_v_heads, mod.head_v_dim, dtype=torch.float64)
    for h in range(mod.num_v_heads):
        state = torch.zeros(mod.head_k_dim, mod.head_v_dim, dtype=torch.float64)
        for t in range(length):
            state = state * g[t, h].exp()
            if mode == "value" or t not in src:
                delta = beta[t, h] * (v[t, h] - state.T @ k[t, h])
                state = state + torch.outer(k[t, h], delta)
            o[t, h] = state.T @ q[t, h]
    z = (x @ f(mod.in_proj_z.weight).T).reshape(length, mod.num_v_heads, mod.head_v_dim)
    o = o * torch.rsqrt(o.pow(2).mean(-1, keepdim=True) + mod.norm.variance_epsilon) * f(mod.norm.weight) * F.silu(z)
    return o.reshape(length, -1) @ f(mod.out_proj.weight).T


def naive_attention(mod, x, cos, sin, src: list[int], dst: list[int], heads: list[int] | None = None) -> torch.Tensor:
    """Qwen3.5's gated full attention in fp64 from its equations, with the (dst, src) logits at -inf in the listed
    query heads (all heads when None). x [T, d]."""

    def f(t):
        return cpu64(t)

    assert mod.q_proj.bias is None
    x, cos, sin = f(x), f(cos), f(sin)
    length, hd = x.shape[0], mod.head_dim
    n_heads, n_kv = mod.config.num_attention_heads, mod.config.num_key_value_heads
    qg = (x @ f(mod.q_proj.weight).T).reshape(length, n_heads, 2 * hd)
    q, gate = qg[..., :hd], qg[..., hd:].reshape(length, n_heads * hd)

    def rms(z, norm):
        return z * torch.rsqrt(z.pow(2).mean(-1, keepdim=True) + norm.eps) * (1 + f(norm.weight))

    q = rms(q, mod.q_norm)
    k = rms((x @ f(mod.k_proj.weight).T).reshape(length, n_kv, hd), mod.k_norm)
    v = (x @ f(mod.v_proj.weight).T).reshape(length, n_kv, hd)
    rot = cos.shape[-1]

    def rope(z):
        zr, zp = z[..., :rot], z[..., rot:]
        half = torch.cat([-zr[..., rot // 2 :], zr[..., : rot // 2]], dim=-1)
        return torch.cat([zr * cos[:, None, :] + half * sin[:, None, :], zp], dim=-1)

    q, k = rope(q), rope(k)
    causal = torch.ones(length, length, dtype=torch.bool).tril()
    keep = causal.clone()
    for d in dst:
        for s in src:
            keep[d, s] = False
    out = torch.zeros(length, n_heads, hd, dtype=torch.float64)
    groups = n_heads // n_kv
    for h in range(n_heads):
        scores = (q[:, h] @ k[:, h // groups].T) * hd**-0.5
        mask = keep if heads is None or h in heads else causal
        out[:, h] = scores.masked_fill(~mask, float("-inf")).softmax(-1) @ v[:, h // groups]
    return (out.reshape(length, -1) * torch.sigmoid(gate)) @ f(mod.o_proj.weight).T


class Capture:
    """Inputs (kwargs) and outputs of one module during a forward."""

    def __init__(self, module):
        self.module = module
        self.kwargs: Any = None
        self.out: Any = None

    def __enter__(self):
        self.handles = [
            self.module.register_forward_pre_hook(self._pre, with_kwargs=True),
            self.module.register_forward_hook(self._post, with_kwargs=True),
        ]
        return self

    def _pre(self, _m, _args, kwargs):
        self.kwargs = dict(kwargs)

    def _post(self, _m, _args, _kwargs, out):
        self.out = out[0] if isinstance(out, tuple) else out

    def __exit__(self, *exc):
        for h in self.handles:
            h.remove()


def logits(model, ids):
    with torch.no_grad():
        return model(input_ids=ids, use_cache=False).logits


# ---- unit tests (tiny random model, no download) ---------------------------------------------------------------------


def test_layer_kinds_of_tiny_model():
    assert layer_kinds(tiny_model()) == TYPES


@pytest.mark.parametrize("empty", ["src", "dst"])
def test_noop_empty_sets_is_bit_exact(empty):
    model = tiny_model()
    ids = ids_for(1, 23, batch=2)
    ref = logits(model, ids)
    some = [[3, 4, 5], [10, 11]]
    none: list[list[int]] = [[], []]
    src, dst = (none, some) if empty == "src" else (some, none)
    with knock_out(model, range(len(TYPES)), src, dst):
        got = logits(model, ids)
    assert torch.equal(got, ref)


@pytest.mark.parametrize("mode", ["value", "absent"])
def test_deltanet_matches_naive_fp64(mode):
    """The knocked DeltaNet output equals the step-by-step fp64 reference at D, and the normal output elsewhere. D
    starts right after S (inside the conv's reach), so the conv-tap removal is exercised; T = 70 spans two 64-token
    chunks of the chunked kernel."""
    model = tiny_model()
    layer = 1
    mod = decoder_layers(model)[layer].linear_attn
    ids = ids_for(2, 70, batch=2)
    src = [[20, 21, 22, 23, 24], [60, 61]]
    dst = [[25, 26, 40, 69], [62, 63, 66]]
    with Capture(mod) as plain:
        logits(model, ids)
    with knock_out(model, [layer], src, dst, mode=mode), Capture(mod) as hooked:
        logits(model, ids)
    x = plain.kwargs["hidden_states"]
    assert torch.equal(hooked.kwargs["hidden_states"], x)  # the first knocked layer's input is untouched
    for row in range(2):
        ref_plain = naive_deltanet(mod, x[row], set())
        ref_knock = naive_deltanet(mod, x[row], set(src[row]), mode)
        scale = ref_plain.abs().max()
        assert (cpu64(plain.out[row]) - ref_plain).abs().max() / scale < REL  # the reference is the layer
        d = dst[row]
        assert (cpu64(hooked.out[row, d]) - ref_knock[d]).abs().max() / scale < REL
        assert (ref_knock[d] - ref_plain[d]).abs().max() / scale > 1e-3  # the knock-out changed D's output
        rest = [t for t in range(70) if t not in d]
        assert torch.equal(hooked.out[row, rest], plain.out[row, rest])


@pytest.mark.parametrize("impl", ["sdpa", "eager"])
def test_full_attention_matches_naive_fp64(impl):
    model = tiny_model(impl)
    layer = 3
    mod = decoder_layers(model)[layer].self_attn
    ids = ids_for(3, 30, batch=2)
    src = [[5, 6, 7], [1, 12]]
    dst = [[20, 29], [13, 14, 15]]
    with Capture(mod) as plain:
        logits(model, ids)
    with knock_out(model, [layer], src, dst), Capture(mod) as hooked:
        logits(model, ids)
    x = plain.kwargs["hidden_states"]
    cos, sin = plain.kwargs["position_embeddings"]
    for row in range(2):
        ref_knock = naive_attention(mod, x[row], cos[row], sin[row], src[row], dst[row])
        ref_plain = naive_attention(mod, x[row], cos[row], sin[row], [], [])
        scale = ref_plain.abs().max()
        assert (cpu64(plain.out[row]) - ref_plain).abs().max() / scale < REL
        assert (cpu64(hooked.out[row]) - ref_knock).abs().max() / scale < REL
        assert (ref_knock[dst[row]] - ref_plain[dst[row]]).abs().max() / scale > 1e-3


@pytest.mark.parametrize("impl", ["sdpa", "eager"])
def test_per_head_mask_matches_naive_fp64(impl):
    """Blocking only some query heads (the unit under grouped-query attention: the tiny model has 4 query heads on 2
    key/value heads) equals the fp64 reference with the (D, S) logits masked in those heads alone; a row with heads
    None blocks every head, as before."""
    model = tiny_model(impl)
    layer = 3
    mod = decoder_layers(model)[layer].self_attn
    ids = ids_for(10, 30, batch=3)
    src = [[5, 6, 7], [1, 12], [8, 9]]
    dst = [[20, 29], [13, 14, 15], [25]]
    heads = [[1], [0, 3], None]
    with Capture(mod) as plain:
        logits(model, ids)
    with knock_out(model, [layer], src, dst, heads=heads), Capture(mod) as hooked:
        logits(model, ids)
    x = plain.kwargs["hidden_states"]
    cos, sin = plain.kwargs["position_embeddings"]
    for row in range(3):
        ref = naive_attention(mod, x[row], cos[row], sin[row], src[row], dst[row], heads[row])
        everyone = naive_attention(mod, x[row], cos[row], sin[row], src[row], dst[row])
        scale = ref.abs().max()
        assert (cpu64(hooked.out[row]) - ref).abs().max() / scale < REL
        if heads[row] is not None:  # blocking some heads is not blocking all of them
            assert (ref[dst[row]] - everyone[dst[row]]).abs().max() / scale > 1e-3


def test_heads_only_on_full_attention():
    model = tiny_model()
    with pytest.raises(AssertionError), knock_out(model, [0], [[2]], [[5]], heads=[[0]]):
        pass
    with pytest.raises(AssertionError), knock_out(model, [3], [[2]], [[5]], heads=[[4]]):  # 4 query heads: 0-3
        pass


def test_attention_probs_matches_eager_weights():
    """The readout's attention (recomputed from the layer inputs) equals eager attention's own weights."""
    model = tiny_model("eager")
    ids = ids_for(11, 26, batch=2)
    q_pos = [25, 24, 10]
    got = attention_probs(model, ids, [3, 7], q_pos)
    for layer in (3, 7):
        mod: Any = decoder_layers(model)[layer].self_attn
        seen: dict = {}

        def keep(_m, _a, _k, out, seen=seen):
            seen["w"] = out[1]

        handle = mod.register_forward_hook(keep, with_kwargs=True)
        try:
            with torch.no_grad():
                model(input_ids=ids, use_cache=False, output_attentions=True)
        finally:
            handle.remove()
        ref = seen["w"][:, :, q_pos, :].float()
        assert (got[layer] - ref).abs().max() < ABS
        assert torch.allclose(got[layer].sum(-1), torch.ones_like(got[layer].sum(-1)), atol=1e-5)


def test_causality_nothing_before_min_dst_changes():
    model = tiny_model()
    ids = ids_for(4, 40, batch=3)
    src = [[2, 3, 4, 5], [10, 11], [30]]
    dst = [[17, 18, 30], [12, 39], [33, 34]]
    per_row_layers = [range(8), [0, 3, 5], [4, 7]]
    ref = logits(model, ids)
    with knock_out(model, per_row_layers, src, dst):
        got = logits(model, ids)
    for row in range(3):
        first = min(dst[row])
        assert (got[row, :first] - ref[row, :first]).abs().max() < ABS
        assert (got[row, first:] - ref[row, first:]).abs().max() > 3 * ABS  # row 3: one source token, two layers


def test_positive_control_last_position_reads_nothing():
    """Every position but the first and the last blocked from the last at every layer (mode 'absent'): the last
    position's output depends on its own token and the first only, so two prompts that share those give the same last
    logits. (Mode 'value' leaves S's keys, betas and decays, which scale how much of the first token's value survives
    in the DeltaNet state: test_value_mode_keeps_the_weights_absent_mode_removes_everything.)"""
    mode = "absent"
    model = tiny_model()
    a, b = ids_for(5, 33), ids_for(6, 33)
    b[0, 0], b[0, -1] = a[0, 0], a[0, -1]
    assert not torch.equal(a, b)
    src, dst = [list(range(1, 32))], [[32]]
    with knock_out(model, range(8), src, dst, mode=mode):
        la, lb = logits(model, a)[0, -1], logits(model, b)[0, -1]
    assert (la - lb).abs().max() < ABS
    assert (logits(model, a)[0, -1] - logits(model, b)[0, -1]).abs().max() > 10 * ABS  # unhooked: context matters


def test_value_mode_keeps_the_weights_absent_mode_removes_everything():
    """S in the middle, D = every later position, all layers: with mode 'absent' the outputs after S do not depend on
    S's tokens at all; with mode 'value' they do, through the DeltaNet weights alone (S's key, beta and decay, and its
    taps in the next tokens' keys and queries), since attention and every value of S are blocked."""
    model = tiny_model()
    a = ids_for(7, 36)
    b = a.clone()
    b[0, 12:18] = ids_for(8, 6)[0]
    src, dst = [list(range(12, 18))], [list(range(18, 36))]
    out = {}
    for mode in ("value", "absent"):
        with knock_out(model, range(8), src, dst, mode=mode):
            out[mode] = (logits(model, a)[0, 18:] - logits(model, b)[0, 18:]).abs().max()
    assert out["absent"] < ABS
    assert out["value"] > 10 * ABS


def test_rejects_overlapping_sets_and_bad_layers():
    model = tiny_model()
    with pytest.raises(AssertionError), knock_out(model, [0], [[1, 2]], [[2, 3]]):
        pass
    with pytest.raises(AssertionError), knock_out(model, [8], [[1]], [[3]]):
        pass
    with pytest.raises(AssertionError), knock_out(model, [0], [[0, 1]], [[3]]):  # the first token is never blocked
        pass


# ---- model tests (Qwen3.5-0.8B, fp32) --------------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
PROMPT = "Jack's pet is a cow. Anna's pet is a dog. The cow's locker is 5. The dog's locker is 7.\nWhich locker belongs to Jack's pet? Answer:"
OTHER = "Jack's pet is a pig. Rose's pet is a cat. The pig's locker is 9. The cat's locker is 3.\nWhich locker belongs to Jack's pet? Answer:"


@pytest.fixture(scope="module")
def small():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    cfg = yaml.safe_load((ROOT / "configs/models/qwen3.5-0.8b.yaml").read_text())
    device = "cuda" if torch.cuda.is_available() else "cpu"  # with fla installed, CPU forwards fail (test_model.py)
    tok = AutoTokenizer.from_pretrained(cfg["name"], revision=cfg["revision"])
    hf = AutoModelForCausalLM.from_pretrained(
        cfg["name"], revision=cfg["revision"], dtype=torch.float32, device_map=device, attn_implementation="sdpa"
    ).eval()
    return hf, tok


def encode(tok, text, device):
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    return torch.tensor([enc.input_ids], device=device), enc.offset_mapping


def char_span(offsets, text, phrase) -> list[int]:
    a = text.index(phrase)
    b = a + len(phrase)
    return [i for i, (s, e) in enumerate(offsets) if s < b and e > a]


@pytest.mark.model
def test_small_layer_kinds(small):
    hf, _ = small
    kinds = layer_kinds(hf)
    assert len(kinds) == 24
    assert [i for i, k in enumerate(kinds) if k == FULL] == list(range(3, 24, 4))


@pytest.mark.model
def test_small_noop_is_bit_exact(small):
    hf, tok = small
    ids, _ = encode(tok, PROMPT, hf.device)
    ref = logits(hf, ids)
    with knock_out(hf, range(24), [[]], [[5, 6, 7]]):
        got = logits(hf, ids)
    assert torch.equal(got, ref)


@pytest.mark.model
def test_small_causality(small):
    hf, tok = small
    ids, offsets = encode(tok, PROMPT, hf.device)
    src = char_span(offsets, PROMPT, "The cow's locker is 5.")
    dst = char_span(offsets, PROMPT, "Which locker belongs to Jack's pet? Answer:")
    ref = logits(hf, ids)[0]
    with knock_out(hf, range(24), [src], [dst]):
        got = logits(hf, ids)[0]
    first = min(dst)
    before = (got[:first] - ref[:first]).abs().max().item()
    after = (got[first:] - ref[first:]).abs().max().item()
    print(f"0.8B causality: max |dlogit| before min(D) {before:.2e}, from min(D) on {after:.2e}")
    assert before < ABS
    assert after > 100 * ABS


@pytest.mark.model
def test_small_positive_control(small):
    """Blocking every token but the first from the last position at every layer makes the last logits independent of
    the context (a prompt with other context tokens, same length, same first and last token)."""
    hf, tok = small
    a, _ = encode(tok, PROMPT, hf.device)
    b, _ = encode(tok, OTHER, hf.device)
    assert a.shape == b.shape and a[0, 0] == b[0, 0] and a[0, -1] == b[0, -1] and not torch.equal(a, b)
    n = a.shape[1]
    with knock_out(hf, range(24), [list(range(1, n - 1))], [[n - 1]], mode="absent"):
        diff = (logits(hf, a)[0, -1] - logits(hf, b)[0, -1]).abs().max().item()
    plain = (logits(hf, a)[0, -1] - logits(hf, b)[0, -1]).abs().max().item()
    print(f"0.8B positive control: max |dlogit| knocked {diff:.2e}, unhooked {plain:.2e}")
    assert diff < ABS
    assert plain > 100 * ABS


@pytest.mark.model
@pytest.mark.parametrize("layer", [0, 12])
def test_small_deltanet_matches_naive_fp64(small, layer):
    """On real weights (fla's kernels on CUDA): the knocked DeltaNet output at D vs the fp64 reference."""
    hf, tok = small
    ids, offsets = encode(tok, PROMPT, hf.device)
    src = char_span(offsets, PROMPT, "The cow's locker is 5.")
    dst = char_span(offsets, PROMPT, "\nWhich locker")  # right after S: inside the conv's reach
    mod = decoder_layers(hf)[layer].linear_attn
    with knock_out(hf, [layer], [src], [dst]), Capture(mod) as hooked:
        logits(hf, ids)
    x = hooked.kwargs["hidden_states"][0]
    ref = naive_deltanet(mod, x, set(src))
    plain = naive_deltanet(mod, x, set())
    scale = plain.abs().max()
    err = ((cpu64(hooked.out[0, dst]) - ref[dst]).abs().max() / scale).item()
    moved = ((ref[dst] - plain[dst]).abs().max() / scale).item()
    print(f"0.8B layer {layer}: knocked vs fp64 reference rel err {err:.2e} (knock-out moved D by {moved:.2e})")
    assert err < REL
    assert moved > 10 * err
