#!/usr/bin/env bash
# J++ on google/gemma-4-31B-it, the published recipe (64 wikitext texts x 128 tokens, skip 16, target = final block,
# LRP rlens, 8 experts) at layers 24-45 (every 3rd), safety-research/jpp_lens@93f02cd. Zach, 2026-10-20.
set -euo pipefail
cd /workspace/ext/jpp_lens
set -a; . /workspace/bridge-jspace/.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache
OUT=/workspace/ext/gemma_it_fit
L=24,27,30,33,36,39,42,45
C="uv run --no-sync python scripts/jpp_cli.py"
M="--hf-model-name google/gemma-4-31B-it"
$C fit-shard $M --layers $L --router-path $OUT/router.pt --shard-idx 0 --num-shards 1 --num-prompts 64 --target-offset -1 \
  --lrp-mode rlens --jacobian-rows-per-pass 16 --max-seq-len 128 --skip-first-n-positions 16 --checkpoint-every-n-prompts 8 \
  --artifacts-base-dir $OUT/artifacts --checkpoint-name fit64
SHARD=$(ls -d $OUT/artifacts/*/fit64/shard0of1 | tail -1)
$C merge-experts --checkpoint-dirs $SHARD --out $OUT/experts.pt --pooled-lens-out $OUT/pooled_lens.pt
uv run --no-sync python $OUT/grade.py $OUT/model_correctness.csv
$C fit-weights $M --layers $L --experts $OUT/experts.pt --items fit:0 --correctness-csv $OUT/model_correctness.csv \
  --cache-path $OUT/readout_cache.pt --out $OUT/gemma-4-31B-it_jpp_lens.pt
$C evaluate $M --layers $L --lens $OUT/gemma-4-31B-it_jpp_lens.pt $OUT/pooled_lens.pt --items held-out:0 \
  --correctness-csv $OUT/model_correctness.csv --out $OUT/eval_ranks.csv
BASE=/workspace/hf_cache/hub/models--neuronpedia--jacobian-lens/snapshots/e166deb5ad540932100ef803c8c9bcc2a5453694/gemma-4-31b/jpp/Salesforce-wikitext/gemma-4-31B_jpp_lens.pt
$C evaluate $M --layers $L --lens $BASE --items held-out:0 --correctness-csv $OUT/model_correctness.csv \
  --out $OUT/eval_ranks_baselens.csv || echo "base-lens evaluate failed (format); skipped"
echo FIT_DONE
