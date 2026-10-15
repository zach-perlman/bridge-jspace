"""Shared figure style and layout. Every part A figure has the same frame, so a reader outside the project can read it
without the code: a title that asks the figure's question, a muted note under it saying what data it is (model,
which questions, prompts) and what the shading means, percent axes that say what the percentage is of, and the
legend under the panels."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

from matplotlib.ticker import FuncFormatter, PercentFormatter

INK, MUTED, GRID, SURFACE = "#0b0b0b", "#898781", "#e1e0d9", "#fcfcfb"
AXIS = "#c3c2b7"
READER_TITLE = {"logit": "logit lens (baseline)", "jlens": "J-lens", "jpp": "J++"}


def style_axes(ax) -> None:
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=9)


def percent_axis(ax, axis: str = "y") -> None:
    """Tick labels as 0%..100% for a share stored as 0..1."""
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(PercentFormatter(1.0, decimals=0))


def times_axis(ax) -> None:
    """Tick labels for a log10 ratio: 0 -> 1x, 1 -> 10x, -1 -> 1/10x."""
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{10**v:,.0f}×" if v >= 0 else f"1/{10**-v:,.0f}×"))


def shade_band(ax, lo: int, hi: int, label: bool = True) -> None:
    """The layer band the summaries average over, labelled in words at the top of the panel."""
    ax.axvspan(lo, hi, color=GRID, alpha=0.7, lw=0, zorder=0)
    if label:
        ax.annotate(f"layers {lo}-{hi}\n(summary band)", ((lo + hi) / 2, 1), xycoords=("data", "axes fraction"),
                    xytext=(0, -3), textcoords="offset points", ha="center", va="top", fontsize=7.5, color=MUTED)  # fmt: skip


def run_note(manifest: dict[str, Any], n: int) -> str:
    """Which model and questions an exp11 / exp12 run is on, from its manifest, in words a reader outside the project
    can follow (no internal label names). Part B's v4 labels judge correctness on the greedy continuation, the
    earlier ones on the first answer word. Prompt handling is the README's shared setup; only a run that departs from
    it (prompts as published) says so."""
    cfg, p = manifest["config"], manifest["config"]["params"]
    model = cfg["model"]["name"].split("/")[-1]
    labels = Path(p.get("labels_file", "")).parent.name
    judged = "its greedy continuation contains the answer" if "v4" in labels else "its first word is the answer"
    prompts = "" if p.get("strip_trailing_space") else " Prompts as published (ending in a lone space)."
    return f"{model}, the {n} two-hop questions it answers correctly ({judged}).{prompts}"


def bootstrap_note(n_boot: int) -> str:
    return f"95% bootstrap CI over questions ({n_boot:,} resamples)"


def finish(fig, path: Path, title: str, note: str, handles=None, ncols: int | None = None) -> None:
    """Title and note above the panels, legend below them; save at 150 dpi and close."""
    import matplotlib.pyplot as plt  # here, so importing this module never picks a backend before the caller's use()

    h, w = fig.get_figheight(), fig.get_figwidth()
    note_lines = textwrap.wrap(note, width=int(w * 15.5))
    head = 0.42 + 0.17 * len(note_lines)  # inches above the panels
    foot = 0.45 if handles else 0.05
    fig.text(0.01, 1 - 0.1 / h, title, ha="left", va="top", fontsize=12, color=INK)
    fig.text(0.01, 1 - 0.36 / h, "\n".join(note_lines), ha="left", va="top", fontsize=8.5, color=MUTED, linespacing=1.4)
    if handles:
        fig.legend(handles=handles, loc="lower center", ncols=ncols or len(handles), frameon=False, fontsize=9,
                   labelcolor=INK, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.tight_layout(rect=(0, foot / h, 1, 1 - head / h))
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
