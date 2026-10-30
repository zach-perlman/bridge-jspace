"""report_breadth (Zach, 2026-10-27): the breadth half's README in the shape of Dan's (question, claims in bold,
evidence, controls, what failed, one grid of models x experiments), every number from one data.csv.

  docs/breadth/data.csv          every number: key, figure, model, quantity, value, lo, hi, n, unit, source
                                 (Dan's columns figure..source, plus a key the template cites and a unit)
  docs/breadth/README.template.md   hand-written prose; numbers only through markers
  docs/breadth/README.md         rendered

Markers: {{v|key}} value; {{a|key}} its size, unsigned; {{ci|key}} "[lo, hi]"; {{vci|key}} "value [lo, hi]"; {{n|key}}; {{grid}} the models x
experiments table; {{head}} the commit. A marker whose key is not in data.csv stops the build.

python scripts/report_breadth.py            (CPU only; reads results/ and the clean worktree's results)
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from scripts import fig_neel as F  # noqa: E402

D, RES, A2, SET = F.D, F.RES, F.A2, F.SET
OUT = ROOT / "docs" / "breadth"
FIGS_OUT = ROOT / "figures" / "breadth"  # figures/ by track (Dan, 30 Oct)
CLEAN = Path("/workspace/clean_bridge/results")
ROWS: list[dict] = []

# model key -> (name, digest label, prefix, band)
M = {
    "q27": ("Qwen3.6-27B", "Qwen3.6-27B", "", "32-40"),
    "q9": ("Qwen3.5-9B", "Qwen3.5-9B", "qwen35_9b_", "12-16"),
    "nl": ("Nemotron 3.5 Lightning", "Nemotron-3.5-Lightning", "nem35l_", "27-33"),
    "ds": ("DeepSeek-V4-Flash", "DeepSeek-V4-Flash", "dsv4f_", "18-23"),
    "mi": ("Ministral-3-14B", "Ministral-3-14B", "min14_", "32-37"),
    "nb": ("Nemotron 3.5 Bolt", "Nemotron-3.5-Bolt", "nem35b_", "42-53"),
    "ol": ("OLMo-3-32B base", "OLMo-3-32B (base, Q&A)", "olmo32_", "12-20"),
    "mu": ("Muse Glimmer 30B", "Muse-Glimmer-30B", "muse30_", "36-42"),
    "q122": ("Qwen3.5-122B (FP8)", "Qwen3.5-122B", "qwen35_122b_", "39-45"),
}
V2 = list(M)


def add(key, figure, model, quantity, value, lo=None, hi=None, n=None, unit="points", source=""):
    if value is None:
        return
    ROWS.append({"key": key, "figure": figure, "model": model, "quantity": quantity, "value": round(float(value), 3),
                 "lo": "" if lo is None else lo, "hi": "" if hi is None else hi, "n": "" if n is None else n, "unit": unit, "source": source})  # fmt: skip


def jl(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def c1u(run: str, band: str):
    """The logit-lens arm's gap at the model's own band (a c1_specificity file can hold several bands)."""
    s = jl(A2 / "c1_specificity" / f"{run}.json")
    b = (s or {}).get("bands", {}).get(f"L{band}", {})
    return (100 * b["unembed10"]["gap"], None) if "unembed10" in b else None


def ko_run(m):
    return D.MODELS[[x[0] for x in D.MODELS].index(M[m][1])]


def pointer_keys(m: str) -> None:
    """Amendment 51's pointer tests (Bolt's at K 100, amendment 55 note 1)."""
    run = dict(D.POINTER).get(M[m][1])
    s = jl(RES / "jswap" / run / "summary.json") if run else None
    if s:
        t = lambda c: s[f"memory/{c}"]["transfer"]  # noqa: E731
        src = f"results/jswap/{dict(D.POINTER)[M[m][1]]}/summary.json"
        add(f"ptr.{m}.swap", "pointer", m, "J-part swap, same passage", t("swap"), *s["memory/swap"]["ci"], s["memory/swap"]["n"], source=src)
        add(f"ptr.{m}.neutral", "pointer", m, "neutral-sentence donor / same-passage swap", t("swap_neutral") / t("swap"), unit="ratio", source=src)
        add(f"ptr.{m}.noown", "pointer", m, "without own-word directions / swap", t("swap_noown") / t("swap"), unit="ratio", source=src)
        add(f"ptr.{m}.rot", "pointer", m, "neutral donor, rotated", t("swap_neutral_rot"), source=src)
        # the same transfers in points with their 95% intervals (Dan 30 Oct: r4's rows 2-5; scripts/ptr_intervals.py checks
        # them against the per-item rows)
        for key, cond, what in (("neutral_pts", "swap_neutral", "neutral-sentence donor, transfer"),
                                ("noown_pts", "swap_noown", "without own-word directions, transfer"),
                                ("rot_pts", "swap_neutral_rot", "neutral donor, rotated, transfer")):  # fmt: skip
            add(f"ptr.{m}.{key}", "pointer", m, what, t(cond), *s[f"memory/{cond}"]["ci"], s[f"memory/{cond}"]["n"], source=src)
        rels = sorted({k.split("/")[0][len("memory_"):] for k in s if k.startswith("memory_")})
        read = [r for r in rels if (s.get(f"memory_{r}/swap", {}).get("transfer") or 0) >= 10]
        held = [r for r in read if s[f"memory_{r}/swap_neutral"]["transfer"] >= 2 / 3 * s[f"memory_{r}/swap"]["transfer"]]
        add(f"ptr.{m}.rel_held", "pointer", m, "relations where the neutral donor keeps >= 2/3", len(held), unit="count", source=src)
        add(f"ptr.{m}.rel_read", "pointer", m, "relations read (swap >= 10)", len(read), unit="count", source=src)
        tl = s["timeline_memory"]
        lays = sorted({int(x.split("/L")[1]) for x in tl})
        fx = next((la for la in lays if tl[f"none/L{la}"]["kept"] >= 50), None)
        add(f"ptr.{m}.lookup", "pointer", m, "first layer where the lens reads X's attribute on >= 50% (answer position)", fx, unit="layer", source=src)


def collect() -> None:
    # ---- 1. knock-out at K = 10 (test)
    for m in V2:
        lab, ko, band, _s, sw, mid, pr, pc, xr, renders = ko_run(m)
        src = f"results/ablate_v2/jsuite2_score/{ko}.json"
        j = D.mk(ko)
        if not j:
            continue
        add(f"ko.{m}.mk", "knockout", m, "M - K, J++ top 10", j["d"], *j["ci"], j["n"], source=src)
        add(f"ko.{m}.klost", "knockout", m, "stated facts (K) lost", j["K"], unit="abs", source=src)
        for cond, q in (("paper10_rot", "rot"), ("unembed10", "u")):
            x = D.mk(ko, cond)
            if x:
                add(f"ko.{m}.{q}", "knockout", m, f"M - K, {cond}", x["d"], *x["ci"], source=src)
        if pc:
            x = D.mk(pc, "paper10_pcasize")
            if x:
                add(f"ko.{m}.pc", "knockout", m, "M - K, same norm along top principal directions", x["d"], *x["ci"], source=f"results/ablate_v2/jsuite2_score/{pc}.json")
                add(f"ko.{m}.pcr", "knockout", m, "size-matched / J++ M - K", x["d"] / j["d"], unit="ratio", source=f"results/ablate_v2/jsuite2_score/{pc}.json")
        so = (jl(A2 / "soft_score" / f"{ko}.json") or {}).get("paper10")
        if so:
            add(f"ko.{m}.soft", "knockout", m, "M - K by probability", so["soft_M-K"], *so["soft_ci"], source=f"results/ablate_v2/soft_score/{ko}.json")
        for i, r in enumerate(renders, 2):
            x = D.mk(r)
            if x:
                add(f"ko.{m}.r{i}", "knockout", m, f"M - K, rendering {i}", x["d"], *x["ci"], source=f"results/ablate_v2/jsuite2_score/{r}.json")
        c = F.score(ko).get("facts", {}).get("paper10/start=all", {}).get("loss", {})
        for f in "KPANM":
            if f in c:
                add(f"ko.{m}.lost{f}", "knockout", m, f"points lost, final {f}", c[f], unit="abs", source=src)
        for st in "PTM":
            x = F.cell(ko, f"paper10/start={st}")
            if x:
                add(f"ko.{m}.start{st}", "knockout", m, f"M - K, start {st}", x[0], *x[1], source=src)
        for rel in ("countries", "languages", "people", "cities", "companies", "landmarks", "dishes", "animals"):
            x = F.cell(ko, f"paper10/relation={rel}")
            if x:
                add(f"ko.{m}.rel.{rel}", "knockout", m, f"M - K, relation {rel}", x[0], *x[1], source=src)
        for h in "AB":
            x = F.cell(ko, f"paper10/half={h}")
            if x:
                add(f"ko.{m}.half{h}", "knockout", m, f"M - K, test half {h}", x[0], *x[1], source=src)
        rr = f"{M[m][2]}{SET}_ko_cand2_v1+{M[m][2]}jsuite_v2_1_test_chat_R_ko_cand2_v1"
        x = F.cell(rr, "paper10/never_named", "RM-MM")
        if x:
            add(f"r.{m}", "never named", m, "RM - MM (bridge never named minus named once)", x[0], *x[1], source=f"results/ablate_v2/jsuite2_score/{rr}.json")
    # removal size of the top-10 removal at the band
    for lab, run in D.SIZE:
        m = next((k for k, v in M.items() if v[1] == lab), None)
        if m:
            add(f"size.{m}", "knockout", m, "share of the residual norm removed, J++ top 10", D.share(run, "jlens_top10"), unit="pct", source=f"results/removal_size/{run}/summary.json")
    # plain-text cost of the removal (gate band)
    for m, run in (("q27", "textloss_top_l32_40_v1"), ("q9", "qwen35_9b_textloss_top_l12_16_v1"), ("nl", "nem35l_textloss_top_v2gate_v1"),
                   ("ds", "dsv4f_textloss_top_v2gate_v1"), ("mi", "min14_textloss_top_v2gate_v1"), ("nb", "nem35b_textloss_top_v2gate_v1"),
                   ("ol", "olmo32_textloss_top_l20_44_v1"), ("mu", "muse30_textloss_top_l36_42_v1"), ("q122", "qwen35_122b_textloss_L39-45_v1"),
                   ("q32", "qwen3_32b_textloss_top_l44_52_v1"), ("oh7", "olmoh7_textloss_top_l4_8_v1"), ("o7", "olmo3d7_textloss_top_l10_14_v1"),
                   ("gemma", "gemma4itf_sink_textloss_v1"), ("gptoss", "gptoss20_textloss_top_v1"), ("kol", "kol1_textloss_top_l15_35_v1")):  # fmt: skip
        s = jl(RES / "removal_textloss" / run / "summary.json")
        if s:
            nll = s["mean_nll"]
            add(f"text.{m}", "gate", m, "plain-text loss added by the top-10 removal", nll["top10"] - nll["none"], unit="nats", source=f"results/removal_textloss/{run}/summary.json")
            add(f"text.{m}.rot", "gate", m, "plain-text loss added, rotated", nll["top10_rot"] - nll["none"], unit="nats", source=f"results/removal_textloss/{run}/summary.json")
    # ---- clean-checkout reruns, row by row
    for m, (old, new) in {"q27": ("jsuite_v2_test_chat_ko_cand2_v1", "clean_jsuite_v2_test_chat_ko_cand2_v1"),
                          "q9": ("qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", "qwen35_9b_clean_jsuite_v2_test_chat_ko_cand2_v1"),
                          "nl": ("nem35l_jsuite_v2_test_chat_ko_cand2_v1", "nem35l_clean_jsuite_v2_test_chat_ko_cand2_v1")}.items():  # fmt: skip
        a, b = A2 / old / "rows.jsonl", CLEAN / "ablate_v2" / new / "rows.jsonl"
        if a.exists() and b.exists() and (CLEAN / "ablate_v2" / new / "summary.json").exists():
            k = lambda x: (x["family"], x["id"], x["kind"], x["band"], x["condition"])  # noqa: E731
            ra = {k(x): x for x in map(json.loads, a.read_text().splitlines())}
            rb = {k(x): x for x in map(json.loads, b.read_text().splitlines())}
            sh = set(ra) & set(rb)
            add(f"clean.{m}.rows", "reruns", m, "rows compared (run of record vs clean checkout)", len(sh), unit="count", source=f"clean worktree {new}")
            add(f"clean.{m}.diff", "reruns", m, "rows whose answer differs", sum(ra[x]["correct"] != rb[x]["correct"] for x in sh), unit="count", source=f"clean worktree {new}")
    c = jl(RES / "checks" / "clean_nem35l_rerun_1027.json")
    if c:
        r = c["M-K"]["rerun"]
        add("clean.nl.mk_rerun", "reruns", "nl", "M - K, Lightning clean-checkout rerun", r["diff"], *r["ci"], source="results/checks/clean_nem35l_rerun_1027.json")
    # ---- 2. other datasets (the Qwens; toy, natural, natplus, v1)
    for m, pre in (("q27", ""), ("q9", "qwen35_9b_")):
        for i, run in enumerate(("full2_ko_v1", "fresh2_ko_v1", "fresh3_ko_v1"), 1):
            x = F.c1gap(pre + run)
            if x:
                add(f"toy.{m}.s{i}", "datasets", m, f"toy puzzles, data seed {i}: memory minus prompt finals", x[0], source=f"results/ablate_v2/c1_v2/{pre}{run}.json")
        x = c1u(pre + "full2_ko_unembed_v1", M[m][3])
        if x:
            add(f"toy.{m}.u", "datasets", m, "toy puzzles, logit lens", x[0], source=f"results/ablate_v2/c1_specificity/{pre}full2_ko_unembed_v1.json")
        for i in (1, 2, 3):
            x = F.c1gap(f"{pre}natural_v{i}_chat_ko_v1")
            if x:
                add(f"nat.{m}.s{i}", "datasets", m, f"natural fact chains, seed {i}", x[0], source=f"results/ablate_v2/c1_v2/{pre}natural_v{i}_chat_ko_v1.json")
        x = c1u(f"{pre}natural_v1_chat_ko_unembed_v1", M[m][3])
        if x:
            add(f"nat.{m}.u", "datasets", m, "natural fact chains, logit lens", x[0], source=f"results/ablate_v2/c1_specificity/{pre}natural_v1_chat_ko_unembed_v1.json")
        npr = f"{pre}natplus_v1_chat_ko_cand2_v1"
        for key, cond, grp in (("", "paper10", "all/all"), (".u", "unembed10", "all/all"), (".pop", "paper10", "popularity/popular"), (".rare", "paper10", "popularity/rare")):
            x = F.natplus(npr, cond, grp)
            if x:
                add(f"natplus.{m}{key}", "datasets", m, f"natplus {grp} {cond}", x[0], *(x[1] or (None, None)), source=f"results/ablate_v2/natplus_split/{npr}.json")
        v1r = f"{pre}jsuite_v1_facts_test_chat_ko_cand2_v1"
        for key, run_, cond in (("", v1r, "paper10"), (".u", v1r, "unembed10"), (".s2", f"{pre}jsuite_v1_facts_s2_test_chat_ko_cand2_v1", "paper10"),
                                (".prefill", f"{pre}jsuite_v1_facts_test_prefill_ko_cand2_v1", "paper10")):  # fmt: skip
            x = F.v1(run_, cond)
            if x:
                add(f"v1.{m}{key}", "datasets", m, f"jsuite v1 M - P ({run_}, {cond})", x[0], *x[1], source=f"results/ablate_v2/jsuite_score/{run_}.json")
    for key, run_ in (("v1.q9.qa", "qwen35_9b_jsuite_v1_facts_test_qa_ko_cand2_v1"), ("v1.q9base.qa", "qwen35_9bb_jsuite_v1_facts_test_qa_ko_cand2_v1"),
                      ("v1.q9inst.qa", "qwen35_9boj_jsuite_v1_facts_test_qa_ko_cand2_v1"), ("v1.q27.jlens", "q27jlens_jsuite_v1_facts_test_chat_ko_cand2_v1")):  # fmt: skip
        x = F.v1(run_)
        if x:
            add(key, "datasets", key.split(".")[1], f"jsuite v1 M - P ({run_})", x[0], *x[1], source=f"results/ablate_v2/jsuite_score/{run_}.json")
    x = D.mk("qwen35_9bb_jsuite_v2_test_qa_ko_cand2_v1")
    if x:
        add("ko.q9base.mk", "datasets", "q9base", "M - K, 9B base model (Q&A)", x["d"], *x["ci"], x["n"], source="results/ablate_v2/jsuite2_score/qwen35_9bb_jsuite_v2_test_qa_ko_cand2_v1.json")
    # other models on the earlier datasets
    for m, run in (("q32", "qwen3_32b_full2_ko_v1"), ("q32", "qwen3_32b_fresh2_ko_v1"), ("mu", "muse30_full2_ko_v1"), ("oh7", "olmoh7_big2_ko_v1"),
                   ("o7", "olmo3d7_big2_ko_v1"), ("q122", "qwen35_122b_full2_ko_v1"), ("oh7", "olmoh7_natural_v1_chat_ko_v1"), ("o7", "olmo3d7_natural_v1_chat_ko_v1")):  # fmt: skip
        x = F.c1gap(run)
        if x:
            add(f"old.{m}.{run}", "datasets", m, f"gap on {run}", x[0], source=f"results/ablate_v2/c1_v2/{run}.json")
    # keep-own: toy (c1_v2 keepown.restored) and v2 (amendment 55)
    for m, run in (("q27", "full2_ko_keepown_v1"), ("q9", "qwen35_9b_full2_ko_keepown_v1"), ("q32", "qwen3_32b_full2_ko_keepown_v1")):
        s = jl(A2 / "c1_v2" / f"{run}.json")
        if s and "keepown" in s:
            add(f"keepown.toy.{m}", "keep-own", m, "toy: share of the loss restored by keeping the own word", s["keepown"]["restored"], unit="ratio", source=f"results/ablate_v2/c1_v2/{run}.json")
    for m in ("q27", "q9", "nl", "mi"):
        run = f"{M[m][2]}{SET}_ko_cand2_L{M[m][3]}_keepown_s150_v1"
        a, b = F.cell(run, "paper10/start=all"), F.cell(run, "paper10_keepown/start=all")
        if a and b:
            add(f"keepown.{m}.mk", "keep-own", m, "M - K, paper10 (keep-own run)", a[0], *a[1], source=f"results/ablate_v2/jsuite2_score/{run}.json")
            add(f"keepown.{m}.mkk", "keep-own", m, "M - K, own word kept", b[0], *b[1], source=f"results/ablate_v2/jsuite2_score/{run}.json")
            add(f"keepown.{m}", "keep-own", m, "share restored by keeping the own word", 1 - b[0] / a[0], unit="ratio", source=f"results/ablate_v2/jsuite2_score/{run}.json")
    # ---- 3. positions
    for m in ("q27", "q9", "nl"):
        for st in ("P", "T", "M", "all"):
            for mode in ("", "_posbridge", "_poscontext", "_posquestion"):
                run = f"{M[m][2]}{SET}_ko_cand2{mode}_v1"
                x = F.cell(run, f"paper10/start={st}")
                if x:
                    add(f"pos.{m}.{st}.{mode.strip('_pos') or 'all'}", "positions", m, f"M - K, start {st}, {mode.strip('_') or 'every token'}", x[0], *x[1], source=f"results/ablate_v2/jsuite2_score/{run}.json")
                xr = F.cell(run, f"paper10_rot/start={st}") if st == "all" else None  # the rotated control of each middle-band removal
                if xr:
                    add(f"pos.{m}.{st}.{mode.strip('_pos') or 'all'}.rot", "positions", m, f"M - K, start {st}, {mode.strip('_') or 'every token'} (paper10_rot)", xr[0], *xr[1], source=f"results/ablate_v2/jsuite2_score/{run}.json")
    for key, run in (("pos.q27late.bridge", "jsuite_v2_test_chat_ko_cand2_L52-60_posbridge_v1"), ("pos.q27late.question", "jsuite_v2_test_chat_ko_cand2_L52-60_posquestion_v1"),
                     ("pos.mi.bridge", "min14_jsuite_v2_test_chat_ko_cand2_L32-37_posbridge_v1"), ("pos.mi.question", "min14_jsuite_v2_test_chat_ko_cand2_L32-37_posquestion_v1"),
                     ("pos.q122.bridge", "qwen35_122b_jsuite_v2_test_chat_ko_cand2_posbridge_v1"), ("pos.q122.question", "qwen35_122b_jsuite_v2_test_chat_ko_cand2_posquestion_v1"),
                     ("pos.ds.question", "dsv4f_jsuite_v2_test_chat_ko_cand2_L18-23_posquestion_v1"),
                     ("pos.mu.bridge", "muse30_jsuite_v2_test_chat_ko_cand2_L36-42_posbridge_v1"), ("pos.mu.question", "muse30_jsuite_v2_test_chat_ko_cand2_L36-42_posquestion_v1"),
                     ("pos.nb.bridge", "nem35b_jsuite_v2_test_chat_ko_cand2_L42-53_k100_posbridge_s150_v1"), ("pos.nb.question", "nem35b_jsuite_v2_test_chat_ko_cand2_L42-53_k100_posquestion_s150_v1")):  # fmt: skip
        cond = "top100" if key.startswith("pos.nb") else "paper10"
        x = F.cell(run, f"{cond}/start=all")
        if x:
            add(key, "positions", key.split(".")[1], f"M - K at {run}", x[0], *x[1], source=f"results/ablate_v2/jsuite2_score/{run}.json")
    # ---- 4. swaps, pointer, probe, lookup
    for key, run in (("q27", "jswap_v2_v1"), ("q9", "qwen35_9b_jswap_v2_v1"), ("nl", "nem35l_jswap_v2_v1"), ("ol", "olmo32_jswap_v2_v1"),
                     ("nb", "nem35b_jswap_v2_v1"), ("nb.k100", "nem35b_jswap_v2_k100_v1"), ("ds.mid", "dsv4f_jswap_v2_L22-27_v1"),
                     ("mi.mid", "min14_jswap_v2_L20-25_v1"), ("mi.mid.k100", "min14_jswap_v2_L20-25_k100_v1")):  # fmt: skip
        p = D.pooled(run) or {}
        for c in ("swap", "paste", "swap_comp", "swap_rot", "swap_u"):
            v = p.get(f"memory/{c}")
            if v:
                add(f"swap.{key}.{c}", "swaps", key.split(".")[0], f"transfer, memory finals pooled, {c} ({run})", v["transfer"], *v["ci"], v["n"], source=f"results/jswap/{run}/rows.jsonl")
    # stated finals under the swaps (Dan's gaps.md row 3, 2026-10-27): the J-part, its complement and the paste on PK / TK
    for key, run in (("q27", "jswap_v2_v1"), ("q9", "qwen35_9b_jswap_v2_v1"), ("nl", "nem35l_jswap_v2_v1")):
        s_ = jl(RES / "jswap" / run / "summary.json") or {}
        for w in ("PK", "TK"):
            for c, ck in (("swap", "swapK"), ("swap_comp", "comp"), ("paste", "pasteK")):
                v = s_.get(f"{w}/{c}")
                if v:
                    add(f"swap.{key}.{ck}.{w}", "swaps", key, f"transfer on stated final {w}, {c} ({run})", v["transfer"], *v["ci"], v["n"], source=f"results/jswap/{run}/summary.json")
    for m, run in (("q27", "jswap_ans_v2_v1"), ("q9", "qwen35_9b_jswap_ans_v2_v1")):
        s = jl(RES / "jswap" / run / "summary.json") or {}
        for c in ("swap", "swap_noans", "swap_ans", "swap_ans_rot"):
            v = s.get(f"PM/{c}")
            if v:
                add(f"ans.{m}.{c}", "swaps", m, f"transfer (PM), {c}", v["transfer"], *v["ci"], source=f"results/jswap/{run}/summary.json")
    for m in ("q27", "q9", "nl"):
        lab, ko, band, _s, sw, mid, pr, pc, xr, renders = ko_run(m)
        s = jl(RES / "jswap" / xr / "summary.json")
        if s:
            add(f"xrel.{m}", "pointer", m, "cross-relation / same-relation donor", s["memory/swap_xrel"]["transfer"] / s["memory/swap_srel"]["transfer"], unit="ratio", source=f"results/jswap/{xr}/summary.json")
        pointer_keys(m)
        s = jl(RES / "probe_ceiling" / pr / "summary.json")
        if s and "memory_valid/swap" in s:
            add(f"probe.{m}.swap", "probe", m, "J++ swap on probe-valid relations", s["memory_valid/swap"]["transfer"], source=f"results/probe_ceiling/{pr}/summary.json")
            add(f"probe.{m}.probe", "probe", m, "probe-subspace swap", s["memory_valid/swap_probe"]["transfer"], source=f"results/probe_ceiling/{pr}/summary.json")
            sp = s["memory_valid/swap_probe"]
            add(f"probe.{m}.probe_pts", "probe", m, "probe-subspace swap, transfer (probe-valid relations)", sp["transfer"], *sp["ci"], sp["n"], source=f"results/probe_ceiling/{pr}/summary.json")
    pointer_keys("nb")
    # ---- 5. dose (amendment 54) and swap dose (amendment 55)
    for (mm, pre, band), m in zip(F.DOSE54, ("q27", "q9", "nl", "mi", "nb", "ds", "mu"), strict=True):
        d = F.dose_data(mm, pre, band)
        if not d:
            continue
        src = f"results/ablate_v2/jsuite2_score/{pre}{SET}_ko_cand2_{band}_dose54_s150_v1.json"
        for r in d:
            k = r["k"]
            add(f"dose.{m}.k{k}", "dose", m, f"M - K, J++ top {k}", r["mk"], *r["ci"], source=src)
            for q in ("rot", "pc", "u", "smk", "spc", "K", "sK", "exc"):
                if r[q] is not None:
                    add(f"dose.{m}.k{k}.{q}", "dose", m, f"{q} at K {k}", r[q], source=src)
            add(f"dose.{m}.k{k}.share", "dose", m, f"residual share removed at K {k}", r["share"], unit="pct", source=src)
        r10 = next((r for r in d if r["k"] == 10), None)
        if r10 and r10["pc"] is not None and f"ko.{m}.pcr" not in {x["key"] for x in ROWS}:  # no stand-alone size-matched run (Bolt): the dose run's K 10
            add(f"ko.{m}.pcr", "knockout", m, "size-matched / J++ M - K at K 10 (dose run, 150 per word)", r10["pc"] / r10["mk"], unit="ratio", source=src)
        rd = F.dose_readings(d)
        add(f"dose.{m}.kstar", "dose", m, "plateau K* as pre-registered", rd["kstar"], unit="K", source=src)
        if rd["limit"]:
            add(f"dose.{m}.limit", "dose", m, "specificity limit as pre-registered (stated facts lose > 10, or size-matched > half of J++)", rd["limit"], unit="K", source=src)
        add(f"dose.{m}.ekstar", "dose", m, "plateau K* on the J-specific excess (note 1)", rd["ekstar"], unit="K", source=src)
        if rd["plim"]:
            add(f"dose.{m}.plim", "dose", m, "probability limit (stated facts lose > 10 by probability)", rd["plim"], unit="K", source=src)
    for m, runs in (("q27", ["jswap_v2_k10_s150_v1", "jswap_v2_k30_s150_v1", "jswap_v2_k100_s150_v1"]),
                    ("q9", ["qwen35_9b_jswap_v2_k10_s150_v1", "qwen35_9b_jswap_v2_k30_s150_v1", "qwen35_9b_jswap_v2_k100_s150_v1"]),
                    ("nl", ["nem35l_jswap_v2_k10_s150_v1", "nem35l_jswap_v2_k30_s150_v1", "nem35l_jswap_v2_k100_s150_v1"]),
                    ("nb", ["nem35b_jswap_v2_v1", "nem35b_jswap_v2_k30_v1", "nem35b_jswap_v2_k100_v1"]),
                    ("mi", ["min14_jswap_v2_L20-25_v1", "min14_jswap_v2_L20-25_k30_v1", "min14_jswap_v2_L20-25_k100_v1"])):  # fmt: skip
        for k, run in zip((10, 30, 100), runs, strict=True):
            p = D.pooled(run) or {}
            v = p.get("memory/swap")
            if v:
                add(f"swapk.{m}.k{k}", "swap dose", m, f"J-part swap transfer, K {k}", v["transfer"], *v["ci"], v["n"], source=f"results/jswap/{run}/rows.jsonl")
    # ---- 6. beyond two hops (v1 modules), generation spot-check
    c = jl(A2 / "nat3_score" / "jsuite_v1_threehop_chat_ko_cand2_v1.json")
    if c:
        for w, v in c["cells"]["all/paper10"].items():
            add(f"hop3.q27.{w}", "three hops", "q27", f"excess over PPP, {w}", v["excess_over_PPP"], *v["ci"], v["n"], source="results/ablate_v2/nat3_score/jsuite_v1_threehop_chat_ko_cand2_v1.json")
    for m, run in (("q27", "jsuite_v1_numbers_chat_ko_cand2_pi_v1"), ("q9", "qwen35_9b_jsuite_v1_numbers_chat_ko_cand2_pi_v1")):
        s = jl(A2 / "ctxcomp_score" / f"{run}.json")
        if s:
            for k in ("KR-PR", "AR-PR", "MR-PR"):
                v = s["cells"]["paper10"]["contrasts"][k]
                add(f"num.{m}.{k}", "numbers", m, f"numbers {k}", v["diff"], *v["ci"], source=f"results/ablate_v2/ctxcomp_score/{run}.json")
    for m, run in (("q27", "natplus_v1_chat_genspot_cand2_v1"), ("q9", "qwen35_9b_natplus_v1_chat_genspot_cand2_strat_v1"), ("nl", "nem35l_natplus_v1_chat_genspot_cand2_v1"), ("mu", "muse30_natplus_v1_chat_genspot_cand2_v1")):
        s = jl(RES / "gen_spot" / run / "summary.json")
        if s:
            for w in ("PM", "MM"):
                cl = s["cells"][f"{w}/paper10"]["class"]
                n = sum(cl.values())
                add(f"gen.{m}.{w}.bridge", "spot-check", m, f"{w}: replies naming the bridge", 100 * cl.get("bridge", 0) / n, n=n, unit="pct", source=f"results/gen_spot/{run}/summary.json")
                add(f"gen.{m}.{w}.right", "spot-check", m, f"{w}: replies still right", 100 * cl.get("answer", 0) / n, n=n, unit="pct", source=f"results/gen_spot/{run}/summary.json")
    # f2's paired differences, lens part minus a same-size control (Dan 30 Oct; scripts/f2_differences.py)
    from scripts import f2_differences as F2  # noqa: PLC0415

    for r in F2.rows():
        add(r["key"], r["figure"], r["model"], r["quantity"], r["value"], r["lo"], r["hi"], r["n"] or None, r["unit"], r["source"])


def collect_night() -> None:
    """2026-10-27 night (amendments 55-56): Lightning on the natural sets, the v2 modules, determinism, lens kind."""
    npr = "nem35l_natplus_v1_chat_ko_cand2_v1"
    for key, cond, grp in (("", "paper10", "all/all"), (".u", "unembed10", "all/all"), (".rot", "paper10_rot", "all/all"),
                           (".pop", "paper10", "popularity/popular"), (".rare", "paper10", "popularity/rare")):  # fmt: skip
        x = F.natplus(npr, cond, grp)
        if x:
            add(f"natplus.nl{key}", "datasets", "nl", f"natplus {grp} {cond}", x[0], *(x[1] or (None, None)), source=f"results/ablate_v2/natplus_split/{npr}.json")
    c = jl(A2 / "nat3_score" / "nem35l_nat3_v1_chat_ko_cand2_v1_drop.json")
    if c:
        for cond in ("paper10", "paper10_rot", "unembed10"):
            for w, v in c["cells"][f"all/{cond}"].items():
                add(f"nat3.nl.{cond}.{w}", "three hops", "nl", f"natural three-hop excess over PPP, {w}, {cond}", v["excess_over_PPP"], *v["ci"], v["n"], source="results/ablate_v2/nat3_score/nem35l_nat3_v1_chat_ko_cand2_v1_drop.json")
    # v2's modules (amendment 56 A) and jsuite_v2nb's (amendment 57: numbers reps 80, a second three-hop seed)
    for tag, st in (("mod", SET), ("mod2", "jsuite_v2nb_test_chat")):
        for m, pre in (("q27", ""), ("q9", "qwen35_9b_"), ("nl", "nem35l_")):
            for mod, run in (("threehop", f"{pre}{st}_threehop_ko_cand2_v1"), ("numbers", f"{pre}{st}_numbers_ko_cand2_dd_v1")):
                s = jl(A2 / "jsuite2_score" / f"{run}.json")
                if not s:
                    continue
                for cond in ("paper10", "paper10_rot", "unembed10", "unembed10_rot"):
                    cell = s[mod].get(cond, {})
                    for con, v in cell.get("contrasts", {}).items():
                        add(f"{tag}.{m}.{mod}.{cond}.{con}", mod, m, f"{st} {mod} {con} ({cond})", v["diff"], *v["ci"], source=f"results/ablate_v2/jsuite2_score/{run}.json")
                    for w, lo in cell.get("loss", {}).items():
                        add(f"{tag}.{m}.{mod}.{cond}.loss.{w}", mod, m, f"{st} {mod} points lost, {w} ({cond})", lo, n=cell["n"].get(w), unit="abs", source=f"results/ablate_v2/jsuite2_score/{run}.json")
    c = jl(RES / "checks" / "clean57_1027.json")
    if c:
        cs = c["comparisons"]
        same = [r for r in cs if r["rows_record"] == r["rows_clean"] == r["shared"] and not any(r["differing"].values()) and r["max_abs_logp_diff"] == 0]
        add("clean57.n", "reruns", "all", "amendment 57 clean-checkout comparisons", len(cs), unit="count", source="results/checks/clean57_1027.json")
        add("clean57.same", "reruns", "all", "of them row-identical (every read and log-probability)", len(same), unit="count", source="results/checks/clean57_1027.json")
        add("clean57.rows", "reruns", "all", "rows and items compared", sum(r["shared"] for r in cs), unit="count", source="results/checks/clean57_1027.json")
    # late-band position splits (amendment 57 B), start = all, as the 27B's late band
    for m, pre, band in (("q9", "qwen35_9b_", "26-29"), ("nl", "nem35l_", "33-39"), ("q27", "", "52-60")):
        for mode, suf in (("all", ""), ("question", "_posquestion"), ("bridge", "_posbridge")):
            run = f"{pre}{SET}_ko_cand2_L{band}{suf}_v1"
            for cond, ck in (("paper10", ""), ("paper10_rot", ".rot"), ("unembed10", ".u")):
                x = F.cell(run, f"{cond}/start=all")
                if x:
                    add(f"late.{m}.{mode}{ck}", "positions", m, f"M - K at L{band}, {mode} ({cond})", x[0], *x[1], source=f"results/ablate_v2/jsuite2_score/{run}.json")
    x = D.mk("qwen35_9boj_jsuite_v2_test_chat_ko_cand2_v1")
    if x:
        add("ko.q9oj.mk", "lens kind", "q9", "M - K, 9B with our own J++ fit", x["d"], *x["ci"], x["n"], source="results/ablate_v2/jsuite2_score/qwen35_9boj_jsuite_v2_test_chat_ko_cand2_v1.json")
    a, b = A2 / "nem35l_jsuite_v2_test_chat_ko_cand2_detcheck_v1" / "rows.jsonl", CLEAN / "ablate_v2" / "nem35l_clean_jsuite_v2_test_chat_ko_cand2_v1" / "rows.jsonl"
    if a.exists() and b.exists():
        k = lambda x: (x["family"], x["id"], x["kind"], x["band"], x["condition"])  # noqa: E731
        ra = {k(x): x for x in map(json.loads, a.read_text().splitlines())}
        rb = {k(x): x for x in map(json.loads, b.read_text().splitlines())}
        sh = set(ra) & set(rb)
        add("det.nl.rows", "reruns", "nl", "determinism check: rows compared with the clean rerun", len(sh), unit="count", source="results/ablate_v2/nem35l_jsuite_v2_test_chat_ko_cand2_detcheck_v1")
        add("det.nl.same", "reruns", "nl", "determinism check: rows with identical log-probability", sum(ra[x]["logp"] == rb[x]["logp"] for x in sh), unit="count", source="results/ablate_v2/nem35l_jsuite_v2_test_chat_ko_cand2_detcheck_v1")


# ---- rendering
def fmt(r: dict, ci: bool = False) -> str:
    v, u = r["value"], r["unit"]
    if u == "points":
        s = "0" if abs(v) < 0.5 else f"{v:+.0f}"
    elif u == "ratio":
        s = f"{v:.2f}"
    elif u == "pct":
        s = f"{v:.0f}%"
    elif u == "abs":
        s = f"{v:.0f}"
    elif u == "nats":
        s = f"{v:+.2f} nats"
    else:
        s = f"{v:.0f}"
    if ci and r["lo"] != "":
        s += f" [{r['lo']:.0f}, {r['hi']:.0f}]" if u == "points" else f" [{r['lo']}, {r['hi']}]"
    return s


def grid(rows: dict) -> str:
    def g(key, ci=False):
        return fmt(rows[key], ci) if key in rows else "·"

    head = ["Model", "plain-text cost", "M − K (top 10)", "rotated / logit lens", "size-matched (share)", "by probability",
            "renderings", "clean rerun", "keep-own restores", "J-part swap / paste", "neutral donor", "probe swap (J++ / probe)", "dose: K* (excess)"]  # fmt: skip
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for m in V2:
        ren = ", ".join(g(f"ko.{m}.r{i}") for i in (2, 3) if f"ko.{m}.r{i}" in rows) or "·"
        cl = f"{g(f'clean.{m}.diff')} of {g(f'clean.{m}.rows')} differ" if f"clean.{m}.rows" in rows else "·"
        sw = f"swap.{m}" if f"swap.{m}.swap" in rows else f"swap.{m}.mid" if f"swap.{m}.mid.swap" in rows else None
        swc = f"{g(sw + '.swap')} / {g(sw + '.paste')}" + (" (mid depth)" if sw and sw.endswith("mid") else "") if sw else "·"
        if m == "nb" and "swap.nb.k100.swap" in rows:
            swc += f"; K 100: {g('swap.nb.k100.swap')}"
        out.append("| " + " | ".join([M[m][0] + f" (L{M[m][3]})", g(f"text.{m}"), g(f"ko.{m}.mk", True), f"{g(f'ko.{m}.rot')} / {g(f'ko.{m}.u')}",
                                      g(f"ko.{m}.pcr"), g(f"ko.{m}.soft"), ren, cl, g(f"keepown.{m}"), swc, g(f"ptr.{m}.neutral"),
                                      f"{g(f'probe.{m}.swap')} / {g(f'probe.{m}.probe')}" if f"probe.{m}.swap" in rows else "·",
                                      f"{g(f'dose.{m}.kstar')} ({g(f'dose.{m}.ekstar')})" if f"dose.{m}.kstar" in rows else "·"]) + " |")  # fmt: skip
    return "\n".join(out)


def render() -> None:
    rows = {r["key"]: r for r in ROWS}
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    tpl = (OUT / "README.template.md").read_text()
    missing = []

    def sub(mo):
        kind, *rest = mo.group(1).split("|")
        if kind == "grid":
            return grid(rows)
        if kind == "head":
            return head
        key = rest[0]
        if key not in rows:
            missing.append(key)
            return "??"
        r = rows[key]
        return {"v": fmt(r), "a": f"{abs(r['value']):.0f}", "vci": fmt(r, True), "ci": fmt(r, True)[len(fmt(r)) + 1 :], "n": str(r["n"])}[kind]

    text = re.sub(r"\{\{([^}]+)\}\}", sub, tpl)
    if missing and "--draft" not in sys.argv:
        sys.exit(f"markers without a number in data.csv: {sorted(set(missing))}")
    if missing:
        print(f"DRAFT: {len(set(missing))} markers shown as ??: {sorted(set(missing))}")
    (OUT / "README.md").write_text("<!-- Generated by scripts/report_breadth.py from docs/breadth/README.template.md and data.csv; edit the template. -->\n" + text)
    print(f"README.md: {text.count(chr(10))} lines, {len(ROWS)} numbers in data.csv")


FIGS = {"F01_dataset": "fig00_dataset", "F03_needed": "fig01_needed", "F04_settings": "fig02_datasets", "F05_robust": "fig03_robust",
        "F06_where": "fig04_where", "F07_carries": "fig05_carries", "F08_pointer": "fig06_pointer", "F09_lookup": "fig07_lookup",
        "F02_readable": "fig08_readable", "F10_dose": "fig09_dose", "F11_beyond": "fig10_beyond", "F12_scorecard": "fig11_scorecard"}  # fmt: skip


def copy_figures() -> None:
    """The figure set (scripts/fig_neel.py, rendered into /workspace/scratch/neel_figures) under the README's names."""
    import shutil

    FIGS_OUT.mkdir(parents=True, exist_ok=True)
    for src, dst in FIGS.items():
        f = F.OUT / f"{src}.png"
        if f.exists():
            shutil.copyfile(f, FIGS_OUT / f"{dst}.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    copy_figures()
    collect()
    collect_night()
    with (OUT / "data.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["key", "figure", "model", "quantity", "value", "lo", "hi", "n", "unit", "source"])
        w.writeheader()
        w.writerows(ROWS)
    print(f"data.csv: {len(ROWS)} rows")
    if (OUT / "README.template.md").exists():
        render()
