#!/bin/bash
# Zach (2026-10-27, prereg amendment 57): after amendment 56 D's DeepSeek chain. A: jsuite_v2nb (seed 2701, numbers reps
# 80): competence on its numbers lookup / recall words (and three-hop words), then amendment 56 A's knock-out on them
# (smoke of one item per word first). B: late-band position splits (all-token, question-only, bridge-only) on
# jsuite_v2_test_chat at a dev-picked band.
# Usage: h200_h0nb_1027.sh GPU STEP ...   waitq:JOB  comp:TARGET:PREFIX:nu|nuth  mod:TARGET:PREFIX:BAND:BATCH:nu|th
#        all:TARGET:PREFIX:BAND:BATCH  pos:TARGET:PREFIX:BAND:BATCH:MODE
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-27, prereg amendment 57)"
NB=jsuite_v2nb_test_chat
NUW="nPL nPM nKL nKM nAL nAM nML nMM"
THW="PPP MPP PMP PPM MPM MMP PMM MMM"
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qsE "^EXIT [0-9]+" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    comp)
      export BJ_TARGET=$a; p=$b; cn=${p}${NB}_competence_cand2_v1
      words="$NUW"; [ $c = nuth ] && words="$NUW $THW"
      echo "=== competence $cn smoke $(date -u +%T)"
      $PY scripts/natural_v1.py competence --set $NB --name ${cn}_smoke1027 --words $words --read cand2 --hop1 gen --limit 16 --why "$W: smoke" \
        > /workspace/scratch/${cn}_smoke1027.log 2>&1 < /dev/null || { fail "$a competence smoke" /workspace/scratch/${cn}_smoke1027.log; continue; }
      echo "=== competence $cn $(date -u +%T)"
      [ -f results/tasks_v2/$cn/summary.json ] || $PY scripts/natural_v1.py competence --set $NB --name $cn --words $words --read cand2 --hop1 gen \
        --why "$W: $a competence on jsuite_v2nb ($c words)" > /workspace/scratch/$cn.log 2>&1 < /dev/null \
        || { fail "$a competence" /workspace/scratch/$cn.log; continue; }
      echo "=== competence $cn done $(date -u +%T)";;
    mod)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; cn=${p}${NB}_competence_cand2_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $a: no competence $cn"; fails=$((fails + 1)); continue; }
      if [ $e = th ]; then words="$THW"; extra=""; r=${p}${NB}_threehop_ko_cand2_v1; grepx="^threehop"
      else words="$NUW"; extra="--dict-digits"; r=${p}${NB}_numbers_ko_cand2_dd_v1; grepx="^numbers"; fi
      args="--plan bands --bands $band --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $NB --tasks-competence $cn --tasks-words $words --tasks-level all --tasks-per-word --kinds clean --batch $batch --read cand2 $extra"
      echo "=== smoke ${r}_smoke1027 $(date -u +%T)"
      $PY scripts/ablate_v2.py --name ${r}_smoke1027 --why "$W: smoke" $args --n 1 > /workspace/scratch/${r}_smoke1027.log 2>&1 < /dev/null || { fail "$a $e smoke" /workspace/scratch/${r}_smoke1027.log; continue; }
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, jsuite_v2nb module $e at L$band" $args --n 1000 \
        > /workspace/scratch/$r.log 2>&1 < /dev/null || { fail "$a $e KO" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite2_score.py $r --set $NB | grep -E "$grepx" | sed "s/^/=== H0NB $a $e: /";;
    all|pos)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; SET=jsuite_v2_test_chat; cn=${p}${SET}_competence_cand2_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $a: no competence $cn"; fails=$((fails + 1)); continue; }
      if [ $kind = all ]; then r=${p}${SET}_ko_cand2_L${band}_v1; extra="--conditions paper10 paper10_rot unembed10 unembed10_rot"; tag="all"
      else r=${p}${SET}_ko_cand2_L${band}_pos${e}_v1; extra="--positions $e --conditions paper10 paper10_rot"; tag=$e; fi
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a late band L$band, $tag" --plan bands --bands $band \
        $extra --tasks $SET --tasks-competence $cn --tasks-words $FACTS --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 \
        > /workspace/scratch/$r.log 2>&1 < /dev/null || { fail "$a L$band $tag" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite2_score.py $r --set $SET | grep -E "^facts (paper10|paper10_rot|unembed10) +start=" | sed "s/^/=== LATE $a L$band $tag: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== h0nb GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
