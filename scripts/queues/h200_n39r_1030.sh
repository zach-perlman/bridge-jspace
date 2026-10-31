#!/bin/bash
# Zach (2026-10-30, prereg amendment 67, note 39 arm 5R): a random-projection control for note 39's sufficiency. Usage:
#   h200_n39r_1030.sh MODEL GPU [WAITJOB ...]     MODEL: 27b | 9b | nem35l | muse30 (Muse: descriptive)
# Per model, after note 39's run (results/paper_swap_decomp/<prefix>n39_v1) has finished:
#   1. a 2-item smoke (moved to /workspace/scratch/n39r)
#   2. the rerun: arms 1, 5, 5R and the nulls of arms 1 and 5 on the primary items, at the main band and at arm 1's
#      median-onset window, batches padded to note 39's shape, checked against the stored rows: <prefix>n39r_v1
#   3. the reading (sufficiency answer-specific or not; without capital/language/country items, descriptive)
#      -> /workspace/scratch/<prefix>note39r.txt
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
W="Zach (2026-10-30, prereg amendment 67 note 39 arm 5R, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
R=results/paper_swap_decomp
PREV=${P}n39_v1
[ -f $R/$PREV/summary.json ] || { echo "=== $R/$PREV has no summary.json (note 39 not finished)"; exit 1; }
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== paper_swap_decomp/$r $(date -u +%T)"
  if [ -f $R/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
sk=${P}n39r_smoke1030
go $sk $PY scripts/paper_swap_5r.py --name $sk --why "$W: smoke" --prev $PREV --limit 2 || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n39r && mv $R/$sk /workspace/scratch/n39r/$sk-$(date -u +%H%M) 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
r=${P}n39r_v1
go $r $PY scripts/paper_swap_5r.py --name $r --why "$W: arm 5R rerun" --prev $PREV
if [ -f $R/$r/summary.json ]; then
  .venv/bin/python scripts/paper_swap_read5r.py $R/$PREV $R/$r > /workspace/scratch/${P}note39r.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note39r.txt; fails=$((fails + 1)); }
  grep -h "^reading\|^stored\|^# note 39" /workspace/scratch/${P}note39r.txt | cut -c1-400
fi
echo "=== n39r $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
