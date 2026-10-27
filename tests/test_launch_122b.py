"""scripts/remote/launch_122b.py's GPU check: the 122B in FP8 (~125 GB) needs 135 GiB in total over the box's GPUs (one
H200, or 2x H100 80 GB with the model split over them), never on one 80 GB card."""

from scripts.remote import launch_122b as L


def test_two_h100s_pass_on_their_total_and_one_does_not():
    assert L.gpu_problems([79.6, 79.6], [9.0, 9.0]) == []  # 2x H100 PCIe 80 GB: 159.2 GiB in total
    assert L.gpu_problems([139.8], [9.0]) == []  # one H200
    assert L.gpu_problems([79.6], [9.0]) == ["the GPUs have 79.6 GiB in total (1 x 79.6) < 135"]
    assert L.gpu_problems([79.2, 79.2], [8.0, 8.0]) == ["compute capability 8.0 < 8.9: no native FP8"]  # 2x A100
    assert L.gpu_problems([], []) == ["no GPU"]


def test_several_gpus_split_the_model():
    assert "BJ_DEVICE_MAP" not in L.box_env("/w")
    assert L.box_env("/w", 2)["BJ_DEVICE_MAP"] == "auto" and L.box_env("/w", 2)["HF_HOME"] == "/w/hf"
