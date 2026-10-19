"""J-space concentration per layer (with relative depth), per family, for suite_split parts runs.

python scripts/suite_split_by_layer.py RUN:N_LAYERS [RUN:N_LAYERS ...]
"""

import collections
import json
import sys
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parents[1] / "results" / "suite_split"


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def main(specs: list[str]) -> None:
    for spec in specs:
        run, n_layers = spec.split(":")
        nl = int(n_layers)
        outs, fve = rows(R / run / "outcomes.jsonl"), rows(R / run / "fve.jsonl")
        share = {(f["family"], f["name"], f["layer"]): f["share"] for f in fve if f.get("what") == "jspace"}
        cell: dict[tuple, dict[str, dict[str, float]]] = collections.defaultdict(dict)
        for o in outs:
            if o["source"] == "cf" and not o["null"] and o["part"] in ("jspace", "full"):
                cell[(o["family"], o["layer"])].setdefault(o["name"], {})[o["part"]] = o["frac"]
        print(f"== {run} (concentration by layer; depth = layer / {nl})")
        fams = list(dict.fromkeys(f for f, _ in cell))
        print("layer  depth " + " ".join(f"{f:>6}" for f in fams))
        for layer in sorted({la for _, la in cell}):
            out = []
            for f in fams:
                d = cell.get((f, layer))
                if not d:
                    out.append("     -")
                    continue
                j = np.array([v["jspace"] for v in d.values()])
                full = np.array([v["full"] for v in d.values()])
                s = np.array([share[(f, n, layer)] for n in d])
                out.append(f"{j.sum() / max((s * full).sum(), 1e-9):6.2f}")
            print(f"{layer:5d}  {layer / nl:4.2f} " + " ".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
