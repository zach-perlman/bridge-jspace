#!/bin/bash
# Zach (2026-10-21, decided with Zach): Qwen3.6-27B on the full v8 set after competence (comp_both_1021.sh; smokes
# already passed in full_27b_v2). Speed-ups: steering skips the "all positions" site (no rule uses it: it rewrites
# the tokens C changes), and the knock-out runs alongside steering (the knock-out is launch-bound, steering
# GPU-bound). Steering: write_max v2, question + final positions, every word of the counterfactual domains, 40 per word
# (scripts/c2_graded.py, rule 238724c/2c826f3). Knock-out: paper10 + rotated control, whole question at 12-20, 20-28,
# 32-40 and whole depth, then each step alone at 32-40 (scripts/c1_v2.py, rule b7100e0). Both scored with and
# without guessable items.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo "=== start $(date -u +%FT%TZ)"
WHY="Zach (2026-10-21): the full v8 set (full v2 everywhere), 27B"
COMP=full_v8_competence_v1
WORDS="PP PM MP MM CP CM PPP PPM PMP MPP MPM MMP"
T="--tasks full_v8 --tasks-competence $COMP --tasks-words $WORDS --tasks-level all --tasks-strata core secondary"
W="--tasks full_v8 --tasks-competence $COMP --tasks-level all --families $WORDS"
(
  $PY scripts/ablate_v2.py --name full_ko_v1 --why "$WHY: C1, whole question" --plan bands --bands 12-20 20-28 32-40 0-62 \
    --conditions paper10 paper10_rot $T --n 1000 --kinds clean --batch 32 \
    && $PY scripts/c1_v2.py full_ko_v1 --middle L32-40 --set full_v8 \
    && $PY scripts/c1_v2.py full_ko_v1 --middle L32-40 --set full_v8 --drop-guessable > /dev/null || echo "=== knock-out FAILED"
  $PY scripts/ablate_v2.py --name full_ko_steps_v1 --why "$WHY: C1, each step alone at the middle band" --plan bands \
    --bands 32-40 --conditions paper10 paper10_rot $T --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py full_ko_steps_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== steps knock-out FAILED"
  echo "=== knock-out branch done $(date -u +%FT%TZ)"
) &
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name wm2_full_v1 --why "$WHY: write_max v2, C2-graded (question and final positions)" \
  --n 40 --possets question final $W \
  && $PY scripts/c2_graded.py wm2_full_v1 && $PY scripts/c2_graded.py wm2_full_v1 --drop-guessable > /dev/null \
  || echo "=== steering FAILED"
echo "=== steering branch done $(date -u +%FT%TZ)"
wait
echo "=== 27B full done $(date -u +%FT%TZ)"
