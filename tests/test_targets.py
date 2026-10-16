"""Part B's target switch (pins.TARGETS): the default stays Qwen3.6-27B with its pins, paths and tokenization."""

import pytest

from bridge_jspace import pins, tokens


def test_default_target_is_qwen_with_its_pins():
    assert pins.TARGET == "qwen3.6-27b"
    assert (pins.MODEL_REPO, pins.MODEL_REVISION) == (pins.QWEN_REPO, pins.QWEN_REVISION)
    assert pins.CACHE_DIR == pins.REPO_ROOT / "cache"
    assert pins.RUN_PREFIX == ""
    assert pins.LENS_SOURCES["jpp"] == (pins.LENS_REPO, pins.JPP_FILE, pins.LENS_REVISION)


def test_every_target_names_its_runs_and_layers():
    for name, t in pins.TARGETS.items():
        assert t["norm_gain"] in ("one_plus_weight", "weight") and t["n_layers"] > 0
        assert (t["run_prefix"] == "") == (name == "qwen3.6-27b")


def test_raw_encoding_is_plain_tokenization_on_qwen():
    try:
        tok = tokens.load_tokenizer()
    except Exception:  # the snapshot is not cached on this machine
        pytest.skip("Qwen3.6-27B tokenizer not cached")
    text = "The capital of the country where Lyon is located is"
    enc = tokens.raw_encoding(tok, text, offsets=True)
    ref = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    assert enc["input_ids"] == ref.input_ids
    assert enc["offset_mapping"] == [tuple(o) for o in ref.offset_mapping]
