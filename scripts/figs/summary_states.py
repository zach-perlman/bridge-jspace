"""summary_states: one state per (summary row, model) for the README's summary figure, from grid.csv.

A row is a finding in plain words (the lens gate split into its two reads; findings 2 and 8 merged). A cell's state is
readme_draft.model_state (the committed per-model rule, imported, not reimplemented) over the model's main-lens cells
of the row (readme_draft.read_grid: grid.csv's lens column without "listed beside", breakdown rows left out), shown as
one of four: holds / fails (mixed drawn as fails) / can't tell / not tested. Where findings 2 and 8 disagree, the worse
verdict is shown (fails, then mixed, then holds); where neither has a verdict, the more informative state (can't tell
before not tested); the counts are over both findings' settings.

Counts: "✓ k/j" = holds in k of the j settings judged (holds, fails or mixed); a setting with parts (finding 5's 1st-2nd
and 3rd on) is judged by model_state over its parts. "few": the cell is drawn as fails and every failing grid cell
behind it has fewer than FEW_ITEMS items (the README: "too few items").

Pure functions only: no drawing, no file reading (pass readme_draft.read_grid's cells).
"""

from __future__ import annotations

import collections
from dataclasses import dataclass

from scripts import cross_model_grid as G
from scripts import readme_draft as RD

FEW_ITEMS = 30
# readme_draft's states shown as four; mixed is drawn as fails (hatched)
SHOWN = {"holds": "holds", "fails": "fails", "mixed": "fails", "unclear": "can't tell", "values only": "can't tell",
         "not testable": "not tested", "missing": "not tested"}  # fmt: skip
WORSE = ("fails", "mixed", "holds", "unclear", "values only", "not testable", "missing")  # first = shown


@dataclass(frozen=True)
class SummaryRow:
    label: str
    findings: tuple[str, ...]  # grid findings; two (2 and 8): the worse of their states is shown
    setting: str = ""  # one grid setting only (the lens gate's two reads); "": every setting of the finding

    @property
    def lens(self) -> bool:
        return G.FINDING[self.findings[0]].lens


SUMMARY_ROWS = (
    SummaryRow("The last tokens read the answer's digit", ("f3",)),
    SummaryRow("The lookup ends in a late attention read", ("f4",)),
    SummaryRow("Order label, then the bridge's identity", ("f5",)),
    SummaryRow("The label counts list order", ("f6",)),
    SummaryRow("Lens reads the bridge at its word", ("gate",), "v1 (at the word)"),
    SummaryRow("… after its word", ("gate",), "v2 (after the word)"),
    SummaryRow("A lens push writes recall, not the lookup", ("f7",)),
    SummaryRow("The lookup ignores the lens-readable part", ("f2", "f8")),
    SummaryRow("Removing the J-space spares the lookup", ("f1",)),
)
ROW_GROUPS = (("The lookup's route", False), ("The lens claims", True))  # label, SummaryRow.lens


@dataclass(frozen=True)
class SummaryCell:
    state: str  # readme_draft.model_state over the row's cells for the model (the worse of two findings')
    held: int  # settings that hold
    judged: int  # settings that hold, fail or are mixed
    few: bool  # shown as fails, and every failing cell has fewer than FEW_ITEMS items

    @property
    def shown(self) -> str:
        return SHOWN[self.state]

    @property
    def label(self) -> str:
        """'✓ 3/3', '✗ 1/4', '?' (can't tell) or '–' (not tested)."""
        if self.shown in ("holds", "fails"):
            return f"{'✓' if self.shown == 'holds' else '✗'} {self.held}/{self.judged}"
        return "?" if self.shown == "can't tell" else "–"


def summary_cell(cells: list[RD.Cell], row: SummaryRow, model: str) -> SummaryCell:
    per = [[c for c in cells if c.model == model and c.finding == f and row.setting in ("", c.setting)]
           for f in row.findings]  # fmt: skip
    state = min((RD.model_state(c.word for c in cs) for cs in per), key=WORSE.index)
    mine = [c for cs in per for c in cs]
    by: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for c in mine:
        by[(c.finding, c.setting)].append(c.word)
    settings = [RD.model_state(ws) for ws in by.values()]
    held = settings.count("holds")
    failing = [c for c in mine if c.word == "fails"]
    few = SHOWN[state] == "fails" and bool(failing) and all(c.n is not None and c.n < FEW_ITEMS for c in failing)
    return SummaryCell(state, held, held + settings.count("fails") + settings.count("mixed"), few)


def summary_cells(cells: list[RD.Cell]) -> dict[tuple[int, str], SummaryCell]:
    """(row index in SUMMARY_ROWS, model key) -> its cell, for every row and every model of the grid."""
    return {(i, m.key): summary_cell(cells, row, m.key) for i, row in enumerate(SUMMARY_ROWS) for m in G.MODELS}
