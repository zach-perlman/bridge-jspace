#!/bin/bash
# Zach (2026-10-26, amendment 49 note 4): with Bolt's queue profile script (PID $1) paused, once its dev competence (PID
# $2) has exited: (1) the dev profile in right-padded batches, with the queue's arguments plus --pad; (2) the padded
# competence path checked against the exact-length dev competence on the first 400 dev items (agreement on `correct`
# >= 0.99, else stop here); (3) if it passes, Bolt's test competence by the padded path under the queue's own run name,
# so the queue skips it; then the queue script is resumed (it finds the profile's summary and skips its own run).
set -u
QPID=$1; CPID=$2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=nemotron-3.5-bolt
PY="uv run --no-sync python"
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
resume() { kill -CONT $QPID && echo "=== queue script resumed $(date -u +%T)"; }
trap resume EXIT
while kill -0 $CPID 2>/dev/null; do sleep 20; done
echo "=== competence child exited $(date -u +%T)"
DC=nem35b_jsuite_v2_dev_chat_competence_cand2_v1
r=nem35b_jsuite_v2_dev_chat_profile_cand2_v1
[ -f results/tasks_v2/$DC/summary.json ] || { echo "=== no dev competence summary; nothing run"; exit 0; }
if [ ! -f results/ablate_v2/$r/summary.json ]; then
  echo "=== PADPROF $r $(date -u +%T)"
  $PY scripts/ablate_v2.py --name $r --why "Zach (2026-10-25, prereg amendment 42): nemotron-3.5-bolt depth profile on the dev split" --plan bands \
    --bands 0-11 6-17 12-23 18-29 24-35 30-41 36-47 42-53 48-59 54-65 60-71 66-77 72-83 --conditions paper10 paper10_rot unembed10 --tasks jsuite_v2_dev_chat \
    --tasks-competence $DC --tasks-words PP PK PM MP MK MM --tasks-level all --n 1000 --kinds clean --batch 16 --read cand2 \
    --sample-per-word 40 --sample-seed 0 --pad > /workspace/scratch/$r.log 2>&1 < /dev/null \
    && echo "=== PADPROF done $(date -u +%T)" || { echo "=== PADPROF FAILED (the queue runs its own profile)"; tail -3 /workspace/scratch/$r.log; mv results/ablate_v2/$r /workspace/scratch/killed_1025/${r}_padfail 2>/dev/null; }
fi
CK=nem35b_jsuite_v2_dev_chat_competence_fastcheck_1026
echo "=== FASTCOMP check $(date -u +%T)"
$PY scripts/natural_v1.py competence --set jsuite_v2_dev_chat --name $CK --read cand2 --hop1 gen --words $FACTS --limit 400 \
  --why "Zach (2026-10-26, amendment 49 note 4): padded competence path vs the exact-length run, first 400 dev items" > /workspace/scratch/$CK.log 2>&1 < /dev/null \
  || { echo "=== FASTCOMP check FAILED to run"; tail -3 /workspace/scratch/$CK.log; exit 0; }
v=$(python3 - results/tasks_v2/$DC/items.jsonl results/tasks_v2/$CK/items.jsonl <<'PY'
import json, sys
a = {(r["id"], r["part"]): r for r in map(json.loads, open(sys.argv[1]))}
b = {(r["id"], r["part"]): r for r in map(json.loads, open(sys.argv[2]))}
k = sorted(set(a) & set(b))
ag = lambda f: sum(a[x].get(f) == b[x].get(f) for x in k) / len(k)
g = [x for x in k if x[1] == "step1"]
gen = sum(a[x].get("correct_gen") == b[x].get("correct_gen") for x in g) / max(1, len(g))
c = ag("correct")
print(("PASS" if c >= 0.99 else "STOP"), f"shared {len(k)} parts; agreement correct {c:.4f}, correct_cand2 {ag('correct_cand2'):.4f}, correct_top {ag('correct_top'):.4f}, hop-1 gen {gen:.4f} (n {len(g)})")
PY
)
echo "=== FASTCOMP $v"
[[ $v == PASS* ]] || exit 0
TC=nem35b_jsuite_v2_test_chat_competence_cand2_v1
if [ ! -f results/tasks_v2/$TC/summary.json ]; then
  echo "=== FASTCOMP test competence $(date -u +%T)"
  $PY scripts/natural_v1.py competence --set jsuite_v2_test_chat --name $TC --read cand2 --hop1 gen --words $FACTS \
    --why "Zach (2026-10-26, amendment 49 note 4): nemotron-3.5-bolt on jsuite_v2_test_chat (padded path)" > /workspace/scratch/$TC.log 2>&1 < /dev/null \
    && python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== NQCOMP nemotron-3.5-bolt', {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$TC/summary.json \
    || { echo "=== FASTCOMP test competence FAILED (the queue runs its own)"; tail -3 /workspace/scratch/$TC.log; mv results/tasks_v2/$TC /workspace/scratch/killed_1025/${TC}_fastfail 2>/dev/null; }
fi
echo "=== padprof done $(date -u +%T)"
