"""bolt_shim_check (Zach, 2026-10-25, amendment 40 note 1): model._gated_rmsnorm_shim against transformers' Zamba2RMSNormGated, fp32 and bf16 inputs."""
import os, sys
os.environ["BJ_TARGET"] = "nemotron-3.5-bolt"
sys.path.insert(0, "src")
import torch
from bridge_jspace import model as M
M._gated_rmsnorm_shim()
from mamba_ssm.ops.triton.layernorm_gated import rmsnorm_fn
from transformers.models.zamba2.modeling_zamba2 import Zamba2RMSNormGated
torch.manual_seed(0)
x, z = torch.randn(2, 5, 8192), torch.randn(2, 5, 8192)
ref = Zamba2RMSNormGated(8192, 1024, eps=1e-5); ref.weight.data = torch.randn(8192)
ours = rmsnorm_fn(x=x, weight=ref.weight, bias=None, z=z, eps=1e-5, group_size=1024, norm_before_gate=False)
r = ref(x, z)
print("fp32: max abs diff", (ours - r).abs().max().item(), "max rel", ((ours - r).abs() / r.abs().clamp_min(1e-3)).max().item())
xb, zb = x.bfloat16(), z.bfloat16()
ob, rb = rmsnorm_fn(x=xb, weight=ref.weight, bias=None, z=zb, eps=1e-5, group_size=1024, norm_before_gate=False), ref(xb, zb)
exact = rmsnorm_fn(x=xb.float(), weight=ref.weight, bias=None, z=zb.float(), eps=1e-5, group_size=1024, norm_before_gate=False)
print("bf16 in: shim vs fp32 math", (ob.float() - exact).abs().max().item(), "| transformers vs fp32 math", (rb.float() - exact).abs().max().item())
