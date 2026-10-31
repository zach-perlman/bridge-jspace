#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 11, item 4): Bolt's layer sweep, overnight filler only: after the note 11
# jobs, on both GPUs. Usage: h200_n11bolt_1028.sh WAITJOB [WAITJOB ...]
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_GRAM_PROJ=1 BJ_TARGET=nemotron-3.5-bolt
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 11, item 4)"
for j in "$@"; do
  echo "=== waiting for $j $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$j.log; do sleep 60; done
done
r=nem35b_nn_swap_sweep_v1
if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; exit 0; fi
echo "=== nn_swap/$r $(date -u +%T)"
$PY scripts/nn_swap.py --name $r --why "$W: Bolt layer sweep (overnight filler)" --competence nem35b_jsuite_v3_test_chat_competence_cand2_v1 \
  --words RM MM PM --scene-words RM MM PM --sample-per-word 80 --conds insert_k10 insert_k10_rand \
  --sweep 6-11 12-17 18-23 24-29 30-35 36-41 42-47 48-53 54-59 60-65 66-71 72-77 78-83 > /workspace/scratch/$r.log 2>&1 < /dev/null \
  || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; exit 3; }
echo "=== done $r $(date -u +%T)"
