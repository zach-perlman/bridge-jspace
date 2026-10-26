"""45a, descriptive, after the data (Dan 26 Oct ~21:20 and ~21:25): one table per model beside the rule.

1. Where the position answers lost in V1-V3 go: the lookup's answer route (identity / position / value / original /
   other) per variant V0-V4, on the first-locker moves (the rule's scenes: the same base scenes in every variant),
   with the whole change and with the pointer part only (keep_alf).
2. beta, the code's shift at O's bridge word against V0 (x6_routes.prepend_betas, in units of mu_j+1 - mu_j), per
   variant over all moves, mean with a cluster-bootstrap CI over bridge items: the rule's third read.
3. The unedited reads per variant (competence.jsonl, every generated case, the gate's input): the share each reader
   reads right on O and on S.

uv run python scripts/x45a_descriptive.py --runs qwen35_9b_x6_routes_x45a x6_routes_x45a_27b muse30b_x6_routes_x45a
Writes results/x6_routes/x45a-descriptive-<time>/{table.md, table.json}. CPU, read-only on the runs.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x0_necessity as X
from scripts import x6_routes as R

ROUTES = ("identity", "position", "value", "original", "other")
ARMS = {"whole": "the whole change", "keep_alf": "the pointer part only"}


def route_table(rows: list[dict]) -> dict:
    """Per arm and variant, the lookup's route shares on the first-locker moves, over the base scenes present in every
    variant (as the rule)."""
    lk = [r for r in rows if r["reader"] == X.LOOKUP and r.get("variant") and r["arm"] in ARMS]
    variants = [v for v in R.PREPEND if any(r["variant"] == v for r in lk)]
    bases = set.intersection(*({r["base_scene"] for r in lk if r["variant"] == v} for v in variants))
    first = {r["base_scene"] for r in lk if 0 in r["move"]} & bases
    out: dict = {"n": len(first), "variants": variants, "share": {}}
    for a in ARMS:
        for v in variants:
            got = Counter(r["route"] for r in lk if r["arm"] == a and r["variant"] == v and r["base_scene"] in first)
            out["share"][f"{a}|{v}"] = {k: got[k] / len(first) for k in ROUTES} if first else {}
    return out


def beta_table(betas: list[dict], n_boot: int = X.N_BOOT) -> dict:
    """Per variant (V1-V4), the mean beta over all moves with a cluster-bootstrap CI over bridge items."""
    out = {}
    for v in sorted({b["variant"] for b in betas}):
        mine = [b for b in betas if b["variant"] == v]
        rr = X.resampled_rates({"beta": [b["beta"] for b in mine]}, [b["entity"] for b in mine], n_boot)
        out[v] = {"n": len(mine), "beta": [float(np.mean([b["beta"] for b in mine])), *X.interval(rr["beta"])]}
    return out


def accuracy_table(comp: list[dict], variant_of: dict[str, str]) -> dict:
    """Per variant, reader and prompt (org = O, alt = S), the share of generated cases read right, unedited."""
    out: dict = {}
    for r in comp:
        v = variant_of.get(r["scene"])
        if v is None:
            continue
        cell = out.setdefault(v, {}).setdefault(f"{r['reader']}|{r['variant']}", [0, 0])
        cell[0] += int(r["read_right"])
        cell[1] += 1
    return {v: {k: {"right": a, "n": n, "share": a / n} for k, (a, n) in cells.items()} for v, cells in out.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True, help="45a routes runs (results/x6_routes/<run>)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    out = R.RESULTS / f"x45a-descriptive-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob, lines = {}, ["# 45a, descriptive, after the data (Dan 26 Oct ~21:20 / ~21:25)", "",
                       "Not part of the rule (jobs/c3/batch45.yaml). Lookup reads at the layer fixed in advance. UNVERIFIED.", ""]  # fmt: skip
    for run in a.runs:
        src = R.RESULTS / run
        m = json.loads((src / "manifest.json").read_text())
        cases = X.read_jsonl(src / "cases.jsonl")
        routes = route_table(X.read_jsonl(src / "outcomes.jsonl"))
        betas = beta_table(X.read_jsonl(src / "beta.jsonl"), a.n_boot)
        acc = accuracy_table(X.read_jsonl(src / "competence.jsonl"), {c["scene"]: c["variant"] for c in cases})
        blob[run] = {
            "model": m["model"]["target"],
            "layer": m["layer"],
            "routes": routes,
            "beta": betas,
            "accuracy": acc,
        }
        lines += [f"## {m['model']['target']} (L{m['layer']}; {run})", "",
                  f"1. The lookup's answer route on the first-locker moves (n = {routes['n']} base scenes, the same in "
                  "every variant): identity / position / value / original / other.", "",
                  "| variant | " + " | ".join(ARMS.values()) + " |", "|---|---|---|"]  # fmt: skip
        for v in routes["variants"]:
            cells = [" / ".join(f"{routes['share'][f'{arm}|{v}'][k]:.2f}" for k in ROUTES) for arm in ARMS]
            lines.append(f"| {v} | " + " | ".join(cells) + " |")
        lines += ["", "2. beta, the code's shift vs V0 at O's bridge word (units of mu_j+1 - mu_j; all moves):", "",
                  "| variant | n | beta [CI] |", "|---|---|---|"]  # fmt: skip
        lines += [
            f"| {v} | {b['n']} | {b['beta'][0]:.2f} [{b['beta'][1]:.2f}, {b['beta'][2]:.2f}] |"
            for v, b in betas.items()
        ]
        lines += ["", "3. Unedited reads per variant (every generated case): share read right, lookup O / S, recall O / S.",
                  "", "| variant | lookup O | lookup S | recall O | recall S |", "|---|---|---|---|---|"]  # fmt: skip
        for v in R.PREPEND:
            if v in acc:
                c = acc[v]
                lines.append(f"| {v} | " + " | ".join(f"{c[k]['share']:.2f} ({c[k]['right']}/{c[k]['n']})"
                                                     for k in (f"{X.LOOKUP}|org", f"{X.LOOKUP}|alt", f"{X.RECALL}|org",
                                                               f"{X.RECALL}|alt")) + " |")  # fmt: skip
        lines.append("")
    (out / "table.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
