"""The depth README's cards (Dan's restructure brief, 28 Oct 22:20): every card heading is a question; every card has
the eight bullet fields in order (Question, Why we asked, Data, Method, Rule fixed in advance, Result, Read, Caveats),
its Question bullet repeats the heading, its Read has two to four bullets and no number, and its figure comes between
the Rule and the Result with an italic caption (Dan, 29 Oct 12:50); a page figure belongs to exactly one card (a second figure in a card needs its own
sentence); the page's figures are the contact sheet's (readme_story_figures.README_NAMES); no internal id in the body
(scripts/check_figure_terms.py's README_IDS); and the claims table (rewritten last) keeps its twelve graded rows.

Dan's 90-word card cap (v6 iteration 2) is dropped: the eight-field cards replace it (Dan, 28 Oct 22:20)."""

import itertools
import re
from pathlib import Path

from scripts import check_figure_terms as C
from scripts import readme_story_figures as F

REPO = Path(__file__).resolve().parents[1]
PAGE = REPO / "docs" / "depth" / "README.md"
FIELDS = ("Question", "Why we asked", "Data", "Method", "Rule, fixed in advance", "Result", "Read", "Caveats")
GRADES = {"A", "B"}
# Dan 29 Oct 12:50 (docs_1250): Parts I-V hold cards; Part VI keeps one-line links to the ledger, no card
CONVERTED = ("Part I.", "Part II.", "Part III.", "Part IV.", "Part V.")
IMAGE = re.compile(r"^!\[[^\]]+\]\(([^)]+)\)", re.M)


def text() -> str:
    return re.sub(r"<!--.*?-->", "", PAGE.read_text(), flags=re.S)


def parts(page: str) -> dict[str, str]:
    """'## Part ...' heading -> its body (up to the next '## ')."""
    out = {}
    for m in re.finditer(r"^## (Part [^\n]+)\n(.*?)(?=^## |\Z)", page, re.M | re.S):
        out[m.group(1)] = m.group(2)
    return out


def cards(page: str) -> dict[str, str]:
    """Card heading -> its body, over the converted parts."""
    out = {}
    for head, body in parts(page).items():
        if not head.startswith(CONVERTED):
            continue
        for m in re.finditer(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", body, re.M | re.S):
            out[m.group(1).strip()] = m.group(2)
    return out


def fields(body: str) -> list[tuple[str, int]]:
    """(field label, line index) for each top-level '- **Label.**' bullet."""
    return [(m.group(1), i) for i, line in enumerate(body.splitlines()) if (m := re.match(r"^- \*\*(.+?)\.\*\*", line))]


def test_every_converted_part_has_cards():
    cs = cards(text())
    assert cs, "no card in the converted parts"
    for head, body in parts(text()).items():
        if head.startswith(CONVERTED):
            assert re.search(r"^### ", body, re.M), head


def test_card_headings_are_questions_and_part_headings_statements():
    for head in cards(text()):
        assert head.endswith("?"), head
    for head in parts(text()):
        assert not head.endswith("?"), head


def test_every_card_has_the_eight_fields_in_order():
    for head, body in cards(text()).items():
        assert [f for f, _ in fields(body)] == list(FIELDS), (head, fields(body))
        first = next(line for line in body.splitlines() if line.startswith("- **Question.**"))
        assert first.removeprefix("- **Question.**").strip() == head, head


def test_read_has_two_to_four_bullets_without_numbers():
    for head, body in cards(text()).items():
        lines = body.splitlines()
        idx = dict(fields(body))
        read = lines[idx["Read"] + 1 : idx["Caveats"]]
        bullets = [line for line in read if line.startswith("  - ")]
        assert 2 <= len(bullets) <= 4, (head, bullets)
        for b in bullets:  # no new numbers in Read: no digit beyond model sizes
            assert not re.search(r"\d", re.sub(r"\b\d+B\b", "", b)), (head, b)


def test_figure_after_the_method_with_a_caption():
    # Dan 29 Oct 12:50 (docs_1250): "Question / Why we asked / Data / Method / Rule / one figure after Method / Result";
    # the figure sits between the Rule and the Result
    for head, body in cards(text()).items():
        lines = body.splitlines()
        idx = dict(fields(body))
        imgs = [i for i, line in enumerate(lines) if IMAGE.match(line)]
        assert imgs, f"{head}: no figure"
        assert all(idx["Rule, fixed in advance"] < i < idx["Result"] for i in imgs), (
            f"{head}: a figure outside Rule-Result"
        )
        for i in imgs:
            cap = lines[i + 1] if i + 1 < len(lines) else ""
            assert re.fullmatch(r"\*[^*].*\*", cap.strip()), f"{head}: no italic caption under {lines[i]}"
        for a, b in itertools.pairwise(imgs):  # a second figure needs its own sentence
            between = [x for x in lines[a + 2 : b] if x.strip()]
            assert between, f"{head}: a second figure without its own sentence"


def test_converted_figures_belong_to_one_card_only():
    page = text()
    for head, body in cards(page).items():
        for target in IMAGE.findall(body):
            assert page.count(f"]({target})") == 1, (head, target)


def test_page_figures_are_the_contact_sheet():
    shown = {Path(t).stem for t in IMAGE.findall(text().split("## Appendix A")[0])}
    assert shown == set(F.README_NAMES), shown ^ set(F.README_NAMES)


def test_no_internal_ids_in_the_body():
    hits = C.readme_ids(C.readme_body_lines(PAGE.read_text()))
    assert not hits, hits


def test_no_bullet_starts_with_we():
    for line in text().splitlines():
        assert not re.match(r"^\s*- (?:\*\*[^*]*\*\*\s*)?We\b", line), line


def claims_rows(page: str) -> list[list[str]]:
    table = page.split("## Claims", 1)[1].split("\n## ", 1)[0]
    rows = [r for r in table.splitlines() if r.startswith("| ") and not r.startswith(("| #", "|---"))]
    return [[c.strip() for c in r.strip()[1:-1].split("|")] for r in rows]


def test_claims_table_grades_and_hand_check():
    # Dan 21:20: his twelve findings in his order (Fig. 11's rows, word for word); the restructure's new columns come
    # with the claims-table rewrite, the last step of Dan's 22:20 order of work
    rows = claims_rows(text())
    assert [r[0] for r in rows] == [str(k) for k in range(1, 13)]
    for r in rows:
        assert len(r) == 6, r
        assert re.sub(r"\*\*", "", r[3]).split(" ")[0] in GRADES, r
        assert r[5] in ("no", "yes"), r
