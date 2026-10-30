#!/bin/bash
# Zach (2026-10-21, decided with Zach): GPU 0 of the 2x H200 box, after the 27B steering rerun (moved from GPU 1): the 27B knock-out additions on
# the two-step words of full_v8. (1) C1's second kill test: paper10 / paper10_keepown and their rotated controls at
# L32-40 (c1_v2: >= 75% of the memory-final loss restored kills C1). (2) Two more rotation seeds for the control
# (paper10_rot, --seed-offset 1 and 2). (3) The position split: the facts only (--positions context) and the question
# only (--positions question), paper10 + rotated, at L12-20 and L32-40.
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
$PY scripts/ablate_v2.py --name full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep the subject's own word)" \
  --plan bands --bands 32-40 --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T \
  && $PY scripts/c1_v2.py full2_ko_keepown_v1 --middle L32-40 --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name full2_ko_rotseed${s}_v1 --why "$WHY: another draw of the rotated control (seed offset $s)" \
    --plan bands --bands 32-40 --conditions paper10_rot --seed-offset $s $T || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" \
    --plan bands --bands 12-20 32-40 --conditions paper10 paper10_rot --positions $pos $T \
    && $PY scripts/c1_v2.py full2_ko_pos_${pos}_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
echo "=== GPU 1 Qwen reruns done $(date -u +%FT%TZ)"
# --- appended 2026-10-21 ~19:40 UTC while this queue waited (Zach: "Queue it such that all these additions will apply to
# the current 27b model and all future models"; pipeline review, code 1330338 + 7363cf7). The 27B additions, GPU 0,
# before the Gemma steering: (1) the paste ceiling for wm2_full2_v2 (its joint copy stacked): copy only, same cases,
# c2_graded --ceiling-from; (2) the specificity control: unembed10 + rotated at 12-20, 20-28, 32-40 (whole depth left
# out: ~90 min), compared with full2_ko_v1's paper10 on the same items; (3) the copy sweep again with the band paste.
echo "=== 27B additions $(date -u +%FT%TZ)"
W2B="--possets question final --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-level all"
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name smoke_wm2_copyonly_1021 --why smoke --n 2 --writes copy $W2B --families PP MM \
  && BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name wm2_full2_v2_ceiling --why "$WHY: the paste ceiling for wm2_full2_v2 (its joint copy stacked)" \
  --n 1000 --writes copy $W2B --families PP PM MP MM CP CM \
  && $PY scripts/c2_graded.py wm2_full2_v2 --ceiling-from wm2_full2_v2_ceiling | tail -8 \
  && $PY scripts/c2_graded.py wm2_full2_v2 --fresh-vs wm2_full2_v1 --ceiling-from wm2_full2_v2_ceiling | tail -4 \
  && $PY scripts/c2_graded.py wm2_full2_v2 --drop-guessable --ceiling-from wm2_full2_v2_ceiling > /dev/null || echo "=== paste ceiling FAILED"
$PY scripts/ablate_v2.py --name smoke_unembed_ko_1021 --why smoke --plan bands --bands 32-40 --conditions unembed10 unembed10_rot \
  --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words PP MM --tasks-level all --n 2 --kinds clean --batch 16 \
  && $PY scripts/ablate_v2.py --name full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands 12-20 20-28 32-40 --conditions unembed10 unembed10_rot $T \
  && $PY scripts/c1_specificity.py full2_ko_v1 full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py full2_ko_unembed_v1 --middle L32-40 --set full_v8 > /dev/null || echo "=== unembed knock-out FAILED"
$PY scripts/copy_sweep.py --name smoke_copy_sweep_band_1021 --why smoke --tasks full_v8 --tasks-competence full_v8_competence_v1 \
  --families PP MM --n 1 \
  && $PY scripts/copy_sweep.py --name copy_sweep_full2_v2 --why "$WHY: the copy sweep with the band paste (v1's from mode stacked)" \
  --tasks full_v8 --tasks-competence full_v8_competence_v1 --families PP PM MP MM --n 40 || echo "=== copy sweep v2 FAILED"
echo "=== 27B additions done $(date -u +%FT%TZ)"
# --- appended 2026-10-21 ~19:50 UTC while this queue waited (Zach: fill the 27B's gaps so it matches Gemma and Qwen3-32B;
# docs/archive/setup_grid.md): (1) plain-text loss under the knock-out at every layer of 32-40 (it had 32, 36, 40 only);
# (2) the copy-only paste ceiling for the three-step steering (wm2_full3_v1 predates the joint copy); (3) the lens check
# every model gets: graded on jpp_lens's readout items and scored at every layer, the published J++ and the logit lens.
echo "=== 27B gap fills $(date -u +%FT%TZ)"
$PY scripts/removal_textloss.py --name textloss_top_l32_40_v1 --why "$WHY: plain-text loss under the knock-out at every layer of 32-40, as Gemma and Qwen3-32B" \
  --layers $(seq 32 40) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== 27B text loss FAILED"
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name wm2_full3_v1_ceiling --why "$WHY: the paste ceiling for the three-step steering (wm2_full3_v1 had none)" \
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
# --- appended 2026-10-21 ~20:00 UTC while this queue waited (decided with Zach): the 27B's depth profile on the v2 rule
# words, the same plan as every model's (nine-layer windows sliding by 4; PP MP PM MM, first 60 eligible per word;
# paper10 + rotated): is 32-40, chosen on the suite, also where the v2 split is, or should the 27B's middle-band runs
# be redone? (Analysis: half the bridge entities choose the window, the other half score it.)
echo "=== 27B depth profile $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name full2_profile_v1 --why "$WHY: depth profile on the v2 rule words (does 32-40 hold on v2?)" \
  --plan bands --bands 0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 52-60 \
  --conditions paper10 paper10_rot --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words PP MP PM MM \
  --tasks-level all --n 60 --kinds clean --batch 32 || echo "=== 27B depth profile FAILED"
echo "=== 27B depth profile done $(date -u +%FT%TZ)"
