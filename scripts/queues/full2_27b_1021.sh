#!/bin/bash
# Zach (2026-10-21, decided with Zach): the 27B's two-step headline runs on the full v8 set (the words the C1 and C2
# rules compare, plus the computed starts): P->P, P->M, M->P, M->M, C->P, C->M. The three-step words follow separately,
# after their fix (per-word eligibility, more data). Steering (write_max v2, question + final positions, 40 per word;
# scripts/c2_graded.py) alongside the knock-out (paper10 + rotated control, whole question at 12-20, 20-28, 32-40 and
# whole depth, then each step alone at 32-40; scripts/c1_v2.py). After the padding check; padded knock-out batches
# only if it passed. Both scored with and without guessable items.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
until grep -q "^EXIT" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-padcheck-1021-0519.log; do sleep 30; done
PAD=$([ -f /workspace/scratch/markers/pad_validated ] && echo --pad); echo "=== start $(date -u +%FT%TZ); knock-out batches: ${PAD:-exact-length}"
WHY="Zach (2026-10-21): the full v8 set, two-step words, 27B"
COMP=full_v8_competence_v1
WORDS="PP PM MP MM CP CM"
T="--tasks full_v8 --tasks-competence $COMP --tasks-words $WORDS --tasks-level all"
W="--tasks full_v8 --tasks-competence $COMP --tasks-level all --families $WORDS"
(
  $PY scripts/ablate_v2.py --name full2_ko_v1 --why "$WHY: C1, whole question" --plan bands --bands 12-20 20-28 32-40 0-62 \
    --conditions paper10 paper10_rot $T --n 1000 --kinds clean --batch 32 $PAD \
    && $PY scripts/c1_v2.py full2_ko_v1 --middle L32-40 --set full_v8 \
    && $PY scripts/c1_v2.py full2_ko_v1 --middle L32-40 --set full_v8 --drop-guessable > /dev/null || echo "=== knock-out FAILED"
  $PY scripts/ablate_v2.py --name full2_ko_steps_v1 --why "$WHY: C1, each step alone at the middle band" --plan bands \
    --bands 32-40 --conditions paper10 paper10_rot $T --n 1000 --kinds step1 step2 --batch 32 $PAD \
    && $PY scripts/c1_v2.py full2_ko_steps_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== steps knock-out FAILED"
  echo "=== knock-out branch done $(date -u +%FT%TZ)"
) &
BJ_BATCH=64 $PY scripts/write_max.py --name wm2_full2_v1 --why "$WHY: write_max v2, C2-graded (question and final positions)" \
  --n 40 --possets question final $W \
  && $PY scripts/c2_graded.py wm2_full2_v1 && $PY scripts/c2_graded.py wm2_full2_v1 --drop-guessable > /dev/null \
  || echo "=== steering FAILED"
echo "=== steering branch done $(date -u +%FT%TZ)"
wait
echo "=== 27B two-step done $(date -u +%FT%TZ)"
