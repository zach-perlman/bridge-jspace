#!/usr/bin/env bash
# Does merging two J++ shards equal one run over the same prompts? (Dan, 22-23 Oct night, before the Qwen3-32B fit.)
# Qwen3.5-0.8B, layers 6,12,18: one router (8 prompts, seed 0); 2 shards x 2 prompts (one per GPU) merged, against
# 1 shard x 4 prompts; the merged experts / pooled lenses must agree within fp tolerance (merge_compare.py).
# usage (on the box): bash ~/work/bridge-jspace/scripts/lens_fit/merge_check.sh > ~/work/merge_check.log 2>&1
set -euo pipefail
W=$HOME/work
export UV_CACHE_DIR=$W/uv-cache HF_HOME=$W/hf PATH=$HOME/.local/bin:$PATH
cd "$W/jpp_lens"
C="uv run --no-sync python scripts/jpp_cli.py"
M="--hf-model-name Qwen/Qwen3.5-0.8B"
L=6,12,18
O=$W/merge_check
rm -rf "$O" && mkdir -p "$O"
COMMON=(--layers "$L" --router-path "$O/router.pt" --num-prompts 4 --target-offset -1 --lrp-mode rlens
        --jacobian-rows-per-pass 16 --max-seq-len 128 --skip-first-n-positions 16 --checkpoint-every-n-prompts 2)
$C fit-router $M --layers "$L" --num-prompts 8 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 --out "$O/router.pt"
CUDA_VISIBLE_DEVICES=0 $C fit-shard $M "${COMMON[@]}" --shard-idx 0 --num-shards 2 --artifacts-base-dir "$O/two" --checkpoint-name s &
CUDA_VISIBLE_DEVICES=1 $C fit-shard $M "${COMMON[@]}" --shard-idx 1 --num-shards 2 --artifacts-base-dir "$O/two" --checkpoint-name s &
wait
CUDA_VISIBLE_DEVICES=0 $C fit-shard $M "${COMMON[@]}" --shard-idx 0 --num-shards 1 --artifacts-base-dir "$O/one" --checkpoint-name s
$C merge-experts --checkpoint-dirs $(ls -d "$O"/two/*/s/shard0of2 | tail -1) $(ls -d "$O"/two/*/s/shard1of2 | tail -1) \
  --out "$O/experts_two.pt" --pooled-lens-out "$O/pooled_two.pt"
$C merge-experts --checkpoint-dirs $(ls -d "$O"/one/*/s/shard0of1 | tail -1) --out "$O/experts_one.pt" --pooled-lens-out "$O/pooled_one.pt"
uv run --no-sync python "$W/bridge-jspace/scripts/lens_fit/merge_compare.py" "$O/experts_two.pt" "$O/experts_one.pt" \
  "$O/pooled_two.pt" "$O/pooled_one.pt"
