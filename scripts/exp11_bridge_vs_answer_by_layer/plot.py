"""Figures for an exp11 run, recomputed from its ranks.jsonl and items.jsonl (eligible items only).

Two figures, one panel per reader, two coloured lines each (blue = bridge, orange = answer):
  pool_top1_by_layer.png   % of questions where the word is ranked first among its candidates (bridge among all
                           entities, answer among all answers), with 95% Wilson CIs; distractors grey, chance dotted.
  advantage_by_layer.png   how many times higher than its own same-category distractor the word ranks in the full
                           vocabulary (median question, middle half shaded); 1x = no better than the distractor.
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
from matplotlib.patches import Patch

from bridge_jspace.plotting import (
    GRID,
    INK,
    MUTED,
    READER_TITLE,
    SURFACE,
    finish,
    percent_axis,
    run_note,
    shade_band,
    style_axes,
    times_axis,
)
from bridge_jspace.stats import wilson

BRIDGE, ANSWER, CONTROL = "#2a78d6", "#eb6834", "#b4b2a9"
PAIRS = (("bridge", "distractor", BRIDGE), ("answer", "swap_answer", ANSWER))


def _load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _label_peak(ax, x, y, text: str, color: str, placed: list[tuple[float, float]]) -> None:
    """Name the line where it peaks: identity without a legend lookup. Bridge and answer often top out together
    near the last layers, so a peak close to an already labelled one gets its label stacked above that label."""
    i = int(np.nanargmax(y))
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    near = [py for px, py in placed if abs(x[i] - px) < 0.08 * (x1 - x0) and abs(y[i] - py) < 0.12 * (y1 - y0)]
    placed.append((x[i], y[i]))
    top = max([y[i], *near])  # stack from the higher peak, so the labels clear each other
    ax.annotate(text, (x[i], top), xytext=(0, 6 + 12 * len(near)), textcoords="offset points", ha="center",
                va="bottom", fontsize=9, color=color, fontweight="bold")  # fmt: skip


def plot_run(run_dir: str | Path, out_dir: str | Path, bands: dict[str, list[int]], chance: dict[str, float]) -> Path:
    run_dir, out = Path(run_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    eligible = {m["name"] for m in _load(run_dir / "items.jsonl") if m["status"] == "eligible"}
    rows = [r for r in _load(run_dir / "ranks.jsonl") if r["name"] in eligible]
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    note = run_note(json.loads((run_dir / "manifest.json").read_text()), len(eligible))
    lo, hi = next(iter(bands.values()))  # the primary band (config order); the others are exploratory
    n_ent, n_ans = round(1 / chance["entities"]), round(1 / chance["answers"])
    n_answer = sum(1 for r in rows if r["reader"] == readers[0] and r["answer_pool"] is not None)

    # 1. Ranked first among its candidates, per layer.
    fig, axes = plt.subplots(1, len(readers), figsize=(5 * len(readers), 4), facecolor=SURFACE, sharey=True)
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        rr = [r for r in rows if r["reader"] == reader]
        x = np.array(rr[0]["layers"])
        shade_band(ax, lo, hi)
        placed: list[tuple[float, float]] = []
        for role, ctrl, color in PAIRS:
            main = np.array([r[f"{role}_pool"] for r in rr if r[f"{role}_pool"] is not None]) == 1
            ctl = np.array([r[f"{ctrl}_pool"] for r in rr if r[f"{ctrl}_pool"] is not None]) == 1
            if not main.size:
                continue
            ls = "-" if role == "bridge" else "--"
            ax.plot(x, ctl.mean(0), color=CONTROL, lw=1, ls=ls, zorder=1)
            ci = np.array([wilson(int(k), main.shape[0]) for k in main.sum(0)])
            ax.fill_between(x, ci[:, 1], ci[:, 2], color=color, alpha=0.15, lw=0, zorder=1)
            ax.plot(x, main.mean(0), color=color, lw=2.5, zorder=2)
            _label_peak(ax, x, main.mean(0), role, color, placed)
        ax.axhline(chance["entities"], color=MUTED, lw=1, ls=":", zorder=1)
        ax.set_ylim(0, 1.08)
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel("model layer (0 = first)", color=MUTED)
        style_axes(ax)
        percent_axis(ax)
    np.atleast_1d(axes)[0].set_ylabel("% of questions with the word\nranked first among its candidates", color=MUTED)
    handles = [
        Line2D([], [], color=BRIDGE, lw=2.5, label=f"bridge (e.g. Brazil), ranked among all {n_ent} entities"),
        Line2D([], [], color=ANSWER, lw=2.5, ls="-", label=f"answer (e.g. Portuguese), among all {n_ans} answers"),
        Line2D([], [], color=CONTROL, lw=1, label="control: same-category distractor (Mexico / Spanish)"),
        Line2D([], [], color=MUTED, lw=1, ls=":", label=f"chance (1 in {n_ent})"),
        Patch(color=GRID, label=f"layers {lo}-{hi}: averaged in the summary"),
    ]
    finish(
        fig,
        out / "pool_top1_by_layer.png",
        "At the last prompt token, at which layers does each reader rank the bridge, and the answer, first?",
        f"{note} Read at the last prompt token. Answer lines: the {n_answer} questions with a single-token answer. "
        "Shaded: 95% Wilson CI.",
        handles,
        ncols=3,
    )

    # 2. Advantage over its own distractor in the vocabulary word rank.
    fig, axes = plt.subplots(1, len(readers), figsize=(5 * len(readers), 4), facecolor=SURFACE, sharey=True)
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        rr = [r for r in rows if r["reader"] == reader]
        x = np.array(rr[0]["layers"])
        shade_band(ax, lo, hi)
        ax.axhline(0, color=INK, lw=0.8, zorder=1)
        placed = []
        for role, ctrl, color in PAIRS:
            pairs = [(r[f"{role}_word"], r[f"{ctrl}_word"]) for r in rr if r[f"{role}_word"] and r[f"{ctrl}_word"]]
            if not pairs:
                continue
            word = np.array([w for w, _ in pairs], dtype=float)
            ctl = np.array([c for _, c in pairs], dtype=float)
            q25, med, q75 = np.percentile(np.log10(ctl) - np.log10(word), [25, 50, 75], axis=0)
            ax.fill_between(x, q25, q75, color=color, alpha=0.15, lw=0)
            ax.plot(x, med, color=color, lw=2.5)
            _label_peak(ax, x, med, role, color, placed)
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel("model layer (0 = first)", color=MUTED)
        style_axes(ax)
        times_axis(ax)
    np.atleast_1d(axes)[0].set_ylabel("times higher than its distractor\n(log scale)", color=MUTED)
    handles = [
        Line2D([], [], color=BRIDGE, lw=2.5, label="bridge vs its distractor (Brazil vs Mexico)"),
        Line2D([], [], color=ANSWER, lw=2.5, label="answer vs its distractor (Portuguese vs Spanish)"),
        Line2D([], [], color=INK, lw=0.8, label="1× = no better than the distractor"),
        Patch(color=GRID, label=f"layers {lo}-{hi}: averaged in the summary"),
    ]
    finish(
        fig,
        out / "advantage_by_layer.png",
        "At the last prompt token, how much higher than its same-category distractor does each reader rank the word?",
        f"{note} Ratio = the distractor's rank / the word's rank in the reader's full vocabulary ranking (10× = "
        "ten times closer to the top). Line: the median question; shaded: the middle half of the questions.",
        handles,
    )
    return out
