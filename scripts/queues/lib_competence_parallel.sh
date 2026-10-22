# Sourced by queue scripts (2026-10-22, speed-up): a model's tasks_v2 competence runs in parallel processes on one GPU.
# The runs are CPU-bound (one Python thread each; the GPU idles), so N at once take about the time of one; results are
# identical to running them one by one (each is its own process with the same code and data).
# Usage: comp_parallel MAX_PARALLEL "WHY" NAME:SET [NAME:SET ...]   (needs $PY and BJ_TARGET set; skips finished runs)
comp_parallel() {
  local maxp=$1 why=$2; shift 2
  local pids=() spec name set
  for spec in "$@"; do
    name=${spec%%:*}; set=${spec#*:}
    [ -f "results/tasks_v2/$name/summary.json" ] && { echo "=== $name done already"; continue; }
    while [ "$(jobs -rp | wc -l)" -ge "$maxp" ]; do sleep 10; done
    echo "=== competence $name ($set) $(date -u +%T)"
    $PY scripts/tasks_v2.py competence --set "$set" --name "$name" --guess --why "$why: competence on $set" > "/workspace/scratch/${name}.log" 2>&1 &
    pids+=($!)
  done
  local fail=0 p
  for p in "${pids[@]}"; do wait "$p" || fail=1; done
  [ $fail = 0 ] || echo "=== a competence run FAILED (see /workspace/scratch/<name>.log)"
  return $fail
}
