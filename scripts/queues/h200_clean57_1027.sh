#!/bin/bash
# Zach (2026-10-27, prereg amendment 57 note 2): clean-checkout reruns of amendment 57's new results from the worktree
# /workspace/clean_bridge (moved to HEAD by the launcher, before either GPU starts; this script only checks it), same
# commands as the runs of record, run names with clean_, compared row by row with them (as amendment 50).
#   nb:TARGET:PREFIX:BAND:BATCH:nu|nuth   competence on jsuite_v2nb, then the numbers (and three-hop) knock-outs
#   late:TARGET:PREFIX:BAND:BATCH         the all-token, question-only and bridge-only knock-outs at BAND (record competence)
# Usage: h200_clean57_1027.sh GPU EXPECTED_HEAD STEP ...
set -u
G=$1; HEAD_WANT=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PYX=/workspace/bridge-jspace/.venv/bin/python
C=/workspace/clean_bridge
[ "$(git -C $C rev-parse HEAD)" = "$HEAD_WANT" ] || { echo "=== CLEAN worktree not at $HEAD_WANT; stop"; exit 1; }
[ -z "$(git -C $C status --short --untracked-files=no)" ] || { echo "=== CLEAN worktree has tracked changes; stop"; exit 1; }
echo "=== CLEAN worktree at $(git -C $C rev-parse --short HEAD) $(date -u +%T)"
cd $C
W="Zach (2026-10-27, prereg amendment 57 note 2): clean-checkout rerun"
NB=jsuite_v2nb_test_chat; V2=jsuite_v2_test_chat
NUW="nPL nPM nKL nKM nAL nAM nML nMM"; THW="PPP MPP PMP PPM MPM MMP PMM MMM"
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
fails=0
compare() {  # $1 sub (tasks_v2|ablate_v2), $2 record name, $3 clean name
  $PYX - "$C/results" /workspace/bridge-jspace/results "$1" "$2" "$3" <<'PY' | sed "s/^/=== CLEAN /"
import json, sys
new, old, sub, oname, name = sys.argv[1:]
f = "items" if sub == "tasks_v2" else "rows"
key = (lambda x: (x["id"], x["part"])) if sub == "tasks_v2" else (lambda x: (x["family"], x["id"], x["kind"], x["band"], x["condition"]))
fields = ("correct", "correct_cand2", "correct_top") + (("gen",) if sub == "tasks_v2" else ())
a = {key(x): x for x in map(json.loads, open(f"{old}/{sub}/{oname}/{f}.jsonl"))}
b = {key(x): x for x in map(json.loads, open(f"{new}/{sub}/{name}/{f}.jsonl"))}
sh = set(a) & set(b)
diff = {k: sum(a[s].get(k) != b[s].get(k) for s in sh) for k in fields}
lp = max((abs(a[s].get("logp", 0) - b[s].get("logp", 0)) for s in sh), default=0)
print(f"{name}: rows record {len(a)} clean {len(b)} shared {len(sh)}; differing {diff}; max |logp diff| {lp:.2e}")
PY
}
for step in "$@"; do
  IFS=: read -r kind a b c d e <<< "$step"
  export BJ_TARGET=$a; p=$b; band=$c; batch=$d
  case $kind in
    nb)
      ocn=${p}${NB}_competence_cand2_v1; cn=${p}clean_${NB}_competence_cand2_v1
      words="$NUW"; [ $e = nuth ] && words="$NUW $THW"
      [ -f results/tasks_v2/$cn/summary.json ] || $PYX scripts/natural_v1.py competence --set $NB --name $cn --words $words --read cand2 --hop1 gen \
        --why "$W of $ocn" > /workspace/scratch/$cn.log 2>&1 < /dev/null || { echo "=== CLEAN $a competence FAILED"; tail -3 /workspace/scratch/$cn.log; fails=$((fails + 1)); continue; }
      compare tasks_v2 $ocn $cn
      mods="nu"; [ $e = nuth ] && mods="nu th"
      for m in $mods; do
        if [ $m = th ]; then w="$THW"; extra=""; orr=${p}${NB}_threehop_ko_cand2_v1; r=${p}clean_${NB}_threehop_ko_cand2_v1
        else w="$NUW"; extra="--dict-digits"; orr=${p}${NB}_numbers_ko_cand2_dd_v1; r=${p}clean_${NB}_numbers_ko_cand2_dd_v1; fi
        echo "=== CLEAN ablate_v2/$r $(date -u +%T)"
        [ -f results/ablate_v2/$r/summary.json ] || $PYX scripts/ablate_v2.py --name $r --why "$W of $orr" --plan bands --bands $band \
          --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $NB --tasks-competence $cn --tasks-words $w --tasks-level all \
          --tasks-per-word --kinds clean --batch $batch --read cand2 $extra --n 1000 > /workspace/scratch/$r.log 2>&1 < /dev/null \
          || { echo "=== CLEAN $a $m KO FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
        $PYX scripts/jsuite2_score.py $r --set $NB | grep -E "^(numbers|threehop) paper10 " | sed "s/^/=== CLEAN $a $m: /"
        compare ablate_v2 $orr $r
      done;;
    late)
      cn=${p}${V2}_competence_cand2_v1
      for mode in all question bridge; do
        if [ $mode = all ]; then orr=${p}${V2}_ko_cand2_L${band}_v1; extra="--conditions paper10 paper10_rot unembed10 unembed10_rot"
        else orr=${p}${V2}_ko_cand2_L${band}_pos${mode}_v1; extra="--positions $mode --conditions paper10 paper10_rot"; fi
        r=${orr/${p}${V2}/${p}clean_${V2}}
        echo "=== CLEAN ablate_v2/$r $(date -u +%T)"
        [ -f results/ablate_v2/$r/summary.json ] || $PYX scripts/ablate_v2.py --name $r --why "$W of $orr" --plan bands --bands $band $extra \
          --tasks $V2 --tasks-competence $cn --tasks-words $FACTS --tasks-level all --n 1000 --kinds clean --batch $batch --read cand2 \
          > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== CLEAN $a $mode FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
        $PYX scripts/jsuite2_score.py $r --set $V2 | grep -E "^facts paper10 +start=all" | sed "s/^/=== CLEAN $a L$band $mode: /"
        compare ablate_v2 $orr $r
      done;;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== clean57 GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
