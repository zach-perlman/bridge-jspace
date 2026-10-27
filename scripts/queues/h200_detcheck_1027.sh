#!/bin/bash
# Zach (2026-10-27, amendment 56 B): Lightning determinism check. Its facts knock-out rerun at HEAD with the clean
# rerun's eligibility, conditions, batch and QR path, compared row by row with the clean rerun (775f83d).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=${1:-1} BJ_TARGET=nemotron-3.5-lightning
unset BJ_GRAM_PROJ
r=nem35l_jsuite_v2_test_chat_ko_cand2_detcheck_v1
echo "=== DETCHECK ablate_v2/$r $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || uv run --no-sync python scripts/ablate_v2.py --name $r --why "Zach (2026-10-27, amendment 56 B): Lightning determinism check" \
  --plan bands --bands 27-33 --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks jsuite_v2_test_chat \
  --tasks-competence nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1 --tasks-words PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN \
  --tasks-level all --n 1000 --kinds clean --batch 16 --read cand2 > /workspace/scratch/$r.log 2>&1 < /dev/null || { echo "=== DETCHECK FAILED"; tail -3 /workspace/scratch/$r.log; exit 1; }
.venv/bin/python - $r <<'PY'
import json, sys
k = lambda x: (x["family"], x["id"], x["kind"], x["band"], x["condition"])
a = {k(x): x for x in map(json.loads, open(f"results/ablate_v2/{sys.argv[1]}/rows.jsonl"))}
b = {k(x): x for x in map(json.loads, open("/workspace/clean_bridge/results/ablate_v2/nem35l_clean_jsuite_v2_test_chat_ko_cand2_v1/rows.jsonl"))}
sh = set(a) & set(b); d = sorted(abs(a[x]["logp"] - b[x]["logp"]) for x in sh)
print(f"=== DETCHECK rows here {len(a)} clean {len(b)} shared {len(sh)}; answers differ {sum(a[x]['correct'] != b[x]['correct'] for x in sh)}; logp identical {sum(v == 0 for v in d)}; max |diff| {d[-1]:.2e}")
PY
