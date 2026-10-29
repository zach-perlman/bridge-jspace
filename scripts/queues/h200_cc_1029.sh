#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 note 24): cue-conflict descriptions. Usage: h200_cc_1029.sh MODEL GPU WAITJOB [WAITJOB ...]
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; KB=12-16; KBATCH=32; CELLS="final 21-24
final 25-28
last 12-16" ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; KB=32-40; KBATCH=32; CELLS="final 49-56
last 24-31
last 32-40" ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; KB=27-33; KBATCH=16; CELLS="final 34-39
final 40-45
last 21-26" ;;
esac
W="Zach (2026-10-29, prereg amendment 58 note 24, $BJ_TARGET)"
SET=jsuite_v4cc_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4cc_cv_v1
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
fails=0
go() {  # go KIND RUN ARGS...
  local kind=$1 r=$2; shift 2
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
sm=${P}${SET}_competence_smoke1029
$PY scripts/natural_v1.py competence --set $SET --name $sm --words MP MM --read cand2 --hop1 gen --limit 8 --why "$W: smoke" \
  > /workspace/scratch/$sm.log 2>&1 < /dev/null || { echo "=== competence smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
mv results/tasks_v2/$sm /workspace/scratch/ 2>/dev/null
echo "=== smoke ok $(date -u +%T)"
go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words MP MM --read cand2 --hop1 gen --why "$W: competence"
go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: controls" --set jsuite_v4ctlcc_test_chat --words H1 RG RO --variants none
if [ ! -f results/tasks_v2/$C/summary.json ] || [ ! -f results/competence_variants/$CV/summary.json ]; then echo "=== no competence for $M"; exit 1; fi
C15="full_cf rem_cf remrand_cf remkeepown_cf noaown_cf noaownctl_cf remkeeprel_cf noarel_cf noarelctl_cf"
read -r s0 b0 <<< "$(echo "$CELLS" | head -1)"
# shellcheck disable=SC2086
go nn_swap ${P}nn_n24_smoke1029 $PY scripts/nn_swap.py --name ${P}nn_n24_smoke1029 --why "$W smoke" --set $SET --items v4ok --competence $C --cv-h1 $CV \
  --words MM --site $s0 --seed 0 --band $b0 --limit 2 --conds $C15 || exit 1
runs=""
while read -r site band; do
  for s in 0 1; do
    r=${P}nn_n24_${site}_MM_L${band}_s${s}_v1; runs="$runs $r"
    # shellcheck disable=SC2086
    go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: note 15's arms on cue-conflict items, $site / MM / L$band, donor seed $s" --set $SET \
      --items v4ok --competence $C --cv-h1 $CV --words MM --site $site --seed $s --band $band --conds $C15
  done
done <<< "$CELLS"
r=${P}${SET}_ko_cand2_v1
go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: note 20's knock-out on cue-conflict items" --plan bands --bands $KB \
  --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word \
  --tasks-level all --n 1000 --kinds clean --batch $KBATCH --read cand2 --tasks-v4-h1 $CV
echo "=== note 24 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
