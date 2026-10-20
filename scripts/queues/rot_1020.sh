#!/usr/bin/env bash
# Size-matched control for the J-space removal (Zach, 2026-10-20 overnight). removal_norms on Gemma: residuals are 92-97%
# a few massive coordinates; the random-dictionary fit removes ~28% of the norm (about all the rest), the J-space fit
# 0.2-0.9%. The rotated control removes the J-space fit turned by a random rotation: the same size, a random direction.
# Rule for Gemma (fixed now): if the rotated control keeps every family/step within 10 points of unedited, the J-space
# minus rotated difference is Gemma's removal result; otherwise none.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
FAILED=0
step() { echo "=== STEP $1 $(date -u +%H:%M:%S)"; shift; "$@" || { echo "=== FAILED (exit $?)"; FAILED=$((FAILED + 1)); }; }
PY="uv run --no-sync python"
W="Zach (2026-10-20, overnight): why does J-space (and random-dictionary) removal break Gemma 4 31B-it but not Qwen3.6-27B? (rows of 32+ tokens; norms_v1 failed on empty WikiText rows)"
step "norms 27B" $PY scripts/removal_norms.py --name norms_v2 --layers 32 36 40 --why "$W"
step "norms gemma" env BJ_TARGET=gemma-4-31b-it-refit $PY scripts/removal_norms.py --name gemma4itr_norms_v2 --layers 30 33 36 --why "$W"
WR="Zach (2026-10-20, overnight): J-space removal against a size-matched control (the J-space fit turned by a random rotation)"
step "gemma rotated" env BJ_TARGET=gemma-4-31b-it-refit $PY scripts/ablate_pilot.py --name gemma4itr_abl_rot_v1 --n 50 \
  --layers 30 33 36 --rotated --comp-main gemma4itb_competence_v1 --comp-computed gemma4itb_competence_computed_v1 \
  --countries-build --why "$WR, Gemma own lens; cases from gemma4itb competence runs (same model and revision)"
step "27B rotated" $PY scripts/ablate_pilot.py --name abl_rot_v1 --n 100 --rotated --why "$WR, 27B (as v1 plus the rotated condition)"
echo "=== QUEUE DONE failed=$FAILED"
exit $FAILED
