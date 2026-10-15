"""Figures for an exp12 run, recomputed from its saved grids (eligible items only). Writes into a new folder.

by_offset.png             one panel per reader: % of band layers with the bridge (blue) / answer (orange) ranked
                          first among its candidates, per prompt position, with 95% bootstrap CIs; distractors grey.
two_step.png              headline: where in the prompt (left, as by_offset for J-lens and J++) and how deep (right:
                          % of questions with the word ranked first per layer, bridge and answer at their best
                          positions, Wilson CIs, and the layer at which each reaches half of the questions).
layers_at_positions_jlens.png  the J-lens position x layer map as lines: % of questions with the word ranked first
                          per layer, one line per position near the end of the prompt, earlier positions pooled.
position_layer.png        reference heatmaps, readers x {bridge, answer}: the same share at every (position, layer);
                          the best position outlined over the band.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter

from bridge_jspace.plotting import (
    GRID,
    INK,
    MUTED,
    READER_TITLE,
    SURFACE,
    bootstrap_note,
    finish,
    percent_axis,
    run_note,
    style_axes,
)

BRIDGE, ANSWER, CONTROL = "#2a78d6", "#eb6834", "#b4b2a9"
# Sequential, one hue each, from the surface to a dark step of the series colour.
CMAP = {
    "bridge": LinearSegmentedColormap.from_list("bridge", [SURFACE, "#86b6ef", BRIDGE, "#104281"]),
    "answer": LinearSegmentedColormap.from_list("answer", [SURFACE, "#f5b08f", ANSWER, "#8a3112"]),
}
POSITION_AXIS = "prompt position, counted back from the last word\n(0 = last word; label: its most common token)"
SHOWN_OFFSETS = (0, -1, -2, -3)  # layers_at_positions: one line each; earlier positions are pooled
# Shades per position, darkest at the last word; identity comes from the end labels, not the shade.
SHADES = {
    "bridge": ("#104281", BRIDGE, "#5f9de6", "#93bdf0"),
    "answer": ("#8a3112", ANSWER, "#f08c5c", "#f5b08f"),
}


def _load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _offset_labels(summary: dict[str, Any]) -> list[str]:
    tokens = summary["tokens_per_offset"]
    return [f"{o}  {tokens[str(o)][0][0].strip() or '␣'!s}" for o in summary["offsets"]]


def _context(run_dir: Path, summary: dict[str, Any], chance: dict[str, float], n_items: int) -> dict[str, Any]:
    """What every figure's note and legend needs: the run's data line, pool sizes, per-position n."""
    manifest = json.loads((run_dir / "manifest.json").read_text())
    n = summary["n_per_offset"]
    first = next(iter(summary["readers"].values()))["by_offset"]
    answer_n = first.get("answer", {}).get("0", {}).get("n")
    return {
        "note": run_note(manifest, n_items),
        "n_boot": manifest["config"]["params"]["n_boot"],
        "n_ent": round(1 / chance["entities"]),
        "n_ans": round(1 / chance["answers"]),
        "n_range": f"{min(n.values())}-{max(n.values())}",
        "answer_n": answer_n,
    }


def _band_note(ctx: dict[str, Any], lo: int, hi: int) -> str:
    answer = f" Answer: the {ctx['answer_n']} questions with a single-token answer." if ctx["answer_n"] else ""
    return (
        f"{ctx['note']} Each point: the share of layers {lo}-{hi} in which the word is ranked first among its "
        f"candidates, averaged over the questions long enough to reach that position ({ctx['n_range']} per "
        f"position).{answer}"
    )


def plot_run(run_dir: str | Path, out_dir: str | Path, summary: dict[str, Any], chance: dict[str, float]) -> Path:
    from .experiment import load_grids

    run_dir, out = Path(run_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary = json.loads(json.dumps(summary, default=str))  # int offsets -> str keys, as on disk
    readers = list(summary["readers"])
    offsets = summary["offsets"]
    lo, hi = summary["band"]
    labels = _offset_labels(summary)
    meta = {m["name"]: m for m in _load(run_dir / "items.jsonl") if m["status"] == "eligible"}
    layers = json.loads((run_dir / "layers.json").read_text())
    ctx = _context(run_dir, summary, chance, len(meta))

    # 1. Band share per offset ("which position to read").
    fig, axes = plt.subplots(1, len(readers), figsize=(5.2 * len(readers), 4.6), facecolor=SURFACE, sharey=True)
    x = np.arange(len(offsets))
    for ax, reader in zip(np.atleast_1d(axes), readers, strict=True):
        res = summary["readers"][reader]
        for role, color, lw in (
            ("distractor", CONTROL, 1),
            ("swap_answer", CONTROL, 1),
            ("bridge", BRIDGE, 2.5),
            ("answer", ANSWER, 2.5),
        ):
            bo = res["by_offset"].get(role, {})
            m = np.array([bo.get(str(o), {}).get("mean", np.nan) for o in offsets])
            ls = "--" if role in ("answer", "swap_answer") else "-"
            ax.plot(x, m, color=color, lw=lw, ls=ls, marker="o" if lw > 1 else None, ms=4)
            if lw > 1:
                lo_ = np.array([bo.get(str(o), {}).get("lo", np.nan) for o in offsets])
                hi_ = np.array([bo.get(str(o), {}).get("hi", np.nan) for o in offsets])
                ax.fill_between(x, lo_, hi_, color=color, alpha=0.15, lw=0)
                opt = res["optimal"].get(role)
                if opt:
                    i = offsets.index(int(opt["offset"]))
                    above = role == "bridge"  # answer label below its point: the bridge line runs above it
                    ax.annotate(f"best for the {role}", (x[i], m[i]), xytext=(0, 8 if above else -10),
                                textcoords="offset points", ha="center", va="bottom" if above else "top", fontsize=8,
                                color=color, fontweight="bold")  # fmt: skip
        ax.axhline(chance["entities"], color=MUTED, lw=1, ls=":")
        ax.set_xticks(x, labels, rotation=60, ha="right", fontsize=8)
        ax.set_ylim(0, 1.05)
        ax.set_title(READER_TITLE.get(reader, reader), color=INK, fontsize=11, loc="left")
        ax.set_xlabel(POSITION_AXIS, color=MUTED, fontsize=9)
        style_axes(ax)
        percent_axis(ax)
    np.atleast_1d(axes)[0].set_ylabel(f"word ranked first in\n% of layers {lo}-{hi}", color=MUTED)
    handles = [
        Line2D([], [], color=BRIDGE, lw=2.5, marker="o", ms=4, label=f"bridge, ranked among {ctx['n_ent']} entities"),
        Line2D([], [], color=ANSWER, lw=2.5, ls="--", marker="o", ms=4, label=f"answer, among {ctx['n_ans']} answers"),
        Line2D([], [], color=CONTROL, lw=1, label="controls: their same-category distractors"),
        Line2D([], [], color=MUTED, lw=1, ls=":", label=f"chance (1 in {ctx['n_ent']})"),
    ]
    finish(
        fig,
        out / "by_offset.png",
        "Where in the prompt is each word readable?",
        f"{_band_note(ctx, lo, hi)} Shaded: {bootstrap_note(ctx['n_boot'])}. 'Best': the position with the highest "
        "value; picked on a random half of the questions and checked on the other half (see the summary).",
        handles,
    )

    # 2. Heatmaps position x layer, every reader.
    fig, axes = plt.subplots(len(readers), 2, figsize=(13, 3.3 * len(readers)), facecolor=SURFACE, squeeze=False)
    for r_i, reader in enumerate(readers):
        grids = load_grids(run_dir / f"grids_{reader}.npz")
        for c_i, role in enumerate(("bridge", "answer")):
            _heatmap(fig, axes[r_i][c_i], grids, summary, meta, layers[reader], labels, reader, role, ctx)
    finish(
        fig,
        out / "position_layer.png",
        "In what share of questions is the word ranked first, at each prompt position and layer?",
        f"{ctx['note']} Each cell averages over the questions long enough to reach that position. Box: the best "
        f"position, over layers {lo}-{hi} (between the dotted lines).",
    )
    _two_step(run_dir, out, summary, meta, layers, labels, ctx)
    _layers_at_positions(run_dir, out, summary, meta, layers, labels, "jlens", ctx)
    return out


def _top1(grids, meta: dict, off: int, role: str) -> np.ndarray:
    """[questions reaching `off`, layers] bool: the word ranked first among its candidates at that position."""
    return np.array([
        grids[nm][f"{role}_pool"][:, m["offsets"].index(off)] == 1
        for nm, m in meta.items()
        if off in m["offsets"] and f"{role}_pool" in grids.get(nm, {})
    ])  # fmt: skip


def _heatmap(fig, ax, grids, summary, meta, layers: list[int], labels, reader, role, ctx) -> None:
    offsets = summary["offsets"]
    lo, hi = summary["band"]
    share = np.full((len(offsets), len(layers)), np.nan)
    for o_i, off in enumerate(offsets):
        top = _top1(grids, meta, off, role)
        if top.size:
            share[o_i] = top.mean(0)
    im = ax.imshow(share, aspect="auto", cmap=CMAP[role], vmin=0, vmax=1, origin="lower",
                   extent=(layers[0] - 0.5, layers[-1] + 0.5, -0.5, len(offsets) - 0.5))  # fmt: skip
    ax.axvline(lo - 0.5, color=MUTED, lw=0.8, ls=":")
    ax.axvline(hi + 0.5, color=MUTED, lw=0.8, ls=":")
    opt = summary["readers"][reader]["optimal"].get(role)
    if opt:
        i = offsets.index(int(opt["offset"]))
        ax.add_patch(plt.Rectangle((lo - 0.5, i - 0.5), hi - lo + 1, 1, fill=False, ec=INK, lw=1.2))  # type: ignore[attr-defined]
    ax.set_yticks(range(len(offsets)), labels, fontsize=7.5)
    pool = f"ranked among {ctx['n_ent']} entities" if role == "bridge" else f"among {ctx['n_ans']} answers"
    ax.set_title(f"{READER_TITLE.get(reader, reader)}: {role}, {pool}", color=INK, fontsize=10, loc="left")
    ax.set_xlabel("model layer (0 = first)", color=MUTED, fontsize=9)
    ax.set_ylabel("prompt position\n(0 = last word)", color=MUTED, fontsize=9)
    ax.tick_params(colors=MUTED, labelsize=8)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.01, format=PercentFormatter(1.0, decimals=0))
    cb.set_label("% of questions,\nword ranked first", color=MUTED, fontsize=8)
    cb.ax.tick_params(labelsize=7, colors=MUTED)


def _share_ci(top1: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-column share of True with a Wilson 95% interval; `top1` is [items, columns] bool."""
    from bridge_jspace.stats import wilson

    k, n = top1.sum(0), top1.shape[0]
    cis = np.array([wilson(int(x), n) for x in k])
    return cis[:, 0], cis[:, 1], cis[:, 2]


