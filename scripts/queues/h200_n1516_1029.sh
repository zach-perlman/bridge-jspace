#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 notes 15-16): on v4, Dan's 51.12 arms (note 15) and Dan's lens part (note 16).
# Usage: h200_n1516_1029.sh NOTE GPU WAITJOB MODEL
#   note 15: the recall twin (MM); 9B cells fixed in note 15; 27B: its MM stage-1 hits at last / final minus 57-62
#   note 16: 9B only; final MM L29-30 (positive check) first, then last MP / MM L4-7, L8-11
set -u
N=$1; G=$2; WAIT=$3; M=$4
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 58 note $N)"
SET=jsuite_v4_test_chat
case $M in
  27b) export BJ_TARGET=qwen3.6-27b; P= ;;
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_ ;;
esac
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
if [ "$N" = 15 ]; then
  CONDS="full_cf rem_cf remrand_cf remkeepown_cf noaown_cf noaownctl_cf remkeeprel_cf noarel_cf noarelctl_cf"
  if [ "$M" = 9b ]; then
    CELLS="final MM 21-24
final MM 25-28
last MM 4-7
last MM 8-11
last MM 12-16"
  else
    S1=results/nn_swap/nn_cf_read/${P}v4_stage1.json
    until [ -f $S1 ]; do sleep 120; done
    CELLS=$(.venv/bin/python - $S1 <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
hits = [(h["site"], h["band"][1:]) for h in d["hits"] if h["word"] == "MM" and h["site"] in ("final", "last") and h["band"] != "L57-62"]
for site, band in sorted(hits, key=lambda x: (x[0] != "final", int(x[1].split("-")[0]))):
    print(site, "MM", band)
PY
)
  fi
else
  CONDS="full_cf jpp_cf jpprand_cf nojpp_cf nojpprand_cf"
  CELLS="final MM 29-30
last MP 4-7
last MP 8-11
last MM 4-7
last MM 8-11"
fi
echo "=== note $N cells for $M: $(echo "$CELLS" | tr '\n' ';')"
fails=0; runs=""
while read -r site word band; do
  [ -n "$site" ] || continue
  for s in 0 1; do
    r=${P}nn_n${N}_${site}_${word}_L${band}_s${s}_v1
    runs="$runs $r"
    echo "=== $r $(date -u +%T)"
    if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; continue; fi
    # shellcheck disable=SC2086
    $PY scripts/nn_swap.py --name $r --why "$W: $BJ_TARGET $site / $word / L$band, donor seed $s" --set $SET --items v4ok \
      --competence $C --cv-h1 $CV --words $word --site $site --seed $s --band $band --conds $CONDS \
      > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
    echo "=== done $r $(date -u +%T)"
  done
done <<< "$CELLS"
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_cf_read.py ${P}v4_n${N} $runs > /workspace/scratch/${P}v4_n${N}.txt 2>&1
echo "=== note $N [$G] $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
