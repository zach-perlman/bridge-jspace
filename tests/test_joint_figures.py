"""scripts/joint_figures.py: the root README's five figures read at 880 px in the joint vocabulary, data/figures/shared/data.csv
is what they plot now, and three numbers per figure match their sources."""

from __future__ import annotations

import json

import pytest
import test_readme_build as RB
from matplotlib.text import Text

from bridge_jspace import plot_style as PS
from scripts import check_figure_terms as C
from scripts import joint_figures as J
from scripts import story_style as S


@pytest.fixture(scope="module")
def drawn():
    """Each figure drawn once (nothing saved) and the data rows they record."""
    J.ROWS.clear()
    plt = S.setup()
    figs = {name: draw(plt) for name, draw in J.FIGURES}
    rows = list(J.ROWS)
    yield figs, rows
    for fig in figs.values():
        plt.close(fig)


def value(rows, figure: str, model: str, quantity: str):
    (row,) = [r for r in rows if (r["figure"], r["model"], r["quantity"]) == (figure, model, quantity)]
    return row


def test_data_csv_is_what_the_figures_plot_now(drawn):
    _, rows = drawn
    assert J.DATA.read_text() == J.data_text(rows), "data/figures/shared/data.csv is stale: rerun scripts/joint_figures.py"
    assert all(r["source"] for r in rows)


@pytest.mark.parametrize("name", [n for n, _ in J.FIGURES])
def test_each_figure_reads_at_880px_in_the_joint_vocabulary(drawn, name):
    fig = drawn[0][name]
    assert fig.get_figwidth() == S.WIDTH
    assert PS.overlaps(fig) == []
    texts = [(name, t.get_text()) for t in fig.findobj(Text) if t.get_text().strip()]
    assert not RB.banned(texts) and not C.retired(texts) and not C.joint_retired(texts)


def breadth(model: str, key: str) -> float:
    return {(r["model"], r["key"]): float(r["value"]) for r in J.read_csv(J.BREADTH)}[(model, key)]


def sourced(rows, figure: str, model: str, source_end: str) -> dict:
    """The one row of a figure and model whose source ends with source_end (labels may be reworded; sources do not)."""
    (row,) = [r for r in rows if (r["figure"], r["model"]) == (figure, model) and r["source"].endswith(source_end)]
    return row


def test_j1_numbers_match_their_sources(drawn):
    _, rows = drawn
    assert sourced(rows, "j1", "Qwen 27B", "| ko.q27.lostM")["value"] == breadth("q27", "ko.q27.lostM") == 53.5
    assert sourced(rows, "j1", "Qwen 9B", "recall extra loss")["value"] == 50.0  # 0.50 in data/figures/depth/data.csv, in pp
    facts = json.loads(
        (J.REPO / "results/ablate_v2/jsuite2_score/muse30_jsuite_v2_test_chat_ko_cand2_v1.json").read_text()
    )["facts"]
    assert (
        sourced(rows, "j1", "Muse 30B", "unembed10/start=all loss M")["value"]
        == facts["unembed10/start=all"]["loss"]["M"]
    )


def test_j2_numbers_match_their_sources(drawn):
    _, rows = drawn
    assert sourced(rows, "j2", "Qwen 9B", "| swap.q9.swap")["value"] == breadth("q9", "swap.q9.swap")
    assert sourced(rows, "j2", "Qwen 27B", "| PK/swap_comp")["value"] == 24.6  # docs/shared/gaps.md row 3
    assert sourced(rows, "j2", "Qwen 27B", "| PK/swap")["value"] == 0.9


def test_j3_numbers_match_their_sources(drawn):
    _, rows = drawn
    lost = {(r["model"], r["quantity"]): r["value"] for r in rows if r["figure"] == "j3"}
    # whole patch 51.0% minus 8.3% without the order signal (fig05), recomputed per scene from outcomes.jsonl
    assert lost[("Qwen 9B", "answers by position lost when the order signal is removed from the change (pp)")] == 42.7
    assert lost[("Muse 30B", "answers by position lost when a random part is removed from the change (pp)")] == -0.3
    assert sourced(rows, "j3", "Qwen 9B", "dose (s / mean s*), s = 2")["value"] == 1.06


