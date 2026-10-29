"""docs/depth/EXPERIMENTS.md (Dan, 29 Oct ~01:10): every cited path exists, every entry has a unique anchor and the
five fields in order, every internal link resolves; the checker catches each failure."""

from scripts import check_ledger as L

REQUIRED = ("t49-2", "t49-5", "t51-1", "t51-2", "t51-3", "t51-4", "t51-5", "t51-7", "t51-10", "t51-11", "t51-12", "z1",
            "z2", "z3", "lightning-layer")  # fmt: skip


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
                     "## Ledger only (opened, not in README)", "## Withdrawn", "## Running or sealed"]  # fmt: skip


def test_the_checker_catches_failures(tmp_path):
    good = ("### A test (1.1, opened x) <a id=\"a\"></a>\n\n- Question: q?\n- Verdict (rule): v.\n- Key numbers, from "
            "`docs/depth/EXPERIMENTS.md`: 1.\n- Where used: ledger only.\n- Caveats: none.\n")  # fmt: skip
    assert not L.problems(good)
    assert L.problems(good.replace("docs/depth/EXPERIMENTS.md", "results/no_such_folder/verdict.md"))
    assert L.problems(good.replace(' <a id="a"></a>', ""))
    assert L.problems(good + good)  # a duplicate anchor
    assert L.problems(good.replace("- Caveats: none.\n", ""))
    assert L.problems(good + "See [b](#b).\n")
