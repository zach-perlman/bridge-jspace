#!/usr/bin/env bash
# Single-step J-space removal on natural_rw v3's items, 27B (Zach, 2026-10-20 overnight).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
uv run --no-sync python scripts/natural_hops_ablate.py --name v3_hops_ablate --from v3_lookup \
  --why "Zach (2026-10-20, overnight): J-space removal hurt both natural v3 versions (NM 45%, NL 55%), unlike the suite's RL (99%); does recalling the birth city itself need the J-space?"
