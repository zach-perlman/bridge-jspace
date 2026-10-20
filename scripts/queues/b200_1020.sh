#!/usr/bin/env bash
# The B200's half of the queue (Zach, 2026-10-20 ~23:30 UTC: "switch to the B200"; the H200 finishes calibration and
# the Phase 1a follow-ups, the B200 takes the rest): ctrl_v5 competence, write_max v2 (smoke, suite and countries,
# ctrl_v5), then the Qwen3-32B J++ fit (smoke, full). Runs after the B200 environment check (b200_check_1020.sh).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
$PY scripts/tasks_v2.py competence --set ctrl_v5 --name ctrl_v5_competence_v1 --guess \
  --why "Zach (2026-10-20): eligibility and the comparison level for write_max on tasks_v2 (C2)"; e=$?
WM="Zach (2026-10-20), Phase 1d: the strongest fair write (write_max v2: lens, difference-of-means, copy; gated; injection control)"
$PY scripts/write_max.py --name smoke_wm2_1020 --why smoke --n 2 --band 34-36 --early 20 --possets question final \
  && $PY scripts/write_max.py --name wm2_suite_v1 --why "$WM, suite and countries" --n 60 \
  && $PY scripts/write_max.py --name wm2_ctrl_v1 --why "$WM, tasks_v2 ctrl_v5" --n 40 --tasks ctrl_v5 \
       --tasks-competence ctrl_v5_competence_v1; f=$?
SMOKE=/workspace/scratch/q32_fit_smoke
bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 \
  && $PY scripts/lens_fit/export_jpp_lens.py "$SMOKE/Qwen3-32B_jpp_lens.pt" "$SMOKE/export_check.pt" --note smoke \
  && rm -rf "$SMOKE" && echo "=== fit smoke ok" \
  && bash scripts/queues/qwen3_32b_fit_1020.sh; g=$?
df -h /workspace | tail -1
exit $((e + f + g))
