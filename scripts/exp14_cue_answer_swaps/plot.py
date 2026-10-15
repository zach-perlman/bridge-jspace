"""Figure for an exp14 run, from its summary: per lens, the share of questions whose answer flips to the swap target's
when the bridge's or the answer's lens direction is swapped, in each cell (positions x layers), next to the
matched-norm random-direction nulls."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from bridge_jspace.plotting import INK, MUTED, READER_TITLE, SURFACE, finish, percent_axis, style_axes

BRIDGE, ANSWER, CONTROL = "#2a78d6", "#eb6834", "#b4b2a9"
CELL_LABEL = {"cue": "cue phrase", "last": "last token"}
# Pinned swaps (the other pair held at its clean coordinates): the same hue, darker, hatched.
KIND_STYLE = {
    "bridge": {"color": BRIDGE, "hatch": None, "label": "bridge swapped (Brazil -> Mexico)"},
    "answer": {"color": ANSWER, "hatch": None, "label": "answer swapped (Portuguese -> Spanish)"},
    "bridge_pinned": {"color": "#104281", "hatch": "//", "label": "bridge swapped, answer held"},
    "answer_pinned": {"color": "#8a3112", "hatch": "//", "label": "answer swapped, bridge held"},
}


def _kinds(rows: list[dict]) -> list[str]:
    return [k for k in KIND_STYLE if any(r["kind"] == k for r in rows)]


def plot_run(run_dir: str | Path, summary: dict[str, Any]) -> Path:
    """flip_rates.png in `run_dir` (a run, or one of its analysis folders)."""
    out = Path(run_dir) / "flip_rates.png"
    rows = summary["rates"]
    lenses = sorted({r["lens"] for r in rows}, key=lambda name: list(READER_TITLE).index(name))
    cells = list(dict.fromkeys((r["positions"], r["band"]) for r in rows))
    rate = {(r["lens"], r["positions"], r["band"], r["kind"], r["null"]): r for r in rows}
    fig, axes = plt.subplots(1, len(lenses), figsize=(6 * len(lenses), 4.4), facecolor=SURFACE, sharey=True)
    kinds = _kinds(rows)
    width = 0.8 / (2 * len(kinds))
    for ax, lens in zip(np.atleast_1d(axes), lenses, strict=True):
        for ci, (positions, band) in enumerate(cells):
            for ki, kind in enumerate(kinds):
                style = KIND_STYLE[kind]
                for null in (False, True):
                    r = rate.get((lens, positions, band, kind, null))
                    if r is None:
                        continue
                    x = ci + (2 * ki + null - (2 * len(kinds) - 1) / 2) * width
                    m, lo, hi = r["flip"]
                    ax.bar(x, m, width * 0.9, color=CONTROL if null else style["color"],
                           hatch=None if null else style["hatch"], edgecolor=SURFACE, lw=0, zorder=2)  # fmt: skip
                    err = [[max(m - lo, 0.0)], [max(hi - m, 0.0)]]  # Wilson at 0 flips: float noise below 0
                    ax.errorbar(x, m, yerr=err, color=INK, lw=1, capsize=2.5, zorder=3)
        ax.set_xticks(range(len(cells)), [f"{CELL_LABEL.get(p, p)}\nlayers {b}" for p, b in cells], fontsize=9)
        ax.set_ylim(0, 1)
        ax.set_title(READER_TITLE.get(lens, lens), color=INK, fontsize=11, loc="left")
        style_axes(ax)
        percent_axis(ax)
        ax.grid(axis="x", visible=False)
    np.atleast_1d(axes)[0].set_ylabel("% of questions whose answer\nflips to the swap target's", color=MUTED)
    n = max(r["n"] for r in rows)
    handles = [
        Patch(
            facecolor=KIND_STYLE[k]["color"],
            hatch=KIND_STYLE[k]["hatch"],
            edgecolor=SURFACE,
            label=KIND_STYLE[k]["label"],
        )
        for k in kinds
    ]
    handles.append(Patch(color=CONTROL, label="random direction, same edit size (right of each)"))
    finish(
        fig,
        out,
        "With the other pair held, does the bridge swap or the answer swap still change the answer?"
        if any(k in kinds for k in ("bridge_pinned", "answer_pinned"))
        else "Does swapping the bridge, or the answer, change the model's answer, and where?",
        f"Qwen3.6-27B, up to {n} two-hop questions it answers correctly (the answer swap needs single-token answers). "
        "Each swap exchanges the two words' coordinates along their lens vectors at the given prompt positions and "
        "layers; a flip = the model's greedy continuation now has the swap target's answer and not its own. Error "
        "bars: 95% Wilson CI.",
        handles,
        ncols=3 if len(handles) > 4 else None,  # the pinned run's five entries in two rows
    )
    return out


def plot_overlap(path: Path, rows: list[dict], post_hoc: bool = False) -> Path:
    """Per lens: flip rates of the two swaps on the cue phrase and at the last token (40-56), for the questions whose
    two swaps overlap little (below the median cosine) and much."""
    cells = [("cue", "24-40"), ("last", "40-56")]
    lenses = sorted({r["lens"] for r in rows}, key=lambda name: list(READER_TITLE).index(name))
    rate = {(r["lens"], r["positions"], r["band"], r["overlap"], r["kind"]): r for r in rows}
    fig, axes = plt.subplots(1, len(lenses), figsize=(6 * len(lenses), 4.6), facecolor=SURFACE, sharey=True)
    kinds = _kinds(rows)
    width = 0.8 / len(kinds)
    first = rows[0]
    n_total = sum(r["n"] for r in rows if (r["lens"], r["positions"], r["band"], r["kind"]) ==
                  (first["lens"], first["positions"], first["band"], first["kind"]))  # fmt: skip
    for ax, lens in zip(np.atleast_1d(axes), lenses, strict=True):
        ticks = []
        for ci, ((positions, band), half) in enumerate((c, h) for c in cells for h in ("low", "high")):
            n = 0
            for ki, kind in enumerate(kinds):
                style = KIND_STYLE[kind]
                r = rate.get((lens, positions, band, half, kind))
                if r is None:
                    continue
                n = max(n, r["n"])
                m, lo, hi = r["flip"]
                x = ci + (ki - (len(kinds) - 1) / 2) * width
                ax.bar(x, m, width * 0.9, color=style["color"], hatch=style["hatch"], edgecolor=SURFACE, lw=0, zorder=2)
                ax.errorbar(x, m, yerr=[[max(m - lo, 0.0)], [max(hi - m, 0.0)]], color=INK, lw=1, capsize=2.5, zorder=3)
            ticks.append(f"{CELL_LABEL.get(positions, positions)}\n{band}, {half}\nn = {n}")
        ax.set_xticks(range(len(ticks)), ticks, fontsize=8.5)
        ax.set_xlabel(
            "where and at which layers the swap edits; overlap between the two swaps", color=MUTED, fontsize=9
        )
        ax.set_ylim(0, 1)
        ax.set_title(READER_TITLE.get(lens, lens), color=INK, fontsize=11, loc="left")
        style_axes(ax)
        percent_axis(ax)
        ax.grid(axis="x", visible=False)
    np.atleast_1d(axes)[0].set_ylabel("% of questions whose answer\nflips to the swap target's", color=MUTED)
    handles = [
        Patch(
            facecolor=KIND_STYLE[k]["color"],
            hatch=KIND_STYLE[k]["hatch"],
            edgecolor=SURFACE,
            label=KIND_STYLE[k]["label"],
        )
        for k in kinds
    ]
    finish(
        fig,
        path,
        "Does swapping the answer change it only where that swap is also a bridge swap?",
        f"Qwen3.6-27B, the {n_total} two-hop questions it answers correctly where both swaps are possible (single-token "
        "answers), split in two halves at the median overlap between the two swaps: "
        "the cosine between the bridge pair's and the answer pair's lens-vector differences (e.g. high for "
        "Spain -> Madrid, low for elephant -> trunk), averaged over the swapped layers. Random-direction controls: 0-1% "
        "everywhere. Error bars: 95% Wilson CI."
        + (" The split was chosen after seeing the results." if post_hoc else " The split was fixed before the run."),
        handles,
    )
    return path
