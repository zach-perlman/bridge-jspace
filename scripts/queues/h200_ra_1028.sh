#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 12): rendering A (the relation after the bridge), targeted runs.
# Usage: h200_ra_1028.sh GPU WAITJOB MODEL [MODEL ...]   (Bolt: its own queue, after its sweep)
set -u
G=$1; WAIT=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 12)"
SET=jsuite_v3ra_test_chat
SCRUBS="noans noansctl noansrel noansrelctl noansown noansownctl"
BANDC=""
for src in insert latent; do
  BANDC="$BANDC ${src}_k10 ${src}_k10_rand ${src}_k10_rot ${src}_ans ${src}_ansctl"
  for s in $SCRUBS; do BANDC="$BANDC ${src}_k10_$s"; done
done
BANDC="$BANDC remove_k10 remove_k10_rot remove_k10_noans remove_k10_noansrel remove_k10_noansown"
REPAIR="repair_k10 repair_k10_rand repair_k10_rot repair_k10_noans repair_full insert_k10"
DECOMP="full_insert lens_insert rem_insert remfix_insert lensrand_insert full_latent lens_latent rem_latent remfix_latent lensrand_latent"
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
  go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words RM MM PM --read cand2 --hop1 gen \
    --why "$W: $BJ_TARGET competence on rendering A (RM MM PM)"
  [ -f results/tasks_v2/$C/summary.json ] || { echo "=== no competence for $M: skipping its runs"; continue; }
  go nn_readout ${P}nn_readout_comp_ra_v1 $PY scripts/nn_readout.py --name ${P}nn_readout_comp_ra_v1 --set $SET --competence $C --items composition
  for s in 0 1; do
    r=${P}nn_ansra_L${BAND}_s${s}_v1
    # shellcheck disable=SC2086
    go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: bridge or answer on rendering A, $BJ_TARGET L$BAND, donor seed $s" --set $SET \
      --band $BAND --competence $C --scene-words RM MM PM --words RM MM PM --sample-refs 80 --seed $s --conds $BANDC
  done
  r=${P}nn_repair_ra_L${BAND}_v1
  # shellcheck disable=SC2086
  go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: composition-failure repair on rendering A, $BJ_TARGET L$BAND" --set $SET \
    --band $BAND --competence $C --scene-words RM MM PM --words RM --items fail --conds $REPAIR
  r=${P}nn_decomp_ra_L${BAND}_last_v1
  # shellcheck disable=SC2086
  go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: decomposition on rendering A, $BJ_TARGET L$BAND, last token" --set $SET \
    --band $BAND --competence $C --scene-words RM MM PM --words RM MM PM --sample-refs 150 --conds $DECOMP
done
echo "=== ra [$G] $* done, $fails failed $(date -u +%FT%TZ)"
