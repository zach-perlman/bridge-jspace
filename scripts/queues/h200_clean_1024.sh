#!/bin/bash
# Zach (2026-10-24): the clean-checkout rerun CLAUDE.md asks for before a result is called positive. The 27B's module 1
# headline (jsuite_v1_facts_test_chat at L32-40, competence then paper10 / rot / unembed10 / rot, cand2, jsuite_score),
# rerun from a fresh git worktree of the committed HEAD (/workspace/clean_bridge: tracked code and data only, empty
# results and cache) with the same Python environment and model / lens caches, then compared row by row with the run of
# record (results/ablate_v2/jsuite_v1_facts_test_chat_ko_cand2_v1). Usage: h200_clean_1024.sh GPU
set -u
G=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_TARGET=qwen3.6-27b
PYX=/workspace/bridge-jspace/.venv/bin/python
C=/workspace/clean_bridge
[ -d $C ] || git worktree add --detach $C HEAD > /dev/null 2>&1 || { echo "=== CLEAN worktree FAILED"; exit 1; }
echo "=== CLEAN worktree at $(git -C $C rev-parse --short HEAD); untracked in it: $(git -C $C status --short | wc -l) $(date -u +%T)"
cd $C
# The worktree carries the committed results, so the rerun writes under clean_ names (same items, same settings).
SET=jsuite_v1_facts_test_chat; ocn=${SET}_competence_cand2_v1; orr=${SET}_ko_cand2_v1; cn=clean_$ocn; r=clean_$orr
[ -f results/tasks_v2/$cn/summary.json ] || $PYX scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen \
  --why "Zach (2026-10-24): clean-checkout rerun of the 27B module 1 headline" > /workspace/scratch/clean_$cn.log 2>&1 || { echo "=== CLEAN competence FAILED"; tail -3 /workspace/scratch/clean_$cn.log; exit 1; }
echo "=== CLEAN competence done $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || $PYX scripts/ablate_v2.py --name $r --why "Zach (2026-10-24): clean-checkout rerun of the 27B module 1 headline" \
  --plan bands --bands 32-40 --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn \
  --tasks-words PP PK PM PA MP MK MM MA TP TK TM TA --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2 > /workspace/scratch/clean_$r.log 2>&1 \
  || { echo "=== CLEAN KO FAILED"; tail -3 /workspace/scratch/clean_$r.log; exit 1; }
$PYX scripts/jsuite_score.py $r | grep -E "^start all " | sed "s/^/=== CLEAN /"
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
echo "=== CLEAN done $(date -u +%FT%TZ)"
