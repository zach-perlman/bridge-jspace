"""ledger_coverage: the coverage table of docs/depth/EXPERIMENTS.md (Dan, 29 Oct 01:15), generated from the committed
coverage matrix (scripts/x52_coverage.py's matrix.json): rows = the matrix's tests in the README's order (Dan's
restructure brief, 29 Oct 08:55) under their Part, columns = 27B / Lightning / 9B / Muse, each cell the matrix's status
as a symbol (✓ done, ◐ partial, ○ below gate, – not tested, ✗ not designed) and its note verbatim as a numbered
footnote under the table (the Lightning gate sentence, said once above the table, left out). A row whose test has a
ledger card links to it. scripts/check_ledger.py checks that the table in the document equals this output, so the
table cannot drift from the matrix. Also the overview heatmap's data (HEATMAP; drawn by scripts/ledger_figures.py).

uv run python scripts/ledger_coverage.py            # prints the table
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "results" / "x52_coverage" / "matrix-20261029T062909Z" / "matrix.json"
COLUMNS = (("qwen3.6-27b", "27B"), ("nemotron-3.5-lightning", "Lightning"), ("qwen3.5-9b", "9B"),
           ("muse-glimmer-30b", "Muse"))  # fmt: skip
# the matrix's row -> the ledger card's anchor (rows without a card stay plain)
ANCHORS = {
    "1. Conflict test (main test, at L)": "lightning-conflict",
    "2. Answer control (51.12 E1)": "t51-12",
    "3. Routes test (identity / position / value; no address; address alone)": "routes",
    "4. Address swap by dose (x8_write, s = 1 / 2 / 4)": "swap",
    "5a. Order split (descriptive)": "order",
    "6. Anatomy by layer (47.8)": "t47-8",
    "8. Lens readout with the item-change control (47.0)": "t47-0",
    "E11: token by layer map (47.D1)": "d1",
    "E3: identity route outside the lens (47.1 atom slices)": "t47-1",
    "E7: six lockers, one code per slot (47.2)": "six",
    "7. Ladder (49.2, rungs 1-6)": "t49-2",
    "9. Last-token read / write (51.10)": "t51-10",
    "10. Attention under the swap (49.7)": "t49-7",
    "E12: address persistence across depth (D4, CPU)": "t47-8",
    "Dose curves, a part alone (51.1)": "t51-1",
    "Split in other texts: varied scenes (x0b)": "x0b",
    "Gain map (49.1)": "t49-1",
    "E6: the address probe (x0_probe v4)": "probe",
    "5b. Copy test (45q)": "t45q",
    "Earlier mention (45p)": "t45p",
    "Split in other texts: natural passages (x5)": "x5",
    "Described bridge (47.3, and 51.12's cue r2)": "t47-3",
    "E8: the report prompt (47.10)": "t47-10",
    "Failed: the address as the recall's second route (48 route2)": "t48-5",
    "Pooled person probe (49.3)": "t49-3",
    "Failed: copying heads pass the rest (48 heads)": "t48-4",
    "Failed: the J++ part keys the attribute; late MLPs (48.2 enrichment)": "t48-2",
    "What is left of the route; the value (47.7)": "t47-7c",
    "Zeroing at one layer (47.5)": "t47-5",
    "Address refit per text format (x45d)": "x45d",
    "The lookup's errors are not address errors (47.13)": "t47-13",
    "Failed: a person mark at the locker sentence (48.3 bind)": "t48-3",
    "Failed: blocking the pick sentence (47.6 edges)": "t47-6",
    "Failed: the address is the same for any kind of item (47.11 agnostic)": "t47-11",
    "Chained addresses (47.14)": "t47-14",
    "E6: the swap after neutral sentences (47.16 distance)": "t47-16",
    "E11: lookups carried before L (47.4 cumulative)": "t47-4",
    "Part V: Zach's passages Z1 / Z2 (x50)": "z1",
    "Part V: Zach's passages Z3 (routes on his passages)": "z3",
    "Learned subspaces (48 DAS; 51.3 DAS at scale)": "t51-3",
    "Joint head ablation under the swap (51.2)": "t51-2",
    "The address at the last token (51.4)": "t51-4",
    "Anatomy on Zach's passages (51.5)": "t51-5",
    "Z1 on the full carrier (51.7)": "t51-7",
    "What is the address: dimension, methods, geometry (51.11)": "t51-11",
    "Answer-direction control on Zach's Z2 (51.12 Z2)": "z2",
}

# The overview heatmap (Dan's restructure brief, 29 Oct 08:55): one row per test card in the ledger's (the README's)
# order, columns 27B / Lightning / 9B / Muse. Each cell is the card's verdict, shortened: H the hypothesis the card asks
# about (its rule's main one) holds, B in between or holds in part, F fails, D descriptive (no rule), N not tested
# (not run, not ported, running), X not designed for that model, G below the model's gate (Dan, 09:15: "not tested
# (gate x < 0.80)", any numbers descriptive only). The words after the code are what the cell shows; each is the card's
# own label or a shortening of it. Left out: Lightning's layer pick (a prerequisite, not a test), the 9B's clean reruns
# (How we checked), the withdrawn card and the running stub; the three one-model rows have no card.
VERDICT_CODES = {"H": "holds", "B": "in between or in part", "F": "fails", "D": "descriptive, no rule",
                 "N": "not tested", "X": "not designed", "G": "below gate"}  # fmt: skip
HEATMAP_LEFT_OUT = ("lightning-layer", "t49-5", "z2", "b52-c")
HEATMAP = (
    ("I", "lightning-conflict", "Conflict test, main test", ("B not confirmed", "H confirmed", "H confirmed", "H confirmed")),
    ("I", "t51-12", "Item or answer, main test", ("H the entity", "H answer not read", "H the entity", "H answer not read")),
    ("I", "t51-12", "Item or answer, his true facts", ("B mixed", "B mixed", "B mixed", "N not run")),
    ("I", "t51-12", "Item or answer, his made-up facts", ("B mixed", "G below gate", "B mixed", "N not run")),
    ("I", "x0b", "Split in prose, JSON, tables", ("H holds", "H holds", "H holds", "H holds")),
    ("I", "x5", "Split in natural passages", ("B mixed", "G below gate", "H holds°", "H holds")),
    ("I", "t51-1", "Each part added by itself", ("B (i) no", "B (ii) no", "H (i), (ii) yes", "H (i), (ii) yes")),
    ("I", "t47-5", "Zeroing at one layer", ("H not needed", "H not needed", "H not needed", "H not needed")),
    ("I", "t49-2", "Ladder: other copies taken out", ("B (a), (b) no", "G below gate", "B (b) no", "B (a), (b) no")),
    ("I", "t45p", "The item's earlier mention", ("H yes", "G below gate", "H yes", "H yes")),
    ("I", "t49-1", "Gain map: weight or route", ("F neither", "F neither", "F neither", "F neither")),
    ("I", "t48-1", "Two learned subspaces", ("F no", "N not ported", "F no", "F no")),
    ("I", "b52-a", "Inside the lens part", ("D bridge words", "D bridge words", "D bridge words", "D bridge words")),
    ("I", "b52-b", "Answer readable, usable", ("D descriptive", "D ours only", "D descriptive", "D descriptive")),
    ("II", "t47-1", "Identity route outside the lens", ("H outside", "H outside", "H outside", "H outside")),
    ("II", "routes", "Routes test and the address", ("B adding: no", "H both routes", "H both routes", "H both routes")),
    ("II", "t47-7c", "Never the value, by format", ("B incomplete", "B incomplete", "B incomplete", "B incomplete")),
    ("II", "t51-3", "Learned subspaces at scale", ("B (iii) no", "N not ported", "B (iii) no", "B (iii) no")),
    ("III", "probe", "Address probe", ("D readable", "D readable", "D readable", "D readable")),
    ("III", "swap", "Address swap, rule at dose 1", ("F no", "F no", "F no", "F no")),
    ("III", "t47-16", "Swap after neutral sentences", ("H robust", "H robust", "H robust", "H robust")),
    ("III", "six", "Six lockers, own code each", ("F none of three", "H own code", "H own code", "H own code")),
    ("III", "t51-11", "What the address is", ("B part 2 only", "N not ported", "B in between", "B mixed")),
    ("III", "t47-0", "Lens readout of the swap", ("H lens blind", "H lens blind", "H lens blind", "H lens blind")),
    ("III", "t47-10", "Report prompt", ("F neither", "G below gate", "G below gate", "G below gate")),
    ("III", "t51-2", "A few heads take the swap", ("F distributed", "F distributed", "F distributed", "F distributed")),
    ("III", "t49-7", "Attention follows the swap", ("F neither", "F neither", "F neither", "F neither")),
    ("III", "t47-14", "Chained addresses", ("F no", "G below gate", "F no", "F no")),
    ("IV", "order", "Split by sentence order", ("D by order", "D by order", "D by order", "D by order")),
    ("IV", "t45q", "Copy test, locker after", ("H yes", "G below gate", "H yes", "H yes")),
    ("IV", "d1", "Token-by-layer map", ("F (a)-(c) no", "F (a)-(c) no", "F (a)-(c) no", "F (a)-(c) no")),
    ("IV", "t47-4", "Lookups read before L", ("D before L", "D before L", "D before L", "D before L")),
    ("IV", "t47-8", "Anatomy by depth, handoff", ("F (a) no", "H (a) yes", "H (a) yes", "H (a) yes")),
    ("IV", "t51-4", "Address at the last token", ("F not there", "B in between", "F not there", "H travels")),
    ("IV", "t51-10", "Entity at the last token", ("B read, not used", "B read, not used", "B read, not used",
                                                  "B read, not used")),
    ("V", "z1", "Zach's passages, true facts", ("F lookup follows", "B in between", "F lookup follows",
                                                "F follows, few")),
    ("V", "z1", "Zach's passages, made-up facts", ("B in between", "G below gate", "H holds", "N not run")),
    ("V", "t51-7", "Full carrier up to L", ("B in between", "B in between", "B in between", "X not designed")),
    ("V", "z3", "Position route, his passages", ("F no position", "B in between", "B in between", "B in between")),
    ("V", "t51-5", "Read window, his passages", ("F not the same", "H same window", "H same window", "X not designed")),
    ("VI", "t47-3", "Described bridge", ("F through lens", "G below gate", "H holds", "H holds")),
    ("VI", "x45d", "Address refit per format", ("B neither", "H refit works", "H refit works", "H refit works")),
    ("VI", "t47-13", "Errors are address errors", ("N 5 errors", "F no", "F no", "F no")),
    ("VI", "t48-2", "Lens part keys the attribute", ("F no", "F no", "F no", "F no")),
    ("VI", "t48-3", "Person mark at the locker", ("F no", "G below gate", "F no", "F no")),
    ("VI", "t49-3", "Pooled person probe", ("B in between", "G below gate", "F neither", "F neither")),
    ("VI", "t48-4", "Copying heads pass the rest", ("F no", "F no", "F no", "F no")),
    ("VI", "t48-5", "Address as the recall's route", ("F no", "G below gate", "F no", "F no")),
    ("VI", "t47-6", "Blocking the pick sentence", ("F no", "N not ported", "F no", "F no")),
    ("VI", "t47-11", "Same address, any item", ("F no", "F no", "F no", "F no")),
)  # fmt: skip


def heatmap_cells() -> list[tuple[str, str, str, list[tuple[str, str]]]]:
    """(part, anchor, row label, [(code, words) per column 27B / Lightning / 9B / Muse]) in HEATMAP's order."""
    out = []
    for part, anchor, label, cells in HEATMAP:
        parsed = [(c[0], c[2:]) for c in cells]
        assert len(parsed) == len(COLUMNS) and all(code in VERDICT_CODES for code, _ in parsed), (label, cells)
        out.append((part, anchor, label, parsed))
    return out


