"""The write-up's styles-plot figures (figkit/writeup_sp.py): the vocabulary's models and templates, the status registry
(written in styles-plot's schema, current, loadable), every figure saves strict, and one data key prints one string
across them."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import pytest
import styles_plot as sp

from bridge_jspace import figdata as FD
from bridge_jspace import palette as P
from bridge_jspace.figkit import writeup_sp as SP
from scripts import status_registry as SR

REPO = Path(__file__).resolve().parents[1]
V = sp.load(REPO / "plotstyle.toml")


def test_models_in_order():
    assert [(e.key, e.name) for e in V.entities("models")][: len(P.MODELS)] == list(P.MODELS)
    assert [e.name for e in V.entities("models")][len(P.MODELS) :] == list(P.BREADTH_ONLY)


def test_read_aloud_matches_a_template():
    s = FD.READ_ALOUD.format(model="Qwen 27B", recall="53.5", lookup="2.6", gap="50.9", ctrl="12.4")
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
    row = SR.convert({"figure": "f", "cell": "c", "reason": "r", "source": "s", **old})
    assert (row["timing"], row["claim"], row["claim_reason"]) == want


def test_registry_is_current_and_loads():
    want = [SR.convert(r) for r in SR.rows()]
    with SR.OUT.open(newline="") as f:
        assert list(csv.DictReader(f)) == want
    assert V.registry_path == SR.OUT
    assert len(sp.load_registry(SR.OUT)) == len(want)


# ---- the figures -----------------------------------------------------------------------------------------------------
BUILT = list(SP.FIGS)


@pytest.fixture(scope="module")
def saved(tmp_path_factory):
    out = tmp_path_factory.mktemp("sp")
    return {fid: sp.save(SP.FIGS[fid](), out / f"{fid}.png", target="post", root=out) for fid in BUILT}


def test_every_figure_saves_strict(saved):
    for fid, report in saved.items():
        assert report.path.exists() and report.problems == [], fid


def test_one_data_key_prints_one_string_across_figures(saved):
    seen = defaultdict(set)
    for report in saved.values():
        for key, s in json.loads(report.sidecar.read_text())["numbers"].items():
            seen[key].add(s)
    assert {k: v for k, v in seen.items() if len(v) > 1} == {}
