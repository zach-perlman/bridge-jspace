#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 11): bridge or answer, and composition failures. Usage:
#   h200_n11_1028.sh GPU STAGE MODEL [MODEL ...]
#   STAGE a: the band runs (seeds 0, 1, 2) and the composition readout; STAGE b: the timing sweep and the repair
set -u
G=$1; STAGE=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 11)"
NEW="insert_k10_noans insert_k10_noansctl insert_ans insert_ansctl latent_k10_noans latent_k10_noansctl latent_ans latent_ansctl"
S0="insert_k10 latent_k10 $NEW remove_k10_noans"
S12="insert_k10 insert_k10_rand insert_k10_rot latent_k10 latent_k10_rand latent_k10_rot $NEW remove_k10 remove_k10_rot remove_k10_noans"
SWEEP="insert_k10 insert_k10_noans insert_ans latent_k10 latent_k10_noans latent_ans insert_k10_rand"
REPAIR="repair_k10 repair_k10_rand repair_k10_rot repair_k10_noans repair_full insert_k10"
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
    27b) export BJ_TARGET=qwen3.6-27b; P=; BAND=32-40; WINS="8-15 16-23 24-31 32-40 41-48 49-56 57-62" ;;
    9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; WINS="4-7 8-11 12-16 17-20 21-24 25-28" ;;
    nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; WINS="6-10 11-15 16-20 21-26 27-33 34-39 40-45 46-50" ;;
  esac
  C=${P}jsuite_v3_test_chat_competence_cand2_v1
  if [ "$STAGE" = a ]; then
    for s in 0 1 2; do
      c=$S12; [ $s = 0 ] && c=$S0
      r=${P}nn_ans_L${BAND}_s${s}_v1
      # shellcheck disable=SC2086
      go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: bridge or answer, $BJ_TARGET L$BAND, donor seed $s" --band $BAND --competence $C \
        --words RM MM PM --sample-refs 80 --seed $s --conds $c
    done
    r=${P}nn_readout_comp_v1
    go nn_readout $r $PY scripts/nn_readout.py --name $r --competence $C --items composition
  else
    r=${P}nn_ans_sweep_v1
    # shellcheck disable=SC2086
    go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: timing sweep, $BJ_TARGET" --sweep $WINS --competence $C --words RM PM \
      --sample-per-word 80 --conds $SWEEP
    r=${P}nn_repair_L${BAND}_v1
    # shellcheck disable=SC2086
    go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: composition-failure repair, $BJ_TARGET L$BAND" --band $BAND --competence $C \
      --words RM --items fail --conds $REPAIR
  fi
done
echo "=== n11 [$G] $STAGE $* done, $fails failed $(date -u +%FT%TZ)"
