"""summary_states: the README summary's state per (row, model), from grid.csv's main-lens cells (Dan's decisions, 23 Oct).

Rows (ROWS): one claim each, in plain words, in two groups (GROUPS: "How a lookup works", "What the J-space carries");
the MAIN figure shows the rows flagged main, the FULL figure all of them. Finding 6 is two rows (the moved filler; one
sentence more or fewer), findings 2 and 8 are one, the lens gate is a descriptive row (where the lens reads a stated
bridge: WHERE), finding 7 reads its main rule only (each run once).

States (STATES): holds · holds (Zach) · fails · ≈ chance · can't tell · not tested. No "mixed" (Dan).

Per setting (a grid setting; finding 5's two parts judged together):
  ≈ chance     a cell that misses the late read's <= 20% bar (its verdict: "more than 20% right") while its 95% interval
               covers the chance level its control text states ("chance N%")
  otherwise    readme_draft.model_state (the committed rule, imported) over the setting's cells, shown as holds; fails
               (also a setting whose parts disagree); can't tell (a control failed, the rule's own inconclusive, values
               only); not tested (not testable, missing)
Per model and finding: the judged settings (holds, fails, ≈ chance) decide by majority: holds if more hold than not;
else ≈ chance if more are at chance than fail; else fails (a tie is not a hold). No judged setting: can't tell if a
setting can't tell, else not tested. The judged settings that did not hold are kept (misses), for the FULL figure.
Findings 2 and 8 in one row: the worse state (WORSE order), counts over both.
Finding 7: amended_differs where the amended rule's verdict on a run differs from the main rule's (drawn as †).
Finding 1: where the grid has no verdict under Zach's rule, his verdict from his Day 3 plan (ZACH): "holds (Zach)".

Pure functions only: pass readme_draft.read_grid's cells.
"""

from __future__ import annotations

import collections
import re
from dataclasses import dataclass

from scripts import cross_model_grid as G
from scripts import readme_build as RB
from scripts import readme_draft as RD

FEW_ITEMS = RB.FEW  # a setting with fewer items: "(n items)" beside it in the FULL figure
GROUPS = ("How a lookup works", "What the J-space carries")
STATES = ("holds", "holds (Zach)", "fails", "≈ chance", "can't tell", "not tested")
WHERE = ("at its word only", "at and after its word", "at its word", "not at its word")  # the lens gate's values
SHOWN = {"holds": "holds", "fails": "fails", "mixed": "fails", "unclear": "can't tell", "values only": "can't tell",
         "not testable": "not tested", "missing": "not tested"}  # readme_draft's states per setting  # fmt: skip
WORSE = ("fails", "≈ chance", "holds", "holds (Zach)", "can't tell", "not tested")  # findings 2 and 8: first wins
CHANCE_BAR = "more than 20% right"  # the late-read rule's verdict text when a cell misses its <= 20% bar
ZACH_SETTING = "tasks, Zach's rule"
# Zach's verdicts on his rule (J-space knock-out), from his Day 3 plan as Dan relayed them (23 Oct): C1 holds on the 27B
# (gap 36; its verdict file is in the grid), 9B (38), 32B (22, one random control 13 off), Muse "holds-ish" (gap 7).
# His verdict files for these three are not on his branch yet.
ZACH = {"9b": "holds", "32b": "holds", "muse": "holds-ish"}


@dataclass(frozen=True)
class Row:
    key: str
    label: str
    short: str  # the claim in a caption's list of exceptions
    group: int  # index in GROUPS
    findings: tuple[str, ...]
    settings: tuple[str, ...] = ()  # the grid settings read; (): all of the finding's
    main: bool = True  # in the MAIN figure
    where: bool = False  # descriptive (the lens gate): a WHERE value, not a verdict


ROWS = (
    Row("f3", "The last tokens read the answer's digit", "digit read", 0, ("f3",)),
    Row("f4", "The lookup ends in a late attention read", "late read", 0, ("f4",)),
    Row("f5", "Order label, then the bridge's identity", "order label", 0, ("f5",)),
    Row("f6a", "Moved filler: follows list order", "moved filler", 0, ("f6",), ("filler moved",)),
    Row("f6b", "One sentence more / fewer", "one sentence more / fewer", 0, ("f6",),
        ("one statement more", "one statement fewer"), main=False),
    Row("lens", "Where the lens reads a stated bridge", "where the lens reads", 1, ("gate",), where=True),
    Row("f7", "A lens push writes recall, not the lookup", "lens push", 1, ("f7",), ("main rule", "main rule, draw 2")),
    Row("f28", "The lookup ignores the lens-readable part", "lens part", 1, ("f2", "f8")),
    Row("f1", "Removing the J-space spares the lookup", "J-space removal", 1, ("f1",)),
)  # fmt: skip
ROW = {r.key: r for r in ROWS}
MAIN_ROWS = tuple(r for r in ROWS if r.main)


