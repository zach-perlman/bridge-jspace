"""The README figures' shared visual language (Dan, 26 Oct ~16:45; docs/figure_plan.md): sized for GitHub's ~880 px
column (8.8 in wide, fonts >= 11 pt), the claim as the title (about 12 words) and one subtitle line on how to read it;
fixed colours (lookup purple, recall dark grey; identity blue, position orange, value green, unchanged light grey;
random controls light grey); extra loss as a dot with a 95% CI whisker on a shared [-0.2, 1.0] axis; models in the
order 9B, 27B, 122B, Muse; one status encoding: filled = fixed in advance, open = after the data, a degree sign on the
label = a rerun with a gate lowered after the data. Every plotted number is recorded for figures/story/data.csv. The
words on the figures: docs/glossary.md."""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "figures" / "story"
SUPP = REPO / "figures" / "supp"
NUMBERS = REPO / "docs" / "x0_numbers.json"
WIDTH = 8.8  # inches: 880 px at 100 px per inch, GitHub's README column
COL = {"lookup": "#6a4bd6", "recall": "#3a3a3a", "identity": "#2b7bba", "position": "#e08a1e", "original": "#c8c8c8",
       "value": "#009e73", "other": "#ececec", "control": "#bdbdbd", "band": "#f0f0f0", "muted": "#666666",
       "shade": "#efe9fb"}  # fmt: skip
FONT = 11  # pt, the smallest text on a README figure
LOWERED = "°"  # on a label: a rerun with the gate lowered to 0.75 after the data
MODELS = (("qwen3.5-9b", "9b", "Qwen3.5-9B"), ("qwen3.6-27b", "27b", "Qwen3.6-27B"),
          ("qwen3.5-122b-a10b", "122b", "Qwen3.5-122B"), ("muse-glimmer-30b", "muse", "Muse Glimmer 30B"))  # fmt: skip
XLIM = (-0.2, 1.0)
NOT_NEEDED = 0.10  # the rule's "not needed" band (X0: extra loss <= 0.10)
ROWS: list[dict] = []
# v6 (Dan's README v6 brief, §5; docs/figure_plan.md "v6 style rules"): a reader's layer is not interpretable where the
# whole change switches < NI_SWITCH of it (scripts/x47_anatomy.py's bar); one look for that shading in every figure.
NI_SWITCH = 0.30
NI_SHADE = {"facecolor": "#f6f6f6", "edgecolor": "#d4d4d4", "hatch": "///", "lw": 0, "zorder": 0}
# the original answer as an empty segment: light grey stays the random control's colour alone
EMPTY = {"facecolor": "none", "edgecolor": "#9a9a9a", "lw": 0.7}
# Dan's figures brief (28 Oct ~18:30) §1, one mark system: colour = who or what (no other hue on a figure that follows
# it), mark = the operation, panel = the model (9B, 27B, Muse). scripts/check_figure_terms.py checks MARK_FIGS' hues.
MARK_COL = {"recall": COL["recall"], "lookup": COL["lookup"], "jpp": "#13998f", "address": COL["position"],
            "identity": COL["identity"], "null": COL["control"]}  # fmt: skip
MARK = {"remove": "o", "zero": "X", "add": "D", "swap": "^", "whole": "s"}
MARK_TEXT = {"remove": "removed from the change", "zero": "taken out of a prompt's own state",
             "add": "added by itself", "swap": "the swap", "whole": "the whole state copied"}  # fmt: skip
MARK_COL_TEXT = {"recall": "recall", "lookup": "lookup", "jpp": "the J++ part", "address": "the address",
                 "identity": "identity route", "null": "a random part (same size)"}  # fmt: skip
STATUS_GLYPH = {"fixed": "●", "after": "○"}
STATUS_TEXT = {"fixed": "fixed in advance", "after": "after the data"}
SUBTITLE = "story_subtitle"  # the attribute title() sets on the subtitle's Text
INSET = "story_inset"  # the attribute inset() sets on a small inset axes (not counted as a panel by the v6 check)


def inset(fig, rect: tuple[float, float, float, float]):
    """v6: a small inset axes at rect (figure fraction), marked so scripts/check_figure_terms.py does not count it as a
    panel."""
    ax = fig.add_axes(rect)
    setattr(ax, INSET, True)
    return ax


def setup():
    plt.rcParams.update({"font.size": FONT, "axes.titlesize": 12, "axes.labelsize": FONT, "xtick.labelsize": FONT,
                         "ytick.labelsize": FONT, "legend.fontsize": FONT, "axes.spines.top": False,
                         "axes.spines.right": False, "font.family": "DejaVu Sans", "svg.fonttype": "none",
                         "axes.edgecolor": "#555555"})  # fmt: skip
    return plt


def title(fig, text: str, sub: str | None = None, limit: int = 70) -> None:
    """The claim as the title and, below it, one line on how to read the figure."""
    assert len(text) <= limit, f"title over {limit} characters: {text!r}"
    # a title (14 pt) or subtitle (11 pt) wider than the 880 px column shrinks to fit it, as measured
    fit(fig, fig.suptitle(text, x=0.01, y=0.995, ha="left", va="top", fontsize=14, weight="bold"))
    if sub:
        h = fig.get_figheight()
        t = fig.text(0.01, 1 - 0.42 / h, sub, ha="left", va="top", fontsize=FONT, color=COL["muted"])
        fit(fig, t)
        # marked for scripts/check_figure_terms.py's v6 rules; a Python attribute, so the saved files do not change
        setattr(t, SUBTITLE, True)


