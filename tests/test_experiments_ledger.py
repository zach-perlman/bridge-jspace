"""docs/depth/EXPERIMENTS.md (Dan, 29 Oct ~01:10; cards since 01:15): every cited path exists, every entry has a unique
anchor and the README Part I card fields in order (a running stub: Question, Status, Where used), every internal link
resolves, every number's source comment resolves on one line of its file, the coverage table is the matrix; the checker
catches each failure."""

from scripts import check_ledger as L

REQUIRED = ("t49-2", "t49-5", "t51-1", "t51-2", "t51-3", "t51-4", "t51-5", "t51-7", "t51-10", "t51-11", "t51-12", "z1",
            "z2", "z3", "lightning-layer", "lightning-conflict", "b52-a", "b52-b", "routes", "six", "swap",
            "order", "t47-0", "t47-8", "d1", "t47-1",
            "t49-7")  # fmt: skip
CARD = """### A test (1.1, opened x) <a id="a"></a>

- **Question.** q?
- **Why we asked.** w.
- **Data.** d.
- **Method.** m.
- **Rule, fixed in advance.** "r."

![a figure](../../figures/story/fig01_split.png)
*What is plotted.*

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


def test_the_ledger_sections_by_status():
    heads = [h for h in L.LEDGER.read_text().splitlines() if h.startswith("## ")]
    assert heads == ["## Flagged for Dan", "## README changes waiting for Dan", "## Coverage",
                     "## Changes a README claim (README must be updated)", "## Supports a README claim",
                     "## Ledger only (opened, not in README)", "## Withdrawn", "## Running or sealed",
                     "## Figure checks"]  # fmt: skip


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


def test_a_running_stub_needs_only_its_status():
    stub = '### Later (1.2, running) <a id="b"></a>\n\n- **Question.** q?\n- **Status.** s.\n- **Where used.** w.\n'
    assert not L.problems(stub)
