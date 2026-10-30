"""The shared scaffold of the redesigned cross-model figures (Dan's figure guide, 23 Oct).

Every figure answers one question, in two versions: MAIN (slides, the README's claim sections: only what decides the
claim, 2400 x 1350 px at 200 dpi, at most 4 panels) and FULL (the README's details: every model, setting and control;
may be taller). A figure is a frame: the title (the claim, <= 12 words), one subtitle line (what is measured), an
optional "How to read" line, the panels, and a caption (<= 2 grey lines: exceptions, n, what was not tested and why).

Colors: model colors are the Okabe-Ito hues of plot_style, each darkened (in HLS lightness) until it has at least 3:1
contrast against white (WCAG 2.x, graphical objects). Semantic colors, the same meaning in every figure: LOOKUP (the
accent) for lookups, RECALL (dark grey) for recalls, CONTROL (light grey) for controls, a pale CHANCE band.
Markers: filled = hybrid, hollow = attention-only (said once, in the caption).

Data: every number a figure draws is also written to figures/archive/cross_model/data/<stem>.json, one record per number with
its grid key (finding, model, setting) when it is a grid cell, so tests can compare it with grid.csv.
"""

from __future__ import annotations

import colorsys
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from bridge_jspace import plot_style as PS
from scripts import readme_build as RB

REPO = RB.REPO
OUT = REPO / "figures" / "archive" / "cross_model"
DATA = OUT / "data"

# ---------------------------------------------------------------- size and type (Dan's guide, section 2)
DPI = 200
MAIN_SIZE = (12.0, 6.75)  # 2400 x 1350 px at 200 dpi, 16:9
FULL_SIZE = (12.0, 9.0)  # 2400 x 1800 px; a FULL figure may set its own height
TITLE, SUBTITLE, HOW, LABEL, TICK, NOTE, CAPTION = 28, 18, 16, 16, 14, 14, 14  # pt; nothing smaller than 14

# ---------------------------------------------------------------- colors (section 5)
INK, INK2, GRID = "#1a1a1a", "#4d4d4d", "#ececec"
LOOKUP = "#6A3D9A"  # the accent: lookups, the deciding quantity in a two-quantity figure (not a model color)
RECALL = "#3d3d3d"  # dark grey: recalls
CONTROL = "#a6a6a6"  # light grey: controls (another sentence hidden, a random push, ...)
CHANCE = "#d9d9d9"  # the chance band's fill (#ececec was too faint at slide size: 5-second test, 23 Oct)
CAPTION_INK = "#5a5a5a"
VERDICT_COLOR, VERDICT_EDGE = PS.VERDICT_COLOR, PS.VERDICT_EDGE  # holds, fails, ≈ chance, ... (plot_style)


def luminance(hex_color: str) -> float:
    """WCAG relative luminance of a #rrggbb color."""
    rgb = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str = "#ffffff") -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def darken_to(hex_color: str, ratio: float = 3.0) -> str:
    """The color, darkened in HLS lightness in small steps (hue and saturation kept) until contrast(white) >= ratio."""
    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    h, lightness, s = colorsys.rgb_to_hls(r, g, b)
    while True:
        rgb = colorsys.hls_to_rgb(h, lightness, s)
        out = "#" + "".join(f"{round(c * 255):02x}" for c in rgb)
        if contrast(out) >= ratio or lightness <= 0:
            return out
        lightness -= 0.01


@dataclass(frozen=True)
class Model:
    key: str
    name: str  # display name (readme_build.NAME)
    short: str
    hybrid: bool
    color: str  # >= 3:1 on white


MODELS = tuple(
    Model(k, RB.NAME[k], RB.SHORT[k], PS.MODEL[k].hybrid, darken_to(PS.MODEL[k].color)) for k in RB.ORDER
)  # hybrids first, then attention-only (readme_build.ORDER)
MODEL = {m.key: m for m in MODELS}


def apply() -> None:
    """rcParams for the redesigned figures (call before drawing)."""
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": NOTE, "axes.titlesize": LABEL, "axes.labelsize": LABEL,
        "xtick.labelsize": TICK, "ytick.labelsize": TICK, "legend.fontsize": NOTE, "text.color": INK,
        "axes.labelcolor": INK, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK,
        "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "white",
        "axes.facecolor": "white", "svg.fonttype": "none", "axes.grid": False,
    })  # fmt: skip


