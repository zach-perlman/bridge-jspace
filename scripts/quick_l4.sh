#!/usr/bin/env bash
set -euo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-calib-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 20; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
R="uv run --no-sync python scripts/read_write.py"
$R --name smoke_1020 --n 3 --why "smoke"
$R --name v1 --why "Zach (2026-10-20), quick experiment L4: does the J-lens read the bridge where the model carries it, and can its direction write it (suite and countries)?"
