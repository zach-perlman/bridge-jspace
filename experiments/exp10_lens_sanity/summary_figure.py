"""Cross-run summary figures for exp10, recomputed from the runs' summary.json and multihop_ranks.jsonl.

Writes a new folder figures/exp10_lens_sanity/<timestamp>/ (never overwrites).
    uv run python -m experiments.exp10_lens_sanity.summary_figure
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bridge_jspace.pins import FIGURES_DIR, RESULTS_DIR

from .plot import GRID, HIT_K, INK, MUTED, STYLE, SURFACE, _style_axes

RUNS_DIR = RESULTS_DIR / "exp10_lens_sanity"
# (label, run id): the four valid runs; 204427/204551 predate the token fix and are superseded.
RUNS = [
    ("Qwen3.5-4B\nprompt as published", "20261013-205029"),
    ("Qwen3.5-4B\nspace stripped", "20261013-205057"),
    ("Qwen3.6-27B\nprompt as published", "20261013-205736"),
    ("Qwen3.6-27B\nspace stripped", "20261013-205936"),
]
LAYER_RUN = "20261013-205936"  # 27B, stripped
READERS = ["logit", "jlens", "jpp"]
SUBSET = "all_single_token"


def _bars(ax) -> None:
    width = 0.26
    for gi, (_, run) in enumerate(RUNS):
        summary = json.loads((RUNS_DIR / run / "summary.json").read_text())
        pk = summary["pass_at_k"][SUBSET]
        for ri, reader in enumerate(READERS):
            if reader not in pk:
                continue  # Qwen3.5-4B has no J++ lens
            v = pk[reader]["10"]
            x = gi + (ri - 1) * width
            st = STYLE[reader]
            ax.bar(x, v["mean"], width * 0.92, color=st["color"], label=st["label"] if gi == 3 else None, zorder=2)
            ax.errorbar(
                x, v["mean"], yerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]], color=INK, lw=1, capsize=3, zorder=3
            )
    ax.set_xticks(range(len(RUNS)), [label for label, _ in RUNS], fontsize=9, color=INK)
    ax.set_ylim(0, 1)
    ax.set_ylabel(f"pass@{HIT_K}: bridge in the reader's top {HIT_K}", color=MUTED)
    ax.set_title(
        f"How often each reader sees the bridge at the last prompt token (n={pk['n']}, 95% CI)",
        color=INK,
        fontsize=11,
        loc="left",
    )
    _style_axes(ax)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK, ncols=3)


def _layers(ax) -> None:
    rows = [
        json.loads(line)
        for line in (RUNS_DIR / LAYER_RUN / "multihop_ranks.jsonl").read_text().splitlines()
        if line.strip()
    ]
    for reader in READERS:
        rr = [r for r in rows if r["reader"] == reader and r["single_token"]]
        hits = np.mean([np.array(r["ranks"]) < HIT_K for r in rr], axis=0)
        st = STYLE[reader]
        ax.plot(rr[0]["layers"], hits, color=st["color"], ls=st["ls"], lw=2, label=st["label"])
    ax.axvspan(35, 52, color=GRID, alpha=0.6, zorder=0, lw=0)
    ax.annotate("J-lens / J++ read the bridge,\nlogit lens does not", (43.5, 0.42), ha="center", fontsize=9, color=INK)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel("layer", color=MUTED)
    ax.set_ylabel(f"share of bridges in top {HIT_K}", color=MUTED)
    ax.set_title("Qwen3.6-27B, by layer (space stripped)", color=INK, fontsize=11, loc="left")
    _style_axes(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK)


def main() -> Path:
    out = FIGURES_DIR / "exp10_lens_sanity" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    for name, draw, size in (("pass_at_10_by_model.png", _bars, (9, 4)), ("27b_by_layer.png", _layers, (8, 3.6))):
        fig, ax = plt.subplots(figsize=size, facecolor=SURFACE)
        draw(ax)
        fig.tight_layout()
        fig.savefig(out / name, dpi=150, facecolor=SURFACE)
        plt.close(fig)
    return out


if __name__ == "__main__":
    print(main())
