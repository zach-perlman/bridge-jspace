"""README v2's figures (Dan, 25 Oct: one story, figures that read at a glance) into figures/story/ (SVG + PNG) and
figures/story/data.csv, in story_style's look. Fig. 0 and Fig. 3 are schematics (no data); the others read the run
files (X0 cells, verdicts) or docs/x0_numbers.json, and record every plotted number. The words on the figures:
docs/glossary.md (tests/test_readme_build.py checks them).

uv run python scripts/readme_story_figures.py                            # figures/story/, figures/supp/
uv run python scripts/readme_story_figures.py --out figures/drafts/v5    # a draft set, Fig. 8b included
"""

from __future__ import annotations

import csv
import itertools
import json
import sys
import textwrap
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib.colors import to_rgba

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


def newest(path: Path, pattern: str) -> Path:
    """The file latest() reads (its path, for a data.csv source)."""
    found = sorted(path.glob(pattern))
    assert found, f"no {pattern} under {path}"
    return found[-1]


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
                    c = cells.setdefault(r["part"], {"share": r["median_share"], "source": run, "n": r.get("n")})
                    c["lookup" if r["reader"] == X.LOOKUP else "recall"] = r["excess"]
        run = XF.Run(MAIN_RUNS[m])
        layer = X.PREDICTED[{k: t for t, k, _ in S.MODELS}[m]]
        allc = run.cells("chat")
        for d in ("wu", "we", "rand"):
            key = ("chat", layer, X.LOOKUP, d, X.K_MAIN, "signed")
            if key in allc:
                cells[d] = {"lookup": allc[key]["excess"], "recall": allc[("chat", layer, X.RECALL, d, X.K_MAIN, "signed")]["excess"],
                            "share": run.share.get(("chat", layer, d, X.K_MAIN, "signed")), "source": MAIN_RUNS[m],
                            "n": int(N[f"n_{m}"])}  # fmt: skip
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


def transfer_cells(target: str, reader: str = X.LOOKUP) -> dict[tuple[str, str], tuple | None]:
    """(scenes, part) -> the reader's (default the lookup's) extra loss (value, lo, hi), and the run's whole-change
    switches as (scenes, "switched"): simple from docs/x0_numbers.json (J++ on the pointer
    directions' own scenes; the pointer directions there); varied per format and natural (the passages whose fact comes
    before the bridge) from the run files, J++ and the pointer on the same items when the pointer run is in."""
    from scripts import x5_natural_split as NS

    m = next(k for t, k, _ in S.MODELS if t == target)
    out: dict = {
        ("simple", "jpp"): S.parse(N.get(f"ss_jpp_{'lk' if reader == X.LOOKUP else 'rc'}_excess_{m}")),
        ("simple", "alf"): S.parse(N.get(f"mmlf_Alf_{'lk' if reader == X.LOOKUP else 'rc'}_excess_{m}")),
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
                cell = NS.cells(rows, scenes, X.N_BOOT, part).get(reader) if scenes else None
                out[(name, part)] = tuple(cell["excess"]) if cell else None
                if cell and part == "jpp":
                    out[(name, "switched")] = (cell["switched_whole"], cell["n"])
                out[(name, "src")] = str((base / run / "outcomes.jsonl").relative_to(pins.REPO_ROOT))
    out[("simple", "src")] = f"ss_jpp_{'lk' if reader == X.LOOKUP else 'rc'}_excess_{m}"
    return out


# ---------------------------------------------------------------------------------------------------------------------
# README v4 (Dan, 26 Oct ~16:45; docs/figure_plan.md): one claim per figure, in story order, figures/story/figNN_*.png.
# The 26 Oct files (fig0_setup.png ... fig11_order.png) are in figures/archive/; the detail panels go to figures/supp/.

NAMES = {m: name for _, m, name in S.MODELS} | {"lightning": "Nemotron 3.5 Lightning"}
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


# Dan's Fig. 0 brief (28 Oct ~22:40): Fig. 0 draws the page's running example, a stored main-test scene (data/tasks_v2/
# d1_topics_v3, scene P2-L0-0133: items PP-L0-0133, the lookup, and PM-L0-0133, the recall); f00_setup checks the
# drawn text against it. The numbers drawn are the scene's, an illustration of the design, not results.
SETUP_SET, SETUP_SCENE = "d1_topics_v3", "P2-L0-0133"
SETUP_LOCKERS = ("The locker of carbon is 3.", "The locker of helium is 5.", "The locker of oxygen is 7.")
SETUP_PICKS = {"original": (("Hugo", "oxygen"), ("Eric", "carbon"), ("Eva", "helium")),
               "changed": (("Hugo", "carbon"), ("Eric", "oxygen"), ("Eva", "helium"))}  # fmt: skip
SETUP_QUESTIONS = (("Lookup", "PP", "Which locker belongs to Eric's pick?", "3", "7", "in the prompt"),
                   ("Recall", "PM", "What is the atomic number of Eric's pick?", "6", "8", "from memory"))  # fmt: skip
SETUP_ASKED = 1  # the asked person's pick sentence (Eric's): its item is the bridge word


def setup_context(version: str) -> str:
    return " ".join([*SETUP_LOCKERS, *(f"{p} picked {x}." for p, x in SETUP_PICKS[version])])


def check_setup_scene() -> None:
    """The drawn scene is the stored one: contexts, questions and both prompts' answers, per reader."""
    path = pins.DATA_DIR / "tasks_v2" / SETUP_SET / "items.jsonl"
    items = {it["word"]: it for it in map(json.loads, path.read_text().splitlines()) if it["scene"] == SETUP_SCENE}
    for _, word, q, a, b, _ in SETUP_QUESTIONS:
        it = items[word]
        drawn = (setup_context("original"), setup_context("changed"), q, a, b)
        stored = (it["context"], it["cf_context"], it["question"], it["answer"], it["cf_answer"])
        assert drawn == stored, (word, drawn, stored)


def f00_setup(plt) -> None:
    """Fig. 0 (Dan's Fig. 0 brief, 28 Oct ~22:40), on the page's running example: the original prompt and the changed
    prompt (the two picks swap), the bridge word marked in each; arrows from the two bridge-word states to Δ; Δ added
    at one layer at the original prompt's bridge word; after that prompt, the two questions, both reading the same
    state, each with the original answer and the changed prompt's (a switch)."""
    check_setup_scene()
    W, H = S.WIDTH, 4.75
    fig = plt.figure(figsize=(W, H), dpi=200)  # measured at the saved dpi: Agg's hinted widths move with the dpi
    ax = fig.add_axes((0, 0, 1, 1))  # data units: inches from the top left
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    S.title(fig, "One prompt, two questions about the same bridge word",
            "Δ: the bridge word's state in the changed prompt minus that in the original prompt, at one layer.")  # fmt: skip
    r = fig.canvas.get_renderer()

    def width(s: str, **kw) -> float:
        t = ax.text(0, 0, s, fontsize=S.FONT, **kw)
        w = t.get_window_extent(r).width / fig.dpi
        t.remove()
        return w

    space, dark, grey = width("a a") - width("aa"), "#1e1e1e", "#666666"
    x0, pitch = 1.42, 0.245
    mark = {"boxstyle": "round,pad=0.12", "fc": "#e2e2e2", "ec": dark, "lw": 0.9}

    def prompt(version: str, top: float, label: str) -> float:
        """The prompt in three lines, its bridge word marked at the end of the second; returns the bridge's right end."""
        sents = [*SETUP_LOCKERS, *(f"{p} picked {x}." for p, x in SETUP_PICKS[version])]
        bridge = SETUP_PICKS[version][SETUP_ASKED][1]
        lines = [" ".join(sents[:2]), " ".join(sents[2:5]), sents[5]]
        widest = max(width(s) for s in lines)
        ax.add_patch(plt.Rectangle((x0 - 0.12, top - 0.17), widest + 0.24, 2 * pitch + 0.34, fc="#f5f5f5",
                                   ec="#bbbbbb", lw=1))  # fmt: skip
        ax.text(0.1, top + pitch, label, fontsize=S.FONT, weight="bold", va="center", linespacing=1.1)
        for k, line in enumerate(lines):
            y = top + k * pitch
            if k != 1:
                ax.text(x0, y, line, fontsize=S.FONT, va="center")
                continue
            head = line[: -len(bridge) - 1].rstrip()
            ax.text(x0, y, head, fontsize=S.FONT, va="center")
            xb = x0 + width(head) + space
            ax.text(xb, y, bridge, fontsize=S.FONT, weight="bold", va="center", bbox=mark, zorder=3)
            end = xb + width(bridge, weight="bold") + 0.03  # clear of the mark's edge
            ax.text(end, y, ".", fontsize=S.FONT, va="center")
        return end + 0.12

    ya, yb, yc = 1.0, 1.98, 3.0  # the three prompts' first lines
    ea = prompt("original", ya, "original\nprompt")
    eb = prompt("changed", yb, "changed\nprompt")
    ax.text(0.1, yb + pitch + 0.36, "(the two\npicks swap)", fontsize=S.FONT - 1, color=grey, va="center",
            linespacing=1.05)  # fmt: skip
    ec = prompt("original", yc, "original\nprompt + Δ")
    # the two bridge-word states into Δ, Δ into the original prompt's bridge word
    xd, yd = 7.72, (ya + yb) / 2 + pitch
    for x, y, end in ((ea, ya + pitch, yd - 0.17), (eb, yb + pitch, yd + 0.17)):
        ax.annotate("", (xd, end), (x, y), arrowprops={"arrowstyle": "-|>", "color": grey, "lw": 1.3, "shrinkA": 0,
                                                        "shrinkB": 0, "connectionstyle": "angle,angleA=0,angleB=90,rad=0"})  # fmt: skip
    ax.text(xd, yd, "Δ", fontsize=15, weight="bold", ha="center", va="center", color=dark,
            bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": dark, "lw": 1.2})  # fmt: skip
    xr = 8.6
    ax.plot([xd + 0.2, xr, xr], [yd, yd, yc + pitch], color=dark, lw=1.6, solid_capstyle="butt")
    ax.annotate("", (ec, yc + pitch), (xr, yc + pitch),
                arrowprops={"arrowstyle": "-|>", "color": dark, "lw": 1.6, "shrinkA": 0, "shrinkB": 0})  # fmt: skip
    ax.text((ec + xr) / 2, yc + pitch - 0.14, "added at one layer", fontsize=S.FONT - 1, color=dark, ha="center",
            va="center")  # fmt: skip
    # after that prompt, either question: both read the same state at the bridge word
    yq, xq, xa = (yc + 2 * pitch + 0.62, yc + 2 * pitch + 0.98), x0 + 0.32, 6.45
    trunk = x0 + 0.1
    ax.plot([trunk, trunk], [yc + 2 * pitch + 0.17, yq[1]], color=grey, lw=1.2)
    ax.text(xa, yc + 2 * pitch + 0.33, "original answer → a switch", fontsize=S.FONT - 1, color=grey, va="center")
    ax.text(xq, yc + 2 * pitch + 0.33, "each question follows this prompt: both read the same state", fontsize=S.FONT - 1,
            color=grey, va="center")  # fmt: skip
    for y, (name, _, q, a, b, src) in zip(yq, SETUP_QUESTIONS, strict=True):
        col = S.COL["lookup" if name == "Lookup" else "recall"]
        ax.plot([trunk, xq - 0.06], [y, y], color=grey, lw=1.2)
        ax.text(0.1, y, f"{name}:", fontsize=S.FONT, weight="bold", color=col, va="center")
        ax.text(xq, y, q, fontsize=S.FONT, va="center")
        ax.text(xa, y, f"{a} → {b}", fontsize=S.FONT, weight="bold", color=col, va="center")
        ax.text(xa + 0.62, y, src, fontsize=S.FONT, color=col, va="center")
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
# Batch 52 (Dan 29 Oct ~08:55): Nemotron 3.5 Lightning is the fourth model; its marks are hollow everywhere (its gate
# was chosen after the 60-scene pre-check was seen), its layer is L14 (amendment 1). Its coverage verdicts hold
# Lightning alone, so they are read by path, never through a newest-folder pattern that the three models' runs use.
LT = ("nemotron-3.5-lightning", "lightning", "Lightning")
LT_L = 14
LT_NOTE = "Hollow marks: Lightning's gate chosen after the 60-scene pre-check was seen."
LT_SPLIT = pins.RESULTS_DIR / "x0_composition" / "split-by-order-20261029T005451Z" / "split.json"
LT_X0B = pins.RESULTS_DIR / "x0b_generalize" / "nem35l_x52_x0b" / "verdict-20261029T014520Z" / "verdict.json"
LT_GATE = "not tested (gate)"
LT_DOSE = pins.RESULTS_DIR / "x51_dose" / "x52_dose-20261029T011635Z"
LT_ROUTES = pins.RESULTS_DIR / "x6_routes" / "nem35l_x52_routes" / "verdict-20261029T004324Z" / "verdict.json"
LT_PROBE = pins.RESULTS_DIR / "x0_probe" / "nem35l_x52_probe" / "probe-20261029T002432Z" / "probe.json"
LT_JREAD = pins.RESULTS_DIR / "x51_jread" / "x52_jread-20261029T005707Z"
LT_ANATOMY = pins.RESULTS_DIR / "x47_anatomy" / "x52_anatomy-20261029T010517Z" / "x47_8.json"
LT_SIX = pins.RESULTS_DIR / "x47_six" / "x52_six-20261029T011006Z"
LT_CONFLICT = pins.RESULTS_DIR / "x0_necessity" / "nem35l_x52_conflict" / "verdict-20261029T001612Z" / "verdict.json"
LT_Z1 = pins.RESULTS_DIR / "x50_zach" / "x52_z1-20261029T013035Z" / "z1.json"
LT_SWAP = pins.RESULTS_DIR / "x8_write" / "nem35l_x52_write" / "verdict-20261029T005021Z" / "verdict.json"
SHORT["lightning"] = "Lightning"


def lightning_cell(setting: str) -> dict:
    """split_cell's dict for Lightning: the main test from its split by sentence order ('all' rows of the conflict
    test at L14), the varied scenes from its X0b verdict; the other settings were not tested (the clean one-pick
    designs and the natural passages failed their gates)."""
    out = {"lk": None, "rc": None, "gap": None, "src": "", "mark": "", "kind": "after", "note": "not run"}
    if setting == "main":
        c = json.loads(LT_SPLIT.read_text())["cells"][f"{LT[0]}|swap"]["cells"]["all"]
        out.update(lk=tuple(c["lookup"]), rc=tuple(c["recall"]), gap=tuple(c["gap"]), src=rel(LT_SPLIT))
    elif setting == "varied":
        v = json.loads(LT_X0B.read_text())
        cell = {c["reader"]: tuple(c["excess"]) for c in v["cells"] if c["layer"] == LT_L and c["dict"] == "jpp"
                and c["k"] == X.K_MAIN and c["omp"] == "signed"}  # fmt: skip
        out.update(lk=cell[X.LOOKUP], rc=cell[X.RECALL], gap=tuple(v["contrast"][str(LT_L)]), src=rel(LT_X0B))
    elif setting in ("natural", "clean"):
        out["note"] = LT_GATE
    return out


def lightning_transfer(reader: str) -> dict[tuple[str, str], tuple | str | None]:
    """transfer_cells' dict for Lightning: prose / JSON / table from its X0b verdict's format strata (L14, J++ k=25
    signed); (scenes, "why") where a row has no cell: no run on the pointer directions' own simple scenes, and its
    natural passages failed their gate."""
    out: dict = {("simple", "why"): "not run", ("natural", "why"): LT_GATE}
    for s in json.loads(LT_X0B.read_text())["strata"]:
        if s["feature"] == "format" and s["reader"] == reader:
            out[(s["value"], "jpp")] = tuple(s["excess"])
            out[(s["value"], "switched")] = (s["switched_whole"], s["n"])
            out[(s["value"], "src")] = rel(LT_X0B)
    return out


GAP_BAR, LOOKUP_BAR = 0.30, 0.10  # 45m's rule (batch45.yaml): the split holds if gap >= 0.3 and lookup <= 0.10
VALID_SWITCHES = 30  # X0's validity bar: a lookup extra loss is drawn only on at least 30 switches


def blend(fig, ax):
    """x in figure fraction, y in the axes' data: text columns beside a panel's rows."""
    from matplotlib.transforms import blended_transform_factory

    return blended_transform_factory(fig.transFigure, ax.transData)


def split_cell(setting: str, target: str, m: str) -> dict:
    """lk / rc / gap as (v, lo, hi), kind (fixed / after), mark (the degree sign), src; lk None where the lookup switches
    too rarely (Muse's natural passages)."""
    if m == "lightning":
        return lightning_cell(setting)
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


def split_rows(ax, setting: str, fig_id: str, ci: bool, gap_col: bool = True, models=S.MODELS) -> None:
    """One row per model (models: story_style.MODELS' entries): the lookup's and the recall's dots joined, the gap at the
    right end (bold; its interval if ci). gap_col False: the gap is recorded but not written (Fig. 1 writes its own
    columns)."""
    S.extra_axis(ax, label=False)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.5", "0.75", "1"])
    if gap_col:  # inside the panel's top band, clear of a two-line panel title
        ax.text(1.04, 0.40, "gap", transform=ax.get_yaxis_transform(), va="bottom", fontsize=S.FONT,
                color=S.COL["muted"], clip_on=False)  # fmt: skip
    what = SETTINGS[setting][0].replace("\n", " ")  # data.csv's quantity text
    labels = []
    for i, (target, m, name) in enumerate(models):
        c = split_cell(setting, target, m)
        labels.append((name if ci else SHORT[m]) + c["mark"])
        lk, rc, y = c["lk"], c["rc"], -i
        if rc is None:
            ax.text(0.4, y, c.get("note", "not run"), ha="center", va="center", color=S.COL["muted"])
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
        S.record(fig_id, target, f"{what}: gap", *gap,
                 source=c["src"] if m == "lightning" else SETTINGS[setting][3].format(m=m))  # fmt: skip
    ax.set_ylim(-len(models) + 0.45, 0.92 if gap_col else 0.55)
    ax.set_yticks([-i for i in range(len(models))], labels)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eeeeee")


V6_MODELS = tuple(x for x in S.MODELS if x[1] != "122b")  # v6: 9B, 27B, Muse; the 122B in supplements only
# the 122B as the fifth model slot, after Lightning (Dan 11:30, q122b_1130: "the 122B as a fifth model where a verdict
# exists ... grey slots elsewhere")
B122 = next(x for x in S.MODELS if x[1] == "122b")
B122_NOTE = "122B: FP8; MoE, ~10B active; L33 (the 27B's relative depth carried over)."


def f01_split(plt) -> None:
    """E1 (v6): the main test, fixed in advance, per model (9B, 27B, Muse) the lookup's and the recall's J++ extra loss
    with 95% intervals, joined; at the right the gap with its interval. The 122B is in s01 (every scene set), the other
    settings in Fig. 1b (fig01b_settings), the split by sentence order in E10 (fig03_order, s03_order_extra_loss)."""
    fig, ax = plt.subplots(figsize=(S.WIDTH, 5.45))
    fig.subplots_adjust(left=0.215, right=0.70, top=0.77, bottom=0.215)
    S.title(fig, "Recall follows the J++ part of the bridge; the lookup mostly does not",
            "Extra loss: switches lost without the J++ part, beyond a random part of the same size; whiskers 95%.")  # fmt: skip
    # Lightning the fourth row (batch 52), its marks hollow; the 122B the fifth (Dan 11:30), at its own gate, filled.
    # split_rows records the 122B's fig01 rows as before (scripts/joint_figures.py's j1 reads them)
    rows = (*V6_MODELS, LT, B122)
    split_rows(ax, "main", "fig01", ci=True, gap_col=False, models=rows)
    first = split_cell("main", *V6_MODELS[0][:2])
    for v, name, col in ((first["lk"], "lookup", S.COL["lookup"]), (first["rc"], "recall", S.COL["recall"])):
        ax.text(v[0], 0.38, name, ha="center", va="bottom", weight="bold", color=col)
    ax.set_ylim(-len(rows) - 0.05, 0.6)  # room for the band's label under the last row
    ax.text(-0.05, -len(rows) + 0.28, "not needed\n(below 0.1)", ha="center", va="center", color=S.COL["muted"],
            linespacing=1.0)  # fmt: skip
    ax.set_xlabel("extra loss without the J++ part")
    # the gap (recall minus lookup) and its interval, fixed in advance
    tr = blend(fig, ax)
    x_gap, x_ci = 0.725, 0.79
    ax.text(x_gap, 0.38, "gap: recall − lookup", transform=tr, va="bottom", color=S.COL["muted"])
    ns = set()
    for i, (_, m, _) in enumerate(rows):
        if m == "lightning":
            g = lightning_cell("main")["gap"]
            ns.add(str(json.loads(LT_SPLIT.read_text())["cells"][f"{LT[0]}|swap"]["cells"]["all"]["n"]))
        else:
            g = interval(f"contrast_{m}")
            ns.add(N[f"n_{m}"])
        ax.text(x_gap, -i, f"{g[0]:.2f}", transform=tr, va="center", fontsize=S.FONT + 2, weight="bold")
        ax.text(x_ci, -i, f"[{g[1]:.2f}, {g[2]:.2f}]", transform=tr, va="center", color=S.COL["muted"])
    fig.text(0.01, 0.02, f"{B122_NOTE}\n{LT_NOTE}", color=S.COL["muted"], fontsize=S.FONT - 1, va="bottom")
    ax.text(0.0, 1.13, "main test (two people swap picks)", transform=ax.transAxes, fontsize=12, weight="bold",
            va="bottom")  # fmt: skip
    S.panel_tag(ax, "–".join(sorted(ns)) + " per model", "fixed")
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


def order_split_path() -> Path:
    """The newest split by sentence order that holds the 9B's main-test cells: batch 52's coverage runs write
    single-model splits into the same folder pattern (Lightning's split-by-order-20261029T005451Z), which the README
    figures must not pick up as the three models' split."""
    found = sorted((pins.RESULTS_DIR / "x0_composition").glob("split-by-order-*/split.json"))
    return next(p for p in reversed(found) if "qwen3.5-9b|swap" in json.loads(p.read_text())["cells"])


def order_cells() -> dict[tuple[str, str, str], dict]:
    """Fig. 3b's cells: (test, model key, before / after) -> {lookup, recall: (v, lo, hi), switches, n, src}; the main
    test from the split by sentence order (results/x0_composition/split-by-order-*, after the data), the clean one-pick
    scenes from 45m (results/x0_necessity/x45m-*, fixed in advance); the lookup's switch count from the same file."""
    root = pins.RESULTS_DIR
    split_path = order_split_path()
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


def order_switches(target: str, m: str) -> dict[tuple[str, str], tuple[float, float, float, int, str]]:
    """The main test's switches under the whole change at the layer fixed in advance, split by sentence order (after
    the data): (before / after, lookup / recall) -> (share, Wilson lo, hi, n, source). Lightning: its conflict test
    (the run its split by sentence order reads) at L14."""
    from bridge_jspace.stats import wilson
    from scripts import x0_strata as ST

    if m == "lightning":
        run, la = json.loads(LT_SPLIT.read_text())["manifest"]["inputs"][f"{LT[0]}|swap"].split("/")[1], LT_L
    else:
        run, la = MAIN_RUNS[m], X.PREDICTED[target]
    rows = [x for x in XF.Run(run).rows if x["rendering"] == "chat" and x["layer"] == la and x["arm"] == "whole"]
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / run / "cases.jsonl") if c["rendering"] == "chat"}
    src = f"results/x0_necessity/{run}/outcomes.jsonl"
    out = {}
    for order in ("before", "after"):
        mine = [x for x in rows if ST.features(cases[x["scene"]])["org locker vs asked pick"] == order]
        for w in (X.LOOKUP, X.RECALL):
            got = [r["switched"] for r in mine if r["reader"] == w]
            k, n = sum(got), len(got)
            p, lo, hi = wilson(k, n)
            out[(order, "lookup" if w == X.LOOKUP else "recall")] = (p, lo, hi, n, src)
    return out


