#!/bin/bash
# Zach (2026-10-21, decided with Zach): write_max v2 on tasks_v2 ctrl_v8 with all four levels pooled (wm2_ctrl_all_v1),
# added next to b200_resume_1021.sh. The queued wm2_ctrl_v1 compares at level 3 only (24 M->P / 24 M->M cases, ~70%
# with a dom direction); every ctrl_v8 word is >= 85% at every level and M->P / M->M share scenes (same level and domain
# mix), so pooling levels keeps the comparison matched: 476 cases (130 P->P / P->M, 108 M->P / M->M), ~90% with dom.
# Starts after the queue's write_max runs end (wm2_ctrl_v1 written, or no write_max process left) and >= 120 GB free.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
until [ -f results/write_max/wm2_ctrl_v1/summary.json ] || ! pgrep -f "scripts/write_max[.]py" >/dev/null; do sleep 60; done
sleep 30
until [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 120000 ]; do sleep 60; done
echo "=== start $(date -u +%FT%TZ); free MiB $(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits)"
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True $PY scripts/write_max.py --name wm2_ctrl_all_v1 \
  --why "Zach (2026-10-20), Phase 1d: the strongest fair write (write_max v2), tasks_v2 ctrl_v8, all four levels pooled" \
  --n 1000 --tasks ctrl_v8 --tasks-competence ctrl_v8_competence_v1 --tasks-level all
