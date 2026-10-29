"""Part B's target model (pins.TARGET: Qwen3.6-27B by default, or Gemma 4 31B-it): loading, raw-text forwards with
per-layer residual edits, word ranks, greedy continuations.

Conventions
- "Layer l" is the output of decoder block l (the J-lens's source convention), for l in 0..n_layers - 2.
- Prompts are raw text, no chat template, as in the jlens reference code; a target that needs a BOS gets it first
  (tokens.raw_encoding).
- Word rank: the rank of the best candidate id after formatting tokens (no letter or digit, special and added tokens)
  are removed from the distribution, as in the reference swap runner.
"""

import contextlib
import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import torch
from huggingface_hub import snapshot_download

from . import pins, tokens

# An edit gets the block output at one layer, [seq, d] fp32, and returns the edited residual.
Edit = Callable[[torch.Tensor], torch.Tensor]

_HAS_LETTER_OR_DIGIT = re.compile(r"[^\W_]")
_HAS_LETTER = re.compile(r"[^\W\d_]")


@dataclass
class Model:
    hf: Any  # transformers' Qwen3_5ForCausalLM or Gemma4ForConditionalGeneration: untyped submodule access
    tokenizer: Any
    decoded: list[str]  # decode of every id in the lm_head's vocabulary
    special_ids: frozenset[int]  # special and added tokens
    formatting_mask: torch.Tensor  # [vocab] bool, cuda: True for formatting tokens

    @property
    def text(self):
        """The text decoder (its layers and final norm): hf.model, or a multimodal model's hf.model.language_model."""
        return getattr(self.hf.model, "language_model", self.hf.model)

    @property
    def layers(self):
        return self.text.layers

    @property
    def final_norm(self):
        """The norm before the lm_head: text.norm, or NemotronH's text.norm_f (2026-10-25)."""
        return self.text.norm if hasattr(self.text, "norm") else self.text.norm_f

    def encode(self, text: str) -> torch.Tensor:
        return torch.tensor([tokens.raw_encoding(self.tokenizer, text)["input_ids"]], device="cuda")

    def unembed(self, h: torch.Tensor) -> torch.Tensor:
        """Final norm then lm_head, fp32 logits, scaled and softcapped as the model's own (Gemma: 30 tanh(x / 30); Muse
        Glimmer: T tanh(m x / T); ranks unchanged)."""
        logits = self.hf.lm_head(self.final_norm(h.to(torch.bfloat16))).float()
        mult = getattr(self.hf.config.get_text_config(), "output_multiplier", None)  # Muse Glimmer: scaled before the cap
        logits = logits * mult if mult else logits
        cap = getattr(self.hf.config.get_text_config(), "final_logit_softcapping", None)
        return cap * torch.tanh(logits / cap) if cap else logits

    def norm_gain(self) -> torch.Tensor:
        """The final RMSNorm's per-dimension gain, fp32: 1 + weight for Qwen3.5-family norms, weight for Gemma 4's."""
        weight = self.final_norm.weight.float()
        return 1.0 + weight if pins.TARGETS[pins.TARGET]["norm_gain"] == "one_plus_weight" else weight

    @torch.no_grad()
    def run(
        self, ids: torch.Tensor, edits: dict[int, Edit] | None = None, record: tuple[int, ...] = ()
    ) -> tuple[torch.Tensor, dict[int, torch.Tensor]]:
        """One forward of a single prompt [1, seq]. Returns the final-position logits [vocab] (fp32) and the block
        outputs [seq, d] (fp32, after any edit at that layer) at the `record` layers."""
        edits = edits or {}
        recorded: dict[int, torch.Tensor] = {}

        def hook_for(layer: int):
            def hook(_module, _args, out):
                h = out[0] if isinstance(out, tuple) else out
                if layer in edits:
                    h = edits[layer](h[0].float()).to(h.dtype)[None]
                if layer in record:
                    recorded[layer] = h[0].float().clone()
                if layer not in edits:
                    return None
                return (h, *out[1:]) if isinstance(out, tuple) else h

            return hook

        with _forward_hooks([(self.layers[layer], hook_for(layer)) for layer in sorted(set(edits) | set(record))]):
            logits = self.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].float()
        return logits, recorded

    @torch.no_grad()
    def greedy_text(self, ids: torch.Tensor, max_new_tokens: int = 8) -> str:
        """Greedy continuation of a short prompt, decoded. Full forwards without a cache: slower, but the same
        forward path as `run`."""
        for _ in range(max_new_tokens):
            next_id = self.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].argmax()
            ids = torch.cat([ids, next_id.view(1, 1)], dim=1)
        return self.tokenizer.decode(ids[0, -max_new_tokens:])

    @torch.no_grad()
    def generate(
        self, ids: torch.Tensor, max_new_tokens: int, edits: dict[int, Edit] | None = None
    ) -> tuple[torch.Tensor, str, int]:
        """Greedy continuation through HF `generate` (as exp13 does), with `edits` applied only to the prompt's own
        forward; generated tokens are not edited. Returns the first step's raw logits [vocab] (fp32), the decoded
        continuation and the number of new tokens."""
        edits = edits or {}
        prompt_len = ids.shape[1]

        def hook_for(layer: int):
            def hook(_module, _args, out):
                h = out[0] if isinstance(out, tuple) else out
                if h.shape[1] != prompt_len:  # a decoding step
                    return None
                h = edits[layer](h[0].float()).to(h.dtype)[None]
                return (h, *out[1:]) if isinstance(out, tuple) else h

            return hook

        with _forward_hooks([(self.layers[layer], hook_for(layer)) for layer in sorted(edits)]):
            out = self.hf.generate(
                input_ids=ids,
                attention_mask=torch.ones_like(ids),
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
                output_logits=True,
                return_dict_in_generate=True,
                **_gen_cache_kw(),
            )
        new = out.sequences[0, prompt_len:]
        return out.logits[0][0].float(), self.tokenizer.decode(new, skip_special_tokens=True), int(new.shape[0])

    @torch.no_grad()
    def generate_batch(
        self, ids: torch.Tensor, max_new_tokens: int, edits: list[dict[int, Edit]], first_logits: bool = False
    ) -> Any:
        """Greedy continuations under several edit sets at once, one batch row per set (a row without an edit at a layer
        passes through): of one prompt [1, seq], or of as many prompts of one length [len(edits), seq]. Each row is
        `generate(ids[row], max_new_tokens, edits[row])` up to batched-kernel rounding; one batched call pays the
        per-kernel launch cost once instead of once per row, which is what bounds generation speed on this model
        (thousands of small kernels per token). Returns the decoded continuations, and with first_logits also the
        first step's raw logits [len(edits), vocab] (fp32), as `generate` returns them."""
        prompt_len = ids.shape[1]

        def hook_for(layer: int):
            def hook(_module, _args, out):
                h = out[0] if isinstance(out, tuple) else out
                if h.shape[1] != prompt_len:  # a decoding step
                    return None
                h = h.clone()
                for row, row_edits in enumerate(edits):
                    if layer in row_edits:
                        h[row] = row_edits[layer](h[row].float()).to(h.dtype)
                return (h, *out[1:]) if isinstance(out, tuple) else h

            return hook

        layers = sorted({layer for row_edits in edits for layer in row_edits})
        batch = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1).contiguous()
        with _forward_hooks([(self.layers[layer], hook_for(layer)) for layer in layers]):
            out = self.hf.generate(
                input_ids=batch,
                attention_mask=torch.ones_like(batch),
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
                output_logits=first_logits,
                return_dict_in_generate=True,
                **_gen_cache_kw(),
            )
        texts = [self.tokenizer.decode(seq[prompt_len:], skip_special_tokens=True) for seq in out.sequences]
        return (texts, out.logits[0].float()) if first_logits else texts

    @torch.no_grad()
    def first_logits_prefix(self, ids: torch.Tensor, edits: list[dict[int, Edit]], start: int, rows: int) -> torch.Tensor:
        """generate_batch(ids, 1, edits, first_logits=True)'s logits [len(edits), vocab] (fp32) for one prompt [1, seq]
        whose edits all act at positions >= start (2026-10-22, the steering speed-up): the first `start` tokens run once,
        batched `rows` wide, and their cache (attention KV, and the hybrid models' recurrent and conv state) is reused;
        each chunk of `rows` edit sets then runs only tokens start.. with every edit's positions shifted by -start.
        Edits must carry `positions` (write_max's AddRows / SetRows). Equal to the full run up to kernel rounding,
        checked per model by write_max --check-prefix."""
        import copy

        seq = ids.shape[1]
        assert 0 < start < seq, (start, seq)
        prefix = self.hf(input_ids=ids[:, :start].expand(rows, -1).contiguous(), use_cache=True)
        cache0 = prefix.past_key_values
        suffix = ids[:, start:].expand(rows, -1).contiguous()
        out = []
        for c0 in range(0, len(edits), rows):
            chunk = list(edits[c0 : c0 + rows])
            n = len(chunk)
            chunk += [{}] * (rows - n)  # padded rows: no edits, outputs dropped
            shifted = []
            for row_edits in chunk:
                se = {}
                for la, e in row_edits.items():
                    assert min(e.positions) >= start, (min(e.positions), start)
                    e2 = copy.copy(e)
                    e2.positions = [q - start for q in e.positions]
                    se[la] = e2
                shifted.append(se)

            def hook_for(layer: int, shifted=shifted):
                def hook(_module, _args, o):
                    h = o[0] if isinstance(o, tuple) else o
                    h = h.clone()
                    for row, row_edits in enumerate(shifted):
                        if layer in row_edits:
                            h[row] = row_edits[layer](h[row].float()).to(h.dtype)
                    return (h, *o[1:]) if isinstance(o, tuple) else h

                return hook

            layers = sorted({la for row_edits in shifted for la in row_edits})
            cache = copy.deepcopy(cache0)
            with _forward_hooks([(self.layers[la], hook_for(la)) for la in layers]):
                logits = self.hf(input_ids=suffix, past_key_values=cache, use_cache=True, logits_to_keep=1).logits[:, -1].float()
            out.append(logits[:n])
        return torch.cat(out)

    def surface_ids(self, word: str) -> list[int]:
        return tokens.surface_ids(self.tokenizer, word)

    def concept_token(self, concept: str) -> int:
        return tokens.concept_token(self.tokenizer, concept)

    def answer_ids(self, answers: list[str]) -> list[int]:
        """Single-token surface ids of any of several accepted answers."""
        return sorted({i for a in answers for i in self.surface_ids(a)})

    def word_rank(self, logits: torch.Tensor, candidate_ids: list[int]) -> int:
        """1 + the number of other word tokens scoring at least as high as the best candidate (formatting tokens
        removed). Strict, so an exact tie with another word (common in bf16) ranks the candidate 2nd, not 1st."""
        word_logits = logits.masked_fill(self.formatting_mask, float("-inf"))
        best = word_logits[candidate_ids].max()
        word_logits[candidate_ids] = float("-inf")
        return int((word_logits >= best).sum()) + 1

    def top_word(self, logits: torch.Tensor) -> str:
        return self.decoded[int(logits.masked_fill(self.formatting_mask, float("-inf")).argmax())]

    def letter_token_ids(self) -> torch.Tensor:
        """Ids of non-special tokens whose decode contains a letter: the J-lens dictionary for the decomposition."""
        keep = [i for i, s in enumerate(self.decoded) if i not in self.special_ids and _HAS_LETTER.search(s)]
        return torch.tensor(keep, device="cuda")


