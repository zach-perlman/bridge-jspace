#!/bin/bash
# Zach (2026-10-30, prereg amendment 69 note 46): notes 37 and 41 on the codename set jsuite_v5al. Usage: h200_n46_1030.sh MODEL GPU [WAITJOB ...]
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
W="Zach (2026-10-30, prereg amendment 69 note 46, $BJ_TARGET)"
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
SET=jsuite_v5al_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v5alctl_cv_v1; R=${P}${SET}_ko37_cand2_v1
mkdir -p /workspace/scratch/n46
if [ ! -f results/tasks_v2/$C/summary.json ] || [ ! -f results/competence_variants/$CV/summary.json ]; then echo "=== no alias competence for $M"; exit 1; fi
CONDS="paper10 paper10_rot paper10_keepA paper10_keepA_rot ansJ ansJ_rot ansU paper10_keepR paper10_keepR_rot paper10_keepR2 paper10_keepR2_rot paper10_keepR4 paper10_keepR4_rot ansR ansR_rot"
ko() {  # ko RUN N WHY
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --keepA-forms every \
    --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --n $n --kinds clean --batch $KBATCH \
    --read cand2 --tasks-v4-h1 $CV
}
sk=${P}${SET}_ko37_smoke1030
ko $sk 2 "smoke" || { echo "=== knock-out smoke FAILED"; exit 1; }
mv results/ablate_v2/$sk /workspace/scratch/n46/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko $R 1000 "note 46, notes 37 and 41 on the codename set jsuite_v5al"
: > /workspace/scratch/${P}note46.txt
rd() { "$@" >> /workspace/scratch/${P}note46.txt 2>&1 || { echo "=== read FAILED: $*"; tail -5 /workspace/scratch/${P}note46.txt; fails=$((fails + 1)); }; }
rd .venv/bin/python scripts/nn_ko37_read.py "$P" --set $SET
rd .venv/bin/python scripts/nn_ko41_read.py "$P" --set $SET --run-a $R --run-n37 $R
grep -h "reading" /workspace/scratch/${P}note46.txt | cut -c1-400
echo "=== n46 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
