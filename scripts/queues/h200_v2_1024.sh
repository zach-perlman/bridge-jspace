#!/bin/bash
# Zach (2026-10-24, prereg amendment 33): the combined suite v2 (jsuite_v2) on the 9B and the 27B. comp: competence
# (cand2, hop 1 by generation) on a split and framing; ko: the facts words (15) on the test split at the model's
# pre-registered band, paper10 / rot / unembed10 / rot, scene eligibility, then jsuite2_score (per start, half, relation).
# Usage: h200_v2_1024.sh GPU STEP ...   waitq:JOB  mem:GB  comp:TARGET:PREFIX:SPLIT[:FRAMING]  ko:TARGET:PREFIX:BAND:BATCH[:FRAMING]
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-24, prereg amendment 33)"
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done
      echo "=== GPU $G has $a GB free $(date -u +%T)";;
    comp)
      export BJ_TARGET=$a; p=$b; set_=jsuite_v2_${c}_${d:-chat}; cn=${p}${set_}_competence_cand2_v1
      echo "=== competence $cn $(date -u +%T)"
      [ -f results/tasks_v2/$cn/summary.json ] || $PY scripts/natural_v1.py competence --set $set_ --name $cn --read cand2 --hop1 gen \
        --why "$W: $a on $set_" > /workspace/scratch/$cn.log 2>&1 || { fail "$a v2 competence" /workspace/scratch/$cn.log; continue; }
      python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== V2COMP $a', {k: round(v['whole'], 2) for k, v in s.items() if len(k.split('/')[0]) == 2})" results/tasks_v2/$cn/summary.json;;
    ko)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; set_=jsuite_v2_test_${e:-chat}; cn=${p}${set_}_competence_cand2_v1; r=${p}${set_}_ko_cand2_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $a ko: no competence $cn"; fails=$((fails + 1)); continue; }
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, v2 facts at L$band" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $set_ --tasks-competence $cn --tasks-words $FACTS \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a v2 KO" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite2_score.py $r --set $set_ --by-relation | grep -E "^facts (paper10|unembed10|paper10_rot) +(start|half)=" | sed "s/^/=== V2 $a: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== v2 GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
