#!/bin/bash
# Zach (2026-10-22): Muse Glimmer 30B replaces Mistral as the second family (Mistral cancelled before its test-set C1;
# the 27B bridge below runs first in h200_bridge_jlens_1022.sh and is skipped here when done). Its published plain J-lens first (Zach: "if
# it's not very good let's consider training our own J++"). GPU 0, after Mistral's test-set C1 (stopped there) and the
# weights' download. Every model's procedure, depths scaled from the 27B's 64 blocks to 52 (x 0.8125, rounded half up):
# the band sweep on ctrl_v8 with 7-layer windows sliding by 3 (9/64 and 4/64 of depth: 7.3 and 3.25); fallback middle
# band 26-32 (the 27B's 32-40); C1 bands 10-16 and 16-22 (12-20, 20-28) and whole depth 0-50; steering band 23-33
# (28-40), every 2nd layer, early 13, 16, 20 (16, 20, 24); plain-text loss at 26-32.
# Order: (1) the lens check and plain-text loss (the untestable gate, docs/prereg_replication_1022.md); (2) the bridge on
# the 27B with neuronpedia's published plain J-lens (1000 prompts; the fitter family of Muse's lens): the same lens check,
# the 27B J++'s for comparison, and the 27B's C1 at 32-40; so the "is the J-lens good enough" call can be made early;
# (3) competence on full_v8 and ctrl_v8, the sweep, C1, the specificity control; (4) C2: the two-step steering on full
# pools with its joint paste ceiling, scored by c2_graded and c2_narrow. The rest follows in h200_muse_rest_1022.sh.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200bridge-*.log && [ -f /workspace/scratch/markers/muse_downloaded ]; do sleep 60; done  # 2026-10-22: Mistral cancelled; the 27B bridge runs first (h200_bridge_jlens_1022.sh)
export BJ_TARGET=muse-glimmer-30b
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )  # the sink verdict (docs/prereg_sink_1021.md)
echo "=== C1 protocol: paper10${S:-}"
WHY="Zach (2026-10-22): Muse Glimmer 30B, the second family, its published plain J-lens (900 prompts)"
TWO="PP PM MP MM CP CM"
C2=muse30_full_v8_competence_v1
CC=muse30_ctrl_v8_competence_v1
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
STEER="--possets question final --band 23-33 --single-step 2 --early 13 16 20"
K="--n 1000 --kinds clean --batch 32"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/lens_agreement.py --name muse30_lens_agreement_v1 --why "$WHY: lens sanity check before any run" \
  || { echo "lens check failed: stop"; exit 1; }
$PY scripts/removal_textloss.py --name muse30_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L26-32 (the 27B's 32-40)" \
  --layers $(seq 26 32) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
echo "=== bridge $(date -u +%T)"
[ -f results/lens_agreement/q27jlens_lens_agreement_v1/summary.json ] || BJ_TARGET=qwen3.6-27b-jlens $PY scripts/lens_agreement.py --name q27jlens_lens_agreement_v1 --why "$WHY: bridge, the same check on the 27B's plain J-lens" || echo "=== 27B J-lens check FAILED"
[ -f results/lens_agreement/lens_agreement_jpp_v1/summary.json ] || BJ_TARGET=qwen3.6-27b $PY scripts/lens_agreement.py --name lens_agreement_jpp_v1 \
  --why "$WHY: the same check on the 27B's own J++" || echo "=== 27B J++ lens check FAILED"
[ -f results/ablate_v2/q27jlens_full2_ko_v1/summary.json ] || BJ_TARGET=qwen3.6-27b-jlens $PY scripts/ablate_v2.py --name q27jlens_full2_ko_v1 \
  --why "$WHY: bridge, the 27B's C1 at 32-40 with neuronpedia's plain J-lens (the lens type Muse gets)" --plan bands \
  --bands 32-40 --conditions paper10$S paper10${S}_rot --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words $TWO --tasks-level all $K \
  && BJ_TARGET=qwen3.6-27b-jlens $PY scripts/c1_v2.py q27jlens_full2_ko_v1 --middle L32-40 --set full_v8 --suffix "$S" | tail -2 || echo "=== 27B bridge FAILED"
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
