"""competence_variants (Zach, 2026-10-27, prereg amendment 58 note 2): unedited accuracy of every item of the chosen words
under prompt variants, after Redwood's no-CoT tests (Greenblatt 2026): "none" (the competence prompt), "filler300" (the
question followed by the integers 1..300, content-free filler, before the instruction) and "repeat5" (the question
written five times). The passage is unchanged. Reads: cand2 on the first generated token (as competence and the
knock-outs read) and the greedy reply (--max-new tokens), one generate per batch of same-length prompts (no padding).
Descriptive, no rule. Writes results/competence_variants/NAME/{manifest.json, rows.jsonl, summary.json}.

python scripts/competence_variants.py --name N --why W [--set jsuite_v2_1_test_chat] --words RM RA ... [--limit K]
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from scripts import ablate_v2 as AV  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402

RESULTS = pins.RESULTS_DIR / "competence_variants"
FILLER = " ".join(str(i) for i in range(1, 301))


def variant(q: str, v: str) -> str:
    if v == "none":
        return q
    if v == "filler300":
        return f"{q}\n\n{FILLER}\n\n"
    if v == "repeat5":
        return "\n".join([q] * 5)
    raise ValueError(v)


def prompt(tok, it: dict, v: str, set_name: str) -> dict:
    """The whole question's prompt and its read, as ablate_v2.tasks_prompts builds them (kind 'clean')."""
    k = it["kind"]
    ids = S.ids(tok, T.render(tok, {**it, "_question": variant(it["question"], v), "_kind": k}))
    ids += S.ids(tok, " ") if k == "digit" else []
    p = {"ids": ids, "tok": S.answer_token(tok, it["answer"], k)}
    vocab = it.get("answer_vocab") or AV.natural_vocab(set_name)[(it["domain"], "answer")]
    both = lambda x: {S.answer_token(tok, x, k), S.answer_token(tok, x.lower(), k)}  # noqa: E731
    p["cands"] = sorted({S.answer_token(tok, x, k) for x in vocab} | {p["tok"]})
    p["ok2"] = sorted(both(it["answer"]))
    p["cands2"] = sorted({t for x in vocab for t in both(x)} | set(p["ok2"]))
    return p


@torch.no_grad()
def main(args) -> None:
    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out_dir = RESULTS / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    items = [it for it in T.load(args.set) if it.get("word") in set(args.words)]
    if args.limit:
        seen: collections.Counter = collections.Counter()
        items = [it for it in items if (seen.update([it["word"]]) or seen[it["word"]] <= args.limit)]
    jobs = [(it, v, prompt(tok, it, v, args.set)) for it in items for v in args.variants]
    (out_dir / "manifest.json").write_text(json.dumps({
        "run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": commit, "model": pins.model_pin(), "set": args.set, "words": args.words, "variants": args.variants,
        "n_items": len(items), "max_new_tokens": args.max_new, "batch": args.batch, "limit": args.limit, "read": "cand2",
        "doc": (__doc__ or "").split("\n\n")[0]}, indent=2) + "\n")  # fmt: skip
    by_len: dict = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j[2]["ids"])].append(j)
    t0, done, rows = time.time(), 0, []
    with (out_dir / "rows.jsonl").open("w") as f:
        for n in sorted(by_len):
            group = by_len[n]
            for i in range(0, len(group), args.batch):
                chunk = group[i : i + args.batch]
                ids = torch.tensor([j[2]["ids"] for j in chunk], device="cuda")
                texts, logits = model.generate_batch(ids, args.max_new, [{} for _ in chunk], first_logits=True)
                for row, ((it, v, p), text) in enumerate(zip(chunk, texts, strict=True)):
                    r = {"id": it["id"], "word": it["word"], "variant": v, "answer": it["answer"], "text": text,
                         **AV.reads(logits[row], p, "cand2")}  # fmt: skip
                    rows.append(r)
                    f.write(json.dumps(r) + "\n")
                done += len(chunk)
            f.flush()
            print(f"{done}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    cells = {}
    for w in args.words:
        for v in args.variants:
            rs = [r for r in rows if r["word"] == w and r["variant"] == v]
            if rs:
                cells[f"{w}/{v}"] = {"n": len(rs), "acc_cand2": round(sum(r["correct_cand2"] for r in rs) / len(rs), 4)}
    (out_dir / "summary.json").write_text(json.dumps({"seconds": round(time.time() - t0), "n": done, "cells": cells}, indent=1) + "\n")
    print("done", done, round(time.time() - t0), "s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--set", default="jsuite_v2_1_test_chat")
    ap.add_argument("--words", nargs="+", required=True)
    ap.add_argument("--variants", nargs="+", default=["none", "filler300", "repeat5"])
    ap.add_argument("--max-new", type=int, default=24)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0)
    main(ap.parse_args())
