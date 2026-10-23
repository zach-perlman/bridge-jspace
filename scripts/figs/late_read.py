"""late_read: finding 4, "A lookup ends in a late attention read of the answer's sentence" (Dan's figure guide 6a).

late_read_main: one dot plot. Rows = models (hybrids, then attention-only); x = % of lookups (answers copied from a
sentence in the prompt) still right with that sentence hidden from the tokens after the question (the chat template's
tokens up to the answer: attn_knockout's "final" destination), in every attention layer (every layer on
attention-only models); one panel per setting: the three prompt sets (scene sets 1-3: a dot each, stacked in the
row), table, JSON, long context. A dot is the model's marker (filled = hybrid, hollow = attention-only) with a thin 95%
interval, a small grey tick the off-path sentence hidden instead (a control: it should stay high). The one reference
(Dan, 23 Oct 15:30) is the floor per model, not chance: % still right with the sentence hidden from EVERY token after
it (all layers: a conservative lower bound), measured on prompt set 1 only, drawn as a short dark line in that
panel's row (none yet for Muse and the 122B). Only the exceptions carry a value label, beside their dots: a cell that
fails the rule or stays above its chance. A cell failing on a control (Olmo-Hybrid's table: its DeltaNet control) is
named in the caption with the control's number. MAIN draws no words in the panels: a blank cell, a missing stacked dot
or floor is explained in the caption.
late_read_full: the same with the prose format and not-interpretable cells (and floors) in pale grey; a blank cell
carries a short grey word; the rule in the caption.
late_read_deltanet_main: the hybrids only: the sentence hidden in every attention layer (grey) against every DeltaNet
layer instead (the accent), a dot per setting stacked in the row, the rule's bar (>= 90% kept) as a light band.

Every number is from grid.csv: a cell's value via common.cell_number; a control's number (the off-path sentence, the
DeltaNet layers; chance where it is drawn, in digit_not_name) from the cell's control text (readme_build.CONTROLS
patterns), recorded with source CONTROL_TEXT and its pattern, so control_mismatches can re-read it; a floor from its
late-read-v2 breakdown row (FLOOR_SOURCE, re-read by floor_mismatches). digit_not_name draws the same layout with
these helpers.

uv run python -m scripts.figs.late_read [--grid results/cross_model/<stamp>] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
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
# the reference band (chance; the DeltaNet rule's bar): common.CHANCE is too faint at slide size (5-second test,
# 23 Oct), so a little darker here, still light
BAND = "#d9d9d9"
# readme_build.reason's words, shorter, for a cell drawn as a grey word (FULL)
STATUS = {"still running": "running", "too few items answered right": "too few items", "not on Zach's branch": "not run",
          "too few usable scenes": "too few scenes", "no layer to test": "no layer"}  # fmt: skip
BLANK_ORDER = ("control failed", "too few items", "not run")  # a blank cell's reason in the caption (MAIN)


@dataclass(frozen=True)
class Panel:
    title: str
    settings: tuple[str, ...]  # grid settings drawn in the panel (several: stacked in the row)


MAIN_PANELS = (Panel("3 prompt sets", DRAWS), Panel("Table", ("table",)), Panel("JSON", ("JSON",)),
               Panel("Long context", ("long context",)))  # fmt: skip
FULL_PANELS = (MAIN_PANELS[0], Panel("Prose", ("prose",)), *MAIN_PANELS[1:])


@dataclass(frozen=True)
class Control:
    """A number in a cell's control text: group 1 of `pattern` is the value, groups 2-3 (when present) its interval.
    `fails`: how a cell failing on this control reads in the caption ({v}: the number)."""

    name: str
    pattern: str
    what: str
    short: str = ""
    fails: str = ""


CHANCE = Control("chance", RB.CONTROLS["f4"]["chance"], "chance, % (1 / the listed answers)")
OFF = Control(
    "another sentence", RB.CONTROLS["f4"]["another sentence"], "% right, the off-path sentence hidden instead"
)
DELTANET = Control("DeltaNet", RB.CONTROLS["f4"]["DeltaNet"], "% right, hidden in every DeltaNet layer instead",
                   "DeltaNet", "fails its DeltaNet control ({v} kept)")  # fmt: skip


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


# The floor (Dan, 23 Oct 15:30): % still right with the answer's sentence hidden from EVERY token after it (the
# "after" destination, all layers: a conservative lower bound). grid.csv has it in the late-read-v2 breakdown row of the
# first prompt set only (readme_build.Book leaves breakdown rows out, so it is read here). Only that row is read: the
# second-prompt-set and long-context floor runs are unopened.
FLOOR_SETTING = "draw 1 · last tokens' share"
FLOOR_ON = "draw 1"  # the grid setting the floor was measured on: drawn in the panel that holds it
FLOOR_SOURCE = "grid.csv late-read-v2 row"  # Number.source of a floor; checked by floor_mismatches
FLOOR = Control("floor", r"from every token after it \(all layers\): (\d+)% \[(\d+), (\d+)\]",
                "% right, the answer's sentence hidden from every token after it (all layers): the floor")  # fmt: skip


@dataclass(frozen=True)
class Floor:
    number: C.Number
    word: str  # the late-read-v2 row's verdict word (not interpretable: drawn pale, FULL only)


def floor_rows(grid_dir: Path) -> dict[str, dict[str, str]]:
    """model key -> grid.csv's late-read-v2 row of the first prompt set (main lens)."""
    out = {}
    for r in csv.DictReader(io.StringIO((grid_dir / "grid.csv").read_text())):
        m = RD.MODEL_BY_LABEL.get(r["model"])
        if m and r["rule id"] == "late-read-v2" and r["setting"] == FLOOR_SETTING and not r["lens"].endswith(RD.BESIDE):
            out[m.key] = r
    return out


