#!/bin/bash
# Zach (2026-10-21): set up the 2x H200 NVL box after the B200 went down, and gate it before resuming. Environment from
# uv.lock (torch 2.11.0+cu128, transformers 5.17.0, fla 0.5.2), without causal-conv1d (built for the B200 only; the
# models fall back to their torch convolution, as on the first H200). Gate (the B200 gate's rule: >= 97% item
# agreement): ctrl_v8 competence vs the B200's ctrl_v8_competence_v1, and a small knock-out (3 items per word of
# full_v8, layers 32-40 and whole depth, paper10 / rotated / top5) vs the B200's pad_check_exact_1021. GPU 0 only.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache CUDA_VISIBLE_DEVICES=0
until grep -q "^EXIT" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-download-1021-1627.log && grep -q "^EXIT" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-jppenv-1021-1633.log; do sleep 30; done
echo "=== env $(date -u +%T)"
rm -rf .venv && uv sync > /workspace/scratch/uv_sync.log 2>&1 || { echo "uv sync failed"; tail -20 /workspace/scratch/uv_sync.log; exit 1; }
.venv/bin/python -c "import torch, fla, transformers; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0), 'fla', fla.__version__, 'transformers', transformers.__version__)"
.venv/bin/python -m pytest -q tests/test_ablate.py 2>&1 | tail -2
PY="uv run --no-sync python"
echo "=== gate: competence $(date -u +%T)"
$PY scripts/tasks_v2.py competence --set ctrl_v8 --name h200x2_gate_ctrl_v8_competence --guess \
  --why "Zach (2026-10-21): gate of the 2x H200 NVL box against the B200 (ctrl_v8_competence_v1)" > /workspace/scratch/gate_comp.log 2>&1
$PY scripts/gate_compare.py competence h200x2_gate_ctrl_v8_competence ctrl_v8_competence_v1; c=$?
echo "=== gate: knock-out $(date -u +%T)"
$PY scripts/ablate_v2.py --name h200x2_gate_ko --why "Zach (2026-10-21): gate of the 2x H200 NVL box against the B200 (pad_check_exact_1021)" \
  --plan bands --bands 32-40 0-62 --conditions paper10 paper10_rot top5 --tasks full_v8 --tasks-competence full_v8_competence_v1 \
  --tasks-words PP PM MP MM CP CM PPP PPM PMP MPP MPM MMP --tasks-level all --tasks-strata core secondary --n 3 \
  --kinds clean step1 --batch 32 > /workspace/scratch/gate_ko.log 2>&1
$PY scripts/gate_compare.py ablate h200x2_gate_ko pad_check_exact_1021; k=$?
[ $c -eq 0 ] && [ $k -eq 0 ] && echo "=== GATE PASSED $(date -u +%T)" || { echo "=== GATE FAILED"; exit 1; }
