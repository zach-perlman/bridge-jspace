#!/bin/bash
# Zach (2026-10-21; replaces h200_gemma_B3b/B3c_1021.sh before they started (a failed suite smoke now falls back to the
# relative-depth band instead of stopping), decided with Zach: each model's middle band is
# chosen by the procedure that picked the 27B's 32-40, on its own suite depth sweep, before its tasks_v2 knock-outs;
# scripts/choose_band.py): Gemma 4 31B-it with its every-layer J++, the knock-outs on GPU 1 right after its fit. First the
# suite sweep (paper10 + rotated, BL BR RL RR, n = 100, nine-layer windows sliding by 4) and the band choice (MID);
# then, on full_v8's two-step words: the C1 rule (c1_v2 --middle MID; whole question at 11-19, 19-27, MID and whole
# depth), the specificity control (unembed10 at 11-19, 19-27, MID), keep own word, two more control seeds, the position
# split (11-19, MID), each step alone (MID); three-step words on full_v8b: whole question, each step alone (MID); the
# lens check. The early bands stay at the 27B's relative depths.
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
$PY scripts/ablate_v2.py --name gemma4itf_smoke_suite_ko_1021 --why smoke --plan bands --bands 30-38 \
  --conditions paper10 paper10_rot --families BL BR RL RR --kinds clean --n 2 --competence gemma4itb_competence_v1 \
  --batch 16 || echo "=== suite smoke FAILED: the middle band falls back to the relative-depth band"
SW=gemma4itf_suite_sweep_v1
[ -f results/ablate_v2/$SW/summary.json ] || $PY scripts/ablate_v2.py --name $SW \
  --why "$WHY: suite depth sweep to choose the middle band (the 27B's procedure)" --plan bands \
  --bands 0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 --conditions paper10 paper10_rot \
  --families BL BR RL RR --kinds clean --n 100 --competence gemma4itb_competence_v1 || echo "=== suite sweep FAILED"
MID=$($PY scripts/choose_band.py $SW) || MID=""
[ -n "$MID" ] || { MID=30-38; echo "=== no band chosen: the relative-depth band 30-38 instead"; }
echo "=== middle band: $MID (relative-depth band: 30-38)"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
BANDS=$(uniq_bands 11-19 19-27 $MID 0-58)
$PY scripts/ablate_v2.py --name gemma4itf_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T2 $K \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_v1 --middle L$MID --set full_v8 | tail -2 \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_v1 --middle L$MID --set full_v8 --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_smoke_unembed_ko_1021 --why smoke --plan bands --bands 30-38 \
  --conditions unembed10 unembed10_rot $T2 --n 2 --kinds clean --batch 16 \
  && $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands $(uniq_bands 11-19 19-27 $MID) --conditions unembed10 unembed10_rot $T2 $K \
  && $PY scripts/c1_specificity.py gemma4itf_full2_ko_v1 gemma4itf_full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_unembed_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== Gemma unembed knock-out FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands $MID --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_keepown_v1 --middle L$MID --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_rotseed${s}_v1 --why "$WHY: rotated control, seed offset $s" --plan bands \
    --bands $MID --conditions paper10_rot --seed-offset $s $T2 $K || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands $(uniq_bands 11-19 $MID) --conditions paper10 paper10_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_pos_${pos}_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name gemma4itf_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at the middle band" --plan bands \
  --bands $MID --conditions paper10 paper10_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py gemma4itf_full2_ko_steps_v1 --middle L$MID --set full_v8 > /dev/null || echo "=== two-step steps FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T3 $K \
  && $PY scripts/c1_v2.py gemma4itf_full3_ko_v1 --middle L$MID --set full_v8b > /dev/null || echo "=== three-step knock-out FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at the middle band" --plan bands \
  --bands $MID --conditions paper10 paper10_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
  && $PY scripts/c1_v2.py gemma4itf_full3_ko_steps_v1 --middle L$MID --set full_v8b > /dev/null || echo "=== three-step steps FAILED"
mkdir -p results/lens_check/gemma-4-31b-it-full
( cd /workspace/ext/jpp_lens && uv run --no-sync python scripts/jpp_cli.py evaluate --hf-model-name google/gemma-4-31B-it \
    --layers $(seq -s, 0 58) --lens logit --items held-out:0 \
    --correctness-csv /workspace/bridge-jspace/results/lens_fit/gemma_it_full/model_correctness.csv \
    --out /workspace/bridge-jspace/results/lens_check/gemma-4-31b-it-full/eval_ranks_logit.csv ) > /workspace/scratch/gemma_lens_check.log 2>&1 \
  || echo "=== Gemma lens check FAILED"
echo "=== Gemma knock-outs done $(date -u +%FT%TZ)"
