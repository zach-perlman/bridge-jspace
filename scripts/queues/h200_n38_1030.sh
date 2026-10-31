#!/bin/bash
# Zach (2026-10-30, prereg amendment 65 note 38): the size and semantics loopholes of notes 11-13. Usage:
#   h200_n38_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Per model:
#   - the band run: note 11's jobs (v3 rendering 0; RM every eligible item, PM 80 seeded; donor seed 0; the description's
#     last token, PM its mention; the model's band), with the raw arms rerun in-run (insert_k10, insert_k10_rot,
#     insert_k10_noansrel, insert_k10_noansrelctl, clamp, clamp_null, clamp_noans; the reader checks them against the
#     stored rows of notes 9, 11 and 13) and note 38's arms (insert_k10_noansrel_nm / _x2 / _x4, insert_k10_noansoff,
#     insert_k10_noansform, insert_relans, clamp_noans_nm);
#   - the sweep: note 11's windows, RM and PM 80 each (its --sample-per-word 80): insert_k10_noansrel_nm and insert_relans,
#     with insert_k10 (checked against note 11's stored sweep) and insert_k10_rot (for "beyond rotated") beside;
#   - the reader (scripts/nn_swap38_read.py).
#   The 9B's smoke (<= 8 items) ran by hand before this queue (job ...-n38smoke-1030-*, moved to /workspace/scratch/n38);
#   the 27B and Lightning run a 2-item smoke first. Muse is not here: it has no note 11 v3 jobs (no muse30_nn_ans_* runs).
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; WINS="4-7 8-11 12-16 17-20 21-24 25-28" ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; BAND=32-40; WINS="8-15 16-23 24-31 32-40 41-48 49-56 57-62" ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; WINS="6-10 11-15 16-20 21-26 27-33 34-39 40-45 46-50" ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 65 note 38, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
C=${P}jsuite_v3_test_chat_competence_cand2_v1
BANDC="insert_k10 insert_k10_rot insert_k10_noansrel insert_k10_noansrelctl insert_k10_noansrel_nm insert_k10_noansrel_x2 insert_k10_noansrel_x4 insert_k10_noansoff insert_k10_noansform insert_relans clamp clamp_null clamp_noans clamp_noans_nm"
SWEEPC="insert_k10 insert_k10_rot insert_k10_noansrel_nm insert_relans"
if [ "$M" != 9b ]; then
  sk=${P}nn38_L${BAND}_smoke1030
  # shellcheck disable=SC2086
  go nn_swap $sk $PY scripts/nn_swap.py --name $sk --why "$W: smoke" --band $BAND --competence $C --words RM PM --sample-refs 80 --seed 0 \
    --limit 2 --conds $BANDC || { echo "=== smoke FAILED"; exit 1; }
  mkdir -p /workspace/scratch/n38 && mv results/nn_swap/$sk /workspace/scratch/n38/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
r=${P}nn38_L${BAND}_v1
# shellcheck disable=SC2086
go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: note 11's band jobs (donor seed 0), raw arms rerun, note 38's arms" --band $BAND \
  --competence $C --words RM PM --sample-refs 80 --seed 0 --conds $BANDC
r=${P}nn38_sweep_v1
# shellcheck disable=SC2086
go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: note 11's sweep windows, noansrel_nm and relans" --sweep $WINS --competence $C \
  --words RM PM --sample-per-word 80 --conds $SWEEPC
.venv/bin/python scripts/nn_swap38_read.py "$P" --band-run ${P}nn38_L${BAND}_v1 --sweep-run ${P}nn38_sweep_v1 > /workspace/scratch/${P}note38.txt 2>&1 \
  || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note38.txt; fails=$((fails + 1)); }
grep -h "reading\|stored check" /workspace/scratch/${P}note38.txt | cut -c1-400
echo "=== n38 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
