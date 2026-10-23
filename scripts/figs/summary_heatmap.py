"""summary_heatmap: the README's summary, claims x models, on the shared scaffold (Dan's decisions, 23 Oct).

summary_heatmap_main (slides, the README's top): the eight claims of the two groups ("How a lookup works", "What the
J-space carries") against the eight models (hybrids, then attention-only, apart under small grey headings); a cell is
its state's color with the state written in it (blank: not tested), † where finding 7's amended rule differs.
summary_heatmap_full (the README's details): every row (the second counting test too); a cell adds "k/j" (settings that
hold / settings judged), the judged settings that did not hold (with their items when fewer than 30), and why a cell
can't tell or was not tested.

States and their rules: scripts/figs/summary_states.py (readme_draft's committed rule per setting; no "mixed"). Colors:
plot_style.VERDICT_COLOR. The title is Dan's; the caption lists every cell that fails and why the blank cells were not
tested, both computed from the grid. The data file holds one record per cell (its state, counts and misses).

uv run python -m scripts.figs.summary_heatmap [--grid results/cross_model/<stamp>] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import collections
import itertools
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import matplotlib.patheffects as pe
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from bridge_jspace import plot_style as PS
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C
from scripts.figs import summary_states as SS

STEM = "summary_heatmap"
TITLE = "The lookup's route holds on all eight models; the lens part doesn't"  # Dan, 23 Oct
SUBTITLE = "Each cell: a model's verdict on a claim over all its runs; ≈ chance = drops to guessing"
# MAIN has no how-to-read line: its rows need the height (the title takes two lines), and every cell names its state
HOW = {"main": None, "full": "k/j = settings that hold / judged, then those that did not; † = the amended rule differs"}
SIZE = {"main": C.MAIN_SIZE, "full": (12.0, 10.5)}
MARGIN = 0.36  # inches: the frame's text starts at 3% of the width
RIGHT = 0.2  # inches right of the cells
GAP = 0.02  # inches: half the white gap between two cells
COL_GAP = 0.3  # inches between the hybrids and the attention-only models
ROW_GAP = 0.28  # inches between the two groups of rows (the second group's heading)
PAD = 0.15  # inches between the row labels and the cells
NAMES_Y = 0.04  # inches between the cells and the model names above them
LINE = 0.95  # line spacing of multi-line labels and cell texts
NB = " "  # a space a cell's text is never broken at ("≈ chance", "5 items")
# shorter words for a FULL cell (the caption keeps readme_build.reason's)
WHY = {"a control failed": "control failed", "the rule: inconclusive": "rule: unclear", "no rule (values only)": "no rule",
       "still running": "running", "too few usable scenes": "too few scenes",
       "too few items answered right": "too few items", "no layer to test": "no layer",
       "not on Zach's branch": "not run"}  # fmt: skip
SETTING_WORDS = (("main rule, draw 2", "set 2"), ("main rule", "set 1"), ("stated bridge, ", "stated, "),
                 ("draw ", "set "), ("one statement ", "one "), ("long context", "long ctx"),
                 ("tasks, Zach's rule", "Zach's tasks"), ("filler moved", "moved filler"))  # fmt: skip


def setting_name(s: str) -> str:
    for a, b in SETTING_WORDS:
        s = s.replace(a, b)
    return s


def wrap(fig: Figure, text: str, size: float, width: float, max_lines: int, weight: str = "normal") -> str | None:
    """`text` broken at spaces into lines no wider than `width` inches as drawn; None if it needs more lines."""
    words = text.split(" ")
    lines = [words[0]]
    for w in words[1:]:
        if PS.text_width(fig, f"{lines[-1]} {w}", size, weight) <= width:
            lines[-1] = f"{lines[-1]} {w}"
        else:
            lines.append(w)
    if len(lines) > max_lines or any(PS.text_width(fig, x, size, weight) > width for x in lines):
        return None
    return "\n".join(lines)


def fill(c: SS.Cell) -> str:
    if c.state in SS.WHERE:
        return C.VERDICT_COLOR["descriptive"]
    return C.VERDICT_COLOR["holds" if c.state == "holds (Zach)" else c.state]


def main_text(c: SS.Cell) -> list[str]:
    """MAIN: the state alone (blank where not tested; the amended rule's † is in FULL)."""
    return [] if c.state == "not tested" else [c.state]


def full_text(c: SS.Cell) -> list[str]:
    """FULL: the state with k/j, then the judged settings that did not hold (or why there is no verdict)."""
    if c.state in SS.WHERE or c.state == "holds (Zach)":  # Zach's own word ("holds-ish") is in the caption
        return [c.state]
    if c.state in ("can't tell", "not tested"):
        return [c.state, WHY.get(c.why, c.why)]
    out = [f"{c.state.replace(' ', NB)} {c.held}/{c.judged}" + (" †" if c.amended_differs else "")]
    if not c.misses or c.state != "holds":  # the exceptions inside a cell that holds; elsewhere k/j says it
        return out
    if len(c.misses) > 2:
        k = collections.Counter(s.state for s in c.misses)
        return [*out, ", ".join(f"{n} {'at chance' if st == '≈ chance' else 'fail'}" for st, n in k.items())]
    return out + [f"{setting_name(s.setting)} {'≈' + NB + 'chance' if s.state == '≈ chance' else 'fails'}"
                  + (f" ({s.n}{NB}items)" if s.n is not None and s.n < SS.FEW_ITEMS else "") for s in c.misses]  # fmt: skip


def cell_lines(fig: Figure, phrases: list[str], width: float) -> str:
    out = []
    for p in phrases:
        w = wrap(fig, p, C.NOTE, width, 3)
        if w is None:
            raise ValueError(f"a cell's text does not fit its width: {p!r}")
        out.append(w)
    return "\n".join(out)


# ---------------------------------------------------------------- the caption: computed from the cells


def failures(tab: dict[tuple[str, str], SS.Cell], rows: tuple[SS.Row, ...]) -> list[str]:
    """'moved filler (32B)': per row, the models whose cell fails."""
    out = []
    for r in rows:
        ms = [C.MODEL[m].short for m in RB.ORDER if tab[(r.key, m)].state == "fails"]
        if ms:
            out.append(f"{r.short} ({', '.join(ms)})")
    return out


def untested(tab: dict[tuple[str, str], SS.Cell], rows: tuple[SS.Row, ...], short: bool) -> list[str]:
    by: dict[str, list[str]] = collections.defaultdict(list)
    for m in RB.ORDER:
        for r in rows:
            c = tab[(r.key, m)]
            why = WHY.get(c.why, c.why) if short else c.why
            if c.state == "not tested" and why not in by[m]:
                by[m].append(why)
    return [f"{C.MODEL[m].short} ({', '.join(by[m])})" for m in RB.ORDER if by[m]]


def caption(fig: Figure, tab: dict[tuple[str, str], SS.Cell], rows: tuple[SS.Row, ...], grid: str, kind: str) -> str:
    """At most two lines that fit the figure's width: the cells that fail, the Zach note, why cells were not tested,
    and (last) the grid; the phrases in any order that fits, each in its longest wording that still lets everything
    fit (else ValueError). The list of failing cells shortens to their models (MAIN) or is left out (FULL, whose cells
    name them)."""
    fails = failures(tab, rows)
    zach = {m: tab[(r.key, m)].zach for r in rows for m in RB.ORDER if tab[(r.key, m)].zach}
    own = [f"{C.MODEL[m].short}: “{w}”" for m, w in zach.items() if w != "holds"]  # where his word was not "holds"
    phrases: list[list[str]] = []  # each phrase's wordings, longest first; shortened in this list's order
    if zach:
        also = f" ({'; '.join(own)})" if own else ""
        phrases.append([f"(Zach): his plan; his verdict files are not on his branch yet{also}.",
                        f"(Zach): his plan; files not on his branch yet{also}."])  # fmt: skip
    nt_long, nt_short = untested(tab, rows, False), untested(tab, rows, True)
    if nt_long:
        phrases.append([f"Not tested: {', '.join(nt_long)}.", f"Not tested: {', '.join(nt_short)}.",
                        f"Not tested: {', '.join(x.replace('too few', 'few') for x in nt_short)}."])  # fmt: skip
    if fails:
        failed = [C.MODEL[m].short for m in RB.ORDER if any(tab[(r.key, m)].state == "fails" for r in rows)]
        shorter = "" if kind == "full" else f"Fails: {', '.join(failed)}."
        phrases.append([f"Fails: {'; '.join(fails)}.", shorter])
    phrases.reverse()  # the failing cells first on the page
    width = fig.get_size_inches()[0] - MARGIN - 0.12

    def fits(texts: list[str]) -> list[str] | None:
        lines: list[str] = []
        for text in texts:
            if lines and PS.text_width(fig, f"{lines[-1]} {text}", C.CAPTION) <= width:
                lines[-1] = f"{lines[-1]} {text}"
            else:
                lines.append(text)
        return lines if len(lines) <= 2 and all(PS.text_width(fig, x, C.CAPTION) <= width for x in lines) else None

    choice = [0] * len(phrases)
    while True:
        for order in itertools.permutations(range(len(phrases))):
            lines = fits([t for j in order if (t := phrases[j][choice[j]])] + [f"Grid {grid}."])
            if lines:
                return "\n".join(lines)
        longer = [j for j, p in enumerate(phrases) if choice[j] < len(p) - 1]
        if not longer:
            raise ValueError(f"the caption does not fit two lines: {[p[-1] for p in phrases]}")
        choice[max(longer)] += 1  # the Zach note first, then the reasons, the failing cells' claims last


# ---------------------------------------------------------------- drawing


def wrap_title(fr: C.Frame) -> None:
    """common.frame draws the title on one line; a title wider than the figure goes on two, the lines below move down."""
    fig = fr.fig
    w, h = fig.get_size_inches()
    r = PS.renderer(fig)
    t = next(x for x in fig.texts if x.get_gid() == "title")
    text = wrap(fig, t.get_text(), C.TITLE, w - 2 * MARGIN, 3, "bold")
    if text is None or "\n" not in text:
        return
    before = t.get_window_extent(r).height
    t.set_text(text)
    t.set_linespacing(1.0)
    dy = (t.get_window_extent(r).height - before) / fig.dpi / h
    for x in fig.texts:
        if x.get_gid() in ("subtitle", "how"):
            x.set_y(x.get_position()[1] - dy)


def draw(tab: dict[tuple[str, str], SS.Cell], rows: tuple[SS.Row, ...], kind: str, grid: str) -> C.Frame:
    fr = C.frame(kind, TITLE, SUBTITLE, how=HOW[kind], caption="x\nx", size=SIZE[kind])
    fig, ax = fr.fig, fr.axes[0]
    w, h = fig.get_size_inches()
    r = PS.renderer(fig)
    wrap_title(fr)
    cap = next(x for x in fig.texts if x.get_gid() == "caption")
    cap.set_text(caption(fig, tab, rows, grid, kind))
    header = [x for x in fig.texts if x.get_gid() in ("title", "subtitle", "how")]
    head = max(h - x.get_window_extent(r).y0 / fig.dpi for x in header)  # inches from the top
    cap_top = cap.get_window_extent(r).y1 / fig.dpi
    names_h, group_h = C.LABEL * 1.2 / 72, C.NOTE * 1.2 / 72
    band = NAMES_Y + names_h + 0.04 + 0.02 + group_h
    grid_top, grid_bottom = h - head - 0.08 - band, cap_top + 0.1
    rh = (grid_top - grid_bottom - ROW_GAP) / len(rows)
    sample = fig.text(0, 0, "Ag\nAg", fontsize=C.TICK, linespacing=LINE)
    two = sample.get_window_extent(r).height / fig.dpi + 0.03  # two label lines and the overlap check's margins
    sample.remove()
    lab_w = max(PS.text_width(fig, rw.label, C.TICK) for rw in rows)
    if rh >= two:  # rows tall enough for two-line labels: the narrowest width at which every label takes <= 2
        lab_w = next(x / 20 for x in range(36, 100) if all(wrap(fig, rw.label, C.TICK, x / 20, 2) for rw in rows))
    lab_w = max([lab_w] + [PS.text_width(fig, g, C.NOTE) for g in SS.GROUPS])  # the row groups' headings
    left = MARGIN + lab_w + PAD
    pitch = (w - left - RIGHT - COL_GAP) / len(C.MODELS)
    grid_w, grid_h = w - left - RIGHT, grid_top - grid_bottom
    ax.set_position((left / w, grid_bottom / h, grid_w / w, grid_h / h))
    ax.set_xlim(0, grid_w)
    ax.set_ylim(grid_h, 0)  # data units: inches from the grid's top-left corner
    ax.set_xticks([])
    ax.set_yticks([])  # no tick labels at all (axis "off" hides them but the overlap check would still see them)
    ax.axis("off")
    full_names = max(PS.text_width(fig, m.name, C.LABEL) for m in C.MODELS) <= pitch - 0.08
    xs = {m.key: (i + 0.5) * pitch + (0 if m.hybrid else COL_GAP) for i, m in enumerate(C.MODELS)}
    first = {g: min(i for i, rw in enumerate(rows) if rw.group == g) for g in {rw.group for rw in rows}}
    ys = [i * rh + (ROW_GAP if rw.group > 0 else 0.0) for i, rw in enumerate(rows)]  # each row's top
    inner = pitch - 2 * GAP - 0.02
    for i, rw in enumerate(rows):
        label = (wrap(fig, rw.label, C.TICK, lab_w, 2) if rh >= two else None) or rw.label
        ax.text(-PAD, ys[i] + rh / 2, label, ha="right", va="center", fontsize=C.TICK, linespacing=LINE)
        for m in C.MODELS:
            c = tab[(rw.key, m.key)]
            x0 = xs[m.key] - pitch / 2
            white = c.state == "not tested"  # outlined: white on white
            ax.add_patch(Rectangle((x0 + GAP, ys[i] + GAP), pitch - 2 * GAP, rh - 2 * GAP, facecolor=fill(c), zorder=1,
                                   edgecolor=C.VERDICT_EDGE if white else "none", linewidth=1.2 if white else 0))  # fmt: skip
            text = cell_lines(fig, main_text(c) if kind == "main" else full_text(c), inner)
            if text:
                ax.text(xs[m.key], ys[i] + rh / 2, text, ha="center", va="center", fontsize=C.NOTE, zorder=4,
                        color=C.CAPTION_INK if c.state == "not tested" else C.INK, linespacing=LINE, gid="value",
                        path_effects=[pe.withStroke(linewidth=4, foreground=fill(c))])  # fmt: skip
    # above the cells (negative y): the model names, a thin rule and the model group's heading above it
    for g, i in first.items():  # a small grey heading above each group of rows
        y = -NAMES_Y if i == 0 else ys[i] - ROW_GAP / 2
        ax.text(-PAD, y, SS.GROUPS[g], ha="right", va="bottom" if i == 0 else "center", fontsize=C.NOTE,
                color=C.CAPTION_INK, gid="group")  # fmt: skip
    for m in C.MODELS:
        ax.text(xs[m.key], -NAMES_Y, m.name if full_names else m.short, ha="center", va="bottom", fontsize=C.LABEL,
                color=C.INK)  # fmt: skip
    rule_y = -(NAMES_Y + names_h + 0.04)
    for label, hybrid in (("Hybrids", True), ("Attention-only", False)):
        cols = [xs[m.key] for m in C.MODELS if m.hybrid == hybrid]
        ax.add_line(Line2D([min(cols) - pitch / 2 + GAP, max(cols) + pitch / 2 - GAP], [rule_y] * 2, lw=1,
                           color=C.CONTROL, clip_on=False))  # fmt: skip
        ax.text((min(cols) + max(cols)) / 2, rule_y - 0.02, label, ha="center", va="bottom", fontsize=C.NOTE,
                color=C.CAPTION_INK, gid="group")  # fmt: skip
    return fr


def numbers(tab: dict[tuple[str, str], SS.Cell], rows: tuple[SS.Row, ...]) -> list[C.Number]:
    """One record per drawn cell (not a grid value: common.check_numbers skips it)."""
    out = []
    for rw in rows:
        for m in RB.ORDER:
            c = tab[(rw.key, m)]
            out.append(C.Number(float(c.held), f"{rw.label}: settings that hold", model=m, source="summary_states",
                                extra={"row": rw.key, "state": c.state, "judged": c.judged, "zach": c.zach,
                                       "amended_differs": c.amended_differs, "why": c.why,
                                       "misses": [[s.finding, s.setting, s.state, s.n] for s in c.misses]}))  # fmt: skip
    return out


def summary_heatmap(grid_dir: Path, kind: str, out: Path = C.OUT) -> list[Path]:
    cells, _ = RD.read_grid((grid_dir / "grid.csv").read_text())
    rows = SS.MAIN_ROWS if kind == "main" else SS.ROWS
    tab = SS.table(cells, rows)
    return C.save(draw(tab, rows, kind, grid_dir.name), STEM, numbers(tab, rows), out)


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
    grid_dir = Path(a.grid) if a.grid else newest_grid()
    for kind in ("main", "full") if a.only is None else (a.only,):
        for p in summary_heatmap(grid_dir, kind, Path(a.out)):
            print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
