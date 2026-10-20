#!/usr/bin/env bash
# Hand-over (Zach, 2026-10-20): when calib_v5's competence summary exists, stop after_coarse_1020.sh (this session's
# own job; it would be starting ctrl_v5's competence) and run after_calib_1020.sh, which holds the revised order.
cd /workspace/bridge-jspace
while [ ! -f results/tasks_v2/calib_v5_competence_v1/summary.json ]; do sleep 15; done
echo "=== calib_v5 competence written $(date -u +%H:%M:%S); stopping bridge-cse_01EetL8PM7B9hLWZTfSi7urd-aftercoarse-1020-2029"
tmux kill-session -t bridge-cse_01EetL8PM7B9hLWZTfSi7urd-aftercoarse-1020-2029 2>/dev/null
sleep 3
pkill -f "tasks_v2.py competence --set ctrl_v5" 2>/dev/null
sleep 5
echo "STOPPED by bridge-cse_01EetL8PM7B9hLWZTfSi7urd-aftercalib-1020-2257 at $(date -u +%Y-%m-%dT%H:%M:%S+00:00): handed over to after_calib_1020.sh (revised order)" >> /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-aftercoarse-1020-2029.log
nvidia-smi --query-gpu=memory.used --format=csv,noheader
bash scripts/queues/after_calib_1020.sh
