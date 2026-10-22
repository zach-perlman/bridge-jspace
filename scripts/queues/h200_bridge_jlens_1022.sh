#!/bin/bash
# Zach (2026-10-22): the 27B lens bridge for Muse, moved ahead on GPU 0 while Muse's weights wait for disk (Mistral was
# cancelled): the lens check on neuronpedia's published plain J-lens for Qwen3.6-27B (1000 prompts) and on the 27B's J++,
# then the 27B's C1 at 32-40 with the J-lens (docs/prereg_replication_1022.md, amendment 1).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )
WHY="Zach (2026-10-22): bridge for Muse Glimmer 30B's plain J-lens"
echo "=== start $(date -u +%FT%TZ)"
BJ_TARGET=qwen3.6-27b-jlens $PY scripts/lens_agreement.py --name q27jlens_lens_agreement_v1 --why "$WHY: the lens check on the 27B's plain J-lens" || echo "=== 27B J-lens check FAILED"
BJ_TARGET=qwen3.6-27b $PY scripts/lens_agreement.py --name lens_agreement_jpp_v1 --why "$WHY: the same check on the 27B's own J++" || echo "=== 27B J++ lens check FAILED"
echo "=== 27B C1 at 32-40 with the J-lens $(date -u +%T)"
BJ_TARGET=qwen3.6-27b-jlens $PY scripts/ablate_v2.py --name q27jlens_full2_ko_v1 \
  --why "$WHY: the 27B's C1 at 32-40 with neuronpedia's plain J-lens (the lens type Muse gets)" --plan bands \
  --bands 32-40 --conditions paper10$S paper10${S}_rot --tasks full_v8 --tasks-competence full_v8_competence_v1 \
  --tasks-words PP PM MP MM CP CM --tasks-level all --n 1000 --kinds clean --batch 32 \
  && BJ_TARGET=qwen3.6-27b-jlens $PY scripts/c1_v2.py q27jlens_full2_ko_v1 --middle L32-40 --set full_v8 --suffix "$S" | tail -2 || echo "=== 27B bridge FAILED"
echo "=== bridge done $(date -u +%FT%TZ)"
