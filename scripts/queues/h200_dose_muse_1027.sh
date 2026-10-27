#!/bin/bash
# Zach (2026-10-26, prereg amendment 54): one dose grid for every cached model, plus the missing position splits and
# Lightning's clean-checkout rerun. Steps run in order on the GPUs given:
#   dose:M    removal sizes at K 1/3/10/30/100/300 (J++, logit lens, top principal directions), then the test knock-out
#             at M's band, 150 random per word (seed 0): top K at every K, rotated at every K, size-matched (top-256
#             principal directions) and logit lens at K >= 10
#   pos:M     the knock-out restricted to positions (Lightning: paper10 / rot / logit lens, all items, bridge / context /
#             question; Bolt: top100 / rot, 150 per word, bridge / question)
#   clean:M   M's headline from the clean worktree /workspace/clean_bridge at HEAD, compared row by row (as amendment 50)
#   wait:JOB  wait until JOB's log ends with a numeric EXIT
# Models: 27b 9b nem35l min14 nem35b muse30. (Copy of h200_dose_1026.sh, amendment 57 note 1: Muse added.) Usage: h200_dose_1026.sh GPUS STEP [STEP ...]
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
PYX=/workspace/bridge-jspace/.venv/bin/python
W="Zach (2026-10-27, prereg amendment 57 note 1; design of amendment 54)"
SET=jsuite_v2_test_chat
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
KS="1 3 10 30 100 300"
CONDS="top1 top1_rot top3 top3_rot top10 top10_rot top10_pcasize unembed10 top30 top30_rot top30_pcasize unembed30 top100 top100_rot top100_pcasize unembed100 top300 top300_rot top300_pcasize unembed300"
fails=0

model() {
  case $1 in
    27b) KEY=qwen3.6-27b; P=; BAND=32-40; B=32 ;;
    9b) KEY=qwen3.5-9b; P=qwen35_9b_; BAND=12-16; B=32 ;;
    nem35l) KEY=nemotron-3.5-lightning; P=nem35l_; BAND=27-33; B=16 ;;
    min14) KEY=ministral-3-14b; P=min14_; BAND=32-37; B=16 ;;
    nem35b) KEY=nemotron-3.5-bolt; P=nem35b_; BAND=42-53; B=16 ;;
    muse30) KEY=muse-glimmer-30b; P=muse30_; BAND=36-42; B=16 ;;
    *) echo "=== unknown model $1"; return 1 ;;
  esac
  export BJ_TARGET=$KEY
  C=${P}${SET}_competence_cand2_v1
}

score() {  # $1 run, $2 tag
  $PY scripts/jsuite2_score.py $1 --set $SET | grep -E "^facts \S+ +start=all" | sed "s/^/=== $2 /"
  $PY scripts/soft_score.py $1 --set $SET | sed "s/^/=== ${2}SOFT /"
}

