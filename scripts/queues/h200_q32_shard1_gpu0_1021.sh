#!/bin/bash
# Zach (2026-10-21, "no wasted GPU time"; replaces the waiting h200_q32_shard_1021.sh 1): shard 1 of the Qwen3-32B
# fit on GPU 0 right after shard 0. It waited for the Gemma knock-outs on GPU 1 (until ~09:00 UTC on 10-22), which
# left GPU 0 idle for hours after shard 0. Same recipe and statistics as h200_q32_shard_1021.sh with K = 1.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=0 UV_CACHE_DIR=/workspace/uv-cache
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
OUT=/workspace/ext/qwen3_32b_fit M="--hf-model-name Qwen/Qwen3-32B" LAYERS=$(seq -s, 0 62)
K=1
until grep -qs "^EXIT" $R-h200q32s0-*.log; do sleep 60; done
[ -f "$OUT/shard0.done" ] && [ -f "$OUT/router.pt" ] || { echo "shard 0 failed: stop"; exit 1; }
echo "=== GPU 0 free for shard 1 $(date -u +%FT%TZ)"
cd /workspace/ext/jpp_lens
C="uv run --no-sync python scripts/jpp_cli.py"
for rows in 32 16; do
  echo "=== fit-shard $K of 2, $rows rows per pass $(date -u +%T)"
  $C fit-shard $M --layers "$LAYERS" --router-path "$OUT/router.pt" --shard-idx $K --num-shards 2 --num-prompts 32 \
    --target-offset -1 --lrp-mode rlens --jacobian-rows-per-pass $rows --max-seq-len 128 --skip-first-n-positions 16 \
    --checkpoint-every-n-prompts 8 --artifacts-base-dir "$OUT/artifacts" --checkpoint-name fit32 > /workspace/scratch/q32_shard$K.log 2>&1 \
    && { touch "$OUT/shard$K.done"; echo "=== shard $K done $(date -u +%T)"; exit 0; }
  echo "=== $rows rows failed ($(grep -m1 -oiE "out of memory" /workspace/scratch/q32_shard$K.log))"
  rm -rf "$OUT"/artifacts/*/fit32/shard${K}of2
done
exit 1
