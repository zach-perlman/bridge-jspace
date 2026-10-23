"""nat3_score (Zach, 2026-10-23, prereg amendment 15): a knock-out run on nat3_v1_chat, all 8 three-step words.
Per condition: accuracy lost (points, items right unedited) per word, and each word's excess over P->P->P with a 95%
bootstrap interval over start entities (resampled jointly across words); by chain type too. Clean words (no adjacent
memory hops): PPP, MPP, PMP, PPM, MPM; skip-prone: PMM, MMM, MMP. --min-p keeps only items the model answers
with at least that probability unedited (most lucky guesses on a 5-way answer are low-confidence). Descriptive.
Writes results/ablate_v2/nat3_score/RUN[_pX].json.

python scripts/nat3_score.py RUN [--set nat3_v1_chat]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
WORDS = ("PPP", "MPP", "PMP", "PPM", "MPM", "MMP", "PMM", "MMM")
CLEAN = ("PPP", "MPP", "PMP", "PPM", "MPM")


def main(run: str, set_name: str, min_p: float = 0.0) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    import math

    floor = math.log(min_p) if min_p > 0 else -math.inf
    ok = {(r["family"], r["id"]) for r in rows
          if r["condition"] == "none" and r["correct"] and r["kind"] == "clean" and r["logp"] >= floor}  # fmt: skip
    conds = list(dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"))
    out: dict = {"run": run, "set": set_name, "min_p": min_p, "cells": {}}
    rng = random.Random(0)
    for split in ("all", "cities", "people"):
        for cond in conds:
            sel = collections.defaultdict(list)  # word -> [(start, correct)]
            for r in rows:
                if r["condition"] != cond or r["kind"] != "clean" or (r["family"], r["id"]) not in ok:
                    continue
                it = items[r["id"]]
                if split != "all" and it["domain"] != split:
                    continue
                sel[r["family"]].append((it["bridge"], r["correct"]))
            words = [w for w in WORDS if sel[w]]
            if "PPP" not in words:
                continue
            loss = {w: 100 * (1 - sum(c for _, c in sel[w]) / len(sel[w])) for w in words}
            starts = sorted({b for w in words for b, _ in sel[w]})
            boots = collections.defaultdict(list)
            for _ in range(1000):
                pick = collections.Counter(rng.choice(starts) for _ in starts)
                lb = {}
                for w in words:
                    tot = [(c, pick[b]) for b, c in sel[w] if pick[b]]
                    n = sum(m for _, m in tot)
                    lb[w] = 100 * (1 - sum(c * m for c, m in tot) / n) if n else None
                for w in words:
                    if lb[w] is not None and lb["PPP"] is not None:
                        boots[w].append(lb[w] - lb["PPP"])
            cell = {}
            for w in words:
                b = sorted(boots[w])
                ci = [round(b[int(0.025 * len(b))]), round(b[int(0.975 * len(b)) - 1])] if b else None
                cell[w] = {"loss": round(loss[w], 1), "excess_over_PPP": round(loss[w] - loss["PPP"], 1), "ci": ci, "n": len(sel[w]),
                           "clean": w in CLEAN}  # fmt: skip
            out["cells"][f"{split}/{cond}"] = cell
            print(f"{split:7s} {cond:14s} " + "  ".join(f"{w} {cell[w]['loss']:4.0f} ({cell[w]['excess_over_PPP']:+.0f} {cell[w]['ci']}, n={cell[w]['n']})"
                                                       for w in words))  # fmt: skip
    (RES / "nat3_score").mkdir(exist_ok=True)
    (RES / "nat3_score" / f"{run}{'_p%g' % min_p if min_p else ''}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", default="nat3_v1_chat")
    ap.add_argument("--min-p", type=float, default=0.0, help="only items whose unedited answer probability is at least this (lucky guesses out)")
    a = ap.parse_args()
    main(a.run, a.set, a.min_p)
