"""Every run's manifest records the env switches that change what the run does (run_switches.switches()): the target
key, BJ_DEVICE_MAP, BJ_SUITE_BATCH and the target's frozen lens sha256 (Dan, 27 Oct)."""

import ast
import json
import os
import subprocess
import sys

import pytest

from bridge_jspace import pins
from bridge_jspace.run_switches import switches

REPO = pins.REPO_ROOT
CODE = "import json; from bridge_jspace.run_switches import switches; print(json.dumps(switches()))"

# Manifest writers that record no switches, and why. A new writer either records "switches": switches() (directly or
# through a same-module helper that does) or is listed here.
LEFT_OUT = {
    **dict.fromkeys(
        [
            "scripts/ctxcomp.py:make",
            "scripts/jsuite_facts.py:make",
            "scripts/jsuite_numbers.py:make",
            "scripts/jsuite_threehop.py:main",
            "scripts/jsuite_v2.py:main",
            "scripts/jsuite_v2_1.py:main",
            "scripts/merge_tasks_sets.py:main",
            "scripts/mm_absent.py:main",
            "scripts/natctl.py:make",
            "scripts/natplus.py:make",
            "scripts/natural3.py:make",
            "scripts/natural_v1.py:make",
            "scripts/natural_v1.py:derive_prefill",
            "scripts/natural_v1.py:derive_qa",
            "scripts/tasks_v2.py:make",
            "scripts/exp19_fit_data/make_manifest.py:main",
            "scripts/exp19_fit_data/make_manifest64.py:main",
        ],
        "a data set's manifest, not a run's",
    ),
    "scripts/x0_composition.py:main": "CPU analysis of existing runs' outputs; no model",
    "scripts/xfig_depth_profile.py:build": "a figure's manifest; no model",
    "scripts/lens_fit/lens_eval.py:main": "the J++ recipe's evaluation: model, lenses and device map are its own "
    "arguments (recorded); it reads no BJ_ switch",
    "scripts/indep_check.py:run": "the independent re-implementation imports nothing from bridge_jspace; model, lens "
    "and device are its own arguments (recorded)",
}
# Writers of a dict their callers build with a helper that records the switches.
DELEGATES = {"scripts/statement_positions.py:write_manifest": "manifest_common"}


