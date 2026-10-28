"""README v2's figures (Dan, 25 Oct: one story, figures that read at a glance) into figures/story/ (SVG + PNG) and
figures/story/data.csv, in story_style's look. Fig. 0 and Fig. 3 are schematics (no data); the others read the run
files (X0 cells, verdicts) or docs/x0_numbers.json, and record every plotted number. The words on the figures:
docs/glossary.md (tests/test_readme_build.py checks them).

uv run python scripts/readme_story_figures.py                            # figures/story/, figures/supp/
uv run python scripts/readme_story_figures.py --out figures/drafts/v5    # a draft set, Fig. 8b included
"""

from __future__ import annotations

import csv
import json
import sys
import textwrap
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import story_style as S
from scripts import x0_figures as XF
from scripts import x0_necessity as X

N = S.numbers()
# Tests scored after the overnight queue (Dan 27 Oct ~01:05), drawn only once their scored result folders are named
# here (paths under results/); None = not scored yet: the figure is not drawn and its plotting is tested on fake data.
# 45q: {"verdict", "link", "sweep"} folders (x45b_binding q-verdict / q-link-table / q-sweep-table); 45p: the x45p
# verdict folder; 45i: {"9b", "27b"} the no-template main-test runs (results/x0_necessity); 45e_122b: the 122B's
# identity run (results/x6_routes)
LANDED: dict[str, Any] = {
    "45q": {"verdict": "x45b_binding/x45q-20261027T005345Z", "link": "x45b_binding/x45q-link-20261027T005346Z",
            "sweep": "x45b_binding/x45q-sweep-20261027T005346Z"},
    "45p": "x45p/x45p-20261027T012017Z",
    "45i": {"9b": "qwen35_9b_x45i_main_nochat_g75", "27b": "x45i_main_nochat_27b_g75"},
    "45e_122b": "qwen35_122b_x6_routes_d1_g75",
}  # fmt: skip


def interval(key: str) -> tuple[float, float, float]:
    """docs/x0_numbers.json's 'v [lo, hi]' for key; fails loudly where a figure would draw a missing number."""
    v = S.parse(N.get(key))
    assert v is not None, f"docs/x0_numbers.json: no interval for {key}"
    return v


MAIN_RUNS = {
    "9b": "qwen35_9b_x0_necessity",
    "27b": "x0_necessity_27b_chat",
    "122b": "qwen35_122b_x0_necessity_r2",
    "muse": "muse30b_x0_necessity",
}
# Muse's natural passages: the lookup switches in few of them, so its interval is too wide for a gap label (Dan, 26 Oct)
NO_GAP_LABEL = {("muse", "Natural passages")}
# Fig. 5's depth curve: Muse's main test at more layers (muse_depth, after the data), once it is in results/
DEPTH_RUNS = {"muse": "muse30b_x0_necessity_depth"}


def depth_run(m: str) -> str:
    run = DEPTH_RUNS.get(m)
    return run if run and (X.RESULTS / run / "outcomes.jsonl").exists() else MAIN_RUNS[m]


NEEDS = 0.30  # the lookup "still needs J++" where its extra loss is at least this (Dan's Q35.1 bar), for Fig. 5's shade


def latest(path: Path, pattern: str):
    found = sorted(path.glob(pattern))
    return json.loads(found[-1].read_text()) if found else None


def s01_split(plt) -> None:
    """Supplementary to Fig. 1: per model, the lookup's and the recall's J++ extra loss in each setting, joined; the gap printed."""
    rows = [("main test\n(two people swap picks)", "lk_excess_{m}", "rc_excess_{m}", "contrast_{m}", {}),
            ("one-pick scenes (only\nthe asked pick changes)", "single_lk_excess_{m}", "single_rc_excess_{m}",
             "single_contrast_{m}", {"9b": "after", "27b": "after"}),
            ("matched scenes\n(two people swap picks)", "comp_two_fmno_lk_{m}", "comp_two_fmno_rc_{m}", None,
             {"9b": "after", "27b": "after", "122b": "after", "muse": "after"}),
            ("matched scenes (only\nthe asked pick changes)", "comp_one_fmno_lk_{m}", "comp_one_fmno_rc_{m}",
             None, {"9b": "after", "27b": "after", "122b": "after", "muse": "after"}),
            ("varied scenes: prose /\nJSON / table", "x0b_lk_excess_{m}", "x0b_rc_excess_{m}", "x0b_c_{m}", {}),
            ("natural passages", "nat_lk_excess_{m}", "nat_rc_excess_{m}", "nat_gap_{m}", {})]  # fmt: skip
    fig, axes = plt.subplots(1, len(S.MODELS), figsize=(S.WIDTH, 6.3), sharey=True)
    fig.subplots_adjust(left=0.295, right=0.995, top=0.74, bottom=0.09, wspace=0.10)
    S.title(fig, "The split in every scene set",
            "Extra loss (0-1): switches lost without the J++ part, minus those lost without a random part\n"
            "(same size); 95% CI. Gap = recall minus lookup.")  # fmt: skip
    for ax, (target, m, name) in zip(axes, S.MODELS, strict=True):
        S.extra_axis(ax)
        ax.set_title(name, fontsize=10.5, weight="bold")
        for i, (label, lk_k, rc_k, gap_k, kinds) in enumerate(rows):
            y = -i
            lk, rc = S.parse(N.get(lk_k.format(m=m))), S.parse(N.get(rc_k.format(m=m)))
            if lk_k.startswith("x0b_"):  # varied scenes: the X0b verdict's cells
                lk, rc = x0b_cell(target, X.LOOKUP), x0b_cell(target, X.RECALL)
            natural = lk_k.startswith("nat_")
            kind = kinds.get(m, "fixed")
            if lk is None or rc is None:
                rerun = latest(pins.RESULTS_DIR / "x5_natural" / "qwen35_9b_x5_natural_g75", "verdict-*/verdict.json")
                if natural and m == "9b" and rerun:
                    lk, rc = rerun["main"]["excess"][X.LOOKUP], rerun["main"]["excess"][X.RECALL]
                    kind = "rerun"
                else:
                    ax.text(0.4, y, "not tested (gate)" if natural else "not run", ha="center", va="center",
                            fontsize=9.5, color=S.COL["muted"])  # fmt: skip
                    continue
            ax.plot([lk[0], rc[0]], [y, y], color="#cccccc", lw=2.2, zorder=1)
            S.dot(ax, 0, y, lk, S.COL["lookup"], kind)
            S.dot(ax, 0, y, rc, S.COL["recall"], kind)
            if kind == "rerun":  # the gate lowered to 0.75 after the data, as on Fig. 1b's 9B°
                ax.text(max(lk[2], rc[2]) + 0.03, y, S.LOWERED, va="center", fontsize=S.FONT)
            g = S.parse(N.get(gap_k.format(m=m))) if gap_k else None
            gap = g[0] if g and kind != "rerun" else rc[0] - lk[0]
            if (m, "Natural passages" if natural else label) not in NO_GAP_LABEL:
                ax.text(
                    (lk[0] + rc[0]) / 2,
                    y + 0.3,
                    f"gap {gap:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    color="#444444",
                )
            for w, v in ((X.LOOKUP, lk), (X.RECALL, rc)):
                S.record("s01", target, f"{label.replace(chr(10), ' ')}: {'lookup' if w == X.LOOKUP else 'recall'} extra loss",
                         *v, source=lk_k.format(m=m) if w == X.LOOKUP else rc_k.format(m=m))  # fmt: skip
            S.record(
                "s01",
                target,
                f"{label.replace(chr(10), ' ')}: gap",
                round(gap, 4),
                source=gap_k.format(m=m) if gap_k else "recall minus lookup",
            )
        ax.set_ylim(-len(rows) + 0.4, 0.7)
        ax.grid(axis="x", color="#eeeeee")
    axes[0].set_yticks([-i for i in range(len(rows))], [r[0] for r in rows])
    axes[0].tick_params(axis="y", length=0)
    hs, ls = reader_handles(plt)
    sh, sl = S.status_handles()
    legend(fig, hs + sh, ls + sl, 0.86)
    S.save(fig, "s01_split_all_scene_sets", supp=True)


def x0b_cell(target: str, reader: str):
    """X0b's pooled cell at the layer fixed in advance (its verdict's cells), as (v, lo, hi)."""
    run = {"qwen3.5-9b": "qwen35_9b_x0b_v2", "qwen3.6-27b": "x0b_v2_27b", "qwen3.5-122b-a10b": "qwen35_122b_x0b_v2",
           "muse-glimmer-30b": "muse30b_x0b_v2"}[target]  # fmt: skip
    v = latest(pins.RESULTS_DIR / "x0b_generalize" / run, "verdict-*/verdict.json")
    assert v is not None, f"no X0b verdict for {run}"
    c = next(c for c in v["cells"] if c["layer"] == X.PREDICTED[target] and c["reader"] == reader and c["dict"] == "jpp"
             and c["k"] == X.K_MAIN and c["omp"] == "signed")  # fmt: skip
    return tuple(c["excess"])


def parts_cells() -> dict[str, dict[str, dict]]:
    """Fig. 2's cells per model: part -> {lookup, recall, share, kind}; from the parts runs' verdicts and the main
    runs' X0 cells (logit lens, input embeddings, random: two people swap picks)."""
    out: dict[str, dict[str, dict]] = {}
    runs = {"9b": ("qwen35_9b_x0_pcaeq", "qwen35_9b_x0_parts", "qwen35_9b_x0_jppother"),
            "27b": ("x0_pcaeq_27b", "x0_parts_27b", "x0_jppother_27b"),
            "122b": ("qwen35_122b_x0_parts", "qwen35_122b_x0_parts", "qwen35_122b_x0_jppother"),
            "muse": ("muse30b_x0_parts", "muse30b_x0_parts", "muse30b_x0_jppother")}  # fmt: skip
    for m, (pcaeq, word, other) in runs.items():
        cells: dict[str, dict] = {}
        for run, parts in ((pcaeq, ("jpp", "jwo", "pca_eq")), (word, ("w",)), (other, ("jpp_other",))):
            v = latest(pins.RESULTS_DIR / "x0_parts" / run, "verdict-*/verdict.json")
            for r in (v or {}).get("rows", []):
                if r["part"] in parts:
                    c = cells.setdefault(r["part"], {"share": r["median_share"], "source": run})
                    c["lookup" if r["reader"] == X.LOOKUP else "recall"] = r["excess"]
        run = XF.Run(MAIN_RUNS[m])
        layer = X.PREDICTED[{k: t for t, k, _ in S.MODELS}[m]]
        allc = run.cells("chat")
        for d in ("wu", "we", "rand"):
            key = ("chat", layer, X.LOOKUP, d, X.K_MAIN, "signed")
            if key in allc:
                cells[d] = {"lookup": allc[key]["excess"], "recall": allc[("chat", layer, X.RECALL, d, X.K_MAIN, "signed")]["excess"],
                            "share": run.share.get(("chat", layer, d, X.K_MAIN, "signed")), "source": MAIN_RUNS[m]}  # fmt: skip
        out[m] = cells
    return out


def s02_parts(plt) -> None:
    """Supplementary to Fig. 2: every part tried, per model; status as in Fig. 2 (the parts runs on the one-pick scenes
    after the data, the logit-lens, input-embedding and random-atom dictionaries from the main test fixed in advance)."""
    parts = [("jpp", "J++ part"), ("jwo", "J++ part without the\nword's directions"), ("w", "the word's directions"),
             ("pca_eq", "PCA directions\n(same size)"), ("jpp_other", "J++ part fitted to\nanother scene"),
             ("wu", "logit-lens directions"), ("we", "input-embedding\ndirections"), ("rand", "random lens directions")]  # fmt: skip
    cells = parts_cells()
    fig, axes = plt.subplots(1, len(S.MODELS), figsize=(S.WIDTH, 6.4), sharey=True)
    fig.subplots_adjust(left=0.205, right=0.995, top=0.70, bottom=0.09, wspace=0.12)
    S.title(
        fig,
        "Every part we removed, against the J++ part",
        "Extra loss (0-1): switches lost without the part, minus those lost without a random part\n"
        "(same size); recall with 95% CI. The first five rows: one-pick scenes (only the asked pick\n"
        "changes); the last three: main test (two people swap picks). Random atoms: a dictionary.",
    )
    for ax, (target, m, name) in zip(axes, S.MODELS, strict=True):
        S.extra_axis(ax)
        ax.set_title(name, fontsize=10.5, weight="bold")
        for i, (p, label) in enumerate(parts):
            y = -i
            c = cells[m].get(p)
            if c is None or "recall" not in c:
                ax.text(0.4, y, "not run", ha="center", va="center", fontsize=9.5, color=S.COL["muted"])
                continue
            S.dot(ax, 0, y, c["recall"], S.COL["recall"], "fixed" if p in ("wu", "we", "rand") else "after")
            ax.plot([c["lookup"][0]], [y], "o", ms=4.5, color=S.COL["lookup"], zorder=4)
            if c["share"] is not None:
                # a white box: a recall interval reaching the right edge (Muse's J++) must not read as a minus sign
                ax.text(1.0, y, f"{100 * c['share']:.0f}%", ha="right", va="center", fontsize=9.5, color=S.COL["muted"],
                        transform=ax.get_yaxis_transform(), zorder=5,
                        bbox=dict(boxstyle="square,pad=0.45", fc="white", ec="none"))  # fmt: skip
            S.record(
                "s02", target, f"{label.replace(chr(10), ' ')}: recall extra loss", *c["recall"], source=c["source"]
            )
            S.record(
                "s02", target, f"{label.replace(chr(10), ' ')}: lookup extra loss", *c["lookup"], source=c["source"]
            )
            if c["share"] is not None:
                S.record(
                    "s02",
                    target,
                    f"{label.replace(chr(10), ' ')}: share of the change",
                    c["share"],
                    source=c["source"],
                )
        ax.set_ylim(-len(parts) + 0.4, 0.7)
        ax.grid(axis="x", color="#eeeeee")
    axes[0].set_yticks([-i for i in range(len(parts))], [p[1] for p in parts])
    axes[0].tick_params(axis="y", length=0)
    sh, sl = S.status_handles(("fixed", "after"))
    marks = [plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=7),
             plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=4.5), *sh,
             plt.Line2D([], [], ls="", marker="")]  # fmt: skip
    legend(fig, marks, ["recall", "lookup", *sl, "grey % = the part's share of the change"], 0.835)
    S.save(fig, "s02_parts_all", supp=True)


# s05's rows; each random part (same size) sits directly under its part
ARMS4 = (("whole", "whole change"), ("no_jpp", "without the J++ part"), ("no_jpp_rand", "without a random part\n(same size)"),
         ("no_alf", "without the pointer"), ("no_alf_rand", "without a random part\n(same size)"))  # fmt: skip
ROUTES = (
    ("identity", "identity"),
    ("position", "position"),
    ("value", "value"),
    ("original", "original answer"),
    ("other", "other"),
)
ROUTE_COL = {"identity": S.COL["identity"], "position": S.COL["position"], "value": S.COL["value"],
             "original": S.COL["original"], "other": S.COL["other"]}  # fmt: skip


KEEP4 = (("keep_alf", "only the pointer"), ("keep_alf_rand", "only a random part\n(same size)"),
         ("keep_jpp", "only the J++ part"), ("keep_jpp_rand", "only a random part\n(same size)"))  # fmt: skip


def s05_routes(plt) -> None:
    """Another item moved, at the layer fixed in advance: route shares per arm, the removals (x6_routes) above and each
    part added alone (x6_routes_keeponly) below; the 122B's runs after the data (gate 0.75), hatched."""
    runs = (("qwen3.5-9b", "Qwen3.5-9B", "qwen35_9b_x6_routes", "qwen35_9b_x6_routes_keeponly", "fixed"),
            ("qwen3.6-27b", "Qwen3.6-27B", "x6_routes_27b", "x6_routes_keeponly_27b", "fixed"),
            ("qwen3.5-122b-a10b", "Qwen3.5-122B", "qwen35_122b_x6_routes_g75", "qwen35_122b_x6_routes_keeponly_g75",
             "rerun"),
            ("muse-glimmer-30b", "Muse Glimmer 30B", "muse30b_x6_routes", "muse30b_x6_routes", "fixed"))  # fmt: skip
    ys = [-i for i in range(len(ARMS4))] + [-len(ARMS4) - 0.6 - i for i in range(len(KEEP4))]
    labels = [a[1] for a in ARMS4] + [a[1] for a in KEEP4]
    fig, axes = plt.subplots(1, len(runs), figsize=(S.WIDTH, 5.9), sharey=True)
    fig.subplots_adjust(left=0.28, right=0.985, top=0.77, bottom=0.09, wspace=0.22)
    S.title(fig, "Every routes arm, another item moved",
            "Routes test (another item moved): lookup answers (%). Each random part (same size) sits under\n"
            f"its part. Fixed in advance; hatched: {S.LOWERED} gate lowered to 0.75 after the data.")  # fmt: skip
    for ax, (target, name, run, keep_run, kind) in zip(axes, runs, strict=True):
        ax.set_title(name + (S.LOWERED if kind == "rerun" else ""), fontsize=10.5, weight="bold")
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1], ["0", "50", "100"])
        ax.axhline(-len(ARMS4) + 0.2, color="#bbbbbb", lw=0.8)
        for source, arms, y0 in ((run, ARMS4, ys[: len(ARMS4)]), (keep_run, KEEP4, ys[len(ARMS4) :])):
            v = latest(pins.RESULTS_DIR / "x6_routes" / source, "verdict-*/verdict.json")
            if v is None:
                ax.text(
                    0.5,
                    (y0[0] + y0[-1]) / 2,
                    "not run",
                    ha="center",
                    va="center",
                    fontsize=10,
                    color=S.COL["muted"],
                )
                continue
            rows = {(r["condition"], r["arm"]): r for r in v["rows"]}
            for y, (arm, _) in zip(y0, arms, strict=True):
                r = rows.get(("C2", arm))
                if r is None:
                    continue
                left = 0.0
                for route, _ in ROUTES:
                    sh = r["share"][route][0]
                    ax.barh(y, sh, left=left, height=0.72, color=ROUTE_COL[route], edgecolor="white", lw=0.8,
                            hatch="//" if kind == "rerun" else None)  # fmt: skip
                    if sh >= 0.15:
                        ax.text(left + sh / 2, y, f"{100 * sh:.0f}", ha="center", va="center", fontsize=9,
                                color="white" if route in ("identity", "value") else "#222222")  # fmt: skip
                    S.record("s05", target, f"another item moved, {arm}: {route} share", *r["share"][route], n=r["n"],
                             source=source)  # fmt: skip
                    left += sh
        ax.set_ylim(ys[-1] - 0.6, 0.6)
    fig.supxlabel("lookup answers (%)", x=0.63, y=0.01, fontsize=10.5)
    axes[0].set_yticks(ys, labels)
    axes[0].tick_params(axis="y", length=0)
    hs = [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL[r]) for r, _ in ROUTES[:4]]
    legend(fig, hs, [n for _, n in ROUTES[:4]], 0.865)
    S.save(fig, "s05_routes_all_arms", supp=True)


D1_RUNS = {
    "qwen3.5-9b": "qwen35_9b_x6_routes_d1",
    "qwen3.6-27b": "x6_routes_d1_27b",
    "muse-glimmer-30b": "muse30b_x6_routes_d1_r2",
}
D1_PARTS = (("d1", "alf", "the pointer"), ("both", "both", "the pointer and\nthe J++ part"),
            ("d1", "jpp+alf+idout", "the pointer, the\nJ++ part and identity\noutside J++"))  # fmt: skip


def s10_removed_together(plt) -> None:
    """Top: the sanity swap's lookup extra loss without the J++ part, without the pointer, without both (batch 34's bar
    dotted); middle: the switches lost without the pointer, with the J++ part, with a random part of the J++ part's
    size (batch 36's bar: the random union + 0.15, dotted); bottom: batch 40's parts with their share of the change. The
    recall as small grey dots."""
    runs = (("qwen3.5-9b", "9b", "Qwen3.5-9B", "qwen35_9b_x6_routes_bothoff", "qwen35_9b_x6_routes_bothoff_ctrl", "fixed"),
            ("qwen3.6-27b", "27b", "Qwen3.6-27B", "x6_routes_bothoff_27b", "x6_routes_bothoff_ctrl_27b", "fixed"),
            ("qwen3.5-122b-a10b", "122b", "Qwen3.5-122B", "qwen35_122b_x6_routes_bothoff_g75",
             "qwen35_122b_x6_routes_bothoff_ctrl_g75", "rerun"),
            ("muse-glimmer-30b", "muse", "Muse Glimmer 30B", "muse30b_x6_routes", "muse30b_x6_routes", "fixed"))  # fmt: skip
    parts = (("jpp", "without the J++ part"), ("alf", "without the pointer"),
             ("both", "without the J++ part\nand the pointer"))  # fmt: skip
    ctrl = (
        ("alf", "without the pointer"),
        ("alf + J++", "without the pointer\nand the J++ part"),
        ("alf + random (J++ share)", "without the pointer and\na random part (same size)"),
    )
    fig, axes = plt.subplots(3, len(runs), figsize=(S.WIDTH, 9.6), sharey="row",
                             gridspec_kw={"height_ratios": [1, 1, 1.4]})  # the bottom row's labels run to three lines  # fmt: skip
    fig.subplots_adjust(left=0.26, right=0.985, top=0.78, bottom=0.06, wspace=0.20, hspace=0.58)
    S.title(
        fig,
        "Removing the J++ part, the pointer and identity outside J++: the bars",
        "Sanity swap. Extra loss (0-1): switches lost without the part, minus those lost without a random\n"
        "part (same size). Dotted: bars fixed in advance (Q34 top, Q36 middle); bottom: Q40's parts with\n"
        "their share of the change.",
    )
    for j, (target, _, name, run, ctrl_run, kind) in enumerate(runs):
        top, bot = axes[0, j], axes[1, j]
        S.extra_axis(top)
        top.set_title(name + (S.LOWERED if kind == "rerun" else ""), fontsize=10.5, weight="bold")
        v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
        ex = {(x["condition"], x["reader"], x["part"]): x for x in (v or {}).get("extra", [])}
        if not ex:
            S.empty(top, "not run")
        else:
            for i, (p, label) in enumerate(parts):
                lk, rc = ex[("C0", X.LOOKUP, p)]["excess"], ex[("C0", X.RECALL, p)]["excess"]
                top.plot([rc[0]], [-i - 0.22], "o", ms=4.5, color="#9a9a9a", zorder=3)
                S.dot(top, 0, -i, lk, S.COL["lookup"], "rerun" if kind == "rerun" else "fixed")
                S.record("s10", target, f"the sanity swap, lookup extra loss {label.replace(chr(10), ' ')}", *lk,
                         source=run)  # fmt: skip
                S.record("s10", target, f"the sanity swap, recall extra loss {label.replace(chr(10), ' ')}", *rc,
                         source=run)  # fmt: skip
            bar = ex[("C0", X.LOOKUP, "alf")]["excess"][0] + 0.15
            top.plot([bar, bar], [-2.35, -1.65], color="#333333", lw=1.6, ls=":")
            S.record("s10", target, "batch 34's bar (pointer alone + 0.15)", round(bar, 4), source=run)
        top.set_ylim(-len(parts) + 0.4, 0.6)
        bot.set_xlim(0, 100)
        bot.set_xticks(*PCT)
        bot.set_xlabel("switches lost (%)")
        bot.grid(axis="x", color="#eeeeee")
        cv = latest(pins.RESULTS_DIR / "x6_routes" / ctrl_run, "verdict-*/verdict.json") if ctrl_run else None
        cc = {(x["condition"], x["reader"], x["arm"]): x for x in (cv or {}).get("ctrl", [])}
        if not cc:
            S.empty(bot, "not run")
        else:
            for i, (arm, label) in enumerate(ctrl):
                lk, rc = cc[("C0", X.LOOKUP, arm)]["lost"], cc[("C0", X.RECALL, arm)]["lost"]
                bot.plot([100 * rc[0]], [-i - 0.22], "o", ms=4.5, color="#9a9a9a", zorder=3)
                S.dot(bot, 0, -i, tuple(100 * x for x in lk), S.COL["lookup"], kind)
                S.record(
                    "s10",
                    target,
                    f"the sanity swap, lookup switches lost: {label.replace(chr(10), ' ')}",
                    *lk,
                    source=ctrl_run,
                )
                S.record(
                    "s10",
                    target,
                    f"the sanity swap, recall switches lost: {label.replace(chr(10), ' ')}",
                    *rc,
                    source=ctrl_run,
                )
            bar = cc[("C0", X.LOOKUP, "alf + random (J++ share)")]["lost"][0] + 0.15
            bot.plot([100 * bar, 100 * bar], [-1.35, -0.65], color="#333333", lw=1.6, ls=":")
            S.record("s10", target, "batch 36's bar (pointer + random + 0.15)", round(bar, 4), source=ctrl_run)
        bot.set_ylim(-len(ctrl) + 0.4, 0.6)
        # identity outside J++ (batch 40): the lookup's extra loss without the pointer, the pointer + J++ (the
        # both-removed run) and the pointer + J++ + identity outside J++, each part's median share of the change beside it
        third = axes[2, j]
        S.extra_axis(third)
        d1 = (
            latest(pins.RESULTS_DIR / "x6_routes" / D1_RUNS[target], "verdict-*/verdict.json")
            if D1_RUNS.get(target)
            else None
        )
        dx = {(x["condition"], x["reader"], x["part"]): x for x in (d1 or {}).get("extra", [])}
        if not dx:  # batch 40 covered the 9B, the 27B and Muse only
            S.empty(third, "not run")
        else:
            for i, (src, part, label) in enumerate(D1_PARTS):
                e = (dx if src == "d1" else ex).get(("C0", X.LOOKUP, part))
                if e is None:
                    continue
                S.dot(third, 0, -i, e["excess"], S.COL["lookup"], kind)
                third.text(0.98, -i, f"{100 * e['share']:.0f}%", ha="right", va="center", fontsize=9, color=S.COL["muted"],
                           transform=third.get_yaxis_transform())  # fmt: skip
                what = label.replace("\n", " ")
                S.record("s10", target, f"the sanity swap, lookup extra loss without {what}", *e["excess"],
                         source=D1_RUNS[target] if src == "d1" else run)  # fmt: skip
                S.record("s10", target, f"share of the change: {what}", round(e["share"], 4),
                         source=D1_RUNS[target] if src == "d1" else run)  # fmt: skip
        third.set_ylim(-len(D1_PARTS) + 0.4, 0.6)
    axes[0, 0].set_yticks([-i for i in range(len(parts))], [p[1] for p in parts])
    axes[1, 0].set_yticks([-i for i in range(len(ctrl))], [c[1] for c in ctrl])
    axes[2, 0].set_yticks([-i for i in range(len(D1_PARTS))], [f"without {d[2]}" for d in D1_PARTS])
    for ax in axes[:, 0]:
        ax.tick_params(axis="y", length=0)
    sh, sl = S.status_handles()
    marks = [plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=7),
             plt.Line2D([], [], marker="o", ls="", color="#9a9a9a", ms=4.5),
             plt.Line2D([], [], ls=":", color="#333333", lw=1.6), *sh]  # fmt: skip
    legend(fig, marks, ["lookup (95% CI)", "recall", "bar fixed in advance (Q34, Q36)", *sl], 0.875)
    S.save(fig, "s10_removed_together_bars", supp=True)


