#!/bin/bash
# Zach (2026-10-29, prereg amendment 59 note 27): v4 with the question first. Usage: h200_qf_1029.sh MODEL GPU [WAITJOB ...]
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
W="Zach (2026-10-29, prereg amendment 59 note 27, $BJ_TARGET)"
SET=jsuite_v4qf_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
sm=${P}${SET}_competence_smoke1029
$PY scripts/natural_v1.py competence --set $SET --name $sm --words MP MM --read cand2 --hop1 gen --limit 8 --why "$W: smoke" \
  > /workspace/scratch/$sm.log 2>&1 < /dev/null || { echo "=== competence smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
mv results/tasks_v2/$sm /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
if [ ! -f results/tasks_v2/$C/summary.json ]; then
  $PY scripts/natural_v1.py competence --set $SET --name $C --words MP MM --read cand2 --hop1 gen --why "$W: competence, question first" \
    > /workspace/scratch/$C.log 2>&1 < /dev/null || { echo "=== $C FAILED"; tail -3 /workspace/scratch/$C.log; exit 1; }
fi
echo "=== done $C $(date -u +%T)"
r=${P}${SET}_ko_cand2_v1
if [ ! -f results/ablate_v2/$r/summary.json ]; then
  $PY scripts/ablate_v2.py --name $r --why "$W: note 20's knock-out, question first" --plan bands --bands $KB \
    --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word \
    --tasks-level all --n 1000 --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 $CV > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
fi
echo "=== done $r $(date -u +%T)"
r=${P}nn_readout_v4qf_prime_v1
if [ ! -f results/nn_readout/$r/summary.json ]; then
  $PY scripts/nn_readout.py --name $r --set $SET --competence $C --cv-h1 $CV --items v4 --priming \
    > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
fi
echo "=== done $r $(date -u +%T)"
.venv/bin/python scripts/nn_priming_read.py "$P" $r v4qf > /workspace/scratch/${P}v4qf_n25.txt 2>&1 || fails=$((fails + 1))
.venv/bin/python scripts/nn_order_read.py "$P" > /workspace/scratch/${P}v4qf_n27.txt 2>&1 || { echo "=== order read FAILED"; tail -5 /workspace/scratch/${P}v4qf_n27.txt; fails=$((fails + 1)); }
grep -h "reading" /workspace/scratch/${P}v4qf_n27.txt
echo "=== note 27 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