def s03_order_split(plt) -> None:
    """Supplementary to E10 (Fig. 3 until v6, all four models): (a) after the data: the lookups (open purple bars, 95%
    Wilson) and the recalls (grey dots) the whole change switches in the main test, the original bridge's locker
    sentence before vs after the asked person's pick sentence. (b) The recall's (and the lookup's, where it has at
    least 30 switches) extra loss without the J++ part, locker before vs after the pick: the main test (after the data)
    and the clean one-pick scenes (45m, fixed in advance); on the main test's locker-before rows the gap (recall minus
    lookup, docs/split_by_order.md; Fig. 1's column until v6)."""
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
        sw = order_switches(target, m)
        for j, order in enumerate(("before", "after")):
            x = i * 3.6 + j * 1.3
            for what in ("lookup", "recall"):
                p, lo, hi, n, src = sw[(order, what)]
                p, lo, hi = 100 * p, 100 * lo, 100 * hi
                if what == "lookup":
                    ax.bar(x, p, width=0.72, fc="white", ec=S.COL["lookup"], lw=2)
                    ax.errorbar(x, p, yerr=[[p - lo], [hi - p]], color="#333333", capsize=3, lw=1)
                    ax.text(x, hi + 2, f"{p:.0f}%", ha="center", va="bottom", fontsize=S.FONT, weight="bold")
                else:
                    ax.plot([x + 0.62], [p], "o", ms=6, color=S.COL["recall"], zorder=3)
                S.record("s03", target, f"{what}s switched by the whole change, locker sentence {order} the pick",
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
            S.record("s03", target, f"{what}: recall extra loss", *c["recall"], n=c["n"], source=c["src"])
            S.record("s03", target, f"{what}: lookup switches", c["switches"], n=c["n"], source=c["src"])
            S.dot(bx, 0, yy, c["recall"], S.COL["recall"], kind, size=9)
            if c["switches"] >= VALID_SWITCHES:
                bx.plot([c["lookup"][0], c["recall"][0]], [yy, yy], color="#d6d6d6", lw=3.5, zorder=1,
                        solid_capstyle="butt")  # fmt: skip
                S.dot(bx, 0, yy, c["lookup"], S.COL["lookup"], kind, size=9)
                S.record("s03", target, f"{what}: lookup extra loss", *c["lookup"], n=c["n"], source=c["src"])
                gap = S.parse(N.get(f"sbo_swap_before_gap_{m}")) if (test, order) == ("main", "before") else None
                if gap is not None:  # Fig. 1's locker-before gap column until v6
                    bx.text((c["lookup"][0] + c["recall"][0]) / 2, yy + 0.2, f"gap {gap[0]:.2f}", ha="center",
                            va="bottom", fontsize=S.FONT - 1, color="#444444")  # fmt: skip
                    S.record("s03", target, "main test (two people swap picks), locker before the pick: gap", *gap,
                             n=int(N[f"sbo_swap_before_n_{m}"]), source=f"sbo_swap_before_gap_{m}")  # fmt: skip
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
    S.save(fig, "s03_order_split", supp=True)


ORDER_SWEEP = (("bw", "the bridge-word change", "--", "o"), ("ls", "the copy into the locker sentences", "-", "o"))
BLOCK = 1.3  # Fig. 3 (b): one block per model on one axis, each block the model's layers scaled to [0, 1]


def f03_order(plt) -> None:
    """E10 (v6), two panels, 9B / 27B / Muse. (a) After the data: the share of lookups (purple bars) and recalls (grey
    dots) the whole change at the bridge word switches in the main test, the locker sentence before vs after the asked
    pick, with 95% Wilson intervals. (b) Z1 (Dan's 18:30 brief, fixed in advance): the same on Zach's passages, the
    lookup's switch under the whole change at our layer, the bridge's fact sentence before vs after the sentence naming
    the bridge. (c) 45q (clean scenes, the locker after the pick): the lookups switched by layer,
    the bridge-word change (dashed) against the copy of the changed prompt's states into the locker sentences (solid);
    the sweep after the data (open marks), the rule's arms fixed in advance (filled: at L the bridge-word change and the
    copy, at L/2 the copy); one block per model on one axis, x = the layer index (ticks 0, L, the last layer swept).
    The old Fig. 3 with the 122B and its extra-loss panel: figures/supp/s03_order_split; the old Fig. 3b stays
    fig03b_layers until the README drops it. Lightning (batch 52, hollow): A from its conflict test at L14, B from its
    Z1 run (LT_Z1), C not tested (its clean one-pick scenes missed their gate)."""
    h = 11.85  # the bottom 0.3 in: the 122B's caption line (the panels keep their places from the top)
    fig = plt.figure(figsize=(S.WIDTH, h))

    def box(left: float, width: float, top_in: float, bottom_in: float) -> tuple[float, float, float, float]:
        return (left, 1 - bottom_in / h, width, (bottom_in - top_in) / h)

    S.title(fig, "Locker after the pick: the link is made in the locker sentences",
            "A, B: switches under the bridge-word change, by sentence order (ours, Zach's). C: by layer.")  # fmt: skip
    a = fig.add_axes(box(0.11, 0.86, 1.95, 3.7))
    zb = fig.add_axes(box(0.11, 0.86, 5.35, 6.75))  # four models: three-line order labels, two-line names
    b = fig.add_axes(box(0.11, 0.81, 8.3, 10.55))
    # five groups across the panel: every name on at most two short lines
    long_name = {**NAMES, "muse": "Muse\nGlimmer 30B", "lightning": "Nemotron 3.5\nLightning", "122b": "Qwen3.5-\n122B"}

    # (a) the order split
    w = 0.34
    ns = []
    rows = (*V6_MODELS, LT, B122)  # the 122B the fifth (Dan 11:30): its main run at L33, at its own gate
    hollow_bar = {"facecolor": "white", "edgecolor": S.COL["lookup"], "lw": 1.6}
    for i, (target, m, _) in enumerate(rows):
        sw, lt = order_switches(target, m), m == "lightning"
        for j, order in enumerate(("before", "after")):
            x = i + (j - 0.5) * 0.42
            p, lo, hi, n, src = sw[(order, "lookup")]
            a.bar(x, p, width=w, zorder=2, **(hollow_bar if lt else {"color": S.COL["lookup"]}))
            a.plot([x, x], [lo, hi], color="#1e1e1e", lw=1.2, zorder=3)
            a.text(x, hi + 0.02, f"{p:.2f}", ha="center", va="bottom", fontsize=S.FONT - 1, color=S.COL["lookup"],
                   weight="bold")  # fmt: skip
            r = sw[(order, "recall")]
            xr = x + w / 2 + 0.05  # the recall beside its lookup bar
            a.plot([xr, xr], [r[1], r[2]], color=S.COL["recall"], lw=1.2, zorder=4)
            a.plot([xr], [r[0]], "D", ms=5.5, color=S.COL["recall"], zorder=5,
                   **({"mfc": "white", "mew": 1.2} if lt else {"mec": "white", "mew": 0.6}))  # fmt: skip
            # "locker first" / "locker after" (the panel title says "the pick"): five groups leave no room for three lines
            a.text(x, -0.04, f"locker\n{'first' if order == 'before' else 'after'}", ha="center", va="top",
                   fontsize=S.FONT - 1, linespacing=1.0)  # fmt: skip
            if i == 0 and j == 0:  # Dan (21:50): the panel names its two marks, on its first pair
                a.text(xr + 0.06, r[0], "recall", ha="left", va="center", fontsize=S.LABEL_PT, color=S.COL["recall"])
                a.text(x, p / 2, "lookup", ha="center", va="center", rotation=90, fontsize=S.LABEL_PT, color="white")
            for what in ("lookup", "recall"):
                v0, v1, v2, nn, _ = sw[(order, what)]
                S.record("fig03", target, f"{what}s switched by the whole change, locker sentence {order} the pick",
                         round(v0, 4), round(v1, 4), round(v2, 4), nn, source=src)  # fmt: skip
            ns.append(n)
        a.text(i, -0.33, long_name[m], ha="center", va="top", fontsize=S.FONT, weight="bold", linespacing=1.0)
    a.set_xlim(-0.6, len(rows) - 0.4)
    a.set_ylim(0, 1.05)
    a.set_xticks([])
    a.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    a.set_ylabel("lookups switched (share)")
    a.grid(axis="y", color="#eeeeee")
    a.set_axisbelow(True)
    a.set_title("A  The bridge word moves the lookup when the locker comes first", loc="left", fontsize=12,
                weight="bold", pad=26)  # fmt: skip
    S.panel_tag(a, f"{min(ns)}–{max(ns)} per bar", "after")

    # (b) Z1 on Zach's passages (the order split fixed after the gate, before the data): the lookup's switch under the
    # whole change, the bridge's fact sentence before vs after the sentence that names the bridge, at our layer
    zdir = latest_verdict("x50_zach/z1-*")
    zns = []
    zmods = sorted((x for x in json.loads((zdir / "z1.json").read_text())["models"] if x["status"] == "tested"),
                   key=lambda x: [t for t, _, _ in V6_MODELS].index(x["target"]))  # fmt: skip
    zmods = [(mod, rel(zdir / "z1.json")) for mod in zmods]
    zmods += [(mod, rel(LT_Z1)) for mod in json.loads(LT_Z1.read_text())["models"]
              if mod["status"] == "tested" and mod["target"] == LT[0]]  # fmt: skip
    for i, (mod, zsrc) in enumerate(zmods):
        target, la = mod["target"], str(mod["layers"][0])  # our layer (the Muse's L36 has no lookup switch)
        m = next(k for t, k, _ in rows if t == target)
        lt = m == "lightning"
        strata = mod["layer_results"][la]["order"]["strata"]
        for j, (key, label) in enumerate((("fact-first", "fact\nfirst"), ("fact-after", "fact\nafter"))):
            x = i + (j - 0.5) * 0.42
            p, lo, hi = strata[key]["whole_switch"]
            zb.bar(x, p, width=w, zorder=2, **(hollow_bar if lt else {"color": S.COL["lookup"]}))
            zb.plot([x, x], [lo, hi], color="#1e1e1e", lw=1.2, zorder=3)
            zb.text(x, hi + 0.02, f"{p:.2f}", ha="center", va="bottom", fontsize=S.FONT - 1, color=S.COL["lookup"],
                    weight="bold")  # fmt: skip
            zb.text(x, -0.05, label, ha="center", va="top", fontsize=S.FONT - 1, linespacing=1.0)
            if i == 0 and j == 0:  # Dan (21:50): the panel names its bars
                zb.text(x, p / 2, "lookup", ha="center", va="center", rotation=90, fontsize=S.LABEL_PT, color="white")
            S.record("fig03", target, f"Zach's passages, L{la}: lookups switched by the whole change, {key}",
                     round(p, 4), round(lo, 4), round(hi, 4), strata[key]["n"], source=zsrc)  # fmt: skip
            zns.append(strata[key]["n"])
        zb.text(i, -0.36, long_name[m], ha="center", va="top", fontsize=S.FONT, weight="bold", linespacing=1.0)
    # the 122B: Zach's passages never ran on it; its slot stays, grey
    i_b = len(zmods)
    zb.text(i_b, 0.5, "not run", ha="center", va="center", color=S.COL["muted"])
    zb.text(i_b, -0.36, long_name["122b"], ha="center", va="top", fontsize=S.FONT, weight="bold", linespacing=1.0)
    zb.set_xlim(-0.6, len(rows) - 0.4)
    zb.set_ylim(0, 1.05)
    zb.set_xticks([])
    zb.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    zb.set_ylabel("lookups switched\n(share)")
    zb.grid(axis="y", color="#eeeeee")
    zb.set_axisbelow(True)
    zb.set_title("B  On Zach's passages too: the fact sentence before vs after the bridge's sentence", loc="left",
                 fontsize=12, weight="bold", pad=26)  # fmt: skip
    S.panel_tag(zb, f"{min(zns)}–{max(zns)} per bar", "fixed")

    # (c) 45q: the link made in the locker sentences, by layer
    b.set_title("C  Locker after the pick: lookups switched, by layer", loc="left", fontsize=12, weight="bold", pad=26)
    q = LANDED.get("45q")
    if not q:
        S.empty(b, "not run")
        S.save(fig, "fig03_order")
        return
    d = {k: pins.RESULTS_DIR / p for k, p in q.items()}
    vsrc, ssrc = rel(d["verdict"] / "x45q.json"), rel(d["sweep"] / "sweep.json")
    v = json.loads((d["verdict"] / "x45q.json").read_text())
    sweep = json.loads((d["sweep"] / "sweep.json").read_text())["runs"]
    by = {mod["model"]: mod for mod in v["models"] if mod["status"] != "pending"}
    ticks, tick_labels, nq = [], [], []
    blocks = (*Q_MODELS, LT[:2], B122[:2])  # the 122B: no 45q run, a grey "not run" block
    for k, (target, m) in enumerate(blocks):
        x0 = k * BLOCK
        mod = by.get(target)
        b.text(x0 + 0.5, -0.14, SHORT[m], transform=b.get_xaxis_transform(), ha="center", va="top", fontsize=S.FONT,
               weight="bold")  # fmt: skip
        if m == "lightning":  # below gate (its clean one-pick recall 0.751 < 0.80): the rule's arms only, hollow
            if not LT_45Q.exists():
                b.text(x0 + 0.5, 0.5, LT_GATE, ha="center", color=S.COL["muted"])
                continue
            lm = next(x for x in json.loads(LT_45Q.read_text())["models"] if x["model"] == target)
            lk, la, half = lm["readers"][X.LOOKUP], lm["layer"], lm["arm_layers"]["d"]
            last = max(LT_LAYERS_LAST, la)

            def at_lt(layer: float) -> float:
                return x0 + layer / last  # noqa: B023 (used inside this iteration only)

            for xl, txt, ha in ((half, "L/2", "right"), (la, "L", "left")):  # L/2 and L close: labels apart
                b.axvline(at_lt(xl), ymax=0.93, color="#555555", ls=":", lw=1.1, zorder=0)
                b.text(at_lt(xl), 0.95, txt, ha=ha, va="bottom", fontsize=S.FONT - 1, color="#555555")
            for arm, xl, what in (("a", la, "the bridge-word change at L"),
                                  ("c", la, "copy at L, every locker-sentence token"),
                                  ("d", half, "copy at L/2, every locker-sentence token")):  # fmt: skip
                r = lk["rate"][arm]
                b.plot([at_lt(xl)] * 2, [r[1], r[2]], color="#1e1e1e", lw=1.4, zorder=5)
                b.plot(
                    [at_lt(xl)],
                    [r[0]],
                    "o",
                    ms=8,
                    color=S.COL["lookup"],
                    mfc="white",
                    mec=S.COL["lookup"],
                    mew=1.8,
                    zorder=6,
                )
                S.record("fig03", target, f"45q, the rule's arm {arm}: {what} (lookups switched)", *r, n=lk["n"],
                         source=rel(LT_45Q))  # fmt: skip
            b.text(x0 + 0.5, 0.86, "below gate", ha="center", fontsize=S.FONT - 1, color=S.COL["muted"])
            nq.append(str(lm["sanity"]["pass"]))
            ticks += [at_lt(0), at_lt(la), at_lt(last)]
            tick_labels += ["0", str(la), str(last)]
            continue
        if mod is None or mod["run"] not in sweep or "readers" not in mod:
            b.text(x0 + 0.5, 0.5, "not run" if mod is None else "not tested", ha="center", color=S.COL["muted"])
            continue
        cells = sorted(sweep[mod["run"]]["cells"][X.LOOKUP], key=lambda c: c["layer"])
        last = cells[-1]["layer"]

        def at(layer: float) -> float:
            return x0 + layer / last  # noqa: B023 (used inside this iteration only)

        la, half = mod["layer"], mod["arm_layers"]["d"]
        for xl, txt in ((half, "L/2"), (la, "L")):
            b.axvline(at(xl), ymax=0.93, color="#555555", ls=":", lw=1.1, zorder=0)
            b.text(at(xl), 0.95, txt, ha="center", va="bottom", fontsize=S.FONT - 1, color="#555555")
        xs = [at(c["layer"]) for c in cells]
        for arm, name, ls, mk in ORDER_SWEEP:
            y = np.array([c[arm] for c in cells])
            b.fill_between(xs, y[:, 1], y[:, 2], color=S.COL["lookup"], alpha=0.13, lw=0, zorder=1)
            b.plot(xs, y[:, 0], color=S.COL["lookup"], ls=ls, lw=2.0, marker=mk, ms=4.5, mfc="white",
                   mec=S.COL["lookup"], mew=1.2, zorder=2)  # fmt: skip
            for c in cells:
                S.record("fig03", target, f"45q, layer {c['layer']}: {name} (lookups switched)", *c[arm], n=c["n"],
                         source=ssrc)  # fmt: skip
        lk = mod["readers"][X.LOOKUP]
        for arm, xl, what in (("a", la, "the bridge-word change at L"), ("c", la, "copy at L, every locker-sentence token"),
                              ("d", half, "copy at L/2, every locker-sentence token")):  # fmt: skip
            r = lk["rate"][arm]
            b.plot([at(xl)] * 2, [r[1], r[2]], color="#1e1e1e", lw=1.4, zorder=5)
            b.plot([at(xl)], [r[0]], "o", ms=8, color=S.COL["lookup"], mec="#1e1e1e", mew=1.0, zorder=6)
            S.record("fig03", target, f"45q, the rule's arm {arm}: {what} (lookups switched)", *r, n=lk["n"],
                     source=vsrc)  # fmt: skip
        nq.append(str(mod["sanity"]["pass"]))
        ticks += [at(0), at(la), at(last)]
        tick_labels += ["0", str(la), str(last)]
        if k == 0:  # the copy's line labelled on the first block
            peak = max(cells, key=lambda c: c["ls"][0])
            b.text(at(peak["layer"]) + 0.05, peak["ls"][0] + 0.05, "the change copied into\nthe locker sentences", va="bottom",
                   fontsize=S.FONT - 1, color=S.COL["lookup"], linespacing=1.0)  # fmt: skip
        if k == 1:  # Dan (21:50): the panel names its dashed line too, under the 27B's plateau (empty there)
            b.text(at(cells[0]["layer"]) + 0.02, 0.45, "change at the\nbridge word", va="center", ha="left",
                   fontsize=S.FONT - 1, color=S.COL["lookup"], linespacing=1.0, zorder=4,
                   bbox={"boxstyle": "square,pad=0.1", "fc": "white", "ec": "none"})  # fmt: skip
    b.set_xlim(-0.06, (len(blocks) - 1) * BLOCK + 1.06)
    b.set_xticks(ticks, tick_labels)
    b.set_ylim(-0.03, 1.05)
    b.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    b.set_ylabel("lookups switched (share)")
    b.text(1.01, -0.045, "layer", transform=b.transAxes, ha="left", va="top")
    b.grid(axis="y", color="#eeeeee")
    b.set_axisbelow(True)
    S.panel_tag(b, ", ".join(nq), "after")
    hs = [plt.Rectangle((0, 0), 1, 1, color=S.COL["lookup"]),
          plt.Line2D([], [], marker="D", ls="", color=S.COL["recall"], ms=5.5),
          plt.Line2D([], [], color=S.COL["lookup"], ls="--", lw=2.0), plt.Line2D([], [], color=S.COL["lookup"], lw=2.0),
          plt.Line2D([], [], marker="o", ls="", ms=8, color=S.COL["lookup"], mec="#1e1e1e")]  # fmt: skip
    legend(fig, hs, ["lookup", "recall", "the change at the bridge word", "the change copied into the locker sentences",
                     "the rule, fixed in advance"], 1 - 0.62 / h, ncol=3)  # fmt: skip
    lt_c = (
        "C: Lightning below gate (its clean one-pick recall misses the gate), the rule's arms only, no layer sweep.\n"
    )
    fig.text(
        0.01,
        0.06 / h,
        (lt_c if LT_45Q.exists() else "") + B122_NOTE + " B, C: not run on the 122B.\n" + LT_NOTE,
        color=S.COL["muted"],
        fontsize=S.FONT - 1,
        va="bottom",
    )
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
          ("a2", "(2) (1), and without the\nJ++ part at the earlier mention"),
          ("a3", "(3) (1), and without a random\npart (same size) there"),
          ("a4", "(4) (1), and as in (2) at\nanother item's mention"))  # fmt: skip


