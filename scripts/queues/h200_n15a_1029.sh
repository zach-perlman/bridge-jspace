#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 15 addendum): note 10's lens part against Dan's same-share random part, 9B MM.
# Usage: h200_n15a_1029.sh GPU WAITJOB
set -u
G=$1; WAIT=$2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1 BJ_TARGET=qwen3.5-9b
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 58 note 15 addendum)"
SET=jsuite_v4_test_chat; P=qwen35_9b_
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
CONDS="full_cf lens_cf rem_cf lensshr_cf remshr_cf"
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
sm=${P}nn_n15a_smoke1029
# shellcheck disable=SC2086
$PY scripts/nn_swap.py --name $sm --why "$W smoke" --set $SET --items v4ok --competence $C --cv-h1 $CV --words MM --site final --seed 0 \
  --band 21-24 --limit 2 --conds $CONDS > /workspace/scratch/$sm.log 2>&1 < /dev/null && grep -q '"remshr_cf"' results/nn_swap/$sm/rows.jsonl \
  || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
echo "=== smoke ok $(date -u +%T)"
fails=0; runs=""
while read -r site band; do
  for s in 0 1; do
    r=${P}nn_n15a_${site}_MM_L${band}_s${s}_v1
    runs="$runs $r"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: $site / MM / L$band, donor seed $s" --set $SET --items v4ok --competence $C --cv-h1 $CV \
      --words MM --site $site --seed $s --band $band --conds $CONDS > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done <<'CELLS'
final 21-24
final 25-28
last 4-7
last 8-11
last 12-16
CELLS
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_cf_read.py ${P}v4_n15a $runs > /workspace/scratch/${P}v4_n15a.txt 2>&1
echo "=== note 15a done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
