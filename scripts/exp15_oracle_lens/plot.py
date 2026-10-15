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
from matplotlib.lines import Line2D

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


LENS_GROUPS = [  # (label, test on the reading's lens class and the better lens's rank)
    ("both lenses\nrank it 1st", lambda c, rank: c == "both"),
    ("one lens\nranks it 1st", lambda c, rank: c == "one"),
    ("neither: the better\nlens has it 2nd-3rd", lambda c, rank: c == "neither" and rank <= 3),
    ("neither:\n4th-10th", lambda c, rank: c == "neither" and 4 <= rank <= 10),
    ("neither:\n11th or lower", lambda c, rank: c == "neither" and rank >= 11),
]


def _reader(params: dict[str, Any]) -> tuple[str, str]:
    """The verbalizer's full and short name: the oracle lens (exp15) or the NLA (exp16)."""
    full = params.get("reader", "oracle lens")
    return full, "oracle" if full == "oracle lens" else full


def plot_vs_lenses(path: Path, reads: list[dict], params: dict[str, Any]) -> Path:
    """One chart: how often the oracle names the word, by how well the lenses see it at that reading (left: both rank
    it 1st; right: the better lens has it 11th or lower); bridge and answer side by side; dashed: the word's
    distractor named where neither lens has the word, the oracle's false-alarm baseline."""
    n_boot, seed = params["n_boot"], params["boot_seed"]
    full, short = _reader(params)
    clean = [r for r in reads if r["condition"] == "clean"]
    words = [  # (label, lens class field, rank prefix, named field, distractor field, colour)
        ("the bridge (e.g. Brazil)", "lens_class", "", "named_bridge", "named_distractor", BRIDGE),
        ("the answer (e.g. Portuguese)", "answer_lens_class", "answer_", "named_answer", "named_swap_answer", ANSWER),
    ]
    fig, ax = plt.subplots(figsize=(13, 6.2), facecolor=SURFACE)
    width = 0.38
    bases = []
    for wi, (label, cls, prefix, field, d_field, color) in enumerate(words):
        rows = [r for r in clean if r.get(cls) is not None]
        for gi, (_, test) in enumerate(LENS_GROUPS):
            sub = [r for r in rows if test(r[cls], _best_rank(r, prefix))]
            m, lo, hi = _clustered(sub, field, n_boot, seed)
            x = gi + (wi - 0.5) * width
            ax.bar(x, m, width * 0.9, color=color, zorder=2, label=label if gi == 0 else None)
            ax.errorbar(x, m, yerr=[[max(m - lo, 0)], [max(hi - m, 0)]], color=INK, lw=1, capsize=2.5, zorder=3)
            ax.text(x, hi + 0.015, f"{m:.0%}", ha="center", va="bottom", fontsize=10.5, color=INK, fontweight="bold")
        base = _clustered([r for r in rows if r[cls] == "neither"], d_field, n_boot, seed)[0]
        ax.axhline(base, color=color, lw=1.4, ls=DASH, zorder=1)
        bases.append((base, f"{label.split(' (')[0]}'s distractor: {base:.0%}", color))
    for base, text, color in bases:  # the higher line's label above it, the lower one's below
        above = base >= max(b for b, _, _ in bases)
        ax.annotate(text, (len(LENS_GROUPS) - 0.45, base), xytext=(0, 4 if above else -4), textcoords="offset points",
                    va="bottom" if above else "top", ha="left", fontsize=9, color=color)  # fmt: skip
    ax.set_xticks(range(len(LENS_GROUPS)), [g for g, _ in LENS_GROUPS], fontsize=10)
    ax.set_xlabel("how the J-lens and J++ rank the word at that reading (left: they see it; right: they miss it)",
                  color=MUTED, fontsize=10)  # fmt: skip
    ax.set_ylabel(f"% of readings where the {full}\nnames the word", color=MUTED, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_xlim(-0.6, len(LENS_GROUPS) + 0.9)
    style_axes(ax)
    percent_axis(ax)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right", frameon=False, fontsize=10, labelcolor=INK)
    n = len({r["name"] for r in clean})
    n_answer = len({r["name"] for r in clean if r.get("answer_lens_class") is not None})
    mean_bridge = _clustered([r for r in reads if r["condition"] == "mean"], "named_bridge", n_boot, seed)[0]
    finish(
        fig,
        path,
        f"The less the lenses see the word, the less often the {full} names it, but well above its false alarms",
        f"Qwen3.6-27B, the {n} two-hop questions it answers correctly ({n_answer} with a single-token word answer for "
        f"the orange bars). One reading = the {full}'s words for the activation at one question, position (the "
        "last word, -1, the cue phrase's last token) and layer "
        f"({', '.join(map(str, params['read_layers']))}); readings grouped by how the J-lens and J++ rank the word "
        f"there (exp12). Dashed lines: how often the {short} names the word's distractor (Mexico for Brazil) where "
        f"neither lens has the word. The bridge read from the mean activation (no question): {mean_bridge:.0%}. Each "
        f"question weighted equally; error bars: {bootstrap_note(n_boot)}.",
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
    full, short = _reader(params)
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
    ax.set_ylabel(f"% of questions whose {short} words\nname the swap target (e.g. Mexico)", color=MUTED, fontsize=10)
    finish(
        fig,
        path,
        f"After the bridge swap, the {full} names the swap target only where the model's answer changes",
        "Qwen3.6-27B. exp14's J++ bridge swap exchanges Brazil's and Mexico's lens coordinates on the cue phrase "
        f'("Amazon River ends", layers 24-40). The {short} then reads the last word and -1 (positions the swap does not '
        f"edit) at layer {layer}. If it only re-solved the question from the activation, it would keep saying Brazil. "
        f"Error bars: {bootstrap_note(n_boot)}.",
    )
    return path


def plot_by_layer(path: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> Path:
    n_boot, seed, layers = params["n_boot"], params["boot_seed"], params["read_layers"]
    full, short = _reader(params)
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
    axes[0].set_title(f"Where neither lens ranks the bridge 1st:\nhow often does the {short} name it?", color=INK,
                      fontsize=12, loc="left")  # fmt: skip

    ax = axes[1]
    ax.axvspan(24, 40, color=CONTROL, alpha=0.2, lw=0, zorder=0)
    n_flip = sum(r["exp14_flip"] is True for r in item_rows)
    n_kept = sum(r["exp14_flip"] is False for r in item_rows)
    for label, condition, flip, color in (
        (f"before the swap ({n_flip} questions)", "clean", True, BRIDGE_L),
        (f"after the swap, answer changed ({n_flip} questions)", "swapped", True, BRIDGE),
        (f"after the swap, answer stayed ({n_kept} questions)", "swapped", False, KEPT),
    ):
        names = {r["name"] for r in item_rows if r["exp14_flip"] is flip}

        def at(layer: int, names=names, condition=condition) -> list[dict]:
            return [r for r in reads if r["condition"] == condition and r["name"] in names and r["layer"] == layer
                    and r["position"] in POSITIONS_AFTER]  # fmt: skip

        line(ax, at, "named_distractor", color, label, ls=DASH if condition == "clean" else "-",
             band=condition == "swapped" and flip)  # fmt: skip
    ax.set_title(f"After the bridge swap: how often does the {short}\nname the swap target (e.g. Mexico)?", color=INK,
                 fontsize=12, loc="left")  # fmt: skip
    for ax in axes:
        ax.legend(loc="upper left" if ax is axes[1] else "upper right", frameon=False, fontsize=9.5, handlelength=4,
                  labelcolor=INK)  # fmt: skip
        ax.set_xticks(xs, [str(layer) for layer in layers], fontsize=10)
        ax.set_xlabel(f"layer the {full} reads" + ("\n(grey: the layers the swap edits)" if ax is axes[1] else ""),
                      color=MUTED, fontsize=10)  # fmt: skip
        ax.set_ylim(0, 1)
        style_axes(ax)
        percent_axis(ax)
    axes[0].set_ylabel(f"% of readings whose {short} words name it", color=MUTED, fontsize=10)
    n = len({r["name"] for r in clean})
    finish(
        fig,
        path,
        f"At which layers does the {full} see what the lenses miss, and follow the swap?",
        f"Qwen3.6-27B, the {n} two-hop questions it answers correctly. Left: readings at the last word, -1 and the cue "
        "phrase's last token where neither the J-lens nor J++ ranks the bridge 1st. Right: exp14's J++ bridge swap "
        f"on the cue phrase (layers 24-40), {short} readings at the last word and -1 (two per question and layer). "
        "Each question weighted equally; "
        f"shading: {bootstrap_note(n_boot)}.",
    )
    return path


READER_COLOR = {"jlens": "#2a78d6", "jpp": "#1b9e77", "oracle": "#7b3fb5"}
READER_NAME = {
    "jlens": "J-lens (word ranked 1st)",
    "jpp": "J++ (word ranked 1st)",
    "oracle": "oracle lens (word in its text)",
}


def plot_readers(path: Path, reads: list[dict], params: dict[str, Any]) -> Path:
    """The three readers on the same readings, by layer: how often each has the word (a lens: ranks it 1st among its
    candidates; the oracle: names it), and how often each has the word's distractor instead (dashed)."""
    n_boot, seed, layers = params["n_boot"], params["boot_seed"], params["read_layers"]
    full, _ = _reader(params)
    names = {**READER_NAME, "oracle": f"{full} (word in its text)"}
    clean = [r for r in reads if r["condition"] == "clean"]
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.0), facecolor=SURFACE, sharey=True)
    xs = np.array(layers)
    words = [
        ("the bridge (e.g. Brazil)", "", "distractor_", "named_bridge", "named_distractor", "lens_class"),
        ("the answer (e.g. Portuguese)", "answer_", "swap_answer_", "named_answer", "named_swap_answer",
         "answer_lens_class"),
    ]  # fmt: skip
    for ax, (title, prefix, d_prefix, named, d_named, cls) in zip(axes, words, strict=True):
        rows = [  # per reading, 0/1 for each reader and word (copies: the readings are not changed)
            {"name": r["name"], "layer": r["layer"],
             **{f"_{lens}_word": r[f"{prefix}{lens}_rank"] == 1 for lens in ("jlens", "jpp")},
             **{f"_{lens}_distractor": r[f"{d_prefix}{lens}_rank"] == 1 for lens in ("jlens", "jpp")},
             "_oracle_word": r[named], "_oracle_distractor": r[d_named]}
            for r in clean
            if r.get(cls) is not None
        ]  # fmt: skip
        for reader in ("jlens", "jpp", "oracle"):
            color = READER_COLOR[reader]
            for kind, ls, lw in (("word", "-", 2.6 if reader == "oracle" else 2.0), ("distractor", DASH, 1.4)):
                stats = [_clustered([r for r in rows if r["layer"] == layer], f"_{reader}_{kind}", n_boot, seed)
                         for layer in layers]  # fmt: skip
                ax.plot(xs, [s[0] for s in stats], ls=ls, color=color, lw=lw, marker="o", ms=4, zorder=3)
                if kind == "word":
                    ax.fill_between(xs, [s[1] for s in stats], [s[2] for s in stats], color=color, alpha=0.1, lw=0)
        ax.set_title(f"Who has {title}?", color=INK, fontsize=12, loc="left")
        ax.set_xticks(xs, [str(layer) for layer in layers], fontsize=10)
        ax.set_xlabel("layer", color=MUTED, fontsize=10)
        ax.set_ylim(0, 1)
        style_axes(ax)
        percent_axis(ax)
    axes[0].set_ylabel("% of readings where the reader has the word", color=MUTED, fontsize=10)
    handles = [
        *(
            Line2D([], [], color=READER_COLOR[k], lw=2.4, marker="o", label=names[k])
            for k in ("jlens", "jpp", "oracle")
        ),
        Line2D(
            [], [], color=MUTED, lw=1.4, ls=DASH, marker="o", label="dashed: the same reader has the distractor instead"
        ),
    ]
    n = len({r["name"] for r in clean})
    n_answer = len({r["name"] for r in clean if r.get("answer_lens_class") is not None})
    finish(
        fig,
        path,
        f"J-lens, J++ and the {full} on the same activations: who has the bridge and the answer, at each layer?",
        f"Qwen3.6-27B, the {n} two-hop questions it answers correctly (right: the {n_answer} whose answer is a "
        "single-token word); each reader reads the same activations: the last word, -1 and the cue phrase's last "
        'token, at each layer. "Has the word": for a lens, it ranks the word 1st among its candidates (the bridge '
        f"among 97 entities, the answer among 112 answers); for the {full}, the word appears in its text. The two "
        "criteria differ, so compare each reader with its own distractor line (dashed, e.g. Mexico for Brazil). Each "
        f"question weighted equally; shading: {bootstrap_note(n_boot)}.",
        handles,
        ncols=4,
        handlelength=4,
    )
    return path


def plot_run(out_dir: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> list[Path]:
    """The figures; the by-layer ones only when the readings span several layers."""
    paths = [
        plot_vs_lenses(out_dir / "oracle_vs_lenses.png", reads, params),
        plot_after_swap(out_dir / "after_swap.png", reads, item_rows, params),
    ]
    if len(params["read_layers"]) > 1:
        paths += [
            plot_readers(out_dir / "readers_by_layer.png", reads, params),
            plot_by_layer(out_dir / "by_layer.png", reads, item_rows, params),
        ]
    return paths


def plot_combined(out_dir: Path, reads: list[dict], item_rows: list[dict], params: dict[str, Any]) -> list[Path]:
    """Runs pooled over layers: the same figures (oracle_vs_lenses pools the layers; after_swap uses the first run's
    swap layer)."""
    return plot_run(out_dir, reads, item_rows, params)
