#!/bin/bash
# Zach (2026-10-21, decided with Zach; replaces the rest of h200_gemma_B3e_1021.sh once its C1 and specificity control are
# done; the rest sat at a band where every word is near 0%): the attention-sink diagnostic, docs/prereg_sink_1021.md.
# (1) Gemma, ctrl_v8, layers 30-38 / 40-48 / 48-56, paper10_nosink + rotated: decides (scripts/sink_decision.py writes
# the protocol for later C1 runs to the marker). Descriptive: (2) Gemma plain-text loss with and without _nosink, (3) the
# Gemma dose at 30-38, (4) the 27B at 12-20 and 32-40 under _nosink, (5) Gemma's lens check (moved from B3e).
# ARTIFACT: the 27B's test-set C1 at 32-40 under _nosink (within 5 points of 36 keeps its results), then Gemma's band
# re-chosen on ctrl_v8 under _nosink and its C1 core rerun (C1 with the pre-set 30-38 band added, specificity,
# keep-own). Otherwise: Gemma's test-set C1 at the pre-set relative band 30-38 under paper10.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
MKP=/workspace/scratch/markers/c1_protocol
GT=gemma-4-31b-it-full
CC=gemma4itf_ctrl_v8_competence_v1
C2=gemma4itr_full_v8_competence_v1
TWO="PP PM MP MM CP CM"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
K="--n 1000 --kinds clean --batch 32"
CTRL="--tasks ctrl_v8 --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32"
WHY="Zach (2026-10-21): the attention-sink diagnostic (docs/prereg_sink_1021.md)"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
echo "=== start $(date -u +%FT%TZ)"
BJ_TARGET=$GT $PY scripts/ablate_v2.py --name gemma4itf_sink_diag_v1 --why "$WHY: Gemma, decides" --plan bands \
  --bands 30-38 40-48 48-56 --conditions paper10_nosink paper10_nosink_rot $CTRL --tasks-competence $CC || echo "=== diagnostic FAILED"
$PY scripts/sink_decision.py gemma4itf_sink_diag_v1 --marker $MKP > /workspace/scratch/sink_verdict.txt 2>&1 || echo "=== verdict FAILED"
head -16 /workspace/scratch/sink_verdict.txt
[ -s $MKP ] || { echo paper10 > $MKP; echo "=== no verdict written: paper10 kept"; }
echo "=== protocol: $(cat $MKP) $(date -u +%T)"
BJ_TARGET=$GT $PY scripts/removal_textloss.py --name gemma4itf_sink_textloss_v1 --why "$WHY: Gemma plain-text loss, 30-38" \
  --layers $(seq 30 38) --conditions none top1 top1_rot top1_nosink top1_nosink_rot top10 top10_rot top10_nosink top10_nosink_rot \
  || echo "=== text loss FAILED"
BJ_TARGET=$GT $PY scripts/ablate_v2.py --name gemma4itf_sink_dose_v1 --why "$WHY: Gemma dose at 30-38" --plan bands --bands 30-38 \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot $CTRL --tasks-competence $CC || echo "=== dose FAILED"
$PY scripts/ablate_v2.py --name sink_diag_27b_v1 --why "$WHY: the 27B" --plan bands --bands 12-20 32-40 \
  --conditions paper10_nosink paper10_nosink_rot $CTRL --tasks-competence ctrl_v8_competence_v1 || echo "=== 27B diagnostic FAILED"
$PY scripts/sink_decision.py gemma4itf_sink_diag_v1 --textloss gemma4itf_sink_textloss_v1 --dose gemma4itf_sink_dose_v1 \
  --qwen sink_diag_27b_v1 > /dev/null || echo "=== full verdict tables FAILED"
