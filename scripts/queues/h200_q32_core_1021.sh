#!/bin/bash
# 2026-10-21 (Zach: verify C1 and C2 on Qwen3-32B and Mistral before anything else; the 9B moves to the end).
# Replaces h200_q32_B6_1021.sh and h200_q32_A3_1021.sh before they started, split in two jobs on GPU 1:
# h200_q32_core_1021.sh (this one, right after the fit job): the ctrl_v8 band sweep and band choice, two-step C1, the
# specificity control, then C2: the two-step steering on full pools with its joint paste ceiling (c2_graded).
# h200_q32_rest_1021.sh then runs the rest of both scripts unchanged (keep-own, control seeds, position split, steps,
# three-step; plain-text loss, positive control, copy sweep, three-step steering, lens check).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK=/workspace/scratch/markers/q32_competence_done
until grep -qs "^EXIT" $R-h200q32fit-*.log; do sleep 60; done  # the rebalance: right after its fit and competence runs on GPU 1
grep -q '"qwen3-32b"' src/bridge_jspace/pins.py || { echo "no qwen3-32b target (fit or gate failed): stop"; exit 1; }
C2=qwen3_32b_full_v8_competence_v1
C3=qwen3_32b_full_v8b_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] || { echo "missing Qwen3-32B full_v8 competence: stop"; exit 1; }
export BJ_TARGET=qwen3-32b
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )  # 2026-10-21: the attention-sink verdict (docs/prereg_sink_1021.md, h200_gemma_B3g_1021.sh)
echo "=== C1 protocol: paper10${S:-}"

WHY="Zach (2026-10-21): Qwen3-32B, every-layer J++ (32 prompts)"
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
K="--n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name qwen3_32b_smoke_full_ko_1021 --why smoke --plan bands --bands 32-40 \
  --conditions paper10$S paper10${S}_rot unembed10$S $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
[ -f results/tasks_v2/qwen3_32b_ctrl_v8_competence_v1/summary.json ] || $PY scripts/tasks_v2.py competence --set ctrl_v8 --name qwen3_32b_ctrl_v8_competence_v1 --guess \
  --why "$WHY: competence on ctrl_v8 (the band sweep's items)" > /workspace/scratch/qwen3_32b_ctrl_comp.log 2>&1 || echo "=== ctrl_v8 competence FAILED"
SW=qwen3_32b_ctrl_sweep_v1
[ -f results/ablate_v2/$SW/summary.json ] || $PY scripts/ablate_v2.py --name $SW \
  --why "$WHY: v2 depth sweep on ctrl_v8 to choose the middle band (every model's procedure)" --plan bands \
  --bands 0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 52-60 --conditions paper10$S paper10${S}_rot \
  --tasks ctrl_v8 --tasks-competence qwen3_32b_ctrl_v8_competence_v1 --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32 \
  || echo "=== ctrl_v8 sweep FAILED"
MID=$($PY scripts/choose_band.py $SW "$S") || MID=""
[ -n "$MID" ] || { MID=32-40; echo "=== no band chosen: the relative-depth band 32-40 instead"; }
echo "=== middle band: $MID (relative-depth band: 32-40)"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
BANDS=$(uniq_bands 12-20 20-28 $MID 0-62)
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10$S paper10${S}_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_v1 --middle L$MID --set full_v8 --suffix "$S" | tail -2 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_v1 --middle L$MID --set full_v8 --suffix "$S" --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
[ -n "$S" ] && { $PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_paper10mid_v1 --why "$WHY: C1 at the middle band under paper10 too (both protocols reported)" \
  --plan bands --bands $MID --conditions paper10 paper10_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_paper10mid_v1 --middle L$MID --set full_v8 | tail -2 || echo "=== paper10 at the middle band FAILED"; }
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands $(uniq_bands 12-20 20-28 $MID) --conditions unembed10$S unembed10${S}_rot $T2 $K \
  && $PY scripts/c1_specificity.py qwen3_32b_full2_ko_v1 qwen3_32b_full2_ko_unembed_v1 --set full_v8 --suffix "$S" | tail -6 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_unembed_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== unembed knock-out FAILED"
CS=qwen3_32b_competence_v1
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
STEER="--possets question final --band 28-40 --single-step 2 --early 16 20 24"
BJ_SUITE_BATCH=32 $PY scripts/write_max.py --name qwen3_32b_smoke_wm2_full_1021 --why smoke --n 2 --band 32-34 \
  --single-step 1 --early 24 --possets question final $W2 || { echo "smoke failed: stop"; exit 1; }
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_full2_v1 --why "$WHY: two-step steering, full pools, joint paste ceiling" \
  --n 1000 $STEER $W2 && $PY scripts/c2_graded.py qwen3_32b_wm2_full2_v1 | tail -14 \
  && $PY scripts/c2_graded.py qwen3_32b_wm2_full2_v1 --drop-guessable > /dev/null || echo "=== two-step steering FAILED"
echo "=== Qwen3-32B core (C1 + C2) done $(date -u +%FT%TZ)"
$PY scripts/c2_narrow.py qwen3_32b_wm2_full2_v1 qwen3_32b_wm2_full2_v1_noguess || echo "=== C2-narrow scoring FAILED"  # appended 2026-10-22 (docs/prereg_replication_1022.md)
# appended 2026-10-22 (Zach: specificity caveat): the share of the residual each knock-out removes, J-lens vs unembedding
$PY scripts/removal_size.py --name qwen3_32b_removal_size_v1 --why "Zach (2026-10-22): removal size, J-lens vs unembedding (Qwen3-32B)" --layers 16 24 32 36 40 || echo "=== Qwen3-32B removal size FAILED"
# appended 2026-10-22: the hand-check packet for this model's C1 and the cross-model table (CPU)
$PY scripts/verify_c1.py qwen3_32b_full2_ko_v1 L$MID full_v8 $C2 > /dev/null || echo "=== verify packet FAILED"
$PY scripts/cross_model_summary.py > /dev/null || echo "=== cross-model summary FAILED"
