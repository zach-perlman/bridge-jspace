"""counting: finding 6 (Dan's figure guide, 6d): the order label counts order in the list, not place in the text.

Every number is from grid.csv's finding-6 cells: the key number is the % of patched answers at the same order in the
list (the cell's value and interval); its controls are read from the cell's "chance or control level" text: the same
place in the text (every setting) and counted from the end (one statement more / fewer), each with its interval.
Control numbers go to the data file with source "grid.csv control text" (check_numbers compares grid values only).

MAIN: the filler-moved test only, one row per model: list order (the accent, big; filled = hybrid, hollow =
attention-only) vs place in text (light grey), each labelled on a row line beside its marks; the caption says why a
failing model fails and names the holding models as low as it. FULL: all three settings side by side, counted from
the end as a grey tick. A model whose cell fails the rule gets the small grey word "fails" beside its row.

uv run python scripts/figs/counting.py --grid results/cross_model/<stamp> [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bridge_jspace import plot_style as PS
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C
from scripts.figs import order_identity as OI  # pack (the caption), room_for_titles, WHICH: shared with finding 5

STEM = "counting"
F = "f6"
SETTINGS = ("filler moved", "one statement more", "one statement fewer")
NUM = r"(-?\d+(?:\.\d+)?)"
# a control's number and interval in grid.csv's control text (cross_model_grid.ev_f6: "<name> 9% [7, 13]")
RIVALS = {"place in text": re.compile(rf"the same place in the text {NUM}% \[{NUM}, {NUM}\]"),
          "from the end": re.compile(rf"counted from the end {NUM}% \[{NUM}, {NUM}\]")}  # fmt: skip
WHAT = {"order": "% of patched answers at the same order in the list", "place in text": "% at the same place in the "
        "text (control)", "from the end": "% at the same order counted from the end (control)"}  # fmt: skip


def control(c: RD.Cell, name: str) -> tuple[float, float, float] | None:
    m = RIVALS[name].search(c.control)
    return (float(m.group(1)), float(m.group(2)), float(m.group(3))) if m else None


def cells(b: RB.Book, setting: str) -> dict[str, RD.Cell]:
    """{model: its cell with a value} in the setting."""
    return {c.model: c for c in b.of(F) if c.setting == setting and c.value is not None}


def why_fails(c: RD.Cell) -> str:
    """Filler moved: the rule needs list order's interval above the text place's pooled and in >= 2 of 3 topics at one
    layer; grid.csv has the pooled intervals at the layer shown (a decisive one), so a failing cell whose pooled
    interval clears the control's failed on the topics."""
    t = control(c, "place in text")
    if c.ci is not None and t is not None and c.ci[0] > t[2]:
        return "purple is above grey over all items, but not in 2 of 3 topics as the rule needs"
    return "the purple and grey intervals overlap"


def fails_sentence(got: dict[str, RD.Cell], keys: list[str]) -> str:
    """'32B fails: ...; Gemma, as low, passes both.': each failing model with its reason, and the holding models whose
    list-order share is as low (within 3 points), so a reader does not take the low dot for the failure."""
    out = []
    for k in (k for k in keys if got[k].word == "fails"):
        v = got[k].value or 0.0
        low = [h for h in keys if got[h].word == "holds" and (got[h].value or 0.0) <= v + 3]
        tail = (
            f"; {', '.join(C.MODEL[h].short for h in low)}, as low, {'pass' if len(low) > 1 else 'passes'} both"
            if low
            else ""
        )
        out.append(f"{C.MODEL[k].short} fails: {why_fails(got[k])}{tail}.")
    return " ".join(out)


