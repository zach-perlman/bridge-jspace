#!/bin/bash
# Zach (2026-10-21, "Sure, queue it"; every model gets the same set): Qwen3-32B with its every-layer J++, GPU 1 part,
# after the Gemma knock-outs (h200_gemma_B3, with its appended additions) and the Qwen3-32B competence runs (GPU 0,
# h200_q32_A_1021.sh). Gemma's B3 set at the 27B's depths (64 layers): two-step words on full_v8: the C1 rule (c1_v2
# --middle L32-40; whole question at 12-20, 20-28, 32-40 and whole depth), the specificity control (unembed10 at the
# narrow bands; c1_specificity), C1's second kill test (keep own word), two more control seeds, the position split, each
# step alone; three-step words on full_v8b (per-word eligibility): whole question and each step alone. The dose curves
# run on GPU 0.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK=/workspace/scratch/markers/q32_competence_done
until grep -qs "^EXIT" $R-h200gemmaB3-*.log && { [ -f $MK ] || grep -qs "^EXIT" $R-h200q32A-*.log; }; do sleep 60; done
grep -q '"qwen3-32b"' src/bridge_jspace/pins.py || { echo "no qwen3-32b target (fit or gate failed): stop"; exit 1; }
C2=qwen3_32b_full_v8_competence_v1
C3=qwen3_32b_full_v8b_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] || { echo "missing Qwen3-32B full_v8 competence: stop"; exit 1; }
export BJ_TARGET=qwen3-32b
WHY="Zach (2026-10-21): Qwen3-32B, every-layer J++ (32 prompts)"
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
BANDS="12-20 20-28 32-40 0-62"
K="--n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name qwen3_32b_smoke_full_ko_1021 --why smoke --plan bands --bands 32-40 \
  --conditions paper10 paper10_rot unembed10 $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_v1 --middle L32-40 --set full_v8 | tail -2 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_v1 --middle L32-40 --set full_v8 --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands 12-20 20-28 32-40 --conditions unembed10 unembed10_rot $T2 $K \
  && $PY scripts/c1_specificity.py qwen3_32b_full2_ko_v1 qwen3_32b_full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_unembed_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== unembed knock-out FAILED"
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands 32-40 --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_keepown_v1 --middle L32-40 --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_rotseed${s}_v1 --why "$WHY: rotated control, seed offset $s" --plan bands \
    --bands 32-40 --conditions paper10_rot --seed-offset $s $T2 $K || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands 12-20 32-40 --conditions paper10 paper10_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py qwen3_32b_full2_ko_pos_${pos}_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at 32-40" --plan bands \
  --bands 32-40 --conditions paper10 paper10_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_steps_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== two-step steps FAILED"
if [ -f results/tasks_v2/$C3/summary.json ]; then
  $PY scripts/ablate_v2.py --name qwen3_32b_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
    --bands $BANDS --conditions paper10 paper10_rot $T3 $K \
    && $PY scripts/c1_v2.py qwen3_32b_full3_ko_v1 --middle L32-40 --set full_v8b > /dev/null || echo "=== three-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name qwen3_32b_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at 32-40" --plan bands \
    --bands 32-40 --conditions paper10 paper10_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py qwen3_32b_full3_ko_steps_v1 --middle L32-40 --set full_v8b > /dev/null || echo "=== three-step steps FAILED"
else
  echo "=== no full_v8b competence: three-step knock-outs skipped"
fi
echo "=== Qwen3-32B GPU 1 part done $(date -u +%FT%TZ)"
