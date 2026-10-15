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


def plot_run(run_dir: str | Path, summary: dict[str, Any]) -> Path:
    out = Path(run_dir) / "flip_rates.png"
    rows = summary["rates"]
    lenses = sorted({r["lens"] for r in rows}, key=lambda name: list(READER_TITLE).index(name))
    cells = list(dict.fromkeys((r["positions"], r["band"]) for r in rows))
    rate = {(r["lens"], r["positions"], r["band"], r["kind"], r["null"]): r for r in rows}
    fig, axes = plt.subplots(1, len(lenses), figsize=(6 * len(lenses), 4.4), facecolor=SURFACE, sharey=True)
    width = 0.2
    for ax, lens in zip(np.atleast_1d(axes), lenses, strict=True):
        for ci, (positions, band) in enumerate(cells):
            for ki, (kind, color) in enumerate((("bridge", BRIDGE), ("answer", ANSWER))):
                for null in (False, True):
                    r = rate.get((lens, positions, band, kind, null))
                    if r is None:
                        continue
                    x = ci + (2 * ki + null - 1.5) * width
                    m, lo, hi = r["flip"]
                    ax.bar(x, m, width * 0.9, color=CONTROL if null else color, zorder=2)
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
        Patch(color=BRIDGE, label="bridge swapped (Brazil -> Mexico)"),
        Patch(color=ANSWER, label="answer swapped (Portuguese -> Spanish)"),
        Patch(color=CONTROL, label="random direction, same edit size (right of each)"),
    ]
    finish(
        fig,
        out,
        "Does swapping the bridge, or the answer, change the model's answer, and where?",
        f"Qwen3.6-27B, up to {n} two-hop questions it answers correctly (the answer swap needs single-token answers). "
        "Each swap exchanges the two words' coordinates along their lens vectors at the given prompt positions and "
        "layers; a flip = the model's greedy continuation now has the swap target's answer and not its own. Error "
        "bars: 95% Wilson CI.",
        handles,
    )
    return out
