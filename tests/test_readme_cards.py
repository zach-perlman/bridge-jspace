"""The depth README v6, iteration 2 (Dan, 28 Oct ~15:40): ten experiment cards with six bullet fields in a fixed order
(E10 carries a second Result bullet, the earlier mention), one figure per card (E5 two, since Dan's round 3), no
footers, no internal names on the page, and a claims table of the A and B claims with a grade each."""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAGE = REPO / "docs" / "depth" / "README.md"
FIELDS = ("Hypothesis", "Mechanics", "Data", "Result", "Figure", "Conclusion")
CARD = re.compile(r"^### (E\d+)\. (.+?) <a id=\"([a-z0-9-]+)\"></a>$", re.M)
CARDS = ["E1", "E2", "E3", "E5", "E6", "E7", "E8", "E10", "E11", "E12"]
GRADES = {"A", "B"}
MAX_CARD_WORDS = 90  # Dan, iteration 2: words with a letter, field labels, figure and numbers left out
# Internal names a reader outside the project should never see (Dan, iteration 2 §3); the Appendix's
# "where things live" line is the one place for paths.
BANNED = re.compile(
    r"\bx(?:0|6|8)_\w*|\bx4[5-8]\w*|\b4[5-9]\.\d+\b|\bC[02]\b|\bP2-L0\b|\bjobs/|\bresults/|data\.csv|\bX0 read\b"
    r"|\bthe box\b|\bamendment\b|\bbatch\b",
    re.I,
)


def page_body(text: str) -> str:
    """The page without its source comments and without the Appendix."""
    return re.sub(r"<!--.*?-->", "", text.split("## Appendix A", 1)[0], flags=re.S)


def cards(text: str) -> dict[str, str]:
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


def test_ten_cards_in_order():
    assert [m.group(1) for m in CARD.finditer(PAGE.read_text())] == CARDS


def test_every_card_has_the_six_bullet_fields_in_order():
    for cid, body in cards(PAGE.read_text()).items():
        found = re.findall(r"^- \*\*(\w+)\.\*\*", body, re.M)
        dedup = [f for i, f in enumerate(found) if i == 0 or f != found[i - 1]]  # E10's two Result bullets
        assert dedup == list(FIELDS), (cid, found)
        assert found.count("Result") == (2 if cid == "E10" else 1), (cid, found)


# Dan's figure fixes, round 3 (28 Oct 21:10): E5 shows Fig. 6b as its second figure ("the same routes by depth");
# every other card keeps one
FIGURES_PER_CARD = {"E5": 2}


def test_one_figure_per_card():
    for cid, body in cards(PAGE.read_text()).items():
        assert len(re.findall(r"!\[[^\]]+\]\(([^)]+)\)", body)) == FIGURES_PER_CARD.get(cid, 1), cid


def test_cards_at_most_90_words():
    for cid, body in cards(re.sub(r"<!--.*?-->", "", PAGE.read_text(), flags=re.S)).items():
        body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)
        body = re.sub(r"\*\*(?:" + "|".join(FIELDS) + r")\.\*\*", "", body)
        n = len([w for w in body.split() if re.search(r"[A-Za-z]", w)])
        assert n <= MAX_CARD_WORDS, (cid, n)


def test_no_footers_and_no_internal_names():
    text = PAGE.read_text()
    assert "<sub>" not in text
    assert not (found := sorted(set(BANNED.findall(page_body(text))))), found


def test_claims_table_links_grades_and_hand_check():
    text = PAGE.read_text()
    rows = claims_rows(text)
    assert [r[0] for r in rows] == ["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "9a", "10", "11"]
    for r in rows:
        assert len(r) == 6, r
        assert re.sub(r"\*\*", "", r[3]).split(" ")[0] in GRADES, r
        assert r[5] in ("no", "yes"), r
