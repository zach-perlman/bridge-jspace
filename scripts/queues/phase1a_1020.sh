#!/usr/bin/env bash
# Phase 1a (Zach, 2026-10-20). (1) paper10's numerical stability: the transit band (32,36,40), TF32 vs fp32, n=100;
# rule (decided): paper10 is the headline knock-out if the two agree on >= 98% of items. (2) The depth sweep:
# 31 three-layer bands sliding by 2, 14 nine-layer bands sliding by 4, every layer 0-62 (paper10 + controls only
# there); omp25 / paper10 with rotated-removal and rotated-dictionary controls; n=100 per family, whole questions.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
W="Zach (2026-10-20), Phase 1a"
F="BL BR RL RR TYPO TRANS R B"
$PY scripts/ablate_v2.py --name paper10_stability_tf32 --plan bands --bands 32,36,40 --conditions paper10 \
  --families $F --kinds clean hop --why "$W: paper10 numerical stability, TF32"; a=$?
$PY scripts/ablate_v2.py --name paper10_stability_fp32 --plan bands --bands 32,36,40 --conditions paper10 --no-tf32 \
  --families $F --kinds clean hop --why "$W: paper10 numerical stability, fp32"; b=$?
$PY scripts/ablate_v2.py --name depth_v1 --plan depth --n 100 --families BL BR RL RR R B --kinds clean \
  --why "$W: where in depth does removing the J-space break each family? (timing confound for C1)"; c=$?
exit $((a + b + c))
