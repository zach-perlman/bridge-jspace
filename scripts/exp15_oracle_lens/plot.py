"""Figures for an exp15 analysis, each answering one question in plain words. A "reading" is the oracle lens's words for
the activation at one question, prompt position and layer.

- oracle_vs_lenses.png: how often the oracle names the bridge (and the answer) where the lenses rank it 1st, where
  they do not (split by how far down the better lens has it), and the controls.
- after_swap.png: after exp14's J++ bridge swap on the cue phrase, does the oracle name the swap target, where the
  model's answer changes and where it does not?
- by_layer.png: the same two results by the layer the oracle reads."""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bridge_jspace.plotting import INK, MUTED, SURFACE, bootstrap_note, finish, percent_axis, style_axes
from bridge_jspace.stats import bootstrap_mean

BRIDGE, ANSWER, CONTROL = "#2a78d6", "#eb6834", "#b4b2a9"
BRIDGE_L, ANSWER_L = "#9cc3ef", "#f5b597"  # lighter: where the lenses miss the word
KEPT = "#6f6d66"
DASH = (0, (4, 2.5))
POSITIONS_AFTER = ("last", "prev")  # the swap test reads the last word and -1, away from the edited cue phrase


def _clustered(rows: list[dict], field: str, n_boot: int, seed: int) -> tuple[float, float, float]:
    """Mean of `field` over questions (each question's mean over its readings), bootstrap CI over questions."""
    by: dict[str, list[float]] = {}
    for r in rows:
        by.setdefault(r["name"], []).append(float(r[field]))
    if not by:
        return (np.nan, np.nan, np.nan)
    return bootstrap_mean([statistics.mean(v) for v in by.values()], n_boot, seed)


def _best_rank(r: dict, prefix: str) -> int:
    return min(r[f"{prefix}jlens_rank"], r[f"{prefix}jpp_rank"])


def _hbars(ax, rows: list[tuple[str, list[dict], str, str]], n_boot: int, seed: int) -> None:
    """Horizontal bars, top to bottom: (label, readings, field, colour); the value at the bar's end, the number of
    readings and questions under the label."""
    labels = []
    for i, (label, sub, field, color) in enumerate(rows):
        labels.append(f"{label}\n({len(sub)} readings, {len({r['name'] for r in sub})} questions)")
        m, lo, hi = _clustered(sub, field, n_boot, seed)
        if np.isnan(m):
            continue
        ax.barh(i, m, 0.7, color=color, zorder=2)
        ax.errorbar(m, i, xerr=[[max(m - lo, 0)], [max(hi - m, 0)]], color=INK, lw=1, capsize=2.5, zorder=3)
        ax.text(hi + 0.015, i, f"{m:.0%}", va="center", ha="left", fontsize=11, color=INK, fontweight="bold")
    ax.set_yticks(range(len(rows)), labels, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.08)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    style_axes(ax)
    percent_axis(ax, "x")
    ax.grid(axis="y", visible=False)


