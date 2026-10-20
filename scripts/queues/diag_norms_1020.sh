#!/usr/bin/env bash
# Removal diagnostic on Gemma (own lens) and the 27B, at each one's removal layers (Zach, 2026-10-20 overnight).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
W="Zach (2026-10-20, overnight): why does J-space (and random-dictionary) removal break Gemma 4 31B-it but not Qwen3.6-27B?"
BJ_TARGET=gemma-4-31b-it-refit uv run --no-sync python scripts/removal_norms.py --name gemma4itr_norms_v1 --layers 30 33 36 --why "$W"; a=$?
uv run --no-sync python scripts/removal_norms.py --name norms_v1 --layers 32 36 40 --why "$W"; b=$?
exit $((a + b))
