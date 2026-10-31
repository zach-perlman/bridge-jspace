"""nn_wrongbridge (Zach, 2026-10-28, prereg amendment 58 note 9 addendum): WorkspaceBench's wrong-bridge test on the
never-named items (CPU, stored runs only).

For each RM item where the model, asked hop 1 alone ("Which novelist wrote Arrow of God?", its v3 competence run's
generated name), names a different bridge B' of the same relation that our table knows, with an attribute different
from the true bridge B's: is its answer to the whole question (the greedy reply in its competence_variants run, note 1's
rule with v3's aliases) B''s attribute ("follows its own bridge"), B's ("true answer despite the wrong bridge"), or
other? Baseline: how often the model gives B''s attribute to the other RM items of the relation (its marginal rate).
Reading (fixed in the addendum): "composes through its own bridge" if the own-bridge share exceeds the baseline by
>= 20 points with a 95% bootstrap interval (over bridges) above 0. Generated names outside the table are counted.

python scripts/nn_wrongbridge.py PREFIX NAME
"""

from __future__ import annotations

import collections
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
from score_greedy import right as right0  # noqa: E402

SET = "jsuite_v3_test_chat"


def main(p: str, name: str) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (ROOT / "data/tasks_v2" / SET / "items.jsonl").open()}
    alias = collections.defaultdict(set)
    for it in items.values():
        alias[it["answer"]] |= set(it.get("answer_aliases") or [])
    right = lambda text, v: any(right0(text, x) for x in {v} | alias[v])  # noqa: E731
    table = json.loads((ROOT / "data/v3_bridges.json").read_text())
    names = collections.defaultdict(list)  # relation -> [(form, bridge)]
    attr = {}
    for r in table:
        attr[(r["relation"], r["bridge"])] = r["answer"]
        for form in {r["bridge"], *(r.get("bridge_alts") or [])}:
            names[r["relation"]].append((form.casefold(), r["bridge"]))
    gen, whole = {}, {}
    for line in (ROOT / "results/tasks_v2" / f"{p}{SET}_competence_cand2_v1" / "items.jsonl").open():
        r = json.loads(line)
        if r["part"] == "step1" and ":RM-" in r["id"]:
            gen[r["id"]] = (r.get("gen") or "").strip().split("\n")[0]
    for line in (ROOT / "results/competence_variants" / f"{p}jsuite_v3_cv_v1" / "rows.jsonl").open():
        r = json.loads(line)
        if r["id"] in items and items[r["id"]]["word"] == "RM":
            whole[r["id"]] = r["text"]

    def match(rel: str, text: str) -> str | None:
        t = text.casefold()
        hits = [(len(f), b) for f, b in names[rel] if re.search(r"(?<!\w)" + re.escape(f) + r"(?!\w)", t)]
        return max(hits)[1] if hits else None

    counts = collections.Counter()
    rows = []
    for i, g in gen.items():
        it = items[i]
        rel, b = it["relation"], it["bridge"]
        bp = match(rel, g)
        if bp == b:
            counts["hop1_right"] += 1
            continue
        if bp is None:
            counts["hop1_unknown_name"] += 1
            continue
        if attr[(rel, bp)] == attr[(rel, b)]:
            counts["hop1_wrong_same_attribute"] += 1
            continue
        if i not in whole:
            continue
        counts["hop1_wrong_known"] += 1
        a_own, a_true = attr[(rel, bp)], attr[(rel, b)]
        others = [j for j in whole if items[j]["relation"] == rel and j != i and items[j]["answer"] != a_own]
        base = sum(right(whole[j], a_own) for j in others) / max(1, len(others))
        cls = "own_bridge" if right(whole[i], a_own) else "true" if right(whole[i], a_true) else "other"
        rows.append({"id": i, "relation": rel, "bridge": b, "named": bp, "gen": g, "answer_text": whole[i][:40], "cls": cls, "baseline": round(base, 4)})
    n = len(rows)
    out = {"model": name, "counts": dict(counts), "n": n}
    if n:
        share = {c: round(100 * sum(r["cls"] == c for r in rows) / n, 1) for c in ("own_bridge", "true", "other")}
        base = round(100 * sum(r["baseline"] for r in rows) / n, 1)
        by = collections.defaultdict(list)
        for r in rows:
            by[f"{r['relation']}:{r['bridge']}"].append(100 * ((r["cls"] == "own_bridge") - r["baseline"]))
        rng, keys, bs = random.Random(0), sorted(by), []
        for _ in range(1000):
            xs = [x for k in (rng.choice(keys) for _ in keys) for x in by[k]]
            bs.append(sum(xs) / len(xs))
        bs.sort()
        out.update({"share": share, "baseline_own": base, "own_minus_baseline": round(share["own_bridge"] - base, 1),
                    "ci": [round(bs[25], 1), round(bs[974], 1)],
                    "composes_through_own_bridge": share["own_bridge"] - base >= 20 and bs[25] > 0})  # fmt: skip
    d = ROOT / "results/nn_wrongbridge"
    d.mkdir(exist_ok=True)
    (d / f"{p or 'qwen36_27b_'}wrongbridge.json").write_text(json.dumps({**out, "rows": rows}, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    for r in rows[:8]:
        print(f"  {r['bridge']:>14s} -> named {r['named']:<14s} | answer {r['answer_text']!r:42s} {r['cls']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
