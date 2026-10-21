#!/bin/bash
# Zach (2026-10-21, decided with Zach: "Is the dose curve important now? ... Can we wait for the three models to finish
# first?"): the dose curves Gemma and Qwen3-32B had queued, moved after every model's core runs (the 9B's included).
# Usage: h200_dose_after_1021.sh gemma|qwen3-32b. Gemma on GPU 1 after the 9B's knock-outs; Qwen3-32B on GPU 0 after the
# 9B's GPU 0 part. The 27B's and the 9B's dose curves are not queued (to decide once the core results are in).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
K="--n 1000 --kinds clean --batch 32"
D="top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot"
S="top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot"
case "$1" in
  gemma) export CUDA_VISIBLE_DEVICES=1 BJ_TARGET=gemma-4-31b-it-full; W=h200q9B; P=gemma4itf_; C2=gemma4itr_full_v8_competence_v1
         BANDS="30-38 11-19"; SINGLE="34 15"; WHY="Zach (2026-10-21): Gemma 4 31B-it, every-layer J++";;
  qwen3-32b) export CUDA_VISIBLE_DEVICES=0 BJ_TARGET=qwen3-32b; W=h200q9A; P=qwen3_32b_; C2=qwen3_32b_full_v8_competence_v1
         BANDS="32-40 12-20"; SINGLE="36 16"; WHY="Zach (2026-10-21): Qwen3-32B, every-layer J++ (32 prompts)";;
  *) echo "usage: $0 gemma|qwen3-32b"; exit 1;;
esac
until grep -qs "^EXIT" $R-$W-*.log; do sleep 60; done
grep -q "\"$BJ_TARGET\"" src/bridge_jspace/pins.py && [ -f results/tasks_v2/$C2/summary.json ] || { echo "no $BJ_TARGET target or competence: stop"; exit 1; }
echo "=== start $1 $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name ${P}full_dose_v1 --why "$WHY: knock-out dose on the 2x2 words" --plan bands --bands $BANDS \
  --tasks full_v8 --tasks-competence $C2 --tasks-words PP PM MP MM --tasks-level all $K --conditions $D || echo "=== dose FAILED"
$PY scripts/ablate_v2.py --name ${P}full_dose_single_v1 --why "$WHY: smaller doses, single layers" --plan bands --bands $SINGLE \
  --tasks full_v8 --tasks-competence $C2 --tasks-words PP PM MP MM --tasks-level all $K --conditions $S || echo "=== single-layer dose FAILED"
echo "=== $1 doses done $(date -u +%FT%TZ)"
