#!/bin/bash
# Zach (2026-10-21, decided with Zach: fixes first, the 27B reruns before Gemma): GPU 0 of the 2x H200 box, after its
# gate. (1) The 27B three-step step-by-step knock-out the B200 did not finish (full3_ko_steps_v2). (2) copy_sweep: where
# the question / final positions carry the bridge (two-step words of full_v8, 40 per word). (3) The two-step steering
# rerun with the fixes (wm2_full2_v2): full pools, question + final positions, layers 28-40, the joint copy ceiling;
# scored by c2_graded (C2-graded; C2-relative, fixed in 411e956), on every case, on the cases wm2_full2_v1 did not use
# (the clean test: C2-relative was designed after seeing it), and without guessable cases.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=0 UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200gate-*.log; do sleep 60; done
{ grep -qs "GATE PASSED" $R-h200gate-*.log || [ -f /workspace/scratch/markers/gate_accepted ]; } || { echo "the box gate did not pass: stop"; exit 1; }  # accepted with a caveat (Zach)
WHY="Zach (2026-10-21): 27B, after the fixes"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name full3_ko_steps_v2 --why "$WHY: full_v8b three-step words, each step alone at L32-40 (rerun; the B200 went down)" \
  --plan bands --bands 32-40 --conditions paper10 paper10_rot --tasks full_v8b --tasks-competence full_v8b_competence_v1 \
  --tasks-words PPP PPM PMP MPP MPM MMP --tasks-level all --tasks-strata core secondary --tasks-per-word --n 1000 \
  --kinds step1 step2 step3 --batch 32 \
  && $PY scripts/c1_v2.py full3_ko_steps_v2 --middle L32-40 --set full_v8b > /dev/null || echo "=== three-step steps FAILED"
$PY scripts/copy_sweep.py --name copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence full_v8_competence_v1 --families PP PM MP MM --n 40 || echo "=== copy sweep FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name wm2_full2_v2 --why "$WHY: two-step steering, full pools, joint copy ceiling" \
  --n 1000 --possets question final --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-level all \
  --families PP PM MP MM CP CM \
  && $PY scripts/c2_graded.py wm2_full2_v2 | tail -14 \
  && $PY scripts/c2_graded.py wm2_full2_v2 --fresh-vs wm2_full2_v1 | tail -4 \
  && $PY scripts/c2_graded.py wm2_full2_v2 --drop-guessable > /dev/null || echo "=== steering rerun FAILED"
echo "=== GPU 0 Qwen reruns done $(date -u +%FT%TZ)"
