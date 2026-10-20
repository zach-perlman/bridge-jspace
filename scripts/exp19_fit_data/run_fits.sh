#!/usr/bin/env bash
# exp19_fit_data: fit one J++ lens per fitting pool on Qwen3.6-27B, then score them all in one evaluate call.
#   bash scripts/exp19_fit_data/run_fits.sh RUN_NAME   (on the GPU box; the manifest must exist first)
# Lenses and caches go to cache/exp19/RUN_NAME/ (not committed); the scores to results/exp19_fit_data/RUN_NAME/.
# Shard checkpoints and merged experts (about 53 GB each) live in /dev/shm and are deleted once a lens is saved.
set -euo pipefail
RUN=$1
REPO=/workspace/bridge-jspace
export PATH="$HOME/.local/bin:$PATH"; set -a; . "$REPO/.env"; set +a
RES=$REPO/results/exp19_fit_data/$RUN; CACHE=$REPO/cache/exp19/$RUN; SHM=/dev/shm/exp19/$RUN
test -f "$RES/manifest.json" || { echo "write the manifest first"; exit 1; }
HF=Qwen/Qwen3.6-27B; LAYERS=$(seq -s, 0 62); NP=25; ROWS=16  # 32 runs out of memory on Qwen (smoke test)
CONDS=${CONDS:-wiki_a math wiki_b chat mix}  # fitting order; fit_v2 resumed without wiki_b (its amendment_1.json)
NPJ=/workspace/lensfit/neuronpedia/utils/neuronpedia-utils/neuronpedia_utils/jlens
cd /workspace/lensfit/jpp_lens
export PYTHONPATH=src
PY=.venv/bin/python; CLI="$PY $REPO/scripts/exp19_fit_data/jpp_pool_cli.py"
stamp() { echo "=== $(date -u +%H:%M:%S) $*"; }
mkdir -p "$CACHE" "$SHM"

stamp grade
[ -f "$CACHE/correctness.csv" ] || $PY "$NPJ/jpp/grade.py" --hf-model-name "$HF" --layers "$LAYERS" --out "$CACHE/correctness.csv"

for c in $CONDS; do  # math right after wiki_a: the main comparison first
  D=$CACHE/$c; S=$SHM/$c; mkdir -p "$D" "$S"
  export FIT_POOL_JSON=$REPO/data/exp19_fit_pools/$c.json
  stamp "$c fit-router"
  [ -f "$D/router.pt" ] || $CLI fit-router --hf-model-name "$HF" --layers "$LAYERS" --out "$D/router.pt"
  stamp "$c fit-shard n=$NP"
  if [ ! -f "$D/shard_dir.txt" ]; then
    $CLI fit-shard --hf-model-name "$HF" --layers "$LAYERS" --router-path "$D/router.pt" --num-prompts "$NP" \
      --jacobian-rows-per-pass "$ROWS" --artifacts-base-dir "$S/artifacts" --checkpoint-name "exp19_$c" \
      | tail -1 > "$D/shard_dir.tmp"
    mv "$D/shard_dir.tmp" "$D/shard_dir.txt"  # only once the shards are done, so a rerun after a crash refits them
  fi
  stamp "$c merge-experts"
  [ -f "$D/pooled_$c.pt" ] || $CLI merge-experts --checkpoint-dirs "$(cat "$D/shard_dir.txt")" \
    --checkpoint-name "exp19_$c" --out "$S/experts.pt" --pooled-lens-out "$D/pooled_$c.pt"
  stamp "$c fit-weights"
  [ -f "$D/jpp_$c.pt" ] || $CLI fit-weights --hf-model-name "$HF" --layers "$LAYERS" --experts "$S/experts.pt" \
    --correctness-csv "$CACHE/correctness.csv" --cache-path "$CACHE/readout_cache.pt" --out "$D/jpp_$c.pt"
  if [ -f "$D/jpp_$c.pt" ] && [ -f "$D/pooled_$c.pt" ]; then rm -rf "$S"; stamp "$c scratch deleted"; fi
done
unset FIT_POOL_JSON

stamp evaluate
REV=$(grep -oP '^LENS_REVISION = "\K[0-9a-f]+' "$REPO/src/bridge_jspace/pins.py")
PUB=$($PY -c "
from huggingface_hub import hf_hub_download as d
r='$REV'
print(d('neuronpedia/jacobian-lens','qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt',revision=r),
      d('neuronpedia/jacobian-lens','qwen3.6-27b/jlens/Salesforce-wikitext/Qwen3.6-27B_jacobian_lens_n1000.pt',revision=r))")
LENSES=()
for c in $CONDS; do LENSES+=("$CACHE/$c/jpp_$c.pt" "$CACHE/$c/pooled_$c.pt"); done
[ -f "$RES/eval_ranks.csv" ] || $CLI evaluate --hf-model-name "$HF" --layers "$LAYERS" \
  --correctness-csv "$CACHE/correctness.csv" --lens "${LENSES[@]}" $PUB logit --out "$RES/eval_ranks.csv"
cat "$RES/eval_ranks_pass_at_k.csv" | grep ",10,item," || true
stamp done
