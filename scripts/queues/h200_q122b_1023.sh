#!/bin/bash
# Zach (2026-10-23; approved: "Go ahead" on the 122B; GPU 0 alone once downloaded: the Olmo-3 run moved to GPU 1): Qwen3.5-122B-A10B (FP8, published J++) through every model's C1
# procedure on GPU 0, after the 122B download and the Olmo-3 powered run. 48 blocks: 7-layer windows sliding by 3 (as
# Muse's 52). Batch 8 (the old pipeline ran out of memory at 16). Competence on ctrl_v8 and full_v8_two (full_v8's two-step
# items, same ids). Steps: the untestable gate (L21-27), competence, ctrl_v8 sweep, band, C1 at the band and at the
# 27B's relative depth (24-30), the logit-lens control, the dose at the band.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^=== 122B downloaded" $R-h200dl122b-1023-0200.log; do sleep 60; done
export BJ_TARGET=qwen3.5-122b-a10b
P=qwen35_122b_
WHY="Zach (2026-10-23): Qwen3.5-122B-A10B (published J++) on the v2 pipeline (a third Qwen3.5/3.6 hybrid; larger model)"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }
echo "=== start $(date -u +%FT%TZ)"
run removal_textloss/${P}textloss_top_v1 $PY scripts/removal_textloss.py --name ${P}textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L21-27 (the gate)" \
  --layers $(seq 21 27) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
for spec in ${P}ctrl_v8_competence_v1:ctrl_v8 ${P}full_v8_two_competence_v1:full_v8_two; do
  c=${spec%%:*} s=${spec#*:}
  run tasks_v2/$c $PY scripts/tasks_v2.py competence --set $s --name $c --guess --why "$WHY: competence on $s" > /workspace/scratch/$c.log 2>&1 || echo "=== competence $c FAILED"
done
[ -f results/tasks_v2/${P}full_v8_two_competence_v1/summary.json ] || { echo "no competence: stop"; exit 1; }
run ablate_v2/${P}ctrl_sweep_v1 $PY scripts/ablate_v2.py --name ${P}ctrl_sweep_v1 --why "$WHY: depth sweep on ctrl_v8 to choose the middle band (7-layer windows sliding by 3)" \
  --plan bands --bands 0-6 3-9 6-12 9-15 12-18 15-21 18-24 21-27 24-30 27-33 30-36 33-39 36-42 39-45 --conditions paper10 paper10_rot \
  --tasks ctrl_v8 --tasks-competence ${P}ctrl_v8_competence_v1 --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 8 || echo "=== sweep FAILED"
MID=$($PY scripts/choose_band.py ${P}ctrl_sweep_v1 "") || MID=""
[ -n "$MID" ] || { MID=24-30; echo "=== no band chosen: the relative-depth band 24-30 instead"; }
echo "=== middle band: $MID"
T2="--tasks full_v8_two --tasks-competence ${P}full_v8_two_competence_v1 --tasks-words PP PM MP MM CP CM --tasks-level all"
K="--n 1000 --kinds clean --batch 8"
BANDS=$(echo "$MID 24-30" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " ")
run ablate_v2/${P}smoke_full_ko_1023 $PY scripts/ablate_v2.py --name ${P}smoke_full_ko_1023 --why smoke --plan bands --bands $MID --conditions paper10 paper10_rot $T2 --n 2 --kinds clean --batch 4 \
  || { echo "smoke failed: stop"; exit 1; }
run ablate_v2/${P}full2_ko_v1 $PY scripts/ablate_v2.py --name ${P}full2_ko_v1 --why "$WHY: C1 at the band and at 24-30" --plan bands --bands $BANDS \
  --conditions paper10 paper10_rot $T2 $K || echo "=== C1 FAILED"
$PY scripts/c1_v2.py ${P}full2_ko_v1 --middle L$MID --set full_v8_two | tail -2
run ablate_v2/${P}full2_ko_unembed_v1 $PY scripts/ablate_v2.py --name ${P}full2_ko_unembed_v1 --why "$WHY: the logit-lens control at the band" --plan bands --bands $MID \
  --conditions unembed10 unembed10_rot $T2 $K || echo "=== logit-lens control FAILED"
run ablate_v2/${P}full2_dose_v1 $PY scripts/ablate_v2.py --name ${P}full2_dose_v1 --why "$WHY: the dose at the band (descriptive)" --plan bands --bands $MID \
  --tasks full_v8_two --tasks-competence ${P}full_v8_two_competence_v1 --tasks-words PP PM MP MM --tasks-level all $K \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top25 top25_rot top50 top50_rot top100 top100_rot || echo "=== dose FAILED"
echo "=== 122B done $(date -u +%FT%TZ)"
