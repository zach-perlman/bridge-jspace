"""c2_route_crosstab: the lookup's route under "whole" against its route under an arm, C2 scenes (POST HOC; Dan 30 Oct; CPU, descriptive, no rule).

Reads results/x6_routes/<run>/outcomes.jsonl of each model's main routes run (the runs behind the depth README's routes
figure: fig05), C2 rows of the lookup reader (PP) only, and cross-tabulates per scene the route (identity / position / value /
original / other, x6_routes.classify) under "whole" with the route under: no_alf (without the pointer directions), no_jpp
(without J++), and their size-matched random arms (no_alf_rand, no_jpp_rand). Counts only; scene ids of every identity ->
position cell are listed. Two paired contrasts per model, 95% cluster bootstrap over the bridge entity
(x0_necessity.resampled_rates, seed 0; same draws for both arms): (a) the share of whole = position scenes that leave position under
no_alf, minus the same under no_alf_rand; (b) the share of whole = identity scenes that go to position under no_jpp, minus the same under
no_jpp_rand. Writes results/c2_route_crosstab/<UTC>/ (manifest.json first, tables.json, tables.md).
"""

from __future__ import annotations

import collections
import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import x0_necessity as X  # noqa: E402

RUNS = {"qwen3.5-9b": "qwen35_9b_x6_routes", "qwen3.6-27b": "x6_routes_27b", "muse-glimmer-30b": "muse30b_x6_routes",
        "nemotron-3.5-lightning": "nem35l_x52_routes", "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_g75"}  # fmt: skip
ROUTES = ("identity", "position", "value", "original", "other")
ARMS = (("no_alf", "without the pointer directions"), ("no_alf_rand", "size-matched random part (control of the pointer arm)"),
        ("no_jpp", "without J++"), ("no_jpp_rand", "size-matched random part (control of the J++ arm)"))  # fmt: skip
READER, COND = "PP", "C2"


def contrast(route, entity, scenes, start, goal, arm, rand, n_boot=X.N_BOOT):
    """Among the scenes whose route under "whole" is `start`: the share that goes to `goal` (None: that leave `start`) under `arm`, minus
    the same under `rand`; paired cluster bootstrap over the bridge entity. Returns counts, shares and [point, lo, hi]."""
    base = [s for s in scenes if route[(s, "whole")] == start]
    hit = lambda s, a: int(route[(s, a)] == goal if goal else route[(s, a)] != start)  # noqa: E731
    ents = [entity[s] for s in scenes]
    o = {k: [hit(s, a) if s in base else 0 for s in scenes] for k, a in (("arm", arm), ("rand", rand))}
    o["den"] = [int(s in base) for s in scenes]
    rr = X.resampled_rates(o, ents, n_boot, X.BOOT_SEED)
    with np.errstate(divide="ignore", invalid="ignore"):
        d = rr["arm"] / rr["den"] - rr["rand"] / rr["den"]
    n = len(base)
    sh = {k: sum(o[k]) / n if n else None for k in ("arm", "rand")}
    return {"n_whole_" + start: n, "arm": arm, "count_arm": sum(o["arm"]), "count_rand": sum(o["rand"]), "share_arm": sh["arm"], "share_rand": sh["rand"],
            "difference": [sh["arm"] - sh["rand"], *X.interval(d)] if n else None}  # fmt: skip


def main() -> None:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "c2_route_crosstab" / stamp
    out.mkdir(parents=True)
    (out / "manifest.json").write_text(json.dumps({"exp": "c2_route_crosstab", "runs": RUNS, "reader": READER, "condition": COND,
                                                   "cpu": True, "post_hoc": True, "rule": None, "written_utc": stamp}, indent=2) + "\n")  # fmt: skip
    res: dict = {}
    for model, run in RUNS.items():
        route: dict[tuple[str, str], str] = {}
        entity: dict[str, str] = {}
        for line in (REPO / "results" / "x6_routes" / run / "outcomes.jsonl").open():
            r = json.loads(line)
            if r["condition"] == COND and r["reader"] == READER:
                route[(r["scene"], r["arm"])] = r["route"]
                entity[r["scene"]] = r["entity"]
        scenes = sorted({s for s, a in route if a == "whole"})
        res[model] = {
            "run": run,
            "n": len(scenes),
            "whole": dict(collections.Counter(route[(s, "whole")] for s in scenes)),
            "arms": {},
        }
        for arm, text in ARMS:
            tab = collections.Counter((route[(s, "whole")], route[(s, arm)]) for s in scenes)
            res[model]["arms"][arm] = {"text": text, "marginal": dict(collections.Counter(route[(s, arm)] for s in scenes)),
                                       "cells": {f"{a}->{b}": n for (a, b), n in sorted(tab.items())},
                                       "identity_to_position": sorted(s for s in scenes if (route[(s, "whole")], route[(s, arm)]) == ("identity", "position"))}  # fmt: skip
        res[model]["contrasts"] = {
            "a_leave_position_no_alf_minus_rand": contrast(
                route, entity, scenes, "position", None, "no_alf", "no_alf_rand"
            ),
            "b_identity_to_position_no_jpp_minus_rand": contrast(
                route, entity, scenes, "identity", "position", "no_jpp", "no_jpp_rand"
            ),
        }
    (out / "tables.json").write_text(json.dumps(res, indent=1) + "\n")
    md = ["# C2 lookup: route under whole -> route under the arm (n scenes per model; rows whole, columns arm)\n"]
    for model, d in res.items():
        md.append(
            f"## {model} ({d['run']}), n = {d['n']}; whole: "
            + ", ".join(f"{k} {d['whole'].get(k, 0)}" for k in ROUTES)
            + "\n"
        )
        for arm, a in d["arms"].items():
            md.append(f"**{arm}** ({a['text']}); identity -> position: {len(a['identity_to_position'])}\n")
            md.append("| whole \\ arm | " + " | ".join(ROUTES) + " | total |\n|---|" + "---|" * (len(ROUTES) + 1))
            for w in ROUTES:
                cnt = [a["cells"].get(f"{w}->{b}", 0) for b in ROUTES]
                if sum(cnt):
                    md.append(f"| {w} | " + " | ".join(map(str, cnt)) + f" | {sum(cnt)} |")
            md.append("")
            if a["identity_to_position"]:
                md.append("identity -> position scenes: " + ", ".join(a["identity_to_position"]) + "\n")
    for model, d in res.items():
        for k, c in d["contrasts"].items():
            md.append(f"{model} {k}: " + json.dumps(c))
    (out / "tables.md").write_text("\n".join(md) + "\n")
    print(out)


if __name__ == "__main__":
    main()