X8_RUNS = {
    "9b": "qwen35_9b_x8_write",
    "27b": "x8_write_27b",
    "122b": "qwen35_122b_x8_write_g75",
    "muse": "muse30b_x8_write",
}


TRANSFER_RUNS = {  # the varied-scene and natural runs with the pointer arm (T), and without it (J++ only) as fallback
    "qwen3.5-9b": (("qwen35_9b_x0b_v2_ptr", "qwen35_9b_x0b_v2"), ("qwen35_9b_x5_natural_ptr", "qwen35_9b_x5_natural_g75")),
    "qwen3.6-27b": (("x0b_v2_ptr_27b", "x0b_v2_27b"), ("x5_natural_ptr_27b", "x5_natural_27b")),
    "qwen3.5-122b-a10b": (("qwen35_122b_x0b_v2_ptr", "qwen35_122b_x0b_v2"), ("qwen35_122b_x5_natural_ptr", "qwen35_122b_x5_natural")),
    "muse-glimmer-30b": (("muse30b_x0b_v2_ptr", "muse30b_x0b_v2"), ("muse30b_x5_natural_ptr", "muse30b_x5_natural")),
}  # fmt: skip
SCENES = ("simple", "prose", "json", "table", "natural")


def transfer_cells(target: str) -> dict[tuple[str, str], tuple | None]:
    """(scenes, part) -> the lookup's extra loss (value, lo, hi): simple from docs/x0_numbers.json (J++ on the pointer
    directions' own scenes; the pointer directions there); varied per format and natural (the passages whose fact comes
    before the bridge) from the run files, J++ and the pointer on the same items when the pointer run is in."""
    from scripts import x5_natural_split as NS

    m = next(k for t, k, _ in S.MODELS if t == target)
    out: dict = {
        ("simple", "jpp"): S.parse(N.get(f"ss_jpp_lk_excess_{m}")),
        ("simple", "alf"): S.parse(N.get(f"mmlf_Alf_lk_excess_{m}")),
    }
    (x0b_ptr, x0b), (nat_ptr, nat) = TRANSFER_RUNS[target]
    for runs, kind in (((x0b_ptr, x0b), "x0b"), ((nat_ptr, nat), "x5")):
        base = pins.RESULTS_DIR / ("x0b_generalize" if kind == "x0b" else "x5_natural")
        run = next((r for r in runs if (base / r / "outcomes.jsonl").exists()), None)
        out[(kind, "gate")] = (base / runs[0]).exists() and not (base / runs[0] / "outcomes.jsonl").exists()
        out[(kind, "after")] = run is not None and run.endswith(
            "_g75"
        )  # the 9B's natural J++: gate 0.75, after the data
        if run is None:
            continue
        cases = {c["scene"]: c for c in X.read_jsonl(base / run / "cases.jsonl")}
        rows = X.read_jsonl(base / run / "outcomes.jsonl")
        if kind == "x0b":
            layer = json.loads((base / run / "manifest.json").read_text())["predicted"]
            rows = [r for r in rows if r["layer"] == layer]
        done = {r["scene"] for r in rows if r["arm"] == "whole"}
        subsets = ({f: {s for s in done if cases[s]["format"] == f} for f in ("prose", "json", "table")} if kind == "x0b"
                   else {"natural": {s for s in done if NS.placement(cases[s])["original"] == "before"}})  # fmt: skip
        for name, scenes in subsets.items():
            for part in ("jpp", "alf"):
                if part == "alf" and run != runs[0]:
                    continue  # the pointer arm only in the T runs
                cell = NS.cells(rows, scenes, X.N_BOOT, part).get(X.LOOKUP) if scenes else None
                out[(name, part)] = tuple(cell["excess"]) if cell else None
    return out


# ---------------------------------------------------------------------------------------------------------------------
# README v4 (Dan, 26 Oct ~16:45; docs/figure_plan.md): one claim per figure, in story order, figures/story/figNN_*.png.
# The 26 Oct files (fig0_setup.png ... fig11_order.png) are in figures/archive/; the detail panels go to figures/supp/.

NAMES = {m: name for _, m, name in S.MODELS}
LOWERED_M = {"122b"}  # the 122B's routes, writes and pointer runs: gate lowered to 0.75 after the data


def name_of(m: str, lowered: bool = False) -> str:
    return NAMES[m] + (S.LOWERED if lowered else "")


def legend(fig, handles, labels, y: float, ncol: int | None = None) -> None:
    """One legend under the subtitle; more than four entries wrap to rows of three (the 880 px width)."""
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.0, y), frameon=False, handletextpad=0.4,
               ncol=ncol or (len(labels) if len(labels) <= 4 else 3), columnspacing=1.2, handlelength=1.4)  # fmt: skip


PCT = ([0, 50, 100], ["0", "50", "100"])  # ticks of a share axis in % (docs/glossary.md); data.csv keeps the fractions


def reader_handles(plt) -> tuple[list, list[str]]:
    return ([plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=7),
             plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=7)], ["lookup", "recall"])  # fmt: skip


def f00_setup(plt) -> None:
    """The original prompt, the changed prompt (the swapped bridge) and the difference at the bridge word added into the
    original; the two questions about the same bridge."""
    fig = plt.figure(figsize=(S.WIDTH, 3.9))
    ax = fig.add_axes((0, 0, 1, 0.82))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 44)
    ax.axis("off")
    S.title(fig, "One prompt, two questions about the same bridge word",
            "The change: the difference at the bridge word between the two prompts, added at one layer.")  # fmt: skip
    red, w = "#b23b3b", 0.96  # w: x units per character at 11 pt
    xs = {}
    for name, y, bridge in (("original", 35, "frog"), ("changed", 21, "tick")):
        ax.text(1, y + 3.5, f"{name}\nprompt", fontsize=S.FONT, weight="bold", va="center")
        x = 13.0
        for i, s in enumerate(("The locker of the frog is 5.", "The locker of the tick is 2.", "Iris picked the ")):
            text = s + (bridge + "." if i == 2 else "")
            ww = 2.0 + w * len(text)
            ax.add_patch(plt.Rectangle((x, y), ww, 7, fc="#f5f5f5", ec="#bbbbbb", lw=1))
            ax.text(x + 1.0, y + 3.5, s, va="center", fontsize=S.FONT)
            if i == 2:
                bx = x + 1.0 + w * len(s)
                ax.text(bx, y + 3.5, bridge, va="center", fontsize=S.FONT, weight="bold", color=red,
                        bbox=dict(boxstyle="round,pad=0.15", fc="#fde3e3", ec="none"))  # fmt: skip
                ax.text(bx + w * len(bridge), y + 3.5, ".", va="center", fontsize=S.FONT)
                xs[name] = bx + w * len(bridge) / 2
            x += ww + 1.5
    ax.annotate("", (xs["original"], 34.6), (xs["changed"], 28.6),
                arrowprops=dict(arrowstyle="->", color=red, lw=1.6))  # fmt: skip
    ax.text(xs["original"] - 3, 31.6, "difference at the bridge word,\nadded into the original prompt", fontsize=S.FONT,
            color=red, ha="right", va="center")  # fmt: skip
    for y, name, q, a, col in ((12, "Lookup", "Which locker belongs to Iris's pick?", "5, read from the prompt", S.COL["lookup"]),
                               (4, "Recall", "How many legs does Iris's pick have?", "4, from memory", S.COL["recall"])):  # fmt: skip
        ax.text(1, y, f"{name}:", fontsize=S.FONT, weight="bold", color=col, va="center")
        ax.text(13, y, q, fontsize=S.FONT, va="center")
        ax.text(64, y, f"→ {a}", fontsize=S.FONT, va="center", color=col)
    S.save(fig, "fig00_setup")


# Fig. 1 and Fig. 1b (Dan's mock-ups, 26 Oct ~17:15): rows = models; Fig. 1 the main test alone with the gap and its
# interval at the right; Fig. 1b one panel per other setting. Each setting: the lookup's / recall's / gap's key.
SHORT = {"9b": "9B", "27b": "27B", "122b": "122B", "muse": "Muse"}
SETTINGS = {  # the scene sets' names as docs/glossary.md words them (a newline: where Fig. 1b's panel title wraps)
    "main": ("main test (two people swap picks)", "lk_excess_{m}", "rc_excess_{m}", "contrast_{m}"),
    "ld": ("main test (two people swap picks),\nscored on the logit difference", "ld_lk_{m}", "ld_rc_{m}", "ld_gap_{m}"),
    "single": ("one-pick scenes\n(only the asked pick changes)", "single_lk_excess_{m}", "single_rc_excess_{m}", "single_contrast_{m}"),
    # 45m (batch 45, fixed in advance): the asked pick changes to an added locker item nobody picks; locker-before cells
    "clean": ("clean one-pick scenes,\nlocker before the pick", "x45m_before_lk_{m}", "x45m_before_rc_{m}", "x45m_before_gap_{m}"),
    "varied": ("varied scenes: prose / JSON / table", "x0b_lk_excess_{m}", "x0b_rc_excess_{m}", "x0b_c_{m}"),
    "natural": ("natural passages", "nat_lk_excess_{m}", "nat_rc_excess_{m}", "nat_gap_{m}"),
}  # fmt: skip
AFTER_SETTING = {("single", "9b"), ("single", "27b")}  # one-change scenes on the 9B and 27B: after the data
GAP_BAR, LOOKUP_BAR = 0.30, 0.10  # 45m's rule (batch45.yaml): the split holds if gap >= 0.3 and lookup <= 0.10
VALID_SWITCHES = 30  # X0's validity bar: a lookup extra loss is drawn only on at least 30 switches


def blend(fig, ax):
    """x in figure fraction, y in the axes' data: text columns beside a panel's rows."""
    from matplotlib.transforms import blended_transform_factory

    return blended_transform_factory(fig.transFigure, ax.transData)


def split_cell(setting: str, target: str, m: str) -> dict:
    """lk / rc / gap as (v, lo, hi), kind (fixed / after), mark (the degree sign), src; lk None where the lookup switches
    too rarely (Muse's natural passages)."""
    _, lk_k, rc_k, gap_k = SETTINGS[setting]
    if setting == "varied":
        lk, rc = x0b_cell(target, X.LOOKUP), x0b_cell(target, X.RECALL)
    else:
        lk, rc = S.parse(N.get(lk_k.format(m=m))), S.parse(N.get(rc_k.format(m=m)))
    out = {"lk": lk, "rc": rc, "gap": S.parse(N.get(gap_k.format(m=m))), "src": lk_k.format(m=m), "mark": "",
           "kind": "after" if (setting, m) in AFTER_SETTING else "fixed"}  # fmt: skip
    if setting == "natural" and m == "9b":  # the run fixed in advance missed its gate: the rerun at 0.75
        out.update(
            {
                k: S.parse(N.get(f"natg75_{key}_9b"))
                for k, key in (("lk", "lk_excess"), ("rc", "rc_excess"), ("gap", "gap"))
            }
        )
        out.update(kind="after", mark=S.LOWERED, src="natg75_lk_excess_9b")
    if setting == "natural" and m == "muse":  # the lookup switches in 10 of 60 passages: no lookup point, no gap
        out.update(lk=None, gap=None)
    return out


def split_rows(ax, setting: str, fig_id: str, ci: bool, gap_col: bool = True) -> None:
    """One row per model: the lookup's and the recall's dots joined, the gap at the right end (bold; its interval if
    ci). gap_col False: the gap is recorded but not written (Fig. 1 writes its own columns)."""
    S.extra_axis(ax, label=False)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.5", "0.75", "1"])
    if gap_col:  # inside the panel's top band, clear of a two-line panel title
        ax.text(1.04, 0.40, "gap", transform=ax.get_yaxis_transform(), va="bottom", fontsize=S.FONT,
                color=S.COL["muted"], clip_on=False)  # fmt: skip
    what = SETTINGS[setting][0].replace("\n", " ")  # data.csv's quantity text
    labels = []
    for i, (target, m, name) in enumerate(S.MODELS):
        c = split_cell(setting, target, m)
        labels.append((name if ci else SHORT[m]) + c["mark"])
        lk, rc, y = c["lk"], c["rc"], -i
        if rc is None:
            ax.text(0.4, y, "not run", ha="center", va="center", color=S.COL["muted"])
            continue
        if lk is None:
            S.dot(ax, 0, y, rc, S.COL["recall"], c["kind"])
            n_sw, n = N.get("nat_lk_whole_sw_muse"), N.get("nat_n_muse")
            ax.text(-0.18, y, f"lookup: too few\nswitches ({n_sw} of {n})", va="center", color=S.COL["lookup"],
                    style="italic")  # fmt: skip
            if gap_col:
                ax.text(1.04, y, "–", transform=ax.get_yaxis_transform(), va="center", weight="bold", clip_on=False)
            S.record(fig_id, target, f"{what}: recall extra loss", *rc, source=c["src"])
            continue
        ax.plot([lk[0], rc[0]], [y, y], color="#d6d6d6", lw=4, zorder=1, solid_capstyle="butt")
        S.dot(ax, 0, y, lk, S.COL["lookup"], c["kind"], size=11 if ci else 9.5)
        S.dot(ax, 0, y, rc, S.COL["recall"], c["kind"], size=11 if ci else 9.5)
        gap = c["gap"] or (rc[0] - lk[0], rc[0] - lk[0], rc[0] - lk[0])
        if gap_col:
            ax.text(1.04, y, f"{gap[0]:.2f}", transform=ax.get_yaxis_transform(), va="center", fontsize=S.FONT + 2,
                    weight="bold", clip_on=False)  # fmt: skip
        if gap_col and ci:
            ax.text(1.155, y, f"[{gap[1]:.2f}, {gap[2]:.2f}]", transform=ax.get_yaxis_transform(), va="center",
                    color=S.COL["muted"], clip_on=False)  # fmt: skip
        S.record(fig_id, target, f"{what}: lookup extra loss", *lk, source=c["src"])
        S.record(fig_id, target, f"{what}: recall extra loss", *rc, source=c["src"].replace("lk", "rc"))
        S.record(fig_id, target, f"{what}: gap", *gap, source=SETTINGS[setting][3].format(m=m))
    ax.set_ylim(-len(S.MODELS) + 0.45, 0.92 if gap_col else 0.55)
    ax.set_yticks([-i for i in range(len(S.MODELS))], labels)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eeeeee")


def f01_split(plt) -> None:
    """The main test, fixed in advance on all four models: per model the lookup's and the recall's J++ extra loss; at
    the right the gap with its interval, and beside it (after the data, docs/split_by_order.md) the gap in the scenes
    whose locker sentence comes before the asked pick."""
    fig, ax = plt.subplots(figsize=(S.WIDTH, 5.0))
    fig.subplots_adjust(left=0.215, right=0.585, top=0.645, bottom=0.185)
    S.title(fig, "Recall follows the J++ part of the bridge; the lookup mostly does not",
            "Extra loss (0-1): switches lost without the J++ part, minus those lost without a random part\n"
            "(same size). 0 = the reader does not need the J++ part; 1 = every switch needs it.\n"
            "Main test (two people swap picks).")  # fmt: skip
    split_rows(ax, "main", "fig01", ci=True, gap_col=False)
    first = split_cell("main", *S.MODELS[0][:2])
    for v, name, col in ((first["lk"], "lookup", S.COL["lookup"]), (first["rc"], "recall", S.COL["recall"])):
        ax.text(v[0], 0.38, name, ha="center", va="bottom", weight="bold", color=col)
    ax.set_ylim(-4.05, 0.55)  # room for the band's label under the last row
    ax.text(-0.05, -3.68, "not needed\n(below 0.1)", ha="center", va="center", color=S.COL["muted"])
    ax.set_xlabel("extra loss without the J++ part")
    # the two gap columns: the main test's (fixed in advance) and the locker-before scenes' (after the data, open mark)
    tr, grey = blend(fig, ax), "#7a7a7a"
    x_gap, x_ci, x_mark, x_bgap, x_bci = 0.600, 0.663, 0.790, 0.803, 0.858
    ax.text(x_gap, 0.38, "gap", transform=tr, va="bottom", color=S.COL["muted"])
    ax.text(x_mark - 0.008, 0.38, "gap, locker before\nthe pick", transform=tr, va="bottom", color=S.COL["muted"])
    for i, (target, m, _) in enumerate(S.MODELS):
        g, b = interval(f"contrast_{m}"), S.parse(N.get(f"sbo_swap_before_gap_{m}"))
        ax.text(x_gap, -i, f"{g[0]:.2f}", transform=tr, va="center", fontsize=S.FONT + 2, weight="bold")
        ax.text(x_ci, -i, f"[{g[1]:.2f}, {g[2]:.2f}]", transform=tr, va="center", color=S.COL["muted"])
        if b is None:
            ax.text(x_bgap, -i, "not run", transform=tr, va="center", color=S.COL["muted"])
            continue
        ax.plot([x_mark], [-i], "o", ms=7, mfc="white", mec=grey, mew=1.6, transform=tr, clip_on=False)
        ax.text(x_bgap, -i, f"{b[0]:.2f}", transform=tr, va="center", fontsize=S.FONT + 2)
        ax.text(x_bci, -i, f"[{b[1]:.2f}, {b[2]:.2f}]", transform=tr, va="center", color=S.COL["muted"])
        S.record("fig01", target, "main test (two people swap picks), locker before the pick: gap", *b,
                 n=int(N[f"sbo_swap_before_n_{m}"]), source=f"sbo_swap_before_gap_{m}")  # fmt: skip
    sh, sl = S.status_handles(("fixed", "after"))
    legend(fig, sh, sl, 0.80)
    fig.text(0.01, 0.02, "Lines: 95% intervals, bootstrap over bridge items.", color=S.COL["muted"])
    S.save(fig, "fig01_split")


def f01b_settings(plt) -> None:
    """The same per model in the other settings: the logit difference, the clean one-pick scenes with the locker before
    the pick (45m, fixed in advance; the 9B misses the 0.3 bar), varied scenes, natural passages. The one-pick scenes
    with the duplicate pick moved to figures/supp/s01b_one_pick_duplicate."""
    fig, axes = plt.subplots(2, 2, figsize=(S.WIDTH, 7.9))
    fig.subplots_adjust(left=0.07, right=0.91, top=0.665, bottom=0.075, wspace=0.42, hspace=0.62)
    S.title(fig, "Recall follows the J++ part more than the lookup in every setting",
            "Extra loss (0-1): switches lost without the J++ part, minus those lost without a random part\n"
            "(same size). Logit difference: the share of the logit shift lost instead of switches lost.\n"
            "Clean one-pick scenes: the asked pick changes to a locker item nobody picks; the split holds\n"
            "where the gap is at least 0.3 and the lookup at most 0.1.")  # fmt: skip
    for ax, setting in zip(axes.flat, ("ld", "clean", "varied", "natural"), strict=True):
        split_rows(ax, setting, "fig01b", ci=False)
        ax.set_title(SETTINGS[setting][0], loc="left", weight="bold", fontsize=S.FONT + 0.5)
        ax.set_xlabel("extra loss (logit difference)" if setting == "ld" else "extra loss without the J++ part")
        if setting != "clean":
            continue
        for i, (_, m, _) in enumerate(S.MODELS):
            gap = S.parse(N.get(SETTINGS["clean"][3].format(m=m)))
            if gap is not None and gap[0] < GAP_BAR:
                ax.text(0.98, -i, f"gap below the\n{GAP_BAR:.1f} bar", ha="right", va="center", style="italic",
                        color=S.COL["muted"], linespacing=1.0)  # fmt: skip
    hs, ls = reader_handles(plt)
    sh, sl = S.status_handles()
    legend(fig, hs + sh, ls + sl, 0.855)
    S.save(fig, "fig01b_settings")


def s01b_one_pick(plt) -> None:
    """Supplementary to Fig. 1b: the one-pick scenes (Fig. 1b's panel until batch 45), with the duplicate check (Dan,
    26 Oct ~22:10; results/x0_necessity/duplicate-*): the new bridge is an item another person already picks."""
    dup = latest(pins.RESULTS_DIR / "x0_necessity", "duplicate-*/duplicate.json")
    assert dup is not None, "no duplicate check in results/x0_necessity"
    src = sorted((pins.RESULTS_DIR / "x0_necessity").glob("duplicate-*/duplicate.json"))[-1].relative_to(pins.REPO_ROOT)
    fig, ax = plt.subplots(figsize=(S.WIDTH, 4.9))
    fig.subplots_adjust(left=0.10, right=0.86, top=0.60, bottom=0.27)
    S.title(fig, "One-pick scenes: the new bridge is already another person's pick",
            "Extra loss (0-1): switches lost without the J++ part, minus those lost without a random part\n"
            "(same size). One-pick scenes (only the asked pick changes).")  # fmt: skip
    split_rows(ax, "single", "s01b", ci=False)
    ax.set_xlabel("extra loss without the J++ part")
    hs, ls = reader_handles(plt)
    sh, sl = S.status_handles(("fixed", "after"))
    legend(fig, hs + sh, ls + sl, 0.74, ncol=4)
    cell = next(e for e in dup["qwen3.5-9b"] if e["run"].startswith("x0_necessity/"))
    before, after = cell["cells"]["gap"]["before"], cell["cells"]["gap"]["after"]
    fig.text(0.01, 0.025, "In this design the new bridge is an item another person already picks; when that pick\n"
             "comes first, the recall needs the J++ part much less "
             f"(9B gap {before[0]:.2f} vs {after[0]:.2f}).", color=S.COL["muted"])  # fmt: skip
    for when, v in (("before", before), ("after", after)):
        S.record("s01b", "qwen3.5-9b", f"one-pick scenes, the other person's pick of the new bridge {when} the asked "
                 "pick: gap", *v, n=cell["n"][when], source=str(src))  # fmt: skip
    S.save(fig, "s01b_one_pick_duplicate", supp=True)


