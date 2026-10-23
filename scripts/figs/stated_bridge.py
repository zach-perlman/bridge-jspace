"""stated_bridge: finding 2 as the lookup/recall contrast, "the lens-readable part moves recall, not the lookup" (Dan's
figure guide, 6f; title and order from Dan, 23 Oct).

The test (statement_positions parts runs judged by d1_verdict): the stated bridge is changed (Jack's pet: cow -> pig)
and one part of that change is pasted back at the decisive cell (from a lens-free map): the lens-readable part
(J-space), a random part keeping the lens part's share of the change (jspace_matched: the same size), or the rest. A bar
is the % of answers switched to the new bridge's answer; lookups (the accent color) and recalls (dark grey) side by
side for each part, in that order: the lens part, the random part beside it as its baseline (light grey), the rest as
the reference that does move the lookup (lighter tints).

Numbers: the lookups' lens part is the grid cell's value (common.cell_number); the recalls' lens part, the lookups' rest
and both random parts are the cell's control text in grid.csv (source CONTROL, extra["control"] = the name in
readme_build.CONTROLS["f2"], so a test can match them with Book.control). The recalls' rest is not in the grid: it and
the interval of the lookups' rest come from the verdict.json the cell names (source = that file), after the file is
checked against every number the grid has for the cell (a mismatch raises; nothing is patched).

MAIN: each model's main scene set (scene set 2 where planned, else 1; as cross_model_figures.stated_bridge_row) where
the rule judged it (holds / fails): one panel per model. FULL: every setting with a value (scene sets, table, JSON),
one row per model, a cell that is not interpretable in pale grey.

uv run python scripts/figs/stated_bridge.py [--grid DIR] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C

STEM = "stated_bridge"
F = "f2"
SETTINGS = ("draw 1", "draw 2", "table", "JSON")  # the finding's grid settings drawn (no late-binding cells)
FORMAT = {"table": "table", "JSON": "json"}  # grid setting -> verdict.json by_format key
PARTS = ("lens", "random", "rest")  # the random part beside the lens part (its baseline); the rest: the reference
CONTROL = "grid.csv control"  # a number from a cell's control text (check_numbers compares cell values only)
JUDGED = ("holds", "fails", "not interpretable", "inconclusive", "open")

TITLE = "The lens-readable part moves recall, not the lookup"  # Dan, 23 Oct; the 122B in the caption
SUBTITLE = "% of answers switched when one part of a stated bridge's change is pasted back"
NUM = r"(-?\d+(?:\.\d+)?)"
RECALL_LENS = re.compile(rf"recall, lens-readable part \(the control, needs >= 30%\): {NUM}% \[{NUM}, {NUM}\]")
REST = re.compile(rf"lookup, the rest \(needs >= 50%\): {NUM}%")
RANDOM = re.compile(rf"same-share random part \(jspace_matched\): lookups {NUM}% \[{NUM}, {NUM}\] n=(\d+), "
                    rf"recalls {NUM}% \[{NUM}, {NUM}\] n=(\d+)")  # fmt: skip


def tint(hex_color: str, white: float) -> str:
    """The color mixed with white (0: unchanged, 1: white)."""
    rgb = [int(hex_color[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(c + (255 - c) * white):02x}" for c in rgb)


COLOR = {("lookups", "lens"): C.LOOKUP, ("lookups", "rest"): tint(C.LOOKUP, 0.5), ("lookups", "random"): C.CONTROL,
         ("recalls", "lens"): C.RECALL, ("recalls", "rest"): tint(C.RECALL, 0.45), ("recalls", "random"): C.CONTROL}  # fmt: skip
PALE = "#e3e3e3"  # a cell that is not interpretable (FULL only)
SHOWN_WORD = {"holds": "holds", "fails": "fails", "not interpretable": "can't tell", "inconclusive": "can't tell"}


@dataclass
class Bars:
    """One cell's bars: family ("lookups" / "recalls") -> part -> Number (percent, with its interval)."""

    model: str
    setting: str
    word: str
    n: int
    parts: dict[str, dict[str, C.Number]] = field(default_factory=dict)

    def numbers(self) -> list[C.Number]:
        return [n for fam in self.parts.values() for n in fam.values()]