def direct_labels(fig, ax, got: dict[str, RD.Cell], keys: list[str], ys: dict[str, float], xmax: float) -> None:
    """'same place in the text' and 'same order in the list' on a row line, right of their own marks, in the first row
    (top down) where the text fits before the next mark; rows with a verdict word are skipped."""
    inch = ax.get_position().width * fig.get_figwidth() / xmax  # inches per percentage point
    pad, half = 0.1 / inch, 0.14 / inch  # a gap; half a list-order marker
    spans: dict[str, dict[str, tuple[float, float]]] = {}
    for k in keys:
        c, t = got[k], control(got[k], "place in text")
        v = c.value or 0.0
        lo, hi = c.ci if c.ci is not None else (v, v)
        spans[k] = {"order": (min(lo, v - half), max(hi, v + half))}
        if t is not None:
            spans[k]["place in text"] = (min(t[1], t[0] - half), max(t[2], t[0] + half))
    taken: dict[str, list[tuple[float, float]]] = {k: [] for k in keys}
    for name, text, color, weight in (("place in text", "same place in the text", C.INK2, "normal"),
                                      ("order", "same order in the list", C.LOOKUP, "bold")):  # fmt: skip
        w = PS.text_width(fig, text, C.NOTE, weight) / inch
        for k in keys:
            if got[k].word != "holds" or name not in spans[k]:
                continue
            start = spans[k][name][1] + pad
            stops = [a for n, (a, b) in spans[k].items() if n != name and b > start] + [
                a for a, b in taken[k] if b > start
            ]
            if start + w + pad <= min([*stops, xmax]):
                ax.text(start, ys[k], text, ha="left", va="center", fontsize=C.NOTE, color=color, fontweight=weight,
                        gid="label")  # fmt: skip
                taken[k].append((start, start + w))
                break


def dot(key: str, color: str, size: float) -> dict[str, Any]:
    """The list-order mark: C.marker's shape and fill rule (filled = hybrid) in a semantic color."""
    style = C.marker(key, size)
    style["markeredgecolor"] = color
    style["markerfacecolor"] = color if C.MODEL[key].hybrid else "white"
    return style


CTL_MARK: dict[str, dict[str, Any]] = {
    "place in text": {"marker": "o", "markersize": 9, "markerfacecolor": C.CONTROL, "markeredgecolor": C.CONTROL,
                      "linestyle": "none"},
    "from the end": {"marker": "|", "markersize": 16, "markeredgewidth": 3, "markeredgecolor": C.CONTROL,
                     "linestyle": "none"},
}  # fmt: skip


def interval(ax, lo: float, hi: float, y: float, color: str) -> None:
    ax.plot([lo, hi], [y, y], color=color, lw=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"],
            solid_capstyle="butt", gid="ci", zorder=2)  # fmt: skip