# Fig. 2: one panel per part, rows = models with the part's share of the change in the label; J++ and the main
# directions from the parts runs (one-change scenes, after the data), the logit lens and the random lens directions from the main
# test (fixed in advance), as in parts_cells. "rand" is a dictionary of random lens directions picked by the same OMP at its own
# (smaller) share, not the matched control (Dan ~22:40)
SPEC_PARTS = (("jpp", "J++ part"), ("pca_eq", "PCA directions (same size)"), ("wu", "logit-lens directions"),
              ("rand", "random lens directions"))  # fmt: skip


def f02_specificity(plt) -> None:
    """Per part, per model: the recall's extra loss (dot with CI) and the lookup's (small purple dot); the part's share of
    the change in the row label."""
    cells = parts_cells()
    fig, axes = plt.subplots(2, 2, figsize=(S.WIDTH, 7.5), sharex=True)
    fig.subplots_adjust(left=0.13, right=0.99, top=0.69, bottom=0.085, wspace=0.42, hspace=0.38)
    S.title(fig, "No other part of the same size costs the recall as much as the J++ part",
            "Extra loss (0-1): switches lost without the part, minus those lost without a random part\n"
            "(same size). Recall with 95% CI; % = the part's share of the change. Random atoms: a dictionary\n"
            "of random lens directions, picked by the same OMP at its own share.\n"
            "J++ part and PCA directions: one-pick scenes (only the asked pick changes).\n"
            "The other two panels: main test (two people swap picks).", limit=71)  # fmt: skip
    for ax, (p, title) in zip(axes.flat, SPEC_PARTS, strict=True):
        S.extra_axis(ax, label=ax in axes[1])
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.5", "0.75", "1"])
        ax.set_title(title, loc="left", weight="bold", fontsize=S.FONT + 0.5)
        kind = "after" if p in ("jpp", "pca_eq") else "fixed"
        labels = []
        for i, (target, m, _) in enumerate(S.MODELS):
            c = cells[m].get(p)
            if c is None or "recall" not in c:
                labels.append(SHORT[m])
                ax.text(0.4, -i, "not run", ha="center", va="center", color=S.COL["muted"])
                continue
            labels.append(f"{SHORT[m]} ({100 * c['share']:.0f}%)" if c["share"] is not None else SHORT[m])
            S.dot(ax, 0, -i, c["recall"], S.COL["recall"], kind, size=9.5)
            ax.plot([c["lookup"][0]], [-i], "o", ms=6, color=S.COL["lookup"], zorder=4)
            S.record("fig02", target, f"{title}: recall extra loss", *c["recall"], source=c["source"])
            S.record("fig02", target, f"{title}: lookup extra loss", *c["lookup"], source=c["source"])
            if c["share"] is not None:
                S.record("fig02", target, f"{title}: share of the change", c["share"], source=c["source"])
        ax.set_ylim(-len(S.MODELS) + 0.45, 0.55)
        ax.set_yticks([-i for i in range(len(S.MODELS))], labels)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#eeeeee")
    sh, sl = S.status_handles(("fixed", "after"))
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=8),
                 plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=6), *sh],
           ["recall", "lookup", *sl], 0.805)  # fmt: skip
    S.save(fig, "fig02_specificity")


# Fig. 2b (45k, Dan 27 Oct ~01:05): (a) the main test's k-curve (the k-match runs on the 9B and 27B, the main runs'
# k arms on the 122B and Muse; after the data), (b) 45k's routes runs (fixed in advance; Muse: run r4, the rerun that landed)
KCURVE_RUNS = {"9b": "qwen35_9b_x0_kmatch", "27b": "x0_kmatch_27b", "122b": "qwen35_122b_x0_necessity_r2",
               "muse": "muse30b_x0_necessity"}  # fmt: skip
X45K_RUNS = {"9b": "qwen35_9b_x6_routes_x45k", "27b": "x6_routes_x45k_27b", "muse": "muse30b_x6_routes_x45k_r4"}
KS = (25, 50, 100)
K_ARMS = (("whole", None, "whole change"), ("no_jpp", "no_jpp_rand", "without the J++ part:\n25 directions"),
          ("no_jpp50", "no_jpp50_rand", "50 directions"), ("no_jpp100", "no_jpp100_rand", "100 directions"))  # fmt: skip


def f02b_k(plt) -> None:
    """45k, the 27B's k-curve. (a) Per model, the lookup's and the recall's extra loss without the J++ part at 25, 50 and
    100 directions, main test (after the data). (b) Per model, 45k's routes test (another item moved, fixed in advance): the
    lookup's identity / position / original answers under the whole change and without the J++ part at 25 / 50 / 100
    directions (stacked, as Fig. 5), a thin grey bar under each for the identity answers without a random part (same size).
    The 100 directions' overlap with the pointer and the identity direction, and the generic-fitting control, in the
    subtitle; the title states Q45.9's scored label (results/x6_routes/x45k-*)."""
    x45k = latest(pins.RESULTS_DIR / "x6_routes", "x45k-*/x45k.json")
    assert x45k is not None, "no 45k summary in results/x6_routes"
    src_k = "results/x6_routes/" + sorted((pins.RESULTS_DIR / "x6_routes").glob("x45k-*"))[-1].name
    q = x45k["q45_9"]
    assert q["outcome"] == ["(d) can't tell"], q["outcome"]  # the title below states this label
    flags = {x45k["runs"][run]: f for run, f in x45k["flags"].items()}
    geo = {t: f["geometry"]["C2"]["jpp100"] for t, f in flags.items()}
    t27, t9 = "qwen3.6-27b", "qwen3.5-9b"
    other = q["generic"]["jpp_other100"]
    d27 = flags[t27]["d"]
    h = 10.1
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    minus = lambda v: f"{v:.2f}".replace("-", "−")  # noqa: E731
    S.title(fig, "Why a bigger J++ part costs the 27B lookup: can't tell",
            "Three causes, fixed in advance (below); none holds on the 27B. Extra loss (0-1): switches lost without\n"
            "the J++ part, minus those lost without a random part (same size).")  # fmt: skip
    fig.text(0.01, 0.1 / h, textwrap.fill(
        "(1) The lens reads identity: from 25 to 100 directions identity answers fall "
        f"{minus(d27['identity'][0])} beyond the random part, but position answers fall {minus(d27['position'][0])} too "
        "(bar: under 0.1). (2) The lens reads the pointer: the 100 directions overlap it little (mean cos² "
        f"{minus(geo[t27]['U']['mean'])}; with identity, the two items' mean difference, {minus(geo[t27]['id']['mean'])}). "
        f"(3) Any 100 directions would do: another scene's cost the 27B lookup {minus(other[0])} [{minus(other[1])}, "
        f"{minus(other[2])}] in the main test.", 108), color=S.COL["muted"], va="bottom")  # fmt: skip
    for t in (t27, t9):
        for what in ("U", "id"):
            S.record("fig02b", t, f"45k: the 100 directions' mean cos^2 with the {'pointer' if what == 'U' else 'identity direction'}"
                     " (another item moved)", geo[t][what]["mean"], n=geo[t][what]["n"], source=src_k)  # fmt: skip
        for rt in ("identity", "position"):
            S.record("fig02b", t, f"45k: {rt} answers' fall from 25 to 100 directions beyond the random part (another item "
                     "moved)", *flags[t]["d"][rt], source=src_k)  # fmt: skip
    S.record("fig02b", t27, "main test: lookup extra loss without another scene's 100 directions", *other,
             n=q["generic"]["n"][0], source=q["generic"]["generic_run"])  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(
        0.01, at(1.05), "(a) Main test, after the data: extra loss without the J++ part, by directions removed", **head
    )
    open_dot = dict(marker="o", ls="", mfc="white", mew=1.6, ms=7)
    legend(fig, [plt.Line2D([], [], mec=S.COL["lookup"], **open_dot), plt.Line2D([], [], mec=S.COL["recall"], **open_dot)],
           ["lookup", "recall"], at(1.3))  # fmt: skip
    grid_a = fig.add_gridspec(1, 4, left=0.17, right=0.985, top=at(2.1), bottom=at(3.8), wspace=0.12)
    for j, (target, m, _) in enumerate(S.MODELS):
        ax = fig.add_subplot(grid_a[0, j])
        S.extra_axis(ax)
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        run = XF.load(KCURVE_RUNS[m])
        cells = run.cells("chat") if run else {}
        la = X.PREDICTED[target]
        for i, k in enumerate(KS):
            lk, rc = (cells.get(("chat", la, w, "jpp", k, "signed")) for w in (X.LOOKUP, X.RECALL))
            if lk is None or rc is None:
                ax.text(0.4, -i, "not run", ha="center", va="center", color=S.COL["muted"])
                continue
            ax.plot([lk["excess"][0], rc["excess"][0]], [-i, -i], color="#d6d6d6", lw=3.5, zorder=1,
                    solid_capstyle="butt")  # fmt: skip
            for w, c in ((X.LOOKUP, lk), (X.RECALL, rc)):
                col = S.COL["lookup"] if w == X.LOOKUP else S.COL["recall"]
                S.dot(ax, 0, -i, tuple(c["excess"]), col, "after", size=8)
                S.record("fig02b", target, f"(a) main test, {k} directions: {'lookup' if w == X.LOOKUP else 'recall'} extra "
                         "loss", *c["excess"], n=c["n"], source=f"results/x0_necessity/{KCURVE_RUNS[m]}/outcomes.jsonl")  # fmt: skip
        ax.set_ylim(-len(KS) + 0.45, 0.55)
        ax.set_yticks([-i for i in range(len(KS))], [f"{k} directions" for k in KS] if j == 0 else [])
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#eeeeee")

    fig.text(0.01, at(4.65), "(b) Routes test (another item moved), fixed in advance: lookup answers by directions removed",
             **head)  # fmt: skip
    hs = [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL[r]) for r in ("identity", "position", "original")]
    hs.append(plt.Line2D([], [], color=S.COL["control"], lw=4))
    legend(fig, hs, ["identity", "position", "original answer", "identity: without a random part (same size)"], at(4.9),
           ncol=2)  # fmt: skip
    grid_b = fig.add_gridspec(1, 4, left=0.21, right=0.975, top=at(6.05), bottom=at(8.55), wspace=0.26)
    for j, (target, m, _) in enumerate(S.MODELS):
        ax = fig.add_subplot(grid_b[0, j])
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1], ["0", "50", "100"])
        ax.set_ylim(-len(K_ARMS) + 0.35, 0.5)
        ax.set_yticks([-i for i in range(len(K_ARMS))], [a[2] for a in K_ARMS] if j == 0 else [])
        ax.tick_params(axis="y", length=0)
        run = X45K_RUNS.get(m)
        v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json") if run else None
        sh_ = ((v or {}).get("x45k") or {}).get("shares", {}).get("C2")
        if not sh_:
            S.empty(ax, "not run")
            continue
        arms = sh_["arms"]
        for i, (arm, rand, _) in enumerate(K_ARMS):
            left = 0.0
            for route in ("identity", "position", "value", "original", "other"):
                s = arms[arm][route]
                if s[0] > 0:
                    ax.barh(-i, s[0], left=left, height=0.56, color=ROUTE_COL[route], edgecolor="white", lw=0.8)
                if route in ("identity", "position") and s[0] >= 0.13:
                    ax.text(left + s[0] / 2, -i, f"{100 * s[0]:.0f}", ha="center", va="center", fontsize=S.FONT,
                            color="white" if route == "identity" else "#222222")  # fmt: skip
                S.record(
                    "fig02b", target, f"(b) another item moved, {arm}: {route} share", *s, n=sh_["n"], source=str(run)
                )
                left += s[0]
            if rand:
                r_id = arms[rand]["identity"]
                ax.barh(-i - 0.40, r_id[0], height=0.12, color=S.COL["control"], lw=0)
                S.record("fig02b", target, f"(b) another item moved, {rand}: identity share", *r_id, n=sh_["n"],
                         source=str(run))  # fmt: skip
    fig.text(0.6, at(8.95), "lookup answers (%)", ha="center", va="center")
    S.save(fig, "fig02b_k_curve")


ORDER_TESTS = (("main test (two people swap picks)", "main", "after"), ("clean one-pick scenes", "clean", "fixed"))


def order_cells() -> dict[tuple[str, str, str], dict]:
    """Fig. 3b's cells: (test, model key, before / after) -> {lookup, recall: (v, lo, hi), switches, n, src}; the main
    test from the split by sentence order (results/x0_composition/split-by-order-*, after the data), the clean one-pick
    scenes from 45m (results/x0_necessity/x45m-*, fixed in advance); the lookup's switch count from the same file."""
    root = pins.RESULTS_DIR
    split_path = sorted((root / "x0_composition").glob("split-by-order-*/split.json"))[-1]
    clean_path = sorted((root / "x0_necessity").glob("x45m-*/x45m.json"))[-1]
    out: dict[tuple[str, str, str], dict] = {}
    for key, v in json.loads(split_path.read_text())["cells"].items():
        target, design = key.split("|")
        if design != "swap":
            continue
        m = next(k for t, k, _ in S.MODELS if t == target)
        for order in ("before", "after"):
            c = v["cells"][order]
            k = c["lookup_switch"] * c["n"]
            assert abs(k - round(k)) < 1e-6, (key, order, k)  # a share of n items: an integer count
            out[("main", m, order)] = {"lookup": tuple(c["lookup"]), "recall": tuple(c["recall"]), "switches": round(k),
                                       "n": c["n"], "src": str(split_path.relative_to(pins.REPO_ROOT))}  # fmt: skip
    for mod in json.loads(clean_path.read_text())["models"]:
        m = next(k for t, k, _ in S.MODELS if t == mod["target"])
        for order in ("before", "after"):
            c = mod["cells"][f"locker-{order}"]
            out[("clean", m, order)] = {"lookup": tuple(c["lookup"]["excess"]), "recall": tuple(c["recall"]["excess"]),
                                        "switches": c["lookup"]["switched_whole"], "n": c["n"],
                                        "src": str(clean_path.relative_to(pins.REPO_ROOT))}  # fmt: skip
    return out


def f03_order(plt) -> None:
    """(a) After the data: the lookups (open purple bars, 95% Wilson) and the recalls (grey dots) the whole change
    switches in the main test, the original bridge's locker sentence before vs after the asked person's pick sentence.
    (b) The recall's (and the lookup's, where it has at least 30 switches) extra loss without the J++ part, locker before
    vs after the pick: the main test (after the data) and the clean one-pick scenes (45m, fixed in advance)."""
    from bridge_jspace.stats import wilson
    from scripts import x0_strata as ST

    h = 10.25
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    a_top, a_bot = 1.95, 4.15
    ax = fig.add_axes((0.09, at(a_bot), 0.895, at(a_top) - at(a_bot)))
    S.title(fig, "Lookups follow the change mostly when the locker sentence comes first",
            "Main test (two people swap picks) unless marked. Extra loss (0-1): switches lost without the\n"
            "J++ part, minus those lost without a random part (same size).")  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(0.01, at(1.05), "(a) Lookups the whole change switches (%), with 95% intervals; after the data", **head)
    xs, labels = [], []
    for i, (target, m, name) in enumerate(S.MODELS):
        run, la = MAIN_RUNS[m], X.PREDICTED[target]
        rows = [x for x in XF.Run(run).rows if x["rendering"] == "chat" and x["layer"] == la and x["arm"] == "whole"]
        cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / run / "cases.jsonl") if c["rendering"] == "chat"}
        for j, order in enumerate(("before", "after")):
            mine = [x for x in rows if ST.features(cases[x["scene"]])["org locker vs asked pick"] == order]
            src = f"results/x0_necessity/{run}/outcomes.jsonl"
            x = i * 3.6 + j * 1.3
            for w in (X.LOOKUP, X.RECALL):
                got = [r["switched"] for r in mine if r["reader"] == w]
                k, n = sum(got), len(got)
                p, lo, hi = (100 * t for t in wilson(k, n))
                if w == X.LOOKUP:
                    ax.bar(x, p, width=0.72, fc="white", ec=S.COL["lookup"], lw=2)
                    ax.errorbar(x, p, yerr=[[p - lo], [hi - p]], color="#333333", capsize=3, lw=1)
                    ax.text(x, hi + 2, f"{p:.0f}%", ha="center", va="bottom", fontsize=S.FONT, weight="bold")
                else:
                    ax.plot([x + 0.62], [p], "o", ms=6, color=S.COL["recall"], zorder=3)
                what = "lookups" if w == X.LOOKUP else "recalls"
                S.record("fig03", target, f"{what} switched by the whole change, locker sentence {order} the pick",
                         round(p / 100, 4), round(lo / 100, 4), round(hi / 100, 4), n, source=src)  # fmt: skip
            xs.append(x)
            labels.append(f"locker\n{order}\nthe pick")
        # the model's name under the three-line tick labels, 0.7 in below the axis
        ax.text(i * 3.6 + 0.65, -0.70 / (a_bot - a_top), name, transform=ax.get_xaxis_transform(), ha="center",
                va="top", fontsize=S.FONT, weight="bold")  # fmt: skip
    ax.set_xticks(xs, labels)
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 112)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel("lookups switched (%)")
    ax.grid(axis="y", color="#eeeeee")
    ax.set_axisbelow(True)
    legend(fig, [plt.Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["lookup"], lw=2),
                 plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=6)],
           ["lookup", "recall"], at(1.3))  # fmt: skip

    # (b) rows: a heading per test, then its models; two panels, locker before / after the pick
    fig.text(0.01, at(5.55), "(b) Extra loss without the J++ part, locker before vs after the pick", **head)
    sh, sl = S.status_handles(("fixed", "after"))
    hs, ls = reader_handles(plt)
    legend(fig, hs + sh, ls + sl, at(5.85), ncol=4)
    cells = order_cells()
    ys: list[tuple[str, str, str, float]] = []  # (test, model key, label, y)
    y = 0.0
    for name, test, _ in ORDER_TESTS:
        ys.append((test, "", name, y))
        y -= 0.95
        for _, m, _ in S.MODELS:
            ys.append((test, m, SHORT[m], y))
            y -= 0.9
        y -= 0.25
    b_top, b_bot = 6.55, 9.7
    panels = ((0.205, "before"), (0.530, "after"))
    for x0, order in panels:
        bx = fig.add_axes((x0, at(b_bot), 0.27, at(b_top) - at(b_bot)))
        S.extra_axis(bx, label=False)
        bx.set_title(f"locker {order} the pick", fontsize=S.FONT, weight="bold")
        bx.set_xlabel("extra loss without the J++ part")
        bx.grid(axis="x", color="#eeeeee")
        too_few = []
        for test, m, _label, yy in ys:
            if not m:
                continue
            target = next(t for t, k, _ in S.MODELS if k == m)
            kind = next(k for _, t, k in ORDER_TESTS if t == test)
            c = cells.get((test, m, order))
            what = f"(b) {next(n for n, t, _ in ORDER_TESTS if t == test)}, locker {order} the pick"
            if c is None:
                bx.text(0.4, yy, "not run", ha="center", va="center", color=S.COL["muted"])
                continue
            S.record("fig03", target, f"{what}: recall extra loss", *c["recall"], n=c["n"], source=c["src"])
            S.record("fig03", target, f"{what}: lookup switches", c["switches"], n=c["n"], source=c["src"])
            S.dot(bx, 0, yy, c["recall"], S.COL["recall"], kind, size=9)
            if c["switches"] >= VALID_SWITCHES:
                bx.plot([c["lookup"][0], c["recall"][0]], [yy, yy], color="#d6d6d6", lw=3.5, zorder=1,
                        solid_capstyle="butt")  # fmt: skip
                S.dot(bx, 0, yy, c["lookup"], S.COL["lookup"], kind, size=9)
                S.record("fig03", target, f"{what}: lookup extra loss", *c["lookup"], n=c["n"], source=c["src"])
            else:
                too_few.append((yy, c))
        if too_few:  # the lookup's counts at the panel's right: too few switches (k of n)
            tr = blend(fig, bx)
            bx.text(0.82, ys[0][3] + 0.1, "lookup: too few\nswitches (k of n)", transform=tr, va="center",
                    color=S.COL["lookup"], linespacing=1.0)  # fmt: skip
            for yy, c in too_few:
                bx.text(0.82, yy, f"{c['switches']} of {c['n']}", transform=tr, va="center", color=S.COL["lookup"],
                        style="italic")  # fmt: skip
        bx.set_ylim(ys[-1][3] - 0.55, ys[0][3] + 0.55)
        rows = [(yy, label) for _, m, label, yy in ys if m]
        bx.set_yticks([yy for yy, _ in rows], [label for _, label in rows] if order == "before" else [])
        bx.tick_params(axis="y", length=0)
        if order == "before":
            for _, m, label, yy in ys:  # the tests' headings in the left margin, wrapped to fit it
                if not m:
                    bx.text(0.01, yy, textwrap.fill(label, 18), transform=blend(fig, bx), fontsize=S.FONT,
                            weight="bold", va="center", linespacing=1.0)  # fmt: skip
    S.save(fig, "fig03_order")


SWEEP_RUNS = {"9b": "qwen35_9b_x45b_sweep_v2", "27b": "x45b_sweep_v2_27b"}  # 45b's layer sweep (after the data)
# the sweep's arms: the bridge-word change; the changed prompt's states copied into the original prompt at every token of
# the locker sentences (ls) or only at the item's tokens in them (li); number (lv) and period (lf) only, drawn as one line
SWEEP_ARMS = (("bw", "the bridge-word change", "#222222", "-", "o"),
              ("ls", "copy at the locker sentences: every token", S.COL["lookup"], "-", "o"),
              ("li", "copy at the locker sentences: the item's tokens only", S.COL["lookup"], "--", "s"))  # fmt: skip


def sweep_of(m: str) -> tuple[dict, Path]:
    """The newest 45b sweep of a model that has the sanity filter (the items identical after the bridge word)."""
    root = pins.RESULTS_DIR / "x45b_binding" / SWEEP_RUNS[m]
    found = [p for p in sorted(root.glob("sweep-*/sweep.json")) if "sanity" in json.loads(p.read_text())]
    return json.loads(found[-1].read_text()), found[-1]


