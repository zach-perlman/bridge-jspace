#!/usr/bin/env bash
set -euo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-readwrite-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 20; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
S="uv run --no-sync python scripts/suite_v1.py"
P="uv run --no-sync python scripts/suite_split.py"
W="Zach (2026-10-20), quick experiment L3 after Neel's feedback: is a computed bridge (never written, not a recalled entity) carried in the J-space, and as its own word?"
$S manifest --set computed --name competence_computed_v1 --why "$W (competence first)"
$S competence --name competence_computed_v1
$P manifest_map --name map_C3_v1 --wording C --families ARITH TYPO TRANS --why "$W"
$P run_map --name map_C3_v1
$P manifest_parts --name parts_C3_cal_v1 --map map_C3_v1 --calibrate --why "$W"
$P run_parts --name parts_C3_cal_v1
