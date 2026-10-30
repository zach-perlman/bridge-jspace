"""The dot table (Dan's reference renderer, figref/dottable.py, 30 Oct; ported as is, PNG only). Built to look like figures/depth/fig00_setup.png (Dan's reference):
rows with bold labels on the left, aligned columns, numbers in their own column, colour only for meaning and
introduced by the coloured word itself (no legend box), grey for everything secondary, all text horizontal.

A figure is a table: one row per model (or per condition), one column per measurement. Each column is either a
panel (dots on a shared row axis) or a text column (numbers). Rows are zebra-striped across the whole width so the
eye can follow a model from the label to its last number.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

INK, MUTED, FAINT, GRID, ZEBRA, BAND = "#1A1A1A", "#6B6B6B", "#BDBDBD", "#E4E4E4", "#F5F5F5", "#E6E6E6"
C = {"recall": "#2B2B2B", "lookup": "#6B5BD2", "lens": "#1A9E8A", "address": "#E08A1E", "identity": "#3A7DC9",
     "control": "#A8A8A8", "other": "#D9D9D9"}  # fmt: skip

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "svg.fonttype": "none",
                     "axes.edgecolor": FAINT, "xtick.color": MUTED, "xtick.labelsize": 11})  # fmt: skip

BEFORE_SAVE = None  # a hook f(fig, path) run before every save
ROW_H, HEAD_H, FOOT_H, LABEL_ROW = 0.50, 0.85, 0.62, 0.46  # inches; LABEL_ROW: direct labels above row 1
KEY_H = 0.42  # the key row under the axes


@dataclass
class Row:
    name: str
    sub: str = ""  # grey second line (a layer, "post hoc")
    hollow: bool = False  # post hoc: hollow marks and a grey ○ after the name


@dataclass
class Col:
    width: float  # inches
    title: str = ""
    sub: str = ""  # grey line under the title: the unit or what was done
    draw: object = None  # panel: f(ax, rows) ; text column: f(i, row) -> [(text, colour, weight)]
    xlim: tuple | None = None
    xticks: list | None = None
    xfmt: str = "{:g}"
    text: bool = False
    align: str = "left"


@dataclass
class Table:
    rows: list
    cols: list
    label_w: float = 1.7
    pad: float = 0.25  # between columns
    zebra: bool = True
    extra: list = field(default_factory=list)  # callbacks f(fig) after drawing
    labels: bool = True  # reserve the direct-label row above row 1
    # the key under the axes, [(mark, colour, words)], e.g. ("●", C["control"], "control: a random part"): for marks
    # that mean the same in every column, where a head label over column 1 would read as that column's only (Dan, 30 Oct)
    key: list = field(default_factory=list)
    head: float = HEAD_H  # header height (inches); raise it for group titles above the column titles

    def render(self, path: str, dpi: int = 160) -> None:
        n = len(self.rows)
        lab = LABEL_ROW if self.labels else 0.12
        width = self.label_w + sum(c.width for c in self.cols) + self.pad * (len(self.cols) + 1)
        body = n * ROW_H + lab
        height = self.head + body + FOOT_H + (KEY_H if self.key else 0)
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        fy = lambda inch_from_top: 1 - inch_from_top / height  # noqa: E731
        fx = lambda inch: inch / width  # noqa: E731
        top = self.head + lab  # first row's top edge, inches from the figure top

        if self.zebra:  # stripes across the whole table, behind everything
            for i in range(n):
                if i % 2 == 0:
                    fig.patches.append(Rectangle((0, fy(top + (i + 1) * ROW_H)), 1, ROW_H / height,
                                                 transform=fig.transFigure, color=ZEBRA, zorder=-5))  # fmt: skip
        for i, r in enumerate(self.rows):  # row labels
            y = fy(top + (i + 0.5) * ROW_H)
            if not r.name and r.sub:  # a sub-row of a group (S6): its short label alone, indented, grey
                fig.text(fx(0.3), y, r.sub, ha="left", va="center", fontsize=11.5, color=MUTED)
                continue
            dy = 0.09 if r.sub else 0
            t = fig.text(fx(0.12), y + dy / height * 1.0, r.name, ha="left", va="center", fontsize=13,
                         weight="bold", color=INK)  # fmt: skip
            if r.hollow:
                fig.canvas.draw()
                bb = t.get_window_extent()
                fig.text(bb.x1 / fig.bbox.width + fx(0.06), y + dy / height, "○", ha="left", va="center",
                         fontsize=12, color=MUTED)  # fmt: skip
            if r.sub:
                fig.text(fx(0.12), y - 0.17 / height, r.sub, ha="left", va="center", fontsize=11, color=MUTED)

        x = self.label_w + self.pad
        for c in self.cols:
            if c.title:
                fig.text(
                    fx(x),
                    fy(0.22 + self.head - HEAD_H),
                    c.title,
                    ha="left",
                    va="top",
                    fontsize=13,
                    weight="bold",
                    color=INK,
                )
            if c.sub:
                fig.text(fx(x), fy(0.52 + self.head - HEAD_H), c.sub, ha="left", va="top", fontsize=11.5, color=MUTED)
            if c.text:
                for i, r in enumerate(self.rows):
                    y = fy(top + (i + 0.5) * ROW_H)
                    rich(fig, fx(x + (c.width if c.align == "right" else 0)), y, c.draw(i, r), ha=c.align)
            else:
                ax = fig.add_axes((fx(x), fy(top + n * ROW_H), fx(c.width), (n * ROW_H + lab) / height))
                ax.set_zorder(1)
                ax.set_ylim(n - 0.5, -0.5 - lab / ROW_H)
                ax.set_xlim(*c.xlim)
                for s in ("left", "right", "top"):
                    ax.spines[s].set_visible(False)
                ax.spines["bottom"].set_color(FAINT)
                ax.set_yticks([])
                ax.patch.set_alpha(0)
                if c.xticks is not None:
                    ax.set_xticks(c.xticks, [c.xfmt.format(t) for t in c.xticks])
                ax.tick_params(axis="x", length=3, color=FAINT, pad=4)
                for t in ax.get_xticks():
                    ax.plot([t, t], [n - 0.5, -0.5], color=GRID, lw=0.8, zorder=0)
                if c.xlim[0] < 0 < c.xlim[1]:
                    ax.plot([0, 0], [n - 0.5, -0.5], color=MUTED, lw=0.9, zorder=1)
                c.draw(ax, self.rows)
            x += c.width + self.pad
        if self.key:
            parts = []
            for k, (mark, col, words) in enumerate(self.key):
                parts += [
                    ("     " if k else "", MUTED, "normal"),
                    (mark + " ", col, "normal"),
                    (words, MUTED, "normal"),
                ]
            rich(fig, fx(0.12), fy(height - 0.24), parts, size=11.5)
        for f in self.extra:
            f(fig)
        if BEFORE_SAVE is not None:  # the kit's table lint (figkit/lint.py table_problems)
            BEFORE_SAVE(fig, path)
        fig.savefig(path, dpi=dpi, facecolor="white")
        plt.close(fig)


def rich(fig, x, y, parts, ha="left", size=12.5):
    """Coloured words side by side, e.g. [("0.53", INK, "bold"), (" [0.42, 0.61]", MUTED, "normal")]."""
    fig.canvas.draw()
    texts, w = [], 0.0
    for s, col, wt in parts:
        t = fig.text(x, y, s, ha="left", va="center", fontsize=size, color=col, weight=wt)
        texts.append(t)
        w += t.get_window_extent().width / fig.bbox.width
    if ha == "right":
        x -= w
    for t in texts:
        t.set_x(x)
        x += t.get_window_extent().width / fig.bbox.width


# ---- marks ------------------------------------------------------------------------------------------------------------
def dot(ax, x, y, color, hollow=False, size=9.5, cell=None, value=None, vfmt="{:.2f}", vside="right", zorder=4):
    if cell and cell[1] is not None:
        ax.plot([cell[1], cell[2]], [y, y], color=color, lw=1.8, solid_capstyle="butt", zorder=zorder - 1)
    ax.plot([x], [y], "o", ms=size, color=color, mfc="white" if hollow else color, mew=2 if hollow else 0,
            zorder=zorder)  # fmt: skip
    if value is not None:
        x0 = cell[2] if (cell and cell[2] is not None and vside == "right") else x
        x0 = cell[1] if (cell and cell[1] is not None and vside == "left") else x0
        pts = 9 if x0 == x else 5
        ax.annotate(
            clean(vfmt.format(value)),
            (x0, y),
            xytext=(pts if vside == "right" else -pts, 0),
            textcoords="offset points",
            ha="left" if vside == "right" else "right",
            va="center",
            fontsize=11.5,
            color=color if color != C["control"] else MUTED,
            annotation_clip=False,
            zorder=6,
            bbox={
                "boxstyle": "square,pad=0.12",
                "facecolor": ZEBRA if round(y) % 2 == 0 else "white",
                "edgecolor": "none",
            },
        )


def clean(s: str) -> str:
    return s[1:] if s.startswith("-") and set(s[1:]) <= set("0.") else s


def under(ax, x, word):
    """A grey word under the x axis (below the tick labels), for a band or rule that has no room above."""
    ax.annotate(
        word,
        (x, 0),
        xycoords=("data", "axes fraction"),
        xytext=(0, -26),
        textcoords="offset points",
        ha="center",
        va="top",
        fontsize=10.5,
        color=MUTED,
        annotation_clip=False,
    )


def connector(ax, a, b, y):
    ax.plot([a, b], [y, y], color="#D6D6D6", lw=3.2, solid_capstyle="round", zorder=2)


def head_label(ax, x, text, color, ha="center", weight="bold"):
    """A direct label above the first row: the coloured word that replaces a legend entry."""
    top = ax.get_ylim()[1]
    ax.text(x, -0.5 + 0.55 * (top + 0.5), text, ha=ha, va="center", fontsize=12, color=color, weight=weight)


def band(ax, lo, hi, n, word=None):
    ax.add_patch(Rectangle((lo, -0.5), hi - lo, n, color=BAND, zorder=0.5, lw=0))
    if word:
        ax.text((lo + hi) / 2, n - 0.5 - 0.12, word, ha="center", va="bottom", fontsize=10.5, color=MUTED, zorder=1)


def vrule(ax, x, n, word=None, ha="left"):
    ax.plot([x, x], [n - 0.5, -0.5], color="#8C8C8C", ls=(0, (4, 3)), lw=1.1, zorder=1)
    if word:
        ax.text(x + (0.01 if ha == "left" else -0.01) * (ax.get_xlim()[1] - ax.get_xlim()[0]), n - 0.5 - 0.1, word,
                ha=ha, va="bottom", fontsize=10.5, color=MUTED)  # fmt: skip
