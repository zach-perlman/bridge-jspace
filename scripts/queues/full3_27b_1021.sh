#!/bin/bash
# Zach (2026-10-21, decided with Zach): the 27B's three-step runs on full_v8b with per-word eligibility, after its
# competence (comp3_1021.sh). Steering (write_max v2, question + final positions, 40 per word) alongside the knock-out
# (paper10 + rotated control, whole question at 12-20, 20-28, 32-40 and whole depth, then each step alone at 32-40).
# No rule uses these words (C1/C2 compare the two-step pairs): reported, with and without guessable items.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
until grep -qs "^EXIT" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-comp3-*.log; do sleep 60; done
[ -f results/tasks_v2/full_v8b_competence_v1/summary.json ] || { echo "no 27B full_v8b competence: stop"; exit 1; }
PAD=$([ -f /workspace/scratch/markers/pad_validated ] && echo --pad); echo "=== start $(date -u +%FT%TZ); knock-out batches: ${PAD:-exact-length}"
WHY="Zach (2026-10-21): full_v8b, three-step words, per-word eligibility, 27B"
COMP=full_v8b_competence_v1
WORDS="PPP PPM PMP MPP MPM MMP"
T="--tasks full_v8b --tasks-competence $COMP --tasks-words $WORDS --tasks-level all --tasks-strata core secondary --tasks-per-word"
W="--tasks full_v8b --tasks-competence $COMP --tasks-level all --families $WORDS --tasks-per-word"
(
  $PY scripts/ablate_v2.py --name full3_ko_v1 --why "$WHY: knock-out, whole question" --plan bands \
    --bands 12-20 20-28 32-40 0-62 --conditions paper10 paper10_rot $T --n 1000 --kinds clean --batch 32 $PAD \
    && $PY scripts/c1_v2.py full3_ko_v1 --middle L32-40 --set full_v8b > /dev/null \
    && $PY scripts/c1_v2.py full3_ko_v1 --middle L32-40 --set full_v8b --drop-guessable > /dev/null || echo "=== knock-out FAILED"
  $PY scripts/ablate_v2.py --name full3_ko_steps_v1 --why "$WHY: knock-out, each step alone at the middle band" --plan bands \
    --bands 32-40 --conditions paper10 paper10_rot $T --n 1000 --kinds step1 step2 step3 --batch 32 $PAD \
    && $PY scripts/c1_v2.py full3_ko_steps_v1 --middle L32-40 --set full_v8b > /dev/null || echo "=== steps knock-out FAILED"
) &
BJ_BATCH=64 $PY scripts/write_max.py --name wm2_full3_v1 --why "$WHY: write_max v2 (question and final positions)" \
  --n 40 --possets question final $W \
  && $PY scripts/c2_graded.py wm2_full3_v1 > /dev/null && $PY scripts/c2_graded.py wm2_full3_v1 --drop-guessable > /dev/null \
  || echo "=== steering FAILED"
wait
echo "=== 27B three-step done $(date -u +%FT%TZ)"