ko() {  # $1 run, $2 why, rest: extra ablate_v2 arguments
  local r=$1 why=$2; shift 2
  echo "=== ablate_v2/$r $(date -u +%T)"
  [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $why" --plan bands --bands $BAND \
    --tasks $SET --tasks-competence $C --tasks-words $FACTS --tasks-level all --n 1000 --kinds clean --batch $B --read cand2 "$@" \
    > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); return 1; }
}

for step in "$@"; do
  kind=${step%%:*}; arg=${step#*:}
  case $kind in
    wait)
      echo "=== waiting for $arg $(date -u +%T)"
      until grep -qsE "^EXIT [0-9]+" /workspace/runs/$arg.log; do sleep 60; done
      echo "=== $arg ended: $(grep -E '^EXIT' /workspace/runs/$arg.log | tail -1)" ;;
    dose)
      model $arg || { fails=$((fails + 1)); continue; }
      s=${P}removal_size_L${BAND}_dose54_v1
      [ -f results/removal_size/$s/summary.json ] || $PY scripts/removal_size.py --name $s --why "$W: $KEY removal sizes at L$BAND, K $KS" \
        --layers $(seq ${BAND%-*} ${BAND#*-}) --ks $KS --pca > /workspace/scratch/$s.log 2>&1 < /dev/null || { echo "=== $s FAILED"; tail -3 /workspace/scratch/$s.log; fails=$((fails + 1)); }
      $PYX - $s <<'PY' | sed "s/^/=== SIZE $arg /"
import json, statistics, sys
s = json.load(open(f"results/removal_size/{sys.argv[1]}/summary.json"))["median_share"]
keys = list(next(iter(s.values())))
print(" ".join(f"{k} {100 * statistics.median(v[k] for v in s.values()):.1f}%" for k in keys))
PY
      r=${P}${SET}_ko_cand2_L${BAND}_dose54_s150_v1
      ko $r "$KEY test knock-out, dose grid K $KS with rotated, size-matched and logit-lens controls" \
        --conditions $CONDS --sample-per-word 150 --sample-seed 0 && score $r "DOSE $arg" ;;
    pos)
      model $arg || { fails=$((fails + 1)); continue; }
      if [ $arg = nem35b ]; then modes="bridge question"; conds="top100 top100_rot"; extra="--sample-per-word 150 --sample-seed 0"; tag=_L${BAND}_k100; sfx=_s150
      else modes="bridge context question"; conds="paper10 paper10_rot unembed10"; extra=""; tag=; sfx=; fi
      for mode in $modes; do
        r=${P}${SET}_ko_cand2${tag}_pos${mode}${sfx}_v1
        # shellcheck disable=SC2086
        ko $r "$KEY knock-out at L$BAND only at the $mode positions" --positions $mode --conditions $conds $extra && score $r "POS $arg $mode"
      done ;;
    clean)
      model $arg || { fails=$((fails + 1)); continue; }
      CL=/workspace/clean_bridge; H=$(git rev-parse HEAD)
      [ -z "$(git -C $CL status --short --untracked-files=no)" ] || { echo "=== CLEAN worktree has tracked changes; skip"; fails=$((fails + 1)); continue; }
      git -C $CL checkout -q --detach $H || { echo "=== CLEAN checkout FAILED"; fails=$((fails + 1)); continue; }
      echo "=== CLEAN $arg worktree at $(git -C $CL rev-parse --short HEAD) $(date -u +%T)"
      ocn=$C; orr=${P}${SET}_ko_cand2_v1; cn=clean_$C; r=clean_${P}${SET}_ko_cand2_v1
      WC="$W: clean-checkout rerun of $KEY's headline"
      ( cd $CL && unset BJ_GRAM_PROJ \
        && { [ -f results/tasks_v2/$cn/summary.json ] || $PYX scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen --why "$WC" > /workspace/scratch/$cn.log 2>&1 < /dev/null; } \
        && echo "=== CLEAN $arg competence done $(date -u +%T)" \
        && { [ -f results/ablate_v2/$r/summary.json ] || $PYX scripts/ablate_v2.py --name $r --why "$WC" --plan bands --bands $BAND \
               --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn --tasks-words $FACTS \
               --tasks-level all --n 1000 --kinds clean --batch $B --read cand2 > /workspace/scratch/$r.log 2>&1 < /dev/null; } \
        && $PYX scripts/jsuite2_score.py $r --set $SET | grep -E "^facts (paper10|unembed10) +start=all" | sed "s/^/=== CLEAN $arg /" \
        && $PYX - "$CL/results" /workspace/bridge-jspace/results "$ocn" "$orr" "$cn" "$r" <<'PY'
import json, sys
new, old, ocn, orr, cn, r = sys.argv[1:]
def rows(base, sub, name, key):
    return {key(x): x for x in map(json.loads, open(f"{base}/{sub}/{name}/{'items' if sub == 'tasks_v2' else 'rows'}.jsonl"))}
kc = lambda x: (x["id"], x["part"])
kr = lambda x: (x["family"], x["id"], x["kind"], x["band"], x["condition"])
for sub, oname, name, key, fields in (("tasks_v2", ocn, cn, kc, ("correct", "correct_cand2", "correct_top", "gen")), ("ablate_v2", orr, r, kr, ("correct", "correct_cand2", "correct_top"))):
    a, b = rows(old, sub, oname, key), rows(new, sub, name, key)
    shared = set(a) & set(b)
    diff = {f: sum(a[k].get(f) != b[k].get(f) for k in shared) for f in fields}
    lp = max((abs(a[k].get("logp", 0) - b[k].get("logp", 0)) for k in shared), default=0)
    print(f"=== CLEAN {sub}: rows old {len(a)} new {len(b)} shared {len(shared)}; differing {diff}; max |logp diff| {lp:.2e}")
PY
      ) || { echo "=== CLEAN $arg FAILED"; tail -3 /workspace/scratch/$r.log 2>/dev/null; fails=$((fails + 1)); } ;;
    *) echo "=== unknown step $step"; fails=$((fails + 1)) ;;
  esac
done
echo "=== dose54 [$G] $* done, $fails failed $(date -u +%FT%TZ)"
