"""The figure sets' layout (Dan, 7 Nov; by track, 8 Nov; figkit/layout.py): figures/ holds only the track folders
breadth/, depth/ and common/, each only its sets; every set is flat and numbered, holds only its figures, README.md,
_meta/ and _sheets/ (an empty set, common/examples, has no sheets); every figure has its sidecar under _meta/ and is in its set's order; every
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
NAME = re.compile(r"^(?:00_key|(?:\d{2}[a-z]?\d?|a\d{2}|s\d{2}|e\d{2}|r\d{2})_[a-z0-9_]+)\.png$")  # e: the post's setup figures; r: its results figures
LINK = re.compile(r"\]\(([^)\s]+?\.png)\)")
ARCHIVES = ("docs/archive/", "data/figures/archive/", "results/")
# templates whose links are written from the repo root (their builder rewrites them for the rendered page)
ROOT_RELATIVE = {"docs/readme/README.template.md", "docs/depth/README.template.md"}


def docs() -> list[str]:
    out = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, cwd=REPO).stdout.split()
    return [f for f in out if not f.startswith(ARCHIVES)]


def links(md: str) -> list[str]:
    base = Path(".") if md in ROOT_RELATIVE else Path(md).parent
    text = re.sub(r"(?ms)^(`{3,}).*?^\1", "", (REPO / md).read_text(errors="ignore"))  # a link in a code block is an example
    return [os.path.normpath(base / t) for t in LINK.findall(text) if "://" not in t]


def test_figures_holds_the_tracks_and_their_sets_only():
    tracks = {p.name: {q.name for q in p.iterdir()} for p in (REPO / "figures").iterdir()}
    assert tracks == {
        "breadth": {"readme", "examples"},
        "depth": {"readme", "ledger", "examples"},
        "common": {"readme", "writeup", "examples"},
    }, tracks
    assert set(L.ORDER) == {f"{t}/{s}" for t, sets in tracks.items() for s in sets}


@pytest.mark.parametrize("group", list(L.ORDER))
def test_a_set_holds_only_its_figures_its_index_meta_and_sheets(group):
    folder = REPO / "figures" / group
    entries = {p.name for p in folder.iterdir()}
    pngs = {n for n in entries if n.endswith(".png")}
    assert entries - pngs <= {"README.md", "_meta", "_sheets"}, entries - pngs
    assert all(NAME.match(n) for n in pngs), sorted(n for n in pngs if not NAME.match(n))
    assert pngs == {f"{stem}.png" for stem in L.names(group).values()}
    meta = {p.name for p in (folder / "_meta").iterdir()}
    # problems.json: each figure's last problems per target, written by styles-plot's save (0.2, C5)
    if not L.names(group):  # an empty set (common/examples): its index, order and caption store only
        assert entries == {"README.md", "_meta"} and meta == {"order.txt", "captions.toml"}, (entries, meta)
        return
    assert meta - {"captions.toml", "captions_short.toml"} == ({f"{stem}.styles.json" for stem in L.names(group).values()}
                                        | {"order.txt", "problems.json"})  # fmt: skip
    assert (folder / "_meta" / "order.txt").read_text().split() == [f"{s}.png" for s in L.names(group).values()]
    assert {p.name for p in (folder / "_sheets").iterdir()} == {"contact_sheet.png", "contact_sheet_gray.png"}
    assert not [p for p in folder.rglob("*") if p.is_dir() and p.name not in ("_meta", "_sheets")]


@pytest.mark.parametrize("group", list(L.ORDER))
def test_every_set_has_one_caption_per_figure(group):
    """Dan, 8 Nov (G2): figures/<set>/_meta/captions.toml in every set, one caption per figure and none left over."""
    import tomllib

    store = REPO / "figures" / group / "_meta" / "captions.toml"
    assert store.exists(), f"{group}: no _meta/captions.toml"
    captions = tomllib.loads(store.read_text())
    assert set(captions) == set(L.names(group).values()), set(captions) ^ set(L.names(group).values())
    assert all(isinstance(c, str) and c.strip() for c in captions.values())


@pytest.mark.parametrize("group", list(L.ORDER))
def test_short_captions_name_real_figures_and_stay_short(group):
    """The README pages' short captions (readability brief, 8 Nov): only for figures of the set, at most 60 words."""
    import tomllib

    store = REPO / "figures" / group / "_meta" / "captions_short.toml"
    short = tomllib.loads(store.read_text()) if store.exists() else {}
    assert set(short) <= set(L.names(group).values()), set(short) - set(L.names(group).values())
    assert not (long := {k: n for k, c in short.items() if (n := len(re.findall(r"\w[\w'’.-]*", c))) > 60}), long


@pytest.mark.parametrize("group", list(L.ORDER))
def test_the_index_lists_every_figure_in_order(group):
    text = (REPO / "figures" / group / "README.md").read_text()
    shown = re.findall(r'<img src="([^"]+)\.png"', text)
    assert shown == list(L.names(group).values())


def test_first_sentence_drops_src_comments_and_keeps_placeholders_visible():
    from bridge_jspace.figkit.captions import first_sentence

    assert first_sentence("Rows are 3<!-- src: a | b --> models; {{q|95%}} intervals. Left: x.") == (
        "Rows are 3 models; 95% intervals."
    )
    assert first_sentence("At layer {{x|layer_27b}}. Next.") == "At layer `{{x|layer_27b}}`."
    assert first_sentence("Fig. 5a, e.g. here, has 0.10 of it. Next.") == "Fig. 5a, e.g. here, has 0.10 of it."


@pytest.mark.parametrize("group", [g for g in L.ORDER if g != "common/writeup"])  # the write-up passes its own lines
def test_the_index_shows_each_captions_first_sentence(group):
    from bridge_jspace.figkit import captions as C

    rows = {m[0]: m[1] for m in re.findall(r'<img src="([^"]+)\.png"[^|]*\| (.*) \| [^|]*\|$', (
        REPO / "figures" / group / "README.md").read_text(), flags=re.M)}  # fmt: skip
    for stem in L.names(group).values():
        assert rows[stem] == C.first_sentence(C.caption(group, stem)).replace("|", "\\|"), stem


def test_every_figure_outside_the_write_up_is_embedded_by_a_doc():
    used = {p for md in docs() if not md.startswith("figures/") for p in links(md)}
    for group in L.ORDER:
        if group == "common/writeup":  # embedded by the post (outside the repo) and by its index
            continue
        for stem in L.names(group).values():
            assert f"figures/{group}/{stem}.png" in used, f"{group}/{stem}.png is embedded by no doc"


def test_every_figure_link_resolves():
    dead = [(md, p) for md in docs() for p in links(md) if not (REPO / p).exists()]
    assert not dead, dead


def test_names_follow_the_document():
    assert L.names("common/writeup")["fig05a_controls_band"] == "05a_controls_band"
    assert L.names("common/writeup")["key"] == "00_key"
    assert L.names("common/writeup")["figA1_agents"] == "a01_agents"
    assert L.names("depth/readme")["s01_split_all_scene_sets"] == "s01_split_all_scene_sets"
    assert L.names("depth/ledger")["fig40_item_not_answer"] == "01_item_not_answer"
    assert L.names("common/readme")["p0b_tools"] == "01_tools"
    assert L.names("breadth/examples")["e3_chains"] == "02_chains"
    assert L.names("common/examples") == {}