def floors(grid_dir: Path) -> tuple[dict[str, Floor], dict[str, str]]:
    """The floors by model, and why a model has none (its row's verdict, as blank_reason words)."""
    have, none = {}, {}
    rows = floor_rows(grid_dir)
    for m in C.MODELS:
        r = rows.get(m.key)
        x = re.search(FLOOR.pattern, r["chance or control level"]) if r else None
        if r is None or x is None:
            none[m.key] = "not run"
            continue
        word = next((w for w in G.VERDICTS if r["verdict"].startswith(w)), r["verdict"])
        n = int(r["n"]) if r["n"].strip() else None
        num = C.Number(float(x.group(1)), FLOOR.what, F, m.key, FLOOR_SETTING, "", (float(x.group(2)),
                       float(x.group(3))), n, FLOOR_SOURCE, {"control": "floor", "pattern": FLOOR.pattern})  # fmt: skip
        have[m.key] = Floor(num, word)
    return have, none


def floor_mismatches(path: Path, grid_dir: Path) -> list[str]:
    """common.check_numbers for the floors: each must be what FLOOR's pattern finds in its grid.csv row."""
    rows, bad = floor_rows(grid_dir), []
    for d in json.loads(path.read_text()):
        if d["source"] != FLOOR_SOURCE:
            continue
        r = rows.get(d["model"])
        x = re.search(d["extra"]["pattern"], r["chance or control level"]) if r else None
        if d["setting"] != FLOOR_SETTING or x is None or abs(float(x.group(1)) - d["value"]) > 1e-9:
            bad.append(f"{path.name}: floor {d['model']}")
    return bad


def status(cells: list[RD.Cell]) -> str:
    """The grey word of a cell drawn without data (FULL)."""
    if any(c.word == "not interpretable" for c in cells):
        return "control failed"
    why = RB.reason(cells) if cells else "not in the grid"
    return STATUS.get(why, why)