# Lightning's 45p, below gate (exploratory: its clean one-pick recall 0.751 < 0.80): a fourth panel, hollow (Dan's
# figures brief, 29 Oct 10:00: "fig03c_earlier_mention: + Lightning below gate once 45p lands")
LT_45P = pins.RESULTS_DIR / "x45p" / "x52_45p_below-20261029T090351Z" / "x45p.json"
# Lightning's 45q (the copy test), below gate as well: Fig. 3 (c)'s fourth block, the rule's arms only (no layer sweep
# ran), on Lightning's sampled-layer axis (its conflict sweep's last layer)
LT_45Q = pins.RESULTS_DIR / "x45b_binding" / "x52_45q_below-20261029T085135Z" / "x45q.json"
LT_LAYERS_LAST = max(c["layer"] for c in json.loads(LT_CONFLICT.read_text())["cells"])


def f03c_p(plt, verdict_dir: Path, title: str | None = None) -> str:
    """45p (results/x45p/x45p-*, fixed in advance): clean one-pick scenes whose new item's locker sentence comes before
    the asked pick; one panel per model (9B, 27B, Muse: no 122B run), one row per arm (Fig. 2's style): the recall's
    switches lost against arm (1), and the lookup's, with 95% intervals (both filled, apart by colour); arm (1)'s own
    switches as text. The rule and n are the README card's (a main-page figure since Dan's restructure brief, 28 Oct
    22:20: a one-line subtitle, v6). Story Fig. 3c if the rule holds, else figures/supp/s03c (titled with the null).
    Returns the saved name."""
    v = json.loads((verdict_dir / "x45p.json").read_text())
    by = {m["target"]: m for m in v["models"]}
    if LT_45P.exists():
        by |= {m["target"]: m for m in json.loads(LT_45P.read_text())["models"] if m["target"] == LT[0]}
    label = v["verdict"]["label"]
    holds = label == "holds"
    default = "The recall reads the item's earlier mention when its locker came first" if holds else (
        "No sign the recall reads the earlier mention (rule not met)")  # fmt: skip
    # the 122B the fifth slot (Dan 11:30): no 45p run, a narrower grey panel
    fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH, 5.1), sharey=True, gridspec_kw={"width_ratios": [1, 1, 1, 1, 0.6]})
    fig.subplots_adjust(left=0.30, right=0.975, top=0.71, bottom=0.24, wspace=0.12)
    S.title(fig, title or default, "Clean one-pick scenes, the new item's locker before the pick: switches lost against "
            "arm (1)")  # fmt: skip
    for ax, (target, m, _) in zip(axes, (*CARD_MODELS, LT, B122), strict=True):
        lt = m == "lightning"
        src = rel(LT_45P) if lt else rel(verdict_dir / "x45p.json")
        mod = by.get(target)
        below = lt and mod is not None and "readers" in mod  # Lightning's slot: its below-gate run, or grey
        ax.set_title(SHORT.get(m, LT[2]) + (" ○\nbelow gate" if below else ""), fontsize=S.FONT, weight="bold")
        ax.set_xlim(-20, 100)
        ax.axvline(0, color="#999999", lw=0.8, zorder=1)
        ax.set_xticks(*PCT)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_ylim(-len(P_ROWS) + 0.45, 0.55)
        ax.tick_params(axis="y", length=0)
        if mod is None or "readers" not in mod:
            # Dan's figures brief (29 Oct 10:00): the slot stays, with a short grey label
            grey = "not run" if mod is None or mod["status"] == "pending" else "not tested"
            S.empty(ax, "not tested: gate" if lt else grey)
            ax.set_xticks([])  # an empty slot draws no axis numbers (they would crowd its neighbour's) and no zero line
            ax.grid(False)
            for line in list(ax.lines):
                line.remove()
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
            S.dot(ax, 0, -i + 0.15, tuple(100 * x for x in r), S.COL["recall"], "after" if lt else "fixed", size=8)
            q = lk["loss"][arm]
            if q[0] == q[0]:
                S.dot(ax, 0, -i - 0.15, tuple(100 * x for x in q), S.COL["lookup"], "after" if lt else "fixed", size=8)
                S.record("fig03c", target, f"45p, {arm}: lookup switches lost against (1)", *q, n=lk["n"], source=src)
            S.record("fig03c", target, f"45p, {arm}: recall switches lost against (1)", *r, n=rc["n"], source=src)
        S.record("fig03c", target, "45p: the rule holds", int(bool(mod.get("holds"))), source=src)
    axes[0].set_yticks([-i for i in range(len(P_ROWS))], [r[1] for r in P_ROWS])
    fig.supxlabel("switches lost (%)", x=0.62, y=0.1, fontsize=S.FONT)
    note = ("9B, 27B, Muse: fixed in advance. "
            + ("Lightning below gate (its clean one-pick recall misses the 0.80 gate): descriptive only. "
               if "readers" in by.get(LT[0], {}) else "Lightning: not tested (gate). ") + "122B: not run. " + LT_NOTE)  # fmt: skip
    fig.text(0.01, 0.01, "\n".join(textwrap.wrap(note, 112)), fontsize=S.FONT - 1, color=S.COL["muted"], va="bottom")
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=8),
                 plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=8)],
           ["recall", "lookup"], 0.83)  # fmt: skip
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

    split_path = order_split_path()
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


# Dan's Fig. 4 / 5 brief (28 Oct ~20:30): one three-box drawing of the routes test, readable at card width, on Fig. 5
# (in full, with the definitions line) and, small, on Fig. 5d so the route colours mean the same on both; Fig. 4 (the
# supplement s04) draws the full one larger. Each predicted locker in its route's colour (the lookup is asked on the
# original prompt: identity and position name its lockers, the value the changed prompt's new number); the moved
# sentence outlined dark; the original answer empty, as in Fig. 5's bars.
ROUTES_DEFINED = ("identity route: the item's own locker; position route: the locker now at the item's old place; "
                  "value: the new number")  # fmt: skip
MOVED_EDGE = "#1e1e1e"


def routes_drawing(plt, ax, small: bool = False) -> None:
    """The routes test on ax (axis off, x and y 0-100): the original and the changed prompt as three lockers each.
    Full: route labels over the original prompt's predicted lockers (original answer, position route, identity
    route), "value" under the moved sentence, a note on the move and the asked person's pick sentence. Small (Fig.
    5d): the boxes and their colours only. Drawn on Fig. 0's items (Dan's Fig. 0 brief, 28 Oct ~22:40: one domain on
    the main page; the routes test's own scenes are animals): the original prompt's lockers as in Fig. 0; the changed
    prompt, the routes test's way: Eric picks oxygen, whose locker sentence trades places with helium's and gets a
    new number."""
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])  # no hidden tick labels left for the overlap checks
    ax.set_yticks([])
    ax.axis("off")
    fs = S.FONT - 2 if small else S.FONT
    xs = (45, 67, 89) if small else (37.5, 62, 86.5)
    w, h = (20, 34) if small else (23.5, 11)  # full: room for a six-letter element at 11 pt
    rows = (("original prompt", 58 if small else 64, (("carbon", "3"), ("helium", "5"), ("oxygen", "7")),
             "Eric picked carbon."),
            ("changed prompt", 6 if small else 30, (("carbon", "3"), ("oxygen", "4"), ("helium", "5")),
             "Eric picked oxygen."))  # fmt: skip
    # (row, column) -> (route colour, label): the lockers each route predicts
    fill = {(0, 1): (ROUTE_COL["position"], "position\nroute"), (0, 2): (ROUTE_COL["identity"], "identity\nroute"),
            (1, 1): (ROUTE_COL["value"], "value")}  # fmt: skip
    for r, (label, y, lockers, pick) in enumerate(rows):
        ax.text(0, y + h / 2, label.replace(" ", "\n"), fontsize=fs, weight="bold", va="center", linespacing=1.0)
        for c, (x, (item, digit)) in enumerate(zip(xs, lockers, strict=True)):
            col = fill.get((r, c), (None, ""))[0]
            if small and col == ROUTE_COL["value"]:  # Fig. 5d draws no value: its colour stays off the mark system
                col = None
            moved = (r, c) == (1, 1)
            empty = (r, c) == (0, 0)  # the original answer
            # a light wash of the route's colour under the text, its full colour on the edge; the moved one dark
            face = to_rgba(col, 0.25) if col else ("white" if empty else "#f5f5f5")
            ax.add_patch(plt.Rectangle((x - w / 2, y), w, h, fc=face, zorder=2,
                                       ec=MOVED_EDGE if moved else col or ("#9a9a9a" if empty else "#bbbbbb"),
                                       lw=2.2 if moved or col else 1.0, ls=(0, (3, 1.5)) if moved else "-"))  # fmt: skip
            ax.text(x, y + h / 2, f"{item}: {digit}", ha="center", va="center", fontsize=fs, zorder=3)
        if not small:
            ax.text(100, y - 4.5, pick, ha="right", va="center", fontsize=fs - 1, style="italic")
    if small:
        return
    y0, y1 = rows[0][1], rows[1][1]
    for (r, c), (col, text) in fill.items():
        above = r == 0
        # the value's label under the changed prompt's pick sentence, which ends under its box
        ax.text(xs[c], y0 + h + 9 if above else y1 - 12, text, ha="center", va="center", fontsize=fs, color=col,
                weight="bold", linespacing=1.0)  # fmt: skip
    ax.text(xs[0], y0 + h + 9, "original\nanswer", ha="center", va="center", fontsize=fs, color="#7f7f7f",
            weight="bold", linespacing=1.0)  # fmt: skip
    ax.text(xs[0] - w / 2, y1 - 22, "the moved sentence:\nhelium's place, new number", ha="left", va="center",
            fontsize=fs - 1, color=MOVED_EDGE, linespacing=1.05)  # fmt: skip


def f04_routes_design(plt) -> None:
    """Fig. 4 (the supplement s04, linked once from the README; Dan's Fig. 4 / 5 brief): Fig. 5's drawing, larger, with
    the definitions line."""
    h = 4.6
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, "Each route predicts a different locker",
            "The change at 'carbon' comes from the changed prompt's 'oxygen'; the lookup is asked on the original prompt.")  # fmt: skip
    routes_drawing(plt, fig.add_axes((0.12, 0.55 / h, 0.62, 1 - 1.35 / h)))
    S.fit(fig, fig.text(0.01, 0.18 / h, ROUTES_DEFINED + "\nDrawn on Fig. 0's items; the routes test's own scenes are "
                        "animals.", ha="left", va="bottom", fontsize=S.FONT - 1, color="#555555"))  # fmt: skip
    S.save(fig, "s04_routes_design", supp=True)


# Fig. 5's result rows (v6): the arm, its label, and the random control drawn as a thin light grey bar under it (the
# position answers without a random part of the same size); the keep-only arms and the 122B are in s05
ROUTE_ROWS = (("whole", "whole change", None), ("no_alf", "without the address", "no_alf_rand"))
ROUTE_RUNS = {"9b": ("qwen35_9b_x6_routes", "qwen35_9b_x6_routes_keeponly"),
              "27b": ("x6_routes_27b", "x6_routes_keeponly_27b"),
              "122b": ("qwen35_122b_x6_routes_g75", "qwen35_122b_x6_routes_keeponly_g75"),
              "muse": ("muse30b_x6_routes", "muse30b_x6_routes")}  # fmt: skip


# the 122B (FP8; MoE, ~10B active; L33), Figs. 5 and 7's fifth slot (Dan 11:30, the coordinator 12:15): its routes and
# swap runs ran at the gate lowered to 0.75 after the data (their 0.80 routes run missed it on the recall), marked °;
# each file by its explicit path
Q122 = ("qwen3.5-122b-a10b", "122b", "Qwen3.5-122B")
Q122_ROUTES = pins.RESULTS_DIR / "x6_routes" / "qwen35_122b_x6_routes_g75" / "verdict-20261025T134214Z" / "verdict.json"
Q122_KEEP = (pins.RESULTS_DIR / "x6_routes" / "qwen35_122b_x6_routes_keeponly_g75" / "verdict-20261025T202506Z"
             / "verdict.json")  # fmt: skip
Q122_PROBE = pins.RESULTS_DIR / "x0_probe" / "qwen35_122b_x0_probe_v4" / "probe-20261024T230718Z" / "probe.json"
Q122_SWAP = pins.RESULTS_DIR / "x8_write" / "qwen35_122b_x8_write_g75" / "verdict-20261026T125705Z" / "verdict.json"
Q122_RECALL = pins.RESULTS_DIR / "x8_write" / "qwen35_122b_x8_write_g75" / "recall-20261026T125802Z" / "recall.json"
Q122_NOTE = (
    "122B° (FP8; MoE, ~10B active; L33, the 27B's relative depth carried over): gate lowered to 0.75 after the data."
)


def f05_routes(plt) -> None:
    """Fig. 5 (E5, v6): left, the routes test drawn (routes_drawing); right, another item moved, at the layer fixed in
    advance, per model two stacked rows of lookup answers, whole change and without the address, each identity /
    position share with its 95% interval, the original answer empty; under the second row a thin light grey bar for
    the position answers without a random part of the same size; the value's share (0.00 on every row) in the legend,
    not as a box per row (v6 iteration 2). Blocks: 9B, 27B, Muse; Lightning (batch 52) the fourth, at L14, its bars
    hollow (outlined); the 122B the fifth (Q122_ROUTES, its gate lowered after the data: ° on its name and n). The
    keep-only arms are in s05."""
    # Dan (21:55): no line under the plot; the routes are defined once, in the README's Setup
    h, cap, lt_in, q_in = 7.93 + 0.3, 0.35, 1.08, 1.08  # lt_in, q_in: Lightning's and the 122B's blocks
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, "The lookup takes the identity route or the position route, never the value",
            "Left: where each route sends the lookup. Right: lookup answers with the change placed at L.",
            limit=80)  # fmt: skip
    left_ax = fig.add_axes((0.01, (0.22 + cap + lt_in + q_in + 0.3) / h, 0.40, 3.75 / h))
    routes_drawing(plt, left_ax)
    left_ax.text(0, 1.015, "The routes test", transform=left_ax.transAxes, fontsize=12, weight="bold", va="bottom")
    ax_in = 3.24 + lt_in + q_in
    ax = fig.add_axes((0.625, (0.54 + cap + 0.3) / h, 0.355, ax_in / h))
    models = [(t, m) for t, m, _ in S.MODELS if m != "122b"]  # 9B, 27B, Muse; then Lightning and the 122B
    gap, y, ticks, labels, ns, values, block_y = 2.75, 0.0, [], [], {}, [], {}
    for target, m in (*models, LT[:2], Q122[:2]):
        lt, q = m == "lightning", m == "122b"
        path = LT_ROUTES if lt else Q122_ROUTES if q else None
        run = rel(path) if path else ROUTE_RUNS[m][0]
        v = json.loads(path.read_text()) if path else latest(pins.RESULTS_DIR / "x6_routes" / run,
                                                              "verdict-*/verdict.json")  # fmt: skip
        rows = {r["arm"]: r for r in (v or {}).get("rows", []) if r["condition"] == "C2"}
        block_y[m] = y
        ax.text(-0.02, y + 0.62, name_of(m, lowered=q), transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=S.FONT, weight="bold")  # fmt: skip
        for i, (arm, label, rand) in enumerate(ROUTE_ROWS):
            yi = y - i
            ticks.append(yi)
            labels.append(label)
            r = rows.get(arm)
            if r is None:
                S.empty(ax, "not run")
                continue
            if i == 0:
                ns[m] = str(r["n"])
            left = 0.0
            for route in ("identity", "position"):
                sh = r["share"][route]
                fill = (
                    {"fc": "white", "ec": ROUTE_COL[route], "lw": 1.6} if lt else {"color": ROUTE_COL[route], "lw": 0}
                )
                ax.barh(yi, sh[0], left=left, height=0.62, **fill)
                ax.plot([left + sh[1], left + sh[2]], [yi - 0.2, yi - 0.2], color="#1e1e1e", lw=1.2,
                        solid_capstyle="butt")  # fmt: skip
                if sh[0] >= 0.15:
                    ax.text(left + sh[0] / 2, yi + 0.06, f"{sh[0]:.2f}", ha="center", va="center", fontsize=S.FONT,
                            color="white" if route == "identity" and not lt else "#222222")  # fmt: skip
                left += sh[0]
            ax.barh(yi, 1 - left, left=left, height=0.62, **S.EMPTY)  # the original answer (and other)
            for route, _ in ROUTES:
                S.record("fig05", target, f"another item moved, {arm}: {route} share", *r["share"][route], n=r["n"],
                         source=run)  # fmt: skip
            values.append(r["share"]["value"][0])  # recorded above; shown once, in the legend
            rr = rows.get(rand) if rand else None
            if rr is not None:
                pos = rr["share"]["position"]
                yc = yi - 0.48
                ax.barh(yc, pos[0], height=0.16, **({"fc": "white", "ec": "#9a9a9a", "lw": 1.0} if lt
                                                    else {"color": S.COL["control"], "lw": 0}))  # fmt: skip
                ax.plot([pos[1], pos[2]], [yc, yc], color="#7a7a7a", lw=1.0, solid_capstyle="butt")
                ax.text(pos[2] + 0.02, yc, f"{pos[0]:.2f}", va="center", fontsize=S.FONT, color=S.COL["muted"])
                S.record("fig05", target, f"another item moved, {rand}: position share", *pos, n=rr["n"], source=run)
        y -= gap
    ax.set_xlim(0, 1.06)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax.spines["bottom"].set_bounds(0, 1)
    ax.set_ylim(y + gap - 1.75, 1.0)
    ax.set_yticks(ticks, labels)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("share of lookups")
    ax.text(-0.5, 1 + 0.29 / ax_in, "Lookup answers at L", transform=ax.transAxes, fontsize=12, weight="bold",
            va="bottom")  # fmt: skip
    S.panel_tag(ax, ", ".join(ns[m] for _, m in models), "fixed")
    # Lightning's n with its open glyph, the 122B's with its gate's °, each beside its own block
    for m, glyph in (("lightning", S.STATUS_GLYPH["after"]), ("122b", S.STATUS_GLYPH["fixed"] + S.LOWERED)):
        ax.text(1.0, block_y[m] + 0.62, f"n = {ns[m]}  {glyph}", ha="right", va="center",
                transform=ax.get_yaxis_transform(), fontsize=S.FONT, color=S.COL["muted"])  # fmt: skip
    fig.text(0.01, 0.08 / h, f"{LT_NOTE}\n{Q122_NOTE}", color=S.COL["muted"], fontsize=S.FONT - 1, va="bottom",
             linespacing=1.3)  # fmt: skip
    top = max(values, default=0.0)
    value_label = "value: 0.00 in every row" if top < 0.005 else f"value: at most {top:.2f}"
    hs = [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL["identity"]), plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL["position"]),
          plt.Rectangle((0, 0), 1, 1, **S.EMPTY), plt.Rectangle((0, 0), 1, 0.35, color=S.COL["control"]),
          plt.Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["value"], lw=1.3)]  # fmt: skip
    legend(fig, hs, ["identity route", "position route", "the original answer", "position, a random part removed",
                     value_label],
           1 - 0.605 / h, ncol=3)  # fmt: skip
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


