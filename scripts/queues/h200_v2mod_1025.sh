#!/bin/bash
# Zach (2026-10-25, prereg amendment 37 B): v2 modules 3 (three-hop) and 2 (numbers) on jsuite_v2_test_chat, the model's v2
# test competence, per-item eligibility, paper10 / rot / unembed10 / rot, cand2 (numbers: --dict-digits); a smoke of one
# item per word first (its failure skips the full run); scored by jsuite2_score.
# Usage: h200_v2mod_1025.sh GPU STEP ...   waitq:JOB  mod:TARGET:PREFIX:BAND:BATCH:th|nu
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 37 B)"
SET=jsuite_v2_test_chat
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mod)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; cn=${p}${SET}_competence_cand2_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $a: no competence $cn"; fails=$((fails + 1)); continue; }
      if [ $e = th ]; then words="PPP MPP PMP PPM MPM MMP PMM MMM"; extra=""; r=${p}${SET}_threehop_ko_cand2_v1; grepx="^threehop"
      else words="nPR nPL nPM nKR nKL nKM nAR nAL nAM nMR nML nMM"; extra="--dict-digits"; r=${p}${SET}_numbers_ko_cand2_dd_v1; grepx="^numbers"; fi
      args="--plan bands --bands $band --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn --tasks-words $words --tasks-level all --tasks-per-word --kinds clean --batch $batch --read cand2 $extra"
      echo "=== smoke ${r}_smoke1025 $(date -u +%T)"
      $PY scripts/ablate_v2.py --name ${r}_smoke1025 --why "$W: smoke" $args --n 1 > /workspace/scratch/${r}_smoke1025.log 2>&1 || { fail "$a $e smoke" /workspace/scratch/${r}_smoke1025.log; continue; }
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, module $e at L$band" $args --n 1000 \
        > /workspace/scratch/$r.log 2>&1 || { fail "$a $e KO" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite2_score.py $r --set $SET | grep -E "$grepx" | sed "s/^/=== V2MOD $a $e: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== v2mod GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
