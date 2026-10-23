"""One style for the merged cross-model figures: Okabe-Ito colors, one fixed color and place per model, slide sizes.

Okabe and Ito (2008), "Color Universal Design": eight colors that stay apart under the common color-vision
deficiencies. Every merged figure takes a model's color, marker fill and place from MODELS, so a model looks the same
in every figure. Hybrids (DeltaNet and attention layers) get warm colors and filled markers, attention-only models cool
colors (and black) and hollow markers; the two groups are also drawn apart.

Slides: 16:9 at 13.33 x 7.5 in, i.e. 1920 px wide at 144 dpi, so a 14 pt font is 14 pt on a 1920 px slide. PNG at
200 dpi and SVG (text kept as text).

overlaps(fig) is the machine check for readability: no two drawn texts may touch, none may leave the figure, and no
value or status label may leave its panel; it can name the texts it finds by role only, so a figure of results nobody
has read yet can be checked without printing a number.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.patheffects as pe
from matplotlib.text import Text
from matplotlib.transforms import Bbox

OKABE_ITO = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky blue": "#56B4E9",
    "bluish green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish purple": "#CC79A7",
}


@dataclass(frozen=True)
class ModelStyle:
    key: str  # scripts/cross_model_grid.py's model key
    label: str
    hybrid: bool
    color: str
    edge: str  # marker edge and line outline: the color itself, or dark where the color is too light on white


_DARK_EDGE = "#5c5400"  # the yellow's outline: a dark olive, so the light yellow stays visible on white
MODELS = (
    ModelStyle("27b", "Qwen3.6-27B", True, OKABE_ITO["vermillion"], OKABE_ITO["vermillion"]),
    ModelStyle("9b", "Qwen3.5-9B", True, OKABE_ITO["orange"], OKABE_ITO["orange"]),
    ModelStyle("olmo_hybrid", "Olmo-Hybrid-7B", True, OKABE_ITO["yellow"], _DARK_EDGE),
    ModelStyle("122b", "Qwen3.5-122B", True, OKABE_ITO["reddish purple"], OKABE_ITO["reddish purple"]),
    ModelStyle("32b", "Qwen3-32B", False, OKABE_ITO["blue"], OKABE_ITO["blue"]),
    ModelStyle("olmo", "OLMo-3-7B-I", False, OKABE_ITO["sky blue"], OKABE_ITO["sky blue"]),
    ModelStyle("muse", "Muse 30B", False, OKABE_ITO["bluish green"], OKABE_ITO["bluish green"]),
    ModelStyle("gemma", "Gemma 4 31B-it", False, OKABE_ITO["black"], OKABE_ITO["black"]),
)
MODEL = {m.key: m for m in MODELS}
GROUPS = (("Hybrid", True), ("Attention only", False))  # group label, hybrid

# slide geometry and type
FIGSIZE = (13.333, 7.5)
PNG_DPI = 200
FONT, TICK, LABEL, PANEL_TITLE, SUBTITLE, TITLE = 14, 14, 15, 16, 15, 18  # pt; nothing below FONT
INK, INK2, GRID = "#1a1a1a", "#4d4d4d", "#e6e6e6"
COMPARE, COMPARE2 = "#4d4d4d", "#a3a3a3"  # a comparison series drawn beside a model's own color (dark, light grey)
# the one extra color, used only for the decisive comparison (the gap between the two arms a claim is about, and the
# background of a contrast panel): a pale lavender, apart from every Okabe-Ito color
HIGHLIGHT, HIGHLIGHT_BG = "#C9B3E6", "#F5F0FB"

# lines: dashed = chance or the control level, dotted = the rule's bar
CHANCE_LINE: dict[str, Any] = {"color": "#6b6b6b", "linestyle": (0, (6, 4)), "linewidth": 1.8}
RULE_LINE: dict[str, Any] = {"color": INK, "linestyle": (0, (1, 2.2)), "linewidth": 2.2}
NOT_INTERPRETABLE: dict[str, Any] = {"facecolor": "#f0f0f0", "edgecolor": "#a0a0a0", "hatch": "///", "linewidth": 0}
VERDICT_SYMBOL = {"holds": "✓", "fails": "✗", "inconclusive": "≈", "open": "○"}
# Verdict colors, the same meaning in every figure (Dan, 23 Oct): fills that carry dark text (INK on each >= 5:1, WCAG
# AA); holds and fails are also >= 3:1 against white. Checked with the dataviz palette validator (OKLab x100, all pairs
# of the five fills): >= 10.8 apart under protan, deutan and tritan simulation, >= 17.4 in normal vision. The state is
# also written in every cell, so no state rests on color alone. "descriptive": a value that is not a verdict (where the
# lens reads a stated bridge). "not tested" is white, outlined with VERDICT_EDGE.
VERDICT_COLOR = {"holds": "#2E9E86", "fails": "#D9782D", "≈ chance": "#EBBE45", "can't tell": "#E6E6E6",
                 "not tested": "#FFFFFF", "descriptive": "#93B4E0"}  # fmt: skip
VERDICT_EDGE = "#c4c4c4"


def apply() -> None:
    """rcParams for the merged figures (call before drawing)."""
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": FONT, "axes.titlesize": PANEL_TITLE, "axes.labelsize": LABEL,
        "xtick.labelsize": TICK, "ytick.labelsize": TICK, "legend.fontsize": FONT, "text.color": INK,
        "axes.labelcolor": INK, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK,
        "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "white",
        "axes.facecolor": "white", "svg.fonttype": "none", "hatch.linewidth": 1.0, "hatch.color": "#a0a0a0",
    })  # fmt: skip


def marker(key: str, shape: str = "o", size: float = 11) -> dict[str, Any]:
    """Plot kwargs for a model's marker: its color, filled on a hybrid, hollow (white inside) on attention-only."""
    m = MODEL[key]
    return {"marker": shape, "markersize": size, "markerfacecolor": m.color if m.hybrid else "white",
            "markeredgecolor": m.edge, "markeredgewidth": 2.2, "linestyle": "none"}  # fmt: skip


