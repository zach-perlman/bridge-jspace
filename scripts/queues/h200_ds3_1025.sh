#!/bin/bash
# Zach (2026-10-25, prereg amendment 39 note 2): DeepSeek-V4-Flash a third time. Its second chain (h200nqDS2, this script's
# h200_ds2_1025.sh) stopped at the smoke: the harness read one of its 4 residual streams (model._streamed now reads
# their mean and lifts edits to all 4). Its first chain (h200nqDS-1025-0505) had
# failed at load in every step (transformers' DeepseekV4 supports no sdpa; pins now sets attn eager). Smoke first
# (scripts/new_model_smoke.py; stop if the unembed's top-1 differs, plain-text NLL >= 4 nats, or a no-op edit
# changes the logits), then amendment 39's
# procedure unchanged: h200_nq_1025.sh gate, dev, test, swap on GPUs 0,1. Usage: h200_ds3_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=deepseek-v4-flash
PY="uv run --no-sync python"
echo "=== start $(date -u +%FT%TZ)"
for g in 0 1; do need=$([ $g = 0 ] && echo 60000 || echo 120000); until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $need ]; do sleep 60; done; done
echo "=== GPUs ready (GPU 0 beside Ministral) $(date -u +%T)"
$PY scripts/new_model_smoke.py > /workspace/scratch/dsv4f_smoke.log 2>&1 < /dev/null || { echo "=== deepseek-v4-flash smoke FAILED"; tail -5 /workspace/scratch/dsv4f_smoke.log; exit 1; }
verdict=$(python3 - results/checks/dsv4f_smoke.json <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
ok = s["unembed"]["top1_same"] and s["wikitext_nll"]["as_harness"] < 4 and s["noop_edit_max_abs_diff"] == 0
print("PASS" if ok else "STOP", json.dumps({k: s[k] for k in ("final_norm", "streams", "stream_mean_top1", "unembed", "noop_edit_max_abs_diff", "wikitext_nll", "load_s") if k in s}), "greedy:", repr(s["chat"]["greedy"]))
PY
)
echo "=== DSSMOKE $verdict $(date -u +%T)"
[[ $verdict == PASS* ]] || exit 1
bash scripts/queues/h200_nq_1025.sh 0,1 deepseek-v4-flash dsv4f_ gate dev test swap
