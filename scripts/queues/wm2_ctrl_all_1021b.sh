#!/bin/bash
# Zach (2026-10-21, decided with Zach): write_max v2 on tasks_v2 ctrl_v8 with all four levels pooled (wm2_ctrl_all_v1),
# the primary test of C2-graded (scripts/c2_graded.py). Relaunch of wm2_ctrl_all_1021.sh (cancelled before it ran):
# the level-3 run showed tasks_v2 cases take ~20 s and 133 GB at batch 128, too much next to the replication, so this
# runs at BJ_BATCH=32 and starts only when >= 95 GB has stayed free for 3 checks a minute apart (the replication loaded).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
until [ -f results/write_max/wm2_ctrl_v1/summary.json ] || ! pgrep -f "scripts/write_max[.]py" >/dev/null; do sleep 60; done
sleep 240
ok=0
while [ $ok -lt 3 ]; do
  free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
  if [ "$free" -ge 95000 ]; then ok=$((ok + 1)); else ok=0; fi
  sleep 60
done
echo "=== start $(date -u +%FT%TZ); free MiB $(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits)"
BJ_SUITE_BATCH=32 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True $PY scripts/write_max.py --name wm2_ctrl_all_v1 \
  --why "Zach (2026-10-20), Phase 1d: the strongest fair write (write_max v2), tasks_v2 ctrl_v8, all four levels pooled" \
  --n 1000 --tasks ctrl_v8 --tasks-competence ctrl_v8_competence_v1 --tasks-level all
