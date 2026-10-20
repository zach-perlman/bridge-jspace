#!/usr/bin/env bash
# Before the depth sweep (Zach, 2026-10-20): (1) where the lens mostly reads the input token (defines the workspace
# range); (2) the v1 check at n=100 with TF32 and with full fp32 (keep TF32 if every family is within 5 points of v1
# and fp32 does not match v1 better).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
W="Zach (2026-10-20): decisions before the ablate_v2 depth sweep"
$PY scripts/lens_input_identity.py --name input_identity_v1 --n 25 --why "$W: the workspace range"; a=$?
$PY scripts/ablate_v2.py --name v1check_tf32 --plan v1check --n 100 --conditions omp25 gauss \
  --families BL BR RL RR TYPO TRANS R B --kinds clean hop --why "$W: v1 agreement with TF32"; b=$?
$PY scripts/ablate_v2.py --name v1check_fp32 --plan v1check --n 100 --conditions omp25 gauss --no-tf32 \
  --families BL BR RL RR TYPO TRANS R B --kinds clean hop --why "$W: v1 agreement in full fp32"; c=$?
exit $((a + b + c))
