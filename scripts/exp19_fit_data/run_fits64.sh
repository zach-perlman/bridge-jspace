#!/usr/bin/env bash
# exp19_fit_data, 64-prompt fits: J++ lenses on the first 64 texts of the chat and WikiText (wiki_a) pools, with the
# routers, item grades and readout cache of fit_v2 (same pools, same seed), each lens scored as soon as it is saved.
#   bash scripts/exp19_fit_data/run_fits64.sh RUN_NAME   (on the GPU box; the manifest must exist first)
# Lenses go to cache/exp19/RUN_NAME/ (not committed); the scores to results/exp19_fit_data/RUN_NAME/eval_<lens>/.
set -euo pipefail
RUN=$1
REPO=/workspace/bridge-jspace
export PATH="$HOME/.local/bin:$PATH"; set -a; . "$REPO/.env"; set +a
RES=$REPO/results/exp19_fit_data/$RUN; CACHE=$REPO/cache/exp19/$RUN; SHM=/dev/shm/exp19/$RUN; V2=$REPO/cache/exp19/fit_v2
test -f "$RES/manifest.json" || { echo "write the manifest first"; exit 1; }
HF=Qwen/Qwen3.6-27B; LAYERS=$(seq -s, 0 62); NP=64; ROWS=16
cd /workspace/lensfit/jpp_lens
export PYTHONPATH=src
PY=.venv/bin/python; CLI="$PY $REPO/scripts/exp19_fit_data/jpp_pool_cli.py"
stamp() { echo "=== $(date -u +%H:%M:%S) $*"; }
mkdir -p "$CACHE" "$SHM"
for f in correctness.csv readout_cache.pt; do [ -f "$CACHE/$f" ] || cp "$V2/$f" "$CACHE/$f"; done

for spec in chat64:chat wiki64:wiki_a; do  # chat first: the condition asked for
  c=${spec%%:*}; pool=${spec##*:}
  D=$CACHE/$c; S=$SHM/$c; mkdir -p "$D" "$S"
  export FIT_POOL_JSON=$REPO/data/exp19_fit_pools/$pool.json
  for f in router.pt router_stamp.json; do [ -f "$D/$f" ] || cp "$V2/$pool/$f" "$D/$f"; done  # fit_v2's router
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
  unset FIT_POOL_JSON
  stamp "$c evaluate"
  E=$RES/eval_$c; mkdir -p "$E"
  [ -f "$E/eval_ranks.csv" ] || $CLI evaluate --hf-model-name "$HF" --layers "$LAYERS" \
    --correctness-csv "$CACHE/correctness.csv" --lens "$D/jpp_$c.pt" "$D/pooled_$c.pt" --out "$E/eval_ranks.csv" \
    || stamp "$c evaluate FAILED (the next fit still runs)"
  grep ",10,item," "$E/eval_ranks_pass_at_k.csv" | grep macro || true
done
stamp done
