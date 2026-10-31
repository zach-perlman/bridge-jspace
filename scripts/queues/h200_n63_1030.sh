#!/bin/bash
# Zach (2026-10-30, prereg amendment 86 note 63): the mechanism beyond country answers. Note 57's battery (amendment 78, as
# scripts/queues/h200_n57_1030.sh: band, batch, every position, --keepA-forms every, --topk-chunk 1024) plus note 37's
# paper10_keepA / _rot (its K reading) in ONE ablate_v2 run on jsuite_v2_test_chat (MP vs MM, every relation; the reader splits
# them post hoc into the non-country relations (animals, countries -> continent, languages) and the country-type ones, beside).
# Conditions (the note's list): paper10, paper10_keepA, paper10_onlyA, paper10_onlyRperp, top30 / top100 with keepA and keepRE,
# ansJ, ansRe, each + _rot; each matching forward (paper10, topK, ansJ) runs before the condition it sizes. Not run: note 57's
# keepRivals / keepRandRivals (not in note 63's list).
# Gate: the v2 competence run ({P}jsuite_v2_test_chat_competence_cand2_v1; cand2) per word (--tasks-per-word, level all: whole,
# hop 1 and hop 2 right). Note 20's v4_split (--tasks-v4-h1) needs a v4 control set and an H1 competence_variants run that v2
# lacks; its other rule (the no-description guess wrong) is applied post hoc by the reader (scripts/nn_ko63_read.py).
# Then the reader; it checks paper10 / paper10_rot / none against the stored {P}jsuite_v2_test_chat_ko_cand2_v1 rows.
# Usage: h200_n63_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b (primary) | 27b | nem35l (confirmatory)
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
SET=jsuite_v2_test_chat
C=${P}${SET}_competence_cand2_v1
W="Zach (2026-10-30, prereg amendment 86 note 63, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
[ -f results/tasks_v2/$C/summary.json ] || { echo "=== missing results/tasks_v2/$C"; exit 1; }
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONDS="paper10 paper10_rot paper10_keepA paper10_keepA_rot paper10_onlyA paper10_onlyA_rot paper10_onlyRperp paper10_onlyRperp_rot"
for k in 30 100; do CONDS="$CONDS top$k top${k}_rot top${k}_keepA top${k}_keepA_rot top${k}_keepRE top${k}_keepRE_rot"; done
CONDS="$CONDS ansJ ansJ_rot ansRe ansRe_rot"
ko() {  # ko RUN N WHY: note 57's knock-out command on v2 (per-word gate; no v4 H1 gate)
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --keepA-forms every --topk-chunk 1024 \
    --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --n $n \
    --kinds clean --batch $KBATCH --read cand2
}
sk=${P}${SET}_ko63_smoke1030
if [ ! -d /workspace/scratch/n63/$sk ]; then  # smoke: 4 items per word (8 items)
  ko $sk 4 "smoke" || { echo "=== smoke FAILED"; exit 1; }
  mkdir -p /workspace/scratch/n63 && mv results/ablate_v2/$sk /workspace/scratch/n63/ 2>/dev/null
fi
echo "=== smoke ok $(date -u +%T)"
[ -n "${N63_SMOKE_ONLY:-}" ] && { .venv/bin/python scripts/nn_ko63_read.py "$P" --run-dir /workspace/scratch/n63/$sk --out-dir /workspace/scratch/n63 || fails=$((fails + 1)); echo "=== n63 $M smoke only, $fails failed"; [ "$fails" = 0 ]; exit; }
ko ${P}${SET}_ko63_cand2_v1 1000 "note 63: note 57's battery + keepA on v2's relations (MP vs MM), read per relation"
.venv/bin/python scripts/nn_ko63_read.py "$P" >> /workspace/scratch/${P}note63.txt 2>&1 || { echo "=== read FAILED"; tail -5 /workspace/scratch/${P}note63.txt; fails=$((fails + 1)); }
grep -h "^reading\|stored check" /workspace/scratch/${P}note63.txt | tail -20 | cut -c1-700
echo "=== n63 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
