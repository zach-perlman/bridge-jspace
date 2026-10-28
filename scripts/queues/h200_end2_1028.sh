#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 10 addendum): Bolt, targeted, with note 10's references. Replaces
# h200_end_1028.sh's bolt mode, which ran RM only: the references (MM, PM) need their own competence rows, since under
# --scene-words RM their scenes (which hold no RM item) would pass unchecked. Usage:
#   h200_end2_1028.sh PREPJOB WAITJOB ...   after all: Bolt (both GPUs) v3 competence on RM MM PM (smoke first), then
#                                            note 9's never-named swap at L42-53, k 10 30 100, references capped at 80
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 10 addendum)"
waitjob() { echo "=== waiting for $1 $(date -u +%T)"; until grep -qsE "^EXIT [0-9]+" /workspace/runs/$1.log; do sleep 60; done; echo "=== $1 ended: $(grep -E '^EXIT' /workspace/runs/$1.log | tail -1)"; }
PREP=$1; shift
waitjob $PREP
grep -qa "^BOLT READY" /workspace/runs/$PREP.log || { echo "=== Bolt not ready"; exit 3; }
for j in "$@"; do waitjob $j; done
export CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=nemotron-3.5-bolt
C=nem35b_jsuite_v3_test_chat_competence_cand2_v1
$PY scripts/natural_v1.py competence --set jsuite_v3_test_chat --name nem35b_jsuite_v3_test_chat_competence_smoke1028 --words RM MM PM --read cand2 \
  --hop1 gen --limit 8 --why "$W: smoke" > /workspace/scratch/bolt_comp_smoke.log 2>&1 || { echo "=== Bolt smoke FAILED"; tail -5 /workspace/scratch/bolt_comp_smoke.log; exit 3; }
mv results/tasks_v2/nem35b_jsuite_v3_test_chat_competence_smoke1028 /workspace/scratch/
echo "=== Bolt smoke OK $(date -u +%T)"
[ -f results/tasks_v2/$C/summary.json ] || $PY scripts/natural_v1.py competence --set jsuite_v3_test_chat --name $C --words RM MM PM --read cand2 --hop1 gen \
  --why "$W: Bolt v3 competence on RM and its references MM, PM (eligibility)" > /workspace/scratch/$C.log 2>&1 || { echo "=== $C FAILED"; tail -3 /workspace/scratch/$C.log; exit 3; }
echo "=== done $C $(date -u +%T)"
r=nem35b_nn_swap_L42-53_v1
[ -f results/nn_swap/$r/summary.json ] || $PY scripts/nn_swap.py --name $r --why "$W: Bolt never-named swap at L42-53, references capped at 80" --band 42-53 \
  --competence $C --words RM MM PM --scene-words RM MM PM --sample-refs 80 --ks 10 30 100 > /workspace/scratch/$r.log 2>&1 || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; exit 3; }
echo "=== done $r $(date -u +%T)"
