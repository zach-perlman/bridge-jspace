#!/bin/bash
# Zach (2026-10-21, decided with Zach: full v2 everywhere): Qwen3.6-27B on the full v8 set (full_v8, 9858032). After
# the Gemma every-layer fit (the GPU's only job until then). Competence (which items the 27B gets right), smokes, then
# in parallel: (A) the knock-out, C1 (scripts/c1_v2.py, rule fixed in b7100e0): paper10 + rotated control on every
# word's whole question at layers 12-20, 20-28, 32-40 and whole depth, then each step alone at 32-40; (B) write_max
# v2, C2-graded (scripts/c2_graded.py, rule fixed in 238724c/2c826f3): every word of the counterfactual domains, 40 per
# word. Batches 16 / 32 so the two fit together.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -q "^EXIT" $R-gemmafit-1021-0428.log; do sleep 120; done
ok=0; while [ $ok -lt 3 ]; do
  [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 150000 ] && ok=$((ok + 1)) || ok=0
  sleep 30; done
echo "=== start $(date -u +%FT%TZ)"
WHY="Zach (2026-10-21): the full v8 set (full v2 everywhere), 27B"
COMP=full_v8_competence_v1
WORDS="PP PM MP MM CP CM PPP PPM PMP MPP MPM MMP"
$PY scripts/tasks_v2.py competence --set full_v8 --name $COMP --guess --why "$WHY: which items the 27B gets right" \
  || { echo "competence failed: stop"; exit 1; }
T="--tasks full_v8 --tasks-competence $COMP --tasks-words $WORDS --tasks-level all --tasks-strata core secondary"
W="--tasks full_v8 --tasks-competence $COMP --tasks-level all --families $WORDS"
$PY scripts/ablate_v2.py --name smoke_full_ko_1021 --why smoke --plan bands --bands 32-40 --conditions paper10 paper10_rot \
    $T --n 2 --kinds clean step1 --batch 16 \
  && BJ_BATCH=32 $PY scripts/write_max.py --name smoke_wm2_full_1021 --why smoke --n 2 --band 34-36 --early 20 \
    --possets question final $W || { echo "smokes failed: stop"; exit 1; }
echo "=== smokes ok $(date -u +%FT%TZ)"
(
  $PY scripts/ablate_v2.py --name full_ko_v1 --why "$WHY: C1, whole question" --plan bands --bands 12-20 20-28 32-40 0-62 \
    --conditions paper10 paper10_rot $T --n 1000 --kinds clean --batch 16 \
    && $PY scripts/c1_v2.py full_ko_v1 --middle L32-40 --set full_v8 || echo "=== knock-out FAILED"
  $PY scripts/ablate_v2.py --name full_ko_steps_v1 --why "$WHY: C1, each step alone at the middle band" --plan bands \
    --bands 32-40 --conditions paper10 paper10_rot $T --n 1000 --kinds step1 step2 step3 --batch 16 \
    && $PY scripts/c1_v2.py full_ko_steps_v1 --middle L32-40 --set full_v8 || echo "=== steps knock-out FAILED"
  echo "=== knock-out branch done $(date -u +%FT%TZ)"
) &
BJ_BATCH=32 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True $PY scripts/write_max.py --name wm2_full_v1 \
  --why "$WHY: write_max v2, C2-graded" --n 40 $W && $PY scripts/c2_graded.py wm2_full_v1 || echo "=== steering FAILED"
echo "=== steering branch done $(date -u +%FT%TZ)"
wait
echo "=== 27B full done $(date -u +%FT%TZ)"
