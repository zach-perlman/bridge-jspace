#!/usr/bin/env bash
# Set up a fresh 2x H200 box for the Qwen3-32B J++ fit (Dan, 22-23 Oct night): uv, the recipe
# (safety-research/jpp_lens@93f02cd) with its environment, the weights (Qwen3-32B at the pinned revision; Qwen3.5-0.8B
# for the merge check). No token is written to disk; the models are public.
# usage (on the box): bash ~/work/bridge-jspace/scripts/lens_fit/h200_setup.sh > ~/work/setup.log 2>&1
set -euo pipefail
W=$HOME/work
mkdir -p "$W"
export UV_CACHE_DIR=$W/uv-cache HF_HOME=$W/hf
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=$HOME/.local/bin:$PATH
cd "$W"
[ -d jpp_lens ] || git clone -q https://github.com/safety-research/jpp_lens.git
cd jpp_lens && git checkout -q 93f02cd && git log --oneline -1
uv sync --extra cu128  # torch is an extra of the recipe (cu128: CUDA 12.8 GPUs)
echo "=== weights $(date -u +%H:%M:%S)"
uv run --no-sync python -c "
from huggingface_hub import snapshot_download
print(snapshot_download('Qwen/Qwen3.5-0.8B', revision='2fc06364715b967f1860aea9cf38778875588b17'))
print(snapshot_download('Qwen/Qwen3-32B', revision='9216db5781bf21249d130ec9da846c4624c16137'))
"
echo "SETUP_DONE $(date -u +%H:%M:%S)"
