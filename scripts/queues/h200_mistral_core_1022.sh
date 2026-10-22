#!/bin/bash
# Zach (2026-10-21): verify C1 and C2 on a second family before anything else. Mistral-Small-24B-Instruct-2501 (40
# blocks) with solarkyle's plain J-lens (its only lens; pins.TARGETS), GPU 0, right after the 27B additions (h200_q27c).
# Every model's procedure, depths scaled from the 27B's 64 blocks to 40 (rounded half up): the band sweep on ctrl_v8 with
# 6-layer windows sliding by 2 (9/64 and 4/64 of depth: 5.6 and 2.5), fallback middle band 20-25 (the 27B's 32-40); C1
# bands 8-13 and 13-18 (12-20, 20-28) and whole depth 0-38; steering band 18-25 (28-40), every 2nd layer, early 10, 13,
# 15 (16, 20, 24); plain-text loss at 20-25. First the lens sanity check and the plain-text loss (Gemma's failure mode
# shows there), then competence on full_v8 and ctrl_v8, the sweep, C1 and the specificity control; the bridges (the
# 27B's C1 at 32-40 with solarkyle's 27B lens; Gemma's plain-text loss with solarkyle's Gemma lens); then C2: the
# two-step steering on full pools with its joint paste ceiling. The rest follows in h200_mistral_rest_1022.sh.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200q27b-*.log; do sleep 60; done
export BJ_TARGET=mistral-small-24b-2501
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )  # the sink verdict (docs/prereg_sink_1021.md)
echo "=== C1 protocol: paper10${S:-}"
WHY="Zach (2026-10-21): Mistral-Small-24B-2501, the second family, solarkyle's plain J-lens"
TWO="PP PM MP MM CP CM"
C2=mistral24_full_v8_competence_v1
CC=mistral24_ctrl_v8_competence_v1
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
STEER="--possets question final --band 18-25 --single-step 2 --early 10 13 15"
K="--n 1000 --kinds clean --batch 32"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/lens_agreement.py --name mistral24_lens_agreement_v1 --why "$WHY: lens sanity check before any run" \
  || { echo "lens check failed: stop"; exit 1; }