def marker(key: str, size: float = 12, shape: str = "o") -> dict[str, Any]:
    """A model's marker: its color, filled on a hybrid, hollow on attention-only."""
    m = MODEL[key]
    return {"marker": shape, "markersize": size, "markerfacecolor": m.color if m.hybrid else "white",
            "markeredgecolor": m.color, "markeredgewidth": 2.4, "linestyle": "none"}  # fmt: skip


ERRORBAR: dict[str, Any] = {"elinewidth": 1.4, "capsize": 0, "alpha": 0.55}  # thin, light, no caps


# ---------------------------------------------------------------- the frame (section 3)


@dataclass
class Frame:
    fig: Figure
    axes: list[Any]
    kind: str  # "main" / "full"


def frame(kind: str, title: str, subtitle: str, *, how: str | None = None, caption: str | None = None,
          nrows: int = 1, ncols: int = 1, size: tuple[float, float] | None = None, sharex: bool = False,
          sharey: bool = False, width_ratios: list[float] | None = None, height_ratios: list[float] | None = None,
          wspace: float = 0.35, hspace: float = 0.45, left: float = 0.17, right: float = 0.97,
          panel_titles: bool = False) -> Frame:  # fmt: skip
    """A figure with its header (title, subtitle, how to read) on top, its caption at the bottom, the panels between.
    `left` leaves room for row labels (model names); panels are created with a gridspec inside the free band;
    `panel_titles` keeps room above the top panels for their titles (ax.set_title)."""
    if len(title.split()) > 12:
        raise ValueError(f"title over 12 words: {title!r}")
    if kind == "main" and nrows * ncols > 4:
        raise ValueError("a MAIN figure has at most 4 panels")
    apply()
    w, h = size or (MAIN_SIZE if kind == "main" else FULL_SIZE)
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    pt = 1 / 72 / h  # one point as a fraction of the figure's height
    y = 1 - 22 * pt
    fig.text(0.03, y, title, fontsize=TITLE, fontweight="bold", va="top", ha="left", gid="title")
    y -= (TITLE * 1.35) * pt
    fig.text(0.03, y, subtitle, fontsize=SUBTITLE, va="top", ha="left", color=INK2, gid="subtitle")
    y -= (SUBTITLE * 1.4) * pt
    if how:
        fig.text(0.03, y, "How to read: " + how, fontsize=HOW, va="top", ha="left", color=INK2, style="italic",
                 gid="how")  # fmt: skip
        y -= (HOW * 1.45) * pt
    top = y - (14 + (LABEL * 1.8 if panel_titles else 0)) * pt
    axis_room = TICK * 1.6 + LABEL * 1.8 + 12  # x tick labels and the x label below the lowest panels
    bottom = (18 + axis_room) * pt
    if caption:
        lines = caption.count("\n") + 1
        if lines > 2:
            raise ValueError("a caption has at most 2 lines")
        fig.text(0.03, 14 * pt, caption, fontsize=CAPTION, va="bottom", ha="left", color=CAPTION_INK,
                 linespacing=1.3, gid="caption")  # fmt: skip
        bottom = (14 + CAPTION * 1.35 * lines + 14 + axis_room) * pt
    gs = fig.add_gridspec(nrows, ncols, left=left, right=right, top=top, bottom=bottom, wspace=wspace,
                          hspace=hspace, width_ratios=width_ratios, height_ratios=height_ratios)  # fmt: skip
    axes: list[Any] = []
    for r in range(nrows):
        for c in range(ncols):
            share = {}
            if axes and sharex:
                share["sharex"] = axes[0]
            if axes and sharey:
                share["sharey"] = axes[0]
            axes.append(fig.add_subplot(gs[r, c], **share))
    return Frame(fig, axes, kind)


def model_rows(ax, keys: list[str], *, gap: float = 0.8, label: bool = True) -> dict[str, float]:
    """y positions for model rows, top to bottom in ORDER, with a gap between hybrids and attention-only and a small
    grey heading above each group (no rotated text); returns {model key: y}. Draws the model names as tick labels."""
    ys: dict[str, float] = {}
    y = 0.0
    prev = None
    heads: list[tuple[float, str]] = []
    for m in (m for m in MODELS if m.key in keys):
        if prev is None or prev != m.hybrid:
            if prev is not None:
                y += gap
            heads.append((y - 0.62, "Hybrids" if m.hybrid else "Attention-only"))
        ys[m.key] = y
        y += 1
        prev = m.hybrid
    ax.set_ylim(y - 0.4, -1.0)
    if label:
        ax.set_yticks(list(ys.values()), [MODEL[k].name for k in ys])
        ax.tick_params(axis="y", length=0, labelsize=LABEL)
        for yy, text in heads:
            ax.text(0, yy, text, transform=ax.get_yaxis_transform(), ha="right", va="bottom", fontsize=NOTE,
                    color=CAPTION_INK, gid="group")  # fmt: skip
    return ys


