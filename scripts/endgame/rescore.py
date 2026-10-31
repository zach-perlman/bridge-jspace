"""Endgame rescore (CPU only, read-only on the repo). Parts A (reproduce), B (subsets), C (margin-matched gap).

Reuses scripts/jsuite2_score.boot (bootstrap over relation:bridge clusters, percentile 95%) and
scripts/c1_v2.margin_matched (0.25-logit margin bins, bootstrap over items). Writes only under OUT.
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

REPO = Path("/workspace/bridge-jspace")
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import c1_v2 as C  # noqa: E402
from scripts import jsuite2_score as J  # noqa: E402

assert "torch" not in sys.modules
OUT = Path("/workspace/scratch/endgame")
RES = REPO / "results" / "ablate_v2"
SET = "jsuite_v2_test_chat"
MODELS = {  # key: (label, headline run, pca run)
    "q27": ("Qwen 27B", "jsuite_v2_test_chat_ko_cand2_v1", "jsuite_v2_test_chat_ko_cand2_L32-40_pca_v1"),
    "q9": ("Qwen 9B", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_L12-16_pca_v1"),
    "nl": ("Lightning", "nem35l_jsuite_v2_test_chat_ko_cand2_v1", "nem35l_jsuite_v2_test_chat_ko_cand2_L27-33_pca_v1"),
}
HEADLINE = {"q27": 50.9, "q9": 42.6, "nl": 53.1}  # docs/breadth/data.csv ko.*.mk
CSV_ROT = {"q27": 2.7, "q9": 1.8, "nl": 3.6}
CSV_U = {"q27": 1.9, "q9": 1.4, "nl": 8.7}
CSV_PC = {"q27": 12.4, "q9": 7.3, "nl": 8.2}

items = {json.loads(x)["id"]: json.loads(x) for x in (REPO / "data/tasks_v2" / SET / "items.jsonl").read_text().splitlines()}


def load_rows(run: str) -> list[dict]:
    rows = [json.loads(x) for x in (RES / run / "rows.jsonl").read_text().splitlines()]
    return [r for r in rows if r["kind"] == "clean" and r["id"] in items]


def replicate_main(run: str, by_relation: bool = True) -> dict:
    """jsuite2_score.main's facts part, verbatim logic and rng order, without writing into the repo."""
    rows = load_rows(run)
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    conds = list(dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"))
    rng = random.Random(0)
    out = {}
    for cond in conds:
        rs = [r for r in rows if r["condition"] == cond and (r["family"], r["id"]) in ok]
        fr = [r for r in rs if items[r["id"]]["module"] == "facts"]
        if not fr:
            continue
        keys = [("start", s) for s in ("P", "M", "T", "all")] + [("half", h) for h in ("A", "B")]
        if by_relation:
            keys += [("relation", x) for x in sorted({items[r["id"]]["relation"] for r in fr})]
        for kind, val in keys:
            sel = collections.defaultdict(list)
            for r in fr:
                it = items[r["id"]]
                if kind == "start" and val != "all" and it["start"] != val:
                    continue
                if it["start"] == "R":
                    continue
                if kind == "half" and it.get("half") != val:
                    continue
                if kind == "relation" and it["relation"] != val:
                    continue
                sel[it["final"]].append((f"{it['relation']}:{it['bridge']}", r["correct"]))
            if all(sel[f] for f in "KM"):
                out[f"{cond}/{kind}={val}"] = J.boot(sel, J.FACT_CONTRASTS, rng)
    return out


def comp_run_of(run: str) -> str:
    return json.loads((RES / run / "manifest.json").read_text())["tasks"][1]


def comp_rows(comp: str) -> list[dict]:
    return [json.loads(x) for x in (REPO / "results/tasks_v2" / comp / "items.jsonl").read_text().splitlines()]


import subprocess
report: dict = {"A": {}, "B": {}, "C": {}, "guess_drop": {},
                "repo_head": subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()}
GUESS_BRIDGES: set = set()

# ---------------- A: reproduce ----------------
for m, (label, run, pca) in MODELS.items():
    rep = {}
    for r_ in (run, pca):
        stored = json.loads((RES / "jsuite2_score" / f"{r_}.json").read_text())["facts"]
        mine = replicate_main(r_, by_relation=any("relation=" in k for k in stored))
        worst = 0.0
        mism = []
        for k, cell in stored.items():
            if k not in mine:
                mism.append(f"missing {k}")
                continue
            for c, v in cell["contrasts"].items():
                d = abs(v["diff"] - mine[k]["contrasts"][c]["diff"])
                worst = max(worst, d)
                if v["ci"] != mine[k]["contrasts"][c]["ci"]:
                    mism.append(f"ci {k} {c} stored {v['ci']} mine {mine[k]['contrasts'][c]['ci']}")
            if cell["n"] != mine[k]["n"]:
                mism.append(f"n {k} stored {cell['n']} mine {mine[k]['n']}")
        extra = [k for k in mine if k not in stored]
        rep[r_] = {"cells": len(stored), "max_abs_diff_any_contrast": worst, "mismatches": mism[:20], "n_mismatch": len(mism),
                   "extra_cells": extra[:5]}
        if r_ == run:
            rep["paper10_MK"] = mine["paper10/start=all"]["contrasts"]["M-K"]
            rep["rot_MK"] = mine["paper10_rot/start=all"]["contrasts"]["M-K"]
            rep["u_MK"] = mine["unembed10/start=all"]["contrasts"]["M-K"]
            rep["n_M"] = mine["paper10/start=all"]["n"]["M"]
        else:
            rep["pcasize_MK"] = mine["paper10_pcasize/start=all"]["contrasts"]["M-K"]
    rep["csv"] = {"mk": HEADLINE[m], "rot": CSV_ROT[m], "u": CSV_U[m], "pc": CSV_PC[m]}
    rep["within_0.1"] = all(abs(a - b) <= 0.1 for a, b in (
        (rep["paper10_MK"]["diff"], HEADLINE[m]), (rep["rot_MK"]["diff"], CSV_ROT[m]),
        (rep["u_MK"]["diff"], CSV_U[m]), (rep["pcasize_MK"]["diff"], CSV_PC[m])))
    report["A"][m] = rep
    print("A", m, rep["paper10_MK"], rep["rot_MK"], rep["u_MK"], rep["pcasize_MK"], "within 0.1:", rep["within_0.1"],
          {k: (v["max_abs_diff_any_contrast"], v["n_mismatch"]) for k, v in rep.items() if isinstance(v, dict) and "cells" in v})

if not all(report["A"][m]["within_0.1"] for m in MODELS):
    (OUT / "rescore.json").write_text(json.dumps(report, indent=1))
    sys.exit("A FAILED: headline not reproduced within 0.1; stopping")

# ---------------- B: subsets ----------------
SUBSETS = ["1 all", "2 start P", "3 start T", "4 start M", "5 not guessable", "6 >=14 candidates", "7 non-eponymous", "8 STRICT",
           "5b not guessable (bridge-level)", "8b STRICT (bridge-level guess)"]


def guess_scenes(comp: str) -> tuple[set, int, int]:
    """Scenes whose recalled-final (xM) item's guess prompt the model answers right (competence 'correct', cand2 read)."""
    g = {r["scene"] for r in comp_rows(comp) if r["part"] == "guess" and r["id"] in items
         and items[r["id"]]["module"] == "facts" and items[r["id"]]["final"] == "M" and r["correct"]}
    scenes = {it["scene"] for it in items.values() if it["module"] == "facts" and it["start"] in "PMT"}
    return g, len(g), len(scenes)


def in_subset(it: dict, s: str, gs: set) -> bool:
    if it["start"] not in "PMT":
        return False
    ng = it["scene"] not in gs
    # robustness variant: drop a bridge (relation:bridge, every start and level) if any of its M-final guess prompts is right
    ngb = f"{it['relation']}:{it['bridge']}" not in GUESS_BRIDGES
    c14 = len(it["answer_vocab"]) >= 14
    ne = not it["eponymous"]
    return {"1 all": True, "2 start P": it["start"] == "P", "3 start T": it["start"] == "T", "4 start M": it["start"] == "M",
            "5 not guessable": ng, "6 >=14 candidates": c14, "7 non-eponymous": ne,
            "8 STRICT": it["start"] == "P" and ng and c14 and ne,
            "5b not guessable (bridge-level)": ngb, "8b STRICT (bridge-level guess)": it["start"] == "P" and ngb and c14 and ne}[s]


def cell(rows: list[dict], ok: set, cond: str, s: str, gs: set) -> dict | None:
    sel = collections.defaultdict(list)
    for r in rows:
        if r["condition"] != cond or (r["family"], r["id"]) not in ok:
            continue
        it = items[r["id"]]
        if it["module"] != "facts" or not in_subset(it, s, gs):
            continue
        sel[it["final"]].append((f"{it['relation']}:{it['bridge']}", r["correct"]))
    if not all(sel[f] for f in "KM"):
        return None
    c = J.boot(sel, J.FACT_CONTRASTS, random.Random(0))
    c["bridges"] = len({b for v in sel.values() for b, _ in v})
    return c


for m, (label, run, pca) in MODELS.items():
    comp = comp_run_of(run)
    assert comp == comp_run_of(pca), (comp, comp_run_of(pca))
    gs, ng, ns = guess_scenes(comp)
    scene_bridge = {it["scene"]: f"{it['relation']}:{it['bridge']}" for it in items.values() if it["module"] == "facts"}
    GUESS_BRIDGES = {scene_bridge[s_] for s_ in gs}
    # how many of the knock-out's own scored scenes this drops
    rows_h = load_rows(run)
    scored = {items[r["id"]]["scene"] for r in rows_h if items[r["id"]]["module"] == "facts"}
    report["guess_drop"][m] = {"comp_run": comp, "guessable_scenes_in_set": ng, "scenes_in_set": ns,
                               "scored_scenes": len(scored), "scored_scenes_dropped": len(scored & gs),
                               "guessable_bridges": len(GUESS_BRIDGES), "bridges": len(set(scene_bridge.values())),
                               "scored_scenes_dropped_bridge_level": sum(1 for s_ in scored if scene_bridge[s_] in GUESS_BRIDGES)}
    out_m = {}
    for run_, conds in ((run, ("paper10", "paper10_rot", "unembed10", "unembed10_rot")), (pca, ("paper10_pcasize",))):
        rows = load_rows(run_)
        ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
        for cond in conds:
            for s in SUBSETS:
                out_m[f"{cond}|{s}"] = cell(rows, ok, cond, s, gs)
    report["B"][m] = out_m

passes = {}
for m in MODELS:
    st = report["B"][m]["paper10|8 STRICT"]
    rt = report["B"][m]["paper10_rot|8 STRICT"]
    passes[m] = bool(st and rt and st["contrasts"]["M-K"]["diff"] >= 10 and rt["contrasts"]["M-K"]["diff"] <= 10)
report["B_pass"] = {"per_model": passes, "pass": sum(passes.values()) >= 2}
print("B pass", report["B_pass"])

# ---------------- C: margin-matched ----------------
C.MEMORY_FINAL, C.PROMPT_FINAL = ("PM", "MM", "TM"), ("PK", "MK", "TK")  # recalled vs stated, same question and answer
for m, (label, run, pca) in MODELS.items():
    comp = comp_run_of(run)
    margin = {r["id"]: r["margin"] for r in comp_rows(comp) if r["part"] == "whole" and r.get("margin") is not None}
    rows = load_rows(run)
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    res = {}
    for cond in ("paper10", "paper10_rot", "unembed10"):
        its = [(r["family"], margin[r["id"]], 1 - int(r["correct"])) for r in rows
               if r["condition"] == cond and r["family"] in C.MEMORY_FINAL + C.PROMPT_FINAL
               and (r["family"], r["id"]) in ok and r["id"] in margin]
        mm = C.margin_matched(its)
        # c1_v2-style variant: every row (loss = unedited correct - knock-out correct), not only unedited-right items
        none = {(r["family"], r["id"]): r["correct"] for r in rows if r["condition"] == "none"}
        its_all = [(r["family"], margin[r["id"]], int(none[(r["family"], r["id"])]) - int(r["correct"])) for r in rows
                   if r["condition"] == cond and r["family"] in C.MEMORY_FINAL + C.PROMPT_FINAL and r["id"] in margin]
        mm_all = C.margin_matched(its_all)
        res[cond] = {"unedited_right_only": mm, "all_rows_c1v2_style": {k: mm_all[k] for k in ("raw_gap", "matched_gap", "matched_gap_ci", "matched_n", "memory_n")},
                     "n_items": len(its), "n_prompt": sum(1 for w, _, _ in its if w in C.PROMPT_FINAL)}
        print("C", m, cond, round(100 * mm["raw_gap"], 1), round(100 * mm["matched_gap"], 1),
              [round(100 * x, 1) for x in mm.get("matched_gap_ci", [])], mm["matched_n"], "/", mm["memory_n"])
    report["C"][m] = res

(OUT / "rescore.json").write_text(json.dumps(report, indent=1, default=str))
print("wrote", OUT / "rescore.json")
