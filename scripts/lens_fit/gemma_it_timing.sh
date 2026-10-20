#!/usr/bin/env bash
set -uo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-gfitrouter-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 15; done
grep -q '^EXIT 0' "$PREV" || { echo "router failed"; exit 1; }
cd /workspace/ext/jpp_lens
set -a; . /workspace/bridge-jspace/.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache
OUT=/workspace/ext/gemma_it_fit
for R in 16 8; do
  t0=$(date +%s)
  uv run --no-sync python scripts/jpp_cli.py fit-shard --hf-model-name google/gemma-4-31B-it --layers 24,27,30,33,36,39,42,45 \
    --router-path $OUT/router.pt --shard-idx 0 --num-shards 1 --num-prompts 1 --target-offset -1 --lrp-mode rlens \
    --jacobian-rows-per-pass $R --max-seq-len 128 --skip-first-n-positions 16 --checkpoint-every-n-prompts 1 \
    --artifacts-base-dir $OUT/artifacts --checkpoint-name timing_r$R && { echo "TIMING rows=$R seconds=$(( $(date +%s) - t0 ))"; break; }
  echo "rows=$R failed"
done
