"""necessity: does a stated bridge need its lens-readable part? (Dan, 23 Oct 15:30; Dan's figure guide.)

The stated-bridge parts runs (statement_positions, judged for finding 2 by d1_verdict): the stated bridge is changed
(Jack's pet: cow -> pig) and the change, or a part of it, is pasted back. Bars, % switched to the new bridge's answer,
lookups (the accent) and recalls (dark grey) side by side: the whole change (Δ, part "full"), the change without its
lens-readable part (Δ−J, "not_jspace"), the lens-readable part alone (J, "jspace"), the change without a random part
of J's size (Δ−rand, "not_rand_sub": not in these runs, so not drawn; its bar appears where a run has its rows) and a
random part of J's share (rand, "jspace_matched"; light grey, its values printed, a 0 drawn as a baseline tick).

Runs: only the opened scene-set-2 parts runs the finding-2 grid cells name (their verdict.json's "parts"): the 27B and
9B at their decisive cell, the 122B at its decisive cell (context, layer 24) and at layers 27 and 30 of the same run and
position set (EXTRA_LAYERS). Rates: d1_verdict.rate on the cell's rows (source cf, not the random-direction null).
At a decisive cell every number the grid has is the grid's (finding 2's cell value and its control text, via
stated_bridge.collect) after the run's rows are checked against it and against the verdict.json (a mismatch raises);
the rest comes from the run's outcomes.jsonl (source = that file). No committed rule judges necessity: values only.

MAIN: the three decisive cells; FULL: also the 122B at layers 27 and 30.

uv run python scripts/figs/necessity.py [--grid DIR] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import functools
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bridge_jspace.stats import wilson
from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C
from scripts.figs import stated_bridge as SB

STEM = "necessity"
F = "f2"
MODELS = ("27b", "9b", "122b")
EXTRA_LAYERS = {"122b": (27, 30)}  # Dan, 23 Oct 15:30: the 122B also at layers 27 and 30 (same run, same set)
# (run part, tick label); Δ−rand (not_rand_sub) is drawn only where a run has its rows (none of these runs has)
PARTS = (("full", "whole"), ("not_jspace", "minus J"), ("jspace", "J only"), ("not_rand_sub", "minus rand"),
         ("jspace_matched", "random"))  # fmt: skip
FAMILY = {"lookups": "PP", "recalls": "PM"}
SP = G.RESULTS / "statement_positions"

TITLE = "Only recall needs the lens-readable part"
SUBTITLE = "% switched; lookups read the answer from the prompt, recalls from memory"
HOW = "J = the stated bridge's lens-readable part; values only (no rule), n = {n}"


@dataclass
class Cell:
    """One parts cell: family ("lookups" / "recalls") -> run part -> Number (percent, Wilson 95%)."""

    model: str
    setting: str
    where: str  # the position set (context, bridge_word, bind_bridge)
    layer: int
    decisive: bool
    n: int
    parts: dict[str, dict[str, C.Number]] = field(default_factory=dict)

    def numbers(self) -> list[C.Number]:
        return [n for fam in self.parts.values() for n in fam.values()]


@functools.cache
def rows_of(path: Path) -> tuple[dict, ...]:
    """A parts run's patched rows (source cf, not the random-direction null), as d1_verdict.block selects them."""
    keep = []
    for line in path.read_text().splitlines():
        r = json.loads(line)
        if r["source"] == "cf" and not r["null"]:
            keep.append(r)
    return tuple(keep)


def rate(rows: tuple[dict, ...], family: str, where: str, layer: int, part: str) -> list:
    """[rate, lo, hi, n] of the rows switched to the new bridge's answer (role b): d1_verdict.rate."""
    got = [r for r in rows if r["family"] == family and r["set"] == where and r["layer"] == layer and r["part"] == part]
    return [*wilson(sum(r["role"] == "b" for r in got), len(got)), len(got)]


def collect(b: RB.Book, m: str, root: Path = C.REPO, sp: Path = SP) -> list[Cell]:
    """The model's cells: its decisive cell (finding 2's main scene set) and EXTRA_LAYERS; [] without a value."""
    setting = SB.main_setting(b, m)
    c = SB.cell_of(b, m, setting)
    grid = SB.collect(b, m, setting, root)  # the grid's numbers there, checked against the verdict file
    if c is None or grid is None:
        return []
    v = json.loads((root / c.path).read_text())
    where, decisive = v["cell"]["set"], int(v["cell"]["layer"])
    path = sp / v["parts"] / "outcomes.jsonl"
    rows = rows_of(path)
    src = str(path.relative_to(C.REPO)) if path.is_relative_to(C.REPO) else str(path)
    out = []
    for layer in (decisive, *EXTRA_LAYERS.get(m, ())):
        cell = Cell(m, setting, where, layer, layer == decisive, 0)
        for fam, family in FAMILY.items():
            cell.parts[fam] = {}
            for part, _ in PARTS:
                t = rate(rows, family, where, layer, part)
                if t[3]:
                    cell.parts[fam][part] = C.Number(100 * t[0], f"{fam} switched, part {part}", F, m, setting, "",
                                                     (100 * t[1], 100 * t[2]), t[3], source=src,
                                                     extra={"family": family, "part": part, "set": where,
                                                            "layer": layer})  # fmt: skip
        if not all(cell.parts[f].get(p) for f in FAMILY for p in ("full", "not_jspace", "jspace")):
            raise ValueError(f"necessity {m}: no full / not_jspace / jspace rows at {where} layer {layer} in {src}")
        cell.n = cell.parts["lookups"]["full"].n or 0
        if cell.decisive:
            use_grid(cell, grid, v)
        out.append(cell)
    return out


