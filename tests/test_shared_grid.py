"""docs/shared/grid.csv and figures/shared/grid.png (scripts/shared_grid.py): every cell resolves to its source key
(depth: its scorecard.csv row and that row's data.csv key; breadth: docs/breadth/data.csv keys and their values under the
scorecard rule), the file is what the script builds from the sources now, and the figure reads at 880 px in the
glossary's words."""

from __future__ import annotations

import csv
import json

import pytest
import test_readme_build as RB
from matplotlib.text import Text

from bridge_jspace import plot_style as PS
from scripts import check_figure_terms as C
from scripts import shared_grid as G
from scripts import story_style as S


def read(path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def grid() -> list[dict]:
    return read(G.GRID)


def find(grid, claim: str, model: str, study: str) -> dict:
    (row,) = [r for r in grid if (r["claim"], r["model"], r["study"]) == (claim, model, study)]
    return row


def test_grid_is_what_the_sources_give_now(grid):
    assert list(grid[0]) == list(G.FIELDS)
    assert grid == G.build(), "docs/shared/grid.csv is stale: rerun scripts/shared_grid.py"


def test_every_claim_has_all_nine_models_and_only_shared_claims_have_both_studies(grid):
    headers = [h for h, _, _ in G.MODELS]
    assert len(headers) == len(set(headers)) == 9
    assert [name for _, name, _ in G.MODELS[:4]] == [name for _, _, name in S.MODELS]  # depth's four first
    columns: dict[tuple[str, str], list[str]] = {}
    for r in grid:
        columns.setdefault((r["claim"], r["study"]), []).append(r["model"])
    assert all(models == headers for models in columns.values())
    studies: dict[str, set[str]] = {}
    for claim, study in columns:
        studies.setdefault(claim, set()).add(study)
    assert {c for c, s in studies.items() if len(s) == 2} == set(G.SHARED)


def test_depth_cells_resolve_to_their_scorecard_row_and_key(grid):
    card = {(r["claim"], r["model"]): r for r in read(G.SCORECARD)}
    numbers = json.loads(S.NUMBERS.read_text())
    recorded = {(r["figure"], r["model"], r["quantity"]) for r in read(G.DEPTH_DATA)}
    targets = {name: target for target, _, name in S.MODELS}
    seen = set()
    for r in (r for r in grid if r["study"] == "depth"):
        assert r["source"] == "data/figures/depth/scorecard.csv"
        got = card.get((r["source row"], r["model key"]))
        if got is None:  # never run on this model: no scorecard row, a dash
            assert (r["cell"], r["flag"], r["key"], r["value"]) == ("-", "", "", ""), r
            continue
        seen.add((r["source row"], r["model key"]))
        assert (r["cell"], r["flag"], r["key"]) == (got["cell"], got["flag"], got["data.csv key"]), r
        if r["key"]:
            fig_id, quantity = r["key"].split(":", 1)
            ok = quantity in numbers if fig_id == "numbers" else (fig_id, targets[r["model key"]], quantity) in recorded
            assert ok and r["value"], r
    assert seen == set(card), "a scorecard.csv row is missing from the grid"


def test_breadth_cells_resolve_to_their_data_csv_keys(grid):
    data = {(r["model"], r["key"]): float(r["value"]) for r in read(G.BREADTH_DATA)}
    rules = {rule[0]: rule for rule in G.BREADTH_RULES}
    graded = 0
    for r in (r for r in grid if r["study"] == "breadth"):
        assert r["source"] == "docs/breadth/data.csv"
        _, column, keys_of, verdict, flag = rules[r["claim"]]
        keys = keys_of(r["model key"])
        assert r["source row"] == column
        if r["cell"] == "-":  # not run, or not in data.csv
            assert (r["flag"], r["key"]) == ("", "") and not all((r["model key"], k) in data for k in keys), r
            continue
        assert r["key"].split("; ") == keys, r
        assert r["cell"] == verdict(*[data[(r["model key"], k)] for k in keys]), r
        assert r["flag"] == G.breadth_flag(flag, r["model key"], keys), r
        graded += 1
    assert graded == 64  # 10 rules x 9 models, less the 26 cells data.csv has no key for


# five cells per source against the numbers each README states (depth: data/figures/depth/scorecard.csv; breadth: Zach's
# README sections 1, 4 and 8)
@pytest.mark.parametrize(
    ("claim", "model", "study", "cell"),
    [
        (G.RECALL, "Qwen3.6-27B", "depth", "~"),
        (G.MARGIN, "Qwen3.5-122B-A10B (FP8)", "depth", "ok"),
        ("locker before the pick", "Qwen3.5-122B-A10B (FP8)", "depth", "x"),
        ("natural passages", "Muse Glimmer 30B", "depth", "-"),
        ("refit per format", "Nemotron 3.5 Bolt", "depth", "-"),
        (G.RECALL, "Nemotron 3.5 Bolt", "breadth", "x"),  # +6 [3, 9]
        (G.RECALL, "DeepSeek-V4-Flash", "breadth", "~"),  # +18, weak
        (G.MARGIN, "Qwen3.5-122B-A10B (FP8)", "breadth", "x"),  # +2 by probability against +48
        ("specific: rotated and logit-lens removals cost < 10", "Muse Glimmer 30B", "breadth", "x"),  # logit lens +35
        ("another entity's J++ part moves the answer (≥ 20 points)", "Ministral-3-14B", "breadth", "x"),  # +3, mid depth
    ],
)  # fmt: skip
def test_spot_cells(grid, claim, model, study, cell):
    assert find(grid, claim, model, study)["cell"] == cell


@pytest.mark.parametrize("name", list(G.FIGURES))
def test_each_grid_figure_reads_at_880px_in_the_joint_vocabulary(grid, name):
    plt = S.setup()
    fig = G.draw(plt, grid, name)
    try:
        assert fig.get_figwidth() == S.WIDTH
        assert PS.overlaps(fig) == []
        texts = [(name, t.get_text()) for t in fig.findobj(Text) if t.get_text().strip()]
        assert not RB.banned(texts) and not C.retired(texts) and not C.joint_retired(texts)
        assert G.FIGURES[name][0] in [t for _, t in texts]
    finally:
        plt.close(fig)


def test_the_two_figures_show_every_grid_claim_once_on_the_models_that_have_cells(grid):
    placed = [(name, claim) for name, (*_, groups, _) in G.FIGURES.items() for _, items in groups for _, claim in items]
    assert sorted(claim for _, claim in placed) == sorted(dict.fromkeys(r["claim"] for r in grid))
    for name, claim in placed:  # a figure leaves out only models where the claim has no graded cell
        shown = set(G.FIGURES[name][2])
        graded = {G.code_of(r) for r in grid if r["claim"] == claim and r["cell"] != "-"}
        assert graded <= shown, (name, claim, graded - shown)
    labels = [short for *_, groups, _ in G.FIGURES.values() for _, items in groups for short, _ in items]
    assert all(len(s.split()) <= 9 for s in labels), [s for s in labels if len(s.split()) > 9]
