"""late_read: finding 4, "A lookup ends in a late attention read of the answer's sentence" (Dan's figure guide 6a).

late_read_main: one dot plot. Rows = models (hybrids, then attention-only); x = % of lookups still right with the
answer's sentence hidden from the tokens after the question (the chat template's tokens up to the answer:
attn_knockout's "final" destination), in every attention layer (every layer on attention-only models); one
panel per setting: the three scene sets (a dot each, stacked in the row), table, JSON, long context. A dot is the
model's marker (filled = hybrid, hollow = attention-only) with a thin 95% interval, a small grey tick the off-path
sentence hidden instead, a light grey band chance (per cell, from its control text). Only the exceptions carry a value
label: a cell that fails the rule or stays above its chance. A cell with no value, or (MAIN) a failed control, is a
short grey word.
late_read_full: the same with the prose format, every model, not-interpretable cells in pale grey, the rule in the
caption.
late_read_deltanet_main: the hybrids only: the sentence hidden in every attention layer (grey) against every DeltaNet
layer instead (the accent), a dot per setting.

Every number is from grid.csv: a cell's value via common.cell_number; a control's number (chance, the off-path
sentence, the DeltaNet layers) from the cell's control text (readme_build.CONTROLS patterns), recorded with source
CONTROL_TEXT and its pattern, so control_mismatches can re-read it. digit_not_name draws the same layout with these
helpers.

uv run python -m scripts.figs.late_read [--grid results/cross_model/<stamp>] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bridge_jspace import plot_style as PS
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C

F = "f4"
STEM, STEM_DN = "late_read", "late_read_deltanet"
CONTROL_TEXT = "grid.csv control text"  # Number.source of a control's number; common.check_numbers skips it
DRAWS = ("draw 1", "draw 2", "draw 3")
SHOWN = ("holds", "fails", "inconclusive", "open")  # cells drawn as data (FULL: "not interpretable" too, pale)
PALE = C.CONTROL  # a not-interpretable cell's data (FULL only)
# readme_build.reason's words, shorter, for a cell drawn as a grey word
STATUS = {"still running": "running", "too few items answered right": "too few items", "not on Zach's branch": "not run",
          "too few usable scenes": "too few scenes", "no layer to test": "no layer"}  # fmt: skip


@dataclass(frozen=True)
class Panel:
    title: str
    settings: tuple[str, ...]  # grid settings drawn in the panel (several: stacked in the row)


MAIN_PANELS = (Panel("Scene sets 1-3", DRAWS), Panel("Table", ("table",)), Panel("JSON", ("JSON",)),
               Panel("Long context", ("long context",)))  # fmt: skip
FULL_PANELS = (MAIN_PANELS[0], Panel("Prose", ("prose",)), *MAIN_PANELS[1:])


@dataclass(frozen=True)
class Control:
    """A number in a cell's control text: group 1 of `pattern` is the value, groups 2-3 (when present) its interval."""

    name: str
    pattern: str
    what: str
    short: str = ""  # its words in a value label


CHANCE = Control("chance", RB.CONTROLS["f4"]["chance"], "chance, % (1 / the listed answers)")
OFF = Control(
    "another sentence", RB.CONTROLS["f4"]["another sentence"], "% right, the off-path sentence hidden instead"
)
DELTANET = Control("DeltaNet", RB.CONTROLS["f4"]["DeltaNet"], "% right, hidden in every DeltaNet layer instead",
                   "DeltaNet")  # fmt: skip


def cell(b: RB.Book, f: str, m: str, setting: str) -> RD.Cell | None:
    return next((c for c in b.of(f, m) if c.setting == setting and c.part == ""), None)


def control(c: RD.Cell, ctl: Control) -> C.Number | None:
    """The control's number in the cell's control text, keyed by the cell; None when the text has none."""
    x = re.search(ctl.pattern, c.control)
    if x is None:
        return None
    ci = (float(x.group(2)), float(x.group(3))) if x.re.groups >= 3 and x.group(2) is not None else None
    return C.Number(float(x.group(1)), ctl.what, c.finding, c.model, c.setting, c.part, ci, c.n, CONTROL_TEXT,
                    {"control": ctl.name, "pattern": ctl.pattern})  # fmt: skip


