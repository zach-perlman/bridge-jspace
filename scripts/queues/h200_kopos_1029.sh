#!/bin/bash
# Zach (2026-10-29, prereg amendment 61 notes 32-33): v4 knock-out at the lookup's forming / formed bands, and at the main band
# restricted to the description or the final token. Usage: h200_kopos_1029.sh MODEL GPU [WAITJOB ...]
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; LATE="25-28 29-30"; KBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; LATE="49-56 57-62"; KBATCH=32 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; LATE="34-39 40-45"; KBATCH=16 ;;
esac
W="Zach (2026-10-29, prereg amendment 61, $BJ_TARGET)"
SET=jsuite_v4_test_chat; C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
common="--tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 $CV"
sk=${P}${SET}_kopos_smoke1029
# shellcheck disable=SC2086
$PY scripts/ablate_v2.py --name $sk --why "$W smoke" --plan bands --bands $KB --conditions paper10 paper10_rot --positions desc --n 4 $common \
  > /workspace/scratch/$sk.log 2>&1 < /dev/null || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/$sk.log; exit 1; }
mv results/ablate_v2/$sk /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
for B in $LATE; do
  r=${P}${SET}_ko_L${B}_cand2_v1
  if [ ! -f results/ablate_v2/$r/summary.json ]; then
    # shellcheck disable=SC2086
    $PY scripts/ablate_v2.py --name $r --why "$W: note 32, knock-out at L$B" --plan bands --bands $B \
      --conditions paper10 paper10_rot unembed10 paper10_pcasize --n 1000 $common > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
  fi
  .venv/bin/python scripts/nn_ko_read.py $r | cut -c1-400
  echo "=== done $r $(date -u +%T)"
done
for POS in desc final; do
  r=${P}${SET}_ko_pos${POS}_cand2_v1
  if [ ! -f results/ablate_v2/$r/summary.json ]; then
    # shellcheck disable=SC2086
    $PY scripts/ablate_v2.py --name $r --why "$W: note 33, knock-out at L$KB, positions $POS" --plan bands --bands $KB \
      --conditions paper10 paper10_rot --positions $POS --n 1000 $common > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
  fi
  .venv/bin/python scripts/nn_ko_read.py $r | cut -c1-400
  echo "=== done $r $(date -u +%T)"
done
echo "=== notes 32-33 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
