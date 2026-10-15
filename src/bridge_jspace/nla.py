"""The NLA (natural-language autoencoder) for Qwen3.6-27B: a separate 27B verbalizer that describes one layer-42
residual vector in words.

Read contract (WorkspaceBench's NLA reader and the repo's nla_meta.yaml): `av_base` (Qwen3.6-27B with the warm-start
LoRA merged) plus one GRPO adapter (rsLoRA r64); the `actor` prompt, chat template with add_generation_prompt and
enable_thinking=False; the vector is added at the output of decoder block 1, at the marker token (㈜, id 158983),
norm-matched: h <- h + |h| * v / |v|; the answer is the text inside <explanation> ... </explanation>. Trained on
layer-42 activations only; the layer is not part of the prompt. The reference reader samples; we decode greedily.

The adapter runs as forward hooks (bridge_jspace.oracle.LoraHooks), as for the oracle lens.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
from pathlib import Path
from typing import Any

import torch
import yaml
from huggingface_hub import snapshot_download

from . import pins
from .oracle import LoraHooks, module_pairs

MARKER_ID = 158983
LAYER = 42


def nla_dir() -> Path:
    """The pinned snapshot (av_base and the adapter), downloaded beforehand."""
    return Path(
        snapshot_download(
            pins.NLA_REPO,
            revision=pins.NLA_REVISION,
            allow_patterns=["av_base/*", f"{pins.NLA_ADAPTER}/*"],
            local_files_only=True,
        )
    )


def load_adapter(root: Path) -> tuple[dict[str, tuple[torch.Tensor, torch.Tensor]], float, dict[str, Any]]:
    """The pinned GRPO adapter: {module path: (A, B)} fp32 on the CPU, its scale (rsLoRA: alpha / sqrt(r)), its
    config."""
    from safetensors.torch import load_file

    adir = root / pins.NLA_ADAPTER
    weights = adir / "adapter_model.safetensors"
    with open(weights, "rb") as f:
        got = hashlib.file_digest(f, "sha256").hexdigest()
    if got != pins.NLA_ADAPTER_SHA256:
        raise ValueError(f"NLA adapter sha256 {got} != pinned {pins.NLA_ADAPTER_SHA256}")
    config = json.loads((adir / "adapter_config.json").read_text())
    if config["peft_type"] != "LORA" or config["use_dora"]:
        raise ValueError(f"unexpected adapter type: {config}")
    r, alpha = config["r"], config["lora_alpha"]
    scale = alpha / r**0.5 if config["use_rslora"] else alpha / r
    return module_pairs(load_file(weights)), scale, config


class NLA:
    """The verbalizer on the GPU: `read` (greedy explanations) and `next_token_logits` (with the adapter switched on or
    off, for the gate)."""

    def __init__(self, root: Path | None = None):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        root = root or nla_dir()
        base = root / "av_base"
        self.meta = yaml.safe_load((base / "nla_meta.yaml").read_text())
        if (
            int(self.meta["tokens"]["injection_token_id"]) != MARKER_ID
            or self.meta["extraction"]["layer_index"] != LAYER
        ):
            raise ValueError("nla_meta.yaml does not match the pinned contract (marker 158983, layer 42)")
        self.tokenizer: Any = AutoTokenizer.from_pretrained(base)
        template = self.meta["prompt_templates"].get("av") or self.meta["prompt_templates"]["actor"]
        out = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": template.format(injection_char=self.meta["tokens"]["injection_char"])}],
            tokenize=True,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        self.ids = list(out["input_ids"] if hasattr(out, "keys") else out)
        slots = [i for i, t in enumerate(self.ids) if t == MARKER_ID]
        if len(slots) != 1:
            raise ValueError(f"the marker appears {len(slots)} times in the prompt")
        self.slot = slots[0]
        self.hf: Any = AutoModelForCausalLM.from_pretrained(base, dtype=torch.bfloat16, device_map="cuda").eval()
        pairs, self.scale, self.adapter_config = load_adapter(root)
        self.n_modules = len(pairs)
        self.hooks = LoraHooks(self.hf, pairs, self.scale)
        (self.block1,) = [m for n, m in self.hf.named_modules() if n.endswith("model.layers.1")]

    @contextlib.contextmanager
    def _inject(self, vectors: torch.Tensor):
        """Add each row of `vectors` [n, d] at the marker of the matching batch row, norm-matched to the residual
        there, on the forward that holds the prompt (decoding steps have one position and are left alone)."""
        v = vectors.to("cuda").float()
        unit = v / v.norm(dim=-1, keepdim=True).clamp_min(1e-9)

        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            if h.shape[1] <= self.slot:
                return None
            hp = h[:, self.slot, :].float()
            h[:, self.slot, :] = (hp + hp.norm(dim=-1, keepdim=True) * unit).to(h.dtype)
            return out

        handle = self.block1.register_forward_hook(hook)
        try:
            yield
        finally:
            handle.remove()

    @torch.no_grad()
    def read(self, vectors: torch.Tensor, max_new_tokens: int) -> list[str]:
        """Greedy explanations for each layer-42 vector [n, d]."""
        ids = torch.tensor([self.ids] * len(vectors), device="cuda")
        with self.hooks.on(), self._inject(vectors):
            out = self.hf.generate(
                input_ids=ids,
                attention_mask=torch.ones_like(ids),
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
            )
        texts = self.tokenizer.batch_decode(out[:, ids.shape[1] :], skip_special_tokens=True)
        return [explanation(t) for t in texts]

    @torch.no_grad()
    def next_token_logits(self, vectors: torch.Tensor, adapter: bool = True) -> torch.Tensor:
        """Logits [n, vocab] (fp32) of the first generated token, with or without the adapter."""
        ids = torch.tensor([self.ids] * len(vectors), device="cuda")
        with self.hooks.on() if adapter else contextlib.nullcontext(), self._inject(vectors):
            logits = self.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits
        return logits[:, -1].float()


def explanation(text: str) -> str:
    """The text inside <explanation> ... </explanation> (all of it if the tag never closes)."""
    return text.split("</explanation>")[0].strip().removeprefix("<explanation>").strip()


@torch.no_grad()
def nla_sanity_gate(
    nla: NLA, fact_vectors: torch.Tensor, cfg: dict[str, Any], max_new_tokens: int, seed: int
) -> dict[str, Any]:
    """Is the NLA loaded and reading? Before any experiment read: (1) its own logits are unchanged once the adapter is
    switched off again; (2) the adapter moves them; (3) reading the layer-42 vector at the last token of short facts
    (captured beforehand with Qwen3.6-27B), it names the expected answer for at least `min_named` facts; (4) a random
    vector names at most `max_random_named` of those answers."""
    from .oracle import named

    facts = cfg["facts"]
    probe = fact_vectors[:1]
    before = nla.next_token_logits(probe, adapter=False)
    on = nla.next_token_logits(probe, adapter=True)
    change = float((on - before).abs().max())
    reads = nla.read(fact_vectors, max_new_tokens)
    random = torch.randn(1, fact_vectors.shape[1], generator=torch.Generator().manual_seed(seed))
    random_read = nla.read(random, max_new_tokens)[0]
    after = nla.next_token_logits(probe, adapter=False)
    drift = float((after - before).abs().max())
    hits = [any(named(t, reads[i]) for t in f["targets"]) for i, f in enumerate(facts)]
    random_hits = [any(named(t, random_read) for t in f["targets"]) for f in facts]
    failed = [
        msg
        for ok, msg in (
            (drift < 1e-2, f"logits moved by {drift:.3g} after the adapter was switched off"),
            (change > cfg["min_logit_change"], f"the adapter moves the logits by only {change:.3g}"),
            (sum(hits) >= cfg["min_named"], f"known facts named {sum(hits)}/{len(facts)} < {cfg['min_named']}"),
            (sum(random_hits) <= cfg["max_random_named"], f"a random vector names {sum(random_hits)} facts' words"),
        )
        if not ok
    ]
    return {
        "passed": not failed,
        "failed": failed,
        "logit_drift": drift,
        "adapter_max_logit_change": change,
        "marker_slot": nla.slot,
        "adapter": {"modules": nla.n_modules, "scale": nla.scale, "r": nla.adapter_config["r"]},
        "facts": [{**f, "named": hit, "read": reads[i]} for i, (f, hit) in enumerate(zip(facts, hits, strict=True))],
        "random_vector": {"named": sum(random_hits), "read": random_read},
    }
