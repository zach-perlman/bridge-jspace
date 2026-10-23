#!/bin/bash
# Zach (2026-10-23, prereg amendment 12): the natural pilot (natural_v1_chat) on Olmo-Hybrid or Olmo-3.
# Usage: h200_amend12_1023.sh GPU olmoh|olmo3
set -u
G=$1; M=$2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
WHY="Zach (2026-10-23, prereg amendment 12)"
case $M in
  olmoh) export BJ_TARGET=olmo-hybrid-7b; p=olmoh7_; band=4-8;;
  olmo3) export BJ_TARGET=olmo-3-7b; p=olmo3d7_; band=10-14;;
esac
set_=natural_v1_chat; c=${p}${set_}_competence_v1; r=${p}${set_}_ko_v1
echo "=== competence $c $(date -u +%T)"
[ -f results/tasks_v2/$c/summary.json ] || $PY scripts/natural_v1.py competence --set $set_ --name $c --why "$WHY: $BJ_TARGET on $set_" > /workspace/scratch/$c.log 2>&1 \
  || { echo "=== $M competence FAILED"; tail -3 /workspace/scratch/$c.log; exit 1; }
python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== natural $M whole:', {k: v['whole'] for k, v in s.items()})" results/tasks_v2/$c/summary.json
T="--tasks $set_ --tasks-competence $c --tasks-words PP PM MP MM --tasks-level all --n 1000 --kinds clean --batch 32"
for pair in "$r:paper10 paper10_rot" "${r%_v1}_unembed_v1:unembed10 unembed10_rot"; do
  n=${pair%%:*}; conds=${pair#*:}
  echo "=== ablate_v2/$n $(date -u +%T)"
  [ -f results/ablate_v2/$n/summary.json ] || $PY scripts/ablate_v2.py --name $n --why "$WHY: $BJ_TARGET on $set_ at L$band ($conds)" --plan bands --bands $band \
    --conditions $conds $T > /workspace/scratch/$n.log 2>&1 || { echo "=== $M $conds FAILED"; tail -3 /workspace/scratch/$n.log; }
done
$PY scripts/c1_v2.py $r --middle L$band --set $set_ | tail -2
$PY scripts/c1_specificity.py $r ${r%_v1}_unembed_v1 --set $set_ | tail -3 | sed "s/^/=== spec $M: /"
echo "=== amendment 12 $M done $(date -u +%FT%TZ)"
