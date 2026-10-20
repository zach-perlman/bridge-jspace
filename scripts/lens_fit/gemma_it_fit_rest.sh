#!/usr/bin/env bash
# Resume of gemma_it_fit_full.sh after its grading step failed (fit-shard and merge-experts done, 2026-10-20 07:06):
# grade, fit-weights, evaluate (the new lens, the pooled lens, the base-model J++). Zach, 2026-10-20.
set -euo pipefail
cd /workspace/ext/jpp_lens
set -a; . /workspace/bridge-jspace/.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache
OUT=/workspace/ext/gemma_it_fit
L=24,27,30,33,36,39,42,45
C="uv run --no-sync python scripts/jpp_cli.py"
M="--hf-model-name google/gemma-4-31B-it"
uv run --no-sync python $OUT/grade.py $OUT/model_correctness.csv
$C fit-weights $M --layers $L --experts $OUT/experts.pt --items fit:0 --correctness-csv $OUT/model_correctness.csv \
  --cache-path $OUT/readout_cache.pt --out $OUT/gemma-4-31B-it_jpp_lens.pt
echo LENS_DONE
$C evaluate $M --layers $L --lens $OUT/gemma-4-31B-it_jpp_lens.pt $OUT/pooled_lens.pt --items held-out:0 \
  --correctness-csv $OUT/model_correctness.csv --out $OUT/eval_ranks.csv
BASE=/workspace/hf_cache/hub/models--neuronpedia--jacobian-lens/snapshots/e166deb5ad540932100ef803c8c9bcc2a5453694/gemma-4-31b/jpp/Salesforce-wikitext/gemma-4-31B_jpp_lens.pt
$C evaluate $M --layers $L --lens $BASE --items held-out:0 --correctness-csv $OUT/model_correctness.csv \
  --out $OUT/eval_ranks_baselens.csv || echo "base-lens evaluate failed; skipped"
echo FIT_DONE