def blank_reason(c: RD.Cell | None) -> str:
    """Why a cell is blank, in the caption's words (BLANK_ORDER, or readme_build.reason's own)."""
    if c is None:
        return "not run"
    if c.word == "not interpretable":
        return "control failed"
    why = RB.reason([c])
    if why in ("too few items answered right", "too few usable scenes"):
        return "too few items"
    return "not run" if why in ("still running", "run failed", "not run", "no result", "not on Zach's branch") else why


def pct(x: float) -> str:
    return f"{RD.r0(x)}%"


def span(xs: list[float]) -> str:
    lo, hi = RD.r0(min(xs)), RD.r0(max(xs))
    return f"{lo}%" if lo == hi else f"{lo}-{hi}%"


def setting_words(settings: list[str]) -> str:
    """'prompt sets 1-2, JSON' (grid settings in plain words; draws merged)."""
    draws = [s.split()[1] for s in settings if s in DRAWS]
    rest = [s for s in settings if s not in DRAWS]
    out = []
    if draws:
        nums = "-".join((draws[0], draws[-1])) if len(draws) > 1 and int(draws[-1]) - int(draws[0]) == len(draws) - 1 else ", ".join(draws)  # fmt: skip
        out.append(f"prompt set{'s' if len(draws) > 1 else ''} {nums}")
    return ", ".join(out + rest)


def join_or(words: list[str]) -> str:
    return words[0] if len(words) == 1 else f"{', '.join(words[:-1])} or {words[-1]}"


# ---------------------------------------------------------------- the dot plot (shared with digit_not_name)


@dataclass(frozen=True)
class Dots:
    """What a dot plot draws per cell: the cell's value as the model's dot, optional controls beside it."""

    finding: str
    what: str  # the dot's meaning in the data file
    tick: Control | None = None  # a small grey tick
    second: Control | None = None  # a second mark in the model's colors (a diamond), with its interval
    why: Callable[[RD.Cell], Control | None] | None = None  # a failing cell's failing control (its value passes)
    reference: str = "chance"  # the one reference: "chance" (a band per panel) or "floor" (per model row, late_read)


@dataclass
class Notes:
    """What the panels leave to the caption."""

    labelled: list[RD.Cell] = field(default_factory=list)  # exceptions with a value label
    unlabelled: list[RD.Cell] = field(default_factory=list)  # exceptions whose label found no room
    on_control: list[tuple[RD.Cell, Control, C.Number]] = field(default_factory=list)  # failing on a control
    blank: set[str] = field(default_factory=set)  # why a cell (or a stacked dot) is not drawn
    fewer: bool = False  # a stacked row has fewer dots than settings
    pale: bool = False  # a not-interpretable cell (or floor) is drawn (FULL)
    no_floor: dict[str, str] = field(default_factory=dict)  # model -> why its row has no floor


def above_chance(c: RD.Cell) -> bool:
    ch = control(c, CHANCE)
    return ch is not None and c.value is not None and c.value > ch.value


def exception(c: RD.Cell) -> bool:
    """A cell that carries a value label: it fails the rule or stays above its chance."""
    return c.word == "fails" or above_chance(c)


def setup(ax: Any, title: str, keys: list[str], first: bool, label_room: bool = True) -> dict[str, float]:
    ys = C.model_rows(ax, keys, gap=1.1, label=first)
    # the first group heading stays inside the panel, under its title; `label_room`: room under the last row for the
    # chance band's label
    ax.set_ylim(max(ys.values()) + (1.55 if label_room else 0.75), -1.3)
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
    """A label just right of [lo, hi] in the row, else just left of it; none when neither side stays in the panel and
    off every mark (the caption then names the cell)."""
    fig = ax.figure
    r = PS.renderer(fig)
    box = ax.get_window_extent(r)
    marks = [m for _, m in PS.graphic_boxes(fig, r)]
    x0, x1 = ax.get_xlim()
    gap = 5 * fig.dpi / 72 * (x1 - x0) / box.width  # 5 pt in data units: beside the interval, clear of its end
    for x, ha in ((hi + gap, "left"), (lo - gap, "right")):
        t = ax.text(x, y, text, ha=ha, fontsize=C.NOTE, color=C.INK, va="center", gid=gid)
        e = t.get_window_extent(r).padded(2)
        if e.x0 >= box.x0 and e.x1 <= box.x1 and not any(e.overlaps(m) for m in marks):
            return True
        t.remove()
    return False


