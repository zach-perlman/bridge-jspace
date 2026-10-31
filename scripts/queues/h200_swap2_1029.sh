#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 17 27B addendum and note 18). Usage: h200_swap2_1029.sh MODE GPU WAITJOB MODEL
#   MODE value (note 17) or position (note 18); MODEL 27b or 9b
set -u
MODE=$1; G=$2; WAIT=$3; M=$4
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  27b) export BJ_TARGET=qwen3.6-27b; P=; BL="8-15 16-23 24-31 32-40"; BS="0-7 8-15 16-23 24-31 32-40"; BF="41-48 49-56 57-62"; SM=24-31 ;;
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; BL="4-7 8-11 12-16"; BS="0-3 4-7 8-11 12-16"; BF="21-24 25-28 29-30"; SM=8-11 ;;
esac
case $MODE in value) N=17; FLAG=--value-swap ;; position) N=18; FLAG=--position-swap ;; esac
W="Zach (2026-10-29, prereg amendment 58 note $N, $MODE swap)"
SET=jsuite_v4_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
sm=${P}nn_n${N}_smoke1029b
$PY scripts/nn_swap.py --name $sm --why "$W smoke" --set $SET --items v4ok --competence $C --cv-h1 $CV --words MP MM --site last --seed 0 \
  --band $SM --limit 2 $FLAG --conds full_cf lensrand_cf > /workspace/scratch/$sm.log 2>&1 < /dev/null \
  || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
grep -E "jobs; by word" /workspace/scratch/$sm.log
echo "=== smoke ok $(date -u +%T)"
fails=0; runs=""
for s in 0 1; do
  for site in last span final; do
    case $site in last) B=$BL ;; span) B=$BS ;; final) B=$BF ;; esac
    r=${P}nn_n${N}_${site}_s${s}_v1
    runs="$runs $r"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: site $site, donor seed $s" --set $SET --items v4ok --competence $C --cv-h1 $CV \
      --words MP MM --site $site --seed $s --sweep $B $FLAG --conds full_cf lensrand_cf > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done
# shellcheck disable=SC2086
{ .venv/bin/python scripts/nn_cf_read.py ${P}v4_n${N} $runs; echo "--- all pairs (MM's reading)"; .venv/bin/python scripts/nn_cf_read.py ${P}v4_n${N}_all $runs --all-pairs; } > /workspace/scratch/${P}v4_n${N}.txt 2>&1
echo "=== note $N ($MODE, $M) done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