def load_model() -> Model:
    from transformers import AutoConfig, AutoModelForCausalLM, AutoModelForImageTextToText

    path = snapshot_download(
        pins.MODEL_REPO, revision=pins.MODEL_REVISION, local_files_only=True,
        ignore_patterns=pins.TARGETS[pins.TARGET].get("snapshot_ignore"),
    )
    tokenizer = tokens.load_tokenizer()
    extra: dict[str, Any] = {}
    cfg = None
    if remote := pins.TARGETS[pins.TARGET].get("remote_lm"):  # Nemotron 3.5 Bolt (2026-10-25): see _remote_lm
        auto, cfg = _remote_lm(path, remote)
        extra.update(config=cfg, key_mapping=remote["key_mapping"])
    else:
        architectures = AutoConfig.from_pretrained(path).architectures or []
        multimodal = any(a.endswith("ForConditionalGeneration") for a in architectures)
        auto = AutoModelForImageTextToText if multimodal else AutoModelForCausalLM  # Gemma 4: the checkpoint's own class
    if pins.TARGETS[pins.TARGET].get("dequantize_mxfp4"):  # gpt-oss (2026-10-23): bf16 experts, as the J++ fitter loads them
        from transformers import Mxfp4Config

        extra["quantization_config"] = Mxfp4Config(dequantize=True)
    attn = pins.TARGETS[pins.TARGET].get("attn", "sdpa")  # gpt-oss: eager (learned attention sinks)
    device_map: Any = "cuda"
    if pins.TARGETS[pins.TARGET].get("split_gpus"):  # 2026-10-25 (DeepSeek-V4-Flash, 160 GB): two GPUs, see _split_map
        device_map = _split_map(auto, path, pins.TARGETS[pins.TARGET]["split_gpus"], cfg)
    hf = auto.from_pretrained(path, dtype=torch.bfloat16, device_map=device_map, attn_implementation=attn, **extra).eval()
    if pins.TARGETS[pins.TARGET].get("use_kernels") and not os.environ.get("BJ_NO_KERNELS"):  # Nemotron 3.5 (amendment 42): HF-hub kernels
        hf.set_use_kernels(True)
    n = hf.config.get_text_config().num_hidden_layers
    assert n == pins.N_LAYERS, f"{pins.MODEL_REPO} has {n} blocks; pins.TARGETS says {pins.N_LAYERS}"
    vocab = hf.lm_head.weight.shape[0]
    decoded = tokenizer.batch_decode([[i] for i in range(vocab)])
    special = frozenset(tokenizer.all_special_ids) | frozenset(int(i) for i in tokenizer.added_tokens_decoder)
    formatting = [i for i, s in enumerate(decoded) if i in special or not _HAS_LETTER_OR_DIGIT.search(s)]
    mask = torch.zeros(vocab, dtype=torch.bool, device="cuda")
    mask[formatting] = True
    return Model(hf, tokenizer, decoded, special, mask)


