"""scripts/readme_lint.py: the readability measures count what a reader sees outside the folds."""

from __future__ import annotations

from scripts import readme_lint as R


def measure(tmp_path, text: str) -> dict:
    p = tmp_path / "README.md"
    p.write_text(text, encoding="utf-8")
    return R.measure(p)


def test_a_ledger_label_counts_in_prose_but_not_as_link_text(tmp_path):
    assert measure(tmp_path, "H1 held on the 27B.\n")["labels"] == 1
    assert measure(tmp_path, "Held ([ledger: H1](docs/plans/hypotheses.md#h1)).\n")["labels"] == 0


def test_folds_comments_and_tables_stay_out_of_the_outside_counts(tmp_path):
    m = measure(tmp_path, "One: two.<!-- src: a | b: c -->\n\n<details>\n\nC2 held: yes.\n\n</details>\n\n| a: | b |\n")
    assert m["labels"] == 0
    assert m["colons_outside"] == 1


def test_a_hard_wrapped_caption_counts_in_full(tmp_path):
    text = ("![alt](fig.png)\n\n*One two three four\nfive six seven\neight nine ten.*\n\nNot the caption.\n\n"
            "![alt](b.png)\n*Eleven twelve.*\n![alt](c.png)\n\n- a list, not a caption*\n")  # fmt: skip
    assert R.captions(text) == [10, 2]


def test_a_track_report_gets_the_larger_word_budget(tmp_path):
    assert R.role(R.REPO / "README.md") == "root"
    assert R.role(R.REPO / "docs" / "track" / "README.md") == "track"
    assert R.ROLE_TARGETS["root"]["words_outside"] == 2000
    assert R.ROLE_TARGETS["track"]["words_outside"] == 2500
    p = tmp_path / "README.md"
    p.write_text("One two three four five six seven eight nine ten. " * 220, encoding="utf-8")  # 2,200 words
    rel = str(p)  # absolute: REPO / p keeps it as is
    assert R.main([rel]) == 0  # not the repo root's README: the track budget
    assert R.main(["--role", "root", rel]) == 1


def test_a_per_model_slash_list_is_counted(tmp_path):
    assert measure(tmp_path, "Recall drops 0.50 / 0.74 / 0.75 ○ beyond random.\n")["slash_outside"] == 1
    assert measure(tmp_path, "Recall and lookup answer from memory / from the prompt.\n")["slash_outside"] == 0
