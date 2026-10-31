#!/bin/bash
# Amendment 66 addendum (2026-10-30): the silent-dissent items' gate (guess control, direct-shortcut flag, name/stem filter) and
# the reader's strata. Usage: h200_sdgate_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Waits for the WAITJOBs, then for the model's known stage ({P}sd_known_v1/summary.json); runs an
#   8-item smoke of scripts/sd_gate.py (moved to /workspace/scratch/sd), the gate on every known item ({P}sd_gate_v1); then, once
#   the model's knock-out run has finished ({P}sd_ko_test_v1/summary.json; and {P}sd_ko_dev_v1 if it exists), the reader with
#   --gate (the registered name rule), with --gate --drop-bridge-named, and with --gate --name-rule canonical (descriptive).
#   The knock-out runs are not touched. GPU memory: the model only (9B ~20 GB, 27B ~55 GB, Lightning ~60 GB), for a few minutes.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; GBATCH=64 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; GBATCH=64 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; GBATCH=32 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="amendment 66 addendum (2026-10-30, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1
echo "=== waiting for $KN $(date -u +%T)"
until [ -f results/sd_necessity/$KN/summary.json ]; do sleep 60; done
mkdir -p /workspace/scratch/sd
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/sd/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/sd/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
SG=${P}sd_gate_smoke1030
go $SG $PY scripts/sd_gate.py --name $SG --why "$W: smoke" --items-run $KN --n 8 --batch $GBATCH || { echo "=== smoke FAILED"; exit 1; }
mv results/sd_necessity/$SG /workspace/scratch/sd/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
GT=${P}sd_gate_v1
go $GT $PY scripts/sd_gate.py --name $GT --why "$W: the gate on every known item" --items-run $KN --batch $GBATCH || { echo "=== gate FAILED"; exit 1; }
.venv/bin/python -c "import json; d=json.load(open('results/sd_necessity/$GT/summary.json'))['by']; [print(' ', k, v) for k, v in d.items()]"
for KO in ${P}sd_ko_test_v1 ${P}sd_ko_dev_v1; do
  if [ "$KO" = ${P}sd_ko_dev_v1 ] && [ ! -d results/sd_necessity/$KO ]; then continue; fi
  echo "=== waiting for $KO $(date -u +%T)"
  until [ -f results/sd_necessity/$KO/summary.json ]; do sleep 60; done
  for V in "" "--drop-bridge-named" "--name-rule canonical"; do
    tag=$(echo "$V" | tr -d '-' | tr ' ' '_'); out=/workspace/scratch/sd/${KO}_read_gated${tag:+_$tag}.txt
    # shellcheck disable=SC2086
    .venv/bin/python scripts/nn_sd_read.py $KO --gate $GT $V > $out 2>&1 || { echo "=== read $KO $V FAILED"; tail -5 $out; fails=$((fails + 1)); continue; }
  done
  echo "=== $KO, gated (primary):"
  grep -h "^reading" /workspace/scratch/sd/${KO}_read_gated.txt | cut -c1-400
done
echo "=== sdgate $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