def f03b_layers(plt, supp: bool = False) -> None:
    """After the data (45b's sweep, results/x45b_binding/*sweep_v2*): locker-after scenes on the items identical after the
    bridge word, 9B and 27B: the lookup's switch rate by layer for the bridge-word change and for the changed prompt's
    states copied into the original prompt at the locker sentences (every token / the item's tokens only); the number and
    the period alone (0 at every layer) as one flat line; a vertical line at the layer fixed in advance."""
    fig_id = "s03b" if supp else "fig03b"  # supp: the 35-item version once 45q is Fig. 3b (Dan ~01:05)
    blobs = {m: sweep_of(m) for m in SWEEP_RUNS}
    ns = {m: b["sanity"]["pass"] for m, (b, _) in blobs.items()}
    fig, axes = plt.subplots(1, len(SWEEP_RUNS), figsize=(S.WIDTH, 5.3), sharey=True)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.60, bottom=0.12, wspace=0.10)
    S.title(fig, "Locker after the pick: what moves the lookup at each layer",
            "Locker after the pick; only the items identical after the bridge word (n = "
            f"{ns['9b']} on the 9B, {ns['27b']} on\nthe 27B). Lookups switched (%), 95% intervals; after the data. "
            "Copy: the changed prompt's\nstates put into the original prompt at the locker sentences, at that layer.")  # fmt: skip
    flat = "#9a9a9a"
    for ax, (m, (blob, path)) in zip(axes, blobs.items(), strict=True):
        target = next(t for t, k, _ in S.MODELS if k == m)
        src = str(path.relative_to(pins.REPO_ROOT))
        cells = sorted(blob["cells"][X.LOOKUP], key=lambda c: c["layer"])
        layers = [c["layer"] for c in cells]
        for arm, label, col, ls, mk in SWEEP_ARMS:
            ax.plot(layers, [100 * c[arm][0] for c in cells], color=col, ls=ls, lw=1.8, zorder=2)
            for c in cells:
                v = c[arm]
                ax.plot([c["layer"]] * 2, [100 * v[1], 100 * v[2]], color=col, lw=1.2, alpha=0.8, zorder=2)
                ax.plot([c["layer"]], [100 * v[0]], mk, ms=7, mfc="white", mec=col, mew=1.6, zorder=3)
                S.record(fig_id, target, f"layer {c['layer']}: {label} (lookups switched)", *v, n=c["n"], source=src)
        for c in cells:  # the number and the period alone: one line, drawn only while both are flat at 0
            assert c["lv"] == c["lf"] == [0.0, 0.0, 0.0], (m, c["layer"], c["lv"], c["lf"])
            for arm in ("lv", "lf"):
                S.record(fig_id, target, f"layer {c['layer']}: copy at the {'number' if arm == 'lv' else 'period'} "
                         "only (lookups switched)", *c[arm], n=c["n"], source=src)  # fmt: skip
        ax.plot(layers, [0] * len(layers), color=flat, lw=2.2, zorder=1)
        la = X.PREDICTED[target]
        ax.axvline(la, color="#555555", ls=":", lw=1.2, zorder=0)
        ax.text(la - 0.25, 103, "layer fixed\nin advance", ha="right", va="top", color="#555555", linespacing=1.0)
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_xticks(layers)
        ax.set_xlim(layers[0] - 0.8, layers[-1] + 0.8)
        ax.set_ylim(-4, 106)
        ax.set_yticks(*PCT)
        ax.set_xlabel("layer")
        ax.grid(axis="y", color="#eeeeee")
    axes[0].set_ylabel("lookups switched (%)")
    hs = [plt.Line2D([], [], color=col, ls=ls, marker=mk, mfc="white", mec=col, mew=1.6, ms=7, lw=1.8)
          for _, _, col, ls, mk in SWEEP_ARMS] + [plt.Line2D([], [], color=flat, lw=2.2)]  # fmt: skip
    legend(fig, hs, [a[1] for a in SWEEP_ARMS] + ["copy at the number or period only"], 0.775, ncol=2)
    S.save(fig, "s03b_layers_45b" if supp else "fig03b_layers", supp=supp)


# ---- after the overnight queue (Dan 27 Oct ~01:05): drawn once LANDED names the scored result folders --------------
Q_MODELS = (("qwen3.5-9b", "9b"), ("qwen3.6-27b", "27b"), ("muse-glimmer-30b", "muse"))  # 45q, 45p: no 122B run
Q_LINES = (("bw", "the bridge-word change", "#222222", "-", "o"),
           ("ls", "copy at every locker-sentence token", S.COL["lookup"], "-", "o"),
           ("li", "copy at the item's own tokens", S.COL["lookup"], "--", "s"),
           ("lr", "copy at the other locker-sentence tokens", S.COL["lookup"], ":", "^"))  # fmt: skip
MADE_BY_L, MADE_BY_HALF = (
    0.5,
    0.4,
)  # the copy "makes the link" at a layer: at least half of the switches (about, at L/2)


def made_by(lk: dict) -> str:
    """Where the full copy makes the link on one model (the rule's arms, lookups switched): 'L/2' if the copy at L/2
    already switches about half (>= 0.4), 'L' if the copy at L switches at least half, else 'not'."""
    return "L/2" if lk["rate"]["d"][0] >= MADE_BY_HALF else "L" if lk["rate"]["c"][0] >= MADE_BY_L else "not"


def rel(path: Path) -> str:
    return str(path.relative_to(pins.REPO_ROOT)) if path.is_relative_to(pins.REPO_ROOT) else str(path)


def model_list(keys: list[str]) -> str:
    names = [SHORT[m] for m in keys]
    return "the Qwens" if set(keys) == {"9b", "27b"} else " and ".join(names)


def q_sweep_line(ax, cells: list[dict], arm: str, col: str, ls: str, mk: str, lw: float = 1.6, ms: float = 5.5) -> None:
    """One arm of the 45q sweep on ax: the line through the points, each point's 95% interval, open marks."""
    layers = [c["layer"] for c in cells]
    ax.plot(layers, [100 * c[arm][0] for c in cells], color=col, ls=ls, lw=lw, zorder=2)
    for c in cells:
        ax.plot([c["layer"]] * 2, [100 * c[arm][1], 100 * c[arm][2]], color=col, lw=1.0, alpha=0.7, zorder=2)
        ax.plot([c["layer"]], [100 * c[arm][0]], mk, ms=ms, mfc="white", mec=col, mew=1.4, zorder=3)


def q_layer_axis(ax, layers: list[int], mod: dict) -> None:
    """A 45q panel's layer ticks and its dotted lines at L/2 and L."""
    ax.set_xlim(layers[0] - 1.5, layers[-1] + 2.5)
    ax.set_xticks(layers[::2] if len(layers) <= 9 else layers[::3])
    for x, txt in ((mod["arm_layers"]["d"], "L/2"), (mod["layer"], "L")):
        ax.axvline(x, color="#555555", ls=":", lw=1.2, zorder=0)
        ax.text(x + 0.6, 103, txt, ha="left", va="top", color="#555555")


def f03b_q(plt, verdict_dir: Path, link_dir: Path, sweep_dir: Path, title: str | None = None) -> None:
    """45q (results/x45b_binding/x45q-*, x45q-link-*, x45q-sweep-*): clean locker-after scenes, one panel per model
    (9B, 27B, Muse). The lookup's switch rate by layer (the sweep, after the data, open marks): the bridge-word change
    and the copy of the changed prompt's states at every locker-sentence token; dotted lines at L/2 and L. The rule's
    arms (fixed in advance, filled), from the verdict: at L the bridge-word change (a) and the copy (c), at L/2 the copy
    (d) (Muse's sweep, every 4th layer, has no point at its L or L/2). The subtitle: where the copy makes the link
    (made_by) and n; the rule and its verdict as a footnote. The other copies (the item's own tokens, the other tokens,
    the number or the period; without each token's J++ part or a random part, 45n): figures/supp/s03d (s03d_q)."""
    v = json.loads((verdict_dir / "x45q.json").read_text())
    sweep = json.loads((sweep_dir / "sweep.json").read_text())["runs"]
    by = {m["model"]: m for m in v["models"] if m["status"] != "pending"}
    label = v["verdict"]["label"]
    held, tested = v["verdict"]["models_holding"], v["verdict"]["models_tested"]
    ns = " / ".join(str(by[t]["sanity"]["pass"]) if t in by else "–" for t, _ in Q_MODELS)
    where = {m: made_by(by[t]["readers"][X.LOOKUP]) for t, m in Q_MODELS if "readers" in by.get(t, {})}
    by_l, by_half = [m for m, w in where.items() if w == "L"], [m for m, w in where.items() if w == "L/2"]
    claim = ", ".join(p for p in (f"by L on {model_list(by_l)}" if by_l else "",
                                  f"from about L/2 on {model_list(by_half)}" if by_half else "") if p)  # fmt: skip
    default = {"holds": "On clean scenes with the locker after the pick, the locker sentences make the link",
               "does not hold": "Locker after the pick: the copy into the locker sentences falls short"}  # fmt: skip
    h = 5.6
    fig, axes = plt.subplots(1, len(Q_MODELS), figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.09, right=0.985, top=1 - 1.75 / h, bottom=1.25 / h, wspace=0.10)
    S.title(fig, title or default.get(label, "Locker after the pick: where the link is made"),
            f"Lookups switched (%), 95% intervals; n = {ns} clean one-pick scenes (9B / 27B / Muse).\n"
            f"The copy into the locker sentences makes the link {claim or 'on no model'}.", limit=86)  # fmt: skip
    fig.text(0.01, 0.1 / h, textwrap.fill(
        "Lines: the layer sweep, after the data. Filled dots: the rule, fixed in advance (the copy at L or L/2 switches "
        "at least half of the changed prompt's switches, the bridge-word change at L at most 0.25, on 2 of 3 models): "
        f"{label}, {held} of {tested}.", 104), color=S.COL["muted"], va="bottom")  # fmt: skip
    for t, m in Q_MODELS:
        if m in where:
            S.record("fig03b", t, "45q: where the copy makes the link (L/2: copy at L/2 >= 0.4; L: copy at L >= 0.5)",
                     where[m], source=rel(verdict_dir / "x45q.json"))  # fmt: skip
    for ax, (target, m) in zip(axes, Q_MODELS, strict=True):
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_ylim(-4, 106)
        ax.set_yticks(*PCT)
        ax.grid(axis="y", color="#eeeeee")
        ax.set_xlabel("layer")
        mod = by.get(target)
        if mod is None or mod["run"] not in sweep or "readers" not in mod:
            S.empty(ax, "not run" if mod is None else "not tested")
            ax.set_xticks([])
            continue
        cells = sorted(sweep[mod["run"]]["cells"][X.LOOKUP], key=lambda c: c["layer"])
        for arm, name, col, ls, mk in Q_LINES[:2]:
            q_sweep_line(ax, cells, arm, col, ls, mk, lw=2.2)
            for c in cells:
                S.record("fig03b", target, f"45q, layer {c['layer']}: {name} (lookups switched)", *c[arm], n=c["n"],
                         source=rel(sweep_dir / "sweep.json"))  # fmt: skip
        la, half = mod["layer"], mod["arm_layers"]["d"]
        q_layer_axis(ax, [c["layer"] for c in cells], mod)
        lk = mod["readers"][X.LOOKUP]
        for arm, x, col, what in (("a", la, "#222222", "the bridge-word change at L"),
                                  ("c", la, S.COL["lookup"], "copy at L, every locker-sentence token"),
                                  ("d", half, S.COL["lookup"], "copy at L/2, every locker-sentence token")):  # fmt: skip
            r = lk["rate"][arm]
            ax.plot([x] * 2, [100 * r[1], 100 * r[2]], color=col, lw=1.6, zorder=5)
            ax.plot([x], [100 * r[0]], "o", ms=9, color=col, mec="white", mew=1.0, zorder=6)
            S.record("fig03b", target, f"45q, the rule's arm {arm}: {what} (lookups switched)", *r, n=lk["n"],
                     source=rel(verdict_dir / "x45q.json"))  # fmt: skip
        S.record("fig03b", target, "45q, the rule: copy at L's share of the changed prompt's lookup switches",
                 *lk["of_S"]["c"], n=lk["S_switched"], source=rel(verdict_dir / "x45q.json"))  # fmt: skip
        S.record(
            "fig03b", target, "45q: the rule holds", int(bool(mod.get("holds"))), source=rel(verdict_dir / "x45q.json")
        )
    axes[0].set_ylabel("lookups switched (%)")
    hs = [plt.Line2D([], [], color=col, ls=ls, marker=mk, mfc="white", mec=col, mew=1.4, ms=5.5, lw=2.2)
          for _, _, col, ls, mk in Q_LINES[:2]]  # fmt: skip
    hs.append(plt.Line2D([], [], marker="o", ls="", color="#555555", ms=9))
    legend(fig, hs, ["the bridge-word change", "the copy into the locker sentences", "the rule, fixed in advance"],
           1 - 0.95 / h)  # fmt: skip
    S.save(fig, "fig03b_layers")
    s03d_q(plt, by, sweep, json.loads((link_dir / "link.json").read_text())["runs"], verdict_dir, sweep_dir, link_dir)


def s03d_q(plt, by: dict, sweep: dict, link: dict, verdict_dir: Path, sweep_dir: Path, link_dir: Path) -> None:
    """Supplementary to Fig. 3b (45q, after the data): (a) per model, the lookup's switch rate by layer for the copy at
    every locker-sentence token (as in Fig. 3b) against the copy at the item's own tokens only, at the other
    locker-sentence tokens only, and at the number or the period only; (b) at L, the copy at every locker-sentence token
    (the rule's arm c) against the same copy without each token's J++ part and without a random part (same size), 45n."""
    h = 8.5
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    S.title(fig, "Supplement to Fig. 3b: which locker-sentence tokens carry the link",
            "Clean one-pick scenes, locker after the pick. Lookups switched (%), 95% intervals; after the data.")  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(0.01, at(0.95), "(a) The copy at a part of the locker sentences, by layer", **head)
    grey = "#9a9a9a"
    lines = (*Q_LINES[1:], ("lvf", "copy at the number or the period only", grey, "-", ""))
    hs = [plt.Line2D([], [], color=col, ls=ls, marker=mk, mfc="white", mec=col, mew=1.4, ms=5.5, lw=2.0)
          for _, _, col, ls, mk in lines]  # fmt: skip
    legend(fig, hs, [x[1] for x in lines], at(1.2), ncol=2)
    grid = fig.add_gridspec(1, len(Q_MODELS), left=0.09, right=0.985, top=at(2.35), bottom=at(4.75), wspace=0.10)
    axes = [fig.add_subplot(grid[0, j]) for j in range(len(Q_MODELS))]
    for j, (ax, (target, m)) in enumerate(zip(axes, Q_MODELS, strict=True)):
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_ylim(-4, 106)
        ax.set_yticks(*PCT)
        ax.grid(axis="y", color="#eeeeee")
        ax.set_xlabel("layer")
        if j:
            ax.tick_params(labelleft=False)
        mod = by.get(target)
        if mod is None or mod["run"] not in sweep or "readers" not in mod:
            S.empty(ax, "not run" if mod is None else "not tested")
            ax.set_xticks([])
            continue
        cells = sorted(sweep[mod["run"]]["cells"][X.LOOKUP], key=lambda c: c["layer"])
        src = rel(sweep_dir / "sweep.json")
        for arm, name, col, ls, mk in Q_LINES[1:]:
            q_sweep_line(ax, cells, arm, col, ls, mk, lw=2.2 if arm == "ls" else 1.6)
            for c in cells:
                S.record("s03d", target, f"45q, layer {c['layer']}: {name} (lookups switched)", *c[arm], n=c["n"],
                         source=src)  # fmt: skip
        for arm in ("lv", "lf"):
            ax.plot([c["layer"] for c in cells], [100 * c[arm][0] for c in cells], color=grey, lw=2.0, zorder=1)
            for c in cells:
                S.record("s03d", target, f"45q, layer {c['layer']}: copy at the {'number' if arm == 'lv' else 'period'}"
                         " only (lookups switched)", *c[arm], n=c["n"], source=src)  # fmt: skip
        q_layer_axis(ax, [c["layer"] for c in cells], mod)
    axes[0].set_ylabel("lookups switched (%)")

    fig.text(0.01, at(5.45), "(b) The copy at L, every locker-sentence token, and without a part of it", **head)
    b = fig.add_axes((0.25, at(7.85), 0.72, at(5.9) - at(7.85)))
    rows = (("c", "the copy (the rule's point)", S.COL["lookup"], "o"),
            ("c_nojpp", "without the J++ part", S.COL["lookup"], "D"),
            ("c_norand", "without a random part (same size)", grey, "D"))  # fmt: skip
    ys = {t: -k for k, (t, _) in enumerate(Q_MODELS)}
    for target, _m in Q_MODELS:
        mod = by.get(target)
        if mod is None or "readers" not in mod:
            b.text(50, ys[target], "not run", ha="center", va="center", color=S.COL["muted"])
            continue
        rates = link.get(mod["run"], {}).get("readers", {}).get(X.LOOKUP, {})
        for k, (arm, what, col, mk) in enumerate(rows):
            y = ys[target] + 0.25 - 0.25 * k
            if arm == "c":
                r = mod["readers"][X.LOOKUP]["rate"]["c"]
                S.record("s03d", target, "45q, the rule's arm c: copy at L, every locker-sentence token (lookups "
                         "switched)", *r, n=mod["readers"][X.LOOKUP]["n"], source=rel(verdict_dir / "x45q.json"))  # fmt: skip
            elif arm in rates:
                r = rates[arm]
                S.record("s03d", target, f"45q, copy at L {what} (lookups switched)", *r,
                         n=link[mod["run"]]["sanity"]["pass"], source=rel(link_dir / "link.json"))  # fmt: skip
            else:
                continue
            b.plot([100 * r[1], 100 * r[2]], [y, y], color=col, lw=1.6, zorder=2)
            b.plot([100 * r[0]], [y], mk, ms=8 if mk == "o" else 7, color=col, zorder=3)
    b.set_xlim(0, 100)
    b.set_xticks(*PCT)
    b.set_xlabel("lookups switched (%)")
    b.set_ylim(-len(Q_MODELS) + 0.5, 0.5)
    b.set_yticks(list(ys.values()), [name_of(m) for _, m in Q_MODELS])
    b.tick_params(axis="y", length=0)
    b.grid(axis="x", color="#eeeeee")
    b.legend([plt.Line2D([], [], marker=mk, ls="", color=col, ms=7) for _, _, col, mk in rows], [r[1] for r in rows],
             loc="upper left", frameon=False, handletextpad=0.4, handlelength=1.0, fontsize=S.FONT)  # fmt: skip
    S.save(fig, "s03d_link_copy_variants", supp=True)


P_ROWS = (("a1", "(1) without the J++ part\nat the bridge word"),
          ("a2", "(2) (1), and without it at\nthe earlier mention"),
          ("a3", "(3) (1), and without a random\npart (same size) there"),
          ("a4", "(4) (1), and without it at\nanother item's mention"))  # fmt: skip


def f03c_p(plt, verdict_dir: Path, title: str | None = None) -> str:
    """45p (results/x45p/x45p-*, fixed in advance): clean one-pick scenes whose new item's locker sentence comes before
    the asked pick; one panel per model, one row per arm (Fig. 2's style): the recall's switches lost against arm (1),
    and the lookup's, with 95% intervals (both filled, apart by colour); arm (1)'s own switches as text. Story Fig. 3c if the
    rule holds, else figures/supp/s03c (titled with the null). Returns the saved name."""
    v = json.loads((verdict_dir / "x45p.json").read_text())
    by = {m["target"]: m for m in v["models"]}
    label = v["verdict"]["label"]
    holds = label == "holds"
    default = "The recall reads the item's earlier mention when its locker came first" if holds else (
        "No sign the recall reads the earlier mention (rule not met)")  # fmt: skip
    fig, axes = plt.subplots(1, 4, figsize=(S.WIDTH, 5.6), sharey=True)
    fig.subplots_adjust(left=0.30, right=0.975, top=0.62, bottom=0.12, wspace=0.12)
    ns = " / ".join(
        str(by[t]["readers"]["recall"]["n"]) if t in by and "readers" in by[t] else "–" for t, _ in Q_MODELS
    )
    S.title(fig, title or default,
            "Clean one-pick scenes, the new item's locker before the pick (n = "
            f"{ns} on the 9B / 27B / Muse).\nSwitches lost (%): 1 − switches under the arm / under (1), 95% intervals. Rule, "
            "fixed in advance:\n(2) loses at least 0.2 more than (3) and 0.15 more than (4), on 2 of 3 models:\n"
            f"{label}, {v['verdict']['models_holding']} of {v['verdict']['models']}.", limit=86)  # fmt: skip
    src = rel(verdict_dir / "x45p.json")
    for ax, (target, m, _) in zip(axes, S.MODELS, strict=True):
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_xlim(-20, 100)
        ax.axvline(0, color="#999999", lw=0.8, zorder=1)
        ax.set_xticks(*PCT)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_ylim(-len(P_ROWS) + 0.45, 0.55)
        ax.tick_params(axis="y", length=0)
        mod = by.get(target)
        if mod is None or "readers" not in mod:
            S.empty(ax, "not run" if mod is None or mod["status"] == "pending" else "not tested")
            continue
        rc, lk = mod["readers"]["recall"], mod["readers"]["lookup"]
        ax.text(-17, 0, f"{rc['hits']['a1']} of {rc['n']}\nrecalls switch", va="center", color=S.COL["muted"],
                linespacing=1.0)  # fmt: skip
        S.record("fig03c", target, "45p, (1): recalls switched", rc["hits"]["a1"], n=rc["n"], source=src)
        for i, (arm, _) in enumerate(P_ROWS[1:], start=1):
            r = rc["loss"][arm]
            if r[0] is None or r[0] != r[0]:  # nan: (1) switches no recall
                continue
            # both readers fixed in advance: filled, told apart by colour only (Dan 27 Oct ~11:20)
            S.dot(ax, 0, -i + 0.15, tuple(100 * x for x in r), S.COL["recall"], "fixed", size=8)
            q = lk["loss"][arm]
            if q[0] == q[0]:
                S.dot(ax, 0, -i - 0.15, tuple(100 * x for x in q), S.COL["lookup"], "fixed", size=8)
                S.record("fig03c", target, f"45p, {arm}: lookup switches lost against (1)", *q, n=lk["n"], source=src)
            S.record("fig03c", target, f"45p, {arm}: recall switches lost against (1)", *r, n=rc["n"], source=src)
        S.record("fig03c", target, "45p: the rule holds", int(bool(mod.get("holds"))), source=src)
    axes[0].set_yticks([-i for i in range(len(P_ROWS))], [r[1] for r in P_ROWS])
    fig.supxlabel("switches lost (%)", x=0.62, y=0.01, fontsize=S.FONT)
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=8),
                 plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=8)],
           ["recall", "lookup"], 0.73)  # fmt: skip
    name = "fig03c_earlier_mention" if holds else "s03c_earlier_mention"
    S.save(fig, name, supp=not holds)
    return name


NOCHAT_ROUTES = {"9b": ("qwen35_9b_x6_routes", "qwen35_9b_x6_routes_x45i_nochat"),
                 "27b": ("x6_routes_27b", "x6_routes_x45i_nochat_27b")}  # fmt: skip


def s01c_nochat(plt, runs: dict[str, str], title: str | None = None) -> None:
    """45i' (descriptive, after the data, gate lowered to 0.75): the main test without the chat template on the 9B and
    27B (runs: model key -> results/x0_necessity run, rendering nochat) against the chat template (the split by sentence
    order's main-test cells): (a) the gap, all scenes; (b) the gap, locker before the pick; (c) the routes test's value
    answers with and without the template (another item moved, whole change)."""
    from scripts import x0_split_by_order as SO

    split_path = sorted((pins.RESULTS_DIR / "x0_composition").glob("split-by-order-*/split.json"))[-1]
    chat = json.loads(split_path.read_text())["cells"]
    rows_ = []  # (model key, target, rendering, {all, before} cells, source)
    for target, m, _ in S.MODELS:
        if m not in runs:
            continue
        rows_.append((m, target, "chat", chat[f"{target}|swap"]["cells"], rel(split_path)))
        src = X.RESULTS / runs[m]
        cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "nochat"}
        cells = SO.group_cells(X.read_jsonl(src / "outcomes.jsonl"), cases, X.PREDICTED[target], X.N_BOOT, "nochat")
        rows_.append((m, target, "nochat", cells, rel(src / "outcomes.jsonl")))
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, 4.6), sharey=True, gridspec_kw={"width_ratios": [1, 1, 0.75]})
    fig.subplots_adjust(left=0.27, right=0.985, top=0.60, bottom=0.15, wspace=0.12)
    S.title(fig, title or "Without the chat template the split is still there (after the data)",
            "Main test (two people swap picks). Gap = recall's extra loss minus the lookup's (0-1), 95%\n"
            f"intervals. Without the chat template: after the data, {S.LOWERED} gate lowered to 0.75. Routes test: "
            "another\nitem moved, whole change.")  # fmt: skip
    black = "#222222"
    labels = []
    for i, (m, target, rend, cells, src) in enumerate(rows_):
        y = -i
        nochat = rend == "nochat"
        labels.append(f"{SHORT[m]}, " + (f"without the\nchat template{S.LOWERED}" if nochat else "chat template"))
        for ax, g, kind in ((axes[0], "all", "after" if nochat else "fixed"), (axes[1], "before", "after")):
            c = cells.get(g)
            if c is None:
                ax.text(0.4, y, "not run", ha="center", va="center", color=S.COL["muted"])
                continue
            S.dot(ax, 0, y, tuple(c["gap"]), black, kind, size=8)
            S.record("s01c", target, f"main test, {'all scenes' if g == 'all' else 'locker before the pick'}, "
                     f"{'without the chat template' if nochat else 'chat template'}: gap", *c["gap"], n=c["n"],
                     source=src)  # fmt: skip
        run = NOCHAT_ROUTES.get(m, (None, None))[1 if nochat else 0]
        v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json") if run else None
        r = next((r for r in (v or {}).get("rows", []) if r["condition"] == "C2" and r["arm"] == "whole"), None)
        if r is None:
            axes[2].text(0.5, y, "not run", ha="center", va="center", color=S.COL["muted"],
                         transform=axes[2].get_yaxis_transform())  # fmt: skip
            continue
        k = round(r["share"]["value"][0] * r["n"])
        axes[2].text(0.5, y, f"{k} of {r['n']}", ha="center", va="center", transform=axes[2].get_yaxis_transform())
        S.record("s01c", target, f"routes test, another item moved, whole change, {'without the chat template' if nochat else 'chat template'}: "
                 "value answers", k, n=r["n"], source=str(run))  # fmt: skip
    for ax, t in ((axes[0], "(a) all scenes"), (axes[1], "(b) locker before the pick")):
        S.extra_axis(ax, label=False)
        ax.set_title(t, fontsize=S.FONT, weight="bold", loc="left")
        ax.grid(axis="x", color="#eeeeee")
    axes[2].set_title("(c) value answers", fontsize=S.FONT, weight="bold", loc="left")
    axes[2].set_xticks([])
    for side in ("top", "right", "bottom"):
        axes[2].spines[side].set_visible(False)
    axes[0].set_ylim(-len(rows_) + 0.45, 0.55)
    axes[0].set_yticks([-i for i in range(len(rows_))], labels)
    axes[0].tick_params(axis="y", length=0)
    fig.supxlabel("gap", x=0.47, y=0.01, fontsize=S.FONT)
    sh, sl = S.status_handles()
    legend(fig, sh, sl, 0.775)
    S.save(fig, "s01c_no_chat_template", supp=True)


