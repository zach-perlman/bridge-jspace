#!/usr/bin/env bash
# Plain-text loss under J-space removal vs a size-matched rotated removal, Gemma and the 27B (Zach, 2026-10-20 overnight).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
W="Zach (2026-10-20, overnight): does J-space removal break the model on plain text (Gemma breaks on every task, lookups too)?"
BJ_TARGET=gemma-4-31b-it-refit uv run --no-sync python scripts/removal_textloss.py --name gemma4itr_textloss_v1 --layers 30 33 36 --why "$W"; a=$?
uv run --no-sync python scripts/removal_textloss.py --name textloss_v1 --layers 32 36 40 --why "$W"; b=$?
exit $((a + b))
