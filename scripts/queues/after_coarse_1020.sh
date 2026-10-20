#!/usr/bin/env bash
# Chained after the coarse depth sweep (Zach, 2026-10-20: "Competence + 32B fit"; then "Fix + swap queue": the
# Qwen3-32B J++ fit first, while the tasks generator is fixed; calibration after it, on calib_v3).
#  1. Qwen3-32B J++: an end-to-end smoke (1 prompt, layers 30-31, scratch dir, deleted after), then the full fit
#  2. tasks calibration: scripts/queues/calib_v3_competence.sh (read only when reached, so it can change until then)
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
SMOKE=/workspace/scratch/q32_fit_smoke
bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 \
  && $PY scripts/lens_fit/export_jpp_lens.py "$SMOKE/Qwen3-32B_jpp_lens.pt" "$SMOKE/export_check.pt" --note smoke \
  && rm -rf "$SMOKE" && echo "=== fit smoke ok" \
  && bash scripts/queues/qwen3_32b_fit_1020.sh; a=$?
bash scripts/queues/calib_v3_competence.sh; b=$?
df -h /workspace | tail -1
exit $((a + b))
