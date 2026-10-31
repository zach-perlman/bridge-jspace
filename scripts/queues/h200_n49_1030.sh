#!/bin/bash
# Zach (2026-10-30, prereg amendment 72 notes 49 + 50): the paper's output protection sealed (protF, protC, keepT10, keepRT10,
# keepOwn, keepSib) and the orthogonal placebo / exact complement / rank-matched ansR (keepR4perp, keepR8perp, onlyA, ansRk), each
# + _rot, in ONE ablate_v2 run per model on v4 seed 4001 (jsuite_v4_test_chat), as note 41's run A: note 20's knock-out exactly
# (its band, --tasks-per-word --tasks-level all --n 1000, kinds clean, the model's batch, cand2, v4_split's gate, every position),
# paper10 / paper10_rot rerun in-run (checked against note 41's stored rows by the reader). keeplog.jsonl logs E_X, alpha_X, the
# protections' still-removed answer part, ranks; every row carries edit_rel (|edit|^2 / |h|^2). Then scripts/nn_ko49_read.py.
# Usage: h200_n49_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
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
W="Zach (2026-10-30, prereg amendment 72 notes 49 + 50, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
SET=jsuite_v4_test_chat
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONDS="paper10 paper10_rot"
for x in protF protC keepT10 keepRT10 keepOwn keepSib keepR4perp keepR8perp onlyA; do CONDS="$CONDS paper10_$x paper10_${x}_rot"; done
CONDS="$CONDS ansRk ansRk_rot"
ko() {  # ko RUN N WHY: note 20's knock-out command
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --keepA-forms every \
    --tasks $SET --tasks-competence ${P}${SET}_competence_cand2_v1 --tasks-words MP MM --tasks-per-word --tasks-level all --n $n \
    --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 ${P}jsuite_v4_cv_v1
}
sk=${P}${SET}_ko49_smoke1030
ko $sk 2 "smoke" || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n49 && rm -rf /workspace/scratch/n49/$sk && mv results/ablate_v2/$sk /workspace/scratch/n49/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko ${P}${SET}_ko49_cand2_v1 1000 "notes 49 + 50: protection sealed, orthogonal placebo, onlyA, ansRk on v4 (MP vs MM)"
.venv/bin/python scripts/nn_ko49_read.py "$P" >> /workspace/scratch/${P}note49.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note49.txt; fails=$((fails + 1)); }
grep -h "^reading\|stored check" /workspace/scratch/${P}note49.txt | tail -12 | cut -c1-600
echo "=== n49 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
