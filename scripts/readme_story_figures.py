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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import story_style as S
from scripts import x0_figures as XF
from scripts import x0_necessity as X

N = S.numbers()
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
             ("wu", "logit-lens directions"), ("we", "input-embedding\ndirections"), ("rand", "random atoms")]  # fmt: skip
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
# The 26 Oct files (fig0_setup.png ... fig11_order.png) stay as they are; the detail panels go to figures/supp/.

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
    "varied": ("varied scenes: prose / JSON / table", "x0b_lk_excess_{m}", "x0b_rc_excess_{m}", "x0b_c_{m}"),
    "natural": ("natural passages", "nat_lk_excess_{m}", "nat_rc_excess_{m}", "nat_gap_{m}"),
}  # fmt: skip
AFTER_SETTING = {("single", "9b"), ("single", "27b")}  # one-change scenes on the 9B and 27B: after the data


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


def split_rows(ax, setting: str, fig_id: str, ci: bool) -> None:
    """One row per model: the lookup's and the recall's dots joined, the gap at the right end (bold; its interval if
    ci)."""
    S.extra_axis(ax, label=False)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.5", "0.75", "1"])
    ax.text(1.04, 0.45, "gap", transform=ax.get_yaxis_transform(), fontsize=S.FONT, color=S.COL["muted"], clip_on=False)
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
            ax.text(1.04, y, "–", transform=ax.get_yaxis_transform(), va="center", weight="bold", clip_on=False)
            S.record(fig_id, target, f"{what}: recall extra loss", *rc, source=c["src"])
            continue
        ax.plot([lk[0], rc[0]], [y, y], color="#d6d6d6", lw=4, zorder=1, solid_capstyle="butt")
        S.dot(ax, 0, y, lk, S.COL["lookup"], c["kind"], size=11 if ci else 9.5)
        S.dot(ax, 0, y, rc, S.COL["recall"], c["kind"], size=11 if ci else 9.5)
        gap = c["gap"] or (rc[0] - lk[0], rc[0] - lk[0], rc[0] - lk[0])
        ax.text(1.04, y, f"{gap[0]:.2f}", transform=ax.get_yaxis_transform(), va="center", fontsize=S.FONT + 2,
                weight="bold", clip_on=False)  # fmt: skip
        if ci:
            ax.text(1.155, y, f"[{gap[1]:.2f}, {gap[2]:.2f}]", transform=ax.get_yaxis_transform(), va="center",
                    color=S.COL["muted"], clip_on=False)  # fmt: skip
        S.record(fig_id, target, f"{what}: lookup extra loss", *lk, source=c["src"])
        S.record(fig_id, target, f"{what}: recall extra loss", *rc, source=c["src"].replace("lk", "rc"))
        S.record(fig_id, target, f"{what}: gap", *gap, source=SETTINGS[setting][3].format(m=m))
    ax.set_ylim(-len(S.MODELS) + 0.45, 0.55)
    ax.set_yticks([-i for i in range(len(S.MODELS))], labels)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eeeeee")


def f01_split(plt) -> None:
    """The main test, fixed in advance on all four models: per model the lookup's and the recall's J++ extra loss, the
    gap with its interval at the right."""
    fig, ax = plt.subplots(figsize=(S.WIDTH, 4.6))
    fig.subplots_adjust(left=0.215, right=0.70, top=0.72, bottom=0.20)
    S.title(fig, "Recall needs the J++ part of the bridge; the lookup mostly does not",
            "Extra loss (0-1): switches lost without the J++ part, minus those lost without a random part\n"
            "(same size). 0 = the reader does not need the J++ part; 1 = every switch needs it.\n"
            "Main test (two people swap picks), fixed in advance.")  # fmt: skip
    split_rows(ax, "main", "fig01", ci=True)
    first = split_cell("main", *S.MODELS[0][:2])
    for v, name, col in ((first["lk"], "lookup", S.COL["lookup"]), (first["rc"], "recall", S.COL["recall"])):
        ax.text(v[0], 0.38, name, ha="center", va="bottom", weight="bold", color=col)
    ax.set_ylim(-4.05, 0.55)  # room for the band's label under the last row
    ax.text(-0.05, -3.68, "not needed\n(below 0.1)", ha="center", va="center", color=S.COL["muted"])
    ax.set_xlabel("extra loss without the J++ part")
    fig.text(0.01, 0.02, "Lines: 95% intervals, bootstrap over bridge items.", color=S.COL["muted"])
    S.save(fig, "fig01_split")


