#!/bin/bash
# Zach (2026-10-28, prereg amendment 58 note 10): the end of the queue. Usage:
#   h200_end_1028.sh prep GPU WAITJOB          Muse's held v3 runs, then (only if they finished) drop Muse's and Ministral's
#                                              caches and download Bolt (Zach's OK, 28 Oct); prints BOLT READY
#   h200_end_1028.sh bolt PREPJOB WAITJOB ...  after all: Bolt (both GPUs) v3 competence on RM (smoke first), then the
#                                              never-named swap at L42-53, k 10 30 100
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
W="Zach (2026-10-28, prereg amendment 58 note 10)"
waitjob() { echo "=== waiting for $1 $(date -u +%T)"; until grep -qsE "^EXIT [0-9]+" /workspace/runs/$1.log; do sleep 60; done; echo "=== $1 ended: $(grep -E '^EXIT' /workspace/runs/$1.log | tail -1)"; }
mode=$1; shift
if [ "$mode" = prep ]; then
  G=$1; waitjob $2
  bash scripts/queues/h200_v3next_1028.sh $G cv:muse30 ko:muse30:jsuite_v3_test_chat cv21:muse30
  if [ -f results/ablate_v2/muse30_jsuite_v3_test_chat_ko_cand2_v1/summary.json ] && [ -f results/competence_variants/muse30_jsuite_v3_cv_v1/summary.json ]; then
    echo "=== dropping Muse's and Ministral's weight caches (Zach's OK, 28 Oct) $(date -u +%T)"
    rm -rf /workspace/hf_cache/hub/models--meta-models--Muse-Glimmer-30B /workspace/hf_cache/hub/models--mistralai--Ministral-3-14B-Instruct-2512-BF16
  else
    echo "=== Muse's runs did not all finish: no cache drop, no Bolt"; exit 3
  fi
  free=$(df --output=avail -BG /workspace | tail -1 | tr -dc 0-9)
  echo "=== free ${free}G $(date -u +%T)"
  [ "$free" -ge 160 ] || { echo "=== under 160G free: no Bolt download"; exit 3; }
  .venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16', revision='e09a4cedb1787db1760375ee5539f222cae0c672')" \
    > /workspace/scratch/bolt_download_1028.log 2>&1 || { echo "=== Bolt download FAILED"; tail -3 /workspace/scratch/bolt_download_1028.log; exit 3; }
  echo "=== free after: $(df --output=avail -BG /workspace | tail -1 | tr -dc 0-9)G"
  echo "BOLT READY $(date -u +%T)"
elif [ "$mode" = bolt ]; then
  PREP=$1; shift
  waitjob $PREP
  grep -qa "^BOLT READY" /workspace/runs/$PREP.log || { echo "=== Bolt not ready"; exit 3; }
  for j in "$@"; do waitjob $j; done
  export CUDA_VISIBLE_DEVICES=0,1 BJ_TARGET=nemotron-3.5-bolt
  C=nem35b_jsuite_v3_test_chat_competence_cand2_v1
  $PY scripts/natural_v1.py competence --set jsuite_v3_test_chat --name nem35b_jsuite_v3_test_chat_competence_smoke1028 --words RM --read cand2 --hop1 gen \
    --limit 8 --why "$W: smoke" > /workspace/scratch/bolt_comp_smoke.log 2>&1 || { echo "=== Bolt smoke FAILED"; tail -5 /workspace/scratch/bolt_comp_smoke.log; exit 3; }
  mv results/tasks_v2/nem35b_jsuite_v3_test_chat_competence_smoke1028 /workspace/scratch/
  echo "=== Bolt smoke OK $(date -u +%T)"
  [ -f results/tasks_v2/$C/summary.json ] || $PY scripts/natural_v1.py competence --set jsuite_v3_test_chat --name $C --words RM --read cand2 --hop1 gen \
    --why "$W: Bolt v3 competence on the never-named items (eligibility)" > /workspace/scratch/$C.log 2>&1 || { echo "=== $C FAILED"; tail -3 /workspace/scratch/$C.log; exit 3; }
  echo "=== done $C $(date -u +%T)"
  r=nem35b_nn_swap_L42-53_v1
  [ -f results/nn_swap/$r/summary.json ] || $PY scripts/nn_swap.py --name $r --why "$W: Bolt never-named swap at L42-53" --band 42-53 --competence $C \
    --words RM --scene-words RM --ks 10 30 100 > /workspace/scratch/$r.log 2>&1 || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; exit 3; }
  echo "=== done $r $(date -u +%T)"
fi