def _gen_cache_kw() -> dict[str, Any]:
    """2026-10-29: a model built by its own code (pins remote_lm, Bolt) wants its hybrid Mamba cache, and generate() hands
    it transformers' DynamicCache; it generates without a cache (as natural_v1's hop 1 does). Other models: unchanged."""
    return {"use_cache": False} if pins.TARGETS[pins.TARGET].get("remote_lm") else {}


def _remote_lm(path: str, spec: dict[str, Any]):
    """The language model alone out of a multimodal checkpoint whose code ships with it (Nemotron 3.5 Bolt: NVIDIA's
    NemotronHPuzzleForCausalLM, heterogeneous MoE blocks, which transformers' own NemotronH cannot build), at the pinned
    revision, read before use (Zach approved running it, 2026-10-25). Returns (class, config): the config from the
    checkpoint's config.json under spec["config_key"], its special floats decoded as transformers does; the checkpoint's
    keys are mapped onto the class by spec["key_mapping"] and the vision tower's weights are left unloaded."""
    import json
    from pathlib import Path

    from transformers.dynamic_module_utils import get_class_from_dynamic_module

    def special(o):
        return float(o["__float__"]) if set(o) == {"__float__"} else o

    if spec.get("hub_mamba") and not os.environ.get("BJ_NO_KERNELS"):
        _hub_mamba_ssm(**spec["hub_mamba"])
    _gated_rmsnorm_shim()
    raw = json.loads((Path(path) / "config.json").read_text(), object_hook=special)[spec["config_key"]]
    cfg = get_class_from_dynamic_module(spec["config"], path).from_dict(raw)
    cls = get_class_from_dynamic_module(spec["model"], path)
    if not os.environ.get("BJ_SLOW_MOE"):  # amendment 49 note 3: grouped GEMMs instead of NVIDIA's per-expert loop
        _patch_fast_moe(cls)
    return cls, cfg


