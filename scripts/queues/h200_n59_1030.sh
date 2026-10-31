#!/bin/bash
# Prereg amendment 84 note 59 (2026-10-30): safety-relevant agent settings with note 56 / 56c machinery (person-birthcity-cntry):
# K token presence (instr_city, instr_city_seen, instr_city_lure, instr_vis), A arbiter (judge_ft, judge_tf, judge_ver), B user
# sycophancy (syc_wrong, syc_right, syc_doubt, tool_wrong), plus solo (G1 in-run). Usage: [N59_SPLIT=dev] h200_n59_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b (test and dev primary) | nem35l (confirmatory) | 27b (descriptive). Waits for the WAITJOBs (^EXIT) and the model's known
#   stage and gate. One knock-out run of scripts/nn_sd_necessity.py on the split's round-0-right items of person-birthcity-cntry,
#   mid band: paper10, paper10_rot, paper10_pcasize, unembed10, paper10_keepA, ansJ, ansJ_rot (+ the unedited read); --gen (the
#   unedited 12-token outcome, for validity) and --log-prot. An 8-item smoke first (moved to /workspace/scratch/n59). Then
#   scripts/nn_sd_ma1_read.py --note59 (gated, names as written; note 56's peer-name filter), appended to
#   /workspace/scratch/{P}note59.txt; its reading lines go to this log. Run name {P}sd59_ko_{split}_v1.
#   Batches (N59_KBATCH / N59_GBATCH): 9B 32/64, Lightning 16/32, 27B 16/32.
#   GPU [E]: 9B test ~35 min (350 items x 12 conversations x 8 forwards), dev ~22; Lightning ~45; 27B ~100.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32; GBATCH=64 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=16; GBATCH=32 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; KBATCH=16; GBATCH=32 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
KBATCH=${N59_KBATCH:-$KBATCH}; GBATCH=${N59_GBATCH:-$GBATCH}
SPLIT=${N59_SPLIT:-test}
W="prereg amendment 84 note 59, agent safety settings (2026-10-30, $BJ_TARGET, $SPLIT split)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
done
grep -q '"judge_ft"' scripts/sd_prompts.py && grep -q 'control=c' scripts/nn_sd_necessity.py || { echo "=== the amendment 84 code is missing"; exit 1; }
S=/workspace/scratch/n59
mkdir -p $S
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > $S/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 $S/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONVS="solo instr_city instr_city_seen instr_city_lure instr_vis judge_ft judge_tf judge_ver syc_wrong syc_right syc_doubt tool_wrong"
EDITS="$KB:paper10,paper10_rot,paper10_pcasize,unembed10,paper10_keepA,ansJ,ansJ_rot"
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  if [ -d results/sd_necessity/$r ] && [ ! -f results/sd_necessity/$r/summary.json ]; then  # a failed attempt: set aside
    mv results/sd_necessity/$r $S/$r.partial.$(date -u +%H%M%S) && echo "=== moved a partial $r to $S"
  fi
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split $SPLIT --categories person-birthcity-cntry \
    --convs $CONVS --edits $EDITS --batch $KBATCH --gen --gen-batch $GBATCH --log-prot --read-lenses jpp "$@"
}
rd() {  # rd RUN OUT: the note 59 reader
  .venv/bin/python scripts/nn_sd_ma1_read.py $1 --note59 --gate $GT --name-rule canonical > $2 2>&1
}
SO=${P}sd59_ko_${SPLIT}smoke1030; KO=${P}sd59_ko_${SPLIT}_v1
ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
rd $SO $S/${SO}_read.txt || { echo "=== smoke read FAILED"; tail -5 $S/${SO}_read.txt; exit 1; }
grep -h "validity" $S/${SO}_read.txt | cut -c1-300
rm -rf $S/$SO; mv results/sd_necessity/$SO $S/ 2>/dev/null
mv results/sd_necessity/nn_sd_read/${SO}_note59.json $S/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko $KO "K, A, B and solo ($SPLIT split, person-birthcity-cntry)" || { echo "=== $KO FAILED"; exit 1; }
OUT=/workspace/scratch/${P}note59.txt
if rd $KO $S/${KO}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $KO (scripts/nn_sd_ma1_read.py --note59, commit $(git rev-parse --short HEAD))"; cat $S/${KO}_read.txt; echo; } >> $OUT
  grep -h "^reading" $S/${KO}_read.txt | cut -c1-400
else
  echo "=== read FAILED"; tail -5 $S/${KO}_read.txt; fails=$((fails + 1))
fi
echo "=== n59 $M ($SPLIT) done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
