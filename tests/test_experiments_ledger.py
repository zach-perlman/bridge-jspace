"""docs/depth/EXPERIMENTS.md (Dan, 29 Oct ~01:10; cards since 01:15; in the README's order since 08:55): every cited
path exists, every entry has a unique anchor, its status tag and the README Part I card fields in order with the figure
right after Method (a running stub: Question, Status, Where used), every internal link resolves, every number's source
comment resolves on one line of its file, the coverage table is the matrix; the checker catches each failure."""

from scripts import check_ledger as L

REQUIRED = ("t49-2", "t49-5", "t51-1", "t51-2", "t51-3", "t51-4", "t51-5", "t51-7", "t51-10", "t51-11", "t51-12", "z1",
            "z2", "z3", "lightning-layer", "lightning-conflict", "b52-a", "b52-b", "routes", "six", "swap",
            "order", "t47-0", "t47-8", "d1", "t47-1",
            "t49-7", "x0b", "t49-1", "t47-14", "t47-16", "t47-4",
            "t48-3", "t47-6", "t47-11", "t47-5", "x45d", "t47-13", "t47-7c",
            "t48-1", "t49-3", "t48-4", "t48-2", "probe", "t45q",
            "t45p", "x5", "t47-3", "t47-10", "t48-5")  # fmt: skip
CARD = """### A test (1.1, opened x) <a id="a"></a>

`in README` `below gate: Lightning` *Used in: README Part I card.*

- **Question.** q?
- **Why we asked.** w.
- **Data.** d.
- **Method.** m.

![a figure](../../figures/depth/fig01_split.png)
*What is plotted.*

- **Rule, fixed in advance.** "r."
- **Result.** 0.53<!-- src: docs/depth/notes/handcheck_clean49.md | Main test gap :: 0.53 -->
- **Read.**
  - r.
- **Caveats.**
  - c.
"""


def test_the_ledger_is_well_formed():
    assert not (bad := L.problems(L.LEDGER.read_text())), bad


def test_the_ledger_covers_dans_list():
    text = L.LEDGER.read_text()
    for anchor in REQUIRED:
        assert f'<a id="{anchor}"></a>' in text, anchor


def test_the_coverage_table_is_the_matrix():
    assert not (bad := L.coverage_problems(L.LEDGER.read_text())), bad
    assert L.coverage_problems("no table here")


def test_the_coverage_table_is_symbols_with_footnotes():
    """Dan's restructure brief (29 Oct 08:55): every matrix row once, in the README's order; each cell one symbol of the
    legend (✓ ◐ ○ – ✗) and at most one footnote number; every number listed under the table; no status words in a
    cell."""
    import json
    import re

    from scripts import ledger_coverage as LC

    out = LC.table()
    rows = [line for line in out.splitlines() if line.startswith("| ") and not line.startswith("| **")][1:]  # no header
    m = json.loads(LC.MATRIX.read_text())
    assert len(rows) == len(m["rows"])
    notes = {int(n) for n in re.findall(r"(?m)^(\d+)\. ", out)}
    for row in rows:
        for c in row.strip("| ").split(" | ")[1:]:
            assert re.fullmatch(r"[✓◐○–✗](?: <sup>(\d+)</sup>)?", c), c
            for n in re.findall(r"<sup>(\d+)</sup>", c):
                assert int(n) in notes
    assert notes == set(range(1, len(notes) + 1))
    parts = [line for line in out.splitlines() if line.startswith("| **Part")]
    assert [p.split(".")[0] for p in parts] == [f"| **Part {r}" for r in ("I", "II", "III", "IV", "V", "VI")]