def _fast_moe(self, hidden_states, topk_indices, topk_weights):
    """Nemotron 3.5 Bolt's NemotronHMoE.moe (2026-10-26, amendment 49 note 3) with one host sync per layer instead of one per
    expert: NVIDIA's loop calls every expert with torch.where (a sync each) and runs a no-op for each unused expert (zeros:
    no MLP bias). Here the same expert calls on the same token rows in the same order (row-major (token, slot), as
    torch.where gives), accumulated in the same expert order, unused experts skipped: the same numbers, differentiable."""
    import torch

    k = topk_indices.shape[1]
    flat = topk_indices.reshape(-1)
    order = torch.argsort(flat, stable=True)
    tok, slot = torch.div(order, k, rounding_mode="floor"), order % k
    counts = torch.bincount(flat, minlength=len(self.experts)).tolist()
    final = torch.zeros_like(hidden_states, dtype=topk_weights.dtype)
    start = 0
    for e, c in enumerate(counts):
        if c:
            ti, wi = tok[start : start + c], slot[start : start + c]
            final.index_add_(0, ti, self.experts[e](hidden_states[ti]) * topk_weights[ti, wi].unsqueeze(-1))
            start += c
    return final.type(hidden_states.dtype)


def _grouped_moe(self, hidden_states, topk_indices, topk_weights):
    """Bolt's NemotronHMoE.moe as two grouped GEMMs per layer (2026-10-26, amendment 49 note 3; ~50x faster than NVIDIA's
    per-expert loop on one Bolt layer). On first use the experts' weights are stacked into [E, out, in] tensors and each
    expert's Linear is pointed at its slice (no copy kept). Tokens are sorted by expert (row-major (token, slot) within an
    expert, as the loop), multiplied by torch._grouped_mm, put back in (token, slot) order and summed over the k slots
    with their routing weights (a fixed order: deterministic). The same computation up to bf16 rounding (one Bolt layer:
    relative difference 2e-5; gradients flow); checked against the exact loop on Bolt itself before use."""
    import torch

    if not hasattr(self, "_bj_up_proj"):
        for name in ("up_proj", "down_proj"):
            W = torch.stack([getattr(e, name).weight.data for e in self.experts])
            for i, e in enumerate(self.experts):
                getattr(e, name).weight = torch.nn.Parameter(W[i], requires_grad=getattr(e, name).weight.requires_grad)
            setattr(self, f"_bj_{name}", W)
    T, k = topk_indices.shape
    flat = topk_indices.reshape(-1)
    order = torch.argsort(flat, stable=True)
    offs = torch.cumsum(torch.bincount(flat, minlength=len(self.experts)), 0).to(torch.int32)
    y = torch._grouped_mm(hidden_states[torch.div(order, k, rounding_mode="floor")], self._bj_up_proj.transpose(1, 2), offs=offs)
    y = torch._grouped_mm(self.experts[0].act_fn(y), self._bj_down_proj.transpose(1, 2), offs=offs)
    back = torch.empty_like(y)
    back[order] = y
    return (back.view(T, k, -1) * topk_weights.unsqueeze(-1)).sum(1).type(hidden_states.dtype)


