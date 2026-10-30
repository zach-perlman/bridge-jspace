"""f11_parts_recount: the archived F11 arms recomputed from the run files on the current code (POST HOC; Dan 31 Oct; CPU, report only).

F11 ("parts at unequal shares", superseded by F14) removed four parts of the one-change edit, each against a random part of its own share, at the model's X0 layer
(9B L12, 27B L32; the single-change items, n = 200): the bridge word only (w), J++ with the word's own tokens banned (jw), the layer's top-2,000 PCA directions (pca),
J++ (jpp). This reads the saved outcomes.jsonl / shares.jsonl of x0_parts/qwen35_9b_x0_parts and x0_parts_27b with x0_necessity.cells_of (the switches blocked beyond
the random part, `excess`, 95% cluster-bootstrap intervals over the bridge entity, seed 0) and sets each cell beside the archived verdict.json row.

uv run python scripts/f11_parts_recount.py        # writes results/f11_parts_recount/<UTC>/
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import x0_necessity as X  # noqa: E402

RUNS = {"qwen3.5-9b": "qwen35_9b_x0_parts", "qwen3.6-27b": "x0_parts_27b"}
PARTS = ("w", "jw", "pca", "jpp")


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "f11_parts_recount" / stamp
    out.mkdir(parents=True, exist_ok=False)
    (out / "manifest.json").write_text(json.dumps({"exp": "f11_parts_recount", "post_hoc": True, "cpu": True, "runs": RUNS, "written_utc": stamp}, indent=2) + "\n")
    res: dict = {}
    for model, run in RUNS.items():
        src = REPO / "results" / "x0_parts" / run
        m = json.loads((src / "manifest.json").read_text())
        rows = X.read_jsonl(src / "outcomes.jsonl")
        shares = X.read_jsonl(src / "shares.jsonl")
        cells = X.cells_of(rows, X.N_BOOT)
        old_path = sorted(src.glob("verdict-*/verdict.json"))[-1]
        old = {(r["part"], r["reader"]): r for r in json.loads(old_path.read_text())["rows"]}
        res[model] = {"run": run, "layer": m["layer"], "items": m["items"], "archived_verdict": str(old_path.relative_to(REPO)), "cells": {}}
        for d in PARTS:
            share = statistics.median(s["share"] for s in shares if s["dict"] == d)
            for w in X.READERS:
                c = cells[next(k for k in cells if k[2] == w and k[3] == d)]
                res[model]["cells"][f"{d}/{'lookup' if w == X.LOOKUP else 'recall'}"] = {
                    "median_share": round(share, 4), "excess": [round(v, 4) for v in c["excess"]],
                    "archived_excess": [round(v, 4) for v in old[(d, w)]["excess"]], "label": c["label"]}  # fmt: skip
        res[model]["reproduces_archived"] = all(v["excess"] == v["archived_excess"] for v in res[model]["cells"].values())
    (out / "tables.json").write_text(json.dumps(res, indent=1) + "\n")
    print(out)
    for model, d in res.items():
        print(model, "reproduces the archived verdict:", d["reproduces_archived"])
        for k, v in d["cells"].items():
            print(f"  {k:12s} share {v['median_share']:.3f}  excess {v['excess']}  {v['label']}")
    return out


if __name__ == "__main__":
    main()
