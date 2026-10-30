#!/bin/bash
# h200_n54_1030.sh plus amendment 75 (2026-10-30): the same note 54 run (same run name {P}sd_n54_v1, so nothing done is redone)
# with bridgeJ_peerperp and bridgeJ_peerperp_rot added (P1-perp, read in-run by nn_sd_read.py --note54).
# N54PP=1 (the 9B, whose note 54 run exists): instead a run of only none, bridgeJ_ctrl, bridgeJ_peer, bridgeJ_peerperp and
# bridgeJ_peerperp_rot on solo, press_vis and hop1_vis, test + dev ({P}sd_n54pp_v1), read with --p1-run {P}sd_n54_v1 (its
# positive control and P1). Usage: [N54PP=1] h200_n54b_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
# From h200_n54_1030.sh: prereg amendment 72 note 54 and amendment 73's extension: note 40's R3 de-confounded (bridgeJperp),
# the peers' premise (bridgeJ_peer), every span's rotation.
#   Waits for the WAITJOBs, then for the model's known stage and gate ({P}sd_known_v1, {P}sd_gate_v1). One knock-out run on
#   --split all (test + dev), conversations solo press_vis press_hid hop1_vis, mid band: paper10, paper10_rot, bridgeJ,
#   bridgeJ_rot, bridgeJ_ctrl, bridgeJ_ctrl_rot, bridgeJperp, bridgeJ_peer, bridgeJ_peer_rot (+ the unedited read); J++ read
#   every 2nd layer and over the late band (the readout dissociation); no --gen. The 27B runs only its gated (names as written)
#   no-shortcut and landmark items (--uids, from its gate). An 8-item smoke first (moved to /workspace/scratch/n54). Then the
#   reader (--note54; G2 and the rerun check from {P}sd_ko_test_v1, waited for, and {P}sd_ko_dev_v1, waited for if it has
#   started), appended to /workspace/scratch/{P}note54.txt. Batch: N54_KBATCH overrides (9B 32, Lightning 16, 27B 16).
#   GPU [E], with the two added edits: 9B ~22 min, ~32 GB; Lightning ~30 min (measured rate; ~75 by the note 40 job anchor),
#   ~60-70 GB; 27B ~17 min, ~70-78 GB. N54PP=1 on the 9B: ~9 min, ~32 GB.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; LB=26-29; KBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; LB=52-55; KBATCH=16 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; LB=42-45; KBATCH=16 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
KBATCH=${N54_KBATCH:-$KBATCH}
W="prereg amendments 72-73 and 75, note 54 (2026-10-30, $BJ_TARGET)"
PP=${N54PP:-0}
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1
echo "=== waiting for $KN and $GT $(date -u +%T)"
until [ -f results/sd_necessity/$KN/summary.json ] && [ -f results/sd_necessity/$GT/summary.json ]; do sleep 60; done
S=/workspace/scratch/n54
mkdir -p $S
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > $S/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 $S/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONVS="solo press_vis press_hid hop1_vis"
EDITS="$KB:paper10,paper10_rot,bridgeJ,bridgeJ_rot,bridgeJ_ctrl,bridgeJ_ctrl_rot,bridgeJperp,bridgeJ_peer,bridgeJ_peer_rot,bridgeJ_peerperp,bridgeJ_peerperp_rot"
SO=${P}sd_n54b_smoke1030; R=${P}sd_n54_v1; WHY="note 54 and its extension (bridgeJperp; bridgeJ_peer; every span rotated) and amendment 75 (bridgeJ_peerperp), test + dev"
if [ "$PP" = 1 ]; then  # amendment 75's own run (the 9B)
  CONVS="solo press_vis hop1_vis"
  EDITS="$KB:bridgeJ_ctrl,bridgeJ_peer,bridgeJ_peerperp,bridgeJ_peerperp_rot"
  SO=${P}sd_n54pp_smoke1030; R=${P}sd_n54pp_v1; WHY="amendment 75 P1-perp (bridgeJ_peerperp; none, bridgeJ_ctrl, bridgeJ_peer rerun), test + dev"
fi
LBL=$(seq -s' ' ${LB%-*} ${LB#*-})  # the late band's layers, read beside every 2nd layer
UIDS=()
if [ "$M" = 27b ]; then  # amendment 73: on the 27B, the no-shortcut and landmark items only (gated, names as written)
  UF=$S/n54_uids_27b.txt
  .venv/bin/python -c "
import json, sys
g = [json.loads(l) for l in open('results/sd_necessity/$GT/gate.jsonl')]
u = sorted(x['uid'] for x in g if x['gated_canonical'] and (not x['shortcut'] or x['category'].startswith('landmark')))
open('$UF', 'w').write(''.join(v + '\n' for v in u))
print('27B uids (gated, names as written; no-shortcut or landmark):', len(u))
" || { echo "=== uid list FAILED"; exit 1; }
  UIDS=(--uids $UF)
fi
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  if [ -d results/sd_necessity/$r ] && [ ! -f results/sd_necessity/$r/summary.json ]; then  # a failed attempt of this queue: set aside
    mv results/sd_necessity/$r $S/$r.partial.$(date -u +%H%M%S) && echo "=== moved a partial $r to $S"
  fi
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split all --convs $CONVS --edits $EDITS \
    --batch $KBATCH --read-lenses jpp --read-extra $LBL "${UIDS[@]}" "$@"
}
rm -rf $S/$SO
ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
mv results/sd_necessity/$SO $S/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko $R "$WHY" || { echo "=== n54b $M: run FAILED"; exit 1; }
REFS=""
for x in ${P}sd_ko_test_v1 ${P}sd_ko_dev_v1; do  # the note 40 test run is required (G2); the note 47 dev run if it has started
  if [ $x = ${P}sd_ko_test_v1 ] || [ -d results/sd_necessity/$x ]; then
    echo "=== waiting for $x (G2 and the rerun check) $(date -u +%T)"
    until [ -f results/sd_necessity/$x/summary.json ]; do sleep 60; done
    REFS="$REFS $x"
  fi
done
P1R=()
if [ "$PP" = 1 ]; then
  echo "=== waiting for ${P}sd_n54_v1 (the positive control and P1) $(date -u +%T)"
  until [ -f results/sd_necessity/${P}sd_n54_v1/summary.json ]; do sleep 60; done
  P1R=(--p1-run ${P}sd_n54_v1)
fi
out=$S/${R}_read.txt
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_sd_read.py $R --note54 --gate $GT --ref-runs $REFS --late $LBL "${P1R[@]}" > $out 2>&1 || { echo "=== read FAILED"; tail -5 $out; fails=$((fails + 1)); }
{ echo "######## $(date -u +%FT%TZ) $R"; cat $out; } >> /workspace/scratch/${P}note54.txt
grep -hE "^(reading|beside|descriptive|check|G2)" $out | cut -c1-400
echo "=== n54b $M (N54PP=$PP) done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
