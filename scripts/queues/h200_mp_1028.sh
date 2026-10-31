#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 13): the latent first hop into an in-context second hop (MP), and the
# clamp's break-test. Usage: h200_mp_1028.sh GPU WAITJOB MODEL [MODEL ...]
set -u
G=$1; WAIT=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 13)"
SET=jsuite_v3mp_test_chat
MPC="insert_k10 insert_k10_rand insert_k10_rot insert_k10_noansrel insert_k100 full_insert lens_insert rem_insert remfix_insert lensrand_insert remove_k10 remove_k10_rot"
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return; }
  echo "=== done $r $(date -u +%T)"
}
for M in "$@"; do
  case $M in
    27b) export BJ_TARGET=qwen3.6-27b; P=; BAND=32-40 ;;
    9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; BAND=12-16 ;;
    nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; BAND=27-33 ;;
  esac
  C=${P}${SET}_competence_cand2_v1
  go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words MP --read cand2 --hop1 gen \
    --why "$W: $BJ_TARGET competence on MP (hop 2 the passage lookup)"
  if [ -f results/tasks_v2/$C/summary.json ]; then
    for s in 0 1; do
      r=${P}nn_mp_L${BAND}_s${s}_v1
      # shellcheck disable=SC2086
      go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: MP swap, $BJ_TARGET L$BAND, donor seed $s" --set $SET --band $BAND \
        --competence $C --words MP --scene-words MP --seed $s --conds $MPC
    done
  else
    echo "=== no MP competence for $M"; fails=$((fails + 1))
  fi
  r=${P}nn_clampnoans_L${BAND}_v1
  go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: the clamp's break-test, $BJ_TARGET L$BAND" --band $BAND \
    --competence ${P}jsuite_v3_test_chat_competence_cand2_v1 --words RM MM PM --sample-refs 80 --conds clamp clamp_null clamp_noans
done
echo "=== mp [$G] $* done, $fails failed $(date -u +%FT%TZ)"
