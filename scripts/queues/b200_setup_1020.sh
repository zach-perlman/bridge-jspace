#!/usr/bin/env bash
# B200 setup (Zach, 2026-10-20: switch to the B200; use the faster kernels). The repo, its .env and jpp_lens came from
# the H200 at e4af295. Environments as on the H200 (torch 2.11.0+cu128, transformers 5.17.0, fla 0.5.2) plus
# causal-conv1d (the short convolution of the Qwen3.5/3.6 linear-attention layers; the H200 ran its torch fallback).
set -euo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache
mkdir -p "$HF_HOME" "$UV_CACHE_DIR" /workspace/scratch
echo "=== uv sync (bridge-jspace) $(date -u +%T)"
uv sync
echo "=== causal-conv1d $(date -u +%T)"
uv pip install --python .venv/bin/python ninja packaging wheel setuptools
TORCH_CUDA_ARCH_LIST="10.0" MAX_JOBS=96 uv pip install --python .venv/bin/python --no-build-isolation causal-conv1d
.venv/bin/python -c "import causal_conv1d, fla, torch, transformers; print('causal_conv1d', causal_conv1d.__version__, 'fla', fla.__version__, 'torch', torch.__version__, 'transformers', transformers.__version__)"
echo "=== downloads $(date -u +%T)"
uv run --no-sync python - <<'PY'
from huggingface_hub import hf_hub_download, snapshot_download
from bridge_jspace import pins
print(snapshot_download(pins.QWEN_REPO, revision=pins.QWEN_REVISION, max_workers=16))
repo, file, rev = pins.LENS_SOURCES["jpp"]
print(hf_hub_download(repo, file, revision=rev))
print(snapshot_download("Qwen/Qwen3-32B", revision="9216db5781bf21249d130ec9da846c4624c16137", max_workers=16,
                        allow_patterns=["*.json", "*.safetensors", "*.txt", "tokenizer*", "merges.txt", "vocab.json"]))
PY
echo "=== jpp_lens env $(date -u +%T)"
cd /workspace/ext/jpp_lens && uv sync --extra cu128 && .venv/bin/python -c "import torch; print('jpp_lens torch', torch.__version__)"
cd /workspace/bridge-jspace
echo "=== tests $(date -u +%T)"
uv run --no-sync python -m pytest -q tests/test_ablate.py 2>&1 | tail -2
df -h /workspace | tail -1
echo "=== setup done $(date -u +%T)"