def dot_panel(ax: Any, b: RB.Book, dots: Dots, panel: Panel, ys: dict[str, float], kind: str,
              numbers: list[C.Number], notes: Notes,
              floor: tuple[dict[str, Floor], dict[str, str]] | None = None) -> None:  # fmt: skip
    """One panel: per model row, its cells of the panel's settings (several stacked), their controls, and the
    reference (chance across the panel, or the floor per row in the panel that holds the floor's setting)."""
    k = len(panel.settings)
    off = {s: (i - (k - 1) / 2) * 0.3 for i, s in enumerate(panel.settings)}
    size = 11 if k == 1 else 9
    chances: list[tuple[float, float]] = []  # (row y, chance)
    for m, y in ys.items():
        by = {s: cell(b, dots.finding, m, s) for s in panel.settings}
        cells = [c for c in by.values() if c is not None]
        shown = [c for c in cells if c.value is not None and (c.word in SHOWN or (kind == "full" and c.word == "not interpretable"))]  # fmt: skip
        missing = [s for s in panel.settings if not any(c.setting == s for c in shown)]
        notes.blank |= {blank_reason(by[s]) for s in missing}
        notes.fewer |= bool(shown) and bool(missing)
        if not shown:
            if kind == "full":
                ax.text(0, y, status(cells), fontsize=C.NOTE, color=C.CAPTION_INK, style="italic", va="center",
                        ha="left", gid="status")  # fmt: skip
            continue
        his, los = [], []
        for c in shown:
            yy = y + off[c.setting]
            pale = c.word == "not interpretable"
            notes.pale |= pale
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
            if dots.reference == "chance" and (ch := control(c, CHANCE)) is not None:
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
        for c in judged:  # a cell failing on a control: named in the caption with the control's number
            ctl = dots.why(c) if dots.why and c.word == "fails" else None
            if ctl is not None and (n := control(c, ctl)) is not None:
                numbers.append(n)
                notes.on_control.append((c, ctl, n))
        named = {id(c) for c, _, _ in notes.on_control}
        exc = [c for c in judged if exception(c) and id(c) not in named]
        if exc:
            text = span([c.value for c in judged if c.value is not None])
            (notes.labelled if place(ax, y, min(los), max(his), text) else notes.unlabelled).extend(exc)
    if dots.reference == "chance":
        band(ax, chances, max(ys.values()) + 1.1 if ys else 0.0)
    elif floor is not None and FLOOR_ON in panel.settings:
        floor_bands(ax, ys, floor, kind, numbers, notes)


def floor_bands(ax: Any, ys: dict[str, float], floor: tuple[dict[str, Floor], dict[str, str]], kind: str,
                numbers: list[C.Number], notes: Notes) -> None:  # fmt: skip
    """The floor per model row: a short dark line at its value, drawn over the row's dots (they sit on or near it: a
    band behind them would be hidden), short of the next row's; a not-interpretable floor pale on FULL, left out on
    MAIN; a row without one is named in the caption."""
    have, none = floor
    for m, y in ys.items():
        f = have.get(m)
        if (
            f is None
            or f.word not in (*SHOWN, "not interpretable")
            or (f.word == "not interpretable" and kind == "main")
        ):
            notes.no_floor[m] = (
                "control failed" if f is not None and f.word == "not interpretable" else none.get(m, "not run")
            )
            continue
        pale = f.word == "not interpretable"
        ax.plot([f.number.value] * 2, [y - 0.42, y + 0.42], color=C.CONTROL if pale else C.INK2, lw=2.2,
                solid_capstyle="butt", gid="tick", zorder=5)  # fmt: skip
        numbers.append(f.number)
        notes.pale |= pale


