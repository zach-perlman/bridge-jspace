"""natplus_split (Zach, 2026-10-23, prereg amendment 14): a knock-out run on natplus_v1_chat scored by popularity
(popular / rare bridges) and by relation, with 95% bootstrap intervals over bridge entities. Accuracy lost (points,
items right unedited) per word and the gap (mean of P->M, M->M minus mean of P->P, M->P), for every condition in the
run. Descriptive. Writes results/ablate_v2/natplus_split/RUN.json.

python scripts/natplus_split.py RUN [--set natplus_v1_chat]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
WORDS = ("PP", "MP", "PM", "MM")


def gap_of(loss: dict) -> float:
    return (loss["PM"] + loss["MM"]) / 2 - (loss["PP"] + loss["MP"]) / 2


def main(run: str, set_name: str) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    conds = list(dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"))
    cells: dict = collections.defaultdict(list)  # (split, value, cond, word) -> [(bridge, correct)]
    for r in rows:
        if r["condition"] == "none" or (r["family"], r["id"]) not in ok:
            continue
        it = items[r["id"]]
        for split, val in (("all", "all"), ("popularity", it["popularity"]), ("relation", it["domain"]),
                           ("relation_popularity", f"{it['domain']}/{it['popularity']}")):  # fmt: skip
            cells[(split, val, r["condition"], r["family"])].append((it["bridge"], r["correct"]))
    rng = random.Random(0)
    out: dict = {"run": run, "set": set_name, "cells": {}}
    for split, val in sorted({(s, v) for s, v, _, _ in cells}):
        for cond in conds:
            sel = {w: cells.get((split, val, cond, w), []) for w in WORDS}
            if not all(sel.values()):
                continue
            loss = {w: 100 * (1 - sum(c for _, c in v) / len(v)) for w, v in sel.items()}
            bridges = sorted({b for v in sel.values() for b, _ in v})
            boots = []
            for _ in range(1000):  # resample bridge entities, every word together
                pick = collections.Counter(rng.choice(bridges) for _ in bridges)
                lb = {}
                for w, v in sel.items():
                    tot = [(c, pick[b]) for b, c in v if pick[b]]
                    n = sum(m for _, m in tot)
                    lb[w] = 100 * (1 - sum(c * m for c, m in tot) / n) if n else None
                if None not in lb.values():
                    boots.append(gap_of(lb))
            boots.sort()
            ci = [round(boots[int(0.025 * len(boots))]), round(boots[int(0.975 * len(boots)) - 1])] if boots else None
            out["cells"][f"{split}/{val}/{cond}"] = {"loss": {w: round(x, 1) for w, x in loss.items()}, "gap": round(gap_of(loss), 1),
                                                     "gap_ci": ci, "n": {w: len(v) for w, v in sel.items()}}  # fmt: skip
            print(f"{split:20s} {val:22s} {cond:14s} " + " ".join(f"{w} {loss[w]:5.1f}" for w in WORDS)
                  + f"  gap {gap_of(loss):5.1f} {ci}  n {[len(sel[w]) for w in WORDS]}")  # fmt: skip
    (RES / "natplus_split").mkdir(exist_ok=True)
    (RES / "natplus_split" / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", default="natplus_v1_chat")
    a = ap.parse_args()
    main(a.run, a.set)
