#!/bin/bash
# Zach (2026-10-30, prereg amendment 68 note 43): note 37 on a held-out v4 data draw, jsuite_v4p4002 (seed 4002).
# Usage: h200_n43_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
#   Pipeline as note 20's (scripts/queues/h200_v4_1028.sh): competence (MP MM, cand2, hop 1 by generation) and the controls
#   (H1 RG RO on jsuite_v4p4002ctl_test_chat; nn_swap.v4_split maps the draw to it since note 43's fix), then the knock-out
#   exactly as note 37's (band, --tasks-per-word --tasks-level all --n 1000, kinds clean, the model's batch, cand2, the v4
#   gate) under note 37's conditions (--keepA-forms every), plus note 41's keepR / R2 / R4 (+ _rot) and ansR (+ _rot) only if
#   note 41's code is in the committed HEAD when this queue reaches the knock-out (the note's condition). Then the readers:
#   nn_ko37_read --set, nn_ko41_read --set (if note 41's conditions ran) and nn_ko43_read (against seed 4001's readings).
#   Smokes first: competence on 8 items; a 2-item knock-out on every model (the draw's gate has not been smoked).
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
W="Zach (2026-10-30, prereg amendment 68 note 43, $BJ_TARGET)"
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
SET=jsuite_v4p4002_test_chat; CTL=jsuite_v4p4002ctl_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4p4002_cv_v1; R=${P}${SET}_ko37_cand2_v1
mkdir -p /workspace/scratch/n43
sm=${P}${SET}_competence_smoke1030
go tasks_v2 $sm $PY scripts/natural_v1.py competence --set $SET --name $sm --words MP MM --read cand2 --hop1 gen --limit 8 --why "$W: smoke" \
  || { echo "=== competence smoke FAILED"; exit 1; }
mv results/tasks_v2/$sm /workspace/scratch/n43/ 2>/dev/null
go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words MP MM --read cand2 --hop1 gen --why "$W: competence"
go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: controls (closed-book hop 1, recognition, role noun only)" \
  --set $CTL --words H1 RG RO --variants none
if [ ! -f results/tasks_v2/$C/summary.json ] || [ ! -f results/competence_variants/$CV/summary.json ]; then echo "=== no competence for $M"; exit 1; fi
CONDS="paper10 paper10_rot paper10_keepA paper10_keepA_rot ansJ ansJ_rot ansU"
N41=0
if git show HEAD:scripts/ablate_v2.py 2>/dev/null | grep -q '"paper10_keepR4_rot"'; then
  CONDS="$CONDS paper10_keepR paper10_keepR_rot paper10_keepR2 paper10_keepR2_rot paper10_keepR4 paper10_keepR4_rot ansR ansR_rot"; N41=1
fi
echo "=== note 41 conditions included: $N41 ($(git rev-parse --short HEAD))"
ko() {  # ko RUN N WHY
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --keepA-forms every \
    --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --n $n --kinds clean --batch $KBATCH \
    --read cand2 --tasks-v4-h1 $CV
}
sk=${P}${SET}_ko37_smoke1030
ko $sk 2 "smoke" || { echo "=== knock-out smoke FAILED"; exit 1; }
mv results/ablate_v2/$sk /workspace/scratch/n43/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko $R 1000 "note 43, note 37 (and note 41 if included) on the held-out draw jsuite_v4p4002"
: > /workspace/scratch/${P}note43.txt
rd() { "$@" >> /workspace/scratch/${P}note43.txt 2>&1 || { echo "=== read FAILED: $*"; tail -5 /workspace/scratch/${P}note43.txt; fails=$((fails + 1)); }; }
rd .venv/bin/python scripts/nn_ko37_read.py "$P" --set $SET
[ "$N41" = 1 ] && rd .venv/bin/python scripts/nn_ko41_read.py "$P" --set $SET --run-a $R --run-n37 $R
rd .venv/bin/python scripts/nn_ko43_read.py "$P"
grep -h "reading\|note 43\|headline" /workspace/scratch/${P}note43.txt | cut -c1-400
echo "=== n43 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
