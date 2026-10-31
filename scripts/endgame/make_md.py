"""Write rescore.md and competence_cards.md from rescore.json and competence_cards.json."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path("/workspace/scratch/endgame")
R = json.loads((OUT / "rescore.json").read_text())
D = json.loads((OUT / "competence_cards.json").read_text())
LBL = {"q27": "Qwen 27B", "q9": "Qwen 9B", "nl": "Lightning"}
RUNS = {"q27": ("jsuite_v2_test_chat_ko_cand2_v1", "jsuite_v2_test_chat_ko_cand2_L32-40_pca_v1", "L32-40"),
        "q9": ("qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_L12-16_pca_v1", "L12-16"),
        "nl": ("nem35l_jsuite_v2_test_chat_ko_cand2_v1", "nem35l_jsuite_v2_test_chat_ko_cand2_L27-33_pca_v1", "L27-33")}


def mk(c: dict | None) -> str:
    if not c:
        return "n/a"
    x = c["contrasts"]["M-K"]
    return f"{x['diff']:.1f} [{x['ci'][0]}, {x['ci'][1]}]"


def p(x, d=0) -> str:
    return "-" if x is None else f"{100 * x:.{d}f}"


L = ["# Endgame rescore of the jsuite v2 facts knock-out (CPU only, stored rows; no new GPU runs)", "",
     f"Repo /workspace/bridge-jspace at {R['repo_head'][:8]} (branch recovery-2026-10-19), read only. Code: "
     "/workspace/scratch/endgame/code/rescore.py (imports scripts/jsuite2_score.boot and scripts/c1_v2.margin_matched). "
     "Data: data/tasks_v2/jsuite_v2_test_chat (179 bridges x 2 levels; facts module). Raw numbers: rescore.json.", "",
     "Runs (one knock-out run per model; single data seed; deterministic conditions; the rotated controls use one fixed rotation seed):", ""]
for m, (h, pc, band) in RUNS.items():
    L.append(f"- {LBL[m]}: {h} (band {band}; paper10, paper10_rot, unembed10, unembed10_rot) and {pc} (paper10_pcasize); "
             f"competence run {R['guess_drop'][m]['comp_run']}")
L += ["", "M - K = points lost on recalled (final M) minus points lost on stated (final K); points lost = 100 x (1 - knock-out "
      "accuracy) among items right unedited in the same run (the scorer's definition). 95% CI: percentile bootstrap over "
      "relation:bridge clusters, 1000 reps, the scorer's boot(); CIs are rounded to integers by the scorer.", "",
      "## A. Reproduction", "",
      "| model | paper10 M-K | paper10_rot | unembed10 | pcasize | data.csv (mk / rot / u / pc) | within 0.1 |", "|---|---|---|---|---|---|---|"]
for m in RUNS:
    a = R["A"][m]
    f = lambda x: f"{x['diff']:.1f} [{x['ci'][0]}, {x['ci'][1]}]"  # noqa: E731
    L.append(f"| {LBL[m]} | {f(a['paper10_MK'])} (n M = {a['n_M']}) | {f(a['rot_MK'])} | {f(a['u_MK'])} | {f(a['pcasize_MK'])} | "
             f"{a['csv']['mk']} / {a['csv']['rot']} / {a['csv']['u']} / {a['csv']['pc']} | {'yes' if a['within_0.1'] else 'NO'} |")
cells = sum(v["cells"] for m in RUNS for k, v in R["A"][m].items() if isinstance(v, dict) and "cells" in v)
mis = sum(v["n_mismatch"] for m in RUNS for k, v in R["A"][m].items() if isinstance(v, dict) and "cells" in v)
L += ["", f"Every facts cell of the six stored score JSONs ({cells} cells: every condition x start / half / relation; every contrast, "
      f"its CI and every n) was recomputed with the scorer's logic and rng order: {mis} mismatches, max |diff| 0.0.", ""]

L += ["## B. Subsets", "",
      "Subset CIs: a fresh random.Random(0) per cell (the scorer shares one rng across cells, so the 'all' row's CI can differ "
      "by 1 point from the stored one: 27B [46, 56] here vs [46, 55] stored; point values identical).", "",
      "Definitions. Starts: P (bridge read, a made-up person bound to it), T (tracked), M (described). "
      "5 'not guessable': drop every item of a scene (start x level x bridge; the 5 finals share it) if the model's own "
      "competence run (the knock-out's tasks[1] run; cand2 read) answers the guess prompt of that scene's recalled-final item "
      "(word PM / TM / MM: the start replaced by an unknown one) correctly. 6: answer_vocab >= 14 (drops countries k=5 and "
      "animals k=6). 7: eponymous == False. 8 STRICT = start P and 5 and 6 and 7. 5b / 8b (robustness, stricter): drop a "
      "whole relation:bridge (both levels, every start) if any of its recalled-final guess prompts is right.", "",
      "| model | guessable scenes in set (of 1074) | scored scenes dropped by 5 (of scored) | guessable bridges (of 179) | scored scenes dropped by 5b |",
      "|---|---|---|---|---|"]
for m in RUNS:
    g = R["guess_drop"][m]
    L.append(f"| {LBL[m]} | {g['guessable_scenes_in_set']} | {g['scored_scenes_dropped']} of {g['scored_scenes']} | "
             f"{g['guessable_bridges']} | {g['scored_scenes_dropped_bridge_level']} of {g['scored_scenes']} |")
L.append("")
SUBS = ["1 all", "2 start P", "3 start T", "4 start M", "5 not guessable", "6 >=14 candidates", "7 non-eponymous", "8 STRICT",
        "5b not guessable (bridge-level)", "8b STRICT (bridge-level guess)"]
for m in RUNS:
    B = R["B"][m]
    L += [f"### {LBL[m]}", "", "| subset | n K / n M (bridges) | lost K / lost M (paper10) | paper10 M-K | paper10_rot | unembed10 | unembed10_rot | pcasize |",
          "|---|---|---|---|---|---|---|---|"]
    for s in SUBS:
        c = B[f"paper10|{s}"]
        L.append(f"| {s} | {c['n']['K']} / {c['n']['M']} ({c['bridges']}) | {c['loss']['K']:.1f} / {c['loss']['M']:.1f} | **{mk(c)}** | "
                 f"{mk(B[f'paper10_rot|{s}'])} | {mk(B[f'unembed10|{s}'])} | {mk(B[f'unembed10_rot|{s}'])} | {mk(B[f'paper10_pcasize|{s}'])} |")
    L.append("")
bp = R["B_pass"]
L += ["Pass bar (fixed in advance): STRICT M - K >= 10 with paper10_rot M - K <= 10, in >= 2 of 3 models.", "",
      "| model | STRICT paper10 M-K | STRICT rot M-K | pass |", "|---|---|---|---|"]
for m in RUNS:
    L.append(f"| {LBL[m]} | {mk(R['B'][m]['paper10|8 STRICT'])} | {mk(R['B'][m]['paper10_rot|8 STRICT'])} | {'PASS' if bp['per_model'][m] else 'fail'} |")
L += ["", f"Result: {'PASS' if bp['pass'] else 'FAIL'} ({sum(bp['per_model'].values())} of 3 models).", ""]

L += ["## C. Confidence-matched gap (c1_v2.margin_matched, applied to v2)", "",
      "Method = scripts/c1_v2.margin_matched unchanged (0.25-logit bins of the unedited answer margin from the competence run's "
      "'whole' row; recalled-final items against stated-final items in the same bin, bins weighted by recalled-final items; 95% "
      "bootstrap over items, 1000 reps, seed 0), with its groups set to recalled = PM, MM, TM and stated = PK, MK, TK "
      "(same question and answer). Items: right unedited in the knock-out run (so 'raw' equals the headline M - K). The c1_v2-style "
      "variant over every row (loss = unedited correct - knock-out correct) is in rescore.json and differs by at most 1.1 points (Lightning paper10: matched 49.6 [44.1, 55.7], 509 of 568 matched).", "",
      "| model | condition | raw | matched [95% CI] | matched / recalled-final items | reweighted to K margins | to M margins | median margin PK / MK / TK vs PM / MM / TM |",
      "|---|---|---|---|---|---|---|---|"]
for m in RUNS:
    for cond, v in R["C"][m].items():
        x = v["unedited_right_only"]
        md = x["median_margin"]
        L.append(f"| {LBL[m]} | {cond} | {p(x['raw_gap'], 1)} | **{p(x['matched_gap'], 1)}** [{p(x['matched_gap_ci'][0], 1)}, {p(x['matched_gap_ci'][1], 1)}] | "
                 f"{x['matched_n']} / {x['memory_n']} | {p(x['gap_at_prompt_margins'], 1)} | {p(x['gap_at_memory_margins'], 1)} | "
                 f"{md['PK']:.2f} / {md['MK']:.2f} / {md['TK']:.2f} vs {md['PM']:.2f} / {md['MM']:.2f} / {md['TM']:.2f} |")
L += ["", "Loss (points) by quartile of the unedited margin under paper10 (Q1 least confident; cuts over both groups), n per cell:", "",
      "| model | group | Q1 | Q2 | Q3 | Q4 |", "|---|---|---|---|---|---|"]
for m in RUNS:
    x = R["C"][m]["paper10"]["unedited_right_only"]
    for g, lab in (("memory", "recalled (M)"), ("prompt", "stated (K)")):
        L.append(f"| {LBL[m]} | {lab} | " + " | ".join(f"{p(a)} (n={n})" for a, n in x["by_quartile"][g]) + " |")
(OUT / "rescore.md").write_text("\n".join(L) + "\n")

# ---------------- competence cards ----------------
C = ["# Competence cards (unedited, cand2 read, stored competence runs; no new runs)", "",
     "Code: /workspace/scratch/endgame/code/competence_cards.py; raw numbers competence_cards.json. Accuracy in %. "
     "'correct' is each run's own field: cand2 read (top among the item's candidate answers, either case); hop 1 also needs "
     "the greedy generation to name the bridge (hop1='gen').", "",
     "Columns: n = items in the set; whole; h1 / h2 / h3 = each hop alone; guess = the guess prompt (start replaced by an unknown "
     "one; candidates = answer_vocab); chance = mean over items of 1/k, k = len(answer_vocab); maj = majority baseline: per "
     "relation (domain for three-hop), share of items whose answer is that relation's most common answer, pooled; real = "
     "(whole - guess) / (1 - guess), * if >= 0.7; elig = items passing tasks_v2.eligible's rule with the knock-out runs' settings "
     "(facts: scene rule over the 15 facts words; three-hop and numbers: per-item rule; level 'all', core stratum; replicated "
     "without its assert and checked equal to tasks_v2.eligible and to the knock-out rows' item sets where those exist); "
     "h1x = items with hop 1 alone wrong, and the share of them right on the whole question (shortcut diagnostic).", "",
     "Notes:"] + [f"- {n}" for n in D["notes"]] + [
     "- Lightning: facts from nem35l_jsuite_v2_test_chat_competence_cand2_v1 (the headline knock-out's); three-hop and numbers "
     "from nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1 (the run the Lightning three-hop / numbers knock-outs used; the "
     "facts-only run has no three-hop / numbers rows).",
     "- Ministral, Bolt, DeepSeek: their jsuite v2 test competence runs cover the 15 facts words only (manifest 'words'); "
     "three-hop and number words: NOT COMPUTABLE from stored runs.",
     "- OLMo: only a QA-rendering run exists (olmo32_jsuite_v2_test_qa_competence_cand2_v1 on jsuite_v2_test_qa; the same items, "
     "ids j2:qa:* map 1:1 to j2:chat:*, same questions and answers). Not directly comparable to the chat-rendered runs.",
     "- Never-named R start: v2.1 R competence runs exist for 27B, 9B, Lightning, Ministral, Muse, 122B. None for Bolt, "
     "DeepSeek, OLMo (OLMo has none; 9B-base has a QA one, not included).",
     "- The guess prompt keeps the scene's context (only the start is replaced), so 'guess' measures priors plus context cues, "
     "not priors alone: for K / A / P finals the answer is in the passage (guess 20-60%); for the R start the in-context "
     "entities are other countries etc. and RM / RN guess rates are 0-2%.",
     "- ANOMALY, not investigated: OLMo (QA rendering) answers the guess prompt right on 100% of nPR, nKR, nAR, nMR items "
     "(e.g. 53 of 53 nPR; 'How many fruits did Wanda pack?' with Wanda absent). The Qwen / Lightning runs do not (0-31%). "
     "Treat OLMo's number-word guess / real columns as suspect.",
     "- Common subset: three strong models = 27B, 9B, Lightning (the three headline models).", ""]


def row(w: str, c: dict) -> str:
    if not c.get("n"):
        return f"| {w} | {c.get('missing', 'no rows')} |" + " |" * 10
    h = c["hops"]
    return (f"| {w} | {c['n']} | {p(c['whole'])} | {p(h.get('step1'))} | {p(h.get('step2'))} | {p(h.get('step3'))} | {p(c['guess'])} | "
            f"{p(c['chance'])} | {p(c['majority_per_relation'])} | {p(c['real_comp'])}{'*' if c['real_comp_ge_0.7'] else ''} | "
            f"{c.get('eligible_n', '-')} | {c['hop1_wrong_n']}: {p(c['hop1_wrong_whole_right'])} |")


HDR = ["| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
# summary first: key cells across models
C += ["## Summary across models (recalled-final words, the two-hop words a model fails most, three-hop and number flags)", "",
      "| model | PM whole/guess/real | MM | TM | TP | MP | elig scenes P/M/T (of 358 per word) | three-hop words real >= 0.7 | number words real >= 0.7 |",
      "|---|---|---|---|---|---|---|---|---|"]
for m, v in D["models"].items():
    W = v["words"]
    f3 = lambda w: f"{p(W[w]['whole'])}/{p(W[w]['guess'])}/{p(W[w]['real_comp'])}"  # noqa: E731
    th = [w for w in ("PPP", "MPP", "PMP", "PPM", "MPM", "MMP", "PMM", "MMM") if W[w].get("n")]
    nu = [w for w in ("nPR", "nPL", "nPM", "nKR", "nKL", "nKM", "nAR", "nAL", "nAM", "nMR", "nML", "nMM") if W[w].get("n")]
    C.append(f"| {v['label']} | {f3('PM')} | {f3('MM')} | {f3('TM')} | {f3('TP')} | {f3('MP')} | "
             f"{W['PP'].get('eligible_n')}/{W['MP'].get('eligible_n')}/{W['TP'].get('eligible_n')} | "
             + (f"{sum(W[w]['real_comp_ge_0.7'] for w in th)} of 8 ({', '.join(w for w in th if W[w]['real_comp_ge_0.7'])})" if th else "no run") + " | "
             + (f"{sum(W[w]['real_comp_ge_0.7'] for w in nu)} of 12 ({', '.join(w for w in nu if W[w]['real_comp_ge_0.7'])})" if nu else "no run") + " |")
C += ["", "## Three-hop shortcut diagnostic (items whose hop 1 alone is wrong: n, and % of them right on the whole chain)", "",
      "| model | " + " | ".join(("PPP", "MPP", "PMP", "PPM", "MPM", "MMP", "PMM", "MMM")) + " |", "|---|" + "---|" * 8]
for m, v in D["models"].items():
    W = v["words"]
    if not W["PPP"].get("n"):
        C.append(f"| {v['label']} | no three-hop run |" + " |" * 7)
        continue
    C.append(f"| {v['label']} | " + " | ".join(f"{W[w]['hop1_wrong_n']}: {p(W[w]['hop1_wrong_whole_right'])}" for w in ("PPP", "MPP", "PMP", "PPM", "MPM", "MMP", "PMM", "MMM")) + " |")
C.append("")
C += ["## Never-named R start (v2.1 R competence runs)", "", *HDR]
for m, v in D["R"].items():
    C.append(f"| **{D['models'][m]['label']}** ({v['run']}) |" + " |" * 11)
    for w, c in v["words"].items():
        C.append(row(w, c))
C += ["", "RM per relation:", "", "| model | " + " | ".join(sorted(next(iter(D["R"].values()))["per_relation_RM"])) + " |",
      "|---|" + "---|" * len(next(iter(D["R"].values()))["per_relation_RM"])]
for m, v in D["R"].items():
    C.append(f"| {D['models'][m]['label']} | " + " | ".join(f"{p(c['whole'])}/{p(c['guess'])}/{p(c['real_comp'])} e{c.get('eligible_n')}"
                                                         for r, c in sorted(v["per_relation_RM"].items())) + " |")
C += ["(cells: whole / guess / real, e = eligible n)", ""]
C += ["## Common subset (items eligible in all three strong models: 27B, 9B, Lightning; by the knock-out's rule)", "",
      "Whole / guess / real on that subset. The three strong models are 100% on 'whole' there by construction (eligible = every "
      "non-guess prompt right); their guess rates are not.", ""]
for mod, v in D["common"].items():
    words = list(next(iter(v["per_model"].values())).keys())
    C += [f"### {mod}: {v['n_items']} items", "", "| model | " + " | ".join(words) + " |", "|---|" + "---|" * len(words)]
    for m, cw in v["per_model"].items():
        C.append(f"| {D['models'][m]['label']} | " + " | ".join(
            (f"{p(c['whole'])}/{p(c['guess'])}/{p(c['real_comp'])} (n{c['n']})" if c.get("n") else "-") for c in cw.values()) + " |")
    C.append("")
C += ["## Full cards per model", ""]
for m, v in D["models"].items():
    C += [f"### {v['label']} ({v['set']}; runs: " + ", ".join(sorted(set(v["runs"].values()))) + ")", "", *HDR]
    for w, c in v["words"].items():
        C.append(row(w, c))
    C += ["", "Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):", "",
          "| relation (k) | PM | MM | TM |", "|---|---|---|---|"]
    if v["per_relation"]:
        for r in sorted(v["per_relation"]["PM"]):
            cs = [v["per_relation"][w][r] for w in ("PM", "MM", "TM")]
            C.append(f"| {r} ({cs[0]['k'][0]}) | " + " | ".join(
                f"{p(c['whole'])} / {p(c['guess'])} / {p(c['real_comp'])}{'*' if c['real_comp_ge_0.7'] else ''}, e{c.get('eligible_n')} "
                f"(maj {p(c['majority_pooled'])}% '{c['majority_answer']}')" for c in cs) + " |")
    C.append("")
(OUT / "competence_cards.md").write_text("\n".join(C) + "\n")
print("ok")