def use_grid(cell: Cell, grid: SB.Bars, v: dict) -> None:
    """At the decisive cell: the run's rates checked against the grid (its rounding) and the verdict file (exactly),
    then the grid's numbers drawn where it has them."""
    same = (
        ("lookups", "jspace", grid.parts["lookups"]["lens"], 0.05),
        ("lookups", "not_jspace", grid.parts["lookups"]["rest"], 0.5),
        ("recalls", "jspace", grid.parts["recalls"]["lens"], 0.5),
        ("recalls", "not_jspace", grid.parts["recalls"]["rest"], 1e-9),
        *((f, "jspace_matched", grid.parts[f]["random"], 0.5) for f in FAMILY if "random" in grid.parts[f]),
    )
    for fam, part, num, tol in same:
        if abs(cell.parts[fam][part].value - num.value) > tol + 1e-9:
            raise ValueError(f"necessity {cell.model}: the run's {fam} {part} is not the grid's")
    for fam, key in (("lookups", "lookup"), ("recalls", "recall")):
        if abs(cell.parts[fam]["full"].value - 100 * v[key]["full"][0]) > 1e-9:
            raise ValueError(f"necessity {cell.model}: the run's {fam} full is not the verdict file's")
    for fam, part, num, _ in same:
        cell.parts[fam][part] = num


def shown_parts(cells: list[Cell]) -> list[tuple[str, str]]:
    """The parts with rows in any drawn cell, in PARTS order (Δ−rand only once a run has it)."""
    return [(p, t) for p, t in PARTS if any(p in c.parts[f] for c in cells for f in FAMILY)]


# ---------------------------------------------------------------- drawing


def draw_panel(ax, cell: Cell, parts: list[tuple[str, str]]) -> list:
    """Per part two bars (lookups, recalls; the random part light grey), thin light intervals; the values printed
    above the bars minus J (bold) and the random part's (grey), each over its own bar, else leaning outward, else
    higher (the first free place: stated_bridge.place); a 0 bar drawn as a baseline tick. Returns the labels."""
    ax.set_xlim(-0.55, len(parts) - 0.45)
    ax.set_xticks(range(len(parts)), [t for _, t in parts])
    ax.tick_params(axis="x", length=0, pad=6)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 50, 100], ["0", "50", "100"])
    ax.spines["bottom"].set_color(C.CONTROL)
    labels = []
    for i, (part, _) in enumerate(parts):
        for fam, dx in zip(FAMILY, (-SB.DX, SB.DX), strict=True):
            num = cell.parts[fam].get(part)
            if num is None:
                continue
            x = i + dx
            color = C.CONTROL if part == "jspace_matched" else SB.COLOR[fam]
            ax.bar(x, num.value, width=SB.W, color=color, linewidth=0, zorder=2)
            if num.value < 0.5:
                ax.plot([x - SB.W / 2, x + SB.W / 2], [0, 0], color=color, linewidth=4, solid_capstyle="butt",
                        zorder=2.5, clip_on=False)  # fmt: skip
            if num.ci is not None:
                ax.plot([x, x], [max(0.0, num.ci[0]), num.ci[1]], color=C.INK, linewidth=C.ERRORBAR["elinewidth"],
                        alpha=C.ERRORBAR["alpha"], solid_capstyle="butt", zorder=3, gid="ci")  # fmt: skip
            if part in ("not_jspace", "jspace_matched"):
                labels.append((x, dx, num, part == "not_jspace"))
    texts: list = []
    for x, dx, num, strong in labels:  # after every bar is drawn, so a label keeps off its neighbours
        out = "right" if dx < 0 else "left"
        edge = x + (SB.W / 2 if dx < 0 else -SB.W / 2)

        def make(xx, ha, dy, num=num, strong=strong):
            return ax.annotate(f"{RD.r0(num.value)}%", (xx, SB.top_of(num)), xytext=(0, dy), textcoords="offset points",
                               ha=ha, va="bottom", fontsize=C.NOTE, color=C.INK if strong else C.CAPTION_INK,
                               fontweight="bold" if strong else "normal", gid="value", zorder=4)  # fmt: skip

        SB.place(ax, [(x, "center", 4), (edge, out, 4), (x, "center", 22), (edge, out, 22)], make, texts,
                 required=True)  # fmt: skip
    return texts