def fit(fig, t, right: float = 0.99) -> None:
    """Shrink text t (left-aligned at its x, figure fraction) until it ends by `right` of the figure's width."""
    r = fig.canvas.get_renderer()
    room = (right - t.get_position()[0]) * fig.get_figwidth()
    # Agg hints glyphs to whole pixels, so the width moves in steps: shrink by quarter points until it fits
    while t.get_window_extent(r).width / fig.dpi > room and t.get_fontsize() > 8:
        t.set_fontsize(t.get_fontsize() - 0.25)


def panel_tag(ax, n: str | None, status: str | None, inside: bool = False) -> None:
    """v6: "n = <n>" and the status glyph alone (filled = fixed in advance, open = after the data; the README's key
    says which) in small type at the panel's top right (above the frame, or inside its corner on a white patch); status
    None for a schematic. n per model reads "758, 758, 657" (9B, 27B, Muse)."""
    parts = [f"n = {n}"] if n else []
    parts += [STATUS_GLYPH[status]] if status else ["schematic"]
    y, va = (0.985, "top") if inside else (1.015, "bottom")
    ax.text(0.995 if inside else 1.0, y, ("\n" if inside else "  ").join(parts), transform=ax.transAxes, ha="right",
            va=va, fontsize=FONT, multialignment="right",
            color=COL["muted"], zorder=8, bbox={"boxstyle": "square,pad=0.15", "fc": "white", "ec": "none"})  # fmt: skip


def not_interpretable(ax, spans: list[tuple[float, float]], y: float = 0.55) -> None:
    """v6: the same hatched shading over each (x0, x1) span where the whole change switches < NI_SWITCH, labelled
    'not interpretable' at height y (axes units) where the span is wide enough."""
    for x0, x1 in spans:
        ax.axvspan(x0, x1, **NI_SHADE)
        if x1 - x0 >= 2.5:
            ax.text((x0 + x1) / 2, y, "not\ninterpretable", transform=ax.get_xaxis_transform(), ha="center",
                    va="center", fontsize=FONT, color=COL["muted"], zorder=7,
                    bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "none"})  # fmt: skip


def spans(flags: list[bool], step: float = 1.0) -> list[tuple[float, float]]:
    """The runs of True in flags as (x0, x1) spans on an axis with one position per flag (index * step)."""
    out: list[tuple[float, float]] = []
    for i, f in enumerate(flags):
        if not f:
            continue
        if out and abs(out[-1][1] - (i - 0.5) * step) < 1e-9:
            out[-1] = (out[-1][0], (i + 0.5) * step)
        else:
            out.append(((i - 0.5) * step, (i + 0.5) * step))
    return out


def status_handles(kinds=("fixed", "after", "lowered")) -> tuple[list, list[str]]:
    """Legend entries for the one status encoding (grey, so they do not read as a reader)."""
    g = "#7a7a7a"
    hs = {"fixed": (plt.Line2D([], [], marker="o", ls="", color=g, ms=7), "fixed in advance"),
          "after": (plt.Line2D([], [], marker="o", ls="", mfc="white", mec=g, mew=1.6, ms=7), "after the data"),
          "lowered": (plt.Line2D([], [], ls="", marker=""), f"{LOWERED} gate lowered to 0.75 after the data")}  # fmt: skip
    return [hs[k][0] for k in kinds], [hs[k][1] for k in kinds]


def numbers() -> dict[str, str]:
    return {k: v["text"] for k, v in json.loads(NUMBERS.read_text()).items()}


def parse(text: str | None) -> tuple[float, float, float] | None:
    """'0.53 [0.42, 0.61]' (with typographic minus signs) -> (0.53, 0.42, 0.61); None if absent."""
    if not text:
        return None
    v = [float(x.replace("−", "-")) for x in re.findall(r"[−-]?\d+\.\d+", text)]
    return (v[0], v[1], v[2]) if len(v) >= 3 else None


def record(fig: str, model: str, quantity: str, v, lo=None, hi=None, n=None, source: str = "") -> None:
    ROWS.append({"figure": fig, "model": model, "quantity": quantity, "value": v, "lo": lo, "hi": hi, "n": n,
                 "source": source})  # fmt: skip


def dot(ax, x: float, y: float, v: tuple[float, float, float], color: str, kind: str = "fixed", size: float = 7.5):
    """An extra-loss dot with its 95% CI whisker; kind: fixed (filled) or after / rerun (open; a rerun's degree sign goes
    on its label, not on the mark)."""
    ax.plot([v[1], v[2]], [y, y], color=color, lw=1.6, zorder=2, solid_capstyle="butt")
    face = color if kind == "fixed" else "white"
    ax.plot([v[0]], [y], "o", ms=size, mfc=face, mec=color, mew=1.6, zorder=3)


def extra_axis(ax, label: bool = True) -> None:
    ax.set_xlim(*XLIM)
    ax.axvspan(XLIM[0], NOT_NEEDED, color=COL["band"], lw=0, zorder=0)
    ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    if label:
        ax.set_xlabel("extra loss")


def empty(ax, text: str) -> None:
    ax.text(0.5, 0.5, text, transform=ax.transAxes, ha="center", va="center", fontsize=FONT, color=COL["muted"])


def save(fig, name: str, supp: bool = False) -> None:
    out = SUPP if supp else OUT
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.svg", facecolor="white")
    fig.savefig(out / f"{name}.png", dpi=200, facecolor="white")
    plt.close(fig)


def write_data() -> None:
    """figures/story/data.csv: every plotted number, then every number docs/x0_numbers.json holds (the README's)."""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["figure", "model", "quantity", "value", "lo", "hi", "n", "source"])
    w.writeheader()
    w.writerows(ROWS)
    for key, num in json.loads(NUMBERS.read_text()).items():
        w.writerow({"figure": "numbers", "quantity": key, "value": num["text"], "source": num["source"]})
    (OUT / "data.csv").write_text(buf.getvalue())