def _patch_fast_moe(cls) -> None:
    """Point the class's sibling module's NemotronHMoE.moe at _grouped_moe, or with BJ_EXACT_MOE at _fast_moe (the exact
    loop with one sync per layer); this process only."""
    import sys

    mod = sys.modules[cls.__module__]
    nh = getattr(mod, "modeling_nemotron_h", mod)
    nh.NemotronHMoE.moe = _fast_moe if os.environ.get("BJ_EXACT_MOE") else _grouped_moe


def _hub_mamba_ssm(repo: str, revision: str) -> None:
    """Bolt's code imports mamba_ssm itself, so transformers' set_use_kernels cannot reach it (2026-10-25, amendment 44).
    Load the prebuilt HF-hub mamba-ssm (the package transformers fetches for Lightning, pinned) and register it as
    mamba_ssm and the submodules Bolt's code imports, and report mamba_ssm as available to transformers' check, so that
    code takes its kernel path. Nothing is compiled or installed."""
    import importlib
    import sys

    import kernels
    import transformers.utils.import_utils as iu

    k = kernels.get_kernel(repo, revision=revision)
    sys.modules["mamba_ssm"] = k
    for sub in ("ops", "ops.triton", "ops.triton.ssd_combined", "ops.triton.selective_state_update", "ops.triton.layernorm_gated"):
        sys.modules[f"mamba_ssm.{sub}"] = importlib.import_module(f"{k.__name__}.{sub}")
    iu.is_mamba_2_ssm_available = lambda: True