def f03b(plt) -> None:
    """README Fig. 3b: 45q once LANDED names its folders (the 35-item 45b sweep then goes to figures/supp/s03b),
    else the 45b sweep."""
    if LANDED.get("45q"):
        d = {k: pins.RESULTS_DIR / p for k, p in LANDED["45q"].items()}
        f03b_q(plt, d["verdict"], d["link"], d["sweep"])
        f03b_layers(plt, supp=True)
    else:
        f03b_layers(plt)


def f03c(plt) -> None:
    """45p once scored (README Fig. 3c if its rule holds, else figures/supp/s03c); nothing before."""
    if LANDED.get("45p"):
        f03c_p(plt, pins.RESULTS_DIR / LANDED["45p"])


def s01c(plt) -> None:
    """45i' once its runs are named; nothing before."""
    if LANDED.get("45i"):
        s01c_nochat(plt, LANDED["45i"])


def f04_routes_design(plt) -> None:
    """The routes test: the original and the changed prompt as three lockers each; the changed prompt's moved sentence
    highlighted; an arrow from each route to the locker it predicts."""
    fig = plt.figure(figsize=(S.WIDTH, 4.6))
    ax = fig.add_axes((0, 0, 1, 0.82))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")
    S.title(fig, "Each route predicts a different locker",
            "The change at 'goose' comes from the changed prompt's 'rabbit';\n"
            "the lookup is asked on the original prompt.")  # fmt: skip
    col_x = [24 + 19.5 * j for j in range(3)]  # the three lockers' centres
    for j, name in enumerate(("first locker", "second locker", "third locker")):
        ax.text(col_x[j], 57, name, ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"])
    rows = (("original", 34, [("duck", "4"), ("rabbit", "3"), ("goose", "2")], "Beth picked the goose."),
            ("changed", 18, [("rabbit", "7"), ("duck", "4"), ("goose", "2")], "Beth picked the rabbit."))  # fmt: skip
    for label, y, lockers, pick in rows:
        ax.text(1, y + 3, f"{label}\nprompt", fontsize=S.FONT, weight="bold", va="center")
        for j, (item, digit) in enumerate(lockers):
            moved = label == "changed" and item == "rabbit"
            ax.add_patch(plt.Rectangle((col_x[j] - 9, y), 18, 6, fc="#fff1dc" if moved else "#f5f5f5",
                                       ec=S.COL["position"] if moved else "#bbbbbb", lw=1.8 if moved else 1))  # fmt: skip
            ax.text(col_x[j], y + 3, f"{item}: {digit}", ha="center", va="center", fontsize=S.FONT)
        ax.text(75, y + 3, pick, fontsize=S.FONT, va="center")
    # identity, position and the original answer point down at the original prompt's lockers; value points up at the
    # changed prompt's
    for route, digit, col, j, y_label, y_box in (("position", "4", S.COL["position"], 0, 47, 40.2),
                                                 ("identity", "3", S.COL["identity"], 1, 47, 40.2),
                                                 ("original answer", "2", "#7f7f7f", 2, 47, 40.2),
                                                 ("value", "7", S.COL["value"], 0, 6, 17.8)):  # fmt: skip
        ax.text(col_x[j], y_label, f"{route} → {digit}", fontsize=S.FONT + 1, weight="bold", color=col, ha="center",
                va="center", bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=col, lw=1.4))  # fmt: skip
        start = y_label - 2.6 if y_label > y_box else y_label + 2.6
        ax.annotate("", (col_x[j], y_box), (col_x[j], start), arrowprops=dict(arrowstyle="->", color=col, lw=1.6))
    ax.text(col_x[0] + 13, 6, "the moved sentence: first place, new number", fontsize=S.FONT, color=S.COL["position"],
            va="center")  # fmt: skip
    # v6: Fig. 5's left panel draws this design; the full-width schematic stays as a supplement
    S.save(fig, "s04_routes_design", supp=True)


def routes_design_panel(plt, ax) -> None:
    """Fig. 5's left panel: f04_routes_design's schematic at half width. The original and the changed prompt as three
    lockers each (the changed prompt's moved sentence outlined in orange); identity, position and the original answer
    point down at the original prompt's lockers, the value up at the changed prompt's new number."""
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 103)
    ax.axis("off")
    col_x = (35, 61, 87)
    for x, name in zip(col_x, ("first", "second", "third"), strict=True):
        ax.text(x, 98, name, ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"])
    ax.text(1, 98, "locker", ha="left", va="center", fontsize=S.FONT, color=S.COL["muted"])
    rows = (("original\nprompt", 57, (("duck", "4"), ("rabbit", "3"), ("goose", "2")), "Beth picked the goose."),
            ("changed\nprompt", 33, (("rabbit", "7"), ("duck", "4"), ("goose", "2")), "Beth picked the rabbit."))  # fmt: skip
    for label, y, lockers, pick in rows:
        ax.text(1, y + 5, label, fontsize=S.FONT, weight="bold", va="center", linespacing=1.0)
        for x, (item, digit) in zip(col_x, lockers, strict=True):
            moved = label.startswith("changed") and item == "rabbit"
            ax.add_patch(plt.Rectangle((x - 11, y), 22, 10, fc="#fff1dc" if moved else "#f5f5f5",
                                       ec=S.COL["position"] if moved else "#bbbbbb", lw=1.8 if moved else 1))  # fmt: skip
            ax.text(x, y + 5, f"{item}: {digit}", ha="center", va="center", fontsize=S.FONT)
        ax.text(100, y - 5, pick, ha="right", va="center", fontsize=S.FONT, style="italic")
    for route, digit, col, j in (("position", "4", S.COL["position"], 0), ("identity", "3", S.COL["identity"], 1),
                                 ("original\nanswer", "2", "#7f7f7f", 2)):  # fmt: skip
        ax.text(col_x[j], 83, f"{route}\n→ {digit}" if "\n" not in route else f"{route} → {digit}", ha="center",
                va="center", fontsize=S.FONT, color=col, linespacing=1.0,
                bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": col, "lw": 1.3})  # fmt: skip
        ax.annotate("", (col_x[j], 67.5), (col_x[j], 75.5), arrowprops={"arrowstyle": "->", "color": col, "lw": 1.5})
    ax.text(col_x[0], 12, "value → 7", ha="center", va="center", fontsize=S.FONT, color=S.COL["value"],
            bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": S.COL["value"], "lw": 1.3})  # fmt: skip
    ax.annotate(
        "", (col_x[0], 32.5), (col_x[0], 17), arrowprops={"arrowstyle": "->", "color": S.COL["value"], "lw": 1.5}
    )


# Fig. 5's result rows (v6): the arm, its label, and the random control drawn as a thin light grey bar under it (the
# position answers without a random part of the same size); the keep-only arms and the 122B are in s05
ROUTE_ROWS = (("whole", "whole change", None), ("no_alf", "without the address", "no_alf_rand"))
ROUTE_RUNS = {"9b": ("qwen35_9b_x6_routes", "qwen35_9b_x6_routes_keeponly"),
              "27b": ("x6_routes_27b", "x6_routes_keeponly_27b"),
              "122b": ("qwen35_122b_x6_routes_g75", "qwen35_122b_x6_routes_keeponly_g75"),
              "muse": ("muse30b_x6_routes", "muse30b_x6_routes")}  # fmt: skip


def f05_routes(plt) -> None:
    """Fig. 5 (E5, v6): left, the routes design (routes_design_panel); right, another item moved, at the layer fixed in
    advance, per model (9B, 27B, Muse) two stacked rows of lookup answers, whole change and without the address, each
    identity / position share with its 95% interval, the original answer empty; under the second row a thin light grey
    bar for the position answers without a random part of the same size; the value as an empty slot labelled with its
    share (0) at the right of each row. The 122B and the keep-only arms are in s05."""
    fig = plt.figure(figsize=(S.WIDTH, 5.4))
    S.title(fig, "The lookup follows identity or position, never the value",
            "Left: where each route sends the lookup. Right: lookup answers with the change placed at L.")  # fmt: skip
    left_ax = fig.add_axes((0.01, 0.04, 0.40, 0.70))
    routes_design_panel(plt, left_ax)
    left_ax.text(0, 1.015, "The routes test", transform=left_ax.transAxes, fontsize=12, weight="bold", va="bottom")
    ax = fig.add_axes((0.625, 0.10, 0.36, 0.60))
    models = [(t, m) for t, m, _ in S.MODELS if m != "122b"]  # v6: the 122B in supplements only
    gap, y, ticks, labels, ns = 2.75, 0.0, [], [], set()
    for target, m in models:
        run = ROUTE_RUNS[m][0]
        v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
        rows = {r["arm"]: r for r in (v or {}).get("rows", []) if r["condition"] == "C2"}
        ax.text(-0.02, y + 0.62, NAMES[m], transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=S.FONT, weight="bold")  # fmt: skip
        for i, (arm, label, rand) in enumerate(ROUTE_ROWS):
            yi = y - i
            ticks.append(yi)
            labels.append(label)
            r = rows.get(arm)
            if r is None:
                S.empty(ax, "not run")
                continue
            ns.add(r["n"])
            left = 0.0
            for route in ("identity", "position"):
                sh = r["share"][route]
                ax.barh(yi, sh[0], left=left, height=0.62, color=ROUTE_COL[route], lw=0)
                ax.plot([left + sh[1], left + sh[2]], [yi - 0.2, yi - 0.2], color="#1e1e1e", lw=1.2,
                        solid_capstyle="butt")  # fmt: skip
                if sh[0] >= 0.15:
                    ax.text(left + sh[0] / 2, yi + 0.06, f"{sh[0]:.2f}", ha="center", va="center", fontsize=S.FONT,
                            color="white" if route == "identity" else "#222222")  # fmt: skip
                left += sh[0]
            ax.barh(yi, 1 - left, left=left, height=0.62, **S.EMPTY)  # the original answer (and other)
            for route, _ in ROUTES:
                S.record("fig05", target, f"another item moved, {arm}: {route} share", *r["share"][route], n=r["n"],
                         source=run)  # fmt: skip
            # the value: an empty slot labelled with its share, filled only if the lookup ever takes it
            val = r["share"]["value"][0]
            ax.add_patch(plt.Rectangle((1.07, yi - 0.31), 0.13, 0.62, fc=S.COL["value"] if val > 0 else "white",
                                       ec=S.COL["value"], lw=1.3, clip_on=False))  # fmt: skip
            ax.text(1.135, yi, f"{val:.0f}" if val == 0 else f"{val:.2f}", ha="center", va="center",
                    fontsize=S.FONT, color=S.COL["value"] if val == 0 else "white", weight="bold")  # fmt: skip
            rr = rows.get(rand) if rand else None
            if rr is not None:
                pos = rr["share"]["position"]
                yc = yi - 0.48
                ax.barh(yc, pos[0], height=0.16, color=S.COL["control"], lw=0)
                ax.plot([pos[1], pos[2]], [yc, yc], color="#7a7a7a", lw=1.0, solid_capstyle="butt")
                ax.text(pos[2] + 0.02, yc, f"{pos[0]:.2f}", va="center", fontsize=S.FONT, color=S.COL["muted"])
                S.record("fig05", target, f"another item moved, {rand}: position share", *pos, n=rr["n"], source=run)
        y -= gap
    ax.set_xlim(0, 1.2)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax.spines["bottom"].set_bounds(0, 1)
    ax.set_ylim(y + gap - 1.75, 1.0)
    ax.set_yticks(ticks, labels)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("share of lookups", x=0.42)
    ax.text(1.135, 0.62, "value", ha="center", va="center", fontsize=S.FONT, color=S.COL["value"])
    ax.text(-0.5, 1.09, "Lookup answers at L", transform=ax.transAxes, fontsize=12, weight="bold", va="bottom")
    n = "–".join(str(k) for k in sorted(ns)) + " per model"
    S.panel_tag(ax, n, "fixed")
    S.panel_tag(left_ax, None, None)
    hs = [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL["identity"]), plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL["position"]),
          plt.Rectangle((0, 0), 1, 1, **S.EMPTY), plt.Rectangle((0, 0), 1, 0.35, color=S.COL["control"])]  # fmt: skip
    legend(fig, hs, ["identity", "position", "original answer", "position, without a random part (same size)"], 0.885,
           ncol=4)  # fmt: skip
    S.save(fig, "fig05_routes")


ROUTE_LAYERS = {"9b": (("qwen35_9b_x6_routes_l6", 6, "fixed"), ("qwen35_9b_x6_routes_sweep_l8", 8, "after"),
                       ("qwen35_9b_x6_routes_sweep_l10", 10, "after"), ("qwen35_9b_x6_routes", 12, "fixed")),
                "27b": (("x6_routes_l16_27b", 16, "fixed"), ("x6_routes_sweep_l20_27b", 20, "after"),
                        ("x6_routes_sweep_l24_27b", 24, "after"), ("x6_routes_sweep_l28_27b", 28, "after"),
                        ("x6_routes_27b", 32, "fixed")),
                "122b": (("qwen35_122b_x6_routes_sweep_l24_g75", 24, "after"), ("qwen35_122b_x6_routes_l27_g75", 27, "after"),
                         ("qwen35_122b_x6_routes_sweep_l30_g75", 30, "after"), ("qwen35_122b_x6_routes_g75", 33, "after"),
                         ("qwen35_122b_x6_routes_sweep_l36_g75", 36, "after")),
                # Muse: L34 not tested (the sanity swap moved the lookup in no scene; batch 38's G2)
                "muse": (("muse30b_x6_routes_l13", 13, "fixed"), ("muse30b_x6_routes", 26, "fixed"))}  # fmt: skip


def f06_depth(plt) -> None:
    """Candidate, after the data: top, the J++ extra loss by layer (points with CIs, no connecting line); bottom, the
    position share when another item moved, at each layer the routes test ran; purple shading over the layers where the
    lookup still needs J++ (extra loss >= NEEDS); x = layer number."""
    fig, axes = plt.subplots(2, 4, figsize=(S.WIDTH, 6.3), sharex="col", gridspec_kw={"height_ratios": [1.2, 1]})
    fig.subplots_adjust(left=0.11, right=0.985, top=0.71, bottom=0.09, wspace=0.22, hspace=0.18)
    S.title(fig, "Position answers appear with depth, once the lookup stops needing the J++ part",
            "Extra loss (0-1): switches lost without the J++ part, minus those without a random part (same size).\n"
            f"Shaded: the lookup still needs the J++ part (extra loss ≥ 0.3). {S.LOWERED} gate lowered to 0.75 after the data.",
            limit=78)  # fmt: skip
    for j, (target, m, _) in enumerate(S.MODELS):
        top, bot = axes[0, j], axes[1, j]
        cells = XF.Run(depth_run(m)).cells("chat")
        layers = sorted({k[1] for k in cells})
        top.axhspan(S.XLIM[0], S.NOT_NEEDED, color=S.COL["band"], lw=0, zorder=0)
        need, measured = [], []
        for w, col, dx in ((X.LOOKUP, S.COL["lookup"], -0.25), (X.RECALL, S.COL["recall"], 0.25)):
            pts = [(la, cells[("chat", la, w, *X.MAIN)]) for la in layers]
            pts = [(la, c) for la, c in pts if c["valid"]]
            for la, c in pts:
                e = c["excess"]
                top.plot([la + dx, la + dx], [e[1], e[2]], color=col, lw=1.2, alpha=0.8)
                top.plot([la + dx], [e[0]], "o", ms=5, mfc="white", mec=col, mew=1.5)
                S.record("fig06", target, f"layer {la}: {'lookup' if w == X.LOOKUP else 'recall'} J++ extra loss", *e,
                         n=c["n"], source=depth_run(m))  # fmt: skip
            measured += [la for la, _ in pts]
            if w == X.LOOKUP:
                need = [la for la, c in pts if c["excess"][0] >= NEEDS]
        steps = sorted(set(measured))
        half = (steps[1] - steps[0]) / 2 if len(steps) > 1 else 1
        if need:
            for ax in (top, bot):
                ax.axvspan(steps[0] - half, max(need) + half, color=S.COL["shade"], lw=0, zorder=0)
        top.set_ylim(*S.XLIM)
        top.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        top.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        top.grid(axis="y", color="#eeeeee")
        bot.set_ylim(0, 100)
        bot.set_yticks(*PCT)
        for run, layer, kind in ROUTE_LAYERS[m]:
            v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
            r = next((r for r in (v or {}).get("rows", []) if r["condition"] == "C2" and r["arm"] == "whole"), None)
            if r is None:
                continue
            pos = r["share"]["position"]
            bot.plot([layer, layer], [100 * pos[1], 100 * pos[2]], color=S.COL["position"], lw=1.6)
            bot.plot([layer], [100 * pos[0]], "o", ms=7, mfc=S.COL["position"] if kind == "fixed" else "white",
                     mec=S.COL["position"], mew=1.6)  # fmt: skip
            S.record("fig06", target, f"layer {layer}: position share (another item moved, whole change)", *pos,
                     n=r["n"], source=run)  # fmt: skip
        tested = steps + [la for _, la, _ in ROUTE_LAYERS[m]]
        bot.set_xlim(min(tested) - 2, max(tested) + 2)
        bot.grid(axis="y", color="#eeeeee")
        bot.set_xlabel("layer")
    axes[0, 0].set_ylabel("extra loss without\nthe J++ part")
    axes[1, 0].set_ylabel("position\nanswers (%)")
    for ax in axes[:, 1:].flat:
        ax.tick_params(labelleft=False)
    hs, ls = reader_handles(plt)
    hs.append(plt.Line2D([], [], marker="o", ls="", color=S.COL["position"], ms=7))
    sh, sl = S.status_handles(("after",))
    legend(fig, hs + sh, [*ls, "position answers (filled: fixed in advance)", "open: " + sl[0]], 0.85, ncol=2)
    S.save(fig, "fig06_depth")


def f07_writes(plt) -> None:
    """Batch 44: per model, the lookup's share sent to the written locker against the dose in units of a real pointer
    change's size (each pair's s / s*), thin lines per locker pair, the thick line their mean, grey the random direction
    (at s / the pairs' mean s*); below, the recall's changed answers under the strongest write: the target item, the third
    item, other."""
    fig = plt.figure(figsize=(S.WIDTH, 7.0))
    grid = fig.add_gridspec(1, 4, left=0.13, right=0.99, top=0.75, bottom=0.47, wspace=0.14)
    S.title(fig, "One fixed vector written at the bridge sends the lookup to its locker",
            "Dose: × a real change's size. Thin: each locker pair; thick: their mean.\n"
            f"{S.LOWERED} gate lowered to 0.75 after the data.")  # fmt: skip
    bars = fig.add_axes((0.25, 0.10, 0.60, 0.23))
    for i, (target, m, _) in enumerate(S.MODELS):
        ax = fig.add_subplot(grid[0, i])
        ax.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        root = pins.RESULTS_DIR / "x8_write" / X8_RUNS[m]
        v, rc = latest(root, "verdict-*/verdict.json"), latest(root, "recall-*/recall.json")
        if v is None or rc is None:
            S.empty(ax, "not run")
            continue
        s_star = rc["s_real"]
        mean_star = sum(s_star.values()) / len(s_star)
        by_s: dict[float, list[float]] = {}
        for j in range(3):
            for k in range(3):
                if j == k:
                    continue
                pts = sorted(
                    (c["s"], c["target"][0]) for c in v["cells"] if c["kind"] == "write" and c["pair"] == [j, k]
                )
                star = s_star[f"{min(j, k)}-{max(j, k)}"]
                ax.plot([s / star for s, _ in pts], [100 * t for _, t in pts], color=S.COL["lookup"], lw=1, alpha=0.35)
                for s, t in pts:
                    by_s.setdefault(s, []).append(t)
        mean = sorted((s, sum(t) / len(t)) for s, t in by_s.items())
        ax.plot([s / mean_star for s, _ in mean], [100 * t for _, t in mean], color=S.COL["lookup"], lw=3, marker="o",
                ms=5)  # fmt: skip
        rand = sorted((c["s"], c["target"]) for c in v["cells"] if c["kind"] == "random" and c["pair"] is None)
        ax.plot([s / mean_star for s, _ in rand], [100 * t[0] for _, t in rand], color="#9a9a9a", lw=2, marker="s",
                ms=5)  # fmt: skip
        for s, t in mean:
            S.record("fig07", target, f"lookup target share, mean over locker pairs, s = {s:g}", round(t, 4),
                     source=X8_RUNS[m])  # fmt: skip
            S.record("fig07", target, f"dose (s / mean s*), s = {s:g}", round(s / mean_star, 4), source=X8_RUNS[m])
        for s, t in rand:
            S.record("fig07", target, f"lookup target share, random direction, s = {s:g}", *t, source=X8_RUNS[m])
        ax.axvline(1, color="#555555", lw=1, ls=":")
        ax.set_ylim(0, 100)
        ax.set_yticks(*PCT)
        ax.set_xlim(0, 4.2)
        ax.set_xticks([0, 1, 2, 3, 4])
        ax.grid(axis="y", color="#eeeeee")
        if i:
            ax.tick_params(labelleft=False)
        else:
            ax.set_ylabel("lookups to the\nwritten locker (%)")
        got = rc["changed_by_item"].get("write|4", {})
        total = sum(got.values())
        left = 0.0
        for item, col, label in (("target", S.COL["lookup"], "the written locker's item"), ("third", "#d98cb3", "the third item"),
                                 ("other", "#c8c8c8", "other")):  # fmt: skip
            share = sum(
                n for it, n in got.items() if (it == item if item != "other" else it not in ("target", "third"))
            )
            share = share / total if total else 0
            bars.barh(-i, share, left=left, height=0.6, color=col, edgecolor="white", lw=0.8)
            if share >= 0.1:
                bars.text(left + share / 2, -i, f"{100 * share:.0f}%", ha="center", va="center", fontsize=S.FONT,
                          color="white" if item == "target" else "#222222")  # fmt: skip
            S.record("fig07", target, f"recall changed under the strongest write (s = 4): {label}", round(share, 4),
                     n=total, source=X8_RUNS[m])  # fmt: skip
            left += share
        bars.text(1.01, -i, f"{total} changed", va="center", fontsize=S.FONT, color=S.COL["muted"])
    fig.text(0.56, 0.41, "dose (× a real change)", ha="center", va="center")  # one x label for the four panels
    bars.set_xlim(0, 1)
    bars.set_xticks([0, 0.5, 1], ["0", "50", "100"])
    bars.set_yticks([-i for i in range(4)], [name_of(m, m in LOWERED_M) for _, m, _ in S.MODELS])
    bars.tick_params(axis="y", length=0)
    bars.set_title("When the recall changed under the strongest write, it named:", fontsize=S.FONT, loc="left", x=-0.3)
    bars.legend([plt.Rectangle((0, 0), 1, 1, color=c) for c in (S.COL["lookup"], "#d98cb3", "#c8c8c8")],
                ["the written locker's item", "the third item", "other"], loc="upper left", bbox_to_anchor=(-0.3, -0.18),
                ncol=3, frameon=False, handlelength=1.2)  # fmt: skip
    legend(fig, [plt.Line2D([], [], color=S.COL["lookup"], lw=3), plt.Line2D([], [], color="#9a9a9a", lw=2, marker="s"),
                 plt.Line2D([], [], color="#555555", ls=":")],
           ["write", "random direction (same size)", "as large as a real change"], 0.84)  # fmt: skip
    S.save(fig, "fig07_writes")


# Fig. 8 (a) (Dan, 27 Oct ~00:30; the layout of the 26 Oct Fig. 8b draft): 45a's sentence before the lockers, rows top
# to bottom with a divider after the second; the variants' labels in Dan's words
LAYOUT_ROWS = (("V0", "no sentence"), ("V4", "a neutral sentence"), ("V1", "a pick naming the\nfirst-locker item"),
               ("V2", "a pick naming\nanother locker item"), ("V3", "a pick naming an\nitem with no locker"))  # fmt: skip
LAYOUT_YS = (0, -1, -2.4, -3.4, -4.4)  # the gap after the second row holds the divider


def layout_table() -> dict[str, tuple[str, dict]]:
    """45a's descriptive table (results/x6_routes/x45a-descriptive-*, after the data): target -> (run, block)."""
    table = latest(pins.RESULTS_DIR / "x6_routes", "x45a-descriptive-*/table.json") or {}
    return {b["model"]: (run, b) for run, b in table.items()}


def layout_panel(ax, target: str, m: str, run: str, b: dict, fig_id: str) -> None:
    """One model's 45a panel: per variant the lookup's answers on first-locker moves under the whole change (stacked:
    identity, position, original; other only if >= 0.02; value is 0 everywhere), and beta (the shift of the pointer's
    code vs no sentence) at the right."""
    ax.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
    r, beta = b["routes"], b["beta"]
    for (v, label), y in zip(LAYOUT_ROWS, LAYOUT_YS, strict=True):
        what = label.replace("\n", " ")
        share, left = r["share"][f"whole|{v}"], 0.0
        for route in ("identity", "position", "value", "original", "other"):
            sh = share.get(route, 0.0)
            if sh <= 0 or (route == "other" and sh < 0.02):
                continue
            ax.barh(y, sh, left=left, height=0.68, color=ROUTE_COL[route], edgecolor="white", lw=0.8)
            if route in ("identity", "position") and sh >= 0.13:  # narrower: the label overflows (Dan ~22:05)
                pct = round(100 * float(f"{sh:.2f}"))  # the percent of the README's two-decimal number
                ax.text(left + sh / 2, y, f"{pct}", ha="center", va="center", fontsize=S.FONT,
                        color="white" if route == "identity" else "#222222")  # fmt: skip
            ci = r["identity_ci"][f"whole|{v}"] if route == "identity" else (None, None)
            S.record(fig_id, target, f"45a, first-locker moves, whole change, {what}: {route} share", round(sh, 4), *ci,
                     n=r["n"], source=f"x6_routes/{run}")  # fmt: skip
            left += sh
        if v in beta:
            bv = beta[v]["beta"]
            ax.text(1.04, y, f"{bv[0]:.2f}", va="center", ha="left", fontsize=S.FONT, color="#222222",
                    transform=ax.get_yaxis_transform())  # fmt: skip
            S.record(fig_id, target, f"45a, beta vs no sentence: {what}", round(bv[0], 4), bv[1], bv[2],
                     n=beta[v]["n"], source=f"x6_routes/{run}")  # fmt: skip
    ax.plot([0, 1], [-1.7, -1.7], color="#999999", ls="--", lw=1, clip_on=False)
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.5, 1], ["0", "50", "100"])
    ax.set_ylim(-4.85, 0.5)
    ax.tick_params(axis="y", length=0)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)


