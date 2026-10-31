"""ko_subsets_v4 (Zach, 2026-10-29 red-team check, committed 2026-10-30 after the recount found it uncommitted): the v4
headline knock-out gap (recall MM minus lookup MP, points lost among items right unedited, note 20's runs) on subsets of
the gated items, with all four conditions. Not pre-registered: a confound check run after the headline was read.

Subsets (fixed word lists, not a per-model shortcut test):
  all; "no named work, no revealing name" (descriptions without a skip_cues flag in data/v3_bridges.json, i.e. no named
  famous work, and items whose bridge name does not reveal the answer: name_reveals_answer false); "named work only";
  "no films"; "less popular" (popularity != popular).
Gap = 100 * (mean MM loss - mean MP loss); 95% bootstrap over bridges (2000, random.Random(0)).

python scripts/ko_subsets_v4.py  -> results/ablate_v2/nn_ko_read/v4_subsets.json (+ a printed table)
"""

from __future__ import annotations

import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B = {(b["relation"], b["bridge"]): b for b in json.load(open(ROOT / "data" / "v3_bridges.json"))}
ITEMS = {json.loads(l)["id"]: json.loads(l) for l in open(ROOT / "data" / "tasks_v2" / "jsuite_v4_test_chat" / "items.jsonl")}
CONDS = ("paper10", "paper10_rot", "unembed10", "paper10_pcasize")
MODELS = {"9b": "qwen35_9b_", "27b": "", "lightning": "nem35l_"}


def named_work(it):
    b = B.get((it["relation"], it["bridge"]))
    if not b:
        return None
    for d, sc in zip(b["descriptions"], b.get("skip_cues", [])):
        if d["clause"] in it["start_desc"]:
            return bool(sc)
    return None


SUBSETS = {
    "all": lambda it: True,
    "no named work, no revealing name": lambda it: named_work(it) is False and not it.get("name_reveals_answer"),
    "named work only": lambda it: named_work(it) is True,
    "no films": lambda it: it["relation"] != "films",
    "less popular": lambda it: it.get("popularity") != "popular",
}


def gap(us):
    mm = [x for f, x in us if f == "MM"]
    mp = [x for f, x in us if f == "MP"]
    return 100 * (sum(mm) / len(mm) - sum(mp) / len(mp)) if mm and mp else float("nan")


def run(P):
    acc = collections.defaultdict(dict)
    for line in open(ROOT / "results" / "ablate_v2" / f"{P}jsuite_v4_test_chat_ko_cand2_v1" / "rows.jsonl"):
        r = json.loads(line)
        if r.get("kind", "clean") == "clean":
            acc[(r["family"], r["condition"])][r["id"]] = bool(r["correct_cand2"])
    out = {}
    for name, keep in SUBSETS.items():
        rec = {}
        for cond in CONDS:
            if (("MM", cond) not in acc) or (("MP", cond) not in acc):
                continue
            by = collections.defaultdict(list)
            n = collections.Counter()
            for fam in ("MM", "MP"):
                for i in acc[(fam, "none")]:
                    it = ITEMS[i]
                    if keep(it) and i in acc[(fam, cond)]:
                        by[it["bridge"]].append((fam, acc[(fam, "none")][i] - acc[(fam, cond)][i]))
                        n[fam] += 1
            us = [u for k in by for u in by[k]]
            keys, rng, bs = sorted(by), random.Random(0), []
            for _ in range(2000):
                v = gap([u for k in (rng.choice(keys) for _ in keys) for u in by[k]])
                if v == v:
                    bs.append(v)
            bs.sort()
            ci = [round(bs[int(0.025 * len(bs))], 1), round(bs[int(0.975 * len(bs)) - 1], 1)] if bs else None
            rec[cond] = {"gap": round(gap(us), 1), "ci": ci, "n_MM": n["MM"], "n_MP": n["MP"]}
        out[name] = rec
    return out


if __name__ == "__main__":
    res = {"note": "not pre-registered; a confound check after the headline was read (2026-10-29 red-team)", "models": {}}
    for m, P in MODELS.items():
        res["models"][m] = run(P)
        for name, rec in res["models"][m].items():
            p = rec.get("paper10", {})
            print(f"{m:9s} {name:34s} n {p.get('n_MM')}/{p.get('n_MP')} gap {p.get('gap')} {p.get('ci')} | "
                  + " | ".join(f"{c} {rec[c]['gap']}" for c in CONDS[1:] if c in rec))
    d = ROOT / "results" / "ablate_v2" / "nn_ko_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / "v4_subsets.json").write_text(json.dumps(res, indent=1) + "\n")
