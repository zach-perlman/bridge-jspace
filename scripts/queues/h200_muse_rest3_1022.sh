#!/bin/bash
# 2026-10-22 ~07:20 UTC (efficiency): the aligned-band steering runs only the writes the C2 rules score (lens_add,
# lens_swap, copy for the ceiling, and the early injection control); c2_graded / c2_narrow give identical verdicts
# and numbers without the transplant and difference-of-means writes (checked on wm2_full2_v2). Saves ~half the run.
# 2026-10-22 (Zach; replaces h200_muse_rest2_1022.sh before it started: Muse's kill tests dropped, since the knock-out
# barely moves Muse, and the dose curve runs in the core job instead). Was: (Zach: "Go"; replaces h200_muse_rest_1022.sh): the rest of Muse Glimmer 30B's set (our
# J++), GPU 0, reordered so that what the claims hinge on runs first: (1) C1's kill tests at the middle band (keep own
# word, two more rotated-control seeds); (2) C2 at the aligned band (band copy sweep, window 10 by 2 = the 27B's 12 by 2
# of 64 scaled to 52; scripts/choose_steer_band.py; steering there, c2_graded and c2_narrow), reported beside the
# pre-registered current-band run; (3) everything else of the old rest, unchanged (competence on full_v8b and the
# suite, position split, steps, three-step, positive control, three-step steering, plain-text loss at the chosen band).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200muse-*.log; do sleep 60; done
export BJ_TARGET=muse-glimmer-30b
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )
echo "=== C1 protocol: paper10${S:-}"
WHY="Zach (2026-10-22): Muse Glimmer 30B, the second family, its published plain J-lens (900 prompts)"
C2=muse30_full_v8_competence_v1
C3=muse30_full_v8b_competence_v1
CS=muse30_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] || { echo "no Muse full_v8 competence: stop"; exit 1; }
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
STEER="--possets question final --band 23-33 --single-step 2 --early 13 16 20"
K="--n 1000 --kinds clean --batch 32"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
MID=$($PY scripts/choose_band.py muse30_ctrl_sweep_v1 "$S") || MID=""
[ -n "$MID" ] || { MID=26-32; echo "=== no band chosen: the relative-depth band 26-32 instead"; }
echo "=== middle band: $MID (relative-depth band: 26-32)"
BANDS=$(uniq_bands 10-16 16-22 $MID 0-50)
echo "=== start $(date -u +%FT%TZ)"
echo "=== copy sweep $(date -u +%T)"
$PY scripts/copy_sweep.py --name muse30_copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $C2 --families PP PM MP MM --n 40 --step 2 --window 10 || echo "=== copy sweep FAILED"
echo "=== aligned-band C2 $(date -u +%T)"
AB=$($PY scripts/choose_steer_band.py muse30_copy_sweep_full2_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
if [ -n "$AB" ]; then
  BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full2_aligned_v1 --why "$WHY: two-step steering at the aligned band ${AB%% *} (scripts/choose_steer_band.py)" \
    --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB%% *} --single-step 2 --early 13 16 20 $W2 \
    && $PY scripts/c2_graded.py muse30_wm2_full2_aligned_v1 | tail -14 \
    && $PY scripts/c2_graded.py muse30_wm2_full2_aligned_v1 --drop-guessable > /dev/null \
    && $PY scripts/c2_narrow.py muse30_wm2_full2_aligned_v1 muse30_wm2_full2_aligned_v1_noguess || echo "=== aligned steering FAILED"
fi
echo "=== the rest $(date -u +%T)"
[ -f results/tasks_v2/$C3/summary.json ] || { $PY scripts/tasks_v2.py competence --set full_v8b --name $C3 --guess \
  --why "$WHY: competence on full_v8b (three-step words)" > /workspace/scratch/muse30_comp3.log 2>&1 \
  && $PY scripts/competence_full_report.py $C3 | tail -16 || echo "=== full_v8b competence FAILED"; }
[ -f results/suite_v1/$CS/summary.json ] || { $PY scripts/suite_v1.py manifest --set main --name $CS --limit 150 \
  --why "$WHY: suite competence (first 150 per family) for the steering positive control, as the others" \
  && $PY scripts/suite_v1.py competence --name $CS > /workspace/scratch/muse30_suitecomp.log 2>&1 || echo "=== suite competence FAILED"; }
for pos in context question; do
  $PY scripts/ablate_v2.py --name muse30_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands $(uniq_bands 10-16 $MID) --conditions paper10$S paper10${S}_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py muse30_full2_ko_pos_${pos}_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name muse30_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at the middle band" --plan bands \
  --bands $MID --conditions paper10$S paper10${S}_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py muse30_full2_ko_steps_v1 --middle L$MID --set full_v8 --suffix "$S" > /dev/null || echo "=== two-step steps FAILED"
if [ -f results/tasks_v2/$C3/summary.json ]; then
  $PY scripts/ablate_v2.py --name muse30_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
    --bands $BANDS --conditions paper10$S paper10${S}_rot $T3 $K \
    && $PY scripts/c1_v2.py muse30_full3_ko_v1 --middle L$MID --set full_v8b --suffix "$S" > /dev/null || echo "=== three-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name muse30_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at the middle band" --plan bands \
    --bands $MID --conditions paper10$S paper10${S}_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py muse30_full3_ko_steps_v1 --middle L$MID --set full_v8b --suffix "$S" > /dev/null || echo "=== three-step steps FAILED"
else
  echo "=== no full_v8b competence: three-step knock-outs skipped"
fi
[ -f results/suite_v1/$CS/summary.json ] \
  && BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 23-33 --single-step 2 --early 13 16 20 --from-competence $CS \
  && $PY scripts/c2_graded.py muse30_wm2_posctrl_v1 | tail -2 || echo "=== positive control FAILED"
[ -f results/tasks_v2/$C3/summary.json ] \
  && BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full3_v1 --why "$WHY: three-step steering" --n 40 $STEER $W3 \
  && $PY scripts/c2_graded.py muse30_wm2_full3_v1 > /dev/null || echo "=== three-step steering FAILED"
[ "$MID" != 26-32 ] && { $PY scripts/removal_textloss.py --name muse30_textloss_top_l${MID%-*}_${MID#*-}_v1 \
  --why "$WHY: plain-text loss under the knock-out at the chosen band" --layers $(seq ${MID%-*} ${MID#*-}) \
  --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss at the chosen band FAILED"; }
echo "=== Muse rest done $(date -u +%FT%TZ)"
