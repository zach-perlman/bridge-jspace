#!/bin/bash
# Zach (2026-10-26, prereg amendment 53): is Ministral's "readable, not carried" a top-10 artifact, as Bolt's was?
# GPU 0: the test knock-out at its band L32-37 with top30 / top100, rotations and the logit lens at 30 and 100 (all
# eligible items, as its top-10 run). GPU 1: removal sizes (K 10/30/100) at L20-25 and L32-37, then the J-part swap at
# mid depth L20-25 with K = 30 and 100 (all items, as its K = 10 run). Normal-equations projection (BJ_GRAM_PROJ).
# Usage: h200_mink_1026.sh ko|swap
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True BJ_TARGET=ministral-3-14b BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-26, prereg amendment 53)"
SET=jsuite_v2_test_chat; C=min14_${SET}_competence_cand2_v1
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
if [ "$1" = ko ]; then
  export CUDA_VISIBLE_DEVICES=0
  r=min14_${SET}_ko_cand2_L32-37_k30k100_v1
  echo "=== ablate_v2/$r $(date -u +%T)"
  [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: Ministral test knock-out at K 30 and 100" --plan bands --bands 32-37 \
    --conditions top30 top30_rot top100 top100_rot unembed30 unembed100 --tasks $SET --tasks-competence $C --tasks-words $FACTS --tasks-level all \
    --n 1000 --kinds clean --batch 16 --read cand2 > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
  $PY scripts/jsuite2_score.py $r --set $SET | grep -E "^facts \S+ +start=all" | sed "s/^/=== MINK /"
  $PY scripts/soft_score.py $r --set $SET | sed "s/^/=== MINKSOFT /"
else
  export CUDA_VISIBLE_DEVICES=1
  for band in 20-25 32-37; do
    s=min14_removal_size_L${band}_k_v1
    [ -f results/removal_size/$s/summary.json ] || $PY scripts/removal_size.py --name $s --why "$W: Ministral removal sizes at K 10/30/100, L$band" \
      --layers $(seq ${band%-*} ${band#*-}) --ks 10 30 100 > /workspace/scratch/$s.log 2>&1 < /dev/null || { echo "=== $s FAILED"; fails=$((fails + 1)); }
    grep -E "^  L" /workspace/scratch/$s.log | head -2 | sed "s/^/=== MINKSIZE L$band /"
  done
  for k in 30 100; do
    r=min14_jswap_v2_L20-25_k${k}_v1
    echo "=== jswap/$r $(date -u +%T)"
    [ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "$W: Ministral J-part swap with K $k at mid depth L20-25" --set $SET --band 20-25 \
      --competence $C --batch 8 --k $k > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    CUDA_VISIBLE_DEVICES="" .venv/bin/python scripts/jswap_pool.py $r 2>/dev/null | sed "s/^/=== MINKSWAP k$k /"
  done
fi
echo "=== mink $1 done, $fails failed $(date -u +%FT%TZ)"
exit $fails
