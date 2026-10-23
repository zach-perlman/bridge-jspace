#!/bin/bash
# Zach (2026-10-23, prereg amendment 10). Usage: h200_amend10_1023.sh GPU STEP [STEP ...]
#   A (bridge absent): mm9 / mm27 / mmmuse / mm122: competence on full_v8_mmabs, then the knock-out at the model's fixed
#   band(s), M->M only. waitmem MB: wait for that much free memory on this GPU. waitq JOB: wait for a job log's EXIT.
#   B (natural pilot): nat TARGET PREFIX FRAMING BAND BATCH (added when natural_v1 is built).
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
. scripts/queues/lib_competence_parallel.sh
WHY="Zach (2026-10-23, prereg amendment 10)"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }

mm() {  # mm TARGET PREFIX "BANDS" BATCH
  export BJ_TARGET=$1; local p=$2 bands=$3 batch=$4 c=${2}full_v8_mmabs_competence_v1
  comp_parallel 1 "$WHY: $1, M->M with the bridge absent from the context" $c:full_v8_mmabs || { echo "=== $1 mmabs competence FAILED"; return 1; }
  run ablate_v2/${p}mmabs_ko_v1 $PY scripts/ablate_v2.py --name ${p}mmabs_ko_v1 --why "$WHY: $1, M->M with the bridge absent, knock-out at $bands" \
    --plan bands --bands $bands --conditions paper10 paper10_rot --tasks full_v8_mmabs --tasks-competence $c --tasks-words MM \
    --tasks-level all --n 1000 --kinds clean --batch $batch > /workspace/scratch/${p}mmabs_ko_v1.log 2>&1 || { echo "=== $1 mmabs knock-out FAILED"; tail -3 /workspace/scratch/${p}mmabs_ko_v1.log; }
}

for step in "$@"; do
  case $step in
    waitmem:*) want=${step#waitmem:}
      until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge "$want" ]; do sleep 30; done
      echo "=== GPU $G has >= $want MiB free $(date -u +%T)";;
    waitq:*) j=${step#waitq:}
      until grep -qs "^EXIT" $R-$j.log; do sleep 60; done; echo "=== $j finished $(date -u +%T)";;
    mm9) mm qwen3.5-9b qwen35_9b_ "12-16" 32;;
    mm27) mm qwen3.6-27b "" "32-40" 16;;
    mmmuse) mm muse-glimmer-30b muse30_ "36-42" 32;;
    mm122) mm qwen3.5-122b-a10b qwen35_122b_ "39-45 24-30" 8;;
  esac
done
echo "=== amendment 10 GPU $G done $(date -u +%FT%TZ)"
