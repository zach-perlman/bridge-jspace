#!/bin/bash
# Amendment 42 (2026-10-25): h200_depth_1025.sh with its --why strings marked amendment 42.
# Zach (2026-10-25, prereg amendment 37 A): depth-matched bands. all: the all-token knock-out (paper10 / rot / unembed10 /
# rot) at BAND on jsuite_v2_test_chat, the 15 facts words, the model's v2 test competence; pos: the same restricted to
# MODE (question / context / bridge; paper10 / rot). Run names carry the band. Scored by jsuite2_score.
# (all also serves amendment 37 D: OLMo's v2 knock-out at its own band, with FRAMING qa.)
# Usage: h200_depth_1025.sh GPU STEP ...   waitq:JOB  mem:GB  all:TARGET:PREFIX:BAND:BATCH[:FRAMING]  pos:TARGET:PREFIX:BAND:BATCH:MODE
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 42)"
WORDS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done
      echo "=== GPU $G has $a GB free $(date -u +%T)";;
    all|pos)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; SET=jsuite_v2_test_chat
      [ $kind = all ] && SET=jsuite_v2_test_${e:-chat}
      cn=${p}${SET}_competence_cand2_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $a: no competence $cn"; fails=$((fails + 1)); continue; }
      if [ $kind = all ]; then r=${p}${SET}_ko_cand2_L${band}_v1; extra="--conditions paper10 paper10_rot unembed10 unembed10_rot"; tag="all"
      else r=${p}${SET}_ko_cand2_L${band}_pos${e}_v1; extra="--positions $e --conditions paper10 paper10_rot"; tag=$e; fi
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a at L$band, $tag" --plan bands --bands $band \
        $extra --tasks $SET --tasks-competence $cn --tasks-words $WORDS \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a L$band $tag" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite2_score.py $r --set $SET --by-relation | grep -E "^facts (paper10|paper10_rot|unembed10) +start=" | sed "s/^/=== DEPTH $a L$band $tag: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== depth GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
