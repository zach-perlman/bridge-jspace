"""dose_gaps: the C1 gap by dose (number of top lens directions removed) from an ablate_v2 dose run (Zach, 2026-10-23).
Accuracy lost (points) on items right unedited, per rule word, for each condition (topK and topK_rot); gap = mean(P->M,
M->M) - mean(P->P, M->P), as scripts/c1_v2.py's rule. Descriptive (no rule). Writes results/ablate_v2/dose_gaps/RUN.json.

python scripts/dose_gaps.py RUN
"""

import collections
import json
import sys
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"
WORDS = ("PP", "MP", "PM", "MM")


def main(run: str) -> None:
    rows = [json.loads(line) for line in open(RES / run / "rows.jsonl")]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    acc = collections.defaultdict(list)
    for r in rows:
        if r["condition"] != "none" and (r["family"], r["id"]) in ok:
            acc[(r["band"], r["condition"], r["family"])].append(r["correct"])
    out = {"run": run, "n_right_unedited": dict(collections.Counter(f for f, _ in ok)), "cells": {}}
    for band, cond in sorted({(b, c) for b, c, _ in acc}):
        loss = {w: round(100 * (1 - sum(acc[(band, cond, w)]) / len(acc[(band, cond, w)])), 1) for w in WORDS if acc[(band, cond, w)]}
        if len(loss) == 4:
            gap = (loss["PM"] + loss["MM"]) / 2 - (loss["PP"] + loss["MP"]) / 2
            out["cells"][f"{band}/{cond}"] = {"loss": loss, "gap": round(gap, 1)}
            print(f"{band} {cond:12s} " + " ".join(f"{w} {loss[w]:5.1f}" for w in WORDS) + f"  gap {gap:5.1f}")
    (RES / "dose_gaps").mkdir(exist_ok=True)
    (RES / "dose_gaps" / f"{run}.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
