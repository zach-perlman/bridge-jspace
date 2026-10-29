#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 notes 15 and 17, Lightning addendum). Usage: h200_n15n17L_1029.sh GPU WAITJOB
set -u
G=$1; WAIT=$2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1 BJ_TARGET=nemotron-3.5-lightning
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 58 notes 15 and 17, Lightning addendum)"
SET=jsuite_v4_test_chat; P=nem35l_
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
C15="full_cf rem_cf remrand_cf remkeepown_cf noaown_cf noaownctl_cf remkeeprel_cf noarel_cf noarelctl_cf"
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
run() {  # run NAME ARGS...
  local r=$1; shift
  if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; return; fi
  $PY scripts/nn_swap.py --name $r --set $SET --items v4ok --competence $C --cv-h1 $CV "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
# shellcheck disable=SC2086
run ${P}nn_n15_smoke1029 --why "$W smoke" --words MM --site final --seed 0 --band 40-45 --limit 2 --conds $C15 || exit 1
run ${P}nn_n17_smoke1029 --why "$W smoke" --words MP MM --site last --seed 0 --band 11-15 --limit 2 --value-swap --conds full_cf lensrand_cf || exit 1
echo "=== smoke ok $(date -u +%T)"
CELLS=$(.venv/bin/python - results/nn_swap/nn_cf_read/${P}v4_stage1.json <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
hits = [(h["site"], h["band"][1:]) for h in d["hits"] if h["word"] == "MM" and h["site"] in ("final", "last") and h["band"] != "L46-50"]
for site, band in sorted(hits, key=lambda x: (x[0] != "final", int(x[1].split("-")[0]))):
    print(site, band)
PY
)
echo "=== note 15 cells for nem35l: $(echo "$CELLS" | tr '\n' ';')"
r15=""
while read -r site band; do
  [ -n "$site" ] || continue
  for s in 0 1; do
    r=${P}nn_n15_${site}_MM_L${band}_s${s}_v1; r15="$r15 $r"
    # shellcheck disable=SC2086
    run $r --why "$W: note 15, $site / MM / L$band, donor seed $s" --words MM --site $site --seed $s --band $band --conds $C15
  done
done <<< "$CELLS"
# shellcheck disable=SC2086
.venv/bin/python scripts/nn_cf_read.py ${P}v4_n15 $r15 > /workspace/scratch/${P}v4_n15.txt 2>&1
echo "=== note 15 nem35l done $(date -u +%T)"
r17=""
for s in 0 1; do
  for site in last span final; do
    case $site in last) B="6-10 11-15 16-20 21-26" ;; span) B="0-5 6-10 11-15 16-20 21-26" ;; final) B="34-39 40-45 46-50" ;; esac
    r=${P}nn_n17_${site}_s${s}_v1; r17="$r17 $r"
    # shellcheck disable=SC2086
    run $r --why "$W: note 17, value swap, site $site, donor seed $s" --words MP MM --site $site --seed $s --sweep $B --value-swap --conds full_cf lensrand_cf
  done
done
# shellcheck disable=SC2086
{ .venv/bin/python scripts/nn_cf_read.py ${P}v4_n17 $r17; echo "--- all pairs (MM's reading)"; .venv/bin/python scripts/nn_cf_read.py ${P}v4_n17_all $r17 --all-pairs; } > /workspace/scratch/${P}v4_n17.txt 2>&1
echo "=== notes 15+17 nem35l done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
