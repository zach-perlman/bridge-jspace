#!/bin/bash
# Amendment 41 (2026-10-25): h200_v21r_1024.sh with its --why strings marked amendment 41 (Ministral follow-up).
# Zach (2026-10-24, prereg amendment 35 note 1): v2.1's R items only, beside a model's v2 run (v2.1 = v2 + R, ids
# shared). r: competence on RM RA RN (candidate pools from the whole set), the knock-out on RM RA RN at the model's v2
# band with its v2 conditions, then jsuite2_score on the model's v2 knock-out --with the R run (checks model, lens, band,
# conditions, read, positions match; items disjoint).
# Usage: h200_v21r_1024.sh GPU STEP ...   waitq:JOB  r:TARGET:PREFIX:BAND:BATCH[:FRAMING]
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 41)"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    r)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; f=${e:-chat}; set_=jsuite_v2_1_test_$f
      cn=${p}${set_}_R_competence_cand2_v1; r=${p}${set_}_R_ko_cand2_v1; v2=${p}jsuite_v2_test_${f}_ko_cand2_v1
      echo "=== R competence $cn $(date -u +%T)"
      [ -f results/tasks_v2/$cn/summary.json ] || $PY scripts/natural_v1.py competence --set $set_ --name $cn --read cand2 --hop1 gen \
        --words RM RA RN --why "$W: $a, R items of $set_" > /workspace/scratch/$cn.log 2>&1 || { fail "$a R competence" /workspace/scratch/$cn.log; continue; }
      python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== V21R COMP $a', {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$cn/summary.json
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, R items at L$band" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $set_ --tasks-competence $cn --tasks-words RM RA RN \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a R KO" /workspace/scratch/$r.log; continue; }
      [ -f results/ablate_v2/$v2/summary.json ] || { echo "=== $a: no v2 knock-out $v2 to score with"; fails=$((fails + 1)); continue; }
      $PY scripts/jsuite2_score.py $v2 --set $set_ --by-relation --with $r | grep -E "^facts (paper10|unembed10|paper10_rot) +(start=all|never-named)" | sed "s/^/=== V21R $a: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== v2.1 R GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
