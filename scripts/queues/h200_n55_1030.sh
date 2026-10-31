#!/bin/bash
# Zach (2026-10-30, prereg amendment 72 note 55): the paper's strengths, matched for generic damage (Fig. 22 + 24 on open
# models). Usage: h200_n55_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
#   Bands: the paper's medium and heavy (percent of depth 54-79 and 42-88, taken inward): 9B L17-24 / L14-27, 27B L35-49 /
#   L27-55, Lightning L28-40 / L22-44.
#   1. Smokes (moved to /workspace/scratch/n55): paper_ko_decomp --bands on 4 items per set; ablate_v2's v4 run on 2 items
#      per word. Skipped when the full runs exist.
#   2. scripts/paper_ko_decomp.py --bands: the paper's ML, MH, OO and its rhyme set PO under top3 / paper10 / top30,
#      pca3 / pca10 / pca30, unembed10 / unembed30, paper10_rot and paper10_pcasize at both bands, keep_T and keep_E (ML) /
#      keep_B (MH) / keep_S (PO) at medium; note 45's gate and reads; byte check against ablate_v2's recipe at both bands;
#      then the text stage (plain-text top-1 agreement, 64 WikiText rows and 64 v4 passages, scripts/removal_textloss.py).
#   3. v4 (note 20's knock-out exactly, as note 37's queue: gate, items, batch, cand2) at both bands under paper10,
#      paper10_rot, paper10_pcasize, unembed10, paper10_keepA, paper10_keepA_rot (--keepA-forms every).
#   4. The reader (scripts/paper_ko_read55.py), appended to /workspace/scratch/<prefix>note55.txt; its reading lines here.
#   BJ_GRAM_PROJ=1 as notes 37 and 45.
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; MED=17-24; HEAVY=14-27; KBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; MED=35-49; HEAVY=27-55; KBATCH=32 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; MED=28-40; HEAVY=22-44; KBATCH=16 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
W="Zach (2026-10-30, prereg amendment 72 note 55, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
SET=jsuite_v4_test_chat
STORED37=${P}${SET}_ko37_cand2_v1
[ -f results/ablate_v2/$STORED37/summary.json ] || { echo "=== note 37's run $STORED37 missing (its unedited rows are checked)"; exit 1; }
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
paper() {  # paper RUN WHY [EXTRA ARGS...]: note 55 on the paper's sets, then the text stage
  local r=$1 why=$2; shift 2
  go paper_ko_decomp $r $PY scripts/paper_ko_decomp.py --name $r --why "$W: $why" --sets ML MH OO PO \
    --bands medium=$MED heavy=$HEAVY --keep-band medium "$@"
}
CONDS="paper10 paper10_rot paper10_pcasize unembed10 paper10_keepA paper10_keepA_rot"
ko() {  # ko RUN N WHY: note 20's knock-out command (note 37's queue) at the paper's bands with note 55's v4 conditions
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $MED $HEAVY --conditions $CONDS --keepA-forms every \
    --tasks $SET --tasks-competence ${P}${SET}_competence_cand2_v1 --tasks-words MP MM --tasks-per-word --tasks-level all --n $n \
    --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 ${P}jsuite_v4_cv_v1
}
r=${P}n55_v1
v=${P}${SET}_ko55_cand2_v1
mkdir -p /workspace/scratch/n55
if [ ! -f results/paper_ko_decomp/$r/summary.json ] || [ ! -f results/ablate_v2/$v/summary.json ]; then
  sk=${P}n55_smoke1030
  paper $sk "smoke" --limit 4 || { echo "=== smoke FAILED"; exit 1; }
  mv results/paper_ko_decomp/$sk /workspace/scratch/n55/$sk-$(date -u +%H%M) 2>/dev/null
  vk=${P}${SET}_ko55_smoke1030
  ko $vk 2 "smoke" || { echo "=== v4 smoke FAILED"; exit 1; }
  mv results/ablate_v2/$vk /workspace/scratch/n55/$vk-$(date -u +%H%M) 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
paper $r "note 55, the paper's sets and the text metric at its medium and heavy strengths"
ko $v 1000 "note 55, v4 at the paper's medium and heavy strengths"
if [ -f results/paper_ko_decomp/$r/summary.json ]; then
  V4=""
  [ -f results/ablate_v2/$v/summary.json ] && V4="--v4 $v --v4-stored $STORED37"
  # shellcheck disable=SC2086
  .venv/bin/python scripts/paper_ko_read55.py results/paper_ko_decomp/$r $V4 > /workspace/scratch/${P}note55.part.txt 2>&1 \
    || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note55.part.txt; fails=$((fails + 1)); }
  { echo "=== $(date -u +%FT%TZ)"; cat /workspace/scratch/${P}note55.part.txt; } >> /workspace/scratch/${P}note55.txt
  grep -h "^reading\|^# note 55" /workspace/scratch/${P}note55.part.txt | cut -c1-500
fi
echo "=== n55 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
