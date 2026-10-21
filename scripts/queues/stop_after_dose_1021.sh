#!/usr/bin/env bash
# Zach (2026-10-21 ~00:30 UTC): pause the queue after the dose curve until tasks_v2's three-step questions are fixed.
Q=bridge-cse_01EetL8PM7B9hLWZTfSi7urd-b200all2-1020-2334
cd /workspace/bridge-jspace
while [ ! -f results/ablate_v2/dose_v1/summary.json ]; do
  grep -q "^EXIT" /workspace/runs/$Q.log && { echo "queue ended before the dose curve finished"; exit 1; }
  sleep 5
done
tmux kill-session -t $Q && echo "PAUSED by Zach after dose_v1 at $(date -u +%FT%T): fixing tasks_v2's three-step questions first" >> /workspace/runs/$Q.log
sleep 3
pkill -f "ablate_v2.py --name pos_context_v1" 2>/dev/null
sleep 3
rm -rf results/ablate_v2/pos_context_v1   # started seconds before the pause, if at all: manifest only, no rows
nvidia-smi --query-gpu=memory.used --format=csv,noheader
echo "queue paused $(date -u +%T)"
