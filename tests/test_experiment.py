import json

import pytest

from bridge_jspace.config import ExperimentConfig, ModelConfig
from bridge_jspace.experiment import Experiment
from bridge_jspace.pins import LENS_EVAL_MULTIHOP_SHA256, lens_eval_multihop_items, load_pinned_items, probe_swap_items


class _Probe(Experiment):
    seen_manifest: dict | None = None

    def run(self):
        _Probe.seen_manifest = json.loads(self.path("manifest.json").read_text())
        return {"x": 1}


def _cfg(tmp_path) -> ExperimentConfig:
    return ExperimentConfig(
        name="exp99_probe", target="t:T", results_dir=str(tmp_path), model=ModelConfig(name="org/m", revision="r")
    )


def test_manifest_written_before_run(tmp_path):
    exp = _Probe(_cfg(tmp_path), run_dir=tmp_path / "run")
    assert exp.execute() == {"x": 1}
    m = _Probe.seen_manifest
    assert m is not None
    assert m["exp_id"] == "exp99_probe"
    assert m["config"]["model"]["revision"] == "r"
    assert {"sha", "dirty"} <= set(m["git"])
    assert "torch" in m["packages"]
    assert json.loads((tmp_path / "run" / "summary.json").read_text()) == {"x": 1}


def test_existing_run_dir_is_never_overwritten(tmp_path):
    (tmp_path / "run").mkdir()
    with pytest.raises(FileExistsError):
        _Probe(_cfg(tmp_path), run_dir=tmp_path / "run").execute()


def test_pinned_data_loads():
    assert len(probe_swap_items()) == 90
    items = lens_eval_multihop_items()
    assert len(items) == 93
    assert all(it["intermediates"] for it in items)


def test_pin_mismatch_raises(tmp_path):
    p = tmp_path / "x.json"
    p.write_text('{"items": []}')
    with pytest.raises(ValueError, match="sha256"):
        load_pinned_items(p, LENS_EVAL_MULTIHOP_SHA256)
