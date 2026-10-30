#!/bin/bash
# Zach (2026-10-30, prereg amendment 63 note 35 + addendum): MC and MC0 on jsuite_v5kn2c. Usage: h200_mc35_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 9b | 27b | nem35l. Per model: competence (MC MC0), controls (H1 C0), the knock-out exactly as the v5key2 named run
#   (h200_v5b_1029.sh's v4 branch: band, four conditions, --tasks-per-word --tasks-level all --n 1000, kinds clean step2,
#   the model's batch, cand2, v4_split's gate), the removal record + MC / MC0 margins, MP's margins, the reader.
#   Queued after DeepSeek (amendment 63 addenda).
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
esac
W="Zach (2026-10-30, prereg amendment 63 note 35 + addendum, MC MC0, $BJ_TARGET)"
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
SET=jsuite_v5kn2c_test_chat; CTL=jsuite_v5kn2cctl_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v5kn2cctl_cv_v1; R=${P}${SET}_ko_cand2_v1
RM=${P}${SET}_removed_v1; MG=${P}jsuite_v5kn2_test_chat_margins_v1
run() {
  go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words MC MC0 --read cand2 --hop1 gen --why "$W: competence" || return 1
  go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: controls" --set $CTL --words H1 C0 --variants none || return 1
  go ablate_v2 $R $PY scripts/ablate_v2.py --name $R --why "$W: note 20's knock-out" --plan bands --bands $KB \
    --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words MC MC0 --tasks-per-word \
    --tasks-level all --n 1000 --kinds clean step2 --batch $KBATCH --read cand2 --tasks-v4-h1 $CV || return 1
  go ablate_v2 $RM $PY scripts/nn_v5_mc_removed.py --name $RM --why "$W: answer exclusion (all positions, band layers) + margins" \
    --bands $KB --tasks $SET --tasks-competence $C --tasks-words MC MC0 --kinds clean step2 --tasks-v4-h1 $CV --n 1000 --batch $KBATCH --ko-run $R
  go ablate_v2 $MG $PY scripts/nn_v5_mc_removed.py --name $MG --why "$W: MP's margins (v5key2 named run's items)" --bands $KB \
    --tasks jsuite_v5kn2_test_chat --tasks-competence ${P}jsuite_v5kn2_test_chat_competence_cand2_v1 --tasks-words MP --kinds clean \
    --tasks-v4-h1 ${P}jsuite_v5kn2ctl_cv_v1 --n 1000 --batch $KBATCH --margin-only --ko-run ${P}jsuite_v5kn2_test_chat_ko_cand2_v1
}
run
.venv/bin/python scripts/nn_v5_mc_read.py "$P" > /workspace/scratch/${P}mc35.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}mc35.txt; fails=$((fails + 1)); }
grep -h "^reading" /workspace/scratch/${P}mc35.txt
echo "=== mc35 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
