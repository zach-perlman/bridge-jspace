"""Check our verbalizer readers against WorkspaceBench's reference code path on the same activations.

Ours: the adapter as forward hooks (bridge_jspace.oracle / bridge_jspace.nla), greedy. Reference: WorkspaceBench's
OLens / NLA read (github.com/camilablank/workspace-bench, src/wsbench/produce/methods.py @92d763e722, MIT): the adapter
through peft's PeftModel, its sampling (temperature 1.0, top-p 0.95, top-k 64, 256 tokens); here also greedy, so the
two paths can be compared token for token. The activations: short facts and a few exp15 questions' last word, captured
from Qwen3.6-27B with no adapter, at an oracle layer (36, 44) and at 42 for the NLA.

peft is not a project dependency; this check runs with it added for the one call:
    uv run --with peft==0.19.1 python scripts/check_reference_readers.py
Writes results/checks/reference_readers-<timestamp>.json (write-once).
"""

from __future__ import annotations

import gc
import json
from datetime import datetime
from typing import Any

import torch
from huggingface_hub import hf_hub_download

from bridge_jspace import pins

PROMPTS = [
    "Fact: The capital of France is",
    "Fact: The largest planet in the solar system is",
    "Fact: The language spoken in the country where the Amazon River ends is",
    "Fact: The capital of the country where Naples is located is",
    "Fact: The color of the long-necked bird in the famous Tchaikovsky ballet is",
]
ORACLE_LAYERS = (36, 44)
SAMPLING = {"do_sample": True, "temperature": 1.0, "top_p": 0.95, "top_k": 64}  # WorkspaceBench's Sampling()
MAX_NEW = {"oracle": 96, "nla": 160}


def capture() -> tuple[Any, dict[int, torch.Tensor]]:
    """Qwen3.6-27B (part B's Model) and the last-token residuals [n_prompts, d] at the oracle layers and 42, captured
    with no adapter."""
    from bridge_jspace.model import load_model

    model = load_model()
    layers = (*ORACLE_LAYERS, 42)
    out: dict[int, list[torch.Tensor]] = {layer: [] for layer in layers}
    for prompt in PROMPTS:
        _, h = model.run(model.encode(prompt), record=layers)
        for layer in layers:
            out[layer].append(h[layer][-1].cpu())
    return model, {layer: torch.stack(v) for layer, v in out.items()}


@torch.no_grad()
def oracle_reads(model: Any, vectors: dict[int, torch.Tensor]) -> list[dict[str, Any]]:
    """Ours (hooks) greedy and sampled; then the reference path (PeftModel) greedy and sampled, same embeddings."""
    from peft import PeftModel  # pyright: ignore[reportMissingImports]

    from bridge_jspace.oracle import ALPHA, LoraHooks, Oracle, carrier, load_adapter

    pairs, scale, _ = load_adapter()
    oracle = Oracle(model, LoraHooks(model.hf, pairs, scale))
    tok = model.tokenizer
    rows = []
    for layer in ORACLE_LAYERS:
        for i, prompt in enumerate(PROMPTS):
            v = vectors[layer][i : i + 1]
            row = {
                "reader": "oracle",
                "layer": layer,
                "prompt": prompt,
                "ours_greedy": oracle.read(v, layer, MAX_NEW["oracle"])[0],
            }
            e = oracle._embeds(v, layer, [])
            with oracle.hooks.on():
                torch.manual_seed(0)
                out = model.hf.generate(inputs_embeds=e, attention_mask=torch.ones(e.shape[:2], dtype=torch.long, device="cuda"),
                                        max_new_tokens=MAX_NEW["oracle"], pad_token_id=tok.eos_token_id, **SAMPLING)  # fmt: skip
            row["ours_sampled"] = tok.decode(out[0], skip_special_tokens=True).strip()
            rows.append(row)
    adapter_dir = hf_hub_download(pins.LENS_REPO, f"{pins.ORACLE_DIR}/adapter_config.json", revision=pins.LENS_REVISION)
    peft_model = PeftModel.from_pretrained(model.hf, adapter_dir.rsplit("/", 1)[0]).eval()
    embed = peft_model.get_input_embeddings()
    for row in rows:
        ids, slot = carrier(tok, row["layer"])
        v = vectors[row["layer"]][PROMPTS.index(row["prompt"])].to("cuda").float()
        e = embed(torch.tensor([ids], device="cuda")).clone()
        e[0, slot, :] = (ALPHA * v / v.norm().clamp_min(1e-9)).to(e.dtype)
        mask = torch.ones(1, len(ids), dtype=torch.long, device="cuda")
        for name, kwargs in (("ref_greedy", {"do_sample": False}), ("ref_sampled", SAMPLING)):
            torch.manual_seed(0)
            out = peft_model.generate(inputs_embeds=e, attention_mask=mask, max_new_tokens=MAX_NEW["oracle"],
                                      pad_token_id=tok.eos_token_id, **kwargs)  # fmt: skip
            row[name] = tok.decode(out[0], skip_special_tokens=True).strip()
    peft_model.unload()  # back to the bare model before it is freed
    return rows


