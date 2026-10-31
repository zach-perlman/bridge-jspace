#!/bin/bash
# Zach (2026-10-29, prereg amendment 59 note 26): what the J-space shows at the bridge (top-20 tokens; priming with no relation
# asked; priming on cue-conflict descriptions). Usage: h200_pack_1029.sh MODEL GPU [WAITJOB ...]
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
  muse) export BJ_TARGET=muse-glimmer-30b; P=muse30_ ;;
esac
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
C=${P}jsuite_v4_test_chat_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
CC=${P}jsuite_v4cc_test_chat_competence_cand2_v1; CCV=${P}jsuite_v4cc_cv_v1
fails=0
sm=${P}nn_readout_v4ctl_smoke1029
$PY scripts/nn_readout.py --name $sm --set jsuite_v4_test_chat --competence $C --cv-h1 $CV --items v4ctl --priming --topk 20 --limit 4 \
  > /workspace/scratch/$sm.log 2>&1 < /dev/null && [ -s results/nn_readout/$sm/topk.jsonl ] || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
grep -h "prompts; by family" /workspace/scratch/$sm.log
mv results/nn_readout/$sm /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
r=${P}nn_readout_v4ctl_v1
if [ ! -f results/nn_readout/$r/summary.json ]; then
  $PY scripts/nn_readout.py --name $r --set jsuite_v4_test_chat --competence $C --cv-h1 $CV --items v4ctl --priming --topk 20 \
    > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
fi
echo "=== done $r $(date -u +%T)"
r=${P}nn_readout_v4cc_v1
if [ -f results/tasks_v2/$CC/summary.json ] && [ -f results/competence_variants/$CCV/summary.json ]; then
  if [ ! -f results/nn_readout/$r/summary.json ]; then
    $PY scripts/nn_readout.py --name $r --set jsuite_v4cc_test_chat --competence $CC --cv-h1 $CCV --items v4cc --priming --topk 20 \
      > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
  fi
  echo "=== done $r $(date -u +%T)"
else
  echo "=== no cue-conflict competence for $M: (c) skipped"
fi
.venv/bin/python scripts/nn_bridge_read.py "$P" > /workspace/scratch/${P}v4_n26.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}v4_n26.txt; fails=$((fails + 1)); }
echo "=== note 26 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
