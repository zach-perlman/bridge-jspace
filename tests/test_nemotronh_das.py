"""Batch 52 (Lightning ports, Dan's 08:55 queue item 3): x48_das's torch path for NemotronH's Mamba-2 (BJ_DAS_MAMBA=torch)
on a tiny random NemotronH built from transformers' own classes (Mamba-2, MoE and attention blocks; CPU, float64, no
kernel installed, so every Mamba-2 function is transformers' torch reference). Checked: kernels_off undoes a
kernelize-style forward swap (kernels.layer._replace_forward: an instance `forward`) and puts it back; with the switch
the DAS forward takes the torch reference only while a gradient is recorded; the DAS edit's gradient through the torch
path matches finite differences; right padding leaves a row's read unchanged; train_subspace runs through it."""

import types
from typing import Any

import pytest
import torch

transformers = pytest.importorskip("transformers")

from scripts import x48_das as D  # noqa: E402

KINDS = ["mamba", "moe", "attention", "mamba", "moe", "mamba"]
V, H = 64, 32


def tiny(dtype=torch.float64, experts: str = "eager"):
    """float64 needs the eager experts loop (torch._grouped_mm, Lightning's default on the GPU, has no float64)."""
    from transformers import NemotronHConfig, NemotronHForCausalLM

    kw: dict[str, Any] = dict(vocab_size=V, hidden_size=H, num_attention_heads=4, num_key_value_heads=2, head_dim=8,
                              intermediate_size=48, layers_block_type=list(KINDS), num_hidden_layers=len(KINDS),
                              mamba_num_heads=4, mamba_head_dim=16, n_groups=2, ssm_state_size=8, chunk_size=8,
                              n_routed_experts=4, num_experts_per_tok=2, moe_intermediate_size=16,
                              moe_shared_expert_intermediate_size=24, n_group=1, topk_group=1,
                              attn_implementation="eager", experts_implementation=experts)  # fmt: skip
    torch.manual_seed(0)
    m: Any = NemotronHForCausalLM(NemotronHConfig(**kw))
    m = m.to(dtype).eval()
    for p in m.parameters():
        p.requires_grad_(False)
    return m


def wrap(m):
    """The attributes of bridge_jspace.model.Model that batch_logits and train_subspace read."""
    return types.SimpleNamespace(hf=m, layers=m.model.layers, device=torch.device("cpu"),
                                 tokenizer=types.SimpleNamespace(pad_token_id=0, eos_token_id=0))  # fmt: skip


@pytest.fixture
def swapped():
    """A tiny NemotronH whose kernel functions and kernel layers carry a kernelize-style instance forward that counts
    its calls and runs the class's own forward (the torch reference), as a stand-in for an HF-hub kernel. The Func
    objects are module-level singletons of transformers' NemotronH, so the swap is undone after the test."""
    m = tiny()
    calls = {"n": 0}

    def kernel(self, *args, **kwargs):
        calls["n"] += 1
        return type(self).forward(self, *args, **kwargs)

    objs = D.kernelized(m)
    for o in objs:
        o.forward = types.MethodType(kernel, o)
    try:
        yield m, objs, calls
    finally:
        for o in objs:
            vars(o).pop("forward", None)


def ids_of(n: int, seed: int) -> list[int]:
    return torch.randint(1, V, (n,), generator=torch.Generator().manual_seed(seed)).tolist()


def test_kernelized_finds_the_mamba_functions_and_the_norms():
    m = tiny()
    names = {type(o).kernel_layer_name for o in D.kernelized(m)}
    assert {"causal_conv1d_fn", "mamba_chunk_scan_combined", "RMSNorm", "rotary_pos_emb"} <= names
    with D.kernels_off(m) as refs:
        pass
    assert "transformers.models.nemotron_h.modeling_nemotron_h.mamba2_chunk_scan" in refs
    assert "transformers.models.nemotron_h.modeling_nemotron_h.causal_conv1d_fn" in refs


def test_kernels_off_runs_the_torch_reference_and_puts_the_kernels_back(swapped):
    m, objs, calls = swapped
    ids = torch.tensor([ids_of(11, 1)])
    with torch.no_grad():
        ref = m(ids).logits
        assert calls["n"] > 0
        calls["n"] = 0
        with D.kernels_off(m):
            out = m(ids).logits
        assert calls["n"] == 0 and torch.equal(out, ref)
        m(ids)
    assert calls["n"] > 0 and all("forward" in vars(o) for o in objs)


def test_kernels_off_refuses_a_fallback_that_is_not_torch():
    """A kernel function whose fallback resolved to an installed package (mamba_ssm) is not the torch reference."""
    from transformers.integrations.hub_kernels import use_kernel_func_from_hub_with_fallback

    def chunk(x):
        return x

    # 'json' imports, so json.dumps stands in for an installed package's function
    fn = use_kernel_func_from_hub_with_fallback("dumps", "json")(chunk)
    with pytest.raises(AssertionError, match="not transformers' torch reference"):
        D.torch_reference_of(fn)