def _gated_rmsnorm_shim() -> None:
    """Bolt's code imports mamba_ssm's Triton gated RMSNorm (rmsnorm_fn) unconditionally and fails without mamba_ssm,
    which this env lacks (its Mamba scan then takes the code's own torch path, as Lightning's does). If mamba_ssm is
    absent, register mamba_ssm.ops.triton.layernorm_gated with rmsnorm_fn = mamba_ssm's pure-torch reference of that
    kernel (rms_norm_ref: fp32, gate silu(z) before the norm when norm_before_gate is False, per-group RMS, weight and bias
    in fp32, cast back), so nothing else of the code changes. Only modules the import names are added."""
    import importlib.machinery
    import importlib.util
    import sys
    import types

    if importlib.util.find_spec("mamba_ssm") is not None:
        return

    def rmsnorm_fn(x, weight, bias=None, z=None, eps=1e-6, group_size=None, norm_before_gate=True, upcast=True):
        dtype = x.dtype
        weight = weight.float()
        bias = bias.float() if bias is not None else None
        if upcast:
            x = x.float()
            z = z.float() if z is not None else z
        if z is not None and not norm_before_gate:
            x = x * torch.nn.functional.silu(z)
        g = x.shape[-1] if group_size is None else group_size
        xg = x.view(*x.shape[:-1], x.shape[-1] // g, g)
        out = (xg * torch.rsqrt(xg.square().mean(dim=-1, keepdim=True) + eps)).view(x.shape) * weight
        if bias is not None:
            out = out + bias
        if z is not None and norm_before_gate:
            out = out * torch.nn.functional.silu(z)
        return out.to(dtype)

    for name in ("mamba_ssm", "mamba_ssm.ops", "mamba_ssm.ops.triton", "mamba_ssm.ops.triton.layernorm_gated"):
        mod = types.ModuleType(name)
        mod.__spec__ = importlib.machinery.ModuleSpec(name, None)
        sys.modules[name] = mod
    sys.modules["mamba_ssm.ops.triton.layernorm_gated"].rmsnorm_fn = rmsnorm_fn


def _split_map(auto, path: str, cut: int, cfg=None) -> dict[str, int]:
    """A device map over two GPUs: decoder blocks below `cut` on cuda:0, the rest on cuda:1, everything else (embeddings,
    final norm, lm_head, rotary tables) on cuda:0, so inputs, logits and the lens's tensors stay on cuda:0 as on one
    GPU. Blocks on cuda:1 are bridged by _forward_hooks."""
    from accelerate import init_empty_weights
    from transformers import AutoConfig

    cfg = cfg if cfg is not None else AutoConfig.from_pretrained(path)
    with init_empty_weights():
        skel = auto.from_config(cfg) if hasattr(auto, "from_config") else auto(cfg)
    n = cfg.get_text_config().num_hidden_layers
    layers_path = next(name for name, mod in skel.named_modules()
                       if isinstance(mod, torch.nn.ModuleList) and name.endswith("layers") and len(mod) >= n)  # fmt: skip
    dm: dict[str, int] = {}
    mod, prefix = skel, ""
    for part in layers_path.split("."):
        for cname, _ in mod.named_children():
            if cname != part:
                dm[f"{prefix}{cname}"] = 0
        mod, prefix = getattr(mod, part), f"{prefix}{part}."
    for i in range(len(mod)):
        dm[f"{layers_path}.{i}"] = 0 if i < cut else 1
    return dm


def _moved(x, device):
    if isinstance(x, torch.Tensor):
        return x.to(device)
    if isinstance(x, tuple):
        return tuple(_moved(v, device) for v in x)
    return x


def _bridged(module, hook):
    """A forward hook for a block that may sit on another GPU than cuda:0 (split_gpus): the hook sees the block's output
    on cuda:0, as on one GPU, and what it returns goes back to the block's device."""
    dev = next(module.parameters()).device
    if dev.type != "cuda" or dev.index in (None, 0):
        return hook

    def wrapped(m, args, out):
        r = hook(m, args, _moved(out, "cuda:0"))
        return None if r is None else _moved(r, dev)

    return wrapped


def _streamed(hook):
    """A forward hook for a block whose output is several parallel residual streams [B, S, R, D] (DeepSeek-V4's
    hyper-connections, 2026-10-25): the hook sees the lens's residual, the mean over the streams [B, S, D] (the
    convention of the published DeepSeek-V4 J++: jpp_lens's residual_streams.py), and what it returns is lifted back by
    adding its change to the mean to every stream (the uniform shift under which that lens's Jacobian is defined), so
    the streams' mean moves exactly as edited and a no-op edit leaves them bit-identical. Single-stream outputs pass
    through unchanged."""

    def wrapped(m, args, out):
        x = out[0] if isinstance(out, tuple) else out
        if x.dim() != 4:
            return hook(m, args, out)
        mean = x.mean(dim=2)
        r = hook(m, args, (mean, *out[1:]) if isinstance(out, tuple) else mean)
        if r is None:
            return None
        new = r[0] if isinstance(r, tuple) else r
        y = (x.float() + (new.float() - mean.float()).unsqueeze(2)).to(x.dtype)
        return (y, *out[1:]) if isinstance(out, tuple) else y

    return wrapped


@contextlib.contextmanager
def _forward_hooks(pairs):
    handles = [module.register_forward_hook(_bridged(module, _streamed(hook))) for module, hook in pairs]
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()
