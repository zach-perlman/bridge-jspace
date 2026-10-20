#!/usr/bin/env bash
# Download Qwen/Qwen3-32B at a pinned revision into the shared HF cache (Zach, 2026-10-20; CPU/network only).
set -euo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
uv run --no-sync python -c "
from huggingface_hub import snapshot_download
p = snapshot_download('Qwen/Qwen3-32B', revision='9216db5781bf21249d130ec9da846c4624c16137',
                      allow_patterns=['*.json', '*.safetensors', '*.txt', 'tokenizer*', 'merges.txt', 'vocab.json'])
print('downloaded to', p)
"
df -h /workspace | tail -1
