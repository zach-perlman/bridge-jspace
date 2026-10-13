import json

import pytest

from bridge_jspace.config import ExperimentConfig, ModelConfig
from bridge_jspace.experiment import Experiment
from bridge_jspace.pins import LENS_EVAL_MULTIHOP_SHA256, lens_eval_multihop_items, load_pinned_items, probe_swap_items
from bridge_jspace.utils import git_state


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


def test_git_dirty_ignores_results_only(tmp_path, monkeypatch):
    import subprocess

    def git(*args):
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    git("init", "-q")
    (tmp_path / "a.py").write_text("x = 1\n")
    git("add", "a.py")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "results" / "exp10_x" / "run").mkdir(parents=True)
    (tmp_path / "results" / "exp10_x" / "run" / "summary.json").write_text("{}")
    assert git_state()["dirty"] is False  # an earlier run's output must not mark the next run dirty
    (tmp_path / "a.py").write_text("x = 2\n")
    assert git_state()["dirty"] is True


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
