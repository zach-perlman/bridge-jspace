#!/bin/bash
# Zach (2026-10-27, amendment 55 note 1): a relabelled copy of h200_fix_1023.sh (amendment 20 recipes) for new models. Usage: h200_fix_1023.sh GPU STEP ...
#   c1:TARGET:PREFIX:SET:BAND:BATCH   competence + knock-out (paper10/rot, unembed10/rot), c1_v2, c1_specificity, natplus_split
#   nat3:TARGET:PREFIX:BAND:BATCH     competence + knock-out on nat3_v1_chat (8 words, per-word eligibility), nat3_score
#   gen:TARGET:PREFIX:BAND            gen_spot on natplus_v1_chat, checked against PREFIXnatplus_v1_chat_ko_cand2_v1
#   waitq:JOB                         wait for a job's log to show EXIT
#   stopat:JOB:MARK                   when JOB's log shows MARK (fixed string), stop that job (ours) and its children
#   mem:GB                            wait until this GPU has GB free
# Every failed step is counted; the queue exits with the count (EXIT 0 only if every step succeeded).
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-27, prereg amendment 55 note 1; recipe of amendment 20)"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
comp() {  # comp SET NAME
  [ -f results/tasks_v2/$2/summary.json ] && return 0
  echo "=== competence $2 $(date -u +%T)"
  $PY scripts/natural_v1.py competence --set $1 --name $2 --read cand2 --why "$W: cand2 read, $BJ_TARGET on $1" \
    > /workspace/scratch/$2.log 2>&1 || { fail "$2" /workspace/scratch/$2.log; return 1; }
}
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done
      echo "=== GPU $G has $a GB free $(date -u +%T)";;
    stopat)
      until grep -qsF -- "$b" $R-$a.log || grep -qs "^EXIT" $R-$a.log; do sleep 20; done
      if ! grep -qs "^EXIT" $R-$a.log; then
        pp=$(tmux list-panes -t bridge-cse_01EetL8PM7B9hLWZTfSi7urd-$a -F "#{pane_pid}" 2>/dev/null)
        kids=$(pstree -p "$pp" | grep -o "([0-9]*)" | tr -d "()" | grep -v "^$pp$")
        [ -n "$pp" ] && [ -n "$kids" ] && kill $kids 2>/dev/null
        until grep -qs "^EXIT" $R-$a.log; do sleep 5; done
        echo "=== stopped $a at '$b' $(date -u +%T)"
      fi;;
    c1)
      export BJ_TARGET=$a; p=$b; set_=$c; band=$d; batch=$e; cn=${p}${set_}_competence_cand2_v1; r=${p}${set_}_ko_cand2_v1
      comp $set_ $cn || continue
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: cand2 read, $a, C1 on $set_ at L$band" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $set_ --tasks-competence $cn --tasks-words PP PM MP MM \
        --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a $set_ C1" /workspace/scratch/$r.log; continue; }
      $PY scripts/c1_v2.py $r --middle L$band --set $set_ | tail -2 | sed "s/^/=== C1 $a $set_: /"
      $PY scripts/c1_specificity.py $r $r --set $set_ | tail -2 | sed "s/^/=== spec $a $set_: /"
      $PY scripts/natplus_split.py $r --set $set_ | tail -6 | sed "s/^/=== split $a $set_: /";;
    nat3)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; set_=nat3_v1_chat; cn=${p}${set_}_competence_cand2_v1; r=${p}${set_}_ko_cand2_v1
      comp $set_ $cn || continue
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: cand2 read, $a, three-step at L$band" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $set_ --tasks-competence $cn --tasks-words PPP MPP PMP PPM MPM MMP PMM MMM \
        --tasks-level all --tasks-per-word --n 1000 --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$a nat3" /workspace/scratch/$r.log; continue; }
      $PY scripts/nat3_score.py $r --drop "South Africa" | grep -E "^all" | sed "s/^/=== nat3 $a: /";;
    gen)
      export BJ_TARGET=$a; p=$b; band=$c; r=${p}natplus_v1_chat_genspot_cand2_v1
      echo "=== gen_spot/$r $(date -u +%T)"
      [ -f results/gen_spot/$r/summary.json ] || $PY scripts/gen_spot.py --name $r --why "$W: generation spot-check, $a" --set natplus_v1_chat \
        --competence ${p}natplus_v1_chat_competence_cand2_v1 --band $band --n 25 --read cand2 --check ${p}natplus_v1_chat_ko_cand2_v1 \
        > /workspace/scratch/$r.log 2>&1 || { fail "$a gen" /workspace/scratch/$r.log; continue; }
      grep -E "^Candidate|^\| (PP|PM|MP|MM)/" results/gen_spot/$r/summary.md | sed "s/^/=== GEN $a: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== fix GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
