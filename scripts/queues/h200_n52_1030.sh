#!/bin/bash
# Zach (2026-10-30, prereg amendment 72 note 52): note 44's spans residualised on jsuite_v5kn2c, as note 44: note 35's knock-out
# exactly (its band, --tasks-per-word --tasks-level all --n 1000, kinds clean step2, words MC MC0, the model's batch, cand2, v4_split's
# gate on jsuite_v5kn2cctl) under paper10, paper10_rot (rerun in-run), paper10_keepCapPerp, paper10_keepCtyPerp, paper10_keepShared.
# keeplog.jsonl logs E and rank per span. Then scripts/nn_ko52_read.py.
# Usage: h200_n52_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=32 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; KBATCH=16 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 72 note 52, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
MC=jsuite_v5kn2c_test_chat
CONDS="paper10 paper10_rot paper10_keepCapPerp paper10_keepCtyPerp paper10_keepShared"
ko() {  # ko RUN N WHY
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --tasks $MC \
    --tasks-competence ${P}${MC}_competence_cand2_v1 --tasks-words MC MC0 --tasks-per-word --tasks-level all --n $n --kinds clean step2 \
    --batch $KBATCH --read cand2 --tasks-v4-h1 ${P}jsuite_v5kn2cctl_cv_v1
}
sk=${P}${MC}_ko52_smoke1030
ko $sk 2 "smoke" || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n49 && rm -rf /workspace/scratch/n49/$sk && mv results/ablate_v2/$sk /workspace/scratch/n49/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko ${P}${MC}_ko52_cand2_v1 1000 "note 52: note 44's spans residualised (CapPerp, CtyPerp, Shared) on MC0 / MC"
.venv/bin/python scripts/nn_ko52_read.py "$P" >> /workspace/scratch/${P}note52.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note52.txt; fails=$((fails + 1)); }
grep -h "^reading\|note 44 beside" /workspace/scratch/${P}note52.txt | tail -4 | cut -c1-600
echo "=== n52 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
