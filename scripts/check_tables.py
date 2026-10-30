"""check_tables: no blank or placeholder cell in any README table (Dan 30 Oct, depth README brief).

A cell with no result says why: "not run", "below gate (0.73 < 0.80)", "not designed", "Q-before gate failed". A bare dash,
an empty cell or "can't tell" without its reason is a defect; a row that ran on one model leaves the grid for a sentence
under the table.

uv run python scripts/check_tables.py         # the three READMEs, exit 1 on a defect
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
READMES = (REPO / "README.md", REPO / "docs" / "depth" / "README.md", REPO / "docs" / "breadth" / "README.md")
PLACEHOLDERS = {"", "–", "-", "—", "?", "n/a", "N/A", "can't tell", "can’t tell"}
COMMENT = re.compile(r"<!--.*?-->", re.S)
SEPARATOR = re.compile(r"^\s*\|[-: |]+\|\s*$")


def cells(row: str) -> list[str]:
    s = row.strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") else s
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def empty_cells(text: str) -> list[str]:
    """'line N, column K: <row start>' for every body cell of every table that is blank or a bare placeholder."""
    lines = COMMENT.sub("", text).split("\n")
    out = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and SEPARATOR.match(lines[i + 1]):
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                cs = cells(lines[j])
                out += [f"line {j + 1}, column {k + 1}: {cs[0][:50]!r} has {c!r}" for k, c in enumerate(cs)
                        if c in PLACEHOLDERS]  # fmt: skip
                j += 1
            i = j
        else:
            i += 1
    return out


def main() -> int:
    bad = 0
    for path in READMES:
        if not path.exists():
            continue
        found = empty_cells(path.read_text(encoding="utf-8"))
        bad += len(found)
        for f in found:
            print(f"{path.relative_to(REPO)}: {f}")
    print(f"check_tables: {bad} blank or placeholder cell(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
