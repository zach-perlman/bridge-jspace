#!/bin/bash
# Zach (2026-10-23, prereg amendment 10). Usage: h200_amend10_1023.sh GPU STEP [STEP ...]
#   A (bridge absent): mm9 / mm27 / mmmuse / mm122: competence on full_v8_mmabs, then the knock-out at the model's fixed
#   band(s), M->M only. waitmem MB: wait for that much free memory on this GPU. waitq JOB: wait for a job log's EXIT.
#   B (natural pilot): nat TARGET PREFIX FRAMING BAND BATCH (added when natural_v1 is built).
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
. scripts/queues/lib_competence_parallel.sh
WHY="Zach (2026-10-23, prereg amendment 10)"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }

mm() {  # mm TARGET PREFIX "BANDS" BATCH
  export BJ_TARGET=$1; local p=$2 bands=$3 batch=$4 c=${2}full_v8_mmabs_competence_v1
  comp_parallel 1 "$WHY: $1, M->M with the bridge absent from the context" $c:full_v8_mmabs || { echo "=== $1 mmabs competence FAILED"; return 1; }
  run ablate_v2/${p}mmabs_ko_v1 $PY scripts/ablate_v2.py --name ${p}mmabs_ko_v1 --why "$WHY: $1, M->M with the bridge absent, knock-out at $bands" \
    --plan bands --bands $bands --conditions paper10 paper10_rot --tasks full_v8_mmabs --tasks-competence $c --tasks-words MM \
    --tasks-level all --n 1000 --kinds clean --batch $batch > /workspace/scratch/${p}mmabs_ko_v1.log 2>&1 || { echo "=== $1 mmabs knock-out FAILED"; tail -3 /workspace/scratch/${p}mmabs_ko_v1.log; }
}

mp() {  # mp TARGET PREFIX SET COMP "BANDS" BATCH: the same M->M knock-out with the bridge present (full_v8), M->M only
  export BJ_TARGET=$1; local p=$2 set=$3 c=$4 bands=$5 batch=$6
  run ablate_v2/${p}mmpres_ko_v1 $PY scripts/ablate_v2.py --name ${p}mmpres_ko_v1 --why "$WHY: $1, M->M with the bridge present (the control for mmabs), knock-out at $bands" \
    --plan bands --bands $bands --conditions paper10 paper10_rot --tasks $set --tasks-competence $c --tasks-words MM \
    --tasks-level all --n 1000 --kinds clean --batch $batch > /workspace/scratch/${p}mmpres_ko_v1.log 2>&1 || { echo "=== $1 mmpres knock-out FAILED"; tail -3 /workspace/scratch/${p}mmpres_ko_v1.log; }
  [ -f results/ablate_v2/${p}mmabs_ko_v1/summary.json ] && $PY scripts/mm_absent_compare.py ${p}mmpres_ko_v1 ${p}mmabs_ko_v1 | sed "s/^/=== mmabs $1: /"
}

nat() {  # nat TARGET PREFIX SET BAND BATCH: natural_v1 competence (first-token read), then C1 at the model's fixed band
  export BJ_TARGET=$1; local p=$2 set=$3 band=$4 batch=$5 c=${2}${3}_competence_v1 r=${2}${3}_ko_v1
  if [ ! -f results/tasks_v2/$c/summary.json ]; then
    echo "=== competence $c $(date -u +%T)"
    $PY scripts/natural_v1.py competence --set $set --name $c --why "$WHY: $1 on $set (natural pilot)" > /workspace/scratch/$c.log 2>&1 \
      || { echo "=== $1 $set competence FAILED"; tail -3 /workspace/scratch/$c.log; return 1; }
  fi
  python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== natural $1 $set whole:', {k: v['whole'] for k, v in s.items()})" results/tasks_v2/$c/summary.json
  if [ ! -f results/ablate_v2/$r/summary.json ]; then
    echo "=== ablate_v2/$r $(date -u +%T)"
    $PY scripts/ablate_v2.py --name $r --why "$WHY: $1, C1 on $set at its fixed band L$band (natural pilot)" --plan bands --bands $band \
      --conditions paper10 paper10_rot --tasks $set --tasks-competence $c --tasks-words PP PM MP MM --tasks-level all --n 1000 \
      --kinds clean --batch $batch > /workspace/scratch/$r.log 2>&1 || { echo "=== $1 $set C1 FAILED"; tail -3 /workspace/scratch/$r.log; return 1; }
  fi
  $PY scripts/c1_v2.py $r --middle L$band --set $set | tail -2
}

