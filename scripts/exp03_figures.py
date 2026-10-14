"""Figures for exp03_brew_swaps (part B), in part A's style, from follow-up runs' outcomes.

  exp03_figures.py OUT_NAME RUN [RUN ...]  -> figures/exp03_brew_swaps/OUT_NAME/ (write-once)
      steering_start_line.png   steering the start line along S' - S, by size: which colour the model answers, read
                                off the table: two lookups from S' (f(f(S'))), one lookup (f(S')), S' itself, the
                                original answer, or none of these; random-direction nulls
      steering_after_start.png  steering the positions after the start colour along X - I: one lookup from X (f(X),
                                the intermediate used as a step), X itself (a candidate answer), the original answer

Every steering scale and band in the runs is drawn; runs are merged (e.g. start_steer and start_steer_low).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.plotting import INK, MUTED, SURFACE, style_axes

EXP = "exp03_brew_swaps"
CONTROL = "#b4b2a9"
CATEGORIES = {  # kind -> [(category, colour, label)]
    "steer_start": [
        ("two", "#3d8c5a", "f(f(S')): both lookups from the new start"),
        ("one", "#9cc9a8", "f(S'): one lookup from the new start (when not the original answer)"),
        ("said", "#8a3db8", "S' itself"),
        ("kept", MUTED, "the original answer"),
    ],
    "steer": [
        ("one", "#3d8c5a", "f(X): the intermediate used as a step"),
        ("said", "#8a3db8", "X itself: a candidate answer"),
        ("kept", MUTED, "the original answer"),
    ],
}
FILES = {
    "steer_start": ("steering_start_line.png", "Steer the start line toward another start colour S'"),
    "steer": ("steering_after_start.png", "Steer the positions after the start colour toward another colour X"),
}
BAND_NOTE = {"36-52": " (the J-lens reads the intermediate here)"}


def category(o: dict, item: dict, table: dict) -> str:
    """Where the answer sits relative to the swapped-in colour's chain in the table. An unchanged answer is always
    "kept", even where one lookup from the new colour lands on it (about 1 in 6 start_steer items)."""
    colour, kind = o["colour"], o["kind"]
    new = item["start_swap"] if kind == "steer_start" else item["swap_to"]
    one = table[new]["stir"]
    if kind == "steer_start" and one in table and colour == table[one]["stir"]:
        return "two"
    if colour == item["answer"]:
        return "kept"
    if colour == one:
        return "one"
    if colour == new:
        return "said"
    return "none" if colour is None else "other"


def load(runs: list[str]) -> dict:
    """Shares per (kind, band, lens, null, scale, category), with n, from the runs' outcomes."""
    bank = {it["name"]: it for it in pins.brew_items()}
    counts: dict[tuple, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for run in runs:
        run_dir = pins.RESULTS_DIR / EXP / run
        items = {r["name"]: r for r in map(json.loads, (run_dir / "items.jsonl").read_text().splitlines())}
        for o in map(json.loads, (run_dir / "outcomes.jsonl").read_text().splitlines()):
            if o["kind"] not in CATEGORIES:
                continue
            key = (o["kind"], o["band"], o["lens"], o["null"], o["scale"])
            counts[key][category(o, items[o["name"]], bank[o["name"]]["table"])] += 1
            counts[key]["n"] += 1
    return counts


def steering(counts: dict, kind: str, out: Path) -> None:
    file, title = FILES[kind]
    keys = [k for k in counts if k[0] == kind]
    bands = sorted({k[1] for k in keys}, key=lambda b: int(b.split("-")[0]))
    n = max(counts[k]["n"] for k in keys)
    fig, axes = plt.subplots(1, len(bands), figsize=(5.0 * len(bands), 4.3), facecolor=SURFACE, sharey=True)
    for ax, band in zip(np.atleast_1d(axes), bands, strict=True):
        style_axes(ax)
        for lens, ls in (("jpp", "-"), ("jlens", (0, (3, 2)))):
            real = sorted((k for k in keys if k[1] == band and k[2] == lens and not k[3]), key=lambda k: k[4])
            xs = [100 * k[4] for k in real]
            for cat, color, _ in CATEGORIES[kind]:
                ys = [counts[k][cat] / counts[k]["n"] for k in real]
                ax.plot(xs, ys, color=color, ls=ls, lw=2.2 if lens == "jpp" else 1.4, marker="o", ms=4)
            for k in keys:
                if k[1] == band and k[2] == lens and k[3]:
                    ax.plot(100 * k[4], 1 - counts[k]["kept"] / counts[k]["n"], color=CONTROL, marker="s", ms=6, lw=0)
        ax.set_xscale("log")
        ax.minorticks_off()
        ticks = sorted({100 * k[4] for k in keys})
        ax.set_xticks(ticks, [f"{t:g}%" for t in ticks])
        ax.set_ylim(-0.02, 1.02)
        ax.set_xlabel("steering size, share of the residual norm", color=MUTED)
        ax.set_title(f"layers {band}{BAND_NOTE.get(band, '')}", loc="left", color=INK, fontsize=10)
    np.atleast_1d(axes)[0].set_ylabel("share of questions", color=MUTED)
    fig.suptitle(f"{title} (brew, Qwen3.6-27B, n={n}): which colour does the model answer?", x=0.01, ha="left",
                 color=INK)  # fmt: skip
    handles = [Line2D([], [], color=color, lw=2, label=label) for _, color, label in CATEGORIES[kind]]
    handles += [
        Line2D([], [], color=CONTROL, marker="s", lw=0, label="random direction: answer changed"),
        Line2D([], [], color=INK, lw=2, label="J++ (solid) / J-lens (dashed)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.13, 1, 0.94))
    fig.savefig(out / file, dpi=170, facecolor=SURFACE)
    plt.close(fig)


def main(out_name: str, runs: list[str], out_root: Path) -> None:
    out = out_root / out_name
    out.mkdir(parents=True, exist_ok=False)
    counts = load(runs)
    for kind in CATEGORIES:
        if any(k[0] == kind for k in counts):
            steering(counts, kind, out)
    (out / "sources.json").write_text(json.dumps({"runs": runs}, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out_name", help="folder under figures/exp03_brew_swaps/ (write-once)")
    parser.add_argument("runs", nargs="+", help="exp03 follow-up runs")
    parser.add_argument("--out-root", type=Path, default=pins.FIGURES_DIR / EXP, help="for test renders")
    args = parser.parse_args()
    main(args.out_name, args.runs, args.out_root)
