"""summary_states on a SYNTHETIC grid.csv (no result file is read): every readme_draft state shown as one of four, the
counts per setting (a setting's parts judged together), findings 2 and 8 merged (the worse shown), the lens listed
beside and the breakdown rows ignored, the few-items mark."""

from __future__ import annotations

import csv
import io

from scripts import cross_model_grid as G
from scripts import readme_draft as RD
from scripts.figs import summary_states as SS

MAIN_LENS = "J++, synthetic, 00000000"
# (model, finding, grid.csv setting, verdict, n); every other model and finding has no row (missing)
SYNTH = (
    ("27b", "f3", "draw 1", "holds", 300), ("27b", "f3", "draw 2", "holds", 300),
    ("27b", "f3", "prose", "fails (the name hidden leaves > 35% right)", 20),  # mixed; its only failure has n < 30
    ("27b", "f4", "draw 1", "fails", 300), ("27b", "f4", "draw 2", "holds", 300), ("27b", "f4", "table", "fails", 20),
    ("27b", "f5", "draw 1", "holds", 300), ("27b", "f5", "draw 1, 3rd on", "holds", 400),
    ("27b", "f5", "draw 2", "fails", 300), ("27b", "f5", "draw 2, 3rd on", "holds", 400),  # draw 2: mixed parts
    ("27b", "f6", "filler moved", "holds", 400), ("27b", "f6", "one statement more", "holds", 400),
    ("27b", "gate", "v1 (at the word)", "holds", 60), ("27b", "gate", "v2 (after the word)", "fails", 60),
    ("27b", "f7", "main rule", "inconclusive (the lookup moves between 10% and 30%)", 100),
    ("27b", "f7", "amended rule", "holds", 100),
    ("27b", "f2", "draw 1", "holds", 120), ("27b", "f2", "draw 2", "holds", 180),
    ("27b", "f8", "stated bridge, draw 1", "fails", 120),  # findings 2 and 8 disagree: the worse is shown
    ("27b", "f1", "animal suite", "open (descriptive, no committed rule)", 400),
    ("27b", "f1", "animal suite · lookup, bridge stated", "fails", 100),  # a breakdown row: not judged
    ("9b", "f3", "draw 1", "holds", 300),
    ("9b", "f2", "draw 2", "holds", 180),
    ("9b", "f8", "stated bridge, draw 2", "not interpretable (no recall written)", 180),  # holds beats can't tell
    ("9b", "f1", "animal suite", "not testable (no lens)", None),
    ("olmo", "f2", "table", "not testable (gate v1 failed)", None),
    ("olmo", "f8", "last tokens", "open (values only)", 250),  # values only beats not testable
)  # fmt: skip
BESIDE_ROW = ("27b", "f6", "one statement fewer", "fails", 400)  # another lens, listed beside: never read


def synth_csv(rows=SYNTH, beside=(BESIDE_ROW,)) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(G.COLUMNS)
    for (m, f, s, verdict, n), lens in [*((r, MAIN_LENS) for r in rows),
                                        *((r, "plain J-lens (synthetic, listed beside)") for r in beside)]:  # fmt: skip
        w.writerow([G.MODEL[m].label, G.FINDING[f].name, s, lens, "" if n is None else n, "" if n is None else "50.0 %",
                    "" if n is None else "[40.0, 60.0]", "", verdict, "", "-", f"results/fake/{m}_{f}/summary.json"])  # fmt: skip
    return out.getvalue()


def table(rows=SYNTH) -> dict[tuple[int, str], SS.SummaryCell]:
    cells, _ = RD.read_grid(synth_csv(rows))
    return SS.summary_cells(cells)


def row_of(label: str) -> int:
    return next(i for i, r in enumerate(SS.SUMMARY_ROWS) if r.label == label)


def test_every_state_and_finding_is_covered():
    assert set(SS.SHOWN) == set(RD.STATES) and set(SS.WORSE) == set(RD.STATES)
    assert set(SS.SHOWN.values()) == {"holds", "fails", "can't tell", "not tested"}
    assert {f for r in SS.SUMMARY_ROWS for f in r.findings} == {f.key for f in G.FINDINGS}  # no finding left out
    assert [r.lens for r in SS.SUMMARY_ROWS] == [False] * 4 + [True] * 5  # the lookup's route, then the lens claims


def test_states_and_counts():
    tab = table()

    def got(label: str, model: str) -> tuple[str, str, bool]:
        c = tab[(row_of(label), model)]
        return c.state, c.label, c.few

    assert got("The last tokens read the answer's digit", "27b") == ("mixed", "✗ 2/3", True)  # failing only at n < 30
    assert got("The lookup ends in a late attention read", "27b") == ("mixed", "✗ 1/3", False)  # one failure n=300
    assert got("Order label, then the bridge's identity", "27b") == ("mixed", "✗ 1/2", False)  # settings, not parts
    assert got("The label counts list order", "27b") == ("holds", "✓ 2/2", False)  # the beside lens's fail ignored
    assert got("Lens reads the bridge at its word", "27b") == ("holds", "✓ 1/1", False)
    assert got("… after its word", "27b") == ("fails", "✗ 0/1", False)
    # the main rule's inconclusive is not judged
    assert got("A lens push writes recall, not the lookup", "27b") == ("holds", "✓ 1/1", False)
    assert got("The lookup ignores the lens-readable part", "27b") == ("fails", "✗ 2/3", False)  # 8 fails: the worse
    assert got("Removing the J-space spares the lookup", "27b") == ("values only", "?", False)  # breakdown row ignored
    assert got("The last tokens read the answer's digit", "9b") == ("holds", "✓ 1/1", False)
    assert got("The lookup ignores the lens-readable part", "9b") == ("holds", "✓ 1/1", False)
    assert got("Removing the J-space spares the lookup", "9b") == ("not testable", "–", False)
    assert got("The lookup ignores the lens-readable part", "olmo") == ("values only", "?", False)
    assert got("The last tokens read the answer's digit", "gemma") == ("missing", "–", False)
    assert len(tab) == len(SS.SUMMARY_ROWS) * len(G.MODELS)
    assert tab[(row_of("The last tokens read the answer's digit"), "27b")].shown == "fails"


def test_an_empty_grid_is_not_tested_everywhere():
    assert {c.label for c in table(()).values()} == {"–"}
