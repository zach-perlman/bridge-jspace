"""digit_not_name: finding 3, "The last tokens read the answer's digit, not the entity's name" (Dan's figure guide 6b).

The late_read layout (scripts/figs/late_read.py's dot plot): rows = models, one panel per setting, x = % of lookups
still right. Two marks per row, in the model's colors (filled = hybrid, hollow = attention-only), each with a thin 95%
interval: the dot = the answer's sentence without its name hidden from the tokens after the question (the chat
template's tokens up to the answer; only the name visible: the digit hidden; the grid cell's value), the diamond = the
sentence without its digit hidden (only the digit visible: the name
hidden; the cell's control text). A light grey band = chance (per cell, from its control text). Value labels only on
the exceptions: a cell that fails the rule or whose dot stays above chance.
digit_not_name_main: the three scene sets (stacked in the row), table, JSON; models with a judged cell.
digit_not_name_full: the prose format added, not-interpretable cells in pale grey, and a small grey tick: the lowest of
the off-path control (the same parts of another sentence hidden; the rule needs >= 90%).

uv run python -m scripts.figs.digit_not_name [--grid results/cross_model/<stamp>] [--only main|full] [--out DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts import readme_build as RB
from scripts import readme_draft as RD
from scripts.figs import common as C
from scripts.figs import late_read as LR

F = "f3"
STEM = "digit_not_name"
NAME_MAX = 35.0  # the rule (cross_model_grid RULES["name-digit"]): only the name visible leaves <= 35% right
# the digit left visible = the name hidden: readme_build.CONTROLS["f3"]["digit visible"], with its interval
DIGIT_ONLY = LR.Control("digit visible", RB.CONTROLS["f3"]["digit visible"] + r" \[(\d+), (\d+)\]",
                        "% right, the sentence without its digit hidden (only the digit visible)", "digit only")  # fmt: skip
# the off-path control: the lowest of an off-path sentence's parts hidden at both places
OFF_PARTS = LR.Control("another sentence", RB.CONTROLS["f3"]["another sentence"],
                       "% right, an off-path sentence's part hidden instead (the lowest)")  # fmt: skip
MAIN_PANELS = (LR.MAIN_PANELS[0], LR.Panel("Table", ("table",)), LR.Panel("JSON", ("JSON",)))
FULL_PANELS = (LR.MAIN_PANELS[0], LR.Panel("Prose", ("prose",)), *MAIN_PANELS[1:])
WHAT = "% right, the sentence without its name hidden (only the name visible)"


def why_f3(c: RD.Cell) -> LR.Control | None:
    """A failing cell whose dot passes the rule's 35% fails on the other half: only the digit visible keeps < 70%."""
    return DIGIT_ONLY if c.value is not None and c.value <= NAME_MAX else None


TITLE = "The last tokens need the digit, not the name"
SUBTITLE = "% still right when the tokens after the question see only the name, or only the digit"
HOW = {"main": "dot = name only, diamond = digit only. Left = the lookup breaks. Grey band = chance.",
       "full": "dot = name only, diamond = digit only, tick = another sentence. Band = chance."}  # fmt: skip
RULE = "dot ≤ 35%, diamond ≥ 70%, tick ≥ 90%"


def digit_not_name(b: RB.Book, kind: str, out: Path = C.OUT) -> list[Path]:
    panels = MAIN_PANELS if kind == "main" else FULL_PANELS
    dots = LR.Dots(F, WHAT, tick=OFF_PARTS if kind == "full" else None, second=DIGIT_ONLY, why=why_f3)
    cap = LR.caption(b, F, panels, why_f3, RULE, kind)
    return LR.dot_figure(b, dots, panels, kind, TITLE, SUBTITLE, HOW[kind], cap, STEM, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", default=None, help="a results/cross_model/<stamp> folder (default: the newest)")
    ap.add_argument("--only", choices=("main", "full"), default=None, help="one version (default: both)")
    ap.add_argument("--out", default=str(C.OUT), help="output folder (default figures/cross_model)")
    a = ap.parse_args(argv)
    b = RB.Book(Path(a.grid) if a.grid else LR.newest_grid())
    for kind in ("main", "full") if a.only is None else (a.only,):
        for p in digit_not_name(b, kind, Path(a.out)):
            print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
