"""stated_bridge: finding 2 as the lookup/recall contrast, "the lens-readable part moves recall, not the lookup" (Dan's
figure guide, 6f; title and order from Dan, 23 Oct).

The test (statement_positions parts runs judged by d1_verdict): the stated bridge is changed (Jack's pet: cow -> pig)
and one part of that change is pasted back at the decisive cell (from a lens-free map): the lens-readable part
(J-space), a random part keeping the lens part's share of the change (jspace_matched: the same size), or the rest. A bar
is the % of answers switched to the new bridge's answer; lookups (the accent color) and recalls (dark grey, one shade
per kind) side by side for each part, in that order: the lens part, the random part beside it as its baseline (light
grey, its values printed: a 0 is drawn as a baseline tick, not left blank), the rest as the reference that does move
the lookup. MAIN names the two kinds on the first panel's bars (direct labels) and defines them in the subtitle.

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
import itertools
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bridge_jspace import plot_style as PS
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
SUBTITLE = "% switched to the new answer; lookups read it from the prompt, recalls from memory"
HOW_MAIN = "a stated bridge's change is pasted back in part: lens part, same-size random part, or rest"
HOW_FULL = "a stated bridge's change is pasted back in part; purple = lookups, grey = recalls"
NUM = r"(-?\d+(?:\.\d+)?)"
RECALL_LENS = re.compile(rf"recall, lens-readable part \(the control, needs >= 30%\): {NUM}% \[{NUM}, {NUM}\]")
REST = re.compile(rf"lookup, the rest \(needs >= 50%\): {NUM}%")
RANDOM = re.compile(rf"same-share random part \(jspace_matched\): lookups {NUM}% \[{NUM}, {NUM}\] n=(\d+), "
                    rf"recalls {NUM}% \[{NUM}, {NUM}\] n=(\d+)")  # fmt: skip


FAMS = ("lookups", "recalls")
COLOR = {"lookups": C.LOOKUP, "recalls": C.RECALL}  # one shade per kind for the lens part and the rest
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

W, DX = 0.42, 0.24  # bar width; lookups at -DX, recalls at +DX of the part's place
ALIGN = 15.0  # a place's two value labels whose bars' tops are this close (in %) are printed at one height


def shift(fr: C.Frame, top: float = 0, bottom: float = 0) -> None:
    """Move the panels' top down by `top` points (room for panel headings under the frame's header) and their bottom
    down by `bottom` points (the frame keeps room for an x label these panels do not have)."""
    gs = fr.axes[0].get_subplotspec().get_gridspec()
    h = 72 * fr.fig.get_figheight()
    gs.update(top=gs.top - top / h, bottom=gs.bottom - bottom / h)


def head(ax, left: str, right: str, size: float = C.LABEL, right_size: float = C.NOTE) -> None:
    """A panel's heading: `left` and a grey word at the right (the verdict)."""
    ax.annotate(left, (0, 1), xycoords="axes fraction", xytext=(0, 10), textcoords="offset points", ha="left",
                va="bottom", fontsize=size, color=C.INK)  # fmt: skip
    ax.annotate(right, (1, 1), xycoords="axes fraction", xytext=(0, 10), textcoords="offset points", ha="right",
                va="bottom", fontsize=right_size, color=C.CAPTION_INK)  # fmt: skip


def crosses(ax, bb) -> bool:
    """A curve of the panel (Line2D gid "curve") passes through the box (each segment sampled in display space)."""
    for ln in ax.get_lines():
        if ln.get_gid() != "curve":
            continue
        xy = ln.get_transform().transform(ln.get_xydata())
        for (x0, y0), (x1, y1) in itertools.pairwise(xy):
            if any(bb.contains(x0 + (x1 - x0) * k / 40, y0 + (y1 - y0) * k / 40) for k in range(41)):
                return True
    return False


def free(ax, t, avoid: list) -> bool:
    """`t` inside its panel, touching no marker or interval of the figure, no curve or bar of its panel and no text
    in `avoid`."""
    r = PS.renderer(ax.figure)
    bb = t.get_window_extent(r).padded(2)
    box = ax.get_window_extent(r)
    if not (box.contains(bb.x0, bb.y0) and box.contains(bb.x1, bb.y1)) or crosses(ax, bb):
        return False
    if any(bb.overlaps(g) for _, g in PS.graphic_boxes(ax.figure, r)):
        return False
    if any(p.get_height() > 0 and bb.overlaps(p.get_window_extent(r)) for p in ax.patches):
        return False
    # both boxes grown by 2 px, as plot_style.overlaps (the save's check) grows each text: a gap under 4 px is a touch
    return not any(bb.overlaps(o.get_window_extent(r).padded(2)) for o in avoid if o is not t)


def place(ax, cands: list, make, placed: list, *, required: bool = False):
    """The first candidate whose text (`make(*candidate)`) is free (see `free`), added to `placed`. None free: nothing
    drawn, or with `required` the first candidate (the save's overlap check then names it)."""
    for cand in cands:
        t = make(*cand)
        ax.figure.canvas.draw()
        if free(ax, t, placed):
            placed.append(t)
            return t
        t.remove()
    if required and cands:
        t = make(*cands[0])
        placed.append(t)
        return t
    return None


def top_of(num: C.Number | None) -> float:
    """The top of a bar's mark: its interval's upper end, else its value."""
    return 0.0 if num is None else max(num.value, num.ci[1] if num.ci else num.value)


