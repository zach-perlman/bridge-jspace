#!/bin/bash
# Zach (2026-10-21): when Gemma's specificity control is scored (or its queue has moved past it), stop h200_gemma_B3e_1021.sh
# (its wrapper first, so no EXIT line releases the 9B queue) and start h200_gemma_B3g_1021.sh under a name the 9B queue
# still waits for.
set -u
cd /workspace/bridge-jspace
P=bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until [ -f results/ablate_v2/c1_v2/gemma4itf_full2_ko_unembed_v1.json ] || [ -f results/ablate_v2/gemma4itf_full2_ko_keepown_v1/manifest.json ] \
  || grep -qs "unembed knock-out FAILED" /workspace/runs/$P-h200gemmaB3-*.log; do sleep 30; done
sleep 20
J=$(ls /workspace/runs | grep "^$P-h200gemmaB3-.*\.log$" | sed "s/\.log$//" | head -1)
echo "stopping $J at $(date -u +%T): $(tail -n1 /workspace/runs/$J.log | cut -c1-80)"
INNER=$(ps -eo pid,args | grep "[r]un_job_inner.sh $J" | awk '{print $1}')
Q=$(ps -eo pid,ppid,args | awk -v p="$INNER" '$2==p {print $1}')
[ -n "$INNER" ] && kill -9 $INNER
for q in $Q; do for c in $(pgrep -P $q); do pkill -9 -P $c 2>/dev/null; kill -9 $c 2>/dev/null; done; kill -9 $q 2>/dev/null; done
sleep 2
tmux kill-session -t $J 2>/dev/null
mkdir -p /workspace/runs/archive_cancelled && mv /workspace/runs/$J.log /workspace/runs/$J.cmd /workspace/runs/$J.dir /workspace/runs/archive_cancelled/
sleep 5
nvidia-smi --query-gpu=index,memory.used --format=csv,noheader
T=$(date -u +%m%d-%H%M)
/root/run_job.sh $P-h200gemmaB3-$T /workspace/bridge-jspace "bash scripts/queues/h200_gemma_B3g_1021.sh"
echo "started the diagnostic at $(date -u +%T)"
