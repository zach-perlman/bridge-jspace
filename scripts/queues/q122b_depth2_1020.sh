#!/usr/bin/env bash
# Rerun of q122b_depth_1020.sh at batch 8 (Zach, 2026-10-20 overnight): qwen35_122b_abl_depth_v1 ran out of GPU memory
# at batch 16 with three layers' dictionaries (manifest only, no results).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=qwen3.5-122b-a10b BJ_BATCH=16 BJ_ABL_BATCH=8
uv run --no-sync python scripts/ablate_pilot.py --name qwen35_122b_abl_depth_v2 --n 100 --layers 24 27 30 \
  --comp-main qwen35_122b_competence_v1 --comp-computed none --comp-tool qwen35_122b_competence_tool_v1 --countries-build \
  --why "Zach (2026-10-20, overnight): the 122B J-space removal at the 27B's relative depth (24/27/30, three layers), as qwen35_122b_abl_v1 otherwise; batch 8 (depth_v1 ran out of memory at 16)"
