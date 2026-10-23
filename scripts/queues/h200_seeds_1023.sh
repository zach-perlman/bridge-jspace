#!/bin/bash
# Zach (2026-10-23, prereg amendment 19). Usage: h200_seeds_1023.sh GPU STEP ...
#   gen:TARGET:PREFIX:BAND           generation spot-check on natplus_v1_chat (checked against PREFIXnatplus_v1_chat_ko_cand_v1)
#   c1:TARGET:PREFIX:SET:BAND:BATCH  competence + knock-out (paper10/rot, unembed10/rot), c1_v2, c1_specificity, natplus_split
#   waitq:JOB                        wait for a job's log to show EXIT
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-23, prereg amendment 19)"
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    gen)
      export BJ_TARGET=$a; p=$b; band=$c; n=${d:-25}; r=${p}natplus_v1_chat_genspot${d:+_n$d}_v1
      echo "=== gen_spot/$r $(date -u +%T)"
      [ -f results/gen_spot/$r/summary.json ] || $PY scripts/gen_spot.py --name $r --why "$W: generation spot-check, $a" --set natplus_v1_chat \
        --competence ${p}natplus_v1_chat_competence_cand_v1 --band $band --n $n --check ${p}natplus_v1_chat_ko_cand_v1 \
        > /workspace/scratch/$r.log 2>&1 || { echo "=== $a gen FAILED"; tail -3 /workspace/scratch/$r.log; continue; }
      grep -E "^Candidate|^\| (PP|PM|MP|MM)/" results/gen_spot/$r/summary.md | sed "s/^/=== GEN $a: /";;
    c1)
      export BJ_TARGET=$a; p=$b; set_=$c; band=$d; batch=$e; cn=${p}${set_}_competence_cand_v1; r=${p}${set_}_ko_cand_v1
      echo "=== competence $cn $(date -u +%T)"
      [ -f results/tasks_v2/$cn/summary.json ] || $PY scripts/natural_v1.py competence --set $set_ --name $cn --read cand --why "$W: $a on $set_" \
        > /workspace/scratch/$cn.log 2>&1 || { echo "=== $a $set_ competence FAILED"; tail -3 /workspace/scratch/$cn.log; continue; }
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, C1 on $set_ at L$band" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $set_ --tasks-competence $cn --tasks-words PP PM MP MM \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand > /workspace/scratch/$r.log 2>&1 || { echo "=== $a $set_ C1 FAILED"; tail -3 /workspace/scratch/$r.log; continue; }
      $PY scripts/c1_v2.py $r --middle L$band --set $set_ | tail -2 | sed "s/^/=== C1 $a $set_: /"
      $PY scripts/c1_specificity.py $r $r --set $set_ | tail -2 | sed "s/^/=== spec $a $set_: /"
      $PY scripts/natplus_split.py $r --set $set_ | tail -4 | sed "s/^/=== split $a $set_: /";;
  esac
done
echo "=== seeds GPU $G done $(date -u +%FT%TZ)"
