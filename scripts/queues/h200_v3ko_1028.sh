#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 8): note 4's v3 removal matrix, relaunched with the normal-equations
# projection (BJ_GRAM_PROJ=1, amendment 52 note 1). Arguments unchanged from the 27 Oct launch. Usage: h200_v3ko_1028.sh GPU MODEL ...
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
SCENE="PK PM MK MM WK WM TK TM XK XM QK QM JK JM YK YM RM"
ALLW="JH JK JM MA MC MD ME MF MG MH MK MM MN MP PA PC PD PE PF PG PH PK PM PN PP QH QK QM RA RM RN TK TM WA WK WM WN XK XM YK YM"
rc=0
for m in "$@"; do
  case $m in
    27b) KEY=qwen3.6-27b; P=; BAND=32-40; B=32 ;;
    9b) KEY=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; B=32 ;;
    nem35l) KEY=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; B=16 ;;
    *) echo "=== unknown model $m"; rc=1; continue ;;
  esac
  r=${P}jsuite_v3_test_chat_ko_cand2_v1
  echo "=== ablate_v2/$r $(date -u +%T)"
  # shellcheck disable=SC2086
  BJ_TARGET=$KEY uv run --no-sync python scripts/ablate_v2.py --name $r \
    --why "Zach (2026-10-27, prereg amendment 58 note 4): $KEY v3 knock-out matrix (v1); relaunched with BJ_GRAM_PROJ=1 (note 8)" \
    --plan bands --bands $BAND --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks jsuite_v3_test_chat \
    --tasks-competence ${P}jsuite_v3_test_chat_competence_cand2_v1 --tasks-words $ALLW --tasks-scene-words $SCENE --tasks-level all \
    --n 1000 --kinds clean --batch $B --read cand2 || { echo "=== $r FAILED"; rc=1; }
  echo "=== done $r $(date -u +%T)"
done
exit $rc