def f08_first_locker(plt) -> None:
    """After the data. 45a: per model (9B, 27B, Muse) the lookup's answers on first-locker moves under the whole change,
    by the sentence added before the lockers, and at the right the code shift (beta: how far the pointer's code moves
    against no sentence, in positions). The routes test's position answers by the move and the neutral-sentence test:
    figures/supp/s08b (s08b_pointer_moves); the 26 Oct panels on what the prompt names first and the label-free
    pointer: figures/supp/s08_first_sentence_and_label_free."""
    by = layout_table()
    h = 5.1
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    S.title(fig, "A neutral sentence barely moves the pointer's code; naming an item does",
            "Bars: lookup answers (%) on first-locker moves with a sentence before the lockers (routes test, after the\n"
            "data). Numbers at the right: how far the pointer's code shifts against no sentence, in positions.",
            limit=86)  # fmt: skip
    names = {"identity": "identity", "position": "position", "original": "original answer"}
    legend(fig, [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL[k]) for k in names], list(names.values()), at(1.0))
    models = [(t, m) for t, m, _ in S.MODELS if t in by]
    grid_a = fig.add_gridspec(1, len(models), left=0.255, right=0.905, top=at(1.65), bottom=at(4.3), wspace=0.40)
    axes_a = [fig.add_subplot(grid_a[0, j]) for j in range(len(models))]
    for ax, (target, m) in zip(axes_a, models, strict=True):
        layout_panel(ax, target, m, *by[target], "fig08")
    axes_a[0].set_yticks(LAYOUT_YS, [label for _, label in LAYOUT_ROWS])
    for ax in axes_a[1:]:
        ax.set_yticks(LAYOUT_YS, [])
    fig.text(0.58, at(4.8), "lookup answers (%), first-locker moves, whole change", ha="center", va="center")
    S.save(fig, "fig08_first_locker")
    s08b_pointer_moves(plt)


def s08b_pointer_moves(plt) -> None:
    """Supplementary to Fig. 8 (after the data): (a) the routes test, the position answers with only the pointer for
    moves to or from the first locker vs between the second and third (grey: the whole change); (b) the
    neutral-sentence test (batch 44 B): the code's shift in positions with a sentence before the first locker (B1) or
    between the lockers and the picks (B2). Layout in inches from the top. data.csv keeps the quantities' names from
    Fig. 8's panels (b) and (c)."""
    pairs = latest(pins.RESULTS_DIR / "x8_write", "pairs-*/pairs.json") or {}
    h = 7.3
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    S.title(fig, "Supplement to Fig. 8: the pointer by the move, and a neutral sentence",
            f"All after the data; {S.LOWERED} gate lowered to 0.75 after the data.")  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(0.01, at(0.85), "(a) Only the pointer: position answers by the move", **head)
    legend(fig, [plt.Rectangle((0, 0), 1, 1, color=S.COL["position"]), plt.Rectangle((0, 0), 1, 1, color="#c8c8c8")],
           ["only the pointer", "whole change"], at(1.1))  # fmt: skip
    grid_b = fig.add_gridspec(1, 4, left=0.24, right=0.98, top=at(1.8), bottom=at(3.2), wspace=0.14)
    for j, (target, m, _) in enumerate(S.MODELS):
        b = fig.add_subplot(grid_b[0, j])
        b.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        moves = pairs.get(target, {}).get("moves", {})
        groups = (  # data.csv's name for the group (as before), its tick label (narrow lines: the panels are 1.5 in)
            ("with the first", "moves\nwith the\nfirst\nlocker", [k for k in moves if "0" in k.split("-")]),
            ("second ↔ third", "second\n↔ third\nlocker", ["1-2", "2-1"]),
        )
        xs = (0, 1.15)
        for x, (name, _, keys) in zip(xs, groups, strict=True):
            for ai, (arm, col) in enumerate((("whole", "#c8c8c8"), ("keep_alf", S.COL["position"]))):
                vals = [(moves[k]["position"][arm], moves[k]["n"]) for k in keys
                        if k in moves and moves[k]["position"][arm] is not None]  # fmt: skip
                if not vals:
                    continue
                share = sum(v * n for v, n in vals) / sum(n for _, n in vals)
                b.bar(x + (ai - 0.5) * 0.38, 100 * share, width=0.36, color=col, edgecolor="white")
                S.record("s08b", target, f"(b) routes, position share, {arm}, moves {name}", round(share, 4),
                         n=sum(n for _, n in vals), source="x8_write pairs")  # fmt: skip
        b.set_xticks(xs, [g[1] for g in groups])
        b.set_xlim(-0.45, 1.6)
        b.set_ylim(0, 100)
        b.set_yticks(*PCT)
        b.tick_params(axis="x", length=0)
        b.grid(axis="y", color="#eeeeee")
        if j:
            b.tick_params(labelleft=False)
        else:
            b.set_ylabel("position\nanswers (%)")

    fig.text(0.01, at(4.4), "(b) A neutral sentence barely moves the pointer's code", **head)
    c = fig.add_axes((0.10, at(6.5), 0.40, at(4.9) - at(6.5)))
    open_dot = dict(marker="o", ls="", mfc="white", mew=1.6, ms=7)
    fig.legend([plt.Line2D([], [], mec=S.COL["lookup"], **open_dot), plt.Line2D([], [], mec="#9a9a9a", **open_dot)],
               ["a sentence before the first locker\n(would shift the code if it\ncounted sentences)",
                "a sentence between the lockers\nand the picks (would shift it if\nit counted distance back)"],
               loc="center left", bbox_to_anchor=(0.55, at(5.7)), frameon=False, handletextpad=0.4,
               labelspacing=1.0, handlelength=1.4)  # fmt: skip
    for i, (target, m, _) in enumerate(S.MODELS):
        v = latest(pins.RESULTS_DIR / "x8_write" / X8_ORDER[m], "verdict-*/verdict.json")
        if v is None:
            c.text(i, 0.5, "not run", ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"], rotation=90)
            continue
        for k, (b_, col) in enumerate((("B1", S.COL["lookup"]), ("B2", "#9a9a9a"))):
            beta = v["variants"][b_]["beta"]
            c.plot([i + (k - 0.5) * 0.3] * 2, [beta[1], beta[2]], color=col, lw=1.6)
            c.plot([i + (k - 0.5) * 0.3], [beta[0]], "o", ms=7, mfc="white", mec=col, mew=1.6)
            S.record("s08b", target, f"(c) neutral sentence {b_}: the code's shift in positions", *beta,
                     n=v["variants"][b_]["n"], source=X8_ORDER[m])  # fmt: skip
    for line_y, ls, text in ((0.5, "--", "counts as shifted"), (1.0, ":", "one full position")):
        c.axhline(line_y, color="#555555", ls=ls, lw=1)
        c.text(-0.45, line_y + 0.02, text, ha="left", va="bottom", fontsize=S.FONT, color="#555555")
    c.set_ylim(-0.1, 1.2)
    c.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    c.set_xlim(-0.5, 3.5)
    c.set_xticks(range(4), ["9B", "27B", f"122B{S.LOWERED}", "Muse"])
    c.set_ylabel("code shift (positions)")
    c.grid(axis="y", color="#eeeeee")
    fig.text(0.01, at(7.0), "Same neutral sentence in both prompts (no item, no digit, 10-12 tokens).",
             color=S.COL["muted"], va="center")  # fmt: skip
    S.save(fig, "s08b_pointer_moves_and_neutral_sentence", supp=True)


NAMED_LABEL = (
    "bridge named first,\nits locker sentence",
    "bridge named first,\na pick sentence",
    "another item\nnamed first",
)
X8_ORDER = {"9b": "qwen35_9b_x8_order", "27b": "x8_order_27b", "122b": "qwen35_122b_x8_order_g75",
            "muse": "muse30b_x8_order_r2"}  # fmt: skip
PCF = {"9b": "qwen35_9b_x7_pcf", "27b": "x7_pcf_27b", "122b": "qwen35_122b_x7_pcf", "muse": "muse30b_x7_pcf"}


def s08_first_sentence(plt) -> None:
    """Supplementary to Fig. 8 (its 26 Oct panels (a) and (d), after the data): (a) the main test's pointer removal, the
    lookup's extra loss by which item the first sentence names (x0_first_sentence, NAMED); (b) the label-free pointer's
    overlap with the pointer (mean cos^2), chance = a random 4-d subspace's (4 / d, the P_cf reports'
    random_mean_cos2)."""
    from scripts import x0_first_sentence as FS

    first = latest(pins.RESULTS_DIR / "x0_massmean", "first-sentence-*/first.json") or {}
    h = 7.6
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    grid_a = fig.add_gridspec(1, 4, left=0.24, right=0.98, top=at(2.0), bottom=at(3.85), wspace=0.14)
    S.title(fig, "Supplement to Fig. 8: the first sentence and the label-free pointer",
            f"All after the data; {S.LOWERED} gate lowered to 0.75 after the data. Extra loss (0-1): switches lost\n"
            "without the pointer, minus those lost without a random part (same size).")  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(0.01, at(1.05), "(a) Without the pointer, by what the prompt names first", **head)
    fig.text(0.01, at(4.55), "(b) label-free pointer: overlap with the pointer (mean cos²)", **head)
    open_dot = dict(marker="o", ls="", mfc="white", mew=1.6, ms=7)
    legend(fig, [plt.Line2D([], [], mec=S.COL["lookup"], **open_dot),
                 plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=5)], ["lookup", "recall"], at(1.3))  # fmt: skip
    for j, (target, m, _) in enumerate(S.MODELS):
        a = fig.add_subplot(grid_a[0, j])
        S.extra_axis(a)
        a.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        f = first.get(target, {})
        for i, g in enumerate(FS.NAMED):
            lk, rc = f.get(f"{X.LOOKUP}|named|{g}", {}), f.get(f"{X.RECALL}|named|{g}", {})
            if "extra_loss" in rc:
                a.plot([rc["extra_loss"][0]], [-i - 0.25], "o", ms=5, color=S.COL["recall"], zorder=3)
            if "extra_loss" in lk:
                S.dot(a, 0, -i, lk["extra_loss"], S.COL["lookup"], "after")
                S.record("s08", target, f"(a) lookup extra loss without the pointer: {g}", *lk["extra_loss"], n=lk["n"],
                         source="x0_first_sentence")  # fmt: skip
        a.set_ylim(-len(FS.NAMED) + 0.4, 0.6)
        a.set_yticks([-i for i in range(len(FS.NAMED))], NAMED_LABEL if j == 0 else [])
        a.tick_params(axis="y", length=0)
    d = fig.add_axes((0.10, at(7.1), 0.40, at(5.15) - at(7.1)))
    chance = {}
    for i, (target, m, _) in enumerate(S.MODELS):
        r = json.loads(p.read_text()) if (p := pins.RESULTS_DIR / "x7_pcf" / PCF[m] / "report.json").exists() else None
        if r is not None:
            d.bar(i, r["mean_cos2_with_alf"], width=0.6, color=S.COL["position"])
            d.text(i, r["mean_cos2_with_alf"] + 0.03, f"{r['mean_cos2_with_alf']:.2f}", ha="center", fontsize=S.FONT)
            S.record("s08", target, "(b) label-free pointer: mean cos^2 with ours", round(r["mean_cos2_with_alf"], 4),
                     source=PCF[m])  # fmt: skip
            chance[target] = (i, r["random_mean_cos2"], PCF[m])
    # chance: a random 4-d subspace against the pointer's, 4 / d per model (d: the hidden size); one line where the four
    # agree to two decimals (they do: 0.0006-0.0013), else one per bar
    for target, (_, ch, src) in chance.items():
        S.record("s08", target, "(b) chance: a random 4-d subspace's mean cos^2 (4 / d)", ch, source=src)
    vals = [ch for _, ch, _ in chance.values()]
    if vals and len({round(ch, 2) for ch in vals}) == 1:
        level = sum(vals) / len(vals)
        d.axhline(level, color="#333333", lw=0.8, ls=":")
        d.text(1.02, level, "chance", transform=d.get_yaxis_transform(), va="center", fontsize=S.FONT,
               color="#333333", clip_on=False)  # fmt: skip
    else:
        for i, ch, _ in chance.values():
            d.plot([i - 0.4, i + 0.4], [ch, ch], color="#333333", lw=0.8, ls=":")
        d.text(1.02, vals[-1], "chance", transform=d.get_yaxis_transform(), va="center", fontsize=S.FONT,
               color="#333333", clip_on=False)  # fmt: skip
    d.set_ylim(-0.05, 1)  # below 0: the chance line (about 0.001) must not hide in the axis
    d.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    d.set_xlim(-0.5, 3.5)
    d.set_xticks(range(4), ["9B", "27B", "122B", "Muse"])
    d.set_ylabel("mean cos²")
    d.grid(axis="y", color="#eeeeee")
    S.save(fig, "s08_first_sentence_and_label_free", supp=True)


X45D_RUNS = {"9b": "qwen35_9b_x45d", "27b": "x45d_27b", "muse": "muse30b_x45d"}  # 45d (fixed in advance); no 122B run
FORMATS = (("prose", "prose"), ("json", "JSON"), ("table", "table"))


def x45d_verdict(m: str) -> tuple[dict | None, str]:
    """45d's newest verdict for a model (results/x0b_generalize/<run>/x45d-*/verdict.json) and its path, or (None, "")."""
    run = X45D_RUNS.get(m)
    found = sorted((pins.RESULTS_DIR / "x0b_generalize" / run).glob("x45d-*/verdict.json")) if run else []
    return (json.loads(found[-1].read_text()), str(found[-1].relative_to(pins.REPO_ROOT))) if found else (None, "")


def f09_transfer(plt) -> None:
    """(a) Per model, the lookup's extra loss without J++ (black) and without the pointer (orange, fit on simple scenes,
    not refit) in simple scenes, varied scenes by format and natural passages (fact first). (b) 45d (fixed in advance):
    per model and format, the lookup's extra loss without the pointer fit on simple scenes (open) and without a pointer
    refit on that format (filled; fit on half of the varied scenes, measured on the other half), each minus its random
    part; a cell under X0's 30-switch bar is not counted."""
    h = 9.35
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    found = {m: (x45d_verdict(m)[0] or {}).get("verdict", {}).get("outcome") for _, m, _ in S.MODELS}
    found_on = [SHORT[m] for m, o in found.items() if o == "pointer elsewhere"]
    not_on = [SHORT[m] for m, o in found.items() if o is not None and o != "pointer elsewhere"]
    # Dan 27 Oct ~11:20: the title and the subtitle's refit line
    S.title(fig, "The split carries over to other texts; the pointer must be refit for each format",
            "The lookup's extra loss (0-1): switches lost without the part, minus those lost without a random\n"
            f"part (same size); refit pointer found on {' and '.join(found_on)}, not {' and '.join(not_on)}.",
            limit=86)  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(0.01, at(0.95), "(a) The pointer fit on simple scenes, not refit", **head)
    black = "#222222"
    sh, sl = S.status_handles()
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=black, ms=7), plt.Line2D([], [], marker="o", ls="", color=S.COL["position"], ms=7), *sh],
           ["without the J++ part", "without the pointer (fit on simple scenes)", *sl], at(1.2))  # fmt: skip
    grid_a = fig.add_gridspec(1, 4, left=0.17, right=0.985, top=at(2.3), bottom=at(4.85), wspace=0.12)
    axes = [fig.add_subplot(grid_a[0, j]) for j in range(4)]
    n_sw, n_nat = N.get("nat_lk_whole_sw_muse"), N.get("nat_n_muse")
    for ax, (target, m, _) in zip(axes, S.MODELS, strict=True):
        S.extra_axis(ax)
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        cells = transfer_cells(target)
        for i, sc in enumerate(SCENES):
            for part, col, dy in (("jpp", black, 0.17), ("alf", S.COL["position"], -0.17)):
                v = cells.get((sc, part))
                kind = "x5" if sc == "natural" else "x0b"
                if (sc, part, m) == ("natural", "jpp", "muse"):  # 10 of 60 passages switch: no J++ point (as Fig. 1b)
                    ax.text(-0.18, -i + dy + 0.12, f"too few switches\n({n_sw} of {n_nat})", fontsize=S.FONT,
                            color=black, va="center", style="italic", linespacing=1.0)  # fmt: skip
                    continue
                if v is None:
                    if part == "alf" and sc != "simple":
                        why = "not tested\n(gate)" if cells.get((kind, "gate")) else "not run"
                        ax.text(0.3, -i + dy, why, fontsize=S.FONT, color=S.COL["muted"], va="center", linespacing=1.0)
                    continue
                after = part == "jpp" and cells.get((kind, "after"))
                S.dot(ax, 0, -i + dy, v, col, "after" if after else "fixed", size=6.5)
                if after:
                    ax.text(v[2] + 0.04, -i + dy, S.LOWERED, va="center", fontsize=S.FONT)
                S.record("fig09", target, f"lookup extra loss without {'J++' if part == 'jpp' else 'the pointer'}: {sc}", *v,
                         source="readme_story_figures.transfer_cells")  # fmt: skip
        ax.set_ylim(-len(SCENES) + 0.4, 0.6)
        ax.tick_params(axis="y", length=0)
        ax.set_yticks([-i for i in range(len(SCENES))],
                      ["simple scenes", "prose", "JSON", "table", "natural\npassages"] if ax is axes[0] else [])  # fmt: skip

    fig.text(0.01, at(5.65), "(b) The pointer refit per format, fixed in advance", **head)
    fig.text(0.01, at(5.92), "Varied scenes: fit on half of them, measured on the other half.", fontsize=S.FONT,
             color=S.COL["muted"], va="top")  # fmt: skip
    orange = S.COL["position"]
    legend(fig, [plt.Line2D([], [], marker="o", ls="", mfc="white", mec=orange, mew=1.6, ms=7),
                 plt.Line2D([], [], marker="o", ls="", color=orange, ms=7)],
           ["without the pointer (fit on simple scenes)", "without the refit pointer"], at(6.25))  # fmt: skip
    grid_b = fig.add_gridspec(1, 4, left=0.17, right=0.985, top=at(7.05), bottom=at(8.75), wspace=0.12)
    for j, (target, m, _) in enumerate(S.MODELS):
        ax = fig.add_subplot(grid_b[0, j])
        S.extra_axis(ax)
        ax.set_title(name_of(m), fontsize=S.FONT, weight="bold")
        v, src = x45d_verdict(m)
        ax.set_ylim(-len(FORMATS) + 0.4, 0.6)
        ax.tick_params(axis="y", length=0)
        ax.set_yticks([-i for i in range(len(FORMATS))], [f[1] for f in FORMATS] if j == 0 else [])
        if v is None:
            S.empty(ax, "not run")
            continue
        cells = {(c["format"], c["part"]): c for c in v["cells"] if c["reader"] == X.LOOKUP}
        for i, (fmt, _) in enumerate(FORMATS):
            refit, simple = cells[(fmt, "pcf")], cells[(fmt, "alf")]
            assert refit["switched_whole"] == simple["switched_whole"], (m, fmt)
            S.record("fig09", target, f"(b) {fmt}: lookup switches with the whole change", refit["switched_whole"],
                     n=refit["n"], source=src)  # fmt: skip
            if not refit["valid"]:  # under X0's bar (S_whole >= 0.3, >= 30 switches): the rule does not count it
                ax.text(0.4, -i, f"not counted\n({refit['switched_whole']} switches)", ha="center", va="center",
                        color=S.COL["muted"], linespacing=1.0)  # fmt: skip
                continue
            for c, kind, dy, what in ((refit, "fixed", 0.17, "the refit pointer"),
                                      (simple, "after", -0.17, "the pointer fit on simple scenes")):  # fmt: skip
                S.dot(ax, 0, -i + dy, tuple(c["excess"]), orange, kind, size=6.5)
                S.record("fig09", target, f"(b) {fmt}: lookup extra loss without {what}", *c["excess"], n=c["n"],
                         source=src)  # fmt: skip
    S.save(fig, "fig09_transfer")


