#!/bin/bash
# Zach (2026-10-23, prereg amendment 7). Usage: h200_amend7_1023.sh GPU STEP [STEP ...]
#   steps: q9s3 (the 9B on fresh_v8s3 at L12-16), olmoh (Olmo-Hybrid on olmo_big_v8 at L4-8 and 12-16),
#          olmo3 (Olmo-3 on olmo_big_v8 at L10-14 and 12-16). Each: competence, smoke, C1 (paper10, paper10_rot), c1_v2.
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
. scripts/queues/lib_competence_parallel.sh
K="--n 1000 --kinds clean --batch 32"
run_set() {  # run_set TARGET PREFIX SET RUN MID "BANDS" WORDS
  export BJ_TARGET=$1; local p=$2 set=$3 run=$4 mid=$5 bands=$6 words=$7 c=${2}${3}_competence_v1
  local why="Zach (2026-10-23, prereg amendment 7): $1 on $set"
  echo "=== $1 on $set $(date -u +%T)"
  comp_parallel 2 "$why" $c:$set || { echo "=== $1 competence FAILED"; return 1; }
  local T="--tasks $set --tasks-competence $c --tasks-words $words --tasks-level all"
  $PY scripts/ablate_v2.py --name ${p}${run}_smoke_1023 --why smoke --plan bands --bands $mid --conditions paper10 paper10_rot $T \
    --n 2 --kinds clean --batch 16 > /workspace/scratch/${p}${run}_smoke.log 2>&1 || { echo "=== $1 smoke failed"; tail -5 /workspace/scratch/${p}${run}_smoke.log; return 1; }
  echo "=== ablate_v2/${p}${run} $(date -u +%T)"
  $PY scripts/ablate_v2.py --name ${p}${run} --why "$why: C1 at the fixed band L$mid" --plan bands --bands $bands \
    --conditions paper10 paper10_rot $T $K && $PY scripts/c1_v2.py ${p}${run} --middle L$mid --set $set | tail -2 || echo "=== $1 C1 FAILED"
}
for step in "$@"; do
  case $step in
    q9s3) run_set qwen3.5-9b qwen35_9b_ fresh_v8s3 fresh3_ko_v1 12-16 "12-16" "PP PM MP MM CP CM";;
    olmoh) run_set olmo-hybrid-7b olmoh7_ olmo_big_v8 big2_ko_v1 4-8 "4-8 12-16" "PP PM MP MM";;
    olmo3) run_set olmo-3-7b olmo3d7_ olmo_big_v8 big2_ko_v1 10-14 "10-14 12-16" "PP PM MP MM";;
  esac
done
echo "=== amendment 7 GPU $G done $(date -u +%FT%TZ)"
