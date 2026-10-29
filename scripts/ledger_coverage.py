"""ledger_coverage: the coverage table of docs/depth/EXPERIMENTS.md (Dan, 29 Oct 01:15), generated from the committed
coverage matrix (scripts/x52_coverage.py's matrix.json): rows = the matrix's tests in its order, columns = 27B /
Lightning / 9B / Muse, each cell the matrix's status and note verbatim (the Lightning gate sentence, said once above
the table, left out of the cells). A row whose test has a ledger card links to it. scripts/check_ledger.py checks that
the table in the document equals this output, so the table cannot drift from the matrix.

uv run python scripts/ledger_coverage.py            # prints the table
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "results" / "x52_coverage" / "matrix-20261029T000836Z" / "matrix.json"
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


def cell(c: dict, gate: str) -> str:
    note = c["note"].replace("; " + gate, "").replace(gate, "").strip()
    status = c["status"]
    if note.startswith(status + ":"):
        note = note[len(status) + 1 :].strip()
    text = f"**{status}**" + (f": {note}" if note else "")
    return text.replace("|", "/")


def table(matrix: Path = MATRIX) -> str:
    m = json.loads(matrix.read_text())
    lines = ["| test | " + " | ".join(name for _, name in COLUMNS) + " |", "|---" * (len(COLUMNS) + 1) + "|"]
    for r in m["rows"]:
        name = r["row"].replace("|", "/")
        if r["row"] in ANCHORS:
            name = f"[{name}](#{ANCHORS[r['row']]})"
        lines.append(f"| {name} | " + " | ".join(cell(r["cells"][k], m["lightning_gate"]) for k, _ in COLUMNS) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(table())
