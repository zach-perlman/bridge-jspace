"""Batch 49's README figure (scripts/story_b49.py) on planted verdict folders: made by x49_gain's own verdict stage from
the planted runs of tests/test_x49_gain.py (no real result is read). The figure builds, records every plotted number
with its verdict file as the source, saves to tmp_path, and has no overlapping text, banned variant or retired term."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import test_x49_gain as TG
from test_readme_phase2_figures import check, saved  # noqa: F401 (saved: a fixture)

from scripts import story_b49 as B
from scripts import story_style as S

N_BOOT = 100


def planted(tmp_path: Path, mp, kinds: dict) -> Path:
    return TG.planted_verdict(tmp_path, mp, kinds, n_boot=N_BOOT)


@pytest.mark.parametrize("kinds", [{"qwen3.5-9b": "a", "qwen3.6-27b": "a_prime", "muse-glimmer-30b": None},
                                   {"qwen3.6-27b": "b"}])  # fmt: skip
def test_figure_on_its_planted_verdict(kinds, tmp_path, monkeypatch, saved):  # noqa: F811
    verdict = planted(tmp_path / "results", monkeypatch, kinds)
    _, build, name = B.TESTS["49.1"]
    assert build(verdict, name) == name
    assert (S.OUT / f"{name}.png").exists() and (S.OUT / f"{name}.svg").exists()
    check(saved[name])
    rows = [r for r in S.ROWS if r["figure"] == B.fig_id(name)]
    assert rows and all(r["source"].endswith("x49_1.json") for r in rows)
    assert any(isinstance(r["value"], float) and r["lo"] is not None for r in rows)  # a number with its interval
    tested = sum(v is not None for v in kinds.values())
    per_reader = 25 + len(B.STRIP)
    assert len([r for r in rows if r["quantity"].startswith("49.1: recall's")]) == tested * per_reader
    assert len([r for r in rows if r["quantity"] == "49.1: the rule's reading"]) == len(B.TARGETS)


def test_titles_read_the_planted_outcomes(tmp_path, monkeypatch):
    def title(kinds: dict) -> str:
        out = planted(tmp_path / str(len(list(tmp_path.iterdir()))), monkeypatch, kinds)
        return B.gain_title(json.loads((out / "x49_1.json").read_text()))

    assert title({"qwen3.5-9b": "a", "qwen3.6-27b": "a", "muse-glimmer-30b": "a"}) == B.TITLES["a"]
    assert (
        title({"qwen3.5-9b": "b", "qwen3.6-27b": "b", "muse-glimmer-30b": "c"}) == f"{B.TITLES['b']}, on 2 of 3 models"
    )
    assert title({"qwen3.5-9b": "a", "qwen3.6-27b": "b", "muse-glimmer-30b": "a_prime"}) == (
        "The gain map: the reading differs by model"
    )
    assert title({"muse-glimmer-30b": None}) == "The gain map: no model tested yet"
    assert all(len(t) <= 86 for t in B.TITLES.values())


def test_a_given_title_wins(tmp_path, monkeypatch, saved):  # noqa: F811
    verdict = planted(tmp_path / "results", monkeypatch, {"qwen3.5-9b": "c"})
    B.build_gain(verdict, "fig27_gain_map", title="A claim Dan wrote")
    assert saved["fig27_gain_map"]["title"] == "A claim Dan wrote"


def test_strip_cells_sit_beside_their_labels():
    # the top cell of the strip is STRIP[0]'s value and carries STRIP[0]'s label (a reversed image once hid this)
    plt = S.setup()
    fig, ax = plt.subplots()
    rate = {a: [k / 10, 0.0, 1.0] for k, (a, _) in enumerate(B.STRIP)}
    B.strip(ax, rate, S.COL["recall"])
    img = ax.images[0]
    top = len(B.STRIP) - 1
    arr = img.get_array()
    assert arr is not None and img.origin == "upper" and float(arr[0, 0]) == rate[B.STRIP[0][0]][0]
    labels = {round(t.get_position()[1]): t.get_text() for t in ax.get_yticklabels()}
    assert labels[top] == B.STRIP[0][1] and labels[0] == B.STRIP[-1][1]
    texts = {round(t.get_position()[1]): t.get_text() for t in ax.texts}
    assert texts[top] == "0" and texts[0] == f"{100 * rate[B.STRIP[-1][0]][0]:.0f}"
    plt.close(fig)