ADDRESS_COL = "#a63d40"  # v6: the address's own hue (no other meaning on the README figures)
SWAP_MARK = {
    "9b": ("o", "-"),
    "27b": ("s", "--"),
    "muse": ("^", ":"),
    "lightning": ("D", "-."),
    "122b": ("v", (0, (6, 2, 1, 2))),
}  # Fig. 7 (c)
# Fig. 7 (b): a model's two arms B_STEP[0] apart, its two rows B_STEP[1] apart, the bar and its random part at B_DY:
# room for each value label on its own line (five models since the 122B joined)
B_STEP, B_DY = (2.1, 1.0), (0.25, -0.27)
# Fig. 7 (c): each model's end label (dx, dy, ha) beside its last point; the 9B's, the 122B's and Lightning's end close
# together: the 9B's above its point, the 122B's under its own, Lightning's up and to the left of its point
END_LABEL = {"Muse": (0.07, 0.06, "left"), "Lightning": (-0.07, 0.06, "right"), "9B": (0.07, 0.03, "left"),
             "122B" + S.LOWERED: (0.07, -0.05, "left")}  # fmt: skip


def route_row(run: str, arm: str) -> dict:
    """The routes test's C2 row of an arm (another item moved) from run's newest verdict."""
    v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
    r = next((r for r in (v or {}).get("rows", []) if r["condition"] == "C2" and r["arm"] == arm), None)
    assert r is not None, f"{run}: no C2 row for {arm}"
    return r


def hbar(ax, y: float, v, col: str, h: float, label: bool = True, ec=None) -> None:
    """A horizontal share bar with its 95% whisker and, if label, its value at the right of the whisker."""
    ax.barh(y, v[0], height=h, color=col, lw=0, zorder=2)
    ax.plot([v[1], v[2]], [y, y], color="#1e1e1e" if ec is None else ec, lw=1.2, zorder=3, solid_capstyle="butt")
    if label:
        ax.text(max(v[0], v[2]) + 0.025, y, f"{v[0]:.2f}", va="center", fontsize=S.FONT,
                color=S.COL["muted"] if col in (S.COL["control"], "white") else "#1e1e1e")  # fmt: skip


def f07_writes(plt) -> None:
    """E6 (v6), three panels, 9B / 27B / Muse. (a) The locker probe at the bridge word, locker-first scenes (x0_probe
    v4: the README's v4_b_before_<m>) against its layout baseline (v4_b_layout_before_<m>). (b) The routes test,
    another item moved, at L: the position share without the address against without a random part (same size)
    (rt_C2_no_alf_position_<m>, rt_C2_no_alf_rand_position_<m>) and with only the address against only a random part
    (rtk_C2_keep_alf_position_<m>, rtk_C2_keep_alf_rand_position_<m>). (c) The swap by dose (x × a real change's
    size): the lookups sent to the target locker, all locker pairs pooled (the README's x8_t<s>_<m>, 95% band), and a
    random vector of the same size; the mean over locker pairs (the 26 Oct line) is still recorded. The recall's
    answers under the strongest swap: figures/supp/s07_recall_follows_swap. Lightning (batch 52, hollow) in each panel
    from its coverage folders (LT_PROBE, LT_ROUTES, LT_SWAP); its swap has no recall stage, so its real change's dose
    s* is the recall stage's formula on the run's manifest norms (scripts/x8_write.py). The 122B the fifth slot in
    each panel (Q122_PROBE, Q122_ROUTES / Q122_KEEP, Q122_SWAP with its recall stage Q122_RECALL), filled, its routes
    and swap runs marked ° (their gate lowered to 0.75 after the data)."""
    from scripts import x0_details as XD

    h = 11.3
    fig = plt.figure(figsize=(S.WIDTH, h))

    def box(left: float, width: float, top_in: float, bottom_in: float) -> tuple[float, float, float, float]:
        return (left, 1 - bottom_in / h, width, (bottom_in - top_in) / h)

    S.title(fig, "The address carries the position route; swapping it moves the lookup",
            "A: a probe at the bridge word. B: without the address, or with only the address, at L. C: the swap, by dose.")  # fmt: skip
    a = fig.add_axes(box(0.185, 0.21, 2.1, 6.8))
    b = fig.add_axes(box(0.675, 0.27, 2.1, 6.8))
    c = fig.add_axes(box(0.155, 0.70, 8.0, 10.1))
    head = {"fontsize": 12, "weight": "bold", "va": "bottom", "linespacing": 1.05}
    fig.text(0.01, 1 - 1.78 / h, "A  A probe reads the address", **head)
    # B's claim on two lines, from the left edge of its row labels
    fig.text(0.44, 1 - 1.78 / h, "B  Without the address, position answers go;\n      with only the address, they come back",
             **head)  # fmt: skip
    names = [NAMES[m] for _, m, _ in V6_MODELS] + ["Nemotron 3.5\nLightning", NAMES["122b"]]  # in full here; "9B" after

    # (a) the probe against the layout alone
    ns_a = []
    for i, (target, m, _) in enumerate((*V6_MODELS, LT, Q122)):
        lt = m == "lightning"
        path = LT_PROBE if lt else Q122_PROBE if m == "122b" else None
        if path:
            src = rel(path)
            rows = {(r["target"], r["stratum"]): r for r in json.loads(path.read_text())["rows"]
                    if r["subset"] == "all"}  # fmt: skip
        else:
            src, rows = XD.probe_v4_rows(m)
        r = rows[(XD.PROBE_TARGETS["slot"], XD.PROBE_ORDERS["first"])]
        for key, v in () if lt else ((f"v4_b_before_{m}", r["probe"]), (f"v4_b_layout_before_{m}", r["layout"])):
            assert N[key] == f"{v[0]:.2f}", (key, N[key], v)  # the README's number, from the same file
        hbar(a, -i + 0.13, r["probe"], ADDRESS_COL, 0.42)
        if lt:  # hollow
            a.patches[-1].set(facecolor="white", edgecolor=ADDRESS_COL, lw=1.6)
        hbar(a, -i - 0.24, r["layout"], "white", 0.16, ec="#7a7a7a")
        # the layout baseline: hatched, so light grey stays the random part's alone
        a.patches[-1].set(edgecolor="#9a9a9a", hatch="////", lw=0.6)
        S.record("fig07", target, "the locker probe at the bridge word, locker-first scenes", *r["probe"], n=r["n"],
                 source=src)  # fmt: skip
        S.record("fig07", target, "the locker probe's layout baseline, locker-first scenes", *r["layout"], n=r["n"],
                 source=src)  # fmt: skip
        ns_a.append(str(r["n"]))
        if i == 0:  # Dan (21:50): the panel names its two bars, on its first row
            a.text(0.03, -i + 0.13, "probe", va="center", fontsize=S.LABEL_PT, color="white", zorder=4)
            a.text(max(r["layout"][0], r["layout"][2]) + 0.33, -i - 0.24, "layout", va="center", fontsize=S.LABEL_PT,
                   color=S.COL["muted"])  # fmt: skip
    a.set_yticks([0, -1, -2, -3, -4], names)
    a.set_ylim(-4.55, 0.5)

    # (b) without the address / with only the address, each against its random part
    ns_b = []
    ticks, labels = [], []
    lt_rows = {r["arm"]: r for r in json.loads(LT_ROUTES.read_text())["rows"] if r["condition"] == "C2"}
    q_rows = {r["arm"]: r for p in (Q122_ROUTES, Q122_KEEP) for r in json.loads(p.read_text())["rows"]
              if r["condition"] == "C2" and (p == Q122_KEEP) == r["arm"].startswith("keep")}  # fmt: skip
    for i, (target, m, _) in enumerate((*V6_MODELS, LT, Q122)):
        lt, q = m == "lightning", m == "122b"
        run, keep = (None, None) if lt or q else ROUTE_RUNS[m]
        for j, (rn, arm, ctl, label, key) in enumerate(
                ((run, "no_alf", "no_alf_rand", "without the address", "rt_C2_no_alf"),
                 (keep, "keep_alf", "keep_alf_rand", "only the address", "rtk_C2_keep_alf"))):  # fmt: skip
            y = -B_STEP[0] * i - B_STEP[1] * j
            got, rand = (
                (lt_rows[arm], lt_rows[ctl]) if lt else (q_rows[arm], q_rows[ctl]) if q
                else (route_row(rn, arm), route_row(rn, ctl))
            )  # fmt: skip
            key = key.replace("rt_", "rtg_") if q and key == "rt_C2_no_alf" else key  # the 122B's g75 keys
            for k, row in () if lt else ((f"{key}_position_{m}", got), (f"{key}_rand_position_{m}", rand)):
                stated = S.parse(N[k])
                assert stated is not None, k
                assert stated[0] == round(row["share"]["position"][0], 2), (k, N[k])
            hbar(b, y + B_DY[0], got["share"]["position"], S.COL["position"], 0.3)
            if lt:  # hollow
                b.patches[-1].set(facecolor="white", edgecolor=S.COL["position"], lw=1.6)
            hbar(b, y + B_DY[1], rand["share"]["position"], S.COL["control"], 0.12)
            if lt:
                b.patches[-1].set(facecolor="white", edgecolor="#9a9a9a", lw=1.0)
            if i == 0 and j == 0:  # Dan (21:50): the panel names its two bars, on its first row
                gp, rp = got["share"]["position"], rand["share"]["position"]
                b.text(max(gp[0], gp[2]) + 0.22, y + B_DY[0], "position answers", va="center", fontsize=S.LABEL_PT,
                       color="#1e1e1e")  # fmt: skip
                b.text(max(rp[0], rp[2]) + 0.22, y + B_DY[1], "random", va="center", fontsize=S.LABEL_PT,
                       color=S.COL["muted"])  # fmt: skip
            if j == 0:
                ns_b.append(str(got["n"]))
            ticks.append(y)
            labels.append(f"{SHORT[m]}{S.LOWERED if q else ''} · {label}")
            src = (rel(LT_ROUTES) if lt else rel(Q122_KEEP if j else Q122_ROUTES) if q
                   else str(newest(pins.RESULTS_DIR / "x6_routes" / rn, "verdict-*/verdict.json").relative_to(S.REPO)))  # fmt: skip
            S.record("fig07", target, f"another item moved, {arm}: position share", *got["share"]["position"],
                     n=got["n"], source=src)  # fmt: skip
            S.record("fig07", target, f"another item moved, {ctl}: position share", *rand["share"]["position"],
                     n=rand["n"], source=src)  # fmt: skip
    b.set_yticks(ticks, labels)
    b.set_ylim(ticks[-1] - 0.6, 0.55)
    for ax in (a, b):
        ax.set_xlim(0, 1.18)
        ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.spines["bottom"].set_bounds(0, 1)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_axisbelow(True)
    a.set_xlabel("share of scenes")
    b.set_xlabel("position answers (share)")
    S.panel_tag(a, ", ".join(ns_a), "after")
    # Lightning: open; the 122B: its n marked ° (gate lowered after the data), its rule fixed in advance
    S.panel_tag(b, f"{', '.join(ns_b[:3])}  {S.STATUS_GLYPH['fixed']};  {ns_b[3]}  {S.STATUS_GLYPH['after']};  "
                   f"{ns_b[4]}{S.LOWERED}", "fixed")  # fmt: skip

    # (c) the swap by dose, pooled over the locker pairs, against a random vector of the same size
    ends = []
    for target, m, _ in (*V6_MODELS, LT, Q122):
        lt = m == "lightning"
        if m == "122b":
            v, run_name, src = json.loads(Q122_SWAP.read_text()), rel(Q122_SWAP), rel(Q122_SWAP)
            s_real = json.loads(Q122_RECALL.read_text())["s_real"]
        elif lt:
            v, run_name, src = json.loads(LT_SWAP.read_text()), rel(LT_SWAP), rel(LT_SWAP)
            norms = v["manifest"]["norms"]  # scripts/x8_write.py's recall stage: s* = median ||U U^T Delta|| / step
            s_real = {pair: norms["median_U_UT_delta_C2"] / step for pair, step in norms["step"].items()}
        else:
            root = pins.RESULTS_DIR / "x8_write" / X8_RUNS[m]
            v, rc = latest(root, "verdict-*/verdict.json"), latest(root, "recall-*/recall.json")
            assert v is not None, f"{X8_RUNS[m]}: no verdict"
            assert rc is not None, f"{X8_RUNS[m]}: no recall stage"
            run_name, src, s_real = (
                X8_RUNS[m],
                str(newest(root, "verdict-*/verdict.json").relative_to(S.REPO)),
                rc["s_real"],
            )
        mean_star = sum(s_real.values()) / len(s_real)
        mk, ls = SWAP_MARK[m]
        by_s: dict[float, list[float]] = {}  # the mean over locker pairs, as recorded since 26 Oct
        for cell in v["cells"]:
            if cell["kind"] == "write" and cell["pair"] is not None:
                by_s.setdefault(cell["s"], []).append(cell["target"][0])
        for s, t in sorted(by_s.items()):
            S.record("fig07", target, f"lookup target share, mean over locker pairs, s = {s:g}", round(sum(t) / len(t), 4),
                     source=run_name)  # fmt: skip
            S.record("fig07", target, f"dose (s / mean s*), s = {s:g}", round(s / mean_star, 4), source=run_name)
        for kind, col in (("write", S.COL["lookup"]), ("random", S.COL["control"])):
            pts = sorted((cell["s"], cell["target"], cell["n"]) for cell in v["cells"]
                         if cell["kind"] == kind and cell["pair"] is None)  # fmt: skip
            x = [s / mean_star for s, _, _ in pts]
            y = np.array([t for _, t, _ in pts])
            hollow = {"mfc": "white", "mew": 1.5} if lt else {}
            if kind == "write":
                c.fill_between(x, y[:, 1], y[:, 2], color=col, alpha=0.15, lw=0, zorder=1)
                c.plot(x, y[:, 0], color=col, ls=ls, lw=2.2, marker=mk, ms=6.5, zorder=3, **hollow)
                ends.append((x[-1], y[-1, 0], SHORT[m] + (S.LOWERED if m == "122b" else "")))
            else:
                c.plot(x, y[:, 0], color=col, ls=ls, lw=1.6, marker=mk, ms=6, zorder=2, **hollow)
                c.vlines(x, y[:, 1], y[:, 2], color=col, lw=1.2, zorder=2)
            for (s, t, n), xi in zip(pts, x, strict=True):
                # the random rows keep their 26 Oct quantity (scripts/joint_figures.py's j3 reads it)
                q = (f"swap: lookups to the target locker, pooled over locker pairs, dose {xi:.2f} (s = {s:g})"
                     if kind == "write" else f"lookup target share, random direction, s = {s:g}")  # fmt: skip
                S.record("fig07", target, q, *t, n=n, source=src)
    for xe, ye, name in ends:  # Muse and the 27B end near the same share: Muse's label above its line; Lightning's
        # last point sits on the 9B's line: its label under it
        dx, dy, ha = END_LABEL.get(name, (0.07, -0.02, "left"))
        c.text(xe + dx, ye + dy, name, va="center", ha=ha, fontsize=S.FONT,
               color=S.COL["lookup"], weight="bold")  # fmt: skip
    c.axvline(1, color="#555555", lw=1, ls=":", zorder=0)
    c.text(1.04, 0.97, "as large as\na real change", transform=c.get_xaxis_transform(), va="top", color="#555555",
           linespacing=1.0)  # fmt: skip
    c.text(2.05, 0.035, "a random part (same size)", va="bottom", color=S.COL["muted"])
    c.set_xlim(0, 3.4)
    c.set_xticks([0, 1, 2, 3])
    c.set_ylim(0, 1)
    c.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    c.grid(axis="y", color="#eeeeee")
    c.set_xlabel("dose, in units of a real change")
    c.set_ylabel("lookups answering the\nswapped-in locker (share)")
    c.set_title("C  A swap sends the lookup to the swapped-in locker", loc="left", fontsize=12, weight="bold", pad=26)
    S.panel_tag(c, "600 per dose and model", "fixed")
    hs = [plt.Rectangle((0, 0), 1, 1, color=ADDRESS_COL), plt.Rectangle((0, 0), 1, 1, color=S.COL["position"]),
          plt.Line2D([], [], color=S.COL["lookup"], lw=2.2), plt.Rectangle((0, 0), 1, 0.4, color=S.COL["control"]),
          plt.Rectangle((0, 0), 1, 0.4, fc="white", ec="#9a9a9a", hatch="////", lw=0.6)]  # fmt: skip
    legend(fig, hs, ["address (probe)", "position answers", "lookup", "a random part (same size)", "layout baseline"],
           1 - 0.62 / h, ncol=3)  # fmt: skip
    fig.text(0.01, 0.08 / h, f"{LT_NOTE}\n{Q122_NOTE}", color=S.COL["muted"], fontsize=S.FONT - 1, va="bottom",
             linespacing=1.3)  # fmt: skip
    S.save(fig, "fig07_writes")


