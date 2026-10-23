#!/bin/bash
# Zach (2026-10-23, prereg amendment 15): nat3_v1_chat, all 8 three-step words, candidate-rank read, per-word
# eligibility. Usage: h200_nat3_1023.sh GPU TARGET:PREFIX:BAND:BATCH ...
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
WHY="Zach (2026-10-23, prereg amendment 15): three-step natural chains"
set_=nat3_v1_chat
for spec in "$@"; do
  IFS=: read -r t p band batch <<< "$spec"
  export BJ_TARGET=$t
  c=${p}${set_}_competence_cand_v1; r=${p}${set_}_ko_cand_v1
  echo "=== competence $c $(date -u +%T)"
  [ -f results/tasks_v2/$c/summary.json ] || $PY scripts/natural_v1.py competence --set $set_ --name $c --read cand --why "$WHY: $t" \
    > /workspace/scratch/$c.log 2>&1 || { echo "=== $t competence FAILED"; tail -3 /workspace/scratch/$c.log; continue; }
  python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== nat3 $t whole:', {k: v['whole'] for k, v in s.items()})" results/tasks_v2/$c/summary.json
  echo "=== ablate_v2/$r $(date -u +%T)"
  [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$WHY: $t at L$band" --plan bands --bands $band \
    --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $set_ --tasks-competence $c \
    --tasks-words PPP MPP PMP PPM MPM MMP PMM MMM --tasks-level all --tasks-per-word --n 1000 --kinds clean --batch $batch --read cand \
    > /workspace/scratch/$r.log 2>&1 || { echo "=== $t C1 FAILED"; tail -3 /workspace/scratch/$r.log; continue; }
  $PY scripts/nat3_score.py $r | grep -E "^all" | sed "s/^/=== nat3 $t: /"
done
echo "=== nat3 GPU $G done $(date -u +%FT%TZ)"
