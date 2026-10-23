#!/bin/bash
# Zach (2026-10-23, descriptive): the Muse diagnostic (scripts/muse_diag.py, amendment 6C's procedure) on the 122B, whose C1
# fails (gap 9 at L39-45, -3 at L24-30): is the bridge removed and rebuilt (redundant routes, as Muse), or kept / not in
# the lens? At both C1 bands (after-band ranks only exist for L24-30: L39-45 + 2 is past the lens). GPU 0.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0 BJ_TARGET=qwen3.5-122b-a10b
PY="uv run --no-sync python"
P=qwen35_122b_
WHY="Zach (2026-10-23, descriptive): the Muse diagnostic on the 122B"
C="--set full_v8_two --competence ${P}full_v8_two_competence_v1"
[ -f results/muse_diag/${P}diag_smoke_1023/summary.json ] || $PY scripts/muse_diag.py --name ${P}diag_smoke_1023 --why smoke --band 24-30 --n 2 $C > /dev/null 2>&1 \
  || { echo "=== smoke FAILED: stop"; exit 1; }
for B in 39-45 24-30; do
  echo "=== muse_diag/${P}diag_L${B}_v1 $(date -u +%T)"
  [ -f results/muse_diag/${P}diag_L${B}_v1/summary.json ] || $PY scripts/muse_diag.py --name ${P}diag_L${B}_v1 --why "$WHY, its C1 band L$B" --band $B --n 60 $C 2>&1 \
    | grep "^DIAG" || echo "=== diag L$B FAILED"
done
echo "=== 122B diag done $(date -u +%FT%TZ)"
