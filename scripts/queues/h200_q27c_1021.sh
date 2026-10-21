#!/bin/bash
# 2026-10-21 (Zach: the new suite, not the old one): the middle band is chosen on ctrl_v8 (the v2 generator, seed 712;
# no prompt or context shared with the test set full_v8), by scripts/choose_band.py, for every model including the 27B.
# Zach (2026-10-21; replaces the waiting h200_q27b_1021.sh, same runs): GPU 0 after the 27B steering rerun. First the
# 27B's ctrl_v8 depth sweep and band choice (MID; 32-40 came from the old suite); if MID is not 32-40, the 27B's C1,
# step-by-step and three-step runs again at MID. Then, at MID: C1's second kill test (keep own word), two more control
# seeds, the position split (12-20, MID); the additions (paste ceiling for wm2_full2_v2, the specificity control at
# 12-20, 20-28, MID, the band copy sweep); the gap fills (plain-text loss at MID's layers, three-step ceiling, lens check).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=0 UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200q27a-*.log; do sleep 60; done  # 2026-10-21: moved to GPU 0 after its steering rerun (balances the GPUs)
WHY="Zach (2026-10-21): 27B, after the fixes"
T="--tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words PP PM MP MM CP CM --tasks-level all --n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
SW=ctrl_sweep_v1
[ -f results/ablate_v2/$SW/summary.json ] || $PY scripts/ablate_v2.py --name $SW \
  --why "$WHY: v2 depth sweep on ctrl_v8 to choose the middle band (every model's procedure)" --plan bands \
  --bands 0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 52-60 --conditions paper10 paper10_rot \
  --tasks ctrl_v8 --tasks-competence ctrl_v8_competence_v1 --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32 \
  || echo "=== ctrl_v8 sweep FAILED"
MID=$($PY scripts/choose_band.py $SW) || MID=""
[ -n "$MID" ] || { MID=32-40; echo "=== no band chosen: the relative-depth band 32-40 instead"; }
echo "=== middle band: $MID (relative-depth band: 32-40)"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
if [ "$MID" != 32-40 ]; then  # pre-stated (Zach, 2026-10-21): the 27B's middle-band runs again at the chosen band
  echo "=== the 27B's band moves from 32-40 to $MID: its middle-band runs again"
  $PY scripts/ablate_v2.py --name full2_ko_mid_v1 --why "$WHY: C1 at the band chosen on ctrl_v8 ($MID)" --plan bands --bands $MID \
    --conditions paper10 paper10_rot $T && $PY scripts/c1_v2.py full2_ko_mid_v1 --middle L$MID --set full_v8 | tail -2 || echo "=== C1 at $MID FAILED"
  $PY scripts/ablate_v2.py --name full2_ko_steps_mid_v1 --why "$WHY: two-step, each step alone at $MID" --plan bands --bands $MID \
    --conditions paper10 paper10_rot --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words PP PM MP MM CP CM \
    --tasks-level all --n 1000 --kinds step1 step2 --batch 32 || echo "=== two-step steps at $MID FAILED"
  $PY scripts/ablate_v2.py --name full3_ko_mid_v1 --why "$WHY: three-step, whole question and each step at $MID" --plan bands --bands $MID \
    --conditions paper10 paper10_rot --tasks full_v8b --tasks-competence full_v8b_competence_v1 --tasks-words PPP PPM PMP MPP MPM MMP \
    --tasks-level all --tasks-strata core secondary --tasks-per-word --n 1000 --kinds clean step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py full3_ko_mid_v1 --middle L$MID --set full_v8b > /dev/null || echo "=== three-step at $MID FAILED"
fi
$PY scripts/ablate_v2.py --name full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep the subject's own word)" \
  --plan bands --bands $MID --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T \
  && $PY scripts/c1_v2.py full2_ko_keepown_v1 --middle L$MID --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name full2_ko_rotseed${s}_v1 --why "$WHY: another draw of the rotated control (seed offset $s)" \
    --plan bands --bands $MID --conditions paper10_rot --seed-offset $s $T || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" \
    --plan bands --bands $(uniq_bands 12-20 $MID) --conditions paper10 paper10_rot --positions $pos $T \
    && $PY scripts/c1_v2.py full2_ko_pos_${pos}_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
