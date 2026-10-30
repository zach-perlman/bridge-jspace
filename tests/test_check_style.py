"""One palette in every README (Dan, 30 Oct): the figures the root and depth READMEs show draw their hues from
bridge_jspace/palette.py; the figure kit and the depth story figures read the same module."""

from __future__ import annotations

from pathlib import Path

from scripts import check_style as CS
from scripts import story_style as S


def test_the_kit_and_the_story_figures_read_the_one_palette():
    from bridge_jspace import palette as P
    from bridge_jspace.figkit import dottable as T

    assert T.C["lens"] == P.ROLE["lens"] and T.C["lookup"] == P.ROLE["lookup"] and T.C["question"] == P.SHADE["question"]
    assert S.MARK_COL["jpp"] == P.ROLE["lens"] and S.COL["lookup"] == P.ROLE["lookup"] and S.COL["recall"] == P.ROLE["recall"]
    assert S.COL["position"] == P.ROLE["address"] and S.COL["identity"] == P.ROLE["identity"]
    assert S.COL["control"] == P.ROLE["control"]


def test_every_depth_and_root_figure_is_on_the_palette():
    bad = []
    for name in ("root", "depth"):
        for png in CS.figures(CS.READMES[name]):
            if "figures/breadth/" in png.as_posix():  # Zach's pre-rendered figures, until they are redrawn
                continue
            share, top, _n = CS.off_palette(png)
            if share > CS.TOLERANCE:
                bad.append((name, Path(png).name, f"{share:.1%}", top))
    assert not bad, bad


def test_a_palette_audit_catches_a_foreign_hue(tmp_path):
    from PIL import Image

    ok, off = tmp_path / "ok.png", tmp_path / "off.png"
    Image.new("RGB", (40, 40), "#6B5BD2").save(ok)  # the lookup purple
    Image.new("RGB", (40, 40), "#184898").save(off)  # a breadth figure's dark blue
    assert CS.off_palette(ok)[0] == 0 and CS.off_palette(off)[0] == 1
