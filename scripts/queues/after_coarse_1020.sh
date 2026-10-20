#!/usr/bin/env bash
# Chained after the coarse depth sweep (Zach, 2026-10-20: "Competence + 32B fit"). Neither job depends on its result.
#  1. tasks_v2 competence: smoke on cf_smoke_1020 (240 items with C and O: also tests the new parts), then calib_v2
#     (2,688 items, every word x level, whole question + each step alone): picks each word's level in the 85-95% band
#  2. Qwen3-32B J++: an end-to-end smoke (1 prompt, layers 30-31, scratch dir, deleted after), then the full fit
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
W="Zach (2026-10-20): calibrate each tasks_v2 word's difficulty on the 27B (level = hardest in 85-95%)"
$PY scripts/tasks_v2.py competence --set cf_smoke_1020 --name smoke_cf_competence_1020 --why "smoke" \
  && $PY scripts/tasks_v2.py competence --set calib_v2 --name calib_v2_competence_v1 --why "$W"; a=$?
SMOKE=/workspace/scratch/q32_fit_smoke
bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 \
  && $PY scripts/lens_fit/export_jpp_lens.py "$SMOKE/Qwen3-32B_jpp_lens.pt" "$SMOKE/export_check.pt" --note smoke \
  && rm -rf "$SMOKE" && echo "=== fit smoke ok" \
  && bash scripts/queues/qwen3_32b_fit_1020.sh; b=$?
df -h /workspace | tail -1
exit $((a + b))
