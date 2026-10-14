"""Figures for an exp11 run, recomputed from its ranks.jsonl and items.jsonl (eligible items only).

Two figures, one panel per reader, two coloured lines each (blue = bridge, orange = answer):
  pool_top1_by_layer.png   share of items where the word is the top-1 among its pool (entities / answers);
                           the same-category distractors are thin grey lines, chance a dotted line.
  advantage_by_layer.png   how far the word ranks above its own distractor (median log10 rank ratio, IQR);
                           0 = no better than the distractor.
Called by the experiment and by `analyze`; both write into a new folder.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from bridge_jspace.plotting import GRID, INK, MUTED, SURFACE, style_axes

BRIDGE, ANSWER, CONTROL = "#2a78d6", "#eb6834", "#b4b2a9"
READER_TITLE = {"logit": "logit lens (baseline)", "jlens": "J-lens", "jpp": "J++"}
PAIRS = (("bridge", "distractor", BRIDGE), ("answer", "swap_answer", ANSWER))


def _load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _shade_bands(ax, bands: dict[str, list[int]]) -> None:
    """Widest band lightest; each labelled at the top, so it is clear which layers the summary averages."""
    for i, (name, (lo, hi)) in enumerate(sorted(bands.items(), key=lambda kv: kv[1][0] - kv[1][1])):
        ax.axvspan(lo, hi, color=GRID, alpha=0.45 + 0.25 * i, lw=0, zorder=0)
        ax.annotate(
            f"{name} {lo}-{hi}",
            (hi, 1),
            xycoords=("data", "axes fraction"),
            xytext=(-2, -2 - 10 * i),
            textcoords="offset points",
            ha="right",
            va="top",
            fontsize=7,
            color=MUTED,
        )


def _label_peak(ax, x, y, text: str, color: str) -> None:
    """Name the line where it peaks: identity without a legend lookup."""
    i = int(np.nanargmax(y))
    ax.annotate(text, (x[i], y[i]), xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                fontsize=9, color=color, fontweight="bold")  # fmt: skip


def plot_run(run_dir: str | Path, out_dir: str | Path, bands: dict[str, list[int]], chance: dict[str, float]) -> Path:
    run_dir, out = Path(run_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    eligible = {m["name"] for m in _load(run_dir / "items.jsonl") if m["status"] == "eligible"}
    rows = [r for r in _load(run_dir / "ranks.jsonl") if r["name"] in eligible]
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    title = f"Last prompt token, {len(eligible)} items the model answers correctly"

    # 1. Top-1 among its pool, per layer.
    fig, axes = plt.subplots(1, len(readers), figsize=(5 * len(readers), 3.8), facecolor=SURFACE, sharey=True)
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        rr = [r for r in rows if r["reader"] == reader]
        x = np.array(rr[0]["layers"])
        _shade_bands(ax, bands)
        for role, ctrl, color in PAIRS:
            main = [r[f"{role}_pool"] for r in rr if r[f"{role}_pool"] is not None]
            ctl = [r[f"{ctrl}_pool"] for r in rr if r[f"{ctrl}_pool"] is not None]
            if not main:
                continue
            ls = "-" if role == "bridge" else "--"
            ax.plot(x, np.mean(np.array(ctl) == 1, axis=0), color=CONTROL, lw=1, ls=ls, zorder=1)
            y = np.mean(np.array(main) == 1, axis=0)
            ax.plot(x, y, color=color, lw=2.5, zorder=2)
            _label_peak(ax, x, y, role, color)
        ax.axhline(chance["entities"], color=MUTED, lw=1, ls=":", zorder=1)
        ax.set_ylim(0, 1.08)
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel("layer", color=MUTED)
        style_axes(ax)
    np.atleast_1d(axes)[0].set_ylabel("share of items: top-1 in its pool", color=MUTED)
    handles = [
        Line2D([], [], color=BRIDGE, lw=2.5, label="bridge (e.g. Brazil) among all entities"),
        Line2D([], [], color=ANSWER, lw=2.5, label="answer (e.g. Portuguese) among all answers"),
        Line2D([], [], color=CONTROL, lw=1, label="control: same-category distractor (Mexico / Spanish)"),
        Line2D([], [], color=MUTED, lw=1, ls=":", label="chance"),
    ]
    _finish(fig, handles, f"{title}: is the word the top candidate?", out / "pool_top1_by_layer.png")

    # 2. Advantage over its own distractor in the vocabulary word rank.
    fig, axes = plt.subplots(1, len(readers), figsize=(5 * len(readers), 3.8), facecolor=SURFACE, sharey=True)
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        rr = [r for r in rows if r["reader"] == reader]
        x = np.array(rr[0]["layers"])
        _shade_bands(ax, bands)
        ax.axhline(0, color=INK, lw=0.8, zorder=1)
        for role, ctrl, color in PAIRS:
            pairs = [(r[f"{role}_word"], r[f"{ctrl}_word"]) for r in rr if r[f"{role}_word"] and r[f"{ctrl}_word"]]
            if not pairs:
                continue
            word = np.array([w for w, _ in pairs], dtype=float)
            ctl = np.array([c for _, c in pairs], dtype=float)
            q25, med, q75 = np.percentile(np.log10(ctl) - np.log10(word), [25, 50, 75], axis=0)
            ax.fill_between(x, q25, q75, color=color, alpha=0.15, lw=0)
            ax.plot(x, med, color=color, lw=2.5)
            _label_peak(ax, x, med, role, color)
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel("layer", color=MUTED)
        style_axes(ax)
    np.atleast_1d(axes)[0].set_ylabel("log10(distractor rank / word rank)", color=MUTED)
    handles = [
        Line2D([], [], color=BRIDGE, lw=2.5, label="bridge vs its distractor (Brazil vs Mexico)"),
        Line2D([], [], color=ANSWER, lw=2.5, label="answer vs its distractor (Portuguese vs Spanish)"),
    ]
    _finish(
        fig,
        handles,
        f"{title}: how far above its distractor (median, shaded IQR; 0 = no better, +1 = 10x higher)",
        out / "advantage_by_layer.png",
    )
    return out


def _finish(fig, handles, title: str, path: Path) -> None:
    fig.suptitle(title, color=INK, fontsize=11, x=0.01, ha="left")
    fig.legend(handles=handles, loc="lower center", ncols=len(handles), frameon=False, fontsize=9, labelcolor=INK)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
