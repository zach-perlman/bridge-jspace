#!/usr/bin/env bash
# Phase 1a, coarse first (Zach, 2026-10-20): 14 nine-layer bands sliding by 4 + every layer (paper10 + controls only
# there); omp25 / paper10, rotated-removal and rotated-dictionary controls; n=100 per family, whole questions. The
# full-resolution depth_v1 was stopped at ~7% (6.5 h projected); 3-layer bands follow only where something changes.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
uv run --no-sync python scripts/ablate_v2.py --name depth_coarse_v1 --plan coarse --n 100 --families BL BR RL RR R B \
  --kinds clean --why "Zach (2026-10-20), Phase 1a coarse: where in depth does removing the J-space break each family? (timing confound for C1)"
