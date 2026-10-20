#!/usr/bin/env bash
set -euo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-natrw-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 15; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
A="uv run --no-sync python scripts/ablate_pilot.py"
$A --name smoke_1020 --n 2 --why "smoke"
$A --name v1 --n 100 --why "Zach (2026-10-20), cheap experiment: the paper's kind of test (remove the J-space at layers 32-40): do recall chains break more than lookup chains?"
