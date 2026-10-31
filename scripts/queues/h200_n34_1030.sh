#!/bin/bash
# Zach (2026-10-30, prereg amendment 63 note 34 + addenda): the provenance probe's GPU extraction on jsuite_v5kc2, one
# model per call. Usage: h200_n34_1030.sh MODEL GPU [WAITJOB ...]   (MODEL: 9b | 27b | nem35l; GPU "" = CPU reader only)
#   With a GPU: scripts/nn_provenance.py (residuals at s1/s2/s3, J/R/U/Z, the claim read, H2 margins), then exit, so the
#   next GPU job in the chain starts. With GPU "": waits, then runs the CPU reader scripts/nn_provenance_read.py.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33 ;;
esac
W="Zach (2026-10-30, prereg amendment 63 note 34 + addenda: the provenance probe, $BJ_TARGET)"
N=${P}nn_provenance_kc2_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
if [ -n "$G" ]; then
  echo "=== nn_provenance/$N $(date -u +%T)"
  if [ -f results/nn_provenance/$N/summary.json ]; then echo "=== $N exists"; exit 0; fi
  $PY scripts/nn_provenance.py --name $N --why "$W" --band $KB --competence ${P}jsuite_v5kc2_test_chat_competence_cand2_v1 \
    > /workspace/scratch/$N.log 2>&1 < /dev/null || { echo "=== $N FAILED"; tail -5 /workspace/scratch/$N.log; exit 1; }
  echo "=== done $N $(date -u +%T)"
else
  [ -f results/nn_provenance/$N/summary.json ] || { echo "=== $N has no summary (extraction failed?)"; exit 1; }
  echo "=== reading $N $(date -u +%T)"
  .venv/bin/python scripts/nn_provenance_read.py $N --jobs 12 > /workspace/scratch/${N}_read.txt 2>&1 < /dev/null \
    || { echo "=== read FAILED"; tail -5 /workspace/scratch/${N}_read.txt; exit 1; }
  grep -i -E "^reading|lens|claim" /workspace/scratch/${N}_read.txt | head -12
  echo "=== n34 read $M done $(date -u +%FT%TZ)"
fi
