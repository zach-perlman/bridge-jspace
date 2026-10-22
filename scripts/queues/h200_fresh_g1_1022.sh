#!/bin/bash
# Zach (2026-10-22, prereg amendment 6A/6D): GPU 1, after the 9B knock-outs (h200q9B6). The 9B and Qwen3-32B on the fresh
# data seed (fresh_v8s2) at their fixed bands; the 9B's removal size (and the share-matched logit-lens control if its J++
# top-10 takes > 1.2x the logit-lens top-10's share) and its dose at L12-16 (descriptive).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200q9B6-1022-0228.log; do sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
TWO="PP PM MP MM CP CM"
K="--n 1000 --kinds clean --batch 32"
fresh() {  # fresh TARGET PREFIX BAND
  export BJ_TARGET=$1; local p=$2 b=$3 c=${2}fresh_v8s2_competence_v1
  local why="Zach (2026-10-22, prereg amendment 6A): $1 on a fresh data seed (fresh_v8s2)"
  if [ ! -f results/tasks_v2/$c/summary.json ]; then
    echo "=== competence $c $(date -u +%T)"
    $PY scripts/tasks_v2.py competence --set fresh_v8s2 --name $c --guess --why "$why: competence" > /workspace/scratch/$c.log 2>&1 \
      && $PY scripts/competence_full_report.py $c | tail -8 || { echo "=== $1 competence FAILED"; tail -5 /workspace/scratch/$c.log; return 1; }
  fi
  local T="--tasks fresh_v8s2 --tasks-competence $c --tasks-words $TWO --tasks-level all"
  $PY scripts/ablate_v2.py --name ${p}fresh2_smoke_1022 --why smoke --plan bands --bands $b --conditions paper10 paper10_rot $T \
    --n 2 --kinds clean --batch 16 > /workspace/scratch/${p}fresh2_smoke.log 2>&1 || { echo "=== $1 smoke failed"; tail -5 /workspace/scratch/${p}fresh2_smoke.log; return 1; }
  echo "=== ablate_v2/${p}fresh2_ko_v1 $(date -u +%T)"
  $PY scripts/ablate_v2.py --name ${p}fresh2_ko_v1 --why "$why: C1 at the fixed band L$b" --plan bands --bands $b \
    --conditions paper10 paper10_rot $T $K \
    && $PY scripts/c1_v2.py ${p}fresh2_ko_v1 --middle L$b --set fresh_v8s2 | tail -2 || echo "=== $1 fresh C1 FAILED"
}
fresh qwen3.5-9b qwen35_9b_ 12-16
export BJ_TARGET=qwen3.5-9b
W9="Zach (2026-10-22, prereg amendment 6D): the 9B"
echo "=== removal_size/qwen35_9b_removal_size_v1 $(date -u +%T)"
[ -f results/removal_size/qwen35_9b_removal_size_v1/summary.json ] || $PY scripts/removal_size.py --name qwen35_9b_removal_size_v1 \
  --why "$W9: residual share removed by J++ vs logit-lens top-K at L12-16" --layers 12 13 14 15 16 --ks 1 10 20 30 40 50 || echo "=== removal size FAILED"
KM=$(python3 - <<'PY'
import json, statistics
d = json.load(open("results/removal_size/qwen35_9b_removal_size_v1/summary.json"))["median_share"]
j = statistics.mean(v["jlens_top10"] for v in d.values()); u = statistics.mean(v["unembed_top10"] for v in d.values())
ks = [int(k.split("top")[1]) for k in next(iter(d.values())) if k.startswith("unembed_top")]
best = min(ks, key=lambda k: abs(statistics.mean(v[f"unembed_top{k}"] for v in d.values()) - j))
print(best if j > 1.2 * u else 0)
PY
)
echo "=== J++ top-10 vs logit-lens share: matched K = ${KM:-?} (0 = within 1.2x, no extra control)"
if [ -n "$KM" ] && [ "$KM" != 0 ] && [ "$KM" != 10 ]; then
  echo "=== ablate_v2/qwen35_9b_full2_ko_unembed_sized_v1 $(date -u +%T)"
  $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_unembed_sized_v1 --why "$W9: the logit-lens control matched in residual share (unembed$KM)" \
    --plan bands --bands 12-16 --conditions unembed$KM unembed${KM}_rot --tasks full_v8 --tasks-competence qwen35_9b_full_v8_competence_v1 \
    --tasks-words $TWO --tasks-level all $K && $PY scripts/c1_v2.py qwen35_9b_full2_ko_unembed_sized_v1 --middle L12-16 --set full_v8 > /dev/null \
    || echo "=== 9B size-matched FAILED"
fi
echo "=== ablate_v2/qwen35_9b_full2_dose_v1 $(date -u +%T)"
$PY scripts/ablate_v2.py --name qwen35_9b_full2_dose_v1 --why "$W9: the dose at L12-16 (descriptive)" --plan bands --bands 12-16 \
  --tasks full_v8 --tasks-competence qwen35_9b_full_v8_competence_v1 --tasks-words PP PM MP MM --tasks-level all $K \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top25 top25_rot top50 top50_rot top100 top100_rot || echo "=== 9B dose FAILED"
fresh qwen3-32b qwen3_32b_ 44-52
echo "=== GPU 1 fresh done $(date -u +%FT%TZ)"
