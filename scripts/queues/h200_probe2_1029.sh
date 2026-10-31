#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 23 addendum 2): the read-out with more training data. Usage: h200_probe2_1029.sh MODEL GPU
set -u
M=$1; G=$2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_ ;;
  27b) export BJ_TARGET=qwen3.6-27b; P= ;;
esac
W="Zach (2026-10-29, prereg amendment 58 note 23 addendum 2, $BJ_TARGET)"
EX=""
for s in 4002 4003 4004 4005 4006; do
  [ -d data/tasks_v2/jsuite_v4p${s}_test_chat ] || .venv/bin/python scripts/jsuite_v4.py --seed $s --name jsuite_v4p$s > /workspace/scratch/jsuite_v4p$s.log 2>&1 \
    || { echo "=== generator $s FAILED"; tail -3 /workspace/scratch/jsuite_v4p$s.log; exit 1; }
  EX="$EX jsuite_v4p${s}_test_chat"
done
sha256sum data/tasks_v2/jsuite_v4p400?_test_chat/items.jsonl | cut -c1-16
C=${P}jsuite_v4_test_chat_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
# shellcheck disable=SC2086
$PY scripts/nn_probe_v4.py --name ${P}nn_probe_v4_smoke1029b --why "$W smoke" --competence $C --cv-h1 $CV --extra-sets $EX --limit 3000 --steps 20 \
  > /workspace/scratch/${P}nn_probe_v4_smoke1029b.log 2>&1 < /dev/null || { echo "=== smoke FAILED"; tail -5 /workspace/scratch/${P}nn_probe_v4_smoke1029b.log; exit 1; }
mv results/nn_probe_v4/${P}nn_probe_v4_smoke1029b /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
r=${P}nn_probe_v4_v2
# shellcheck disable=SC2086
$PY scripts/nn_probe_v4.py --name $r --why "$W: more training data" --competence $C --cv-h1 $CV --readout ${P}nn_readout_v4_v1 --extra-sets $EX \
  > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; exit 1; }
echo "=== note 23b $M done $(date -u +%FT%TZ)"
