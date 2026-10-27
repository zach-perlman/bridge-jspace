#!/bin/bash
# Zach (2026-10-27, amendment 56 D, approved by Zach: "Yes you can delete bolts cache after"): after Bolt's pointer test
# succeeds, drop Bolt's cache, download DeepSeek-V4-Flash (pinned revision), then amendment 54's dose grid at L18-23 and
# DeepSeek's mention / question split at the K where its J-specific excess peaks (below the specificity limit).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_GRAM_PROJ=1 BJ_TARGET=deepseek-v4-flash
PY="uv run --no-sync python"
W="Zach (2026-10-27, prereg amendment 56 D)"
G=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-h200bptr-1027-0400.log
SET=jsuite_v2_test_chat; P=dsv4f_; BAND=18-23; B=16; C=${P}${SET}_competence_cand2_v1
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
KS="1 3 10 30 100 300"
CONDS="top1 top1_rot top3 top3_rot top10 top10_rot top10_pcasize unembed10 top30 top30_rot top30_pcasize unembed30 top100 top100_rot top100_pcasize unembed100 top300 top300_rot top300_pcasize unembed300"
echo "=== DS waiting for Bolt's pointer test $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" $G; do sleep 60; done
grep -qs "=== BPTR done" $G || { echo "=== DS: Bolt's pointer test did not finish; Bolt's cache kept, stop"; exit 1; }
BOLT=models--nvidia--NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16
[ -d /workspace/hf_cache/hub/$BOLT ] && python3 /workspace/scratch/cache_drop.py $BOLT | sed "s/^/=== DS /"
free=$(df -BG --output=avail /workspace | tail -1 | tr -dc 0-9)
echo "=== DS download, $free GB free $(date -u +%T)"
[ "$free" -ge 165 ] || [ -d /workspace/hf_cache/hub/models--deepseek-ai--DeepSeek-V4-Flash/snapshots/60d8d70770c6776ff598c94bb586a859a38244f1 ] || { echo "=== DS download: only $free GB free, stop"; exit 1; }
CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
from huggingface_hub import snapshot_download
print('=== DS download done', snapshot_download('deepseek-ai/DeepSeek-V4-Flash', revision='60d8d70770c6776ff598c94bb586a859a38244f1'))" 2>&1 | grep "=== DS" || { echo "=== DS download FAILED"; exit 1; }
s=${P}removal_size_L${BAND}_dose54_v1
[ -f results/removal_size/$s/summary.json ] || $PY scripts/removal_size.py --name $s --why "$W: DeepSeek removal sizes at L$BAND, K $KS" \
  --layers $(seq ${BAND%-*} ${BAND#*-}) --ks $KS --pca > /workspace/scratch/$s.log 2>&1 < /dev/null || { echo "=== $s FAILED"; tail -3 /workspace/scratch/$s.log; }
r=${P}${SET}_ko_cand2_L${BAND}_dose54_s150_v1
echo "=== ablate_v2/$r $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: DeepSeek test knock-out, dose grid K $KS" --plan bands --bands $BAND \
  --conditions $CONDS --tasks $SET --tasks-competence $C --tasks-words $FACTS --tasks-level all --n 1000 --kinds clean --batch $B --read cand2 \
  --sample-per-word 150 --sample-seed 0 > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; exit 1; }
$PY scripts/jsuite2_score.py $r --set $SET | grep -E "^facts \S+ +start=all" | sed "s/^/=== DOSE dsv4f /"
$PY scripts/soft_score.py $r --set $SET | sed "s/^/=== DOSE dsv4fSOFT /"
K=$(CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
import sys; sys.path[:0] = ['.', 'src']
from scripts import fig_neel as F
d = F.dose_data('DeepSeek-V4-Flash', 'dsv4f_', 'L18-23'); rd = F.dose_readings(d)
ok = [r for r in d if r['exc'] is not None and (rd['limit'] is None or r['k'] < rd['limit'])] or [r for r in d if r['exc'] is not None]
print(max(ok, key=lambda r: r['exc'])['k'])" 2>/dev/null)
echo "=== DS peak-excess K = $K $(date -u +%T)"
for mode in bridge question; do
  r=${P}${SET}_ko_cand2_L${BAND}_k${K}_pos${mode}_s150_v1
  [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: DeepSeek knock-out at L$BAND only at the $mode positions, K $K" \
    --plan bands --bands $BAND --positions $mode --conditions top$K top${K}_rot --tasks $SET --tasks-competence $C --tasks-words $FACTS --tasks-level all \
    --n 1000 --kinds clean --batch $B --read cand2 --sample-per-word 150 --sample-seed 0 > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; continue; }
  $PY scripts/jsuite2_score.py $r --set $SET | grep -E "^facts \S+ +start=all" | sed "s/^/=== POS dsv4f $mode /"
done
echo "=== DS done $(date -u +%FT%TZ)"