def direct_labels(ax, cell: Cell, parts: list[tuple[str, str]], placed: list) -> None:
    """'lookups' and 'recalls' in their colors right above a bar of theirs (whole, else without J), first free place."""
    names = [p for p, _ in parts]
    for fam, dx in zip(FAMILY, (-SB.DX, SB.DX), strict=True):
        cands = []
        for part in ("full", "not_jspace"):
            num = cell.parts[fam].get(part)
            if num is not None and part in names:
                x = names.index(part) + dx
                cands += [(x + off, SB.top_of(num), dy, ha) for dy in (4, 22)
                          for off, ha in ((0, "center"), (-SB.W / 2, "left"), (SB.W / 2, "right"))]  # fmt: skip

        def make(x, y, dy, ha, fam=fam):
            return ax.annotate(fam, (x, y), xytext=(0, dy), textcoords="offset points", ha=ha, va="bottom",
                               fontsize=C.NOTE, color=SB.COLOR[fam], fontweight="bold", gid="direct", zorder=4)  # fmt: skip

        SB.place(ax, cands, make, placed)


def falls(cells: list[Cell]) -> list[str]:
    """The exceptions: where the lookups' interval minus J lies below the whole change's (the lookup needs J too).
    One cell of a model: '122B: minus J, lookups fall from 99% to 75%'; several: the layers (values in the panels)."""
    out = []
    for m in MODELS:
        mine = [c for c in cells if c.model == m]
        down = [c for c in mine if (w := c.parts["lookups"]["full"].ci) and (r := c.parts["lookups"]["not_jspace"].ci)
                and r[1] < w[0]]  # fmt: skip
        if len(mine) == 1 and down:
            c = down[0]
            out.append(f"{C.MODEL[m].short}: minus J, lookups fall from {RD.r0(c.parts['lookups']['full'].value)}% "
                       f"to {RD.r0(c.parts['lookups']['not_jspace'].value)}%.")  # fmt: skip
        elif down:
            out.append(f"{C.MODEL[m].short}: minus J, lookups fall at layer{'s' if len(down) > 1 else ''} "
                       f"{', '.join(str(c.layer) for c in down)}.")  # fmt: skip
    return out


def caption(b: RB.Book, cells: list[Cell], parts: list[tuple[str, str]]) -> str:
    hook = "" if any(p == "not_rand_sub" for p, _ in parts) else " A 'minus rand' bar comes with today's runs."
    return f"{(' '.join(falls(cells)) + hook).strip()}\n{SB.untested(b)}"


def how(cells: list[Cell]) -> str:
    ns = sorted({c.n for c in cells})
    return HOW.format(n=f"{ns[0]}-{ns[-1]}" if len(ns) > 1 else f"{ns[0]}")


def head_of(cell: Cell) -> str:
    return f"layer {cell.layer}"


def figure_main(b: RB.Book, root: Path = C.REPO, sp: Path = SP) -> tuple[C.Frame, list[C.Number]]:
    cells = [c for m in MODELS for c in collect(b, m, root, sp) if c.decisive]
    return figure(b, cells, "main")


def figure_full(b: RB.Book, root: Path = C.REPO, sp: Path = SP) -> tuple[C.Frame, list[C.Number]]:
    cells = [c for m in MODELS for c in collect(b, m, root, sp)]
    return figure(b, cells, "full")


def figure(b: RB.Book, cells: list[Cell], kind: str) -> tuple[C.Frame, list[C.Number]]:
    if not cells:
        raise ValueError("necessity: no cell to draw")
    parts = shown_parts(cells)
    ncols = min(3, len(cells))
    nrows = (len(cells) + ncols - 1) // ncols
    size = None if kind == "main" else (12.0, 3.3 + 3.4 * nrows)
    fr = C.frame(kind, TITLE, SUBTITLE, how=how(cells), caption=caption(b, cells, parts), nrows=nrows, ncols=ncols,
                 size=size, left=0.085, wspace=0.12, hspace=0.6, sharey=True)  # fmt: skip
    SB.shift(fr, top=30, bottom=C.LABEL * 1.8)
    numbers: list[C.Number] = []
    for i, ax in enumerate(fr.axes):
        if i >= len(cells):
            ax.remove()
            continue
        cell = cells[i]
        texts = draw_panel(ax, cell, parts)
        SB.head(ax, C.MODEL[cell.model].name, head_of(cell), right_size=C.NOTE)
        numbers += cell.numbers()
        if i == 0:
            direct_labels(ax, cell, parts, texts)
        if i % ncols:
            ax.tick_params(axis="y", labelleft=False)
        else:
            ax.set_ylabel("% switched")
    return fr, numbers


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    ap.add_argument("--grid", type=Path, default=None, help="results/cross_model/<stamp> (default: the newest)")
    ap.add_argument("--only", choices=("main", "full"), default=None)
    ap.add_argument("--out", type=Path, default=C.OUT)
    a = ap.parse_args(argv)
    b = C.book(a.grid or SB.newest_grid())
    for kind, make in (("main", figure_main), ("full", figure_full)):
        if a.only in (None, kind):
            fr, numbers = make(b)
            for p in C.save(fr, STEM, numbers, a.out):
                print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
