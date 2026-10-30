#!/bin/bash
# Zach (2026-10-30, prereg amendment 72 note 51): dose x keepA on v4 seed 4001 (jsuite_v4_test_chat): top30 and top100, each with
# _rot, _pcasize, _keepA and _keepA_rot, plus paper10 / paper10_rot rerun in-run; note 20's knock-out exactly (as note 41's run A).
# topK carries paper10's protection (the clean top-10 letter rows; checked in the 9B smoke). --topk-chunk 1024: rows per chunk for the
# K > 10 removals (memory at K = 100; rows are independent). keeplog.jsonl logs E_A at each K. Then scripts/nn_ko51_read.py.
# Usage: h200_n51_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
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
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 72 note 51, $BJ_TARGET)"
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
CONDS="paper10 paper10_rot"
for k in 30 100; do CONDS="$CONDS top$k top${k}_rot top${k}_pcasize top${k}_keepA top${k}_keepA_rot"; done
ko() {  # ko RUN N WHY: note 20's knock-out command
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --keepA-forms every \
    --topk-chunk 1024 --tasks $SET --tasks-competence ${P}${SET}_competence_cand2_v1 --tasks-words MP MM --tasks-per-word --tasks-level all \
    --n $n --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 ${P}jsuite_v4_cv_v1
}
sk=${P}${SET}_ko51_smoke1030
ko $sk 2 "smoke" || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n49 && rm -rf /workspace/scratch/n49/$sk && mv results/ablate_v2/$sk /workspace/scratch/n49/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko ${P}${SET}_ko51_cand2_v1 1000 "note 51: dose x keepA (K = 30, 100) on v4 (MP vs MM)"
.venv/bin/python scripts/nn_ko51_read.py "$P" >> /workspace/scratch/${P}note51.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note51.txt; fails=$((fails + 1)); }
grep -h "^reading\|K = 10 beside\|stored check" /workspace/scratch/${P}note51.txt | tail -6 | cut -c1-600
echo "=== n51 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
