#!/bin/bash
# Zach (2026-10-26, prereg amendment 50): amendment 47's cross-relation swap (scripts/jswap_xrel.py) for any model at a band.
# Usage: h200_xrelm_1026.sh GPU STEP ...   STEP: waitq:JOB  xrel:TARGET:PREFIX:BAND:BATCH
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
fails=0
for step in "$@"; do
  IFS=: read -r kind a b c d <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT [0-9]" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    xrel)
      r=${b}jswap_xrel_v2_v1
      echo "=== jswap_xrel/$r at L$c $(date -u +%T)"
      [ -f results/jswap/$r/summary.json ] || BJ_TARGET=$a $PY scripts/jswap_xrel.py --name $r --why "Zach (2026-10-26, prereg amendment 50): $a, the cross-relation swap at L$c" \
        --band $c --set jsuite_v2_test_chat --competence ${b}jsuite_v2_test_chat_competence_cand2_v1 --batch $d > /workspace/scratch/$r.log 2>&1 < /dev/null \
        || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      grep -E "^memory " /workspace/scratch/$r.log | sed "s/^/=== XREL $a /"
      grep -E "^(PP|PK|TP|TK) +swap_xrel " /workspace/scratch/$r.log | sed "s/^/=== XRELLOOK $a /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== xrelm done, $fails failed $(date -u +%FT%TZ)"
exit $fails
