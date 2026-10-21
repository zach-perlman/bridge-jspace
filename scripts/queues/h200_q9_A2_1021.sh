#!/bin/bash
# Zach (2026-10-21; replaces h200_q9_A_1021.sh before it started: its competence steps are skipped when GPU 1's fill
# (h200_q9_B2_1021.sh fill) already made them. Decided with Zach: "Rerun the 9B on this pipeline so it's comparable? After Qwen3-32B"): Qwen3.5-9B
# with its published J++, the same set as the other models at matched relative depth (32 layers: half the 27B's), GPU 0
# part, after Qwen3-32B's GPU 0 part: competence on full_v8 and full_v8b (with guess prompts), plain-text loss under the
# knock-out (L16-20, every layer), the positive control (countries and the suite's M->M from its suite_v1 competence of
# 2026-10-19; reported), copy_sweep (band paste, every layer, window 6), the two-step steering (full pools, question +
# final, band 14-20, every layer single, early 8/10/12; C2-graded and C2-relative), the three-step steering (reported),
# and the lens check. Its knock-outs run on GPU 1 (h200_q9_B_1021.sh). No dose curves (as the 27B: decide later).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK=/workspace/scratch/markers/q9_competence_done
until grep -qs "^EXIT" $R-h200q32A-*.log; do sleep 60; done
export BJ_TARGET=qwen3.5-9b
WHY="Zach (2026-10-21): Qwen3.5-9B on the v2 pipeline (published J++), the same set as the others"
C2=qwen35_9b_full_v8_competence_v1
C3=qwen35_9b_full_v8b_competence_v1
CS=qwen35_9b_competence_v2
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
STEER="--possets question final --band 14-20 --single-step 1 --early 8 10 12"
echo "=== start $(date -u +%FT%TZ)"
[ -f results/tasks_v2/$C2/summary.json ] || $PY scripts/tasks_v2.py competence --set full_v8 --name $C2 --guess --why "$WHY: competence on full_v8" > /workspace/scratch/q9_comp2.log 2>&1 \
  && $PY scripts/competence_full_report.py $C2 | tail -16 || echo "=== 9B full_v8 competence FAILED"
[ -f results/tasks_v2/$C3/summary.json ] || $PY scripts/tasks_v2.py competence --set full_v8b --name $C3 --guess --why "$WHY: competence on full_v8b" > /workspace/scratch/q9_comp3.log 2>&1 \
  && $PY scripts/competence_full_report.py $C3 | tail -16 || echo "=== 9B full_v8b competence FAILED"
touch $MK  # GPU 1's knock-outs wait for this
[ -f results/tasks_v2/$C2/summary.json ] || { echo "no 9B full_v8 competence: stop"; exit 1; }
BJ_BATCH=32 $PY scripts/write_max.py --name qwen35_9b_smoke_wm2_full_1021 --why smoke --n 2 --band 16-17 \
  --single-step 1 --early 12 --possets question final $W2 || { echo "smoke failed: stop"; exit 1; }
$PY scripts/removal_textloss.py --name qwen35_9b_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L16-20" \
  --layers $(seq 16 20) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name qwen35_9b_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 14-20 --single-step 1 --early 8 10 12 --from-competence $CS \
  && $PY scripts/c2_graded.py qwen35_9b_wm2_posctrl_v1 | tail -2 || echo "=== positive control FAILED"
$PY scripts/copy_sweep.py --name qwen35_9b_copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $C2 --families PP PM MP MM --n 40 --step 1 --window 6 || echo "=== copy sweep FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name qwen35_9b_wm2_full2_v1 --why "$WHY: two-step steering, full pools, joint paste ceiling" \
  --n 1000 $STEER $W2 && $PY scripts/c2_graded.py qwen35_9b_wm2_full2_v1 | tail -14 \
  && $PY scripts/c2_graded.py qwen35_9b_wm2_full2_v1 --drop-guessable > /dev/null || echo "=== two-step steering FAILED"
[ -f results/tasks_v2/$C3/summary.json ] \
  && BJ_BATCH=64 $PY scripts/write_max.py --name qwen35_9b_wm2_full3_v1 --why "$WHY: three-step steering" --n 40 $STEER $W3 \
  && $PY scripts/c2_graded.py qwen35_9b_wm2_full3_v1 > /dev/null || echo "=== three-step steering FAILED"
LC=/workspace/bridge-jspace/results/lens_check/qwen3.5-9b
mkdir -p $LC
PUB9=$($PY -c "from huggingface_hub import hf_hub_download as h; print(h('neuronpedia/jacobian-lens', 'qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt', revision='e166deb5ad540932100ef803c8c9bcc2a5453694'))")
( cd /workspace/ext/jpp_lens && uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py Qwen/Qwen3.5-9B $(seq -s, 0 30) $LC/model_correctness.csv \
  && uv run --no-sync python scripts/jpp_cli.py evaluate --hf-model-name Qwen/Qwen3.5-9B --layers $(seq -s, 0 30) --lens $PUB9 logit \
     --items held-out:0 --correctness-csv $LC/model_correctness.csv --out $LC/eval_ranks.csv \
  && uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/lens_check.py | tail -8 ) > /workspace/scratch/q9_lens_check.log 2>&1 \
  || echo "=== 9B lens check FAILED"
echo "=== 9B GPU 0 part done $(date -u +%FT%TZ)"