def f01b_settings(plt) -> None:
    """The same per model in the other settings: the logit difference, one change only, varied scenes, natural passages."""
    fig, axes = plt.subplots(2, 2, figsize=(S.WIDTH, 7.6))
    fig.subplots_adjust(left=0.07, right=0.91, top=0.70, bottom=0.08, wspace=0.42, hspace=0.62)
    S.title(fig, "In every setting, recall needs the J++ part more than the lookup does",
            "Extra loss (0-1): switches lost without the J++ part, minus those lost without a random part\n"
            "(same size). Logit difference: the share of the logit shift lost instead of switches lost.")  # fmt: skip
    for ax, setting in zip(axes.flat, ("ld", "single", "varied", "natural"), strict=True):
        split_rows(ax, setting, "fig01b", ci=False)
        ax.set_title(SETTINGS[setting][0], loc="left", weight="bold", fontsize=S.FONT + 0.5)
        ax.set_xlabel("extra loss (logit difference)" if setting == "ld" else "extra loss without the J++ part")
    hs, ls = reader_handles(plt)
    sh, sl = S.status_handles()
    legend(fig, hs + sh, ls + sl, 0.875)
    S.save(fig, "fig01b_settings")


# Fig. 2: one panel per part, rows = models with the part's share of the change in the label; J++ and the main
# directions from the parts runs (one-change scenes, after the data), the logit lens and the random atoms from the main
# test (fixed in advance), as in parts_cells. "rand" is a dictionary of random atoms picked by the same OMP at its own
# (smaller) share, not the matched control (Dan ~22:40)
SPEC_PARTS = (("jpp", "J++ part"), ("pca_eq", "PCA directions (same size)"), ("wu", "logit-lens directions"),
              ("rand", "random atoms"))  # fmt: skip


def f02_specificity(plt) -> None:
    """Per part, per model: the recall's extra loss (dot with CI) and the lookup's (small purple dot); the part's share of
    the change in the row label."""
    cells = parts_cells()
    fig, axes = plt.subplots(2, 2, figsize=(S.WIDTH, 7.5), sharex=True)
    fig.subplots_adjust(left=0.13, right=0.99, top=0.69, bottom=0.085, wspace=0.42, hspace=0.38)
    S.title(fig, "No other part of the same size costs the recall as much as the J++ part",
            "Extra loss (0-1): switches lost without the part, minus those lost without a random part\n"
            "(same size). Recall with 95% CI; % = the part's share of the change. Random atoms: a dictionary\n"
            "of random atoms, picked by the same OMP at its own share.\n"
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


def f03_order(plt) -> None:
    """After the data: the lookups (open purple bars, 95% Wilson) and the recalls (grey dots) the whole change switches
    in the main test, the original bridge's locker sentence before vs after the asked person's pick sentence."""
    from bridge_jspace.stats import wilson
    from scripts import x0_strata as ST

    fig, ax = plt.subplots(figsize=(S.WIDTH, 5.0))
    fig.subplots_adjust(left=0.09, right=0.995, top=0.72, bottom=0.25)
    S.title(fig, "Lookups follow the change mostly when the locker sentence comes first",
            "Lookups the whole change switches (%), with 95% intervals. Main test (two people swap picks);\n"
            "after the data.")  # fmt: skip
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
        ax.text(i * 3.6 + 0.65, -0.30, name, transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=S.FONT, weight="bold")  # fmt: skip
    ax.set_xticks(xs, labels)
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 112)
    ax.set_ylabel("lookups switched (%)")
    ax.grid(axis="y", color="#eeeeee")
    ax.set_axisbelow(True)
    legend(fig, [plt.Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["lookup"], lw=2),
                 plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=6)],
           ["lookup", "recall"], 0.83)  # fmt: skip
    S.save(fig, "fig03_order")


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
    S.save(fig, "fig04_routes_design")


# Fig. 5's rows: the arm (and the run it comes from: the removals or the keep-only arms), its label, and the random
# control shown as a thin grey bar under it (the position share with a random part of the same size)
ROUTE_ROWS = (("whole", "whole change", None, "main"), ("no_alf", "without the pointer", "no_alf_rand", "main"),
              ("keep_alf", "only the pointer", "keep_alf_rand", "keep"), ("keep_jpp", "only the J++ part", "keep_jpp_rand", "keep"))  # fmt: skip
ROUTE_RUNS = {"9b": ("qwen35_9b_x6_routes", "qwen35_9b_x6_routes_keeponly"),
              "27b": ("x6_routes_27b", "x6_routes_keeponly_27b"),
              "122b": ("qwen35_122b_x6_routes_g75", "qwen35_122b_x6_routes_keeponly_g75"),
              "muse": ("muse30b_x6_routes", "muse30b_x6_routes")}  # fmt: skip


