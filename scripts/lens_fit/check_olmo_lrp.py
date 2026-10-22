"""check_olmo_lrp: the J++ fitter's LRP surgery on the Olmo pair (bridge-jspace, 2026-10-22; prereg amendment 6B).
For allenai/Olmo-Hybrid-Instruct-DPO-7B and allenai/Olmo-3-7B-Instruct-DPO: (1) on the real architecture (meta device,
no weights) the rlens rules patch every residual-stream norm and gated MLP and nothing inside attention or the
GatedDeltaNet, without raising; (2) on a tiny random decoder of the same class the patched forward equals the stock
forward (the rules change gradients only) and the gradients differ (the rules did something).
python -I scripts/lens_fit/check_olmo_lrp.py   (run with /workspace/ext/jpp_lens/.venv/bin/python)"""

import copy
import glob
import json
import sys

import torch
from transformers import AutoConfig, AutoModel, AutoModelForCausalLM

sys.path.insert(0, "/workspace/ext/jpp_lens/src")
from workspace_lens.lrp.lrp import apply_lrp_rules_for_mode  # noqa: E402

out = {}
for repo in ("allenai--Olmo-Hybrid-Instruct-DPO-7B", "allenai--Olmo-3-7B-Instruct-DPO"):
    cfg_path = glob.glob(f"/workspace/hf_cache/hub/models--{repo}/snapshots/*/config.json")[0]
    cfg = AutoConfig.from_pretrained(cfg_path.rsplit("/", 1)[0])
    with torch.device("meta"):
        full = AutoModelForCausalLM.from_config(cfg)
    with apply_lrp_rules_for_mode(full, "rlens") as rep:
        n = cfg.num_hidden_layers
        print(repo, "real architecture: ln_rule", len(rep.ln_rule), "mlp_rule", len(rep.mlp_rule))
        print("  e.g.", rep.ln_rule[:3], rep.mlp_rule[:1])
        assert len(rep.mlp_rule) == n, (len(rep.mlp_rule), n)
        assert len(rep.ln_rule) == 2 * n + 1, (len(rep.ln_rule), 2 * n + 1)  # two residual-stream norms per block + the final norm
        assert not any("linear_attn" in x or "self_attn" in x for x in rep.ln_rule + rep.mlp_rule), "attention / DeltaNet internals patched"
    tc = copy.deepcopy(cfg)
    tc.num_hidden_layers, tc.hidden_size, tc.intermediate_size, tc.vocab_size = 4, 64, 128, 512
    tc.pad_token_id = tc.bos_token_id = tc.eos_token_id = 0
    tc.num_attention_heads, tc.num_key_value_heads = 4, 4
    if hasattr(tc, "head_dim"):
        tc.head_dim = 16
    for k in ("linear_num_key_heads", "linear_num_value_heads"):
        if hasattr(tc, k):
            setattr(tc, k, 2)
    for k in ("linear_key_head_dim", "linear_value_head_dim"):
        if hasattr(tc, k):
            setattr(tc, k, 16)
    tc.layer_types = cfg.layer_types[:3] + [cfg.layer_types[3]]  # three linear / sliding layers and one full-attention layer
    if getattr(tc, "sliding_window", None):
        tc.sliding_window = 8
    torch.manual_seed(0)
    m = AutoModel.from_config(tc).float().eval()
    with torch.no_grad():
        for p in m.parameters():
            p.add_(0.02 * torch.randn_like(p))
    x = torch.randint(0, 512, (1, 12))
    emb = m.embed_tokens(x).detach().requires_grad_(True)
    out0 = m(inputs_embeds=emb).last_hidden_state
    g0, = torch.autograd.grad(out0[0, -1].sum(), emb)
    emb1 = emb.detach().clone().requires_grad_(True)
    with apply_lrp_rules_for_mode(m, "rlens") as rep:
        out1 = m(inputs_embeds=emb1).last_hidden_state
        g1, = torch.autograd.grad(out1[0, -1].sum(), emb1)
    diff, rel = float((out0 - out1).abs().max()), float((g0 - g1).norm() / g0.norm())
    print(f"  tiny decoder ({tc.layer_types}): patched {len(rep.ln_rule)} norms, {len(rep.mlp_rule)} MLPs; forward max |diff| {diff:.2e}, gradient rel. change {rel:.3f}")
    assert diff < 1e-5, "patched forward differs from stock beyond float32 dust (SiLU as z*sigmoid(z) under the identity rule)"
    assert rel > 0, "rules changed no gradient"
    out[repo] = {"ln_rule": len(rep.ln_rule), "forward_max_diff": diff, "grad_rel_change": rel}
print(json.dumps({"ok": True, **out}))
