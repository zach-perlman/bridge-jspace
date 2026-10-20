#!/usr/bin/env bash
set -euo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-ablate-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 15; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
N="uv run --no-sync python scripts/natural_rw.py"
$N --name smoke2_1020 --n 4 --versions MM MX --why "smoke: conflict version"
$N --name v2_conflict --versions MM MX --why "Zach (2026-10-20), cheap experiment N2: v1's prompt version did not force a lookup (the model knows the facts); with the prompt's facts contradicting memory, can the lens write a lookup-used city?"
