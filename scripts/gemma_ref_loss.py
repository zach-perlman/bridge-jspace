"""Harness check (Zach, 2026-10-20 overnight): Gemma 4 31B-it's plain-text loss in our harness was 7.66 nats (27B: 2.33).
Same 16 WikiText rows, loaded three ways: our harness's class (AutoModelForImageTextToText, sdpa), the same with eager
attention, and AutoModelForCausalLM (sdpa) if it loads. Prints mean next-token loss from position 4 for each."""

import gc
import json
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins
from bridge_jspace.tokens import raw_encoding
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoTokenizer

assert pins.TARGET.startswith("gemma"), "run with BJ_TARGET set to a Gemma target"
path = pins.MODEL_REPO
tok = AutoTokenizer.from_pretrained(path, revision=pins.MODEL_REVISION)
texts = [ids for t in pins.wikitext_rows() if len(ids := raw_encoding(tok, t)["input_ids"][:128]) >= 64][:16]
print("first ids", texts[0][:5], "bos", tok.bos_token_id, flush=True)
out = {}
for label, cls, attn in (
    ("image_text_sdpa", AutoModelForImageTextToText, "sdpa"),
    ("image_text_eager", AutoModelForImageTextToText, "eager"),
    ("causal_lm_sdpa", AutoModelForCausalLM, "sdpa"),
):
    try:
        m = cls.from_pretrained(
            path, revision=pins.MODEL_REVISION, dtype=torch.bfloat16, device_map="cuda", attn_implementation=attn
        ).eval()
    except Exception as e:  # noqa: BLE001
        out[label] = f"load failed: {type(e).__name__}: {str(e)[:160]}"
        print(label, out[label], flush=True)
        continue
    nll = []
    with torch.no_grad():
        for ids in texts:
            x = torch.tensor([ids], device="cuda")
            logits = m(input_ids=x, use_cache=False).logits[0].float()
            nll.append(float(torch.nn.functional.cross_entropy(logits[3:-1], x[0, 4:])))
    out[label] = sum(nll) / len(nll)
    print(label, type(m).__name__, out[label], flush=True)
    del m
    gc.collect()
    torch.cuda.empty_cache()
print(json.dumps(out))