def s07_recall_follows_swap(plt) -> None:
    """Supplementary to E6 (Fig. 7's lower panel until v6; after the data): per model (the 122B included), the
    recall's changed answers under the strongest swap (s = 4): the target locker's item, the third item, other."""
    fig, bars = plt.subplots(figsize=(S.WIDTH, 4.2))
    fig.subplots_adjust(left=0.21, right=0.80, top=0.68, bottom=0.22)
    S.title(fig, "Under the strongest swap, a changed recall names the target's item",
            "The recall's changed answers under the swap at its largest dose; after the data.")  # fmt: skip
    third, other = "#d98cb3", "#8a8a8a"
    for i, (target, m, _) in enumerate(S.MODELS):
        rc = latest(pins.RESULTS_DIR / "x8_write" / X8_RUNS[m], "recall-*/recall.json")
        if rc is None:
            bars.text(0.5, -i, "not run", ha="center", va="center", color=S.COL["muted"])
            continue
        got = rc["changed_by_item"].get("write|4", {})
        total = sum(got.values())
        left = 0.0
        for item, col, label in (("target", S.COL["lookup"], "the written locker's item"), ("third", third, "the third item"),
                                 ("other", other, "other")):  # fmt: skip
            share = sum(
                n for it, n in got.items() if (it == item if item != "other" else it not in ("target", "third"))
            )
            share = share / total if total else 0
            bars.barh(-i, share, left=left, height=0.6, color=col, edgecolor="white", lw=0.8)
            if share >= 0.1:
                bars.text(left + share / 2, -i, f"{share:.2f}", ha="center", va="center", fontsize=S.FONT,
                          color="white" if item != "third" else "#222222")  # fmt: skip
            # the quantity keeps its 26 Oct wording (data.csv keys); the figure says "swap"
            S.record("s07", target, f"recall changed under the strongest write (s = 4): {label}", round(share, 4),
                     n=total, source=X8_RUNS[m])  # fmt: skip
            left += share
        bars.text(1.02, -i, f"n {total} changed", va="center", fontsize=S.FONT, color=S.COL["muted"])
    bars.set_xlim(0, 1)
    bars.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    bars.set_xlabel("share of the recall's changed answers")
    bars.set_yticks([-i for i in range(len(S.MODELS))], [name_of(m, m in LOWERED_M) for _, m, _ in S.MODELS])
    bars.tick_params(axis="y", length=0)
    S.panel_tag(bars, None, "after")
    legend(fig, [plt.Rectangle((0, 0), 1, 1, color=c) for c in (S.COL["lookup"], third, other)],
           ["the target locker's item", "the third item", "other"], 0.80)  # fmt: skip
    fig.text(0.01, 0.015, f"{S.LOWERED} gate lowered to 0.75 after the data.", color=S.COL["muted"])
    S.save(fig, "s07_recall_follows_swap", supp=True)


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
    # Dan 27 Oct ~11:20: the title and the subtitle's refit line; v6 iteration 2: "address", one subtitle line (the
    # data.csv quantities keep their 27 Oct wording)
    S.title(fig, "The split carries over to other texts; the address must be refit for each format",
            "The lookup's extra loss beyond a random part (same size); a refit address found on "
            f"{' and '.join(found_on)}, not {' and '.join(not_on)}.", limit=86)  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(0.01, at(0.95), "(a) The address fit on simple scenes, not refit", **head)
    black = "#222222"
    sh, sl = S.status_handles()
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=black, ms=7), plt.Line2D([], [], marker="o", ls="", color=S.COL["position"], ms=7), *sh],
           ["without the J++ part", "without the address (fit on simple scenes)", *sl], at(1.2))  # fmt: skip
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

    fig.text(0.01, at(5.65), "(b) The address refit per format, fixed in advance", **head)
    fig.text(0.01, at(5.92), "Varied scenes: fit on half of them, measured on the other half.", fontsize=S.FONT,
             color=S.COL["muted"], va="top")  # fmt: skip
    orange = S.COL["position"]
    legend(fig, [plt.Line2D([], [], marker="o", ls="", mfc="white", mec=orange, mew=1.6, ms=7),
                 plt.Line2D([], [], marker="o", ls="", color=orange, ms=7)],
           ["without the address (fit on simple scenes)", "without the refit address"], at(6.25))  # fmt: skip
    grid_b = fig.add_gridspec(1, 4, left=0.17, right=0.985, top=at(7.05), bottom=at(8.75), wspace=0.12)
    for j, (target, m, _) in enumerate(S.MODELS):
        ax = fig.add_subplot(grid_b[0, j])
        S.extra_axis(ax)
        ax.set_title(SHORT[m], fontsize=S.FONT, weight="bold")  # full names in (a), short after
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
         lambda m: f"numbers:x8_t4_{m}"),  # v6: Fig. 7 drops the 122B; x8_t4 is every model's pooled swap share
        ("Pointer", "the recall follows the write", v4["The recall follows the write"],
         lambda m: "s07:recall changed under the strongest write (s = 4): the written locker's item"),
        ("Pointer", "counts mentions, not text position", v4["First-mentioned item,\nnot position in the text"],
         lambda m: "s08b:(c) neutral sentence B1: the code's shift in positions"),
        ("Pointer", "a pick sentence first moves the lookup to identity", pick_first,
         lambda m: "fig08:45a, first-locker moves, whole change, a pick naming the first-locker item: identity share"),
        ("Pointer", "refit per format", refit, lambda m: "fig09:(b) prose: lookup extra loss without the refit pointer"),
        ("Pointer", "the pointer fit on simple scenes transfers", transfer, lambda m: f"numbers:tptr_pooled_{m}"),
        ("Limits", "identity outside J++ is specific", specific, lambda m: f"numbers:x45e_cut_{m}"),
        ("Limits", "the recall needs only the J++ part, locker after the pick", only_jpp,
         lambda m: "s03:(b) main test (two people swap picks), locker after the pick: recall extra loss"),
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


# Fig. 11 v6 (Dan's card list, 28 Oct): the README's claims table as a figure. Rows in the table's order (ids checked
# against docs/README.template.md's "## Claims" table); per model a cell read off that table's Models and Grade columns
# (agent's reading, UNVERIFIED), taken from the v5 cells (scorecard_rows, asserted against the verdicts) wherever a v6
# row restates a v5 row; the 122B only where a v5 row covers it. Each cell's data.csv key is the number the claims
# table quotes for that model, else the v5 row's.
SC6_FIELDS: tuple[str, ...] = ("id", "group", "claim", "was", "model", "cell", "flag", "data.csv key", "hand-checked")
SC6_SYMBOL = {**CELL_SYMBOL, "pending": ("…", "#8a8a8a")}
SC6_MODELS = ("9b", "27b", "muse")  # v6 iteration 2: the three README models only (the 122B in supplements)
# Dan's plain findings (28 Oct 21:20): Fig. 11 and the README's claims table hold his twelve sentences, in his order,
# under three groups (the figure's margin headers), numbered 1-12 on the page only; "was" is the claims-table row each
# rewrites (one to one: no row split or merged) and gives its cells (scorecard_v6_rows). Two of his words differ, for
# the page's lint: "the change" for "the edit" (11: "edit" is banned on the page) and "identity route ... position
# route" for "identity ... position" (12: bare "identity" is banned on the figures).
FINDINGS = (
    ("Two readers, one word", "The recall follows the lens part of the bridge word; the lookup follows the rest", "1"),
    ("Two readers, one word", "The recall does not need the lens part at one layer; it has other copies", "5"),
    ("Two readers, one word", "The recall also reads the item's earlier mention", "8"),
    ("What the lookup reads", "The lookup goes by which item it is or where its locker sits, never by the number", "2"),
    ("What the lookup reads", "The lookup's “which item” lives outside the lens", "6"),
    ("What the lookup reads", "The address can be removed, and a swap redirects the lookup", "4a"),
    ("What the lookup reads", "Adding the address alone brings position answers back", "4b"),
    ("What the lookup reads",
     "With six lockers, swaps between given lockers work on most pairs; the code's size is not settled", "10"),
    ("What the lookup reads", "The lens cannot read the address", "9a"),
    ("Where and when the link is made",
     "The bridge word redirects the lookup only when its locker sentence came first", "3"),
    ("Where and when the link is made", "Lookups the change at L misses were read from the bridge word before L", "11"),
    ("Where and when the link is made",
     "The address is readable before the lookup uses it, and the lookup never reads the value", "7"),
)  # fmt: skip
# Fig. 12's rows (Dan's figures brief, ~18:30): off the main figure until the reruns on Zach's P items land (Dan
# 21:20); kept in the supplement version (s11_scorecard_all), in their own group
FIG11_SUPP = (("2×2", "Both operations, both datasets: one direction"),
              ("Z1", "Our removal on Zach's passages: the split, by degree"))  # fmt: skip
FIG11_SUPP_GROUP = "On Zach's passages (Fig. 12)"
# Dan's caption: "a: the order split was fixed after the data": the finding that rests on the sentence-order split
# (claims-table row 3; E10: "order split post hoc") carries "a" on every model; no cell's mark changes
FIG11_AFTER = {"3"}
TEMPLATE = S.REPO / "docs" / "README.template.md"


def two_by_two_cells() -> tuple[dict, dict, dict]:
    """Fig. 11's 2 x 2 and Z1 rows (agent's reading of Fig. 12, after the data, UNVERIFIED). 2 x 2, per model over its
    four cells (our gap, the ladder's rung 6 on our scenes, Z1's gap, his stored M - K): ok if every cell is present
    and above zero (an interval's lower end; rung 6's point beyond 0.10); ~ if those present hold but one is missing
    (not run, too few switches, the Muse's rung 6 outside his band); x if a present cell does not hold. Z1 (marked
    "degree", Dan): the rule's own reading per model (the split holds -> ok, in between -> ~, the lookup follows the lens
    -> x), with the flag 'degree'. Returns (2 x 2 cells, Z1 cells, Z1's data.csv key per model)."""
    lad = {m["target"]: m for m in json.loads((latest_verdict(LADDER_VERDICT) / "x49_2.json").read_text())["models"]}
    z1v = {m["target"]: m for m in json.loads((latest_verdict(Z1_VERDICT) / "z1.json").read_text())["models"]}
    two, z1, key = {"122b": ("-", "")}, {"122b": ("-", "")}, {"122b": ""}
    for target, m, _ in S.MODELS:
        if m == "122b":
            continue
        zm = z1v.get(target, {})
        lr = zm.get("layer_results", {}).get(str(zm.get("layers", [None])[0]))
        z_ok = None if lr is None or lr["lookup"]["switched_whole"] < VALID_SWITCHES else lr["gap"][1] > 0
        ld = lad.get(target, {})
        r6 = None
        if 6 in ld.get("rungs", []) and m != "muse":  # the Muse's rung 6 is hollow (placed outside his band)
            rc, lk = (ld["cells"][w]["all"]["cost"]["6"][0] for w in ("recall", "lookup"))
            r6 = rc - lk > LOOKUP_BAR
        his = zm.get("beside", {}).get("full")
        # the Z1 cell is hollow in Fig. 12 only because a variant reruns tonight: it counts as present; the Muse's rung
        # 6 is hollow because it ran outside his band: it counts as missing
        his_ok = None if his is None else his["paper10"]["m_minus_k"][1] > 0
        cells4 = [interval(f"contrast_{m}")[1] > 0, r6, z_ok, his_ok]
        held = [c for c in cells4 if c is not None]
        two[m] = ("x" if not all(held) else "ok" if len(held) == 4 else "~", "a")
        verdict = (lr or {}).get("verdict", "")
        z1[m] = ("ok" if verdict.startswith("the split holds") else "x" if "follows the lens" in verdict else
                 "-" if not verdict else "~", "degree")  # fmt: skip
        key[m] = ("fig12:our removal, his passages: gap" if z_ok is not None
                  else "fig12:our removal, his passages: lookup switches under the whole change")  # fmt: skip
    return two, z1, key


def claims_table(path: Path = TEMPLATE) -> list[tuple[str, str]]:
    """The first two columns (id, claim) of the template's "## Claims" table, in order."""
    lines = path.read_text().split("## Claims", 1)[1].splitlines()
    rows = []
    for ln in lines:
        if ln.startswith("|"):
            rows.append(ln)
        elif rows:
            break
    return [(ln.split("|")[1].strip(), ln.split("|")[2].strip()) for ln in rows[2:]]


def anatomy_cell(target: str) -> tuple[str, str]:
    """Finding 12 on a model from 47.8's verdict (x47_8.json, the one Fig. 6b draws): 'ok' where its rules read as on
    the 9B and Muse, whose cells are 'ok' (a: identity before position, b: the address readable before it is used,
    d: never the value, all held; c failed on all three), else 'pending'. The 27B's rows are 49.4's reduced grid."""
    v = json.loads((latest_verdict("x47_anatomy/x47_8-*") / "x47_8.json").read_text())
    rules = {m["target"]: m["rules"] for m in v["models"] if m["status"] == "tested"}

    def read(r: dict) -> tuple:
        return tuple(r[k]["holds"] for k in ("a", "b", "c", "d"))

    assert read(rules["qwen3.5-9b"]) == read(rules["muse-glimmer-30b"]) == (True, True, False, True), rules
    return ("ok", "") if target in rules and read(rules[target]) == read(rules["qwen3.5-9b"]) else ("pending", "")


def scorecard_v6_rows(v5_rows: list[dict]) -> list[dict]:
    """Fig. 11's rows (Dan's plain findings, 21:20): (id, group, claim, was, model, cell, flag, data.csv key,
    hand-checked) for the 9B, 27B and Muse; FINDINGS' twelve sentences (id 1-12, each with the cells of the claims-table
    row it rewrites, 'was'), then FIG11_SUPP's two rows (the supplement version). v5_rows: scorecard_rows()."""
    v5 = {(r["claim"], r["model"]): (r["cell"], r["flag"]) for r in v5_rows}
    name = {m: n for _, m, n in S.MODELS}

    def was(claim: str, m: str) -> tuple[str, str]:
        return v5[(claim, name[m])]

    def cells(ok3: str = "ok", /, **over: str | tuple[str, str]) -> dict[str, tuple[str, str]]:
        """ok3 on the 9B, 27B and Muse, '-' on the 122B, with per-model overrides (m=cell or (cell, flag))."""
        out = {m: (ok3, "") for m in ("9b", "27b", "muse")} | {"122b": ("-", "")}
        return out | {m: v if isinstance(v, tuple) else (v, "") for m, v in over.items()}

    three = ("9b", "27b", "muse")
    two, z1, z1_key = two_by_two_cells()
    spec = (  # id, figure label, cells, data.csv key per model
        ("1", "In a conflict the recall follows the J++ part",
         cells(**{m: was("main test", m) for m in three}, **{"122b": "~"}), lambda m: f"numbers:contrast_{m}"),
        ("2×2", "Both operations, both datasets: one direction", two,
         lambda m: "fig12:our removal, our scenes (main test): gap"),
        ("Z1", "Our removal on Zach's passages: the split", z1, lambda m: z1_key[m]),
        ("2", "Lookup by identity route or position route, never the value",
         {m: was("never the value", m) for m in SC6_MODELS}, lambda m: "s05:another item moved, whole: value share"),
        ("3", "Locker before the pick: the bridge word redirects",
         cells(**{m: was("the link sits in the locker sentences, clean one-pick scenes", m) for m in three},
               **{"122b": ("~", "a")}),
         lambda m: "numbers:lk_order_before_122b" if m == "122b" else f"numbers:x45q_c_{m}"),
        ("4a", "The address can be removed; a swap moves the lookup", cells(**{"122b": ("ok", "a")}),
         lambda m: "s05:another item moved, no_alf: position share" if m == "122b"
         else f"numbers:rt_C2_no_alf_position_{m}"),
        ("4b", "Adding only the address creates position answers",
         {m: was("only it gives position answers", m) for m in SC6_MODELS},
         lambda m: f"numbers:rtk_C2_keep_alf_position_{m}"),
        ("5", "The recall follows, but does not need, the J++ part", cells(),
         lambda m: "fig01c:47.5: recall's answers kept at L, the J++ part's 25 directions taken out"),
        ("6", "The lookup's identity route runs outside the lens", cells(),
         lambda m: "e3_identity:47.1: identity answers lost beyond random without lens directions 26-100"),
        # the 27B from 49.4's reduced grid in 47.8's verdict (Dan's caption, 21:20: "The 27B's row 12 is from a
        # reduced layer grid"); it was pending until that grid landed
        ("7", "Identity route early, position late; address formed first", cells(**{"27b": anatomy_cell("qwen3.6-27b")}),
         lambda m: "fig06b:address formed: layer" if m == "27b"
         else "fig06c:D4: the address's mean overlap over every pair of window layers"),
        ("8", "The recall also reads the item's earlier mention",
         cells(**{m: was("the recall reads the earlier mention, locker before the pick", m) for m in three}),
         lambda m: f"numbers:x45p_d23_{m}"),
        ("9a", "The address does not read out through the lens", cells(),
         lambda m: "fig07b_verbal:47.0 (b) share rebuilt by 25 lens directions: pointer"),
        ("9b", "Asked to report the position, the lens stays blind", cells("-", **{"27b": "ok"}),
         lambda m: "e8_report:47.10: the report's extra loss without the address"),
        ("10", "Six lockers: one code per locker, no single shift", cells(**{"27b": "-"}),
         lambda m: "fig09b:47.2: pairwise writes reaching 25% (dose 2)"),
        ("11", "Lookups missed at L read the bridge word before L", cells(**{"27b": "-"}),
         lambda m: "s03e_cumulative:47.4 main, locker-first, lookup: before_L"),
        ("12", "A described bridge: the split holds", cells(**{"27b": "x"}),
         lambda m: "fig05c:47.3: lookup's extra loss without the J++ part" if m == "27b"
         else "fig05c:47.3: gap (recall's extra loss minus the lookup's)"),
        ("13", "The address must be refit per text format", {m: was("refit per format", m) for m in SC6_MODELS},
         lambda m: "fig09:(b) prose: lookup extra loss without the refit pointer"),
        ("14", "The lookup's errors are not address errors", cells("-", **{"9b": "ok"}),
         lambda m: "fig07c:47.13: wrong answers whose locker the address probe predicts"),
        ("15", "Identity outside J++: only partly specific",
         {m: was("identity outside J++ is specific", m) for m in SC6_MODELS}, lambda m: f"numbers:x45em_cut_{m}"),
        ("✗", "The J++ part keys the attribute; late MLPs carry it", cells("x", **{"27b": "-"}),
         lambda m: "fig10b:48.2 B, bridge_late: recall accuracy lost"),
        ("✗", "A person mark at the locker sentence", cells("x", **{"27b": "-"}),
         lambda m: "fig10c:48.3, probe at the item, locker after the pick (accuracy)"),
        ("✗", "The copying heads pass the rest at twice the J++ part", cells("x", **{"27b": "-"}),
         lambda m: "fig10d:48.4: the rule holds"),
        ("✗", "The address is the recall's second route", cells("x"),
         lambda m: "fig10e:48.5, (ii) (i) and the pointer write: recall names the written locker's item"),
        ("✗", "Blocking the pick sentence removes position only", cells("x", **{"27b": "-"}),
         lambda m: "fig09c_formation:47.6 (b): the formation rule holds"),
        ("✗", "The locker digit carries the hall question's address", cells("x", **{"27b": "-"}),
         lambda m: "fig09d:47.14: hall probe at the locker digit"),
        ("✗", "Map rules: one locker cell; the lookup stops first", cells("x", **{"27b": "-"}),
         # Fig. 3d draws the 9B only: Muse's D1 numbers are in its verdict, not in data.csv
         lambda m: "fig03d_depth_map:D1 clean, locker-first, lookup: last layer with the bridge word >= 0.3"
         if m == "9b" else ""),
        ("✗", "Positive control; 9B clean design; 27B strict bar", cells("x", **{"muse": "-"}),
         lambda m: "numbers:x45m_before_gap_9b" if m == "9b" else "numbers:x4_D_elements_27b"),
        ("…", "Pending: weights, the dereference, two sources",
         {m: ("pending", "") for m in SC6_MODELS}, lambda m: ""),
    )  # fmt: skip
    # Dan 21:20: the README's claims table holds his sentences, numbered 1-12 in his order, word for word
    table = claims_table()
    assert table == [(str(k), claim) for k, (_, claim, _) in enumerate(FINDINGS, 1)], \
        f"the README's claims table is out of step with Fig. 11's findings: {table}"  # fmt: skip
    by_id = {cid: (cl, key) for cid, _, cl, key in spec}
    assert len({was for *_, was in FINDINGS}) == len(FINDINGS), "a claims-table row rewritten twice"
    assert all(was in by_id for *_, was in FINDINGS), [was for *_, was in FINDINGS if was not in by_id]
    order = [(str(k), group, claim, was) for k, (group, claim, was) in enumerate(FINDINGS, 1)]
    order += [(cid, FIG11_SUPP_GROUP, claim, cid) for cid, claim in FIG11_SUPP]
    rows = []
    for cid, group, claim, was in order:
        cl, key = by_id[was]
        for m in SC6_MODELS:
            cell, flag = cl[m]
            if was in FIG11_AFTER:
                assert flag in ("", "a"), (was, m, flag)
                flag = "a"
            target = next(t for t, mm, _ in S.MODELS if mm == m)
            rows.append({"id": cid, "group": group, "claim": claim, "was": was, "model": name[m], "target": target,
                         "cell": cell, "flag": flag, "data.csv key": key(m) if cell not in ("-", "pending") else "",
                         "hand-checked": "no"})  # fmt: skip
    return rows


