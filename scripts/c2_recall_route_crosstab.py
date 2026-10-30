"""c2_recall_route_crosstab: the recall's answer by route under "whole" against under an arm, C2 scenes with no route collision (POST HOC;
Dan 30 Oct; CPU, saved x6_routes arms, descriptive, no rule).

The recall (PM) answers with a digit (legs). Its route: identity = the changed item's legs (the recall's changed answer, tok_b), position =
the legs of the item that sits, in the original prompt, at the slot the changed pick occupies in the changed prompt (scripts/c2_route_collision.py),
original = the original answer (tok_A), other. Precedence identity > position > original > other; the scenes where the position item's legs equal
the original answer are counted (ambiguous between position and original; read as position). Only the non-colliding scenes of
scripts/c2_route_collision.py (position legs != changed legs) enter. The digit's token id is base + d, base fixed per model (asserted).

Arms: no_jpp (without J++), no_alf (without the pointer directions), keep_alf (only the pointer directions), each beside its size-matched random
arm (*_rand). Per model one run holds all of them (keep_alf needs the keep-only run for the 9B, 27B and 122B). Writes
results/c2_recall_route_crosstab/<UTC>/ (manifest.json first, tables.json, tables.md).
"""

from __future__ import annotations

import collections
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import c2_route_collision as CR  # noqa: E402

RUNS = {"qwen3.5-9b": "qwen35_9b_x6_routes_keeponly", "qwen3.6-27b": "x6_routes_keeponly_27b", "muse-glimmer-30b": "muse30b_x6_routes",
        "nemotron-3.5-lightning": "nem35l_x52_routes", "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_keeponly_g75"}  # fmt: skip
ROUTES = ("identity", "position", "original", "other")
ARMS = (("no_jpp", "no_jpp_rand"), ("no_alf", "no_alf_rand"), ("keep_alf", "keep_alf_rand"))
READER, COND = "PM", "C2"


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "c2_recall_route_crosstab" / stamp
    out.mkdir(parents=True)
    (out / "manifest.json").write_text(json.dumps({"exp": "c2_recall_route_crosstab", "post_hoc": True, "runs": RUNS, "reader": READER, "condition": COND,
                                                   "scenes": "non-colliding only (scripts/c2_route_collision.py)", "cpu": True, "rule": None,
                                                   "written_utc": stamp}, indent=2) + "\n")  # fmt: skip
    coll = CR.routes_collisions()
    res: dict = {}
    for model, run in RUNS.items():
        clean = {r["scene"]: r for r in coll[model]["non_colliding_items"]}
        cases = {}
        for line in (REPO / "results" / "x6_routes" / run / "cases.jsonl").open():
            c = json.loads(line)
            if c["condition"] == COND:
                cases[c["scene"]] = c
        rows = collections.defaultdict(dict)
        for line in (REPO / "results" / "x6_routes" / run / "outcomes.jsonl").open():
            r = json.loads(line)
            if r["condition"] == COND and r["reader"] == READER and r["scene"] in clean:
                rows[r["scene"]][r["arm"]] = r["top"]
        bases = {cases[s]["readers"]["PM"]["tok_A"] - int(cases[s]["readers"]["PM"]["answer"]) for s in rows}
        assert len(bases) == 1, bases
        assert bases == {
            cases[s]["readers"]["PM"]["tok_b"] - int(cases[s]["readers"]["PM"]["cf_answer"]) for s in rows
        }, bases
        base = bases.pop()
        route: dict[tuple[str, str], str] = {}
        ambiguous = []
        for s, arms in rows.items():
            rd, k = cases[s]["readers"]["PM"], clean[s]
            ident, pos, orig = base + int(rd["cf_answer"]), base + k["position_entity_legs"], rd["tok_A"]
            assert ident != pos
            if pos == orig:
                ambiguous.append(s)
            for arm, top in arms.items():
                route[(s, arm)] = (
                    "identity" if top == ident else "position" if top == pos else "original" if top == orig else "other"
                )
        amb = set(ambiguous)
        res[model] = {"run": run, "n_collisions_excluded": coll[model]["collisions"], "digit_token_base": base,
                      "position_legs_equal_original_answer": len(ambiguous)}  # fmt: skip
        for name, scenes in (("non_colliding", sorted(rows)), ("all_three_distinct", sorted(set(rows) - amb))):
            res[model][name] = {
                "n": len(scenes),
                "whole": dict(collections.Counter(route[(s, "whole")] for s in scenes)),
                "arms": {},
            }
            for arm in [a for pair in ARMS for a in pair]:
                tab = collections.Counter((route[(s, "whole")], route[(s, arm)]) for s in scenes)
                res[model][name]["arms"][arm] = {"marginal": dict(collections.Counter(route[(s, arm)] for s in scenes)),
                                                 "cells": {f"{a}->{b}": n for (a, b), n in sorted(tab.items())}}  # fmt: skip
        res[model]["scenes"] = {s: {a: route[(s, a)] for a in rows[s]} for s in sorted(rows)}
    (out / "tables.json").write_text(json.dumps(res, indent=1) + "\n")
    md = [
        "# C2, recall, non-colliding scenes: route under whole -> under the arm (rows whole, columns arm); post hoc\n"
    ]
    for model, d in res.items():
        for name, text in (("non_colliding", "non-colliding scenes (position legs = original answer: read as position)"),
                           ("all_three_distinct", "scenes where the original, changed and position legs are all different")):  # fmt: skip
            t = d[name]
            md.append(f"## {model} ({d['run']}), {text}: n = {t['n']} (of {len(d['scenes'])} non-colliding; {d['n_collisions_excluded']} colliding excluded;"
                      f" position legs = original answer in {d['position_legs_equal_original_answer']}); whole: "
                      + ", ".join(f"{k} {t['whole'].get(k, 0)}" for k in ROUTES) + "\n")  # fmt: skip
            for arm, a in t["arms"].items():
                md.append(f"**{arm}**; marginal: " + ", ".join(f"{k} {a['marginal'].get(k, 0)}" for k in ROUTES) + "\n")
                md.append("| whole \\ arm | " + " | ".join(ROUTES) + " |\n|---|" + "---|" * len(ROUTES))
                for w in ROUTES:
                    cnt = [a["cells"].get(f"{w}->{b}", 0) for b in ROUTES]
                    if sum(cnt):
                        md.append(f"| {w} | " + " | ".join(map(str, cnt)) + " |")
                md.append("")
    (out / "tables.md").write_text("\n".join(md) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
