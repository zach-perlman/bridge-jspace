#!/bin/bash
# Zach (2026-10-21, decided with Zach): re-test Gemma 4 31B-it (our own J++, target gemma-4-31b-it-refit) with the
# current methods, before the Qwen3-32B measurements. The Oct 20 Gemma tests used one dose only (omp25: 25 atoms at
# 30/33/36, no answer protection) and read_write v1's single lens write (question tokens, sized to the copy).
# Starts after b200_resume_1021.sh and wm2_ctrl_all_1021.sh have ended. Smoke tests first; each step gates the next.
#   1. knock-out dose (ablate_v2): top-K lens directions removed per position with the clean top-10 answer tokens
#      protected (paper10's procedure), K = 1, 2, 5, 10, 25, each with its same-size rotated control, plus omp25 and
#      omp25_rot (the Oct 20 method, as an anchor), at lens layers 24,27 / 30,33,36 (the 27B's L32-40 relative depth)
#      / 39,42,45; suite BL BR RL RR and countries R B, n=100 per family.
#      Rule (fixed before the run): a K is usable only if its rotated control keeps every family within 10 points of
#      unedited; the memory-vs-prompt reading is made at usable K's only.
#   2. write_max v2: lens_add / lens_swap / lens_transpl / dom_add / dom_natural / copy at question, final and all
#      positions, layers 27, 30, 33, 36 (the 27B's band 28-40 relative depth) one at a time and jointly, injection
#      control at layer 24 (the lens's first layer), gated at control keep >= 95%; n=60 per family, write_max's rules.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=gemma-4-31b-it-refit BJ_SUITE_BATCH=64 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -q "^EXIT" $R-resume-1021-0052.log && grep -q "^EXIT" $R-wm2ctrlall-1021-0218.log; do sleep 120; done
until [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 150000 ]; do sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
COMP=gemma4itb_competence_v1
WHY="Zach (2026-10-21): Gemma 4 31B-it re-test with the current methods (own J++)"
DOSE="top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot omp25 omp25_rot"
$PY scripts/ablate_v2.py --name gemma4itr_smoke_dose_1021 --why smoke --plan bands --bands 30,33,36 \
    --conditions top5 top5_rot --n 4 --competence $COMP --countries-build \
  && $PY scripts/write_max.py --name gemma4itr_smoke_wm2_1021 --why smoke --n 2 --layers 30 33 --single-step 1 \
    --early 24 --possets question final --from-competence $COMP \
  && echo "=== smokes ok $(date -u +%FT%TZ)" \
  && $PY scripts/ablate_v2.py --name gemma4itr_dose_v1 --why "$WHY: knock-out dose curve" --plan bands \
    --bands 24,27 30,33,36 39,42,45 --conditions $DOSE --n 100 --competence $COMP --countries-build \
  && $PY scripts/write_max.py --name gemma4itr_wm2_v1 --why "$WHY: write_max v2" --n 60 --layers 27 30 33 36 \
    --single-step 1 --early 24 --from-competence $COMP
