#!/usr/bin/env bash
# B200 gate (Zach, 2026-10-20): the H200's paper10 stability run (1400 prompts, layers 32/36/40, TF32) repeated on the
# B200 with causal-conv1d; the B200 queue runs only if the two agree on >= 97% of items (H200 TF32 vs fp32: 99.0%).
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
T0=$(date +%s)
$PY scripts/ablate_v2.py --name b200_agree_paper10 --plan bands --bands 32,36,40 --conditions paper10 \
  --families BL BR RL RR TYPO TRANS R B --kinds clean hop --why "B200 gate: agreement with the H200 (paper10_stability_tf32)" || exit 1
echo "=== B200 run took $(( $(date +%s) - T0 ))s (H200: 82s of compute in its summary)"
$PY - <<'PY'
import json, statistics, sys
def rows(run):
    return {(r["family"], r["id"], r["kind"], r["condition"]): r for r in map(json.loads, open(f"results/ablate_v2/{run}/rows.jsonl"))}
a, b = rows("paper10_stability_tf32"), rows("b200_agree_paper10")
keys = sorted(set(a) & set(b))
same = statistics.mean(a[k]["correct"] == b[k]["correct"] for k in keys)
dl = statistics.median(abs(a[k]["logp"] - b[k]["logp"]) for k in keys)
none = [k for k in keys if k[3] == "none"]
print(f"items {len(keys)}: same correct {same:.4f}; median |d logp| {dl:.4f}; unedited right on B200 {statistics.mean(b[k]['correct'] for k in none):.4f}")
acc = lambda r, c: statistics.mean(r[k]["correct"] for k in keys if k[3] == c)
print(f"paper10 accuracy H200 {acc(a, 'paper10'):.3f} B200 {acc(b, 'paper10'):.3f}")
sys.exit(0 if same >= 0.97 else 1)
PY
