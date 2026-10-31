#!/bin/bash
# Silent-dissent necessity test (2026-10-30; design /home/zach/scratch/redteam_1030/sd_necessity_design.md; the prereg amendment
# is registered by the orchestrator before this runs). Usage: h200_sd_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Per model: a smoke (their known check on the first 60 facts of each category, then the knock-out on 8
#   items, every conversation and edit, and the reader), moved to /workspace/scratch/sd; then their known check over the three
#   categories (both splits), the knock-out on the test split (--gen: their 12-token outcome, unedited), the reader (and again
#   without items whose transcript names their bridge). Options (environment): SD_CONVS (default the five conversations below),
#   SD_DEV=1 (also the dev split, a held-out replication), SD_JLENS=1 (27B: also read with the paper's plain J-lens file, a
#   labelled one-off lens comparison), SD_EXTRA_EDITS (e.g. ",paper10_keepA,ansJ" appended to the mid band's edits).
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
LENSES="jpp"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; LB=26-29; KBATCH=32; GBATCH=64 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; LB=52-55; KBATCH=32; GBATCH=64; [ "${SD_JLENS:-0}" = 1 ] && LENSES="jpp jlens" ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; LB=42-45; KBATCH=16; GBATCH=32 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
KBATCH=${SD_KBATCH:-$KBATCH}; GBATCH=${SD_GBATCH:-$GBATCH}  # 2026-10-30: the 27B knock-out ran out of memory at 32/64; override per run
W="silent-dissent necessity (2026-10-30, design sd_necessity_design.md, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
mkdir -p /workspace/scratch/sd
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/sd/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/sd/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CATS="landmark-cntry-capital person-birthcity-cntry person-uguniv-hqcity"
CONVS=${SD_CONVS:-"solo agree_vis agree_hid press_vis press_hid"}
EDITS="$KB:paper10,paper10_rot,paper10_pcasize,unembed10,bridgeJ,bridgeJ_ctrl${SD_EXTRA_EDITS:-} $LB:paper10,paper10_rot"
LBL=$(seq -s' ' ${LB%-*} ${LB#*-})  # the late band's layers, read beside every 2nd layer
ko() {  # ko RUN ITEMS SPLIT WHY [EXTRA...]
  local r=$1 it=$2 sp=$3 why=$4; shift 4
  # shellcheck disable=SC2086
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $it --split $sp --convs $CONVS --edits $EDITS \
    --batch $KBATCH --gen --gen-batch $GBATCH --read-lenses $LENSES --read-extra $LBL "$@"
}
read_run() {  # read_run RUN: the reader, then without items whose transcript names their bridge
  .venv/bin/python scripts/nn_sd_read.py $1 > /workspace/scratch/sd/$1_read.txt 2>&1 || { echo "=== read $1 FAILED"; tail -5 /workspace/scratch/sd/$1_read.txt; fails=$((fails + 1)); return 1; }
  .venv/bin/python scripts/nn_sd_read.py $1 --drop-bridge-named > /workspace/scratch/sd/$1_read_nobridge.txt 2>&1 || fails=$((fails + 1))
  grep -h "^reading" /workspace/scratch/sd/$1_read.txt | cut -c1-400
}
# smoke: 60 facts per category, 8 items, everything once
SK=${P}sd_known_smoke1030; SO=${P}sd_ko_smoke1030
# shellcheck disable=SC2086
go $SK $PY scripts/nn_sd_necessity.py known --name $SK --why "$W: smoke" --categories $CATS --per-category 60 --batch $GBATCH \
  || { echo "=== smoke FAILED"; exit 1; }
ko $SO $SK all "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
read_run $SO || { echo "=== smoke read FAILED"; exit 1; }
mv results/sd_necessity/$SK results/sd_necessity/$SO /workspace/scratch/sd/ 2>/dev/null
mv results/sd_necessity/nn_sd_read/$SO*.json /workspace/scratch/sd/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
# the run
KN=${P}sd_known_v1
# shellcheck disable=SC2086
go $KN $PY scripts/nn_sd_necessity.py known --name $KN --why "$W: their known check, pairing, round 0" --categories $CATS --batch $GBATCH \
  || { echo "=== known FAILED"; exit 1; }
grep -h "_round0_accuracy\|_items\"" results/sd_necessity/$KN/summary.json
ko ${P}sd_ko_test_v1 $KN test "the knock-out, their test split" && read_run ${P}sd_ko_test_v1
if [ "${SD_DEV:-0}" = 1 ]; then
  ko ${P}sd_ko_dev_v1 $KN dev "the knock-out, their dev split (held-out replication)" && read_run ${P}sd_ko_dev_v1
fi
echo "=== sd $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
