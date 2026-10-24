#!/bin/bash
# jpp_cli end to end on a tiny random Kolibri1 with the real tokenizer, CPU (Zach, 2026-10-24, amendment 28 note 2).
set -eu
cd /workspace/scratch
set -a; . /workspace/bridge-jspace/.env; set +a
export CUDA_VISIBLE_DEVICES="" PYTHONPATH=/workspace/ext/jpp_lens_kol/src OMP_NUM_THREADS=8
KPY=/workspace/ext/kolibri_env/bin/python
D=/workspace/scratch/tinykol; rm -rf "${D:?}" tinykol_run; mkdir -p tinykol_run
nice -n 10 $KPY - <<'PY'
import torch as t
from transformers import AutoTokenizer, Kolibri1Config, Kolibri1ForCausalLM
t.manual_seed(0)
tok = AutoTokenizer.from_pretrained("Aleph-Alpha/Kolibri-1", revision="5bb7075ba22db733e3834b1c71d2245537cc14ed")
cfg = Kolibri1Config(hidden_size=64, num_hidden_layers=5, num_attention_heads=4, num_key_value_heads=2, head_dim=16,
                     num_experts=16, num_experts_per_tok=4, moe_intermediate_size=32, shared_expert_intermediate_size=32,
                     vocab_size=128000, sliding_window=8, use_sliding_window=True, max_position_embeddings=512,
                     layer_types=["sliding_attention"] * 4 + ["full_attention"], tie_word_embeddings=False,
                     eos_token_id=127906, pad_token_id=127901, bos_token_id=None)
m = Kolibri1ForCausalLM(cfg).to(t.bfloat16)
m.save_pretrained("/workspace/scratch/tinykol"); tok.save_pretrained("/workspace/scratch/tinykol")
print("saved tiny kolibri")
PY
cd /workspace/ext/jpp_lens_kol
C="nice -n 10 $KPY scripts/jpp_cli.py"
$C fit-router --hf-model-name $D --device-map cpu --layers 0,1,2,3 --num-prompts 8 --num-clusters 2 --projection-dim 8 \
  --skip-first-n-positions 16 --max-seq-len 128 --seed 0 --out /workspace/scratch/tinykol_run/router.pt 2>&1 | tail -2
$C fit-shard --hf-model-name $D --device-map cpu --layers 0,1,2,3 --router-path /workspace/scratch/tinykol_run/router.pt \
  --shard-idx 0 --num-shards 1 --num-prompts 2 --target-offset -1 --lrp-mode r+moe --jacobian-rows-per-pass 16 \
  --max-seq-len 128 --skip-first-n-positions 16 --checkpoint-every-n-prompts 2 --artifacts-base-dir /workspace/scratch/tinykol_run/art \
  --checkpoint-name t 2>&1 | grep -v -i warn | tail -4
$C merge-experts --checkpoint-dirs $(ls -d /workspace/scratch/tinykol_run/art/*/t/shard0of*) --num-clusters 2 \
  --out /workspace/scratch/tinykol_run/experts.pt --pooled-lens-out /workspace/scratch/tinykol_run/pooled_lens.pt --device cpu 2>&1 | tail -2
$KPY - <<'PY'
import torch as t, json
d = t.load("/workspace/scratch/tinykol_run/pooled_lens.pt", map_location="cpu", weights_only=False)
print("pooled keys:", list(d) if isinstance(d, dict) else type(d))
J = d["J"] if isinstance(d, dict) and "J" in d else None
print("J:", None if J is None else (tuple(J.shape), J.dtype, bool(t.isfinite(J).all())))
cfg = d.get("config") or d.get("lens_config") or {}
print("config:", {k: cfg.get(k) for k in ("lrp_mode", "num_prompts_trained_on", "source_layers", "relative_end_transport_layer", "num_clusters")} if isinstance(cfg, dict) else cfg)
PY
cat /workspace/scratch/tinykol_run/*stamp*.json 2>/dev/null | head -c 600; echo
echo "CLI DRY RUN DONE"
