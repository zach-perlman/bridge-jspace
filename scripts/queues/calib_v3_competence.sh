#!/usr/bin/env bash
# tasks calibration on calib_v3 (Zach, 2026-10-20). Waits until the set is marked READY (written after it is made,
# checked and committed), then a smoke competence on a small v3 set, then calib_v3.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
while [ ! -f data/tasks_v2/calib_v3/READY ]; do sleep 60; done
echo "=== calib_v3 ready $(date -u +%H:%M:%S)"
echo "(placeholder: the competence commands are filled in once calib_v3 exists)"
exit 1