def test_the_overview_heatmap_follows_the_cards():
    """The heatmap's rows (scripts/ledger_coverage.py's HEATMAP): every card in Parts I-VI, in the ledger's order, its
    Part as in the ledger; nothing else but the cards it leaves out on purpose; every cell a known verdict code. The
    figure sits under "In one minute", before "How to read"."""
    import re

    from scripts import ledger_coverage as LC

    text = L.LEDGER.read_text()
    parts = re.split(r"(?m)^## ", text)
    in_part = {}
    for p in parts:
        m = re.match(r"Part (I|II|III|IV|V|VI)\. ", p)
        for a in re.findall(r'^### .*<a id="([a-z0-9-]+)"></a>', p, re.M):
            in_part[a] = m.group(1) if m else None
    cards = [a for a in in_part if in_part[a]]
    rows = LC.heatmap_cells()
    shown = list(dict.fromkeys(a for _, a, _, _ in rows))
    assert shown == [a for a in cards if a not in LC.HEATMAP_LEFT_OUT]
    assert all(in_part[a] == part for part, a, _, _ in rows)
    assert all(a in in_part for a in LC.HEATMAP_LEFT_OUT)
    top = text.split("## How to read")[0]
    assert "](../../figures/depth/ledger/ledger_coverage_map.png)" in top.split("## In one minute")[1]


def test_the_ledger_follows_the_readme_order():
    """Dan's restructure brief (29 Oct 08:55): In one minute, How to read, the README's Parts I-VI (and How we checked),
    Withdrawn, Run on one model only, then the Appendix."""
    heads = [h for h in L.LEDGER.read_text().splitlines() if h.startswith("## ")]
    assert heads == ["## In one minute", "## How to read",
                     "## Part I. The two readers: lookup and recall",
                     "## Part II. Identity: which item the lookup reads",
                     "## Part III. The address: where the item's locker sits",
                     "## Part IV. Where and when the link is made", "## Part V. Other datasets and operations",
                     "## Part VI. What did not hold", "## Also failed (one line each) <a id=\"also-failed\"></a>", "## How we checked",
                     "## Run on one model only (one line each)",
                     "## Withdrawn",
                     '## The 122B coverage, night 29-30 Oct (coverage, not hand-checked) <a id="cov-122b-night"></a>',
                     "## Running or sealed",
                     '## Appendix A. Flagged for Dan <a id="flagged"></a>',
                     '## Appendix B. README changes waiting for Dan <a id="readme-changes"></a>',
                     '## Appendix C. Coverage table <a id="coverage"></a>',
                     '## Appendix D. Figure checks <a id="figure-checks"></a>']  # fmt: skip


def test_the_checker_catches_failures():
    assert not L.problems(CARD)
    assert L.problems(CARD.replace("docs/depth/notes/handcheck_clean49.md", "results/no_such_folder/verdict.md"))
    assert L.problems(CARD.replace(' <a id="a"></a>', ""))
    assert L.problems(CARD + CARD)  # a duplicate anchor
    assert L.problems(CARD.replace("- **Caveats.**\n", ""))
    assert L.problems(CARD + "See [b](#b).\n")
    assert L.problems(CARD.replace("0.53<!--", "0.54<!--"))  # the shown number is not the source's
    assert L.problems(CARD.replace(":: 0.53 -->", ":: 0.99 -->"))  # the source's number is not in the file
    assert L.problems(CARD.replace("![a figure](../../figures/depth/fig01_split.png)\n", ""))  # no figure
    assert L.problems(CARD.replace("fig01_split", "no_such_figure"))  # the figure's file is missing
    assert L.problems(CARD.replace("*What is plotted.*\n", ""))  # no caption
    assert L.problems(CARD.replace("`in README` ", ""))  # no status tag
    assert L.problems(CARD.replace("`in README`", "`in the README`"))  # not one of the tags
    moved = CARD.replace("![a figure](../../figures/depth/fig01_split.png)\n*What is plotted.*\n\n", "")
    moved = moved.replace("- **Result.**", "\n![a figure](../../figures/depth/fig01_split.png)\n*What is plotted.*\n\n- **Result.**")
    assert L.problems(moved)  # the figure after the rule, not right after Method
    assert not L.problems(CARD + "See [the flags](#flagged).\n## Flags <a id=\"flagged\"></a>\n")  # a section anchor


