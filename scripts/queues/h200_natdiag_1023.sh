#!/bin/bash
# Zach (2026-10-23, descriptive, after amendment 10B note 2): the Muse diagnostic on natural_v1_chat for the 27B (L32-40)
# and Muse (L36-42): is the bridge in the lens top 10, removed by the knock-out, and back after the band?
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
for spec in "qwen3.6-27b::32-40" "muse-glimmer-30b:muse30_:36-42"; do
  t=${spec%%:*}; rest=${spec#*:}; p=${rest%%:*}; b=${rest#*:}
  echo "=== muse_diag/${p}natural_diag_L${b}_v1 $(date -u +%T)"
  [ -f results/muse_diag/${p}natural_diag_L${b}_v1/summary.json ] || BJ_TARGET=$t $PY scripts/muse_diag.py --name ${p}natural_diag_L${b}_v1 \
    --why "Zach (2026-10-23, descriptive): the Muse diagnostic on natural_v1_chat, $t at its C1 band" --band $b --n 60 \
    --set natural_v1_chat --competence ${p}natural_v1_chat_competence_v1 2>&1 | grep -a "^DIAG" || echo "=== diag $t FAILED"
done
echo "=== natural diag done $(date -u +%FT%TZ)"
