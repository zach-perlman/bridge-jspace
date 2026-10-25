#!/bin/bash
# Zach (2026-10-25, prereg amendment 42): DeepSeek-V4-Flash on GPUs 0,1: its dev depth profile (h200_profile_1025.sh),
# the test knock-out at the profile's pick (scripts/profile_pick.py; h200_depth_42.sh all, run names carry the band)
# unless the pick is L36-41 (already run), the swap at mid depth L22-27 (the 27B's relative depth, 50-62% of 43), and
# last the line Lightning's and Bolt's chains wait for. Usage: h200_ds42_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=deepseek-v4-flash
PY="uv run --no-sync python"
W="Zach (2026-10-25, prereg amendment 42)"
SET=jsuite_v2_test_chat
echo "=== start $(date -u +%FT%TZ)"
for g in 0 1; do need=$([ $g = 0 ] && echo 60000 || echo 120000); until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $need ]; do sleep 60; done; done
fails=0
bash scripts/queues/h200_profile_1025.sh 0,1 prof:deepseek-v4-flash:dsv4f_:16:40 || fails=$((fails + 1))
band=$($PY scripts/profile_pick.py dsv4f_jsuite_v2_dev_chat_profile_cand2_v1 2>/dev/null)
echo "=== DS42 pick: '$band'"
if [[ "$band" =~ ^[0-9]+-[0-9]+$ ]] && [ "$band" != 36-41 ]; then
  bash scripts/queues/h200_depth_42.sh 0,1 all:deepseek-v4-flash:dsv4f_:$band:16 || fails=$((fails + 1))
fi
r=dsv4f_jswap_v2_L22-27_v1
echo "=== jswap/$r $(date -u +%T)"
[ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "$W: deepseek-v4-flash, the swap at mid depth L22-27" --set $SET \
  --band 22-27 --competence dsv4f_${SET}_competence_cand2_v1 --batch 8 > /workspace/scratch/$r.log 2>&1 < /dev/null \
  || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
grep -E "^(PM|TM|PN|TN|PK|TK|PP|TP) (swap|remove|swap_rot|swap_u|swap_comp|paste) " /workspace/scratch/$r.log | sed "s/^/=== MIDSWAP deepseek-v4-flash /"
$PY scripts/jswap_by_relation.py $r --set $SET | grep -v -i warn | sed "s/^/=== MIDSWAPREL deepseek-v4-flash /"
echo "=== nq deepseek-v4-flash done, $fails failed $(date -u +%FT%TZ)"
exit $fails
