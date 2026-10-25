"""bolt_load_check (Zach, 2026-10-25, amendment 40 note 1): Bolt load check without weights (CPU): NVIDIA's language-model class built empty from the pinned config, its state
dict against the checkpoint index's keys under pins' key mapping, the split map, the tokenizer and chat rendering."""
import collections, json, os, re, sys
os.environ["BJ_TARGET"] = "nemotron-3.5-bolt"
sys.path.insert(0, "src")
from accelerate import init_empty_weights
from huggingface_hub import snapshot_download
from bridge_jspace import chat, pins, tokens
from bridge_jspace import model as M

path = snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION, allow_patterns=["*.py", "*.json", "*.jinja"])
spec = pins.TARGETS[pins.TARGET]["remote_lm"]
cls, cfg = M._remote_lm(path, spec)
print("class", cls.__name__, "layers", cfg.num_hidden_layers, "time_step_limit", cfg.time_step_limit, "moe_latent", cfg.moe_latent_size)
with init_empty_weights():
    skel = cls(cfg)
names = set(skel.state_dict())
w = json.load(open(path + "/model.safetensors.index.json"))["weight_map"]
def mapk(k):
    for p, r in {"^backbone": "model", **spec["key_mapping"]}.items():
        k2, n = re.subn(p, r, k)
        if n:
            return k2
    return k
mapped = {mapk(k) for k in w}
miss = sorted(names - mapped)
print("model tensors", len(names), "checkpoint keys", len(w), "missing", len(miss), miss[:8])
print("unexpected by prefix", collections.Counter(k.split(".")[0] for k in mapped - names))
print("final norm", type(skel.model.norm_f).__name__, "mixers", collections.Counter(type(l.mixer).__name__ for l in skel.model.layers))
sizes = collections.Counter()
for l in skel.model.layers:
    e = getattr(l.mixer, "experts", None)
    if e is not None:
        sizes[(len(e) if hasattr(e, "__len__") else "fused", getattr(l.mixer, "top_k", None))] += 1
print("moe (experts, top_k) per block", dict(sizes))
dm = M._split_map(cls, path, 44, cfg)
print("split map", collections.Counter(dm.values()), [k for k in dm if "layers" not in k])
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(path)
text = chat.chat_text(tok, "What is the capital of Australia? " + chat.QUESTION_INSTRUCTION)
print(repr(text))
print("ids start", tok(text, add_special_tokens=False).input_ids[:4], "bos", tok.bos_token_id)
mod = sys.modules[cls.__module__.rsplit(".", 1)[0] + ".modeling_nemotron_h"]
print("fast path", mod.is_fast_path_available, "rmsnorm_fn is the shim", mod.rmsnorm_fn.__module__)
import torch
from transformers.models.zamba2.modeling_zamba2 import Zamba2RMSNormGated
x, z = torch.randn(2, 5, 8192, dtype=torch.bfloat16), torch.randn(2, 5, 8192, dtype=torch.bfloat16)
ref = Zamba2RMSNormGated(8192, 1024, eps=1e-5); ref.weight.data = torch.randn(8192)
ours = mod.rmsnorm_fn(x=x, weight=ref.weight, bias=None, z=z, eps=1e-5, group_size=1024, norm_before_gate=False)
print("shim vs transformers' torch gated norm: max abs diff", (ours.float() - ref(x, z).float()).abs().max().item(), "scale", ours.float().abs().mean().item())
