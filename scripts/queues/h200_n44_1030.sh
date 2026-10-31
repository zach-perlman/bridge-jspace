#!/bin/bash
# Zach (2026-10-30, prereg amendment 68 note 44): answer or intermediate on the closed-book capital question (jsuite_v5kn2c MC0;
# MC and the kn2 say twin as references). Usage: h200_n44_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
#   Note 35's knock-out exactly (its band, --tasks-per-word --tasks-level all --n 1000, kinds clean step2, the model's batch,
#   cand2, v4_split's gate on jsuite_v5kn2cctl) on MC MC0 under paper10, paper10_rot (rerun in-run), paper10_keepCap,
#   paper10_keepCty, paper10_keepCapCty, paper10_keepRcap (after paper10: its size is set in paper10's forward), ansCap, ansCty,
#   ansCty_rot; the same conditions on the kn2 say twin (MM, kind clean, its v5key2 gate); then scripts/nn_ko44_read.py.
#   The 9B's smokes ran by hand (job ...-n44smoke-1030-0831, in /workspace/scratch/n44); the 27B and Lightning run a 2-item
#   smoke first.
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
W="Zach (2026-10-30, prereg amendment 68 note 44, $BJ_TARGET)"
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
MC=jsuite_v5kn2c_test_chat; KN=jsuite_v5kn2_test_chat
CONDS="paper10 paper10_rot paper10_keepCap paper10_keepCty paper10_keepCapCty paper10_keepRcap ansCap ansCty ansCty_rot"
ko() {  # ko SET WORDS KINDS CV RUN N WHY
  local set=$1 words=$2 kinds=$3 cv=$4 r=$5 n=$6 why=$7
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --tasks $set \
    --tasks-competence ${P}${set}_competence_cand2_v1 --tasks-words $words --tasks-per-word --tasks-level all --n $n --kinds $kinds \
    --batch $KBATCH --read cand2 --tasks-v4-h1 $cv
}
if [ "$M" != 9b ]; then
  sk=${P}${MC}_ko44_smoke1030
  ko $MC "MC MC0" "clean step2" ${P}jsuite_v5kn2cctl_cv_v1 $sk 2 "smoke" || { echo "=== smoke FAILED"; exit 1; }
  mkdir -p /workspace/scratch/n44 && mv results/ablate_v2/$sk /workspace/scratch/n44/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
ko $MC "MC MC0" "clean step2" ${P}jsuite_v5kn2cctl_cv_v1 ${P}${MC}_ko44_cand2_v1 1000 "note 44, capitals vs countries kept / removed (MC0, MC)"
ko $KN MM clean ${P}jsuite_v5kn2ctl_cv_v1 ${P}${KN}_ko44_cand2_v1 1000 "note 44, the kn2 say twin (MM) under the same conditions"
.venv/bin/python scripts/nn_ko44_read.py "$P" > /workspace/scratch/${P}note44.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note44.txt; fails=$((fails + 1)); }
grep -h "note 44\|ans\*" /workspace/scratch/${P}note44.txt | cut -c1-400
echo "=== n44 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
