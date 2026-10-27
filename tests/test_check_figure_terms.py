"""check_figure_terms: the retired-term matcher and the caption reader."""

from __future__ import annotations

import pytest

from scripts import check_figure_terms as C


@pytest.mark.parametrize(
    "text",
    ["Our pointer separates the first-mentioned item", "first mentioned item", "part removed", "parts removed",
     "Ablation of J++", "ablated", "Q45.9 scored", "Q45", "run qwen35_9b_x6_routes_x45e_dom",
     "results x45e-20261026T224602Z", "x0_kmatch_27b"],
)  # fmt: skip
def test_the_matcher_catches_each_retired_term(text):
    assert C.retired([("example", text)]), text


@pytest.mark.parametrize(
    "text",
    ["The pointer marks the first locker in a clean layout", "without the J++ part", "removed together",
     "the earlier mention", "Q34", "45e", "routes test (another item moved)", "J++ part + pointer", "9B / 27B / Muse",
     "code shift (positions), β 0.15", "too few switches (10 of 60)", "° gate lowered to 0.75 after the data"],
)  # fmt: skip
def test_the_matcher_passes_figure_words(text):
    assert not C.retired([("example", text)]), C.retired([("example", text)])


def test_caption_texts_read_alt_texts_fig_lines_and_the_draft(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    readme.write_text("![A claim](figures/story/fig01.png)\n*Fig. 1.* the first-mentioned item\n<!-- ablation -->\n"
                      "Body text with Q45.9 is not a caption.\n")  # fmt: skip
    draft = tmp_path / "captions.md"
    draft.write_text("- canonical Fig. 2: run x0_kmatch_27b\n- note: ablation here is not canonical\n")
    monkeypatch.setattr(C, "CAPTION_FILES", (readme,))
    monkeypatch.setattr(C, "CAPTIONS_DRAFT", draft)
    texts = C.caption_texts()
    assert [t for _, t in texts] == ["A claim", "*Fig. 1.* the first-mentioned item", "run x0_kmatch_27b"]
    assert {term for _, _, term in C.retired(texts)} == {"first-mentioned", "run id"}


def test_the_repo_captions_have_no_retired_term():
    assert not C.retired(C.caption_texts()), C.retired(C.caption_texts())
