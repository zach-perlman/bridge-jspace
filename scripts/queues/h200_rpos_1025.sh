#!/bin/bash
# Zach (2026-10-25, amendment 35's position prediction; amendment 37 note 1): the question-only knock-out on v2.1's R items
# (RM RA RN), paper10 / rot, at the model's v2 band, with its R-only competence; scored with the model's v2 question-only
# run (jsuite2_score --with) when that exists. Usage: h200_rpos_1025.sh GPU TARGET PREFIX BAND BATCH
set -u
G=$1; T=$2; p=$3; band=$4; batch=$5
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_TARGET=$T
PY="uv run --no-sync python"
SET=jsuite_v2_1_test_chat; cn=${p}${SET}_R_competence_cand2_v1; r=${p}${SET}_R_ko_cand2_posquestion_v1; v2=${p}jsuite_v2_test_chat_ko_cand2_posquestion_v1
[ -f results/tasks_v2/$cn/summary.json ] || { echo "=== RPOS $T: no R competence $cn"; exit 1; }
echo "=== ablate_v2/$r at L$band $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "Zach (2026-10-25, amendment 35 / 37 note 1): $T, R items, question only, L$band" \
  --plan bands --bands $band --positions question --conditions paper10 paper10_rot --tasks $SET --tasks-competence $cn --tasks-words RM RA RN \
  --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { echo "=== RPOS $T FAILED"; tail -3 /workspace/scratch/$r.log; exit 1; }
[ -f results/ablate_v2/$v2/summary.json ] && $PY scripts/jsuite2_score.py $v2 --set $SET --by-relation --with $r | grep -E "^facts (paper10|paper10_rot) +never-named" | sed "s/^/=== RPOS $T: /"
echo "=== RPOS $T done $(date -u +%T)"
