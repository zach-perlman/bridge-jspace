#!/bin/bash
# Zach (2026-10-23, prereg amendment 13): the natural pilot re-scored with the candidate-rank read (ablate_v2 --read cand,
# natural_v1.py competence --read cand): correct = the answer's first token is the top among its relation's answers.
# Usage: h200_cand_1023.sh GPU STEP...   steps: TARGET:PREFIX:SET:BAND:BATCH[:unembed]
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
WHY="Zach (2026-10-23, prereg amendment 13): candidate-rank read"
for spec in "$@"; do
  IFS=: read -r t p set band batch extra <<< "$spec"
  export BJ_TARGET=$t
  c=${p}${set}_competence_cand_v1; r=${p}${set}_ko_cand_v1
  echo "=== competence $c $(date -u +%T)"
  [ -f results/tasks_v2/$c/summary.json ] || $PY scripts/natural_v1.py competence --set $set --name $c --read cand --why "$WHY: $t on $set" \
    > /workspace/scratch/$c.log 2>&1 || { echo "=== $t $set competence FAILED"; tail -3 /workspace/scratch/$c.log; continue; }
  python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== cand $t $set whole:', {k: v['whole'] for k, v in s.items()})" results/tasks_v2/$c/summary.json
  T="--tasks $set --tasks-competence $c --tasks-words PP PM MP MM --tasks-level all --n 1000 --kinds clean --batch $batch --read cand"
  conds="paper10 paper10_rot"; [ "${extra:-}" = unembed ] && conds="paper10 paper10_rot unembed10 unembed10_rot"
  echo "=== ablate_v2/$r $(date -u +%T)"
  [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$WHY: $t, C1 on $set at L$band" --plan bands --bands $band \
    --conditions $conds $T > /workspace/scratch/$r.log 2>&1 || { echo "=== $t $set C1 FAILED"; tail -3 /workspace/scratch/$r.log; continue; }
  $PY scripts/c1_v2.py $r --middle L$band --set $set | tail -2
  [ "${extra:-}" = unembed ] && $PY scripts/c1_specificity.py $r $r --set $set | tail -2 | sed "s/^/=== spec $t: /"
done
echo "=== cand GPU $G done $(date -u +%FT%TZ)"
