#!/usr/bin/env bash
# Cheap experiments A (9B read/write) and B (wording B read/write), Zach 2026-10-20.
set -euo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
R="uv run --no-sync python scripts/read_write.py"
$R --name wordingB_v1 --n 80 --map map_B8_v1 --wording B --families BL BR RL RR --no-countries --scales 1 2 4 8 --why "Zach (2026-10-20), cheap experiment B: does the RL vs RR read/write gap hold in wording B (27B)?"
BJ_TARGET=qwen3.5-9b $R --name qwen35_9b_rw_v1 --n 80 --map qwen35_9b_map_A8_v1 --families BL BR RL RR --no-countries --layers 16 18 20 --scales 0.5 1 2 4 8 16 --why "Zach (2026-10-20), cheap experiment A: read/write on Qwen3.5-9B at the 27B's relative depth (layers 16-20 of 32)"