def f05_routes(plt) -> None:
    """Another item moved, at the layer fixed in advance: the lookup's route shares per arm (stacked), and under each part's
    bar a thin grey bar for the position share with a random part of the same size."""
    fig, axes = plt.subplots(1, 4, figsize=(S.WIDTH, 5.5), sharey=True)
    fig.subplots_adjust(left=0.20, right=0.975, top=0.63, bottom=0.13, wspace=0.24)
    S.title(fig, "The lookup follows identity or position, never the value",
            "Lookup answers (%), routes test (another item moved). Thin grey: position answers with a\n"
            f"random part (same size) instead. Fixed in advance; {S.LOWERED} gate lowered to 0.75 after the data.")  # fmt: skip
    for ax, (target, m, _) in zip(axes, S.MODELS, strict=True):
        ax.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1], ["0", "50", "100"])
        runs: dict[str, str] = dict(zip(("main", "keep"), ROUTE_RUNS[m], strict=True))
        rows = {}
        for key, run in runs.items():
            v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
            rows[key] = {r["arm"]: r for r in (v or {}).get("rows", []) if r["condition"] == "C2"}
        for i, (arm, _, rand, src) in enumerate(ROUTE_ROWS):
            r = rows[src].get(arm)
            if r is None:
                continue
            left = 0.0
            for route, _ in ROUTES:
                sh = r["share"][route][0]
                ax.barh(-i, sh, left=left, height=0.56, color=ROUTE_COL[route], edgecolor="white", lw=0.8)
                if route in ("identity", "position") and sh >= 0.10:
                    ax.text(left + sh / 2, -i, f"{100 * sh:.0f}", ha="center", va="center", fontsize=S.FONT,
                            color="white" if route == "identity" else "#222222")  # fmt: skip
                S.record("fig05", target, f"another item moved, {arm}: {route} share", *r["share"][route], n=r["n"],
                         source=runs[src])  # fmt: skip
                left += sh
            rr = rows[src].get(rand) if rand else None
            if rr is not None:
                pos = rr["share"]["position"][0]
                ax.barh(-i - 0.42, pos, height=0.12, color=S.COL["control"], lw=0)
                ax.text(pos + 0.02, -i - 0.42, f"{100 * pos:.0f}", va="center", fontsize=S.FONT, color=S.COL["muted"])
                S.record("fig05", target, f"another item moved, {rand}: position share", *rr["share"]["position"],
                         n=rr["n"], source=runs[src])  # fmt: skip
        ax.set_ylim(-len(ROUTE_ROWS) + 0.35, 0.5)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks([-i for i in range(len(ROUTE_ROWS))], [r[1] for r in ROUTE_ROWS])
    fig.supxlabel("lookup answers (%)", x=0.6, y=0.01, fontsize=S.FONT)
    hs = [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL[r]) for r, _ in ROUTES[:4]]
    hs += [plt.Rectangle((0, 0), 1, 0.3, color=S.COL["control"])]
    legend(fig, hs, [n for _, n in ROUTES[:4]] + ["random part (same size)"], 0.83)
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
    fig.subplots_adjust(left=0.11, right=0.99, top=0.66, bottom=0.09, wspace=0.16, hspace=0.18)
    S.title(fig, "Position answers appear with depth, once the lookup stops needing the J++ part",
            "Candidate, after the data. Extra loss (0-1): switches lost without the J++ part, minus those lost\n"
            "without a random part (same size). Shaded: layers where the lookup still needs the J++ part\n"
            "(extra loss ≥ 0.3).", limit=78)  # fmt: skip
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
    sh, sl = S.status_handles()
    legend(fig, hs + sh, [*ls, "position answers", *sl], 0.82)
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


NAMED_LABEL = (
    "bridge named first,\nits locker sentence",
    "bridge named first,\na pick sentence",
    "another item\nnamed first",
)
X8_ORDER = {"9b": "qwen35_9b_x8_order", "27b": "x8_order_27b", "122b": "qwen35_122b_x8_order_g75",
            "muse": "muse30b_x8_order_r2"}  # fmt: skip
PCF = {"9b": "qwen35_9b_x7_pcf", "27b": "x7_pcf_27b", "122b": "qwen35_122b_x7_pcf", "muse": "muse30b_x7_pcf"}


