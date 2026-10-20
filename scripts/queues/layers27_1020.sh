#!/usr/bin/env bash
# 27B: is the lookup-used recalled bridge (RL) writable at any depth? dose_v1 steered only at layers 32/36/40 (Zach,
# 2026-10-20 overnight): the same cases and strengths at layers 16-52 (the rest of the stack, every 4th, but the last).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
uv run --no-sync python scripts/read_write.py --name layers_v1 --n 80 --families BL BR RL RR --layers 16 20 24 28 44 48 52 \
  --scales 0.5 1 2 4 8 16 \
  --why "Zach (2026-10-20, overnight): falsification of read-without-write: is RL writable at depths other than 32-40? (as dose_v1, other layers)"
