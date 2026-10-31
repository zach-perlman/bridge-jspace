#!/bin/bash
# Zach (2026-10-30, prereg amendment 62): DeepSeek-V4-Flash after Muse: drop Muse's weights (approved), download DeepSeek, then
# v4 competence / controls / knock-out (L18-23) / priming readout, the alias set and the named key set. Both GPUs.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1 BJ_GRAM_PROJ=1 BJ_TARGET=deepseek-v4-flash
PY="uv run --no-sync python"
P=dsv4f_; KB=18-23; KBATCH=16
W="Zach (2026-10-30, prereg amendment 62, DeepSeek-V4-Flash)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
MU=models--meta-models--Muse-Glimmer-30B
[ -d /workspace/hf_cache/hub/$MU ] && python3 /workspace/scratch/cache_drop.py $MU | sed "s/^/=== /"
free=$(df -BG --output=avail /workspace | tail -1 | tr -dc 0-9)
echo "=== DeepSeek download, $free GB free $(date -u +%T)"
CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
from huggingface_hub import snapshot_download
print('=== DS download done', snapshot_download('deepseek-ai/DeepSeek-V4-Flash', revision='60d8d70770c6776ff598c94bb586a859a38244f1'))" 2>&1 | grep "=== DS" || { echo "=== DS download FAILED"; exit 1; }
fails=0
go() {
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
battery() {  # battery SET CTL WORDS CTLWORDS
  local SET=$1 CTL=$2 words=$3 ctlw=$4
  local C=${P}${SET}_competence_cand2_v1 CV=${P}${CTL%_test_chat}_cv_v1
  local sm=${P}${SET}_competence_smoke1030
  # shellcheck disable=SC2086
  $PY scripts/natural_v1.py competence --set $SET --name $sm --words $words --read cand2 --hop1 gen --limit 8 --why "$W: smoke" > /workspace/scratch/$sm.log 2>&1 < /dev/null \
    || { echo "=== $SET smoke FAILED"; tail -5 /workspace/scratch/$sm.log; fails=$((fails + 1)); return 1; }
  mv results/tasks_v2/$sm /workspace/scratch/ 2>/dev/null; echo "=== $SET smoke ok $(date -u +%T)"
  # shellcheck disable=SC2086
  go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words $words --read cand2 --hop1 gen --why "$W: competence" || return 1
  # shellcheck disable=SC2086
  go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: controls" --set $CTL --words $ctlw --variants none || return 1
  local kinds="clean"; [ "$SET" = jsuite_v5kn2_test_chat ] && kinds="clean step2"
  local r=${P}${SET}_ko_cand2_v1
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: note 20's knock-out at L$KB" --plan bands --bands $KB \
    --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word \
    --tasks-level all --n 1000 --kinds $kinds --batch $KBATCH --read cand2 --tasks-v4-h1 $CV && .venv/bin/python scripts/nn_ko_read.py $r | cut -c1-400
  local tag=${SET#jsuite_}; tag=${tag%_test_chat}
  local rr=${P}nn_readout_${tag}prime_v1
  [ "$tag" = v4 ] || rr=${P}nn_readout_${tag}_v1
  go nn_readout $rr $PY scripts/nn_readout.py --name $rr --set $SET --competence $C --cv-h1 $CV --items v4 --priming --topk 20
}
battery jsuite_v4_test_chat jsuite_v4ctl_test_chat "MP MM" "H1 RG RO"
.venv/bin/python scripts/nn_priming_read.py $P > /workspace/scratch/${P}v4_n25.txt 2>&1 && tail -1 /workspace/scratch/${P}v4_n25.txt
battery jsuite_v5al_test_chat jsuite_v5alctl_test_chat "MP MM" "H1"
.venv/bin/python scripts/nn_v5_read.py alias $P > /workspace/scratch/${P}v5_alias.txt 2>&1; grep -h "reading" /workspace/scratch/${P}v5_alias.txt
battery jsuite_v5kn2_test_chat jsuite_v5kn2ctl_test_chat "MP MM" "H1 K0"
.venv/bin/python scripts/nn_v5_read.py key2 $P > /workspace/scratch/${P}v5_key2.txt 2>&1; grep -h "reading" /workspace/scratch/${P}v5_key2.txt
echo "=== DeepSeek amendment 62 done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
