"""Real Kolibri-1 weights, first 2 blocks, FP8 checkpoint dequantized to bf16 on load (FineGrainedFP8Config(dequantize
=True), as jpp_cli --dequantize-fp8), on CPU (Zach, 2026-10-24, amendment 28 note 2): module classes and dtypes after
dequantization, one routed expert's weight against a hand dequantization of the checkpoint block, and the r+moe
surgery (counts, forward values) on the real blocks."""
# Run: /workspace/ext/kolibri_env/bin/python -I scripts/lens_fit/test_kolibri_real2.py (CUDA_VISIBLE_DEVICES="", HF_HOME set)
import sys

sys.path.insert(0, "/workspace/ext/jpp_lens_kol/src")
import json, glob, os
import torch as t
from safetensors import safe_open
from transformers import AutoConfig, AutoTokenizer, FineGrainedFP8Config, Kolibri1ForCausalLM

from workspace_lens.lrp import apply_lrp_rules_for_mode

t.set_num_threads(8)
R, V = "Aleph-Alpha/Kolibri-1", "5bb7075ba22db733e3834b1c71d2245537cc14ed"
cfg = AutoConfig.from_pretrained(R, revision=V)
cfg.num_hidden_layers = 2
cfg.layer_types = cfg.layer_types[:2]
m = Kolibri1ForCausalLM.from_pretrained(R, revision=V, config=cfg, dtype=t.bfloat16, device_map="cpu",
                                        quantization_config=FineGrainedFP8Config(dequantize=True)).eval()
tok = AutoTokenizer.from_pretrained(R, revision=V)
print("tokenizer bos:", tok.bos_token_id, "| add_bos:", getattr(tok, "add_bos_token", None))
cls = sorted({type(x).__name__ for x in m.modules()})
print("module classes:", cls)
dts = sorted({str(p.dtype) for p in m.parameters()})
print("param dtypes:", dts, "| fp8 params:", [n for n, p in m.named_parameters() if "float8" in str(p.dtype)][:3])
assert not any("FP8" in c or "Fp8" in c for c in cls) and all("float8" not in d for d in dts)
e = m.model.layers[1].mlp.experts
print("experts:", type(e).__name__, tuple(e.gate_up_proj.shape), e.gate_up_proj.dtype, "| lm_head", m.lm_head.weight.dtype)

# hand dequantization of layer 1's expert 7 gate_up block from the checkpoint
snap = os.path.dirname(glob.glob(os.path.expanduser(f"/workspace/hf_cache/hub/models--Aleph-Alpha--Kolibri-1/snapshots/{V}/config.json"))[0])
idx = json.load(open(f"{snap}/model.safetensors.index.json"))["weight_map"]
keys = [k for k in idx if k.startswith("model.layers.1.mlp.experts.") and ("7.gate" in k or "gate_up" in k)]
print("checkpoint keys (sample):", keys[:6])
PY_OK = False
for k in keys:
    if k.endswith("weight") and (".7.gate_proj." in k or k.endswith("experts.gate_up_proj")):
        with safe_open(f"{snap}/{idx[k]}", "pt") as f:
            w = f.get_tensor(k)
        sk = [s for s in (k + "_scale_inv", k.replace("weight", "weight_scale_inv"), k + "_scale") if s in idx]
        with safe_open(f"{snap}/{idx[sk[0]]}", "pt") as f:
            s = f.get_tensor(sk[0])
        print("raw", k, w.dtype, tuple(w.shape), "scale", sk[0], tuple(s.shape))
        if w.dim() == 2:  # per-expert gate_proj [512, 2560], 128x128 blocks
            hand = (w.float().view(w.shape[0] // 128, 128, w.shape[1] // 128, 128) * s.float()[:, None, :, None]).view_as(w.float())
            loaded = e.gate_up_proj[7, :512].float()
        else:
            hand = (w.float().view(w.shape[0], w.shape[1] // 128, 128, w.shape[2] // 128, 128) * s.float()[:, :, None, :, None]).view(w.shape).float()[7]
            loaded = e.gate_up_proj[7].float()
        rel = ((hand.bfloat16().float() - loaded).abs().max() / hand.abs().max()).item()
        print(f"expert 7 gate weights: hand dequant vs loaded, max rel diff {rel:.2e}")
        PY_OK = rel < 1e-2
        break
print("hand dequant check:", "PASS" if PY_OK else "NOT RUN/FAIL")

ids = tok("The capital of France is Paris, and the capital of Japan is", return_tensors="pt").input_ids
with t.no_grad():
    a = m(ids).logits.float()
with apply_lrp_rules_for_mode(m, "r+moe") as rep:
    with t.no_grad():
        b = m(ids).logits.float()
print("r+moe counts:", {k: len(v) for k, v in rep.patched_names().items()})
print(f"forward |stock - patched| {(a - b).abs().max().item():.3e} (logit scale {a.abs().max().item():.1f}); finite {bool(t.isfinite(a).all())}")
