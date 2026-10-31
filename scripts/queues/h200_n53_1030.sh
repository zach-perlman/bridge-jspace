#!/bin/bash
# Zach's session (2026-10-30, prereg amendment 72, note 53): note 39 with energy-matched controls (arm 7E, nested 5R2 / 5R4,
# arm 7 seeds 2 and 3, arms 1, 3 and 5 at every position but the final one), main band, J++. Usage:
#   h200_n53_1030.sh MODEL GPU [WAITJOB ...]     MODEL: 27b | 9b | nem35l | muse30 (Muse: descriptive)
# Per model, after note 39's run (<prefix>n39_v1) and its 5R run (<prefix>n39r_v1) have finished:
#   1. a 2-item smoke (moved to /workspace/scratch/n53)
#   2. the run on note 39's eligible primary items, two 12-row batches per item, arms 1, 3, 5, 7, 5R, the clean row and
#      the nulls checked against the stored rows: <prefix>n53_v1
#   3. the readings E1, E2, E3 and the arm-7 guard spread, appended to /workspace/scratch/<prefix>note53.txt
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
case $M in
  27b) export BJ_TARGET=qwen3.6-27b; P= ;;
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_ ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_ ;;
  muse30) export BJ_TARGET=muse-glimmer-30b; P=muse30_ ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 72 note 53, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
R=results/paper_swap_decomp
PREV=${P}n39_v1; PREV5R=${P}n39r_v1
for d in $PREV $PREV5R; do
  [ -f $R/$d/summary.json ] || { echo "=== $R/$d has no summary.json (not finished)"; exit 1; }
done
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== paper_swap_decomp/$r $(date -u +%T)"
  if [ -f $R/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
r=${P}n53_v1
if [ ! -f $R/$r/summary.json ]; then
  sk=${P}n53_smoke1030
  go $sk $PY scripts/paper_swap_n53.py --name $sk --why "$W: smoke" --prev $PREV --prev5r $PREV5R --limit 2 || { echo "=== smoke FAILED"; exit 1; }
  mkdir -p /workspace/scratch/n53 && mv $R/$sk /workspace/scratch/n53/$sk-$(date -u +%H%M) 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
go $r $PY scripts/paper_swap_n53.py --name $r --why "$W: note 53 run" --prev $PREV --prev5r $PREV5R
if [ -f $R/$r/summary.json ]; then
  O=/workspace/scratch/${P}note53.txt; T=/workspace/scratch/${P}note53.last
  .venv/bin/python scripts/paper_swap_read53.py $R/$PREV $R/$r > $T 2>&1 || { echo "=== read FAILED"; tail -5 $T; fails=$((fails + 1)); }
  { echo "##### $(date -u +%FT%TZ) $R/$r"; cat $T; } >> $O
  grep -h "^reading\|^stored\|^# note 53" $T | cut -c1-500
fi
echo "=== n53 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
