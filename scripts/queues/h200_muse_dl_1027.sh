#!/bin/bash
# Zach (2026-10-27, prereg amendment 57 note 5): drop DeepSeek-V4-Flash's cache (its runs are done, amendment 56 D) with
# the Bolt tool (only files no other model references), then download Muse Glimmer 30B at pins.py's revision.
# The Muse runs themselves are separate jobs that wait for this one (note 5).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
DS=models--deepseek-ai--DeepSeek-V4-Flash
[ -d /workspace/hf_cache/hub/$DS ] && python3 /workspace/scratch/cache_drop.py $DS | sed "s/^/=== MUSE /"
free=$(df -BG --output=avail /workspace | tail -1 | tr -dc 0-9)
echo "=== MUSE download, $free GB free $(date -u +%T)"
[ "$free" -ge 75 ] || [ -d /workspace/hf_cache/hub/models--meta-models--Muse-Glimmer-30B/snapshots/cec94fcfd6512f2cfe708138c32533b346ea4f69 ] || { echo "=== MUSE download: only $free GB free, stop"; exit 1; }
CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
from huggingface_hub import snapshot_download
print('=== MUSE download done', snapshot_download('meta-models/Muse-Glimmer-30B', revision='cec94fcfd6512f2cfe708138c32533b346ea4f69'))" 2>&1 | grep "=== MUSE" || { echo "=== MUSE download FAILED"; exit 1; }
