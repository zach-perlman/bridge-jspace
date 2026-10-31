#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 14 Bolt addendum): Bolt on v4, both GPUs. Usage: h200_v4bolt_1029.sh WAITJOB [WAITJOB ...]
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_GRAM_PROJ=1 BJ_TARGET=nemotron-3.5-bolt
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 58 note 14 Bolt addendum)"
SET=jsuite_v4_test_chat; P=nem35b_
WINS="0-9 10-19 20-29 30-39 40-49 50-59 60-69 70-78 79-86"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
go() {  # go KIND RUN ARGS...
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return; }
  echo "=== done $r $(date -u +%T)"
}
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
sm=${P}${SET}_competence_smoke1029
$PY scripts/natural_v1.py competence --set $SET --name $sm --words MP MM --read cand2 --hop1 gen --limit 8 --why "$W: smoke" \
  > /workspace/scratch/bolt_v4_smoke.log 2>&1 < /dev/null || { echo "=== Bolt smoke FAILED"; tail -5 /workspace/scratch/bolt_v4_smoke.log; exit 3; }
mv results/tasks_v2/$sm /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words MP MM --read cand2 --hop1 gen --why "$W: Bolt v4 competence"
go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: Bolt v4 controls (closed-book hop 1, recognition, role noun only)" \
  --set jsuite_v4ctl_test_chat --words H1 RG RO --variants none
if [ ! -f results/tasks_v2/$C/summary.json ] || [ ! -f results/competence_variants/$CV/summary.json ]; then echo "=== no competence for Bolt"; exit 1; fi
go nn_readout ${P}nn_readout_v4_v1 $PY scripts/nn_readout.py --name ${P}nn_readout_v4_v1 --set $SET --competence $C --cv-h1 $CV --items v4
runs=""
for s in 0 1; do
  for site in last final span; do
    r=${P}nn_cf_${site}_s${s}_v1
    # shellcheck disable=SC2086
    go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: Bolt counterfactual map, site $site, donor seed $s" --set $SET --items v4ok \
      --competence $C --cv-h1 $CV --words MP MM --site $site --seed $s --sweep $WINS --conds full_cf lensrand_cf
    [ -f results/nn_swap/$r/summary.json ] && runs="$runs $r"
    # shellcheck disable=SC2086
    [ -n "$runs" ] && .venv/bin/python scripts/nn_cf_read.py ${P}v4_stage1 $runs > /workspace/scratch/${P}v4_stage1.txt 2>&1
  done
done
echo "=== Bolt v4 done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
