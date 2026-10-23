#!/bin/bash
# Zach (2026-10-23, prereg amendments 16-17). Usage: h200_ctl_1023.sh GPU STEP ...
#   natctl:TARGET:PREFIX:BAND:BATCH   competence + knock-out on natctl_v1_chat (8 words, scene eligibility)
#   sweep:TARGET:PREFIX:BATCH:BANDS   competence + band sweep on natplus_dev_chat, then choose_band
#   waitq:JOB                         wait for a job's log to show EXIT
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
comp() {  # comp SET NAME WHY
  [ -f results/tasks_v2/$2/summary.json ] && return 0
  echo "=== competence $2 $(date -u +%T)"
  $PY scripts/natural_v1.py competence --set $1 --name $2 --read cand --why "$3" > /workspace/scratch/$2.log 2>&1 || { echo "=== $2 FAILED"; tail -3 /workspace/scratch/$2.log; return 1; }
}
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    natctl)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; set_=natctl_v1_chat; cn=${p}${set_}_competence_cand_v1; r=${p}${set_}_ko_cand_v1
      W="Zach (2026-10-23, prereg amendment 16): natctl, $a"
      comp $set_ $cn "$W" || continue
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W at L$band" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $set_ --tasks-competence $cn --tasks-words PP PK PM PA MP MK MM MA \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand > /workspace/scratch/$r.log 2>&1 || { echo "=== $a natctl FAILED"; tail -3 /workspace/scratch/$r.log; continue; }
      $PY scripts/natctl_score.py $r | grep -E "^start" | sed "s/^/=== natctl $a: /";;
    sweep)
      export BJ_TARGET=$a; p=$b; batch=$c; bands=${d//,/ }; set_=natplus_dev_chat; cn=${p}${set_}_competence_cand_v1; r=${p}${set_}_sweep_cand_v1
      W="Zach (2026-10-23, prereg amendment 17): natural band sweep, $a"
      comp $set_ $cn "$W" || continue
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W" --plan bands --bands $bands \
        --conditions paper10 paper10_rot --tasks $set_ --tasks-competence $cn --tasks-words PP PM MP MM --tasks-level all --n 100 \
        --kinds clean --batch $batch --read cand > /workspace/scratch/$r.log 2>&1 || { echo "=== $a sweep FAILED"; tail -3 /workspace/scratch/$r.log; continue; }
      echo "=== natural band $a: $($PY scripts/choose_band.py $r 2>/dev/null | tail -1)";;
  esac
done
echo "=== ctl GPU $G done $(date -u +%FT%TZ)"
