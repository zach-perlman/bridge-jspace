#!/bin/bash
# Zach (2026-10-29, prereg amendment 58 notes 15 addendum, 16, 18 on the 27B / Lightning). Usage: h200_rep_1029.sh MODEL GPU WAITJOB
set -u
M=$1; G=$2; WAIT=$3
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  27b) export BJ_TARGET=qwen3.6-27b; P=; LAST=57-62; BL="8-15 16-23 24-31 32-40"; BS="0-7 8-15 16-23 24-31 32-40"; BF="41-48 49-56 57-62" ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; LAST=46-50; BL="6-10 11-15 16-20 21-26"; BS="0-5 6-10 11-15 16-20 21-26"; BF="34-39 40-45 46-50" ;;
esac
W="Zach (2026-10-29, prereg amendment 58 notes 15a/16/18, $BJ_TARGET)"
SET=jsuite_v4_test_chat
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
S1=results/nn_swap/nn_cf_read/${P}v4_stage1.json
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
run() {  # run NAME ARGS...
  local r=$1; shift
  if [ -f results/nn_swap/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  $PY scripts/nn_swap.py --name $r --set $SET --items v4ok --competence $C --cv-h1 $CV "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null \
    || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
cells() {  # cells KIND: "site word band" lines from stage 1 (15a: MM hits at last/final minus the last window; 16: last, first two windows hit by both words)
  .venv/bin/python - "$S1" "$1" "L$LAST" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); kind, last = sys.argv[2], sys.argv[3]
hits = {(h["site"], h["word"], h["band"]) for h in d["hits"]}
key = lambda b: int(b[1:].split("-")[0])
if kind == "15a":
    for s, w, b in sorted(((s, w, b) for s, w, b in hits if w == "MM" and s in ("final", "last") and b != last), key=lambda t: (t[0] != "final", key(t[2]))):
        print(s, w, b[1:])
else:
    both = sorted({b for s, w, b in hits if s == "last" and w == "MP"} & {b for s, w, b in hits if s == "last" and w == "MM"}, key=key)[:2]
    print("final", "MM", last[1:])
    for w in ("MP", "MM"):
        for b in both:
            print("last", w, b[1:])
PY
}
C15A="full_cf lens_cf rem_cf lensshr_cf remshr_cf"; C16="full_cf jpp_cf jpprand_cf nojpp_cf nojpprand_cf"
# smokes (2 items each)
read -r s0 w0 b0 <<< "$(cells 15a | head -1)"
# shellcheck disable=SC2086
run ${P}nn_n15a_smoke1029 --why "$W smoke" --words $w0 --site $s0 --seed 0 --band $b0 --limit 2 --conds $C15A || exit 1
# shellcheck disable=SC2086
run ${P}nn_n16_smoke1029 --why "$W smoke" --words MM --site final --seed 0 --band $LAST --limit 2 --conds $C16 || exit 1
run ${P}nn_n18_smoke1029 --why "$W smoke" --words MP MM --site last --seed 0 --band ${BL%% *} --limit 2 --position-swap --conds full_cf lensrand_cf || exit 1
echo "=== smoke ok $(date -u +%T)"
for N in 15a 16; do
  CO=$C15A; [ $N = 16 ] && CO=$C16
  CELLS=$(cells $N); echo "=== note $N cells for $M: $(echo "$CELLS" | tr '\n' ';')"
  rs=""
  while read -r site word band; do
    [ -n "$site" ] || continue
    for s in 0 1; do
      r=${P}nn_n${N}_${site}_${word}_L${band}_s${s}_v1; rs="$rs $r"
      # shellcheck disable=SC2086
      run $r --why "$W: note $N, $site / $word / L$band, donor seed $s" --words $word --site $site --seed $s --band $band --conds $CO
    done
  done <<< "$CELLS"
  # shellcheck disable=SC2086
  .venv/bin/python scripts/nn_cf_read.py ${P}v4_n${N} $rs > /workspace/scratch/${P}v4_n${N}.txt 2>&1
  echo "=== note $N $M done $(date -u +%T)"
done
rs=""
for s in 0 1; do
  for site in last span final; do
    case $site in last) B=$BL ;; span) B=$BS ;; final) B=$BF ;; esac
    r=${P}nn_n18_${site}_s${s}_v1; rs="$rs $r"
    # shellcheck disable=SC2086
    run $r --why "$W: note 18, position swap, site $site, donor seed $s" --words MP MM --site $site --seed $s --sweep $B --position-swap --conds full_cf lensrand_cf
  done
done
# shellcheck disable=SC2086
{ .venv/bin/python scripts/nn_cf_read.py ${P}v4_n18 $rs; echo "--- all pairs (MM's reading)"; .venv/bin/python scripts/nn_cf_read.py ${P}v4_n18_all $rs --all-pairs; } > /workspace/scratch/${P}v4_n18.txt 2>&1
echo "=== notes 15a/16/18 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
