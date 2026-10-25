"""profile_score (Zach, 2026-10-25, amendment 42): a model's depth profile from one multi-band dev run (scripts/
h200_profile_1025.sh): per band and condition, points lost (items right unedited) on memory finals (PM, MM), stated
true finals (PK, MK) and passage finals (PP, MP); the contrasts M - K and M - P; 95% bootstrap over bridges (seed 0).
Prints a table and writes results/ablate_v2/profile/RUN.json.
python scripts/profile_score.py RUN N_LAYERS --set jsuite_v2_dev_chat"""
from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"


def main(run: str, n_layers: int, set_name: str) -> None:
    items = {json.loads(x)["id"]: json.loads(x) for x in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(x) for x in (RES / run / "rows.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    cells = collections.defaultdict(list)  # (band, cond, final) -> [(bridge, correct)]
    for r in rows:
        if r["condition"] == "none" or (r["family"], r["id"]) not in ok:
            continue
        it = items[r["id"]]
        cells[(r["band"], r["condition"], it["final"])].append((f"{it['relation']}:{it['bridge']}", r["correct"]))
    bands = sorted({b for b, _, _ in cells}, key=lambda b: int(b.lstrip("L").split("-")[0]))
    conds = sorted({c for _, c, _ in cells})
    rng, out = random.Random(0), {"run": run, "set": set_name, "n_layers": n_layers, "bands": {}}
    for b in bands:
        lo, hi = (int(x) for x in b.lstrip("L").split("-"))
        out["bands"][b] = {"depth": [round(lo / n_layers, 3), round(hi / n_layers, 3)]}
        for c in conds:
            sel = {f: cells[(b, c, f)] for f in "PKM"}
            if not all(sel.values()):
                continue
            loss = {f: 100 * (1 - sum(x for _, x in v) / len(v)) for f, v in sel.items()}
            clusters = sorted({k for v in sel.values() for k, _ in v})
            bs = collections.defaultdict(list)
            for _ in range(500):
                pick = collections.Counter(rng.choice(clusters) for _ in clusters)
                lb = {}
                for f, v in sel.items():
                    tot = [(x, pick[k]) for k, x in v if pick[k]]
                    n = sum(m for _, m in tot)
                    lb[f] = 100 * (1 - sum(x * m for x, m in tot) / n) if n else None
                for a, z in (("M", "K"), ("M", "P")):
                    if lb[a] is not None and lb[z] is not None:
                        bs[f"{a}-{z}"].append(lb[a] - lb[z])
            ci = {k: [round(sorted(v)[int(0.025 * len(v))]), round(sorted(v)[int(0.975 * len(v)) - 1])] for k, v in bs.items()}
            out["bands"][b][c] = {"loss": {f: round(v, 1) for f, v in loss.items()}, "n": {f: len(v) for f, v in sel.items()},
                                  "M-K": round(loss["M"] - loss["K"], 1), "M-K_ci": ci.get("M-K"), "M-P": round(loss["M"] - loss["P"], 1)}  # fmt: skip
    print(f"{'band':8s} {'depth':>9s} " + "  ".join(f"{c:>26s}" for c in conds))
    for b in bands:
        d = out["bands"][b]
        cols = []
        for c in conds:
            x = d.get(c)
            cols.append(f"M-K {x['M-K']:+5.0f} {str(x['M-K_ci']):>10s} K{x['loss']['K']:3.0f}" if x else " " * 26)
        print(f"{b:8s} {100 * d['depth'][0]:3.0f}-{100 * d['depth'][1]:3.0f}%  " + "  ".join(cols))
    (RES / "profile").mkdir(exist_ok=True)
    (RES / "profile" / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("n_layers", type=int)
    ap.add_argument("--set", default="jsuite_v2_dev_chat")
    a = ap.parse_args()
    main(a.run, a.n_layers, a.set)
