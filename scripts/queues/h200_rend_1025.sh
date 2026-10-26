#!/bin/bash
# Zach (2026-10-25, prereg amendment 38 B): a further rendering of v2's facts (same split and halves, new passages):
# competence on the 15 facts words (cand2, hop 1 by generation), the facts knock-out (paper10 / rot / unembed10 / rot)
# at the model's band, jsuite2_score.
# Usage: h200_rend_1025.sh GPU STEP ...   waitq:JOB  rend:TARGET:PREFIX:BAND:BATCH:SETNAME[:N]   (SETNAME e.g. jsuite_v2r2;
#   N: a seeded random N items per word, conditions paper10 / rot / unembed10, run name _sN, amendment 49)
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 38 B)"
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e f <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT [0-9]" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    rend)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; set_=${e}_test_chat; cn=${p}${set_}_competence_cand2_v1; r=${p}${set_}_ko_cand2_v1
      CONDS="paper10 paper10_rot unembed10 unembed10_rot"; SA=""
      if [ -n "${f:-}" ]; then  # amendment 49: a seeded random f items per word; the logit lens's own rotation dropped
        CONDS="paper10 paper10_rot unembed10"; SA="--sample-per-word $f --sample-seed 0"; r=${p}${set_}_ko_cand2_s${f}_v1
      fi
      echo "=== competence $cn $(date -u +%T)"
      [ -f results/tasks_v2/$cn/summary.json ] || $PY scripts/natural_v1.py competence --set $set_ --name $cn --read cand2 --hop1 gen \
        --words $FACTS --why "$W: $a on $set_" > /workspace/scratch/$cn.log 2>&1 || { fail "$a $e competence" /workspace/scratch/$cn.log; continue; }
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, $set_ facts at L$band" --plan bands --bands $band \
        --conditions $CONDS --tasks $set_ --tasks-competence $cn --tasks-words $FACTS \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 $SA > /workspace/scratch/$r.log 2>&1 || { fail "$a $e KO" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite2_score.py $r --set $set_ --by-relation | grep -E "^facts (paper10|unembed10|paper10_rot) +(start=all|half=)" | sed "s/^/=== REND $a $e: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== rend GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
