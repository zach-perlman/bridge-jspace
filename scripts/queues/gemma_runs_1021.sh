#!/bin/bash
# Zach (2026-10-21, decided with Zach): Gemma 4 31B-it with its every-layer J++ (target gemma-4-31b-it-full), after its
# fit, at the 27B's relative depths (60 vs 64 layers), mirroring the 27B: smokes; plain-text loss under the knock-out
# (full lens, L30-38); positive control (countries and the suite's M->M; Gemma's steering counts only if each reaches
# >= 50% with a lens write); two-step words on full_v8 (steering alongside the knock-out; C1 / C2-graded rules); the
# three-step words on full_v8b with per-word eligibility (the same, reported); the knock-out dose on the 2x2 words.
# Ends by touching the marker the Qwen3-32B jobs wait for.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-gemmafit5-*.log; do sleep 120; done
grep -q '"gemma-4-31b-it-full"' src/bridge_jspace/pins.py || { echo "no gemma-4-31b-it-full target (fit or gate failed): stop"; exit 1; }
C2=gemma4itr_full_v8_competence_v1
C3=gemma4itr_full_v8b_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] && [ -f results/tasks_v2/$C3/summary.json ] || { echo "missing Gemma competence: stop"; exit 1; }
ok=0; while [ $ok -lt 3 ]; do
  [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 150000 ] && ok=$((ok + 1)) || ok=0
  sleep 30; done
export BJ_TARGET=gemma-4-31b-it-full PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PAD=$([ -f /workspace/scratch/markers/pad_validated ] && echo --pad); echo "=== start $(date -u +%FT%TZ); knock-out batches: ${PAD:-exact-length}"
WHY="Zach (2026-10-21): Gemma 4 31B-it, every-layer J++"
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
W3="--tasks full_v8b --tasks-competence $C3 --tasks-level all --families $THREE --tasks-per-word"
BANDS="11-19 19-27 30-38 0-58"
STEER="--possets question final --band 26-38 --single-step 2 --early 15 19 23"
$PY scripts/ablate_v2.py --name gemma4itf_smoke_full_ko_1021 --why smoke --plan bands --bands 30-38 \
    --conditions paper10 paper10_rot $T2 --n 2 --kinds clean step1 --batch 16 $PAD \
  && BJ_SUITE_BATCH=32 $PY scripts/write_max.py --name gemma4itf_smoke_wm2_full_1021 --why smoke --n 2 --band 30-32 \
    --single-step 1 --early 23 --possets question final $W2 || { echo "smokes failed: stop"; exit 1; }
echo "=== smokes ok $(date -u +%FT%TZ)"
$PY scripts/removal_textloss.py --name gemma4itf_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L30-38" \
  --layers $(seq 30 38) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 26-38 --single-step 2 --early 15 19 23 --from-competence gemma4itb_competence_v1 \
  && $PY scripts/c2_graded.py gemma4itf_wm2_posctrl_v1 > /dev/null || echo "=== positive control FAILED"
# two-step words (the rules): knock-out alongside steering
(
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
    --bands $BANDS --conditions paper10 paper10_rot $T2 --n 1000 --kinds clean --batch 32 $PAD \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_v1 --middle L30-38 --set full_v8 > /dev/null \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_v1 --middle L30-38 --set full_v8 --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at 30-38" --plan bands \
    --bands 30-38 --conditions paper10 paper10_rot $T2 --n 1000 --kinds step1 step2 --batch 32 $PAD \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_steps_v1 --middle L30-38 --set full_v8 > /dev/null || echo "=== two-step steps FAILED"
) &
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_full2_v1 --why "$WHY: two-step, write_max v2, C2-graded" --n 40 \
  $STEER $W2 && $PY scripts/c2_graded.py gemma4itf_wm2_full2_v1 > /dev/null \
  && $PY scripts/c2_graded.py gemma4itf_wm2_full2_v1 --drop-guessable > /dev/null || echo "=== two-step steering FAILED"
wait
echo "=== two-step done $(date -u +%FT%TZ)"
# three-step words (reported): the same
(
  $PY scripts/ablate_v2.py --name gemma4itf_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
    --bands $BANDS --conditions paper10 paper10_rot $T3 --n 1000 --kinds clean --batch 32 $PAD \
    && $PY scripts/c1_v2.py gemma4itf_full3_ko_v1 --middle L30-38 --set full_v8b > /dev/null \
    && $PY scripts/c1_v2.py gemma4itf_full3_ko_v1 --middle L30-38 --set full_v8b --drop-guessable > /dev/null || echo "=== three-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name gemma4itf_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at 30-38" --plan bands \
    --bands 30-38 --conditions paper10 paper10_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 $PAD \
    && $PY scripts/c1_v2.py gemma4itf_full3_ko_steps_v1 --middle L30-38 --set full_v8b > /dev/null || echo "=== three-step steps FAILED"
) &
BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_full3_v1 --why "$WHY: three-step, write_max v2" --n 40 \
  $STEER $W3 && $PY scripts/c2_graded.py gemma4itf_wm2_full3_v1 > /dev/null \
  && $PY scripts/c2_graded.py gemma4itf_wm2_full3_v1 --drop-guessable > /dev/null || echo "=== three-step steering FAILED"
wait
echo "=== three-step done $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name gemma4itf_full_dose_v1 --why "$WHY: knock-out dose on the 2x2 words" --plan bands \
  --bands 30-38 11-19 --tasks full_v8 --tasks-competence $C2 --tasks-words PP PM MP MM --tasks-level all --n 1000 \
  --kinds clean --batch 32 $PAD \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot \
  || echo "=== dose FAILED"
mkdir -p /workspace/scratch/markers && touch /workspace/scratch/markers/gemma_chain_done
echo "=== gemma done $(date -u +%FT%TZ)"
