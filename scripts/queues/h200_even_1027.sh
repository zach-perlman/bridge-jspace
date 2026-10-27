#!/bin/bash
# Zach (2026-10-27, prereg amendment 55): keep-own-word knock-out and J-part swap dose on v2, in the GPU gaps.
# Steps: smoke:M | keepown:M | swapk:M:K | wait:JOB. Models: 27b 9b nem35l min14. Usage: h200_even_1027.sh GPUS STEP ...
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-27, prereg amendment 55)"
SET=jsuite_v2_test_chat
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
model() {
  case $1 in
    27b) KEY=qwen3.6-27b; P=; BAND=32-40; B=32; SB=8 ;;
    9b) KEY=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; B=32; SB=8 ;;
    nem35l) KEY=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; B=16; SB=8 ;;
    min14) KEY=ministral-3-14b; P=min14_; BAND=32-37; B=16; SB=8 ;;
    *) echo "=== unknown model $1"; return 1 ;;
  esac
  export BJ_TARGET=$KEY
  C=${P}${SET}_competence_cand2_v1
}
for step in "$@"; do
  IFS=: read -r kind a b <<< "$step"
  case $kind in
    wait)
      echo "=== waiting for $a $(date -u +%T)"
      until grep -qsE "^EXIT [0-9]+" /workspace/runs/$a.log; do sleep 60; done
      echo "=== $a ended: $(grep -E '^EXIT' /workspace/runs/$a.log | tail -1)" ;;
    smoke|keepown)
      model $a || { fails=$((fails + 1)); continue; }
      if [ $kind = smoke ]; then r=smoke_keepown55_${a}; extra="--tasks-words PM PK --n 8"; out=/workspace/scratch
      else r=${P}${SET}_ko_cand2_L${BAND}_keepown_s150_v1; extra="--tasks-words $FACTS --n 1000 --sample-per-word 150 --sample-seed 0"; out=; fi
      echo "=== ablate_v2/$r $(date -u +%T)"
      # shellcheck disable=SC2086
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $KEY keep-own-word knock-out at L$BAND" --plan bands --bands $BAND \
        --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot --tasks $SET --tasks-competence $C --tasks-level all --kinds clean \
        --batch $B --read cand2 $extra > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      if [ $kind = smoke ]; then
        echo "=== SMOKE $a ok: $(wc -l < results/ablate_v2/$r/rows.jsonl) rows"; mv results/ablate_v2/$r /workspace/scratch/$r
      else
        $PY scripts/jsuite2_score.py $r --set $SET | grep -E "^facts \S+ +start=all" | sed "s/^/=== KEEPOWN $a /"
        $PY scripts/soft_score.py $r --set $SET | sed "s/^/=== KEEPOWN ${a}SOFT /"
      fi ;;
    swapk)
      model $a || { fails=$((fails + 1)); continue; }
      r=${P}jswap_v2_k${b}_s150_v1
      echo "=== jswap/$r $(date -u +%T)"
      [ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "$W: $KEY J-part swap with K $b at L$BAND" --set $SET --band $BAND \
        --competence $C --batch $SB --sample-per-word 150 --sample-seed 0 --k $b > /workspace/scratch/$r.log 2>&1 < /dev/null \
        || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      CUDA_VISIBLE_DEVICES="" .venv/bin/python scripts/jswap_pool.py $r 2>/dev/null | sed "s/^/=== SWAPK $a k$b /" ;;
    *) echo "=== unknown step $step"; fails=$((fails + 1)) ;;
  esac
done
echo "=== even55 [$G] $* done, $fails failed $(date -u +%FT%TZ)"
