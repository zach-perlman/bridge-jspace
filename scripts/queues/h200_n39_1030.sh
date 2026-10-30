#!/bin/bash
# Zach (2026-10-30, prereg amendment 65 note 39): the paper's 90 two-hop prompts (data/probe_swap.json), the intermediate
# swap decomposed into the answer category's J-directions and the rest. Usage: h200_n39_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 27b | 9b | nem35l | muse30 (Muse: descriptive). Per model: a 2-item smoke (moved to /workspace/scratch/n39),
#   then scripts/paper_swap_decomp.py on all 90 items (arms 1-9 at the cumulative windows and the main band, greedy check
#   at the main band; vocabularies data/paper_answer_types.json, sha256-pinned in the script), then the reader
#   (scripts/paper_swap_read.py -> /workspace/scratch/<prefix>note39.txt). The 27B's run is gated on the A0 reproduction:
#   arm 1 at L24-40 (J++) must land inside exp02 main_v4_jpp's 95% interval on the shared items (repro.json), checked
#   before any window runs; the run stops otherwise.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
case $M in
  27b) export BJ_TARGET=qwen3.6-27b; P=; GATE=--repro-gate ;;
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; GATE= ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; GATE= ;;
  muse30) export BJ_TARGET=muse-glimmer-30b; P=muse30_; GATE= ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 65 note 39, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
sk=${P}n39_smoke1030
go paper_swap_decomp $sk $PY scripts/paper_swap_decomp.py --name $sk --why "$W: smoke" --items amazon-language animal-cover-turtle \
  --n-windows 1 --prompt-end stripped || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n39 && mv results/paper_swap_decomp/$sk /workspace/scratch/n39/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
r=${P}n39_v1
# shellcheck disable=SC2086
go paper_swap_decomp $r $PY scripts/paper_swap_decomp.py --name $r --why "$W: note 39, the paper's prompts decomposed" $GATE
if [ -f results/paper_swap_decomp/$r/repro.json ]; then
  echo "=== A0 reproduction: $(.venv/bin/python -c "import json; d=json.load(open('results/paper_swap_decomp/$r/repro.json')); print('reproduced', d['reproduced'], json.dumps(d['real']))")"
fi
if [ -f results/paper_swap_decomp/$r/summary.json ]; then
  .venv/bin/python scripts/paper_swap_read.py results/paper_swap_decomp/$r > /workspace/scratch/${P}note39.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note39.txt; fails=$((fails + 1)); }
  grep -h "^reading\|^# note 39" /workspace/scratch/${P}note39.txt | cut -c1-400
fi
echo "=== n39 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
