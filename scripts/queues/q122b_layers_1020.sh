#!/usr/bin/env bash
# 122B: does the 27B layer sweep's picture hold (lookup bridge written only by hard early pushes, not in transit)?
# As qwen35_122b_rw_v1 (same cases and strengths) at layers 12/18/24/30/42/45 (Zach, 2026-10-20 overnight).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=qwen3.5-122b-a10b BJ_SUITE_BATCH=16
uv run --no-sync python scripts/read_write.py --name qwen35_122b_layers_v1 --n 60 --map qwen35_122b_map_A4_v1 \
  --country-map qwen35_122b_map_v1 --families BL BR RL RR --layers 12 18 24 30 42 45 --scales 0.5 1 2 4 8 16 \
  --why "Zach (2026-10-20, overnight): the 27B layer sweep (layers_v1) on the 122B: is RL written only by strong early pushes? (as qwen35_122b_rw_v1, other layers)"
