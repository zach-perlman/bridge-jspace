import yaml

from bridge_jspace import pins


def test_pins_agree_with_27b_yaml():
    """Part B reads pins.py, part A reads the YAML: the two must name the same model and J-lens."""
    m = yaml.safe_load((pins.REPO_ROOT / "configs/models/qwen3.6-27b.yaml").read_text())
    assert (m["name"], m["revision"]) == (pins.QWEN_REPO, pins.QWEN_REVISION)
    jlens = m["lenses"]["jlens"]
    assert (jlens.get("repo", "neuronpedia/jacobian-lens"), jlens["revision"], jlens["filename"]) == (
        pins.LENS_REPO,
        pins.LENS_REVISION,
        pins.LENS_FILE,
    )
    jpp = m["lenses"]["jpp"]
    assert (jpp["revision"], jpp["filename"]) == (pins.LENS_REVISION, pins.JPP_FILE)


def test_olmo_hybrid_pins_agree_with_yaml_and_have_no_lens():
    """The lens-free target: pins and its YAML name the same checkpoint; no lens source and no lens layer, so a lens
    stage refuses it up front (check_lens_layers) instead of loading another model's lens."""
    m = yaml.safe_load((pins.REPO_ROOT / "configs/models/olmo-hybrid-7b-instruct-dpo.yaml").read_text())
    t = pins.TARGETS["olmo-hybrid-7b-instruct-dpo"]
    assert (m["name"], m["revision"], m["n_layers"]) == (t["repo"], t["revision"], t["n_layers"])
    assert m["lenses"] == t["lenses"] == {} and t["lens_layers"] == []
    assert t["run_prefix"] == "olmo_hybrid_7b_"
