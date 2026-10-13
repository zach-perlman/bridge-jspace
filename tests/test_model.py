"""Integration on Qwen3.5-0.8B (same qwen3_5 hybrid architecture as Qwen3.6-27B) + its pinned lenses.

`make test-model` (CPU ok). Downloads ~1.7 GB of weights and ~90 MB of lenses on first run.
"""

import pytest
import torch

from bridge_jspace.config import load_config
from bridge_jspace.models import load_lens, load_model
from bridge_jspace.readout import rank_grid, residuals, word_tokens
from bridge_jspace.sanity import check_hf_parity, check_known_fact, check_reference_readout

pytestmark = pytest.mark.model


@pytest.fixture(scope="module")
def setup():
    overrides = ["model=configs/models/qwen3.5-0.8b.yaml"]
    if torch.cuda.is_available():
        # With flash-linear-attention installed (Linux), transformers runs its triton kernels even for
        # a CPU model, which fails; the torch fallback is only used when fla is absent (macOS).
        overrides.append("model.device_map=cuda")
    cfg = load_config("experiments/exp10_lens_sanity/config.yaml", overrides)
    m = load_model(cfg.model)
    lenses = {n: load_lens(lc, m.lm.n_layers, m.lm.d_model, m.device) for n, lc in cfg.model.lenses.items()}
    return m, lenses


def test_loads_text_decoder(setup):
    m, lenses = setup
    assert type(m.hf).__name__ == "Qwen3_5ForCausalLM"
    assert m.lm.n_layers == 24
    assert set(lenses) == {"jlens", "jpp"}
    for lens in lenses.values():
        assert lens.source_layers == list(range(23))


def test_sanity_checks_pass(setup):
    m, lenses = setup
    assert check_known_fact(m, "Fact: The capital of France is", " Paris")["passed"]
    assert check_hf_parity(m, ["Fact: The currency used in the country shaped like a boot is"], atol=1e-2)["passed"]
    for lens in lenses.values():
        assert check_reference_readout(m, lens, "Fact: The capital of France is")["passed"]


@pytest.mark.parametrize("reader", ["jlens", "jpp"])
def test_lens_reads_answer_type_in_late_layers(setup, reader):
    """Guards against garbage readouts. Measured on 0.8B: " currency" is top-1 at the last token from
    layer 16 (J-lens) / 19 (J++) on. The bridge "Italy" is NOT read there (min rank 819 / 1872), so the
    bridge itself is not a usable unit-test target on this model.
    """
    m, lenses = setup
    lens = lenses[reader]
    ids = m.lm.encode("Fact: The currency used in the country shaped like a boot is")
    resid = residuals(m.lm, ids, lens.source_layers)
    w = word_tokens(m.tokenizer, "currency")
    grid = rank_grid(m.lm, lens, resid, lens.source_layers, w.ids, positions=[-1])[:, 0].min(-1).values
    assert int(grid[-4:].max()) <= 2  # last 4 fitted layers
    assert int(grid[:4].min()) > 1000  # early layers do not read it: the readout is layer-dependent