mkdir -p results/lens_check/gemma-4-31b-it-full
( cd /workspace/ext/jpp_lens && uv run --no-sync python scripts/jpp_cli.py evaluate --hf-model-name google/gemma-4-31B-it \
    --layers $(seq -s, 0 58) --lens logit --items held-out:0 \
    --correctness-csv /workspace/bridge-jspace/results/lens_fit/gemma_it_full/model_correctness.csv \
    --out /workspace/bridge-jspace/results/lens_check/gemma-4-31b-it-full/eval_ranks_logit.csv ) > /workspace/scratch/gemma_lens_check.log 2>&1 \
  || echo "=== Gemma lens check FAILED"
if [ "$(cat $MKP)" = nosink ]; then
  echo "=== ARTIFACT: the 27B equivalence, then Gemma's C1 core under _nosink $(date -u +%T)"
  $PY scripts/ablate_v2.py --name full2_ko_nosink_v1 --why "$WHY: the 27B's test-set C1 at 32-40 under _nosink" --plan bands \
    --bands 32-40 --conditions paper10_nosink paper10_nosink_rot --tasks full_v8 --tasks-competence full_v8_competence_v1 \
    --tasks-words $TWO --tasks-level all $K && $PY scripts/c1_v2.py full2_ko_nosink_v1 --middle L32-40 --set full_v8 --suffix _nosink | tail -2 \
    || echo "=== 27B equivalence FAILED"
  export BJ_TARGET=$GT
  SW=gemma4itf_ctrl_sweep_nosink_v1
  $PY scripts/ablate_v2.py --name $SW --why "$WHY: Gemma's band under _nosink (ctrl_v8)" --plan bands \
    --bands 0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 --conditions paper10_nosink paper10_nosink_rot \
    $CTRL --tasks-competence $CC || echo "=== sweep FAILED"
  MID=$($PY scripts/choose_band.py $SW _nosink) || MID=""
  [ -n "$MID" ] || { MID=30-38; echo "=== no band chosen: 30-38 instead"; }
  echo "=== Gemma middle band under _nosink: $MID"
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_nosink_v1 --why "$WHY: Gemma's C1 under _nosink" --plan bands \
    --bands $(uniq_bands 11-19 19-27 30-38 $MID 0-58) --conditions paper10_nosink paper10_nosink_rot $T2 $K \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_nosink_v1 --middle L$MID --set full_v8 --suffix _nosink | tail -2 \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_nosink_v1 --middle L$MID --set full_v8 --suffix _nosink --drop-guessable > /dev/null \
    || echo "=== Gemma C1 under _nosink FAILED"
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_unembed_nosink_v1 --why "$WHY: Gemma's specificity control under _nosink" \
    --plan bands --bands $(uniq_bands 11-19 19-27 $MID) --conditions unembed10_nosink unembed10_nosink_rot $T2 $K \
    && $PY scripts/c1_specificity.py gemma4itf_full2_ko_nosink_v1 gemma4itf_full2_ko_unembed_nosink_v1 --set full_v8 --suffix _nosink | tail -6 \
    || echo "=== Gemma specificity under _nosink FAILED"
  $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_keepown_nosink_v1 --why "$WHY: Gemma's keep-own under _nosink" --plan bands \
    --bands $MID --conditions paper10_nosink paper10_nosink_rot paper10_keepown_nosink paper10_keepown_nosink_rot $T2 $K \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_keepown_nosink_v1 --middle L$MID --set full_v8 --suffix _nosink | tail -3 \
    || echo "=== Gemma keep-own under _nosink FAILED"
else
  echo "=== paper10 stays: Gemma's test-set C1 at the pre-set relative band 30-38 $(date -u +%T)"
  BJ_TARGET=$GT $PY scripts/ablate_v2.py --name gemma4itf_full2_ko_l30_38_v1 --why "$WHY: the pre-set relative band 30-38" \
    --plan bands --bands 30-38 --conditions paper10 paper10_rot $T2 $K \
    && $PY scripts/c1_v2.py gemma4itf_full2_ko_l30_38_v1 --middle L30-38 --set full_v8 | tail -2 || echo "=== 30-38 FAILED"
fi
echo "=== Gemma sink diagnostic done $(date -u +%FT%TZ)"
