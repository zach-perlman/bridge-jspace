"""Check (Zach, 2026-10-20) that jpp_lens's LRP surgery covers Mistral and leaves forward values unchanged: a tiny
random MistralForCausalLM, logits with and without apply_lrp_rules_for_mode('rlens'), and the patch report. Run in the
jpp_lens environment: uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/test_mistral_lrp.py"""
import torch
from transformers import MistralConfig, MistralForCausalLM
from workspace_lens.lrp import apply_lrp_rules_for_mode

torch.manual_seed(0)
cfg = MistralConfig(vocab_size=128, hidden_size=64, intermediate_size=128, num_hidden_layers=2, num_attention_heads=4,
                    num_key_value_heads=2, max_position_embeddings=64)
model = MistralForCausalLM(cfg).eval()
ids = torch.randint(0, 128, (1, 12))
with torch.no_grad():
    stock = model(ids).logits
with apply_lrp_rules_for_mode(model, "rlens") as report:
    with torch.no_grad():
        patched = model(ids).logits
print("report:", report)
print("max |logit difference| with the LRP surgery:", float((stock - patched).abs().max()))
assert torch.allclose(stock, patched, atol=1e-5), "LRP surgery changed the forward values"
print("OK")
