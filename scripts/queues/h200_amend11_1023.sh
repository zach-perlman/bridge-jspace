#!/bin/bash
# Zach (2026-10-23, prereg amendment 11). Usage: h200_amend11_1023.sh GPU STEP [STEP ...]
#   v2_27 / v2_9 / v2_muse: natural_v2_chat (seed 802) competence, then C1 at the model's band.
#   musemid: Muse on natural_v1_chat at L16-22, the knock-out and the logit-lens control.
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
WHY="Zach (2026-10-23, prereg amendment 11)"
v2() {  # v2 TARGET PREFIX BAND BATCH
  export BJ_TARGET=$1; local p=$2 band=$3 batch=$4 set=natural_v2_chat c=${2}natural_v2_chat_competence_v1 r=${2}natural_v2_chat_ko_v1
  if [ ! -f results/tasks_v2/$c/summary.json ]; then
    echo "=== competence $c $(date -u +%T)"
    $PY scripts/natural_v1.py competence --set $set --name $c --why "$WHY: $1 on $set (second natural seed)" > /workspace/scratch/$c.log 2>&1 \
      || { echo "=== $1 $set competence FAILED"; tail -3 /workspace/scratch/$c.log; return 1; }
  fi
  python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== natural $1 $set whole:', {k: v['whole'] for k, v in s.items()})" results/tasks_v2/$c/summary.json
  if [ ! -f results/ablate_v2/$r/summary.json ]; then
    echo "=== ablate_v2/$r $(date -u +%T)"
    $PY scripts/ablate_v2.py --name $r --why "$WHY: $1, C1 on $set at L$band (second natural seed)" --plan bands --bands $band \
      --conditions paper10 paper10_rot --tasks $set --tasks-competence $c --tasks-words PP PM MP MM --tasks-level all --n 1000 \
      --kinds clean --batch $batch > /workspace/scratch/$r.log 2>&1 || { echo "=== $1 $set C1 FAILED"; tail -3 /workspace/scratch/$r.log; return 1; }
  fi
  $PY scripts/c1_v2.py $r --middle L$band --set $set | tail -2
}
for step in "$@"; do
  case $step in
    v2_27) v2 qwen3.6-27b "" 32-40 32;;
    v2_9) v2 qwen3.5-9b qwen35_9b_ 12-16 32;;
    v2_muse) v2 muse-glimmer-30b muse30_ 36-42 32;;
    musemid)
      export BJ_TARGET=muse-glimmer-30b; c=muse30_natural_v1_chat_competence_v1; r=muse30_natural_v1_chat_ko_l1622_v1
      T="--tasks natural_v1_chat --tasks-competence $c --tasks-words PP PM MP MM --tasks-level all --n 1000 --kinds clean --batch 32"
      for pair in "$r:paper10 paper10_rot" "${r%_v1}_unembed_v1:unembed10 unembed10_rot"; do
        n=${pair%%:*}; conds=${pair#*:}
        [ -f results/ablate_v2/$n/summary.json ] || { echo "=== ablate_v2/$n $(date -u +%T)"; $PY scripts/ablate_v2.py --name $n \
          --why "$WHY: Muse on natural_v1_chat at L16-22 ($conds)" --plan bands --bands 16-22 --conditions $conds $T > /workspace/scratch/$n.log 2>&1 \
          || { echo "=== Muse L16-22 $conds FAILED"; tail -3 /workspace/scratch/$n.log; }; }
      done
      $PY scripts/c1_v2.py $r --middle L16-22 --set natural_v1_chat | tail -2
      $PY scripts/c1_specificity.py $r ${r%_v1}_unembed_v1 --set natural_v1_chat | tail -3 | sed "s/^/=== spec Muse L16-22: /";;
  esac
done
echo "=== amendment 11 GPU $G done $(date -u +%FT%TZ)"
