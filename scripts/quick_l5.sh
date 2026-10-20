#!/usr/bin/env bash
# Quick experiment L5: Qwen3.5-122B-A10B (FP8) after the 27B quick runs (L3) finish.
set -euo pipefail
PREV=$(ls /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-computed-*.log)
while ! grep -q '^EXIT' "$PREV"; do sleep 20; done
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=qwen3.5-122b-a10b
S="uv run --no-sync python scripts/suite_v1.py"
C="uv run --no-sync python scripts/control_split.py"
P="uv run --no-sync python scripts/suite_split.py"
W="Zach (2026-10-20), quick experiment L5 (Neel: try a larger model early): does the 27B picture hold on Qwen3.5-122B-A10B?"
$S manifest --set main --name qwen35_122b_smoke_1020 --limit 4 --why "smoke: load, generate, read"
$S competence --name qwen35_122b_smoke_1020
$S manifest --set main --name qwen35_122b_competence_v1 --limit 150 --why "$W (competence on the first 150 items per family)"
$S competence --name qwen35_122b_competence_v1
$C manifest_map --name qwen35_122b_map_v1 --n 100 --why "$W (countries: the positive control)"
$C run_map --name qwen35_122b_map_v1
$C manifest_parts --name qwen35_122b_parts_v1 --map qwen35_122b_map_v1 --v3 --why "$W (countries, with the own-word test)"
$C run_parts --name qwen35_122b_parts_v1
$P manifest_map --name qwen35_122b_map_A4_v1 --families BL BR RL RR --scenes 100 --why "$W (the 2x2 core)"
$P run_map --name qwen35_122b_map_A4_v1
$P manifest_parts --name qwen35_122b_parts_A4_v1 --map qwen35_122b_map_A4_v1 --why "$W (the 2x2 core)"
$P run_parts --name qwen35_122b_parts_A4_v1
