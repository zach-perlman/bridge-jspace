#!/bin/bash
# Zach (2026-10-21, decided with Zach: "competence -> steer -> knockout"): Qwen3.6-27B on the full v8 set, after the
# competence job for both models (comp_both_1021.sh). Smokes; then steering (write_max v2, every word of the
# counterfactual domains, 40 per word; scripts/c2_graded.py, rule 238724c/2c826f3); then the knock-out (paper10 +
# rotated control, whole question at 12-20, 20-28, 32-40 and whole depth, then each step alone at 32-40;
# scripts/c1_v2.py, rule b7100e0). One at a time, each with the GPU to itself.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
until grep -q "^EXIT" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-compboth-1021-0445.log; do sleep 60; done
[ -f results/tasks_v2/full_v8_competence_v1/summary.json ] || { echo "no 27B competence: stop"; exit 1; }
echo "=== start $(date -u +%FT%TZ)"
WHY="Zach (2026-10-21): the full v8 set (full v2 everywhere), 27B"
COMP=full_v8_competence_v1
WORDS="PP PM MP MM CP CM PPP PPM PMP MPP MPM MMP"
T="--tasks full_v8 --tasks-competence $COMP --tasks-words $WORDS --tasks-level all --tasks-strata core secondary"
W="--tasks full_v8 --tasks-competence $COMP --tasks-level all --families $WORDS"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
BJ_BATCH=64 $PY scripts/write_max.py --name smoke_wm2_full_1021 --why smoke --n 2 --band 34-36 --early 20 \
    --possets question final $W \
  && $PY scripts/ablate_v2.py --name smoke_full_ko_1021 --why smoke --plan bands --bands 32-40 \
    --conditions paper10 paper10_rot $T --n 2 --kinds clean step1 --batch 32 || { echo "smokes failed: stop"; exit 1; }
echo "=== smokes ok $(date -u +%FT%TZ)"
BJ_BATCH=64 $PY scripts/write_max.py --name wm2_full_v1 --why "$WHY: write_max v2, C2-graded" --n 40 $W \
  && $PY scripts/c2_graded.py wm2_full_v1 || echo "=== steering FAILED"
echo "=== steering done $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name full_ko_v1 --why "$WHY: C1, whole question" --plan bands --bands 12-20 20-28 32-40 0-62 \
  --conditions paper10 paper10_rot $T --n 1000 --kinds clean --batch 32 \
  && $PY scripts/c1_v2.py full_ko_v1 --middle L32-40 --set full_v8 || echo "=== knock-out FAILED"
$PY scripts/ablate_v2.py --name full_ko_steps_v1 --why "$WHY: C1, each step alone at the middle band" --plan bands \
  --bands 32-40 --conditions paper10 paper10_rot $T --n 1000 --kinds step1 step2 step3 --batch 32 \
  && $PY scripts/c1_v2.py full_ko_steps_v1 --middle L32-40 --set full_v8 || echo "=== steps knock-out FAILED"
echo "=== 27B full done $(date -u +%FT%TZ)"
