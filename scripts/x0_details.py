"""x0_details: every X0 number the README quotes, recomputed from the run files, and the details page.

Writes docs/x0_numbers.json (key -> {"text", "source"}; the README's {{num|key}} markers read it through
scripts/readme_build.py) and docs/x0_details.md, rendered from docs/x0_details.template.md: {{num|key}} becomes the
number, {{tbl|name}} a table generated from the runs. UNVERIFIED like the runs.

uv run python scripts/x0_details.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_descriptive as D
from scripts import x0_figures as XF
from scripts import x0_necessity as X
from scripts import x0_strata as ST

DOCS = pins.REPO_ROOT / "docs"
NUMBERS = DOCS / "x0_numbers.json"
TEMPLATE = DOCS / "x0_details.template.md"
MODELS = {"9b": ("qwen3.5-9b", "qwen35_9b_x0_necessity", "qwen35_9b_x0_kmatch"),
          "27b": ("qwen3.6-27b", "x0_necessity_27b_chat", "x0_kmatch_27b"),
          "122b": ("qwen3.5-122b-a10b", "qwen35_122b_x0_necessity_r2", "qwen35_122b_x0_necessity_r2"),
          "muse": ("muse-glimmer-30b", "muse30b_x0_necessity", "muse30b_x0_necessity")}  # fmt: skip
CTX = "results/d1_verdict/x0_ctx_parts_27b_20261024-144050/verdict.json"
NOCHAT = {"9b": "qwen35_9b_x0_necessity_nothink", "27b": "x0_necessity_27b_nothink"}
DIGIT = {"9b": "qwen35_9b_x0_digit_r2", "27b": "x0_digit_27b_r2", "122b": "qwen35_122b_x0_necessity_r2",
         "muse": "muse30b_x0_necessity"}  # fmt: skip
SINGLE = {"9b": "qwen35_9b_x0_single_r2", "27b": "x0_single_27b_r2", "122b": "qwen35_122b_x0_single",
          "muse": "muse30b_x0_single"}  # fmt: skip
PROBES = {"9b": "qwen35_9b_x0_probe", "27b": "x0_probe_27b"}
PROBES_V4 = {"9b": "qwen35_9b_x0_probe_v4", "27b": "x0_probe_v4_27b", "122b": "qwen35_122b_x0_probe_v4",
             "muse": "muse30b_x0_probe_v4"}  # fmt: skip
AMNESIC = {"9b": "qwen35_9b_x0_amnesic", "27b": "x0_amnesic_27b", "122b": "qwen35_122b_x0_amnesic",
           "muse": "muse30b_x0_amnesic"}  # fmt: skip
X0B = {"9b": "qwen35_9b_x0b_v2", "27b": "x0b_v2_27b", "122b": "qwen35_122b_x0b_v2", "muse": "muse30b_x0b_v2"}
ATOMS = {"letters": "x0_atoms_27b_letters", "all": "x0_atoms_27b_all", "letters_9b": "qwen35_9b_x0_atoms_letters"}
PARTS = {"9b": "qwen35_9b_x0_parts", "27b": "x0_parts_27b"}
MASSMEAN = {"9b": "qwen35_9b_x0_massmean", "27b": "x0_massmean_27b"}
MASSMEAN_LF = {"9b": "qwen35_9b_x0_massmean_lf", "27b": "x0_massmean_lf_27b", "122b": "qwen35_122b_x0_massmean_grid",
               "muse": "muse30b_x0_massmean_grid"}  # fmt: skip
PCAEQ = {"9b": "qwen35_9b_x0_pcaeq", "27b": "x0_pcaeq_27b", "122b": "qwen35_122b_x0_parts", "muse": "muse30b_x0_parts"}
X0BPARTS = {"9b": "qwen35_9b_x0b_parts", "27b": "x0b_parts_27b", "122b": "qwen35_122b_x0b_parts"}
JPPOTHER = {"9b": "qwen35_9b_x0_jppother", "27b": "x0_jppother_27b", "122b": "qwen35_122b_x0_jppother",
            "muse": "muse30b_x0_jppother"}  # fmt: skip
X4 = {"9b": ("qwen35_9b_x4_probe", "qwen35_9b_x4_patch"), "27b": ("x4_probe_27b", "x4_patch_27b"),
      "122b": ("qwen35_122b_x4_probe", "qwen35_122b_x4_patch"), "muse": ("muse30b_x4_probe", "muse30b_x4_patch")}  # fmt: skip
REPLICATE = {"9b": "qwen35_9b_x0_replicate", "27b": "x0_replicate_27b", "muse": "muse30b_x0_replicate"}
NATURAL = {"9b": "qwen35_9b_x5_natural", "27b": "x5_natural_27b", "122b": "qwen35_122b_x5_natural",
           "muse": "muse30b_x5_natural"}  # fmt: skip
ROUTES = {"9b": "qwen35_9b_x6_routes", "27b": "x6_routes_27b", "muse": "muse30b_x6_routes"}
# rte: the early layers (9B L6, 27B L16); rtg: the 122B after the data, gate 0.75; rtb: J++ and the pointer
# directions removed together (x6_routes_bothoff)
ROUTES_MORE = {"rte": {"9b": "qwen35_9b_x6_routes_l6", "27b": "x6_routes_l16_27b", "122b": "qwen35_122b_x6_routes_l27_g75",
                       "muse": "muse30b_x6_routes_l13"},
               "rtg": {"122b": "qwen35_122b_x6_routes_g75"},
               "rtb": {"9b": "qwen35_9b_x6_routes_bothoff", "27b": "x6_routes_bothoff_27b",
                       "122b": "qwen35_122b_x6_routes_bothoff_g75", "muse": "muse30b_x6_routes"},
               "rtc": {"9b": "qwen35_9b_x6_routes_bothoff_ctrl", "27b": "x6_routes_bothoff_ctrl_27b",
                       "122b": "qwen35_122b_x6_routes_bothoff_ctrl_g75", "muse": "muse30b_x6_routes"},
               # the layer sweep (batch 35): rts<layer>_*
               "rts8": {"9b": "qwen35_9b_x6_routes_sweep_l8"}, "rts10": {"9b": "qwen35_9b_x6_routes_sweep_l10"},
               "rts20": {"27b": "x6_routes_sweep_l20_27b"},
               "rts24": {"27b": "x6_routes_sweep_l24_27b", "122b": "qwen35_122b_x6_routes_sweep_l24_g75"},
               "rts30": {"122b": "qwen35_122b_x6_routes_sweep_l30_g75"},
               "rts36": {"122b": "qwen35_122b_x6_routes_sweep_l36_g75"},
               "rts28": {"27b": "x6_routes_sweep_l28_27b"},
               "rtk": {"9b": "qwen35_9b_x6_routes_keeponly", "27b": "x6_routes_keeponly_27b",
                       "122b": "qwen35_122b_x6_routes_keeponly_g75", "muse": "muse30b_x6_routes"},
               # D1 (batch 40): the identity direction, with the pointer and J++
               "rtd": {"9b": "qwen35_9b_x6_routes_d1", "27b": "x6_routes_d1_27b", "muse": "muse30b_x6_routes_d1_r2",
                       "122b": "qwen35_122b_x6_routes_d1_g75"}}  # fmt: skip
NATURAL_G75 = {"9b": "qwen35_9b_x5_natural_g75"}
ORDER = "org locker vs asked pick"


def f2(x: float) -> str:
    return f"{x:.2f}".replace("-", "−")


def ci(v: list[float]) -> str:
    return f"{f2(v[0])} [{f2(v[1])}, {f2(v[2])}]"


def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


class Numbers:
    def __init__(self) -> None:
        self.d: dict[str, dict[str, str]] = {}

    def add(self, key: str, text: str, source: str) -> None:
        assert key not in self.d, key
        self.d[key] = {"text": text, "source": source}


def compute() -> tuple[Numbers, dict[str, list[str]]]:
    num, tables = Numbers(), {}
    for m, (target, run, kmatch) in MODELS.items():
        r = XF.Run(run)
        src = f"results/x0_necessity/{run}/outcomes.jsonl"
        la = X.PREDICTED[target]
        rows = [x for x in r.rows if x["rendering"] == "chat"]
        cells = D.all_cells(rows, X.N_BOOT)
        lk, rc = cells[("chat", la, X.LOOKUP, *X.MAIN)], cells[("chat", la, X.RECALL, *X.MAIN)]
        num.add(f"layer_{m}", str(la), src)
        num.add(f"n_{m}", str(lk["n"]), src)
        num.add(f"ents_{m}", str(lk["entities"]), src)
        num.add(f"verdict_{m}", X.verdict(lk, rc), src)
        for w, c in (("lk", lk), ("rc", rc)):
            num.add(f"{w}_excess_{m}", ci(c["excess"]), src)
            num.add(f"{w}_jdep_{m}", f2(c["Jdep"][0]), src)
            num.add(f"{w}_rdep_{m}", f2(c["Rdep"][0]), src)
            n = c["n"]
            num.add(f"{w}_whole_{m}", str(round(c["S_whole"][0] * n)), src)
            num.add(f"{w}_swhole_pct_{m}", pct(c["S_whole"][0]), src)
            num.add(f"{w}_noj_{m}", str(round(c["S_no_part"][0] * n)), src)
            num.add(f"{w}_norand_{m}", str(round(c["S_no_rand"][0] * n)), src)
            num.add(f"{w}_dropj_{m}", f"{100 * c['drop_noD'][0]:.1f}", src)
            num.add(f"{w}_droprand_{m}", f"{100 * c['drop_noRand'][0]:.1f}", src)
        num.add(f"contrast_{m}", ci(XF.contrast(r, "chat", la)), src)
        num.add(f"jshare_{m}", f2(r.share[("chat", la, *X.MAIN)]), f"results/x0_necessity/{run}/shares.jsonl")
        # k-match: J++ at 25-200 atoms
        km = XF.Run(kmatch)
        kcells = km.cells("chat")
        for (_, l2, w, d, k, omp), c in kcells.items():
            if l2 == la and d == "jpp" and omp == "signed":
                num.add(f"{'lk' if w == X.LOOKUP else 'rc'}_excess_k{k}_{m}", f2(c["excess"][0]),
                        f"results/x0_necessity/{kmatch}/outcomes.jsonl")  # fmt: skip
                other = kcells.get(("chat", la, X.RECALL if w == X.LOOKUP else X.LOOKUP, d, k, omp))
                if w == X.LOOKUP and other:  # the gap along the curve (point estimate; the critic, 26 Oct)
                    num.add(f"contrast_k{k}_{m}", f2(other["excess"][0] - c["excess"][0]),
                            f"results/x0_necessity/{kmatch}/outcomes.jsonl")  # fmt: skip
        # sentence order (whole edit, lookups)
        cases = {c["scene"]: c for c in X.read_jsonl(r.dir / "cases.jsonl") if c["rendering"] == "chat"}
        whole = [x for x in rows if x["layer"] == la and x["reader"] == X.LOOKUP and x["arm"] == "whole"]
        for order in ("before", "after"):
            mine = [x for x in whole if ST.features(cases[x["scene"]])["org locker vs asked pick"] == order]
            k = sum(x["switched"] for x in mine)
            num.add(f"lk_order_{order}_{m}", pct(k / len(mine)), src)
            num.add(f"lk_order_{order}_{m}_k", str(k), src)
            num.add(f"lk_order_{order}_{m}_n", str(len(mine)), src)
        # upstream change
        for name, keep in (("up", lambda x: x["upstream"]), ("af", lambda x: not x["upstream"])):
            sub = X.cells_of([x for x in rows if x["layer"] == la and keep(x)])
            c = sub[("chat", la, X.LOOKUP, *X.MAIN)]
            num.add(f"lk_excess_{name}_{m}", f2(c["excess"][0]), src)
            num.add(f"lk_swhole_{name}_{m}", pct(c["S_whole"][0]), src)
            num.add(f"lk_n_{name}_{m}", str(c["n"]), src)
        # no chat template, thinking off: the gate under the first-token read (the 9B and the 27B)
        if m not in NOCHAT:
            tables[f"layers_{m}"] = table_layers(cells, r)
            tables[f"dicts_{m}"] = table_dicts(cells, r, la)
            tables[f"strata_{m}"] = table_strata(rows, cases, la)
            continue
        g = json.loads((X.RESULTS / NOCHAT[m] / "gate.json").read_text())["gate"]["nothink"]["org_accuracy"]
        num.add(f"nochat_gate_{m}", f"{100 * g['PP']:.1f}% / {100 * g['PM']:.1f}%".replace(".0%", "%"),
                f"results/x0_necessity/{NOCHAT[m]}/gate.json")  # fmt: skip
        tables[f"layers_{m}"] = table_layers(cells, r)
        tables[f"dicts_{m}"] = table_dicts(
            D.all_cells([x for x in km.rows if x["rendering"] == "chat"], X.N_BOOT), km, la
        )
        tables[f"strata_{m}"] = table_strata(rows, cases, la)
    for m, run in DIGIT.items():
        digit_numbers(num, tables, m, run)
    atoms_numbers(num)
    single_numbers(num)
    probe_numbers(num)
    address_numbers(num)
    first_mention_numbers(num)
    x0b_numbers(num)
    parts_numbers(num)
    massmean_numbers(num)
    massmean_lf_numbers(num)
    dup_nearest_numbers(num)
    same_scene_numbers(num)
    replicate_numbers(num)
    natural_numbers(num)
    routes_numbers(num)
    composition_numbers(num)
    natsplit_numbers(num)
    x4_numbers(num)
    predictions_numbers(num)
    x8_numbers(num)
    x8_order_numbers(num)
    tier0_numbers(num)
    x45c_numbers(num)
    batch45_numbers(num)
    overnight_numbers(num)
    t_pointer_numbers(num)
    first_sentence_numbers(num)
    ld_numbers(num)
    corr = json.loads(sorted((X.RESULTS / MODELS["27b"][1]).glob("descriptive-*/cells.json"))[-1].read_text())
    num.add("share_rho_27b", f2(corr["renderings"]["chat"]["correlations"][f"{X.LOOKUP} Jdep"]["spearman"]),
            f"results/x0_necessity/{MODELS['27b'][1]}/descriptive-*/cells.json")  # fmt: skip
    ctx = json.loads((pins.REPO_ROOT / CTX).read_text())["cells"]["context:32"]
    for w in ("lookup", "recall"):
        num.add(f"ctx_{w}_full", pct(ctx[w]["full"][0]), CTX)
        num.add(f"ctx_{w}_noj", pct(ctx[w]["not_jspace"][0]), CTX)
    nec = ctx["necessity"]
    num.add("ctx_recall_drop", f"{100 * nec['recall_drop_J']:.0f}", CTX)
    num.add("ctx_recall_droprand", f"{100 * nec['recall_drop_rand']:.0f}".replace("-", "−"), CTX)
    num.add("ctx_recall_diff", ci(nec["recall_dropJ_minus_droprand"]), CTX)
    num.add("ctx_n", str(nec["n_lookup"]), CTX)
    return num, tables


def digit_numbers(num: Numbers, tables: dict[str, list[str]], m: str, run: str) -> None:
    """The digit check: lookups and recalls by locker order, J++ over letters (jpp) vs every token (jppall) at
    25 / 50 / 100 atoms, and the 10 digit directions alone (jppdig); the answer-digit readout."""
    # the newest strata run that has the sentence order (a later run may hold other features only, e.g. confidence)
    path = [p for p in sorted((X.RESULTS / run).glob("strata-*/strata.json"))
            if any(s["feature"] == ORDER for s in json.loads(p.read_text())["strata"])][-1]  # fmt: skip
    src = str(path.relative_to(pins.REPO_ROOT))
    rows = [s for s in json.loads(path.read_text())["strata"] if s["feature"] == ORDER and s["omp"] == "signed"]
    out = ["| locker vs pick | reader | dictionary | atoms | n | flipped by the whole edit | excess | label |",
           "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    name = {"jpp": "J++ (letters)", "jppall": "J++ (every token)", "jppdig": "the 10 digit directions"}
    for s in sorted(rows, key=lambda s: (s["value"] != "before", s["reader"] != X.LOOKUP, s["dict"], s["k"])):
        if s["dict"] not in name:
            continue
        w = "lk" if s["reader"] == X.LOOKUP else "rc"
        num.add(f"dig_{w}_{s['dict']}_k{s['k']}_{s['value']}_{m}", f2(s["excess"][0]), src)
        out.append(f"| {s['value']} | {'lookup' if w == 'lk' else 'recall'} | {name[s['dict']]} | {s['k']} | {s['n']} | "
                   f"{s['switched_whole']} | {ci(s['excess'])} | {s['label']} |")  # fmt: skip
    tables[f"digit_{m}"] = out
    la = X.PREDICTED[MODELS[m][0]]  # the 122B's X0 run reads out at every layer; the digit runs at one
    readout = [r for r in X.read_jsonl(X.RESULTS / run / "readout.jsonl") if r["layer"] == la]
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / run / "cases.jsonl") if c["rendering"] == "chat"}
    for order in ("before", "after"):
        mine = [r for r in readout if r["reader"] == X.LOOKUP and r["run"] == "org"
                and ST.features(cases[r["scene"]])[ORDER] == order]  # fmt: skip
        num.add(f"dig_readout_first_{order}_{m}", pct(sum(r["rank_org_answer"] == 1 for r in mine) / len(mine)),
                f"results/x0_necessity/{run}/readout.jsonl")  # fmt: skip


def atoms_numbers(num: Numbers) -> None:
    """The J++ atoms of the bridge edit (27B L32, 20 random items): how often the first atom is the bridge's own
    token, and whether a digit or number word enters the top 25 when every token is allowed."""
    for v, run in ATOMS.items():
        rows = [r for r in X.read_jsonl(pins.RESULTS_DIR / "x0_atoms" / run / "atoms.jsonl") if r["subset"] == "all"]
        src = f"results/x0_atoms/{run}/atoms.jsonl"
        first = sum(r["atoms"][0]["mark"] in ("bridge_org", "bridge_alt") for r in rows)
        num.add(f"atoms_first_bridge_{v}", f"{first} of {len(rows)}", src)
        for mark in ("digit", "number_word"):
            k = sum(a["mark"] == mark for r in rows for a in r["atoms"][:25])
            num.add(f"atoms_{mark}_top25_{v}", f"{k} of {25 * len(rows)}", src)
        every = X.read_jsonl(pins.RESULTS_DIR / "x0_atoms" / run / "atoms.jsonl")  # random and asked-first items
        bridge = ("bridge_org", "bridge_alt")
        has = sum(any(a["mark"] in bridge for a in r["atoms"][:25]) for r in every)
        num.add(f"atoms_bridge_top25_{v}", f"{has} of {len(every)}", src)
        share = [sum(a["coef_k25"] ** 2 for a in r["atoms"][:25] if a["mark"] in bridge)
                 / sum(a["coef_k25"] ** 2 for a in r["atoms"][:25]) for r in every]  # fmt: skip
        num.add(f"atoms_bridge_coef2_{v}", pct(sorted(share)[len(share) // 2] if len(share) % 2
                                                else sum(sorted(share)[len(share) // 2 - 1 : len(share) // 2 + 1]) / 2), src)  # fmt: skip


def single_numbers(num: Numbers) -> None:
    """The single-change edit (only the asked pick changes; after data) at the pre-registered layer: the lookup's and
    the recall's excess at k = 25, and the lookup's at k = 100."""
    for m, run in SINGLE.items():
        r = XF.Run(run)
        la = X.PREDICTED[MODELS[m][0]]
        cells = r.cells("chat")
        src = f"results/x0_necessity/{run}/outcomes.jsonl"
        num.add(f"single_lk_excess_{m}", ci(cells[("chat", la, X.LOOKUP, *X.MAIN)]["excess"]), src)
        num.add(f"single_lk_excess_pt_{m}", f2(cells[("chat", la, X.LOOKUP, *X.MAIN)]["excess"][0]), src)
        num.add(f"single_rc_excess_{m}", ci(cells[("chat", la, X.RECALL, *X.MAIN)]["excess"]), src)
        num.add(f"single_lk_excess_k100_{m}", f2(cells[("chat", la, X.LOOKUP, "jpp", 100, "signed")]["excess"][0]), src)
        num.add(f"single_contrast_{m}", ci(XF.contrast(r, "chat", la)), src)  # C under the one-change edit
        for w in X.READERS:
            num.add(f"single_{'lk' if w == X.LOOKUP else 'rc'}_swhole_pct_{m}",
                    pct(cells[("chat", la, w, *X.MAIN)]["S_whole"][0]), src)  # fmt: skip
        found = sorted((X.RESULTS / run).glob("paired-*/paired.json"))  # single minus two-change, shared items
        if not found:  # the 122B: no paired comparison was run
            continue
        paired = found[-1]
        for w, d in json.loads(paired.read_text())["readers"].items():
            num.add(f"paired_{'lk' if w == X.LOOKUP else 'rc'}_excess_{m}", ci(d["paired_difference"]["excess"]),
                    str(paired.relative_to(pins.REPO_ROOT)))  # fmt: skip


def probe_numbers(num: Numbers) -> None:
    """The probes at the bridge's word (X0 items, locker-before; descriptive): (a) the answer digit, (b) the locker
    sentence's index with its visible-layout baseline, (c) the bridge's identity."""
    for m, run in PROBES.items():
        path = sorted((pins.RESULTS_DIR / "x0_probe" / run).glob("probe-*/probe.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        rows = {
            r["target"]: r
            for r in json.loads(path.read_text())["rows"]
            if r["subset"] == "x0" and r["stratum"] == "before"
        }
        num.add(f"probe_a_before_{m}", f2(rows["answer digit"]["probe"][0]), src)
        num.add(f"probe_a_chance_{m}", f2(rows["answer digit"]["chance"]), src)
        num.add(f"probe_b_before_{m}", f2(rows["locker sentence"]["probe"][0]), src)
        num.add(f"probe_b_layout_before_{m}", f2(rows["locker sentence"]["layout"][0]), src)
        num.add(f"probe_c_before_{m}", f2(rows["bridge identity"]["probe"][0]), src)


def massmean_numbers(num: Numbers) -> None:
    """x0_massmean: the mass-mean address (A) and value (V) subspaces removed from, or kept alone in, the single-change
    edit (items with both lockers before the pick): each reader's excess, A's share, and the kept-alone difference."""
    for m, run in MASSMEAN.items():
        path = sorted((pins.RESULTS_DIR / "x0_massmean" / run).glob("verdict-*/verdict.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        for r in json.loads(path.read_text())["rows"]:
            w = "lk" if r["reader"] == X.LOOKUP else "rc"
            for sp in ("A", "V", "AV"):
                num.add(f"mm_{sp}_{w}_excess_{m}", ci(r[sp]["excess"]), src)
            num.add(f"mm_keep_{w}_{m}", ci(r["keep"]["difference"]), src)
            if w == "lk":
                num.add(f"mm_A_share_{m}", pct(r["A"]["share"]), src)


def parts_numbers(num: Numbers) -> None:
    """x0_parts: the word part (w), J++ without the word (jw), the PCA part (pca) and J++ (jpp), each against a random
    part of its own share, on the single-change items: share of ||Δ||² and each reader's excess (parts_*: point
    estimates; pcaeq_* (PCA at J++'s share, word-orthogonal jw) and x0bparts_* (X0b's items): with CIs). Also the
    word part's energy inside jw (fit on the whole Δ): the median of ((jw · w) / ||w||²)²."""
    import numpy as np

    for runs, prefix, fmt in ((PARTS, "parts", lambda v: f2(v[0])), (PCAEQ, "pcaeq", ci), (X0BPARTS, "x0bparts", ci),
                              (JPPOTHER, "jppother", ci)):  # fmt: skip
        for m, run in runs.items():
            found = sorted((pins.RESULTS_DIR / "x0_parts" / run).glob("verdict-*/verdict.json"))
            if not found:  # queued (the 122B's X0b parts)
                continue
            path = found[-1]
            src = str(path.relative_to(pins.REPO_ROOT))
            for r in json.loads(path.read_text())["rows"]:
                w = "lk" if r["reader"] == X.LOOKUP else "rc"
                num.add(f"{prefix}_{r['part']}_{w}_excess_{m}", fmt(r["excess"]), src)
                if prefix == "pcaeq":  # the readings' bars are on the point estimate: three decimals beside the CI
                    num.add(f"{prefix}_{r['part']}_{w}_point_{m}", f"{r['excess'][0]:.3f}", src)
                if w == "lk":
                    num.add(f"{prefix}_{r['part']}_share_{m}", pct(r["median_share"]), src)
    for m, run in PARTS.items():
        path = pins.RESULTS_DIR / "x0_parts" / run / "states.npz"
        z = np.load(path)
        w, jw = (z[k].astype(np.float64) for k in ("part_w", "part_jw"))
        inside = ((w * jw).sum(1) / (w * w).sum(1)) ** 2
        num.add(f"parts_jw_wenergy_{m}", pct(float(np.median(inside))), str(path.relative_to(pins.REPO_ROOT)))


