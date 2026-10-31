#!/bin/bash
# Zach (2026-10-29, prereg amendment 61: the rebuilt sets; amendment 60 notes 29-31 + addendum): the three v4-family sets. Usage: h200_v5_1029.sh SET MODEL GPU [WAITJOB ...]
#   SET: key (jsuite_v5kn named + jsuite_v5kd described), kc (jsuite_v5kc), alias (jsuite_v5al)
#   per set: a pipeline smoke (competence + controls on 8 items, readout on 2), competence, controls, note 20's knock-out at the
#   model's band, the readout (note 25 priming targets + note 26 top-20), then scripts/nn_v5_read.py
set -u
SETK=$1; M=$2; G=$3; shift 3
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=32 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; KBATCH=16 ;;
esac
W="Zach (2026-10-29, prereg amendment 60, $SETK, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
one() {  # one TAG WORDS CTLWORDS SCENEWORDS ITEMS KINDS
  local tag=$1 words=$2 ctlw=$3 scenew=$4 itemsmode=$5 kinds=$6
  local SET=jsuite_${tag}_test_chat CTL=jsuite_${tag}ctl_test_chat
  local C=${P}${SET}_competence_cand2_v1 CV=${P}jsuite_${tag}ctl_cv_v1
  # pipeline smoke on a few items (competence, controls, readout), then set aside
  local sc=${P}${SET}_competence_smoke1029 scv=${P}jsuite_${tag}ctl_cv_smoke1029 sr=${P}nn_readout_${tag}_smoke1029
  # shellcheck disable=SC2086
  $PY scripts/natural_v1.py competence --set $SET --name $sc --words $words --read cand2 --hop1 gen --limit 8 --why "$W: smoke" > /workspace/scratch/$sc.log 2>&1 < /dev/null \
    && $PY scripts/competence_variants.py --name $scv --why "$W: smoke" --set $CTL --words $ctlw --variants none --limit 8 > /workspace/scratch/$scv.log 2>&1 < /dev/null \
    || { echo "=== $tag smoke FAILED"; tail -5 /workspace/scratch/$sc.log /workspace/scratch/$scv.log; fails=$((fails + 1)); return 1; }
  if [ "$itemsmode" = v4all ]; then
    # shellcheck disable=SC2086
    $PY scripts/nn_readout.py --name $sr --set $SET --competence $sc --items v4all --words $words --priming --topk 20 --limit 2 > /workspace/scratch/$sr.log 2>&1 < /dev/null
  else
    $PY scripts/nn_readout.py --name $sr --set $SET --competence $sc --cv-h1 $scv --items v4 --priming --topk 20 --limit 2 > /workspace/scratch/$sr.log 2>&1 < /dev/null
  fi
  [ $? = 0 ] || { echo "=== $tag readout smoke FAILED"; tail -5 /workspace/scratch/$sr.log; fails=$((fails + 1)); return 1; }
  grep -h "prompts; by family" /workspace/scratch/$sr.log
  mv results/tasks_v2/$sc results/competence_variants/$scv results/nn_readout/$sr /workspace/scratch/ 2>/dev/null
  echo "=== $tag smoke ok $(date -u +%T)"
  # shellcheck disable=SC2086
  go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words $words --read cand2 --hop1 gen --why "$W: competence" || return 1
  # shellcheck disable=SC2086
  go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: controls" --set $CTL --words $ctlw --variants none || return 1
  local r=${P}${SET}_ko_cand2_v1
  if [ "$itemsmode" = v4all ]; then  # the conflict set: every item of scenes whose true-control words are right; the scorer gates
    # shellcheck disable=SC2086
    go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: note 20's knock-out" --plan bands --bands $KB \
      --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words $(echo $words | tr ' ' '\n' | grep -v '^T' | tr '\n' ' ') \
      --tasks-scene-words $scenew --tasks-level all --n 1000 --kinds clean --batch $KBATCH --read cand2
  else
    # shellcheck disable=SC2086
    go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: note 20's knock-out" --plan bands --bands $KB \
      --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words $words --tasks-per-word \
      --tasks-level all --n 1000 --kinds $kinds --batch $KBATCH --read cand2 --tasks-v4-h1 $CV
  fi
  local rr=${P}nn_readout_${tag}_v1
  if [ "$itemsmode" = v4all ]; then
    # shellcheck disable=SC2086
    go nn_readout $rr $PY scripts/nn_readout.py --name $rr --set $SET --competence $C --items v4all --words $(echo $words | tr ' ' '\n' | grep -v '^T' | tr '\n' ' ') --priming --topk 20
  else
    go nn_readout $rr $PY scripts/nn_readout.py --name $rr --set $SET --competence $C --cv-h1 $CV --items v4 --priming --topk 20
  fi
}
case $SETK in
  key) one v5kn "MP MM" "H1 K0" "" v4 "clean step2"; one v5kd "MP MM" "H1 K0" "" v4 "clean step2 step3" ;;
  key2) one v5kn2 "MP MM" "H1 K0" "" v4 "clean step2"; one v5kd2 "MP MM" "H1 K0" "" v4 "clean step2 step3" ;;
  kc2) one v5kc2 "CN CA DN DA TN TD" "H1 H2" "TN TD" v4all "clean" ;;
  kc) one v5kc "CN CA DN DA TN TD" "H1 H2" "TN TD" v4all "clean" ;;
  alias) one v5al "MP MM" "H1" "" v4 "clean" ;;
esac
.venv/bin/python scripts/nn_v5_read.py $SETK "$P" > /workspace/scratch/${P}v5_${SETK}.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}v5_${SETK}.txt; fails=$((fails + 1)); }
grep -h "reading" /workspace/scratch/${P}v5_${SETK}.txt | head -8
echo "=== v5 $SETK $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