@dataclass(frozen=True)
class Setting:
    finding: str
    setting: str
    state: str  # holds, fails, ≈ chance, can't tell, not tested
    n: int | None  # its items (the smaller part's, for finding 5)


@dataclass(frozen=True)
class Cell:
    state: str  # one of STATES, or a WHERE value on the lens gate's row
    held: int = 0  # settings that hold
    judged: int = 0  # settings that hold, fail or are at chance
    misses: tuple[Setting, ...] = ()  # judged settings that did not hold
    amended_differs: bool = False
    zach: str = ""  # Zach's own word, where the state comes from his plan
    why: str = ""  # can't tell / not tested: a few words why


def chance_of(control: str) -> float | None:
    m = re.search(r"chance (\d+(?:\.\d+)?)%", control)
    return float(m.group(1)) if m else None


def at_chance(c: RD.Cell) -> bool:
    """A cell that misses the late read's <= 20% bar while its 95% interval covers the chance level."""
    ch = chance_of(c.control)
    return (c.word == "fails" and CHANCE_BAR in c.verdict and c.ci is not None and ch is not None
            and c.ci[0] <= ch <= c.ci[1])  # fmt: skip


def setting_state(cs: list[RD.Cell]) -> str:
    if any(at_chance(c) for c in cs) and not any(c.word == "fails" and not at_chance(c) for c in cs):
        return "≈ chance"
    return SHOWN[RD.model_state(c.word for c in cs)]


def settings_of(cs: list[RD.Cell]) -> list[Setting]:
    by: dict[tuple[str, str], list[RD.Cell]] = collections.defaultdict(list)
    for c in cs:
        by[(c.finding, c.setting)].append(c)
    out = []
    for (f, s), parts in by.items():
        ns = [c.n for c in parts if c.n is not None]
        out.append(Setting(f, s, setting_state(parts), min(ns) if ns else None))
    return out


def decide(ss: list[Setting]) -> str:
    h, f, c = (sum(s.state == w for s in ss) for w in ("holds", "fails", "≈ chance"))
    if h + f + c == 0:
        return "can't tell" if any(s.state == "can't tell" for s in ss) else "not tested"
    if h > f + c:
        return "holds"
    return "≈ chance" if c > f else "fails"


def why(cs: list[RD.Cell], state: str) -> str:
    if state == "can't tell":
        if any(c.word == "not interpretable" for c in cs):
            return "a control failed"
        return "the rule: inconclusive" if any(c.word == "inconclusive" for c in cs) else "no rule (values only)"
    text = " ".join(c.verdict for c in cs)
    if "which failed" in text or " failed at the " in text:  # readme_build.reason reads "waits on" as running
        return "a run failed"
    return RB.reason(cs)


def amended_differs(cs: list[RD.Cell]) -> bool:
    """Finding 7: the amended rule's verdict on some run differs from the main rule's on the same run."""
    word = {c.setting: c.word for c in cs}
    return any(s.startswith("main rule") and word.get(s.replace("main rule", "amended rule", 1), w) != w
               for s, w in word.items())  # fmt: skip


def where_cell(cs: list[RD.Cell]) -> Cell:
    word = {c.setting: c.word for c in cs}
    at, after = word.get("v1 (at the word)"), word.get("v2 (after the word)")
    if at == "holds":
        return Cell({"fails": "at its word only", "holds": "at and after its word"}.get(after or "", "at its word"))
    if at == "fails":
        return Cell("not at its word")
    state = SHOWN[RD.model_state(word.values())]
    return Cell(state, why=why(cs, state))


def cell(cells: list[RD.Cell], row: Row, model: str) -> Cell:
    mine = [c for c in cells if c.model == model and c.finding in row.findings]
    if row.where:
        return where_cell(mine)
    read = [c for c in mine if not row.settings or c.setting in row.settings]
    per = [settings_of([c for c in read if c.finding == f]) for f in row.findings]
    state = min((decide(ss) for ss in per), key=WORSE.index)
    ss = [s for p in per for s in p]
    held = sum(s.state == "holds" for s in ss)
    misses = tuple(s for s in ss if s.state in ("fails", "≈ chance"))
    zach = ""
    graded = any(c.setting == ZACH_SETTING and c.word in ("holds", "fails") for c in read)  # his verdict in the grid
    if "f1" in row.findings and model in ZACH and state in ("can't tell", "not tested") and not graded:
        state, zach = "holds (Zach)", ZACH[model]
    return Cell(state, held, held + len(misses), misses, "f7" in row.findings and amended_differs(mine), zach,
                why(read, state) if state in ("can't tell", "not tested") else "")  # fmt: skip


def table(cells: list[RD.Cell], rows: tuple[Row, ...] = ROWS) -> dict[tuple[str, str], Cell]:
    """(row key, model key) -> its cell, for every row and every model of the grid."""
    return {(r.key, m.key): cell(cells, r, m.key) for r in rows for m in G.MODELS}
