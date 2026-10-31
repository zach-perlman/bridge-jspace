#!/bin/bash
# Prereg amendment 73 note 56 (2026-10-30): copy or compute, the silent-dissent transcript extended. Usage: h200_n56_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Waits for the WAITJOBs (their log's ^EXIT) and for the model's known stage and gate ({P}sd_known_v1,
#   {P}sd_gate_v1). Then scripts/nn_sd_necessity.py ko on the test split (note 40's known items, round 0 right), conversations
#   instr_vis hyp_vis prem_vis prem_hid press_vis (sd_prompts.CONVS; press_vis = note 40's, the reference), mid band only (no late
#   band edits) with paper10, paper10_rot, paper10_pcasize, unembed10, paper10_keepA, ansJ, bridgeJ_ctrl, bridgeJ_peer, --gen (their
#   12-token outcome, unedited), J++ read every 2nd layer plus the late band (D1's readout): an 8-item smoke first (moved to
#   /workspace/scratch/n56), then the run, then scripts/nn_sd_ma1_read.py (gated with names as written, the peer-name filter;
#   D1's solo rows from the model's note 40 run {P}sd_ko_test_v1 if it exists; otherwise D1 reads "not read" and the reader can be
#   rerun later). The reader's output is appended to /workspace/scratch/{P}note56.txt and its reading lines go to this log.
#   Batches (env N56_KBATCH / N56_GBATCH override): 9B 32/64, Lightning 16/32, 27B 16/32 (note 40's 27B relaunch).
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; LB=26-29; KBATCH=32; GBATCH=64 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; LB=52-55; KBATCH=16; GBATCH=32 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; LB=42-45; KBATCH=16; GBATCH=32 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
KBATCH=${N56_KBATCH:-$KBATCH}; GBATCH=${N56_GBATCH:-$GBATCH}
W="prereg amendment 73 note 56, copy or compute (2026-10-30, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1; MAIN=${P}sd_ko_test_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
done
grep -q '"bridgeJ_peer"' scripts/nn_sd_necessity.py || { echo "=== the runner has no bridgeJ_peer edit (SD runner's commit missing)"; exit 1; }
mkdir -p /workspace/scratch/n56
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/n56/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/n56/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONVS="instr_vis hyp_vis prem_vis prem_hid press_vis"
EDITS="$KB:paper10,paper10_rot,paper10_pcasize,unembed10,paper10_keepA,ansJ,bridgeJ_ctrl,bridgeJ_peer"
LBL=$(seq -s' ' ${LB%-*} ${LB#*-})  # the late band's layers, read beside every 2nd layer (D1)
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split test --convs $CONVS --edits $EDITS \
    --batch $KBATCH --gen --gen-batch $GBATCH --read-lenses jpp --read-extra $LBL "$@"
}
rd() {  # rd RUN OUT: the note 56 reader (D1's solo rows from note 40's run if it exists)
  local solo=""
  [ -f results/sd_necessity/$MAIN/summary.json ] && solo="--solo-run $MAIN"
  # shellcheck disable=SC2086
  .venv/bin/python scripts/nn_sd_ma1_read.py $1 --gate $GT --name-rule canonical --late $LBL $solo > $2 2>&1
}
SO=${P}sd56_ko_smoke1030
ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
rd $SO /workspace/scratch/n56/${SO}_read.txt || { echo "=== smoke read FAILED"; tail -5 /workspace/scratch/n56/${SO}_read.txt; exit 1; }
grep -h "^reading: C0" /workspace/scratch/n56/${SO}_read.txt | cut -c1-300
rm -rf /workspace/scratch/n56/$SO; mv results/sd_necessity/$SO /workspace/scratch/n56/ 2>/dev/null
mv results/sd_necessity/nn_sd_read/${SO}_note56.json /workspace/scratch/n56/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
KO=${P}sd56_ko_test_v1
ko $KO "instructed, hypothetical, premise and answer pressure (test split)" || { echo "=== $KO FAILED"; exit 1; }
OUT=/workspace/scratch/${P}note56.txt
if rd $KO /workspace/scratch/n56/${KO}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $KO (scripts/nn_sd_ma1_read.py, commit $(git rev-parse --short HEAD))"; cat /workspace/scratch/n56/${KO}_read.txt; echo; } >> $OUT
  grep -h "^reading" /workspace/scratch/n56/${KO}_read.txt | cut -c1-400
else
  echo "=== read FAILED"; tail -5 /workspace/scratch/n56/${KO}_read.txt; fails=$((fails + 1))
fi
[ -f results/sd_necessity/$MAIN/summary.json ] || echo "=== $MAIN (note 40) not finished: D1 not read; rerun the reader with --solo-run $MAIN once it is"
echo "=== n56 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
