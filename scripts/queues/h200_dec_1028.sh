#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 10): the paper's decomposition on v3. Usage: h200_dec_1028.sh GPU MODEL WAITJOB
set -u
G=$1; M=$2; WAIT=$3
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 10)"
case $M in
  27b) export BJ_TARGET=qwen3.6-27b; P=; BANDS="24-31 32-40" ;;
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; BANDS="12-16" ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; BANDS="21-26 27-33" ;;
esac
C=${P}jsuite_v3_test_chat_competence_cand2_v1
CONDS="full_insert lens_insert rem_insert remfix_insert lensrand_insert full_latent lens_latent rem_latent remfix_latent lensrand_latent"
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
for band in $BANDS; do
  for site in last span; do
    r=${P}nn_decomp_L${band}_${site}_v1
    echo "=== nn_swap/$r $(date -u +%T)"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: $BJ_TARGET decomposition, site $site, L$band" --band $band --site $site --competence $C \
      --words RM MM PM PK --sample-refs 150 --conds $CONDS > /workspace/scratch/$r.log 2>&1 < /dev/null \
      || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done
echo "=== dec [$G] $M done, $fails failed $(date -u +%FT%TZ)"