def draw_panel(ax, bars: Bars, *, ticks: tuple[str, ...], label: tuple[str, ...], pale: bool = False,
               random_values: bool = False, pad: float = 0.52) -> list:  # fmt: skip
    """Three places (lens, random, rest), two bars each (lookups, recalls; the random part light grey), thin light
    intervals. Values printed above the lens part's bars of the families in `label` (bold) and, with `random_values`,
    above the random part's bars (grey): each over its own bar, the two of a place at one height when their bars end
    within ALIGN of each other (one family labelled: above both bars, clear of the other's interval). A bar under half
    a percent gets a short baseline tick in its color, so a 0 reads as a 0, not as missing. Returns the labels."""
    texts = []
    for i, part in enumerate(PARTS):
        nums = {fam: bars.parts[fam].get(part) for fam in FAMS}
        shown = [f for f in FAMS if nums[f] is not None and ((part == "lens" and f in label) or
                                                              (part == "random" and random_values))]  # fmt: skip
        tops = {f: top_of(nums[f]) for f in FAMS}
        both = max(tops.values())
        for fam, dx in zip(FAMS, (-DX, DX), strict=True):
            num = nums[fam]
            if num is None:
                continue
            x = i + dx
            color = PALE if pale else C.CONTROL if part == "random" else COLOR[fam]
            ax.bar(x, num.value, width=W, color=color, linewidth=0, zorder=2)
            if num.value < 0.5:  # drawn as nothing: a baseline tick in the bar's color
                ax.plot([x - W / 2, x + W / 2], [0, 0], color=color, linewidth=4, solid_capstyle="butt", zorder=2.5,
                        clip_on=False)  # fmt: skip
            if num.ci is not None:
                lo, hi = max(0.0, num.ci[0]), num.ci[1]
                ax.plot([x, x], [lo, hi], color=C.INK, linewidth=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"],
                        solid_capstyle="butt", zorder=3, gid="ci")  # fmt: skip
            if fam not in shown:
                continue
            together = (len(shown) == 1 and part == "lens") or (
                len(shown) == 2 and abs(tops[FAMS[0]] - tops[FAMS[1]]) <= ALIGN
            )
            strong = part == "lens" and not pale
            # two labels at one height sit side by side over bars 2 DX apart, narrower than two bold values in a
            # four-panel row: the second family's label goes one line up, so the pair never overlaps
            lift = C.NOTE * 1.25 if together and len(shown) == 2 and fam == FAMS[1] else 0
            texts.append(ax.annotate(f"{RD.r0(num.value)}%", (x, both if together else tops[fam]), xytext=(0, 4 + lift),
                                     textcoords="offset points", ha="center", va="bottom", fontsize=C.NOTE,
                                     color=C.INK if strong else C.CAPTION_INK,
                                     fontweight="bold" if strong else "normal", gid="value", zorder=4))  # fmt: skip
    ax.set_xlim(-pad, len(PARTS) - 1 + pad)  # a narrow panel needs more room for the first label
    ax.set_xticks(range(len(PARTS)), ticks)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 50, 100], ["0", "50", "100"])
    ax.spines["bottom"].set_color(C.CONTROL)
    return texts


def direct_labels(ax, bars: Bars, placed: list) -> None:
    """'lookups' and 'recalls' in their colors right above a bar of theirs (the rest's, else the lens part's; above
    its value label if it has one), at the first free place: the legend, drawn on the data."""
    for fam in FAMS:
        cands = []
        for part in ("rest", "lens"):
            num = bars.parts[fam].get(part)
            if num is None:
                continue
            x = PARTS.index(part) + (-DX if fam == FAMS[0] else DX)
            cands += [(x + off, top_of(num), dy, ha) for dy in (4, 22)
                      for off, ha in ((0, "center"), (-W / 2, "left"), (W / 2, "right"))]  # fmt: skip

        def make(x, y, dy, ha, fam=fam):
            return ax.annotate(fam, (x, y), xytext=(0, dy), textcoords="offset points", ha=ha, va="bottom",
                               fontsize=C.NOTE, color=COLOR[fam], fontweight="bold", gid="direct", zorder=4)  # fmt: skip

        place(ax, cands, make, placed)


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
    fr = C.frame("main", TITLE, SUBTITLE, how=HOW_MAIN, caption=" ".join(exc) + "\n" + untested(b), nrows=1,
                 ncols=len(shown), left=0.085, wspace=0.12, sharey=True)  # fmt: skip
    shift(fr, top=30, bottom=C.LABEL * 1.8)
    numbers: list[C.Number] = [x.parts["lookups"]["lens"] for x in fails]  # the caption's numbers
    for ax, bars in zip(fr.axes, shown, strict=True):
        # "lens part" on two lines: on one it runs into "random" in a four-panel row
        texts = draw_panel(ax, bars, ticks=("lens\npart", "random", "rest"), label=FAMS, random_values=True)
        head(ax, C.MODEL[bars.model].name, SHOWN_WORD.get(bars.word, bars.word), right_size=C.LABEL)
        numbers += bars.numbers()
        if ax is fr.axes[0]:
            direct_labels(ax, bars, texts)
        else:
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
    fr = C.frame("full", TITLE, SUBTITLE, how=HOW_FULL, caption=f"{line1}\n{untested(b)}", nrows=len(rows),
                 ncols=len(cols), size=(12.0, 3.0 + 2.55 * len(rows)), left=0.125, wspace=0.2, hspace=0.62)  # fmt: skip
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
            draw_panel(ax, bars, ticks=("lens", "random", "rest"), label=FAMS[:1], pale=pale, pad=0.68)
            head(ax, RB.show(s), SHOWN_WORD.get(bars.word, bars.word), size=C.NOTE, right_size=C.NOTE)
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
