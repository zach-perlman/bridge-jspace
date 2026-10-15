"""Figures for an exp15 analysis, one column per layer the oracle reads. A "reading" is one question read at one
prompt position and one layer.

- oracle_vs_lenses.png: readings grouped by whether the J-lens and J++ have the bridge (top) or the answer (bottom)
  first there; how often the oracle names the word, its distractor, and the word from the mean activation.
- after_swap.png: after exp14's J++ bridge swap on the cue phrase, how often the oracle names the swap target."""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from bridge_jspace.plotting import INK, MUTED, SURFACE, bootstrap_note, finish, percent_axis, style_axes
from bridge_jspace.stats import bootstrap_mean, wilson

BRIDGE, ANSWER, MEAN = "#2a78d6", "#eb6834", "#c9c7bf"
BRIDGE_D, ANSWER_D = "#9cc3ef", "#f5b597"  # the distractors, lighter
KEPT = "#6f6d66"  # after_swap: questions whose answer the swap keeps
CLASSES = ("both", "one", "neither")
CLASS_LABEL = {
    "both": "both lenses\nhave it first",
    "one": "one lens\nhas it first",
    "neither": "neither lens\nhas it first",
}
POSITION_LABEL = {"last": "last word", "prev": "-1", "cue_last": "cue phrase,\nlast token"}


def _clustered(rows: list[dict], field: str, n_boot: int, seed: int) -> tuple[float, float, float]:
    """Mean of `field` over questions (each question's mean over its readings), bootstrap CI over questions."""
    by: dict[str, list[float]] = {}
    for r in rows:
        by.setdefault(r["name"], []).append(float(r[field]))
    if not by:
        return (np.nan, np.nan, np.nan)
    return bootstrap_mean([statistics.mean(v) for v in by.values()], n_boot, seed)


def _bar(ax, x: float, width: float, value: tuple[float, float, float], color: str, hatch: str | None = None) -> None:
    m, lo, hi = value
    if np.isnan(m):
        return
    ax.bar(x, m, width * 0.88, color=color, hatch=hatch, edgecolor=SURFACE, lw=0, zorder=2)
    ax.errorbar(x, m, yerr=[[max(m - lo, 0.0)], [max(hi - m, 0.0)]], color=INK, lw=1, capsize=2.5, zorder=3)
    ax.annotate(f"{m:.0%}", (x, max(hi, m)), xytext=(0, 2), textcoords="offset points", ha="center", va="bottom",
                fontsize=8, color=INK)  # fmt: skip


def _frame(ax) -> None:
    ax.set_ylim(0, 1.12)
    style_axes(ax)
    percent_axis(ax)
    ax.tick_params(axis="y", labelsize=9.5)
    ax.grid(axis="x", visible=False)


def _by_class(ax, reads, mean_reads, class_field, bars, n_boot, seed) -> None:
    """One group per lens class; `bars`: (field, colour, "clean" or "mean") per bar."""
    width = 0.8 / len(bars)
    ticks = []
    for ci, c in enumerate(CLASSES):
        rows = [r for r in reads if r[class_field] == c]
        mean_rows = [r for r in mean_reads if r[class_field] == c]
        for bi, (field, color, which) in enumerate(bars):
            value = _clustered(mean_rows if which == "mean" else rows, field, n_boot, seed)
            _bar(ax, ci + (bi - (len(bars) - 1) / 2) * width, width, value, color)
        ticks.append(f"{CLASS_LABEL[c]}\n{len(rows)} readings\n{len({r['name'] for r in rows})} questions")
    ax.set_xticks(range(len(CLASSES)), ticks, fontsize=9)
    _frame(ax)