LEFT_RUNS = {"9b": ("qwen35_9b_x6_routes_bothoff", "qwen35_9b_x6_routes_d1", "qwen35_9b_x6_routes_x45e_dom"),
             "27b": ("x6_routes_bothoff_27b", "x6_routes_d1_27b", "x6_routes_x45e_27b_dom"),
             "122b": ("qwen35_122b_x6_routes_bothoff_g75", None, None),
             "muse": ("muse30b_x6_routes", "muse30b_x6_routes_d1_r2", "muse30b_x6_routes_x45e_dom")}  # fmt: skip
# the 122B's 45e job (identity arms only, gate 0.75): its identity row once LANDED["45e_122b"] names the run; it has no
# wrong-pair control, so that cell is "not tested" whatever lands (Dan ~01:05)
NO_WRONG_PAIR = {"122b"}
# the third row (45e, fixed in advance): the wrong pair in place of identity outside J++, at its share of the change
LEFT_PARTS = (("both", "J++ part\n+ pointer"), ("jpp+alf+idout", "+ identity\noutside J++"),
              ("jpp+alf+wrong", "+ wrong pair\ninstead"))  # fmt: skip
SIZE_AT = 0.9  # Dan ~01:05: the wrong-pair bar on the scenes where the control reached at least 0.9 of idout's share


def left_runs(m: str) -> tuple[str | None, ...]:
    """Fig. 10's run per row for a model; the 122B's identity row from LANDED["45e_122b"] once it is set."""
    runs = LEFT_RUNS[m]
    if m == "122b" and LANDED.get("45e_122b"):
        return (runs[0], LANDED["45e_122b"], None)
    return runs


def matched_wrong_cell(run: str, n_boot: int = X.N_BOOT) -> dict:
    """45e's wrong-pair row on the scenes where the control reached at least SIZE_AT of identity outside J++'s share
    (x45e_size_check.matched on the run's norms.jsonl): the sanity swap's lookup cell (X.cell: Jdep, Rdep, extra loss)
    of J++ + the pointer + the wrong pair against its random part of the same share, its median share and n. Its point
    must equal the size check's (results/x6_routes/x45e-size-*/size.json, matched c0.left.no_jppalfwrong)."""
    from scripts import x45e_size_check as Z

    src = pins.RESULTS_DIR / "x6_routes" / run
    norms = X.read_jsonl(src / "norms.jsonl")
    keep = Z.matched(norms, SIZE_AT)
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl")
            if r["scene"] in keep and r["condition"] == "C0" and r["reader"] == X.LOOKUP]  # fmt: skip
    arms = ("whole", "no_jppalfwrong", "no_jppalfwrong_rand")
    by = {a: {r["scene"]: r for r in rows if r["arm"] == a} for a in arms}
    scenes = sorted(set.intersection(*(set(v) for v in by.values())))
    sw = {
        k: [int(by[a][s]["switched"]) for s in scenes]
        for k, a in zip(("whole", "no_part", "no_rand"), arms, strict=True)
    }
    c = X.cell(sw, [by["whole"][s]["entity"] for s in scenes], n_boot)
    share = [n["share_jpp+alf+wrong"] for n in norms if n["condition"] == "C0" and n["scene"] in keep]
    size = latest(pins.RESULTS_DIR / "x6_routes", "x45e-size-*/size.json")
    ref = next(v for v in (size or {}).get("models", {}).values() if v["run"] == run)["matched"]["c0"]
    assert ref["n"] == len(scenes), (run, ref["n"], len(scenes))
    assert abs(ref["left"]["no_jppalfwrong"][0] - (1 - c["Jdep"][0])) < 1e-9, (run, ref["left"], c["Jdep"])
    return {**c, "share": float(np.median(share)), "n": len(scenes)}


def f10_left(plt, matched: bool = True) -> None:
    """The sanity swap, one panel per model (as Figs. 8 and 9), one row per removal: J++ and the pointer (the both-removed
    runs), identity outside J++ removed too (batch 40), and a wrong pair in its place (45e; matched: on the scenes where
    the control reached at least 0.9 of identity outside J++'s share, Dan ~01:05; else every scene, figures/supp/s10b).
    Per row, the share of the whole change's lookup switches still switching with the part removed (purple) and with a
    random part of the same size removed (grey), joined by a line: its length is the part's extra loss. The part's
    median share of the change and n under the row. The subtitle: 45e's condition (ii) on the same scenes."""
    fig_id = "fig10" if matched else "s10b"
    h = 5.6
    fig, axes = plt.subplots(1, 4, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.17, right=0.985, top=1 - 1.75 / h, bottom=1.5 / h, wspace=0.12)
    size = latest(pins.RESULTS_DIR / "x6_routes", "x45e-size-*/size.json") if matched else None
    if matched:
        assert size is not None, "no 45e size check in results/x6_routes"
        by_m = {m: size["models"][t]["matched"]["c2"]["idout_vs_wrong"] for t, m, _ in S.MODELS if t in size["models"]}
        cut = {m: tuple(v) for m, v in by_m.items()}
        src_cut = {m: "results/x6_routes/" + sorted((pins.RESULTS_DIR / "x6_routes").glob("x45e-size-*"))[-1].name
                   for m in cut}  # fmt: skip
        scenes = (f"Wrong pair: mean differences of other item pairs, on the scenes where it reached at least {SIZE_AT} of "
                  "identity outside J++'s share. In the routes test, identity outside J++ cuts identity ")  # fmt: skip
    else:
        cut = {m: interval(f"x45e_cut_{m}") for m in ("9b", "27b", "muse")}
        src_cut = {m: f"x45e_cut_{m}" for m in cut}
        scenes = ("Wrong pair: mean differences of other item pairs, at the share of identity outside J++, every scene. "
                  "In the routes test, identity outside J++ cuts identity ")  # fmt: skip
    # Dan's title (~22:40): 84 characters, 11.0 pt
    S.title(fig, "J++ part, pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's",
            "Sanity swap: lookups still switching (%) of the whole change's switches; purple line: the part's extra loss.\n"
            f"Under each row: the part's share of the change and n. Open marks, {S.LOWERED}: after the data, gate lowered to 0.75.",
            limit=90)  # fmt: skip
    fig.text(0.01, 0.1 / h, textwrap.fill(scenes + f"answers only {cut['9b'][0]:.2f} / {cut['27b'][0]:.2f} / "
             f"{cut['muse'][0]:.2f} more than the wrong pair (9B / 27B / Muse; the bar fixed in advance: 0.15).", 108),
             color=S.COL["muted"], va="bottom")  # fmt: skip
    for m, v in cut.items():
        what = " (scenes where the wrong pair reached 0.9 of its share)" if matched else ""
        S.record(fig_id, next(t for t, k, _ in S.MODELS if k == m), "routes test: identity answers cut by identity "
                 f"outside J++ beyond the wrong pair{what}", *v, source=src_cut[m])  # fmt: skip
    grey = "#a8a8a8"
    for ax, (target, m, _name) in zip(axes, S.MODELS, strict=True):
        ax.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        ax.set_xlim(0, 112)  # a random part can leave more switches than the whole change (Muse: 105%)
        ax.set_xticks(*PCT)
        ax.axvline(100, color="#cccccc", lw=0.8, ls="--", zorder=0)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_axisbelow(True)
        kind = "after" if m in LOWERED_M else "fixed"
        for k, (part, label) in enumerate(LEFT_PARTS):
            y = -k
            if part == "jpp+alf+wrong" and m in NO_WRONG_PAIR:
                ax.text(56, y, "– not tested", ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"])
                continue
            run = left_runs(m)[k]
            wrong = part == "jpp+alf+wrong" and matched and run is not None
            v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json") if run else None
            e = matched_wrong_cell(run) if wrong and run else next(
                (e for e in (v or {}).get("extra", []) if e["condition"] == "C0" and e["reader"] == X.LOOKUP
                 and e["part"] == part), None)  # fmt: skip
            if e is None or run is None:
                ax.text(56, y, "not run", ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"])
                continue
            where = f" (scenes where it reached {SIZE_AT} of identity's share)" if wrong else ""
            pts = {}
            for lost, col, what in ((e["Jdep"], S.COL["lookup"], "the part"),
                                    (e["Rdep"], grey, "a random part of the same size")):  # fmt: skip
                left = (1 - lost[0], 1 - lost[2], 1 - lost[1])
                pts[col] = left
                S.record(fig_id, target, f"sanity swap, lookups still switching without {label.replace(chr(10), ' ')}"
                         f"{where}: {what}", *left, n=e["n"] if wrong else None, source=run)  # fmt: skip
            ax.plot([100 * pts[grey][0], 100 * pts[S.COL["lookup"]][0]], [y, y], color=S.COL["lookup"], lw=2.2,
                    alpha=0.35, zorder=2)  # fmt: skip
            for col, left in pts.items():
                ax.plot([100 * left[1], 100 * left[2]], [y, y], color=col, lw=1.6, zorder=3, solid_capstyle="butt")
                face = col if kind == "fixed" else "white"
                ax.plot([100 * left[0]], [y], "o", ms=8, mfc=face, mec=col, mew=1.6, zorder=4)
            ax.text(2, y - 0.34, f"{100 * e['share']:.0f}%, n {e['n']}", ha="left", va="center", fontsize=S.FONT,
                    color=S.COL["muted"])  # fmt: skip
            S.record(fig_id, target, f"share of the change: {label.replace(chr(10), ' ')}{where}", round(e["share"], 4),
                     source=run)  # fmt: skip
        ax.set_ylim(-len(LEFT_PARTS) + 0.45, 0.45)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks([-k for k in range(len(LEFT_PARTS))], [label for _, label in LEFT_PARTS])
    fig.text(0.58, 1.0 / h, "lookups still switching (%)", ha="center", va="center")
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=8),
                 plt.Line2D([], [], marker="o", ls="", color=grey, ms=8)],
           ["without the part", "without a random part (same size)"], 1 - 0.95 / h)  # fmt: skip
    S.save(fig, "fig10_what_is_left" if matched else "s10b_what_is_left_all_scenes", supp=not matched)


def s10b_all_scenes(plt) -> None:
    """Supplementary to Fig. 10: the wrong pair on every scene (the 45e run as scored)."""
    f10_left(plt, matched=False)


# Fig. 11 v4 (Dan ~16:45): the claims in story order; status per model, read off the verdicts and the README's numbers
# (agent's reading, UNVERIFIED); "a" = after the data (or a gate lowered after the data). Fig. 11 v5 carries these cells
# over where Dan (27 Oct ~00:30) does not restate them.
SCORECARD_V4 = (
    ("The split (main test)", {"9b": ("held", 0), "27b": ("partial", 0), "122b": ("held", 0), "muse": ("held", 0)}),
    ("The split on the logit difference", {"9b": ("held", 0), "27b": ("held", 0), "122b": ("held", 0), "muse": ("held", 0)}),
    ("The split in varied scenes", {"9b": ("held", 0), "27b": ("held", 0), "122b": ("partial", 0), "muse": ("held", 0)}),
    ("The split in natural passages", {"9b": ("held", 1), "27b": ("partial", 0), "122b": ("held", 0),
                                       "muse": ("not tested", 0)}),
    ("Never the value", {"9b": ("held", 0), "27b": ("held", 0), "122b": ("held", 1), "muse": ("held", 0)}),
    ("The lookup needs the pointer", {"9b": ("held", 0), "27b": ("partial", 1), "122b": ("held", 1), "muse": ("held", 0)}),
    ("Only the pointer gives\nposition answers", {"9b": ("held", 0), "27b": ("no", 0), "122b": ("held", 1), "muse": ("held", 0)}),
    ("A write moves the lookup", {"9b": ("held", 1), "27b": ("partial", 1), "122b": ("held", 1), "muse": ("held", 1)}),
    ("The recall follows the write", {"9b": ("held", 1), "27b": ("partial", 1), "122b": ("held", 1), "muse": ("partial", 1)}),
    ("First-mentioned item,\nnot position in the text", {"9b": ("held", 0), "27b": ("held", 1), "122b": ("held", 1),
                                                          "muse": ("held", 1)}),
    ("The pointer transfers", {"9b": ("no", 0), "27b": ("no", 0), "122b": ("no", 0), "muse": ("no", 0)}),
)  # fmt: skip
V4_CELL = {"held": "ok", "partial": "~", "no": "x", "not tested": "-"}
# figures/story/scorecard.csv's cells: ok / ~ / x / - (not run, or too few switches: flag *) / pending; flag a = after
# the data. Its columns (Dan ~00:30): claim, model, cell, flag, data.csv key ("numbers:<x0_numbers key>" or
# "<figure>:<quantity>", the row of figures/story/data.csv that carries the cell's number for that model)
CELL_SYMBOL = {"ok": ("✓", "#2f7d4f"), "~": ("~", "#b07a0a"), "x": ("✗", "#b8433a"), "-": ("–", "#8a8a8a"),
               "pending": ("○", "#8a8a8a")}  # fmt: skip
SC_FIELDS: tuple[str, ...] = ("claim", "model", "cell", "flag", "data.csv key")


def split_verdict(lk: float, gap: float) -> str:
    """The split on one model by 45m's two bars (point estimates), in three levels as Fig. 11 v4 read the main test: ok
    if the gap is at least 0.3 and the lookup at most 0.10; ~ if only the lookup misses its bar; x if the gap misses."""
    if gap < GAP_BAR:
        return "x"
    return "ok" if lk <= LOOKUP_BAR else "~"


def scorecard_rows() -> list[dict]:
    """Fig. 11 v5's rows (Dan, 27 Oct ~00:30), grouped. Cells carried over from SCORECARD_V4 where Dan does not restate
    them; Dan's restated cells checked against their rule wherever the rule is in the result files (an assert); two rows
    computed by a stated reading (agent's, UNVERIFIED): 'locker before the pick' by split_verdict on the main test's
    locker-before cells (the same reading gives v4's main-test row and Dan's 45m row), 'never the value without the chat
    template' as the value share of the routes runs without the template (45i, descriptive) being 0."""
    v4 = {claim: {m: (V4_CELL[s], "a" if a else "") for m, (s, a) in cells.items()} for claim, cells in SCORECARD_V4}
    num = interval
    keys = [m for _, m, _ in S.MODELS]

    # Split
    main = {m: (split_verdict(num(f"lk_excess_{m}")[0], num(f"contrast_{m}")[0]), "") for m in keys}
    assert main == v4["The split (main test)"], (main, v4["The split (main test)"])
    before = {
        m: (split_verdict(num(f"sbo_swap_before_lk_{m}")[0], num(f"sbo_swap_before_gap_{m}")[0]), "a") for m in keys
    }
    clean_dan = {"9b": "x", "27b": "ok", "122b": "-", "muse": "ok"}
    clean = {m: ((split_verdict(num(f"x45m_before_lk_{m}")[0], num(f"x45m_before_gap_{m}")[0]), "")
                 if N.get(f"x45m_before_gap_{m}") else ("-", "")) for m in keys}  # fmt: skip
    assert {m: c for m, (c, _) in clean.items()} == clean_dan, clean
    natural = dict(v4["The split in natural passages"])
    natural["muse"] = ("-", "*")  # too few switches (the footnote)

    # Routes: without the chat template (45i's routes runs, descriptive)
    nochat = {}
    for target, m, _ in S.MODELS:
        run = {"9b": "qwen35_9b_x6_routes_x45i_nochat", "27b": "x6_routes_x45i_nochat_27b"}.get(m)
        v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json") if run else None
        r = next((r for r in (v or {}).get("rows", []) if r["condition"] == "C2" and r["arm"] == "whole"), None)
        if r is None or run is None:
            nochat[m] = ("-", "")
            continue
        S.record("fig11", target, "routes test without the chat template, another item moved, whole: value share",
                 *r["share"]["value"], n=r["n"], source=run)  # fmt: skip
        nochat[m] = ("ok" if r["share"]["value"][0] == 0 else "x", "a")

    # Pointer: 45a (Dan's reading, after the data), 45d's verdicts, the transfer row (Dan: x on all, as v4)
    pick_first = {"9b": ("ok", "a"), "27b": ("ok", "a"), "122b": ("-", ""), "muse": ("~", "a")}
    refit = {}
    for m in keys:
        v, _ = x45d_verdict(m)
        refit[m] = ("-" if v is None else "ok" if v["verdict"]["outcome"] == "pointer elsewhere" else "x", "")
    assert {m: c for m, (c, _) in refit.items()} == {"9b": "ok", "27b": "x", "122b": "-", "muse": "ok"}, refit
    transfer = {m: ("x", "") for m in keys}
    assert transfer == v4["The pointer transfers"], v4["The pointer transfers"]

    # Limits: 45e (both conditions -> ok, one -> ~, none -> x), 45g rule b (main test), 45b on the clean items
    x45e = latest(pins.RESULTS_DIR / "x6_routes", "x45e-*/x45e.json") or {"flags": {}}
    by_target = {x45e["runs"][run]: f for run, f in x45e["flags"].items()}
    specific = {}
    for target, m, _ in S.MODELS:
        f = by_target.get(target)
        held = (f["holds_i"], f["holds_ii"]) if f else None
        specific[m] = ("pending" if held is None else "ok" if all(held) else "~" if any(held) else "x", "")
    if LANDED.get("45e_122b"):  # the 122B's 45e job: identity arms only, no wrong-pair control: not tested here
        specific["122b"] = ("-", "")
    assert {m: c for m, (c, _) in specific.items()} == {"9b": "~", "27b": "~", "122b": "-", "muse": "x"}, specific
    g45 = latest(pins.RESULTS_DIR / "x0_massmean", "score45g-*/score.json") or {"runs": {}}
    swap = {r["model"]: r["clauses"]["b"] for r in g45["runs"].values() if r["scene_set"] == "two people swap"}
    only_jpp = {m: ("pending" if t not in swap else "ok" if swap[t] else "x", "") for t, m, _ in S.MODELS}
    assert {m: c for m, (c, _) in only_jpp.items()} == {"9b": "ok", "27b": "ok", "122b": "ok", "muse": "ok"}
    # 45b (the main test's locker-after items) is no longer a row (Dan 27 Oct ~11:20): a design error, the changed
    # prompt differs after the bridge word there; 45q on the clean scenes is the row
    # 45k (fixed in advance; Q45.9 scored on the 27B): none of the three tested causes holds -> x on the 27B; the 9B
    # is its control and Muse is reported, not counted (Fig. 2b): not tested in this row
    x45k = latest(pins.RESULTS_DIR / "x6_routes", "x45k-*/x45k.json") or {}
    k_out = x45k.get("q45_9", {}).get("outcome")
    k_cause = {m: ("-", "") for m in keys}
    if k_out:
        k_cause["27b"] = ("x" if k_out == ["(d) can't tell"] else "ok", "")
    assert k_cause["27b"] == ("x", ""), k_out
    # after the overnight queue: 45q and 45p (fixed in advance; their verdicts per model), 45i' (after the data, gate
    # 0.75: the split's reading as above on the no-template main test)
    q_v = (
        json.loads((pins.RESULTS_DIR / LANDED["45q"]["verdict"] / "x45q.json").read_text()) if LANDED.get("45q") else {}
    )
    q_by = {mod["model"]: mod for mod in q_v.get("models", [])}
    link_clean = {m: ("-" if "holds" not in q_by.get(t, {}) else "ok" if q_by[t]["holds"] else "x", "")
                  for t, m, _ in S.MODELS}  # fmt: skip
    p_v = json.loads((pins.RESULTS_DIR / LANDED["45p"] / "x45p.json").read_text()) if LANDED.get("45p") else {}
    p_by = {mod["target"]: mod for mod in p_v.get("models", [])}
    earlier = {m: ("-" if p_by.get(t, {}).get("status") != "tested" else "ok" if p_by[t]["holds"] else "x", "")
               for t, m, _ in S.MODELS}  # fmt: skip
    no_tpl = {m: (split_verdict(num(f"x45ig_lk_{m}")[0], num(f"x45ig_gap_{m}")[0]), "a") if N.get(f"x45ig_gap_{m}")
              else ("-", "") for m in keys}  # fmt: skip
    if LANDED.get("45q"):
        assert {m: c for m, (c, _) in link_clean.items()} == {"9b": "ok", "27b": "ok", "122b": "-", "muse": "ok"}
    if LANDED.get("45p"):
        assert {m: c for m, (c, _) in earlier.items()} == {"9b": "ok", "27b": "ok", "122b": "-", "muse": "ok"}

    nat_key = {"9b": "numbers:natg75_gap_9b", "muse": "numbers:nat_lk_whole_sw_muse"}
    spec = (  # group, claim (the figure's row label), cells (model key -> (cell, flag)), data.csv key per model
        ("Split", "main test", main, lambda m: f"numbers:contrast_{m}"),
        ("Split", "a tested cause for the 27B's loss with 100 directions", k_cause,
         lambda m: "fig02b:45k: identity answers' fall from 25 to 100 directions beyond the random part (another item moved)"),
        ("Split", "locker before the pick", before, lambda m: f"numbers:sbo_swap_before_gap_{m}"),
        ("Split", "clean one-pick scenes", clean, lambda m: f"numbers:x45m_before_gap_{m}"),
        ("Split", "logit difference", v4["The split on the logit difference"], lambda m: f"numbers:ld_gap_{m}"),
        ("Split", "varied scenes", v4["The split in varied scenes"], lambda m: f"numbers:x0b_c_{m}"),
        ("Split", "natural passages", natural, lambda m: nat_key.get(m, f"numbers:nat_gap_{m}")),
        ("Split", "without the chat template", no_tpl, lambda m: f"numbers:x45ig_gap_{m}"),
        # the routes rows cite s05 (every model, every arm): v6's Fig. 5 drops the 122B and the keep-only arms
        ("Routes", "never the value", v4["Never the value"],
         lambda m: "s05:another item moved, whole: value share"),
        ("Routes", "never the value without the chat template", nochat,
         lambda m: "fig11:routes test without the chat template, another item moved, whole: value share"),
        ("Pointer", "the lookup needs it", v4["The lookup needs the pointer"],
         lambda m: "s05:another item moved, no_alf: position share"),
        ("Pointer", "only it gives position answers", v4["Only the pointer gives\nposition answers"],
         lambda m: "s05:another item moved, keep_alf: position share"),
        ("Pointer", "a write moves the lookup", v4["A write moves the lookup"],
         lambda m: "fig07:lookup target share, mean over locker pairs, s = 4"),
        ("Pointer", "the recall follows the write", v4["The recall follows the write"],
         lambda m: "fig07:recall changed under the strongest write (s = 4): the written locker's item"),
        ("Pointer", "counts mentions, not text position", v4["First-mentioned item,\nnot position in the text"],
         lambda m: "s08b:(c) neutral sentence B1: the code's shift in positions"),
        ("Pointer", "a pick sentence first moves the lookup to identity", pick_first,
         lambda m: "fig08:45a, first-locker moves, whole change, a pick naming the first-locker item: identity share"),
        ("Pointer", "refit per format", refit, lambda m: "fig09:(b) prose: lookup extra loss without the refit pointer"),
        ("Pointer", "the pointer fit on simple scenes transfers", transfer, lambda m: f"numbers:tptr_pooled_{m}"),
        ("Limits", "identity outside J++ is specific", specific, lambda m: f"numbers:x45e_cut_{m}"),
        ("Limits", "the recall needs only the J++ part, locker after the pick", only_jpp,
         lambda m: "fig03:(b) main test (two people swap picks), locker after the pick: recall extra loss"),
        ("Limits", "the recall reads the earlier mention, locker before the pick", earlier,
         lambda m: f"numbers:x45p_d23_{m}"),
        ("Limits", "the link sits in the locker sentences, clean one-pick scenes", link_clean,
         lambda m: f"numbers:x45q_c_{m}"),
    )  # fmt: skip
    rows = []
    for group, claim, cells, key in spec:
        for target, m, name in S.MODELS:
            cell, flag = cells[m]
            has_number = cell not in ("-", "pending") or flag == "*"
            rows.append({"group": group, "claim": claim, "model": name, "target": target, "cell": cell, "flag": flag,
                         "data.csv key": key(m) if has_number else ""})  # fmt: skip
    return rows


