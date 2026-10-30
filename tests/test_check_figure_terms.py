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
    readme.write_text("![A claim](figures/depth/fig01.png)\n*Fig. 1.* the first-mentioned item\n<!-- ablation -->\n"
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
        "j4_depth_map",
        "j8_routes",
        "j9_link",
        "grid",
        "grid_dan",
    }
    assert not C.retired(texts) and not C.joint_retired(texts), C.retired(texts) + C.joint_retired(texts)


def _v6_layout(**over) -> dict[str, dict]:
    base = {"title": "The lookup follows identity or position, never the value", "subtitle": "One line.", "panels": 2}
    return {name: {**base, **over} for name in C.V6_FIGS}


def test_v6_style_passes_a_clean_figure():
    assert not C.v6_style(_v6_layout(), [(C.V6_FIGS[0], "without the address"), (C.V6_FIGS[0], "the swap")])


@pytest.mark.parametrize(
    ("over", "rule"),
    [({"title": "The split holds on the 9B"}, "digit in the title"), ({"title": "Two\nlines"}, "title over one line"),
     ({"subtitle": "First\nsecond"}, "subtitle over one line"), ({"panels": 3}, "more than two panels"),
     ({"title": ""}, "no title")],
)  # fmt: skip
def test_v6_style_catches_each_break(over, rule):
    assert rule in {r for *_, r in C.v6_style(_v6_layout(**over), [])}


def test_v6_style_catches_retired_words_and_missing_figures():
    texts = [(C.V6_FIGS[0], "without the pointer"), (C.V6_FIGS[0], "a write at the bridge"), ("fig99", "pointer")]
    assert [r for *_, r in C.v6_style(_v6_layout(), texts)] == ["pointer", "write"]
    assert [r for *_, r in C.v6_style({}, [])] == ["not drawn"] * len(C.V6_FIGS)


@pytest.mark.parametrize(
    ("text", "rule"),
    [("answers kept without it", "pronoun for the part"), ("only it", "pronoun for the part"),
     ("With it, position answers come back", "pronoun for the part"), ("the J++ part beside the address", "beside"),
     ("lens reading", "reading"), ("Readings", "reading"), ("random (band: 95%)", "(band: 95%)"),
     ("random or layout control", "random or layout control"), ("3 below random", "below random"),
     ("lookups sent to the target locker", "lookups sent to the target locker"), ("47.10's report", "test number"),
     ("48.2 B", "test number"), ("x0_parts", "run name"), ("qwen35_9b_x6_routes", "run name"), ("x8_write", "run name"),
     ("x45q sweep", "run name"), ("x47_atoms", "run name"), ("x48_enrich", "run name"), ("C0 holds", "C0 / C2"),
     ("C2 control", "C0 / C2"),
     # Dan's Fig. 5b / 5d brief (28 Oct ~20:30): "identity" never bare on a figure
     ("identity", "bare identity"), ("The lookup follows identity or position", "bare identity"),
     ("Identity early, position late", "bare identity"), ("the item's name (identity)", "bare identity"),
     ("27B: identity code", "bare identity"), ("identity\n→ 3", "bare identity")],
)  # fmt: skip
def test_v6_style_catches_iteration_two_strings(text, rule):
    assert rule in {r for *_, r in C.v6_style(_v6_layout(), [(C.V6_FIGS[0], text)])}


@pytest.mark.parametrize(
    "text",
    ["without the address", "only the address", "with the J++ part", "answers kept (share)", "the original answer",
     "a random part (same size)", "lost beyond random: 3 pp", "followed if above", "0.45", "45 pp", "lens directions 1–25",
     "Qwen3.6-27B", "Muse Glimmer 30B", "value: 0.00 in every row", "n = 758, 758, 657", "the bridge word", "it",
     "lookups answering the swapped-in locker", "dose, in units of a real change", "C10", "box", "identity route",
     "Identity route: the answer names the item's own locker", "identity answers lost", "an identity change",
     "identity-route answers", "the identity\nroute", "position route"],
)  # fmt: skip
def test_v6_style_passes_iteration_two_vocabulary(text):
    assert not C.v6_style(_v6_layout(), [(C.V6_FIGS[0], text)]), C.v6_style(_v6_layout(), [(C.V6_FIGS[0], text)])


def test_v6_style_bans_the_rule_in_the_subtitle_only():
    assert "rule:" in {r for *_, r in C.v6_style(_v6_layout(subtitle="Rule: kept above 0.8"), [])}
    assert "rule:" in {r for *_, r in C.v6_style(_v6_layout(subtitle="the swap; rule: kept above 0.8"), [])}
    assert not C.v6_style(_v6_layout(), [(C.V6_FIGS[0], "rule: kept above 0.8")])


def test_v6_titles_take_number_words_not_digits():
    assert not C.v6_style(_v6_layout(title="Ten claims on three models: what held, in part, or failed"), [])
    assert "digit in the title" in {r for *_, r in C.v6_style(_v6_layout(title="Twelve claims on 3 models"), [])}


