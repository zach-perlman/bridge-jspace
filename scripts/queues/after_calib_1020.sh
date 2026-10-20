#!/usr/bin/env bash
# The queue after tasks calibration (Zach, 2026-10-20, after the coarse depth check-in: the dose curve, the position
# split and name vs digit right after calibration, then the rest of after_coarse_1020.sh in its order; then the
# Phase 1a replication: fresh items, wording B, two more control seeds). Since 23:30 UTC this is the H200's half:
# ctrl_v5 competence, write_max v2 and the Qwen3-32B fit moved to the B200 (scripts/queues/b200_1020.sh). Launched by a
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
df -h /workspace | tail -1
exit $((a + b + c + d + h + i))
