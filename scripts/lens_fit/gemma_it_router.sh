#!/usr/bin/env bash
set -euo pipefail
cd /workspace/ext/jpp_lens
set -a; . /workspace/bridge-jspace/.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache
OUT=/workspace/ext/gemma_it_fit
mkdir -p $OUT
uv run --no-sync python scripts/jpp_cli.py fit-router --hf-model-name google/gemma-4-31B-it --layers 24,27,30,33,36,39,42,45 \
  --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 --out $OUT/router.pt
