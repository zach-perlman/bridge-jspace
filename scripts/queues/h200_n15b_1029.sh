#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 15 addendum 2): own vs other answers, 27B. Usage: h200_n15b_1029.sh GPU WAITJOB
set -u
G=$1; WAIT=$2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1 BJ_TARGET=qwen3.6-27b
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 58 note 15 addendum 2)"
SET=jsuite_v4_test_chat; P=
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
CO="full_cf rem_cf remrand_cf remkeepown_cf noaown_cf noaownctl_cf remkeepoth_cf noaoth_cf noaothctl_cf"
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
until [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i $G)" -ge 76800 ]; do sleep 60; done
echo "=== GPU$G free $(date -u +%T)"
fails=0
# shellcheck disable=SC2086
$PY scripts/nn_swap.py --name nn_n15b_smoke1029 --why "$W smoke" --set $SET --items v4ok --competence $C --cv-h1 $CV --words MM --site final \
  --seed 0 --band 49-56 --limit 2 --conds $CO > /workspace/scratch/nn_n15b_smoke1029.log 2>&1 < /dev/null \
  || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/nn_n15b_smoke1029.log; exit 1; }
echo "=== smoke ok $(date -u +%T)"
runs=""
while read -r site band; do
  for s in 0 1; do
    r=nn_n15b_${site}_MM_L${band}_s${s}_v1; runs="$runs $r"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: $site / MM / L$band, donor seed $s" --set $SET --items v4ok --competence $C --cv-h1 $CV \
      --words MM --site $site --seed $s --band $band --conds $CO > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done <<'CELLS'
final 49-56
last 16-23
last 24-31
last 32-40
CELLS
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_cf_read.py v4_n15b $runs > /workspace/scratch/v4_n15b.txt 2>&1
echo "=== note 15b done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
