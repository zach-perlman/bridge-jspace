#!/bin/bash
# Zach (2026-10-21): validate ablate_v2 --pad on the 27B before the Gemma knock-out uses it (scripts/pad_check.py, rule
# fixed there). The same small knock-out twice, exact-length and padded batches: 12 items per word of the full v8 set,
# whole question and step 1, layers 32-40 and whole depth, paper10 / its rotated control / top5. Runs once >= 75 GB
# stays free (after the 27B steering). Accepted -> /workspace/scratch/markers/pad_validated, which the Gemma job reads.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
ok=0; while [ $ok -lt 3 ]; do
  [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 75000 ] && ok=$((ok + 1)) || ok=0
  sleep 30; done
A="--plan bands --bands 32-40 0-62 --conditions paper10 paper10_rot top5 --tasks full_v8 --tasks-competence full_v8_competence_v1
   --tasks-words PP PM MP MM CP CM PPP PPM PMP MPP MPM MMP --tasks-level all --tasks-strata core secondary --n 12
   --kinds clean step1 --batch 32"
$PY scripts/ablate_v2.py --name pad_check_exact_1021 --why "padding check: exact-length batches" $A \
  && $PY scripts/ablate_v2.py --name pad_check_padded_1021 --why "padding check: padded batches" $A --pad \
  && $PY scripts/pad_check.py pad_check_exact_1021 pad_check_padded_1021 \
  && mkdir -p /workspace/scratch/markers && touch /workspace/scratch/markers/pad_validated && echo "=== padding ACCEPTED" \
  || echo "=== padding NOT accepted (or the check failed): the Gemma runs keep exact-length batches"
