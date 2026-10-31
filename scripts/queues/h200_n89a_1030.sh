#!/bin/bash
# Amendment 89 note 68 (2026-10-30): this copy of h200_n57d_1030.sh adds N57_CV (the codename set's control set is jsuite_v5alctl_cv_v1).
# Usage: N57_SET=jsuite_v5al_test_chat N57_CV=jsuite_v5alctl_cv_v1 bash h200_n89a_1030.sh 27b GPU
# Zach (2026-10-30, prereg amendment 83): note 57 (amendment 78, as scripts/queues/h200_n57_1030.sh: same conditions, band, gate,
# batch) on another v4 draw, with the draw's own competence ({P}{SET}_competence_cand2_v1) and control runs ({P}jsuite_v4p400X_cv_v1,
# as notes 43 / 48); the reader (--set) checks paper10 / paper10_rot against the draw's {P}{SET}_ko37_cand2_v1 run and prints
# "reading replication note57 ..." lines against draw 4001's labels.
# Usage: N57_SET=jsuite_v4p4002_test_chat bash h200_n57d_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b | 27b | nem35l
#
# Amendment 78 note 57: the controls the 9B's mechanism claims lacked, in ONE ablate_v2 run on v4 seed
# 4001 (jsuite_v4_test_chat) with note 49's settings (note 20's gate, band, batch, every position): paper10_onlyRperp (vs
# paper10_onlyA), top30 / top100 with keepA and the energy-matched random keepRE, ansRe (vs ansJ), paper10_keepRivals and
# paper10_keepRandRivals, each + _rot; each matching forward (paper10, topK, ansJ) runs before the condition it sizes. Every row
# carries edit_rel; n57_log.jsonl logs the matched sizes and energies. --topk-chunk 1024 as note 51. Then scripts/nn_ko57_read.py.
# Usage: h200_n57_1030.sh MODEL GPU [WAITJOB ...]   MODEL: 9b (amendment 78; 27b | nem35l also accepted)
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
SET=${N57_SET:?set N57_SET, e.g. jsuite_v4p4002_test_chat}
C=${P}${SET}_competence_cand2_v1; CV=${N57_CV:-${P}${SET%_test_chat}_cv_v1}; R37=${P}${SET}_ko37_cand2_v1
W="Zach (2026-10-30, prereg amendment 89 note 68: note 57 on $SET, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
for f in results/tasks_v2/$C/summary.json results/competence_variants/$CV/summary.json results/ablate_v2/$R37/summary.json; do
  [ -f $f ] || { echo "=== missing $f"; exit 1; }
done
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONDS="paper10 paper10_rot paper10_onlyA paper10_onlyA_rot paper10_onlyRperp paper10_onlyRperp_rot"
for k in 30 100; do CONDS="$CONDS top$k top${k}_rot top${k}_keepA top${k}_keepA_rot top${k}_keepRE top${k}_keepRE_rot"; done
CONDS="$CONDS ansJ ansJ_rot ansRe ansRe_rot paper10_keepRivals paper10_keepRivals_rot paper10_keepRandRivals paper10_keepRandRivals_rot"
ko() {  # ko RUN N WHY: note 20's knock-out command
  local r=$1 n=$2 why=$3
  # shellcheck disable=SC2086
  go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $KB --conditions $CONDS --keepA-forms every --topk-chunk 1024 \
    --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word --tasks-level all --n $n \
    --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 $CV
}
sk=${P}${SET}_ko57_smoke1030
ko $sk 2 "smoke" || { echo "=== smoke FAILED"; exit 1; }
mkdir -p /workspace/scratch/n49 && rm -rf /workspace/scratch/n49/$sk && mv results/ablate_v2/$sk /workspace/scratch/n49/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
ko ${P}${SET}_ko57_cand2_v1 1000 "amendment 89 note 68, note 57 on the codename set $SET (MP vs MM)"
O=/workspace/scratch/${P}${SET}_note57.txt
.venv/bin/python scripts/nn_ko57_read.py "$P" --set $SET >> $O 2>&1 || { echo "=== read FAILED"; tail -5 $O; fails=$((fails + 1)); }
grep -h "^reading\|energy matching\|stored check" $O | tail -14 | cut -c1-700
echo "=== n57d $M $SET done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
