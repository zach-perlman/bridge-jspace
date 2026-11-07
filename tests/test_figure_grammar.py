"""Figure grammar v2 (docs/shared/figure_style.md): the meaning checks of figkit/grammar.py catch what they should, the
status registry is well formed, the pilot figures pass, one data key prints one string in every figure, and the
CIEDE2000 used by the colour-vision check is the published one."""

from __future__ import annotations

import csv
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from bridge_jspace import palette as P
from bridge_jspace.figkit import grammar as G
from bridge_jspace.figkit import tables as TB
from bridge_jspace.figkit import terms as TM
from bridge_jspace.figkit import writeup_v2 as W2
from bridge_jspace.figkit.colour_vision import ciede2000

FAKE = {("t", "a"): {"status": "fixed_in_advance", "tag": ""}, ("t", "b"): {"status": "post_hoc", "tag": ""}}


@pytest.fixture
def panel(monkeypatch):
    monkeypatch.setattr(G, "registry", lambda: FAKE)
    G.begin("t")
    fig = plt.figure(figsize=(4, 2), dpi=100)
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.6), xlim=(0, 10), ylim=(1, -1))
    yield fig, ax
    plt.close(fig)


def test_registry_is_well_formed():
    with G.STATUS_CSV.open() as f:
        rows = list(csv.DictReader(f))
    assert rows, "data/figures/status.csv is empty: run scripts/status_registry.py"
    assert len({(r["figure"], r["cell"]) for r in rows}) == len(rows), "a (figure, cell) twice"
    for r in rows:
        assert r["status"] in G.STATUSES, r
        assert r["tag"] in ("", *(TM.NOT_CLAIMED.format(w) for w in TM.NOT_CLAIMED_WHY)), r
        assert r["source"], r


def test_a_role_word_and_a_mark_pass(panel):
    fig, ax = panel
    G.mark(ax, 3, 0, "lookup", "a")
    G.role_word(ax, 3, "lookup", "lookup")
    assert G.check(fig, "t") == []


def test_a_mark_in_another_role_colour_fails(panel):
    fig, ax = panel
    _, = ax.plot([3], [0], "o", color=P.ROLE["recall"])
    _._g = {"kind": "dot", "role": "lookup", "cell": "a", "status": "fixed_in_advance", "hollow": False}
    assert any("tagged lookup drawn in" in p for p in G.check(fig, "t"))


def test_purple_for_a_variable_fails(panel):
    fig, ax = panel
    ax.plot([3], [0], "o", color=P.LEGACY["lookup_dark"])
    assert any("legacy shade" in p for p in G.check(fig, "t"))


def test_an_untagged_role_colour_fails(panel):
    fig, ax = panel
    ax.plot([3], [0], "o", color=P.ROLE["lens"])
    assert any("untagged mark in the lens colour" in p for p in G.check(fig, "t"))


def test_hollow_follows_the_registry_both_ways(panel):
    fig, ax = panel
    G.mark(ax, 3, 0, "control", "b", name="rotated")  # post hoc in the registry: drawn hollow by mark()
    assert ax.lines[-1]._g["hollow"]
    ax.lines[-1]._g["hollow"] = False  # a figure that forced it filled
    assert any("drawn filled, registry says post_hoc" in p for p in G.check(fig, "t"))


def test_key_completeness_both_ways(panel):
    fig, ax = panel
    G.mark(ax, 3, 0, "control", "a", interval=(2, 4), name="rotated")
    probs = G.check(fig, "t")
    assert any("whiskers: 95% interval" in p and "drawn but not named" in p for p in probs)
    assert any("a control drawn but not named" in p for p in probs)
    fig.text(0, 0, TM.KEY_BAND)
    assert any("named but not drawn" in p for p in G.check(fig, "t"))


def test_words_and_cues(panel):
    fig, ax = panel
    fig.text(0, 0, "J++ part removed")
    ax._cue = "← address needed"
    probs = G.check(fig, "t")
    assert any("not in figkit/terms.py" in p for p in probs)
    assert any("banned word" in p for p in probs)
    assert any("is not '→ more …'" in p for p in probs)


@pytest.mark.parametrize(("text", "ok"), [("42.6", True), ("[37.0, 49.0]", True), ("18 of 30", True), ("lookup", True),
                                          ("Qwen 27B", True), ("accuracy drop\n(points)", True), ("pts", False),
                                          ("registered", False), ("Zach's passages", False)])  # fmt: skip
def test_terms_allowed(text, ok):
    assert TM.allowed(text) is ok


def test_numbers_print_one_precision_per_unit():
    G.begin("t")
    assert G.num("k", 42.649, "points") == "42.6"
    assert G.num("k", 0.5349, "share") == "0.53"
    assert G.num("k", 99.4, "accuracy") == "99"
    assert G.num("k", -0.04, "points") == "0.0"  # no "−0.0"
    assert G.num("k", -1.26, "points") == "−1.3"
    assert G.count("k", 18, 30) == "18 of 30"


def test_the_palette_has_one_hue_per_role():
    assert {"answer", "neutral", "mention", "question"} <= set(P.ROLE)
    assert not {v.lower() for v in P.LEGACY.values()} & {v.lower() for v in P.ROLE.values()}
    assert len({v.lower() for v in P.ROLE.values()}) == len(P.ROLE)


@pytest.mark.parametrize(("a", "b", "want"), [((50, 2.6772, -79.7751), (50, 0, -82.7485), 2.0425),
                                              ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
                                              ((50, 2.5, 0), (73, 25, -18), 27.1492)])  # fmt: skip
def test_ciede2000_matches_sharma(a, b, want):
    """Sharma, Wu and Dalal (2005), table 1, pairs 1, 22 and 25."""
    assert round(ciede2000(a, b), 4) == want


@pytest.fixture(scope="module")
def pilot(tmp_path_factory):
    out = tmp_path_factory.mktemp("v2")
    saved = TB.OUT["writeup"]
    TB.OUT["writeup"] = out
    TB.PROBLEMS.clear()
    G.NUMBERS.clear()
    try:
        TB.build("writeup", list(W2.FIGS))
    finally:
        TB.OUT["writeup"] = saved
    return out, list(TB.PROBLEMS), list(G.NUMBERS)


def test_the_pilot_figures_pass_every_check(pilot):
    out, problems, _ = pilot
    assert problems == []
    for fid in W2.FIGS:
        assert (out / f"{fid}.png").exists()


def test_one_data_key_prints_one_string_everywhere(pilot):
    _, _, numbers = pilot
    seen = defaultdict(set)
    for _fid, key, s in numbers:
        seen[key].add(s)
    assert {k: v for k, v in seen.items() if len(v) > 1} == {}
