"""The README and depth sets on styles-plot (figkit/readme_sp.py, depth_sp.py): every figure saves strict for the
readme target, one data key prints one string across them and the write-up, and every README alias has its rows in the
registry under the README's id."""

from __future__ import annotations

import csv
import json
from collections import defaultdict

import pytest
import styles_plot as sp

from bridge_jspace.figkit import readme_sp as RS
from scripts import convert_status_registry as CR

SETS = {**RS.FIGS}
try:  # batch B
    from bridge_jspace.figkit import depth_sp as DS

    SETS.update(DS.FIGS)
except ImportError:  # pragma: no cover - before the depth set exists
    pass


@pytest.fixture(scope="module")
def saved(tmp_path_factory):
    out = tmp_path_factory.mktemp("readme_sp")
    return {fid: sp.save(f(), out / f"{fid}.png", target=RS.TARGET) for fid, f in SETS.items()}


def test_every_figure_saves_strict(saved):
    for fid, report in saved.items():
        assert report.path.exists() and report.problems == [], fid


def test_one_data_key_prints_one_string_across_figures(saved):
    seen = defaultdict(set)
    for report in saved.values():
        for key, s in json.loads(report.sidecar.read_text())["numbers"].items():
            seen[key].add(s)
    assert {k: v for k, v in seen.items() if len(v) > 1} == {}


def test_an_alias_has_the_write_up_figures_cells():
    with CR.OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    cells = defaultdict(set)
    for r in rows:
        cells[r["figure"]].add(r["cell"])
    for fid, wid in RS.ALIAS.items():
        assert cells[fid] == cells[wid], fid