def plot_vs_lenses(path: Path, reads: list[dict], params: dict[str, Any]) -> Path:
    n_boot, seed = params["n_boot"], params["boot_seed"]
    clean = [r for r in reads if r["condition"] == "clean"]
    mean_reads = [r for r in reads if r["condition"] == "mean"]
    fig, axes = plt.subplots(1, 2, figsize=(18, 8.2), facecolor=SURFACE)
    words = [
        ("bridge", "lens_class", "", "named_bridge", "named_distractor", BRIDGE, BRIDGE_L, "Brazil", "Mexico"),
        ("answer", "answer_lens_class", "answer_", "named_answer", "named_swap_answer", ANSWER, ANSWER_L,
         "Portuguese", "Spanish"),
    ]  # fmt: skip
    for ax, (word, cls, prefix, field, d_field, dark, light, eg, d_eg) in zip(axes, words, strict=True):
        rows_cls = [r for r in clean if r.get(cls) is not None]
        neither = [r for r in rows_cls if r[cls] == "neither"]

        def far(lo: int, hi: int, neither=neither, prefix=prefix) -> list[dict]:
            return [r for r in neither if lo <= _best_rank(r, prefix) <= hi]

        bars = [
            (f"both lenses rank the {word} 1st", [r for r in rows_cls if r[cls] == "both"], field, dark),
            ("one of the two lenses ranks it 1st", [r for r in rows_cls if r[cls] == "one"], field, dark),
            ("neither lens ranks it 1st (all)", neither, field, light),
            ("   ... the better lens has it 2nd-3rd", far(2, 3), field, light),
            ("   ... 4th-10th", far(4, 10), field, light),
            ("   ... 11th or lower", far(11, 10**6), field, light),
            (f"control: the distractor ({d_eg}) named where\nneither lens ranks the {word} 1st", neither, d_field,
             CONTROL),
            (f"control: the {word} named from the mean\nactivation (no question in it)",
             [r for r in mean_reads if r.get(cls) is not None], field, CONTROL),
        ]  # fmt: skip
        _hbars(ax, bars, n_boot, seed)
        ax.set_title(f"How often does the oracle lens name the {word} (e.g. {eg})?", color=INK, fontsize=12,
                     loc="left")  # fmt: skip
        ax.set_xlabel(f"% of readings whose oracle bullets name the {word}", color=MUTED, fontsize=10)
    n = len({r["name"] for r in clean})
    n_answer = len({r["name"] for r in clean if r.get("answer_lens_class") is not None})
    finish(
        fig,
        path,
        "Where the J-lens and J++ miss the bridge, the oracle lens still names it in about a third of readings",
        f"Qwen3.6-27B, the {n} two-hop questions it answers correctly (right: the {n_answer} whose answer is a "
        "single-token word). The oracle lens is a LoRA on the model that puts one activation into words. One reading "
        "= its words for the activation at one question, prompt position and layer; positions: the last word, -1 and "
        "the cue phrase's last token (in \"...where the Amazon River ends is\": 'is', 'ends', 'River'); layers "
        f"{', '.join(map(str, params['read_layers']))}. Readings are grouped by whether the J-lens and J++ rank the "
        "word 1st among its candidates at that same question, position and layer (exp12). Each question weighted "
        f"equally; error bars: {bootstrap_note(n_boot)}.",
    )
    return path


def _swap_groups(reads: list[dict], item_rows: list[dict], layer: int) -> list[tuple[str, list[dict], str]]:
    flipped = {r["name"] for r in item_rows if r["exp14_flip"]}
    kept = {r["name"] for r in item_rows if r["exp14_flip"] is False}

    def rows(names: set[str], condition: str) -> list[dict]:
        return [r for r in reads if r["condition"] == condition and r["name"] in names and r["layer"] == layer
                and r["position"] in POSITIONS_AFTER]  # fmt: skip

    return [
        (f"before the swap\n({len(flipped)} questions whose\nanswer the swap changes)", rows(flipped, "clean"),
         BRIDGE_L),
        (f"after the swap,\nthe same {len(flipped)} questions:\nthe model's answer changed", rows(flipped, "swapped"),
         BRIDGE),
        (f"after the swap,\nthe other {len(kept)} questions:\nthe model's answer stayed", rows(kept, "swapped"), KEPT),
    ]  # fmt: skip