def band(ax: Any, chances: list[tuple[float, float]], label_y: float) -> None:
    """The chance band: one across the panel, labelled under the last row, when every cell's chance is the same; else
    one per row, unlabelled."""
    values = {v for _, v in chances}
    if len(values) == 1:
        v = values.pop()
        ax.axvspan(v - 1.5, v + 1.5, color=BAND, zorder=0, lw=0)
        ax.text(v + 2.5, label_y, "chance", ha="left", va="center", fontsize=C.NOTE, color=C.CAPTION_INK, gid="chance")
        return
    for y, v in set(chances):
        ax.fill_betweenx([y - 0.5, y + 0.5], v - 1.5, v + 1.5, color=BAND, lw=0, zorder=0)


# ---------------------------------------------------------------- the caption


HOLDS_ABOVE = "holds above chance"
PHRASE = {"≈ chance": "fails the rule at ≈ chance", "": "fails the rule", HOLDS_ABOVE: "holds but stays above chance"}


def fail_kind(c: RD.Cell, why: Callable[[RD.Cell], Control | None] | None) -> str:
    """How a failing cell fails: 'on <control>' (its value passes, a control named by `why` does not), '≈ chance' (the
    value is over the rule's bar but its interval covers the cell's chance), or '' (plainly)."""
    if why is not None and (ctl := why(c)) is not None:
        return f"on {ctl.short}"
    ch = control(c, CHANCE)
    return "≈ chance" if ch is not None and c.ci is not None and c.ci[0] <= ch.value <= c.ci[1] else ""


def kind_of(c: RD.Cell, why: Callable[[RD.Cell], Control | None] | None) -> str:
    return fail_kind(c, why) if c.word == "fails" else HOLDS_ABOVE


def cells_words(cells: list[RD.Cell]) -> str:
    """'27B (long context), Gemma (prompt sets 1-2, JSON)': models in ORDER."""
    out = []
    for m in C.MODELS:
        ss = [
            s for s in G.FINDING[cells[0].finding].settings if any(c.model == m.key and c.setting == s for c in cells)
        ]
        if ss:
            out.append(f"{m.short} ({setting_words(ss)})")
    return ", ".join(out)


def n_range(numbers: list[C.Number]) -> str:
    ns = [n.n for n in numbers if n.source == "grid.csv" and n.n is not None]
    return f"n = {min(ns)}-{max(ns)}" if ns and min(ns) != max(ns) else (f"n = {ns[0]}" if ns else "")


FILLED = "Filled = hybrid, hollow = attention-only."
FILLED_SHORT = "Filled = hybrid."  # when the long one does not fit two lines (the row headings name both groups)
FLOOR_NOTE = "Floor: prompt set 1, all layers (a lower bound)."


def reasons_words(reasons: set[str]) -> str:
    return join_or(sorted(reasons, key=lambda r: (BLANK_ORDER.index(r) if r in BLANK_ORDER else len(BLANK_ORDER), r)))


