#!/bin/bash
# Zach (2026-10-25, prereg amendment 47): the cross-relation swap (scripts/jswap_xrel.py) on the 9B (L12-16) and the
# 27B (L32-40), GPU 0, after the 9B renderings. Usage: h200_xrel_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 47)"
# 2026-10-25 23:55 UTC (Zach: GPUs underused): no longer waits for the 9B renderings; it runs beside them on GPU 0
fails=0
for spec in "qwen3.5-9b:qwen35_9b_:12-16:16" "qwen3.6-27b::32-40:8"; do
  IFS=: read -r key p band batch <<< "$spec"
  r=${p}jswap_xrel_v2_v1
  echo "=== jswap_xrel/$r at L$band $(date -u +%T)"
  [ -f results/jswap/$r/summary.json ] || BJ_TARGET=$key $PY scripts/jswap_xrel.py --name $r --why "$W: $key, the cross-relation swap at L$band" \
    --band $band --competence ${p}jsuite_v2_test_chat_competence_cand2_v1 --batch $batch > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
  grep -E "^memory " /workspace/scratch/$r.log | sed "s/^/=== XREL $key /"
  grep -E "^(PP|PK|TP|TK) +swap_xrel " /workspace/scratch/$r.log | sed "s/^/=== XRELLOOK $key /"
done
echo "=== xrel done, $fails failed $(date -u +%FT%TZ)"
exit $fails
