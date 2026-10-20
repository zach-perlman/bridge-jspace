#!/usr/bin/env bash
# tasks calibration on calib_v4 (calib_v3 superseded after the second review, never used) (Zach, 2026-10-20). Waits until the set is marked READY (written once it is made,
# reviewed and committed), then a smoke competence on smoke_v4_cf (224 items with C and O: every part, the guess
# prompt included), then calib_v4 (2,688 items, 48 scenes per start group x level). --guess records whether the model
# answers each question with its start made unknown (guessable items are recorded, not dropped).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
while [ ! -f data/tasks_v2/calib_v4/READY ]; do sleep 60; done
echo "=== calib_v4 ready $(date -u +%H:%M:%S)"
W="Zach (2026-10-20): calibrate each tasks_v2 word's difficulty on the 27B (level = hardest in 85-95%), generator v4 (second review)"
$PY scripts/tasks_v2.py competence --set smoke_v4_cf --name smoke_v4_cf_competence --guess --why "smoke" \
  && $PY scripts/tasks_v2.py competence --set calib_v4 --name calib_v4_competence_v1 --guess --why "$W"
