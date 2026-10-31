#!/bin/bash
# Zach (2026-10-30, prereg amendment 64 note 37): answer kept vs answer only on v4. Usage: h200_n37_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Per model: note 20's knock-out exactly (its band, --tasks-per-word --tasks-level all --n 1000,
#   kinds clean, the model's batch, cand2, v4_split's gate) under paper10_keepA, paper10_keepA_rot, ansJ, ansJ_rot, ansU, with
#   paper10 and paper10_rot rerun in the same run (keepA is compared with them within one run; the reader checks them against
#   note 20's stored rows); the same on jsuite_v4cc (descriptive); the reader (scripts/nn_ko37_read.py).
#   The 9B's smoke (8 items per word before the gate) ran by hand before this queue (job ...-n37smoke-1030-0518, moved to
#   /workspace/scratch/n37); the 27B and Lightning run a 2-item smoke first. Queued after notes 34-35 on each GPU.
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
W="Zach (2026-10-30, prereg amendment 64 note 37, $BJ_TARGET)"
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
CONDS="paper10 paper10_rot paper10_keepA paper10_keepA_rot ansJ ansJ_rot ansU"
ko() {  # ko SET CV RUN N WHY: note 20's knock-out command with note 37's conditions
  local SET=$1 CV=$2 r=$3 n=$4 why=$5
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --keepA-forms every \
    --tasks $SET --tasks-competence ${P}${SET}_competence_cand2_v1 --tasks-words MP MM --tasks-per-word --tasks-level all --n $n \
    --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 $CV
}
if [ "$M" != 9b ]; then
  sk=${P}jsuite_v4_test_chat_ko37_smoke1030
  ko jsuite_v4_test_chat ${P}jsuite_v4_cv_v1 $sk 2 "smoke" || { echo "=== smoke FAILED"; exit 1; }
  mkdir -p /workspace/scratch/n37 && mv results/ablate_v2/$sk /workspace/scratch/n37/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
ko jsuite_v4_test_chat ${P}jsuite_v4_cv_v1 ${P}jsuite_v4_test_chat_ko37_cand2_v1 1000 "note 37, answer kept vs answer only on v4 (MP vs MM)"
ko jsuite_v4cc_test_chat ${P}jsuite_v4cc_cv_v1 ${P}jsuite_v4cc_test_chat_ko37_cand2_v1 1000 "note 37 on the cue-conflict set (descriptive)"
.venv/bin/python scripts/nn_ko37_read.py "$P" > /workspace/scratch/${P}note37.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note37.txt; fails=$((fails + 1)); }
grep -h "reading\|stored check" /workspace/scratch/${P}note37.txt | cut -c1-400
echo "=== n37 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