def f08_first(plt) -> None:
    """After the data: (a) the main test's pointer removal, the lookup's extra loss by which item the first sentence
    names (x0_first_sentence, NAMED); (b) the routes test, the position answers with only the pointer for moves to or
    from the first locker vs between the second and third (grey: the whole change); (c) the neutral-sentence test (batch
    44 B): the code's shift in positions with a sentence before the first locker (B1) or between the lockers and the
    picks (B2); (d) the label-free pointer's overlap with the pointer (mean cos^2), chance = a random 4-d subspace's
    (4 / d, the P_cf reports' random_mean_cos2). Layout in inches from the top (Dan ~21:55: legends, not colour words)."""
    from scripts import x0_first_sentence as FS

    first = latest(pins.RESULTS_DIR / "x0_massmean", "first-sentence-*/first.json") or {}
    pairs = latest(pins.RESULTS_DIR / "x8_write", "pairs-*/pairs.json") or {}
    h = 12.5
    fig = plt.figure(figsize=(S.WIDTH, h))

    def at(inch: float) -> float:  # inches from the top -> figure fraction
        return 1 - inch / h

    grid_a = fig.add_gridspec(1, 4, left=0.24, right=0.99, top=at(2.0), bottom=at(3.85), wspace=0.14)
    grid_b = fig.add_gridspec(1, 4, left=0.24, right=0.99, top=at(5.3), bottom=at(6.7), wspace=0.14)
    S.title(fig, "Our pointer directions separate the first-mentioned item from the rest",
            f"All after the data; {S.LOWERED} gate lowered to 0.75 after the data. Extra loss (0-1): switches lost\n"
            "without the pointer, minus those lost without a random part (same size).")  # fmt: skip
    head = dict(fontsize=S.FONT, weight="bold", va="top")
    fig.text(0.01, at(1.05), "(a) Without the pointer, by what the prompt names first", **head)
    fig.text(0.01, at(4.55), "(b) Only the pointer: position answers by the move", **head)
    fig.text(0.01, at(7.85), "(c) A neutral sentence barely moves\nthe pointer's code", **head)
    fig.text(0.58, at(7.85), "(d) label-free pointer: overlap with\nthe pointer (mean cos²)", **head)
    open_dot = dict(marker="o", ls="", mfc="white", mew=1.6, ms=7)
    legend(fig, [plt.Line2D([], [], mec=S.COL["lookup"], **open_dot),
                 plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=5)], ["lookup", "recall"], at(1.3))  # fmt: skip
    legend(fig, [plt.Rectangle((0, 0), 1, 1, color=S.COL["position"]), plt.Rectangle((0, 0), 1, 1, color="#c8c8c8")],
           ["only the pointer", "whole change"], at(4.8))  # fmt: skip
    fig.legend([plt.Line2D([], [], mec=S.COL["lookup"], **open_dot), plt.Line2D([], [], mec="#9a9a9a", **open_dot)],
               ["a sentence before the first locker\n(would shift the code if it counted sentences)",
                "a sentence between the lockers and the picks\n(would shift it if it counted distance back)"],
               loc="upper left", bbox_to_anchor=(0.0, at(8.35)), frameon=False, handletextpad=0.4, labelspacing=0.6,
               handlelength=1.4)  # fmt: skip
    for j, (target, m, _) in enumerate(S.MODELS):
        a, b = fig.add_subplot(grid_a[0, j]), fig.add_subplot(grid_b[0, j])
        S.extra_axis(a)
        a.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        f = first.get(target, {})
        for i, g in enumerate(FS.NAMED):
            lk, rc = f.get(f"{X.LOOKUP}|named|{g}", {}), f.get(f"{X.RECALL}|named|{g}", {})
            if "extra_loss" in rc:
                a.plot([rc["extra_loss"][0]], [-i - 0.25], "o", ms=5, color=S.COL["recall"], zorder=3)
            if "extra_loss" in lk:
                S.dot(a, 0, -i, lk["extra_loss"], S.COL["lookup"], "after")
                S.record("fig08", target, f"(a) lookup extra loss without the pointer: {g}", *lk["extra_loss"], n=lk["n"],
                         source="x0_first_sentence")  # fmt: skip
        a.set_ylim(-len(FS.NAMED) + 0.4, 0.6)
        a.set_yticks([-i for i in range(len(FS.NAMED))], NAMED_LABEL if j == 0 else [])
        a.tick_params(axis="y", length=0)
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
                S.record("fig08", target, f"(b) routes, position share, {arm}, moves {name}", round(share, 4),
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
    c = fig.add_axes((0.10, at(11.45), 0.40, at(9.5) - at(11.45)))
    d = fig.add_axes((0.67, at(11.45), 0.24, at(9.5) - at(11.45)))
    chance = {}
    for i, (target, m, _) in enumerate(S.MODELS):
        v = latest(pins.RESULTS_DIR / "x8_write" / X8_ORDER[m], "verdict-*/verdict.json")
        if v is None:
            c.text(i, 0.5, "not run", ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"], rotation=90)
        else:
            for k, (b_, col) in enumerate((("B1", S.COL["lookup"]), ("B2", "#9a9a9a"))):
                beta = v["variants"][b_]["beta"]
                c.plot([i + (k - 0.5) * 0.3] * 2, [beta[1], beta[2]], color=col, lw=1.6)
                c.plot([i + (k - 0.5) * 0.3], [beta[0]], "o", ms=7, mfc="white", mec=col, mew=1.6)
                S.record("fig08", target, f"(c) neutral sentence {b_}: the code's shift in positions", *beta,
                         n=v["variants"][b_]["n"], source=X8_ORDER[m])  # fmt: skip
        r = json.loads(p.read_text()) if (p := pins.RESULTS_DIR / "x7_pcf" / PCF[m] / "report.json").exists() else None
        if r is not None:
            d.bar(i, r["mean_cos2_with_alf"], width=0.6, color=S.COL["position"])
            d.text(i, r["mean_cos2_with_alf"] + 0.03, f"{r['mean_cos2_with_alf']:.2f}", ha="center", fontsize=S.FONT)
            S.record("fig08", target, "(d) label-free pointer: mean cos^2 with ours", round(r["mean_cos2_with_alf"], 4),
                     source=PCF[m])  # fmt: skip
            chance[target] = (i, r["random_mean_cos2"], PCF[m])
    for line_y, ls, text in ((0.5, "--", "counts as shifted"), (1.0, ":", "one full position")):
        c.axhline(line_y, color="#555555", ls=ls, lw=1)
        c.text(-0.45, line_y + 0.02, text, ha="left", va="bottom", fontsize=S.FONT, color="#555555")
    c.set_ylim(-0.1, 1.2)
    c.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    c.set_xlim(-0.5, 3.5)
    c.set_xticks(range(4), ["9B", "27B", f"122B{S.LOWERED}", "Muse"])
    c.set_ylabel("code shift (positions)")
    c.grid(axis="y", color="#eeeeee")
    fig.text(0.01, at(12.15), "Same neutral sentence in both prompts (no item, no digit, 10-12 tokens).",
             color=S.COL["muted"], va="center")  # fmt: skip
    # chance: a random 4-d subspace against the pointer's, 4 / d per model (d: the hidden size); one line where the four
    # agree to two decimals (they do: 0.0006-0.0013), else one per bar
    for target, (_, ch, src) in chance.items():
        S.record("fig08", target, "(d) chance: a random 4-d subspace's mean cos^2 (4 / d)", ch, source=src)
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
    S.save(fig, "fig08_first_mentioned")


# Fig. 8b (Dan ~21:40, draft until Tuesday's merge): 45a's sentence before the lockers, rows top to bottom with a divider
# after the second; the variants' labels as the README words them
LAYOUT_ROWS = (("V0", "no sentence"), ("V4", "a neutral sentence"), ("V1", "a pick: the first-locker item"),
               ("V2", "a pick: another locker item"), ("V3", "a pick: an item with no locker"))  # fmt: skip
DRAFTS = S.REPO / "figures" / "drafts"


def f08b_layout(plt, draft: bool = True) -> None:
    """After the data (45a, results/x6_routes/x45a-descriptive-*): per model, the lookup's answers on first-locker moves
    under the whole change, by the sentence added before the lockers (stacked: identity, position, original; other only
    if >= 0.02; value is 0 everywhere), and beta, the shift of the pointer's code vs no sentence. The 122B's panel only
    once its run is in the table. draft: saved to figures/drafts/ with its data.csv rows beside it (fig08b_layout.csv)."""
    table = latest(pins.RESULTS_DIR / "x6_routes", "x45a-descriptive-*/table.json") or {}
    by = {b["model"]: (run, b) for run, b in table.items()}
    models = [(t, m) for t, m, _ in S.MODELS if t in by]
    fig, axes = plt.subplots(1, len(models), figsize=(S.WIDTH, 4.9), sharey=True, squeeze=False)
    fig.subplots_adjust(left=0.27, right=0.905, top=0.62, bottom=0.12, wspace=0.40)
    S.title(fig, "Naming an item before the lockers switches the lookup from position to identity",
            "Routes test (another item moved), one sentence added before the lockers in both prompts.\n"
            "After the data; the rule fixed in advance read the answers with only the pointer (mixed).\n"
            "Code shift (positions), β: how far the pointer's code moves against no sentence.", limit=86)  # fmt: skip
    ys = [0, -1, -2.4, -3.4, -4.4]  # the gap after the second row holds the divider
    for ax, (target, m) in zip(axes[0], models, strict=True):
        run, b = by[target]
        ax.set_title(name_of(m, m in LOWERED_M), fontsize=S.FONT, weight="bold")
        r, beta = b["routes"], b["beta"]
        for (v, label), y in zip(LAYOUT_ROWS, ys, strict=True):
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
                S.record("fig08b", target, f"45a, first-locker moves, whole change, {label}: {route} share", round(sh, 4),
                         *ci, n=r["n"], source=f"x6_routes/{run}")  # fmt: skip
                left += sh
            if v in beta:
                bv = beta[v]["beta"]
                ax.text(1.03, y, f"β {bv[0]:.2f}", va="center", ha="left", fontsize=S.FONT, color=S.COL["muted"],
                        transform=ax.get_yaxis_transform())  # fmt: skip
                S.record("fig08b", target, f"45a, beta vs no sentence: {label}", round(bv[0], 4), bv[1], bv[2],
                         n=beta[v]["n"], source=f"x6_routes/{run}")  # fmt: skip
        ax.plot([0, 1], [-1.7, -1.7], color="#999999", ls="--", lw=1, clip_on=False)
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1], ["0", "50", "100"])
        ax.set_ylim(-4.85, 0.5)
        ax.tick_params(axis="y", length=0)
        for side in ("left", "right", "top"):
            ax.spines[side].set_visible(False)
    axes[0][0].set_yticks(ys, [label for _, label in LAYOUT_ROWS])
    fig.supxlabel("lookup answers (%), first-locker moves, whole change", x=0.6, y=0.01, fontsize=S.FONT)
    names = {"identity": "identity", "position": "position", "original": "original answer"}
    legend(fig, [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL[k]) for k in names], list(names.values()), 0.745)
    if not draft:
        S.save(fig, "fig08b_layout")
        return
    DRAFTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(DRAFTS / "fig08b_layout.svg", facecolor="white")
    fig.savefig(DRAFTS / "fig08b_layout.png", dpi=200, facecolor="white")
    plt.close(fig)
    rows = [r for r in S.ROWS if r["figure"] == "fig08b"]
    with (DRAFTS / "fig08b_layout.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def f09_transfer(plt) -> None:
    """Per model, the lookup's extra loss without J++ (black) and without the pointer directions (orange, fit on simple
    scenes, not refit) in simple scenes, varied scenes by format and natural passages (fact first)."""
    fig, axes = plt.subplots(1, 4, figsize=(S.WIDTH, 5.3), sharey=True)
    fig.subplots_adjust(left=0.17, right=0.995, top=0.62, bottom=0.11, wspace=0.12)
    S.title(fig, "The split carries over to other texts; the pointer does not",
            "The lookup's extra loss (0-1): switches lost without the part, minus those lost without a random\n"
            "part (same size). The pointer is fit on simple scenes and not refit.")  # fmt: skip
    black = "#222222"
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
                        ax.text(0.2, -i + dy, why, fontsize=S.FONT, color=S.COL["muted"], va="center", linespacing=1.0)
                    continue
                after = part == "jpp" and cells.get((kind, "after"))
                S.dot(ax, 0, -i + dy, v, col, "after" if after else "fixed", size=6.5)
                if after:
                    ax.text(v[2] + 0.04, -i + dy, S.LOWERED, va="center", fontsize=S.FONT)
                S.record("fig09", target, f"lookup extra loss without {'J++' if part == 'jpp' else 'the pointer'}: {sc}", *v,
                         source="readme_story_figures.transfer_cells")  # fmt: skip
        ax.set_ylim(-len(SCENES) + 0.4, 0.6)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(
        [-i for i in range(len(SCENES))], ["simple scenes", "prose", "JSON", "table", "natural\npassages"]
    )
    sh, sl = S.status_handles()
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=black, ms=7), plt.Line2D([], [], marker="o", ls="", color=S.COL["position"], ms=7), *sh],
           ["without the J++ part", "without the pointer (fit on simple scenes)", *sl], 0.82)  # fmt: skip
    S.save(fig, "fig09_transfer")