def f11_scorecard(plt) -> None:
    """Fig. 11 (Dan's plain findings, 28 Oct 21:20): figures/story/claims_scorecard.csv, written here from
    scorecard_v6_rows, drawn as the README's findings list: FINDINGS' twelve sentences in Dan's order under their three
    margin headers, one column per model (9B, 27B, Muse), a symbol per cell, 'a' as a small superscript, no id column
    and no words in the cells; the supplement version (figures/supp/s11_scorecard_all) adds Fig. 12's two rows.
    figures/story/scorecard.csv keeps v5's rows (scorecard_rows; rows of other models already in the file are kept):
    the joint figures and the shared grid (scripts/joint_figures.py, scripts/shared_grid.py) read its v5 claim names."""
    v5_rows = scorecard_rows()
    S.OUT.mkdir(parents=True, exist_ok=True)
    path = S.OUT / "scorecard.csv"
    ours = {name for _, _, name in S.MODELS}
    kept = []
    if path.exists():
        with path.open() as f:
            kept = [r for r in csv.DictReader(f) if r["model"] not in ours]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(SC_FIELDS))
        w.writeheader()
        w.writerows([{k: r[k] for k in SC_FIELDS} for r in v5_rows] + kept)
    rows = scorecard_v6_rows(v5_rows)
    with (S.OUT / "claims_scorecard.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(SC6_FIELDS))
        w.writeheader()
        w.writerows([{k: r[k] for k in SC6_FIELDS} for r in rows])
    for r in rows:
        key = r["data.csv key"]
        src = ("after the data" if r["flag"] == "a" else "fixed") + (f"; {key}" if key else "")
        main = r["group"] != FIG11_SUPP_GROUP
        S.record("fig11" if main else "s11", r["target"], f"{r['id']} {r['claim']}", r["cell"], source=src)
    main = [r for r in rows if r["group"] != FIG11_SUPP_GROUP]
    # Dan 21:20: the main version's cells are held / in part / failed / not run only
    assert all(r["cell"] in ("ok", "~", "x", "-") for r in main), [r for r in main if r["cell"] == "pending"]
    draw_findings(plt, main, "fig11_scorecard")
    draw_findings(plt, rows, "s11_scorecard_all", supp=True)


# Fig. 11's layout in inches (Dan's plain findings, 21:20): the margin headers, the sentences, the model columns
F11_HEAD_X, F11_TEXT_X, F11_CELL_X = 0.12, 1.74, (7.3, 7.85, 8.4)
F11_WRAP = 62  # sentence characters per line at 11 pt between F11_TEXT_X and the first model column
F11_CAPTION_WRAP = 112  # caption characters per line at 10 pt
F11_LINE, F11_ROW, F11_GROUP_GAP = 0.21, 0.31, 0.16  # inches: a wrapped line, a one-line row, the gap between groups
F11_HEAD_WRAP = {"Two readers, one word": "Two readers,\none word", "What the lookup reads": "What the\nlookup reads",
                 "Where and when the link is made": "Where and when\nthe link is made",
                 FIG11_SUPP_GROUP: "On Zach's\npassages\n(Fig. 12)"}  # fmt: skip


def draw_findings(plt, rows: list[dict], name: str, supp: bool = False) -> None:
    """Fig. 11's drawing: per finding (rows' id order) its sentence, wrapped, and a symbol per model; its group's
    header once in the left margin with a thin bracket over the group's rows; light shading on every other row; Dan's
    caption under it (the supplement adds a line on Fig. 12's rows)."""
    models = [next(n for _, mm, n in S.MODELS if mm == m) for m in SC6_MODELS]
    by = {(r["id"], r["model"]): r for r in rows}
    found = list(dict.fromkeys((r["id"], r["group"], r["claim"]) for r in rows))
    layout, y, last = [], 0.0, None  # (id, group, lines, top y, bottom y) in inches below the column heads
    for cid, group, claim in found:
        if last is not None and group != last:
            y += F11_GROUP_GAP
        lines = textwrap.wrap(claim, F11_WRAP)
        height = F11_ROW + F11_LINE * (len(lines) - 1)
        layout.append((cid, group, lines, y, y + height))
        y, last = y + height, group
    # Dan's caption, with "fixed before" for his "written before" (the figures' lint retires "write" and its forms)
    caption = ["By the rule fixed before each run; a: the order split was fixed after the data. The 27B's row 12 "
               "is from a reduced layer grid."]  # fmt: skip
    if supp:
        caption.append("The last two rows (Fig. 12; there a: read after the data) stay off the main page until the "
                       "reruns on Zach's P items land.")  # fmt: skip
    caption = [w for ln in caption for w in textwrap.wrap(ln, F11_CAPTION_WRAP)]
    top_in, heads_in, bottom_in = 0.95, 0.35, 0.35 + 0.19 * len(caption)
    h = top_in + heads_in + y + bottom_in
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, "Twelve findings on three models", "✓ held  ·  ~ in part  ·  ✗ failed  ·  – not run")
    ax = fig.add_axes((0.0, bottom_in / h, 1.0, (heads_in + y) / h))
    ax.set_xlim(0, S.WIDTH)
    ax.set_ylim(y, -heads_in)  # y in inches, down the page
    ax.axis("off")
    for x, model in zip(F11_CELL_X, models, strict=True):
        ax.text(x, -0.08, SHORT[next(m for _, m, n in S.MODELS if n == model)], ha="center", va="bottom",
                weight="bold", fontsize=S.FONT)  # fmt: skip
    for k, (cid, _group, lines, y0, y1) in enumerate(layout):
        if k % 2 == 0:
            ax.add_patch(plt.Rectangle((F11_TEXT_X - 0.08, y0), S.WIDTH - 0.06 - F11_TEXT_X + 0.08, y1 - y0,
                                       color="#f6f6f6", lw=0, zorder=0))  # fmt: skip
        ax.text(F11_TEXT_X, (y0 + y1) / 2, "\n".join(lines), ha="left", va="center", fontsize=S.FONT,
                linespacing=1.15)  # fmt: skip
        for x, model in zip(F11_CELL_X, models, strict=True):
            r = by[(cid, model)]
            sym, col = SC6_SYMBOL[r["cell"]]
            ax.text(x, (y0 + y1) / 2, sym, ha="center", va="center", fontsize=S.FONT + 3, color=col, weight="bold")
            if r["flag"] == "a":  # Dan: "a" only as a small superscript, explained once in the caption
                ax.text(x + 0.12, (y0 + y1) / 2 - 0.07, "a", ha="left", va="center", fontsize=S.FONT - 2,
                        color=S.COL["muted"])  # fmt: skip
            else:
                assert r["flag"] in ("", "degree"), r  # no other flag; "degree" is said in the supplement's label
    for group in dict.fromkeys(g for _, g, *_ in layout):
        ys = [(y0, y1) for _, g, _, y0, y1 in layout if g == group]
        top, bot = ys[0][0] + 0.04, ys[-1][1] - 0.04
        ax.text(F11_HEAD_X, top + 0.02, F11_HEAD_WRAP[group], ha="left", va="top", fontsize=S.FONT - 0.5,
                weight="bold", color="#444444", linespacing=1.1)  # fmt: skip
        ax.plot([F11_TEXT_X - 0.16] * 2, [top, bot], color="#9a9a9a", lw=1.0)
    fig.text(0.01, 0.1 / h, "\n".join(caption), ha="left", va="bottom", fontsize=S.FONT - 1, color=S.COL["muted"],
             linespacing=1.3)  # fmt: skip
    S.save(fig, name, supp=supp)


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
    """Fig. 7b (E8, v6): 47.0's swap through the lens against random draws, beside 47.10's report on the 27B (its
    numbers recorded under e8_report, the README's keys)."""
    from scripts import story_b50b as B50B

    # Dan's 18:30 brief: two panels with the identity change as the positive control; his 21:00 brief: one row per
    # model, the rank as a score in units of the random band, the 27B's report as one caption sentence
    B50B.build_verbal(VERBAL_SUMMARY, latest_verdict("x47_report/x47_10-*"), "fig07b_verbal")


def s07b_lens_readout(plt) -> None:
    """Supplementary to Fig. 7b: 47.0's three measures (rank, share rebuilt, KL) on the three models."""
    from scripts import story_b47b as B47

    B47.build_47_0(VERBAL_SUMMARY, "s07b_lens_readout", out_dir=S.SUPP)


def latest_verdict(pattern: str) -> Path:
    """The newest verdict folder under results/ matching pattern (each verdict run writes a new folder)."""
    found = sorted((S.REPO / "results").glob(pattern))
    assert found, f"no verdict folder results/{pattern}"
    return found[-1]


ANATOMY_ORDER = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")  # v6: 9B, 27B, Muse (the 122B in supplements)
# 47.8's bars for its l_probe and l_P (scripts/x47_anatomy.py's L_PROBE_BAR, L_P_BAR), for the legend's words only:
# the marked layers are the verdict's rules
PROBE_BAR, POSITION_BAR = 0.80, 0.20
# Dan's figure fixes, round 3 (28 Oct 21:10): the three vertical marks, one line style each on every panel
ANATOMY_MARKS = (("address formed", "l_probe", "--"), ("address used", "l_P", "-"), ("L", "layer", ":"))


def ordinal(k: int) -> str:
    return f"{k}{'nd' if k % 10 == 2 and k % 100 != 12 else 'th'}"  # the grids' steps: 2nd, 4th, 8th


def grid_text(layers: list[int]) -> str:
    """A sampled layer grid in words: 'every 4th', or 'every 8th plus L30 and L34' (a regular grid at its largest step
    plus the layers off it)."""
    steps = sorted({b - a for a, b in itertools.pairwise(layers)})
    if len(steps) == 1:
        return f"every {ordinal(steps[0])}"
    s = steps[-1]
    extra = [la for la in layers if la % s]
    assert [la for la in layers if not la % s] == list(range(s, layers[-1] + 1, s)), layers
    return f"every {ordinal(s)} plus " + " and ".join(f"L{la}" for la in extra)


def f06b_anatomy(plt) -> None:
    """Fig. 6b (E12, and E5's second figure): 47.8 (fixed in advance), per tested model, the lookup's answers under the
    whole change at each sampled layer (identity / position stacked, the original answer empty, the value as a row of
    0s under the bars), each share's 95% interval; the recall's switches as a line with its band; the not-interpretable
    shading from the first layer where the lookup's whole change switches < S.NI_SWITCH to the model's last layer;
    three vertical marks: the layer where the locker probe first reaches 0.8 (rules l_probe: the address is formed),
    where position answers start (l_P: the address is used) and L. One panel per model, x = the layer itself (0 to
    the model's depth), so a reduced grid (the 27B's, 49.4) shows in the bars' spacing; one style for every model (Dan's
    round 3, 28 Oct 21:10). The full sweep (parts, probes) is the verdict folder's x47_anatomy.png. Lightning (batch
    52) the fourth panel from its own verdict (LT_ANATOMY), its marks hollow: bars outlined, the recall's open."""
    vdir = latest_verdict("x47_anatomy/x47_8-*")
    srcs = dict.fromkeys(ANATOMY_ORDER, str((vdir / "x47_8.json").relative_to(S.REPO)))
    tested = {
        m["target"]: m for m in json.loads((vdir / "x47_8.json").read_text())["models"] if m["status"] == "tested"
    }
    models = [tested[t] for t in ANATOMY_ORDER if t in tested]
    assert 0 < len(models) <= 3, f"v6 (Dan's 18:30 brief): 9B, 27B, Muse at most, got {list(tested)}"
    models += [
        m for m in json.loads(LT_ANATOMY.read_text())["models"] if m["status"] == "tested" and m["target"] == LT[0]
    ]
    srcs[LT[0]] = rel(LT_ANATOMY)
    # four models: two rows of two, so each panel keeps the three models' width
    nrows, ncols, row_in, gap_in = (2, 2, 2.5, 0.95) if len(models) == 4 else (1, len(models), 2.6, 0.0)
    # the bottom band: 1.45 in for the axis labels and the caption, 0.45 in more for the 122B's grey row (Dan 11:30:
    # the fifth model slot; 47.8 never ran on it)
    bottom_in = 1.9
    h = 1.95 + nrows * row_in + gap_in + bottom_in
    fig, axes = plt.subplots(nrows, ncols, figsize=(S.WIDTH, h), sharey=True, squeeze=False)
    fig.subplots_adjust(left=0.085, right=0.985, top=1 - 1.95 / h, bottom=bottom_in / h, wspace=0.10,
                        hspace=gap_in / row_in)  # fmt: skip
    S.title(fig, "The address forms early; identity route first, position route later",
            "Bars: lookup answers under the whole change at one layer; line: recall switches; whiskers, bands: 95%.")  # fmt: skip
    values: list[float] = []
    at_l: list[str] = []
    for ax, m in zip(axes.flat, models, strict=True):
        layers, target, rules, depth = m["layers"], m["target"], m["rules"], m["n_layers"]
        src, lt = srcs[target], target == LT[0]
        cells = [m["cells"][str(la)] for la in layers]
        name = next(lab for t, _, lab in (*S.MODELS, LT) if t == target)
        short = SHORT[
            next(k for t, k, _ in (*S.MODELS, LT) if t == target)
        ]  # full name in the first panel, short after
        x = np.array(layers, dtype=float)
        w = 0.85 * min(b - a for a, b in itertools.pairwise(layers))  # bar width: the grid's finest step
        ni = [c["lookup"]["switch"]["whole"][0] < S.NI_SWITCH - 1e-9 for c in cells]
        assert ni == [not c["lookup"]["interpretable"] for c in cells], f"{target}: the shading disagrees with 47.8"
        # shaded from the first layer under the bar to the model's last: every later sampled layer is under it too
        first = next((i for i, f in enumerate(ni) if f), None)
        assert first is None or all(ni[first:]), f"{target}: an interpretable layer after a shaded one"
        if first is not None:
            S.not_interpretable(ax, [(layers[first] - w / 2, depth)])
            S.record("fig06b", target, "first layer where the lookup's whole change switches < 0.3", layers[first],
                     source=src)  # fmt: skip
        bottom = np.zeros(len(layers))
        for rt in ("identity", "position"):
            sh = np.array([c["lookup"]["share"]["whole"][rt] for c in cells])
            fill = {"facecolor": "white", "edgecolor": S.COL[rt], "lw": 1.2} if lt else {"color": S.COL[rt]}
            ax.bar(x, sh[:, 0], bottom=bottom, width=w, zorder=2, **fill)
            off = (-0.22 if rt == "identity" else 0.22) * w
            ax.vlines(x + off, bottom + sh[:, 1], bottom + sh[:, 2], color="#1e1e1e", lw=0.9, zorder=3)
            bottom += sh[:, 0]
        # the original answer (and other): filled light grey (Dan, 21:35), the hatch drawn again over the shaded bars
        ax.bar(x, 1 - bottom, bottom=bottom, width=w, zorder=2, **(S.ORIGINAL | {"facecolor": "white"} if lt
                                                                  else S.ORIGINAL))  # fmt: skip
        if first is not None:
            S.hatch_over(ax, [(layers[first] - w / 2, depth)])
        for la, c in zip(layers, cells, strict=True):
            for rt in ("identity", "position", "value", "original"):
                S.record("fig06b", target, f"layer {la}: lookup {rt} share (whole change)", *c["lookup"]["share"]["whole"][rt],
                         n=c["lookup"]["n"], source=src)  # fmt: skip
        values += [c["lookup"]["share"]["whole"]["value"][0] for c in cells]  # recorded above; shown in the legend
        rc = np.array([c["recall"]["switch"]["whole"] for c in cells])
        ax.fill_between(x, rc[:, 1], rc[:, 2], color=S.COL["recall"], alpha=0.18, lw=0, zorder=4)
        ax.plot(x, rc[:, 0], color=S.COL["recall"], marker="D", ms=4.5, lw=1.8, zorder=5,
                **({"mfc": "white", "mew": 1.2} if lt else {}))  # fmt: skip
        # Dan (21:50): every panel names its line and its first bar: "recall" right of the line where it falls through
        # one half, "identity route" inside the first (all-identity) bar
        k = next((i for i, v in enumerate(rc[:, 0]) if v < 0.8), len(layers) - 1)
        ax.text(x[k] + 0.6 * w, 0.8, "recall", ha="left", va="center", fontsize=S.LABEL_PT, color=S.COL["recall"],
                zorder=7, bbox={"boxstyle": "square,pad=0.1", "fc": "white", "ec": "none"})  # fmt: skip
        # the identity label in the first all-identity bar clear of the vertical marks
        marks = [v for v in (m["layer"], rules["l_probe"], rules["l_P"]) if v is not None]
        j = next((i for i, c in enumerate(cells) if c["lookup"]["share"]["whole"]["identity"][0] >= 0.9
                  and all(abs(x[i] - v) > w for v in marks)), 0)  # fmt: skip
        ax.text(x[j], 0.5, "identity route", ha="center", va="center", rotation=90, fontsize=S.LABEL_PT,
                color=S.COL["identity"] if lt else "white", zorder=7)  # fmt: skip
        for la, c in zip(layers, cells, strict=True):
            S.record("fig06b", target, f"layer {la}: recall switch (whole change)", *c["recall"]["switch"]["whole"],
                     n=c["recall"]["n"], source=src)  # fmt: skip
        # probe before use: the address readable (locker probe >= 0.8, rules' l_probe; dashed), position answers
        # beginning (l_P; solid) and L (dotted), named by the legend (three panels leave no room for labels above
        # each); L also under the layer axis, where it shares a layer with another mark
        for key, field, ls in ANATOMY_MARKS:
            la = m[field] if field == "layer" else rules[field]
            if key != "L":
                S.record("fig06b", target, f"{key}: layer", la, source=src)
            if la is not None:
                ax.axvline(la, color="#1e1e1e", ls=ls, lw=1.3, zorder=6)
        if rules["l_P"] == m["layer"]:
            at_l.append(short)
        ax.text(m["layer"], -0.13, "▲\nL", transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=S.FONT - 1, weight="bold", color="#1e1e1e", linespacing=0.9)  # fmt: skip
        ax.set_xticks([round(depth * k / 4) for k in range(5)])
        ax.set_xlim(0, depth)
        ax.set_xlabel("layer", loc="right", labelpad=6)
        ax.text(0, 1.03, name if ax is axes[0, 0] else short, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=12, weight="bold")  # fmt: skip
        # n per layer (the caption says so), above the frame beside the model's name: inside, its white patch would
        # cover the tops of the bars
        S.panel_tag(ax, str(cells[0]["lookup"]["n"]), "after" if lt else "fixed")
        ax.set_ylim(0, 1.0)
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[:, 0]:
        ax.set_ylabel("share of lookups / recalls")
    top = max(values, default=0.0)
    hs = [plt.Rectangle((0, 0), 1, 1, color=S.COL["identity"]), plt.Rectangle((0, 0), 1, 1, color=S.COL["position"]),
          plt.Rectangle((0, 0), 1, 1, **S.ORIGINAL),
          plt.Line2D([], [], color=S.COL["recall"], marker="D", ms=4.5, lw=1.8),
          *(plt.Line2D([], [], color="#1e1e1e", ls=ls, lw=1.3) for _, _, ls in ANATOMY_MARKS),
          plt.Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["value"], lw=1.3)]  # fmt: skip
    legend(fig, hs, ["identity route", "position route", "the original answer", "recall switches",
                     f"address readable (probe ≥ {PROBE_BAR:.1f})",
                     f"position answers begin (≥ {POSITION_BAR:.1f})", "L, the layer fixed in advance",
                     "value: 0.00 at every layer" if top < 0.005 else f"value: at most {top:.2f}"], 1 - 0.58 / h,
           ncol=3)  # fmt: skip
    # Dan (21:55): one caption line, where two marks coincide; the sampled grid shows in the bars' spacing
    if at_l:
        fig.text(0.01, 0.35 / h, f"{' and '.join(at_l)}: position answers begin at L (the two marks coincide).",
                 ha="left", va="bottom", fontsize=S.FONT - 1, color="#555555")  # fmt: skip
    fig.text(0.01, 0.1 / h, LT_NOTE, ha="left", va="bottom", fontsize=S.FONT - 1, color="#555555")
    # the 122B's slot: one grey row under the panels, as Fig. 1d's
    fig.text(0.01, 0.85 / h, B122[2], ha="left", va="center", fontsize=12, weight="bold")
    fig.text(0.5, 0.85 / h, "not run", ha="center", va="center", color=S.COL["muted"])
    S.save(fig, "fig06b_anatomy")


