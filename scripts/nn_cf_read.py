"""nn_cf_read (Zach, 2026-10-28, prereg amendment 58 note 14): the counterfactual-patching map on jsuite_v4, read (CPU).

Rows from nn_swap runs on v4 (--items v4ok, conditions *_cf: the counterfactual prompt, same passage, the question about
another scene entity D), pooled over the runs given (donor seeds); per site (the run's --site), word (MP lookup / MM
recall twin) and layer window. Classes: donor = D's answer (MP: D's passage value; MM: D's remembered attribute).
Primary rows: pairs whose counterfactual prompt the model answers with D's answer (cf_ok); all pairs beside.
Readings (fixed in note 14):
  the bridge lives here    full_cf moves >= 20% to D's answer, lensrand_cf < 10%, and full - lensrand (paired, 95%
                           bootstrap over bridges) above 0
  the lens part carries it at such a cell: lens >= 2/3 of full and remfix <= 1/3 of full (lensrand < 10): "through";
                           rem >= 2/3 of full: "around"; else "mixed" (each a share moved to D's answer)
Writes results/nn_swap/nn_cf_read/NAME.json, with the cells that meet the first reading (stage 2's targets).

python scripts/nn_cf_read.py NAME RUN [RUN ...] [--all-pairs]
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "nn_swap"


def boot(by: dict[str, list[float]]) -> list[float]:
    rng, keys, out = random.Random(0), sorted(by), []
    for _ in range(1000):
        xs = [x for k in (rng.choice(keys) for _ in keys) for x in by[k]]
        out.append(sum(xs) / len(xs))
    out.sort()
    return [round(out[25], 1), round(out[974], 1)]


def main(name: str, runs: list[str], all_pairs: bool) -> None:
    cell = collections.defaultdict(lambda: collections.defaultdict(dict))  # (site, word, band) -> key -> cond -> cls
    bridge = {}
    for ri, run in enumerate(runs):
        site = json.loads((RES / run / "manifest.json").read_text())["site"]
        for line in (RES / run / "rows.jsonl").read_text().splitlines():
            r = json.loads(line)
            if not all_pairs and r.get("cf_ok") is False:
                continue
            key = f"{ri}:{r['id']}"
            cell[(site, r["family"], r["band"])][key][r["condition"]] = r["cls"]
            bridge[key] = f"{r['rel']}:{r['x']}"
    out: dict = {"runs": runs, "pairs": "all" if all_pairs else "cf_ok", "cells": {}, "hits": []}
    for (site, word, band), by in sorted(cell.items(), key=lambda kv: (kv[0][0], kv[0][1], int(kv[0][2][1:].split("-")[0]))):
        conds = sorted({c for d in by.values() for c in d})
        share = {c: round(100 * sum(d.get(c) == "donor" for d in by.values() if c in d) / max(1, sum(c in d for d in by.values())), 1) for c in conds}
        kept = {c: round(100 * sum(d.get(c) == "kept" for d in by.values() if c in d) / max(1, sum(c in d for d in by.values())), 1) for c in conds}
        third = {c: round(100 * sum(d.get(c) == "third" for d in by.values() if c in d) / max(1, sum(c in d for d in by.values())), 1) for c in conds}
        rec: dict = {"n": len(by), "donor": share, "kept": kept, "third": third}
        if "full_cf" in conds and "lensrand_cf" in conds:
            b = collections.defaultdict(list)
            for k, d in by.items():
                if "full_cf" in d and "lensrand_cf" in d:
                    b[bridge[k]].append(100.0 * ((d["full_cf"] == "donor") - (d["lensrand_cf"] == "donor")))
            ci = boot(b)
            rec["full_minus_rand_ci"] = ci
            rec["bridge_lives_here"] = share["full_cf"] >= 20 and share["lensrand_cf"] < 10 and ci[0] > 0
            if rec["bridge_lives_here"]:
                out["hits"].append({"site": site, "word": word, "band": band})
        if all(f"{k}_cf" in share for k in ("full", "lens", "rem", "remfix", "lensrand")):
            t = {k: share[f"{k}_cf"] - share.get("none", 0.0) for k in ("full", "lens", "rem", "remfix", "lensrand")}
            full = t["full"]
            rec["decomposition"] = {**{k: round(v, 1) for k, v in t.items()},
                                    "verdict": "not read" if full < 20 else "through" if t["lens"] >= 2 / 3 * full and t["remfix"] <= 1 / 3 * full and t["lensrand"] < 10
                                    else "around" if t["rem"] >= 2 / 3 * full else "mixed"}  # fmt: skip
        out["cells"][f"{site}/{word}/{band}"] = rec
        line = f"{site:5s} {word} {band:7s} n {len(by):4d}  " + "  ".join(f"{c} {share[c]:5.1f}" for c in conds if c != "none")
        if "bridge_lives_here" in rec:
            line += f"  full-rand CI {rec['full_minus_rand_ci']}  {'<-- LIVES HERE' if rec['bridge_lives_here'] else ''}"
        if "decomposition" in rec:
            line += f"  decomposition {rec['decomposition']}"
        print(line)
    d = RES / "nn_cf_read"
    d.mkdir(exist_ok=True)
    (d / f"{name}.json").write_text(json.dumps(out, indent=1) + "\n")
    print("hits", json.dumps(out["hits"]))


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if x != "--all-pairs"]
    main(args[0], args[1:], "--all-pairs" in sys.argv)