LEFT_RUNS = {"9b": ("qwen35_9b_x6_routes_bothoff", "qwen35_9b_x6_routes_d1"),
             "27b": ("x6_routes_bothoff_27b", "x6_routes_d1_27b"),
             "122b": ("qwen35_122b_x6_routes_bothoff_g75", None),
             "muse": ("muse30b_x6_routes", "muse30b_x6_routes_d1_r2")}  # fmt: skip
LEFT_PARTS = (("both", "J++ part\n+ pointer"), ("jpp+alf+idout", "+ identity\noutside J++"))


def f10_left(plt) -> None:
    """The sanity swap, one panel per model (as Figs. 8 and 9), one row per removal: J++ and the pointer (the both-removed
    runs), and identity outside J++ removed too (batch 40). Per row, the share of the whole change's lookup switches
    still switching with the part removed (purple) and with a random part of the same size removed (grey), joined by a
    line: its length is the part's extra loss. The part's median share of the change under the row (Dan ~22:00: the
    one-axis version was hard to read)."""
    fig, axes = plt.subplots(1, 4, figsize=(S.WIDTH, 4.5), sharey=True)
    fig.subplots_adjust(left=0.17, right=0.985, top=0.60, bottom=0.15, wspace=0.12)
    # Dan's title (~22:40): 84 characters, 11.0 pt
    S.title(fig, "J++ part, pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's",
            "Sanity swap. Lookups still switching (%), out of the whole change's switches. The line from\n"
            "grey to purple is what the part removes beyond a random part (same size): its extra loss.", limit=90)  # fmt: skip
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
            run = LEFT_RUNS[m][0 if part == "both" else 1]
            v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json") if run else None
            e = next((e for e in (v or {}).get("extra", []) if e["condition"] == "C0" and e["reader"] == X.LOOKUP
                      and e["part"] == part), None)  # fmt: skip
            if e is None:
                ax.text(56, y, "not run", ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"])
                continue
            pts = {}
            for lost, col, what in ((e["Jdep"], S.COL["lookup"], "the part"),
                                    (e["Rdep"], grey, "a random part of the same size")):  # fmt: skip
                left = (1 - lost[0], 1 - lost[2], 1 - lost[1])
                pts[col] = left
                S.record("fig10", target, f"sanity swap, lookups still switching without {label.replace(chr(10), ' ')}: {what}",
                         *left, source=run)  # fmt: skip
            ax.plot([100 * pts[grey][0], 100 * pts[S.COL["lookup"]][0]], [y, y], color=S.COL["lookup"], lw=2.2,
                    alpha=0.35, zorder=2)  # fmt: skip
            for col, left in pts.items():
                ax.plot([100 * left[1], 100 * left[2]], [y, y], color=col, lw=1.6, zorder=3, solid_capstyle="butt")
                face = col if kind == "fixed" else "white"
                ax.plot([100 * left[0]], [y], "o", ms=8, mfc=face, mec=col, mew=1.6, zorder=4)
            ax.text(2, y - 0.3, f"{100 * e['share']:.0f}% of the change", ha="left", va="center", fontsize=S.FONT,
                    color=S.COL["muted"])  # fmt: skip
            S.record("fig10", target, f"share of the change: {label.replace(chr(10), ' ')}", round(e["share"], 4),
                     source=run)  # fmt: skip
        ax.set_ylim(-len(LEFT_PARTS) + 0.45, 0.45)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks([-k for k in range(len(LEFT_PARTS))], [label for _, label in LEFT_PARTS])
    fig.supxlabel("lookups still switching (%)", x=0.58, y=0.01, fontsize=S.FONT)
    sh, sl = S.status_handles()
    legend(fig, [plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=8), plt.Line2D([], [], marker="o", ls="", color=grey, ms=8), *sh],
           ["without the part", "without a random part (same size)", *sl], 0.80)  # fmt: skip
    S.save(fig, "fig10_what_is_left")


