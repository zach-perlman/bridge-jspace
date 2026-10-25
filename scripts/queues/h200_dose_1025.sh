#!/bin/bash
# Zach (2026-10-25, prereg amendment 43): removal-size curves at a model's depth-profile pick (scripts/profile_pick.py)
# on the dev split: top1 / top3 / paper10 / top30 and each one's rotated control, words PP PK PM MP MK MM, n per word
# (default 40), cand2; M - K per condition by scripts/profile_score.py. Descriptive (dev): is top-10 too blunt for one
# model, too weak for another?
# Usage: h200_dose_1025.sh GPUS STEP ...   STEP: waitq:JOB  waitfile:PATH  mem:GPU:GB  dose:TARGET:PREFIX:BATCH[:N]
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 43)"
DEV=jsuite_v2_dev_chat
fails=0
for step in "$@"; do
  IFS=: read -r kind a b c d <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    waitfile) until [ -f "$a" ]; do sleep 60; done; echo "=== $a present $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $a --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((b * 1024)) ]; do sleep 60; done;;
    dose)
      export BJ_TARGET=$a; p=$b; batch=${c:-16}; n=${d:-40}
      band=$($PY scripts/profile_pick.py ${p}${DEV}_profile_cand2_v1 2>/dev/null)
      nl=$($PY -c "import sys; sys.path.insert(0, 'src'); from bridge_jspace import pins; print(pins.N_LAYERS)")
      [[ "$band" =~ ^[0-9]+-[0-9]+$ ]] || { echo "=== DOSE $a: no profile pick ('$band')"; fails=$((fails + 1)); continue; }
      r=${p}${DEV}_dose_L${band}_cand2_v1
      echo "=== DOSE $a at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, removal sizes at its profile pick L$band" --plan bands \
        --bands $band --conditions top1 top1_rot top3 top3_rot paper10 paper10_rot top30 top30_rot --tasks $DEV --tasks-competence ${p}${DEV}_competence_cand2_v1 \
        --tasks-words PP PK PM MP MK MM --tasks-level all --n $n --kinds clean --batch $batch --read cand2 > /workspace/scratch/$r.log 2>&1 < /dev/null \
        || { echo "=== DOSE $a FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      $PY scripts/profile_score.py $r $nl --set $DEV | sed "s/^/=== DOSE $a /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== dose done, $fails failed $(date -u +%FT%TZ)"
exit $fails