def caption(b: RB.Book, dots: Dots, kind: str, rule: str, notes: Notes, numbers: list[C.Number],
            far: bool = False, pale_note: bool = True) -> tuple[list[str], list[str]]:  # fmt: skip
    """The caption's sentences (required, optional), in order: whether any cell fails; what the labels mark (`far`:
    how far below the second mark they stay); the cells failing on a control, with its number; exceptions left
    unlabelled; the untested models; the floor (where it comes from); MAIN: why cells are blank, dots fewer or a floor
    missing; FULL: the rows without a floor, the rule, pale; n; the markers."""
    out = []
    fails = [c for c in notes.labelled + notes.unlabelled if c.word == "fails"] + [c for c, _, _ in notes.on_control]
    if not fails:
        out.append("No cell fails the rule.")
    # with the floor as the reference no chance is drawn: a failure at ≈ chance is just a failure
    phrase = {**PHRASE, "≈ chance": PHRASE[""]} if dots.reference == "floor" else PHRASE
    if notes.labelled:
        kinds = sorted({kind_of(c, dots.why) for c in notes.labelled}, key=list(PHRASE).index)
        s = "Labelled = " + " or ".join(dict.fromkeys(phrase[k] for k in kinds))
        if far and dots.second and kinds == [HOLDS_ABOVE]:
            seconds = [n.value for c in notes.labelled if (n := control(c, dots.second)) is not None]
            s += f", far below {dots.second.short} ({span(seconds)})" if seconds else ""
        out.append(s + ".")
    for c, ctl, n in notes.on_control:
        out.append(f"{C.MODEL[c.model].short}'s {setting_words([c.setting])} {ctl.fails.format(v=pct(n.value))}.")
    for k in sorted({kind_of(c, dots.why) for c in notes.unlabelled}, key=list(PHRASE).index):
        out.append(f"Also {phrase[k]}: {cells_words([c for c in notes.unlabelled if kind_of(c, dots.why) == k])}.")
    if u := C.not_tested(b, dots.finding):
        out.append(u)
    if dots.reference == "floor":
        none = ""
        if kind == "full" and notes.no_floor:  # MAIN: in the "Missing" sentence
            models = ", ".join(C.MODEL[m].short for m in notes.no_floor)
            why = reasons_words(set(notes.no_floor.values()))
            none = f"; none yet: {models}" if why == "not run" else f"; none: {models} ({why})"
        out.append(f"{FLOOR_NOTE[:-1]}{none}.")
    optional = []
    if kind == "main" and (notes.blank or notes.no_floor):
        what = " or ".join(["Missing dots"] * bool(notes.blank) + ["floor" if notes.blank else "Missing floor"] * bool(notes.no_floor))  # fmt: skip
        out.append(f"{what}: {reasons_words(notes.blank | set(notes.no_floor.values()))}.")
    if kind == "full":
        out.append(f"Rule: {rule}.")
        if notes.pale and pale_note:  # else How to read says it
            out.append("Pale = control failed.")
        if notes.fewer:
            optional.append("Fewer dots: not run.")
    return [*out, f"{n_range(numbers)}.", FILLED], optional


def pack(fig: Any, sentences: list[str], optional: list[str] | None = None) -> str:
    """The sentences in at most two caption lines that fit the figure's width (measured, not counted): one line if
    it fits, else the two-line split that keeps the first sentence first and moves the fewest sentences out of their
    order (then the fullest first line). The optional sentences are appended when that costs no more moves."""
    room = (0.985 - 0.03) * fig.get_figwidth()
    width: dict[str, bool] = {}

    def fits(s: str) -> bool:
        if s not in width:
            width[s] = PS.text_width(fig, s, C.CAPTION) <= room
        return width[s]

    def two_lines(ss: list[str]) -> tuple[tuple[int, int], str] | None:
        if fits(" ".join(ss)):
            return (0, 0), " ".join(ss)
        best: tuple[tuple[int, int], str] | None = None
        n = len(ss)
        for mask in range(1, (1 << n) - 1, 2):  # bit i: sentence i on the first line; bit 0 always
            one = [i for i in range(n) if mask >> i & 1]
            two = [i for i in range(n) if not mask >> i & 1]
            l1, l2 = " ".join(ss[i] for i in one), " ".join(ss[i] for i in two)
            if fits(l1) and fits(l2):
                key = (sum(i > two[0] for i in one), -len(l1))
                if best is None or key < best[0]:
                    best = (key, f"{l1}\n{l2}")
        return best

    plain = two_lines(sentences)
    more = two_lines([*sentences, *optional]) if optional else None
    if more is not None and (plain is None or more[0][0] <= plain[0][0]):
        return more[1]
    if plain is None:
        raise ValueError(f"the caption does not fit two lines: {sentences}")
    return plain[1]