def test_a_running_stub_needs_only_its_status():
    stub = '### Later (1.2, running) <a id="b"></a>\n\n- **Question.** q?\n- **Status.** s.\n- **Where used.** w.\n'
    assert not L.problems(stub)
    # batch 53's stubs quote their rule fixed before the run; out of order or a card field in a stub fails
    ruled = stub.replace("- **Status.**", '- **Rule, fixed in advance.** "r."\n- **Status.**')
    assert not L.problems(ruled)
    assert L.problems(stub.replace("- **Status.**", '- **Status.** s.\n- **Rule, fixed in advance.** "r."\n- **X.**'))
    assert L.problems(stub.replace("- **Where used.** w.\n", '- **Where used.** w.\n- **Rule, fixed in advance.** r.\n'))


SLOT_CARD = """### T (1.3, opened x) <a id="t"></a>

`ledger only`

- **Question.** q?
- **Why we asked.** w.
- **Data.** d.
- **Method.** m.

![f](../../figures/depth/ledger/ledger_x.png)
*c.*

- **Rule, fixed in advance.** "r."
- **Result.**

  | | 9B | 27B | Muse | Lightning |
  |---|---|---|---|---|
  | a | 0.10 [0.00, 0.20] | 0.30 | not designed | ○ 0.40 |
  | the rule | **no** | **no** | | not tested (gate 0.751 < 0.80); below gate |

- **Read.**
  - r.
- **Caveats.**
  - c.
"""


def test_the_figure_shows_every_model_of_its_table():
    """Dan's figures brief (29 Oct 10:00): a number in a model's column needs that model's data in the card's ledger
    figure; a column without a number needs its grey slot; a verdict-folder figure on a card is flagged; the README's
    shared figures are left to its build."""
    head, body = L.entries(SLOT_CARD)[0]
    good = {"ledger_x": {"9B": "data", "27B": "data", "Muse": "grey: not designed", "Lightning": "below gate"}}
    assert not L.slot_problems(head, body, good)
    assert L.slot_problems(head, body, {"ledger_x": {**good["ledger_x"], "Lightning": "grey: x"}})  # data shown grey
    assert L.slot_problems(head, body, {"ledger_x": {k: v for k, v in good["ledger_x"].items() if k != "Muse"}})
    assert L.slot_problems(head, body, {})  # no slot record for the figure
    borrowed = SLOT_CARD.replace("../../figures/depth/ledger/ledger_x.png", "../../results/x/verdict.png")
    assert L.slot_problems(*L.entries(borrowed)[0], good)
    readme = SLOT_CARD.replace("../../figures/depth/ledger/ledger_x.png", "../../figures/depth/fig01_split.png")
    assert not L.slot_problems(*L.entries(readme)[0], {})


def test_the_122b_is_checked_like_the_other_models():
    """Dan 12:50: five slots in every per-model figure; a not-run 122B column needs the 122B's grey slot, a 122B number
    its data."""
    good = {"ledger_x": {"9B": "data", "27B": "data", "Muse": "grey: not designed", "Lightning": "below gate"}}
    five = (SLOT_CARD.replace("| Lightning |\n  |---|---|---|---|---|", "| Lightning | 122B |\n  |---|---|---|---|---|---|")
            .replace("| ○ 0.40 |", "| ○ 0.40 | not run |").replace("below gate |\n", "below gate | |\n"))  # fmt: skip
    head, body = L.entries(five)[0]
    assert L.table_columns(body)["122B"] == "none"
    assert L.slot_problems(head, body, good)  # no 122B slot
    assert not L.slot_problems(head, body, {"ledger_x": {**good["ledger_x"], "122B": "grey: not run"}})
    with_number = five.replace("| ○ 0.40 | not run |", "| ○ 0.40 | 0.50 [0.40, 0.60] |")
    head, body = L.entries(with_number)[0]
    assert L.slot_problems(head, body, {"ledger_x": {**good["ledger_x"], "122B": "grey: not run"}})
    assert not L.slot_problems(head, body, {"ledger_x": {**good["ledger_x"], "122B": "data"}})
