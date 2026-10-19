"""Figure for a suite_split parts run: how far each piece of the copy moves the answer, and the J-space part's
concentration (its effect over what its size predicts).  python scripts/suite_split_figure.py PARTS_RUN [PARTS_RUN ...]
Writes figures/suite_split/<run>.png (one row per run)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bridge_jspace import pins

RESULTS = pins.RESULTS_DIR / "suite_split"
OUT = pins.FIGURES_DIR / "suite_split"
ORDER = ("BL", "BR", "RL", "RR", "BLR", "BRL", "NAMES", "CODE")
BARS = (  # (key in the summary's means, label, colour): the reference palette's first four slots, in order
    ("full", "full copy", "#2a78d6"),
    ("not_jspace", "rest of the copy", "#eb6834"),
    ("jspace", "J-space part", "#1baf7a"),
    ("jspace_matched", "equal-sized piece of the copy", "#eda100"),
)
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def main(runs: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(len(runs), 2, figsize=(13, 3.6 * len(runs)), squeeze=False,
                             gridspec_kw={"width_ratios": [2.2, 1]})  # fmt: skip
    for row, run in enumerate(runs):
        s = json.loads((RESULTS / run / "summary.json").read_text())
        fams = [f for f in ORDER if isinstance(s["families"].get(f, {}).get("frac"), dict)]
        ax = axes[row][0]
        width = 0.2
        for i, (key, label, colour) in enumerate(BARS):
            vals = [100 * s["families"][f]["frac"]["means"][key] for f in fams]
            xs = [k + (i - 1.5) * (width + 0.02) for k in range(len(fams))]
            ax.bar(xs, vals, width, color=colour, label=label, zorder=2)
        top = max(100 * s["families"][f]["frac"]["means"]["full"] for f in fams)
        ax.set_ylim(top=top * 1.3)
        ax.set_xticks(range(len(fams)), [f"{f}\nn={s['families'][f]['n']}" for f in fams], color=INK)
        ax.set_ylabel("answer moved toward C (%)", color=MUTED)
        ax.set_title(f"{run}: each piece of the copy, patched alone at the window", loc="left", color=INK, fontsize=11)
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.grid(axis="y", color=GRID, zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
        if row == 0:
            ax.legend(frameon=False, fontsize=9, ncol=4, loc="upper left")
        ax2 = axes[row][1]
        conc = [s["families"][f]["frac"]["jspace"]["concentration"] for f in fams]
        ys = range(len(fams))[::-1]
        for y, (c, lo, hi) in zip(ys, conc, strict=True):
            ax2.plot([lo, hi], [y, y], color="#2a78d6", lw=2, solid_capstyle="round", zorder=2)
            ax2.plot([c], [y], "o", color="#2a78d6", ms=8, zorder=3)
        ax2.axvline(1, color=MUTED, ls="--", lw=1)
        ax2.axvline(2, color=INK, ls=":", lw=1)
        tr = ax2.get_xaxis_transform()
        ax2.text(1, 1.01, "its size", color=MUTED, fontsize=8, va="bottom", ha="center", transform=tr)
        ax2.text(2, 1.01, "inside if above", color=INK, fontsize=8, va="bottom", ha="center", transform=tr)
        verdicts = [s["families"][f]["frac"]["jspace"]["verdict"] for f in fams]
        ax2.set_yticks(list(ys), [f"{f} ({v})" for f, v in zip(fams, verdicts, strict=True)], color=INK)
        ax2.set_xlabel("J-space part: effect / effect its size predicts (95% CI)", color=MUTED)
        ax2.set_xlim(left=0)
        ax2.grid(axis="x", color=GRID, zorder=0)
        ax2.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    path = OUT / f"{'_'.join(runs)}.png"
    fig.savefig(path, dpi=150)
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1:])
