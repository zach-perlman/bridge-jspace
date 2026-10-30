"""Figures across exp02_swaps runs (part B), in part A's style. Reads each run's summary.json and outcomes.jsonl;
writes into a new folder (write-once).

  exp02_figures.py OUT_NAME   -> figures/pre-sprint/exp02_swaps/OUT_NAME/
                                 jpart_vs_remainder.png  J-part / remainder / remainder with J held, J-lens vs J++ vs
                                                      Claude (the headline)
                                 swap_position.png    an example prompt with the swapped regions, and the J-part flip
                                                      rate when only that region is swapped
                                 examples.png         three questions: the answer before and after each swap
                                 by_bridge_type.png   J-part flip rate by what the bridge is (place, person, other)
                                 lens_comparison.png  flip rate per swap condition, J-lens vs J++, per band, with the
                                                      matched-norm nulls and Claude's reference rates
                                 positions.png        flip rate per condition by which prompt positions are swapped
                                 outcomes.png         flip / kept clean / neither per condition, swap vs null
                                 dose.png             flip rate against the edit size, per condition and lens
                                 per_question.png     every eligible question x (condition, lens): flip / kept / neither

Runs (v4: greedy-continuation scoring, stripped prompts, 77 eligible items) are named in RUNS below.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.plotting import GRID, INK, MUTED, SURFACE, style_axes
from bridge_jspace.stats import wilson

EXP = "exp02_swaps"
JLENS, JPP, CONTROL, BROKEN = "#2a78d6", "#eb6834", "#b4b2a9", "#5c5b55"
LENS_COLOR = {"jlens": JLENS, "jpp": JPP}
LENS_TITLE = {"jlens": "J-lens", "jpp": "J++"}
CONDITIONS = ("raw_jlens", "full_probe", "jpart", "remainder", "remainder_clamped")
CONDITION_LABEL = {
    "raw_jlens": "raw lens\nvectors",
    "full_probe": "full\nprobe",
    "jpart": "J-space\npart",
    "remainder": "remainder",
    "remainder_clamped": "remainder,\nJ-space held",
}
CLAUDE = {"jpart": 0.61, "remainder": 0.28, "remainder_clamped": 0.06}  # Gurnee et al. (2026), probe-swap
REGIMES = ("cue", "earlier_noncue", "earlier", "prev", "last", "last_two", "all")
REGIME_LABEL = {
    "cue": "cue\nphrase",
    "earlier_noncue": "other\nearlier words",
    "earlier": "earlier\nwords",
    "prev": "-1\n(bridge read\nbest, part A)",
    "last": "0\n(answer read,\npart A)",
    "last_two": "-1 and 0",
    "all": "every\nposition",
}
BANDS = {"24-40": "layers 24-40 (the gate's pick)", "32-48": "layers 32-48 (part A's band)"}
RUNS = {  # (lens, band, positions) -> run
    ("jlens", "24-40", "all"): "main_v4_jlens",
    ("jpp", "24-40", "all"): "main_v4_jpp",
    ("jlens", "32-48", "all"): "main_v4_jlens_32-48",
    ("jpp", "32-48", "all"): "main_v4_jpp_32-48",
    **{(lens, "24-40", r): f"main_v4_{lens}_pos-{r}" for lens in ("jlens", "jpp") for r in REGIMES if r != "all"},
}


def load(run: str) -> dict[str, Any] | None:
    run_dir = pins.RESULTS_DIR / EXP / run
    if not (run_dir / "summary.json").exists():
        return None
    summary = json.loads((run_dir / "summary.json").read_text())
    outcomes = [json.loads(line) for line in (run_dir / "outcomes.jsonl").read_text().splitlines() if line.strip()]
    items = [json.loads(line) for line in (run_dir / "items.jsonl").read_text().splitlines() if line.strip()]
    rates = {(r["condition"], r["null"]): r for r in summary["rates"]}
    return {"summary": summary, "rates": rates, "outcomes": outcomes, "items": items}


def n_eligible(data: dict[str, Any]) -> int:
    return data["summary"]["items"]["eligible"]


def err(w: list[float]) -> list[list[float]]:
    return [[max(0.0, w[0] - w[1])], [max(0.0, w[2] - w[0])]]


def legend_below(fig, handles: list, ncol: int) -> None:
    fig.legend(handles=handles, loc="lower center", ncol=ncol, frameon=False, fontsize=9, labelcolor=INK)


def lens_comparison(runs: dict, out: Path) -> None:
    bands = [b for b in BANDS if all(runs.get((lens, b, "all")) for lens in LENS_COLOR)]
    fig, axes = plt.subplots(1, len(bands), figsize=(6.4 * len(bands), 4.4), facecolor=SURFACE, sharey=True)
    x = np.arange(len(CONDITIONS))
    for ax, band in zip(np.atleast_1d(axes), bands, strict=True):
        style_axes(ax)
        for offset, lens in ((-0.2, "jlens"), (0.2, "jpp")):
            data = runs[(lens, band, "all")]
            for i, c in enumerate(CONDITIONS):
                w, w0 = data["rates"][(c, False)]["flip"], data["rates"][(c, True)]["flip"]
                ax.bar(i + offset, w[0], width=0.38, color=LENS_COLOR[lens], zorder=2)
                ax.errorbar(i + offset, w[0], yerr=err(w), color=INK, lw=1, capsize=3, zorder=3)
                ax.bar(i + offset, w0[0], width=0.22, color=CONTROL, zorder=4)  # the null, inside the bar
                ax.text(i + offset, w[2] + 0.02, f"{100 * w[0]:.0f}", ha="center", fontsize=8, color=INK)
        for i, c in enumerate(CONDITIONS):
            if c in CLAUDE:
                ax.plot([i - 0.42, i + 0.42], [CLAUDE[c]] * 2, color=INK, lw=1.4, ls=(0, (4, 2)), zorder=5)
        ax.set_xticks(x, [CONDITION_LABEL[c] for c in CONDITIONS], color=INK)
        ax.set_ylim(0, 1)
        ax.set_title(BANDS[band], loc="left", color=INK)
    first = runs[("jlens", bands[0], "all")]
    np.atleast_1d(axes)[0].set_ylabel("share of questions whose answer flips", color=MUTED)
    fig.suptitle(
        f"Swap the bridge for another entity: how often the model gives the other entity's answer "
        f"(Qwen3.6-27B, n={n_eligible(first)}, 95% CI)",
        x=0.01,
        ha="left",
        color=INK,
    )
    legend_below(
        fig,
        [
            Patch(color=JLENS, label="J-lens decomposition"),
            Patch(color=JPP, label="J++ decomposition"),
            Patch(color=CONTROL, label="control: random direction, same edit size"),
            Line2D([], [], color=INK, ls=(0, (4, 2)), label="Claude (Gurnee et al. 2026)"),
        ],
        4,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.95))
    fig.savefig(out / "lens_comparison.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def positions(runs: dict, out: Path) -> None:
    shown = ("raw_jlens", "jpart", "remainder", "remainder_clamped")
    fig, axes = plt.subplots(1, len(shown), figsize=(4.4 * len(shown), 4.4), facecolor=SURFACE, sharey=True)
    x = np.arange(len(REGIMES))
    n = None
    for ax, c in zip(axes, shown, strict=True):
        style_axes(ax)
        ax.axvspan(0.5, 1.5, color="#e9e8e1", zorder=0)  # offset -1: part A's bridge read site
        for offset, lens in ((-0.08, "jlens"), (0.08, "jpp")):
            ys, lo, hi, nulls = [], [], [], []
            for r in REGIMES:
                data = runs.get((lens, "24-40", r))
                w = data["rates"][(c, False)]["flip"] if data else [np.nan] * 3
                ys.append(w[0])
                lo.append(w[1])
                hi.append(w[2])
                nulls.append(data["rates"][(c, True)]["flip"][0] if data else np.nan)
                n = n or (n_eligible(data) if data else None)
            xs = x + offset
            ax.fill_between(xs, lo, hi, color=LENS_COLOR[lens], alpha=0.15, lw=0)
            ax.plot(xs, ys, color=LENS_COLOR[lens], lw=2.2, marker="o", ms=5)
            ax.plot(xs, nulls, color=CONTROL, lw=0, marker="o", ms=4)
        ax.set_xticks(x, [REGIME_LABEL[r] for r in REGIMES], fontsize=8, color=INK)
        ax.set_ylim(0, 1)
        ax.set_title(CONDITION_LABEL[c].replace("\n", " "), loc="left", color=INK)
    axes[0].set_ylabel("share of questions whose answer flips", color=MUTED)
    fig.suptitle(
        f"Where in the prompt does the swap act? Same swaps, applied only at some positions "
        f"(layers 24-40, n={n}, 95% CI)",
        x=0.01,
        ha="left",
        color=INK,
    )
    legend_below(
        fig,
        [
            Line2D([], [], color=JLENS, lw=2.2, marker="o", label="J-lens"),
            Line2D([], [], color=JPP, lw=2.2, marker="o", label="J++"),
            Line2D([], [], color=CONTROL, lw=0, marker="o", label="control: random direction, same edit size"),
            Patch(color="#e9e8e1", label="offset -1: where part A reads the bridge best"),
        ],
        4,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.95))
    fig.savefig(out / "positions.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def outcomes(runs: dict, out: Path) -> None:
    lenses = [lens for lens in LENS_COLOR if runs.get((lens, "24-40", "all"))]
    fig, axes = plt.subplots(1, len(lenses), figsize=(6.2 * len(lenses), 4.0), facecolor=SURFACE, sharex=True)
    for ax, lens in zip(np.atleast_1d(axes), lenses, strict=True):
        style_axes(ax)
        data = runs[(lens, "24-40", "all")]
        rows = [(c, null) for c in CONDITIONS for null in (False, True)]
        for y, (c, null) in enumerate(rows):
            r = data["rates"][(c, null)]
            parts = (r["flip"][0], r["kept_clean"][0], r["neither"])
            colors = (CONTROL if null else LENS_COLOR[lens], "#dddcd4", BROKEN)
            left = 0.0
            for share, color in zip(parts, colors, strict=True):
                ax.barh(y, share, left=left, color=color, height=0.75)
                left += share
        ax.set_yticks(
            range(len(rows)),
            [f"{CONDITION_LABEL[c].replace(chr(10), ' ')}" if not null else "  control" for c, null in rows],
            fontsize=8,
            color=INK,
        )
        ax.invert_yaxis()
        ax.set_xlim(0, 1)
        ax.set_title(LENS_TITLE[lens], loc="left", color=INK)
        ax.set_xlabel("share of questions", color=MUTED)
    fig.suptitle(
        "What each swap does to the answer (layers 24-40): the other entity's answer, the original kept, or neither",
        x=0.01,
        ha="left",
        color=INK,
    )
    legend_below(
        fig,
        [
            Patch(color=JLENS, label="flip (J-lens)"),
            Patch(color=JPP, label="flip (J++)"),
            Patch(color=CONTROL, label="flip (control)"),
            Patch(color="#dddcd4", label="original answer kept"),
            Patch(color=BROKEN, label="neither (collateral damage)"),
        ],
        5,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(out / "outcomes.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def dose(runs: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.6), facecolor=SURFACE)
    style_axes(ax)
    for lens in LENS_COLOR:
        data = runs.get((lens, "24-40", "all"))
        if not data:
            continue
        for c in CONDITIONS:
            for null in (False, True):
                r = data["rates"][(c, null)]
                ax.scatter(
                    r["edit_ratio_median"],
                    r["flip"][0],
                    s=48,
                    color=CONTROL if null else LENS_COLOR[lens],
                    edgecolor="none",
                    zorder=3,
                )
                if not null and not (c == "full_probe" and lens == "jpp"):  # full_probe uses no lens: one label
                    ax.annotate(
                        "full probe (both lenses)" if c == "full_probe" else CONDITION_LABEL[c].replace("\n", " "),
                        (r["edit_ratio_median"], r["flip"][0]),
                        xytext=(6, 3),
                        textcoords="offset points",
                        fontsize=7.5,
                        color=MUTED if c == "full_probe" else LENS_COLOR[lens],
                    )
    ax.set_xscale("log")
    ax.set_ylim(0, 1)
    ax.set_xlabel("edit size: median |edit| / |residual| at the last position (log)", color=MUTED)
    ax.set_ylabel("share of questions whose answer flips", color=MUTED)
    ax.set_title("Effect against edit size (layers 24-40)", loc="left", color=INK)
    ax.legend(
        handles=[
            Line2D([], [], color=JLENS, lw=0, marker="o", label="J-lens"),
            Line2D([], [], color=JPP, lw=0, marker="o", label="J++"),
            Line2D([], [], color=CONTROL, lw=0, marker="o", label="control (random direction)"),
        ],
        frameon=False,
        fontsize=8,
        loc="upper right",
    )
    fig.tight_layout()
    fig.savefig(out / "dose.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def per_question(runs: dict, out: Path) -> None:
    cols = [(lens, c) for c in CONDITIONS for lens in LENS_COLOR if runs.get((lens, "24-40", "all"))]
    base = runs[("jlens", "24-40", "all")]
    items = sorted((r for r in base["items"] if r["status"] == "eligible"), key=lambda r: (r["category"], r["name"]))
    code = {}
    for lens, c in cols:
        for o in runs[(lens, "24-40", "all")]["outcomes"]:
            if o["condition"] == c and not o["null"]:
                code[(o["name"], lens, c)] = 2 if o["flip"] else 1 if o["kept_clean"] else 0
    grid = np.array([[code[(r["name"], lens, c)] for lens, c in cols] for r in items])
    fig, ax = plt.subplots(figsize=(7.6, 0.16 * len(items) + 1.8), facecolor=SURFACE)
    ax.imshow(grid, aspect="auto", cmap=ListedColormap([BROKEN, "#dddcd4", "#3d8c5a"]), vmin=0, vmax=2)
    ax.set_xticks(
        range(len(cols)),
        [f"{CONDITION_LABEL[c].replace(chr(10), ' ')}\n{LENS_TITLE[lens]}" for lens, c in cols],
        fontsize=7,
        rotation=90,
        color=INK,
    )
    ax.set_yticks(range(len(items)), [f"{r['category']}: {r['intermediate']}" for r in items], fontsize=6, color=INK)
    for i in range(2, len(cols), 2):
        ax.axvline(i - 0.5, color=SURFACE, lw=2)
    ax.set_title(f"Every question (n={len(items)}, layers 24-40), grouped by category", loc="left", color=INK)
    ax.legend(
        handles=[
            Patch(color="#3d8c5a", label="flip"),
            Patch(color="#dddcd4", label="kept"),
            Patch(color=BROKEN, label="neither"),
        ],
        frameon=False,
        fontsize=8,
        loc="upper left",
        bbox_to_anchor=(1.0, 1.0),
    )
    fig.tight_layout()
    fig.savefig(out / "per_question.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


# ---- headline figures: one message each ---------------------------------------------------------------------------------

STEPS = ("jpart", "remainder", "remainder_clamped")
STEP_LABEL = {
    "jpart": "swap only the\nJ-space part",
    "remainder": "swap only the\nremainder",
    "remainder_clamped": "swap the remainder,\nJ-space held fixed",
}
PEOPLE = {"Darwin", "Einstein", "Lincoln", "Mozart", "Napoleon", "Newton", "Shakespeare"}
PLACES = {
    "Australia", "Brazil", "Canada", "China", "Egypt", "England", "France", "Germany", "Greece", "Hungary", "Italy",
    "Japan", "Peru", "Philadelphia", "Poland", "Russia", "Seattle", "Spain", "Sweden", "Vatican",
}  # fmt: skip
SHADE = {"cue": "#b9d3f2", "earlier": "#dbe7f6", "prev": "#e9e8e1", "last": "#fbe1d5", "never": "#f1f0ec"}


def _save(fig, out: Path, name: str) -> None:
    fig.savefig(out / name, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def jpart_vs_remainder(runs: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.8), facecolor=SURFACE)
    style_axes(ax)
    x = np.arange(len(STEPS))
    nulls = [runs[(lens, "24-40", "all")]["rates"][(c, True)]["flip"][0] for lens in LENS_COLOR for c in STEPS]
    ax.axhspan(0, max(nulls), color=GRID, zorder=0)
    ax.text(-0.9, max(nulls) + 0.012, "controls (random direction, same edit size)", fontsize=8, color=MUTED)
    lines: list[tuple[str, str, list[float], list | None]] = [("Claude (paper)", INK, [CLAUDE[c] for c in STEPS], None)]
    for lens in ("jpp", "jlens"):
        ws = [runs[(lens, "24-40", "all")]["rates"][(c, False)]["flip"] for c in STEPS]
        lines.append((LENS_TITLE[lens], LENS_COLOR[lens], [w[0] for w in ws], ws))
    for name, color, ys, ws in lines:
        if ws is None:
            ax.plot(x, ys, color=color, lw=1.6, ls=(0, (4, 2)), marker="o", ms=5, zorder=3)
        else:
            ax.fill_between(x, [w[1] for w in ws], [w[2] for w in ws], color=color, alpha=0.14, lw=0)
            ax.plot(x, ys, color=color, lw=2.6, marker="o", ms=7, zorder=4)
        ax.text(-0.08, ys[0], f"{name}  {100 * ys[0]:.0f}%", ha="right", va="center", fontsize=9.5, color=color,
                fontweight="bold")  # fmt: skip
    for i in (1, 2):  # values at the later steps, stacked so they never collide
        for k, (_, color, ys, _) in enumerate(sorted(lines, key=lambda line: -line[2][i])):
            ax.text(i + 0.09, 0.30 - 0.05 * k if i == 1 else 0.16 - 0.05 * k, f"{100 * ys[i]:.0f}%",
                    fontsize=9, color=color, fontweight="bold",
                    bbox={"facecolor": SURFACE, "edgecolor": "none", "pad": 1.5})  # fmt: skip
    ax.set_xticks(x, [STEP_LABEL[c] for c in STEPS], color=INK, fontsize=9)
    ax.set_xlim(-0.95, 2.35)
    ax.set_ylim(0, 0.75)
    ax.set_ylabel("share of questions where the answer\nswitches to the other entity's", color=MUTED)
    n = n_eligible(runs[("jlens", "24-40", "all")])
    ax.set_title(f"The bridge acts through the J-space (Qwen3.6-27B, n={n}, layers 24-40, 95% CI)", loc="left",
                 color=INK)  # fmt: skip
    fig.tight_layout()
    _save(fig, out, "jpart_vs_remainder.png")


def swap_position(runs: dict, out: Path) -> None:
    # Word-level picture of the token regimes; "Fact" is token 0 (the attention sink), never edited.
    words = ["Fact", ":", "The", "capital", "of", "the", "country", "where", "Naples", "is", "located", "is"]
    role = ["never"] + ["earlier"] * 7 + ["cue", "earlier", "prev", "last"]  # "Naples" is the cue
    fig = plt.figure(figsize=(9.4, 6.2), facecolor=SURFACE)
    strip = fig.add_axes((0.04, 0.78, 0.92, 0.12))
    strip.set_axis_off()
    pos = 0.0
    for w, r in zip(words, role, strict=True):
        width = 0.011 * len(w) + 0.035
        strip.add_patch(Rectangle((pos, 0.15), width - 0.006, 0.7, color=SHADE[r], lw=0))
        strip.text(pos + (width - 0.006) / 2, 0.5, w, ha="center", va="center", fontsize=10, color=INK)
        pos += width
    strip.text(pos + 0.01, 0.5, "→ Rome", va="center", fontsize=10, color=INK, fontweight="bold")
    strip.set_xlim(0, 1)
    strip.set_ylim(0, 1)
    fig.text(0.04, 0.955, "Where in the prompt does the bridge act? (example: Naples → Italy → Rome)", fontsize=11.5,
             color=INK)  # fmt: skip
    n = n_eligible(runs[("jlens", "24-40", "all")])
    fig.text(0.04, 0.925, f"The same J-space swap, applied only to the shaded words; layers 24-40, n={n}, 95% CI",
             fontsize=9, color=MUTED)  # fmt: skip
    rows = (("cue", "only the cue phrase: \"Naples\"", "cue"),
            ("earlier_noncue", "only the other earlier words:\n\"The capital of the country where\" ...", "earlier"),
            ("prev", "only the word before \"is\"\n(where part A reads the bridge best)", "prev"),
            ("last", "only the last word, \"is\"\n(where the answer is read)", "last"),
            ("last_two", "both of those", "prev"),
            ("all", "every position", "never"))  # fmt: skip
    ax = fig.add_axes((0.38, 0.1, 0.58, 0.62))
    style_axes(ax)
    y = np.arange(len(rows))[::-1]
    for (regime, _, shade), yi in zip(rows, y, strict=True):
        ax.axhspan(yi - 0.45, yi + 0.45, color=SHADE[shade], zorder=0, lw=0)
        for dy, lens in ((0.14, "jpp"), (-0.14, "jlens")):
            data = runs[(lens, "24-40", regime)]
            w = data["rates"][("jpart", False)]["flip"]
            ax.barh(yi + dy, w[0], height=0.26, color=LENS_COLOR[lens], zorder=2)
            ax.errorbar(w[0], yi + dy, xerr=[[w[0] - w[1]], [w[2] - w[0]]], color=INK, lw=0.8, capsize=2, zorder=3)
            ax.text(w[2] + 0.015, yi + dy, f"{100 * w[0]:.0f}%", va="center", fontsize=8.5, color=LENS_COLOR[lens])
    ax.set_yticks(y, [label for _, label, _ in rows], fontsize=9, color=INK)
    ax.set_xlim(0, 0.75)
    ax.set_xlabel("share of questions where the answer switches", color=MUTED)
    ax.legend(handles=[Patch(color=JPP, label="J++"), Patch(color=JLENS, label="J-lens")], frameon=False,
              fontsize=9, loc="lower right")  # fmt: skip
    _save(fig, out, "swap_position.png")


def examples(runs: dict, out: Path) -> None:
    names = ("amazon-language", "colosseum-currency", "ex-city-capital-Toronto-Lyon")
    data = runs[("jpp", "24-40", "all")]
    items = {r["name"]: r for r in data["items"]}
    prompts = {it["name"]: it["prompt"].strip() for it in json.loads(pins.PROBE_SWAP_FILE.read_text())["items"]}
    got = {(o["name"], o["condition"], o["null"]): o for o in data["outcomes"]}
    # (x, header, outcome key or None for the clean answer)
    cols: list[tuple[float, str, tuple[str, bool] | None]] = [
        (0.47, "no swap", None),
        (0.62, "J-space part\nswapped (J++)", ("jpart", False)),
        (0.75, "remainder\nswapped", ("remainder", False)),
        (0.88, "control:\nrandom direction", ("jpart", True)),
    ]
    fig, ax = plt.subplots(figsize=(10.4, 3.9), facecolor=SURFACE)
    ax.set_axis_off()
    ax.text(0.0, 0.95, "question (bridge → entity swapped in)", fontsize=9, color=MUTED, va="top")
    for x, head, _ in cols:
        ax.text(x, 0.95, head, fontsize=9, color=MUTED, va="top")
    for i, name in enumerate(names):
        y = 0.72 - 0.27 * i
        it = items[name]
        ax.text(0.0, y, prompts[name].removeprefix("Fact: ") + " …", fontsize=9.5, color=INK, va="center")
        ax.text(0.0, y - 0.09, f"bridge {it['intermediate']} → {it['swap_to']}", fontsize=8.5, color=MUTED, va="center")
        for x, _, key in cols:
            if key is None:
                ax.text(x, y, first_answer(it["clean_continuation"]), fontsize=10.5, color=INK, va="center")
                continue
            o = got[(name, key[0], key[1])]
            color = JPP if o["flip"] else MUTED if o["kept_clean"] else BROKEN
            ax.text(x, y, first_answer(o["continuation"]), fontsize=10.5, color=color, va="center",
                    fontweight="bold" if o["flip"] else "normal")  # fmt: skip
    flips = sum(o["flip"] for o in data["outcomes"] if o["condition"] == "jpart" and not o["null"])
    note = (
        "orange: the answer switched to the swapped-in entity's; grey: the original answer kept. Examples picked "
        f"by hand to show a flip; across all {n_eligible(data)} questions the J++ swap flips {flips}."
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 1)
    fig.suptitle("What a swap does: three questions, the model's answer before and after", x=0.01, ha="left",
                 color=INK)  # fmt: skip
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.text(0.01, 0.02, note, fontsize=8, color=MUTED)  # outside the axes, so it cannot squeeze the columns
    _save(fig, out, "examples.png")


def first_answer(text: str) -> str:
    """The continuation up to its first sentence end or line break, trimmed."""
    for stop in (".\n", "\n", ". "):
        text = text.split(stop)[0]
    return text.strip().rstrip(".")


def bridge_kind(entity: str) -> str:
    return "a country or place" if entity in PLACES else "a person" if entity in PEOPLE else "anything else"


def by_bridge_type(runs: dict, out: Path) -> None:
    kinds = ("a country or place", "a person", "anything else")
    fig, ax = plt.subplots(figsize=(8.0, 3.6), facecolor=SURFACE)
    style_axes(ax)
    y = np.arange(len(kinds))[::-1]
    examples = {"a country or place": "Brazil, Italy, Seattle", "a person": "Mozart, Newton",
                "anything else": "oxygen, kidney, owl, May"}  # fmt: skip
    for lens, dy in (("jpp", 0.14), ("jlens", -0.14)):
        data = runs[(lens, "24-40", "all")]
        flips = {o["name"]: o["flip"] for o in data["outcomes"] if o["condition"] == "jpart" and not o["null"]}
        kind_of = {r["name"]: bridge_kind(r["intermediate"]) for r in data["items"] if r["status"] == "eligible"}
        for k, yi in zip(kinds, y, strict=True):
            names = [n for n, kk in kind_of.items() if kk == k]
            w = wilson(sum(flips[n] for n in names), len(names))
            ax.barh(yi + dy, w[0], height=0.26, color=LENS_COLOR[lens])
            ax.errorbar(w[0], yi + dy, xerr=[[w[0] - w[1]], [w[2] - w[0]]], color=INK, lw=0.8, capsize=2)
            ax.text(w[2] + 0.015, yi + dy, f"{100 * w[0]:.0f}%", va="center", fontsize=8.5, color=LENS_COLOR[lens])
            if lens == "jpp":
                ax.text(-0.02, yi - 0.36, f"n={len(names)}; e.g. {examples[k]}", ha="right", fontsize=7.5,
                        color=MUTED, transform=ax.get_yaxis_transform())  # fmt: skip
    ax.set_yticks(y, [f"the bridge is {k}" for k in kinds], fontsize=9.5, color=INK)
    ax.set_xlim(0, 1)
    ax.set_xlabel("share of questions where swapping the J-space part switches the answer", color=MUTED)
    ax.legend(handles=[Patch(color=JPP, label="J++"), Patch(color=JLENS, label="J-lens")], frameon=False,
              fontsize=9, loc="lower right")  # fmt: skip
    ax.set_title("Which questions the swap works on (layers 24-40)", loc="left", color=INK)
    fig.tight_layout()
    _save(fig, out, "by_bridge_type.png")


def main(out_name: str, out_root: Path) -> None:
    out = out_root / out_name
    out.mkdir(parents=True, exist_ok=False)
    runs = {key: data for key, run in RUNS.items() if (data := load(run))}
    print("runs found:", sorted(RUNS[k] for k in runs))
    jpart_vs_remainder(runs, out)
    swap_position(runs, out)
    examples(runs, out)
    by_bridge_type(runs, out)
    lens_comparison(runs, out)
    if any(key[2] != "all" for key in runs):
        positions(runs, out)
    outcomes(runs, out)
    dose(runs, out)
    per_question(runs, out)
    (out / "sources.json").write_text(json.dumps({"runs": sorted(RUNS[k] for k in runs)}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under figures/pre-sprint/exp02_swaps/ (write-once)")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.out_root)
