"""check_muse_lrp: the J++ fitter's LRP surgery on Muse Glimmer 30B (bridge-jspace, 2026-10-22). (1) On the real
architecture (meta device, no weights): the rlens rules patch every residual-stream norm and gated MLP of the text
decoder and nothing in the vision path, without raising. (2) On a tiny random text decoder: the patched forward equals
the stock forward (the rules change gradients only), and gradients differ (the rules did something).
python -I scripts/lens_fit/check_muse_lrp.py   (run from /workspace/ext/jpp_lens's environment)"""

import copy
import glob
import json
import sys

import torch
from transformers import AutoConfig, AutoModel, AutoModelForImageTextToText

sys.path.insert(0, "/workspace/ext/jpp_lens/src")
from workspace_lens.lrp.lrp import apply_lrp_rules_for_mode  # noqa: E402

cfg_path = glob.glob("/workspace/hf_cache/hub/models--meta-models--Muse-Glimmer-30B/snapshots/*/config.json")[0]
cfg = AutoConfig.from_pretrained(cfg_path.rsplit("/", 1)[0])
with torch.device("meta"):
    full = AutoModelForImageTextToText.from_config(cfg)
with apply_lrp_rules_for_mode(full, "rlens") as rep:
    print("real architecture: ln_rule", len(rep.ln_rule), "mlp_rule", len(rep.mlp_rule))
    print("  e.g.", rep.ln_rule[:3], rep.mlp_rule[:1])
    assert not any("vision" in n for n in rep.ln_rule + rep.mlp_rule), "vision modules patched"
    n_layers = cfg.text_config.num_hidden_layers
    assert len(rep.mlp_rule) == n_layers, (len(rep.mlp_rule), n_layers)

tc = copy.deepcopy(cfg.text_config)
tc.num_hidden_layers, tc.hidden_size, tc.intermediate_size = 4, 64, 128
tc.num_attention_heads, tc.num_key_value_heads, tc.head_dim, tc.vocab_size = 4, 2, 16, 512
tc.layer_types = tc.layer_types[:4]
tc.sliding_window = 8
torch.manual_seed(0)
m = AutoModel.from_config(tc).float().eval()
with torch.no_grad():
    for p in m.parameters():
        p.add_(0.02 * torch.randn_like(p))  # zero-init norm weights get non-trivial values
x = torch.randint(0, 512, (1, 12))
emb = m.embed_tokens(x).detach().requires_grad_(True)
out0 = m(inputs_embeds=emb).last_hidden_state
g0, = torch.autograd.grad(out0[0, -1].sum(), emb)
emb1 = emb.detach().clone().requires_grad_(True)
with apply_lrp_rules_for_mode(m, "rlens") as rep:
    out1 = m(inputs_embeds=emb1).last_hidden_state
    g1, = torch.autograd.grad(out1[0, -1].sum(), emb1)
print("tiny decoder: patched", len(rep.ln_rule), "norms,", len(rep.mlp_rule), "MLPs")
print("  forward max |diff|", float((out0 - out1).abs().max()), " gradient rel. change", float((g0 - g1).norm() / g0.norm()))
assert torch.allclose(out0, out1, atol=1e-6, rtol=1e-5), "patched forward differs from stock"
assert float((g0 - g1).norm()) > 0, "rules changed no gradient"
print(json.dumps({"ok": True}))
