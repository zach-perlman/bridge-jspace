#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 notes 19-20): resample ablation and the knock-out on v4, 9B. Usage: h200_abl_1029.sh GPU WAITJOB
set -u
G=$1; WAIT=$2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1 BJ_TARGET=qwen3.5-9b
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 58 notes 19-20)"
SET=jsuite_v4_test_chat; P=qwen35_9b_
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
sm=${P}nn_n19_smoke1029
$PY scripts/nn_swap.py --name $sm --why "$W smoke" --set $SET --items v4ok --competence $C --cv-h1 $CV --words MP MM --site last --seed 0 \
  --band 8-11 --limit 2 --resample --conds full_cf lensrand_cf > /workspace/scratch/$sm.log 2>&1 < /dev/null \
  || { echo "=== n19 smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
grep -E "jobs; by word" /workspace/scratch/$sm.log
sk=${P}${SET}_ko_smoke1029
$PY scripts/ablate_v2.py --name $sk --why "$W smoke" --plan bands --bands 12-16 --conditions paper10 paper10_rot --tasks $SET \
  --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --n 4 --kinds clean --batch 8 --read cand2 --tasks-v4-h1 $CV \
  > /workspace/scratch/$sk.log 2>&1 < /dev/null || { echo "=== n20 smoke FAILED"; tail -5 /workspace/scratch/$sk.log; exit 1; }
grep -E "note 20" /workspace/scratch/$sk.log
mv results/ablate_v2/$sk /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
r=${P}${SET}_ko_cand2_v1
if [ ! -f results/ablate_v2/$r/summary.json ]; then
  $PY scripts/ablate_v2.py --name $r --why "$W: note 20, the knock-out on v4 (MP vs MM), breadth band" --plan bands --bands 12-16 \
    --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word \
    --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2 --tasks-v4-h1 $CV > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
  echo "=== note 20 done $(date -u +%T)"
fi
runs=""
for s in 0 1; do
  for site in last span final; do
    case $site in last) B="4-7 8-11 12-16" ;; span) B="0-3 4-7 8-11 12-16" ;; final) B="21-24 25-28" ;; esac
    r=${P}nn_n19_${site}_s${s}_v1; runs="$runs $r"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: note 19, resample, site $site, donor seed $s" --set $SET --items v4ok --competence $C --cv-h1 $CV \
      --words MP MM --site $site --seed $s --sweep $B --resample --conds full_cf lensrand_cf > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_cf_read.py ${P}v4_n19 $runs --all-pairs > /workspace/scratch/${P}v4_n19.txt 2>&1
echo "=== notes 19-20 done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