def rows_of(b: RB.Book, f: str, panels: tuple[Panel, ...], kind: str) -> list[str]:
    """Models with a drawn cell in some panel (MAIN: a judged one), in ORDER."""
    ok = SHOWN if kind == "main" else (*SHOWN, "not interpretable")
    return [m.key for m in C.MODELS
            if any(c.value is not None and c.word in ok for p in panels for s in p.settings
                   if (c := cell(b, f, m.key, s)) is not None)]  # fmt: skip


def dot_figure(b: RB.Book, dots: Dots, panels: tuple[Panel, ...], kind: str, title: str, subtitle: str, how: str,
               rule: str, stem: str, out: Path, far: bool = False) -> list[Path]:  # fmt: skip
    """Draw the panels, then the caption from what they left to it, check overlaps, save. A How to read that names
    the pale marks keeps the caption from repeating it."""
    keys = rows_of(b, dots.finding, panels, kind)
    numbers: list[C.Number] = []
    notes = Notes()
    # the caption depends on the drawing: two lines are reserved, the text is set after drawing
    wspace = 0.26 if len(panels) <= 4 else 0.4  # five narrow panels: their titles must not read as one
    fr = C.frame(kind, title, subtitle, how=how, caption="x\nx", ncols=len(panels), wspace=wspace, left=0.155,
                 right=0.975, sharex=True)  # fmt: skip
    title_room(fr)
    floor = floors(b.grid_dir) if dots.reference == "floor" else None
    for i, (ax, p) in enumerate(zip(fr.axes, panels, strict=True)):
        ys = setup(ax, p.title, keys, first=i == 0, label_room=dots.reference == "chance")
        dot_panel(ax, b, dots, p, ys, kind, numbers, notes, floor)
    cap = next(t for t in fr.fig.texts if t.get_gid() == "caption")
    sentences, optional = caption(b, dots, kind, rule, notes, numbers, far, pale_note="pale =" not in how)
    try:
        text = pack(fr.fig, sentences, optional)
    except ValueError:  # the markers' sentence shortened before giving up
        text = pack(fr.fig, [FILLED_SHORT if s == FILLED else s for s in sentences], optional)
    cap.set_text(text)
    return C.save(fr, stem, numbers, out)


# ---------------------------------------------------------------- finding 4


def why_f4(c: RD.Cell) -> Control | None:
    """A late-read cell failing on its DeltaNet control (the value itself passes)."""
    return DELTANET if "DeltaNet" in c.verdict else None


DOTS = Dots(F, "% right, the answer's sentence hidden from the tokens after the question", tick=OFF, why=why_f4,
            reference="floor")  # fmt: skip
TITLE = "Hiding the answer's sentence breaks the lookup"
SUBTITLE = "Lookup = answer copied from a prompt sentence. % right with it hidden after the question"
HOW = {"main": "dark line = floor: every later token blocked; tick = another sentence hidden (stays high).",
       "full": "dark line = floor: every later token blocked; tick = other sentence; pale = control failed."}  # fmt: skip
RULE = "≤ 20% (CI ≤ 30%), controls ≥ 90%"


def late_read(b: RB.Book, kind: str, out: Path = C.OUT) -> list[Path]:
    panels = MAIN_PANELS if kind == "main" else FULL_PANELS
    return dot_figure(b, DOTS, panels, kind, TITLE, SUBTITLE, HOW[kind], RULE, STEM, out)


# ---------------------------------------------------------------- the DeltaNet figure (hybrids only)

DN_TITLE = "DeltaNet layers do not need the answer's sentence"
DN_SUBTITLE = "Hybrids mix attention and DeltaNet layers: % right, the sentence hidden in one kind"
DN_HOW = "one dot per setting (prompt sets, formats, long context), stacked in the row."
DN_BAR = 90.0  # the late-read rule: hidden in every DeltaNet layer instead keeps >= 90% (cross_model_grid RULES)


