"""nn_ko_read (Zach, 2026-10-29, amendment 59): note 20's knock-out reading for one ablate_v2 v4 run, with its intervals (the
committed version of the ad hoc scorer used for notes 20 and 24). Loss = accuracy without the edit minus with it, on the gated
items; gap = MM loss - MP loss; bootstrap over items (2000 draws, seed 0). Writes results/ablate_v2/nn_ko_read/RUN.json.
python scripts/nn_ko_read.py RUN [RUN ...]
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"


def main(run: str) -> dict:
    acc = collections.defaultdict(dict)
    for line in (RES / run / "rows.jsonl").open():
        r = json.loads(line)
        acc[(r["family"], r["condition"])][r["id"]] = bool(r["correct_cand2"])
    ids = {f: sorted(acc[(f, "none")]) for f in ("MM", "MP")}
    out = {"run": run, "n": {f: len(v) for f, v in ids.items()}, "conditions": {}}
    rng = random.Random(0)

    def loss(f, c, sel):
        return 100 * (sum(acc[(f, "none")][i] for i in sel) - sum(acc[(f, c)][i] for i in sel)) / len(sel)

    for c in sorted({c for _, c in acc} - {"none"}):
        bs = sorted(loss("MM", c, [rng.choice(ids["MM"]) for _ in ids["MM"]]) - loss("MP", c, [rng.choice(ids["MP"]) for _ in ids["MP"]]) for _ in range(2000))
        out["conditions"][c] = {"loss_MM": round(loss("MM", c, ids["MM"]), 1), "loss_MP": round(loss("MP", c, ids["MP"]), 1),
                                "gap": round(loss("MM", c, ids["MM"]) - loss("MP", c, ids["MP"]), 1), "gap_ci": [round(bs[50], 1), round(bs[1949], 1)]}  # fmt: skip
    d = RES / "nn_ko_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")
    print(run, out["n"], json.dumps(out["conditions"]))
    return out


if __name__ == "__main__":
    for r in sys.argv[1:]:
        main(r)
