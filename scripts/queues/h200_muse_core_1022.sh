#!/bin/bash
# Zach (2026-10-22): Muse Glimmer 30B, the second family, with our own J++ (fit by h200_muse_fit_1022.sh, which also ran
# the published J-lens's gate). GPU 0. Every model's procedure, depths scaled from the 27B's 64 blocks to 52 (x 0.8125,
# rounded half up): the band sweep on ctrl_v8 with 7-layer windows sliding by 3; fallback middle band 26-32 (the 27B's
# 32-40); C1 bands 10-16 and 16-22 (12-20, 20-28) and whole depth 0-50; steering band 23-33 (28-40), every 2nd layer,
# early 13, 16, 20 (16, 20, 24). Plain-text loss under the J++ knock-out at 26-32 (the untestable gate), competence on
# full_v8 and ctrl_v8, the sweep, C1, the specificity control; then C2 (two-step steering, joint paste ceiling,
# c2_graded, c2_narrow). The rest follows in h200_muse_rest_1022.sh.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200musefit-*.log; do sleep 60; done  # 2026-10-22: after our J++ fit (h200_muse_fit_1022.sh)
grep -q '"muse-glimmer-30b": {' src/bridge_jspace/pins.py || { echo "no muse-glimmer-30b J++ target (fit failed): stop"; exit 1; }
export BJ_TARGET=muse-glimmer-30b
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )  # the sink verdict (docs/prereg_sink_1021.md)
echo "=== C1 protocol: paper10${S:-}"
WHY="Zach (2026-10-22): Muse Glimmer 30B, the second family, our J++"
TWO="PP PM MP MM CP CM"
C2=muse30_full_v8_competence_v1
CC=muse30_ctrl_v8_competence_v1
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
STEER="--possets question final --band 23-33 --single-step 2 --early 13 16 20"
K="--n 1000 --kinds clean --batch 32"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/removal_textloss.py --name muse30_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L26-32 (the 27B's 32-40)" \
  --layers $(seq 26 32) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
echo "=== Muse competence $(date -u +%T)"
[ -f results/tasks_v2/$C2/summary.json ] || { $PY scripts/tasks_v2.py competence --set full_v8 --name $C2 --guess \
  --why "$WHY: competence on full_v8" > /workspace/scratch/muse30_comp.log 2>&1 \
  && $PY scripts/competence_full_report.py $C2 | tail -16 || { echo "full_v8 competence FAILED: stop"; exit 1; }; }
[ -f results/tasks_v2/$CC/summary.json ] || $PY scripts/tasks_v2.py competence --set ctrl_v8 --name $CC --guess \
  --why "$WHY: competence on ctrl_v8 (the band sweep's items)" > /workspace/scratch/muse30_ctrl_comp.log 2>&1 || echo "=== ctrl_v8 competence FAILED"
$PY scripts/ablate_v2.py --name muse30_smoke_full_ko_1022 --why smoke --plan bands --bands 26-32 \
  --conditions paper10$S paper10${S}_rot unembed10$S $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
SW=muse30_ctrl_sweep_v1
[ -f results/ablate_v2/$SW/summary.json ] || $PY scripts/ablate_v2.py --name $SW \
  --why "$WHY: v2 depth sweep on ctrl_v8 to choose the middle band (every model's procedure; 7-layer windows by 3)" --plan bands \
  --bands $(for lo in $(seq 0 3 42); do echo -n "$lo-$((lo + 6)) "; done) --conditions paper10$S paper10${S}_rot \
  --tasks ctrl_v8 --tasks-competence $CC --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32 \
  || echo "=== ctrl_v8 sweep FAILED"
MID=$($PY scripts/choose_band.py $SW "$S") || MID=""
[ -n "$MID" ] || { MID=26-32; echo "=== no band chosen: the relative-depth band 26-32 instead"; }
echo "=== middle band: $MID (relative-depth band: 26-32)"
BANDS=$(uniq_bands 10-16 16-22 $MID 0-50)
$PY scripts/ablate_v2.py --name muse30_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10$S paper10${S}_rot $T2 $K \
  && $PY scripts/c1_v2.py muse30_full2_ko_v1 --middle L$MID --set full_v8 --suffix "$S" | tail -2 \
  && $PY scripts/c1_v2.py muse30_full2_ko_v1 --middle L$MID --set full_v8 --suffix "$S" --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
$PY scripts/ablate_v2.py --name muse30_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands $(uniq_bands 10-16 16-22 $MID) --conditions unembed10$S unembed10${S}_rot $T2 $K \
  && $PY scripts/c1_specificity.py muse30_full2_ko_v1 muse30_full2_ko_unembed_v1 --set full_v8 --suffix "$S" | tail -6 \
  && $PY scripts/c1_v2.py muse30_full2_ko_unembed_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== unembed knock-out FAILED"
echo "=== C2 $(date -u +%T)"
BJ_BATCH=32 $PY scripts/write_max.py --name muse30_smoke_wm2_full_1022 --why smoke --n 2 --band 26-28 \
  --single-step 1 --early 16 --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
BJ_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full2_v1 --why "$WHY: two-step steering, full pools, joint paste ceiling" \
  --n 1000 $STEER $W2 && $PY scripts/c2_graded.py muse30_wm2_full2_v1 | tail -14 \
  && $PY scripts/c2_graded.py muse30_wm2_full2_v1 --drop-guessable > /dev/null || echo "=== two-step steering FAILED"
$PY scripts/c2_narrow.py muse30_wm2_full2_v1 muse30_wm2_full2_v1_noguess || echo "=== C2-narrow scoring FAILED"
echo "=== Muse core (C1 + C2) done $(date -u +%FT%TZ)"
# appended 2026-10-22 (Zach: specificity caveat): the share of the residual each knock-out removes, J-lens vs unembedding
BJ_TARGET=qwen3.6-27b $PY scripts/removal_size.py --name removal_size_v1 --why "Zach (2026-10-22): does the unembedding knock-out remove less of the residual than the J-lens one? (27B)" --layers 16 24 32 36 40 || echo "=== 27B removal size FAILED"
$PY scripts/removal_size.py --name muse30_removal_size_v1 --why "Zach (2026-10-22): removal size, J-lens vs unembedding (Muse, J++)" --layers 13 20 26 29 32 || echo "=== Muse removal size FAILED"
# appended 2026-10-22: the hand-check packet for this model's C1 and the cross-model table (CPU)
$PY scripts/verify_c1.py muse30_full2_ko_v1 L$MID full_v8 $C2 > /dev/null || echo "=== verify packet FAILED"
$PY scripts/cross_model_summary.py > /dev/null || echo "=== cross-model summary FAILED"
