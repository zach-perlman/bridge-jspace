"""kernel_nll (Zach, 2026-10-25, amendment 44): the target's mean next-token NLL and per-position top-1 on the first 32
pinned WikiText rows of >= 64 words (128 tokens, encoded as the harness does), loaded as the harness loads it; run
once with kernels and once with BJ_NO_KERNELS=1 to check the kernels against the torch path.
BJ_TARGET=KEY python scripts/kernel_nll.py OUT.pt"""
import os
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins, tokens  # noqa: E402
from bridge_jspace.model import load_model  # noqa: E402

torch.set_grad_enabled(False)
m = load_model()
rows = [r[:2000] for r in pins.wikitext_rows() if len(r.split()) >= 64][:32]
nll, top = [], []
for r in rows:
    x = torch.tensor([tokens.raw_encoding(m.tokenizer, r)["input_ids"][:128]], device="cuda")
    lg = m.hf(input_ids=x, use_cache=False).logits[0].float()
    nll.append(torch.nn.functional.cross_entropy(lg[:-1], x[0, 1:], reduction="none").cpu())
    top.append(lg[:-1].argmax(-1).cpu())
torch.save({"nll": nll, "top": top, "kernels": not os.environ.get("BJ_NO_KERNELS")}, sys.argv[1])
print("KNLL", round(torch.cat(nll).mean().item(), 4), "kernels" if not os.environ.get("BJ_NO_KERNELS") else "torch")
