#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 notes 21-23 + addendum). Usage: h200_rep2_1029.sh MODEL GPU WAITJOB [WAITJOB ...]
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; RB="4-7 8-11 12-16"; LB=12-16; CB="4-11 12-16" ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; RB="16-23 24-31 32-40"; LB=32-40; CB="16-31 32-40" ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; RB="6-10 11-15 16-20 21-26"; LB=21-26; CB="6-20 27-33" ;;
esac
W="Zach (2026-10-29, prereg amendment 58 notes 21-23, $BJ_TARGET)"
SET=jsuite_v4_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
run() {  # run NAME ARGS... (nn_swap)
  local r=$1; shift
  if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  $PY scripts/nn_swap.py --name $r --set $SET --items v4ok --competence $C --cv-h1 $CV "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
C16="full_cf jpp_cf jpprand_cf nojpp_cf nojpprand_cf"
C21="$C16 lens_cf rem_cf lensrand_cf lensnp_cf remnp_cf lensshrnp_cf remshrnp_cf"
CL="$C16 lensnp_cf remnp_cf lensshrnp_cf remshrnp_cf"
b0=${RB%% *}
# shellcheck disable=SC2086
run ${P}nn_n21_smoke1029 --why "$W smoke" --words MP --site last --seed 0 --band $b0 --limit 2 --report --conds $C21 || exit 1
# shellcheck disable=SC2086
run ${P}nn_n22_smoke1029 --why "$W smoke" --words MP MM --site last --seed 0 --band ${CB##* } --limit 2 --conds clamp clamp_null clamp_noans || exit 1
$PY scripts/nn_probe_v4.py --name ${P}nn_probe_v4_smoke1029 --why "$W smoke" --competence $C --cv-h1 $CV --limit 600 --steps 20 \
  > /workspace/scratch/${P}nn_probe_v4_smoke1029.log 2>&1 < /dev/null || { echo "=== n23 smoke FAILED"; tail -5 /workspace/scratch/${P}nn_probe_v4_smoke1029.log; exit 1; }
mv results/nn_probe_v4/${P}nn_probe_v4_smoke1029 /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
# note 21: the report question with Dan's lens part (+ the top-10 beside), and the lookup's missing cell
r21=""
for band in $RB; do
  for s in 0 1; do
    r=${P}nn_n21_last_L${band}_s${s}_v1; r21="$r21 $r"
    # shellcheck disable=SC2086
    run $r --why "$W: note 21, report, last / L$band, donor seed $s" --words MP --site last --seed $s --band $band --report --conds $C21
  done
done
for band in $RB; do
  for s in 0 1; do
    r=${P}nn_n21l_last_MP_L${band}_s${s}_v1; r21="$r21 $r"
    # shellcheck disable=SC2086
    run $r --why "$W: note 21, the lookup with both lens parts, last / MP / L$band, donor seed $s" --words MP --site last --seed $s --band $band --conds $CL
  done
done
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_cf_read.py ${P}v4_n21 $r21 > /workspace/scratch/${P}v4_n21.txt 2>&1
echo "=== note 21 $M done $(date -u +%T)"
# note 22: the paper's clamp
r22=""
for s in 0 1; do
  r=${P}nn_n22_s${s}_v1; r22="$r22 $r"
  # shellcheck disable=SC2086
  run $r --why "$W: note 22, the clamp on v4, donor seed $s" --words MP MM --site last --seed $s --sweep $CB --conds clamp clamp_null clamp_noans
done
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_cf_read.py ${P}v4_n22 $r22 > /workspace/scratch/${P}v4_n22.txt 2>&1
echo "=== note 22 $M done $(date -u +%T)"
# note 23: the trained read-out
r=${P}nn_probe_v4_v1
if [ ! -f results/nn_probe_v4/$r/summary.json ]; then
  $PY scripts/nn_probe_v4.py --name $r --why "$W: note 23" --competence $C --cv-h1 $CV --readout ${P}nn_readout_v4_v1 > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
fi
echo "=== notes 21-23 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
