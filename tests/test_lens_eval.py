"""scripts/lens_fit/lens_eval.py: lens specs, one evaluate call per layer set (the logit lens at the union), and the
metadata it reads from both lens layouts (CPU, tiny synthetic lenses)."""

import pytest
import torch

from scripts.lens_fit import lens_eval as le

SHA = "a" * 64
REV = "e166deb5ad540932100ef803c8c9bcc2a5453694"


def test_parse_spec_hub_and_local():
    s = le.parse_spec(f"hf:neuronpedia/jacobian-lens@{REV}:qwen3-32b/jlens/x/Qwen3-32B_jacobian_lens.pt#{SHA}")
    assert (s.repo, s.revision, s.path, s.sha256) == (
        "neuronpedia/jacobian-lens",
        REV,
        "qwen3-32b/jlens/x/Qwen3-32B_jacobian_lens.pt",
        SHA,
    )
    assert le.parse_spec("/ephemeral/a/pooled_lens.pt") == le.LensSpec(path="/ephemeral/a/pooled_lens.pt")
    with pytest.raises(ValueError, match="40-char"):
        le.parse_spec("hf:repo@main:file.pt")  # a branch is not a pin
    with pytest.raises(ValueError, match="sha256"):
        le.parse_spec("/a.pt#abc")


def test_plan_groups_puts_the_logit_lens_at_the_union():
    every3, every = list(range(0, 31, 3)), list(range(31))
    groups = le.plan_groups({"olmo-3-7b-instruct": every3, "Olmo-3-1025-7B_jacobian_lens": every})
    assert groups == [(every, ["Olmo-3-1025-7B_jacobian_lens", "logit"]), (every3, ["olmo-3-7b-instruct"])]
    # no lens at the union: the logit lens gets its own call
    assert le.plan_groups({"a": [0, 1], "b": [5]}) == [([0, 1, 5], ["logit"]), ([0, 1], ["a"]), ([5], ["b"])]
    assert le.plan_groups({"a": [2, 1, 1]}) == [([1, 2], ["a", "logit"])]
    with pytest.raises(ValueError):
        le.plan_groups({})


def test_lens_meta_reads_both_layouts(tmp_path):
    d = 4
    exported = {"J": {0: torch.eye(d).half(), 3: torch.eye(d).half()}, "source_layers": [3, 0], "d_model": d,
                "n_prompts": 64}  # fmt: skip
    torch.save(exported, tmp_path / "exported.pt")
    assert le.lens_meta(tmp_path / "exported.pt") == {"format": "J", "source_layers": [0, 3], "d_model": d,
                                                      "n_prompts": 64}  # fmt: skip
    recipe = {"parameters": {"jacobians": {5: torch.eye(d)}}, "source_layers": [5],
              "config": {"d_model": d, "num_prompts_trained_on": 32}}  # fmt: skip
    torch.save(recipe, tmp_path / "recipe.pt")
    assert le.lens_meta(tmp_path / "recipe.pt") == {"format": "recipe", "source_layers": [5], "d_model": d,
                                                    "n_prompts": 32}  # fmt: skip
    assert le.sha256_of(tmp_path / "recipe.pt") == le.sha256_of(tmp_path / "recipe.pt")
