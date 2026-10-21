#!/bin/bash
# Zach (2026-10-21, decided with Zach: full v2 everywhere; Gemma before anything Qwen3-32B): Gemma 4 31B-it with its
# every-layer J++ (target gemma-4-31b-it-full, registered by gemma_fit_1021.sh) on the full v8 set, at the 27B's
# relative depths (60 vs 64 layers). After the 27B full-set job. Competence; smokes; positive control (countries and
# the suite's M->M: Gemma's steering counts only if each reaches >= 50% with a lens write); then (A) C2-graded steering, then (B) C1: paper10
# + rotated control at 11-19, 19-27, 30-38 and whole depth, then each step alone at 30-38 (c1_v2 --middle L30-38) and
# the steering: write_max v2, band 26-38, early 15/19/23, 40 per word; then the knock-out dose (top-K, K = 1-100, each
# with its rotated control) on the 2x2 words at 30-38 and 11-19. Touches the marker the Qwen3-32B job waits for.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-gemmafit3-1021-0445.log; do sleep 120; done  # after the 27B job and the fit (competence -> steer -> knockout)
grep -q '"gemma-4-31b-it-full"' src/bridge_jspace/pins.py || { echo "no gemma-4-31b-it-full target (the fit or its gate failed): stop"; exit 1; }
ok=0; while [ $ok -lt 3 ]; do
  [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 150000 ] && ok=$((ok + 1)) || ok=0
  sleep 30; done
echo "=== start $(date -u +%FT%TZ)"
export BJ_TARGET=gemma-4-31b-it-full PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
WHY="Zach (2026-10-21): Gemma 4 31B-it, every-layer J++, the full v8 set"
COMP=gemma4itr_full_v8_competence_v1  # comp_both_1021.sh (same model; competence needs no lens)
WORDS="PP PM MP MM CP CM PPP PPM PMP MPP MPM MMP"
[ -f results/tasks_v2/$COMP/summary.json ] || { echo "no Gemma competence: stop"; exit 1; }
T="--tasks full_v8 --tasks-competence $COMP --tasks-words $WORDS --tasks-level all --tasks-strata core secondary"
W="--tasks full_v8 --tasks-competence $COMP --tasks-level all --families $WORDS"
$PY scripts/ablate_v2.py --name gemma4itf_smoke_full_ko_1021 --why smoke --plan bands --bands 30-38 \
    --conditions paper10 paper10_rot $T --n 2 --kinds clean step1 --batch 16 \
  && BJ_BATCH=32 $PY scripts/write_max.py --name gemma4itf_smoke_wm2_full_1021 --why smoke --n 2 --band 30-32 \
    --single-step 1 --early 23 --possets question final $W || { echo "smokes failed: stop"; exit 1; }
echo "=== smokes ok $(date -u +%FT%TZ)"
$PY scripts/removal_textloss.py --name gemma4itf_textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, the 27B L32-40 depth" \
  --layers $(seq 30 38) --conditions none top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_posctrl_v1 --why "$WHY: positive control (countries, suite M->M)" \
  --n 60 --families RR --band 26-38 --single-step 2 --early 15 19 23 --from-competence gemma4itb_competence_v1 \
  && $PY scripts/c2_graded.py gemma4itf_wm2_posctrl_v1 || echo "=== positive control FAILED"
BJ_BATCH=64 $PY scripts/write_max.py --name gemma4itf_wm2_full_v1 --why "$WHY: write_max v2, C2-graded" --n 40 \
  --band 26-38 --single-step 2 --early 15 19 23 $W && $PY scripts/c2_graded.py gemma4itf_wm2_full_v1 || echo "=== steering FAILED"
  $PY scripts/ablate_v2.py --name gemma4itf_full_ko_v1 --why "$WHY: C1, whole question" --plan bands \
    --bands 11-19 19-27 30-38 0-58 --conditions paper10 paper10_rot $T --n 1000 --kinds clean --batch 32 \
    && $PY scripts/c1_v2.py gemma4itf_full_ko_v1 --middle L30-38 --set full_v8 || echo "=== knock-out FAILED"
  $PY scripts/ablate_v2.py --name gemma4itf_full_ko_steps_v1 --why "$WHY: C1, each step alone at the middle band" \
    --plan bands --bands 30-38 --conditions paper10 paper10_rot $T --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py gemma4itf_full_ko_steps_v1 --middle L30-38 --set full_v8 || echo "=== steps knock-out FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full_dose_v1 --why "$WHY: knock-out dose on the 2x2 words" --plan bands \
  --bands 30-38 11-19 --tasks full_v8 --tasks-competence $COMP --tasks-words PP PM MP MM --tasks-level all --n 1000 \
  --kinds clean --batch 16 \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot \
  || echo "=== dose FAILED"
mkdir -p /workspace/scratch/markers && touch /workspace/scratch/markers/gemma_chain_done
echo "=== gemma full done $(date -u +%FT%TZ)"
