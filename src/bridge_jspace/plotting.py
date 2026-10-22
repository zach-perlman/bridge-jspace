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
# Plain names for the families in every figure, table and report (Dan, 2026-10-21: the letter codes are hard to read):
# "where the bridge comes from -> where the answer comes from". prompt = stated in the prompt, memory = recalled.
FAMILY_LABEL = {
    "BL": "prompt → prompt",
    "BR": "prompt → memory",
    "RL": "memory → prompt",
    "RR": "memory → memory",
    "BLR": "prompt → prompt → memory",
    "BRL": "prompt → memory → prompt",
    "DL": "named → prompt",
    "NAMES": "names: prompt → prompt",
    "CODE": "code: prompt → prompt",
    "TBL": "JSON → prompt",
    "TBR": "JSON → memory",
    "R": "countries: memory → memory",
    "B": "countries: prompt → memory",
    "countries_R": "countries: memory → memory",
    "countries_B": "countries: prompt → memory",
    "TYPO": "typo fixed → memory",
    "TRANS": "translated → memory",
    "ARITH": "sum computed → memory",
}


def family_label(code: str) -> str:
    """The plain name of a family code (unknown codes pass through unchanged)."""
    return FAMILY_LABEL.get(code, code)


# Plain terms for figures (Dan, 2026-10-21: a reader outside the project must not need I, X, A, b, C, O, W-copy).
TERM = {
    "I": "original bridge",  # the bridge of the original prompt
    "X": "other bridge",  # the bridge the edit substitutes
    "A": "original answer",
    "b": "other bridge's answer",  # the answer the model gives with the other bridge
    "clean": "original prompt",
    "C": "donor prompt",  # the same prompt with the other bridge (only the bridge differs)
    "O": "off-path control",  # changes something the answer does not depend on
    "copy": "patch from the donor prompt",
    "push": "lens push (other − original bridge)",
    "random": "random push (same size)",
    "jpart": "lens-readable part",
    "rest": "the rest",
    "flips": "% of original answers that become the alternative answer (original answer → the other bridge's answer)",
}


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


EXPLAIN_LABELS = ("What we did", "Example", "How to read", "Control", "Data")


def finish(
    fig,
    path: Path,
    title: str,
    note: str,
    handles=None,
    ncols: int | None = None,
    handlelength: float | None = None,
    explain: list[tuple[str, str]] | None = None,
) -> None:
    """Title and note above the panels, legend below them; save at 150 dpi and close. A longer `handlelength` keeps
    dashed lines visible as dashes in the legend.

    `explain` (preferred for new figures, Dan 2026-10-21: a one-paragraph note is hard to read): short labelled rows,
    label in bold on the left, e.g. [("What we did", ...), ("Example", ...), ("How to read", ...), ("Control", ...),
    ("Data", ...)] (EXPLAIN_LABELS); `note`, if not empty, is added as the last "Data" row."""
    import matplotlib.pyplot as plt  # here, so importing this module never picks a backend before the caller's use()

    h, w = fig.get_figheight(), fig.get_figwidth()
    fig.text(0.01, 1 - 0.1 / h, title, ha="left", va="top", fontsize=12, color=INK)
    if explain is None:
        note_lines = textwrap.wrap(note, width=int(w * 15.5))
        head = 0.42 + 0.17 * len(note_lines)  # inches above the panels
        fig.text(
            0.01, 1 - 0.36 / h, "\n".join(note_lines), ha="left", va="top", fontsize=8.5, color=MUTED, linespacing=1.4
        )
    else:
        rows_ = [*explain, *([("Data", note)] if note else [])]
        label_w = 1.05  # inches: the bold label column
        y = 0.38
        for label, text in rows_:
            lines = textwrap.wrap(text, width=int((w - label_w - 0.2) * 15.5)) or [""]
            fig.text(0.01, 1 - y / h, label, ha="left", va="top", fontsize=8.5, color=INK, fontweight="bold")
            fig.text(label_w / w, 1 - y / h, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=MUTED,
                     linespacing=1.4)  # fmt: skip
            y += 0.155 * len(lines) + 0.05
        head = y + 0.1
    rows = -(-len(handles) // (ncols or len(handles))) if handles else 0
    foot = 0.2 + 0.25 * rows if handles else 0.05
    if handles:
        fig.legend(handles=handles, loc="lower center", ncols=ncols or len(handles), frameon=False, fontsize=9,
                   **({"handlelength": handlelength} if handlelength else {}),
                   labelcolor=INK, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.tight_layout(rect=(0, foot / h, 1, 1 - head / h))
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
