#!/bin/bash
# Zach (2026-10-21): competence on the full v8 set for both models before any steering or knock-out ("competence ->
# steer -> knockout"). Qwen3.6-27B and Gemma 4 31B-it in parallel (competence needs no lens; Gemma runs under its
# gemma-4-31b-it-refit target, prefix gemma4itr_); then scripts/competence_full_report.py for each.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
WHY="Zach (2026-10-21): competence on the full v8 set before steering and the knock-out"
( BJ_TARGET=gemma-4-31b-it-refit $PY scripts/tasks_v2.py competence --set full_v8 --name gemma4itr_full_v8_competence_v1 \
    --guess --why "$WHY (Gemma 4 31B-it)" > /workspace/scratch/comp_gemma.log 2>&1; echo "=== gemma competence exit $?" ) &
$PY scripts/tasks_v2.py competence --set full_v8 --name full_v8_competence_v1 --guess --why "$WHY (Qwen3.6-27B)" \
  > /workspace/scratch/comp_27b.log 2>&1; echo "=== 27B competence exit $?"
wait
$PY scripts/competence_full_report.py full_v8_competence_v1
$PY scripts/competence_full_report.py gemma4itr_full_v8_competence_v1
