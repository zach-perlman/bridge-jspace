#!/bin/bash
# Zach (2026-10-24, prereg amendment 35): jsuite_v2_1 (v2 + start R, the never-named recall). comp: competence (cand2,
# hop 1 by generation); ko: the 18 facts words at the model's pre-registered band, paper10 / rot / unembed10 / rot, scene
# eligibility, then jsuite2_score (adds RF - MF); pos: the same words with the knock-out only at the question positions
# (paper10, paper10_rot). A copy of h200_v2_1024.sh with the set and words changed (that file is left as it ran).
# Usage: h200_v21_1024.sh GPU STEP ...   waitq:JOB  comp:TARGET:PREFIX:SPLIT[:FRAMING]  ko|pos:TARGET:PREFIX:BAND:BATCH[:FRAMING]
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-24, prereg amendment 35)"
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN RM RA RN"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    comp)
      export BJ_TARGET=$a; p=$b; set_=jsuite_v2_1_${c}_${d:-chat}; cn=${p}${set_}_competence_cand2_v1
      echo "=== competence $cn $(date -u +%T)"
      [ -f results/tasks_v2/$cn/summary.json ] || $PY scripts/natural_v1.py competence --set $set_ --name $cn --read cand2 --hop1 gen \
        --why "$W: $a on $set_" > /workspace/scratch/$cn.log 2>&1 || { fail "$a v2.1 competence" /workspace/scratch/$cn.log; continue; }
      python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== V21COMP $a', {k: round(v['whole'], 2) for k, v in s.items() if len(k.split('/')[0]) == 2})" results/tasks_v2/$cn/summary.json;;
    ko|pos)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; set_=jsuite_v2_1_test_${e:-chat}; cn=${p}${set_}_competence_cand2_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $a $kind: no competence $cn"; fails=$((fails + 1)); continue; }
      if [ $kind = ko ]; then r=${p}${set_}_ko_cand2_v1; extra="--conditions paper10 paper10_rot unembed10 unembed10_rot"
      else r=${p}${set_}_posquestion_v1; extra="--positions question --conditions paper10 paper10_rot"; fi
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, v2.1 facts at L$band ($kind)" --plan bands --bands $band \
        $extra --tasks $set_ --tasks-competence $cn --tasks-words $FACTS \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a v2.1 $kind" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite2_score.py $r --set $set_ --by-relation | grep -E "^facts (paper10|unembed10|paper10_rot) +(start=|half=|never-named)" | sed "s/^/=== V21 $kind $a: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== v2.1 GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