def control_mismatches(path: Path, b: RB.Book) -> list[str]:
    """common.check_numbers for the numbers read from a cell's control text: each must be what its pattern finds."""
    bad = []
    for d in json.loads(path.read_text()):
        if d["source"] != CONTROL_TEXT:
            continue
        c = cell(b, d["finding"], d["model"], d["setting"])
        x = re.search(d["extra"]["pattern"], c.control) if c else None
        if x is None or abs(float(x.group(1)) - d["value"]) > 1e-9:
            bad.append(f"{path.name}: {d['finding']} {d['model']} {d['setting']} {d['extra']['control']}")
    return bad


def status(cells: list[RD.Cell]) -> str:
    """The grey word of a cell drawn without data."""
    if any(c.word == "not interpretable" for c in cells):
        return "control failed"
    why = RB.reason(cells) if cells else "not in the grid"
    return STATUS.get(why, why)


def pct(x: float) -> str:
    return f"{RD.r0(x)}%"


def span(xs: list[float]) -> str:
    lo, hi = RD.r0(min(xs)), RD.r0(max(xs))
    return f"{lo}%" if lo == hi else f"{lo}-{hi}%"


def setting_words(settings: list[str]) -> str:
    """'scene sets 1-2, JSON' (grid settings in plain words; draws merged)."""
    draws = [s.split()[1] for s in settings if s in DRAWS]
    rest = [s for s in settings if s not in DRAWS]
    out = []
    if draws:
        nums = "-".join((draws[0], draws[-1])) if len(draws) > 1 and int(draws[-1]) - int(draws[0]) == len(draws) - 1 else ", ".join(draws)  # fmt: skip
        out.append(f"scene set{'s' if len(draws) > 1 else ''} {nums}")
    return ", ".join(out + rest)


# ---------------------------------------------------------------- the dot plot (shared with digit_not_name)


@dataclass(frozen=True)
class Dots:
    """What a dot plot draws per cell: the cell's value as the model's dot, optional controls beside it."""

    finding: str
    what: str  # the dot's meaning in the data file
    tick: Control | None = None  # a small grey tick
    second: Control | None = None  # a second mark in the model's colors (a diamond), with its interval
    why: Callable[[RD.Cell], Control | None] | None = None  # a failing cell whose label is a control's number


def above_chance(c: RD.Cell) -> bool:
    ch = control(c, CHANCE)
    return ch is not None and c.value is not None and c.value > ch.value


def exception(c: RD.Cell) -> bool:
    """A cell that carries a value label: it fails the rule or stays above its chance."""
    return c.word == "fails" or above_chance(c)


def setup(ax: Any, title: str, keys: list[str], first: bool) -> dict[str, float]:
    ys = C.model_rows(ax, keys, gap=1.1, label=first)
    ax.set_ylim(ax.get_ylim()[0], -1.3)  # the first group heading stays inside the panel, under its title
    if not first:
        ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-6, 106)
    ax.set_xticks([0, 50, 100], ["0", "50", "100%"])
    ax.set_title(title, loc="left", fontsize=C.LABEL, color=C.INK, pad=6, fontweight="bold")
    return ys


def title_room(fr: C.Frame) -> None:
    """Lower the panels' tops by a panel title's height (common.frame leaves room for the header only) and give the
    x label's room (common.frame reserves it; these panels have none: the subtitle and the 100% tick say it) back."""
    pt = 1 / 72 / fr.fig.get_figheight()
    top, bottom = (C.LABEL * 1.4 + 8) * pt, (C.LABEL * 1.8 + 4) * pt
    for ax in fr.axes:
        p = ax.get_position()
        ax.set_position((p.x0, p.y0 - bottom, p.width, p.height - top + bottom))


