"""Figures across exp02_swaps runs (part B), in part A's style. Reads each run's summary.json and outcomes.jsonl;
writes into a new folder (write-once).

  exp02_figures.py OUT_NAME   -> figures/exp02_swaps/OUT_NAME/
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
from matplotlib.patches import Patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.plotting import INK, MUTED, SURFACE, style_axes

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
REGIMES = ("earlier", "prev", "last", "last_two", "all")
REGIME_LABEL = {
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


def main(out_name: str, out_root: Path) -> None:
    out = out_root / out_name
    out.mkdir(parents=True, exist_ok=False)
    runs = {key: data for key, run in RUNS.items() if (data := load(run))}
    print("runs found:", sorted(RUNS[k] for k in runs))
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
    parser.add_argument("out_name", help="folder under figures/exp02_swaps/ (write-once)")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.out_root)
