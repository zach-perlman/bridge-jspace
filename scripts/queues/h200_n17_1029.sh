#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 17): value swap at the description end, 9B. Usage: h200_n17_1029.sh GPU
set -u
G=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1 BJ_TARGET=qwen3.5-9b
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 58 note 17)"
SET=jsuite_v4_test_chat; P=qwen35_9b_
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
sm=${P}nn_n17_smoke1029
$PY scripts/nn_swap.py --name $sm --why "$W smoke" --set $SET --items v4ok --competence $C --cv-h1 $CV --words MP MM --site last --seed 0 \
  --band 8-11 --limit 2 --value-swap --conds full_cf lensrand_cf > /workspace/scratch/$sm.log 2>&1 < /dev/null \
  || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
grep -E "jobs; by word|/(MP|MM)/" /workspace/scratch/$sm.log | head -8
echo "=== smoke ok $(date -u +%T)"
fails=0; runs=""
for s in 0 1; do
  for site in last span final; do
    case $site in last) B="4-7 8-11 12-16" ;; span) B="0-3 4-7 8-11 12-16" ;; final) B="21-24 25-28 29-30" ;; esac
    r=${P}nn_n17_${site}_s${s}_v1
    runs="$runs $r"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: value swap, site $site, donor seed $s" --set $SET --items v4ok --competence $C --cv-h1 $CV \
      --words MP MM --site $site --seed $s --sweep $B --value-swap --conds full_cf lensrand_cf > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done
# shellcheck disable=SC2086
{ .venv/bin/python scripts/nn_cf_read.py ${P}v4_n17 $runs; echo "--- all pairs (MM's reading)"; .venv/bin/python scripts/nn_cf_read.py ${P}v4_n17_all $runs --all-pairs; } > /workspace/scratch/${P}v4_n17.txt 2>&1
echo "=== note 17 done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