def test_das_forward_path_takes_the_torch_reference_only_with_a_gradient(swapped, monkeypatch):
    m, _, calls = swapped
    model = wrap(m)
    rows, pos = [ids_of(9, 2)], [4]
    adds = torch.zeros(1, H, dtype=torch.float64, requires_grad=True)
    monkeypatch.setenv(D.MAMBA_ENV, "torch")
    with torch.no_grad():
        D.batch_logits(model, 1, rows, pos, adds)
    assert calls["n"] > 0, "a read without a gradient keeps the (stand-in) kernels"
    calls["n"] = 0
    D.batch_logits(model, 1, rows, pos, adds).sum().backward()
    assert calls["n"] == 0, "a forward recording a gradient runs the torch reference"
    monkeypatch.delenv(D.MAMBA_ENV)
    D.batch_logits(model, 1, rows, pos, adds)
    assert calls["n"] > 0, "switch off: as loaded"


def test_torch_mamba_records_the_switch_and_refuses_a_model_without_mamba(monkeypatch):
    m = tiny()
    assert D.torch_mamba(m) is None
    monkeypatch.setenv(D.MAMBA_ENV, "torch")
    rec = D.torch_mamba(m)
    assert rec and "3 Mamba-2 mixers" in rec and "mamba2_chunk_scan" in rec
    with pytest.raises(AssertionError, match="no Mamba-2 mixer"):
        D.torch_mamba(torch.nn.Sequential(torch.nn.Linear(2, 2)))


def test_das_gradient_through_the_torch_path_matches_finite_differences(monkeypatch):
    """The DAS edit at a Mamba-2 block's output (L0) and at the MoE block's (L1): d(read logits) / d(adds) by autograd
    through the torch path equals central finite differences (float64 model; batch_logits casts the read to fp32, hence
    the tolerances, far below the size of a wrong gradient)."""
    monkeypatch.setenv(D.MAMBA_ENV, "torch")
    model = wrap(tiny())
    rows, pos = [ids_of(10, 3), ids_of(7, 4)], [5, 2]
    for layer in (0, 1):
        adds = (
            0.5 * torch.randn(2, H, dtype=torch.float64, generator=torch.Generator().manual_seed(5))
        ).requires_grad_()
        assert torch.autograd.gradcheck(lambda a, la=layer: D.batch_logits(model, la, rows, pos, a).double(), (adds,),
                                        eps=1e-3, atol=1e-3, rtol=1e-2)  # fmt: skip


def test_grouped_mm_experts_give_the_eager_gradient(monkeypatch):
    """Lightning's MoE runs transformers' default experts implementation (torch._grouped_mm); in float32 its DAS
    gradient through the torch path equals the eager experts loop's."""
    monkeypatch.setenv(D.MAMBA_ENV, "torch")
    rows, pos = [ids_of(10, 3), ids_of(7, 4)], [5, 2]
    tgt = torch.tensor([3, 17])
    grads = {}
    for experts in ("grouped_mm", "eager"):
        m = tiny(torch.float32, experts)
        assert m.config._experts_implementation == experts
        adds = (0.5 * torch.randn(2, H, generator=torch.Generator().manual_seed(5))).requires_grad_()
        torch.nn.functional.cross_entropy(D.batch_logits(wrap(m), 0, rows, pos, adds), tgt).backward()
        grads[experts] = adds.grad
    assert torch.allclose(grads["grouped_mm"], grads["eager"], rtol=1e-4, atol=1e-6)


def test_right_padding_leaves_each_rows_read_unchanged():
    """batch_logits right-pads a micro-batch; through the Mamba-2 blocks (conv1d and scan) a row's read equals its
    unpadded single-row read."""
    model = wrap(tiny())
    rows, pos = [ids_of(12, 6), ids_of(5, 7)], [6, 3]
    adds = torch.randn(2, H, dtype=torch.float64, generator=torch.Generator().manual_seed(8))
    with torch.no_grad():
        both = D.batch_logits(model, 0, rows, pos, adds)
        one = torch.cat([D.batch_logits(model, 0, [r], [p], a[None]) for r, p, a in zip(rows, pos, adds, strict=True)])
    assert torch.allclose(both, one, atol=1e-5)


def test_train_subspace_runs_through_the_torch_path(swapped, monkeypatch):
    """48.1's training loop with the switch: every training forward on the torch reference, the loss finite and lower
    after training, R orthonormal."""
    m, _, calls = swapped
    monkeypatch.setenv(D.MAMBA_ENV, "torch")
    model = wrap(m)
    g = torch.Generator().manual_seed(9)
    rows = [{"ids": ids_of(8 + i % 3, 10 + i), "pos": 3, "delta": torch.randn(H, generator=g), "target": i % V}
            for i in range(6)]  # fmt: skip
    log: list[dict] = []
    r = D.train_subspace(model, 0, rows, 4, seed=1, steps=26, batch=4, micro=2, lr=1e-2, log=log)
    assert calls["n"] == 0, "no training forward on the (stand-in) kernels"
    assert all(torch.isfinite(torch.tensor(x["loss"])) for x in log) and log[-1]["loss"] < log[0]["loss"]
    assert torch.allclose(r.T @ r, torch.eye(4), atol=1e-4)
