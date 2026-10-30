#!/bin/bash
# Prereg amendment 85 note 62 (2026-10-30): a positive control for note 54's bridge null. Can bridgeJperp see a bridge where one is
# needed? Person-birthcity-cntry, test split. Usage: h200_n62_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | nem35l (primary) | 27b (if time). Waits for the WAITJOBs (^EXIT) and the model's known stage and gate. One
#   knock-out run of scripts/nn_sd_necessity.py on the test split's round-0-right person-birthcity-cntry items: conversations
#   ctx2hop (I: a fact list of 4 shuffled chains, a fictional person, then "In which country was X born?"), solo (P, note 54's
#   prompt) and onehop (O: "{C} is in the country of"); mid band: paper10, paper10_rot, bridgeJ, bridgeJ_rot, bridgeJ_ctrl
#   (count-matched, --ctrl-match count), bridgeJperp (in I orthogonalised to all 4 listed countries' forms), ansJ (+ the unedited
#   read); every edit only from the question's first token (--pos-from question); --gen (the unedited 12-token outcome). An
#   8-item smoke first (moved to /workspace/scratch/n62). Then scripts/nn_sd62_read.py (gated as note 54: gated with names as
#   written and no shortcut), appended to /workspace/scratch/{P}note62.txt; its reading lines go to this log.
#   Run name {P}sd62_ko_test_v1. Batches (N62_KBATCH / N62_GBATCH): 9B 32/64, Lightning 16/32, 27B 16/32.
#   GPU [E, from the 9B smoke and note 54 / 59 timings]: 9B ~8 min, Lightning ~15, 27B ~20.
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
KBATCH=${N62_KBATCH:-$KBATCH}; GBATCH=${N62_GBATCH:-$GBATCH}
W="prereg amendment 85 note 62, bridge positive control (2026-10-30, $BJ_TARGET, test split)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
done
grep -q '"ctx2hop"' scripts/sd_prompts.py && grep -q 'pos-from' scripts/nn_sd_necessity.py && [ -f scripts/nn_sd62_read.py ] \
  || { echo "=== the amendment 85 note 62 code is missing"; exit 1; }
S=/workspace/scratch/n62
mkdir -p $S
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > $S/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 $S/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONVS="ctx2hop solo onehop"
EDITS="$KB:paper10,paper10_rot,bridgeJ,bridgeJ_rot,bridgeJ_ctrl,bridgeJperp,ansJ"
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  if [ -d results/sd_necessity/$r ] && [ ! -f results/sd_necessity/$r/summary.json ]; then  # a failed attempt: set aside
    mv results/sd_necessity/$r $S/$r.partial.$(date -u +%H%M%S) && echo "=== moved a partial $r to $S"
  fi
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split test --categories person-birthcity-cntry \
    --convs $CONVS --edits $EDITS --pos-from question --ctrl-match count --batch $KBATCH --gen --gen-batch $GBATCH --read-lenses jpp "$@"
}
rd() {  # rd RUN OUT: the note 62 reader
  .venv/bin/python scripts/nn_sd62_read.py $1 --gate $GT > $2 2>&1
}
SO=${P}sd62_ko_testsmoke1030; KO=${P}sd62_ko_test_v1
if [ ! -f results/sd_necessity/$KO/summary.json ]; then
  ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
  rd $SO $S/${SO}_read.txt || { echo "=== smoke read FAILED"; tail -5 $S/${SO}_read.txt; exit 1; }
  grep -h "validity" $S/${SO}_read.txt | cut -c1-300
  rm -rf $S/$SO; mv results/sd_necessity/$SO $S/ 2>/dev/null
  mv results/sd_necessity/nn_sd_read/${SO}_note62.json $S/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
ko $KO "I, P and O (test split, person-birthcity-cntry; edits from the question's first token)" || { echo "=== $KO FAILED"; exit 1; }
OUT=/workspace/scratch/${P}note62.txt
if rd $KO $S/${KO}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $KO (scripts/nn_sd62_read.py, commit $(git rev-parse --short HEAD))"; cat $S/${KO}_read.txt; echo; } >> $OUT
  grep -h "^reading" $S/${KO}_read.txt | cut -c1-400
else
  echo "=== read FAILED"; tail -5 $S/${KO}_read.txt; fails=$((fails + 1))
fi
echo "=== n62 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