def massmean_lf_numbers(num: Numbers) -> None:
    """x0_massmean, layout-free mode: A and Alf (A after subtracting each layout group's mean) removed from, or kept
    alone in, the single-change edit: each reader's excess and kept-alone difference, Alf's share, the A-Alf overlap."""
    for m, run in MASSMEAN_LF.items():
        path = sorted((pins.RESULTS_DIR / "x0_massmean" / run).glob("verdict-*/verdict.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        v = json.loads(path.read_text())
        num.add(f"mmlf_overlap_{m}", f2(v["manifest"]["subspaces"]["A_Alf_overlap"]), src)
        for r in v["rows"]:
            w = "lk" if r["reader"] == X.LOOKUP else "rc"
            num.add(f"mmlf_n_{w}_{m}", str(r["n"]), src)
            for sp in ("A", "Alf"):
                num.add(f"mmlf_{sp}_{w}_excess_{m}", ci(r[sp]["excess"]), src)
                num.add(f"mmlf_keep_{sp}_{w}_{m}", ci(r[f"keep_{sp}"]["difference"]), src)
                if w == "lk":
                    num.add(f"mmlf_{sp}_share_{m}", pct(r[sp]["share"]), src)


def replicate_numbers(num: Numbers) -> None:
    """x0_replicate (fixed in advance): each part's extra loss per reader on fresh scenes, the rule's clauses."""
    for m, run in REPLICATE.items():
        path = sorted((pins.RESULTS_DIR / "x0_replicate" / run).glob("verdict-*/verdict.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        v = json.loads(path.read_text())
        for r in v["rows"]:
            w = "lk" if r["reader"] == X.LOOKUP else "rc"
            num.add(f"rep_{r['part']}_{w}_excess_{m}", ci(r["excess"]), src)
            if w == "lk":
                num.add(f"rep_{r['part']}_share_{m}", pct(r["median_share"]), src)
        num.add(f"rep_verdict_{m}", "holds" if v["rule"]["holds"] else "does not hold", src)
        num.add(f"rep_jpp_clause_{m}", "met" if v["rule"]["jpp_clause"] else "not met", src)
        num.add(f"rep_ptr_clause_{m}", "met" if v["rule"]["pointer_clause"] else "not met", src)
        num.add(f"rep_n_{m}", str(v["manifest"]["items"]), src)
    gate = pins.RESULTS_DIR / "x0_replicate" / "qwen35_122b_x0_replicate" / "gate.json"
    if gate.exists():  # the 122B's run fixed in advance stopped at its gate (x0_122b_b9): not tested
        acc = json.loads(gate.read_text())["gate"]["chat"]["org_accuracy"]
        num.add("rep_gate_rc_122b", f2(acc[X.RECALL]), str(gate.relative_to(pins.REPO_ROOT)))


def natural_numbers(num: Numbers) -> None:
    """x5_natural (fixed in advance): the gap and each reader's extra loss; the gate; the scenes the swap rule kept."""
    for m, run in NATURAL.items():
        root = pins.RESULTS_DIR / "x5_natural" / run
        g = json.loads((root / "gate.json").read_text())
        num.add(
            f"nat_cases_{m}",
            f"{g['counts']['cases']} of {g['counts']['scenes']}",
            str((root / "gate.json").relative_to(pins.REPO_ROOT)),
        )
        num.add(
            f"nat_gate_lk_{m}",
            f2(g["org_read_accuracy"][X.LOOKUP]),
            str((root / "gate.json").relative_to(pins.REPO_ROOT)),
        )
        found = sorted(root.glob("verdict-*/verdict.json"))
        if not found:
            continue
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        v = json.loads(found[-1].read_text())
        num.add(f"nat_gap_{m}", ci(v["main"]["gap"]), src)
        num.add(f"nat_label_{m}", v["label"], src)
        num.add(f"nat_n_{m}", str(v["main"]["n"]), src)
        for w, k in ((X.LOOKUP, "lk"), (X.RECALL, "rc")):
            num.add(f"nat_{k}_excess_{m}", ci(v["main"]["excess"][w]), src)
        whole = [r for r in X.read_jsonl(root / "outcomes.jsonl") if r["arm"] == "whole" and r["reader"] == X.LOOKUP]
        num.add(f"nat_lk_whole_sw_{m}", str(sum(r["switched"] for r in whole)),
                str((root / "outcomes.jsonl").relative_to(pins.REPO_ROOT)))  # fmt: skip
    for m, run in NATURAL_G75.items():  # the reruns after the data, gate lowered to 0.75 (descriptive; natg75_*)
        found = sorted((pins.RESULTS_DIR / "x5_natural" / run).glob("verdict-*/verdict.json"))
        if not found:
            continue
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        v = json.loads(found[-1].read_text())
        num.add(f"natg75_gap_{m}", ci(v["main"]["gap"]), src)
        num.add(f"natg75_n_{m}", str(v["main"]["n"]), src)
        for w, k in ((X.LOOKUP, "lk"), (X.RECALL, "rc")):
            num.add(f"natg75_{k}_excess_{m}", ci(v["main"]["excess"][w]), src)


def natsplit_numbers(num: Numbers) -> None:
    """x5_natural_split (B2, after the data): the 27B's natural passages by where the answer's fact sentence sits."""
    found = sorted((pins.RESULTS_DIR / "x5_natural" / NATURAL["27b"]).glob("split-*/split.json"))
    if not found:
        return
    src = str(found[-1].relative_to(pins.REPO_ROOT))
    names = {"all": "all", "after": "after", "before": "before", "both fact sentences before": "both",
             "only the original's before": "org"}  # fmt: skip
    for r in json.loads(found[-1].read_text())["rows"]:
        if r["group"] not in names or (
            r["split"] == "both fact sentences"
            and r["group"] not in ("both fact sentences before", "only the original's before")
        ):
            continue
        key = f"natsplit_{names[r['group']]}"
        num.add(f"{key}_n_27b", str(r["n"]), src)
        for w, wk in ((X.LOOKUP, "lk"), (X.RECALL, "rc")):
            num.add(f"{key}_{wk}_27b", ci(r[w]["excess"]), src)
            num.add(f"{key}_{wk}_sw_27b", str(r[w]["switched_whole"]), src)


def composition_numbers(num: Numbers) -> None:
    """x0_composition (B1, after the data): the J++ extra loss per reader by swap and sentence order, with n."""
    found = sorted((pins.RESULTS_DIR / "x0_composition").glob("*/composition.json"))
    if not found:
        return
    src = str(found[-1].relative_to(pins.REPO_ROOT))
    swaps = {
        "two people swap": "two",
        "only the asked pick": "one",
        "only the asked pick (replication, fresh scenes)": "rep",
    }
    orders = {"all": "all", "both locker sentences before the pick": "both", "only the original's before": "org",
              "the original's after": "after", "first mention: yes": "fmyes", "first mention: no": "fmno"}  # fmt: skip
    for r in json.loads(found[-1].read_text())["rows"]:
        m = {target: key for key, (target, _, _) in MODELS.items()}[r["model"]]
        key = f"comp_{swaps[r['swap']]}_{orders[r['order']]}"
        num.add(f"{key}_n_{m}", str(r["n"]), src)
        for w, wk in ((X.LOOKUP, "lk"), (X.RECALL, "rc")):
            num.add(f"{key}_{wk}_{m}", ci(r[w]["excess"]), src)
        num.add(f"{key}_gap_{m}", f2(r[X.RECALL]["excess"][0] - r[X.LOOKUP]["excess"][0]), src)  # point estimate
        # README v2 table 3c (Dan): a lookup cell whose whole change switches fewer than FEW_SWITCHES lookups is shown
        # in italics with its switch count (GitHub's Markdown has no grey)
        sw = round(r[X.LOOKUP]["S_whole"][0] * r["n"])
        num.add(f"{key}_lk_sw_{m}", str(sw), src)
        cell = ci(r[X.LOOKUP]["excess"])
        num.add(f"{key}_lk_cell_{m}", f"*{cell}; {sw} switches*" if sw < FEW_SWITCHES else cell, src)


FEW_SWITCHES = 30


def routes_numbers(num: Numbers) -> None:
    """x6_routes: the share of lookup answers per route, condition and arm; C0's switch rate (rt: the layers fixed in
    advance; rte, rtg, rtb: ROUTES_MORE); with --bothoff, each part's C0 / C2 extra loss per reader (rtb_ex_*)."""
    for prefix, runs in (("rt", ROUTES), *ROUTES_MORE.items()):
        for m, run in runs.items():
            root = pins.RESULTS_DIR / "x6_routes" / run
            found = sorted(root.glob("verdict-*/verdict.json"))
            if not found:  # queued
                continue
            v = json.loads(found[-1].read_text())
            src = str(found[-1].relative_to(pins.REPO_ROOT))
            for r in v["rows"]:
                for route in ("identity", "position", "value", "original", "recall_follows_s"):
                    num.add(f"{prefix}_{r['condition']}_{r['arm']}_{route}_{m}", ci(r["share"][route]), src)
            for e in v.get("extra", []):
                part = e["part"].replace(" - ", "_minus_")
                w = "lk" if e["reader"] == X.LOOKUP else "rc"
                num.add(f"{prefix}_ex_{e['condition']}_{part}_{w}_{m}", ci(e["excess"]), src)
                if prefix == "rtd":  # D1: the switches left without the part and without its random part; its share
                    for k, lost in (("left", e["Jdep"]), ("randleft", e["Rdep"])):
                        num.add(
                            f"rtd_{k}_{e['condition']}_{part}_{w}_{m}", ci([1 - lost[0], 1 - lost[2], 1 - lost[1]]), src
                        )
                    if w == "lk":
                        num.add(f"rtd_share_{e['condition']}_{part}_{m}", pct(e["share"]), src)
            slug = {"alf": "alf", "alf + J++": "alf_jpp", "alf + random (J++ share)": "alf_rand",
                    "alf + J++ - alf + random": "jpp_minus_rand"}  # fmt: skip
            for e in v.get("ctrl", []):  # --bothoff-ctrl: switches lost per removal (rtc_lost_*)
                w = "lk" if e["reader"] == X.LOOKUP else "rc"
                num.add(f"{prefix}_lost_{e['condition']}_{slug[e['arm']]}_{w}_{m}", ci(e["lost"]), src)
                if slug[e["arm"]] == "alf_jpp":  # the switches left with both removed, 1 - lost
                    left = [1 - e["lost"][0], 1 - e["lost"][2], 1 - e["lost"][1]]
                    num.add(f"{prefix}_left_{e['condition']}_alf_jpp_{w}_{m}", ci(left), src)
            if (root / "c0_check.json").exists():
                c0 = json.loads((root / "c0_check.json").read_text())
                num.add(
                    f"{prefix}_c0_{m}",
                    f2(c0["c0_lookup_switch"]),
                    str((root / "c0_check.json").relative_to(pins.REPO_ROOT)),
                )
    gate_path = pins.RESULTS_DIR / "x6_routes" / "qwen35_122b_x6_routes_c0" / "gate.json"
    if gate_path.exists():  # the 122B: its C0 check stopped at the gate (Q32.9 void; descriptive)
        g = json.loads(gate_path.read_text())["gate"]["C0"]
        src = str(gate_path.relative_to(pins.REPO_ROOT))
        num.add("rt_c0gate_lk_122b", f"{g['org_read_accuracy'][X.LOOKUP]:.3f}", src)
        num.add("rt_c0gate_rc_122b", f"{g['org_read_accuracy'][X.RECALL]:.3f}", src)
        num.add("rt_c0gate_eligible_122b", f"{g['eligible']} of {g['cases']}", src)


def same_scene_numbers(num: Numbers) -> None:
    """F15 (Dan, 25 Oct): J++ and the main directions at J++'s share on the pointer directions' scenes (both locker
    sentences before the pick), recomputed from x0_parts' per-scene outcomes."""
    from scripts import x0_status_pack as SPK

    for m, run in MASSMEAN_LF.items():
        scenes = {r["scene"] for r in X.read_jsonl(pins.RESULTS_DIR / "x0_massmean" / run / "outcomes.jsonl")}
        cells = SPK.same_scene_cells(PCAEQ[m], scenes)
        src = f"results/x0_parts/{PCAEQ[m]}/outcomes.jsonl (scenes of results/x0_massmean/{run})"
        for d, key in (("jpp", "jpp"), ("pca_eq", "pca")):
            for w, wk in ((X.LOOKUP, "lk"), (X.RECALL, "rc")):
                num.add(f"ss_{key}_{wk}_excess_{m}", ci(cells[(d, w)]["excess"]), src)


def dup_nearest_numbers(num: Numbers) -> None:
    """x0_dup_nearest: on the duplicate-pick pairs, where the alt state's nearest class mean in A and in Alf points
    (the alt's locker sentence or the other pick sentence), by which earlier mention of the alt item comes first."""
    for m, run in MASSMEAN_LF.items():
        path = sorted((pins.RESULTS_DIR / "x0_massmean" / run).glob("dup-nearest-*/dup_nearest.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        res = json.loads(path.read_text())["results"]
        for sp, r in res.items():
            num.add(f"dupnn_{sp}_org_{m}", ci(r["org state: org's locker sentence"]["share"]), src)
            for key in ("after", "lockerfirst", "otherfirst"):
                num.add(f"dupnn_{sp}_{key}_alt_{m}", ci(r[f"{key}: alt's locker sentence"]["share"]), src)
                num.add(f"dupnn_{sp}_{key}_other_{m}", ci(r[f"{key}: other pick sentence"]["share"]), src)
                num.add(f"dupnn_{sp}_{key}_n_{m}", str(r[f"{key}: other pick sentence"]["n"]), src)


X8 = {"9b": "qwen35_9b_x8_write", "27b": "x8_write_27b", "122b": "qwen35_122b_x8_write_g75", "muse": "muse30b_x8_write"}


def x8_numbers(num: Numbers) -> None:
    """Batch 44 (x8_write recall stage, after the data): the dose s* at which a write reaches the median norm of a real
    pointer change (min / max over the slot pairs), and the writes whose target item has the original's legs."""
    label = {"9b": "9B", "27b": "27B", "122b": "122B", "muse": "Muse"}
    for m, run in X8.items():
        found = sorted((pins.RESULTS_DIR / "x8_write" / run).glob("recall-*/recall.json"))
        if not found:  # not landed: the README's per-model list says so
            num.add(f"x8_sreal_{m}", f"{label[m]} not landed", f"results/x8_write/{run}")
            continue
        b = json.loads(found[-1].read_text())
        num.add(f"x8_sreal_{m}", f"{label[m]} {f2(min(b['s_real'].values()))} to {f2(max(b['s_real'].values()))}",
                str(found[-1].relative_to(pins.REPO_ROOT)))  # fmt: skip
        b = json.loads(found[-1].read_text())
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        num.add(f"x8_sreal_min_{m}", f2(min(b["s_real"].values())), src)
        num.add(f"x8_sreal_max_{m}", f2(max(b["s_real"].values())), src)
        num.add(f"x8_same_legs_{m}", f"{b['same_legs'][0]} of {b['same_legs'][1]}", src)
        got = b["changed_by_item"].get("write|4", {})
        num.add(f"x8_rc_target_{m}", f"{got.get('target', 0)} of {sum(got.values())}", src)
    for m, run in X8.items():  # the lookup's target share per dose, all pairs (the verdict)
        found = sorted((pins.RESULTS_DIR / "x8_write" / run).glob("verdict-*/verdict.json"))
        if not found:
            continue
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        for c in json.loads(found[-1].read_text())["cells"]:
            if c["pair"] is None:
                num.add(f"x8_{'t' if c['kind'] == 'write' else 'rand'}{c['s']:g}_{m}", ci(c["target"]), src)


# Batch 44 B (order / sentence index / distance); Muse: the rerun at the window fixed in advance (its BOS miscount fixed)
X8_ORDER = {"9b": "qwen35_9b_x8_order", "27b": "x8_order_27b", "122b": "qwen35_122b_x8_order_g75",
            "muse": "muse30b_x8_order_r2"}  # fmt: skip


def x8_order_numbers(num: Numbers) -> None:
    """Batch 44 B: per model the mean beta of B1 / B2 (the verdict) and, after the data, B1's for items in the first slot
    (j = 0, point estimate); for the README's line the models landed so far and the range of that j = 0 shift."""
    label = {"9b": "9B", "27b": "27B", "122b": "122B", "muse": "Muse"}
    landed, j0 = [], []
    for m, run in X8_ORDER.items():
        found = sorted((pins.RESULTS_DIR / "x8_write" / run).glob("verdict-*/verdict.json"))
        if not found:
            continue
        v = json.loads(found[-1].read_text())["variants"]
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        for b in ("B1", "B2"):
            num.add(f"x8_order_{b.lower()}_{m}", ci(v[b]["beta"]), src)
        rows = [r for r in X.read_jsonl(found[-1].parent.parent / "outcomes.jsonl") if r["j"] == 0 and "B1" in r]
        beta0 = sum(r["B1"]["beta"] for r in rows) / len(rows)
        num.add(f"x8_order_b1_j0_{m}", f2(beta0), src.rsplit("/", 2)[0] + "/outcomes.jsonl")
        landed.append(label[m])
        j0.append(beta0)
    src = "results/x8_write (" + ", ".join(X8_ORDER.values()) + ")"
    num.add("x8_order_models", " and ".join([", ".join(landed[:-1]), landed[-1]]) if len(landed) > 1
            else "".join(landed) or "–", src)  # fmt: skip
    num.add("x8_order_j0_range", f"{f2(min(j0))}-{f2(max(j0))}" if j0 else "–", src)


SBO_DESIGNS = {"swap": "two people swap", "one": "only the asked pick", "fresh": "fresh scenes"}


X45B_SWEEP = {"9b": "qwen35_9b_x45b_sweep_v2", "27b": "x45b_sweep_v2_27b"}
X45B_RUNS = {"9b": "qwen35_9b_x45b_binding", "27b": "x45b_binding_27b", "muse": "muse30b_x45b_binding"}
X45D = {"9b": "qwen35_9b_x45d", "27b": "x45d_27b", "muse": "muse30b_x45d"}
X45I_ROUTES = {"9b": "qwen35_9b_x6_routes_x45i_nochat", "27b": "x6_routes_x45i_nochat_27b"}
INDEP = {"9b": "qwen35_9b_x45_indep"}


def batch45_numbers(num: Numbers) -> None:
    """Batch 45's numbers for the README v5 draft (Dan 27 Oct ~00:20 / ~00:30; all UNVERIFIED):
    45m, the clean one-pick design: x45m_<before|after|all>_<lk|rc|gap|n>_<m> (results/x0_necessity/x45m-*) and the
    lookups the whole change switches, x45m_<group>_lksw_<m> (%);
    the 45b sweep on the items identical after the bridge word: x45bsw_<bw|ls|li|lv|lf>_L<layer>_<m> (the lookup's
    switch rate) and x45bsw_pass_<m>; 45b's rule on those items: x45b_sane_<pass|c|a>_<m>;
    45e: x45e_left_<idout|wrong>_<m> (the sanity swap's lookups still switching), x45e_cut_<m> (identity answers cut
    beyond the wrong pair, CI);
    45d: x45d_<prose|json|table>_<m>, the lookup's extra loss without the refit basis on the held-out half ("not
    counted" for a format with too few switches), and x45d_outcome_<m> (the rule's label);
    45i's routes run without the chat template (descriptive): x45i_value_<m>, value answers "k of n" (another item
    moved, whole change);
    45.0, the independent re-implementation: indep_agree_<m>, "k of n" items agreeing on every arm (the fewest)."""
    root = pins.RESULTS_DIR
    found = sorted((root / "x0_necessity").glob("x45m-*/x45m.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        for mod in json.loads(found[-1].read_text())["models"]:
            m = next((k for k, (t, *_) in MODELS.items() if t == mod["target"]), None)
            for grp, c in (mod.get("cells") or {}).items():
                g = grp.split("-")[-1]  # locker-before -> before
                num.add(f"x45m_{g}_n_{m}", str(c["n"]), src)
                if c.get("lookup"):
                    num.add(f"x45m_{g}_lksw_{m}", pct(c["lookup"]["S_whole"][0]), src)
                for k, cell in (("lk", c.get("lookup")), ("rc", c.get("recall"))):
                    if cell and cell.get("valid"):
                        num.add(f"x45m_{g}_{k}_{m}", ci(cell["excess"]), src)
                if c.get("gap") and c.get("lookup", {}).get("valid"):
                    num.add(f"x45m_{g}_gap_{m}", ci(c["gap"]), src)
    for m, run in X45B_SWEEP.items():
        found = [p for p in sorted((root / "x45b_binding" / run).glob("sweep-*/sweep.json"))
                 if "sanity" in json.loads(p.read_text())]  # fmt: skip
        if found:
            src = str(found[-1].relative_to(pins.REPO_ROOT))
            blob = json.loads(found[-1].read_text())
            num.add(f"x45bsw_pass_{m}", f"{blob['sanity']['pass']} of {blob['sanity']['items']}", src)
            for cell in blob["cells"][X.LOOKUP]:
                for arm in ("bw", "ls", "li", "lv", "lf"):
                    if arm in cell:
                        num.add(f"x45bsw_{arm}_L{cell['layer']}_{m}", f2(cell[arm][0]), src)
    for m, run in X45B_RUNS.items():
        found = [p for p in sorted((root / "x45b_binding" / run).glob("verdict-*/verdict.json"))
                 if json.loads(p.read_text()).get("sanity_lookup")]  # fmt: skip
        if found:
            src = str(found[-1].relative_to(pins.REPO_ROOT))
            blob = json.loads(found[-1].read_text())
            lk = blob["sanity_lookup"]
            num.add(f"x45b_sane_pass_{m}", f"{blob['sanity']['pass']} of {blob['sanity']['items']}", src)
            num.add(f"x45b_sane_c_{m}", ci(lk["of_S"]["c"]), src)
            num.add(f"x45b_sane_a_{m}", ci(lk["rate"]["a"]), src)
    found = sorted((root / "x6_routes").glob("x45a-descriptive-*/table.json"))  # 45a, after the data
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        for b in json.loads(found[-1].read_text()).values():
            m = next((k for k, (t, *_) in MODELS.items() if t == b["model"]), None)
            for v in b["routes"]["variants"]:
                num.add(f"x45a_id_{v}_{m}", f2(b["routes"]["share"][f"whole|{v}"]["identity"]), src)
            for v, bt in b["beta"].items():
                num.add(f"x45a_beta_{v}_{m}", f2(bt["beta"][0]), src)
    found = sorted((root / "x6_routes").glob("x45e-*/x45e.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        for run, f in json.loads(found[-1].read_text())["flags"].items():
            m = "9b" if run.startswith("qwen35_9b") else "muse" if run.startswith("muse") else "27b"
            if f.get("c0"):
                num.add(f"x45e_left_idout_{m}", f2(f["c0"]["left"]["no_jppalfidout"][0]), src)
                num.add(f"x45e_left_wrong_{m}", f2(f["c0"]["left"]["no_jppalfwrong"][0]), src)
            if f.get("c2"):
                num.add(f"x45e_cut_{m}", ci(f["c2"]["idout_vs_wrong"]), src)
    for m, run in X45D.items():
        found = sorted((root / "x0b_generalize" / run).glob("x45d-*/verdict.json"))
        if found:
            src = str(found[-1].relative_to(pins.REPO_ROOT))
            blob = json.loads(found[-1].read_text())
            num.add(f"x45d_outcome_{m}", blob["verdict"]["outcome"], src)
            for fmt, v in blob["lookup_refit"].items():
                num.add(f"x45d_{fmt}_{m}", ci(v) if v else "not counted", src)
    for m, run in X45I_ROUTES.items():
        found = sorted((root / "x6_routes" / run).glob("verdict-*/verdict.json"))
        if found:
            src = str(found[-1].relative_to(pins.REPO_ROOT))
            whole = json.loads(found[-1].read_text())["x45i"]["arms"]["whole"]
            num.add(f"x45i_value_{m}", f"{whole['value_count']} of {whole['n']}", src)
    for m, run in INDEP.items():
        path = root / "indep_check" / run / "summary.json"
        if path.exists():
            blob = json.loads(path.read_text())
            agree = min(a["items_agree"] for k, a in blob["arms"].items() if k != "none")  # the rule's arms
            num.add(f"indep_agree_{m}", f"{agree} of {blob['n_items']}", str(path.relative_to(pins.REPO_ROOT)))


X45C_WRITES = {"9b": "qwen35_9b_x8_write12", "27b": "x8_write12_27b", "muse": "muse30b_x8_write12"}


X45I_G75 = {"9b": "qwen35_9b_x45i_main_nochat_g75", "27b": "x45i_main_nochat_27b_g75"}


def target_key(target: str) -> str | None:
    return next((k for k, (t, *_) in MODELS.items() if t == target), None)


def overnight_numbers(num: Numbers) -> None:
    """The tests scored after the overnight queue (Dan 27 Oct ~01:05; all UNVERIFIED):
    45q (fixed in advance; results/x45b_binding/x45q-*): x45q_c_<m> (the copy at L's share of S's lookup switches),
    x45q_a_<m> (the bridge-word change at L, over the items), x45q_n_<m> (items passing the sanity check), x45q_held;
    45p (fixed in advance; results/x45p/x45p-*): x45p_d23_<m>, x45p_d24_<m> (the recall's loss_2 - loss_3 / - loss_4),
    x45p_n_<m>, x45p_held, x45p_lkmax (the largest lookup loss, any model and arm);
    45i' (after the data, gate 0.75; the no-template main test): x45ig_<gap|lk|rc>_<m>, x45ig_before_gap_<m>,
    x45ig_before_n_<m>;
    the 45e size check (results/x6_routes/x45e-size-*, matched scenes): x45em_left_<idout|wrong>_<m>, x45em_cut_<m>,
    x45em_n_<m> (C0 scenes);
    45k (results/x6_routes/x45k-*): x45k_label, x45k_c0_100_27b, x45k_d_<identity|position>_27b, x45k_other_27b,
    x45k_cos2_<U|id>_27b."""
    root = pins.RESULTS_DIR
    found = sorted((root / "x45b_binding").glob("x45q-*/x45q.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        blob = json.loads(found[-1].read_text())
        for mod in blob["models"]:
            m = target_key(mod.get("model", ""))
            if m is None or "readers" not in mod:
                continue
            lk = mod["readers"][X.LOOKUP]
            num.add(f"x45q_c_{m}", ci(lk["of_S"]["c"]), src)
            num.add(f"x45q_a_{m}", ci(lk["rate"]["a"]), src)
            num.add(f"x45q_n_{m}", str(mod["sanity"]["pass"]), src)
        v = blob["verdict"]
        num.add("x45q_held", f"{v['models_holding']} of {v['models']}", src)
    found = sorted((root / "x45p").glob("x45p-*/x45p.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        blob = json.loads(found[-1].read_text())
        lk_losses = []
        for mod in blob["models"]:
            m = target_key(mod["target"])
            if m is None or "readers" not in mod:
                continue
            rc = mod["readers"]["recall"]
            num.add(f"x45p_d23_{m}", ci(rc["diff"]["2-3"]), src)
            num.add(f"x45p_d24_{m}", ci(rc["diff"]["2-4"]), src)
            num.add(f"x45p_n_{m}", str(rc["n"]), src)
            lk_losses += [v[0] for v in mod["readers"]["lookup"]["loss"].values() if v[0] == v[0]]
        v = blob["verdict"]
        num.add("x45p_held", f"{v['models_holding']} of {v['models']}", src)
        if lk_losses:
            num.add("x45p_lkmax", f2(max(lk_losses, key=abs)), src)
    from scripts import x0_split_by_order as SO

    for m, run in X45I_G75.items():
        src_dir = X.RESULTS / run
        if not (src_dir / "outcomes.jsonl").exists():
            continue
        src = str((src_dir / "outcomes.jsonl").relative_to(pins.REPO_ROOT))
        cases = {c["scene"]: c for c in X.read_jsonl(src_dir / "cases.jsonl") if c["rendering"] == "nochat"}
        cells = SO.group_cells(X.read_jsonl(src_dir / "outcomes.jsonl"), cases, X.PREDICTED[MODELS[m][0]], X.N_BOOT,
                               "nochat")  # fmt: skip
        num.add(f"x45ig_gap_{m}", ci(cells["all"]["gap"]), src)
        num.add(f"x45ig_lk_{m}", ci(cells["all"]["lookup"]), src)
        num.add(f"x45ig_rc_{m}", ci(cells["all"]["recall"]), src)
        if "before" in cells:
            num.add(f"x45ig_before_gap_{m}", ci(cells["before"]["gap"]), src)
            num.add(f"x45ig_before_n_{m}", str(cells["before"]["n"]), src)
    found = sorted((root / "x6_routes").glob("x45e-size-*/size.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        for target, r in json.loads(found[-1].read_text())["models"].items():
            m = target_key(target)
            f = r["matched"]
            if m is None or not f.get("c0"):
                continue
            num.add(f"x45em_left_idout_{m}", f2(f["c0"]["left"]["no_jppalfidout"][0]), src)
            num.add(f"x45em_left_wrong_{m}", f2(f["c0"]["left"]["no_jppalfwrong"][0]), src)
            num.add(f"x45em_n_{m}", str(f["c0"]["n"]), src)
            if f.get("c2"):
                num.add(f"x45em_cut_{m}", ci(f["c2"]["idout_vs_wrong"]), src)
    found = sorted((root / "x6_routes").glob("x45k-*/x45k.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        blob = json.loads(found[-1].read_text())
        q = blob["q45_9"]
        num.add("x45k_label", "; ".join(q["outcome"]), src)
        flags = {blob["runs"][run]: f for run, f in blob["flags"].items()}
        f27 = flags.get("qwen3.6-27b")
        if f27:
            num.add("x45k_c0_100_27b", ci(f27["c0_loss"]["jpp100"]["excess"]), src)
            for rt in ("identity", "position"):
                num.add(f"x45k_d_{rt}_27b", ci(f27["d"][rt]), src)
            for what in ("U", "id"):
                num.add(f"x45k_cos2_{what}_27b", f2(f27["geometry"]["C2"]["jpp100"][what]["mean"]), src)
        if q.get("generic"):
            num.add("x45k_other_27b", ci(q["generic"]["jpp_other100"]), src)


def x45c_numbers(num: Numbers) -> None:
    """Batch 45c's writes (Dan 26 Oct ~22:40: descriptive, after the data, here and not in the README body): mu_k - mu_j
    written between the second and third locker at doses 1-4 x a real change, and a random direction of the same norm
    at doses 1 and 4; x45c_<write|random>_<jk>_<dose>_<m> = the share of writes whose lookup answers the written
    locker (results/x8_write/score45c-*)."""
    found = sorted((pins.RESULTS_DIR / "x8_write").glob("score45c-*/score.json"))
    if not found:
        return
    src = str(found[-1].relative_to(pins.REPO_ROOT))
    blob = json.loads(found[-1].read_text())
    for m, run in X45C_WRITES.items():
        for key, v in blob.get(run, {}).items():
            pair, kind, dose = key.split("|")
            num.add(f"x45c_{kind}_{pair.replace('-', '')}_{dose}_{m}", f2(v["target"]), src)
            if (kind, dose) == ("write", "1"):  # the same writes at every dose
                num.add(f"x45c_n_{pair.replace('-', '')}_{m}", str(v["n"]), src)


def tier0_numbers(num: Numbers) -> None:
    """The batch-45 brief's Tier 0 (Dan 26 Oct ~18:30; after the data, descriptive): T0.2 the split by sentence order
    (scripts/x0_split_by_order.py: sbo_<design>_<all|before|after>_<lk|rc|gap|lksw>_<m>); T0.3 the extra loss on p_alt
    (prob_<lk|rc|gap>_<m>); T0.4 a share of the change three ways (share_<median|mean|pooled>_<part>_<m>)."""
    found = sorted((pins.RESULTS_DIR / "x0_composition").glob("split-by-order-*/split.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        for key, v in json.loads(found[-1].read_text())["cells"].items():
            target, design = key.split("|")
            m = next(k for k, (t, *_) in MODELS.items() if t == target)
            for grp, c in v["cells"].items():
                for k, field in (("lk", "lookup"), ("rc", "recall"), ("gap", "gap")):
                    num.add(f"sbo_{design}_{grp}_{k}_{m}", ci(c[field]), src)
                num.add(f"sbo_{design}_{grp}_lksw_{m}", pct(c["lookup_switch"]), src)
                num.add(f"sbo_{design}_{grp}_n_{m}", str(c["n"]), src)
    found = sorted((pins.RESULTS_DIR / "x0_composition").glob("prob-shares-*/prob_shares.json"))
    if found:
        src = str(found[-1].relative_to(pins.REPO_ROOT))
        blob = json.loads(found[-1].read_text())
        for target, c in blob["prob"].items():
            m = next(k for k, (t, *_) in MODELS.items() if t == target)
            for k, field in (("lk", "prob_lookup"), ("rc", "prob_recall"), ("gap", "prob_gap")):
                num.add(f"prob_{k}_{m}", ci(c[field]), src)
        for key, ag in blob["shares"].items():
            target, part = key.split("|")
            m = next(k for k, (t, *_) in MODELS.items() if t == target)
            slug = {"jpp+alf+idout": "jppalfid", "jpp": "jpp"}[part]
            for agg in ("median", "mean", "pooled"):
                if ag[agg] == ag[agg]:  # not nan
                    num.add(f"share_{agg}_{slug}_{m}", pct(ag[agg]), src)


def t_pointer_numbers(num: Numbers) -> None:
    """Batch 42 (T, scripts/t_pointer.py): the lookup's extra loss without the pointer directions (fit on the simple
    scenes) in varied scenes, pooled and per format (prose / json / table), and in natural passages; every model has a
    key, "not landed" until its runs are in."""
    found = sorted((pins.RESULTS_DIR / "t_pointer").glob("verdict-*/verdict.json"))
    blob = json.loads(found[-1].read_text())["models"] if found else {}
    src = str(found[-1].relative_to(pins.REPO_ROOT)) if found else "results/t_pointer"
    for m, (target, *_) in MODELS.items():
        r = blob.get(target, {})
        varied, nat = r.get("varied"), r.get("natural")
        lk = lambda cell: cell["PP"]["excess"]  # noqa: E731
        num.add(f"tptr_pooled_{m}", ci(lk(varied["pooled"])) if varied else "not landed", src)
        num.add(f"tptr_split_{m}", " / ".join(f2(lk(varied[f])[0]) for f in ("prose", "json", "table")) if varied
                else "not landed", src)  # fmt: skip
        num.add(
            f"tptr_natural_{m}",
            "not landed" if nat is None else "not tested (gate)" if "gate" in nat else ci(lk(nat)),
            src,
        )
    # the README's scope line: the range over the models landed so far (point estimates)
    pooled = [r["varied"]["pooled"]["PP"]["excess"][0] for r in blob.values() if r.get("varied")]
    nats = [r["natural"]["PP"]["excess"][0] for r in blob.values() if r.get("natural") and "gate" not in r["natural"]]
    for key, vals in (("tptr_varied_range", pooled), ("tptr_natural_range", nats)):
        lo, hi = (f2(min(vals)), f2(max(vals))) if vals else ("–", "–")
        num.add(key, lo if lo == hi else f"{lo} to {hi}", src)


LD_NAME = {"9b": "9B", "27b": "27B", "122b": "122B", "muse": "Muse"}


def ld_numbers(num: Numbers) -> None:
    """Batch 39 (scripts/x0_logit_diff.py): the gap on the logit difference per model, and each reader's extra loss."""
    found = sorted((pins.RESULTS_DIR / "x0_logit_diff").glob("*/ld.json"))
    if not found:
        return
    b = json.loads(found[-1].read_text())["models"]
    src = str(found[-1].relative_to(pins.REPO_ROOT))
    for m, name in LD_NAME.items():
        if name in b:
            num.add(f"ld_gap_{m}", ci(b[name]["gap"]), src)
            num.add(f"ld_lk_{m}", ci(b[name]["lookup"]["extra"]), src)
            num.add(f"ld_rc_{m}", ci(b[name]["recall"]["extra"]), src)


FS_GROUPS = ("(a) first sentence", "(b) first locker, not first sentence", "(c) neither")
FS_NAMED = (  # x0_first_sentence.NAMED
    "bridge named first, in its locker sentence",
    "bridge named first, in a pick sentence",
    "another item named first",
)


def first_sentence_numbers(num: Numbers) -> None:
    """After the data (Dan 26 Oct ~16:20): the main test's pointer removal by where the bridges' locker sentences sit
    (scripts/x0_first_sentence.py), and the routes per pointer move (x8_write.py pairs): only the pointer part on the moves
    from or to slot 0 vs between slots 1 and 2, and the whole change between slots 1 and 2."""
    first = sorted((pins.RESULTS_DIR / "x0_massmean").glob("first-sentence-*/first.json"))
    pairs = sorted((pins.RESULTS_DIR / "x8_write").glob("pairs-*/pairs.json"))
    fb = json.loads(first[-1].read_text()) if first else {}
    pb = json.loads(pairs[-1].read_text()) if pairs else {}
    fsrc = str(first[-1].relative_to(pins.REPO_ROOT)) if first else ""
    psrc = str(pairs[-1].relative_to(pins.REPO_ROOT)) if pairs else ""
    for m, (target, *_) in MODELS.items():
        f = fb.get(target, {})
        if f:
            cells = [f.get(f"{X.LOOKUP}|{g}", {}) for g in FS_GROUPS]
            num.add(f"fs_groups_{m}", " / ".join(f"{f2(c['extra_loss'][0])} (n {c['n']})" if "extra_loss" in c else "–" for c in cells),
                    fsrc)  # fmt: skip
            num.add(f"fs_diff_{m}", ci(f[f"{X.LOOKUP}|(a) − (b, c)"]["extra_loss"]), fsrc)
            num.add(f"fs_keepdiff_{m}", ci(f[f"{X.LOOKUP}|(a) − (b, c)"]["keep_alf"]), fsrc)
            # Dan ~16:45 (Fig. 8a): by which item the first sentence names (the bridge in its locker sentence / the
            # bridge in a pick sentence / another item); absent in the analyses before that regrouping
            named = [f.get(f"{X.LOOKUP}|named|{g}", {}) for g in FS_NAMED]
            if any(named):
                num.add(f"fs_named_{m}", " / ".join(f2(c["extra_loss"][0]) if "extra_loss" in c else "–" for c in named),
                        fsrc)  # fmt: skip
        mv = pb.get(target, {}).get("moves", {})
        if mv:
            slot0 = [
                v["position"]["keep_alf"]
                for k, v in mv.items()
                if "0" in k.split("-") and v["position"]["keep_alf"] is not None
            ]
            num.add(f"pm_keep_slot0_{m}", f"{f2(min(slot0))} to {f2(max(slot0))}", psrc)
            num.add(f"pm_keep_12_{m}", " / ".join(f2(mv[k]["position"]["keep_alf"]) for k in ("1-2", "2-1")), psrc)
            # the two moves pooled, weighted by their items (Fig. 8b's bar)
            w = [(mv[k]["position"]["keep_alf"], mv[k]["n"]) for k in ("1-2", "2-1")]
            num.add(f"pm_keep_12w_{m}", f2(sum(v * n for v, n in w) / sum(n for _, n in w)), psrc)
            num.add(f"pm_whole_12_{m}", " / ".join(f2(mv[k]["position"]["whole"]) for k in ("1-2", "2-1")), psrc)


def predictions_numbers(num: Numbers) -> None:
    """Dan's prediction score as predictions/README.md's calibration states it (pred_brier, pred_n)."""
    path = pins.REPO_ROOT / "predictions" / "README.md"
    m = re.search(r"\((\d+) scored answers with a confidence\): mean Brier (\d\.\d+)", path.read_text())
    if m:
        num.add("pred_n", m.group(1), "predictions/README.md")
        num.add("pred_brier", m.group(2), "predictions/README.md")


def x4_numbers(num: Numbers) -> None:
    """X4: the probe within each form and as a transfer; each form's and reader's excess; D per domain (entity
    bootstrap), entities with D > 0; C on items eligible for both readers."""
    for m, (probe_run, patch_run) in X4.items():
        path = sorted((pins.RESULTS_DIR / "x4_alias" / probe_run).glob("probe-*/probe.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        p = json.loads(path.read_text())
        for form, r in p["within"].items():
            num.add(f"x4_probe_{form.replace('/', '_')}_{m}", ci(r["probe"]), src)
        for form, r in p["transfer"].items():
            num.add(f"x4_transfer_{form.split('/')[0]}_{m}", ci(r["accuracy"]), src)
        path = sorted((pins.RESULTS_DIR / "x4_alias" / patch_run).glob("verdict-*/verdict.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        v = json.loads(path.read_text())
        for key, c in v["cells"].items():
            domain, form, reader = key.split("/")
            w = "lk" if reader == X.LOOKUP else "rc"
            num.add(f"x4_{domain}_{form}_{w}_excess_{m}", ci(c["excess"]), src)
            num.add(f"x4_{domain}_{form}_{w}_n_{m}", str(c["n"]), src)
        for domain, r in v["rules"].items():
            num.add(f"x4_D_{domain}_{m}", ci(r["difference"]), src)
            num.add(f"x4_Dpos_{domain}_{m}", f"{r['entities_D_positive']} of {len(r['per_entity'])}", src)
        for form, r in v["contrast"].items():
            num.add(f"x4_C_{form.replace('/', '_')}_{m}", ci(r["C"]), src)


def x0b_numbers(num: Numbers) -> None:
    """X0b v2 (exploratory): the pooled rule at the predicted layer, the gate, the k = 100 lookup, probe (b) per format
    (locker-before), and the 27B's locker-before lookups by format (the cross stage)."""
    for m, run in X0B.items():
        root = pins.RESULTS_DIR / "x0b_generalize" / run
        path = sorted(root.glob("verdict-*/verdict.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        v = json.loads(path.read_text())
        pred = v["predicted"]
        cells = {(c["layer"], c["reader"], c["dict"], c["k"], c["omp"]): c for c in v["cells"]}
        lk, rc = cells[(pred, X.LOOKUP, *X.MAIN)], cells[(pred, X.RECALL, *X.MAIN)]
        num.add(f"x0b_verdict_{m}", v["verdict"], src)
        num.add(f"x0b_lk_excess_{m}", ci(lk["excess"]), src)
        num.add(f"x0b_rc_excess_{m}", f2(rc["excess"][0]), src)
        num.add(f"x0b_c_{m}", ci(v["contrast"][str(pred)]), src)
        num.add(f"x0b_n_{m}", f"{lk['n']:,}", src)
        num.add(f"x0b_ents_{m}", str(lk["entities"]), src)
        if (pred, X.LOOKUP, "jpp", 100, "signed") in cells:  # the 122B's run had no k-curve
            num.add(f"x0b_lk_k100_{m}", f2(cells[(pred, X.LOOKUP, "jpp", 100, "signed")]["excess"][0]), src)
        gate = json.loads((root / "gate.json").read_text())["gate"]
        num.add(
            f"x0b_cells_{m}",
            f"{sum(g['pass'] for g in gate.values())} of {len(gate)}",
            str((root / "gate.json").relative_to(pins.REPO_ROOT)),
        )
        for r in v["probe_b"]:
            if r["order"] == "before":
                num.add(f"x0b_probe_{r['format']}_{m}", f2(r["probe"][0]), src)
        cross = sorted(root.glob("cross-*/cross.json"))
        if cross:
            src_c = str(cross[-1].relative_to(pins.REPO_ROOT))
            for r in json.loads(cross[-1].read_text()):
                if r["order"] == "before" and r["reader"] == X.LOOKUP:
                    num.add(f"x0b_lk_before_{r['format']}_{m}", f2(r["excess"][0]), src_c)


def first_mention_numbers(num: Numbers) -> None:
    """The lookup's switch by the alt item's first earlier mention (x0_first_mention; single-change items, both lockers
    before the pick), with the whole edit and without the J++ part."""
    for m, run in SINGLE.items():
        path = sorted((X.RESULTS / run).glob("first-mention-*/first_mention.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        for r in json.loads(path.read_text())["rows"]:
            if r["reader"] != X.LOOKUP:
                continue
            key = "locker" if r["first"] == "locker" else "other"
            num.add(f"fm_lk_whole_{key}_{m}", f2(r["whole"][0]), src)
            num.add(f"fm_lk_noj_{key}_{m}", f2(r["without the J++ part"][0]), src)
            num.add(f"fm_n_{key}_{m}", str(r["n"]), src)


def latest_patched(run: str, target: str) -> Path:
    """The newest x0_probe_patched output of an x0_amnesic run for one target (runs before --target are the address)."""
    paths = sorted((pins.RESULTS_DIR / "x0_amnesic" / run).glob("probe-patched-*/probe_patched.json"),
                   key=lambda p: p.parent.name[-16:])  # by the UTC stamp, not the folder's name  # fmt: skip
    return [p for p in paths if json.loads(p.read_text()).get("target", "address") == target][-1]


def address_numbers(num: Numbers) -> None:
    """The address at the bridge's word (descriptive): the probes on 1,500 fresh scenes (locker-before), probe (a) with
    the locker index factored out, the probe subspace removed from or kept alone in the single-change edit (x0_amnesic),
    and probe (b) on the single-change pairs and on patched states (x0_probe_patched)."""
    for m in PROBES_V4:
        path = sorted((pins.RESULTS_DIR / "x0_probe" / PROBES_V4[m]).glob("probe-*/probe.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        rows = {(r["target"], r["stratum"]): r for r in json.loads(path.read_text())["rows"] if r["subset"] == "all"}
        num.add(f"v4_n_before_{m}", str(rows[("locker sentence", "before")]["n"]), src)
        num.add(f"v4_b_before_{m}", f2(rows[("locker sentence", "before")]["probe"][0]), src)
        num.add(f"v4_b_layout_before_{m}", f2(rows[("locker sentence", "before")]["layout"][0]), src)
        num.add(f"v4_a_before_{m}", f2(rows[("answer digit", "before")]["probe"][0]), src)
        num.add(f"v4_a_after_{m}", f2(rows[("answer digit", "after")]["probe"][0]), src)
        num.add(f"v4_b_after_{m}", f2(rows[("locker sentence", "after")]["probe"][0]), src)
        path = sorted((pins.RESULTS_DIR / "x0_probe" / PROBES_V4[m]).glob("a-given-b-*/a_given_b.json"))[-1]
        res = json.loads(path.read_text())["subsets"]["all"]
        src = str(path.relative_to(pins.REPO_ROOT))
        num.add(f"v4_a_resid_{m}", f2(res["residualised"][0]), src)
        num.add(f"v4_a_index_alone_{m}", f2(res["index_alone"][0]), src)
        path = sorted((pins.RESULTS_DIR / "x0_amnesic" / AMNESIC[m]).glob("verdict-*/verdict.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        am = {(r["order"], r["reader"]): r for r in json.loads(path.read_text())["rows"]}
        for w in X.READERS:
            num.add(f"amn_{'lk' if w == X.LOOKUP else 'rc'}_excess_{m}", ci(am[("before", w)]["excess"]), src)
        num.add(f"amn_share_{m}", pct(am[("before", X.LOOKUP)]["median_share"]).replace("1%", "1%"), src)
        num.add(f"amn_suff_lk_{m}", f2(am[("before", X.LOOKUP)]["probe_only"][0]), src)
        path = latest_patched(AMNESIC[m], "address")
        src = str(path.relative_to(pins.REPO_ROOT))
        pr = json.loads(path.read_text())["results"]
        num.add(f"pair_right_{m}", ci(pr["pair right"]), src)
        dup = pr["duplicate_pick_split"]  # which earlier mention of the alt item the readout follows
        for key, name in (("lockerfirst", "before, the other pick is the latest earlier mention"),
                          ("otherfirst", "before, the alt locker is the latest earlier mention")):  # fmt: skip
            num.add(f"dup_{key}_alt_{m}", f2(dup[name]["alt right"][0]), src)
            num.add(f"dup_{key}_reads_other_{m}", f2(dup[name]["alt state reads the other pick sentence"][0]), src)
            num.add(f"dup_{key}_n_{m}", str(dup[name]["n"]), src)
        num.add(f"dup_after_alt_{m}", f2(dup["after"]["alt right"][0]), src)
        num.add(f"pair_n_{m}", str(json.loads(path.read_text())["n"]), src)
        for k in (25, 100):
            num.add(f"patched_j{k}_alt_{m}", f2(pr[f"org + J++ part, k = {k}: reads the alt's"][0]), src)
            num.add(f"patched_rest{k}_alt_{m}", f2(pr[f"org + rest, k = {k}: reads the alt's"][0]), src)
            e = pr["energy"][f"org + J++ part, k = {k}"]
            num.add(f"patched_j{k}_share_{m}", pct(e["share_of_delta"]), src)
            num.add(f"patched_j{k}_probe_energy_{m}", f"{100 * e['share_in_probe_subspace']:.1f}%", src)


def table_layers(cells: dict, run: Any) -> list[str]:
    out = ["| layer | reader | n | S whole | S without J++ | S without random | excess | J++ share | label |",
           "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for (rr, la, w, *d), c in sorted(cells.items()):
        if tuple(d) == X.MAIN:
            share = run.share[(rr, la, *X.MAIN)]
            out.append(f"| {la} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | {f2(c['S_whole'][0])} | "
                       f"{f2(c['S_no_part'][0])} | {f2(c['S_no_rand'][0])} | {ci(c['excess'])} | {share:.3f} | {c['label']} |")  # fmt: skip
    return out


def table_dicts(cells: dict, run: Any, la: int) -> list[str]:
    out = ["| dictionary | atoms | reader | share removed | dependence | random dependence | excess | label |",
           "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    name = {"jpp": "J++", "wu": "W_U", "we": "W_E", "rand": "random lens directions", "jppall": "J++ (every token)",
            "jppdig": "the 10 digit directions"}  # fmt: skip
    order = lambda kv: (kv[0][3] != "jpp", kv[0][3], kv[0][4], kv[0][2] != X.LOOKUP)  # noqa: E731
    for (_rr, l2, w, d, k, omp), c in sorted(cells.items(), key=order):
        if l2 == la and omp == "signed":
            out.append(f"| {name[d]} | {k} | {'lookup' if w == X.LOOKUP else 'recall'} | "
                       f"{run.share[('chat', la, d, k, omp)]:.3f} | {ci(c['Jdep'])} | {ci(c['Rdep'])} | {ci(c['excess'])} | "
                       f"{c['label']} |")  # fmt: skip
    return out


def table_strata(rows: list[dict], cases: dict, la: int) -> list[str]:
    out = [
        "| split | value | reader | n | flipped by the whole edit | excess | label |",
        "|---|---|---|---|---|---|---|",
    ]
    feat = {s: ST.features(cases[s]) for s in {x["scene"] for x in rows}}
    for key in ST.FEATURES:
        for value in sorted({f[key] for f in feat.values()}):
            cells = X.cells_of([x for x in rows if x["layer"] == la and feat[x["scene"]][key] == value])
            for w in X.READERS:
                c = cells[("chat", la, w, *X.MAIN)]
                flag = " (too few)" if c["switched_whole"] < X.VALID_N else ""
                out.append(f"| {key} | {value} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | "
                           f"{c['switched_whole']}{flag} | {ci(c['excess'])} | {c['label']} |")  # fmt: skip
    return out


def render(text: str, num: Numbers, tables: dict[str, list[str]]) -> str:
    import re

    out = []
    for line in text.splitlines():
        m = re.fullmatch(r"\{\{tbl\|([\w]+)\}\}", line.strip())
        if m:
            out += tables[m.group(1)]
            continue
        out.append(re.sub(r"\{\{num\|([\w]+)\}\}", lambda x: num.d[x.group(1)]["text"], line))
    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    num, tables = compute()
    NUMBERS.write_text(json.dumps(num.d, indent=1, ensure_ascii=False) + "\n")
    page = render(TEMPLATE.read_text(), num, tables)
    (DOCS / "x0_details.md").write_text(
        "<!-- Generated by scripts/x0_details.py from docs/x0_details.template.md and the X0 runs; edit the template. -->\n"
        + page
    )
    print(NUMBERS, len(num.d), "numbers;", DOCS / "x0_details.md")


if __name__ == "__main__":
    main()
