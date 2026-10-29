#!/bin/bash
# Zach (2026-10-29, prereg amendment 59 note 28): Muse Glimmer 30B on v4. Usage: h200_muse_v4_1029.sh ROLE GPU [SEEDS] [WAITJOB ...]
#   a: competence, controls, readout map, note 20's knock-out (L36-42, L26-32), stage 1 at sites last and final (seeds 0 1)
#   b: stage 1 at site span (seeds 0 1), once a's competence and controls exist
#   d: (after a) note 25's priming, the cue-conflict competence and controls, note 26, note 17's value swap at site last
#   c: (after a and b) stage 2 at stage 1's cells, for the donor seeds given (e.g. "0" or "1")
set -u
ROLE=$1; G=$2; shift 2
SEEDS="0 1"; if [ "$ROLE" = c ]; then SEEDS=$1; shift; fi
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1 BJ_TARGET=muse-glimmer-30b
PY="uv run --no-sync python"
W="Zach (2026-10-29, prereg amendment 59 note 28, Muse Glimmer 30B)"
P=muse30_; SET=jsuite_v4_test_chat; WINS="0-5 6-11 12-17 18-23 24-29 30-35 36-41 42-47 48-50"
C=${P}${SET}_competence_cand2_v1; CV=${P}jsuite_v4_cv_v1
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
map() {  # map SITE SEED
  local r=${P}nn_cf_$1_s$2_v1
  # shellcheck disable=SC2086
  go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: counterfactual map, site $1, donor seed $2" --set $SET --items v4ok \
    --competence $C --cv-h1 $CV --words MP MM --site $1 --seed $2 --sweep $WINS --conds full_cf lensrand_cf
}
stage1() {
  local runs=""
  for site in last span final; do for s in 0 1; do [ -f results/nn_swap/${P}nn_cf_${site}_s${s}_v1/summary.json ] && runs="$runs ${P}nn_cf_${site}_s${s}_v1"; done; done
  # shellcheck disable=SC2086
  .venv/bin/python scripts/nn_cf_read.py ${P}v4_stage1 $runs > /workspace/scratch/${P}v4_stage1.txt 2>&1
}
case $ROLE in
a)
  sm=${P}${SET}_competence_smoke1029
  $PY scripts/natural_v1.py competence --set $SET --name $sm --words MP MM --read cand2 --hop1 gen --limit 8 --why "$W: smoke" \
    > /workspace/scratch/$sm.log 2>&1 < /dev/null || { echo "=== Muse smoke FAILED"; tail -5 /workspace/scratch/$sm.log; exit 3; }
  mv results/tasks_v2/$sm /workspace/scratch/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
  go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words MP MM --read cand2 --hop1 gen --why "$W: competence"
  go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: controls (closed-book hop 1, recognition, role noun only)" \
    --set jsuite_v4ctl_test_chat --words H1 RG RO --variants none
  if [ ! -f results/tasks_v2/$C/summary.json ] || [ ! -f results/competence_variants/$CV/summary.json ]; then echo "=== no competence for Muse"; exit 1; fi
  go nn_readout ${P}nn_readout_v4_v1 $PY scripts/nn_readout.py --name ${P}nn_readout_v4_v1 --set $SET --competence $C --cv-h1 $CV --items v4
  for KB in 36-42 26-32; do
    r=${P}${SET}_ko_L${KB}_cand2_v1
    go ablate_v2 $r $PY scripts/ablate_v2.py --name $r --why "$W: note 20's knock-out at L$KB" --plan bands --bands $KB \
      --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence $C --tasks-words MP MM --tasks-per-word \
      --tasks-level all --n 1000 --kinds clean --batch 16 --read cand2 --tasks-v4-h1 $CV && .venv/bin/python scripts/nn_ko_read.py $r
  done
  for site in last final; do for s in 0 1; do map $site $s; done; done
  stage1
  ;;
