#!/bin/bash
# Zach (2026-10-30, prereg amendment 67 note 41 + addendum): note 37's random-span placebo and output-side check on v4.
# Usage: h200_n41_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
#   Run A: note 20's knock-out exactly (its band, --tasks-per-word --tasks-level all --n 1000, kinds clean, the model's batch,
#   cand2, v4_split's gate) under paper10, paper10_rot, paper10_keepR / R2 / R4 (+ _rot) and ansR / ansR_rot, --keepA-forms
#   every (R's row count and exclusions follow note 37's A); its paper10 rows log the retained removal energy (A, R, R2, R4).
#   Run B: the same with --positions final under paper10, paper10_rot, ansJ, ansJ_rot. Then scripts/nn_ko41_read.py, which
#   also reads note 37's stored run ({P}jsuite_v4_test_chat_ko37_cand2_v1; this queue stops if it is missing).
#   The 9B's smokes ran by hand (jobs ...-n41smoke-1030-0813 and -0816b, in /workspace/scratch/n41); the 27B and Lightning
#   run a 2-item smoke of run A first.
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
W="Zach (2026-10-30, prereg amendment 67 note 41 + addendum, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
SET=jsuite_v4_test_chat
if [ ! -f results/ablate_v2/${P}${SET}_ko37_cand2_v1/summary.json ]; then echo "=== note 37's run ${P}${SET}_ko37_cand2_v1 missing"; exit 1; fi
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONDS_A="paper10 paper10_rot paper10_keepR paper10_keepR_rot paper10_keepR2 paper10_keepR2_rot paper10_keepR4 paper10_keepR4_rot ansR ansR_rot"
CONDS_B="paper10 paper10_rot ansJ ansJ_rot"
ko() {  # ko RUN N WHY CONDITIONS [EXTRA ARGS...]: note 20's knock-out command
  local r=$1 n=$2 why=$3 conds=$4; shift 4
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $conds "$@" \
    --tasks $SET --tasks-competence ${P}${SET}_competence_cand2_v1 --tasks-words MP MM --tasks-per-word --tasks-level all --n $n \
    --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 ${P}jsuite_v4_cv_v1
}
if [ "$M" != 9b ]; then
  sk=${P}${SET}_ko41_smoke1030
  ko $sk 2 "smoke" "$CONDS_A" --keepA-forms every || { echo "=== smoke FAILED"; exit 1; }
  mkdir -p /workspace/scratch/n41 && mv results/ablate_v2/$sk /workspace/scratch/n41/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
ko ${P}${SET}_ko41_cand2_v1 1000 "note 41 run A, random kept / removed spans (R, R2, R4) on v4 (MP vs MM)" "$CONDS_A" --keepA-forms every
ko ${P}${SET}_ko41_posfinal_cand2_v1 1000 "note 41 run B, ansJ at the final token only" "$CONDS_B" --positions final
.venv/bin/python scripts/nn_ko41_read.py "$P" > /workspace/scratch/${P}note41.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note41.txt; fails=$((fails + 1)); }
grep -h "reading\|removal:\|output side:\|stored check" /workspace/scratch/${P}note41.txt | cut -c1-400
echo "=== n41 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
