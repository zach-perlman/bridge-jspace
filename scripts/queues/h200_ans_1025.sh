#!/bin/bash
# Zach (2026-10-25, prereg amendment 38 A): what the J-part at the bridge mention carries. scripts/jswap.py on v2 (read and
# tracked starts, the v2 knock-out's eligibility) with swap, swap_ans (only the two answers' J-directions), swap_ans_u
# (their logit-lens directions), swap_ans_rot (same-size random change) and swap_noans (the top-10 J-part without the
# answers' directions); then the memory finals pooled (PM PA PN TM TA TN) per condition.
# Usage: h200_ans_1025.sh GPU STEP ...   waitq:JOB  mem:GB  ans:TARGET:PREFIX:BAND:BATCH
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
fails=0
for step in "$@"; do
  IFS=: read -r kind a b c d <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done
      echo "=== GPU $G has $a GB free $(date -u +%T)";;
    ans)
      export BJ_TARGET=$a; p=$b; band=$c; batch=$d; r=${p}jswap_ans_v2_v1; cn=${p}jsuite_v2_test_chat_competence_cand2_v1
      echo "=== jswap/$r at L$band $(date -u +%T)"
      if [ ! -f results/jswap/$r/summary.json ]; then
        $PY scripts/jswap.py --name $r --why "Zach (2026-10-25, prereg amendment 38 A): $a at L$band" --set jsuite_v2_test_chat --band $band \
          --competence $cn --batch $batch --conds swap swap_ans swap_ans_u swap_ans_rot swap_noans > /workspace/scratch/$r.log 2>&1 \
          || { echo "=== $a ans FAILED"; tail -3 /workspace/scratch/$r.log; fails=$((fails + 1)); continue; }
      fi
      grep -E "^(PM|TM|PK|TK|PP|TP) (swap|swap_ans|swap_ans_u|swap_ans_rot|swap_noans) " /workspace/scratch/$r.log | sed "s/^/=== ANS $a /"
      $PY - $r <<'PY' | sed "s/^/=== ANS $a pooled: /"
import json, sys
sys.path.insert(0, "src"); sys.path.insert(0, ".")
from scripts.jswap import score
rows = [json.loads(x) for x in open(f"results/jswap/{sys.argv[1]}/rows.jsonl")]
s = score([{**r, "family": "MEM"} for r in rows if r["family"][1] in "MAN"])
print("  ".join(f"{c} {s[f'MEM/{c}']['transfer']:+.1f} {s[f'MEM/{c}']['ci']} (n {s[f'MEM/{c}']['n_third']})" for c in ("swap", "swap_ans", "swap_ans_u", "swap_ans_rot", "swap_noans")))
PY
      ;;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== ans GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
