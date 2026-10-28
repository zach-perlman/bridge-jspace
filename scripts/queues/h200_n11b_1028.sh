#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 11 addendum): narrower answer scrubs (the relation's answers; X's and D's
# own), each with its same-size random control, on note 11's three donor seeds at each model's band.
# Usage: h200_n11b_1028.sh GPU WAITJOB MODEL [MODEL ...]
set -u
G=$1; WAIT=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 11 addendum)"
CONDS="insert_k10_noansrel insert_k10_noansrelctl insert_k10_noansown insert_k10_noansownctl latent_k10_noansrel latent_k10_noansrelctl latent_k10_noansown latent_k10_noansownctl remove_k10_noansrel remove_k10_noansown"
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
for M in "$@"; do
  case $M in
    27b) export BJ_TARGET=qwen3.6-27b; P=; BAND=32-40 ;;
    9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; BAND=12-16 ;;
    nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; BAND=27-33 ;;
  esac
  C=${P}jsuite_v3_test_chat_competence_cand2_v1
  for s in 0 1 2; do
    r=${P}nn_ans2_L${BAND}_s${s}_v1
    echo "=== nn_swap/$r $(date -u +%T)"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: narrower scrubs, $BJ_TARGET L$BAND, donor seed $s" --band $BAND --competence $C \
      --words RM MM PM --sample-refs 80 --seed $s --conds $CONDS > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done
echo "=== n11b [$G] $* done, $fails failed $(date -u +%FT%TZ)"
