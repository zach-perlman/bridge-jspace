#!/bin/bash
# Zach (2026-10-21, "Sure, queue it"; decided with Zach: every model gets the same set): Qwen3-32B with its every-layer
# J++, GPU 0 part, after its fit, merge and full_v8 competence (h200_q32_merge_1021.sh). The same runs as Gemma's
# (h200_gemma_A2 + B3 + the additions) at the 27B's depths (both have 64 layers): the extra competence runs (full_v8b for
# the three-step words; suite_v1 main, first 150 per family, for the steering positive control, as Gemma's
# gemma4itb_competence_v1), plain-text loss under the knock-out (L32-40, every layer), the positive control (countries
# and the suite's M->M), copy_sweep (band paste), the two-step steering on full_v8 (full pools, question + final, band
# 28-40, early 16/20/24, joint paste ceiling; C2-graded and C2-relative), the three-step steering (reported), then the
# dose curves (2x2 words: top-K, K = 1-100 at 32-40 and 12-20; single layers 36 and 16, K = 1-10). The other knock-outs
# run on GPU 1 (h200_q32_B_1021.sh), split so both GPUs finish at about the same time.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK=/workspace/scratch/markers/q32_competence_done
until grep -qs "^EXIT" $R-h200q32m-*.log; do sleep 60; done
grep -q '"qwen3-32b"' src/bridge_jspace/pins.py || { echo "no qwen3-32b target (fit or gate failed): stop"; exit 1; }
C2=qwen3_32b_full_v8_competence_v1
C3=qwen3_32b_full_v8b_competence_v1
CS=qwen3_32b_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] || { echo "missing Qwen3-32B full_v8 competence: stop"; exit 1; }
export BJ_TARGET=qwen3-32b
WHY="Zach (2026-10-21): Qwen3-32B, every-layer J++ (32 prompts)"
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
STEER="--possets question final --band 28-40 --single-step 2 --early 16 20 24"
K="--n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/tasks_v2.py competence --set full_v8b --name $C3 --guess \
  --why "$WHY: competence on full_v8b (three-step words), as the 27B and Gemma" > /workspace/scratch/q32_comp3.log 2>&1 \
  && $PY scripts/competence_full_report.py $C3 | tail -16 || echo "=== full_v8b competence FAILED"
$PY scripts/suite_v1.py manifest --set main --name $CS --limit 150 \
  --why "$WHY: suite competence (first 150 per family) for the steering positive control, as Gemma's" \
  && $PY scripts/suite_v1.py competence --name $CS > /workspace/scratch/q32_suitecomp.log 2>&1 || echo "=== suite competence FAILED"
touch $MK  # GPU 1's knock-outs wait for this
BJ_SUITE_BATCH=32 $PY scripts/write_max.py --name qwen3_32b_smoke_wm2_full_1021 --why smoke --n 2 --band 32-34 \
  --single-step 1 --early 24 --possets question final $W2 || { echo "smoke failed: stop"; exit 1; }
$PY scripts/removal_textloss.py --name qwen3_32b_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L32-40" \
  --layers $(seq 32 40) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
[ -f results/suite_v1/$CS/summary.json ] \
  && BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 28-40 --single-step 2 --early 16 20 24 --from-competence $CS \
  && $PY scripts/c2_graded.py qwen3_32b_wm2_posctrl_v1 | tail -2 || echo "=== positive control FAILED"
$PY scripts/copy_sweep.py --name qwen3_32b_copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $C2 --families PP PM MP MM --n 40 || echo "=== copy sweep FAILED"
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_full2_v1 --why "$WHY: two-step steering, full pools, joint paste ceiling" \
  --n 1000 $STEER $W2 && $PY scripts/c2_graded.py qwen3_32b_wm2_full2_v1 | tail -14 \
  && $PY scripts/c2_graded.py qwen3_32b_wm2_full2_v1 --drop-guessable > /dev/null || echo "=== two-step steering FAILED"
[ -f results/tasks_v2/$C3/summary.json ] \
  && BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_full3_v1 --why "$WHY: three-step steering" --n 40 $STEER $W3 \
  && $PY scripts/c2_graded.py qwen3_32b_wm2_full3_v1 > /dev/null || echo "=== three-step steering FAILED"
$PY scripts/ablate_v2.py --name qwen3_32b_smoke_dose_1021 --why smoke --plan bands --bands 32-40 --conditions top1 top1_rot \
  --tasks full_v8 --tasks-competence $C2 --tasks-words PP MM --tasks-level all --n 2 --kinds clean --batch 16 \
  && $PY scripts/ablate_v2.py --name qwen3_32b_full_dose_v1 --why "$WHY: knock-out dose on the 2x2 words" --plan bands \
  --bands 32-40 12-20 --tasks full_v8 --tasks-competence $C2 --tasks-words PP PM MP MM --tasks-level all $K \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot \
  || echo "=== dose FAILED"
$PY scripts/ablate_v2.py --name qwen3_32b_full_dose_single_v1 --why "$WHY: smaller doses, single layers" --plan bands \
  --bands 36 16 --tasks full_v8 --tasks-competence $C2 --tasks-words PP PM MP MM --tasks-level all $K \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot || echo "=== single-layer dose FAILED"
echo "=== Qwen3-32B GPU 0 part done $(date -u +%FT%TZ)"
