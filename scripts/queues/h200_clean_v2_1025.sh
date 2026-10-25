#!/bin/bash
# Zach (2026-10-25, prereg amendment 37 C): the clean-checkout rerun of the v2 headline, the 9B (jsuite_v2_test_chat at
# L12-16, competence then paper10 / rot / unembed10 / rot on the 15 facts words, cand2, jsuite2_score), from the worktree
# /workspace/clean_bridge moved to the current HEAD (tracked code and data only; its untracked results are the v1 rerun's,
# under other names), with the same Python environment and model / lens caches; compared row by row with the runs of
# record. A copy of h200_clean_1024.sh (left as it ran) with the model, set, words and scorer changed. Usage: h200_clean_v2_1025.sh GPU
set -u
G=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_TARGET=qwen3.5-9b
PYX=/workspace/bridge-jspace/.venv/bin/python
C=/workspace/clean_bridge
H=$(git rev-parse HEAD)
[ -z "$(git -C $C status --short --untracked-files=no)" ] || { echo "=== CLEAN worktree has tracked changes; stop"; exit 1; }
git -C $C checkout -q --detach $H || { echo "=== CLEAN checkout FAILED"; exit 1; }
echo "=== CLEAN worktree at $(git -C $C rev-parse --short HEAD); tracked changes: $(git -C $C status --short --untracked-files=no | wc -l) $(date -u +%T)"
cd $C
SET=jsuite_v2_test_chat; ocn=qwen35_9b_${SET}_competence_cand2_v1; orr=qwen35_9b_${SET}_ko_cand2_v1
cn=qwen35_9b_clean_${SET}_competence_cand2_v1; r=qwen35_9b_clean_${SET}_ko_cand2_v1
W="Zach (2026-10-25, prereg amendment 37 C): clean-checkout rerun of the 9B v2 headline"
[ -f results/tasks_v2/$cn/summary.json ] || $PYX scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen \
  --why "$W" > /workspace/scratch/$cn.log 2>&1 || { echo "=== CLEAN competence FAILED"; tail -3 /workspace/scratch/$cn.log; exit 1; }
echo "=== CLEAN competence done $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || $PYX scripts/ablate_v2.py --name $r --why "$W" \
  --plan bands --bands 12-16 --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn \
  --tasks-words PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2 > /workspace/scratch/$r.log 2>&1 \
  || { echo "=== CLEAN KO FAILED"; tail -3 /workspace/scratch/$r.log; exit 1; }
$PYX scripts/jsuite2_score.py $r --set $SET | grep -E "^facts (paper10|unembed10) +start=all" | sed "s/^/=== CLEAN /"
$PYX - "$C/results" /workspace/bridge-jspace/results "$ocn" "$orr" "$cn" "$r" <<'PY'
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
echo "=== CLEAN done $(date -u +%T)"