def plot_lenses(path: Path, reads: list[dict], params: dict[str, Any]) -> Path:
    n_boot, seed, layers = params["n_boot"], params["boot_seed"], params["read_layers"]
    clean = [r for r in reads if r["condition"] == "clean"]
    mean_reads = [r for r in reads if r["condition"] == "mean"]
    fig, axes = plt.subplots(2, len(layers), figsize=(6 * len(layers), 9.6), facecolor=SURFACE, sharey=True)
    rows_spec = [
        ("lens_class", "the bridge (e.g. Brazil)",
         [("named_bridge", BRIDGE, "clean"), ("named_distractor", BRIDGE_D, "clean"), ("named_bridge", MEAN, "mean")]),
        ("answer_lens_class", "the answer (e.g. Portuguese)",
         [("named_answer", ANSWER, "clean"), ("named_swap_answer", ANSWER_D, "clean"),
          ("named_answer", MEAN, "mean")]),
    ]  # fmt: skip
    for ri, (field, word, bars) in enumerate(rows_spec):
        for li, layer in enumerate(layers):
            ax = axes[ri, li]
            at = [r for r in clean if r["layer"] == layer and r.get(field) is not None]
            mean_at = [r for r in mean_reads if r["layer"] == layer and r.get(field) is not None]
            _by_class(ax, at, mean_at, field, bars, n_boot, seed)
            ax.set_title(f"Layer {layer}: {word}", color=INK, fontsize=11.5, loc="left")
        axes[ri, 0].set_ylabel("% of readings whose bullets\nname the word", color=MUTED, fontsize=10)
    handles = [
        Patch(color=BRIDGE, label="the bridge named"),
        Patch(color=BRIDGE_D, label="its distractor (e.g. Mexico) named"),
        Patch(color=MEAN, label="the same word, read from the mean activation"),
        Patch(color=ANSWER, label="the answer named"),
        Patch(color=ANSWER_D, label="its distractor (e.g. Spanish) named"),
    ]
    n = len({r["name"] for r in clean})
    n_answer = len({r["name"] for r in clean if r.get("answer_lens_class") is not None})
    other = float(np.mean([r["named_other_bridges"] for r in clean])) if clean else float("nan")
    finish(
        fig,
        path,
        "Where the J-lens and J++ miss the bridge or the answer, does the oracle lens name it?",
        f"Qwen3.6-27B, the {n} two-hop questions it answers correctly (bottom row: the {n_answer} whose answer is a "
        "single-token word; numeric answers are left out, as the oracle's numbered bullets would count as naming them). The oracle lens (a LoRA on the model that puts one activation into words, as bullets) reads each "
        "question at three prompt positions: the last word, -1 and the cue phrase's last token; one reading = one "
        "question at one position and layer, the three positions pooled in each panel. Readings are grouped by "
        "whether the J-lens and J++ rank the word first among its candidates at that question, position and layer "
        "(exp12). A word counts as named if it appears in the bullets; grey: the mean activation over questions read "
        f"instead. Another question's bridge is named in {other:.1%} of readings. {bootstrap_note(n_boot)}.",
        handles,
        ncols=5,
    )
    return path


def plot_after_swap(path: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> Path:
    layers, positions = params["read_layers"], params["after_swap"]["positions"]
    flipped = {r["name"] for r in item_rows if r["exp14_flip"]}
    kept = {r["name"] for r in item_rows if r["exp14_flip"] is False}
    groups = [(flipped, "clean", BRIDGE_D, None), (flipped, "swapped", BRIDGE, "//"), (kept, "swapped", KEPT, "//")]
    fig, axes = plt.subplots(1, len(layers), figsize=(6 * len(layers), 4.8), facecolor=SURFACE, sharey=True)
    width = 0.8 / len(groups)
    for ax, layer in zip(np.atleast_1d(axes), layers, strict=True):
        for pi, pos in enumerate(positions):
            for gi, (names, cond, color, hatch) in enumerate(groups):
                rows = [r for r in reads if r["condition"] == cond and r["name"] in names and r["position"] == pos
                        and r["layer"] == layer]  # fmt: skip
                value = wilson(sum(r["named_distractor"] for r in rows), len(rows))
                _bar(ax, pi + (gi - (len(groups) - 1) / 2) * width, width, value, color, hatch)
        ax.set_xticks(range(len(positions)), [POSITION_LABEL[p] for p in positions], fontsize=9.5)
        edited = "" if layer > 40 else " (the cue phrase is edited at this layer)"
        ax.set_title(f"Layer {layer}{edited}", color=INK, fontsize=11.5, loc="left")
        _frame(ax)
    np.atleast_1d(axes)[0].set_ylabel("% of questions whose bullets\nname the swap target", color=MUTED, fontsize=10)
    handles = [
        Patch(facecolor=BRIDGE_D, label=f"before the swap: the {len(flipped)} questions whose answer it flips"),
        Patch(facecolor=BRIDGE, hatch="//", edgecolor=SURFACE, label="after the swap, the same questions"),
        Patch(facecolor=KEPT, hatch="//", edgecolor=SURFACE, label=f"after the swap: the {len(kept)} it does not flip"),
    ]
    finish(
        fig,
        path,
        "After the bridge swap (Brazil -> Mexico), does the oracle lens name the swap target?",
        "Qwen3.6-27B. exp14's J++ bridge swap on the cue phrase (layers 24-40) flips the model's answer on some "
        "questions. If the oracle reads the state the model uses, it should name the swap target (e.g. Mexico) after "
        "the swap where the answer flips; if it re-solves the question from the activation, it should keep naming the "
        "original bridge. Read at the last word, -1 and the cue phrase's last token. Error bars: 95% Wilson CI.",
        handles,
    )
    return path


def plot_run(out_dir: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> list[Path]:
    return [
        plot_lenses(out_dir / "oracle_vs_lenses.png", reads, params),
        plot_after_swap(out_dir / "after_swap.png", reads, item_rows, params),
    ]
