#!/bin/bash
# Zach (2026-10-21, decided with Zach: right after the Gemma fit, so GPU 1 never idles): Gemma 4 31B-it with its every-layer J++, the knock-outs on
# GPU 1, at the 27B's relative depths (60 vs 64 layers). Two-step words on full_v8: the C1 rule (c1_v2 --middle L30-38;
# whole question at 11-19, 19-27, 30-38 and whole depth), C1's second kill test (keep own word), two more control
# seeds, the position split, each step alone; three-step words on full_v8b (per-word eligibility, reported); the dose
# curve on the 2x2 words (top-K, K = 1-100 at 30-38 and 11-19) and smaller doses (single layers 34 and 15, K = 1-10).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200gemmafit-*.log; do sleep 60; done  # 2026-10-21 (Zach: no idle GPU): right after the fit, not after the 27B reruns
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
export CUDA_VISIBLE_DEVICES=1
K="--n 1000 --kinds clean --batch 32"
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name gemma4itf_smoke_full_ko_1021 --why smoke --plan bands --bands 30-38 \
  --conditions paper10 paper10_rot $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
$PY scripts/ablate_v2.py --name gemma4itf_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T2 $K \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_v1 --middle L30-38 --set full_v8 | tail -2 \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_v1 --middle L30-38 --set full_v8 --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands 30-38 --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_keepown_v1 --middle L30-38 --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_rotseed${s}_v1 --why "$WHY: rotated control, seed offset $s" --plan bands \
    --bands 30-38 --conditions paper10_rot --seed-offset $s $T2 $K || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands 11-19 30-38 --conditions paper10 paper10_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_pos_${pos}_v1 --middle L30-38 --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name gemma4itf_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at 30-38" --plan bands \
  --bands 30-38 --conditions paper10 paper10_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_steps_v1 --middle L30-38 --set full_v8 > /dev/null || echo "=== two-step steps FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full_dose_v1 --why "$WHY: knock-out dose on the 2x2 words" --plan bands \
  --bands 30-38 11-19 --tasks full_v8 --tasks-competence $C2 --tasks-words PP PM MP MM --tasks-level all $K \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot \
  || echo "=== dose FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full_dose_single_v1 --why "$WHY: smaller doses, single layers (Zach)" --plan bands \
  --bands 34 15 --tasks full_v8 --tasks-competence $C2 --tasks-words PP PM MP MM --tasks-level all $K \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot || echo "=== single-layer dose FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T3 $K \
  && $PY scripts/c1_v2.py gemma4itf_full3_ko_v1 --middle L30-38 --set full_v8b > /dev/null || echo "=== three-step knock-out FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at 30-38" --plan bands \
  --bands 30-38 --conditions paper10 paper10_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
  && $PY scripts/c1_v2.py gemma4itf_full3_ko_steps_v1 --middle L30-38 --set full_v8b > /dev/null || echo "=== three-step steps FAILED"
echo "=== Gemma knock-outs done $(date -u +%FT%TZ)"
# --- appended 2026-10-21 ~19:40 UTC while this queue waited (Zach: the additions apply to every model; 7363cf7): the
# specificity control on Gemma, unembed10 + rotated at 11-19, 19-27, 30-38 (whole depth left out), compared with
# gemma4itf_full2_ko_v1's paper10 on the same items. (Gemma's steering and copy sweep get the paste fixes from the
# code; its C1 reports get the margin-matched gap.)
echo "=== Gemma additions $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name gemma4itf_smoke_unembed_ko_1021 --why smoke --plan bands --bands 30-38 \
  --conditions unembed10 unembed10_rot $T2 --n 2 --kinds clean --batch 16 \
  && $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands 11-19 19-27 30-38 --conditions unembed10 unembed10_rot $T2 $K \
  && $PY scripts/c1_specificity.py gemma4itf_full2_ko_v1 gemma4itf_full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_unembed_v1 --middle L30-38 --set full_v8 > /dev/null || echo "=== Gemma unembed knock-out FAILED"
echo "=== Gemma additions done $(date -u +%FT%TZ)"
