#!/bin/bash
# Zach (2026-10-21): the Qwen3-32B J++ fit after everything else (the Gemma chain's marker), moved out of
# b200_resume_1021.sh when that queue was stopped: the 1-prompt smoke, then qwen3_32b_fit_1020.sh (every layer 0-62).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
until [ -f /workspace/scratch/markers/gemma_chain_done ]; do sleep 120; done
while pgrep -f "scripts/(write_max|ablate_v2)[.]py" >/dev/null || [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -lt 150000 ]; do sleep 60; done
SMOKE=/workspace/scratch/q32_fit_smoke
bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 \
  && $PY scripts/lens_fit/export_jpp_lens.py "$SMOKE/Qwen3-32B_jpp_lens.pt" "$SMOKE/export_check.pt" --note smoke \
  && rm -rf "$SMOKE" && echo "=== fit smoke ok" \
  && bash scripts/queues/qwen3_32b_fit_1020.sh
