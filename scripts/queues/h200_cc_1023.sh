#!/bin/bash
# Zach (2026-10-23, prereg amendment 21): ctxcomp_v1 (numbers computed on the passage). Usage: h200_cc_1023.sh GPU STEP ...
#   cc:TARGET:PREFIX:BAND:BATCH[:N]   competence (cand2) + knock-out (paper10/rot, unembed10/rot) on the 12 words + ctxcomp_score
#                                     (N < 1000: a smoke run, named *_smoke)
#   waitq:JOB / mem:GB                as h200_fix_1023.sh
# Failed steps are counted; the queue exits with the count.
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-23, prereg amendment 21)"
SET=ctxcomp_v1_chat
WORDS="PR PP PM KR KP KM AR AP AM MR MP MM"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done
      echo "=== GPU $G has $a GB free $(date -u +%T)";;
    cc)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; n=${e:-1000}; cn=${p}${SET}_competence_cand2_v1
      r=${p}${SET}_ko_cand2_v1; [ "$n" -lt 1000 ] && r=${p}${SET}_ko_cand2_smoke
      if [ ! -f results/tasks_v2/$cn/summary.json ]; then
        echo "=== competence $cn $(date -u +%T)"
        $PY scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --why "$W: $a on $SET" > /workspace/scratch/$cn.log 2>&1 \
          || { fail "$a competence" /workspace/scratch/$cn.log; continue; }
      fi
      python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== CCCOMP $a whole:', {k: v['whole'] for k, v in s.items()})" results/tasks_v2/$cn/summary.json
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, ctxcomp at L$band" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn --tasks-words $WORDS \
        --tasks-level all --n $n --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a ctxcomp KO" /workspace/scratch/$r.log; continue; }
      $PY scripts/ctxcomp_score.py $r | sed "s/^/=== CC $a: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== cc GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
