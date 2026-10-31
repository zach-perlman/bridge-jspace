#!/bin/bash
# Zach (2026-10-30, prereg amendment 68 note 45): which named word the J-space knock-out needs, on the paper's own
# lens-eval items (multilingual ML, multihop MH, order-of-operations OO descriptive). Usage: h200_n45_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Per model: a smoke (4 items per set, moved to /workspace/scratch/n45), then
#   scripts/paper_ko_decomp.py on every item (gate, ablate_v2's knock-out conditions at note 39's main band, keep / rm
#   spans, the early window = note 39's arm-1 median onset from <prefix>n39_v1, the byte-identity check), then the reader
#   (scripts/paper_ko_read.py -> /workspace/scratch/<prefix>note45.txt). BJ_GRAM_PROJ=1 as note 37's queue.
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
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 68 note 45, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
R=results/paper_ko_decomp
PREV=${P}n39_v1
[ -f results/paper_swap_decomp/$PREV/summary.json ] || { echo "=== note 39 run $PREV missing (the early window comes from it)"; exit 1; }
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== $R/$r $(date -u +%T)"
  if [ -f $R/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
sk=${P}n45_smoke1030
go $sk $PY scripts/paper_ko_decomp.py --name $sk --why "$W: smoke" --limit 4 --prev39 $PREV || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n45 && mv $R/$sk /workspace/scratch/n45/$sk-$(date -u +%H%M) 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
r=${P}n45_v1
go $r $PY scripts/paper_ko_decomp.py --name $r --why "$W: note 45" --prev39 $PREV
if [ -f $R/$r/summary.json ]; then
  .venv/bin/python scripts/paper_ko_read.py $R/$r > /workspace/scratch/${P}note45.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note45.txt; fails=$((fails + 1)); }
  grep -h "^reading\|^# note 45" /workspace/scratch/${P}note45.txt | cut -c1-400
fi
echo "=== n45 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