def panel(ax, b: RB.Book, setting: str, ys: dict[str, float], numbers: list[C.Number], rivals: tuple[str, ...],
          size: float) -> list[str]:  # fmt: skip
    """One setting's rows: the controls (grey, behind) and list order (the accent); returns the failing models."""
    fails = []
    for k, c in cells(b, setting).items():
        if k not in ys:
            continue
        y = ys[k]
        ends = []
        for name in rivals:
            t = control(c, name)
            if t is None:
                continue
            numbers.append(C.Number(t[0], WHAT[name], F, k, setting, ci=(t[1], t[2]), n=c.n,
                                    source="grid.csv control text", extra={"control": name}))  # fmt: skip
            interval(ax, t[1], t[2], y, C.CONTROL)
            ax.plot([t[0]], [y], gid="mark", zorder=3, **CTL_MARK[name])
            ends.append(t[2])
        num = C.cell_number(b, F, k, setting, WHAT["order"])
        assert num is not None
        numbers.append(num)
        if num.ci is not None:
            interval(ax, num.ci[0], num.ci[1], y, C.LOOKUP)
            ends.append(num.ci[1])
        ax.plot([num.value], [y], gid="mark", zorder=4, **dot(k, C.LOOKUP, size))
        if c.word == "fails":
            fails.append(k)
            ax.annotate("fails", xy=(max([num.value, *ends]), y), xytext=(12, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=C.NOTE, color=C.CAPTION_INK, gid="status")  # fmt: skip
        elif c.word == "not interpretable":
            ax.annotate("can't tell", xy=(max([num.value, *ends]), y), xytext=(12, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=C.NOTE, color=C.CAPTION_INK, gid="status")  # fmt: skip
    return fails


def x_axis(ax, xmax: float, label: bool) -> None:
    ax.set_xlim(0, xmax)
    ticks = list(range(0, int(xmax) + 1, 10))
    ax.set_xticks(ticks, [f"{t}" for t in ticks])
    ax.grid(axis="x", color=C.GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    if label:
        ax.set_xlabel("% of answers")


def x_max(b: RB.Book, settings: tuple[str, ...]) -> float:
    """The axis end: the data's, plus room for a "fails" word right of a failing row."""
    hi = 0.0
    for s in settings:
        for c in cells(b, s).values():
            ends = [c.value or 0.0, *(c.ci or ()), *(t[2] for n in RIVALS if (t := control(c, n)))]
            hi = max(hi, max(ends) + (9 if c.word in ("fails", "not interpretable") else 0))
    return max(50.0, math.ceil(hi / 10) * 10)


def names(keys: list[str]) -> str:
    return ", ".join(C.MODEL[k].short for k in keys)


def n_range(b: RB.Book, settings: tuple[str, ...]) -> str:
    ns = [c.n for s in settings for c in cells(b, s).values() if c.n is not None]
    return "–" if not ns else (f"{min(ns)}–{max(ns)}" if min(ns) != max(ns) else str(ns[0]))


MARKS = "Filled = hybrid, hollow = attention-only; bars: 95% CI."


def draw_main(b: RB.Book, out: Path = C.OUT) -> list[Path]:
    setting = "filler moved"
    got = cells(b, setting)
    keys = [m.key for m in C.MODELS if m.key in got]
    if not keys:
        raise ValueError("no model has a filler-moved value")
    caption = OI.pack([fails_sentence(got, keys) or "Holds on every model shown.",
                       f"n = {n_range(b, (setting,))} per model; {OI.WHICH}.", C.not_tested(b, F, None), MARKS])  # fmt: skip
    fr = C.frame("main", "A moved filler sentence doesn't shift the label",
                 "Last two tokens copied from a prompt with a filler moved: same list order or text place?",
                 how="Purple right of grey: the answer follows the list, not the text.", caption=caption, left=0.2,
                 right=0.95)  # fmt: skip
    ax = fr.axes[0]
    ys = C.model_rows(ax, keys)
    numbers: list[C.Number] = []
    panel(ax, b, setting, ys, numbers, ("place in text",), 13)
    xmax = x_max(b, (setting,))
    x_axis(ax, xmax, True)
    direct_labels(fr.fig, ax, got, keys, ys, xmax)
    return C.save(fr, STEM, numbers, out)


def draw_full(b: RB.Book, out: Path = C.OUT) -> list[Path]:
    keys = [m.key for m in C.MODELS if any(m.key in cells(b, s) for s in SETTINGS)]
    if not keys:
        raise ValueError("no model has a finding-6 value")
    fails = {s: [k for k in keys if k in cells(b, s) and cells(b, s)[k].word == "fails"] for s in SETTINGS}
    more, fewer = SETTINGS[1], SETTINGS[2]
    if fails[more] == fails[fewer]:  # the rule judges one more and one fewer together (H-start-v4: the same layer)
        groups = [("filler moved", fails[SETTINGS[0]]), ("one more and one fewer (judged together)", fails[more])]
    else:
        groups = [(RB.show(s), fails[s]) for s in SETTINGS]
    parts = [f"{what}: {names(ks)}" for what, ks in groups if ks]
    line1 = ("Fails the rule: " + "; ".join(parts) + ".") if parts else "Holds on every model shown."
    caption = OI.pack([line1, f"n = {n_range(b, SETTINGS)} per cell; {OI.WHICH}.", C.not_tested(b, F, None), MARKS])
    fr = C.frame("full", "The label counts list order, not place in the text",
                 "Last two tokens copied from a prompt with its list changed: list order or a control?",
                 how="Purple: same order in the list. Grey dot: same place in the text. Grey tick: from the end.",
                 caption=caption, ncols=3, size=(12.0, 8.0), left=0.17, right=0.97, wspace=0.12)  # fmt: skip
    OI.room_for_titles(fr)
    xmax = x_max(b, SETTINGS)
    numbers: list[C.Number] = []
    for i, (ax, s) in enumerate(zip(fr.axes, SETTINGS, strict=True)):
        ys = C.model_rows(ax, keys, label=i == 0)
        if i:
            ax.set_yticks(list(ys.values()), [])
            ax.tick_params(axis="y", length=0)
        rivals = ("place in text",) if s == "filler moved" else ("from the end", "place in text")
        panel(ax, b, s, ys, numbers, rivals, 11)
        x_axis(ax, xmax, i == 1)
        ax.set_title(RB.show(s).capitalize(), fontsize=C.LABEL, fontweight="bold", pad=10)
    return C.save(fr, STEM, numbers, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=None, help="a results/cross_model/<stamp> folder (default: the README's pin)")
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", default=None, help="output folder (default figures/archive/cross_model)")
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
