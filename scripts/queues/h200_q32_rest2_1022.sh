#!/bin/bash
# 2026-10-22 ~07:20 UTC (efficiency): the aligned-band steering runs only the writes the C2 rules score (lens_add,
# lens_swap, copy for the ceiling, and the early injection control); c2_graded / c2_narrow give identical verdicts
# and numbers without the transplant and difference-of-means writes (checked on wm2_full2_v2). Saves ~half the run.
# 2026-10-22 (Zach: "Go"; replaces h200_q32_rest_1021.sh before it started): the rest of Qwen3-32B's set, reordered so
# that what the claims hinge on runs first. (1) C1's kill tests at the middle band: keep own word, two more rotated-
# control seeds. (2) C2 at the aligned band: the band copy sweep, then scripts/choose_steer_band.py (the earliest band
# where pasting C's state flips >= 50% of P->P, P->M, M->P and M->M at one position set; the Day 3 plan's pre-stated
# rule), then the two-step steering there, scored by c2_graded and c2_narrow (reported beside the pre-registered
# current-band run). (3) The 27B's steering at its aligned band (48-60, final; copy_sweep_full2_v2), same scoring.
# (4) Everything else of the old rest, unchanged: position split, steps, three-step, plain-text loss, positive control,
# three-step steering, lens check.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK=/workspace/scratch/markers/q32_competence_done
until grep -qs "^EXIT" $R-h200q32core-*.log; do sleep 60; done  # after the core job (C1 + C2)
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
CS=qwen3_32b_competence_v1
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
STEER="--possets question final --band 28-40 --single-step 2 --early 16 20 24"
SW=qwen3_32b_ctrl_sweep_v1
MID=$($PY scripts/choose_band.py $SW "$S") || MID=""
[ -n "$MID" ] || { MID=32-40; echo "=== no band chosen: the relative-depth band 32-40 instead"; }
echo "=== middle band: $MID (relative-depth band: 32-40)"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
BANDS=$(uniq_bands 12-20 20-28 $MID 0-62)
echo "=== kill tests $(date -u +%T)"
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands $MID --conditions paper10$S paper10${S}_rot paper10_keepown$S paper10_keepown${S}_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_keepown_v1 --middle L$MID --set full_v8 --suffix "$S" | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_rotseed${s}_v1 --why "$WHY: rotated control, seed offset $s" --plan bands \
    --bands $MID --conditions paper10${S}_rot --seed-offset $s $T2 $K || echo "=== control seed $s FAILED"
done
echo "=== copy sweep $(date -u +%T)"
$PY scripts/copy_sweep.py --name qwen3_32b_copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $C2 --families PP PM MP MM --n 40 || echo "=== copy sweep FAILED"
echo "=== aligned-band C2 $(date -u +%T)"
AB=$($PY scripts/choose_steer_band.py qwen3_32b_copy_sweep_full2_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
if [ -n "$AB" ]; then
  BJ_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_full2_aligned_v1 --why "$WHY: two-step steering at the aligned band ${AB%% *} (scripts/choose_steer_band.py)" \
    --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB%% *} --single-step 2 --early 16 20 24 $W2 \
    && $PY scripts/c2_graded.py qwen3_32b_wm2_full2_aligned_v1 | tail -14 \
    && $PY scripts/c2_graded.py qwen3_32b_wm2_full2_aligned_v1 --drop-guessable > /dev/null \
    && $PY scripts/c2_narrow.py qwen3_32b_wm2_full2_aligned_v1 qwen3_32b_wm2_full2_aligned_v1_noguess || echo "=== aligned steering FAILED"
fi
echo "=== 27B aligned-band C2 $(date -u +%T)"
AB27=$(BJ_TARGET=qwen3.6-27b $PY scripts/choose_steer_band.py copy_sweep_full2_v2) || AB27=""
echo "=== 27B aligned band: ${AB27:-none}"
[ -n "$AB27" ] && { BJ_TARGET=qwen3.6-27b BJ_BATCH=64 $PY scripts/write_max.py --name wm2_full2_aligned_v1 \
    --why "Zach (2026-10-22): the 27B's two-step steering at the aligned band ${AB27%% *} (scripts/choose_steer_band.py on copy_sweep_full2_v2)" \
    --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB27%% *} --single-step 2 --early 16 20 24 \
    --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-level all --families PP PM MP MM CP CM \
    && BJ_TARGET=qwen3.6-27b $PY scripts/c2_graded.py wm2_full2_aligned_v1 | tail -14 \
    && BJ_TARGET=qwen3.6-27b $PY scripts/c2_graded.py wm2_full2_aligned_v1 --drop-guessable > /dev/null \
    && BJ_TARGET=qwen3.6-27b $PY scripts/c2_narrow.py wm2_full2_aligned_v1 wm2_full2_aligned_v1_noguess || echo "=== 27B aligned steering FAILED"; }
echo "=== the rest $(date -u +%T)"
for pos in context question; do
  $PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands $(uniq_bands 12-20 $MID) --conditions paper10$S paper10${S}_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py qwen3_32b_full2_ko_pos_${pos}_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at the middle band" --plan bands \
  --bands $MID --conditions paper10$S paper10${S}_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_steps_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== two-step steps FAILED"
if [ -f results/tasks_v2/$C3/summary.json ]; then
  $PY scripts/ablate_v2.py --name qwen3_32b_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
    --bands $BANDS --conditions paper10$S paper10${S}_rot $T3 $K \
    && $PY scripts/c1_v2.py qwen3_32b_full3_ko_v1 --middle L$MID --set full_v8b --suffix "$S" > /dev/null || echo "=== three-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name qwen3_32b_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at the middle band" --plan bands \
    --bands $MID --conditions paper10$S paper10${S}_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py qwen3_32b_full3_ko_steps_v1 --middle L$MID --set full_v8b --suffix "$S" > /dev/null || echo "=== three-step steps FAILED"
else
  echo "=== no full_v8b competence: three-step knock-outs skipped"
fi
$PY scripts/removal_textloss.py --name qwen3_32b_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L32-40" \
  --layers $(seq 32 40) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
[ -f results/suite_v1/$CS/summary.json ] \
  && BJ_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 28-40 --single-step 2 --early 16 20 24 --from-competence $CS \
  && $PY scripts/c2_graded.py qwen3_32b_wm2_posctrl_v1 | tail -2 || echo "=== positive control FAILED"
[ -f results/tasks_v2/$C3/summary.json ] \
  && BJ_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_full3_v1 --why "$WHY: three-step steering" --n 40 $STEER $W3 \
  && $PY scripts/c2_graded.py qwen3_32b_wm2_full3_v1 > /dev/null || echo "=== three-step steering FAILED"
LC=/workspace/bridge-jspace/results/lens_check/qwen3-32b
mkdir -p $LC
( cd /workspace/ext/jpp_lens && uv run --no-sync python scripts/jpp_cli.py evaluate --hf-model-name Qwen/Qwen3-32B \
    --layers $(seq -s, 0 62) --lens logit --items held-out:0 \
    --correctness-csv /workspace/bridge-jspace/results/lens_fit/qwen3_32b/model_correctness.csv --out $LC/eval_ranks_logit.csv \
  && uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/lens_check.py | tail -8 ) > /workspace/scratch/q32_lens_check.log 2>&1 \
  || echo "=== Qwen3-32B lens check FAILED"
echo "=== Qwen3-32B rest done $(date -u +%FT%TZ)"
