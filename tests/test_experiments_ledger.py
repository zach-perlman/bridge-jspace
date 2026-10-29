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

![a figure](../../figures/story/fig01_split.png)
*What is plotted.*

- **Rule, fixed in advance.** "r."
- **Result.** 0.53<!-- src: docs/handcheck_clean49.md | Main test gap :: 0.53 -->
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


def test_the_ledger_follows_the_readme_order():
    """Dan's restructure brief (29 Oct 08:55): In one minute, How to read, the README's Parts I-VI (and How we checked),
    Withdrawn, Run on one model only, then the Appendix."""
    heads = [h for h in L.LEDGER.read_text().splitlines() if h.startswith("## ")]
    assert heads == ["## In one minute", "## How to read",
                     "## Part I. The two readers: lookup and recall",
                     "## Part II. Identity: which item the lookup reads",
                     "## Part III. The address: where the item's locker sits",
                     "## Part IV. Where and when the link is made", "## Part V. Other datasets and operations",
                     "## Part VI. What did not hold", "## How we checked", "## Run on one model only (one line each)",
                     "## Withdrawn", "## Running or sealed",
                     '## Appendix A. Flagged for Dan <a id="flagged"></a>',
                     '## Appendix B. README changes waiting for Dan <a id="readme-changes"></a>',
                     '## Appendix C. Coverage table <a id="coverage"></a>',
                     '## Appendix D. Figure checks <a id="figure-checks"></a>']  # fmt: skip


def test_the_checker_catches_failures():
    assert not L.problems(CARD)
    assert L.problems(CARD.replace("docs/handcheck_clean49.md", "results/no_such_folder/verdict.md"))
    assert L.problems(CARD.replace(' <a id="a"></a>', ""))
    assert L.problems(CARD + CARD)  # a duplicate anchor
    assert L.problems(CARD.replace("- **Caveats.**\n", ""))
    assert L.problems(CARD + "See [b](#b).\n")
    assert L.problems(CARD.replace("0.53<!--", "0.54<!--"))  # the shown number is not the source's
    assert L.problems(CARD.replace(":: 0.53 -->", ":: 0.99 -->"))  # the source's number is not in the file
    assert L.problems(CARD.replace("![a figure](../../figures/story/fig01_split.png)\n", ""))  # no figure
    assert L.problems(CARD.replace("fig01_split", "no_such_figure"))  # the figure's file is missing
    assert L.problems(CARD.replace("*What is plotted.*\n", ""))  # no caption
    assert L.problems(CARD.replace("`in README` ", ""))  # no status tag
    assert L.problems(CARD.replace("`in README`", "`in the README`"))  # not one of the tags
    moved = CARD.replace("![a figure](../../figures/story/fig01_split.png)\n*What is plotted.*\n\n", "")
    moved = moved.replace("- **Result.**", "\n![a figure](../../figures/story/fig01_split.png)\n*What is plotted.*\n\n- **Result.**")
    assert L.problems(moved)  # the figure after the rule, not right after Method
    assert not L.problems(CARD + "See [the flags](#flagged).\n## Flags <a id=\"flagged\"></a>\n")  # a section anchor


def test_a_running_stub_needs_only_its_status():
    stub = '### Later (1.2, running) <a id="b"></a>\n\n- **Question.** q?\n- **Status.** s.\n- **Where used.** w.\n'
    assert not L.problems(stub)
