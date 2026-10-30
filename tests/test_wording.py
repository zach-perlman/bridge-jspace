"""Reader-facing text does not say "loss" (Dan 30 Oct; a TA read it as training loss): accuracy drop for the band measure,
switches blocked for the one-layer measure."""

from __future__ import annotations

import pytest

from scripts import check_wording as W


def test_the_checker_flags_loss_words_but_not_fits_comments_or_markers():
    text = (
        "The recall loses 3 points.\n"
        "The lens fit minimises a training loss.\n"
        "Kept<!-- src: data.csv | recall extra loss --> and {{d|fig|9b|switches lost beyond random}} and `loss_k`.\n"
    )
    assert [h.split(":")[0] for h in W.loss_words(text)] == ["line 1"]


@pytest.mark.parametrize("path", W.FILES, ids=lambda p: str(p.relative_to(W.REPO)))
def test_reader_facing_files_do_not_say_loss(path):
    if not path.exists():
        pytest.skip("no such file")
    assert not (hits := W.loss_words(path.read_text(encoding="utf-8"))), hits
