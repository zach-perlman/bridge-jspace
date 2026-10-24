"""CPU checks of the Kolibri-1 LRP port (jpp_lens_kol; Zach, 2026-10-24, amendment 28 note 2) on a tiny random
Kolibri1 (5 blocks: 4 sliding + 1 full attention, 16 experts top-4, ungated shared expert)."""
# Run: /workspace/ext/kolibri_env/bin/python -I scripts/lens_fit/test_kolibri_lrp.py (CUDA_VISIBLE_DEVICES="", HF_HOME set)
import sys

sys.path.insert(0, "/workspace/ext/jpp_lens_kol/src")
import torch as t
from transformers import Kolibri1Config, Kolibri1ForCausalLM

from workspace_lens.lrp import LrpRuleConfig, apply_lrp_rules, apply_lrp_rules_for_mode

t.manual_seed(0)
t.set_num_threads(8)
cfg = Kolibri1Config(hidden_size=64, num_hidden_layers=5, num_attention_heads=4, num_key_value_heads=2, head_dim=16,
                     num_experts=16, num_experts_per_tok=4, moe_intermediate_size=32, shared_expert_intermediate_size=32,
                     vocab_size=512, sliding_window=8, use_sliding_window=True, max_position_embeddings=256,
                     layer_types=["sliding_attention"] * 4 + ["full_attention"], tie_word_embeddings=False)
m = Kolibri1ForCausalLM(cfg).float().eval()
with t.no_grad():  # non-trivial norm gains and router bias so the rules have something to act on
    for n, p in m.named_parameters():
        if n.endswith("norm.weight") or "layernorm" in n:
            p.copy_(1 + 0.3 * t.randn_like(p))
    for mod in m.modules():
        if type(mod).__name__ == "Kolibri1TopKRouter":
            mod.weight.normal_(0, 0.5); mod.e_score_correction_bias.normal_(0, 0.1)
        if type(mod).__name__ == "Kolibri1Experts":
            mod.gate_up_proj.normal_(0, 0.1); mod.down_proj.normal_(0, 0.1)
for p in m.parameters():
    p.requires_grad_(False)
ids = t.randint(0, 512, (2, 24))
print("experts implementation:", getattr(m.config, "_experts_implementation", None))

# 1. forward values: stock vs patched (r+moe)
with t.no_grad():
    stock = m(ids).logits
with apply_lrp_rules_for_mode(m, "r+moe") as rep:
    with t.no_grad():
        patched = m(ids).logits
names = rep.patched_names()
print("patched counts:", {k: len(v) for k, v in names.items()})
print("ln_rule names (block 0):", [n for n in names["ln_rule"] if ".layers.0." in n], "final:", [n for n in names["ln_rule"] if "layers" not in n])
assert len(names["ln_rule"]) == 4 * 5 + 1, names["ln_rule"]
assert not any("self_attn" in n.split(".") for n in names["ln_rule"])
assert len(names["mlp_rule"]) == 5 and all(n.endswith("shared_experts") for n in names["mlp_rule"])
assert len(names["moe_experts"]) == 5 and len(names["moe_gates"]) == 5
d = (stock - patched).abs().max().item()
print(f"1. forward max |stock - patched| logits: {d:.3e} (logit scale {stock.abs().max().item():.2f})")
assert d < 1e-4

# 2. the ungated block rule alone: d(block)/dx == J_experts + 4 J_shared (shared_expert_scale backward-only)
blk = m.model.layers[2].mlp
x = t.randn(1, 6, 64, requires_grad=True)
v = t.randn(1, 6, 64)
with apply_lrp_rules(m, LrpRuleConfig(shared_expert_scale=4.0)) as rep2:
    y = blk(x)
(g_patched,) = t.autograd.grad((y * v).sum(), x)
x2 = x.detach().clone().requires_grad_(True)
_, w, idx = blk.gate(x2)
ye = blk.experts(x2.view(-1, 64), idx, w).view(1, 6, 64)
ys = blk.shared_experts(x2)
(ge,) = t.autograd.grad((ye * v).sum(), x2, retain_graph=True)
(gs,) = t.autograd.grad((ys * v).sum(), x2)
d2 = (g_patched - (ge + 4 * gs)).abs().max().item()
d2s = (g_patched - (ge + gs)).abs().max().item()
print(f"2. ungated block: |g - (J_e + 4 J_s)| {d2:.2e}; vs stock (J_e + J_s) {d2s:.2e}; values equal: {t.equal(y.detach(), (ye + ys).detach())}")
assert d2 < 1e-5 and d2s > 1e-3

# 3. the experts patch alone with every rule off == stock experts (values and grads): sentinel slot handled
exp = blk.experts
xs = t.randn(6, 64, requires_grad=True)
_, w, idx = blk.gate(xs)
w = w.detach().requires_grad_(True)
from workspace_lens.lrp.lrp import _make_moe_experts_lrp_forward
pf = _make_moe_experts_lrp_forward(False, False, False)
yp = pf(exp, xs, idx, w)
ys_ = type(exp).forward(exp, xs, idx, w)
gp = t.autograd.grad((yp * 1.7).sum(), [xs, w])
gs_ = t.autograd.grad((ys_ * 1.7).sum(), [xs, w])
print(f"3. experts loop, rules off: value diff {(yp - ys_).abs().max().item():.2e}, grad diff {max((a - b).abs().max().item() for a, b in zip(gp, gs_)):.2e}")
assert (yp - ys_).abs().max() < 1e-5

# 4. the full preset changes gradients through a deep path (rules live), and stays finite
def jac_row(rules: bool) -> t.Tensor:
    h = {}
    def hook(mod, inp, out):
        out.requires_grad_(True); h["x"] = out; return out
    hd = m.model.layers[1].register_forward_hook(hook)
    try:
        if rules:
            with apply_lrp_rules_for_mode(m, "r+moe"):
                out = m.model(ids[:1], use_cache=False, output_hidden_states=True).hidden_states[-1]
        else:
            out = m.model(ids[:1], use_cache=False, output_hidden_states=True).hidden_states[-1]
    finally:
        hd.remove()
    (g,) = t.autograd.grad(out[0, -1, 3], h["x"])
    return g
with t.enable_grad():
    g_stock, g_rule = jac_row(False), jac_row(True)
cos = t.nn.functional.cosine_similarity(g_stock.flatten(), g_rule.flatten(), dim=0).item()
print(f"4. Jacobian row layer1 -> final, stock vs r+moe: cosine {cos:.3f}, finite {bool(t.isfinite(g_rule).all())}")
assert t.isfinite(g_rule).all() and cos < 0.9999
print("ALL CPU CHECKS PASSED")
