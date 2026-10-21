#!/bin/bash
# Zach (2026-10-21, decided with Zach: no idle GPU): the Qwen3-32B every-layer J++ fit split across both GPUs at the end.
# Usage: h200_q32_shard_1021.sh K (K = 0 or 1, the GPU and the shard). The recipe of qwen3_32b_fit_1020.sh / fit_jpp.sh
# (layers 0-62, 32 WikiText prompts, skip 16, target = the final block, LRP rlens, 8 experts, 32 rows per pass where it
# fits else 16), with fit-shard run as 2 shards of 16 prompts (shard K on GPU K, after that GPU's Gemma branch); the
# shard statistics are summed by merge-experts, so it is the same estimator. Shard 0 also fits the router (and runs a
# 1-prompt smoke first); shard 1 waits for the router. The merge and the rest run in h200_q32_merge_1021.sh.
set -u
K=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=$K UV_CACHE_DIR=/workspace/uv-cache
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
OUT=/workspace/ext/qwen3_32b_fit M="--hf-model-name Qwen/Qwen3-32B" LAYERS=$(seq -s, 0 62)
if [ "$K" = 0 ]; then until grep -qs "^EXIT" $R-h200gemmaA2-*.log; do sleep 60; done; else until grep -qs "^EXIT" $R-h200gemmaB3-*.log; do sleep 60; done; fi
echo "=== GPU $K free $(date -u +%FT%TZ)"
mkdir -p "$OUT"
cd /workspace/ext/jpp_lens
C="uv run --no-sync python scripts/jpp_cli.py"
if [ "$K" = 0 ]; then
  SMOKE=/workspace/scratch/q32_fit_smoke
  bash /workspace/bridge-jspace/scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 > /workspace/scratch/q32_smoke.log 2>&1 \
    && rm -rf "$SMOKE" || { echo "32B fit smoke failed"; tail -20 /workspace/scratch/q32_smoke.log; exit 1; }
  echo "=== router $(date -u +%T)"
  $C fit-router $M --layers "$LAYERS" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 --out "$OUT/router.tmp.pt" \
    > /workspace/scratch/q32_router.log 2>&1 && mv "$OUT/router.tmp.pt" "$OUT/router.pt" || { echo "router failed"; exit 1; }
else
  until [ -f "$OUT/router.pt" ]; do sleep 60; done
fi
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
