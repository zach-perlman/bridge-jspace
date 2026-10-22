#!/bin/bash
# Zach (2026-10-21): the rest of Mistral-Small-24B-2501's set, GPU 0, after h200_mistral_core_1022.sh (C1 + C2): the
# other models' knock-out set at its chosen band (keep own word, two more control seeds, the position split, each step
# alone; three-step whole and each step), the competence runs they need (full_v8b; suite_v1 main, first 150 per family,
# for the steering positive control), the positive control (reported, binding for no model), copy_sweep (band paste,
# every layer, window 8 = the 27B's 12 of 64 scaled to 40), three-step steering, and the plain-text loss at the chosen
# band if it differs from 20-25. No dose curves (as the 27B and the 9B: decide later).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200mistral-*.log; do sleep 60; done
export BJ_TARGET=mistral-small-24b-2501
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )
echo "=== C1 protocol: paper10${S:-}"
WHY="Zach (2026-10-21): Mistral-Small-24B-2501, the second family, solarkyle's plain J-lens"
C2=mistral24_full_v8_competence_v1
C3=mistral24_full_v8b_competence_v1
CS=mistral24_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] || { echo "no Mistral full_v8 competence: stop"; exit 1; }
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
STEER="--possets question final --band 18-25 --single-step 2 --early 10 13 15"
K="--n 1000 --kinds clean --batch 32"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
MID=$($PY scripts/choose_band.py mistral24_ctrl_sweep_v1 "$S") || MID=""
[ -n "$MID" ] || { MID=20-25; echo "=== no band chosen: the relative-depth band 20-25 instead"; }
echo "=== middle band: $MID (relative-depth band: 20-25)"
BANDS=$(uniq_bands 8-13 13-18 $MID 0-38)
echo "=== start $(date -u +%FT%TZ)"
[ -f results/tasks_v2/$C3/summary.json ] || { $PY scripts/tasks_v2.py competence --set full_v8b --name $C3 --guess \
  --why "$WHY: competence on full_v8b (three-step words)" > /workspace/scratch/mistral24_comp3.log 2>&1 \
  && $PY scripts/competence_full_report.py $C3 | tail -16 || echo "=== full_v8b competence FAILED"; }
[ -f results/suite_v1/$CS/summary.json ] || { $PY scripts/suite_v1.py manifest --set main --name $CS --limit 150 \
  --why "$WHY: suite competence (first 150 per family) for the steering positive control, as the others" \
  && $PY scripts/suite_v1.py competence --name $CS > /workspace/scratch/mistral24_suitecomp.log 2>&1 || echo "=== suite competence FAILED"; }
$PY scripts/ablate_v2.py --name mistral24_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands $MID --conditions paper10$S paper10${S}_rot paper10_keepown$S paper10_keepown${S}_rot $T2 $K \
  && $PY scripts/c1_v2.py mistral24_full2_ko_keepown_v1 --middle L$MID --set full_v8 --suffix "$S" | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name mistral24_full2_ko_rotseed${s}_v1 --why "$WHY: rotated control, seed offset $s" --plan bands \
    --bands $MID --conditions paper10${S}_rot --seed-offset $s $T2 $K || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name mistral24_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands $(uniq_bands 8-13 $MID) --conditions paper10$S paper10${S}_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py mistral24_full2_ko_pos_${pos}_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name mistral24_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at the middle band" --plan bands \
  --bands $MID --conditions paper10$S paper10${S}_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py mistral24_full2_ko_steps_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== two-step steps FAILED"
if [ -f results/tasks_v2/$C3/summary.json ]; then
  $PY scripts/ablate_v2.py --name mistral24_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
    --bands $BANDS --conditions paper10$S paper10${S}_rot $T3 $K \
    && $PY scripts/c1_v2.py mistral24_full3_ko_v1 --middle L$MID --set full_v8b --suffix "$S" > /dev/null || echo "=== three-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name mistral24_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at the middle band" --plan bands \
    --bands $MID --conditions paper10$S paper10${S}_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py mistral24_full3_ko_steps_v1 --middle L$MID --set full_v8b --suffix "$S" > /dev/null || echo "=== three-step steps FAILED"
else
  echo "=== no full_v8b competence: three-step knock-outs skipped"
fi
[ -f results/suite_v1/$CS/summary.json ] \
  && BJ_BATCH=64 $PY scripts/write_max.py --name mistral24_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 18-25 --single-step 2 --early 10 13 15 --from-competence $CS \
  && $PY scripts/c2_graded.py mistral24_wm2_posctrl_v1 | tail -2 || echo "=== positive control FAILED"
$PY scripts/copy_sweep.py --name mistral24_copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $C2 --families PP PM MP MM --n 40 --step 1 --window 8 || echo "=== copy sweep FAILED"
[ -f results/tasks_v2/$C3/summary.json ] \
  && BJ_BATCH=64 $PY scripts/write_max.py --name mistral24_wm2_full3_v1 --why "$WHY: three-step steering" --n 40 $STEER $W3 \
  && $PY scripts/c2_graded.py mistral24_wm2_full3_v1 > /dev/null || echo "=== three-step steering FAILED"
[ "$MID" != 20-25 ] && { $PY scripts/removal_textloss.py --name mistral24_textloss_top_l${MID%-*}_${MID#*-}_v1 \
  --why "$WHY: plain-text loss under the knock-out at the chosen band" --layers $(seq ${MID%-*} ${MID#*-}) \
  --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss at the chosen band FAILED"; }
echo "=== Mistral rest done $(date -u +%FT%TZ)"
