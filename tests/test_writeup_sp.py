"""The write-up's styles-plot figures (figkit/writeup_sp.py): plotstyle.toml says what figkit/terms.py says, the
registry conversion keeps every status, every figure saves strict, and one data key prints one string across them."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import pytest
import styles_plot as sp

from bridge_jspace import palette as P
from bridge_jspace.figkit import terms as TM
from bridge_jspace.figkit import writeup_sp as SP
from scripts import convert_status_registry as CR

REPO = Path(__file__).resolve().parents[1]
V = sp.load(REPO / "plotstyle.toml")


# ---- the vocabulary --------------------------------------------------------------------------------------------------
def test_roles_keep_their_colours_and_words():
    for name, role in V.roles.items():
        assert role.hex.upper() == P.ROLE[name].upper()
        assert role.word == TM.ROLE_WORD[name]
        assert role.meaning == TM.ROLE_MEANING[name]
    assert "mention" not in V.roles and "question" not in V.roles  # no colours (Dan, 7 Nov)


def test_units_controls_and_words_match_terms():
    for u, title in TM.UNIT.items():
        assert V.units[u].title == title
        assert V.cue(u) == TM.cue(u)
    assert V.controls == TM.CONTROLS
    assert V.missing == TM.MISSING
    assert V.not_claimed == TM.NOT_CLAIMED_WHY
    assert V.key_tick and TM.KEY_TICK.endswith(V.key_tick)
    assert V.key_band and TM.KEY_BAND.endswith(V.key_band)
    assert {b.pattern for b in V.banned} >= set(TM.BANNED)


def test_models_in_order():
    assert [(e.key, e.name) for e in V.entities("models")][: len(P.MODELS)] == list(P.MODELS)
    assert [e.name for e in V.entities("models")][len(P.MODELS) :] == list(P.BREADTH_ONLY)


def test_read_aloud_matches_a_template():
    s = TM.READ_ALOUD.format(model="Qwen 27B", recall="53.5", lookup="2.6", gap="50.9", ctrl="12.4")
    assert V.template_re.fullmatch(s)


# ---- the registry ----------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(("old", "want"), [
    ({"status": "post_hoc", "tag": ""}, ("post_hoc", "claimed", "")),
    ({"status": "fixed_in_advance", "tag": ""}, ("fixed_in_advance", "claimed", "")),
    ({"status": "post_hoc", "tag": "not claimed: shared with the logit lens"},
     ("post_hoc", "not_claimed", "shared with the logit lens")),
    ({"status": "descriptive", "tag": ""}, ("fixed_in_advance", "descriptive", "")),
])  # fmt: skip
def test_conversion_keeps_timing_and_claim(old, want):
    row = CR.convert({"figure": "f", "cell": "c", "reason": "r", "source": "s", **old})
    assert (row["timing"], row["claim"], row["claim_reason"]) == want


def test_converted_registry_is_current_and_loads():
    with CR.SRC.open(newline="") as f:
        want = [CR.convert(r) for r in csv.DictReader(f)]
    with CR.OUT.open(newline="") as f:
        assert list(csv.DictReader(f)) == want
    reg = sp.load_registry(CR.OUT)
    assert len(reg) == len(want)


# ---- the figures -----------------------------------------------------------------------------------------------------
# styles-plot 0.1.7 regression (reported): the 27B's "0.61" is set left of its dot across the zero line though the
# right side is free; fig05b built strict on 0.1.6 and its PNG is that build
LIBRARY_REGRESSION = {"fig05b_controls_layer"}
BUILT = [f for f in SP.FIGS if f not in LIBRARY_REGRESSION]


@pytest.mark.xfail(strict=True, reason="styles-plot 0.1.7: left value label across the zero line (fig05b)")
def test_fig05b_saves_strict(tmp_path):
    sp.save(SP.FIGS["fig05b_controls_layer"](), tmp_path / "fig05b.png", target="post")


@pytest.fixture(scope="module")
def saved(tmp_path_factory):
    out = tmp_path_factory.mktemp("sp")
    return {fid: sp.save(SP.FIGS[fid](), out / f"{fid}.png", target="post") for fid in BUILT}


def test_every_figure_saves_strict(saved):
    for fid, report in saved.items():
        assert report.path.exists() and report.problems == [], fid


def test_one_data_key_prints_one_string_across_figures(saved):
    seen = defaultdict(set)
    for report in saved.values():
        for key, s in json.loads(report.sidecar.read_text())["numbers"].items():
            seen[key].add(s)
    assert {k: v for k, v in seen.items() if len(v) > 1} == {}
