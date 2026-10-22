#!/bin/bash
# Zach (2026-10-22, prereg amendment 6C): the Muse diagnostic on GPU 0 after the 27B's fresh-seed job (memory): a 2-item
# smoke, Muse at L36-42, the 27B at L32-40 as the reference, then the pre-registered reading.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200freshg0-1022-2135.log; do sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
WHY="Zach (2026-10-22, prereg amendment 6C): why Muse's recalls can be steered but not knocked out"
[ -f results/muse_diag/muse30_diag_smoke_1022/summary.json ] || BJ_TARGET=muse-glimmer-30b $PY scripts/muse_diag.py --name muse30_diag_smoke_1022 --why smoke \
  --band 36-42 --n 2 > /workspace/scratch/musediag_smoke.log 2>&1 || { echo "smoke failed: stop"; tail -5 /workspace/scratch/musediag_smoke.log; exit 1; }
echo "=== muse_diag/muse30_diag_v1 $(date -u +%T)"
[ -f results/muse_diag/muse30_diag_v1/summary.json ] || BJ_TARGET=muse-glimmer-30b $PY scripts/muse_diag.py --name muse30_diag_v1 --why "$WHY: Muse, its C1 band" \
  --band 36-42 --n 60 2>&1 | grep "^DIAG" || echo "=== Muse diag FAILED"
echo "=== muse_diag/q27_diag_v1 $(date -u +%T)"
[ -f results/muse_diag/q27_diag_v1/summary.json ] || BJ_TARGET=qwen3.6-27b $PY scripts/muse_diag.py --name q27_diag_v1 --why "$WHY: the 27B as the reference, its C1 band" \
  --band 32-40 --n 60 2>&1 | grep "^DIAG" || echo "=== 27B diag FAILED"
python3 - <<'PY'
import json
m = json.load(open("results/muse_diag/muse30_diag_v1/summary.json"))["by_word"]["all"]
q = json.load(open("results/muse_diag/q27_diag_v1/summary.json"))["by_word"]["all"]
b_m, b_q = m["removed_span"], q["removed_span"]
v = ("the knock-out mostly misses Muse's bridge (reach)" if b_m < 20 and b_q >= 50 else
     "Muse's recall survives removal of its bridge's lens directions (redundant routes)" if b_m >= 50 else "mixed")
print(f"VERDICT (amendment 6C): bridge removed at the question span / final position: Muse {b_m}% / {m['removed_final']}%, "
      f"27B {b_q}% / {q['removed_final']}% -> {v}")
PY
echo "=== Muse diag done $(date -u +%FT%TZ)"
