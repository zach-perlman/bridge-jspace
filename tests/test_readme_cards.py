"""The depth README v6 (Dan, 28 Oct ~14:30): experiments as cards E1-E16 with six fields in a fixed order, one figure per
card (a pending card says "None yet"; E15 is a table), and a claims table that links every card and grades each claim
with A, B, C, ✗ or …."""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAGE = REPO / "docs" / "depth" / "README.md"
FIELDS = ("Hypothesis", "Mechanics", "Data", "Result", "Figure", "Conclusion")
CARD = re.compile(r"^### (E\d+)\. (.+?) <a id=\"([a-z0-9-]+)\"></a>$", re.M)
GRADES = {"A", "B", "C", "✗", "…"}


def cards(text: str) -> dict[str, str]:
    """Card id -> its body, from its heading to the next heading of level <= 3 (E10c's level-4 card stays inside E10)."""
    heads = list(CARD.finditer(text))
    out = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end() : end]
        nxt = re.search(r"^## ", body, re.M)
        out[m.group(1)] = body[: nxt.start()] if nxt else body
    return out


def claims_rows(text: str) -> list[list[str]]:
    table = text.split("## Claims", 1)[1].split("\n## ", 1)[0]
    rows = [r for r in table.splitlines() if r.startswith("| ") and not r.startswith("| #") and not r.startswith("|---")]
    return [[c.strip() for c in re.sub(r"<!--.*?-->", "", r).strip()[1:-1].split("|")] for r in rows]


def test_sixteen_cards_in_order():
    ids = [m.group(1) for m in CARD.finditer(PAGE.read_text())]
    assert ids == [f"E{i}" for i in range(1, 17)], ids


def test_every_card_has_the_six_fields_in_order():
    for cid, body in cards(PAGE.read_text()).items():
        main = body.split("#### ", 1)[0]  # E10c is checked as its own block below
        found = [f for f in re.findall(r"\*\*(\w+)\.\*\*", main) if f in FIELDS]
        assert found == list(FIELDS), (cid, found)


def test_one_figure_per_card_or_pending_or_a_table():
    for cid, body in cards(PAGE.read_text()).items():
        main = body.split("#### ", 1)[0]
        figs = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", main)
        if "**Figure.** None yet." in main:
            assert not figs and "Sealed" in main, cid
        elif cid == "E15":
            assert "| Account |" in main, cid
        else:
            assert len(figs) == 1, (cid, figs)


def test_claims_table_links_every_card_and_grades_mechanically():
    text = PAGE.read_text()
    rows = claims_rows(text)
    linked = set(re.findall(r"\(#(e\d+[a-z]?-[a-z-]+)\)", text.split("## Claims", 1)[1].split("\n## ", 1)[0]))
    anchors = {m.group(3) for m in CARD.finditer(text)}
    assert anchors <= linked, sorted(anchors - linked)
    for r in rows:
        grade = re.sub(r"\*\*", "", r[8]).split(" ")[0]
        assert grade in GRADES, (r[0], r[8])
        if r[0] in ("✗", "…"):
            assert grade == r[0], r[0]