def place(ax: Any, y: float, lo: float, hi: float, text: str, gid: str = "value") -> bool:
    """A label right of [lo, hi] in the row, else left of it; none when neither side stays in the panel and off every
    mark (the caption names every labelled cell, so a label left out loses no information)."""
    fig = ax.figure
    r = PS.renderer(fig)
    box = ax.get_window_extent(r)
    marks = [m for _, m in PS.graphic_boxes(fig, r)]
    for x, ha in ((hi + 3, "left"), (lo - 3, "right")):
        t = ax.text(x, y, text, ha=ha, fontsize=C.NOTE, color=C.INK, va="center", gid=gid)
        e = t.get_window_extent(r).padded(2)
        if e.x0 >= box.x0 and e.x1 <= box.x1 and not any(e.overlaps(m) for m in marks):
            return True
        t.remove()
    return False


def dot_panel(ax: Any, b: RB.Book, dots: Dots, panel: Panel, ys: dict[str, float], kind: str,
              numbers: list[C.Number]) -> None:  # fmt: skip
    """One panel: per model row, its cells of the panel's settings (several stacked), their controls and chance."""
    k = len(panel.settings)
    off = {s: (i - (k - 1) / 2) * 0.3 for i, s in enumerate(panel.settings)}
    size = 11 if k == 1 else 9
    chances: list[tuple[float, float]] = []  # (row y, chance)
    for m, y in ys.items():
        cells = [c for s in panel.settings if (c := cell(b, dots.finding, m, s)) is not None]
        shown = [c for c in cells if c.value is not None and (c.word in SHOWN or (kind == "full" and c.word == "not interpretable"))]  # fmt: skip
        if not shown:
            ax.text(0, y, status(cells), fontsize=C.NOTE, color=C.CAPTION_INK, style="italic", va="center",
                    ha="left", gid="status")  # fmt: skip
            continue
        his, los = [], []
        for c in shown:
            yy = y + off[c.setting]
            pale = c.word == "not interpretable"
            num = C.cell_number(b, dots.finding, m, c.setting, dots.what)
            assert num is not None
            assert c.value is not None
            numbers.append(num)
            lo, hi = c.ci or (c.value, c.value)
            color = PALE if pale else C.MODEL[m].color
            ax.plot([lo, hi], [yy, yy], color=color, lw=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"],
                    solid_capstyle="butt", gid="ci", zorder=2)  # fmt: skip
            mk = C.marker(m, size)
            if pale:
                mk.update(markerfacecolor="white", markeredgecolor=PALE)
            ax.plot([c.value], [yy], **mk, gid="mark", zorder=4)
            if not pale:
                his.append(hi)
                los.append(lo)
            if (ch := control(c, CHANCE)) is not None:
                numbers.append(ch)
                chances.append((y, ch.value))
            if dots.tick and (t := control(c, dots.tick)) is not None:
                numbers.append(t)
                ax.plot([t.value], [yy], marker="|", markersize=size + 5, markeredgewidth=2.4, color=C.CONTROL,
                        linestyle="none", gid="tick", zorder=3)  # fmt: skip
            if dots.second and (s2 := control(c, dots.second)) is not None:
                numbers.append(s2)
                if s2.ci:
                    ax.plot(list(s2.ci), [yy, yy], color=color, lw=C.ERRORBAR["elinewidth"],
                            alpha=C.ERRORBAR["alpha"], solid_capstyle="butt", gid="ci", zorder=2)  # fmt: skip
                ax.plot([s2.value], [yy], **{**mk, "marker": "D", "markersize": size - 1}, gid="mark", zorder=4)
        judged = [c for c in shown if c.word != "not interpretable"]
        if any(exception(c) for c in judged):
            fail = next((c for c in judged if c.word == "fails" and dots.why and dots.why(c)), None)
            why = dots.why(fail) if fail and dots.why else None
            n = control(fail, why) if fail is not None and why is not None else None
            if why is not None and n is not None:
                if place(ax, y, min(los), max(his), f"{why.short} {pct(n.value)}") and n not in numbers:
                    numbers.append(n)  # the failing control's number, drawn only in its label
            else:
                place(ax, y, min(los), max(his), span([c.value for c in judged if c.value is not None]))
    band(ax, chances)