def line(key: str, width: float = 2.6) -> dict[str, Any]:
    """Plot kwargs for a model's line (a light color gets a dark outline)."""
    m = MODEL[key]
    out: dict[str, Any] = {"color": m.color, "linewidth": width}
    if m.edge != m.color:
        out["path_effects"] = [pe.Stroke(linewidth=width + 1.6, foreground=m.edge), pe.Normal()]
    return out


HALO = [pe.withStroke(linewidth=3.5, foreground="white")]  # value labels stay legible over lines, grid and hatching
# text roles (Text gid) whose content can carry a result: a report names them by role, never by their text
MASKED = ("value", "n", "tick", "status")


def renderer(fig):
    """The figure's renderer (the Agg canvas's), to measure drawn text."""
    return fig.canvas.get_renderer()


def text_width(fig, s: str, size: float = FONT, weight: str = "normal") -> float:
    """Width of `s` in inches as the figure's renderer draws it."""
    t = fig.text(0, 0, s, fontsize=size, fontweight=weight)
    w = t.get_window_extent(renderer(fig)).width / fig.dpi
    t.remove()
    return w


def drawn_texts(fig) -> list[tuple[Text, str]]:
    """Every visible, non-empty text the figure draws, with its role: "tick" for the current tick labels (a stale
    tick from matplotlib's pool is left out), else the Text's gid ("value", "n", "status", ...) or ""."""
    pool: set[int] = set()
    current: list[Text] = []
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            for tk in axis.get_major_ticks() + axis.get_minor_ticks():
                pool.update((id(tk.label1), id(tk.label2)))
            current += list(axis.get_ticklabels(which="both"))
    out = [(t, t.get_gid() or "") for t in fig.findobj(Text) if id(t) not in pool] + [(t, "tick") for t in current]
    return [(t, role) for t, role in out if t.get_visible() and t.get_text().strip()]