# Fig. 11 (Dan ~16:45): the claims in story order; status per model, read off the verdicts and the README's numbers
# (agent's reading, UNVERIFIED); "a" = after the data (or a gate lowered after the data)
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
SYMBOL = {"held": ("✓", "#2f7d4f"), "partial": ("~", "#b07a0a"), "no": ("✗", "#b8433a"), "not tested": ("–", "#8a8a8a")}


def f11_scorecard(plt) -> None:
    """Rows = claims in story order, columns = models; a symbol per cell (held / partial / no / not tested) and a small
    'a' for after the data."""
    fig, ax = plt.subplots(figsize=(S.WIDTH, 6.9))
    fig.subplots_adjust(left=0.36, right=0.99, top=0.86, bottom=0.07)
    S.title(fig, "What held where", "✓ held   ~ partial   ✗ no   – too few switches*;   a: after the data")
    n_sw, n = N.get("nat_lk_whole_sw_muse"), N.get("nat_n_muse")
    fig.text(0.01, 0.015, f"*Muse, natural passages: the lookup has too few switches ({n_sw} of {n}).",
             color=S.COL["muted"])  # fmt: skip
    for j, (target, m, name) in enumerate(S.MODELS):
        ax.text(j, 0.75, name.replace(" Glimmer 30B", "\nGlimmer 30B"), ha="center", va="bottom", fontsize=S.FONT,
                weight="bold")  # fmt: skip
        for i, (claim, cells) in enumerate(SCORECARD_V4):
            status, after = cells[m]
            sym, col = SYMBOL[status]
            ax.text(j, -i, sym, ha="center", va="center", fontsize=S.FONT + 7, color=col, weight="bold")
            if after:
                ax.text(j + 0.2, -i + 0.18, "a", ha="left", va="center", fontsize=S.FONT, color=S.COL["muted"])
            if claim == "The split in natural passages" and m == "muse":  # the footnote under the figure
                ax.text(j + 0.2, -i + 0.18, "*", ha="left", va="center", fontsize=S.FONT + 2, color=S.COL["muted"])
            S.record("fig11", target, claim.replace("\n", " "), status, source="after the data" if after else "fixed")
    for i in range(len(SCORECARD_V4)):
        if i % 2 == 0:
            ax.axhspan(-i - 0.5, -i + 0.5, color="#f6f6f6", lw=0, zorder=0)
    ax.set_xlim(-0.5, len(S.MODELS) - 0.5)
    ax.set_ylim(-len(SCORECARD_V4) + 0.45, 1.5)
    ax.set_yticks([-i for i in range(len(SCORECARD_V4))], [c for c, _ in SCORECARD_V4])
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    S.save(fig, "fig11_scorecard")


