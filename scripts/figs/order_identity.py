"""order_identity: finding 5 (Dan's figure guide, 6c): the last two tokens carry the place in the list for the 1st and
2nd sentence, the bridge's identity from the 3rd on.

Every number is a grid.csv cell of finding 5: per model and setting (scene sets 1-3 of the 5-sentence lists, 8 and 12
sentences) two parts, "1st-2nd" (position - identity, points) and "3rd on" (identity - position, points). Both parts
are drawn as ONE quantity, position minus identity, so the 3rd-on part is drawn negated (below 0 where identity wins);
the data file keeps the grid's value and records the drawn one as extra["drawn"].

MAIN: the 27B, 122B, 32B and OLMo-3 at the 5-sentence lists (one dot per scene set) and one inset with the same models
at 12 sentences. FULL: every model with a value, all list lengths (5 = the darkest shade of the model's color, 8, 12
lighter; distinct markers). A failing part gets the small grey word "fails" (MAIN) and is named in the caption; a part
whose control failed is drawn grey.

uv run python scripts/figs/order_identity.py --grid results/cross_model/<stamp> [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bridge_jspace import plot_style as PS
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C

STEM = "order_identity"
F = "f5"
PARTS = ("1st-2nd", "3rd on")
SIGN = {"1st-2nd": 1, "3rd on": -1}  # drawn = SIGN * grid value: position minus identity for both parts
WHAT = {"1st-2nd": "position - identity, points", "3rd on": "identity - position, points (drawn negated)"}
PART_LABEL = {"1st-2nd": "1st–2nd", "3rd on": "3rd on"}
MAIN_MODELS = ("27b", "122b", "32b", "olmo")
POS_BG, ID_BG = "#f4f0f9", "#eef4f2"  # very light: above 0 "position wins", below 0 "identity wins"
SIDE = -46  # points left of a row's first panel: the side labels (right of them: the y tick labels)

TITLE = "Position wins for sentences 1–2, identity after"
SUBTITLE = "Last two tokens swapped in: % answers at the same place minus % at the donor's entity"
HOW = "Both parts drawn as place minus entity: up = position wins, down = identity wins."
MARKS = "Filled = hybrid, hollow = attention-only; bars: 95% CI."


@dataclass(frozen=True)
class ListLen:
    n: str  # sentences per list
    settings: tuple[str, ...]  # grid settings
    shape: str
    tint: float  # mixed toward white: 0 = the model's own color (5 sentences, the darkest)


LISTS = (ListLen("5", ("draw 1", "draw 2", "draw 3"), "o", 0.0), ListLen("8", ("8 sentences",), "s", 0.28),
         ListLen("12", ("12 sentences",), "^", 0.5))  # fmt: skip
LIST = {li.n: li for li in LISTS}


def tint(hex_color: str, t: float) -> str:
    rgb = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    return "#" + "".join(f"{round((c + (1 - c) * t) * 255):02x}" for c in rgb)


def cell(b: RB.Book, m: str, setting: str, part: str) -> RD.Cell | None:
    return next((c for c in b.of(F, m) if c.setting == setting and c.part == part and c.value is not None), None)


def has_values(b: RB.Book, m: str, settings: tuple[str, ...]) -> bool:
    return any(cell(b, m, s, p) for s in settings for p in PARTS)


def failed(c: RD.Cell) -> bool:
    """This part failed its half of the rule (A: 1st-2nd, B: 3rd on; grid.csv's control text says 'A: False')."""
    return c.word == "fails" and ": False" in c.control


@dataclass
class Facts:
    """What the caption says about the cells a figure draws."""

    fails: list[str] = field(default_factory=list)  # "32B scene set 1, 3rd on"
    unclear: list[str] = field(default_factory=list)
    ns: list[int] = field(default_factory=list)

    @property
    def n_range(self) -> str:
        if not self.ns:
            return "–"
        lo, hi = min(self.ns), max(self.ns)
        return f"{lo}–{hi}" if lo != hi else str(lo)

    @property
    def sentences(self) -> list[str]:
        out = []
        if self.fails:
            out.append("Fails the rule: " + "; ".join(self.fails) + ".")
        if self.unclear:
            out.append("Grey: a control failed (" + "; ".join(self.unclear) + ").")
        return out


def facts(b: RB.Book, keys: list[str], settings: tuple[str, ...]) -> Facts:
    """The failing parts and the not-interpretable settings (a setting's verdict covers both its parts), the n's."""
    out = Facts()
    for k in keys:
        for s in settings:
            where = f"{C.MODEL[k].short} {RB.show(s)}"
            for p in PARTS:
                c = cell(b, k, s, p)
                if c is None:
                    continue
                if c.n is not None:
                    out.ns.append(c.n)
                if c.word == "not interpretable":
                    if where not in out.unclear:
                        out.unclear.append(where)
                elif failed(c):
                    out.fails.append(f"{where}, {PART_LABEL[p]}")
    return out


def pack(sentences: list[str], width: float = 11.5) -> str:
    """The caption's sentences, greedily packed into lines of at most `width` inches as drawn (frame() refuses more
    than two lines)."""
    C.apply()
    fig = Figure(dpi=C.DPI)
    FigureCanvasAgg(fig)
    lines = [""]
    for s in (x for x in sentences if x):
        joined = f"{lines[-1]} {s}".strip()
        if lines[-1] and PS.text_width(fig, joined, C.CAPTION) > width:
            lines.append(s)
        else:
            lines[-1] = joined
    return "\n".join(lines)


def missing_text(b: RB.Book, keys: list[str], settings: tuple[str, ...]) -> str:
    """'Not run: Olmo-Hybrid scene set 3; Gemma 8 and 12 sentences.': settings without a value, by reason."""
    by: dict[str, list[str]] = {}
    for k in keys:
        gone = [s for s in settings if not any(cell(b, k, s, p) for p in PARTS)]
        if not gone:
            continue
        reason = RB.reason([c for c in b.of(F, k) if c.setting in gone])
        shown = [RB.show(s) for s in gone]
        if len(shown) > 1 and all(s.endswith(" sentences") for s in shown):
            shown = [" and ".join(s.removesuffix(" sentences") for s in shown) + " sentences"]
        by.setdefault(reason, []).append(f"{C.MODEL[k].short} {', '.join(shown)}")
    return " ".join(f"{r[0].upper()}{r[1:]}: {'; '.join(v)}." for r, v in by.items())


def dot(ax, b: RB.Book, m: str, setting: str, part: str, x: float, li: ListLen, numbers: list[C.Number],
        size: float) -> RD.Cell | None:  # fmt: skip
    """One grid cell as a dot at x with its interval, drawn as position minus identity; None when it has no value."""
    c = cell(b, m, setting, part)
    num = C.cell_number(b, F, m, setting, WHAT[part], part)
    if c is None or num is None:
        return None
    s = SIGN[part]
    y = s * num.value
    num.extra = {"drawn": y, "list": li.n}
    numbers.append(num)
    color = C.CONTROL if c.word == "not interpretable" else tint(C.MODEL[m].color, li.tint)
    if num.ci is not None:
        lo, hi = sorted(s * v for v in num.ci)
        ax.plot([x, x], [lo, hi], color=color, lw=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"],
                solid_capstyle="butt", gid="ci", zorder=2)  # fmt: skip
    style = C.marker(m, size, li.shape)
    style["markeredgecolor"] = color
    style["markerfacecolor"] = color if C.MODEL[m].hybrid else "white"
    ax.plot([x], [y], gid="mark", zorder=3, **style)
    return c


def y_range(b: RB.Book, keys: list[str]) -> tuple[float, float]:
    vals = [SIGN[c.part] * v for k in keys for c in b.of(F, k) if c.ci and c.value is not None for v in c.ci]
    return min(-60.0, min(vals, default=0) - 6), max(100.0, max(vals, default=0) + 6)


def base(ax, ylim: tuple[float, float], *, first: bool) -> None:
    """The two shaded halves, the zero line, the y scale (tick labels and side labels on a row's first panel)."""
    ax.axhspan(0, ylim[1], color=POS_BG, lw=0, zorder=0)
    ax.axhspan(ylim[0], 0, color=ID_BG, lw=0, zorder=0)
    ax.axhline(0, color=C.INK2, lw=0.9, zorder=1)
    ax.set_ylim(*ylim)
    ys = [v for v in (-50, 0, 50, 100) if ylim[0] <= v <= ylim[1]]
    ax.set_yticks(ys, [(f"{v:+d}".replace("-", "−") if v else "0") for v in ys])  # shared: hidden per panel below
    ax.tick_params(axis="y", length=3.5 if first else 0, labelleft=first)
    ax.tick_params(axis="x", length=0)
    ax.spines["left"].set_visible(first)
    if first:
        for text, y in (("position\nwins", 75), ("identity\nwins", -25)):  # between the ticks (y_range: -60..100 in)
            ax.annotate(text, xy=(0, y), xycoords=ax.get_yaxis_transform(), xytext=(SIDE, 0),
                        textcoords="offset points", ha="right", va="center", fontsize=C.NOTE, color=C.CAPTION_INK,
                        gid="side")  # fmt: skip


def parts_axis(ax) -> None:
    ax.set_xlim(-0.5, 1.5)
    ax.set_xticks([0, 1], [PART_LABEL[p] for p in PARTS])


def room_for_titles(fr: C.Frame, pts: float = 30, bottom: float = 0) -> None:
    """Lower the panels' top by `pts` points (frame() places the panels right under the header, with no room for the
    panel titles above them) and move their bottom by `bottom` points."""
    gs = fr.axes[0].get_subplotspec().get_gridspec()
    pt = 1 / 72 / fr.fig.get_figheight()
    gs.update(top=gs.top - pts * pt, bottom=gs.bottom + bottom * pt)
    for ax in fr.axes:
        ax.set_position(ax.get_subplotspec().get_position(fr.fig))


def title(ax, m: str) -> None:
    ax.set_title(C.MODEL[m].name, fontsize=C.LABEL, fontweight="bold", color=C.MODEL[m].color, pad=8)


def fails_word(ax, x: float, y: float, part: str) -> None:
    """The verdict as a small grey word beside the failing dot, on the side of the gap between the two parts."""
    left = part == "3rd on"
    ax.annotate("fails", xy=(x, y), xytext=(-14 if left else 14, 0), textcoords="offset points",
                ha="right" if left else "left", va="center", fontsize=C.NOTE, color=C.CAPTION_INK, gid="status")  # fmt: skip


def draw_main(b: RB.Book, out: Path = C.OUT) -> list[Path]:
    five, twelve = LIST["5"], LIST["12"]
    keys = [k for k in MAIN_MODELS if has_values(b, k, five.settings)]
    if not keys:
        raise ValueError("no model of the MAIN figure has a 5-sentence value")
    inset = [k for k in keys if has_values(b, k, twelve.settings)]
    fx, f12 = facts(b, keys, five.settings), facts(b, inset, twelve.settings)
    both = Facts(fx.fails + f12.fails, fx.unclear + f12.unclear)  # each named with its setting
    caption = pack([*both.sentences, f"n = {fx.n_range} items per dot (12 sentences: {f12.n_range}); memory → "
                    "prompt lookups.", missing_text(b, keys, five.settings + twelve.settings),
                    C.not_tested(b, F, MAIN_MODELS),
                    "Inset: 12-sentence lists, same models in the same order." if inset else "", MARKS])  # fmt: skip
    fr = C.frame("main", TITLE, SUBTITLE, how=HOW, caption=caption, ncols=4, sharey=True, left=0.135, right=0.79,
                 wspace=0.12)  # fmt: skip
    room_for_titles(fr)
    ylim = y_range(b, keys)
    numbers: list[C.Number] = []
    offsets = (-0.16, 0.0, 0.16)
    for i, ax in enumerate(fr.axes):
        if i >= len(keys):
            ax.remove()
            continue
        k = keys[i]
        base(ax, ylim, first=i == 0)
        for s, dx in zip(five.settings, offsets, strict=True):
            for xi, p in enumerate(PARTS):
                c = dot(ax, b, k, s, p, xi + dx, five, numbers, 12)
                if c is not None and c.value is not None and failed(c):
                    fails_word(ax, xi + (offsets[0] if p == "3rd on" else offsets[-1]), SIGN[p] * c.value, p)
        parts_axis(ax)
        title(ax, k)
    first, last = fr.axes[0].get_position(), fr.axes[len(keys) - 1].get_position()
    fr.fig.text((first.x0 + last.x1) / 2, first.y0 - 0.075, "Sentence asked about, in 5-sentence lists (one dot per "
                "scene set)", ha="center", va="top", fontsize=C.LABEL, gid="xlabel")  # fmt: skip
    if inset:
        ins = fr.fig.add_axes((0.835, last.y0, 0.14, last.height), sharey=fr.axes[0])
        base(ins, ylim, first=False)
        ins.spines["left"].set_visible(True)
        step = 0.54 / max(len(inset) - 1, 1)
        for j, k in enumerate(inset):
            dx = -0.27 + step * j if len(inset) > 1 else 0.0
            for xi, p in enumerate(PARTS):
                dot(ins, b, k, twelve.settings[0], p, xi + dx, twelve, numbers, 10)
        parts_axis(ins)
        ins.set_title("12 sentences", fontsize=C.LABEL, fontweight="bold", color=C.INK2, pad=8)
    return C.save(fr, STEM, numbers, out)


def draw_full(b: RB.Book, out: Path = C.OUT) -> list[Path]:
    settings = tuple(s for li in LISTS for s in li.settings)
    keys = [m.key for m in C.MODELS if has_values(b, m.key, settings)]
    if not keys:
        raise ValueError("no model has a value for finding 5")
    groups = [g for g in ([k for k in keys if C.MODEL[k].hybrid], [k for k in keys if not C.MODEL[k].hybrid]) if g]
    ncols = max(len(g) for g in groups)
    fx = facts(b, keys, settings)
    caption = pack([*fx.sentences, missing_text(b, keys, settings), C.not_tested(b, F),
                    f"n = {fx.n_range}; 5 sentences: 3 scene sets; memory → prompt.", MARKS])  # fmt: skip
    fr = C.frame("full", TITLE, SUBTITLE, how=HOW, caption=caption, nrows=len(groups), ncols=ncols, size=(12.0, 10.0),
                 sharey=True, left=0.135, right=0.975, wspace=0.12, hspace=0.5)  # fmt: skip
    room_for_titles(fr, bottom=-22)  # two rows of x tick labels and no x label: the frame's x-label room is spare
    ylim = y_range(b, keys)
    numbers: list[C.Number] = []
    offsets = {"5": (-0.36, -0.26, -0.16), "8": (0.06,), "12": (0.32,)}
    center = {"5": -0.26, "8": 0.06, "12": 0.32}
    for r, g in enumerate(groups):
        for j in range(ncols):
            ax = fr.axes[r * ncols + j]
            if j >= len(g):
                ax.remove()
                continue
            k = g[j]
            base(ax, ylim, first=j == 0)
            for li in LISTS:
                for s, dx in zip(li.settings, offsets[li.n], strict=True):
                    for xi, p in enumerate(PARTS):
                        dot(ax, b, k, s, p, xi + dx, li, numbers, 9.5)
            parts_axis(ax)
            ax.set_xlim(-0.55, 1.55)
            ax.tick_params(axis="x", which="major", pad=24)
            ax.set_xticks([xi + center[li.n] for xi in range(2) for li in LISTS], [li.n for _ in range(2) for li in
                          LISTS], minor=True)  # fmt: skip
            ax.tick_params(axis="x", which="minor", length=0, pad=4, labelcolor=C.CAPTION_INK)
            title(ax, k)
            if j == 0:
                ax.annotate("sentences\nper list", xy=(0, 0), xycoords="axes fraction", xytext=(SIDE + 30, -5),
                            textcoords="offset points", ha="right", va="top", fontsize=C.NOTE, color=C.CAPTION_INK,
                            gid="side")  # fmt: skip
                top = ax.get_position().y1 + 10 / 72 / fr.fig.get_figheight()
                fr.fig.text(0.03, top, "Hybrids" if C.MODEL[k].hybrid else "Attention-only", ha="left", va="bottom",
                            fontsize=C.NOTE, color=C.CAPTION_INK, gid="group")  # fmt: skip
    return C.save(fr, STEM, numbers, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=None, help="a results/cross_model/<stamp> folder (default: the README's pin)")
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", default=None, help="output folder (default figures/cross_model)")
    a = ap.parse_args(argv)
    b = C.book(Path(a.grid).resolve() if a.grid else None)
    out = Path(a.out) if a.out else C.OUT
    for kind, draw in (("main", draw_main), ("full", draw_full)):
        if a.only in (None, kind):
            for p in draw(b, out):
                print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
