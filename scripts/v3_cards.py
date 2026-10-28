"""v3_cards (Zach, 2026-10-28, amendment 58 note 4): competence cards on jsuite v3 for one model (CPU; stored runs only).

Inputs: results/tasks_v2/{p}jsuite_v3_test_chat_competence_cand2_v1 (whole, each hop alone, guess; K and M words),
results/competence_variants/{p}jsuite_v3_cv_v1 (cand2 + greedy reply, every word), {p}jsuite_v3probes_cv_v1 (probes).
Per word x level: whole accuracy (cand2; free generation by note 1's rule), hop 1 and hop 2 alone, guess, chance 1/k,
real-composition share (acc - guess)/(1 - guess); recalled finals: lure capture (the reply is another answer-vocabulary
word that appears in the passage); conflict finals: passage / memory / other; Y: follows the alternative bridge;
W vs M guess; probes: skip-the-bridge accuracy; the eligible-scene funnel (V4 rule).

python scripts/v3_cards.py PREFIX NAME   (PREFIX "" for Qwen 27B, "qwen35_9b_", "nem35l_")
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
from score_greedy import right  # noqa: E402

SET = "jsuite_v3_test_chat"
KM = ["PK", "PM", "MK", "MM", "WK", "WM", "TK", "TM", "XK", "XM", "QK", "QM", "JK", "JM", "YK", "YM", "RM"]


def pct(xs) -> float | None:
    return round(100 * sum(xs) / len(xs), 1) if xs else None


def main(p: str, name: str) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (ROOT / "data/tasks_v2" / SET / "items.jsonl").open()}
    comp = collections.defaultdict(dict)
    for line in (ROOT / "results/tasks_v2" / f"{p}{SET}_competence_cand2_v1" / "items.jsonl").open():
        r = json.loads(line)
        comp[r["id"]][r["part"]] = r["correct"]
    cv = {}
    for line in (ROOT / "results/competence_variants" / f"{p}jsuite_v3_cv_v1" / "rows.jsonl").open():
        r = json.loads(line)
        cv[r["id"]] = r
    cells = collections.defaultdict(lambda: collections.defaultdict(list))
    conflict = collections.defaultdict(collections.Counter)
    lure = collections.defaultdict(list)
    for iid, it in items.items():
        r = cv.get(iid)
        if r is None:
            continue
        key = (it["word"], it["level"])
        c = cells[key]
        c["cand2"].append(bool(r["correct_cand2"]))
        g = right(r["text"], it["answer"])
        c["free"].append(g)
        if iid in comp:
            for part in ("step1", "step2", "guess"):
                if part in comp[iid]:
                    c[part].append(bool(comp[iid][part]))
        c["k"].append(len(it["answer_vocab"]))
        if it["final"] in "MAN" and not g:  # a wrong recalled answer: another answer word from the passage?
            present = [v for v in it["answer_vocab"] if v != it["answer"] and v.lower() in it["context"].lower()]
            lure[key].append(any(right(r["text"], v) for v in present))
        if it["final"] in "CDEF":
            src = "passage" if right(r["text"], it["conflict_value"]) else "memory" if right(r["text"], it["memory_answer"]) else "other"
            conflict[(it["word"], "near" if it["cf_near"] else "far")][src] += 1
            conflict[(it["word"], "all")][src] += 1
    # eligibility funnel (V4: the scene's K and M items, and their hops alone, right; R: its M item)
    scene_items = collections.defaultdict(list)
    for iid, it in items.items():
        if it["word"] in KM:
            scene_items[it["scene"]].append(iid)
    def right_all(i: str) -> bool:  # whole question and each hop alone (the guess prompt is not part of eligibility)
        parts = {k: v for k, v in comp.get(i, {}).items() if k != "guess"}
        return bool(parts) and all(parts.values())

    ok = {s: all(right_all(i) for i in ids) for s, ids in scene_items.items()}
    elig = collections.Counter(s.split(":")[2].split("-")[0] + "-" + s.split(":")[2].split("-")[1] for s, v in ok.items() if v)
    total = collections.Counter(s.split(":")[2].split("-")[0] + "-" + s.split(":")[2].split("-")[1] for s in ok)
    out = {"model": name, "cells": {}, "conflict": {}, "lure_capture_of_wrong": {}, "eligible_scenes": {}}
    for (w, lv), c in sorted(cells.items()):
        guess = pct(c["guess"])
        acc = pct(c["cand2"])
        real = None if guess is None or acc is None or guess >= 100 else round((acc - guess) / (100 - guess), 2)
        out["cells"][f"{w}-L{lv}"] = {"n": len(c["cand2"]), "cand2": acc, "free": pct(c["free"]), "hop1": pct(c["step1"]),
                                      "hop2": pct(c["step2"]), "guess": guess, "chance": round(100 / (sum(c["k"]) / len(c["k"])), 1),
                                      "real_share": real}  # fmt: skip
    for k, cnt in sorted(conflict.items()):
        n = sum(cnt.values())
        out["conflict"][f"{k[0]}-{k[1]}"] = {"n": n, **{s: round(100 * cnt[s] / n, 1) for s in ("passage", "memory", "other")}}
    out["lure_capture_of_wrong"] = {f"{w}-L{lv}": {"wrong": len(v), "lure": pct(v)} for (w, lv), v in sorted(lure.items())}
    out["eligible_scenes"] = {k: f"{elig[k]}/{total[k]}" for k in sorted(total)}
    pr = ROOT / "results/competence_variants" / f"{p}jsuite_v3probes_cv_v1" / "rows.jsonl"
    if pr.exists():
        rows = [json.loads(line) for line in pr.open()]
        pitems = {json.loads(line)["id"]: json.loads(line) for line in (ROOT / "data/tasks_v2/jsuite_v3probes_test_chat/items.jsonl").open()}
        by = collections.defaultdict(list)
        for r in rows:
            by[pitems[r["id"]]["relation"]].append(right(r["text"], r["answer"]))
        out["probes_skip_bridge_right"] = {rel: f"{pct(v)}% of {len(v)}" for rel, v in sorted(by.items())}
    d = ROOT / "results/v3_cards"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{p or 'qwen36_27b_'}cards.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("eligible_scenes", "conflict", "probes_skip_bridge_right") if k in out}, indent=1)[:4000])
    for k in ("PK-L1", "PM-L1", "PM-L2", "PM-L3", "PH-L1", "PH-L3", "MM-L1", "WM-L1", "RM-L1", "TM-L1", "XM-L1", "YM-L1", "QM-L1", "JM-L1", "MH-L1"):
        if k in out["cells"]:
            print(k, out["cells"][k])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
