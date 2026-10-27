#!/bin/bash
# Zach (2026-10-23, prereg amendment 8b addendum): gpt-oss-20b steering with neuronpedia's plain J-lens, as the J++ steering
# in scripts/queues/h200_gpu1b_1023.sh. GPU 1, alongside it.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1 BJ_TARGET=gpt-oss-20b-jlens
PY="uv run --no-sync python"
P=gptoss20j_
WHY="Zach (2026-10-23, prereg amendment 8b): gpt-oss-20b with neuronpedia's plain J-lens (a labelled comparison lens)"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }
CF=gptoss20_full_v8_competence_v1
W2="--tasks full_v8 --tasks-competence $CF --tasks-level all --families PP PM MP MM CP CM"
run write_max/${P}smoke_wm2_1023 env BJ_SUITE_BATCH=16 $PY scripts/write_max.py --name ${P}smoke_wm2_1023 --why smoke --n 2 --band 12-13 --single-step 1 --early 6 \
  --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
run copy_sweep/${P}copy_sweep_full2_v1 $PY scripts/copy_sweep.py --name ${P}copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $CF --families PP PM MP MM --n 40 --step 1 --window 4
run write_max/${P}wm2_full2_v1 env BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_full2_v1 --why "$WHY: two-step steering at 10-15 (the 27B's 28-40 scaled)" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band 10-15 --single-step 1 --early 4 6 8 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_v1 | tail -3 && $PY scripts/c2_graded.py ${P}wm2_full2_v1 --drop-guessable > /dev/null \
  && $PY scripts/c2_narrow.py ${P}wm2_full2_v1 ${P}wm2_full2_v1_noguess > /dev/null
AB=$($PY scripts/choose_steer_band.py ${P}copy_sweep_full2_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
[ -n "$AB" ] && run write_max/${P}wm2_full2_aligned_v1 env BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_full2_aligned_v1 --why "$WHY: steering at the aligned band ${AB%% *}" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB%% *} --single-step 1 --early 4 6 8 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_aligned_v1 | tail -3
echo "=== gpt-oss J-lens steering done $(date -u +%FT%TZ)"