def plot_after_swap(path: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> Path:
    n_boot, seed, layer = params["n_boot"], params["boot_seed"], params["after_swap"]["layer"]
    fig, ax = plt.subplots(figsize=(10, 5.8), facecolor=SURFACE)
    groups = _swap_groups(reads, item_rows, layer)
    for i, (_, rows, color) in enumerate(groups):
        m, lo, hi = _clustered(rows, "named_distractor", n_boot, seed)
        ax.bar(i, m, 0.6, color=color, zorder=2)
        ax.errorbar(i, m, yerr=[[max(m - lo, 0)], [max(hi - m, 0)]], color=INK, lw=1, capsize=3, zorder=3)
        ax.text(i, hi + 0.02, f"{m:.0%}", ha="center", va="bottom", fontsize=13, color=INK, fontweight="bold")
    ax.set_xticks(range(len(groups)), [label for label, *_ in groups], fontsize=10)
    ax.set_ylim(0, 1)
    style_axes(ax)
    percent_axis(ax)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("% of questions whose oracle bullets\nname the swap target (e.g. Mexico)", color=MUTED, fontsize=10)
    finish(
        fig,
        path,
        "After the bridge swap, the oracle lens names the swap target only where the model's answer changes",
        "Qwen3.6-27B. exp14's J++ bridge swap exchanges Brazil's and Mexico's lens coordinates on the cue phrase "
        '("Amazon River ends", layers 24-40). The oracle then reads the last word and -1 (positions the swap does not '
        f"edit) at layer {layer}. If it only re-solved the question from the activation, it would keep saying Brazil. "
        f"Error bars: {bootstrap_note(n_boot)}.",
    )
    return path


def plot_by_layer(path: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> Path:
    n_boot, seed, layers = params["n_boot"], params["boot_seed"], params["read_layers"]
    clean = [r for r in reads if r["condition"] == "clean"]
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.6), facecolor=SURFACE, sharey=True)
    xs = np.array(layers)

    def line(ax, rows_at, field: str, color: str, label: str, ls: Any = "-", band: bool = False) -> None:
        stats = [_clustered(rows_at(layer), field, n_boot, seed) for layer in layers]
        ax.plot(xs, [s[0] for s in stats], ls=ls, color=color, lw=2.5, marker="o", ms=5, zorder=3, label=label)
        if band:
            ax.fill_between(xs, [s[1] for s in stats], [s[2] for s in stats], color=color, alpha=0.15, lw=0)

    def blind(layer: int) -> list[dict]:
        return [r for r in clean if r["layer"] == layer and r["lens_class"] == "neither"]

    line(axes[0], blind, "named_bridge", BRIDGE, "the bridge (e.g. Brazil)", band=True)
    line(axes[0], blind, "named_distractor", CONTROL, "its distractor (e.g. Mexico)", ls=DASH)
    axes[0].set_title("Where neither lens ranks the bridge 1st:\nhow often does the oracle name it?", color=INK,
                      fontsize=12, loc="left")  # fmt: skip

    ax = axes[1]
    ax.axvspan(24, 40, color=CONTROL, alpha=0.2, lw=0, zorder=0)
    for label, condition, flip, color in (
        ("before the swap", "clean", True, BRIDGE_L),
        ("after the swap, answer changed", "swapped", True, BRIDGE),
        ("after the swap, answer stayed", "swapped", False, KEPT),
    ):
        names = {r["name"] for r in item_rows if r["exp14_flip"] is flip}

        def at(layer: int, names=names, condition=condition) -> list[dict]:
            return [r for r in reads if r["condition"] == condition and r["name"] in names and r["layer"] == layer
                    and r["position"] in POSITIONS_AFTER]  # fmt: skip

        line(ax, at, "named_distractor", color, label, ls=DASH if condition == "clean" else "-",
             band=condition == "swapped" and flip)  # fmt: skip
    ax.set_title("After the bridge swap: how often does the oracle\nname the swap target (e.g. Mexico)?", color=INK,
                 fontsize=12, loc="left")  # fmt: skip
    for ax in axes:
        ax.legend(loc="upper left" if ax is axes[1] else "upper right", frameon=False, fontsize=9.5, handlelength=4,
                  labelcolor=INK)  # fmt: skip
        ax.set_xticks(xs, [str(layer) for layer in layers], fontsize=10)
        ax.set_xlabel("layer the oracle lens reads" + ("\n(grey: the layers the swap edits)" if ax is axes[1] else ""),
                      color=MUTED, fontsize=10)  # fmt: skip
        ax.set_ylim(0, 1)
        style_axes(ax)
        percent_axis(ax)
    axes[0].set_ylabel("% of readings whose oracle bullets name it", color=MUTED, fontsize=10)
    n = len({r["name"] for r in clean})
    finish(
        fig,
        path,
        "At which layers does the oracle lens see what the lenses miss, and follow the swap?",
        f"Qwen3.6-27B, the {n} two-hop questions it answers correctly. Left: readings at the last word, -1 and the cue "
        "phrase's last token where neither the J-lens nor J++ ranks the bridge 1st. Right: exp14's J++ bridge swap "
        "on the cue phrase (layers 24-40), oracle readings at the last word and -1. Each question weighted equally; "
        f"shading: {bootstrap_note(n_boot)}.",
    )
    return path


def plot_run(out_dir: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> list[Path]:
    return [
        plot_vs_lenses(out_dir / "oracle_vs_lenses.png", reads, params),
        plot_after_swap(out_dir / "after_swap.png", reads, item_rows, params),
        plot_by_layer(out_dir / "by_layer.png", reads, item_rows, params),
    ]


def plot_combined(out_dir: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> list[Path]:
    """Runs pooled over layers: the same figures (oracle_vs_lenses pools the layers; after_swap uses the first run's
    swap layer)."""
    return plot_run(out_dir, reads, item_rows, params)
