#!/bin/bash
# Zach (2026-10-23, prereg amendment 9). Usage: h200_amend9_1023.sh GPU STEP [STEP ...]
#   steps: diag (B: the diagnostic on the 9B, Qwen3-32B, Olmo-Hybrid, Olmo-3); s27 / s32 / smuse / s122 (A: a data seed);
#          c2muse / c2q9 / c2q27 (C: C2 on fresh_v8s2); all122 (D: the 122B at every lens layer); wait122 (wait for the
#          122B steering to leave GPU 1).
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
. scripts/queues/lib_competence_parallel.sh
WHY="Zach (2026-10-23, prereg amendment 9)"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }

diag() {  # diag TARGET PREFIX BAND [--set S --competence C]
  export BJ_TARGET=$1; local p=$2 b=$3; shift 3
  run muse_diag/${p}diag_L${b}_v1 $PY scripts/muse_diag.py --name ${p}diag_L${b}_v1 --why "$WHY: the Muse diagnostic, $BJ_TARGET at its C1 band" \
    --band $b --n 60 "$@" 2>&1 | grep -a "^DIAG\|^===" || echo "=== diag $BJ_TARGET FAILED"
}

c1_seed() {  # c1_seed TARGET PREFIX SET RUN MID "BANDS" BATCH
  export BJ_TARGET=$1; local p=$2 set=$3 run=$4 mid=$5 bands=$6 batch=$7 c=${2}${3}_competence_v1
  echo "=== $1 on $set $(date -u +%T)"
  comp_parallel 1 "$WHY: $1 on $set" $c:$set || { echo "=== $1 competence FAILED"; return 1; }
  local T="--tasks $set --tasks-competence $c --tasks-words PP PM MP MM CP CM --tasks-level all"
  [ -f results/ablate_v2/${p}${run}_smoke_1023/summary.json ] || $PY scripts/ablate_v2.py --name ${p}${run}_smoke_1023 --why smoke --plan bands --bands $mid \
    --conditions paper10 paper10_rot $T --n 2 --kinds clean --batch 8 > /workspace/scratch/${p}${run}_smoke.log 2>&1 \
    || { echo "=== $1 smoke failed"; tail -3 /workspace/scratch/${p}${run}_smoke.log; return 1; }
  run ablate_v2/${p}${run} $PY scripts/ablate_v2.py --name ${p}${run} --why "$WHY: $1 C1 on $set at its fixed band(s) $bands" --plan bands --bands $bands \
    --conditions paper10 paper10_rot $T --n 1000 --kinds clean --batch $batch \
    && $PY scripts/c1_v2.py ${p}${run} --middle L$mid --set $set | tail -2 || echo "=== $1 C1 FAILED"
}

c2_fresh() {  # c2_fresh TARGET PREFIX BATCH STEER...
  export BJ_TARGET=$1; local p=$2 batch=$3 c=${2}fresh_v8s2_competence_v1 run=${2}wm2_fresh2_v1; shift 3
  comp_parallel 1 "$WHY: $BJ_TARGET on fresh_v8s2" $c:fresh_v8s2 || { echo "=== $BJ_TARGET competence FAILED"; return 1; }
  run write_max/$run env BJ_SUITE_BATCH=$batch $PY scripts/write_max.py --name $run --why "$WHY: $BJ_TARGET C2 on a fresh data seed, its full_v8 settings" \
    --n 1000 "$@" --tasks fresh_v8s2 --tasks-competence $c --tasks-level all --families PP PM MP MM CP CM \
    && $PY scripts/c2_graded.py $run | tail -3 && $PY scripts/c2_graded.py $run --drop-guessable > /dev/null \
    && $PY scripts/c2_narrow.py $run ${run}_noguess | tail -1 || echo "=== $BJ_TARGET C2 FAILED"
}

for step in "$@"; do
  case $step in
    diag)
      diag qwen3.5-9b qwen35_9b_ 12-16
      diag qwen3-32b qwen3_32b_ 44-52
      diag olmo-hybrid-7b olmoh7_ 4-8 --set olmo_big_v8nc --competence olmoh7_olmo_big_v8nc_competence_v1
      diag olmo-3-7b olmo3d7_ 10-14 --set olmo_big_v8nc --competence olmo3d7_olmo_big_v8nc_competence_v1;;
    s27) c1_seed qwen3.6-27b "" fresh_v8s3 fresh3_ko_v1 32-40 "32-40" 32;;
    s32) c1_seed qwen3-32b qwen3_32b_ fresh_v8s3 fresh3_ko_v1 44-52 "44-52" 32;;
    smuse) c1_seed muse-glimmer-30b muse30_ fresh_v8s2 fresh2_ko_v1 36-42 "36-42" 32;;
    s122) c1_seed qwen3.5-122b-a10b qwen35_122b_ fresh_v8s2 fresh2_ko_v1 39-45 "39-45 24-30" 8;;
    c2muse) c2_fresh muse-glimmer-30b muse30_ 64 --possets question final --band 23-33 --single-step 2 --early 13 16 20 \
              --writes lens_add lens_swap copy early_lens_add early_embed_add;;
    c2q9) c2_fresh qwen3.5-9b qwen35_9b_ 64 --possets question final --band 14-20 --single-step 1 --early 8 10 12;;
    c2q27) c2_fresh qwen3.6-27b "" 64 --possets question final;;
    all122)
      export BJ_TARGET=qwen3.5-122b-a10b
      run ablate_v2/qwen35_122b_full2_ko_all_v1 $PY scripts/ablate_v2.py --name qwen35_122b_full2_ko_all_v1 --why "$WHY: the 122B at every lens layer (D)" \
        --plan bands --bands 0-46 --conditions paper10 paper10_rot --tasks full_v8_two --tasks-competence qwen35_122b_full_v8_two_competence_v1 \
        --tasks-words PP PM MP MM CP CM --tasks-level all --n 1000 --kinds clean --batch 8 \
        && $PY scripts/c1_v2.py qwen35_122b_full2_ko_all_v1 --middle L0-46 --set full_v8_two | tail -2 || echo "=== 122B all-layer FAILED";;
    waitc27)  # 2026-10-23 ~06:20: the queue was restarted with fewer steps; the 27B's competence kept running on its own
      while [ ! -f results/tasks_v2/fresh_v8s3_competence_v1/summary.json ] && pgrep -f "[n]ame fresh_v8s3_competence_v1" > /dev/null; do sleep 30; done
      echo "=== 27B competence on fresh_v8s3: $([ -f results/tasks_v2/fresh_v8s3_competence_v1/summary.json ] && echo done || echo MISSING) $(date -u +%T)";;
    wait122)
      until grep -qs "^EXIT" $R-h200q122bsteer-1023-0435.log && [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 135000 ]; do sleep 60; done
      echo "=== GPU $G free $(date -u +%T)";;
  esac
done
echo "=== amendment 9 GPU $G done $(date -u +%FT%TZ)"
