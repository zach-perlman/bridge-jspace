"""The oracle lens on Qwen3.6-27B: a LoRA on the model itself that puts one residual vector into words, as bullets of
concepts.

Read contract (the adapter's UPSTREAM_README, which says to take it whole): the vector replaces the input embedding of
a marker token (㈜, id 158983) in the `concepts_raw` prompt as alpha * h / |h| with alpha = 16000; one user turn,
chat template with add_generation_prompt and enable_thinking=False; trained on layers 20-60 in steps of 4. The vector
is captured with the adapter off and read with it on.

The adapter runs as forward hooks (out += scale * x A^T B^T on each target Linear) instead of being merged into the
bf16 weights, so the base model is never modified and capture / read use exactly the same weights. Reference reader:
WorkspaceBench's OLens (github.com/camilablank/workspace-bench, MIT), which samples; we decode greedily.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import torch
from huggingface_hub import hf_hub_download

from . import pins
from .model import Model

PROMPT = (
    "An activation vector from layer {layer} of a language model is enclosed in activation tags: "
    "<activation>{char}</activation>. Produce distinct concepts that encode this activation, each as a '- ' bullet "
    "on its own line."
)
ALPHA = 16000.0
MARKER_ID = 158983  # ㈜, the slot the contract names
TRAINED_LAYERS = tuple(range(20, 61, 4))
_PREFIX, _A, _B = "base_model.model.", ".lora_A.weight", ".lora_B.weight"


def load_adapter() -> tuple[dict[str, tuple[torch.Tensor, torch.Tensor]], float, dict[str, Any]]:
    """The pinned adapter: {module path: (A [r, in], B [out, r])} fp32 on the CPU, its scale, its config."""
    from safetensors.torch import load_file

    weights = hf_hub_download(
        pins.LENS_REPO, f"{pins.ORACLE_DIR}/adapter_model.safetensors", revision=pins.LENS_REVISION
    )
    config_path = hf_hub_download(pins.LENS_REPO, f"{pins.ORACLE_DIR}/adapter_config.json", revision=pins.LENS_REVISION)
    with open(weights, "rb") as f:
        got = hashlib.file_digest(f, "sha256").hexdigest()
    if got != pins.ORACLE_ADAPTER_SHA256:
        raise ValueError(f"oracle adapter sha256 {got} != pinned {pins.ORACLE_ADAPTER_SHA256}")
    config = json.loads(Path(config_path).read_text())
    if config["peft_type"] != "LORA" or config["use_rslora"] or config["use_dora"]:
        raise ValueError(f"unexpected adapter type: {config}")
    return module_pairs(load_file(weights)), config["lora_alpha"] / config["r"], config


def module_pairs(state: dict[str, torch.Tensor]) -> dict[str, tuple[torch.Tensor, torch.Tensor]]:
    """PEFT LoRA state dict -> {module path in the base model: (A, B)}; every A must have its B."""
    a = {k[len(_PREFIX) : -len(_A)]: v for k, v in state.items() if k.endswith(_A)}
    b = {k[len(_PREFIX) : -len(_B)]: v for k, v in state.items() if k.endswith(_B)}
    if set(a) != set(b) or len(a) + len(b) != len(state) or not all(k.startswith(_PREFIX) for k in state):
        raise ValueError("adapter keys are not LoRA A/B pairs under base_model.model.")
    return {m: (a[m].float(), b[m].float()) for m in sorted(a)}


def lora_delta(x: torch.Tensor, a: torch.Tensor, b: torch.Tensor, scale: float) -> torch.Tensor:
    """The adapter's addition to a Linear's output for input x [..., in], in fp32."""
    return scale * (x.float() @ a.T) @ b.T


class LoraHooks:
    """The adapter on a model, switched on with `with hooks.on():`. Every module path must exist and be a Linear."""

    def __init__(self, hf: torch.nn.Module, pairs: dict[str, tuple[torch.Tensor, torch.Tensor]], scale: float):
        self.scale = scale
        self.modules: list[tuple[torch.nn.Module, torch.Tensor, torch.Tensor]] = []
        for path, (a, b) in pairs.items():
            module = hf.get_submodule(path)
            if not isinstance(module, torch.nn.Linear) or tuple(module.weight.shape) != (b.shape[0], a.shape[1]):
                raise ValueError(f"{path}: not a Linear of shape {(b.shape[0], a.shape[1])}")
            device = module.weight.device
            self.modules.append((module, a.to(device), b.to(device)))

    @contextlib.contextmanager
    def on(self):
        def hook_for(a: torch.Tensor, b: torch.Tensor):
            def hook(_module, args, out):
                return out + lora_delta(args[0], a, b, self.scale).to(out.dtype)

            return hook

        handles = [m.register_forward_hook(hook_for(a, b)) for m, a, b in self.modules]
        try:
            yield
        finally:
            for h in handles:
                h.remove()


def carrier(tokenizer: Any, layer: int) -> tuple[list[int], int]:
    """The chat-templated prompt's ids for a layer and the marker slot's index (the first enclosed ideograph that is
    one token and appears once in the render, as the reference renderer picks it)."""
    for code in range(0x3200, 0x3400):
        char = chr(code)
        ids = tokenizer(char, add_special_tokens=False)["input_ids"]
        if len(ids) != 1:
            continue
        out = tokenizer.apply_chat_template(
            [{"role": "user", "content": PROMPT.format(layer=layer, char=char)}],
            tokenize=True,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        rendered = list(out["input_ids"] if hasattr(out, "keys") else out)
        slots = [i for i, t in enumerate(rendered) if t == ids[0]]
        if len(slots) == 1:
            if ids[0] != MARKER_ID:
                raise ValueError(f"marker {char!r} is id {ids[0]}, the contract says {MARKER_ID}")
            return rendered, slots[0]
    raise ValueError("no enclosed ideograph survives as a single token in the carrier prompt")


class Oracle:
    """Reads residual vectors of `model` at a trained layer. Use only after every activation has been captured with
    the adapter off: the adapter is on inside `read` and `first_bullet_logits`."""

    def __init__(self, model: Model, hooks: LoraHooks):
        self.model, self.hooks = model, hooks
        self.hf: Any = model.hf  # typed nn.Module in part B's Model
        tokenizer: Any = model.tokenizer
        self.tokenizer = tokenizer
        self.dash = tokenizer("-", add_special_tokens=False)["input_ids"]
        self._carriers: dict[int, tuple[list[int], int]] = {}

    def _embeds(self, vectors: torch.Tensor, layer: int, extra: list[int]) -> torch.Tensor:
        if layer not in TRAINED_LAYERS:
            raise ValueError(f"layer {layer} is off the oracle's contract {TRAINED_LAYERS}")
        if layer not in self._carriers:
            self._carriers[layer] = carrier(self.tokenizer, layer)
        ids, slot = self._carriers[layer]
        embed = self.hf.get_input_embeddings()
        e = embed(torch.tensor([ids + extra], device="cuda")).repeat(len(vectors), 1, 1)
        v = vectors.to("cuda").float()
        e[:, slot] = (ALPHA * v / v.norm(dim=-1, keepdim=True).clamp_min(1e-9)).to(e.dtype)
        return e

    @torch.no_grad()
    def read(self, vectors: torch.Tensor, layer: int, max_new_tokens: int) -> list[str]:
        """Greedy bullets for each vector [n, d] captured at `layer`."""
        e = self._embeds(vectors, layer, [])
        with self.hooks.on():
            out = self.hf.generate(
                inputs_embeds=e,
                attention_mask=torch.ones(e.shape[:2], dtype=torch.long, device="cuda"),
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        return [t.strip() for t in self.tokenizer.batch_decode(out, skip_special_tokens=True)]

    @torch.no_grad()
    def first_bullet_logits(self, vectors: torch.Tensor, layer: int) -> torch.Tensor:
        """Logits [n, vocab] (fp32) of the first bullet's first token: the prompt followed by "-"."""
        e = self._embeds(vectors, layer, self.dash)
        mask = torch.ones(e.shape[:2], dtype=torch.long, device="cuda")
        with self.hooks.on():
            out = self.hf(inputs_embeds=e, attention_mask=mask, use_cache=False, logits_to_keep=1)
        return out.logits[:, -1].float()


