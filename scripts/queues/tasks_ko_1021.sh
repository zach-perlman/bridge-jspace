#!/bin/bash
# Zach (2026-10-21, decided with Zach: v2 replaces v1): the first knock-out on tasks_v2, Qwen3.6-27B. ctrl_v8 (P->P,
# P->M, M->P, M->M; animals, planets, elements, Greek letters; six formats), all four levels, every eligible item;
# paper10 and its rotated control at layers 12-20, 20-28, 32-40 and whole depth (the bands of the v1 replication);
# the whole question and each step alone. Scored by scripts/c1_v2.py (rule fixed in b7100e0 before this ran).
# Batch 16 (tasks_v2 prompts are long; it shares the GPU with wm2_ctrl_all_v1); starts once >= 100 GB stays free.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
ok=0; while [ $ok -lt 3 ]; do
  [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 100000 ] && ok=$((ok + 1)) || ok=0
  sleep 60; done
T="--tasks ctrl_v8 --tasks-competence ctrl_v8_competence_v1 --tasks-words PP PM MP MM --tasks-level all"
$PY scripts/ablate_v2.py --name smoke_tasks_ko_1021 --why smoke --plan bands --bands 32-40 --conditions paper10 paper10_rot \
    $T --n 2 --kinds clean step1 step2 --batch 16 \
  && $PY scripts/ablate_v2.py --name tasks_ko_v1 --why "Zach (2026-10-21): C1 on tasks_v2 (v2 replaces v1), 27B" \
    --plan bands --bands 12-20 20-28 32-40 0-62 --conditions paper10 paper10_rot $T --n 1000 --kinds clean step1 step2 \
    --batch 16 \
  && $PY scripts/c1_v2.py tasks_ko_v1 --middle L32-40
