#!/bin/bash
# Amendment 67 note 42 (2026-10-30): position split for note 40's visible-answer effect. Usage: h200_sd42_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Waits for the WAITJOBs and for the model's known stage and gate ({P}sd_known_v1, {P}sd_gate_v1). A knock-out
#   run of scripts/nn_sd_necessity.py on the test split restricted to press_vis and press1_vis, with paper10, paper10_rot,
#   paper10_skipown(_rot) and paper10_onlyown(_rot) at the mid band (the model's known items, as note 40; no generation, no late
#   band): an 8-item smoke first (moved to /workspace/scratch/sd), then the run; then, once the model's note 40 run
#   ({P}sd_ko_test_v1, for the solo split) has finished, the reader with --note42 --gate (names as written: --name-rule
#   canonical, primary) and with the alias rule beside.
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
W="amendment 67 note 42 (2026-10-30, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1; MAIN=${P}sd_ko_test_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
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
EDITS="$KB:paper10,paper10_rot,paper10_skipown,paper10_skipown_rot,paper10_onlyown,paper10_onlyown_rot"
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  go $r $PY scripts/nn_sd_necessity.py ko --name $r --why "$W: $why" --items-run $KN --split test --convs press_vis press1_vis \
    --edits $EDITS --batch $KBATCH "$@"
}
SO=${P}sd42_ko_smoke1030
ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
.venv/bin/python scripts/nn_sd_read.py $SO --note42 --gate $GT --name-rule canonical > /workspace/scratch/sd/${SO}_read.txt 2>&1 \
  || { echo "=== smoke read FAILED"; tail -5 /workspace/scratch/sd/${SO}_read.txt; exit 1; }
mv results/sd_necessity/$SO /workspace/scratch/sd/ 2>/dev/null
mv results/sd_necessity/nn_sd_read/${SO}_note42*.json /workspace/scratch/sd/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
KO=${P}sd42_ko_test_v1
ko $KO "position split (press_vis, press1_vis; test split)" || { echo "=== $KO FAILED"; exit 1; }
echo "=== waiting for $MAIN (solo split) $(date -u +%T)"
until [ -f results/sd_necessity/$MAIN/summary.json ]; do sleep 60; done
.venv/bin/python scripts/nn_sd_read.py $KO --note42 --gate $GT --name-rule canonical --solo-run $MAIN > /workspace/scratch/sd/${KO}_note42.txt 2>&1 \
  || { echo "=== read FAILED"; tail -5 /workspace/scratch/sd/${KO}_note42.txt; fails=$((fails + 1)); }
.venv/bin/python scripts/nn_sd_read.py $KO --note42 --gate $GT --solo-run $MAIN > /workspace/scratch/sd/${KO}_note42_aliasrule.txt 2>&1 \
  || { echo "=== read (alias rule) FAILED"; fails=$((fails + 1)); }
grep -h "^reading" /workspace/scratch/sd/${KO}_note42.txt | cut -c1-400
echo "=== sd42 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
