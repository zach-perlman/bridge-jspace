"""No blank or placeholder cell in any README table (Dan 30 Oct): a cell with no result says why."""

from __future__ import annotations

import pytest

from scripts import check_tables as C


def test_the_checker_flags_blank_dash_and_bare_cant_tell():
    table = "| | 9B | 27B |\n|---|---|---|\n| a | 1 | – |\n| b |  | can't tell |\n| c | not run | below gate (0.73 < 0.80) |\n"
    found = C.empty_cells(table)
    assert len(found) == 3
    assert not any("not run" in f or "below gate" in f for f in found)


def test_the_header_corner_and_html_comments_are_not_cells():
    table = "| | 9B |\n|---|---|\n| a | 1<!-- src: x \\| y --> |\n"
    assert C.empty_cells(table) == []


@pytest.mark.parametrize("path", C.READMES, ids=lambda p: p.parent.name or "root")
def test_readme_tables_have_no_blank_cells(path):
    if not path.exists():
        pytest.skip("no such README")
    assert not (found := C.empty_cells(path.read_text(encoding="utf-8"))), found
