#!/bin/bash
# Zach (2026-10-25, prereg amendment 41): DeepSeek-V4-Flash follow-ups on GPUs 0,1. Its amendment-39 band L36-41 broke
# lookups as much as recall (uninformative). Steps: (1) the test knock-out at L27-32, the lookup-sparing band rule's
# pick on its dev sweep (scripts/band_rule2.py), paper10 / rot / unembed10 / rot; (2) only if that M - K >= 15:
# question-only and bridge-mention-only at L27-32 (paper10 / rot); (3) the swap at mid depth, L22-27 (the 27B's relative
# depth, 50-62% of 43 blocks), with jswap_by_relation. Lightning's J-lens fit (h200nemL5) is stopped right after its
# first checkpoint (jlens resumes from it) and relaunched as h200nemL6 at the end. Last, the line Bolt's chain waits for.
# Usage: h200_ds41_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=deepseek-v4-flash
PY="uv run --no-sync python"
W="Zach (2026-10-25, prereg amendment 41)"
P=bridge-cse_01EetL8PM7B9hLWZTfSi7urd; R=/workspace/runs/$P
L=cache/nemotron-3.5-lightning/lenses/jlens/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jlens.pt
SET=jsuite_v2_test_chat
echo "=== start $(date -u +%FT%TZ)"
until [ -f $L.ckpt ] || grep -qs "^EXIT" $R-h200nemL5-1025-1600.log; do sleep 20; done
tmux kill-session -t $P-h200nemL5-1025-1600 2>/dev/null \
  && echo "EXIT 1 stopped by h200ds41 right after its first J-lens checkpoint (resumed in h200nemL6) $(date -u +%FT%TZ)" >> $R-h200nemL5-1025-1600.log
echo "=== Lightning fit paused, checkpoint $(stat -c %y $L.ckpt 2>/dev/null | cut -c12-19) $(date -u +%T)"
for g in 0 1; do need=$([ $g = 0 ] && echo 60000 || echo 120000); until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $need ]; do sleep 60; done; done
fails=0
bash scripts/queues/h200_depth_41.sh 0,1 all:deepseek-v4-flash:dsv4f_:27-32:16 || fails=$((fails + 1))
mk=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['facts']['paper10/start=all']['contrasts']['M-K']['diff'])" \
  results/ablate_v2/jsuite2_score/dsv4f_${SET}_ko_cand2_L27-32_v1.json 2>/dev/null || echo nan)
echo "=== DS41 M-K at L27-32: $mk"
if python3 -c "import sys; sys.exit(0 if float(sys.argv[1]) >= 15 else 1)" "$mk" 2>/dev/null; then
  bash scripts/queues/h200_depth_41.sh 0,1 pos:deepseek-v4-flash:dsv4f_:27-32:16:question pos:deepseek-v4-flash:dsv4f_:27-32:16:bridge || fails=$((fails + 1))
fi
r=dsv4f_jswap_v2_L22-27_v1
echo "=== jswap/$r $(date -u +%T)"
[ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "$W: deepseek-v4-flash, the swap at mid depth L22-27" --set $SET \
  --band 22-27 --competence dsv4f_${SET}_competence_cand2_v1 --batch 8 > /workspace/scratch/$r.log 2>&1 \
  || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); }
grep -E "^(PM|TM|PN|TN|PK|TK|PP|TP) (swap|remove|swap_rot|swap_u|swap_comp|paste) " /workspace/scratch/$r.log | sed "s/^/=== MIDSWAP deepseek-v4-flash /"
$PY scripts/jswap_by_relation.py $r --set $SET | grep -v -i warn | sed "s/^/=== MIDSWAPREL deepseek-v4-flash /"
echo "=== nq deepseek-v4-flash done, $fails failed $(date -u +%FT%TZ)"
/root/run_job.sh $P-h200nemL6-1025-1600 /workspace/bridge-jspace "bash scripts/queues/h200_nem_1025.sh 1"
exit $fails
