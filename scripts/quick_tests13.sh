#!/usr/bin/env bash
# Tests 1 and 3 (Zach, 2026-10-20) and the TwoHopFact screening for Day 1.
set -euo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
R="uv run --no-sync python scripts/read_write.py"
W1="Zach (2026-10-20), test 1: steering strength sweep; is RL unwritable at any strength, or only at the ones tried?"
$R --name smoke_dose_1020 --n 2 --families BL BR RL RR --scales 0.5 1 2 4 8 16 --why "smoke"
$R --name dose_v1 --n 80 --families BL BR RL RR --scales 0.5 1 2 4 8 16 --why "$W1"
uv run --no-sync python scripts/twohop_pilot.py competence --screen --name screen_v1 --why "Zach (2026-10-20): screen TwoHopFact (5 types, 2,479 rows) for facts the 27B knows, for Day 1's natural memory-vs-prompt set"
export BJ_TARGET=qwen3.5-122b-a10b BJ_BATCH=16
W3="Zach (2026-10-20), test 3: does read without write survive on Qwen3.5-122B-A10B? (layers 36 and 39, its window)"
$R --name qwen35_122b_smoke_rw_1020 --n 2 --map qwen35_122b_map_A4_v1 --country-map qwen35_122b_map_v1 --families BL BR RL RR --layers 36 39 --scales 1 4 16 --why "smoke"
$R --name qwen35_122b_rw_v1 --n 60 --map qwen35_122b_map_A4_v1 --country-map qwen35_122b_map_v1 --families BL BR RL RR --layers 36 39 --scales 0.5 1 2 4 8 16 --why "$W3"