def deltanet(b: RB.Book, out: Path = C.OUT) -> list[Path]:
    """The hybrids' cells with a DeltaNet control: hidden in every attention layer (grey) vs every DeltaNet layer."""
    settings = G.FINDING[F].settings
    pairs: dict[str, list[tuple[RD.Cell, C.Number]]] = {}
    left: set[str] = set()  # why a hybrid's setting has no dot
    for m in C.MODELS:
        if not m.hybrid:
            continue
        for s in settings:
            c = cell(b, F, m.key, s)
            if c is not None and c.value is not None and c.word in SHOWN and (dn := control(c, DELTANET)) is not None:
                pairs.setdefault(m.key, []).append((c, dn))
            else:
                left.add(blank_reason(c))
    numbers: list[C.Number] = []
    fr = C.frame("main", DN_TITLE, DN_SUBTITLE, how=DN_HOW, caption="x\nx", left=0.2, right=0.95)
    ax = fr.axes[0]
    ys = C.model_rows(ax, list(pairs))
    for t in [t for t in ax.texts if t.get_gid() == "group"]:
        t.remove()  # every row is a hybrid: the subtitle says it
    last = max(ys.values())
    ax.set_ylim(last + 1.2, -1.25)  # room above the first row for the direct labels, under the last for the band's
    ax.spines["left"].set_visible(False)
    ax.set_xlim(-3, 103)
    ax.set_xticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
    ax.set_xlabel("% right", fontsize=C.LABEL)
    ax.axvspan(DN_BAR, 103, color=BAND, zorder=0, lw=0)
    ax.text(DN_BAR - 1, last + 0.8, f"the rule: ≥ {DN_BAR:.0f}% kept", ha="right", va="center", fontsize=C.NOTE,
            color=C.CAPTION_INK, gid="chance")  # fmt: skip
    slot = {s: (i - (len(settings) - 1) / 2) * 0.12 for i, s in enumerate(settings)}
    for m, y in ys.items():
        for c, dn in pairs[m]:
            yy = y + slot[c.setting]
            num = C.cell_number(b, F, m, c.setting, "% right, hidden in every attention layer")
            assert num is not None
            numbers += [num, dn]
            ax.plot([num.value], [yy], marker="o", markersize=8, color=C.CONTROL, linestyle="none", gid="mark",
                    zorder=3)  # fmt: skip
            ax.plot([dn.value], [yy], marker="o", markersize=10, color=C.LOOKUP, linestyle="none", gid="mark",
                    zorder=4)  # fmt: skip
        for c, dn in pairs[m]:
            if dn.value < DN_BAR:
                ax.text(dn.value - 2, y + slot[c.setting], f"{setting_words([c.setting])}: {pct(dn.value)}",
                        ha="right", va="center", fontsize=C.NOTE, color=C.INK, gid="value")  # fmt: skip
    top = min(ys.values()) - 0.75  # direct labels above the first row, at the two clusters' ends
    ax.text(0, top, "hidden in the attention layers", ha="left", va="center", fontsize=C.NOTE, color=C.CAPTION_INK,
            gid="label")  # fmt: skip
    ax.text(DN_BAR - 1, top, "hidden in the DeltaNet layers", ha="right", va="center", fontsize=C.NOTE,
            color=C.LOOKUP, gid="label")  # fmt: skip
    ns = [c.n for cs in pairs.values() for c, _ in cs if c.n is not None]
    counts = ", ".join(f"{C.MODEL[m].short} {len(v)}" for m, v in pairs.items())
    reasons = sorted(left, key=lambda r: (BLANK_ORDER.index(r) if r in BLANK_ORDER else len(BLANK_ORDER), r))
    rest = f"; the rest: {join_or(reasons)}" if left else ""
    sentences = [f"Settings drawn: {counts} of {len(settings)}{rest}.", f"n = {min(ns)}-{max(ns)} per dot.",
                 "Attention-only models have no DeltaNet layers."]  # fmt: skip
    cap = next(t for t in fr.fig.texts if t.get_gid() == "caption")
    cap.set_text(pack(fr.fig, sentences))
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