def control(m: str, setting: str, name: str, what: str, value: float, ci=None, n=None, *, f: str = F,
            **extra) -> C.Number:  # fmt: skip
    """A number of the cell's control text (`name`: its readme_build.CONTROLS[f] key)."""
    return C.Number(value, what, f, m, setting, "", ci, n, source=CONTROL, extra={"control": name, **extra})


def from_file(m: str, setting: str, what: str, t: list, path: str, key: str) -> C.Number:
    return C.Number(100 * t[0], what, F, m, setting, "", (100 * t[1], 100 * t[2]), int(t[3]), source=path,
                    extra={"key": key})  # fmt: skip


def cell_of(b: RB.Book, m: str, setting: str, f: str = F) -> RD.Cell | None:
    return next((c for c in b.of(f, m) if c.setting == setting and c.part == ""), None)


def verdict_parts(v: dict, setting: str) -> tuple[list, list, list, list, str]:
    """(lookups lens, lookups rest, recalls lens, recalls rest) as [p, lo, hi, n], and the recalls' rest's key."""
    if setting in FORMAT:
        d = v["by_format"][FORMAT[setting]]
        return (d["PP_jspace"], d["PP_not_jspace"], d["PM_jspace"], d["PM_not_jspace"],
                f"by_format.{FORMAT[setting]}.PM_not_jspace")  # fmt: skip
    return (v["lookup"]["jspace"], v["lookup"]["not_jspace"], v["recall"]["jspace"], v["recall"]["not_jspace"],
            "recall.not_jspace")  # fmt: skip


def collect(b: RB.Book, m: str, setting: str, root: Path = C.REPO) -> Bars | None:
    """The cell's bars, or None when the cell has no value. Raises ValueError when its files disagree with the grid."""
    c = cell_of(b, m, setting)
    lens = C.cell_number(b, F, m, setting, "lookups switched, lens-readable part")
    if c is None or lens is None:
        return None
    rc, rest, rnd = RECALL_LENS.search(c.control), REST.search(c.control), RANDOM.search(c.control)
    if rc is None or rest is None:
        raise ValueError(f"{F} {m} {setting}: no recall control or rest in the grid's control text")
    v = json.loads((root / c.path).read_text())
    lk_lens, lk_rest, rc_lens, rc_rest, key = verdict_parts(v, setting)
    if (
        abs(100 * lk_lens[0] - lens.value) > 0.05 + 1e-9
        or G.r100(lk_rest[0]) != float(rest.group(1))
        or G.r100(rc_lens[0]) != float(rc.group(1))
    ):
        raise ValueError(f"{F} {m} {setting}: {c.path} disagrees with the grid")
    lookups = {
        "lens": lens,
        "rest": control(m, setting, "rest", "lookups switched, the rest", float(rest.group(1)),
                        (100 * lk_rest[1], 100 * lk_rest[2]), int(lk_rest[3]), ci_from=c.path),
    }  # fmt: skip
    recalls = {
        "lens": control(m, setting, "recall", "recalls switched, lens-readable part", float(rc.group(1)),
                        (float(rc.group(2)), float(rc.group(3))), int(rc_lens[3])),
        "rest": from_file(m, setting, "recalls switched, the rest", rc_rest, c.path, key),
    }  # fmt: skip
    if rnd is not None:
        g = rnd.groups()
        lookups["random"] = control(m, setting, "random lookups", "lookups switched, same-share random part",
                                    float(g[0]), (float(g[1]), float(g[2])), int(g[3]))  # fmt: skip
        recalls["random"] = control(m, setting, "random recalls", "recalls switched, same-share random part",
                                    float(g[4]), (float(g[5]), float(g[6])), int(g[7]))  # fmt: skip
    return Bars(m, setting, c.word, c.n or int(lk_lens[3]), {"lookups": lookups, "recalls": recalls})


def main_setting(b: RB.Book, m: str) -> str:
    """Scene set 2 where the model has it planned, else scene set 1 (the plan decides, never the result)."""
    d2 = cell_of(b, m, "draw 2")
    return "draw 2" if d2 is not None and not (d2.word == "missing" and "no spec" in d2.verdict) else "draw 1"


def untested(b: RB.Book, keys=None, f: str = F) -> str:
    """common.not_tested's models and reasons, models with the same reason grouped: 'Not tested: A (r); B, C (s).'"""
    groups: dict[str, list[str]] = {}
    for mm in C.MODELS:
        cs = b.of(f, mm.key)
        if (keys is None or mm.key in keys) and not any(c.word in JUDGED for c in cs):
            groups.setdefault(RB.reason(cs), []).append(mm.short)
    return (
        ("Not tested: " + "; ".join(f"{', '.join(ms)} ({why})" for why, ms in groups.items()) + ".") if groups else ""
    )


