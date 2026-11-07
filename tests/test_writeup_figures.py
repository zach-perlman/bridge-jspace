"""The LessWrong write-up's figures (figures/writeup/, `make figures-writeup`): every figure of the target exists, is
1600 px wide, within the aspect range and on white; the dot table's write-up knobs leave the other targets alone."""

from __future__ import annotations

import csv
import re
import sys

import pytest

from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import lint
from bridge_jspace.figkit import tables as TB
from bridge_jspace.figkit.theme import WRITEUP, WRITEUP_ASPECT, WRITEUP_MIN_ROW

OUT = TB.OUT["writeup"]
REPO = TB.REPO
DATA = REPO / "data" / "figures" / "writeup" / "data.csv"
PATH = re.compile(r"\b(?:results|data|docs|scripts)/[\w.\-/\[\]]+")
# the precision each figure prints (one precision per column; Amendment 1): key prefix -> decimals
PRINTED = {"fig04.recall": 0, "fig04.lookup": 0, "fig04.gap": 1, "fig05.band_diff": 1, "fig10.span_only_matched": 2,
           "fig10": 2, "fig11": 1, "figA1": 1, "fig12": 1}  # fmt: skip


def _stored() -> list[dict]:
    with DATA.open() as f:
        return list(csv.DictReader(f))


def _digits(key: str) -> int:
    return next(d for p, d in sorted(PRINTED.items(), key=lambda kv: -len(kv[0])) if key.startswith(p))


def test_every_data_row_names_existing_sources():
    for r in _stored():
        paths = PATH.findall(r["source"])
        assert paths, f"{r['key']}: no file in its source"
        for p in paths:
            assert (REPO / p).exists(), f"{r['key']}: {p} does not exist"


@pytest.fixture(scope="module")
def recomputed() -> dict:
    sys.path.insert(0, str(REPO))
    from scripts import writeup_data as WD

    return {r["key"]: r for r in WD.rows()}


def test_recomputing_each_row_gives_its_value_at_the_printed_precision(recomputed):
    stored = _stored()
    assert {r["key"] for r in stored} == set(recomputed), "data.csv is stale: run scripts/writeup_data.py"
    for r in stored:
        new, d = recomputed[r["key"]], _digits(r["key"])
        for field in ("value", "lo", "hi"):
            a, b = r[field], new[field]
            if a == "" or b == "":
                assert a == "" and b == "", (r["key"], field, a, b)
                continue
            assert round(float(a), d) == round(float(b), d), (r["key"], field, a, b)


def test_each_new_figure_has_rows():
    keys = {r["key"].split(".")[0] for r in _stored()}
    assert {"fig04", "fig05", "fig10", "fig11"} <= keys


@pytest.mark.parametrize("fig_id", TB.TARGET["writeup"])
def test_every_writeup_figure_has_a_png(fig_id):
    assert (OUT / f"{fig_id}.png").exists(), f"run `make figures-writeup`: {fig_id}.png missing"


@pytest.mark.parametrize("fig_id", TB.TARGET["writeup"])
def test_writeup_png_geometry(fig_id):
    png = OUT / f"{fig_id}.png"
    if not png.exists():
        pytest.skip("missing (reported by the test above)")
    assert lint.png_problems(png, round(WRITEUP.sizes["full"][0] * WRITEUP.dpi), WRITEUP_ASPECT) == []


def test_writeup_ids_stay_out_of_the_readme():
    assert not set(TB.TARGET["writeup"]) & set(TB.TARGET["readme"])


def test_build_restores_the_default_font_sizes(tmp_path, monkeypatch):
    monkeypatch.setitem(TB.OUT, "writeup", tmp_path)
    TB.build("writeup", ["fig01"])
    assert T.FS == T.FS_DEFAULT
    assert T.MIN_ROW_H == 0.0
    assert (tmp_path / "fig01_main_split.png").exists()


def test_png_problems_flags_a_wrong_width(tmp_path):
    from PIL import Image

    p = tmp_path / "x.png"
    Image.new("RGB", (800, 400), "white").save(p)
    probs = lint.png_problems(p, 1600, WRITEUP_ASPECT)
    assert any("800 px wide" in s for s in probs)
    Image.new("RGBA", (1600, 800), (255, 255, 255, 0)).save(p)
    assert any("transparent" in s for s in lint.png_problems(p, 1600, WRITEUP_ASPECT))


@pytest.mark.parametrize(("height", "ok"), [(1600, True), (1700, False), (616, True), (600, False)])
def test_png_problems_aspect_range(tmp_path, height, ok):
    """Amendment 1: width:height from 1.0 (square) to 2.6."""
    from PIL import Image

    p = tmp_path / "x.png"
    Image.new("RGB", (1600, height), "white").save(p)
    assert (lint.png_problems(p, 1600, WRITEUP_ASPECT) == []) is ok


def _panel():
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(4, 2), dpi=100)
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7), xlim=(-10, 10), ylim=(1, -1))
    ax.plot([0, 0], [1, -1], color=T.MUTED)  # a zero line
    ax.plot([5], [0], "o", ms=9.5, color=T.INK)  # a dot
    return fig, ax


def test_crossings_flags_text_over_a_line_or_on_a_mark():
    """Review of batch 2: text never crosses a line (spine, zero line, rule) or sits on a mark."""
    fig, ax = _panel()
    ax.text(0, 0.5, "267 items", ha="center", va="center")
    ax.text(5.6, 0, "6.2", ha="left", va="center")
    probs = lint.crossings(fig, "x")
    assert any("crosses a line '267 items'" in p for p in probs)
    assert any("on a mark '6.2'" in p for p in probs)


def test_crossings_lets_a_masking_note_stop_the_lines_but_not_the_marks():
    fig, ax = _panel()
    t = ax.text(0, 0.6, "descriptive", ha="center", va="center")
    t._masks_lines = True
    ax.text(-8, -0.6, "clear", ha="left", va="center")
    assert lint.crossings(fig, "x") == []
    t.set_position((5, 0.1))
    assert any("on a mark" in p for p in lint.crossings(fig, "x"))


def test_grid_lines_are_exempt():
    fig, ax = _panel()
    ax.plot([-5, -5], [1, -1], color=T.GRID)
    ax.text(-5, 0.5, "on the grid", ha="center", va="center")
    assert lint.crossings(fig, "x") == []


@pytest.mark.parametrize(("n", "skip", "spans"), [(4, (), [(0, 4)]), (8, (0, 4), [(1, 4), (5, 8)]), (3, (2,), [(0, 2)])])
def test_lines_stop_at_skipped_rows(n, skip, spans):
    assert T.runs(n, skip) == spans


def test_writeup_rejects_a_squeezed_row(tmp_path, monkeypatch):
    """Amendment 1: every dot-table row of the write-up is at least WRITEUP_MIN_ROW tall."""
    monkeypatch.setattr(T, "MIN_ROW_H", WRITEUP_MIN_ROW)
    t = T.Table([T.Row("a")], [T.Col(1.0, "x", draw=lambda ax, r: None, xlim=(0, 1))], row_h=0.27)
    with pytest.raises(ValueError, match="row"):
        t.render(str(tmp_path / "x.png"))
