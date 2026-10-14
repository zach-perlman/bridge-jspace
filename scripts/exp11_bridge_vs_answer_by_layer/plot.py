"""Figures for an exp11 run, recomputed from its ranks.jsonl and items.jsonl (eligible items only).

Each call writes a new folder `<run_dir>/figures-<timestamp>/` (never overwrites).
    uv run python -m scripts.exp11_bridge_vs_answer_by_layer.plot results/exp11_bridge_vs_answer_by_layer/<stamp>
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bridge_jspace.plotting import GRID, INK, MUTED, SURFACE, style_axes

# Colour = what the word is (bridge vs answer); dashes = its same-category distractor.
ROLE_STYLE = {
    "bridge": {"color": "#2a78d6", "ls": "-", "label": "bridge (Brazil)"},
    "distractor": {"color": "#2a78d6", "ls": ":", "label": "bridge distractor (Mexico)"},
    "answer": {"color": "#eb6834", "ls": "-", "label": "answer (Portuguese)"},
    "swap_answer": {"color": "#eb6834", "ls": ":", "label": "answer distractor (Spanish)"},
}
READER_TITLE = {"logit": "logit lens", "jlens": "J-lens", "jpp": "J++"}


def _load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _figure_legend(fig, axes) -> None:
    """One legend under the panels: inside a panel it covers the curves."""
    handles, labels = np.atleast_1d(axes)[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncols=4, frameon=False, fontsize=9, labelcolor=INK)
    fig.subplots_adjust(bottom=0.22)


def plot_run(run_dir: str | Path, band: tuple[int, int] | list[int] = (32, 48)) -> Path:
    run_dir = Path(run_dir)
    eligible = {m["name"] for m in _load(run_dir / "items.jsonl") if m["status"] == "eligible"}
    rows = [r for r in _load(run_dir / "ranks.jsonl") if r["name"] in eligible]
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    out = run_dir / f"figures-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()

    # 1. Median word rank per layer (log scale, 1 at the top), IQR band for the bridge and the answer.
    fig, axes = plt.subplots(1, len(readers), figsize=(5 * len(readers), 4), facecolor=SURFACE, sharey=True)
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        rr = [r for r in rows if r["reader"] == reader]
        layers = rr[0]["layers"]
        ax.axvspan(band[0], band[1], color=GRID, alpha=0.6, lw=0, zorder=0)
        for role, st in ROLE_STYLE.items():
            m = np.array([r[f"{role}_word"] for r in rr if r[f"{role}_word"] is not None], dtype=float)
            q25, med, q75 = np.percentile(m, [25, 50, 75], axis=0)
            ax.plot(layers, med, color=st["color"], ls=st["ls"], lw=2, label=st["label"])
            if st["ls"] == "-":
                ax.fill_between(layers, q25, q75, color=st["color"], alpha=0.12, lw=0)
        ax.set_yscale("log")
        ax.invert_yaxis()
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel("layer", color=MUTED)
        style_axes(ax)
    np.atleast_1d(axes)[0].set_ylabel("median word rank (1 = top; shaded: IQR)", color=MUTED)
    _figure_legend(fig, axes)
    fig.suptitle(
        f"Last prompt token, {len(eligible)} items the model answers correctly; grey band = layers {band[0]}-{band[1]}",
        color=INK,
        fontsize=11,
        x=0.01,
        ha="left",
    )
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(out / "word_rank_by_layer.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)

    # 2. Share of items where the word is top-1 among its pool (entities or answers).
    fig, axes = plt.subplots(1, len(readers), figsize=(5 * len(readers), 3.6), facecolor=SURFACE, sharey=True)
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        rr = [r for r in rows if r["reader"] == reader]
        layers = rr[0]["layers"]
        ax.axvspan(band[0], band[1], color=GRID, alpha=0.6, lw=0, zorder=0)
        for role, st in ROLE_STYLE.items():
            pool = [r[f"{role}_pool"] for r in rr if r[f"{role}_pool"] is not None]
            share = np.mean(np.array(pool) == 1, axis=0)
            ax.plot(layers, share, color=st["color"], ls=st["ls"], lw=2, label=st["label"])
        ax.set_ylim(0, 1)
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel("layer", color=MUTED)
        style_axes(ax)
    np.atleast_1d(axes)[0].set_ylabel("share top-1 in its pool", color=MUTED)
    _figure_legend(fig, axes)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(out / "pool_top1_by_layer.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(plot_run(sys.argv[1]))