# Dan's restructure brief (29 Oct 08:55): the table's cells are symbols, the matrix's notes numbered footnotes under it
SYMBOL = {"done": "✓", "partial": "◐", "below gate": "○", "not tested": "–", "missing": "–", "running": "–",
          "queued": "–", "not designed": "✗"}  # fmt: skip
LEGEND = ("✓ done, ◐ partial, ○ below the model's gate (not tested; a below-gate run is exploratory), – not tested "
          "(including missing, running or queued), ✗ not designed for that model; a number points to the matrix's note "
          "for that cell, listed under the table.")  # fmt: skip
PART_TITLE = {"I": "Part I. The two readers", "II": "Part II. Identity", "III": "Part III. The address",
              "IV": "Part IV. Where and when", "V": "Part V. Other datasets", "VI": "Part VI. What did not hold",
              None: "Withdrawn, or run on one model only"}  # fmt: skip
# not-tested cells whose matrix note does not name the gate, but whose card does (47.10: the report reader below 0.80
# in the cited verdict; the card's "not tested (gate x < 0.80)")
GATE_FROM_CARD = {("E8: the report prompt (47.10)", t) for t in ("qwen3.5-9b", "muse-glimmer-30b",
                                                                 "nemotron-3.5-lightning")}  # fmt: skip