def band(ax: Any, chances: list[tuple[float, float]]) -> None:
    """The chance band: one across the panel when every cell's chance is the same, else one per row."""
    values = {v for _, v in chances}
    if len(values) == 1:
        C.chance_band(ax, values.pop())
        return
    for y, v in set(chances):
        ax.fill_betweenx([y - 0.5, y + 0.5], v - 1, v + 1, color=C.CHANCE, lw=0, zorder=0)


def fail_kind(c: RD.Cell, why: Callable[[RD.Cell], Control | None] | None) -> str:
    """How a failing cell fails: 'on <control>' (its value passes, a control named by `why` does not), '≈ chance' (the
    value is over the rule's bar but its interval covers the cell's chance), or '' (plainly)."""
    if why is not None and (ctl := why(c)) is not None:
        return f"on {ctl.short}"
    ch = control(c, CHANCE)
    return "≈ chance" if ch is not None and c.ci is not None and c.ci[0] <= ch.value <= c.ci[1] else ""


HOLDS_ABOVE = "holds above chance"


def exception_words(b: RB.Book, f: str, settings: tuple[str, ...],
                    why: Callable[[RD.Cell], Control | None] | None = None) -> list[str]:  # fmt: skip
    """['Fail at ≈ chance: 27B (long context), Gemma (scene sets 1-2, JSON).', 'Fail on DeltaNet: Olmo-Hybrid
    (table).']: the labelled cells (exception()), grouped by how they fail, a holding cell above chance last; models
    in ORDER. 'No cell fails the rule.' comes first when none fails."""
    groups: dict[str, list[str]] = {}
    for m in C.MODELS:
        by: dict[str, list[str]] = {}
        for s in settings:
            c = cell(b, f, m.key, s)
            if c is not None and c.word == "fails":
                by.setdefault(fail_kind(c, why), []).append(s)
            elif c is not None and c.word == "holds" and above_chance(c):
                by.setdefault(HOLDS_ABOVE, []).append(s)
        for kind, ss in by.items():
            groups.setdefault(kind, []).append(f"{m.short} ({setting_words(ss)})")
    head = {"≈ chance": "Fail at ≈ chance", "": "Fail", HOLDS_ABOVE: "Hold above chance"}
    order = sorted(groups, key=lambda k: (k == HOLDS_ABOVE, k != "≈ chance", k != "", k))
    out = [f"{head.get(k, 'Fail ' + k)}: {', '.join(groups[k])}." for k in order]
    return out if any(k != HOLDS_ABOVE for k in groups) else ["No cell fails the rule.", *out]


def n_range(numbers: list[C.Number]) -> str:
    ns = [n.n for n in numbers if n.source == "grid.csv" and n.n is not None]
    return f"n = {min(ns)}-{max(ns)}" if ns and min(ns) != max(ns) else (f"n = {ns[0]}" if ns else "")


def rows_of(b: RB.Book, f: str, panels: tuple[Panel, ...], kind: str) -> list[str]:
    """Models with a drawn cell in some panel (MAIN: a judged one), in ORDER."""
    ok = SHOWN if kind == "main" else (*SHOWN, "not interpretable")
    return [m.key for m in C.MODELS
            if any(c.value is not None and c.word in ok for p in panels for s in p.settings
                   if (c := cell(b, f, m.key, s)) is not None)]  # fmt: skip


def dot_figure(b: RB.Book, dots: Dots, panels: tuple[Panel, ...], kind: str, title: str, subtitle: str, how: str,
               caption: Callable[[list[C.Number]], list[str]], stem: str, out: Path) -> list[Path]:  # fmt: skip
    """Draw the panels, then the caption (it quotes the drawn cells' n), check overlaps, save."""
    keys = rows_of(b, dots.finding, panels, kind)
    numbers: list[C.Number] = []
    # the caption quotes the drawn numbers' n: two lines are reserved, the text is set after drawing
    fr = C.frame(kind, title, subtitle, how=how, caption="x\nx", ncols=len(panels), wspace=0.26, left=0.155,
                 right=0.975)  # fmt: skip
    title_room(fr)
    for i, (ax, p) in enumerate(zip(fr.axes, panels, strict=True)):
        ys = setup(ax, p.title, keys, first=i == 0)
        dot_panel(ax, b, dots, p, ys, kind, numbers)
    cap = next(t for t in fr.fig.texts if t.get_gid() == "caption")
    cap.set_text(pack(fr.fig, caption(numbers)))
    return C.save(fr, stem, numbers, out)