@torch.no_grad()
def nla_reads(vectors: torch.Tensor) -> list[dict[str, Any]]:
    """Ours greedy and sampled; then the reference path (av_base + PeftModel, its block-1 hook) greedy and sampled."""
    from peft import PeftModel  # pyright: ignore[reportMissingImports]

    from bridge_jspace.nla import NLA, explanation

    nla = NLA()
    rows = [{"reader": "nla", "layer": 42, "prompt": p, "ours_greedy": t}
            for p, t in zip(PROMPTS, nla.read(vectors, MAX_NEW["nla"]), strict=True)]  # fmt: skip
    ids = torch.tensor([nla.ids], device="cuda")
    for i, row in enumerate(rows):
        with nla.hooks.on(), nla._inject(vectors[i : i + 1]):
            torch.manual_seed(0)
            out = nla.hf.generate(input_ids=ids, attention_mask=torch.ones_like(ids), max_new_tokens=MAX_NEW["nla"],
                                  pad_token_id=nla.tokenizer.eos_token_id, **SAMPLING)  # fmt: skip
        row["ours_sampled"] = explanation(nla.tokenizer.decode(out[0, ids.shape[1] :], skip_special_tokens=True))
    from bridge_jspace.nla import nla_dir

    peft_model = PeftModel.from_pretrained(nla.hf, str(nla_dir() / pins.NLA_ADAPTER)).eval()
    for i, row in enumerate(rows):
        for name, kwargs in (("ref_greedy", {"do_sample": False}), ("ref_sampled", SAMPLING)):
            with nla._inject(vectors[i : i + 1]):  # the reference injects the same way (methods.py NLA.bind's hook)
                torch.manual_seed(0)
                out = peft_model.generate(input_ids=ids, attention_mask=torch.ones_like(ids),
                                          max_new_tokens=MAX_NEW["nla"], pad_token_id=nla.tokenizer.eos_token_id,
                                          **kwargs)  # fmt: skip
            row[name] = explanation(nla.tokenizer.decode(out[0, ids.shape[1] :], skip_special_tokens=True))
    return rows


def main() -> None:
    out = pins.RESULTS_DIR / "checks" / f"reference_readers-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    assert not out.exists(), f"{out} exists; checks are write-once"
    model, captured = capture()
    rows = oracle_reads(model, captured)
    nla_vectors = captured[42]
    del model, captured
    gc.collect()
    torch.cuda.empty_cache()
    rows += nla_reads(nla_vectors)
    for row in rows:  # how far the two greedy paths agree
        a, b = row["ours_greedy"], row["ref_greedy"]
        row["greedy_common_prefix_chars"] = next(
            (k for k, (x, y) in enumerate(zip(a, b, strict=False)) if x != y), min(len(a), len(b))
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"workspace_bench": "methods.py @92d763e722", "sampling": SAMPLING, "rows": rows}, indent=2,
                              ensure_ascii=False))  # fmt: skip
    print(out)


if __name__ == "__main__":
    main()