# ---------------------------------------------------------------- drawing

W, DX = 0.36, 0.2  # bar width; lookups at -DX, recalls at +DX of the part's place


def shift(fr: C.Frame, top: float = 0, bottom: float = 0) -> None:
    """Move the panels' top down by `top` points (room for panel headings under the frame's header) and their bottom
    down by `bottom` points (the frame keeps room for an x label these panels do not have)."""
    gs = fr.axes[0].get_subplotspec().get_gridspec()
    h = 72 * fr.fig.get_figheight()
    gs.update(top=gs.top - top / h, bottom=gs.bottom - bottom / h)


def head(ax, left: str, right: str, size: float = C.LABEL) -> None:
    """A panel's heading: `left` and a small grey word at the right (the verdict)."""
    ax.annotate(left, (0, 1), xycoords="axes fraction", xytext=(0, 10), textcoords="offset points", ha="left",
                va="bottom", fontsize=size, color=C.INK)  # fmt: skip
    ax.annotate(right, (1, 1), xycoords="axes fraction", xytext=(0, 10), textcoords="offset points", ha="right",
                va="bottom", fontsize=C.NOTE, color=C.CAPTION_INK)  # fmt: skip


def draw_panel(ax, bars: Bars, *, ticks: tuple[str, ...], label: tuple[str, ...], pale: bool = False) -> None:
    """Three places (lens, rest, random), two bars each (lookups, recalls), thin light intervals; the value printed
    above the bars of the families in `label` at the lens part (one family: above both bars, clear of the other's
    interval in a narrow panel)."""

    def top_of(num: C.Number | None) -> float:
        return 0.0 if num is None else max(num.value, num.ci[1] if num.ci else num.value)

    for i, part in enumerate(PARTS):
        both = max(top_of(bars.parts[fam].get(part)) for fam in ("lookups", "recalls"))
        for fam, dx in (("lookups", -DX), ("recalls", DX)):
            num = bars.parts[fam].get(part)
            if num is None:
                continue
            x = i + dx
            ax.bar(x, num.value, width=W, color=PALE if pale else COLOR[(fam, part)], linewidth=0, zorder=2)
            if num.ci is not None:
                lo, hi = max(0.0, num.ci[0]), num.ci[1]
                ax.plot([x, x], [lo, hi], color=C.INK, linewidth=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"],
                        solid_capstyle="butt", zorder=3, gid="ci")  # fmt: skip
            top = top_of(num) if len(label) > 1 else both
            if part == "lens" and fam in label:
                ax.annotate(f"{RD.r0(num.value)}%", (x, top), xytext=(0, 4), textcoords="offset points", ha="center",
                            va="bottom", fontsize=C.NOTE, color=C.CAPTION_INK if pale else C.INK,
                            fontweight="normal" if pale else "bold", gid="value", zorder=4)  # fmt: skip
    ax.set_xlim(-0.6, len(PARTS) - 0.4)
    ax.set_xticks(range(len(PARTS)), ticks)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 50, 100], ["0", "50", "100"])
    ax.spines["bottom"].set_color(C.CONTROL)


