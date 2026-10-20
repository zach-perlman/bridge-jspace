#!/usr/bin/env bash
# 27B: is the J-space removal's hit on the JSON lookup about the answer being a name? (Zach, 2026-10-20 overnight)
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
uv run --no-sync python scripts/tool_answer_type.py --name v1 --n 150 \
  --why "Zach (2026-10-20, overnight): tool_abl_v1's TBL (name answer) lost 30% under J-space removal, the suite's digit-answer lookups 1%: same JSON scenes, name vs digit answer"
