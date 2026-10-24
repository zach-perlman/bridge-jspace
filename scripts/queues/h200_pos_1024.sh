#!/bin/bash
# Zach (2026-10-24, prereg amendment 30): position-restricted knock-outs on module 1 (jsuite_v1_facts_test_chat), at the
# model's pre-registered band: the same removal (paper10, and its rotated size-matched control) applied only at the
# passage (context), only from the question on (question), only at the answer position (final), or only at the
# bridge's mentions (bridge). 12 words, scene eligibility from the model's test competence, cand2; jsuite_score.
# Usage: h200_pos_1024.sh GPU STEP ...   waitq:JOB   mem:GB   pos:TARGET:PREFIX:BAND:BATCH:MODE[:u]
# (2026-10-24: a trailing :u runs the logit-lens control, unembed10 and its rotation, named *_pos<MODE>_u_v1)
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-24, prereg amendment 30)"
SET=jsuite_v1_facts_test_chat
WORDS="PP PK PM PA MP MK MM MA TP TK TM TA"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e f <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done
      echo "=== GPU $G has $a GB free $(date -u +%T)";;
    pos)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; mode=$e; conds="paper10 paper10_rot"; sfx=""
      [ "${f:-}" = u ] && { conds="unembed10 unembed10_rot"; sfx=_u; }
      cn=${p}${SET}_competence_cand2_v1; r=${p}${SET}_ko_cand2_pos${mode}${sfx}_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $a pos $mode: no test competence $cn"; fails=$((fails + 1)); continue; }
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, the knock-out at L$band only at the $mode positions" \
        --plan bands --bands $band --positions $mode --conditions $conds --tasks $SET --tasks-competence $cn --tasks-words $WORDS \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a pos $mode" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite_score.py $r | grep -E "^start (all|P |M |T )" | grep -E "paper10 |paper10_rot |unembed10 |unembed10_rot " | sed "s/^/=== POS $a $mode$sfx: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== pos GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