# ---------------------------------------------------------------- finding 4


def why_f4(c: RD.Cell) -> Control | None:
    """A late-read cell failing on its DeltaNet control (the value itself passes): labelled with that control."""
    return DELTANET if "DeltaNet" in c.verdict else None


DOTS = Dots(F, "% right, the answer's sentence hidden from the tokens after the question", tick=OFF, why=why_f4)
TITLE = "Blocking the late read drops lookups to chance"
SUBTITLE = "% of lookups right with the answer's sentence hidden from the tokens after the question"
HOW = "left = the lookup breaks. Grey band = chance; grey tick = another sentence hidden."


FILLED = "Filled = hybrid, hollow = attention-only."


def caption(b: RB.Book, f: str, panels: tuple[Panel, ...], why: Callable[[RD.Cell], Control | None] | None,
            rule: str, kind: str) -> Callable[[list[C.Number]], list[str]]:  # fmt: skip
    """The caption's sentences, in order: the labelled cells (exception_words), the untested models; MAIN: n, where
    the prose format is, the markers; FULL: the rule, pale = a control failed, n, the markers."""
    settings = tuple(s for p in panels for s in p.settings)

    def cap(numbers: list[C.Number]) -> list[str]:
        head = exception_words(b, f, settings, why) + ([u] if (u := C.not_tested(b, f)) else [])
        if kind == "main":
            return [*head, f"{n_range(numbers)} per dot; the prose format is in the full figure.", FILLED]
        return [*head, f"Rule: {rule}.", "Pale = control failed.", f"{n_range(numbers)}.", FILLED]

    return cap


def pack(fig: Any, sentences: list[str]) -> str:
    """The sentences in at most two caption lines that fit the figure's width (measured, not counted): one line if
    it fits, else the two-line split that keeps the first sentence first and moves the fewest sentences out of their
    order (then the fullest first line). A few sentences, so every split is tried."""
    room = (0.985 - 0.03) * fig.get_figwidth()
    width: dict[str, bool] = {}

    def fits(s: str) -> bool:
        if s not in width:
            width[s] = PS.text_width(fig, s, C.CAPTION) <= room
        return width[s]

    if fits(" ".join(sentences)):
        return " ".join(sentences)
    best: tuple[tuple[int, int], str] | None = None
    n = len(sentences)
    for mask in range(1, (1 << n) - 1, 2):  # bit i: sentence i on the first line; bit 0 always
        one = [i for i in range(n) if mask >> i & 1]
        two = [i for i in range(n) if not mask >> i & 1]
        l1, l2 = " ".join(sentences[i] for i in one), " ".join(sentences[i] for i in two)
        if fits(l1) and fits(l2):
            key = (sum(i > two[0] for i in one), -len(l1))
            if best is None or key < best[0]:
                best = (key, f"{l1}\n{l2}")
    if best is None:
        raise ValueError(f"the caption does not fit two lines: {sentences}")
    return best[1]


RULE = "≤ 20% (CI ≤ 30%), controls ≥ 90%"


def late_read(b: RB.Book, kind: str, out: Path = C.OUT) -> list[Path]:
    panels = MAIN_PANELS if kind == "main" else FULL_PANELS
    return dot_figure(b, DOTS, panels, kind, TITLE, SUBTITLE, HOW, caption(b, F, panels, why_f4, RULE, kind), STEM,
                      out)  # fmt: skip


# ---------------------------------------------------------------- the DeltaNet figure (hybrids only)

DN_TITLE = "Hiding it in the DeltaNet layers changes nothing"
DN_SUBTITLE = "Hybrids: % of lookups still right, the sentence hidden from the tokens after the question"


