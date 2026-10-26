#!/bin/bash
# Zach (2026-10-26, prereg amendment 52): is Bolt's J-space dependence spread over more than 10 directions? At its test
# band L42-53, on the same 150 random items per word as its top-10 test (seed 0): removal sizes at K = 10, 30, 100; the
# test knock-out with top30 / top100, their rotations and the logit lens at the same K; the J-part swap with K = 30 and 100.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=nemotron-3.5-bolt BJ_GRAM_PROJ=1  # amendment 52 note 1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-26, prereg amendment 52)"
SET=jsuite_v2_test_chat; C=nem35b_${SET}_competence_cand2_v1
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
echo "=== start $(date -u +%FT%TZ)"
for j in h200mon0-1026-0340 h200ptr27-1026-0330; do until grep -qs "^EXIT [0-9]" $R-$j.log; do sleep 60; done; done
for g in 0 1; do until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 120000 ]; do sleep 60; done; done
echo "=== GPUs 0,1 free $(date -u +%T)"
s=nem35b_removal_size_L42-53_v1
[ -f results/removal_size/$s/summary.json ] || $PY scripts/removal_size.py --name $s --why "$W: Bolt removal sizes at K 10/30/100" --layers $(seq 42 53) --ks 10 30 100 \
  > /workspace/scratch/$s.log 2>&1 < /dev/null || { echo "=== $s FAILED"; tail -3 /workspace/scratch/$s.log; fails=$((fails + 1)); }
grep -E "^  L(42|47|53):" /workspace/scratch/$s.log | sed "s/^/=== BOLTKSIZE /"
r=nem35b_${SET}_ko_cand2_L42-53_k30k100_v1
echo "=== ablate_v2/$r $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: Bolt test knock-out at K 30 and 100" --plan bands --bands 42-53 \
  --conditions top30 top30_rot top100 top100_rot unembed30 unembed100 --tasks $SET --tasks-competence $C --tasks-words $FACTS --tasks-level all \
  --n 1000 --kinds clean --batch 16 --read cand2 --sample-per-word 150 --sample-seed 0 > /workspace/scratch/$r.log 2>&1 < /dev/null \
  || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
$PY scripts/jsuite2_score.py $r --set $SET | grep -E "^facts \S+ +start=all" | sed "s/^/=== BOLTK /"
$PY scripts/soft_score.py $r --set $SET | sed "s/^/=== BOLTKSOFT /"
for k in 30 100; do
  r=nem35b_jswap_v2_k${k}_v1
  echo "=== jswap/$r $(date -u +%T)"
  [ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "$W: Bolt J-part swap with K $k at L42-53" --set $SET --band 42-53 \
    --competence $C --batch 8 --sample-per-word 150 --sample-seed 0 --k $k > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
  CUDA_VISIBLE_DEVICES="" .venv/bin/python scripts/jswap_pool.py $r 2>/dev/null | sed "s/^/=== BOLTKSWAP k$k /"
done
echo "=== boltk done, $fails failed $(date -u +%FT%TZ)"
exit $fails