def note_of(c: dict, gate: str) -> str:
    """The matrix's note for a cell, without the Lightning gate sentence (said once above the table) or a repeated
    status word."""
    note = c["note"].replace("; " + gate, "").replace(gate, "").strip()
    if note.startswith(c["status"] + ":"):
        note = note[len(c["status"]) + 1 :].strip()
    return note.replace("|", "/")


def status_of(c: dict, note: str, row: str = "", target: str = "") -> str:
    """The cell's symbol class: the matrix's status, with a not-tested cell whose reason is the gate read as below gate
    (DAS's note names the gate second, after the missing port: not tested)."""
    if c["status"] == "not tested" and (("gate" in note and not note.startswith("DAS"))
                                        or (row, target) in GATE_FROM_CARD):  # fmt: skip
        return "below gate"
    return c["status"]


def ordered_rows(m: dict) -> list[tuple[str | None, dict]]:
    """The matrix's rows in the README's order: by their card's place in HEATMAP (the ledger's order), rows without a
    card shown there (withdrawn, or no card) last, in the matrix's order."""
    first = {}
    for i, (part, anchor, _, _) in enumerate(HEATMAP):
        first.setdefault(anchor, (i, part))
    keyed = []
    for j, r in enumerate(m["rows"]):
        i, part = first.get(ANCHORS.get(r["row"], ""), (len(HEATMAP), None))
        keyed.append((i, j, part, r))
    return [(part, r) for _, _, part, r in sorted(keyed, key=lambda k: (k[0], k[1]))]


