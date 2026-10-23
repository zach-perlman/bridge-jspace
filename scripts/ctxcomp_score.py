"""ctxcomp_score (Zach, 2026-10-23, prereg amendment 21): a knock-out run on ctxcomp_v1_chat (12 words SF: start S in
P stated, K counted, A arithmetic, M recalled; final F in R report, P seat lookup, M recall). Per condition: points
lost per word (items right unedited), and amendment 21's contrasts with 95% bootstrap intervals over scenes
(resampled within each start; a scene holds its start's R, P and M items):
  final rule   SM - SP for each start S (prediction 1: >= 20)
  computation  KP - PP, AP - PP (prediction 2: within 10)
  report       KR - PR, AR - PR (prediction 3: >= 15)
Descriptive besides those. Writes results/ablate_v2/ctxcomp_score/RUN.json.

python scripts/ctxcomp_score.py RUN [--set ctxcomp_v1_chat]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
STARTS, FINALS = "PKAM", "RPM"
CONTRASTS = [(f"{s}M", f"{s}P") for s in STARTS] + [("KP", "PP"), ("AP", "PP"), ("KR", "PR"), ("AR", "PR"), ("MR", "PR")]


def main(run: str, set_name: str) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"] and r["kind"] == "clean"}
    conds = list(dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"))
    out: dict = {"run": run, "set": set_name, "cells": {}}
    rng = random.Random(0)
    for cond in conds:
        sel = collections.defaultdict(list)  # word -> [(scene, correct)]
        for r in rows:
            if r["condition"] == cond and r["kind"] == "clean" and (r["family"], r["id"]) in ok:
                sel[r["family"]].append((items[r["id"]]["scene"], r["correct"]))
        words = [s + f for s in STARTS for f in FINALS if sel[s + f]]
        loss = {w: 100 * (1 - sum(c for _, c in sel[w]) / len(sel[w])) for w in words}
        scenes = {s: sorted({sc for f in FINALS for sc, _ in sel[s + f]}) for s in STARTS}
        boots = collections.defaultdict(list)
        for _ in range(1000):
            pick = {s: collections.Counter(rng.choice(scenes[s]) for _ in scenes[s]) for s in STARTS if scenes[s]}
            lb = {}
            for w in words:
                tot = [(c, pick[w[0]][sc]) for sc, c in sel[w] if pick[w[0]][sc]]
                n = sum(m for _, m in tot)
                lb[w] = 100 * (1 - sum(c * m for c, m in tot) / n) if n else None
            for a, b in CONTRASTS:
                if lb.get(a) is not None and lb.get(b) is not None:
                    boots[f"{a}-{b}"].append(lb[a] - lb[b])
        cell = {"loss": {w: round(loss[w], 1) for w in words}, "n": {w: len(sel[w]) for w in words}, "contrasts": {}}
        for a, b in CONTRASTS:
            bs = sorted(boots[f"{a}-{b}"])
            if a in loss and b in loss and bs:
                cell["contrasts"][f"{a}-{b}"] = {"diff": round(loss[a] - loss[b], 1),
                                                 "ci": [round(bs[int(0.025 * len(bs))]), round(bs[int(0.975 * len(bs)) - 1])]}  # fmt: skip
        out["cells"][cond] = cell
        print(f"{cond:14s} lost " + " ".join(f"{w} {loss[w]:3.0f}" for w in words) + "  n " + str([len(sel[w]) for w in words]))
        print(f"{'':14s} " + "  ".join(f"{k} {v['diff']:+.0f} {v['ci']}" for k, v in cell["contrasts"].items()))
    (RES / "ctxcomp_score").mkdir(exist_ok=True)
    (RES / "ctxcomp_score" / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", default="ctxcomp_v1_chat")
    a = ap.parse_args()
    main(a.run, a.set)
