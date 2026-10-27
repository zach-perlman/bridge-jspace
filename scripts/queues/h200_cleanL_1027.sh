#!/bin/bash
# Zach (2026-10-27, amendment 54 part C): Lightning's v2 headline from the clean worktree /workspace/clean_bridge at HEAD,
# compared row by row with the runs of record (as amendment 50 for the 27B). A fixed copy of h200_dose_1026.sh's clean
# step: its run names now start with the model prefix (nem35l_clean_...), which pins.check_run_name requires.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=${1:-0} BJ_TARGET=nemotron-3.5-lightning
unset BJ_GRAM_PROJ
PYX=/workspace/bridge-jspace/.venv/bin/python
SET=jsuite_v2_test_chat; P=nem35l_; BAND=27-33; B=16
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
CL=/workspace/clean_bridge; H=$(git rev-parse HEAD)
[ -z "$(git -C $CL status --short --untracked-files=no)" ] || { echo "=== CLEAN worktree has tracked changes; stop"; exit 1; }
git -C $CL checkout -q --detach $H || { echo "=== CLEAN checkout FAILED"; exit 1; }
echo "=== CLEAN nem35l worktree at $(git -C $CL rev-parse --short HEAD) $(date -u +%T)"
ocn=${P}${SET}_competence_cand2_v1; orr=${P}${SET}_ko_cand2_v1; cn=${P}clean_${SET}_competence_cand2_v1; r=${P}clean_${SET}_ko_cand2_v1
W="Zach (2026-10-27, amendment 54 part C): clean-checkout rerun of Lightning's headline"
cd $CL
[ -f results/tasks_v2/$cn/summary.json ] || $PYX scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen --why "$W" \
  > /workspace/scratch/$cn.log 2>&1 < /dev/null || { echo "=== CLEAN competence FAILED"; tail -3 /workspace/scratch/$cn.log; exit 1; }
echo "=== CLEAN nem35l competence done $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || $PYX scripts/ablate_v2.py --name $r --why "$W" --plan bands --bands $BAND \
  --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn --tasks-words $FACTS \
  --tasks-level all --n 1000 --kinds clean --batch $B --read cand2 > /workspace/scratch/$r.log 2>&1 < /dev/null \
  || { echo "=== CLEAN KO FAILED"; tail -3 /workspace/scratch/$r.log; exit 1; }
$PYX scripts/jsuite2_score.py $r --set $SET | grep -E "^facts (paper10|unembed10) +start=all" | sed "s/^/=== CLEAN nem35l /"
$PYX - "$CL/results" /workspace/bridge-jspace/results "$ocn" "$orr" "$cn" "$r" <<'PY'
import json, sys
new, old, ocn, orr, cn, r = sys.argv[1:]
def rows(base, sub, name, key):
    return {key(x): x for x in map(json.loads, open(f"{base}/{sub}/{name}/{'items' if sub == 'tasks_v2' else 'rows'}.jsonl"))}
kc = lambda x: (x["id"], x["part"])
kr = lambda x: (x["family"], x["id"], x["kind"], x["band"], x["condition"])
for sub, oname, name, key, fields in (("tasks_v2", ocn, cn, kc, ("correct", "correct_cand2", "correct_top", "gen")), ("ablate_v2", orr, r, kr, ("correct", "correct_cand2", "correct_top"))):
    a, b = rows(old, sub, oname, key), rows(new, sub, name, key)
    shared = set(a) & set(b)
    diff = {f: sum(a[k].get(f) != b[k].get(f) for k in shared) for f in fields}
    lp = max((abs(a[k].get("logp", 0) - b[k].get("logp", 0)) for k in shared), default=0)
    print(f"=== CLEAN {sub}: rows old {len(a)} new {len(b)} shared {len(shared)}; differing {diff}; max |logp diff| {lp:.2e}")
PY
echo "=== CLEAN nem35l done $(date -u +%T)"
