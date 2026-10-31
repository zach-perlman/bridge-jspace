#!/bin/bash
# Prereg amendments 80-81 note 56c (2026-10-30): is C1 plain one-hop recall, and does an order spare only what is in context?
#   Amendment 81: in ask_city and instr_city the agent completes the hop-2 relation on e2' ("<e2'> is in the country of"); each
#   new cell is read only if, unedited, it says e3' >= 60% with first-token agreement >= 90%.
# Usage: h200_n56c_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b (registered); 27b | nem35l work the same way if ever wanted.
#   Waits for the WAITJOBs (^EXIT), the model's known stage and gate, and its note 56 test run ({P}sd56_ko_test_v1, for the
#   reader's reference lines). One knock-out run of scripts/nn_sd_necessity.py on the test split, note 56's items (round 0
#   right; the reader's gate, names as written, and peer-name filter), restricted to person-birthcity-cntry (the only
#   category whose peers' bridge is a city and answer a country, the relation the registered wording asks for):
#   conversations ask_city instr_city instr_vis hyp_vis (sd_prompts.CONVS; instr_vis, hyp_vis = note 56's, the reference),
#   note 56's mid-band edits with amendment 76's perp pair (paper10, paper10_rot, paper10_pcasize, unembed10, paper10_keepA,
#   ansJ, bridgeJ_ctrl, bridgeJ_peer, bridgeJ_peerperp, bridgeJ_peerperp_rot), --gen, J++ read every 2nd layer plus the late
#   band. An 8-item smoke first (moved to /workspace/scratch/n56). Then scripts/nn_sd_ma1_read.py (Q1, Q2 and the either-answer
#   table; note 56's lines beside), appended to /workspace/scratch/{P}note56c.txt; its reading lines go to this log.
#   GPU [E] 9B: ~15 min, ~33 GB (347 items x 4 conversations x 11 forwards, ~0.032 s/row; generation ~0.156 s/prompt).
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
W="prereg amendments 80-81 note 56c, ask_city / instr_city (2026-10-30, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1; MAIN=${P}sd_ko_test_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
done
grep -q '"bridgeJ_peerperp"' scripts/nn_sd_necessity.py || { echo "=== the runner has no bridgeJ_peerperp edit"; exit 1; }
grep -q 'def final_statement' scripts/sd_prompts.py || { echo "=== sd_prompts lacks amendment 81 (final_statement)"; exit 1; }
mkdir -p /workspace/scratch/n56
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/n56/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/n56/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONVS="ask_city instr_city instr_vis hyp_vis"
EDITS="$KB:paper10,paper10_rot,paper10_pcasize,unembed10,paper10_keepA,ansJ,bridgeJ_ctrl,bridgeJ_peer,bridgeJ_peerperp,bridgeJ_peerperp_rot"
LBL=$(seq -s' ' ${LB%-*} ${LB#*-})  # the late band's layers, read beside every 2nd layer (D1)
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  if [ -d results/sd_necessity/$r ] && [ ! -f results/sd_necessity/$r/summary.json ]; then  # a failed attempt: set aside
    mv results/sd_necessity/$r /workspace/scratch/n56/$r.partial.$(date -u +%H%M%S) && echo "=== moved a partial $r to /workspace/scratch/n56"
  fi
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split test --categories person-birthcity-cntry \
    --convs $CONVS --edits $EDITS --batch $KBATCH --gen --gen-batch $GBATCH --read-lenses jpp --read-extra $LBL "$@"
}
rd() {  # rd RUN OUT: the note 56 reader (Q1, Q2 and the either table; D1's solo rows from note 40's run if it exists)
  local solo=""
  [ -f results/sd_necessity/$MAIN/summary.json ] && solo="--solo-run $MAIN"
  # shellcheck disable=SC2086
  .venv/bin/python scripts/nn_sd_ma1_read.py $1 --gate $GT --name-rule canonical --late $LBL $solo > $2 2>&1
}
SO=${P}sd56c_ko_smoke1030; KO=${P}sd56c_ko_test_v1
ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
rd $SO /workspace/scratch/n56/${SO}_read.txt || { echo "=== smoke read FAILED"; tail -5 /workspace/scratch/n56/${SO}_read.txt; exit 1; }
grep -hE "^reading: (C0|Q1|Q2)" /workspace/scratch/n56/${SO}_read.txt | cut -c1-300
rm -rf /workspace/scratch/n56/$SO; mv results/sd_necessity/$SO /workspace/scratch/n56/ 2>/dev/null
mv results/sd_necessity/nn_sd_read/${SO}_note56.json /workspace/scratch/n56/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko $KO "ask_city, instr_city, instr_vis, hyp_vis (test split, person-birthcity-cntry)" || { echo "=== $KO FAILED"; exit 1; }
OUT=/workspace/scratch/${P}note56c.txt
if rd $KO /workspace/scratch/n56/${KO}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $KO (scripts/nn_sd_ma1_read.py, commit $(git rev-parse --short HEAD))"; cat /workspace/scratch/n56/${KO}_read.txt; echo; } >> $OUT
  grep -h "^reading" /workspace/scratch/n56/${KO}_read.txt | cut -c1-400
else
  echo "=== read FAILED"; tail -5 /workspace/scratch/n56/${KO}_read.txt; fails=$((fails + 1))
fi
echo "=== n56c $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
