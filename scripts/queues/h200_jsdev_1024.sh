#!/bin/bash
# Zach (2026-10-24, prereg amendment 29): bands chosen on the jsuite dev split (bridges disjoint from the test split).
# Usage: h200_jsdev_1024.sh GPU STEP ...   dev:TARGET:PREFIX:BATCH:BANDS (comma-separated)   waitq:JOB   mem:GB
# competence (cand2, --hop1 gen) on jsuite_v1_facts_dev_chat, sweep (paper10 / rotated, PP PM MP MM, n 100), choose_band.
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-24, prereg amendment 29)"
DEV=jsuite_v1_facts_dev_chat
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done
      echo "=== GPU $G has $a GB free $(date -u +%T)";;
    dev)
      export BJ_TARGET=$a; p=$b; batch=$c; bands=${d//,/ }; cn=${p}${DEV}_competence_cand2_v1; sw=${p}${DEV}_sweep_cand2_v1
      if [ ! -f results/tasks_v2/$cn/summary.json ]; then
        echo "=== competence $cn $(date -u +%T)"
        $PY scripts/natural_v1.py competence --set $DEV --name $cn --read cand2 --hop1 gen --why "$W: $a on $DEV" > /workspace/scratch/$cn.log 2>&1 \
          || { fail "$a dev competence" /workspace/scratch/$cn.log; continue; }
      fi
      echo "=== ablate_v2/$sw $(date -u +%T)"
      [ -f results/ablate_v2/$sw/summary.json ] || $PY scripts/ablate_v2.py --name $sw --why "$W: $a band sweep on the dev split" --plan bands --bands $bands \
        --conditions paper10 paper10_rot --tasks $DEV --tasks-competence $cn --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean \
        --batch $batch --read cand2 > /workspace/scratch/$sw.log 2>&1 || { fail "$a dev sweep" /workspace/scratch/$sw.log; continue; }
      echo "=== DEVBAND $a: $($PY scripts/choose_band.py $sw 2>/dev/null | tail -1)";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== jsdev GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
