"""r_matched (Zach, 2026-10-25, beside amendment 35): v2.1's RF - MF on matched pairs only. The scorer's RF - MF compares
each start's own eligible scenes, and R scenes are harder (the bridge never named), so the two sides can hold different
items. Here only pairs whose R item and its M item (derived_from) were both right unedited are kept; loss per word and
RF - MF with a 95% bootstrap over bridges (seed 0), per condition.

python scripts/r_matched.py V2_RUN R_RUN --set jsuite_v2_1_test_chat
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "ablate_v2"


def main(v2: str, rrun: str, set_name: str) -> None:
    items = {json.loads(x)["id"]: json.loads(x) for x in (ROOT / "data" / "tasks_v2" / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(x) for run in (v2, rrun) for x in (RES / run / "rows.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items]
    ok = {r["id"] for r in rows if r["condition"] == "none" and r["correct"]}
    pairs = [(i, items[i]["derived_from"]) for i in ok if items[i].get("start") == "R" and items[i]["derived_from"] in ok]
    keep = {x for p in pairs for x in p}
    out = {"v2": v2, "r": rrun, "n_pairs": len(pairs), "by_word_pairs": dict(collections.Counter(items[r]["word"] for r, _ in pairs)), "cells": {}}
    print(f"{len(pairs)} matched pairs {out['by_word_pairs']}")
    for cond in dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"):
        sel = collections.defaultdict(list)
        for r in rows:
            if r["condition"] == cond and r["id"] in keep:
                it = items[r["id"]]
                sel[it["word"]].append((f"{it['relation']}:{it['bridge']}", r["correct"]))
        loss = {w: 100 * (1 - sum(c for _, c in v) / len(v)) for w, v in sel.items()}
        clusters, rng = sorted({b for v in sel.values() for b, _ in v}), random.Random(0)
        cell = {"loss": {w: round(v, 1) for w, v in loss.items()}, "contrasts": {}}
        for f in "MAN":
            a, b = "R" + f, "M" + f
            if a not in sel or b not in sel:
                continue
            bs = []
            for _ in range(1000):
                pick = collections.Counter(rng.choice(clusters) for _ in clusters)
                lb = {}
                for w in (a, b):
                    tot = [(c, pick[k]) for k, c in sel[w] if pick[k]]
                    n = sum(m for _, m in tot)
                    lb[w] = 100 * (1 - sum(c * m for c, m in tot) / n) if n else None
                if None not in lb.values():
                    bs.append(lb[a] - lb[b])
            bs.sort()
            cell["contrasts"][f"{a}-{b}"] = {"diff": round(loss[a] - loss[b], 1), "ci": [round(bs[int(0.025 * len(bs))]), round(bs[int(0.975 * len(bs)) - 1])]}
        out["cells"][cond] = cell
        print(f"{cond:14s} lost " + " ".join(f"{w} {v:.0f}" for w, v in sorted(loss.items())) + "  "
              + "  ".join(f"{k} {v['diff']:+.0f} {v['ci']}" for k, v in cell["contrasts"].items()))  # fmt: skip
    (RES / "r_matched").mkdir(exist_ok=True)
    (RES / "r_matched" / f"{rrun}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("v2")
    ap.add_argument("r")
    ap.add_argument("--set", required=True)
    a = ap.parse_args()
    main(a.v2, a.r, a.set)
