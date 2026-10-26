#!/bin/bash
# Zach (2026-10-26, prereg amendment 51): what the mention's J-part carries (scripts/jswap_pointer.py) for a model at its
# band, N random jobs per word. Usage: h200_ptr_1026.sh GPU STEP ...   STEP: waitq:JOB  ptr:TARGET:PREFIX:BAND:BATCH:N
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
fails=0
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT [0-9]" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    ptr)
      r=${b}jswap_pointer_v2_s${e}_v1
      echo "=== jswap_pointer/$r at L$c $(date -u +%T)"
      [ -f results/jswap/$r/summary.json ] || BJ_TARGET=$a $PY scripts/jswap_pointer.py --name $r --why "Zach (2026-10-26, prereg amendment 51): $a at L$c" \
        --band $c --competence ${b}jsuite_v2_test_chat_competence_cand2_v1 --batch $d --sample-per-word $e > /workspace/scratch/$r.log 2>&1 < /dev/null \
        || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      grep -E "^memory +|^memory_[a-z]+ +(swap|swap_neutral|swap_noown) " /workspace/scratch/$r.log | sed "s/^/=== PTR $a /"
      grep -E "^(PP|PK|TP|TK) " /workspace/scratch/$r.log | sed "s/^/=== PTRLOOK $a /"
      grep -E "^timeline " /workspace/scratch/$r.log | sed "s/^/=== PTRTL $a /" | cut -c1-600;;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== ptr done, $fails failed $(date -u +%FT%TZ)"
exit $fails
