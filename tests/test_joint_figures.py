"""scripts/joint_figures.py: the root README's five figures read at 880 px in the joint vocabulary, figures/shared/data.csv
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
    assert J.DATA.read_text() == J.data_text(rows), "figures/shared/data.csv is stale: rerun scripts/joint_figures.py"
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


def test_j1_numbers_match_their_sources(drawn):
    _, rows = drawn
    assert (
        value(rows, "j1", "Qwen 27B", "remove everywhere: recalled answers lost (points)")["value"]
        == breadth("q27", "ko.q27.lostM")
        == 53.5
    )
    assert value(rows, "j1", "Qwen 9B", "remove from the change: recalled answers' extra loss (x 100)")["value"] == 50.0
    muse = [
        r
        for r in rows
        if r["figure"] == "j1" and r["model"] == "Muse 30B" and "largest control (logit lens)" in r["quantity"]
    ]
    facts = json.loads(
        (J.REPO / "results/ablate_v2/jsuite2_score/muse30_jsuite_v2_test_chat_ko_cand2_v1.json").read_text()
    )["facts"]
    assert [r["value"] for r in muse] == [facts["unembed10/start=all"]["loss"]["M"]]


def test_j2_numbers_match_their_sources(drawn):
    _, rows = drawn
    q = "{}: {} answer moves (points)"
    assert value(rows, "j2", "Qwen 9B", q.format("swap the lens part", "recalled"))["value"] == breadth(
        "q9", "swap.q9.swap"
    )
    assert (
        value(rows, "j2", "Qwen 27B", q.format("swap everything else", "stated"))["value"] == 24.6
    )  # docs/shared/gaps.md row 3
    assert value(rows, "j2", "Qwen 27B", q.format("swap the lens part", "stated"))["value"] == 0.9


def test_j3_numbers_match_their_sources(drawn):
    _, rows = drawn
    assert value(rows, "j3", "Qwen 9B", "answers by position: without the order signal (share)")["value"] == 0.083
    assert (
        value(rows, "j3", "Muse 30B", "answers by position: without a random part (same size) (share)")["value"]
        == 0.547
    )
    assert value(rows, "j3", "Qwen 9B", "the order signal's write dose (x a real change's size)")["value"] == 1.06


def test_grid_front_cells_come_from_the_grid(drawn):
    _, rows = drawn
    assert value(rows, "grid_front", "Qwen 27B", "finding 1 (depth)")["value"] == "~"
    assert value(rows, "grid_front", "Muse 30B", "finding 4 (both)")["value"] == "x a"
    assert value(rows, "grid_front", "Nemotron Lightning", "finding 3 (depth)")["value"] == "-"


def test_example_texts_are_quoted_from_their_sources():
    src = (J.REPO / "scripts" / "readme_story_figures.py").read_text()
    assert all(s in src for s in (*J.DAN_SCENE[:2], "Iris picked the ", *(q for q, _, _ in J.DAN_QUESTIONS)))
    assert J.zach_texts()["question"] == "The composer who wrote The Magic Flute was of which nationality?"


@pytest.mark.parametrize(
    ("d", "b", "s", "want"),
    [("ok", "ok", "ok", ("ok", "")), ("~", "ok", "ok", ("~", "")), ("ok", "ok", "x", ("x", "")), ("ok", "x", "ok", ("x", "")),
     ("-", "ok", "ok", ("-", "")), ("ok", "ok", "~", ("~", ""))],
)  # fmt: skip
def test_agree_rule(d, b, s, want):
    cell = lambda c: {"cell": c, "flag": ""}  # noqa: E731
    assert J.agree(cell(d), cell(b), cell(s)) == want
