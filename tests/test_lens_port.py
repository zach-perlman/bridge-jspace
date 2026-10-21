"""The lens stages (read_write, ablate_pilot, suite_split's map and parts) take the target's frozen lens and its lens
layers from pins: Qwen keeps J++ at every layer it used, OLMo uses its J-lens at layers 0, 3, ..., 30 only; a lens stage
refuses a layer without a map before it writes anything, and its manifest records the lens and its layers (no model)."""

import json
import os
import subprocess
import sys

import pytest

from bridge_jspace import pins
from scripts import ablate_pilot as A
from scripts import read_write as RW
from scripts import suite_split as P
from scripts import suite_v1 as S

OLMO_LENS_LAYERS = list(range(0, 31, 3))


class Stop(Exception):
    """Raised by a fake load_model: the manifest is written, the run itself is not wanted."""


def test_default_target_keeps_jpp_and_its_grids():
    assert pins.FROZEN_LENS == "jpp" and pins.LENS_LAYERS is None
    assert pins.on_lens((32, 36, 40)) == (32, 36, 40)
    pins.check_lens_layers((32, 36, 40))
    assert tuple(range(0, 61, 4)) == P.MAP_LAYERS  # Qwen3.6-27B's map grid, as before the port
    assert (RW.LAYERS, A.LAYERS) == ((32, 36, 40), (32, 36, 40))


def test_every_target_has_its_frozen_lens_and_valid_lens_layers():
    for name, t in pins.TARGETS.items():
        if not t["lenses"]:  # pinned for lens-free runs only (qwen3-32b until Zach's J++ fit is pinned)
            continue
        assert t.get("frozen_lens", "jpp") in t["lenses"], name
        layers = t.get("lens_layers")
        if layers is not None:  # J_l maps a block output to the final block's: source layers 0..n_layers - 2
            assert layers == sorted(set(layers)) and layers[0] >= 0 and layers[-1] <= t["n_layers"] - 2, name


@pytest.mark.parametrize("target", ["olmo-3-7b-base", "olmo-3-7b-instruct"])
def test_olmo_target_uses_its_jlens_at_its_lens_layers(target):
    code = (
        "import json; from bridge_jspace import pins; from scripts import suite_split as P\n"
        "try:\n    pins.check_lens_layers((15, 32)); refused = False\nexcept AssertionError:\n    refused = True\n"
        "print(json.dumps([pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256, pins.LENS_LAYERS, list(P.MAP_LAYERS), refused]))"
    )
    env = {**os.environ, "BJ_TARGET": target}
    env.pop("BJ_FORMAT", None)
    out = subprocess.run([sys.executable, "-c", code], cwd=pins.REPO_ROOT, env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    key, sha, layers, map_layers, refused = json.loads(out.stdout.strip().splitlines()[-1])
    assert key == "jlens" and sha == pins.TARGETS[target]["frozen_lens_sha256"]
    assert layers == OLMO_LENS_LAYERS
    assert map_layers == list(range(0, 28, 3))  # lens layers below the last three blocks (29-31)
    assert refused


def test_parts_window_keeps_only_lens_layers(monkeypatch):
    summary = {"answer_formed": {"BL": 24}, "windows": {"BL": {"question": [14, 15, 16, 18, 21, 24, 27]},
                                                        "RR": {"question": [12, 13]}}}  # fmt: skip
    cap, window = P.parts_window(summary, ["BL", "RR", "RL"])
    assert window == {"BL": [14, 15, 16, 18, 21], "RR": [12, 13], "RL": []}  # default target: below the cap only
    monkeypatch.setattr(pins, "LENS_LAYERS", OLMO_LENS_LAYERS)
    cap, window = P.parts_window(summary, ["BL", "RR", "RL"])
    assert cap == {"BL": 24, "RR": P.ANSWER_ONSET, "RL": P.ANSWER_ONSET}
    assert window == {"BL": [15, 18, 21], "RR": [12], "RL": []}
    assert P.parts_window(summary, ["BL"], cap_override=19)[1] == {"BL": [15, 18]}


@pytest.mark.parametrize("module", [RW, A])
def test_lens_stage_refuses_layers_without_a_map(module, monkeypatch, tmp_path):
    monkeypatch.setattr(pins, "LENS_LAYERS", OLMO_LENS_LAYERS)
    monkeypatch.setattr(module, "RESULTS", tmp_path)
    monkeypatch.setattr(module, "LAYERS", (32, 36, 40))  # the 27B's default window: no map on OLMo
    with pytest.raises(AssertionError, match="have no jpp map"):
        module.main("lens_port_test", "test", 1)
    assert not (tmp_path / "lens_port_test").exists()


def fake_competence(root, run: str) -> None:
    (root / "suite_v1" / run).mkdir(parents=True)
    (root / "suite_v1" / run / "items.jsonl").write_text(json.dumps({"id": "BL-0000", "correct": True}) + "\n")


def test_lens_stage_manifests_record_the_lens_and_its_layers(monkeypatch, tmp_path):
    from bridge_jspace import model as model_module

    def stop():
        raise Stop

    monkeypatch.setattr(model_module, "load_model", stop)
    monkeypatch.setattr(pins, "LENS_LAYERS", OLMO_LENS_LAYERS)
    monkeypatch.setattr(pins, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(S, "RESULTS", tmp_path / "suite_v1")
    fake_competence(tmp_path, "comp")
    for module, kwargs in ((RW, {"comp_run": "comp"}), (A, {"comp_main": "comp", "comp_computed": None})):
        monkeypatch.setattr(module, "RESULTS", tmp_path / module.__name__)
        monkeypatch.setattr(module, "LAYERS", (15, 18, 21))
        with pytest.raises(Stop):
            module.main("lens_port_test", "test", 1, **kwargs)
        m = json.loads((tmp_path / module.__name__ / "lens_port_test" / "manifest.json").read_text())
        assert m["lens"] == [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256]
        assert m["lens_layers"] == OLMO_LENS_LAYERS and m["layers"] == [15, 18, 21]
