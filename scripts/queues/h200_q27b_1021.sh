#!/bin/bash
# Zach (2026-10-21, decided with Zach): GPU 0 of the 2x H200 box, after the 27B steering rerun (moved from GPU 1): the 27B knock-out additions on
# the two-step words of full_v8. (1) C1's second kill test: paper10 / paper10_keepown and their rotated controls at
# L32-40 (c1_v2: >= 75% of the memory-final loss restored kills C1). (2) Two more rotation seeds for the control
# (paper10_rot, --seed-offset 1 and 2). (3) The position split: the facts only (--positions context) and the question
# only (--positions question), paper10 + rotated, at L12-20 and L32-40.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=0 UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200q27a-*.log; do sleep 60; done  # 2026-10-21: moved to GPU 0 after its steering rerun (balances the GPUs)
WHY="Zach (2026-10-21): 27B, after the fixes"
T="--tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words PP PM MP MM CP CM --tasks-level all --n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep the subject's own word)" \
  --plan bands --bands 32-40 --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T \
  && $PY scripts/c1_v2.py full2_ko_keepown_v1 --middle L32-40 --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name full2_ko_rotseed${s}_v1 --why "$WHY: another draw of the rotated control (seed offset $s)" \
    --plan bands --bands 32-40 --conditions paper10_rot --seed-offset $s $T || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" \
    --plan bands --bands 12-20 32-40 --conditions paper10 paper10_rot --positions $pos $T \
    && $PY scripts/c1_v2.py full2_ko_pos_${pos}_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
echo "=== GPU 1 Qwen reruns done $(date -u +%FT%TZ)"
