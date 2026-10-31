"""v3_score (Zach, 2026-10-28, prereg amendment 58 note 4): a jsuite v3 knock-out run scored by note 4's readings (CPU).

Points lost = among the items right unedited (as jsuite2_score), 95% bootstrap over bridges (relation:bridge, resampled
jointly), per condition x start x level (all, 1, 2, 3):
  contrasts   M - K (headline), M - P, M - N, A - M, H - K, M - H, G - K
  hard read   start P: H's loss under each condition minus paper10_rot's, and H vs M difficulty: unedited accuracy and
              median unedited log p of the answer's first token (the run's own `none` rows; note 4 says "margin": the
              knock-out rows carry log p, not the margin, so log p is the measure here), plus the M - H gap matched in
              log-p bins (0.5 nats, weighted by M items)
  conflict    finals C D E F (every item of an eligible scene, right or not): the share of answers giving the passage's
              (counterfactual) value, memory's value, or other, per condition; the shift from `none`; paper10's shift
              minus each control's, bootstrap over bridges; by word and near / far
  never-named RM - MM
  relations   start P, level all: M - K per relation
  P_nofilms   start P without films (cand2 reads a director's surname; the model writes the first name first)
  P_strict    P_nofilms and the item's guess prompt wrong in the model's competence run (no K or M item without one)
Writes results/ablate_v2/v3_score/RUN.json.

python scripts/v3_score.py RUN [--set jsuite_v3_test_chat]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
from jsuite2_score import boot  # noqa: E402

RES = ROOT / "results" / "ablate_v2"
DATA = ROOT / "data" / "tasks_v2"
CONTRASTS = (("M", "K"), ("M", "P"), ("M", "N"), ("A", "M"), ("H", "K"), ("M", "H"), ("G", "K"))
CONFLICT = "CDEF"
BIN = 0.5


def paired_boot(vals: dict[str, list[float]], rng: random.Random, reps: int = 1000) -> list[float]:
    """vals: cluster -> per-item differences; percentile interval of the mean, clusters resampled."""
    cl = sorted(vals)
    out = []
    for _ in range(reps):
        xs = [x for c in (rng.choice(cl) for _ in cl) for x in vals[c]]
        out.append(sum(xs) / len(xs))
    out.sort()
    return [round(out[int(0.025 * reps)], 1), round(out[int(0.975 * reps) - 1], 1)]


def main(run: str, set_name: str) -> None:
    from transformers import AutoTokenizer

    from scripts import suite_v1 as S

    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    man = json.loads((RES / run / "manifest.json").read_text())
    tok = AutoTokenizer.from_pretrained(man["model"]["repo"], revision=man["model"]["revision"])
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items]
    none = {r["id"]: r for r in rows if r["condition"] == "none"}
    guessed = {}  # the model's competence run (the run's eligibility): its guess prompt, right or not
    comp = man.get("tasks", [None, None])[1]
    if comp and (ROOT / "results" / "tasks_v2" / comp / "items.jsonl").exists():
        for line in (ROOT / "results" / "tasks_v2" / comp / "items.jsonl").open():
            r = json.loads(line)
            if r["part"] == "guess":
                guessed[r["id"]] = r["correct"]
    ok = {i for i, r in none.items() if r["correct"]}
    conds = list(dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"))
    by_cond = {c: {r["id"]: r for r in rows if r["condition"] == c} for c in conds}
    cl = lambda it: f"{it['relation']}:{it['bridge']}"  # noqa: E731
    rng = random.Random(0)
    out: dict = {"run": run, "set": set_name, "conditions": conds, "n_items": len(none), "cells": {}, "hard_read": {},
                 "conflict": {}, "never_named": {}, "relations": {}}  # fmt: skip
    starts = sorted({items[i]["start"] for i in none})
    # 1. points lost per condition x start x level
    for cond in conds:
        # P_nofilms: cand2 reads a director's surname, the model writes the first name; P_strict: also the item's guess
        # prompt wrong in the competence run (as the v2 re-score's strict subset)
        for st in [*starts, "named", "P_nofilms", "P_strict"]:
            for lv in ("all", 1, 2, 3):
                sel = collections.defaultdict(list)
                for i, r in by_cond[cond].items():
                    it = items[i]
                    if i not in ok or it["final"] in CONFLICT:
                        continue
                    if st in ("P_nofilms", "P_strict"):
                        if it["start"] != "P" or it["relation"] == "films":
                            continue
                        if st == "P_strict" and guessed.get(i, True):
                            continue
                    elif (st == "named" and it["start"] == "R") or (st != "named" and it["start"] != st):
                        continue
                    if lv != "all" and it["level"] != lv:
                        continue
                    sel[it["final"]].append((cl(it), r["correct"]))
                if sum(map(len, sel.values())) == 0:
                    continue
                cell = boot(sel, CONTRASTS, rng)
                out["cells"][f"{cond}/{st}/L{lv}"] = cell
    # 2. hard read (start P): H vs M difficulty, H's loss against rotated, the log-p matched M - H gap
    for lv in ("all", 1, 2, 3):
        pick = lambda f, lv=lv: [i for i in none if items[i]["start"] == "P" and items[i]["final"] == f and (lv == "all" or items[i]["level"] == lv)]  # noqa: E731
        H, M = pick("H"), pick("M")
        if not H or not M:
            continue
        d = {"unedited_acc": {f: round(100 * sum(none[i]["correct"] for i in ids) / len(ids), 1) for f, ids in (("H", H), ("M", M))},
             "median_logp_right": {f: round(statistics.median([none[i]["logp"] for i in ids if i in ok]), 3) for f, ids in (("H", H), ("M", M)) if any(i in ok for i in ids)},
             "n": {"H": len(H), "M": len(M)}, "by_condition": {}}  # fmt: skip
        for cond in conds:
            loss = lambda ids, cond=cond: [int(none[i]["correct"]) - int(by_cond[cond][i]["correct"]) for i in ids if i in ok and i in by_cond[cond]]  # noqa: E731
            lh, lm = loss(H), loss(M)
            bins = collections.defaultdict(lambda: ([], []))
            for k, ids in enumerate((M, H)):
                for i in ids:
                    if i in ok and i in by_cond[cond]:
                        bins[math.floor(none[i]["logp"] / BIN)][k].append(int(none[i]["correct"]) - int(by_cond[cond][i]["correct"]))
            num = den = 0.0
            for a, b in bins.values():
                if a and b:
                    num += len(a) * (statistics.mean(a) - statistics.mean(b))
                    den += len(a)
            d["by_condition"][cond] = {"H_lost": round(100 * statistics.mean(lh), 1) if lh else None,
                                       "M_lost": round(100 * statistics.mean(lm), 1) if lm else None,
                                       "M_minus_H_logp_matched": round(100 * num / den, 1) if den else None, "matched_M_items": int(den)}  # fmt: skip
        rot = d["by_condition"].get("paper10_rot", {}).get("H_lost")
        for cond, c in d["by_condition"].items():
            c["H_minus_rot"] = round(c["H_lost"] - rot, 1) if c["H_lost"] is not None and rot is not None else None
        out["hard_read"][f"P/L{lv}"] = d
    # 3. conflict: answer source shares, shifts from none, paper10's shift minus each control's
    forms = lambda v, k: {S.answer_token(tok, v, k), S.answer_token(tok, v.lower(), k)}  # noqa: E731

    def source(it: dict, pick: int) -> str:
        if pick in forms(it["conflict_value"], it["kind"]):
            return "passage"
        return "memory" if pick in forms(it["memory_answer"], it["kind"]) else "other"

    cf = [i for i in none if items[i]["final"] in CONFLICT]
    groups = {"all": cf}
    for i in cf:
        it = items[i]
        groups.setdefault(it["word"], []).append(i)
        groups.setdefault(f"{it['word']}-{'near' if it['cf_near'] else 'far'}", []).append(i)
        groups.setdefault(f"{it['start']}-start", []).append(i)
    for g, ids in groups.items():
        if not ids:
            continue
        cell: dict = {"n": len(ids), "share": {}, "shift": {}}
        src = {c: {i: source(items[i], by_cond[c][i]["pick2"]) for i in ids if i in by_cond[c]} for c in conds}
        src["none"] = {i: source(items[i], none[i]["pick2"]) for i in ids}
        for c, s in src.items():
            cnt = collections.Counter(s.values())
            cell["share"][c] = {k: round(100 * cnt[k] / len(s), 1) for k in ("passage", "memory", "other")} if s else None
        for c in conds:
            if src[c]:
                cell["shift"][c] = round(cell["share"][c]["passage"] - cell["share"]["none"]["passage"], 1)
        if "paper10" in conds:
            for ctrl in [c for c in conds if c != "paper10"]:
                vals = collections.defaultdict(list)
                for i in ids:
                    if i in src["paper10"] and i in src[ctrl]:
                        vals[cl(items[i])].append(100 * ((src["paper10"][i] == "passage") - (src[ctrl][i] == "passage")))
                if vals:
                    xs = [x for v in vals.values() for x in v]
                    cell[f"paper10_minus_{ctrl}"] = {"diff": round(sum(xs) / len(xs), 1), "ci": paired_boot(vals, rng)}
        out["conflict"][g] = cell
    # 4. never-named and 5. relations
    for cond in conds:
        sel = collections.defaultdict(list)
        for i, r in by_cond[cond].items():
            it = items[i]
            if i in ok and it["word"] in ("RM", "MM"):
                sel[it["word"]].append((cl(it), r["correct"]))
        if sel.get("RM") and sel.get("MM"):
            out["never_named"][cond] = boot(sel, [("RM", "MM")], rng)
        for rel in sorted({it["relation"] for it in items.values()}):
            sel = collections.defaultdict(list)
            for i, r in by_cond[cond].items():
                it = items[i]
                if i in ok and it["start"] == "P" and it["relation"] == rel and it["final"] in "KM":
                    sel[it["final"]].append((cl(it), r["correct"]))
            if sel.get("K") and sel.get("M"):
                out["relations"][f"{cond}/{rel}"] = boot(sel, [("M", "K")], rng)
    d = RES / "v3_score"
    d.mkdir(exist_ok=True)
    (d / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")
    # the headline lines
    for cond in conds:
        for st in ("P", "P_nofilms", "P_strict", "M", "T", "W", "Q", "J", "X", "Y", "named"):
            c = out["cells"].get(f"{cond}/{st}/Lall")
            if c:
                print(f"{cond:16s} start {st:9s} lost " + " ".join(f"{f} {c['loss'].get(f, float('nan')):4.0f}" for f in "PKMANHG")
                      + "  " + "  ".join(f"{k} {v['diff']:+.0f} {v['ci']}" for k, v in c["contrasts"].items() if k in ("M-K", "H-K", "M-H")))  # fmt: skip
    for k, v in out["hard_read"].items():
        print("hard read", k, json.dumps({c: (x["H_minus_rot"], x["M_minus_H_logp_matched"]) for c, x in v["by_condition"].items()}), v["unedited_acc"], v["median_logp_right"])
    c = out["conflict"].get("all")
    if c:
        print("conflict all", c["share"], {k: v for k, v in c.items() if k.startswith("paper10_minus")})
    for cond, v in out["never_named"].items():
        print("never-named", cond, v["loss"], v["contrasts"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    a = ap.parse_args()
    main(a.run, a.set)
