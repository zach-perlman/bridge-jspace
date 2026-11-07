"""The LessWrong write-up's figures (figures/writeup/, `make figures-writeup`): every figure of the target exists, is
1600 px wide, within the aspect range and on white; the dot table's write-up knobs leave the other targets alone."""

from __future__ import annotations

import pytest

from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import lint
from bridge_jspace.figkit import tables as TB
from bridge_jspace.figkit.theme import WRITEUP, WRITEUP_ASPECT

OUT = TB.OUT["writeup"]


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
    assert (tmp_path / "fig01_main_split.png").exists()


def test_png_problems_flags_a_wrong_width(tmp_path):
    from PIL import Image

    p = tmp_path / "x.png"
    Image.new("RGB", (800, 400), "white").save(p)
    probs = lint.png_problems(p, 1600, (1.4, 2.6))
    assert any("800 px wide" in s for s in probs)
    Image.new("RGBA", (1600, 800), (255, 255, 255, 0)).save(p)
    assert any("transparent" in s for s in lint.png_problems(p, 1600, (1.4, 2.6)))
