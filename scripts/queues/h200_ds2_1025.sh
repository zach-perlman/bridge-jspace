#!/bin/bash
# Zach (2026-10-25, prereg amendment 39 note 1): DeepSeek-V4-Flash again, its first chain (h200nqDS-1025-0505) having
# failed at load in every step (transformers' DeepseekV4 supports no sdpa; pins now sets attn eager). Smoke first
# (scripts/new_model_smoke.py; stop if the unembed's top-1 differs or plain-text NLL >= 4 nats), then amendment 39's
# procedure unchanged: h200_nq_1025.sh gate, dev, test, swap on GPUs 0,1. Usage: h200_ds2_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=deepseek-v4-flash
PY="uv run --no-sync python"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/new_model_smoke.py > /workspace/scratch/dsv4f_smoke.log 2>&1 < /dev/null || { echo "=== deepseek-v4-flash smoke FAILED"; tail -5 /workspace/scratch/dsv4f_smoke.log; exit 1; }
verdict=$(python3 - results/checks/dsv4f_smoke.json <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
ok = s["unembed"]["top1_same"] and s["wikitext_nll"]["as_harness"] < 4
print("PASS" if ok else "STOP", json.dumps({k: s[k] for k in ("final_norm", "unembed", "wikitext_nll", "load_s")}), "greedy:", repr(s["chat"]["greedy"]))
PY
)
echo "=== DSSMOKE $verdict $(date -u +%T)"
[[ $verdict == PASS* ]] || exit 1
bash scripts/queues/h200_nq_1025.sh 0,1 deepseek-v4-flash dsv4f_ gate dev test swap