def _two_step(
    run_dir: Path, out: Path, summary: dict[str, Any], meta: dict, layers: dict, labels: list[str], ctx
) -> None:
    from .experiment import load_grids

    offsets = summary["offsets"]
    lo, hi = summary["band"]
    readers = [r for r in ("jlens", "jpp") if r in summary["readers"]]
    if not readers:
        return
    fig, (ax_p, ax_d) = plt.subplots(
        1, 2, figsize=(13, 4.8), facecolor=SURFACE, gridspec_kw={"width_ratios": [1, 1.25]}
    )
    x = np.arange(len(offsets))
    ts_shown = None
    for reader in readers:
        thick = reader == "jlens"
        res = summary["readers"][reader]
        g = load_grids(run_dir / f"grids_{reader}.npz")
        for role, color in (("bridge", BRIDGE), ("answer", ANSWER)):
            bo = res["by_offset"].get(role, {})
            m = np.array([bo.get(str(o), {}).get("mean", np.nan) for o in offsets])
            ax_p.plot(x, m, color=color, lw=2.6 if thick else 1.2, alpha=1 if thick else 0.7,
                      marker="o" if thick else None, ms=4)  # fmt: skip
            if thick:
                lo_ = np.array([bo.get(str(o), {}).get("lo", np.nan) for o in offsets])
                hi_ = np.array([bo.get(str(o), {}).get("hi", np.nan) for o in offsets])
                ax_p.fill_between(x, lo_, hi_, color=color, alpha=0.15, lw=0)
        if thick:
            d = res["by_offset"].get("distractor", {})
            ax_p.plot(x, [d.get(str(o), {}).get("mean", np.nan) for o in offsets], color=CONTROL, lw=1)
        # depth: bridge at its best offset, answer at its best offset
        ts = res.get("two_step")
        if not ts:
            continue
        lay = np.array(layers[reader])
        for role, off, color in (("bridge", ts["bridge_offset"], BRIDGE), ("answer", ts["answer_offset"], ANSWER)):
            top = np.array([g[n][f"{role}_pool"][:, meta[n]["offsets"].index(int(off))] == 1
                            for n in meta if int(off) in meta[n]["offsets"] and f"{role}_pool" in g.get(n, {})])  # fmt: skip
            share, l95, h95 = _share_ci(top)
            ax_d.plot(lay, share, color=color, lw=2.6 if thick else 1.2, alpha=1 if thick else 0.7)
            if thick:
                ax_d.fill_between(lay, l95, h95, color=color, alpha=0.15, lw=0)
        if thick:
            ts_shown = ts
            c = ts["crossing"]["0.5"]
            for layer, color in ((c["bridge_layer"], BRIDGE), (c["answer_layer"], ANSWER)):
                ax_d.plot([layer], [0.5], marker="o", ms=7, color=color, mec=SURFACE, mew=1.5, zorder=5)
            lag = c.get("lag_layers", {})
            ax_d.annotate("", xy=(c["answer_layer"], 0.5), xytext=(c["bridge_layer"], 0.5),
                          arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.2})  # fmt: skip
            ax_d.annotate(
                f"answer {lag.get('median', c['answer_layer'] - c['bridge_layer']):.0f} layers later\n"
                f"(95% CI {lag.get('lo', np.nan):.0f}-{lag.get('hi', np.nan):.0f})",
                (c["bridge_layer"], 0.5), xytext=(4, -7), textcoords="offset points",  # under the arrow's start,
                ha="left", va="top", fontsize=8.5, color=INK,  # clear of the answer line rising to its end
            )  # fmt: skip
    ax_p.set_xticks(x, labels, rotation=60, ha="right", fontsize=8)
    ax_p.set_ylim(0, 1)
    ax_p.set_ylabel(f"word ranked first in\n% of layers {lo}-{hi}", color=MUTED)
    ax_p.set_xlabel(POSITION_AXIS, color=MUTED, fontsize=9)
    ax_p.set_title(f"Where in the prompt (averaged over layers {lo}-{hi})", color=INK, fontsize=11, loc="left")
    ax_d.axhline(0.5, color=MUTED, lw=0.8, ls=":")
    ax_d.annotate("half of the questions", (1, 0.5), xycoords=("axes fraction", "data"), xytext=(-2, -3),
                  textcoords="offset points", ha="right", va="top", fontsize=7.5, color=MUTED)  # fmt: skip
    ax_d.axvspan(lo, hi, color=GRID, alpha=0.7, lw=0, zorder=0)
    ax_d.set_ylim(0, 1)
    ax_d.set_xlabel("model layer (0 = first)", color=MUTED)
    ax_d.set_ylabel("% of questions with the word\nranked first among its candidates", color=MUTED)
    if ts_shown:
        ax_d.set_title(
            f"How deep: bridge read at position {ts_shown['bridge_offset']}, answer at {ts_shown['answer_offset']}",
            color=INK, fontsize=11, loc="left",
        )  # fmt: skip
    for ax in (ax_p, ax_d):
        style_axes(ax)
        percent_axis(ax)
    handles = [
        Line2D([], [], color=BRIDGE, lw=2.6, label=f"bridge, ranked among {ctx['n_ent']} entities"),
        Line2D([], [], color=ANSWER, lw=2.6, label=f"answer, among {ctx['n_ans']} answers"),
        Line2D([], [], color=INK, lw=2.6, label="thick: J-lens (shaded: 95% CI)"),
        Line2D([], [], color=INK, lw=1.2, alpha=0.7, label="thin: J++"),
        Line2D([], [], color=CONTROL, lw=1, label="control: the bridge's distractor"),
        Patch(color=GRID, label=f"layers {lo}-{hi}"),
    ]
    finish(
        fig,
        out / "two_step.png",
        "Where in the prompt, and how deep, are the bridge and the answer readable?",
        f"{_band_note(ctx, lo, hi)} Left CI: {bootstrap_note(ctx['n_boot'])}; right CI: Wilson. Dots: the first "
        "layer at which half of the questions have the word ranked first; the lag's CI is a bootstrap over questions.",
        handles,
        ncols=3,
    )


