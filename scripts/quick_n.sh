#!/usr/bin/env bash
set -euo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-cheapab-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 15; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
N="uv run --no-sync python scripts/natural_rw.py"
$N --name smoke_1020 --n 4 --why "smoke"
$N --name v1 --why "Zach (2026-10-20), cheap experiment N: does read without write appear on natural facts (country of a person's birth city: recalled vs read from the prompt)?"
