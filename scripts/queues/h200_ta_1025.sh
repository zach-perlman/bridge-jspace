#!/bin/bash
# Zach (2026-10-25, prereg amendment 48; the TA's notes): the probe ceiling (scripts/probe_ceiling.py) and the variance
# control (ablate_v2's paper10_pcasize, paper10's size along the residual's top principal directions, and pca1; the test
# knock-out's items and band; jsuite2_score + soft_score; removal_size --pca at the band layers) for one model at a band.
# Usage: h200_ta_1025.sh GPUS STEP ...   STEP: waitq:JOB  probe:TARGET:PREFIX:BAND:BATCH  pca:TARGET:PREFIX:BAND:BATCH
#   (probe uses PREFIXjsuite_v2_dev_chat_competence_cand2_v1 and PREFIXjsuite_v2_test_chat_competence_cand2_v1)
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 48)"
SET=jsuite_v2_test_chat
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
for step in "$@"; do
  IFS=: read -r kind a b c d <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT [0-9]" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    probe)
      export BJ_TARGET=$a; r=${b}probe_ceiling_L${c}_v1
      echo "=== probe_ceiling/$r $(date -u +%T)"
      [ -f results/probe_ceiling/$r/summary.json ] || $PY scripts/probe_ceiling.py --name $r --why "$W: $a, the probe ceiling at the mention, causal part at L$c" \
        --band $c --dev-competence ${b}jsuite_v2_dev_chat_competence_cand2_v1 --test-competence ${b}${SET}_competence_cand2_v1 --stride 2 --batch $d \
        > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      grep -E "^[a-z]+: n train" /workspace/scratch/$r.log | sed "s/^/=== PROBEREAD $a /" | cut -c1-260
      grep -E "^probe-valid" /workspace/scratch/$r.log | sed "s/^/=== PROBEVALID $a /"
      grep -E "^memory(_valid)? " /workspace/scratch/$r.log | sed "s/^/=== PROBESWAP $a /"
      grep -E "^(PP|PK|TP|TK) +(swap_probe|remove_probe) " /workspace/scratch/$r.log | sed "s/^/=== PROBELOOK $a /";;
    pca)
      export BJ_TARGET=$a; r=${b}${SET}_ko_cand2_L${c}_pca_v1
      echo "=== ablate_v2/$r $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a, the variance control (paper10_pcasize, pca1) at L$c" --plan bands \
        --bands $c --conditions paper10_pcasize pca1 --tasks $SET --tasks-competence ${b}${SET}_competence_cand2_v1 --tasks-words $FACTS --tasks-level all \
        --n 1000 --kinds clean --batch $d --read cand2 > /workspace/scratch/$r.log 2>&1 < /dev/null \
        || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      $PY scripts/jsuite2_score.py $r --set $SET | grep -E "^facts (pca[0-9]+|paper10_pcasize) +start=all" | sed "s/^/=== PCA $a: /"
      $PY scripts/soft_score.py $r --set $SET | sed "s/^/=== PCASOFT $a: /"
      s=${b}removal_size_pca_L${c}_v1
      [ -f results/removal_size/$s/summary.json ] || $PY scripts/removal_size.py --name $s --why "$W: $a, removal size of pca vs paper10 at L$c" \
        --layers $(seq ${c%-*} ${c#*-}) --ks 1 3 10 --pca > /workspace/scratch/$s.log 2>&1 < /dev/null \
        || { echo "=== $s FAILED"; tail -3 /workspace/scratch/$s.log; fails=$((fails + 1)); continue; }
      grep -E "^  L" /workspace/scratch/$s.log | sed "s/^/=== PCASIZE $a /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== ta done, $fails failed $(date -u +%FT%TZ)"
exit $fails
