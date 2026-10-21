#!/bin/bash
# 2026-10-21 (Zach: the new suite, not the old one): the middle band is chosen on ctrl_v8 (the v2 generator, seed 712;
# no prompt or context shared with the test set full_v8), by scripts/choose_band.py, for every model including the 27B.
# Zach (2026-10-21; replaces h200_q32_B2_1021.sh before it started, decided with Zach: each model's middle band is
# chosen by the procedure that picked the 27B's 32-40, on its own suite depth sweep, before its tasks_v2 knock-outs):
# Qwen3-32B with its every-layer J++, GPU 1 part, after the 9B fill (h200_q9_B2_1021.sh fill) and its competence runs
# (GPU 0, h200_q32_A2_1021.sh). First the suite sweep (paper10 + rotated, BL BR RL RR, n = 100, the 27B's nine-layer
# windows) and the band choice (MID); then Gemma's knock-out set: the C1 rule (whole question at 12-20, 20-28, MID and
# whole depth), the specificity control (12-20, 20-28, MID), keep own word, two more control seeds, the position split
# (12-20, MID), each step alone (MID); three-step whole question and each step (MID). Doses run at the end
# (h200_dose_after_1021.sh).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK=/workspace/scratch/markers/q32_competence_done
until grep -qs "^EXIT" $R-h200q9F-*.log && { [ -f $MK ] || grep -qs "^EXIT" $R-h200q32A-*.log; }; do sleep 60; done  # 2026-10-21: after the 9B fill on GPU 1 (it starts after the Gemma knock-outs and hands GPU 1 back once this competence is ready)
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
K="--n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name qwen3_32b_smoke_full_ko_1021 --why smoke --plan bands --bands 32-40 \
  --conditions paper10 paper10_rot unembed10 $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
[ -f results/tasks_v2/qwen3_32b_ctrl_v8_competence_v1/summary.json ] || $PY scripts/tasks_v2.py competence --set ctrl_v8 --name qwen3_32b_ctrl_v8_competence_v1 --guess \
  --why "$WHY: competence on ctrl_v8 (the band sweep's items)" > /workspace/scratch/qwen3_32b_ctrl_comp.log 2>&1 || echo "=== ctrl_v8 competence FAILED"
SW=qwen3_32b_ctrl_sweep_v1
[ -f results/ablate_v2/$SW/summary.json ] || $PY scripts/ablate_v2.py --name $SW \
  --why "$WHY: v2 depth sweep on ctrl_v8 to choose the middle band (every model's procedure)" --plan bands \
  --bands 0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 52-60 --conditions paper10 paper10_rot \
  --tasks ctrl_v8 --tasks-competence qwen3_32b_ctrl_v8_competence_v1 --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32 \
  || echo "=== ctrl_v8 sweep FAILED"
MID=$($PY scripts/choose_band.py $SW) || MID=""
[ -n "$MID" ] || { MID=32-40; echo "=== no band chosen: the relative-depth band 32-40 instead"; }
echo "=== middle band: $MID (relative-depth band: 32-40)"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
BANDS=$(uniq_bands 12-20 20-28 $MID 0-62)
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_v1 --middle L$MID --set full_v8 | tail -2 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_v1 --middle L$MID --set full_v8 --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands $(uniq_bands 12-20 20-28 $MID) --conditions unembed10 unembed10_rot $T2 $K \
  && $PY scripts/c1_specificity.py qwen3_32b_full2_ko_v1 qwen3_32b_full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_unembed_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== unembed knock-out FAILED"
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands $MID --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_keepown_v1 --middle L$MID --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_rotseed${s}_v1 --why "$WHY: rotated control, seed offset $s" --plan bands \
    --bands $MID --conditions paper10_rot --seed-offset $s $T2 $K || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands $(uniq_bands 12-20 $MID) --conditions paper10 paper10_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py qwen3_32b_full2_ko_pos_${pos}_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name qwen3_32b_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at the middle band" --plan bands \
  --bands $MID --conditions paper10 paper10_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py qwen3_32b_full2_ko_steps_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== two-step steps FAILED"
if [ -f results/tasks_v2/$C3/summary.json ]; then
  $PY scripts/ablate_v2.py --name qwen3_32b_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
    --bands $BANDS --conditions paper10 paper10_rot $T3 $K \
    && $PY scripts/c1_v2.py qwen3_32b_full3_ko_v1 --middle L$MID --set full_v8b > /dev/null || echo "=== three-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name qwen3_32b_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at the middle band" --plan bands \
    --bands $MID --conditions paper10 paper10_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py qwen3_32b_full3_ko_steps_v1 --middle L$MID --set full_v8b > /dev/null || echo "=== three-step steps FAILED"
else
  echo "=== no full_v8b competence: three-step knock-outs skipped"
fi
echo "=== Qwen3-32B GPU 1 part done $(date -u +%FT%TZ)"
