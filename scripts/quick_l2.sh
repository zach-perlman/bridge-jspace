#!/usr/bin/env bash
set -euo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-computed-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 20; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
uv run --no-sync python scripts/twohop_pilot.py competence --name competence_v1 --why "Zach (2026-10-20), quick experiment L2 (Neel: too toy): can the 27B chain natural two-hop facts without chain of thought, from memory and with either fact in the prompt?"
