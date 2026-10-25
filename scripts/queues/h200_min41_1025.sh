#!/bin/bash
# Zach (2026-10-25, prereg amendment 41): Ministral 3 14B follow-ups on GPU 0. Amendment 39 allows positions and R items
# once M - K >= 15; Ministral's is +23. Steps: question-only and bridge-mention-only knock-outs at its band L32-37
# (paper10 / rot; h200_depth_41.sh); v2.1's R items at L32-37 scored with its v2 run (h200_v21r_41.sh), and r_matched;
# the swap at mid depth, L20-25 (the 27B's L32-40 relative depth, 50-62% of 40 blocks), with jswap_by_relation.
# Usage: h200_min41_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0 BJ_TARGET=ministral-3-14b
PY="uv run --no-sync python"
W="Zach (2026-10-25, prereg amendment 41)"
echo "=== start $(date -u +%FT%TZ)"
fails=0
bash scripts/queues/h200_depth_41.sh 0 pos:ministral-3-14b:min14_:32-37:16:question pos:ministral-3-14b:min14_:32-37:16:bridge || fails=$((fails + 1))
bash scripts/queues/h200_v21r_41.sh 0 r:ministral-3-14b:min14_:32-37:16 || fails=$((fails + 1))
$PY scripts/r_matched.py min14_jsuite_v2_test_chat_ko_cand2_v1 min14_jsuite_v2_1_test_chat_R_ko_cand2_v1 --set jsuite_v2_1_test_chat 2>&1 \
  | grep -E "pairs|paper10|unembed10" | sed "s/^/=== RMATCH ministral-3-14b /"
r=min14_jswap_v2_L20-25_v1
echo "=== jswap/$r $(date -u +%T)"
[ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "$W: ministral-3-14b, the swap at mid depth L20-25" --set jsuite_v2_test_chat \
  --band 20-25 --competence min14_jsuite_v2_test_chat_competence_cand2_v1 --batch 8 > /workspace/scratch/$r.log 2>&1 \
  || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
grep -E "^(PM|TM|PN|TN|PK|TK|PP|TP) (swap|remove|swap_rot|swap_u|swap_comp|paste) " /workspace/scratch/$r.log | sed "s/^/=== MIDSWAP ministral-3-14b /"
$PY scripts/jswap_by_relation.py $r --set jsuite_v2_test_chat | grep -v -i warn | sed "s/^/=== MIDSWAPREL ministral-3-14b /"
echo "=== min41 done, $fails failed $(date -u +%FT%TZ)"
exit $fails
