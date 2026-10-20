#!/usr/bin/env bash
# 122B J-space removal at the 27B's relative depth with as many layers (Zach, 2026-10-20 overnight): qwen35_122b_abl_v1
# removed at 36/39 (its copy window, 75-81% of 48 layers) and hurt the recall chains far less than the 27B's run at
# 32/36/40 (50-62% of 64); here 24/27/30 (50-62%), three layers.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=qwen3.5-122b-a10b BJ_BATCH=16
uv run --no-sync python scripts/ablate_pilot.py --name qwen35_122b_abl_depth_v1 --n 100 --layers 24 27 30 \
  --comp-main qwen35_122b_competence_v1 --comp-computed none --comp-tool qwen35_122b_competence_tool_v1 --countries-build \
  --why "Zach (2026-10-20, overnight): the 122B J-space removal at the 27B's relative depth (24/27/30, three layers), as qwen35_122b_abl_v1 otherwise"
