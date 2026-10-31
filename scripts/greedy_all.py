"""greedy_all (Zach, 2026-10-27, prereg amendment 58 note 1): the model's raw greedy reply to every item's whole
question, unedited. The competence and knock-out runs read only whether the answer's first token outranks the
relation's other answers (cand2). This records what the model actually writes, for every item (eligible or not), so
free-generation accuracy, answer form and any reasoning before the answer can be scored later (note 2's rule, CPU).
Prompts are built exactly as ablate_v2.tasks_prompts builds the whole question (tasks_v2.render, thinking off,
"Answer:" prefilled, a space after it for digit answers). Greedy, --max-new tokens, prompts of one length batched
together (no padding: the hybrid models' recurrent layers would see pad tokens). Descriptive, no rule.
Writes results/greedy_all/NAME/{manifest.json, rows.jsonl, summary.json}.

python scripts/greedy_all.py --name N --why W [--set jsuite_v2_test_chat] [--max-new 24] [--batch 32] [--limit K]
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
from scripts import suite_v1 as S  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402

RESULTS = pins.RESULTS_DIR / "greedy_all"


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
    items = T.load(args.set)
    if args.limit:  # smoke: the first --limit items of each word
        seen: collections.Counter = collections.Counter()
        items = [it for it in items if (seen.update([it["word"]]) or seen[it["word"]] <= args.limit)]
    prompts = []
    for it in items:
        ids = S.ids(tok, T.render(tok, {**it, "_question": it["question"], "_kind": it["kind"]}))
        ids += S.ids(tok, " ") if it["kind"] == "digit" else []
        prompts.append((it, ids))
    (out_dir / "manifest.json").write_text(json.dumps({
        "run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": commit, "model": pins.model_pin(), "set": args.set, "n_items": len(prompts),
        "max_new_tokens": args.max_new, "batch": args.batch, "limit": args.limit, "greedy": True,
        "doc": (__doc__ or "").split("\n\n")[0]}, indent=2) + "\n")  # fmt: skip
    by_len: dict = collections.defaultdict(list)
    for it, ids in prompts:
        by_len[len(ids)].append((it, ids))
    t0, done = time.time(), 0
    with (out_dir / "rows.jsonl").open("w") as f:
        for n in sorted(by_len):
            group = by_len[n]
            for i in range(0, len(group), args.batch):
                chunk = group[i : i + args.batch]
                ids = torch.tensor([x[1] for x in chunk], device="cuda")
                texts = model.generate_batch(ids, args.max_new, [{} for _ in chunk])
                for (it, _), text in zip(chunk, texts, strict=True):
                    f.write(json.dumps({"id": it["id"], "word": it["word"], "module": it.get("module"),
                                        "relation": it.get("relation") or it.get("domain"), "level": it.get("level"),
                                        "kind": it["kind"], "answer": it["answer"], "bridge": it.get("bridge"),
                                        "text": text}) + "\n")  # fmt: skip
                done += len(chunk)
            f.flush()
            print(f"{done}/{len(prompts)} {time.time() - t0:.0f}s", flush=True)
    (out_dir / "summary.json").write_text(json.dumps({"seconds": round(time.time() - t0), "n": done}) + "\n")
    print("done", done, round(time.time() - t0), "s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--set", default="jsuite_v2_test_chat")
    ap.add_argument("--max-new", type=int, default=24)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--limit", type=int, default=0)
    main(ap.parse_args())
