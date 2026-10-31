#!/bin/bash
# h200_n56_1030.sh plus amendment 76 (2026-10-30): the same note 56 run (same run name {P}sd56_ko_test_v1, so nothing done is
# redone) with bridgeJ_peerperp and bridgeJ_peerperp_rot added to the mid-band edits (C4-perp, read in-run by nn_sd_ma1_read.py).
# N56PP=1 (the 9B, whose note 56 run exists): instead a run of only none, bridgeJ_ctrl, bridgeJ_peer, bridgeJ_peerperp and
# bridgeJ_peerperp_rot on hyp_vis and prem_hid, test split, no --gen ({P}sd56pp_v1), then the reader on {P}sd56_ko_test_v1 with
# --perp-run {P}sd56pp_v1 (C4-perp, post hoc on the 9B). N56_SPLIT=dev (amendment 77, the 9B): the same run on the dev split
# ({P}sd56_ko_dev_v1, same conversations, edits incl. the perp pair, filter and readings), D1's solo rows from note 47's
# {P}sd_ko_dev_v1, and a "Replicates" line against {P}sd56_ko_test_v1's labels.
# Usage: [N56PP=1 | N56_SPLIT=dev] h200_n56b_1030.sh MODEL GPU [WAITJOB ...]
# From h200_n56_1030.sh:
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
W="prereg amendments 73 and 76, note 56, copy or compute (2026-10-30, $BJ_TARGET)"
PP=${N56PP:-0}
SPLIT=${N56_SPLIT:-test}  # amendment 77: N56_SPLIT=dev runs the dev split ({P}sd56_ko_dev_v1; D1's solo rows from note 47's {P}sd_ko_dev_v1)
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1; MAIN=${P}sd_ko_${SPLIT}_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
done
grep -q '"bridgeJ_peerperp"' scripts/nn_sd_necessity.py || { echo "=== the runner has no bridgeJ_peerperp edit (SD runner's commit missing)"; exit 1; }
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
EDITS="$KB:paper10,paper10_rot,paper10_pcasize,unembed10,paper10_keepA,ansJ,bridgeJ_ctrl,bridgeJ_peer,bridgeJ_peerperp,bridgeJ_peerperp_rot"
GEN=(--gen --gen-batch $GBATCH)
SO=${P}sd56b_ko_smoke1030; KO=${P}sd56_ko_test_v1; WHY="instructed, hypothetical, premise and answer pressure (test split; + bridgeJ_peerperp, amendment 76)"
REF=()
if [ "$SPLIT" != test ]; then  # amendment 77: the same run on another split, read against the test split's labels
  SO=${P}sd56b_ko_${SPLIT}smoke1030; KO=${P}sd56_ko_${SPLIT}_v1; WHY="note 56 on the $SPLIT split (amendment 77; + bridgeJ_peerperp, amendment 76)"
  REF=(--ref-run ${P}sd56_ko_test_v1)
fi
if [ "$PP" = 1 ]; then  # amendment 76's own run (the 9B): C4-perp only
  CONVS="hyp_vis prem_hid"
  EDITS="$KB:bridgeJ_ctrl,bridgeJ_peer,bridgeJ_peerperp,bridgeJ_peerperp_rot"
  GEN=()
  SO=${P}sd56pp_smoke1030; KO=${P}sd56pp_v1; WHY="amendment 76 C4-perp (bridgeJ_peerperp; none, bridgeJ_ctrl, bridgeJ_peer rerun; hyp_vis, prem_hid; test split)"
fi
LBL=$(seq -s' ' ${LB%-*} ${LB#*-})  # the late band's layers, read beside every 2nd layer (D1)
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  if [ -d results/sd_necessity/$r ] && [ ! -f results/sd_necessity/$r/summary.json ]; then  # a failed attempt: set aside
    mv results/sd_necessity/$r /workspace/scratch/n56/$r.partial.$(date -u +%H%M%S) && echo "=== moved a partial $r to /workspace/scratch/n56"
  fi
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split $SPLIT --convs $CONVS --edits $EDITS \
    --batch $KBATCH "${GEN[@]}" --read-lenses jpp --read-extra $LBL "$@"
}
rd() {  # rd RUN OUT: the note 56 reader (D1's solo rows from note 40's run if it exists); N56PP=1: the main run, --perp-run RUN
  local solo="" run=$1
  [ -f results/sd_necessity/$MAIN/summary.json ] && solo="--solo-run $MAIN"
  [ "$PP" = 1 ] && { solo="$solo --perp-run $1"; run=${P}sd56_ko_test_v1; }
  # shellcheck disable=SC2086
  .venv/bin/python scripts/nn_sd_ma1_read.py $run --gate $GT --name-rule canonical --late $LBL $solo "${REF[@]}" > $2 2>&1
}
if [ "$PP" = 1 ]; then
  echo "=== waiting for ${P}sd56_ko_test_v1 (the main note 56 run, read with --perp-run) $(date -u +%T)"
  until [ -f results/sd_necessity/${P}sd56_ko_test_v1/summary.json ]; do sleep 60; done
fi
ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
rd $SO /workspace/scratch/n56/${SO}_read.txt || { echo "=== smoke read FAILED"; tail -5 /workspace/scratch/n56/${SO}_read.txt; exit 1; }
grep -h "^reading: C0" /workspace/scratch/n56/${SO}_read.txt | cut -c1-300
rm -rf /workspace/scratch/n56/$SO; mv results/sd_necessity/$SO /workspace/scratch/n56/ 2>/dev/null
mv results/sd_necessity/nn_sd_read/${SO}_note56.json results/sd_necessity/nn_sd_read/*_note56_perp-${SO}.json /workspace/scratch/n56/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko $KO "$WHY" || { echo "=== $KO FAILED"; exit 1; }
OUT=/workspace/scratch/${P}note56.txt
if rd $KO /workspace/scratch/n56/${KO}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $KO (scripts/nn_sd_ma1_read.py, commit $(git rev-parse --short HEAD))"; cat /workspace/scratch/n56/${KO}_read.txt; echo; } >> $OUT
  grep -h "^reading" /workspace/scratch/n56/${KO}_read.txt | cut -c1-400
else
  echo "=== read FAILED"; tail -5 /workspace/scratch/n56/${KO}_read.txt; fails=$((fails + 1))
fi
[ -f results/sd_necessity/$MAIN/summary.json ] || echo "=== $MAIN (note 40) not finished: D1 not read; rerun the reader with --solo-run $MAIN once it is"
echo "=== n56b $M (N56PP=$PP, split $SPLIT) done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