natctl() {  # natctl TARGET PREFIX SET BAND BATCH: the logit-lens control and each step alone on a natural set (10B note 2)
  export BJ_TARGET=$1; local p=$2 set=$3 band=$4 batch=$5 c=${2}${3}_competence_v1 r=${2}${3}_ko_v1
  local T="--tasks $set --tasks-competence $c --tasks-words PP PM MP MM --tasks-level all --n 1000 --batch $batch"
  run ablate_v2/${r%_v1}_unembed_v1 $PY scripts/ablate_v2.py --name ${r%_v1}_unembed_v1 --why "$WHY: $1, the logit-lens control on $set at L$band" \
    --plan bands --bands $band --conditions unembed10 unembed10_rot $T --kinds clean > /workspace/scratch/${r%_v1}_unembed_v1.log 2>&1 \
    && $PY scripts/c1_specificity.py $r ${r%_v1}_unembed_v1 --set $set | tail -3 | sed "s/^/=== spec $1: /" || echo "=== $1 $set unembed FAILED"
  run ablate_v2/${r%_v1}_steps_v1 $PY scripts/ablate_v2.py --name ${r%_v1}_steps_v1 --why "$WHY: $1, each step alone on $set at L$band" \
    --plan bands --bands $band --conditions paper10 paper10_rot $T --kinds step1 step2 > /workspace/scratch/${r%_v1}_steps_v1.log 2>&1 \
    && $PY scripts/c1_v2.py ${r%_v1}_steps_v1 --middle L$band --set $set > /dev/null && echo "=== steps $1 $set done" || echo "=== $1 $set steps FAILED"
}

for step in "$@"; do
  case $step in
    waitmem:*) want=${step#waitmem:}
      until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge "$want" ]; do sleep 30; done
      echo "=== GPU $G has >= $want MiB free $(date -u +%T)";;
    waitq:*) j=${step#waitq:}  # a short job name (h200...) or the full one (2026-10-23 fix: the full name was prefixed twice)
      case $j in bridge-cse_*) f=/workspace/runs/$j.log;; *) f=$R-$j.log;; esac
      [ -f "$f" ] || { echo "=== waitq: no log $f: stop"; exit 1; }
      until grep -qs "^EXIT" "$f"; do sleep 60; done; echo "=== $j finished $(date -u +%T)";;
    mm9) mm qwen3.5-9b qwen35_9b_ "12-16" 32;;
    mm27) mm qwen3.6-27b "" "32-40" 16;;
    mmmuse) mm muse-glimmer-30b muse30_ "36-42" 32;;
    mm122) mm qwen3.5-122b-a10b qwen35_122b_ "39-45 24-30" 8;;
    nat9) nat qwen3.5-9b qwen35_9b_ natural_v1_chat 12-16 32; nat qwen3.5-9b qwen35_9b_ natural_v1_qa 12-16 32;;
    nat27) nat qwen3.6-27b "" natural_v1_chat 32-40 32; nat qwen3.6-27b "" natural_v1_qa 32-40 32;;
    natmuse) nat muse-glimmer-30b muse30_ natural_v1_chat 36-42 32; nat muse-glimmer-30b muse30_ natural_v1_qa 36-42 32;;
    nat122) nat qwen3.5-122b-a10b qwen35_122b_ natural_v1_chat 39-45 8; nat qwen3.5-122b-a10b qwen35_122b_ natural_v1_qa 39-45 8;;
    ctl9) natctl qwen3.5-9b qwen35_9b_ natural_v1_chat 12-16 32;;
    ctl27) natctl qwen3.6-27b "" natural_v1_chat 32-40 32;;
    ctlmuse) natctl muse-glimmer-30b muse30_ natural_v1_chat 36-42 32;;
    nat122b)  # 10B note 3: L39-45 breaks every word on natural chat; the 122B's other band of record, L24-30
      export BJ_TARGET=qwen3.5-122b-a10b; c=qwen35_122b_natural_v1_chat_competence_v1; r=qwen35_122b_natural_v1_chat_ko_l2430_v1
      T="--tasks natural_v1_chat --tasks-competence $c --tasks-words PP PM MP MM --tasks-level all --n 1000 --batch 8 --kinds clean"
      run ablate_v2/$r $PY scripts/ablate_v2.py --name $r --why "$WHY: the 122B, C1 on natural_v1_chat at L24-30 (L39-45 broke every word)" \
        --plan bands --bands 24-30 --conditions paper10 paper10_rot $T > /workspace/scratch/$r.log 2>&1 \
        && $PY scripts/c1_v2.py $r --middle L24-30 --set natural_v1_chat | tail -2 || echo "=== 122B natural L24-30 FAILED"
      run ablate_v2/${r%_v1}_unembed_v1 $PY scripts/ablate_v2.py --name ${r%_v1}_unembed_v1 --why "$WHY: the 122B, the logit-lens control on natural_v1_chat at L24-30" \
        --plan bands --bands 24-30 --conditions unembed10 unembed10_rot $T > /workspace/scratch/${r%_v1}_unembed_v1.log 2>&1 \
        && $PY scripts/c1_specificity.py $r ${r%_v1}_unembed_v1 --set natural_v1_chat | tail -3 | sed "s/^/=== spec 122B L24-30: /" || echo "=== 122B L24-30 unembed FAILED";;
    ctl122) natctl qwen3.5-122b-a10b qwen35_122b_ natural_v1_chat 39-45 8;;
    mp9) mp qwen3.5-9b qwen35_9b_ full_v8 qwen35_9b_full_v8_competence_v1 "12-16" 32;;
    mp27) mp qwen3.6-27b "" full_v8 full_v8_competence_v1 "32-40" 16;;
    mpmuse) mp muse-glimmer-30b muse30_ full_v8 muse30_full_v8_competence_v1 "36-42" 32;;
    mp122) mp qwen3.5-122b-a10b qwen35_122b_ full_v8_two qwen35_122b_full_v8_two_competence_v1 "39-45 24-30" 8;;
  esac
done
echo "=== amendment 10 GPU $G done $(date -u +%FT%TZ)"
