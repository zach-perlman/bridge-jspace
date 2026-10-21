#!/bin/bash
# Zach (2026-10-21): competence on full_v8b (full_v8 + 192 more three-step items per word) for both models, after the
# 27B two-step runs; the three-step runs use it (per-word eligibility). Then each model's report.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
until grep -q "^EXIT" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-full2x27b-1021-0529.log; do sleep 60; done
WHY="Zach (2026-10-21): competence on full_v8b before the three-step runs"
( BJ_TARGET=gemma-4-31b-it-refit $PY scripts/tasks_v2.py competence --set full_v8b --name gemma4itr_full_v8b_competence_v1 \
    --guess --why "$WHY (Gemma 4 31B-it)" > /workspace/scratch/comp3_gemma.log 2>&1; echo "=== gemma competence exit $?" ) &
$PY scripts/tasks_v2.py competence --set full_v8b --name full_v8b_competence_v1 --guess --why "$WHY (Qwen3.6-27B)" \
  > /workspace/scratch/comp3_27b.log 2>&1; echo "=== 27B competence exit $?"
wait
$PY scripts/competence_full_report.py full_v8b_competence_v1 --set full_v8b
$PY scripts/competence_full_report.py gemma4itr_full_v8b_competence_v1 --set full_v8b