# Batch 47/48 figures (28 Oct, after Dan's answers at fca83082): name -> (module, builder, verdict folder, title).
# A title is set where the builder's default, built from the verdict's labels, reads stronger than the data.
BATCH47 = {
    "fig01c_zeroing": ("story_b47a", "build_zero", "x47_zero/x47_5-*",
                       "Taking the J++ part out of the changed prompt's state leaves the recall's answers in place"),
    "fig03d_depth_map": ("story_b47b", "build_e11", "x47_depthmap/depth-*", None),
    "fig05b_identity_outside": ("story_b47a", "build_identity", "x47_atoms/x47_1-*", None),  # the main test's parts
    "fig05d_routes_lens": ("story_b47a", "build_routes_lens", "x47_atoms/x47_1-*", None),  # E3 (Dan ~20:30)
    "fig05c_described_bridge": ("story_b47a", "build_cue", "x47_cue/x47_3-*",
                                "A described bridge: the split holds on two of the three models"),
    # pinned: Lightning's 47.13 coverage verdict (x47_13-20261029T035254Z, one model) is newer and would replace the
    # three models' panels
    "fig07c_probe_errors": ("story_b47a", "build_errors", "x47_errors/x47_13-20261028T113107Z", None),
    "fig09b_six_lockers": ("story_b47a", "build_six", "x47_six/x47_2-*", None),
    "fig09c_formation": ("story_b47b", "build_47_6", "x47_edges/x47_6-*",
                         "Blocking the pick sentence from the lockers removes most switches, not only position"),
    # pinned: the 27B's D4 run (persistence-20261029T013614Z, one model) is newer and would drop the 9B and Muse panels
    "fig06c_address_depth": ("story_b47c", "build_depth", "x47_depth_cpu/persistence-20261028T115530Z",
                             "The address is re-encoded early in depth and settles in later layers"),
    "fig09d_chain": ("story_b47c", "build_chain", "x47_chain/x47_14-*", None),
    "fig10b_enrichment": ("story_b48", "build_enrichment", "x48_enrich/x48_2-*",
                         "Without the J++ part the attribute moves only half way; late MLPs are not needed"),
    "fig10c_binding": ("story_b48", "build_binding", "x48_bind/x48_bind-*", None),
    "fig10d_heads": ("story_b48", "build_heads", "x48_heads/x48_heads-*", None),
    "fig10e_second_route": ("story_b48", "build_second_route", "x48_route2/x48_route2-*", None),
}  # fmt: skip
# Lightning's panel (batch 52): its coverage verdict by path, beside the pattern's newest three-model verdict
BATCH47_LIGHTNING = {"fig09b_six_lockers": {"lightning": LT_SIX, "lightning_note": LT_NOTE}}
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
        kw |= BATCH47_LIGHTNING.get(name, {})
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
    on the 27B), recorded for data.csv with the verdict json as source (47.10's: Fig. 7b records them, as e8_report)."""
    v = latest_verdict("x47_distance/x47_16-*") / "x47_16.json"
    m = next(x for x in json.loads(v.read_text())["models"] if x["status"] == "tested")
    src = str(v.relative_to(S.REPO))
    for k in ("0", "5", "20", "50"):
        S.record(
            "e6_distance",
            m["target"],
            f"47.16: position share with {k} neutral sentences",
            m["position"][k],
            source=src,
        )
        S.record("e6_distance", m["target"], f"47.16: slot probe with {k} neutral sentences", m["probe"][k], source=src)
        S.record("e6_distance", m["target"], f"47.16: the swap (fit with none) sends lookups to the target, {k} sentences",
                 m["swap_target"][k], source=src)  # fmt: skip
        if k in m["betas"]:
            S.record("e6_distance", m["target"], f"47.16: the code's shift beta with {k} sentences", *m["betas"][k]["beta"],
                     source=src)  # fmt: skip
    # 47.1 and 47.4: the first verdicts, then batch 52's coverage folders (Lightning; the 27B's 47.4), by explicit path
    for v in (latest_verdict("x47_atoms/x47_1-*") / "x47_1.json",
              pins.RESULTS_DIR / "x47_atoms" / "x52_atoms47-20261029T011717Z" / "x47_1.json"):  # fmt: skip
        src = str(v.relative_to(S.REPO))
        for m in json.loads(v.read_text())["models"]:
            for part in ("1-25", "26-100", "1-100"):
                if part in m.get("routes", {}).get("falls", {}):
                    S.record("e3_identity", m["target"], f"47.1: identity answers lost beyond random without lens directions {part}",
                             *m["routes"]["falls"][part]["identity"], source=src)  # fmt: skip
    for v in (latest_verdict("x47_cumulative/x47_4-*") / "x47_4.json",
              pins.RESULTS_DIR / "x47_cumulative" / "x52_cumulative-20261029T044453Z" / "x47_4.json"):  # fmt: skip
        src = str(v.relative_to(S.REPO))
        for m in json.loads(v.read_text())["models"]:
            for design, cells in m.get("cells", {}).items():
                after = cells.get("lookup", {}).get("locker-after")
                if after and after.get("n"):
                    S.record("e11_before_l", m["target"], f"47.4: {design}, locker after the pick: lookups carried by the bridge word "
                             "before L", *after["terms"]["before_L"], n=after["n"], source=src)  # fmt: skip
    v = latest_verdict("x47_value/x47_7a-*") / "x47_7a.json"
    m = next(x for x in json.loads(v.read_text())["models"] if x["status"] == "tested")
    src = str(v.relative_to(S.REPO))
    for r, name in (("ql", "question last"), ("qf", "question first")):
        S.record("e14_question_first", m["target"], f"47.7(a): value probe at the bridge word, {name}", *m["probe"][r]["probe"],
                 source=src)  # fmt: skip


# the runs behind the README's data catalogue (Dan's restructure brief, 28 Oct 22:20), 9B / 27B / Muse, and Lightning
# (batch 52; no clean one-pick run passed its gate)
CATALOGUE_RUNS = {
    "clean one-pick": ("x0_necessity", {"qwen3.5-9b": "qwen35_9b_x45m_fresh", "qwen3.6-27b": "x45m_fresh_27b",
                                        "muse-glimmer-30b": "muse30b_x45m_fresh"}, ""),
    "routes":("x6_routes", {"qwen3.5-9b": "qwen35_9b_x6_routes", "qwen3.6-27b": "x6_routes_27b",
                             "muse-glimmer-30b": "muse30b_x6_routes", "nemotron-3.5-lightning": "nem35l_x52_routes",
                             "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_g75"}, "C2"),  # the 122B: gate lowered after the data
    "six-locker": ("x47_six", {"qwen3.5-9b": "qwen35_9b_x47_2", "muse-glimmer-30b": "muse30_x47_2",
                               "nemotron-3.5-lightning": "nem35l_x52_six"}, "M6"),
}  # fmt: skip


def card_numbers() -> None:
    """Numbers the README's data catalogue and Part I cards quote that no figure records (Dan's README restructure
    brief, 28 Oct 22:20), each from its run files: the scenes each prompt set used per model; the conflict test's
    answer-direction control (the recall rows of 51.12's opened verdict); the rule labels of the dose curves and the
    removal ladder. Run after the figures: the varied and natural counts are Fig. 9a's own n (S.ROWS)."""
    for name, (exp, runs, prefix) in CATALOGUE_RUNS.items():
        for target, run in runs.items():
            path = pins.RESULTS_DIR / exp / run / "outcomes.jsonl"
            scenes = {r["scene"] for r in X.read_jsonl(path) if r["scene"].startswith(prefix)}
            S.record("catalogue", target, f"{name} scenes: scenes used", len(scenes), source=rel(path))
    for target, (_, (nat_ptr, nat)) in TRANSFER_RUNS.items():  # the 122B too (Dan 11:30: the fifth model)
        base = pins.RESULTS_DIR / "x5_natural"
        run = next(r for r in (nat_ptr, nat) if (base / r / "outcomes.jsonl").exists())  # transfer_cells' choice
        gate = json.loads((base / run / "gate.json").read_text())
        S.record("catalogue", target, "natural passages: scenes eligible", gate["eligible"],
                 source=rel(base / run / "gate.json"))  # fmt: skip
    fig09a = {(r["model"], r["quantity"]): r for r in S.ROWS if r["figure"] == "fig09a"}
    for target, _, _ in (*CARD_MODELS, LT):
        rows = [fig09a[(target, f"recall extra loss without the J++ part: {f}")] for f in ("prose", "json", "table")]
        S.record("catalogue", target, "varied scenes: scenes used (prose, JSON and table)", sum(r["n"] for r in rows),
                 source=rows[0]["source"])  # fmt: skip
        r = fig09a.get((target, "recall extra loss without the J++ part: natural"))  # Lightning: below gate, not drawn
        if r:
            S.record("catalogue", target, "natural passages: scenes used (fact first)", r["n"], source=r["source"])
    for z, what in (("z1", "named bridge"), ("z2", "described bridge")):
        v = latest_verdict(f"x50_zach/{z}-*") / f"{z}.json"
        for m in json.loads(v.read_text())["models"]:
            S.record("catalogue", m["target"], f"Zach's passages, {what}: passages used", m["gate"]["chosen"],
                     source=rel(v))  # fmt: skip
    for m in json.loads(LT_Z1.read_text())["models"]:
        S.record("catalogue", m["target"], "Zach's passages, named bridge: passages used", m["gate"]["chosen"],
                 source=rel(LT_Z1))  # fmt: skip
    v = pins.RESULTS_DIR / "x5_natural" / "nem35l_x52_natural_below" / "gate.json"
    S.record("catalogue", LT[0], "natural passages: scenes eligible (below gate)", json.loads(v.read_text())["eligible"],
             source=rel(v))  # fmt: skip
    v = LT_CONFLICT
    S.record("catalogue", LT[0], "main test: scenes used", next(c["n"] for c in json.loads(v.read_text())["cells"]
             if c["layer"] == LT_L and c["reader"] == "PM"), source=rel(v))  # fmt: skip
    # the answer control: 51.12's opened verdict (9B / 27B / Muse) and Lightning's coverage run (x52_answer, set e1)
    lt_answer = pins.RESULTS_DIR / "x51_answer" / "x52_answer-20261029T002056Z" / "verdict.json"
    # the 122B's coverage run (Dan 11:30, item 3), read for the 122B only (the same folder repeats Lightning's e1)
    q122_answer = pins.RESULTS_DIR / "x51_answer" / "x52_answer-20261029T112359Z" / "verdict.json"
    for v, only in ((latest_verdict("x51_answer/x51_12-*") / "verdict.json", None), (lt_answer, None),
                    (q122_answer, "qwen3.5-122b-a10b")):  # fmt: skip
        for m in json.loads(v.read_text())["models"]:
            if m["set"] != "e1" or (only and m["target"] != only):
                continue
            rc = m["readers"]["recall"]
            S.record("conflict_answer", m["target"], "main test, recall: share of its loss kept when the lens part keeps "
                     "the answer words' directions", *rc["share2"], n=rc["n"], source=rel(v))  # fmt: skip
            S.record("conflict_answer", m["target"], "main test, recall: switches lost beyond random without the answer "
                     "words' directions only", *rc["extra"]["3"], n=rc["n"], source=rel(v))  # fmt: skip
            S.record("conflict_answer", m["target"], "main test, recall: items whose answer word ranks below the lens's "
                     "top 50 at the bridge word", *rc["check"]["not_read"], n=rc["n"], source=rel(v))  # fmt: skip
            S.record("conflict_answer", m["target"], "main test, recall: the rule's label (page words)",
                     ANSWER_LABEL[rc["key"]], source=rel(v))  # fmt: skip
    v = latest_verdict("x51_answer/x51_12-*") / "verdict.json"
    # Part VI (Dan 29 Oct ~01:00): the described bridge on Zach's passages withdrawn, and the locker scenes' answer check
    for m in json.loads(v.read_text())["models"]:
        for w, r in m["readers"].items() if m["set"] in ("z2", "cue") else ():
            fig, what = (
                ("withdrawn_z2", "Zach's described passages")
                if m["set"] == "z2"
                else ("cue_answer", "the described bridge in locker scenes")
            )
            ch = r.get("check", {})
            S.record(fig, m["target"], f"{what}, {w}: the answer word's median lens rank at the changed token (original prompt), rounded",
                     int(ch["median_rank_O"] + 0.5), n=r["n"], source=rel(v))  # fmt: skip
            S.record(fig, m["target"], f"{what}, {w}: the bridge entity's median lens rank at the changed token (original prompt), rounded",
                     int(ch["median_bridge_rank_O"] + 0.5), n=r["n"], source=rel(v))  # fmt: skip
            S.record(fig, m["target"], f"{what}, {w}: items whose answer word ranks below the lens's top 50 at the changed token",
                     *ch["not_read"], n=r["n"], source=rel(v))  # fmt: skip
            S.record(fig, m["target"], f"{what}, {w}: switches lost beyond a random part without the answer directions only",
                     *r["extra"]["3"], n=r["n"], source=rel(v))  # fmt: skip
            if r["extra"].get("3f"):
                S.record(fig, m["target"], f"{what}, {w}: switches lost beyond a frequency-matched part without the answer "
                         "directions only", *r["extra"]["3f"], n=r["n"], source=rel(v))  # fmt: skip
    for v in (latest_verdict("x51_dose/x51_1-*") / "verdict.json", LT_DOSE / "verdict.json"):
        for m in json.loads(v.read_text())["models"]:
            S.record("dose_rules", m["target"], "dose curves: main-test scenes, locker sentences first", m["n"],
                     source=rel(v))  # fmt: skip
            S.record("dose_rules", m["target"], "(i) the lookup is blind to the J++ part", m["rules"]["i"]["label"],
                     source=rel(v))  # fmt: skip
            S.record("dose_rules", m["target"], "(ii) the recall reads the J++ part above its share",
                     m["rules"]["ii"]["recall"]["label"], source=rel(v))  # fmt: skip
            S.record("dose_rules", m["target"], "(iii) together only", m["rules"]["iii"]["recall"]["label"],
                     source=rel(v))  # fmt: skip
    v = latest_verdict(LADDER_VERDICT) / "x49_2.json"
    for m in json.loads(v.read_text())["models"]:
        rules = m["rules"] or {}
        for key, what in (("second_copy", "the second copy is the earlier mention"),
                          ("only_everything", "needed only when everything goes"),
                          ("lookup", "the lookup never needs it")):  # fmt: skip
            label = ("yes" if rules[key] else "no") if key in rules else "not run (bridge-word steps only)"
            S.record("ladder_rules", m["target"], what, label, source=rel(v))


def ladder_agreement() -> None:
    """How we checked (flag 20): the largest difference between the ladder's first runs and the full reruns the README
    cites, per reader over every scene (point estimates), on the steps both ran at the same layers: Muse's step 6 moved
    into Zach's layer band in the rerun (r3), so it is recorded apart; each order's own largest difference beside."""
    first, full = (latest_verdict(p) / "x49_2.json" for p in (LADDER_FIRST, LADDER_VERDICT))
    old = {m["target"]: m for m in json.loads(first.read_text())["models"]}
    worst, worst_order, moved = 0.0, 0.0, 0.0
    for m in json.loads(full.read_text())["models"]:
        o = old.get(m["target"])
        for reader, groups in m["cells"].items():
            for group, cell in groups.items():
                ocell = ((o or {}).get("cells") or {}).get(reader, {}).get(group)
                if not ocell:
                    continue
                for r, cost in cell["cost"].items():
                    if r not in ocell["cost"]:
                        continue
                    d = abs(cost[0] - ocell["cost"][r][0])
                    if m["target"] == "muse-glimmer-30b" and r == "6":
                        moved = max(moved, d) if group == "all" else moved
                    elif group == "all":
                        worst = max(worst, d)
                    else:
                        worst_order = max(worst_order, d)
    src = f"{rel(first)}; {rel(full)}"
    S.record("cards", "", "the ladder: largest difference between the first runs and the full reruns, every scene, "
             "on the steps both ran at the same layers", round(worst, 4), source=src)  # fmt: skip
    S.record("cards", "", "the ladder: the same within one sentence order", round(worst_order, 4), source=src)
    S.record("cards", "muse-glimmer-30b", "the ladder: step 6's difference, every scene (moved into Zach's band)",
             round(moved, 4), source=src)  # fmt: skip


# Batch 52's coverage folders and the morning's CPU checks the README quotes (Dan's README brief, 29 Oct 08:55-09:35),
# each read by its explicit folder (a newest-folder pattern would pick another model's coverage run)
R = pins.RESULTS_DIR
X52 = {
    "zero": R / "x47_zero" / "x52_zero-20261029T032056Z" / "x47_5.json",
    "x0b": LT_X0B,
    "natural": R / "x5_natural" / "nem35l_x52_natural_below" / "verdict-20261029T082128Z" / "verdict.json",
    "atoms": (R / "x52_atoms" / "report-20261029T000125Z" / "tables.json",
              R / "x52_atoms" / "report-20261029T010648Z" / "tables.json"),
    "lenswrite": R / "x51_jread" / "x52_lenswrite-20261029T080535Z" / "lenswrite.json",
    "swaprecall": R / "x8_write" / "x52_swaprecall-20261029T080538Z" / "swaprecall.json",
    "x8_write": {"qwen3.5-9b": "qwen35_9b_x8_write/verdict-20261026T110254Z",
                 "qwen3.6-27b": "x8_write_27b/verdict-20261026T125548Z",
                 "muse-glimmer-30b": "muse30b_x8_write/verdict-20261026T141141Z",
                 "nemotron-3.5-lightning": "nem35l_x52_write/verdict-20261029T005021Z",
                 "qwen3.5-122b-a10b": "qwen35_122b_x8_write_g75/verdict-20261026T125705Z"},
    "z1": (R / "x50_zach" / "z1-20261028T161649Z" / "z1.json", LT_Z1),
    "z1p": (R / "x50_zach" / "x52_z1p-20261029T081112Z" / "z1p.json", R / "x50_zach" / "x52_z1p-20261029T081323Z" / "z1p.json",
            R / "x50_zach" / "x52_z1p-20261029T080731Z" / "z1p.json"),
    "carrier": (R / "x51_carrier" / "x51_7-20261028T171646Z" / "verdict.json",
                R / "x51_carrier" / "x52_carrier-20261029T014338Z" / "verdict.json"),
    "travel": (R / "x51_travel" / "x51_4-20261028T173333Z" / "verdict.json",
               R / "x51_travel" / "x52_travel-20261029T012517Z" / "verdict.json"),
    "z3": (R / "x50_zach" / "z3-20261028T163053Z" / "z3.json", R / "x50_zach" / "x52_z3-20261029T024151Z" / "z3.json",
           R / "x50_zach" / "x52_z3-20261029T013329Z" / "z3.json"),
    "persistence": (R / "x47_depth_cpu" / "persistence-20261029T013614Z" / "persistence.json",
                    R / "x47_depth_cpu" / "persistence-20261029T015607Z" / "persistence.json"),
    "anatomy": (R / "x47_anatomy" / "x47_8-20261028T154518Z" / "x47_8.json",
                R / "x47_anatomy" / "x52_anatomy-20261029T013405Z" / "x47_8.json", LT_ANATOMY),
    "six_27b": R / "x47_six" / "x52_six-20261029T004919Z" / "x47_2.json",
    "addr": R / "x51_addr" / "verdict-20261028T215138Z" / "verdict.json",
    "verbal": R / "x47_verbal" / "summary-20261029T005548Z" / "verbal.json",
    "errors": R / "x47_errors" / "x47_13-20261029T035254Z" / "x47_errors.json",
    "x45d": R / "x0b_generalize" / "nem35l_x52_x45d" / "x45d-20261029T035250Z" / "verdict.json",
}  # fmt: skip


def cards_numbers() -> None:
    """Numbers the README quotes from batch 52's coverage runs (Lightning; the 27B's full grids) and the morning's CPU
    checks, recorded as figure "cards" with each verdict file as source. Lightning's gate was chosen after its 60-scene
    pre-check was seen: the page marks its numbers hollow."""
    lt = LT[0]

    def rec(model: str, what: str, v, src: Path, n=None) -> None:
        vals = list(v) if isinstance(v, (list, tuple)) else [v]
        S.record("cards", model, what, *vals[:3], n=n, source=rel(src))

    # the 122B's L33 as a relative depth (Dan 11:55: "its later layer (L33, relative depth 0.69)"): its predicted layer
    # in the r2 verdict over the pinned number of layers
    p = R / "x0_necessity" / "qwen35_122b_x0_necessity_r2" / "verdict-20261024T171509Z" / "verdict.json"
    la, nl = json.loads(p.read_text())["verdict"]["predicted"], pins.TARGETS["qwen3.5-122b-a10b"]["n_layers"]
    S.record("cards", "qwen3.5-122b-a10b", "L as a relative depth (L / the number of layers)", round(la / nl, 4),
             source=f"{rel(p)} (predicted layer {la}); src/bridge_jspace/pins.py (n_layers {nl})")  # fmt: skip
    # the conflict test at Lightning's layer (rule copied from the 9B; layer fixed by amendment 1)
    v = json.loads(LT_CONFLICT.read_text())
    rec(lt, "L: the layer fixed in advance", v["verdict"]["predicted"], LT_CONFLICT)
    cells = {c["reader"]: c for c in v["cells"] if c["layer"] == LT_L and c["dict"] == "jpp"}
    rec(
        lt, "conflict: recall, switches lost beyond a random part", cells["PM"]["excess"], LT_CONFLICT, cells["PM"]["n"]
    )
    rec(lt, "conflict: recall, switches lost, not net of random", cells["PM"]["Jdep"], LT_CONFLICT, cells["PM"]["n"])
    rec(
        lt, "conflict: lookup, switches lost beyond a random part", cells["PP"]["excess"], LT_CONFLICT, cells["PP"]["n"]
    )
    rec(lt, "conflict: the rule", v["verdict"]["chat"]["verdict"], LT_CONFLICT)
    # other texts: the varied scenes (pooled) and the natural passages (below gate: descriptive)
    v = json.loads(LT_X0B.read_text())
    pp = next(c for c in v["cells"] if c["layer"] == LT_L and c["reader"] == "PP" and c["dict"] == "jpp"
              and c["k"] == 25 and c["omp"] == "signed")  # fmt: skip
    rec(lt, "varied: lookup, switches lost beyond a random part", pp["excess"], LT_X0B, pp["n"])
    rec(lt, "varied: the gap", v["contrast"][str(LT_L)], LT_X0B, pp["n"])
    rec(lt, "varied: the rule", v["verdict"], LT_X0B)
    p = X52["natural"]
    v = json.loads(p.read_text())
    rec(
        lt,
        "natural (below gate): recall, switches lost beyond a random part",
        v["main"]["excess"]["PM"],
        p,
        v["main"]["n"],
    )
    rec(
        lt,
        "natural (below gate): lookup, switches lost beyond a random part",
        v["main"]["excess"]["PP"],
        p,
        v["main"]["n"],
    )
    rec(lt, "natural (below gate): the gap", v["main"]["gap"], p, v["main"]["n"])
    rec(lt, "natural (below gate): the rule's reading", v["label"], p)
    # zeroing at one layer
    p = X52["zero"]
    m = json.loads(p.read_text())["models"][0]
    rc = m["readers"]["recall"]
    rec(
        m["target"],
        "47.5: recall's answers kept at L, the J++ part's 25 directions taken out",
        rc["kept"]["zero_L"],
        p,
        rc["n"],
    )
    rec(m["target"], "47.5: recall's answers lost beyond random (L)", rc["beyond_random"]["L"], p, rc["n"])
    rec(m["target"], "47.5: the rule's reading (recall at L)", m["labels"]["recall L"], p)
    # 52 A: what the lens part's 25 directions stand for (descriptive; the e1 set, the recall's view)
    for p in X52["atoms"]:
        d = json.loads(p.read_text())
        for target, sets in d["summary"].items():
            s = sets["e1"]["PM"]
            rec(target, "52 A: main-test scenes", s["n"], p)
            for cls, what in (("bridge", "the original bridge word"), ("new_bridge", "the new bridge word"),
                              ("answer_own", "the reader's answer word"), ("other", "no scene word")):  # fmt: skip
                rec(target, f"52 A: share of the rebuilt energy in {what}", s["energy"][cls], p, s["n"])
            atoms = [c for cls in ("bridge", "new_bridge") for c in s["bridge_by_match"].get(cls, {}).values()]
            signed = sum(c["atoms"] * c["sign_as_expected"] for c in atoms) / sum(c["atoms"] for c in atoms)
            rec(target, "52 A: the bridge words' directions whose sign points the expected way (old -, new +)",
                round(signed, 4), p)  # fmt: skip
            hand = d["hand"].get(f"{target} e1")
            if hand:
                rec(target, "52 A: hand-checked items (the lookup's view)", hand["items"], p)
                rec(target, "52 A: hand labels agreeing with the classifier", hand["rate"], p, hand["atoms"])
    # 51.10's writes at the last token: what the model outputs (descriptive)
    p = X52["lenswrite"]
    for target, m in json.loads(p.read_text())["models"].items():
        c = m["cells"]
        rec(target, "lenswrite: the recall keeps its clean answer under the lens swap", c["recall|swap"]["original"], p,
            c["recall|swap"]["n"])  # fmt: skip
        rec(target, "lenswrite: the J++ part at gain 2 gives the changed prompt's recall answer", c["recall|jpp2"]["new"],
            p, c["recall|jpp2"]["n"])  # fmt: skip
        rec(target, "lenswrite: a random part at gain 2 gives the changed prompt's recall answer", c["recall|rand2"]["new"],
            p, c["recall|rand2"]["n"])  # fmt: skip
        rec(target, "lenswrite: the most outputs naming the entity or a number word, over every arm",
            max(x[k] for x in c.values() for k in ("entity", "number_word")), p)  # fmt: skip
    # 51.10: the rule's reading at the appended last token (P3), per reader; the 9B / 27B / Muse verdict and Lightning's
    for p in (latest_verdict(JREAD_VERDICT) / "verdict.json", LT_JREAD / "verdict.json"):
        v = json.loads(p.read_text())
        for m in v["models"]:
            for w in ("recall", "lookup"):
                rec(
                    m["target"],
                    f"51.10: {w} at the last token: the rule's reading",
                    v["labels"][m["target"]][w]["P3"],
                    p,
                )
            rec(m["target"], "51.10: main-test scenes, locker first", m["n"], p)
    # the address swap at s = 2: recalls that change, and of those, the swapped-in item's answer
    for target, run in X52["x8_write"].items():
        p = R / "x8_write" / run / "verdict.json"
        cell = next(c for c in json.loads(p.read_text())["cells"] if c["kind"] == "write" and c["pair"] is None
                    and c["s"] == 2)  # fmt: skip
        rec(target, "the address swap at s = 2: recalls that change", cell["recall_changed"], p, cell["n"])
    p = X52["swaprecall"]
    for target, m in json.loads(p.read_text())["models"].items():
        ch = m["cells"]["write|2"]["of_changed"]
        rec(target, "the address swap at s = 2: changed recalls naming the swapped-in item's answer", ch["swapped_in"], p,
            ch["n"])  # fmt: skip
    # Zach's passages: Z1 (true facts) and Z1-P (made-up facts), at each model's L
    for p in (*X52["z1"], *X52["z1p"]):
        tag = "Z1-P" if p.name == "z1p.json" else "Z1"
        for m in json.loads(p.read_text())["models"]:
            r = m["layer_results"][str(m["layers"][0])]
            rec(m["target"], f"{tag}: lookup, switches lost beyond a random part", r["lookup"]["excess"], p, r["n"])
            rec(m["target"], f"{tag}: recall, switches lost beyond a random part", r["recall"]["excess"], p, r["n"])
            rec(m["target"], f"{tag}: the gap", r["gap"], p, r["n"])
            rec(m["target"], f"{tag}: the rule's reading", r["verdict"], p)
            if tag == "Z1-P":
                rec(m["target"], "Z1-P: the gate (the lookup's read accuracy on the original passages)",
                    round(m["gate"]["org_read_accuracy"]["K"], 3), p)  # fmt: skip
    # 51.7: fact-after lookups on the full carrier (the whole before-L)
    for p in X52["carrier"]:
        for m in json.loads(p.read_text())["models"]:
            lk = m["groups"]["fact-after"]["before"]["lookup"]
            rec(m["target"], "51.7: fact-after lookups, full carrier: switches lost beyond a random part", lk["excess"], p,
                lk["n"])  # fmt: skip
    # 51.4: does the address travel to the last token
    for p in X52["travel"]:
        for m in json.loads(p.read_text())["models"]:
            rec(m["target"], "51.4: the rule's reading", m["label"], p)
    # Z3: the routes test on Zach's passages, position share under the whole change at the first layer
    for p in X52["z3"]:
        for m in json.loads(p.read_text())["models"]:
            r = m["layer_results"][str(m["layers"][0])]
            rec(
                m["target"],
                "Z3: position share under the whole change",
                r["shares"]["C2"]["whole"]["position"],
                p,
                r["n"],
            )
    # D4 on the 27B and Lightning (the 9B's and Muse's: Fig. 6c)
    for p in X52["persistence"]:
        for target, m in json.loads(p.read_text())["models"].items():
            rec(
                target,
                "D4: the address's mean overlap over every pair of window layers",
                round(m["U"]["mean_cos2"], 4),
                p,
            )
    # 47.8's rules: the 9B, Muse and the 27B's reduced grid (first run); the 27B's full grid and Lightning (batch 52)
    for p in X52["anatomy"]:
        for m in json.loads(p.read_text())["models"]:
            if m["status"] != "tested":
                continue
            grid = (
                "" if m["target"] != "qwen3.6-27b" else (" (full grid)" if len(m["layers"]) > 10 else " (reduced grid)")
            )
            r = m["rules"]
            for key, what in (
                ("l_J", "the last layer the lookup needs the J++ part"),
                ("l_P", "the first layer of the position route"),
                ("l_probe", "the address readable from"),
            ):
                rec(m["target"], f"47.8{grid}: {what}", r[key], p)
            for key, what in (
                ("a", "(a) the handoff"),
                ("b", "(b) readable before it is used"),
                ("d", "(d) never the value"),
            ):
                rec(m["target"], f"47.8{grid}: {what}", "yes" if r[key]["holds"] else "no", p)
    # six lockers: the 27B's coverage run (not in Fig. 9b)
    p = X52["six_27b"]
    m = next(x for x in json.loads(p.read_text())["models"] if x["target"] == "qwen3.6-27b")
    rec(m["target"], "47.2: pairwise writes reaching 25% (dose 2)", m["rules"]["2"]["pairs_reaching"], p,
        m["rules"]["2"]["pairs"])  # fmt: skip
    # 51.11 on the 9B: the code's size and its shape
    p = X52["addr"]
    m = next(x for x in json.loads(p.read_text())["models"] if x["target"] == "qwen3.5-9b")
    rec(m["target"], "51.11 part 1: the code's size", m["part1"]["rule"]["text"], p)
    rec(m["target"], "51.11 part 3: the order", m["part3"]["rule"]["text"], p)
    rec(m["target"], "51.11 part 3: midpoint swaps reaching the slot between, from the first slot (dose 2)",
        m["part3"]["rule"]["mid"]["1"], p)  # fmt: skip
    rec(m["target"], "51.11 part 3: full swaps reaching their target (dose 2)", m["part3"]["rule"]["full_far"], p)
    # Lightning's 45p below gate (exploratory; descriptive only, no rule label on the page)
    m = next(x for x in json.loads(LT_45P.read_text())["models"] if x["target"] == lt)
    rc = m["readers"]["recall"]
    for k, what in (("2-3", "(2) minus (3)"), ("2-4", "(2) minus (4)")):
        rec(lt, f"45p (below gate): recall, loss in {what}", rc["diff"][k], LT_45P, rc["n"])
    # Lightning: the lens and the address (47.0), the lookup's errors (47.13), the refit address (45d)
    p = X52["verbal"]
    b = json.loads(p.read_text())["models"][lt]["b"]["all|25"]
    rec(lt, "47.0 (b) share rebuilt by 25 lens directions: pointer", b["pointer"], p)
    rec(lt, "47.0 (b) share rebuilt by 25 lens directions: random draws (mean)", b["random_mean"], p)
    p = X52["errors"]
    m = json.loads(p.read_text())["models"][0]
    rec(m["target"], "47.13: wrong answers whose locker the address probe predicts", m["rates"]["match"]["probe"], p,
        m["rates"]["n"])  # fmt: skip
    p = X52["x45d"]
    v = json.loads(p.read_text())
    for fmt, cell in v["lookup_refit"].items():
        rec(lt, f"45d: the refit address, lookup switches lost beyond random: {fmt}", cell, p)


CARD_MODELS = tuple(m for m in S.MODELS if m[1] != "122b")  # 9B, 27B, Muse
# 51.12's verdict keys in the page's words (the verdict's own label stays in verdict.json)
ANSWER_LABEL = {"entity": "the item", "answer": "the answer", "mixed": "mixed", "na": "can't tell",
                "not_read": "the answer word is not read"}  # fmt: skip


def f15_mechanisms(plt) -> None:
    """Fig. 15 (E15, v6): the five failed mechanism tests in one panel, from their newest verdicts."""
    from scripts import story_b48 as B48

    B48.build_mechanisms({"48.2": latest_verdict("x48_enrich/x48_2-*"), "48.3": latest_verdict("x48_bind/x48_bind-*"),
                          "48.4": latest_verdict("x48_heads/x48_heads-*"),
                          "48.5": latest_verdict("x48_route2/x48_route2-*"),
                          "47.6": latest_verdict("x47_edges/x47_6-*")}, "fig15_mechanisms")  # fmt: skip


def f_batch47(plt) -> None:
    batch47_figures(plt)


# Dan's figures brief (28 Oct ~18:30): the mark legend, the removal ladder (E2, replacing fig01c) and the 2 x 2. The
# ladder: the full reruns for every step (Dan's flag-20 decision, 29 Oct 09:05): the 9B's run, the 27B's x52_ladder_27b_a
# and Muse's r3 (muse30_x52_ladder) in one verdict, so no column mixes runs
LADDER_VERDICT = "x49_ladder/x52_ladder-20261029T012701Z"
LADDER_FIRST = (
    "x49_ladder/x49_2-20261028T161612Z"  # the first runs (the 27B: bridge-word steps only), for the agreement
)
Z1_VERDICT = "x50_zach/z1-*"


def f00b_marks(plt) -> None:
    from scripts import story_b50 as B50

    B50.build_marks("fig00b_marks")


def f01d_ladder(plt) -> None:
    from scripts import story_b50 as B50

    B50.build_ladder(latest_verdict(LADDER_VERDICT), "fig01d_ladder", lightning=True)


def f09a_transfer(plt) -> None:
    from scripts import story_b50b as B50B

    B50B.build_transfer("fig09a_transfer")


def f09b_refit(plt) -> None:
    from scripts import story_b50b as B50B

    B50B.build_refit("fig09b_refit")


def f13_attention(plt) -> None:
    from scripts import story_b50b as B50B

    B50B.build_attention(latest_verdict("x49_attn/x49_7-*"), "fig13_attention")


def f14_learned(plt) -> None:
    from scripts import story_b51 as B51

    # Dan's rethink (28 Oct ~21:45): 51.3's opened verdict on all three models (more pairs than 48.1 / 49.8's 9B runs)
    B51.build_learned(latest_verdict("x51_das/verdict-*"), "fig14_learned")


def f12_two_by_two(plt) -> None:
    from scripts import story_b50 as B50

    B50.build_two_by_two(latest_verdict(LADDER_VERDICT), latest_verdict(Z1_VERDICT), "fig12_two_by_two", lightning=True)


def s_batch47(plt) -> None:
    batch47_figures(plt, BATCH47_SUPP, supp=True)


def f16_dose(plt) -> None:
    from scripts import story_b51 as B51

    B51.build_dose(latest_verdict("x51_dose/x51_1-*"), "fig16_dose", LT_DOSE, LT_NOTE)


def s14_learned_sizes(plt) -> None:
    from scripts import story_b51 as B51

    B51.build_sizes(latest_verdict("x51_das/verdict-*"), "s14_learned_sizes")


# Dan's 51.10 brief (28 Oct ~22:35): the opened verdict (x51_jread/x51_10-<UTC>) and its runs' read folders
JREAD_VERDICT = "x51_jread/x51_10-*"


def f17_jspace_last_token(plt) -> None:
    from scripts import story_b51b as B51B

    B51B.build_last_token(latest_verdict(JREAD_VERDICT), "fig17_jspace_last_token", LT_JREAD,
                          "Lightning: read bars hatched, swap bars dashed: its gate chosen after the 60-scene pre-check "
                          "was seen.")  # fmt: skip


def f18_atoms(plt) -> None:
    from scripts import story_b52 as B52

    B52.build_atoms(tuple(p.parent for p in X52["atoms"]), "fig18_atoms")


def s17_jspace_grids(plt) -> None:
    from scripts import story_b51b as B51B

    B51B.build_grids(latest_verdict(JREAD_VERDICT), "s17_jspace_grid")


# v6: Fig. 4's schematic is Fig. 5's left panel; the full-width one is the supplement s04_routes_design
README_FIGS = (f00_setup, f01_split, f01b_settings, f02_specificity, f02b_k, f03_order, f03b, f03c, f05_routes,
               f06_depth, f06b_anatomy, f07_writes, f07b_verbal, f08_first_locker, f09_transfer, f10_left, f11_scorecard,
               f_batch47, f15_mechanisms, f00b_marks, f01d_ladder, f12_two_by_two, f09a_transfer, f09b_refit,
               f13_attention, f14_learned, f16_dose, f17_jspace_last_token, f18_atoms)  # fmt: skip
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
    s07b_lens_readout,
    s07_recall_follows_swap,
    s03_order_split,
    s14_learned_sizes,
    s17_jspace_grids,
)


