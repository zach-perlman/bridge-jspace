"""The figure sets' layout (Dan, 7 Nov; figkit/layout.py): every figures/<set>/ is flat and numbered, holds only its
figures, README.md, _meta/ and _sheets/; every figure has its sidecar under _meta/ and is in its set's order; every
figure outside the write-up is embedded by a doc (the write-up's are embedded by the post, outside the repo); every
figure link in the repo's docs resolves."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest

from bridge_jspace.figkit import layout as L

REPO = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^(?:00_key|(?:\d{2}[a-z]?\d?|a\d{2}|s\d{2})_[a-z0-9_]+)\.png$")
LINK = re.compile(r"\]\(([^)\s]+?\.png)\)")
ARCHIVES = ("docs/archive/", "data/figures/archive/", "results/")
# templates whose links are written from the repo root (their builder rewrites them for the rendered page)
ROOT_RELATIVE = {"docs/readme/README.template.md", "docs/depth/README.template.md"}


def docs() -> list[str]:
    out = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, cwd=REPO).stdout.split()
    return [f for f in out if not f.startswith(ARCHIVES)]


def links(md: str) -> list[str]:
    base = Path(".") if md in ROOT_RELATIVE else Path(md).parent
    return [os.path.normpath(base / t) for t in LINK.findall((REPO / md).read_text(errors="ignore")) if "://" not in t]


@pytest.mark.parametrize("group", list(L.ORDER))
def test_a_set_holds_only_its_figures_its_index_meta_and_sheets(group):
    folder = REPO / "figures" / group
    entries = {p.name for p in folder.iterdir()}
    pngs = {n for n in entries if n.endswith(".png")}
    assert entries - pngs <= {"README.md", "_meta", "_sheets"}, entries - pngs
    assert all(NAME.match(n) for n in pngs), sorted(n for n in pngs if not NAME.match(n))
    assert pngs == {f"{stem}.png" for stem in L.names(group).values()}
    meta = {p.name for p in (folder / "_meta").iterdir()}
    assert meta == {f"{stem}.styles.json" for stem in L.names(group).values()} | {"order.txt"}
    assert (folder / "_meta" / "order.txt").read_text().split() == [f"{s}.png" for s in L.names(group).values()]
    assert {p.name for p in (folder / "_sheets").iterdir()} == {"contact_sheet.png", "contact_sheet_gray.png"}
    assert not [p for p in folder.rglob("*") if p.is_dir() and p.name not in ("_meta", "_sheets")]


@pytest.mark.parametrize("group", list(L.ORDER))
def test_the_index_lists_every_figure_in_order(group):
    text = (REPO / "figures" / group / "README.md").read_text()
    shown = re.findall(r'<img src="([^"]+)\.png"', text)
    assert shown == list(L.names(group).values())


def test_every_figure_outside_the_write_up_is_embedded_by_a_doc():
    used = {p for md in docs() if not md.startswith("figures/") for p in links(md)}
    for group in L.ORDER:
        if group == "writeup":  # embedded by the post (outside the repo) and by its index
            continue
        for stem in L.names(group).values():
            assert f"figures/{group}/{stem}.png" in used, f"{group}/{stem}.png is embedded by no doc"


def test_every_figure_link_resolves():
    dead = [(md, p) for md in docs() for p in links(md) if not (REPO / p).exists()]
    assert not dead, dead


def test_names_follow_the_document():
    assert L.names("writeup")["fig05a_controls_band"] == "05a_controls_band"
    assert L.names("writeup")["key"] == "00_key"
    assert L.names("writeup")["figA1_agents"] == "a01_agents"
    assert L.names("depth")["s01_split_all_scene_sets"] == "s01_split_all_scene_sets"
    assert L.names("readme")["p0b_tools"] == "01_tools"