echo "=== GPU 1 Qwen reruns done $(date -u +%FT%TZ)"
# --- appended 2026-10-21 ~19:40 UTC while this queue waited (Zach: "Queue it such that all these additions will apply to
# the current 27b model and all future models"; pipeline review, code 1330338 + 7363cf7). The 27B additions, GPU 0,
# before the Gemma steering: (1) the paste ceiling for wm2_full2_v2 (its joint copy stacked): copy only, same cases,
# c2_graded --ceiling-from; (2) the specificity control: unembed10 + rotated at 12-20, 20-28, 32-40 (whole depth left
# out: ~90 min), compared with full2_ko_v1's paper10 on the same items; (3) the copy sweep again with the band paste.
echo "=== 27B additions $(date -u +%FT%TZ)"
W2B="--possets question final --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-level all"
BJ_BATCH=64 $PY scripts/write_max.py --name smoke_wm2_copyonly_1021 --why smoke --n 2 --writes copy $W2B --families PP MM \
  && BJ_BATCH=64 $PY scripts/write_max.py --name wm2_full2_v2_ceiling --why "$WHY: the paste ceiling for wm2_full2_v2 (its joint copy stacked)" \
  --n 1000 --writes copy $W2B --families PP PM MP MM CP CM \
  && $PY scripts/c2_graded.py wm2_full2_v2 --ceiling-from wm2_full2_v2_ceiling | tail -8 \
  && $PY scripts/c2_graded.py wm2_full2_v2 --fresh-vs wm2_full2_v1 --ceiling-from wm2_full2_v2_ceiling | tail -4 \
  && $PY scripts/c2_graded.py wm2_full2_v2 --drop-guessable --ceiling-from wm2_full2_v2_ceiling > /dev/null || echo "=== paste ceiling FAILED"
$PY scripts/ablate_v2.py --name smoke_unembed_ko_1021 --why smoke --plan bands --bands 32-40 --conditions unembed10 unembed10_rot \
  --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words PP MM --tasks-level all --n 2 --kinds clean --batch 16 \
  && $PY scripts/ablate_v2.py --name full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands $(uniq_bands 12-20 20-28 $MID) --conditions unembed10 unembed10_rot $T \
  && $PY scripts/c1_specificity.py full2_ko_v1 full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py full2_ko_unembed_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== unembed knock-out FAILED"
$PY scripts/copy_sweep.py --name smoke_copy_sweep_band_1021 --why smoke --tasks full_v8 --tasks-competence full_v8_competence_v1 \
  --families PP MM --n 1 \
  && $PY scripts/copy_sweep.py --name copy_sweep_full2_v2 --why "$WHY: the copy sweep with the band paste (v1's from mode stacked)" \
  --tasks full_v8 --tasks-competence full_v8_competence_v1 --families PP PM MP MM --n 40 || echo "=== copy sweep v2 FAILED"
echo "=== 27B additions done $(date -u +%FT%TZ)"
# --- appended 2026-10-21 ~19:50 UTC while this queue waited (Zach: fill the 27B's gaps so it matches Gemma and Qwen3-32B;
# docs/setup_grid.md): (1) plain-text loss under the knock-out at every layer of 32-40 (it had 32, 36, 40 only);
# (2) the copy-only paste ceiling for the three-step steering (wm2_full3_v1 predates the joint copy); (3) the lens check
# every model gets: graded on jpp_lens's readout items and scored at every layer, the published J++ and the logit lens.
echo "=== 27B gap fills $(date -u +%FT%TZ)"
$PY scripts/removal_textloss.py --name textloss_top_l${MID%-*}_${MID#*-}_v1 --why "$WHY: plain-text loss under the knock-out at every layer of 32-40, as Gemma and Qwen3-32B" \
  --layers $(seq ${MID%-*} ${MID#*-}) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== 27B text loss FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name wm2_full3_v1_ceiling --why "$WHY: the paste ceiling for the three-step steering (wm2_full3_v1 had none)" \
  --n 40 --writes copy --possets question final --tasks full_v8b --tasks-competence full_v8b_competence_v1 --tasks-level all \
  --families PPP PPM PMP MPP MPM MMP --tasks-per-word \
  && $PY scripts/c2_graded.py wm2_full3_v1 --ceiling-from wm2_full3_v1_ceiling > /dev/null || echo "=== 27B three-step ceiling FAILED"
LC=/workspace/bridge-jspace/results/lens_check/qwen3.6-27b
PUB=/workspace/hf_cache/hub/models--neuronpedia--jacobian-lens/snapshots/e166deb5ad540932100ef803c8c9bcc2a5453694/qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt
mkdir -p $LC
( cd /workspace/ext/jpp_lens && uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py Qwen/Qwen3.6-27B $(seq -s, 0 62) $LC/model_correctness.csv \
  && uv run --no-sync python scripts/jpp_cli.py evaluate --hf-model-name Qwen/Qwen3.6-27B --layers $(seq -s, 0 62) --lens $PUB logit \
     --items held-out:0 --correctness-csv $LC/model_correctness.csv --out $LC/eval_ranks.csv \
  && uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/lens_check.py | tail -8 ) > /workspace/scratch/q27_lens_check.log 2>&1 \
  || echo "=== 27B lens check FAILED"
tail -8 /workspace/scratch/q27_lens_check.log
echo "=== 27B gap fills done $(date -u +%FT%TZ)"