def named(word: str, text: str) -> bool:
    """`word` appears in `text` as a whole word, ignoring case and a plural ending (s / es)."""
    return re.search(rf"(?<![^\W\d_]){re.escape(word)}(?:e?s)?(?![^\W\d_])", text, flags=re.IGNORECASE) is not None


@torch.no_grad()
def sanity_gate(model: Model, oracle: Oracle, cfg: dict[str, Any], max_new_tokens: int, seed: int) -> dict[str, Any]:
    """Is the oracle loaded and reading? Before any experiment read: (1) the model's own logits are unchanged once
    the adapter is switched off again; (2) the adapter moves the oracle's logits; (3) reading the last token of short
    facts at `cfg["layers"]`, it names the expected word (the fact's answer, not in the prompt) for at least
    `min_named` facts; (4) a random vector (the slot takes only its direction) names at most `max_random_named` of those words."""
    facts, layers = cfg["facts"], cfg["layers"]
    probe = model.encode(facts[0]["prompt"])
    before, _ = model.run(probe)
    captured = [model.run(model.encode(f["prompt"]), record=tuple(layers))[1] for f in facts]
    vectors = {layer: torch.stack([h[layer][-1] for h in captured]) for layer in layers}

    first = vectors[layers[0]][:1]
    on = oracle.first_bullet_logits(first, layers[0])
    off = oracle.hf(inputs_embeds=oracle._embeds(first, layers[0], oracle.dash), use_cache=False, logits_to_keep=1)
    change = float((on - off.logits[:, -1].float()).abs().max())
    reads = {layer: oracle.read(vectors[layer], layer, max_new_tokens) for layer in layers}
    random = torch.randn(1, first.shape[1], generator=torch.Generator().manual_seed(seed))
    random_reads = {layer: oracle.read(random, layer, max_new_tokens)[0] for layer in layers}
    after, _ = model.run(probe)
    drift = float((after - before).abs().max())

    hits = [any(named(t, reads[ly][i]) for ly in layers for t in f["targets"]) for i, f in enumerate(facts)]
    random_hits = [any(named(t, random_reads[ly]) for ly in layers for t in f["targets"]) for f in facts]
    failed = [
        msg
        for ok, msg in (
            (drift < 1e-2, f"base logits moved by {drift:.3g} after the adapter was switched off"),
            (change > cfg["min_logit_change"], f"the adapter moves the oracle's logits by only {change:.3g}"),
            (sum(hits) >= cfg["min_named"], f"known facts named {sum(hits)}/{len(facts)} < {cfg['min_named']}"),
            (sum(random_hits) <= cfg["max_random_named"], f"a random vector names {sum(random_hits)} facts' words"),
        )
        if not ok
    ]
    return {
        "passed": not failed,
        "failed": failed,
        "base_logit_drift": drift,
        "adapter_max_logit_change": change,
        "marker_slots": {layer: oracle._carriers[layer][1] for layer in layers},
        "facts": [
            {**f, "named": hit, "reads": {layer: reads[layer][i] for layer in layers}}
            for i, (f, hit) in enumerate(zip(facts, hits, strict=True))
        ],
        "random_vector": {"named": sum(random_hits), "reads": random_reads},
    }
