#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 5): the ports to jsuite v3. Usage: h200_v3ports_1028.sh GPU STEP ...
# Steps: wait:JOB (until /workspace/runs/JOB.log ends with EXIT) | waitfile:PATH | smoke:M (aborts the queue on a failure)
#        | ans:M | swap:M | pos:M | pointer:M | keepown:M | xrel:M | readout:M | all:M (note 5's order) | swapfam:M | removal:M
# Models: 27b 9b nem35l. Eligibility: each model's v3 competence, note 4's scene rule.
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 5)"
SET=jsuite_v3_test_chat
FACTS="PP PK PM PA PN MP MK MM MA MN TK TM WK WM WA WN RM RA RN"
NAMED="PP PK PM PA PN MP MK MM MA MN TK TM WK WM WA WN"
SCENE="PK PM MK MM WK WM TK TM XK XM QK QM JK JM YK YM RM"
fails=0
model() {
  case $1 in
    27b) KEY=qwen3.6-27b; P=; BAND=32-40; DEEP=52-60; B=32 ;;
    9b) KEY=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; DEEP=26-29; B=32 ;;
    nem35l) KEY=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; DEEP=33-39; B=16 ;;
    *) echo "=== unknown model $1"; return 1 ;;
  esac
  export BJ_TARGET=$KEY
  C=${P}${SET}_competence_cand2_v1
}
ko() {  # ko RUN BAND "CONDITIONS" "WORDS" "EXTRA ARGS" WHAT
  local r=$1
  echo "=== ablate_v2/$r $(date -u +%T)"
  if [ -f results/ablate_v2/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  # shellcheck disable=SC2086
  $PY scripts/ablate_v2.py --name $r --why "$W: $KEY $6" --plan bands --bands $2 --conditions $3 --tasks $SET \
    --tasks-competence $C --tasks-words $4 --tasks-scene-words $SCENE --tasks-level all --kinds clean --batch $B --read cand2 $5 \
    > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
sw() {  # sw SCRIPT RUN "EXTRA ARGS" WHAT
  local r=$2
  echo "=== jswap/$r $(date -u +%T)"
  if [ -f results/jswap/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  # shellcheck disable=SC2086
  $PY scripts/$1.py --name $r --why "$W: $KEY $4" --set $SET --band $BAND --competence $C --batch 8 $3 \
    > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
run_step() {
  local kind=$1 a=$2
  case $kind in
    wait)
      echo "=== waiting for $a $(date -u +%T)"
      until grep -qsE "^EXIT [0-9]+" /workspace/runs/$a.log; do sleep 60; done
      echo "=== $a ended: $(grep -E '^EXIT' /workspace/runs/$a.log | tail -1)" ;;
    waitfile)
      echo "=== waiting for $a $(date -u +%T)"
      until [ -f "$a" ]; do sleep 60; done
      echo "=== $a is there $(date -u +%T)" ;;
    smoke)
      model $a || return 1
      local s=v3ports_smoke_$a ok=1
      ko ${P}${s}_ans $BAND "ansJ ansJ_rot ansU ansU_rot" "PK PM RM" "--n 2" "smoke" || ok=0
      ko ${P}${s}_pos $DEEP "paper10 paper10_rot" "PK PM" "--n 2 --positions bridge" "smoke" || ok=0
      ko ${P}${s}_keepown $BAND "paper10_keepown paper10_keepown_rot" "PK PM" "--n 2" "smoke" || ok=0
      sw jswap ${P}${s}_swap "--limit 2" "smoke" || ok=0
      sw jswap_pointer ${P}${s}_pointer "--limit 2" "smoke" || ok=0
      sw jswap_xrel ${P}${s}_xrel "--limit 2" "smoke" || ok=0
      for d in results/ablate_v2/${P}${s}_* results/jswap/${P}${s}_*; do [ -d "$d" ] && mv "$d" /workspace/scratch/; done
      if [ $ok = 1 ]; then echo "PORTSMOKE OK"; else echo "PORTSMOKE FAILED"; exit 3; fi ;;
    ans)
      model $a || return 1
      ko ${P}${SET}_ko_cand2_L${BAND}_ans_v1 $BAND "ansJ ansJ_rot ansU ansU_rot" "$FACTS" "--n 1000" "answer-only removal at L$BAND" ;;
    pos)
      model $a || return 1
      for band in $BAND $DEEP; do
        for mode in bridge question; do
          ko ${P}${SET}_ko_cand2_L${band}_pos${mode}_v1 $band "paper10 paper10_rot" "$NAMED" "--n 1000 --positions $mode" "$mode-only knock-out at L$band"
        done
      done ;;
    keepown)
      model $a || return 1
      ko ${P}${SET}_ko_cand2_L${BAND}_keepown_s150_v1 $BAND "paper10 paper10_rot paper10_keepown paper10_keepown_rot" "$FACTS" \
        "--n 1000 --sample-per-word 150 --sample-seed 0" "keep-own-word knock-out at L$BAND" ;;
    swap)
      model $a || return 1
      sw jswap ${P}jswap_v3_v1 "" "J-part swap at L$BAND" ;;
    pointer)
      model $a || return 1
      sw jswap_pointer ${P}jswap_pointer_v3_s150_v1 "--sample-per-word 150" "what the mention's J-part carries at L$BAND" ;;
    xrel)
      model $a || return 1
      sw jswap_xrel ${P}jswap_xrel_v3_v1 "" "cross-context swap at L$BAND" ;;
    readout)
      model $a || return 1
      local r=${P}bridge_readout_v3_v1
      echo "=== bridge_readout/$r $(date -u +%T)"
      if [ -f results/bridge_readout/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
      $PY scripts/bridge_readout.py --name $r --competence $C --set $SET > /workspace/scratch/$r.log 2>&1 < /dev/null \
        || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
      echo "=== done $r $(date -u +%T)" ;;
    all) for k in ans swap pos pointer keepown xrel readout; do run_step $k $a; done ;;
    swapfam) for k in swap pointer xrel readout; do run_step $k $a; done ;;
    removal) for k in ans pos keepown; do run_step $k $a; done ;;
    *) echo "=== unknown step $kind:$a"; fails=$((fails + 1)) ;;
  esac
}
for step in "$@"; do
  IFS=: read -r kind a <<< "$step"
  run_step "$kind" "$a"
done
echo "=== v3ports [$G] $* done, $fails failed $(date -u +%FT%TZ)"
