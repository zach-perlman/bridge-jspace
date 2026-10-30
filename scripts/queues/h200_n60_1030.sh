#!/bin/bash
# Zach (2026-10-30, prereg amendment 85 note 60): outputs vs pivots on the paper's own tasks (paper_ko_decomp --n60, the
# note 55 path). Usage: h200_n60_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | nem35l | 27b
#   9B and Lightning: ML and MH (primary) and PO (rhyme, label-free keeps only, beside); 27B: MH (descriptive) and PO.
#   Bands: the paper's medium band (9B L17-24, 27B L35-49, Lightning L28-40) and, for MH, note 39's median-onset window
#   (from <prefix>n39_v1, as note 45). Conditions on paper10: rot, pcasize, keepT10 / keepRT10E, keep_T / E / I (ML),
#   keep_T / B (MH), keep_<X>perp / keepRE_<X>perp, keep_ctl (ctlE / ctlB), onlyT10 / onlyRT10E.
#   A smoke (4 items per set, moved to /workspace/scratch/n60), the full run, then scripts/paper_ko_read60.py appended to
#   /workspace/scratch/<prefix>note60.txt (its reading lines here). BJ_GRAM_PROJ=1 as notes 45 and 55.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; MED=17-24; SETS="ML MH PO" ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; MED=35-49; SETS="MH PO" ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; MED=28-40; SETS="ML MH PO" ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 85 note 60, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
R=paper_ko_decomp
PREV=${P}n39_v1
[ -f results/paper_swap_decomp/$PREV/summary.json ] || { echo "=== note 39 run $PREV missing (MH's early window comes from it)"; exit 1; }
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== $R/$r $(date -u +%T)"
  if [ -f results/$R/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
r=${P}n60_v1
mkdir -p /workspace/scratch/n60
if [ ! -f results/$R/$r/summary.json ]; then
  sk=${P}n60_smoke1030
  # shellcheck disable=SC2086
  go $sk $PY scripts/paper_ko_decomp.py --name $sk --why "$W: smoke" --n60 --sets $SETS --bands medium=$MED --prev39 $PREV --limit 4 \
    || { echo "=== smoke FAILED"; exit 1; }
  mv results/$R/$sk /workspace/scratch/n60/$sk-$(date -u +%H%M) 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
# shellcheck disable=SC2086
go $r $PY scripts/paper_ko_decomp.py --name $r --why "$W: note 60, outputs vs pivots on the paper's tasks" --n60 --sets $SETS \
  --bands medium=$MED --prev39 $PREV
if [ -f results/$R/$r/summary.json ]; then
  .venv/bin/python scripts/paper_ko_read60.py results/$R/$r > /workspace/scratch/${P}note60.part.txt 2>&1 \
    || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note60.part.txt; fails=$((fails + 1)); }
  { echo "=== $(date -u +%FT%TZ)"; cat /workspace/scratch/${P}note60.part.txt; } >> /workspace/scratch/${P}note60.txt
  grep -h "^reading\|^# note 60" /workspace/scratch/${P}note60.part.txt | cut -c1-500
fi
echo "=== n60 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
