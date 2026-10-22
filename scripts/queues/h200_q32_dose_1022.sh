#!/bin/bash
# 2026-10-21 (Zach: verify C1 and C2 on Qwen3-32B and Mistral first; replaces h200_after3_1021.sh gpu0 before it
# started): Qwen3-32B's plain-text loss at its chosen band (if it differs from 32-40) and its dose curves, now on GPU 1
# after h200_q32_rest_1021.sh. Gemma's doses are dropped (Gemma is untestable with the knock-out); the 27B's, the
# 9B's and Mistral's are not queued (decide later).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
K="--n 1000 --kinds clean --batch 32"
D="top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot"
S="top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot"
#W64="0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 52-60"
#W60="0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56"
#W32="0-4 2-6 4-8 6-10 8-12 10-14 12-16 14-18 16-20 18-22 20-24 22-26 24-28 26-30"
textloss_at() {  # textloss_at TARGET PREFIX MID RELATIVE: only when the chosen band differs from the relative one
  [ "$3" = "$4" ] && return 0
  BJ_TARGET=$1 $PY scripts/removal_textloss.py --name ${2}textloss_top_l${3%-*}_${3#*-}_v1 \
    --why "Zach (2026-10-21): plain-text loss under the knock-out at the band chosen on ctrl_v8" \
    --layers $(seq ${3%-*} ${3#*-}) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== $1 text loss FAILED"
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
export CUDA_VISIBLE_DEVICES=1
until grep -qs "^EXIT" $R-h200q32rest-*.log; do sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
have qwen3-32b qwen3_32b_full_v8_competence_v1 && {
  M=$(mid qwen3_32b_ctrl_sweep_v1 32-40); textloss_at qwen3-32b qwen3_32b_ $M 32-40
dose qwen3-32b qwen3_32b_ qwen3_32b_full_v8_competence_v1 "$M 12-20" "$(center $M) 16" "Zach (2026-10-21): Qwen3-32B, every-layer J++ (32 prompts)"; }
echo "=== Qwen3-32B doses done $(date -u +%FT%TZ)"
