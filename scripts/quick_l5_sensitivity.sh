#!/usr/bin/env bash
# L5 sensitivity: the 122B's parts with the window's upper layer at 42 (just below where its last token alone carries
# the answer, layer 42 in qwen35_122b_map_v1) instead of the 27B's relative depth (33). Chosen after seeing that map.
set -euo pipefail
PREV=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-l5sens-1020-0154.log
while ! grep -q '^EXIT' "$PREV"; do sleep 20; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=qwen3.5-122b-a10b BJ_BATCH=16
C="uv run --no-sync python scripts/control_split.py"
P="uv run --no-sync python scripts/suite_split.py"
W="Zach (2026-10-20), L5 sensitivity (chosen after the 122B map): windows up to layer 41, below the 122B's last-token answer layer (42), instead of the 27B's relative depth (33)"
$C manifest_parts --name qwen35_122b_parts_cap42_v2 --map qwen35_122b_map_v1 --v3 --cap 42 --why "$W"
$C run_parts --name qwen35_122b_parts_cap42_v2
$P manifest_parts --name qwen35_122b_parts_A4_cap42_v1 --map qwen35_122b_map_A4_v1 --cap 42 --why "$W"
$P run_parts --name qwen35_122b_parts_A4_cap42_v1
