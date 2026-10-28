"""nn_contrast (Zach, 2026-10-28, prereg amendment 58 note 9, item 1): the composition contrast, scored (CPU).

From an ablate_v2 run with --kinds clean step1 step2 on RM (never named), MM and PM: per word and condition, the points
lost on the whole question, hop 1 alone and hop 2 alone, over the items right unedited on all three (paired), and the
contrast loss(whole) - loss(hop 2) with a 95% bootstrap over bridges. RM is also split by the clue-only questions
(either wording right / both wrong / no named clue) and without films. Note 9's reading: "composition needs the
workspace beyond the final recall" if RM's contrast is >= 10 under paper10 with the controls' < 10. Hop 1's loss uses the
first-token read among the relation's bridges, which share first tokens (people 25/63): it is reported, not read.
Writes results/ablate_v2/nn_contrast/RUN.json.

python scripts/nn_contrast.py RUN PREFIX   (PREFIX "" for the 27B, "qwen35_9b_", "nem35l_")
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SET = "jsuite_v3_test_chat"


def boot(vals: dict[str, list[float]], reps: int = 1000) -> list[float]:
    rng = random.Random(0)
    cl = sorted(vals)
    out = []
    for _ in range(reps):
        xs = [x for c in (rng.choice(cl) for _ in cl) for x in vals[c]]
        out.append(sum(xs) / len(xs))
    out.sort()
    return [round(out[int(0.025 * reps)], 1), round(out[int(0.975 * reps) - 1], 1)]


def main(run: str, p: str) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (ROOT / "data/tasks_v2" / SET / "items.jsonl").open()}
    rows = [json.loads(line) for line in (ROOT / "results/ablate_v2" / run / "rows.jsonl").open()]
    pitems = {}  # probe id -> (bridge, desc_index); bridge names may contain ":" (film titles)
    for sname in ("jsuite_v3probes_test_chat", "jsuite_v3probesB_test_chat"):
        for line in (ROOT / "data/tasks_v2" / sname / "items.jsonl").open():
            it = json.loads(line)
            pitems[it["id"]] = (it["bridge"], it["desc_index"])
    clue = {}  # (bridge, desc_index) -> right on either wording
    for name in (f"{p}jsuite_v3probes_cv_v1", f"{p}jsuite_v3probesB_cv_v1"):
        f = ROOT / "results/competence_variants" / name / "rows.jsonl"
        if f.exists():
            for line in f.open():
                r = json.loads(line)
                key = pitems[r["id"]]
                clue[key] = clue.get(key, False) or bool(r["correct_cand2"])
    res = collections.defaultdict(dict)  # (id, kind) -> {cond: correct}
    for r in rows:
        res[(r["id"], r["kind"])][r["condition"]] = r["correct"]
    conds = sorted({r["condition"] for r in rows} - {"none"})
    out: dict = {"run": run, "cells": {}}

    def group(it: dict) -> str:
        key = (it["bridge"], it.get("desc_index"))
        return "no_clue" if key not in clue else ("clue_right" if clue[key] else "clue_wrong")

    for word in ("RM", "MM", "PM"):
        ids = sorted({i for (i, k) in res if items[i]["word"] == word})
        paired = [i for i in ids if all(res.get((i, k), {}).get("none") for k in ("clean", "step1", "step2"))]
        subsets = {"all": paired, "no_films": [i for i in paired if items[i]["relation"] != "films"]}
        if word == "RM":
            for g in ("clue_right", "clue_wrong", "no_clue"):
                subsets[g] = [i for i in paired if group(items[i]) == g]
        for sname, sub in subsets.items():
            if not sub:
                continue
            for c in conds:
                loss = {k: 100 * sum(1 - res[(i, k)].get(c, True) for i in sub) / len(sub) for k in ("clean", "step1", "step2")}
                vals = collections.defaultdict(list)
                for i in sub:
                    vals[f"{items[i]['relation']}:{items[i]['bridge']}"].append(100 * ((1 - res[(i, "clean")][c]) - (1 - res[(i, "step2")][c])))
                out["cells"][f"{word}/{sname}/{c}"] = {"n": len(sub), "lost_whole": round(loss["clean"], 1), "lost_hop1": round(loss["step1"], 1),
                                                       "lost_hop2": round(loss["step2"], 1), "whole_minus_hop2": round(loss["clean"] - loss["step2"], 1),
                                                       "ci": boot(vals)}  # fmt: skip
    rm = {c: out["cells"].get(f"RM/all/{c}") for c in conds}
    if rm.get("paper10"):
        ctrl = [rm[c]["whole_minus_hop2"] for c in conds if c != "paper10" and rm.get(c)]
        out["reading"] = {"paper10_contrast": rm["paper10"]["whole_minus_hop2"], "ci": rm["paper10"]["ci"], "controls": ctrl,
                          "composition_needs_workspace": rm["paper10"]["whole_minus_hop2"] >= 10 and all(x < 10 for x in ctrl)}  # fmt: skip
    d = ROOT / "results/ablate_v2/nn_contrast"
    d.mkdir(exist_ok=True)
    (d / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["cells"].items():
        print(f"{k:32s} n {v['n']:4d}  lost whole {v['lost_whole']:5.1f}  hop1 {v['lost_hop1']:5.1f}  hop2 {v['lost_hop2']:5.1f}  whole-hop2 {v['whole_minus_hop2']:+5.1f} {v['ci']}")
    print("reading:", out.get("reading"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
