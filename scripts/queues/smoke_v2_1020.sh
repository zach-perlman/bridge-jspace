#!/usr/bin/env bash
# Smoke tests for ablate_v2 (Zach, 2026-10-20): 2 items per family; v1 check, then the depth plan with all six conditions.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
$PY scripts/ablate_v2.py --name smoke_v1check_1020 --plan v1check --n 2 --conditions omp25 gauss \
  --families BL BR RL RR TYPO TRANS R B --kinds clean hop --why "smoke"; a=$?
$PY scripts/ablate_v2.py --name smoke_depth_1020 --plan depth --n 2 --why "smoke"; b=$?
nvidia-smi --query-gpu=memory.used --format=csv,noheader
exit $((a + b))
