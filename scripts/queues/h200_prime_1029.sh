#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 25): priming at the bridge. Usage: h200_prime_1029.sh MODEL GPU WAITJOB [WAITJOB ...]
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_ ;;
  27b) export BJ_TARGET=qwen3.6-27b; P= ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_ ;;
esac
SET=jsuite_v4_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1; R=${P}nn_readout_v4prime_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
sm=${P}nn_readout_v4prime_smoke1029
$PY scripts/nn_readout.py --name $sm --set $SET --competence $C --cv-h1 $CV --items v4 --priming --limit 8 \
  > /workspace/scratch/$sm.log 2>&1 < /dev/null || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
.venv/bin/python scripts/nn_priming_read.py "$P" $sm > /workspace/scratch/${sm}_read.log 2>&1 || { echo "=== smoke read FAILED"; tail -5 /workspace/scratch/${sm}_read.log; exit 1; }
mv results/nn_readout/$sm /workspace/scratch/ 2>/dev/null
mv results/nn_readout/nn_priming_read/${P}v4_n25.json /workspace/scratch/${sm}_n25.json 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
if [ ! -f results/nn_readout/$R/summary.json ]; then
  $PY scripts/nn_readout.py --name $R --set $SET --competence $C --cv-h1 $CV --items v4 --priming \
    > /workspace/scratch/$R.log 2>&1 < /dev/null || { echo "=== $R FAILED"; tail -5 /workspace/scratch/$R.log; exit 1; }
fi
echo "=== done $R $(date -u +%T)"
.venv/bin/python scripts/nn_priming_read.py "$P" > /workspace/scratch/${P}v4_n25.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}v4_n25.txt; exit 1; }
tail -1 /workspace/scratch/${P}v4_n25.txt
echo "=== note 25 $M done $(date -u +%FT%TZ)"
