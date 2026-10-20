#!/usr/bin/env bash
# Waits for the B200 setup job, runs the gate, then the B200's half of the queue (Zach, 2026-10-20).
SETUP=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-b200setup-1020-2324.log
while ! grep -q "^EXIT" "$SETUP"; do sleep 20; done
grep -q "^EXIT 0" "$SETUP" || { echo "setup failed"; exit 1; }
cd /workspace/bridge-jspace
bash scripts/queues/b200_check_1020.sh && bash scripts/queues/b200_1020.sh
