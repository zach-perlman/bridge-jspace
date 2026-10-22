#!/bin/bash
# Zach (2026-10-22, prereg amendment 6A/6D): the 27B on a fresh data seed (fresh_v8s2) at its fixed band L32-40, on GPU 0
# beside the 9B steering; then the 27B's dose at L32-40 on full_v8's 2x2 words (descriptive, figure 3B).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
export BJ_TARGET=qwen3.6-27b
WHY="Zach (2026-10-22, prereg amendment 6A): the 27B on a fresh data seed (fresh_v8s2)"
TWO="PP PM MP MM CP CM"
C=fresh_v8s2_competence_v1
K="--n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
if [ ! -f results/tasks_v2/$C/summary.json ]; then
  echo "=== competence $C $(date -u +%T)"
  $PY scripts/tasks_v2.py competence --set fresh_v8s2 --name $C --guess --why "$WHY: competence" > /workspace/scratch/$C.log 2>&1 \
    && $PY scripts/competence_full_report.py $C | tail -8 || { echo "=== competence FAILED"; tail -5 /workspace/scratch/$C.log; exit 1; }
fi
T="--tasks fresh_v8s2 --tasks-competence $C --tasks-words $TWO --tasks-level all"
echo "=== smoke $(date -u +%T)"
$PY scripts/ablate_v2.py --name fresh2_smoke_1022 --why smoke --plan bands --bands 32-40 --conditions paper10 paper10_rot $T \
  --n 2 --kinds clean --batch 16 > /workspace/scratch/fresh2_smoke.log 2>&1 || { echo "smoke failed: stop"; tail -5 /workspace/scratch/fresh2_smoke.log; exit 1; }
echo "=== ablate_v2/fresh2_ko_v1 $(date -u +%T)"
$PY scripts/ablate_v2.py --name fresh2_ko_v1 --why "$WHY: C1 at the fixed band L32-40" --plan bands --bands 32-40 \
  --conditions paper10 paper10_rot $T $K \
  && $PY scripts/c1_v2.py fresh2_ko_v1 --middle L32-40 --set fresh_v8s2 | tail -2 || echo "=== fresh C1 FAILED"
echo "=== ablate_v2/full2_dose_v1 $(date -u +%T)"
$PY scripts/ablate_v2.py --name full2_dose_v1 --why "Zach (2026-10-22, prereg amendment 6D): the 27B's dose at L32-40 (descriptive)" \
  --plan bands --bands 32-40 --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words PP PM MP MM --tasks-level all $K \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top25 top25_rot top50 top50_rot top100 top100_rot || echo "=== 27B dose FAILED"
echo "=== GPU 0 fresh done $(date -u +%FT%TZ)"
