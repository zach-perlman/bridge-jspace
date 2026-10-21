#!/bin/bash
# Zach (2026-10-21): does the current knock-out (top-K lens directions) break Gemma on plain text, as the 25-atom one
# did (7.66 -> 18.48 nats)? Gemma 4 31B-it with the layers 24-45 lens at 30/33/36 (the Oct 20 setting) and the 27B at
# 32/36/40 for comparison: none, the old removal and its rotated control, top-1/5/10 and their rotated controls, every
# position, nothing protected. After the competence job; shares the GPU with steering once >= 80 GB stays free.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
until grep -q "^EXIT" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-compboth-1021-0445.log; do sleep 60; done
ok=0; while [ $ok -lt 3 ]; do
  [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 80000 ] && ok=$((ok + 1)) || ok=0
  sleep 30; done
C="none jspace rotated top1 top1_rot top5 top5_rot top10 top10_rot"
WHY="Zach (2026-10-21): plain-text loss under the current knock-out (top-K) vs the 25-atom one"
BJ_TARGET=gemma-4-31b-it-refit $PY scripts/removal_textloss.py --name gemma4itr_textloss_top_v1 --why "$WHY (Gemma)" \
  --layers 30 33 36 --conditions $C
$PY scripts/removal_textloss.py --name textloss_top_v1 --why "$WHY (27B)" --layers 32 36 40 --conditions $C
