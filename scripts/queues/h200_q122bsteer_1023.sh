#!/bin/bash
# Zach (2026-10-23): Qwen3.5-122B-A10B steering (descriptive; the per-model procedure every model got), on GPU 1 once the
# gpt-oss steering jobs are done. Two-step items of full_v8 (full_v8_two, with counterfactuals; the 122B's competence was
# run on it). Copy sweep; steering at 21-30 (the 27B's 28-40 scaled to 48 layers); the aligned band. Batch 8: the weights
# take ~127 GB of the 143.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1 BJ_TARGET=qwen3.5-122b-a10b
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200gpu1b-1023-0420.log && grep -qs "^EXIT" $R-h200gptossjw-1023-0425.log \
  && [ "$(nvidia-smi -i 1 --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 135000 ]; do sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
P=qwen35_122b_
WHY="Zach (2026-10-23): Qwen3.5-122B-A10B (published J++) on the v2 pipeline, steering"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }
CF=${P}full_v8_two_competence_v1
W2="--tasks full_v8_two --tasks-competence $CF --tasks-level all --families PP PM MP MM CP CM"
run write_max/${P}smoke_wm2_1023 env BJ_BATCH=8 $PY scripts/write_max.py --name ${P}smoke_wm2_1023 --why smoke --n 2 --band 24-25 --single-step 1 --early 15 \
  --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
run copy_sweep/${P}copy_sweep_full2_v1 env BJ_BATCH=8 $PY scripts/copy_sweep.py --name ${P}copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8_two --tasks-competence $CF --families PP PM MP MM --n 40 --step 1 --window 6
run write_max/${P}wm2_full2_v1 env BJ_BATCH=8 $PY scripts/write_max.py --name ${P}wm2_full2_v1 --why "$WHY: two-step steering at 21-30 (the 27B's 28-40 scaled)" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band 21-30 --single-step 1 --early 12 15 18 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_v1 | tail -3 && $PY scripts/c2_graded.py ${P}wm2_full2_v1 --drop-guessable > /dev/null \
  && $PY scripts/c2_narrow.py ${P}wm2_full2_v1 ${P}wm2_full2_v1_noguess > /dev/null
AB=$($PY scripts/choose_steer_band.py ${P}copy_sweep_full2_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
[ -n "$AB" ] && run write_max/${P}wm2_full2_aligned_v1 env BJ_BATCH=8 $PY scripts/write_max.py --name ${P}wm2_full2_aligned_v1 --why "$WHY: steering at the aligned band ${AB%% *}" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB%% *} --single-step 1 --early 12 15 18 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_aligned_v1 | tail -3
echo "=== 122B steering done $(date -u +%FT%TZ)"
