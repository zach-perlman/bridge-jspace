#!/bin/bash
# Zach (2026-10-23, prereg amendment 18): WorkspaceBench wrong-bridge items. GPU 1, alongside the band sweeps.
set -u
G=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
W="Zach (2026-10-23, prereg amendment 18): WorkspaceBench wrong-bridge items"
waitmem() { until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge "$1" ]; do sleep 30; done; }
waitmem 70000
echo "=== wrong_bridge/wb_wrong_bridge_v1 $(date -u +%T)"
[ -f results/wrong_bridge/wb_wrong_bridge_v1/summary.json ] || BJ_TARGET=qwen3.6-27b $PY scripts/wrong_bridge_causal.py --name wb_wrong_bridge_v1 \
  --why "$W: the 27B at L32-40" --band 32-40 --batch 4 2>&1 | grep -a "^WB" || echo "=== 27B wrong_bridge FAILED"
for spec in "qwen3.5-9b:qwen35_9b_:12-16" "muse-glimmer-30b:muse30_:36-42"; do
  t=${spec%%:*}; rest=${spec#*:}; p=${rest%%:*}; band=${rest#*:}
  waitmem 70000
  echo "=== wrong_bridge/${p}wb_screen_v1 $(date -u +%T)"
  [ -f results/wrong_bridge/${p}wb_screen_v1/summary.json ] || BJ_TARGET=$t $PY scripts/wrong_bridge_causal.py --name ${p}wb_screen_v1 \
    --why "$W: does $t answer through the same wrong bridges?" --band $band --screen 2>&1 | grep -a "^SCREEN" || echo "=== $t screen FAILED"
done
n9=$(python3 -c "import json; print(len(json.load(open('results/wrong_bridge/qwen35_9b_wb_screen_v1/screen.json'))['transfer']))" 2>/dev/null || echo 0)
echo "=== 9B transfer: $n9 items"
if [ "$n9" -ge 30 ]; then
  echo "=== wrong_bridge/qwen35_9b_wb_wrong_bridge_v1 $(date -u +%T)"
  [ -f results/wrong_bridge/qwen35_9b_wb_wrong_bridge_v1/summary.json ] || BJ_TARGET=qwen3.5-9b $PY scripts/wrong_bridge_causal.py --name qwen35_9b_wb_wrong_bridge_v1 \
    --why "$W: the 9B on the items it also answers through the wrong bridge, at L12-16" --band 12-16 --batch 8 \
    --items-from results/wrong_bridge/qwen35_9b_wb_screen_v1/screen.json 2>&1 | grep -a "^WB" || echo "=== 9B wrong_bridge FAILED"
fi
echo "=== wrong_bridge done $(date -u +%FT%TZ)"