def chance_band(ax, lo: float, hi: float | None = None, *, horizontal: bool = False, label: str | None = None) -> None:
    """A light grey band at chance (a single value gets a narrow band); the one reference a panel may carry."""
    hi = lo if hi is None else hi
    span = (lo - 1, hi + 1) if hi - lo < 1 else (lo, hi)
    (ax.axhspan if horizontal else ax.axvspan)(*span, color=CHANCE, zorder=0, lw=0)
    if label:
        if horizontal:
            ax.text(1.0, span[1], label, transform=ax.get_yaxis_transform(), ha="right", va="bottom", fontsize=NOTE,
                    color=CAPTION_INK, gid="chance")  # fmt: skip
        else:
            ax.text(span[1] + 1, 1.0, label, transform=ax.get_xaxis_transform(), ha="left", va="bottom",
                    fontsize=NOTE, color=CAPTION_INK, gid="chance")  # fmt: skip


# ---------------------------------------------------------------- data, checks, saving


@dataclass
class Number:
    """One number a figure draws: its value and, for a grid cell, the cell's key (finding, model, setting[, part])."""

    value: float
    what: str  # e.g. "% right, sentence hidden"
    finding: str | None = None
    model: str | None = None
    setting: str | None = None
    part: str = ""
    ci: tuple[float, float] | None = None
    n: int | None = None
    source: str = "grid.csv"  # or the run file a curve comes from
    extra: dict[str, Any] = field(default_factory=dict)


def book(grid_dir: Path | None = None) -> RB.Book:
    """The grid's main-lens cells (the grid pinned in docs/depth/README.template.md unless given)."""
    return RB.Book(grid_dir or RB.pinned_grid(RB.TEMPLATE.read_text()))


def cell_number(b: RB.Book, f: str, m: str, setting: str, what: str, part: str = "") -> Number | None:
    """The grid cell's value as a Number, or None when the cell has no value."""
    cs = [c for c in b.of(f, m) if c.setting == setting and c.part == part and c.value is not None]
    if not cs:
        return None
    c = cs[0]
    return Number(c.value, what, f, m, setting, part, c.ci, c.n)  # type: ignore[arg-type]


def not_tested(b: RB.Book, f: str, keys: Iterable[str] | None = None) -> str:
    """'Not tested: Olmo-Hybrid (no lens), Gemma (still running)': models without a judged cell, with the reason."""
    out = []
    for m in MODELS:
        if keys is not None and m.key not in keys:
            continue
        cs = b.of(f, m.key)
        if not any(c.word in ("holds", "fails", "not interpretable", "inconclusive", "open") for c in cs):
            out.append(f"{m.short} ({RB.reason(cs)})")
    return ("Not tested: " + ", ".join(out) + ".") if out else ""


def save(fr: Frame, stem: str, numbers: list[Number], out: Path = OUT) -> list[Path]:
    """<stem>_<kind>.png (200 dpi) and .svg at the frame's size, after the overlap check, and the numbers' data file."""
    bad = PS.overlaps(fr.fig)
    if bad:
        raise ValueError(f"{stem}_{fr.kind}: overlapping or clipped text: {bad[:8]}")
    out.mkdir(parents=True, exist_ok=True)
    paths = [out / f"{stem}_{fr.kind}.png", out / f"{stem}_{fr.kind}.svg"]
    fr.fig.savefig(paths[0], dpi=DPI, facecolor="white")
    fr.fig.savefig(paths[1], facecolor="white")
    (out / "data").mkdir(exist_ok=True)
    (out / "data" / f"{stem}_{fr.kind}.json").write_text(json.dumps([asdict(n) for n in numbers], indent=1) + "\n")
    plt.close(fr.fig)
    return paths


def check_numbers(path: Path, b: RB.Book) -> list[str]:
    """Mismatches between a figure's data file and grid.csv: every Number with a grid key must equal its cell."""
    bad = []
    for d in json.loads(path.read_text()):
        if d["source"] != "grid.csv" or d["finding"] is None:
            continue
        cs = [c for c in b.of(d["finding"], d["model"]) if c.setting == d["setting"] and c.part == d["part"]]
        if not cs or cs[0].value is None or abs(cs[0].value - d["value"]) > 1e-9:
            bad.append(f"{path.name}: {d['finding']} {d['model']} {d['setting']} {d['part']}")
    return bad
