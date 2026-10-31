#!/bin/bash
# Zach (2026-10-30, prereg amendment 89 note 69): note 37 / 57's answer-direction battery at the description tokens only
# (--positions desc), v4 draw 4001, note 37's gate / band / batch / cand2 read (as h200_kopos_1029.sh); then scripts/nn_ko89_read.py.
# Usage: h200_n89c_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 27b (primary) | 9b
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=32 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 89 note 69, $BJ_TARGET)"
SET=jsuite_v4_test_chat; C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
CONDS="paper10 paper10_rot paper10_keepA paper10_keepA_rot ansJ ansJ_rot ansU paper10_onlyA paper10_onlyA_rot paper10_onlyRperp paper10_onlyRperp_rot ansRe ansRe_rot"
common="--plan bands --bands $KB --conditions $CONDS --keepA-forms every --topk-chunk 1024 --positions desc --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 $CV"
sk=${P}${SET}_ko69desc_smoke1030
echo "=== smoke $(date -u +%T)"
# shellcheck disable=SC2086
$PY scripts/ablate_v2.py --name $sk --why "$W smoke" --n 4 $common > /workspace/scratch/$sk.log 2>&1 < /dev/null \
  || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/$sk.log; exit 1; }
mkdir -p /workspace/scratch/n69 && rm -rf /workspace/scratch/n69/$sk && mv results/ablate_v2/$sk /workspace/scratch/n69/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
r=${P}${SET}_ko69desc_cand2_v1
if [ ! -f results/ablate_v2/$r/summary.json ]; then
  # shellcheck disable=SC2086
  $PY scripts/ablate_v2.py --name $r --why "$W: note 69, the answer battery at the description tokens" --n 1000 $common \
    > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -5 /workspace/scratch/$r.log; exit 1; }
fi
echo "=== done $r $(date -u +%T)"
O=/workspace/scratch/${P}note69.txt
.venv/bin/python scripts/nn_ko89_read.py "$P" > $O 2>&1 || { echo "=== read FAILED"; tail -5 $O; exit 1; }
grep -h "^reading\|MP loss\|energy matching" $O | cut -c1-600
echo "=== n69 $M done $(date -u +%FT%TZ)"
