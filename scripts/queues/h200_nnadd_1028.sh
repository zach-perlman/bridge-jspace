#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 9 addendum): final clause only + necessity at the site. Usage: h200_nnadd_1028.sh GPU MODEL WAITJOB
set -u
G=$1; M=$2; WAIT=$3
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 9 addendum)"
case $M in
  27b) export BJ_TARGET=qwen3.6-27b; P=; BAND=32-40 ;;
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; BAND=12-16 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; BAND=27-33 ;;
esac
C=${P}jsuite_v3_test_chat_competence_cand2_v1
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
go() {
  local d=$1 r=$2; shift 2
  echo "=== $d/$r $(date -u +%T)"
  if [ -f results/$d/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
go competence_variants ${P}jsuite_v3fc_cv_v1 $PY scripts/competence_variants.py --name ${P}jsuite_v3fc_cv_v1 --set jsuite_v3fc_test_chat \
  --words FC --variants none --why "$W: $BJ_TARGET final clause only"
for site in last final; do
  go nn_swap ${P}nn_swap_L${BAND}_${site}_remove_v1 $PY scripts/nn_swap.py --name ${P}nn_swap_L${BAND}_${site}_remove_v1 \
    --why "$W: $BJ_TARGET necessity at the site ($site)" --band $BAND --site $site --competence $C --conds remove_k10 remove_k10_rot
done
echo "=== nnadd [$G] $M done, $fails failed $(date -u +%FT%TZ)"
