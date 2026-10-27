#!/bin/bash
# One step of the Muse grid (Dan, 26 Oct, overnight; batch 38), run unattended by a jobq job:
#   bash scripts/muse_step.sh RESULT_DIR NAME 'COMMAND with {N} for the run name'
# - runs COMMAND with the readers' gate at 0.80 (G1, fixed in advance);
# - if the run's gate.json says the gate missed: reruns as NAME_g75 with BJ_GATE=0.75 (after the data, descriptive,
#   not scored; Dan's fallback for G1 in [0.75, 0.80)); if that misses too: "NOT TESTED" (below 0.75: stop);
# - an OOM / CUDA / preemption failure is retried once (the partial run folder renamed *_failed_try1), then skipped;
# - a code error is logged and skipped (exit 1; later jobs do not depend on it).
# RESULT_DIR "-" = no gate file to check. Every line it prints starts with [muse_step].
rdir=$1 name=$2 tmpl=$3
n=$name gate=0.80 try=1
while true; do
  log=$(mktemp)
  echo "[muse_step] start $n (gate $gate, try $try)"
  (export BJ_GATE=$gate; eval "${tmpl//\{N\}/$n}") 2>&1 | tee "$log"
  rc=${PIPESTATUS[0]}
  if [ "$rdir" != "-" ] && python3 scripts/gate_missed.py "results/$rdir/$n"; then
    if [ "$gate" = 0.80 ]; then
      echo "[muse_step] gate missed at 0.80: rerun after the data at 0.75 as ${name}_g75"
      gate=0.75 n=${name}_g75 try=1
      continue
    fi
    echo "[muse_step] NOT TESTED $n: the gate missed at 0.75 too"
    exit 0
  fi
  if [ "$rc" -eq 0 ]; then echo "[muse_step] DONE $n"; exit 0; fi
  if [ "$try" -eq 1 ] && grep -qiE "out of memory|CUDA error|cuda runtime|NCCL|illegal memory|Killed|preempt" "$log"; then
    [ "$rdir" != "-" ] && [ -d "results/$rdir/$n" ] && mv "results/$rdir/$n" "results/$rdir/${n}_failed_try1"
    echo "[muse_step] OOM / CUDA failure: retry once"
    try=2
    continue
  fi
  echo "[muse_step] SKIPPED $n (exit $rc)"
  exit 1
done
