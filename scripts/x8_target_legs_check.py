"""x8_target_legs_check: the share of recalls the address swap changes, on all scenes and on scenes where a change is possible (POST HOC; Dan 30 Oct;
CPU, saved x8_write rows, descriptive; the pre-set rule below).

x8_write (batch 44) writes h + s (mu_k - mu_j) at the bridge word of the routes test's C2 scenes (j = the bridge item's locker slot, both k != j) and
reads the recall ("How many legs does <p>'s pick have?"). When the item at the target slot k has as many legs as the item at the original slot j, a
followed pointer cannot show as a changed recall ("collision"). Per model, kind (write / random) and s in the stored set: the share of recalls
changed on all rows and on the rows with legs[k] != legs[j] (95% cluster-bootstrap intervals over the bridge entity, x0_necessity.resampled_rates,
seed 0), and the collision rate (rows with legs[k] == legs[j] / rows). Random rows are stored at s = 1 and 4 only.

Pre-set rule (Dan 30 Oct): if the non-colliding share differs from the README's reported share (the write at s = 2, 'the address swap at s = 2:
recalls that change', data/figures/depth/data.csv, cards) by more than 0.05 on any model, the README's "changes ... of recalls" line reports both
numbers; otherwise a caveat line only.

uv run python scripts/x8_target_legs_check.py        # writes results/x8_target_legs_check/<UTC>/ (manifest first)
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import tasks_v2 as T  # noqa: E402
from scripts import x0_necessity as X  # noqa: E402
from scripts import x8_write as W  # noqa: E402

RUNS = {"qwen3.5-9b": "qwen35_9b_x8_write", "qwen3.6-27b": "x8_write_27b", "muse-glimmer-30b": "muse30b_x8_write",
        "nemotron-3.5-lightning": "nem35l_x52_write", "qwen3.5-122b-a10b": "qwen35_122b_x8_write_g75"}  # fmt: skip
BAR = 0.05


def ci(values: list[int], ents: list[str]) -> list[float]:
    if not values:
        return [float("nan")] * 3
    boot = X.resampled_rates({"x": values}, ents, X.N_BOOT, X.BOOT_SEED)["x"]
    return [round(float(np.mean(values)), 4), *(round(b, 4) for b in X.interval(boot))]


def reported() -> dict[str, float]:
    out = {}
    for r in csv.reader((REPO / "data/figures/depth/data.csv").open()):
        if r[0] == "cards" and r[2] == "the address swap at s = 2: recalls that change":
            out[r[1]] = float(r[3])
    return out


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "x8_target_legs_check" / stamp
    out.mkdir(parents=True, exist_ok=False)
    legs = T.DOMAINS["animals"].values
    (out / "manifest.json").write_text(json.dumps({"exp": "x8_target_legs_check", "post_hoc": True, "cpu": True, "runs": RUNS, "bar": BAR,
                                                   "rule": __doc__.split("Pre-set rule")[1].strip().split("\n\n")[0], "written_utc": stamp}, indent=2) + "\n")  # fmt: skip
    rep = reported()
    res: dict = {}
    for model, run in RUNS.items():
        cases = {
            c["scene"]: c
            for c in X.read_jsonl(REPO / "results/x6_routes" / W.ROUTES_OF[model] / "cases.jsonl")
            if c["condition"] == "C2"
        }
        rows = [
            r
            for r in X.read_jsonl(REPO / "results/x8_write" / run / "outcomes.jsonl")
            if r["reader"] == X.RECALL and r["kind"] in ("write", "random")
        ]
        cells: dict = {}
        examples = []
        for r in rows:
            slots = W.slots_of(cases[r["scene"]]["context"])
            same = legs[slots[r["k"]][0]] == legs[slots[r["j"]][0]]
            c = cells.setdefault(
                f"{r['kind']}|{r['s']:g}", {"all": [], "clean": [], "ents_all": [], "ents_clean": [], "collisions": 0}
            )
            c["all"].append(int(r["changed"]))
            c["ents_all"].append(r["entity"])
            c["collisions"] += same
            if not same:
                c["clean"].append(int(r["changed"]))
                c["ents_clean"].append(r["entity"])
            if r["scene"] == "C2-0047" and r["kind"] == "write" and r["s"] == 2:
                examples.append({"scene": r["scene"], "j_item": slots[r["j"]][0], "k_item": slots[r["k"]][0], "legs_j": legs[slots[r["j"]][0]], "legs_k": legs[slots[r["k"]][0]], "changed": int(r["changed"]), "collision": bool(same)})  # fmt: skip
        res[model] = {
            "run": run,
            "scenes": len(cases),
            "reported_s2_write": rep.get(model),
            "examples_C2_0047": examples,
            "cells": {},
        }
        for key, c in cells.items():
            n, nc = len(c["all"]), len(c["clean"])
            res[model]["cells"][key] = {"rows": n, "collisions": c["collisions"], "collision_rate": round(c["collisions"] / n, 4),
                                        "share_all": ci(c["all"], c["ents_all"]), "rows_clean": nc, "share_non_colliding": ci(c["clean"], c["ents_clean"])}  # fmt: skip
        s2 = res[model]["cells"]["write|2"]
        res[model]["diff_non_colliding_vs_reported"] = round(s2["share_non_colliding"][0] - rep[model], 4)
        res[model]["share_all_equals_reported"] = abs(s2["share_all"][0] - rep[model]) < 5e-5
    worst = max(abs(m["diff_non_colliding_vs_reported"]) for m in res.values())
    res["_rule"] = {
        "max_abs_difference": round(worst, 4),
        "bar": BAR,
        "readme_edit": "report both numbers" if worst > BAR else "caveat line only",
    }
    (out / "tables.json").write_text(json.dumps(res, indent=1) + "\n")
    lines = ["# The address swap: share of recalls changed, all rows vs rows where the target item's legs differ from the original item's (post hoc)\n",
             f"Rule: max |non-colliding - reported| = {res['_rule']['max_abs_difference']} (bar {BAR}): {res['_rule']['readme_edit']}\n"]  # fmt: skip
    for model, m in res.items():
        if model == "_rule":
            continue
        lines.append(
            f"## {model} ({m['run']}); README reports {m['reported_s2_write']:.4f} (write, s = 2); all-rows share equals it: {m['share_all_equals_reported']}\n"
        )
        lines.append(
            "| kind, s | rows | collision rate | share changed, all rows | rows with legs[k] != legs[j] | share changed, non-colliding |\n|---|---|---|---|---|---|"
        )
        for key, c in m["cells"].items():
            f = lambda v: f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]"  # noqa: E731
            lines.append(
                f"| {key} | {c['rows']} | {c['collision_rate']:.3f} ({c['collisions']}) | {f(c['share_all'])} | {c['rows_clean']} | {f(c['share_non_colliding'])} |"
            )
        lines.append(f"\nC2-0047 (write, s = 2): {m['examples_C2_0047']}\n")
    (out / "tables.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