def _end_labels(ax, x: float, ends: list[tuple[float, str, str]], gap: float = 0.07) -> None:
    """Label each line at its right end, pushed apart vertically so the labels never overlap."""
    last = np.inf
    for y, text, color in sorted(ends, key=lambda e: -e[0]):
        y_lab = min(y, last - gap)
        ax.annotate(text, (x, y), xytext=(x + 1.5, y_lab), textcoords="data", va="center", fontsize=8.5,
                    color=color, arrowprops={"arrowstyle": "-", "color": color, "lw": 0.6})  # fmt: skip
        last = y_lab


def _layers_at_positions(run_dir: Path, out: Path, summary: dict, meta: dict, layers: dict, labels: list[str],
                         reader: str, ctx) -> None:  # fmt: skip
    """The heatmap's content as lines: one line per prompt position near the end (the share of questions with the
    word ranked first, by layer), the earlier positions pooled into one grey mean."""
    from bridge_jspace.stats import wilson

    from .experiment import load_grids

    if reader not in summary["readers"]:
        return
    offsets, (lo, hi) = summary["offsets"], summary["band"]
    lay = np.array(layers[reader])
    g = load_grids(run_dir / f"grids_{reader}.npz")
    name = dict(zip(offsets, labels, strict=True))
    shown = [o for o in SHOWN_OFFSETS if o in offsets]
    if not shown:
        return
    earlier = [o for o in offsets if o < min(shown)]
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), facecolor=SURFACE, sharey=True)
    for ax, role in zip(axes, ("bridge", "answer"), strict=True):
        opt = summary["readers"][reader]["optimal"].get(role)
        best = int(opt["offset"]) if opt else None
        ax.axvspan(lo, hi, color=GRID, alpha=0.7, lw=0, zorder=0)
        ax.axhline(0.5, color=MUTED, lw=0.8, ls=":")
        ends: list[tuple[float, str, str]] = []
        if earlier:
            mean = np.mean([_top1(g, meta, o, role).mean(0) for o in earlier], axis=0)
            ax.plot(lay, mean, color=CONTROL, lw=1.4)
            ends.append((mean[-1], f"{max(earlier)} to {min(earlier)}: earlier words, mean", MUTED))
        for off, shade in zip(shown, SHADES[role], strict=False):
            top = _top1(g, meta, off, role)
            if not top.size:  # no question has this word's grid (e.g. only multi-token answers in a smoke run)
                continue
            if off == best:
                ci = np.array([wilson(int(k), top.shape[0]) for k in top.sum(0)])
                ax.fill_between(lay, ci[:, 1], ci[:, 2], color=shade, alpha=0.15, lw=0)
            ax.plot(lay, top.mean(0), color=shade, lw=2.6 if off == best else 1.3, zorder=3 if off == best else 2)
            ends.append((top.mean(0)[-1], name[off] + ("  (best)" if off == best else ""), shade))
        _end_labels(ax, lay[-1], ends)
        pool = f"ranked among {ctx['n_ent']} entities" if role == "bridge" else f"among {ctx['n_ans']} answers"
        ax.set_title(f"{role}, {pool}", color=INK, fontsize=11, loc="left")
        ax.set_xlim(lay[0] - 1, lay[-1] + 17)
        ax.set_xticks(range(0, int(lay[-1]) + 1, 10))
        ax.set_ylim(0, 1)
        ax.set_xlabel("model layer (0 = first)", color=MUTED)
        style_axes(ax)
        percent_axis(ax)
    axes[0].set_ylabel("% of questions with the word\nranked first among its candidates", color=MUTED)
    handles = [
        Patch(color=GRID, label=f"layers {lo}-{hi}: the band the summaries average over"),
        Line2D([], [], color=MUTED, lw=0.8, ls=":", label="half of the questions"),
    ]
    finish(
        fig,
        out / f"layers_at_positions_{reader}.png",
        f"{READER_TITLE.get(reader, reader)}: at which layers is the word ranked first, at each of the last prompt "
        "positions?",
        f"{ctx['note']} One line per prompt position, counted back from the last word (0 = last word; label: its "
        "most common token). Thick line: the best position for that word (shaded: 95% Wilson CI). Grey: the "
        "earlier positions, averaged. Each position counts the questions long enough to reach it.",
        handles,
    )
