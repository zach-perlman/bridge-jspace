#!/bin/bash
# Prereg amendment 88 note 65 and its addendum (2026-10-30): generate vs verify a single claim, same facts, one knock-out.
# Person-birthcity-cntry, test split. Usage: h200_n65_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 27b (primary) | 9b | nem35l (confirmatory). Waits for the WAITJOBs (^EXIT) and the model's known stage and gate. One
#   knock-out run of scripts/nn_sd_necessity.py on the test split's round-0-right person-birthcity-cntry items: conversations solo
#   (G), ver_true / ver_false (V+ / V-: "Claim: ... Is the claim correct? Answer Yes or No.", d = logit " Yes" - logit " No")
#   and choose_tf / choose_ft (C2, beside); mid band, all positions: paper10, paper10_rot, paper10_pcasize, unembed10, ansJ,
#   ansRe (note 57's energy-matched random, sized in ansJ's forward) and the unedited read; --gen (the unedited 12-token
#   outcome) and --gen-edited (12 tokens under every edit: the addendum's read on the 27B, and the generation fallback where a
#   cell's first-token agreement is < 90%; on by default for every model, N65_GEN_EDITED=0 turns it off for the 9B / Lightning).
#   An 8-item smoke first (moved to /workspace/scratch/n65). Then scripts/nn_sd65_read.py (gated as note 59), appended to
#   /workspace/scratch/{P}note65.txt; its reading lines go to this log. Run name {P}sd65_ko_test_v1.
#   Batches (N65_KBATCH / N65_GBATCH): 9B 32/64, Lightning 16/32, 27B 16/32.
#   GPU [E, from the 9B smoke]: see the builder's report.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32; GBATCH=64; GE=${N65_GEN_EDITED:-1} ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=16; GBATCH=32; GE=1 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; KBATCH=16; GBATCH=32; GE=${N65_GEN_EDITED:-1} ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
KBATCH=${N65_KBATCH:-$KBATCH}; GBATCH=${N65_GBATCH:-$GBATCH}
GEF=""; [ "$GE" = 1 ] && GEF="--gen-edited"
W="prereg amendment 88 note 65, generate vs verify (2026-10-30, $BJ_TARGET, test split)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
done
grep -q '"ver_true"' scripts/sd_prompts.py && grep -q 'gen-edited' scripts/nn_sd_necessity.py && [ -f scripts/nn_sd65_read.py ] \
  || { echo "=== the amendment 88 note 65 code is missing"; exit 1; }
S=/workspace/scratch/n65
mkdir -p $S
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > $S/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 $S/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONVS="solo ver_true ver_false choose_tf choose_ft"
EDITS="$KB:paper10,paper10_rot,paper10_pcasize,unembed10,ansJ,ansRe"
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  if [ -d results/sd_necessity/$r ] && [ ! -f results/sd_necessity/$r/summary.json ]; then  # a failed attempt: set aside
    mv results/sd_necessity/$r $S/$r.partial.$(date -u +%H%M%S) && echo "=== moved a partial $r to $S"
  fi
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split test --categories person-birthcity-cntry \
    --convs $CONVS --edits $EDITS --batch $KBATCH --gen --gen-batch $GBATCH $GEF --read-lenses jpp "$@"
}
rd() {  # rd RUN OUT: the note 65 reader
  .venv/bin/python scripts/nn_sd65_read.py $1 --gate $GT > $2 2>&1
}
SO=${P}sd65_ko_testsmoke1030; KO=${P}sd65_ko_test_v1
if [ ! -f results/sd_necessity/$KO/summary.json ]; then
  ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
  rd $SO $S/${SO}_read.txt || { echo "=== smoke read FAILED"; tail -5 $S/${SO}_read.txt; exit 1; }
  grep -h "validity" $S/${SO}_read.txt | cut -c1-300
  rm -rf $S/$SO; mv results/sd_necessity/$SO $S/ 2>/dev/null
  mv results/sd_necessity/nn_sd_read/${SO}_note65.json $S/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
ko $KO "G, V+, V-, C2 (test split, person-birthcity-cntry)" || { echo "=== $KO FAILED"; exit 1; }
OUT=/workspace/scratch/${P}note65.txt
if rd $KO $S/${KO}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $KO (scripts/nn_sd65_read.py, commit $(git rev-parse --short HEAD))"; cat $S/${KO}_read.txt; echo; } >> $OUT
  grep -h "^reading" $S/${KO}_read.txt | cut -c1-400
else
  echo "=== read FAILED"; tail -5 $S/${KO}_read.txt; fails=$((fails + 1))
fi
echo "=== n65 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
