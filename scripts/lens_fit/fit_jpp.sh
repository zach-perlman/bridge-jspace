#!/usr/bin/env bash
# One-command J++ fit for a new target model (Zach, 2026-10-20), generalised from gemma_it_fit_full.sh / _rest.sh.
# The official recipe (safety-research/jpp_lens@93f02cd; Ayonrinde & Lindsey 2026): WikiText texts x 128 tokens, the
# first 16 positions skipped, target = the final block, LRP rules, 8 experts, readout weights fit on the fit:0 items the
# model answers right, held-out evaluation on held-out:0. Decided with Zach (2026-10-20): 32 prompts; every layer in
# the middle of the model (25-80% depth) in one pass, since a full-depth fit does not fit an H200 next to a 32B model.
#
# usage: fit_jpp.sh MODEL LAYERS OUT [N_PROMPTS=32] [LRP_MODE=rlens]
#   MODEL   HF name, e.g. Qwen/Qwen3-32B          LAYERS  comma-separated source layers (e.g. $(seq -s, 16 51))
#   OUT     output directory (router, shard, experts, correctness CSV, lens, evaluation)
set -euo pipefail
MODEL=$1 LAYERS=$2 OUT=$3 N=${4:-32} LRP=${5:-rlens}
# JPP_ROWS (env, default 16): Jacobian rows per backward pass, a batching knob (the same estimator); 2026-10-21: 32 on
# the B200 where it fits (decided with Zach), 16 as the fallback.
cd /workspace/ext/jpp_lens
set -a; . /workspace/bridge-jspace/.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache
mkdir -p "$OUT"
C="uv run --no-sync python scripts/jpp_cli.py"
M="--hf-model-name $MODEL"
STEM=$(basename "$MODEL")
echo "=== router $(date -u +%H:%M:%S)"
$C fit-router $M --layers "$LAYERS" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 --out "$OUT/router.pt"
echo "=== fit-shard ($N prompts) $(date -u +%H:%M:%S)"
$C fit-shard $M --layers "$LAYERS" --router-path "$OUT/router.pt" --shard-idx 0 --num-shards 1 --num-prompts "$N" \
  --target-offset -1 --lrp-mode "$LRP" --jacobian-rows-per-pass "${JPP_ROWS:-16}" --max-seq-len 128 --skip-first-n-positions 16 \
  --checkpoint-every-n-prompts 8 --artifacts-base-dir "$OUT/artifacts" --checkpoint-name "fit$N"
SHARD=$(ls -d "$OUT"/artifacts/*/fit"$N"/shard0of1 | tail -1)
echo "=== merge $(date -u +%H:%M:%S)"
$C merge-experts --checkpoint-dirs "$SHARD" --out "$OUT/experts.pt" --pooled-lens-out "$OUT/pooled_lens.pt"
echo "=== grade $(date -u +%H:%M:%S)"
uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py "$MODEL" "$LAYERS" "$OUT/model_correctness.csv"
echo "=== fit-weights $(date -u +%H:%M:%S)"
$C fit-weights $M --layers "$LAYERS" --experts "$OUT/experts.pt" --items fit:0 --correctness-csv "$OUT/model_correctness.csv" \
  --cache-path "$OUT/readout_cache.pt" --out "$OUT/${STEM}_jpp_lens.pt"
echo "=== evaluate $(date -u +%H:%M:%S)"
$C evaluate $M --layers "$LAYERS" --lens "$OUT/${STEM}_jpp_lens.pt" "$OUT/pooled_lens.pt" --items held-out:0 \
  --correctness-csv "$OUT/model_correctness.csv" --out "$OUT/eval_ranks.csv"
echo "FIT_DONE $OUT/${STEM}_jpp_lens.pt"