# the README's main figures in page order (Dan's v6 iteration 2, 28 Oct ~15:40; his figures brief, ~18:30: fig00b, the
# ladder in fig01c's place, the 2 x 2, Fig. 9 split into 9a here and 9b in Part IV), at most fourteen: fig05c (Part IV,
# now a link), fig11 (the breadth page's, not on the depth page), fig09b_refit (Part IV, a link), fig13 and fig14 (the
# Appendix) moved to the second sheet; Dan decides. His Fig. 5b / 5d brief (~20:30): E3's card shows Fig. 5d, and
# Fig. 5b (the main test's parts) goes to the second sheet, linked from E1, to keep the sheet at fourteen. Dan's
# restructure brief (28 Oct 22:20): one figure per card, every page figure on this sheet in page order; Part I's cards
# show the dose curves (Fig. 16) and the earlier mention (Fig. 3c), the 2 x 2 moves to Part V
README_NAMES = ("fig00_setup", "fig00b_marks", "fig01_split", "fig18_atoms", "fig09a_transfer", "fig16_dose",
                "fig01d_ladder", "fig03c_earlier_mention", "fig05d_routes_lens", "fig05_routes", "fig06b_anatomy",
                "fig07_writes", "fig09b_six_lockers", "fig07b_verbal", "fig03_order", "fig03d_depth_map",
                "fig17_jspace_last_token", "fig12_two_by_two")  # fmt: skip
# the draft set's second sheet: every other figure still drawn (the figures/story/ ones off the main sheet keep their
# files and links), the supplementary figures (README Appendix A) and docs/x0_details.md's figures
SHEET_MORE = ("fig01b_settings", "fig02_specificity", "fig02b_k_curve", "fig03b_layers",
              "fig06_depth", "fig08_first_locker", "fig10_what_is_left", "fig11_scorecard", "fig15_mechanisms",
              "fig13_attention", "fig14_learned", "fig09b_refit", "fig09_transfer",
              *(n for n in BATCH47 if n not in README_NAMES),
              "supp/s01_split_all_scene_sets", "supp/s01b_one_pick_duplicate", "supp/s01c_no_chat_template",
              "supp/s02_parts_all", "supp/s03_order_split", "supp/s03b_layers_45b", "supp/s03d_link_copy_variants",
              "supp/s03e_cumulative", "supp/s04_routes_design", "supp/s05_routes_all_arms", "supp/s07_recall_follows_swap",
              "supp/s07b_lens_readout", "supp/s08_first_sentence_and_label_free",
              "supp/s08b_pointer_moves_and_neutral_sentence", "supp/s10_removed_together_bars", "supp/s10b_what_is_left_all_scenes",
              "supp/s12_das_muse", "supp/s11_scorecard_all", "supp/s14_learned_sizes",
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
    card_numbers()
    ladder_agreement()
    cards_numbers()
    if out is None:  # the ledger's figures (docs/depth/EXPERIMENTS.md) into figures/ledger/, their rows into data.csv
        from scripts import ledger_figures as LF

        LF.build_all(plt)
    check_scorecard_keys(S.OUT / "scorecard.csv")
    check_scorecard_keys(S.OUT / "claims_scorecard.csv")
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