GRAPHICS = ("mark", "ci", "gap", "tick")  # Line2D gids a text must not touch: markers, intervals, gap bars, ticks


def graphic_boxes(fig, r=None) -> list[tuple[str, Bbox]]:
    """Display-space boxes of the figure's marks a text must keep off: every Line2D whose gid is in GRAPHICS; a
    "mark" line gets one box per point (its marker), the others the box of their path grown by half the line width."""
    r = r or renderer(fig)
    out: list[tuple[str, Bbox]] = []
    px = fig.dpi / 72
    for ax in fig.axes:
        for ln in ax.get_lines():
            gid = ln.get_gid()
            if gid not in GRAPHICS or not ln.get_visible():
                continue
            if gid == "mark":
                half = (ln.get_markersize() / 2 + ln.get_markeredgewidth()) * px
                xy = ln.get_transform().transform(ln.get_xydata())
                boxes = [Bbox([[x - half, y - half], [x + half, y + half]]) for x, y in xy]
                if ln.get_clip_on():  # a clipped marker is drawn only inside its panel
                    clip = ax.get_window_extent(r)
                    boxes = [b for b in (Bbox.intersection(b, clip) for b in boxes) if b is not None]
                out += [(gid, b) for b in boxes]
            else:
                out.append((gid, ln.get_window_extent(r).padded(ln.get_linewidth() / 2 * px)))
    return out


def overlaps(fig, pad_px: float = 2.0, mask: bool = False) -> list[tuple[str, str]]:
    """Pairs of drawn texts whose boxes, each grown by `pad_px` pixels, intersect; a text on a marker, an interval, a
    gap bar or a tick (graphic_boxes; paired with that mark's role); and every text that extends outside the figure,
    or (a value or status label) outside its panel. With `mask`, a text of a MASKED role is named by its role
    ("<value>"), so the list can be printed while the figure's numbers stay unread."""
    fig.canvas.draw()
    r = renderer(fig)
    fb = fig.bbox

    def name(t: Text, role: str) -> str:
        return f"<{role}>" if mask and role in MASKED else repr(t.get_text()[:70])

    texts = drawn_texts(fig)
    items = [(name(t, role), t.get_window_extent(r)) for t, role in texts]
    m = pad_px  # a text must keep this margin from the figure's edge too
    out = [(n, "outside the figure") for n, b in items
           if b.x0 < fb.x0 + m or b.y0 < fb.y0 + m or b.x1 > fb.x1 - m or b.y1 > fb.y1 - m]  # fmt: skip
    for (t, role), (n, b) in zip(texts, items, strict=True):  # a value or a status label stays inside its panel
        if role in ("value", "status") and t.axes is not None:
            ab = t.axes.get_window_extent(r)
            if b.x0 < ab.x0 - m or b.x1 > ab.x1 + m or b.y0 < ab.y0 - m or b.y1 > ab.y1 + m:
                out.append((n, "outside its panel"))
    grown = [(n, b.padded(pad_px)) for n, b in items]
    for i, (na, a) in enumerate(grown):
        for nb, b in grown[i + 1 :]:
            if a.overlaps(b):
                out.append((na, nb))
    marks = graphic_boxes(fig, r)
    for (_, role), (n, b) in zip(texts, grown, strict=True):
        if role == "tick":
            continue
        hit = next((gid for gid, g in marks if b.overlaps(g)), None)
        if hit:
            out.append((n, f"a {hit}"))
    return out


def save(fig, out_dir: Path, stem: str) -> list[Path]:
    """PNG (200 dpi) and SVG at the figure's own 16:9 size (no tight bounding box, which would change it)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = [out_dir / f"{stem}.png", out_dir / f"{stem}.svg"]
    fig.savefig(paths[0], dpi=PNG_DPI, facecolor="white")
    fig.savefig(paths[1], facecolor="white")
    return paths