def table(matrix: Path = MATRIX) -> str:
    """The coverage table: one row per matrix row in the README's order under its Part, each cell a symbol and, where the
    matrix has a note, a footnote number; the notes numbered under the table (one number per distinct note)."""
    m = json.loads(matrix.read_text())
    gate = m["lightning_gate"]
    notes: dict[str, int] = {}
    lines = ["| test | " + " | ".join(name for _, name in COLUMNS) + " |", "|---" * (len(COLUMNS) + 1) + "|"]
    last = "start"
    for part, r in ordered_rows(m):
        if part != last:
            lines.append(f"| **{PART_TITLE[part]}** |" + " |" * len(COLUMNS))
            last = part
        name = r["row"].replace("|", "/")
        if r["row"] in ANCHORS:
            name = f"[{name}](#{ANCHORS[r['row']]})"
        cells = []
        for k, _ in COLUMNS:
            c = r["cells"][k]
            note = note_of(c, gate)
            sym = SYMBOL[status_of(c, note, r["row"], k)]
            if note:
                cells.append(f"{sym} <sup>{notes.setdefault(note, len(notes) + 1)}</sup>")
            else:
                cells.append(sym)
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    lines += ["", LEGEND, ""]
    lines += [f"{i}. {note}" for note, i in notes.items()]
    return "\n".join(lines)


if __name__ == "__main__":
    print(table())
