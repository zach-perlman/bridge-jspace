#!/bin/bash
# Zach (2026-10-21): Gemma 4 31B-it with its every-layer J++, branch A on GPU 0 of the 2x H200 box (after the Gemma
# fit and GPU 0's Qwen3-32B work): plain-text loss under the knock-out (L30-38), the positive control (countries and the
# suite's M->M: Gemma's steering counts only if each reaches >= 50% with a lens write), then steering (write_max v2,
# question + final positions, band 26-38, early 15/19/23, 40 per word): two-step words on full_v8 (C2-graded rule),
# three-step words on full_v8b (per-word eligibility, reported). Branch B (GPU 1) does the knock-outs.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200gemmafit-*.log; do sleep 120; done
grep -q '"gemma-4-31b-it-full"' src/bridge_jspace/pins.py || { echo "no gemma-4-31b-it-full target (fit or gate failed): stop"; exit 1; }
C2=gemma4itr_full_v8_competence_v1
C3=gemma4itr_full_v8b_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] && [ -f results/tasks_v2/$C3/summary.json ] || { echo "missing Gemma competence: stop"; exit 1; }
export BJ_TARGET=gemma-4-31b-it-full
WHY="Zach (2026-10-21): Gemma 4 31B-it, every-layer J++"
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
BANDS="11-19 19-27 30-38 0-58"
STEER="--possets question final --band 26-38 --single-step 2 --early 15 19 23"
until grep -qs "^EXIT" $R-h200gpu0-*.log; do sleep 120; done
export CUDA_VISIBLE_DEVICES=0
echo "=== start $(date -u +%FT%TZ)"
BJ_BATCH=32 $PY scripts/write_max.py --name gemma4itf_smoke_wm2_full_1021 --why smoke --n 2 --band 30-32 \
  --single-step 1 --early 23 --possets question final $W2 || { echo "smoke failed: stop"; exit 1; }
$PY scripts/removal_textloss.py --name gemma4itf_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L30-38" \
  --layers $(seq 30 38) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 26-38 --single-step 2 --early 15 19 23 --from-competence gemma4itb_competence_v1 \
  && $PY scripts/c2_graded.py gemma4itf_wm2_posctrl_v1 | tail -2 || echo "=== positive control FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_full2_v1 --why "$WHY: two-step, write_max v2, C2-graded" --n 40 \
  $STEER $W2 && $PY scripts/c2_graded.py gemma4itf_wm2_full2_v1 | tail -2 \
  && $PY scripts/c2_graded.py gemma4itf_wm2_full2_v1 --drop-guessable > /dev/null || echo "=== two-step steering FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_full3_v1 --why "$WHY: three-step, write_max v2" --n 40 \
  $STEER $W3 && $PY scripts/c2_graded.py gemma4itf_wm2_full3_v1 > /dev/null \
  && $PY scripts/c2_graded.py gemma4itf_wm2_full3_v1 --drop-guessable > /dev/null || echo "=== three-step steering FAILED"
echo "=== branch A done $(date -u +%FT%TZ)"
