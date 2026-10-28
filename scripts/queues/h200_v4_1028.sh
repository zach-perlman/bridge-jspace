#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 14): jsuite_v4, the counterfactual-patching map and the readout map.
# Usage: h200_v4_1028.sh GPU WAITJOB MODEL [MODEL ...]
#   per model: competence (MP MM), the controls (H1 RG RO), the readout map, stage 1 (full_cf / lensrand_cf at every
#   layer window, sites last / span / final, donor seeds 0 1), then stage 2 (note 10's decomposition at the cells stage 1
#   finds; if none for a word, at that word's largest full_cf cell, descriptive)
set -u
G=$1; WAIT=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 14)"
SET=jsuite_v4_test_chat
echo "=== waiting for $WAIT $(date -u +%T)"
until grep -qsE "^EXIT [0-9]+" /workspace/runs/$WAIT.log; do sleep 60; done
fails=0
go() {  # go KIND RUN ARGS...: skip a run whose summary exists; log to scratch
  local kind=$1 r=$2; shift 2
  echo "=== $kind/$r $(date -u +%T)"
  if [ -f results/$kind/$r/summary.json ]; then echo "=== $r exists"; return; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return; }
  echo "=== done $r $(date -u +%T)"
}
for M in "$@"; do
  case $M in
    27b) export BJ_TARGET=qwen3.6-27b; P=; WINS="0-7 8-15 16-23 24-31 32-40 41-48 49-56 57-63" ;;
    9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; WINS="0-3 4-7 8-11 12-16 17-20 21-24 25-28 29-31" ;;
    nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; WINS="0-5 6-10 11-15 16-20 21-26 27-33 34-39 40-45 46-51" ;;
  esac
  C=${P}${SET}_competence_cand2_v1
  CV=${P}jsuite_v4_cv_v1
  go tasks_v2 $C $PY scripts/natural_v1.py competence --set $SET --name $C --words MP MM --read cand2 --hop1 gen --why "$W: $BJ_TARGET v4 competence"
  go competence_variants $CV $PY scripts/competence_variants.py --name $CV --why "$W: $BJ_TARGET v4 controls (closed-book hop 1, recognition, role noun only)" \
    --set jsuite_v4ctl_test_chat --words H1 RG RO --variants none
  if [ ! -f results/tasks_v2/$C/summary.json ] || [ ! -f results/competence_variants/$CV/summary.json ]; then
    echo "=== no competence for $M: skipping its maps"; fails=$((fails + 1)); continue
  fi
  go nn_readout ${P}nn_readout_v4_v1 $PY scripts/nn_readout.py --name ${P}nn_readout_v4_v1 --set $SET --competence $C --cv-h1 $CV --items v4
  runs=""
  for site in last span final; do
    for s in 0 1; do
      r=${P}nn_cf_${site}_s${s}_v1
      runs="$runs $r"
      # shellcheck disable=SC2086
      go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: $BJ_TARGET counterfactual map, site $site, donor seed $s" --set $SET --items v4ok \
        --competence $C --cv-h1 $CV --words MP MM --site $site --seed $s --sweep $WINS --conds full_cf lensrand_cf
    done
  done
  # stage 2: the cells stage 1 finds (else each word's largest full_cf cell, descriptive)
  # shellcheck disable=SC2086
  .venv/bin/python scripts/nn_cf_read.py ${P}v4_stage1 $runs > /workspace/scratch/${P}v4_stage1.txt 2>&1
  cells=$(.venv/bin/python - "${P}v4_stage1" <<'EOF'
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
EOF
)
  echo "=== stage 2 cells for $M: $(echo $cells | tr '\n' ' ')"
  while read -r site word band; do
    [ -n "$site" ] || continue
    for s in 0 1; do
      r=${P}nn_cfdec_${site}_${word}_L${band}_s${s}_v1
      go nn_swap $r $PY scripts/nn_swap.py --name $r --why "$W: $BJ_TARGET decomposition at $site / $word / L$band, donor seed $s" --set $SET \
        --items v4ok --competence $C --cv-h1 $CV --words $word --site $site --seed $s --band $band \
        --conds full_cf lens_cf rem_cf remfix_cf lensrand_cf
    done
  done <<< "$cells"
done
echo "=== v4 [$G] $* done, $fails failed $(date -u +%FT%TZ)"