b)
  echo "=== waiting for Muse's competence and controls $(date -u +%T)"
  until [ -f results/tasks_v2/$C/summary.json ] && [ -f results/competence_variants/$CV/summary.json ]; do sleep 60; done
  for s in 0 1; do map span $s; done
  ;;
d)
  stage1
  go nn_readout ${P}nn_readout_v4prime_v1 $PY scripts/nn_readout.py --name ${P}nn_readout_v4prime_v1 --set $SET --competence $C --cv-h1 $CV --items v4 --priming \
    && .venv/bin/python scripts/nn_priming_read.py $P > /workspace/scratch/${P}v4_n25.txt 2>&1 && tail -1 /workspace/scratch/${P}v4_n25.txt
  CC=${P}jsuite_v4cc_test_chat_competence_cand2_v1; CCV=${P}jsuite_v4cc_cv_v1
  go tasks_v2 $CC $PY scripts/natural_v1.py competence --set jsuite_v4cc_test_chat --name $CC --words MP MM --read cand2 --hop1 gen --why "$W: cue-conflict competence"
  go competence_variants $CCV $PY scripts/competence_variants.py --name $CCV --why "$W: cue-conflict controls" --set jsuite_v4ctlcc_test_chat --words H1 RG RO --variants none
  bash scripts/queues/h200_pack_1029.sh muse $G || fails=$((fails + 1))
  B=$(.venv/bin/python -c "
import json; d = json.load(open('results/nn_swap/nn_cf_read/${P}v4_stage1.json'))
print(' '.join(sorted({h['band'][1:] for h in d['hits'] if h['site'] == 'last' and h['word'] == 'MP'}, key=lambda b: int(b.split('-')[0]))))")
  echo "=== value swap bands (stage 1 last MP hits): $B"
  runs=""
  for s in 0 1; do
    r=${P}nn_n17_last_s${s}_v1; runs="$runs $r"
    # shellcheck disable=SC2086
    [ -n "$B" ] && go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: note 17 value swap, site last, donor seed $s" --set $SET --items v4ok \
      --competence $C --cv-h1 $CV --words MP MM --site last --seed $s --sweep $B --value-swap --conds full_cf lensrand_cf
  done
  # shellcheck disable=SC2086
  { .venv/bin/python scripts/nn_cf_read.py ${P}v4_n17 $runs; echo "--- all pairs"; .venv/bin/python scripts/nn_cf_read.py ${P}v4_n17_all $runs --all-pairs; } > /workspace/scratch/${P}v4_n17.txt 2>&1
  ;;
c)
  stage1
  cells=$(.venv/bin/python - "${P}v4_stage1" <<'PYEOF'
import json, sys
d = json.load(open(f"results/nn_swap/nn_cf_read/{sys.argv[1]}.json"))
hits = {(h["site"], h["word"], h["band"]) for h in d["hits"]}
for word in ("MP", "MM"):
    if not any(w == word for _, w, _ in hits):
        cand = [(v["donor"].get("full_cf", 0), k) for k, v in d["cells"].items() if k.split("/")[1] == word]
        if cand:
            site, w, band = max(cand)[1].split("/")
            hits.add((site, w, band))
for site, word, band in sorted(hits):
    print(site, word, band[1:])
PYEOF
)
  echo "=== stage 2 cells: $(echo $cells | tr '\n' ' ')"
  while read -r site word band; do
    [ -n "$site" ] || continue
    for s in $SEEDS; do
      r=${P}nn_cfdec_${site}_${word}_L${band}_s${s}_v1
      go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: decomposition at $site / $word / L$band, donor seed $s" --set $SET \
        --items v4ok --competence $C --cv-h1 $CV --words $word --site $site --seed $s --band $band --conds full_cf lens_cf rem_cf remfix_cf lensrand_cf
    done
  done <<< "$cells"
  ;;
esac
echo "=== Muse note 28 role $ROLE done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
