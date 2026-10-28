#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 6): after the v3 ports. Usage: h200_v3next_1028.sh GPU STEP ...
# Steps: wait:JOB | comp:M:SET (natural_v1 competence, eligibility words) | cv:M (rendering 0: competence_variants on
#        every word, then the probes) | ko:M:SET (note 4's removal matrix) | gall:M (note 1) | cv21:M (note 2)
# Models: 27b 9b nem35l muse30 min14. SET: jsuite_v3_test_chat (rendering 0) or jsuite_v3r1_test_chat (rendering 1).
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
SCENE="PK PM MK MM WK WM TK TM XK XM QK QM JK JM YK YM RM"
ALLW="JH JK JM MA MC MD ME MF MG MH MK MM MN MP PA PC PD PE PF PG PH PK PM PN PP QH QK QM RA RM RN TK TM WA WK WM WN XK XM YK YM"
V21="RM RA RN PM MM PPP MPP PMP PPM MPM MMP PMM MMM nPR nKR nAR nMR nPL nKL nAL nML nPM nKM nAM nMM"
fails=0
model() {
  case $1 in
    27b) KEY=qwen3.6-27b; P=; BAND=32-40; B=32 ;;
    9b) KEY=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; B=32 ;;
    nem35l) KEY=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; B=16 ;;
    muse30) KEY=muse-glimmer-30b; P=muse30_; BAND=36-42; B=16 ;;
    min14) KEY=ministral-3-14b; P=min14_; BAND=32-37; B=16 ;;
    *) echo "=== unknown model $1"; return 1 ;;
  esac
  export BJ_TARGET=$KEY
}
go() {  # go DIR RUN NOTE CMD...: run once (skipped if DIR/RUN/summary.json exists), log to scratch
  local d=$1 r=$2 note=$3; shift 3
  echo "=== $d/$r $(date -u +%T)"
  if [ -f results/$d/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  "$@" > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T) ($note)"
}
for step in "$@"; do
  IFS=: read -r kind a s <<< "$step"
  case $kind in
    wait)
      echo "=== waiting for $a $(date -u +%T)"
      until grep -qsE "^EXIT [0-9]+" /workspace/runs/$a.log; do sleep 60; done
      echo "=== $a ended: $(grep -E '^EXIT' /workspace/runs/$a.log | tail -1)" ;;
    comp)
      model $a || continue
      go tasks_v2 ${P}${s}_competence_cand2_v1 "eligibility" $PY scripts/natural_v1.py competence --set $s --name ${P}${s}_competence_cand2_v1 \
        --words $SCENE --read cand2 --hop1 gen --why "Zach (2026-10-28, prereg amendment 58 note 6): $KEY $s competence (K and M words, eligibility)" ;;
    cv)
      model $a || continue
      go competence_variants ${P}jsuite_v3_cv_v1 "whole-question reads" $PY scripts/competence_variants.py --name ${P}jsuite_v3_cv_v1 --set jsuite_v3_test_chat \
        --words $ALLW --variants none --why "Zach (2026-10-28, prereg amendment 58 note 6): $KEY v3 whole-question reads (cand2 + greedy), all words"
      go competence_variants ${P}jsuite_v3probes_cv_v1 "probes" $PY scripts/competence_variants.py --name ${P}jsuite_v3probes_cv_v1 --set jsuite_v3probes_test_chat \
        --words SK --variants none --why "Zach (2026-10-28, prereg amendment 58 note 6): $KEY v3 skip-the-bridge probes" ;;
    ko)
      model $a || continue
      [ -f results/tasks_v2/${P}${s}_competence_cand2_v1/summary.json ] || { echo "=== no competence for $a $s"; fails=$((fails + 1)); continue; }
      # shellcheck disable=SC2086
      go ablate_v2 ${P}${s}_ko_cand2_v1 "removal matrix" $PY scripts/ablate_v2.py --name ${P}${s}_ko_cand2_v1 \
        --why "Zach (2026-10-28, prereg amendment 58 note 6): $KEY $s knock-out matrix (v1)" --plan bands --bands $BAND \
        --conditions paper10 paper10_rot unembed10 paper10_pcasize --tasks $s --tasks-competence ${P}${s}_competence_cand2_v1 \
        --tasks-words $ALLW --tasks-scene-words $SCENE --tasks-level all --n 1000 --kinds clean --batch $B --read cand2 ;;
    gall)
      model $a || continue
      go greedy_all ${P}greedy_all_v2test_v1 "note 1" $PY scripts/greedy_all.py --name ${P}greedy_all_v2test_v1 \
        --why "Zach (2026-10-27, prereg amendment 58 note 1; requeued by note 6): $KEY" ;;
    cv21)
      model $a || continue
      # shellcheck disable=SC2086
      go competence_variants ${P}competence_variants_v21_v1 "note 2" $PY scripts/competence_variants.py --name ${P}competence_variants_v21_v1 \
        --why "Zach (2026-10-27, prereg amendment 58 note 2; requeued by note 6): $KEY" --words $V21 ;;
    *) echo "=== unknown step $step"; fails=$((fails + 1)) ;;
  esac
done
echo "=== v3next [$G] $* done, $fails failed $(date -u +%FT%TZ)"
