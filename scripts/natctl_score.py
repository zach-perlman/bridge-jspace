"""natctl_score (Zach, 2026-10-23, prereg amendment 16): a knock-out run on natctl_v1_chat. Per condition and start
(P, M): accuracy lost (points, items right unedited) for the four final hops (P new fact in the prompt, K true fact in
the prompt, M recall with the answer word absent, A recall with the answer word present as a distractor value), and
the contrasts K-M, A-M, P-K, P-M with 95% bootstrap intervals over bridge entities (resampled jointly). Descriptive.
Writes results/ablate_v2/natctl_score/RUN.json.

python scripts/natctl_score.py RUN [--set natctl_v1_chat]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
CONTRASTS = (("K", "M"), ("A", "M"), ("P", "K"), ("P", "M"))


def main(run: str, set_name: str) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"] and r["kind"] == "clean"}
    conds = list(dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"))
    out: dict = {"run": run, "set": set_name, "cells": {}}
    rng = random.Random(0)
    for start in ("P", "M", "both"):
        for cond in conds:
            sel = collections.defaultdict(list)  # final -> [(bridge, correct)]
            for r in rows:
                if r["condition"] != cond or r["kind"] != "clean" or (r["family"], r["id"]) not in ok:
                    continue
                if start != "both" and r["family"][0] != start:
                    continue
                sel[r["family"][1]].append((items[r["id"]]["bridge"], r["correct"]))
            if not all(sel[f] for f in "PKMA"):
                continue
            loss = {f: 100 * (1 - sum(c for _, c in sel[f]) / len(sel[f])) for f in "PKMA"}
            bridges = sorted({b for f in "PKMA" for b, _ in sel[f]})
            boots = collections.defaultdict(list)
            for _ in range(1000):
                pick = collections.Counter(rng.choice(bridges) for _ in bridges)
                lb = {}
                for f in "PKMA":
                    tot = [(c, pick[b]) for b, c in sel[f] if pick[b]]
                    n = sum(m for _, m in tot)
                    lb[f] = 100 * (1 - sum(c * m for c, m in tot) / n) if n else None
                for a, b in CONTRASTS:
                    if lb[a] is not None and lb[b] is not None:
                        boots[a + "-" + b].append(lb[a] - lb[b])
            cell = {"loss": {f: round(loss[f], 1) for f in "PKMA"}, "n": {f: len(sel[f]) for f in "PKMA"}, "contrasts": {}}
            for a, b in CONTRASTS:
                bs = sorted(boots[a + "-" + b])
                ci = [round(bs[int(0.025 * len(bs))]), round(bs[int(0.975 * len(bs)) - 1])] if bs else None
                cell["contrasts"][a + "-" + b] = {"diff": round(loss[a] - loss[b], 1), "ci": ci}
            out["cells"][f"{start}/{cond}"] = cell
            print(f"start {start:4s} {cond:14s} lost P {loss['P']:4.0f} K {loss['K']:4.0f} M {loss['M']:4.0f} A {loss['A']:4.0f}  n {[len(sel[f]) for f in 'PKMA']}  "
                  + "  ".join(f"{k} {v['diff']:+.0f} {v['ci']}" for k, v in cell["contrasts"].items()))  # fmt: skip
    (RES / "natctl_score").mkdir(exist_ok=True)
    (RES / "natctl_score" / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", default="natctl_v1_chat")
    a = ap.parse_args()
    main(a.run, a.set)
