import pytest
import yaml

from bridge_jspace.config import load_config

LENS = {"jlens": {"revision": "abc", "filename": "m/jlens.pt"}}


@pytest.fixture
def cfg_path(tmp_path):
    (tmp_path / "m.yaml").write_text(
        yaml.safe_dump({"name": "org/model", "revision": "r1", "dtype": "float32", "lenses": LENS})
    )
    (tmp_path / "m2.yaml").write_text(yaml.safe_dump({"name": "org/other", "revision": "r2"}))
    p = tmp_path / "c.yaml"
    p.write_text(yaml.safe_dump({"name": "exp10_x", "target": "a:B", "model": "m.yaml", "params": {"k": 1}}))
    return p


def test_model_path_relative_to_config(cfg_path):
    cfg = load_config(cfg_path)
    assert cfg.model.name == "org/model"
    assert cfg.model.lenses["jlens"].repo == "neuronpedia/jacobian-lens"
    assert cfg.model.lenses["jlens"].filename == "m/jlens.pt"


def test_overrides_parse_yaml_values(cfg_path):
    cfg = load_config(cfg_path, ["params.k=3", "params.new.deep=[1, 2]", "seed=7"])
    assert cfg.params == {"k": 3, "new": {"deep": [1, 2]}}
    assert cfg.seed == 7


def test_model_swap_then_field_override(cfg_path):
    cfg = load_config(cfg_path, ["model.dtype=bfloat16", f"model={cfg_path.parent / 'm2.yaml'}"])
    assert cfg.model.name == "org/other"
    assert cfg.model.dtype == "bfloat16"
    assert cfg.model.lenses == {}


def test_unknown_field_rejected(cfg_path):
    with pytest.raises(ValueError):
        load_config(cfg_path, ["model.revison=x"])  # typo for revision


def test_model_revision_required(tmp_path):
    (tmp_path / "m.yaml").write_text(yaml.safe_dump({"name": "org/model"}))
    p = tmp_path / "c.yaml"
    p.write_text(yaml.safe_dump({"name": "exp10_x", "target": "a:B", "model": "m.yaml"}))
    with pytest.raises(ValueError):
        load_config(p)


@pytest.mark.parametrize("bad", ["lens_sanity", "exp1_x", "exp10-x", "exp10_X"])
def test_experiment_id_format(cfg_path, bad):
    with pytest.raises(ValueError):
        load_config(cfg_path, [f"name={bad}"])


def test_bad_override_format(cfg_path):
    with pytest.raises(ValueError):
        load_config(cfg_path, ["params.k"])


def test_shipped_configs_load():
    cfg = load_config("scripts/exp10_lens_sanity/config.yaml")
    assert cfg.model.name == "Qwen/Qwen3.5-4B"
    cfg = load_config("scripts/exp10_lens_sanity/config.yaml", ["model=configs/models/qwen3.6-27b.yaml"])
    assert set(cfg.model.lenses) == {"jlens", "jpp"}