def deltanet(b: RB.Book, out: Path = C.OUT) -> list[Path]:
    """The hybrids' cells with a DeltaNet control: hidden in every attention layer (grey) vs every DeltaNet layer."""
    settings = G.FINDING[F].settings
    pairs: dict[str, list[tuple[RD.Cell, C.Number]]] = {}
    for m in C.MODELS:
        if not m.hybrid:
            continue
        for s in settings:
            c = cell(b, F, m.key, s)
            if c is not None and c.value is not None and c.word in SHOWN and (dn := control(c, DELTANET)) is not None:
                pairs.setdefault(m.key, []).append((c, dn))
    numbers: list[C.Number] = []
    fr = C.frame("main", DN_TITLE, DN_SUBTITLE, how="a dot per setting (scene sets, formats, long context); "
                 "most overlap at 100%.", caption="x\nx", left=0.2, right=0.95)  # fmt: skip
    ax = fr.axes[0]
    ys = C.model_rows(ax, list(pairs))
    for t in [t for t in ax.texts if t.get_gid() == "group"]:
        t.remove()  # every row is a hybrid: the subtitle says it
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-3, 103)
    ax.set_xticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
    ax.set_xlabel("% right", fontsize=C.LABEL)
    slot = {s: (i - (len(settings) - 1) / 2) * 0.09 for i, s in enumerate(settings)}
    for m, y in ys.items():
        for c, dn in pairs[m]:
            yy = y + slot[c.setting]
            num = C.cell_number(b, F, m, c.setting, "% right, hidden in every attention layer")
            assert num is not None
            numbers += [num, dn]
            ax.plot([num.value], [yy], marker="o", markersize=9, color=C.CONTROL, linestyle="none", gid="mark",
                    zorder=3)  # fmt: skip
            ax.plot([dn.value], [yy], marker="o", markersize=12, color=C.LOOKUP, linestyle="none", gid="mark",
                    zorder=4)  # fmt: skip
        low = [(c, dn) for c, dn in pairs[m] if dn.value < 90]  # the rule's bar: hidden in DeltaNet keeps >= 90%
        for c, dn in low:
            ax.text(dn.value - 3, y + slot[c.setting], f"{setting_words([c.setting])}: {pct(dn.value)}",
                    ha="right", va="center", fontsize=C.NOTE, color=C.INK, gid="value")  # fmt: skip
    top = min(ys.values()) - 0.68  # direct labels above the first row, at the two clusters' ends
    ax.text(0, top, "hidden in the attention layers", ha="left", va="center", fontsize=C.NOTE, color=C.CAPTION_INK,
            gid="label")  # fmt: skip
    ax.text(100, top, "hidden in the DeltaNet layers", ha="right", va="center", fontsize=C.NOTE, color=C.LOOKUP,
            gid="label")  # fmt: skip
    ns = [c.n for cs in pairs.values() for c, _ in cs if c.n is not None]
    cap = next(t for t in fr.fig.texts if t.get_gid() == "caption")
    cap.set_text(pack(fr.fig, ["Rule: hidden in every DeltaNet layer keeps ≥ 90%.",
                               "Attention-only models have no DeltaNet layers.",
                               f"n = {min(ns)}-{max(ns)} per dot; cells whose off-path control failed are left out."]))  # fmt: skip
    return C.save(fr, STEM_DN, numbers, out)


# ---------------------------------------------------------------- command line


def newest_grid(root: Path = G.OUT) -> Path:
    hits = sorted(p.parent for p in root.glob("*/grid.csv"))
    if not hits:
        raise SystemExit(f"no grid.csv under {root}: run scripts/cross_model_grid.py first")
    return hits[-1]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=None, help="a results/cross_model/<stamp> folder (default: the newest)")
    ap.add_argument("--only", choices=("main", "full"), default=None, help="one version (default: both)")
    ap.add_argument("--out", default=str(C.OUT), help="output folder (default figures/cross_model)")
    a = ap.parse_args(argv)
    b = RB.Book(Path(a.grid) if a.grid else newest_grid())
    out = Path(a.out)
    for kind in ("main", "full") if a.only is None else (a.only,):
        for p in late_read(b, kind, out) + (deltanet(b, out) if kind == "main" else []):
            print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