def run_with_target(target: str) -> dict:
    env = {**os.environ, "BJ_TARGET": target}
    for k in ("BJ_DEVICE_MAP", "BJ_SUITE_BATCH"):
        env.pop(k, None)
    out = subprocess.run([sys.executable, "-c", CODE], cwd=REPO, env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_unset_env_switches_are_none(monkeypatch):
    monkeypatch.delenv("BJ_DEVICE_MAP", raising=False)
    monkeypatch.delenv("BJ_SUITE_BATCH", raising=False)
    assert switches() == {"target": pins.TARGET, "BJ_DEVICE_MAP": None, "BJ_SUITE_BATCH": None,
                          "lens_sha256": pins.FROZEN_LENS_SHA256}  # fmt: skip


def test_set_env_switches_are_recorded_raw(monkeypatch):
    monkeypatch.setenv("BJ_DEVICE_MAP", "auto")
    monkeypatch.setenv("BJ_SUITE_BATCH", "32")
    assert (switches()["BJ_DEVICE_MAP"], switches()["BJ_SUITE_BATCH"]) == ("auto", "32")
    monkeypatch.setenv("BJ_DEVICE_MAP", "")  # set empty: no split (model.placement), told apart from unset
    assert switches()["BJ_DEVICE_MAP"] == ""


def test_the_switch_names_are_the_ones_the_code_reads():
    from bridge_jspace import model

    assert model.DEVICE_MAP_ENV == "BJ_DEVICE_MAP"
    assert '"BJ_SUITE_BATCH"' in (REPO / "scripts" / "suite_split.py").read_text()


def test_default_target_records_the_27b_jpp():
    sw = run_with_target("qwen3.6-27b")
    assert sw == {"target": "qwen3.6-27b", "BJ_DEVICE_MAP": None, "BJ_SUITE_BATCH": None,
                  "lens_sha256": "bbef480b41028e156c4aa3c334ad32d1b76a4017ef3a7245eecf776bf2b58f8f"}  # fmt: skip


def test_target_key_and_lens_follow_bj_target():
    sw = run_with_target("qwen3.5-9b")  # a Hub lens: its pinned sha256
    assert (sw["target"], sw["lens_sha256"]) == ("qwen3.5-9b", pins.TARGETS["qwen3.5-9b"]["frozen_lens_sha256"])
    sw = run_with_target("gemma-4-31b-it")  # a local lens without frozen_lens_sha256: the sha256 lens.py checks
    assert (sw["target"], sw["lens_sha256"]) == ("gemma-4-31b-it", pins.TARGETS["gemma-4-31b-it"]["lenses"]["jpp"][2])
    assert sw["lens_sha256"] != pins.FROZEN_LENS_SHA256


@pytest.mark.parametrize("target", ["olmo-hybrid-7b-instruct-dpo", "gpt-oss-20b-prefit"])
def test_a_lens_free_target_records_no_lens(target):
    assert pins.TARGETS[target]["lenses"] == {}
    assert run_with_target(target) == {"target": target, "BJ_DEVICE_MAP": None, "BJ_SUITE_BATCH": None,
                                       "lens_sha256": None}  # fmt: skip


def test_lens_free_in_process(monkeypatch):
    monkeypatch.setattr(pins, "LENS_SOURCES", {})
    assert switches()["lens_sha256"] is None


# ---- the writers ------------------------------------------------------------------------------------------------


def _is_manifest(node: ast.AST) -> bool:
    return any(isinstance(n, ast.Constant) and n.value == "manifest.json" for n in ast.walk(node))


def _calls(node: ast.AST) -> set[str]:
    return {n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}


def _writes_manifest(fn: ast.FunctionDef) -> bool:
    """A call writing a path that ends in manifest.json: write_text / save_json / json.dump / open(..., "w") on the
    literal, or on a name assigned from an expression holding it."""
    names = {t.id for n in ast.walk(fn) if isinstance(n, ast.Assign) and _is_manifest(n.value)
             for t in n.targets if isinstance(t, ast.Name)}  # fmt: skip

    def hit(x: ast.AST) -> bool:
        return _is_manifest(x) or (isinstance(x, ast.Name) and x.id in names)

    for n in ast.walk(fn):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        attr = f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else ""
        recv = [f.value] if isinstance(f, ast.Attribute) else []
        if attr in ("write_text", "save_json") and any(hit(x) for x in [*recv, *n.args]):
            return True
        if attr == "dump" and any(hit(x) for x in n.args[1:]):
            return True
        mode = [a.value for a in n.args[1:2] if isinstance(a, ast.Constant)]
        if attr == "open" and n.args and hit(n.args[0]) and mode and "w" in str(mode[0]):
            return True
    return False


def manifest_writers() -> dict[str, bool]:
    """file:function -> whether it records the switches (a switches() call in it or in a same-module function it
    calls), for every function in scripts/ and src/ that writes a manifest.json."""
    out = {}
    for path in sorted([*REPO.glob("scripts/**/*.py"), *REPO.glob("src/**/*.py")]):
        text = path.read_text()
        if "manifest.json" not in text:
            continue
        fns = [n for n in ast.walk(ast.parse(text)) if isinstance(n, ast.FunctionDef)]
        recording = {fn.name for fn in fns if "switches" in _calls(fn)}
        for fn in fns:
            if _writes_manifest(fn):
                out[f"{path.relative_to(REPO)}:{fn.name}"] = bool(_calls(fn) & ({"switches"} | recording))
    return out


def test_every_run_manifest_writer_records_the_switches():
    writers = manifest_writers()
    assert len(writers) > 100  # the scan finds the writers (117 when written)
    missing = [w for w, ok in writers.items() if not ok and w not in LEFT_OUT and w not in DELEGATES]
    assert not missing, f"manifest writers without 'switches': switches(): {missing}"
    stale = [w for w in [*LEFT_OUT, *DELEGATES] if w not in writers]
    assert not stale, f"no longer manifest writers: {stale}"


def test_delegate_writers_callers_record_the_switches():
    for writer, helper in DELEGATES.items():
        file, fn = writer.split(":")
        fns = {n.name: n for n in ast.walk(ast.parse((REPO / file).read_text())) if isinstance(n, ast.FunctionDef)}
        assert "switches" in _calls(fns[helper])
        callers = [n for n in fns.values() if fn in _calls(n)]
        assert callers and all(helper in _calls(n) for n in callers), f"{writer}: a caller skips {helper}"


class Stop(Exception):
    """Raised by a fake load_model: the manifest is written, the run itself is not wanted."""


def test_written_manifests_record_the_switches(monkeypatch, tmp_path):
    """Two scripts' manifests and part A's (Experiment.setup), written for real (no model), with the switches set."""
    from bridge_jspace import model as model_module
    from bridge_jspace.config import ExperimentConfig, ModelConfig
    from bridge_jspace.experiment import Experiment
    from scripts import ablate_pilot as A
    from scripts import read_write as RW
    from scripts import suite_v1 as S

    def stop():
        raise Stop

    monkeypatch.setenv("BJ_DEVICE_MAP", "auto")
    monkeypatch.setenv("BJ_SUITE_BATCH", "16")
    want = {"target": pins.TARGET, "BJ_DEVICE_MAP": "auto", "BJ_SUITE_BATCH": "16",
            "lens_sha256": switches()["lens_sha256"]}  # fmt: skip
    monkeypatch.setattr(model_module, "load_model", stop)
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(S, "RESULTS", tmp_path / "suite_v1")
    (tmp_path / "suite_v1" / "comp").mkdir(parents=True)
    (tmp_path / "suite_v1" / "comp" / "items.jsonl").write_text(json.dumps({"id": "BL-0000", "correct": True}) + "\n")
    for module, kwargs in ((RW, {"comp_run": "comp"}), (A, {"comp_main": "comp", "comp_computed": None})):
        monkeypatch.setattr(module, "RESULTS", tmp_path / module.__name__)
        with pytest.raises(Stop):
            module.main("switches_test", "test", 1, **kwargs)
        m = json.loads((tmp_path / module.__name__ / "switches_test" / "manifest.json").read_text())
        assert m["switches"] == want

    class Probe(Experiment):
        def run(self):
            return None

    cfg = ExperimentConfig(name="exp99_probe", target="t:T", results_dir=str(tmp_path),
                           model=ModelConfig(name="org/m", revision="r"))  # fmt: skip
    Probe(cfg, run_dir=tmp_path / "part_a").execute()
    assert json.loads((tmp_path / "part_a" / "manifest.json").read_text())["switches"] == want
