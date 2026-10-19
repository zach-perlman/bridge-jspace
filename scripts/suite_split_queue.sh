#!/usr/bin/env bash
# Queued after the 27B wording-A split job: runs only if that job exited 0.
set -euo pipefail
PREV=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-split27b-1019-2127.log
while ! grep -q '^EXIT' "$PREV"; do sleep 30; done
grep -q '^EXIT 0' "$PREV" || { echo "previous job failed; not starting"; exit 1; }
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
P="uv run --no-sync python scripts/suite_split.py"
S="uv run --no-sync python scripts/suite_v1.py"
F="BL BR RL RR BLR BRL NAMES CODE"
WB="Zach (2026-10-19): the same split on wording B, so no result rests on one template"
W9="Zach (2026-10-19): the same split on Qwen3.5-9B (the paper leaves model size open)"
$P manifest_map --name map_B8_v1 --wording B --families $F --why "$WB"
$P run_map --name map_B8_v1
$P manifest_parts --name parts_B8_v1 --map map_B8_v1 --why "$WB"
$P run_parts --name parts_B8_v1
export BJ_TARGET=qwen3.5-9b
$S manifest --set wording_b --name qwen35_9b_competence_b_v1 --why "Zach (2026-10-19): wording B competence on Qwen3.5-9B before its split"
$S competence --name qwen35_9b_competence_b_v1
for w in A B; do
  $P manifest_map --name qwen35_9b_map_${w}8_v1 --wording $w --families $F --why "$W9, wording $w"
  $P run_map --name qwen35_9b_map_${w}8_v1
  $P manifest_parts --name qwen35_9b_parts_${w}8_v1 --map qwen35_9b_map_${w}8_v1 --why "$W9, wording $w"
  $P run_parts --name qwen35_9b_parts_${w}8_v1
done