README_FIGS = (f00_setup, f01_split, f01b_settings, f02_specificity, f03_order, f04_routes_design, f05_routes, f06_depth, f07_writes,
               f08_first, f09_transfer, f10_left, f11_scorecard)  # fmt: skip


README_NAMES = ("fig00_setup", "fig01_split", "fig01b_settings", "fig02_specificity", "fig03_order",
                "fig04_routes_design", "fig05_routes", "fig06_depth", "fig07_writes", "fig08_first_mentioned",
                "fig09_transfer", "fig10_what_is_left", "fig11_scorecard")  # fmt: skip
# the draft set's second sheet: the supplementary figures (README Appendix A) and docs/x0_details.md's figures
SHEET_MORE = ("supp/s01_split_all_scene_sets", "supp/s02_parts_all", "supp/s05_routes_all_arms",
              "supp/s10_removed_together_bars", "x0_necessity/overview", "x0_necessity/detail_x0_necessity_27b_chat_chat",
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
    """Default: figures/story/ (+ figures/supp/, docs/figures_contact_sheet.png), as before. --out DIR: the whole draft
    set (Dan, 26 Oct ~21:50 / ~22:45: figures/drafts/v5): the README figures with Fig. 8b beside Fig. 8, the
    supplementary figures in DIR/supp, docs/x0_details.md's figures in DIR/x0_necessity (x0_figures) and
    DIR/status_2026-10-24 (x0_status_pack's f6), each folder with its data.csv; DIR/contact_sheet.png (the README
    figures) and DIR/contact_sheet_more.png (the rest). figures/story/, figures/supp/, figures/x0_necessity/ and docs/ stay
    untouched."""
    import argparse

    ap = argparse.ArgumentParser(description="The README figures, their data.csv and contact sheet.")
    ap.add_argument("--out", type=Path, default=None, help="draft output dir (default: figures/story)")
    args = ap.parse_args(argv)
    figs, sheet = list(README_FIGS), S.REPO / "docs" / "figures_contact_sheet.png"
    names: list[str] = list(README_NAMES)
    out = None
    if args.out is not None:
        out = args.out if args.out.is_absolute() else S.REPO / args.out
        S.OUT, S.SUPP, sheet = out, out / "supp", out / "contact_sheet.png"
        figs.insert(figs.index(f08_first) + 1, lambda plt: f08b_layout(plt, draft=False))
        names.insert(names.index("fig08_first_mentioned") + 1, "fig08b_layout")
    plt = S.setup()
    for f in (*figs, s01_split, s02_parts, s05_routes, s10_removed_together):
        f(plt)
    S.write_data()
    contact_sheet(plt, names, sheet)
    if out is not None:
        from scripts import x0_status_pack as SP

        XF.render(out / "x0_necessity")
        SP.render(out / "status_2026-10-24", ["f6"])  # after x0_figures: its style() recolours scripts.figs.common
        plt = S.setup()
        contact_sheet(plt, SHEET_MORE, out / "contact_sheet_more.png")
    print(S.OUT)


if __name__ == "__main__":
    main()
