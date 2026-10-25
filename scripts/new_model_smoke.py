"""new_model_smoke (Zach, 2026-10-25, prereg amendment 40): load checks on a new target (BJ_TARGET) before its lens fit
and runs, no lens needed; the numbers are for a human to read.
1. Blocks: the model's block count is pins' n_layers; the final norm the harness reads (NemotronH: norm_f).
2. Unembed: model.unembed(the last block's output) against the model's own final-position logits.
3. Plain text: mean next-token NLL over the first 32 pinned WikiText rows of >= 64 words (128 tokens), encoded as the
   harness encodes raw text (tokens.raw_encoding: a BOS only if pins says so), and with a BOS first, for comparison.
4. Chat: chat.chat_text on one short question (thinking off, "Answer:" prefilled), and the greedy continuation.
Writes results/checks/PREFIXsmoke.json.

BJ_TARGET=KEY python scripts/new_model_smoke.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import chat, pins, tokens  # noqa: E402
from bridge_jspace.model import load_model  # noqa: E402


@torch.no_grad()
def nll(m, ids: list[int]) -> float:
    x = torch.tensor([ids], device="cuda")
    logits = m.hf(input_ids=x, use_cache=False).logits[0].float()
    return torch.nn.functional.cross_entropy(logits[:-1], x[0, 1:]).item()


def main() -> None:
    torch.set_grad_enabled(False)
    t0 = time.time()
    m = load_model()
    out: dict = {"model": pins.model_pin(), "n_layers": pins.N_LAYERS, "final_norm": type(m.final_norm).__name__,
                 "bos": pins.TARGETS[pins.TARGET]["bos"], "load_s": round(time.time() - t0)}  # fmt: skip
    last = pins.N_LAYERS - 1
    logits, rec = m.run(m.encode("The capital of France is"), record=(last,))
    mine = m.unembed(rec[last][-1:])[0]
    out["unembed"] = {"max_abs_diff": round((mine - logits).abs().max().item(), 4), "top1_same": int(mine.argmax()) == int(logits.argmax()),
                      "top1": m.decoded[int(logits.argmax())]}  # fmt: skip
    rows = [r[:2000] for r in pins.wikitext_rows() if len(r.split()) >= 64][:32]
    plain = [tokens.raw_encoding(m.tokenizer, r)["input_ids"][:128] for r in rows]
    bos = m.tokenizer.bos_token_id
    out["wikitext_nll"] = {"as_harness": round(sum(nll(m, i) for i in plain) / len(plain), 3), "n": len(plain)}
    if bos is not None and plain[0][0] != bos:
        out["wikitext_nll"]["bos_first"] = round(sum(nll(m, [bos, *i[:127]]) for i in plain) / len(plain), 3)
    text = chat.chat_text(m.tokenizer, "What is the capital of Australia? " + chat.QUESTION_INSTRUCTION)
    ids = torch.tensor([m.tokenizer(text, add_special_tokens=False).input_ids], device="cuda")
    out["chat"] = {"rendered": text, "greedy": m.greedy_text(ids, max_new_tokens=8)}
    print(json.dumps(out, indent=1))
    path = pins.RESULTS_DIR / "checks" / f"{pins.RUN_PREFIX}smoke.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