def test_every_readme_figure_is_held_to_the_v6_rules():
    from scripts import readme_story_figures as F

    assert set(F.README_NAMES) <= set(C.V6_FIGS), set(F.README_NAMES) - set(C.V6_FIGS)


def test_v6_style_allows_three_panels_only_where_listed():
    lay = _v6_layout()
    lay["fig07_writes"]["panels"] = 3
    assert not C.v6_style(lay, [])
    lay["fig07_writes"]["panels"] = 4
    assert [r for *_, r in C.v6_style(lay, [])] == ["more than 3 panels"]


def test_a_marked_inset_is_not_a_panel():
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib.figure import Figure

    from scripts import story_style as S

    fig = Figure()
    fig.add_axes((0.1, 0.1, 0.8, 0.8))
    S.inset(fig, (0.6, 0.6, 0.2, 0.2))
    assert len([a for a in fig.axes if not getattr(a, S.INSET, False)]) == 1


# Dan's figures brief (28 Oct ~18:30): no cell status inside a frame; the mark system's hues only


@pytest.mark.parametrize("text", ["cannot report (gate)", "27B: cannot report"])
def test_frame_style_catches_a_status_inside_a_frame(text):
    hits = C.frame_style({"fig01d_ladder": {"in_frame": [text]}}, ["fig01d_ladder"])
    assert [r for *_, r in hits] and all(r.endswith("inside a frame") for *_, r in hits), hits


# Dan's figures brief (29 Oct 10:00): a model without a result keeps its slot with a short grey label
@pytest.mark.parametrize("text", ["not run", "not tested: gate 0.751", "Lightning: not tested (gate)"])
def test_frame_style_allows_a_grey_model_slot(text):
    assert not C.frame_style({"fig01d_ladder": {"in_frame": [text]}}, ["fig01d_ladder"])


def test_frame_style_leaves_other_words_and_other_pages_alone():
    assert not C.frame_style({"fig01d_ladder": {"in_frame": ["too few switches (10 of 60)", "n = 417"]}},
                             ["fig01d_ladder"])  # fmt: skip
    assert not C.frame_style({"s01_split_all_scene_sets": {"in_frame": ["not run"]}}, ["fig01d_ladder"])


def test_colour_key_treats_greys_as_no_hue():
    from scripts import story_style as S

    assert C.colour_key("#3a3a3a") == "" and C.colour_key("white") == "" and C.colour_key((0, 0, 0, 0.5)) == ""
    assert C.colour_key(S.MARK_COL["lookup"]) == S.MARK_COL["lookup"].lower()


# Dan's restructure brief (28 Oct 22:20) §6: no internal ids in the README body


@pytest.mark.parametrize(
    "text",
    ["test 47.5", "49.2's ladder", "51.11 sealed", "Z1 on his passages", "C0 holds", "P2-L0 scenes", "x0_necessity",
     "x45p verdict", "rung 6", "Rungs 1-4", "batch 47", "Amendment 2"],
)  # fmt: skip
def test_the_readme_id_lint_catches_each_internal_id(text):
    assert C.readme_ids([("example", text)]), text


@pytest.mark.parametrize(
    "text",
    ["0.47 [0.41, 0.57]", "47.5%", "the ladder's fifth step", "Zach's operation", "the routes scenes", "9B / 27B / Muse",
     "L to L+3", "the change at L", "200 random vectors", "C10"],
)  # fmt: skip
def test_the_readme_id_lint_passes_page_words(text):
    assert not C.readme_ids([("example", text)]), C.readme_ids([("example", text)])


def test_readme_body_lines_skip_comments_link_targets_and_the_where_line():
    page = "a <!-- src: x | 47.5: key -->\n[fig](results/x0_necessity/a.png)\nwhere things live: results/x47_zero\n"
    assert [t for _, t in C.readme_body_lines(page)] == ["a ", "[fig]()"]


def test_figure_hues_finds_a_stray_colour_and_frame_style_flags_it():
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib.figure import Figure

    from scripts import story_style as S

    fig = Figure()
    ax = fig.add_subplot()
    ax.plot([0, 1], [0, 1], color=S.MARK_COL["recall"])
    ax.bar([0], [1], color=S.MARK_COL["null"], alpha=0.5)
    ax.plot([0.5], [0.5], "X", color=S.MARK_COL["lookup"])
    assert C.figure_hues(fig) == {S.MARK_COL["lookup"].lower()}
    ax.plot([0.2], [0.2], "o", color="#2ca02c")
    hues = C.figure_hues(fig)
    assert "#2ca02c" in hues
    hits = C.frame_style({C.MARK_FIGS[0]: {"hues": hues}}, [])
    assert [(t, r) for _, t, r in hits] == [("#2ca02c", "hue outside the mark system")]