def figure_main(b: RB.Book, root: Path = C.REPO) -> tuple[C.Frame, list[C.Number]]:
    shown: list[Bars] = []
    for mm in C.MODELS:
        bars = collect(b, mm.key, main_setting(b, mm.key), root)
        if bars is not None and bars.word in ("holds", "fails"):
            shown.append(bars)
    if not shown:
        raise ValueError("finding 2: no judged cell to draw")
    fails = [x for x in shown if x.word == "fails"]
    can_t = [mm.short for mm in C.MODELS if (x := cell_of(b, mm.key, main_setting(b, mm.key))) is not None
             and x.word in ("not interpretable", "inconclusive")]  # fmt: skip
    ns = sorted({x.n for x in shown})
    exc = [f"Exception: the {C.MODEL[x.model].short} (lens part moves {RD.r0(x.parts['lookups']['lens'].value)}% "
           "of lookups)." for x in fails]  # fmt: skip
    exc += [f"{', '.join(can_t)}: can't tell (recall control fails)."] if can_t else []
    sets = ", ".join(sorted({RB.show(x.setting) for x in shown})).capitalize()
    exc += [f"{sets}, n = {ns[0]}-{ns[-1]}." if len(ns) > 1 else f"{sets}, n = {ns[0]}."]
    fr = C.frame("main", TITLE, SUBTITLE, how="purple = lookups, grey = recalls; random = a random part of the same size",
                 caption=" ".join(exc) + "\n" + untested(b), nrows=1, ncols=len(shown), left=0.085, wspace=0.18,
                 sharey=True)  # fmt: skip
    shift(fr, top=30, bottom=C.LABEL * 1.8)
    numbers: list[C.Number] = [x.parts["lookups"]["lens"] for x in fails]  # the caption's numbers
    for ax, bars in zip(fr.axes, shown, strict=True):
        draw_panel(ax, bars, ticks=("lens part", "random", "rest"), label=("lookups", "recalls"))
        head(ax, C.MODEL[bars.model].name, SHOWN_WORD.get(bars.word, bars.word))
        numbers += bars.numbers()
        if ax is not fr.axes[0]:
            ax.tick_params(axis="y", labelleft=False)
    fr.axes[0].set_ylabel("% switched")
    return fr, numbers


def figure_full(b: RB.Book, root: Path = C.REPO) -> tuple[C.Frame, list[C.Number]]:
    grid: dict[tuple[str, str], Bars] = {}
    for mm in C.MODELS:
        for s in SETTINGS:
            bars = collect(b, mm.key, s, root)
            if bars is not None:
                grid[(mm.key, s)] = bars
    rows = [mm.key for mm in C.MODELS if any((mm.key, s) in grid for s in SETTINGS)]
    cols = [s for s in SETTINGS if any((m, s) in grid for m in rows)]
    if not rows:
        raise ValueError("finding 2: no cell with a value")
    ns = sorted({x.n for x in grid.values()})
    line1 = "Rule: holds if the lens part moves ≤ 10% of lookups and the rest ≥ 50%, and ≥ 30% of recalls. "
    line1 += f"n = {ns[0]}-{ns[-1]}." if len(ns) > 1 else f"n = {ns[0]}."
    fr = C.frame("full", TITLE, SUBTITLE, how="purple = lookups, grey = recalls; pale = can't tell (a control fails)",
                 caption=f"{line1}\n{untested(b)}", nrows=len(rows), ncols=len(cols), size=(12.0, 3.0 + 2.55 * len(rows)),
                 left=0.125, wspace=0.2, hspace=0.62)  # fmt: skip
    shift(fr, top=30, bottom=C.LABEL * 1.8)
    numbers: list[C.Number] = []
    for r, m in enumerate(rows):  # short names: four setting columns need the width
        first = fr.axes[r * len(cols)].get_position()
        fr.fig.text(0.03, (first.y0 + first.y1) / 2, C.MODEL[m].short, ha="left", va="center", fontsize=C.LABEL,
                    fontweight="bold", color=C.INK, gid="row")  # fmt: skip
        for k, s in enumerate(cols):
            ax = fr.axes[r * len(cols) + k]
            bars = grid.get((m, s))
            if bars is None:  # no empty panels: the setting's slot stays blank
                ax.remove()
                continue
            pale = bars.word not in ("holds", "fails")
            draw_panel(ax, bars, ticks=("lens", "random", "rest"), label=("lookups",), pale=pale)
            head(ax, RB.show(s), SHOWN_WORD.get(bars.word, bars.word), size=C.NOTE)
            numbers += bars.numbers()
    return fr, numbers


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    ap.add_argument("--grid", type=Path, default=None, help="results/cross_model/<stamp> (default: the newest)")
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    a = ap.parse_args(argv)
    grid = a.grid or newest_grid()
    b = C.book(grid)
    for kind, make in (("main", figure_main), ("full", figure_full)):
        if a.only in (None, kind):
            fr, numbers = make(b)
            for p in C.save(fr, STEM, numbers, a.out):
                print("wrote", p)
    return 0


def newest_grid(root: Path = G.OUT) -> Path:
    hits = sorted(d for d in root.glob("*") if (d / "grid.csv").exists())
    if not hits:
        raise SystemExit(f"no grid.csv under {root}")
    return hits[-1]


if __name__ == "__main__":
    raise SystemExit(main())
