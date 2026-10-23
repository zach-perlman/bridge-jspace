"""check_gptoss_lrp: the J++ fitter's "ln" preset on gpt-oss-20b (bridge-jspace, 2026-10-23; prereg amendment 8). (1) On the
real architecture (meta device): every residual-stream RMSNorm is patched (two per block and the final norm), nothing in
attention, no MLP (its experts keep standard gradients); the rlens preset raises (no dense gated MLP). (2) On a tiny random
decoder of the same class: the patched forward equals the stock forward and the gradients differ.
python -I scripts/lens_fit/check_gptoss_lrp.py   (run with /workspace/ext/jpp_lens/.venv/bin/python)"""

import copy
import glob
import json
import sys

import torch
from transformers import AutoConfig, AutoModel, AutoModelForCausalLM

sys.path.insert(0, "/workspace/ext/jpp_lens/src")
from workspace_lens.lrp.lrp import apply_lrp_rules_for_mode  # noqa: E402

cfg = AutoConfig.from_pretrained(glob.glob("/workspace/hf_cache/hub/models--openai--gpt-oss-20b/snapshots/*/config.json")[0].rsplit("/", 1)[0])
cfg.quantization_config = None
if hasattr(cfg, "quantization_config"):
    delattr(cfg, "quantization_config")
with torch.device("meta"):
    full = AutoModelForCausalLM.from_config(cfg)
n = cfg.num_hidden_layers
with apply_lrp_rules_for_mode(full, "ln") as rep:
    print("real architecture, ln preset: ln_rule", len(rep.ln_rule), "mlp_rule", len(rep.mlp_rule), "e.g.", rep.ln_rule[:2])
    assert len(rep.ln_rule) == 2 * n + 1, (len(rep.ln_rule), 2 * n + 1)
    assert not rep.mlp_rule and not any("self_attn" in x for x in rep.ln_rule)
try:
    with apply_lrp_rules_for_mode(full, "rlens"):
        pass
    raise SystemExit("rlens did not raise on gpt-oss: check the guard")
except RuntimeError as e:
    print("rlens raises as expected:", str(e)[:90])
tc = copy.deepcopy(cfg)
tc.num_hidden_layers, tc.hidden_size, tc.intermediate_size, tc.vocab_size = 2, 64, 64, 512
tc.num_attention_heads, tc.num_key_value_heads, tc.head_dim = 4, 2, 16
tc.num_local_experts, tc.num_experts_per_tok = 4, 2
tc.layer_types = cfg.layer_types[:2]
tc.sliding_window = 8
tc.pad_token_id = tc.bos_token_id = tc.eos_token_id = 0
tc._attn_implementation = "eager"
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
with apply_lrp_rules_for_mode(m, "ln") as rep:
    out1 = m(inputs_embeds=emb1).last_hidden_state
    g1, = torch.autograd.grad(out1[0, -1].sum(), emb1)
diff, rel = float((out0 - out1).abs().max()), float((g0 - g1).norm() / g0.norm())
print(f"tiny decoder ({tc.layer_types}): patched {len(rep.ln_rule)} norms; forward max |diff| {diff:.2e}, gradient rel. change {rel:.3f}")
assert diff < 1e-5 and rel > 0
print(json.dumps({"ok": True, "ln_rule": len(rep.ln_rule), "forward_max_diff": diff, "grad_rel_change": rel}))
