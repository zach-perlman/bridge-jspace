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
