#!/bin/bash
# 2026-10-22 ~16:10 UTC: Muse's steering runs crashed in case preparation (scripts/tasks_v2.py prepare looked for the
# question after a newline, which Muse's chat template does not put before a user turn; fixed, identical positions on
# the 27B and Qwen3-32B). Re-run, in order: (1) the test-set C1 with Muse's published J-lens (Zach approved; the
# earlier insertion was skipped by bash's read-ahead); (2) C2 at the current band (pre-registered C2', full writes);
# (3) the removal-size check (27B, Muse) and Muse's verify packet; (4) the copy sweep, aligned band and aligned-band
# steering (scored writes only); (5) three-step steering; then the cross-model table. GPU 0; the 9B follows.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
export BJ_TARGET=muse-glimmer-30b
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )
WHY="Zach (2026-10-22): Muse Glimmer 30B, the second family, our J++"
TWO="PP PM MP MM CP CM"; THREE="PPP PPM PMP MPP MPM MMP"
C2=muse30_full_v8_competence_v1; C3=muse30_full_v8b_competence_v1
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
STEER="--possets question final --band 23-33 --single-step 2 --early 13 16 20"
K="--n 1000 --kinds clean --batch 32"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
MID=$($PY scripts/choose_band.py muse30_ctrl_sweep_v1 "$S") || MID=36-42
echo "=== start $(date -u +%FT%TZ); middle band $MID"
for d in results/write_max/muse30_smoke_wm2_full_1022 results/write_max/muse30_wm2_full2_v1 results/copy_sweep/muse30_copy_sweep_full2_v1 results/write_max/muse30_wm2_full3_v1; do
  [ -d $d ] && [ ! -f $d/summary.json ] && mkdir -p /workspace/runs/archive_cancelled/results && mv $d /workspace/runs/archive_cancelled/results/$(basename $d)_crashed && echo "archived crashed $d"
done
echo "=== J-lens C1 $(date -u +%T)"
BJ_TARGET=muse-glimmer-30b-jlens $PY scripts/ablate_v2.py --name muse30j_full2_ko_v1 \
  --why "Zach (2026-10-22): Muse's test-set C1 with its published J-lens (is the J++ null the model or our lens?)" --plan bands \
  --bands $(uniq_bands $MID 26-32) --conditions paper10$S paper10${S}_rot $T2 $K \
  && BJ_TARGET=muse-glimmer-30b-jlens $PY scripts/c1_v2.py muse30j_full2_ko_v1 --middle L$MID --set full_v8 --suffix "$S" | tail -2 || echo "=== J-lens C1 FAILED"
echo "=== C2 $(date -u +%T)"
BJ_BATCH=32 $PY scripts/write_max.py --name muse30_smoke_wm2_full_1022 --why smoke --n 2 --band 26-28 \
  --single-step 1 --early 16 --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
BJ_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full2_v1 --why "$WHY: two-step steering, full pools, joint paste ceiling" \
  --n 1000 $STEER $W2 && $PY scripts/c2_graded.py muse30_wm2_full2_v1 | tail -14 \
  && $PY scripts/c2_graded.py muse30_wm2_full2_v1 --drop-guessable > /dev/null \
  && $PY scripts/c2_narrow.py muse30_wm2_full2_v1 muse30_wm2_full2_v1_noguess || echo "=== two-step steering FAILED"
BJ_TARGET=qwen3.6-27b $PY scripts/removal_size.py --name removal_size_v1 --why "Zach (2026-10-22): does the unembedding knock-out remove less of the residual than the J-lens one? (27B)" --layers 16 24 32 36 40 || echo "=== 27B removal size FAILED"
$PY scripts/removal_size.py --name muse30_removal_size_v1 --why "Zach (2026-10-22): removal size, J-lens vs unembedding (Muse, J++)" --layers 13 20 26 29 32 || echo "=== Muse removal size FAILED"
$PY scripts/verify_c1.py muse30_full2_ko_v1 L$MID full_v8 $C2 > /dev/null || echo "=== verify packet FAILED"
echo "=== copy sweep $(date -u +%T)"
$PY scripts/copy_sweep.py --name muse30_copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $C2 --families PP PM MP MM --n 40 --step 2 --window 10 || echo "=== copy sweep FAILED"
AB=$($PY scripts/choose_steer_band.py muse30_copy_sweep_full2_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
[ -n "$AB" ] && { BJ_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full2_aligned_v1 --why "$WHY: two-step steering at the aligned band ${AB%% *} (scripts/choose_steer_band.py)" \
    --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB%% *} --single-step 2 --early 13 16 20 $W2 \
    && $PY scripts/c2_graded.py muse30_wm2_full2_aligned_v1 | tail -14 \
    && $PY scripts/c2_graded.py muse30_wm2_full2_aligned_v1 --drop-guessable > /dev/null \
    && $PY scripts/c2_narrow.py muse30_wm2_full2_aligned_v1 muse30_wm2_full2_aligned_v1_noguess || echo "=== aligned steering FAILED"; }
[ -f results/tasks_v2/$C3/summary.json ] && BJ_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full3_v1 --why "$WHY: three-step steering" --n 40 $STEER $W3 \
  && $PY scripts/c2_graded.py muse30_wm2_full3_v1 > /dev/null || echo "=== three-step steering FAILED"
$PY scripts/cross_model_summary.py > /dev/null || echo "=== cross-model summary FAILED"
echo "=== Muse C2 recovery done $(date -u +%FT%TZ)"
