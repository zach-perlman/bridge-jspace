#!/usr/bin/env bash
# Chained after the coarse depth sweep (Zach, 2026-10-20). Order revised the same evening ("do what's best"): the
# decisive Phase-1 tests on the 27B first, generality (the Qwen3-32B J++ fit) after them.
#  1. tasks calibration on calib_v5 (scripts/queues/calib_v3_competence.sh: smoke on smoke_v5_cf, then calib_v5)
#  2. competence on ctrl_v5 (the controlled counterfactual set for C2: PP PM MP MM, 4 levels, 640 items)
#  3. write_max v2: smoke (2 cases per family, 3 layers), then the suite and countries, then ctrl_v5
#  4. Qwen3-32B J++: an end-to-end smoke (1 prompt, layers 30-31, scratch dir, deleted after), then the full fit
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
W="Zach (2026-10-20), Phase 1d: the strongest fair write (write_max v2: lens, difference-of-means, copy; gated; injection control)"
bash scripts/queues/calib_v3_competence.sh; a=$?
$PY scripts/tasks_v2.py competence --set ctrl_v5 --name ctrl_v5_competence_v1 --guess \
  --why "Zach (2026-10-20): eligibility and the comparison level for write_max on tasks_v2 (C2)"; b=$?
$PY scripts/write_max.py --name smoke_wm2_1020 --why smoke --n 2 --band 34-36 --early 20 --possets question final \
  && $PY scripts/write_max.py --name wm2_suite_v1 --why "$W, suite and countries" --n 60 \
  && $PY scripts/write_max.py --name wm2_ctrl_v1 --why "$W, tasks_v2 ctrl_v5" --n 40 --tasks ctrl_v5 \
       --tasks-competence ctrl_v5_competence_v1; c=$?
SMOKE=/workspace/scratch/q32_fit_smoke
bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 \
  && $PY scripts/lens_fit/export_jpp_lens.py "$SMOKE/Qwen3-32B_jpp_lens.pt" "$SMOKE/export_check.pt" --note smoke \
  && rm -rf "$SMOKE" && echo "=== fit smoke ok" \
  && bash scripts/queues/qwen3_32b_fit_1020.sh; d=$?
df -h /workspace | tail -1
exit $((a + b + c + d))
