"""Diagnostic: what the 27B answers on natural_rw's MX (conflict) prompts, the prompt's country or the real one.
python scripts/debug_mx_conflict.py"""

import collections
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace.model import load_model
from scripts import natural_rw as N
from scripts import twohop_pilot as T


@torch.no_grad()
def main(n: int = 40) -> None:
    model = load_model()
    tok = model.tokenizer
    cases = N.build(tok, model, ("MX",))[:n]
    tally: collections.Counter = collections.Counter()
    for c in cases:
        text = model.generate_batch(torch.tensor([c["ids"]], device="cuda"), 12, [{}])[0]
        real = c["real_answer"]
        real_ok = real.split()[0].lower() in text.lower() or (
            "United States" in real and ("USA" in text or "United States" in text)
        )
        tally["prompt's country" if T.judge(text, c["aliases"]) else "real country" if real_ok else "other"] += 1
        if sum(tally.values()) <= 4:
            print(repr(tok.decode(c["ids"][-120:]))[:420])
            print("  ->", repr(text), "| prompt says", c["answer"], "| real", real)
    print(dict(tally), "of", len(cases))


if __name__ == "__main__":
    main()
