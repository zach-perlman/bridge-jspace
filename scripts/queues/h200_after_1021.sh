#!/bin/bash
# Zach (2026-10-21; replaces h200_dose_after_1021.sh before it started, decided with Zach): after every model's core runs,
# each model's depth profile on the v2 rule words (the plan of the 27B's, scaled to depth: windows 9/64 of the depth
# wide sliding by 4/64; PP MP PM MM, first 60 eligible per word; paper10 + rotated), then the dose curves Gemma and
# Qwen3-32B had queued, at each model's chosen middle band (and its center layer) and its early band. Usage: h200_after_1021.sh gpu0|gpu1. GPU 0 after the 9B's GPU 0 part: Qwen3-32B profile, its
# doses. GPU 1 after the 9B's knock-outs: Gemma and 9B profiles, Gemma's doses. (The 27B's profile runs tonight in
# h200_q27b_1021.sh; the 27B's and 9B's doses are not queued.)
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
K="--n 1000 --kinds clean --batch 32"
D="top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot"
S="top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot"
W64="0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 52-60"
W60="0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56"
W32="0-4 2-6 4-8 6-10 8-12 10-14 12-16 14-18 16-20 18-22 20-24 22-26 24-28 26-30"
profile() {  # profile TARGET PREFIX COMPETENCE WINDOWS
  BJ_TARGET=$1 $PY scripts/ablate_v2.py --name ${2}full2_profile_v1 --why "Zach (2026-10-21): depth profile on the v2 rule words, the same plan for every model" \
    --plan bands --bands $4 --conditions paper10 paper10_rot --tasks full_v8 --tasks-competence $3 --tasks-words PP MP PM MM \
    --tasks-level all --n 60 --kinds clean --batch 32 || echo "=== $1 depth profile FAILED"
}
dose() {  # dose TARGET PREFIX COMPETENCE BANDS SINGLE WHY
  BJ_TARGET=$1 $PY scripts/ablate_v2.py --name ${2}full_dose_v1 --why "$6: knock-out dose on the 2x2 words" --plan bands --bands $4 \
    --tasks full_v8 --tasks-competence $3 --tasks-words PP PM MP MM --tasks-level all $K --conditions $D || echo "=== $1 dose FAILED"
  BJ_TARGET=$1 $PY scripts/ablate_v2.py --name ${2}full_dose_single_v1 --why "$6: smaller doses, single layers" --plan bands --bands $5 \
    --tasks full_v8 --tasks-competence $3 --tasks-words PP PM MP MM --tasks-level all $K --conditions $S || echo "=== $1 single-layer dose FAILED"
}
mid() {  # mid SWEEP FALLBACK: the model's chosen middle band (scripts/choose_band.py), else the relative-depth band
  local m; m=$($PY scripts/choose_band.py $1 2>/dev/null) || m=""; echo "${m:-$2}"
}
center() { local lo=${1%-*} hi=${1#*-}; echo $(( (lo + hi) / 2 )); }
have() { grep -q "\"$1\"" src/bridge_jspace/pins.py && [ -f results/tasks_v2/$2/summary.json ]; }
case "$1" in
  gpu0) export CUDA_VISIBLE_DEVICES=0; until grep -qs "^EXIT" $R-h200q9A-*.log; do sleep 60; done
        echo "=== start gpu0 $(date -u +%FT%TZ)"
        have qwen3-32b qwen3_32b_full_v8_competence_v1 && {
          profile qwen3-32b qwen3_32b_ qwen3_32b_full_v8_competence_v1 "$W64"
          M=$(mid qwen3_32b_suite_sweep_v1 32-40); dose qwen3-32b qwen3_32b_ qwen3_32b_full_v8_competence_v1 "$M 12-20" "$(center $M) 16" "Zach (2026-10-21): Qwen3-32B, every-layer J++ (32 prompts)"; } ;;
  gpu1) export CUDA_VISIBLE_DEVICES=1; until grep -qs "^EXIT" $R-h200q9B-*.log; do sleep 60; done
        echo "=== start gpu1 $(date -u +%FT%TZ)"
        have gemma-4-31b-it-full gemma4itr_full_v8_competence_v1 && profile gemma-4-31b-it-full gemma4itf_ gemma4itr_full_v8_competence_v1 "$W60"
        have qwen3.5-9b qwen35_9b_full_v8_competence_v1 && profile qwen3.5-9b qwen35_9b_ qwen35_9b_full_v8_competence_v1 "$W32"
        have gemma-4-31b-it-full gemma4itr_full_v8_competence_v1 && { M=$(mid gemma4itf_suite_sweep_v1 30-38); dose gemma-4-31b-it-full gemma4itf_ gemma4itr_full_v8_competence_v1 "$M 11-19" "$(center $M) 15" "Zach (2026-10-21): Gemma 4 31B-it, every-layer J++"; } ;;
  *) echo "usage: $0 gpu0|gpu1"; exit 1;;
esac
echo "=== $1 done $(date -u +%FT%TZ)"
