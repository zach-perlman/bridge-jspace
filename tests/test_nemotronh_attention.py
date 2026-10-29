"""Batch 52 C (Lightning, key row 10): the NemotronH port of the attention tools, on a tiny random NemotronH built from
transformers' own classes (CPU, eager attention; MLP and attention blocks only, so no Mamba kernel is needed): layer
kinds from the config and from the blocks agree; x49_attn.capture_queries recomputes exactly the softmax attention the
model's own eager attention computes (no norm, no rotary: NoPE); zero_head zeroes one head's slice of o_proj's input."""

import pytest
import torch

transformers = pytest.importorskip("transformers")

from bridge_jspace.knockout import FULL, OTHER, attention_module, config_layer_kinds, layer_kind, layer_kinds  # noqa: E402
from scripts import x49_attn as A  # noqa: E402

KINDS = ["mlp", "full_attention", "mlp", "full_attention"]


def tiny():
    from transformers import NemotronHConfig, NemotronHForCausalLM

    cfg = NemotronHConfig(vocab_size=64, hidden_size=32, num_attention_heads=4, num_key_value_heads=2, head_dim=8,
                          intermediate_size=48, layers_block_type=list(KINDS), num_hidden_layers=len(KINDS),
                          attn_implementation="eager")  # fmt: skip
    torch.manual_seed(0)
    return NemotronHForCausalLM(cfg).eval()


def test_layer_kinds_from_config_and_blocks_agree():
    m = tiny()
    assert config_layer_kinds(m.config) == [OTHER, FULL, OTHER, FULL] == layer_kinds(m)
    blocks = m.model.layers
    assert [layer_kind(b) for b in blocks] == [OTHER, FULL, OTHER, FULL]
    assert attention_module(blocks[1]) is blocks[1].mixer
    with pytest.raises(AssertionError, match="not a softmax-attention block"):
        attention_module(blocks[0])


def test_capture_queries_matches_the_models_own_attention():
    m = tiny()
    ids = torch.randint(0, 64, (1, 9), generator=torch.Generator().manual_seed(1))
    q_pos = [4, 8]
    seen = {}

    def keep(la):
        def hook(_mod, _args, out):
            seen[la] = out[1].detach()  # eager attention returns (output, weights [b, heads, T, T])

        return hook

    handles = [m.model.layers[la].mixer.register_forward_hook(keep(la)) for la in (1, 3)]
    out: dict = {}
    try:
        with torch.no_grad(), A.capture_queries(m, [1, 3], q_pos, out):
            m(ids)
    finally:
        for h in handles:
            h.remove()
    for la in (1, 3):
        probs, scores = out[la]
        assert probs.shape == (4, len(q_pos), 9)
        assert torch.allclose(probs.float(), seen[la][0][:, q_pos].float(), atol=1e-5)
        assert torch.isinf(scores[:, 0, 5:]).all() and not torch.isinf(scores[:, 1]).any()  # causal at position 4


def test_zero_head_zeroes_one_heads_slice_of_o_proj_input():
    m = tiny()
    ids = torch.randint(0, 64, (1, 7), generator=torch.Generator().manual_seed(2))
    got = {}
    mixer = m.model.layers[3].mixer
    with torch.no_grad(), A.zero_head(m, 3, head=2, positions=[5, 6]):
        # registered after zero_head's own pre-hook, so it sees o_proj's input as zero_head leaves it
        h = mixer.o_proj.register_forward_pre_hook(lambda _m, args: got.__setitem__("x", args[0].detach().clone()))
        try:
            m(ids)
        finally:
            h.remove()
    hd = mixer.head_dim
    x = got["x"][0]
    assert (x[[5, 6], 2 * hd : 3 * hd] == 0).all() and x[[5, 6], : 2 * hd].abs().sum() > 0
    assert x[:5, 2 * hd : 3 * hd].abs().sum() > 0  # other positions untouched


def test_lightning_attention_is_a_coverage_run():
    """Batch 52: 49.7 on Lightning is a coverage run (verdict --coverage), outside 49.7's RUNS."""
    lt = "nemotron-3.5-lightning"
    assert lt not in A.RUNS and A.COVERAGE_RUNS[lt].startswith("nem35l_") and A.SCORED.startswith("results/x49_attn/")


def test_lightning_heads_read_lightnings_own_49_7_run():
    """Batch 52: 51.2 on Lightning reads its 49.7 coverage run (attention.npz, items, halves), outside 51.2's RUNS."""
    from scripts import x51_heads as HD

    lt = "nemotron-3.5-lightning"
    assert lt not in HD.RUNS and HD.COVERAGE_RUNS[lt].startswith("nem35l_") and HD.SOURCE[lt] == A.COVERAGE_RUNS[lt]
