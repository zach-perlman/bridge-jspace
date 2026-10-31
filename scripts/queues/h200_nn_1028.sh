#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 9): the never-named program. Usage: h200_nn_1028.sh GPU STEP:MODEL ...
# Steps: ministral:x (Ministral's v3 removal matrix, note 6) | probes (clue-only questions, second wording) |
#        contrast (composed vs each hop alone, ablate_v2 --kinds clean step1 step2) | readout |
#        sweep (windows across depth, sites last and final, transplant + random subspace, 80 items per word) |
#        full (the band: site last with every condition at k 10 30 100; sites span, qmark, final at k 10) |
#        best (each swept site's best window other than the band) | all (probes contrast readout sweep full best).
# Models: 27b 9b nem35l.
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 9)"
SET=jsuite_v3_test_chat
SCENE="PK PM MK MM WK WM TK TM XK XM QK QM JK JM YK YM RM"
ALLW="JH JK JM MA MC MD ME MF MG MH MK MM MN MP PA PC PD PE PF PG PH PK PM PN PP QH QK QM RA RM RN TK TM WA WK WM WN XK XM YK YM"
K10="insert_k10 insert_k10_rand insert_k10_rot insert_k10_u latent_k10 latent_k10_rand latent_k10_rot latent_k10_u clamp clamp_null"
fails=0
model() {
  case $1 in
    27b) KEY=qwen3.6-27b; P=; BAND=32-40; B=32; WINS="8-15 16-23 24-31 32-40 41-48 49-56 57-62" ;;
    9b) KEY=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; B=32; WINS="4-7 8-11 12-16 17-20 21-24 25-28" ;;
    nem35l) KEY=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; B=16; WINS="6-10 11-15 16-20 21-26 27-33 34-39 40-45 46-50" ;;
    *) echo "=== unknown model $1"; return 1 ;;
  esac
  export BJ_TARGET=$KEY
  C=${P}${SET}_competence_cand2_v1
}
go() {  # go DIR RUN CMD...: once (skipped if DIR/RUN/summary.json exists), logged to scratch
  local d=$1 r=$2; shift 2
  echo "=== $d/$r $(date -u +%T)"
  if [ -f results/$d/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
best_window() {  # best_window SITE: the swept window (not the band) with the largest RM insert_k10 transfer
  .venv/bin/python -c '
import json, sys
p, band, site = sys.argv[1], sys.argv[2], sys.argv[3]
s = json.load(open(f"results/nn_swap/{p}nn_swap_sweep_{site}_v1/summary.json"))
cells = {k.split("/")[0][1:]: v["transfer"] for k, v in s.items() if k.endswith("/RM/insert_k10") and v.get("n")}
cells.pop(band, None)
print(max(cells, key=cells.get) if cells else "")' "$P" "$BAND" "$1"
}
run_step() {
  local kind=$1 m=$2
  if [ "$kind" = ministral ]; then
    export BJ_TARGET=ministral-3-14b
    # shellcheck disable=SC2086
    go ablate_v2 min14_${SET}_ko_cand2_v1 $PY scripts/ablate_v2.py --name min14_${SET}_ko_cand2_v1 \
      --why "Zach (2026-10-28, prereg amendment 58 note 6; run at Zach's go, 28 Oct): ministral-3-14b v3 knock-out matrix (v1)" --plan bands --bands 32-37 \
      --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $SET --tasks-competence min14_${SET}_competence_cand2_v1 \
      --tasks-words $ALLW --tasks-scene-words $SCENE --tasks-level all --n 1000 --kinds clean --batch 16 --read cand2
    return
  fi
  model "$m" || return 1
  case $kind in
    probes)
      go competence_variants ${P}jsuite_v3probesB_cv_v1 $PY scripts/competence_variants.py --name ${P}jsuite_v3probesB_cv_v1 \
        --set jsuite_v3probesB_test_chat --words SK --variants none --why "$W: $KEY clue-only questions, second wording" ;;
    contrast)
      # shellcheck disable=SC2086
      go ablate_v2 ${P}${SET}_ko_cand2_L${BAND}_nnhops_v1 $PY scripts/ablate_v2.py --name ${P}${SET}_ko_cand2_L${BAND}_nnhops_v1 \
        --why "$W: $KEY composed vs each hop alone (RM, with MM and PM)" --plan bands --bands $BAND --conditions paper10 paper10_rot unembed10 \
        --tasks $SET --tasks-competence $C --tasks-words RM MM PM --tasks-scene-words $SCENE --tasks-level all --n 1000 \
        --kinds clean step1 step2 --batch $B --read cand2 ;;
    readout)
      go nn_readout ${P}nn_readout_v1 $PY scripts/nn_readout.py --name ${P}nn_readout_v1 --competence $C ;;
    sweep)
      for site in last final; do
        # shellcheck disable=SC2086
        go nn_swap ${P}nn_swap_sweep_${site}_v1 $PY scripts/nn_swap.py --name ${P}nn_swap_sweep_${site}_v1 --why "$W: $KEY layer sweep, site $site" \
          --sweep $WINS --site $site --competence $C --sample-per-word 80
      done ;;
    full)
      go nn_swap ${P}nn_swap_L${BAND}_v1 $PY scripts/nn_swap.py --name ${P}nn_swap_L${BAND}_v1 --why "$W: $KEY swap at the description's end, band" \
        --band $BAND --competence $C --ks 10 30 100
      for site in span qmark final; do
        # shellcheck disable=SC2086
        go nn_swap ${P}nn_swap_L${BAND}_${site}_v1 $PY scripts/nn_swap.py --name ${P}nn_swap_L${BAND}_${site}_v1 --why "$W: $KEY swap, site $site, band" \
          --band $BAND --site $site --competence $C --conds $K10
      done ;;
    best)
      for site in last final; do
        local win extra
        win=$(best_window $site)
        [ -n "$win" ] || { echo "=== no best window for $m ($site)"; fails=$((fails + 1)); continue; }
        echo "=== best window for $m, site $site: L$win"
        if [ $site = last ]; then extra="--ks 10 30 100"; else extra="--conds $K10"; fi
        # shellcheck disable=SC2086
        go nn_swap ${P}nn_swap_L${win}_${site}_best_v1 $PY scripts/nn_swap.py --name ${P}nn_swap_L${win}_${site}_best_v1 \
          --why "$W: $KEY swap, site $site, the sweep's best window" --band $win --site $site --competence $C $extra
      done ;;
    all) for k in probes contrast readout sweep full best; do run_step $k "$m"; done ;;
    *) echo "=== unknown step $kind"; fails=$((fails + 1)) ;;
  esac
}
for step in "$@"; do
  IFS=: read -r kind m <<< "$step"
  run_step "$kind" "$m"
done
echo "=== nn [$G] $* done, $fails failed $(date -u +%FT%TZ)"