def test_grid_front_cells_come_from_the_grid(drawn):
    _, rows = drawn
    assert value(rows, "grid_front", "Qwen 27B", "finding 1 (depth)")["value"] == "~"
    assert value(rows, "grid_front", "Muse 30B", "finding 4 (both)")["value"] == "x a"
    assert value(rows, "grid_front", "Nemotron Lightning", "finding 3 (depth)")["value"] == "-"


def test_j5_numbers_match_the_muse_depth_score(drawn):
    _, rows = drawn
    sc = json.loads(J.x45r_score().read_text())
    assert (
        sourced(rows, "j5", "Muse 30B", "| his_L23_29.paper10.mk")["value"] == sc["his_L23_29"]["paper10"]["mk"] == 6.7
    )
    late = sourced(rows, "j5", "Muse 30B", "| descriptive.L36_42_record.unembed10.mk")["value"]
    assert late == sc["descriptive"]["L36_42_record"]["unembed10"]["mk"] == 34.6
    assert sourced(rows, "j5", "Muse 30B", "| contrast_muse")["value"] == 85  # 0.85 [0.68, 0.98] of the switches, in %
    assert sourced(rows, "j5", "Muse 30B", "paper10_pcasize.mk")["value"] == 4.6  # the largest other control


def test_j8_numbers_match_their_sources(drawn):
    _, rows = drawn
    by = {(r["model"], r["quantity"]): r for r in rows if r["figure"] == "j8"}
    q = "lookup answers by route, whole change: {} (%)"
    assert by[("Qwen 9B", q.format("identity"))]["value"] == 48.0  # fig05: 0.48
    assert by[("Muse 30B", q.format("position"))]["value"] == 54.3  # fig05: 0.5433
    assert all(
        by[(m, q.format("the number"))]["value"] == 0.0 for m in ("Qwen 9B", "Qwen 27B", "Muse 30B", "Qwen 122B")
    )
    for m in ("Qwen 9B", "Qwen 27B", "Muse 30B", "Qwen 122B"):  # each bar sums to 100%
        total = sum(by[(m, q.format(k))]["value"] for k in ("identity", "position", "the original answer or another"))
        assert abs(total - 100) < 0.2, (m, total)


def test_j9_numbers_match_their_sources(drawn):
    _, rows = drawn
    by = {(r["model"], r["quantity"]): r for r in rows if r["figure"] == "j9"}
    carried = "lookup switches carried at the main test's layer: {} (%)"
    assert by[("Qwen 9B", carried.format("the change at the locker sentences"))]["value"] == 69.7  # fig03b arm c 0.6965
    assert by[("Qwen 27B", carried.format("the change at the bridge word"))]["value"] == 1.4  # fig03b arm a 0.0139
    lost = "switches lost at the item's earlier mention, {} (%)"
    assert by[("Muse 30B", lost.format("recalled: lens part taken out there"))]["value"] == 50.9  # fig03c a2 0.5091
    assert by[("Qwen 27B", lost.format("recalled: a random part there"))]["value"] == 8.0  # fig03c a3 0.08


def test_example_texts_are_quoted_from_their_sources():
    src = (J.REPO / "scripts" / "readme_story_figures.py").read_text()
    # Fig. 0's running example (readme_story_figures.f00_setup): its lockers, the asked pick and both questions
    assert all(s in src for s in (*J.DAN_SCENE[:2], *(q for q, _, _ in J.DAN_QUESTIONS)))
    who, item = J.F.SETUP_PICKS["original"][J.F.SETUP_ASKED]
    assert J.DAN_SCENE[2] == f"{who} picked {item}." and f'("{who}", "{item}")' in src
    assert [(q, a) for q, a, _ in J.DAN_QUESTIONS] == [(q, a) for _, _, q, a, _, _ in J.F.SETUP_QUESTIONS]
    assert J.zach_texts()["question"] == "The composer who wrote The Magic Flute was of which nationality?"


@pytest.mark.parametrize(
    ("d", "b", "s", "want"),
    [("ok", "ok", "ok", ("ok", "")), ("~", "ok", "ok", ("~", "")), ("ok", "ok", "x", ("x", "")), ("ok", "x", "ok", ("x", "")),
     ("-", "ok", "ok", ("-", "")), ("ok", "ok", "~", ("~", ""))],
)  # fmt: skip
def test_agree_rule(d, b, s, want):
    cell = lambda c: {"cell": c, "flag": ""}  # noqa: E731
    assert J.agree(cell(d), cell(b), cell(s)) == want
