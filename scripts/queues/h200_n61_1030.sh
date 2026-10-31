#!/bin/bash
# Zach (2026-10-30, prereg amendment 85 note 61): note 58 at 3 new windows (Lightning: windows holding an attention layer; 27B: the 9B
# crossover depths), machinery unchanged. Reader: scripts/nn_ko61_read.py if present (else read later from the stored run).
# Note 58 header follows. (2026-10-30, prereg amendment 84 note 58): the double dissociation with the unembedding dark space (DarkLens, Kuleshova et al.
# 2610.23182 §3.2) on v4 draw 4001's matched twins (MP lookup / MM recall), note 37's gate, band, batch and cand2 read (as note 41's
# run A): paper10 and paper10_rot rerun at the main band, and per 4-layer window (a: the main band's start; b: DarkLens's depth,
# ~55-64% of the layers) darkperm_W and its WikiText-NLL-matched mid-spectrum control midperm_W (calibrated in-run, n58_calib.json;
# W_U's spectrum cached in /workspace/scratch/n58). Then scripts/nn_ko58_read.py.
# Usage: h200_n61_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 27b | nem35l (9b: smoke only)
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32; WA=12-15; WB=17-20; WC=8-11 ;;  # smoke only
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=32; WA=19-22; WB=24-27; WC=28-31 ;;  # 64 layers; 30-35%, 38-43%, 44-49%
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; KBATCH=16; WA=24-27; WB=31-34; WC=17-20 ;;  # attention L26, L33, L19
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 85 note 61, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
SET=jsuite_v4_test_chat
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONDS="paper10 paper10_rot darkperm_L$WA midperm_L$WA darkperm_L$WB midperm_L$WB darkperm_L$WC midperm_L$WC"
ko() {  # ko RUN N WHY: note 20's knock-out command
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS \
    --tasks $SET --tasks-competence ${P}${SET}_competence_cand2_v1 --tasks-words MP MM --tasks-per-word --tasks-level all --n $n \
    --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 ${P}jsuite_v4_cv_v1
}
sk=${P}${SET}_ko61_smoke1030
ko $sk 2 "smoke" || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n61 && rm -rf /workspace/scratch/n61/$sk && mv results/ablate_v2/$sk /workspace/scratch/n61/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
[ "$M" = 9b ] && { echo "=== n61 9b smoke only, done $(date -u +%FT%TZ)"; exit 0; }
ko ${P}${SET}_ko61_cand2_v1 1000 "note 61: note 58 at L$WA, L$WB, L$WC, paper10 rerun, on v4 (MP vs MM)"
if [ -f scripts/nn_ko61_read.py ]; then
  .venv/bin/python scripts/nn_ko61_read.py results/ablate_v2/${P}${SET}_ko61_cand2_v1 "$P" >> /workspace/scratch/${P}note61.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note61.txt; fails=$((fails + 1)); }
  grep -h "^reading" /workspace/scratch/${P}note61.txt | tail -12 | cut -c1-600
else echo "=== reader not present; read later"; fi
echo "=== n61 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
