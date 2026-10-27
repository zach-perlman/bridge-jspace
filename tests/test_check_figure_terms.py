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


@pytest.mark.parametrize(
    "text",
    ["M − K +51", "the K final", "M-K", "PK +24.6", "TK", "P->P->M", "P→P→M", "RM − MM", "a stated answer",
     "Stated answers", "Remove from the change", "removing it from the change", "extra loss (x 100)", "× 100", "x100",
     "an in-context read", "J-part swap", "the J++ part", "entity code", "the order pointer", "45r", "x45r", "Q46.1",
     "GAP -> 45s", "0.30°", "X0 not confirmed", "paper10_rot", "s = 2", "s=4", "his finals"],
)  # fmt: skip
def test_the_joint_matcher_catches_each_retired_term(text):
    assert C.joint_retired([("example", text)]), text


@pytest.mark.parametrize(
    "text",
    ["recalled answer", "lookup answer", "Lookup answers", "the lens part", "remove everywhere", "remove from the patch",
     "whole patch", "swap the lens part", "order signal", "Qwen 9B", "Qwen 27B", "Qwen 122B", "Muse 30B",
     "Nemotron Lightning", "after the data", "Iris picked the frog.", "Which locker belongs to Iris's pick?",
     "Mozart was Austrian by birth.", "The composer who wrote The Magic Flute was of which nationality?",
     "answers lost (pp)", "switches lost beyond a random part (pp)", "about a real patch's size", "Kyoto", "Mozart's",
     "+13.8, below 20", "max 100", "0-100"],
)  # fmt: skip
def test_the_joint_matcher_passes_the_joint_vocabulary(text):
    assert not C.joint_retired([("example", text)]), C.joint_retired([("example", text)])


def test_root_readme_texts_drop_comments_code_spans_and_link_targets(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    readme.write_text("# Title\n<!-- src: docs/breadth/data.csv | ko.q9.mk; M − K -->\nRun `scripts/x0_details.py` here.\n"
                      "[gaps](docs/shared/gaps_45r.md) and ![The stated one](figures/shared/j1.png)\nThe recalled answer.\n")  # fmt: skip
    monkeypatch.setattr(C, "ROOT_README", readme)
    texts = C.root_readme_texts()
    assert [t for _, t in texts] == [
        "# Title",
        "Run  here.",
        "[gaps]() and ![The stated one]()",
        "The recalled answer.",
    ]
    assert [term for *_, term in C.joint_retired(texts)] == ["stated"]


def test_the_joint_figures_draw_no_retired_term():
    texts = C.joint_figure_texts()
    assert {where for where, _ in texts} == {
        "j0_setup",
        "j1_recall_needs_lens",
        "j2_swap",
        "j3_order_signal",
        "grid_front",
        "j5_muse_depth",
        "grid",
        "grid_dan",
    }
    assert not C.retired(texts) and not C.joint_retired(texts), C.retired(texts) + C.joint_retired(texts)
