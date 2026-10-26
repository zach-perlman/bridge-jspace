#!/bin/bash
# Zach (2026-10-25, prereg amendment 42): a model's depth profile on the dev split. Every window (round(9/64 n) wide,
# sliding by round(4/64 n), inside the lens's layers, as amendment 39's sweep) on jsuite_v2_dev_chat's words PP PK PM
# MP MK MM (n per word, default 40), paper10 / paper10_rot / unembed10, cand2; dev competence on the 15 facts words
# first if missing; scored per band by scripts/profile_score.py (M - K with K finals, M - P), picked by
# scripts/profile_pick.py (the largest J-specific M - K where the rotation costs <= 10 on every final).
# Usage: h200_profile_1025.sh GPUS STEP ...   STEP: waitq:JOB  prof:TARGET:PREFIX:BATCH[:N[:rs]]
# Amendment 49 note 1: with /workspace/scratch/PREFIXsample_dev.txt present, or rs, a seeded random N items per word
# over every relation (the first N per word were all countries); rs also names the run PREFIX..._profile_rsN_...
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 42)"
DEV=jsuite_v2_dev_chat
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT [0-9]" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    prof)
      export BJ_TARGET=$a; p=$b; batch=${c:-16}; n=${d:-40}
      read -r BANDS NL <<< "$($PY - <<'PY'
import sys
sys.path.insert(0, "src")
import torch
from bridge_jspace import pins
from huggingface_hub import hf_hub_download
n = pins.N_LAYERS
s0 = pins.LENS_SOURCES[pins.FROZEN_LENS]
path = pins.REPO_ROOT / s0[1] if s0[0] == "local" else hf_hub_download(s0[0], s0[1], revision=s0[2])
src = sorted(int(x) for x in torch.load(path, map_location="cpu", weights_only=True, mmap=True)["source_layers"])
lo, hi = src[0], src[-1]
w, s = max(2, round(9 / 64 * n)), max(1, round(4 / 64 * n))
print("|".join(f"{a}-{a + w - 1}" for a in range(lo, hi - w + 2, s)), n)
PY
)"
      BANDS=${BANDS//|/ }
      SA=""; NN=$n; sfx=""
      if [ -f /workspace/scratch/${p}sample_dev.txt ] || [ "${e:-}" = rs ]; then SA="--sample-per-word $n --sample-seed 0"; NN=1000; fi
      [ "${e:-}" = rs ] && sfx="_rs$n"
      [ -f /workspace/scratch/${p}pad.txt ] && SA="$SA --pad"  # amendment 49 note 4: right-padded batches for this model
      cn=${p}${DEV}_competence_cand2_v1; r=${p}${DEV}_profile${sfx}_cand2_v1
      [ -n "$SA" ] && echo "=== PROFILE $a: a random $n per word over all relations (seed 0), run $r"
      echo "=== PROFILE $a bands $BANDS ($NL blocks) $(date -u +%T)"
      if [ ! -f results/tasks_v2/$cn/summary.json ]; then
        $PY scripts/natural_v1.py competence --set $DEV --name $cn --read cand2 --hop1 gen --words $FACTS --why "$W: $a on $DEV" \
          > /workspace/scratch/$cn.log 2>&1 < /dev/null || { fail "$a dev competence" /workspace/scratch/$cn.log; continue; }
      fi
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $a depth profile on the dev split" --plan bands \
        --bands $BANDS --conditions paper10 paper10_rot unembed10 --tasks $DEV --tasks-competence $cn --tasks-words PP PK PM MP MK MM \
        --tasks-level all --n $NN --kinds clean --batch $batch --read cand2 $SA > /workspace/scratch/$r.log 2>&1 < /dev/null \
        || { fail "$a profile" /workspace/scratch/$r.log; continue; }
      $PY scripts/profile_score.py $r $NL --set $DEV | sed "s/^/=== PROF $a /"
      echo "=== PROFPICK $a $($PY scripts/profile_pick.py $r)";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== profile done, $fails failed $(date -u +%FT%TZ)"
exit $fails
