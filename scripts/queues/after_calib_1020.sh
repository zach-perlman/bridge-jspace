#!/usr/bin/env bash
# The queue after tasks calibration (Zach, 2026-10-20, after the coarse depth check-in: the dose curve, the position
# split and name vs digit right after calibration, then the rest of after_coarse_1020.sh in its order; then the
# Phase 1a replication: fresh items, wording B, two more control seeds; then the 32B fit). Launched by a
# watcher that stops after_coarse_1020.sh once calib_v5's competence is written (a running script cannot be edited).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
W="Zach (2026-10-20), Phase 1a follow-up"
F="BL BR RL RR R B"
$PY scripts/ablate_v2.py --name smoke_dose_1020 --why smoke --plan bands --bands 32-40 --conditions top5 top5_rot \
  --families BL R --n 2 --answertype 2 --positions context \
  && $PY scripts/ablate_v2.py --name dose_v1 --plan bands --bands 32-40 12-20 --families $F --n 100 \
       --conditions top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot \
       --why "$W: dose curve (top-K lens directions, answer kept, K = 5-100; rotated controls)"; a=$?
$PY scripts/ablate_v2.py --name pos_context_v1 --plan bands --bands 12-20 20-28 32-40 --conditions paper10 paper10_rot \
  --positions context --families $F --n 100 --why "$W: position split, the facts only (before the question)"; b=$?
$PY scripts/ablate_v2.py --name pos_question_v1 --plan bands --bands 12-20 20-28 32-40 --conditions paper10 paper10_rot \
  --positions question --families $F --n 100 --why "$W: position split, the question and after only"; c=$?
$PY scripts/ablate_v2.py --name answertype_v2 --plan bands --bands 32-40 52-60 --conditions paper10 paper10_rot \
  --families none --answertype 150 --why "Zach (2026-10-20), Phase 1b: name vs digit answers under paper10"; d=$?
$PY scripts/tasks_v2.py competence --set ctrl_v5 --name ctrl_v5_competence_v1 --guess \
  --why "Zach (2026-10-20): eligibility and the comparison level for write_max on tasks_v2 (C2)"; e=$?
WM="Zach (2026-10-20), Phase 1d: the strongest fair write (write_max v2: lens, difference-of-means, copy; gated; injection control)"
$PY scripts/write_max.py --name smoke_wm2_1020 --why smoke --n 2 --band 34-36 --early 20 --possets question final \
  && $PY scripts/write_max.py --name wm2_suite_v1 --why "$WM, suite and countries" --n 60 \
  && $PY scripts/write_max.py --name wm2_ctrl_v1 --why "$WM, tasks_v2 ctrl_v5" --n 40 --tasks ctrl_v5 \
       --tasks-competence ctrl_v5_competence_v1; f=$?
RW="Zach (2026-10-20), Phase 1a replication (before the 32B fit)"
B="12-20 20-28 32-40 0-62"
$PY scripts/ablate_v2.py --name rep_items_v1 --plan bands --bands $B --conditions paper10 paper10_rot --families $F \
  --n 200 --skip 100 --why "$RW: fresh items 101-300 (countries: what is left of map_v1)"; h=$?
$PY scripts/ablate_v2.py --name rep_wordingB_v1 --plan bands --bands $B --conditions paper10 paper10_rot \
  --families BL BR RL RR --n 100 --wording B --why "$RW: the suite's wording B"; i=$?
for s in 1 2; do
  $PY scripts/ablate_v2.py --name rep_seed${s}_v1 --plan bands --bands $B --conditions paper10_rot --families $F \
    --n 100 --seed-offset $s --why "$RW: another draw of the rotated control (seed offset $s)" || i=1
done
SMOKE=/workspace/scratch/q32_fit_smoke
bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 \
  && $PY scripts/lens_fit/export_jpp_lens.py "$SMOKE/Qwen3-32B_jpp_lens.pt" "$SMOKE/export_check.pt" --note smoke \
  && rm -rf "$SMOKE" && echo "=== fit smoke ok" \
  && bash scripts/queues/qwen3_32b_fit_1020.sh; g=$?
df -h /workspace | tail -1
exit $((a + b + c + d + e + f + g + h + i))
