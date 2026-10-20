# Diagnostic: what the 27B answers on natural_rw MX (conflict) prompts. PYTHONPATH=. uv run python scripts/debug_mx_conflict.py
import collections
import sys

import torch

sys.argv = ["x"]
from bridge_jspace.model import load_model
from scripts import natural_rw as N
from scripts import twohop_pilot as T

model = load_model()
tok = model.tokenizer
cases = [c for c in N.build(tok, model, ("MX",))][:40]
tally = collections.Counter()
for c in cases:
    text = model.generate_batch(torch.tensor([c["ids"]], device="cuda"), 12, [{}])[0]
    prompt_ok = T.judge(text, c["aliases"])
    real_ok = c["real_answer"].split()[0].lower() in text.lower() or (
        "United States" in c["real_answer"] and ("USA" in text or "United States" in text)
    )
    tally["prompt's country" if prompt_ok else "real country" if real_ok else "other"] += 1
    if sum(tally.values()) <= 4:
        print(repr(tok.decode(c["ids"][-120:]))[:420])
        print("  ->", repr(text), "| prompt says", c["answer"], "| real", c["real_answer"])
print(dict(tally), "of", len(cases))
