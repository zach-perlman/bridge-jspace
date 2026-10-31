#!/bin/bash
# Zach (2026-10-29, prereg amendment 61 note 33 addendum): v4 knock-out at the main band restricted to the bridge's mentions in
# the passage. Usage: h200_kobridge_1029.sh MODEL GPU [WAITJOB ...]
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=32 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; KBATCH=16 ;;
esac
W="Zach (2026-10-29, prereg amendment 61 note 33 addendum, $BJ_TARGET)"
SET=jsuite_v4_test_chat; C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
r=${P}${SET}_ko_posbridge_cand2_v1
if [ ! -f results/ablate_v2/$r/summary.json ]; then
  $PY scripts/ablate_v2.py --name $r --why "$W: knock-out at L$KB, the bridge's mentions" --plan bands --bands $KB --conditions paper10 paper10_rot \
    --positions bridge --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --n 1000 --kinds clean \
    --batch $KBATCH --read cand2 --tasks-v4-h1 $CV > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; exit 1; }
fi
.venv/bin/python scripts/nn_ko_read.py $r | cut -c1-400
echo "=== note 33 addendum $M done $(date -u +%FT%TZ)"
