# python scripts/suite_split_by_layer.py RUN:N_LAYERS [...]
"""J-space concentration per layer (relative depth), per family, for suite_split parts runs."""

import collections
import json
import sys

import numpy as np

runs = sys.argv[1:]
R = "/workspace/bridge-jspace/results/suite_split"
for run, nl in (r.split(":") for r in runs):
    nl = int(nl)
    outs = [json.loads(l) for l in open(f"{R}/{run}/outcomes.jsonl")]
    fve = [json.loads(l) for l in open(f"{R}/{run}/fve.jsonl")]
    share = {(f["family"], f["name"], f["layer"]): f["share"] for f in fve if f.get("what") == "jspace"}
    cell = collections.defaultdict(dict)
    for o in outs:
        if o["source"] == "cf" and not o["null"] and o["part"] in ("jspace", "full"):
            cell[(o["family"], o["layer"])].setdefault(o["name"], {})[o["part"]] = o["frac"]
    print(f"== {run} (concentration by layer; depth = layer / {nl})")
    fams = list(dict.fromkeys(f for f, _ in cell))
    layers = sorted({l for _, l in cell})
    print("layer  depth " + " ".join(f"{f:>6}" for f in fams))
    for l in layers:
        row = []
        for f in fams:
            d = cell.get((f, l))
            if not d:
                row.append("     -")
                continue
            J = np.array([v["jspace"] for v in d.values()])
            F = np.array([v["full"] for v in d.values()])
            S = np.array([share[(f, n, l)] for n in d])
            row.append(f"{J.sum() / max((S * F).sum(), 1e-9):6.2f}")
        print(f"{l:5d}  {l / nl:4.2f} " + " ".join(row))