def check_scorecard_keys(path: Path) -> None:
    """Every data.csv key in scorecard.csv names a row that exists: an x0_numbers key, or a recorded (figure, quantity)
    for that model."""
    names = {name: target for target, _, name in S.MODELS}
    recorded = {(r["figure"], r["model"], r["quantity"]) for r in S.ROWS}
    with path.open() as f:
        for r in csv.DictReader(f):
            key = r["data.csv key"]
            if not key or r["model"] not in names:
                continue
            fig_id, quantity = key.split(":", 1)
            ok = quantity in N if fig_id == "numbers" else (fig_id, names[r["model"]], quantity) in recorded
            assert ok, f"scorecard.csv: no data.csv row for {r['claim']!r} / {r['model']}: {key!r}"


WRAP_SC = 50  # Fig. 11's claim labels: one line each where it fits (the label column is half the width)


def f11_scorecard(plt) -> None:
    """figures/story/scorecard.csv (written here from scorecard_rows; rows of other models already in the file are kept,
    so more models can be added as columns) drawn as the scorecard: rows = claims in story order, grouped; columns = the
    file's models (ours first); a symbol per cell and a small 'a' for after the data."""
    rows = scorecard_rows()
    path = S.OUT / "scorecard.csv"
    ours = {name for _, _, name in S.MODELS}
    kept = []
    if path.exists():
        with path.open() as f:
            kept = [r for r in csv.DictReader(f) if r["model"] not in ours]
    S.OUT.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(SC_FIELDS))
        w.writeheader()
        w.writerows([{k: r[k] for k in SC_FIELDS} for r in rows] + kept)
    with path.open() as f:
        table = list(csv.DictReader(f))
    claims = list(dict.fromkeys(r["claim"] for r in rows))  # story order
    groups = {r["claim"]: r["group"] for r in rows}
    unknown = {r["claim"] for r in table} - set(claims)
    assert not unknown, f"scorecard.csv claims without a group in readme_story_figures.scorecard_rows: {unknown}"
    models = list(dict.fromkeys([name for _, _, name in S.MODELS] + [r["model"] for r in table]))
    cells = {(r["claim"], r["model"]): (r["cell"], r["flag"], r["data.csv key"]) for r in table}
    target_of = {name: target for target, _, name in S.MODELS}

    ys, y, last = {}, 0.0, None  # a heading row before each group; a two-line label gets a taller row
    heads, half = [], {}
    for claim in claims:
        if groups[claim] != last:
            heads.append((groups[claim], y))
            y -= 1.0
            last = groups[claim]
        half[claim] = 0.75 if "\n" in textwrap.fill(claim, WRAP_SC) else 0.5
        y -= half[claim] - 0.5
        ys[claim] = y
        y -= half[claim] + 0.5
    h = 1.25 + 0.3 * (-y) + 0.45
    fig, ax = plt.subplots(figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.5, right=0.99, top=1 - 1.45 / h, bottom=0.42 / h)
    S.title(fig, "What held where",
            "✓ held   ~ partial   ✗ no   – not tested*   ○ pending;   a: after the data")  # fmt: skip
    n_sw, n = N.get("nat_lk_whole_sw_muse"), N.get("nat_n_muse")
    fig.text(0.01, 0.12 / h, f"*Not run or not counted; Muse, natural passages: the lookup has too few switches ({n_sw} of {n}).",
             color=S.COL["muted"])  # fmt: skip
    for j, name in enumerate(models):
        ax.text(j, 0.55, textwrap.fill(name.replace("-", " "), 8), ha="center", va="bottom", fontsize=S.FONT, weight="bold",
                linespacing=1.0)  # fmt: skip
        for claim in claims:
            got = cells.get((claim, name))
            if got is None:
                continue
            cell, flag, key = got
            sym, col = CELL_SYMBOL[cell]
            ax.text(j, ys[claim], sym, ha="center", va="center", fontsize=S.FONT + 4, color=col, weight="bold")
            if flag:
                ax.text(j + 0.17, ys[claim] + 0.1, flag, ha="left", va="center", fontsize=S.FONT,
                        color=S.COL["muted"])  # fmt: skip
            src = ("after the data" if "a" in flag else "fixed") + (f"; {key}" if key else "")
            S.record("fig11", target_of.get(name, name), claim, cell, source=src)
    for k, claim in enumerate(claims):
        if k % 2 == 0:
            ax.axhspan(ys[claim] - half[claim], ys[claim] + half[claim], color="#f6f6f6", lw=0, zorder=0)
    tr = blend(fig, ax)
    for group, gy in heads:
        ax.text(0.01, gy - 0.1, group, transform=tr, fontsize=S.FONT + 1, weight="bold", va="center")
    ax.set_xlim(-0.5, len(models) - 0.5)
    ax.set_ylim(y + 0.5, 0.5)
    ax.set_yticks([ys[c] for c in claims], [textwrap.fill(c, WRAP_SC) for c in claims])
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    S.save(fig, "fig11_scorecard")


def probe_rows() -> None:
    """data.csv only, no figure (batch 47 amendment 1, item 2): the x0_probe v4 probes at the bridge word on four
    models, probe.<value|slot|identity>.<9b|27b|122b|muse>.<locker-first|locker-after> with the stored interval and n,
    and their baselines probe.<target>.<majority|layout>.<model>.<order> and probe.<target>.chance.<model>."""
    from scripts import x0_details as XD

    for m in XD.PROBES_V4:
        src, rows = XD.probe_v4_rows(m)
        target = XD.MODELS[m][0]
        for o, stratum in XD.PROBE_ORDERS.items():
            for t, name in XD.PROBE_TARGETS.items():
                r = rows[(name, stratum)]
                S.record("probe", target, f"probe.{t}.{m}.locker-{o}", *r["probe"], n=r["n"], source=src)
                S.record("probe", target, f"probe.{t}.majority.{m}.locker-{o}", *r["majority"], n=r["n"], source=src)
                if r.get("layout"):
                    S.record("probe", target, f"probe.{t}.layout.{m}.locker-{o}", *r["layout"], n=r["n"], source=src)
                if o == "first":
                    S.record("probe", target, f"probe.{t}.chance.{m}", r["chance"], source=src)


VERBAL_SUMMARY = S.REPO / "results" / "x47_verbal" / "summary-20261028T033646Z"  # 47.0, descriptive (no question)


def f07b_verbal(plt) -> None:
    """Fig. 7b: 47.0, read through the J++ lens a pointer write looks like a random draw of the same size."""
    from scripts import story_b47b as B47

    B47.build_47_0(VERBAL_SUMMARY, "fig07b_verbal", out_dir=S.OUT)


def latest_verdict(pattern: str) -> Path:
    """The newest verdict folder under results/ matching pattern (each verdict run writes a new folder)."""
    found = sorted((S.REPO / "results").glob(pattern))
    assert found, f"no verdict folder results/{pattern}"
    return found[-1]


ANATOMY_ORDER = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")  # v6: 9B, 27B, Muse (the 122B in supplements)
# 47.8's bars for its l_probe and l_P (scripts/x47_anatomy.py's L_PROBE_BAR, L_P_BAR), for the legend's words only:
# the marked layers are the verdict's rules
PROBE_BAR, POSITION_BAR = 0.80, 0.20


def f06b_anatomy(plt) -> None:
    """Fig. 6b (E12): 47.8 (fixed in advance), per tested model, the lookup's answers under the whole change at each
    sampled layer (identity / position stacked, the original answer empty, the value as a row of 0s under the bars),
    each share's 95% interval; the recall's switches as a line with its band; the not-interpretable shading where the
    lookup's whole change switches < S.NI_SWITCH; marks at the layer where the locker probe first reaches 0.8 (rules
    l_probe: the address is formed), where position answers start (l_P: the address is used) and at L. One panel per
    model, x = layer index. The full sweep (parts, probes) is the verdict folder's x47_anatomy.png."""
    vdir = latest_verdict("x47_anatomy/x47_8-*")
    src = str((vdir / "x47_8.json").relative_to(S.REPO))
    tested = {
        m["target"]: m for m in json.loads((vdir / "x47_8.json").read_text())["models"] if m["status"] == "tested"
    }
    models = [tested[t] for t in ANATOMY_ORDER if t in tested]
    assert 0 < len(models) <= 2, f"v6: at most two panels, got {list(tested)}"
    fig, axes = plt.subplots(1, len(models), figsize=(S.WIDTH, 5.0), sharey=True, squeeze=False)
    fig.subplots_adjust(left=0.085, right=0.985, top=0.64, bottom=0.14, wspace=0.10)
    S.title(fig, "The address forms early; the lookup goes by identity, then by position",
            "Bars: lookup answers under the whole change at one layer; line: recall switches; whiskers, bands: 95%.")  # fmt: skip
    w = 0.78
    for ax, m in zip(axes[0], models, strict=True):
        layers, target, rules = m["layers"], m["target"], m["rules"]
        cells = [m["cells"][str(la)] for la in layers]
        name = next(lab for t, _, lab in S.MODELS if t == target)
        x = np.arange(len(layers))
        ni = [c["lookup"]["switch"]["whole"][0] < S.NI_SWITCH - 1e-9 for c in cells]
        assert ni == [not c["lookup"]["interpretable"] for c in cells], f"{target}: the shading disagrees with 47.8"
        S.not_interpretable(ax, S.spans(ni))
        bottom = np.zeros(len(layers))
        for rt in ("identity", "position"):
            sh = np.array([c["lookup"]["share"]["whole"][rt] for c in cells])
            ax.bar(x, sh[:, 0], bottom=bottom, color=S.COL[rt], width=w, zorder=2)
            off = -0.17 if rt == "identity" else 0.17
            ax.vlines(x + off, bottom + sh[:, 1], bottom + sh[:, 2], color="#1e1e1e", lw=0.9, zorder=3)
            bottom += sh[:, 0]
        ax.bar(x, 1 - bottom, bottom=bottom, width=w, zorder=2, **S.EMPTY)  # the original answer (and other)
        for la, c in zip(layers, cells, strict=True):
            for rt in ("identity", "position", "value", "original"):
                S.record("fig06b", target, f"layer {la}: lookup {rt} share (whole change)", *c["lookup"]["share"]["whole"][rt],
                         n=c["lookup"]["n"], source=src)  # fmt: skip
        # the value: a row of its shares under the bars, shown even at 0
        for xi, c in zip(x, cells, strict=True):
            v = c["lookup"]["share"]["whole"]["value"][0]
            ax.text(xi, -0.075, f"{v:.0f}" if v == 0 else f"{v:.2f}", ha="center", va="center", fontsize=S.FONT,
                    color=S.COL["value"])  # fmt: skip
        rc = np.array([c["recall"]["switch"]["whole"] for c in cells])
        ax.fill_between(x, rc[:, 1], rc[:, 2], color=S.COL["recall"], alpha=0.18, lw=0, zorder=4)
        ax.plot(x, rc[:, 0], color=S.COL["recall"], marker="D", ms=4.5, lw=1.8, zorder=5)
        for la, c in zip(layers, cells, strict=True):
            S.record("fig06b", target, f"layer {la}: recall switch (whole change)", *c["recall"]["switch"]["whole"],
                     n=c["recall"]["n"], source=src)  # fmt: skip
        # probe before use: where the address is formed (locker probe >= 0.8) and where it is used (position answers
        # start), labelled above the panel; L under the layer axis
        marks = (("address\nformed", rules["l_probe"], "--"), ("address\nused", rules["l_P"], "-"))
        for label, la, ls in marks:
            S.record("fig06b", target, f"{label.replace(chr(10), ' ')}: layer", la, source=src)
            if la is None:
                continue
            xi = layers.index(la)
            ax.axvline(xi, ymin=0.115, color="#1e1e1e", ls=ls, lw=1.2, zorder=6)
            ax.text(xi, 1.02, label, ha="center", va="bottom", fontsize=S.FONT, color="#1e1e1e", linespacing=1.0)
        li = layers.index(m["layer"])
        ax.text(li, -0.13, "▲\nL", transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=S.FONT - 1,
                weight="bold", color="#1e1e1e", linespacing=0.9)  # fmt: skip
        step = 2 if len(layers) > 10 else 1
        ax.set_xticks(x[::step], [str(la) for la in layers][::step])
        ax.set_xlim(-0.6, len(layers) - 0.4)
        ax.set_xlabel("layer", loc="right", labelpad=6)
        ax.text(0, 1.16, name, transform=ax.transAxes, ha="left", va="bottom", fontsize=12, weight="bold")
        S.panel_tag(ax, str(cells[0]["lookup"]["n"]) + " per layer", "fixed", inside=True)
        ax.set_ylim(-0.13, 1.0)
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.spines[["top", "right"]].set_visible(False)
    axes[0, 0].set_ylabel("share of lookups / recalls")
    axes[0, 0].text(-0.6, -0.075, "value", ha="right", va="center", fontsize=S.FONT, color=S.COL["value"])
    hs = [plt.Rectangle((0, 0), 1, 1, color=S.COL["identity"]), plt.Rectangle((0, 0), 1, 1, color=S.COL["position"]),
          plt.Rectangle((0, 0), 1, 1, **S.EMPTY),
          plt.Line2D([], [], color=S.COL["recall"], marker="D", ms=4.5, lw=1.8),
          plt.Line2D([], [], color="#1e1e1e", ls="--", lw=1.2), plt.Line2D([], [], color="#1e1e1e", lw=1.2)]  # fmt: skip
    legend(fig, hs, ["identity", "position", "original answer", "recall switches",
                     f"address formed: locker probe ≥ {PROBE_BAR:.1f}",
                     f"address used: position ≥ {POSITION_BAR:.1f}"], 0.885, ncol=3)  # fmt: skip
    S.save(fig, "fig06b_anatomy")


# Batch 47/48 figures (28 Oct, after Dan's answers at fca83082): name -> (module, builder, verdict folder, title).
# A title is set where the builder's default, built from the verdict's labels, reads stronger than the data.
BATCH47 = {
    "fig01c_zeroing": ("story_b47a", "build_zero", "x47_zero/x47_5-*", None),
    "fig03d_depth_map": ("story_b47b", "build_d1", "x47_depthmap/depth-*", None),
    "fig05b_identity_outside": ("story_b47a", "build_atoms", "x47_atoms/x47_1-*", None),
    "fig05c_described_bridge": ("story_b47a", "build_cue", "x47_cue/x47_3-*",
                                "A described bridge: the split holds on the 9B and Muse, not on the 27B"),
    "fig07c_probe_errors": ("story_b47a", "build_errors", "x47_errors/x47_13-*", None),
    "fig09b_six_lockers": ("story_b47a", "build_six", "x47_six/x47_2-*", None),
    "fig09c_formation": ("story_b47b", "build_47_6", "x47_edges/x47_6-*",
                         "Blocking the pick sentence from the lockers removes most switches, not only position"),
    "fig06c_address_depth": ("story_b47c", "build_depth", "x47_depth_cpu/persistence-*",
                             "The address is re-encoded early in depth and settles in later layers"),
    "fig09d_chain": ("story_b47c", "build_chain", "x47_chain/x47_14-*", None),
    "fig10b_enrichment": ("story_b48", "build_enrichment", "x48_enrich/x48_2-*",
                         "Without the J++ part the attribute moves only half way; late MLPs are not needed"),
    "fig10c_binding": ("story_b48", "build_binding", "x48_bind/x48_bind-*", None),
    "fig10d_heads": ("story_b48", "build_heads", "x48_heads/x48_heads-*", None),
    "fig10e_second_route": ("story_b48", "build_second_route", "x48_route2/x48_route2-*", None),
}  # fmt: skip
BATCH47_SUPP = {
    "s03e_cumulative": ("story_b47b", "build_47_4", "x47_cumulative/x47_4-*", None),
    "s12_das_muse": ("story_b48", "build_das", "x48_das/verdict-*", None),
}  # fmt: skip


def batch47_figures(plt, figs: dict = BATCH47, supp: bool = False) -> None:
    """The batch 47/48 figures from their newest verdict folders (scripts/story_b47a.py, story_b47b.py, story_b48.py),
    into S.OUT (S.SUPP for the supplementary ones)."""
    import importlib

    out_dir = S.SUPP if supp else S.OUT
    for name, (module, builder, pattern, title) in figs.items():
        build = getattr(importlib.import_module(f"scripts.{module}"), builder)
        kw = {"out_dir": out_dir} if module == "story_b47b" else {}
        if module != "story_b47b" and supp:
            saved, S.OUT = S.OUT, out_dir  # story_b47a / story_b48 save through story_style.save into S.OUT
            try:
                build(latest_verdict(pattern), name, title, **kw)
            finally:
                S.OUT = saved
        else:
            build(latest_verdict(pattern), name, title, **kw)


def batch47_numbers() -> None:
    """Numbers the README cards quote from batch-47 verdicts that have no figure of their own (47.16 on the 9B, 47.7(a)
    on the 27B, 47.10 on the 27B), recorded for data.csv with the verdict json as source."""
    v = latest_verdict("x47_distance/x47_16-*") / "x47_16.json"
    m = next(x for x in json.loads(v.read_text())["models"] if x["status"] == "tested")
    src = str(v.relative_to(S.REPO))
    for k in ("0", "5", "20", "50"):
        S.record("e6_distance", m["target"], f"47.16: position share with {k} neutral sentences", m["position"][k], source=src)
        S.record("e6_distance", m["target"], f"47.16: slot probe with {k} neutral sentences", m["probe"][k], source=src)
        S.record("e6_distance", m["target"], f"47.16: the swap (fit with none) sends lookups to the target, {k} sentences",
                 m["swap_target"][k], source=src)  # fmt: skip
        if k in m["betas"]:
            S.record("e6_distance", m["target"], f"47.16: the code's shift beta with {k} sentences", *m["betas"][k]["beta"],
                     source=src)  # fmt: skip
    v = latest_verdict("x47_atoms/x47_1-*") / "x47_1.json"
    src = str(v.relative_to(S.REPO))
    for m in json.loads(v.read_text())["models"]:
        for part in ("1-25", "26-100", "1-100"):
            if part in m.get("routes", {}).get("falls", {}):
                S.record("e3_identity", m["target"], f"47.1: identity answers lost beyond random without lens directions {part}",
                         *m["routes"]["falls"][part]["identity"], source=src)  # fmt: skip
    v = latest_verdict("x47_value/x47_7a-*") / "x47_7a.json"
    m = next(x for x in json.loads(v.read_text())["models"] if x["status"] == "tested")
    src = str(v.relative_to(S.REPO))
    for r, name in (("ql", "question last"), ("qf", "question first")):
        S.record("e14_question_first", m["target"], f"47.7(a): value probe at the bridge word, {name}", *m["probe"][r]["probe"],
                 source=src)  # fmt: skip
    v = latest_verdict("x47_report/x47_10-*") / "x47_10.json"
    src = str(v.relative_to(S.REPO))
    for m in json.loads(v.read_text())["models"]:
        o = m.get("orders", {}).get("last")
        if not o or "report" not in o.get("readers", {}):
            continue
        rd = o["readers"]["report"]
        S.record("e8_report", m["target"], "47.10: the report's extra loss without the address", *rd["alf"]["excess"], source=src)
        S.record("e8_report", m["target"], "47.10: the report's extra loss without the J++ part", *rd["jpp"]["excess"], source=src)
        S.record("e8_report", m["target"], "47.10: lens top-5 holds the right ordinal (report prompt)",
                 *o["lens"]["report"]["top5_ordinal"], source=src)  # fmt: skip


def f_batch47(plt) -> None:
    batch47_figures(plt)


def s_batch47(plt) -> None:
    batch47_figures(plt, BATCH47_SUPP, supp=True)


# v6: Fig. 4's schematic is Fig. 5's left panel; the full-width one is the supplement s04_routes_design
README_FIGS = (f00_setup, f01_split, f01b_settings, f02_specificity, f02b_k, f03_order, f03b, f03c, f05_routes,
               f06_depth, f06b_anatomy, f07_writes, f07b_verbal, f08_first_locker, f09_transfer, f10_left, f11_scorecard,
               f_batch47)  # fmt: skip
SUPP_FIGS = (
    s01_split,
    s01b_one_pick,
    s01c,
    s02_parts,
    f04_routes_design,
    s05_routes,
    s08_first_sentence,
    s10_removed_together,
    s10b_all_scenes,
    s_batch47,
)


README_NAMES = ("fig00_setup", "fig01_split", "fig01b_settings", "fig02_specificity", "fig02b_k_curve", "fig03_order", "fig03b_layers",
                "fig03c_earlier_mention",
                "fig05_routes", "fig06_depth", "fig06b_anatomy", "fig07_writes", "fig07b_verbal", "fig08_first_locker",
                "fig09_transfer", "fig10_what_is_left", "fig11_scorecard", *BATCH47)  # fmt: skip
# the draft set's second sheet: the supplementary figures (README Appendix A) and docs/x0_details.md's figures
SHEET_MORE = ("supp/s01_split_all_scene_sets", "supp/s01b_one_pick_duplicate", "supp/s01c_no_chat_template",
              "supp/s02_parts_all", "supp/s03b_layers_45b", "supp/s03d_link_copy_variants", "supp/s04_routes_design",
              "supp/s05_routes_all_arms", "supp/s08_first_sentence_and_label_free",
              "supp/s08b_pointer_moves_and_neutral_sentence", "supp/s10_removed_together_bars", "supp/s10b_what_is_left_all_scenes",
              "x0_necessity/overview", "x0_necessity/detail_x0_necessity_27b_chat_chat",
              "x0_necessity/detail_qwen35_9b_x0_necessity_chat", "x0_necessity/kmatch", "x0_necessity/kcurve",
              "x0_necessity/share", "x0_necessity/asked_first", "status_2026-10-24/f6_digits")  # fmt: skip


def contact_sheet(
    plt, names=README_NAMES, dest: Path = S.REPO / "docs" / "figures_contact_sheet.png", cols: int = 3
) -> None:
    """dest (default docs/figures_contact_sheet.png): every README figure at the same width, in story order, for one
    look."""
    imgs = [plt.imread(S.OUT / f"{n}.png") for n in names]
    rows = -(-len(imgs) // cols)
    heights = [max(im.shape[0] / im.shape[1] for im in imgs[r * cols : (r + 1) * cols]) for r in range(rows)]
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 6, 6 * sum(heights) + 0.4 * rows),
                             gridspec_kw={"height_ratios": heights})  # fmt: skip
    for k, ax in enumerate(axes.flat):
        ax.axis("off")
        if k < len(imgs):
            ax.imshow(imgs[k])
            ax.set_title(names[k], fontsize=12, loc="left", color=S.COL["muted"])
    fig.tight_layout()
    fig.savefig(dest, dpi=60, facecolor="white")
    plt.close(fig)


def main(argv: list[str] | None = None) -> None:
    """Default: figures/story/ (+ figures/supp/, figures/story/scorecard.csv, docs/figures_contact_sheet.png). --out DIR:
    the whole draft set (Dan, 26 Oct ~21:50 / ~22:45: figures/drafts/v5): the README figures, the supplementary figures
    in DIR/supp, docs/x0_details.md's figures in DIR/x0_necessity (x0_figures) and DIR/status_2026-10-24
    (x0_status_pack's f6), each folder with its data.csv; DIR/contact_sheet.png (the README figures) and
    DIR/contact_sheet_more.png (the rest). figures/story/, figures/supp/, figures/x0_necessity/ and docs/ stay
    untouched. (Fig. 8b, the 26 Oct draft, is Fig. 8 (a) since batch 45.)"""
    import argparse

    ap = argparse.ArgumentParser(description="The README figures, their data.csv and contact sheet.")
    ap.add_argument("--out", type=Path, default=None, help="draft output dir (default: figures/story)")
    args = ap.parse_args(argv)
    sheet = S.REPO / "docs" / "figures_contact_sheet.png"
    out = None
    if args.out is not None:
        out = args.out if args.out.is_absolute() else S.REPO / args.out
        S.OUT, S.SUPP, sheet = out, out / "supp", out / "contact_sheet.png"
    plt = S.setup()
    for f in (*README_FIGS, *SUPP_FIGS):
        f(plt)
    probe_rows()
    batch47_numbers()
    check_scorecard_keys(S.OUT / "scorecard.csv")
    S.write_data()
    contact_sheet(plt, README_NAMES, sheet)
    if out is not None:
        from scripts import x0_status_pack as SP

        XF.render(out / "x0_necessity")
        SP.render(out / "status_2026-10-24", ["f6"])  # after x0_figures: its style() recolours scripts.figs.common
        plt = S.setup()
        contact_sheet(plt, SHEET_MORE, out / "contact_sheet_more.png")
    print(S.OUT)


if __name__ == "__main__":
    main()