$PY scripts/removal_textloss.py --name mistral24_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L20-25 (the 27B's 32-40)" \
  --layers $(seq 20 25) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
[ -f results/tasks_v2/$C2/summary.json ] || { $PY scripts/tasks_v2.py competence --set full_v8 --name $C2 --guess \
  --why "$WHY: competence on full_v8" > /workspace/scratch/mistral24_comp.log 2>&1 \
  && $PY scripts/competence_full_report.py $C2 | tail -16 || { echo "full_v8 competence FAILED: stop"; exit 1; }; }
[ -f results/tasks_v2/$CC/summary.json ] || $PY scripts/tasks_v2.py competence --set ctrl_v8 --name $CC --guess \
  --why "$WHY: competence on ctrl_v8 (the band sweep's items)" > /workspace/scratch/mistral24_ctrl_comp.log 2>&1 || echo "=== ctrl_v8 competence FAILED"
$PY scripts/ablate_v2.py --name mistral24_smoke_full_ko_1022 --why smoke --plan bands --bands 20-25 \
  --conditions paper10$S paper10${S}_rot unembed10$S $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
SW=mistral24_ctrl_sweep_v1
[ -f results/ablate_v2/$SW/summary.json ] || $PY scripts/ablate_v2.py --name $SW \
  --why "$WHY: v2 depth sweep on ctrl_v8 to choose the middle band (every model's procedure; 6-layer windows by 2)" --plan bands \
  --bands $(for lo in $(seq 0 2 32); do echo -n "$lo-$((lo + 5)) "; done) --conditions paper10$S paper10${S}_rot \
  --tasks ctrl_v8 --tasks-competence $CC --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32 \
  || echo "=== ctrl_v8 sweep FAILED"
MID=$($PY scripts/choose_band.py $SW "$S") || MID=""
[ -n "$MID" ] || { MID=20-25; echo "=== no band chosen: the relative-depth band 20-25 instead"; }
echo "=== middle band: $MID (relative-depth band: 20-25)"
BANDS=$(uniq_bands 8-13 13-18 $MID 0-38)
$PY scripts/ablate_v2.py --name mistral24_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10$S paper10${S}_rot $T2 $K \
  && $PY scripts/c1_v2.py mistral24_full2_ko_v1 --middle L$MID --set full_v8 --suffix "$S" | tail -2 \
  && $PY scripts/c1_v2.py mistral24_full2_ko_v1 --middle L$MID --set full_v8 --suffix "$S" --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
$PY scripts/ablate_v2.py --name mistral24_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands $(uniq_bands 8-13 13-18 $MID) --conditions unembed10$S unembed10${S}_rot $T2 $K \
  && $PY scripts/c1_specificity.py mistral24_full2_ko_v1 mistral24_full2_ko_unembed_v1 --set full_v8 --suffix "$S" | tail -6 \
  && $PY scripts/c1_v2.py mistral24_full2_ko_unembed_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== unembed knock-out FAILED"
echo "=== bridges $(date -u +%T)"
BJ_TARGET=qwen3.6-27b-solarlens $PY scripts/lens_agreement.py --name q27solar_lens_agreement_v1 --why "$WHY: bridge, lens sanity check" || echo "=== 27B bridge lens check FAILED"
BJ_TARGET=qwen3.6-27b-solarlens $PY scripts/ablate_v2.py --name q27solar_full2_ko_v1 \
  --why "$WHY: bridge, the 27B's C1 at 32-40 with solarkyle's plain J-lens (the lens type and fitter Mistral gets)" --plan bands \
  --bands 32-40 --conditions paper10$S paper10${S}_rot --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words $TWO --tasks-level all $K \
  && BJ_TARGET=qwen3.6-27b-solarlens $PY scripts/c1_v2.py q27solar_full2_ko_v1 --middle L32-40 --set full_v8 --suffix "$S" | tail -2 || echo "=== 27B bridge FAILED"
BJ_TARGET=qwen3.6-27b $PY scripts/lens_agreement.py --name lens_agreement_jpp_v1 --why "$WHY: the same check on the 27B's own J++" || echo "=== 27B J++ lens check FAILED"
BJ_TARGET=gemma-4-31b-it-full $PY scripts/lens_agreement.py --name gemma4itf_lens_agreement_v1 --why "$WHY: the same check on our Gemma fit" || echo "=== Gemma fit lens check FAILED"
BJ_TARGET=gemma-4-31b-it-solarlens $PY scripts/lens_agreement.py --name gemma4its_lens_agreement_v1 --why "$WHY: bridge, lens sanity check" || echo "=== Gemma bridge lens check FAILED"
BJ_TARGET=gemma-4-31b-it-solarlens $PY scripts/removal_textloss.py --name gemma4its_textloss_top_l30_38_v1 \
  --why "$WHY: bridge, does an independent lens also wreck Gemma's plain text? (ours: 7.66 -> 12.95 at top1)" \
  --layers $(seq 30 38) --conditions none top1 top1_rot top10 top10_rot || echo "=== Gemma bridge text loss FAILED"
echo "=== C2 $(date -u +%T)"
BJ_BATCH=32 $PY scripts/write_max.py --name mistral24_smoke_wm2_full_1022 --why smoke --n 2 --band 20-22 \
  --single-step 1 --early 13 --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
BJ_BATCH=64 $PY scripts/write_max.py --name mistral24_wm2_full2_v1 --why "$WHY: two-step steering, full pools, joint paste ceiling" \
  --n 1000 $STEER $W2 && $PY scripts/c2_graded.py mistral24_wm2_full2_v1 | tail -14 \
  && $PY scripts/c2_graded.py mistral24_wm2_full2_v1 --drop-guessable > /dev/null || echo "=== two-step steering FAILED"
echo "=== Mistral core (C1 + C2) done $(date -u +%FT%TZ)"
