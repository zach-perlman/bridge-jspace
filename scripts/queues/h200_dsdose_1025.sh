#!/bin/bash
# Zach (2026-10-25, prereg amendment 43): after DeepSeek's profile chain (h200ds42): its removal-size curve at the
# profile pick (dev), then, only if its test M - K at the pick is >= 15, the question-only knock-out there (paper10 /
# rot; h200_depth_42.sh). Lightning's chain waits for this one's exit. Usage: h200_dsdose_1025.sh
set -u
cd /workspace/bridge-jspace
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
echo "=== start $(date -u +%FT%TZ)"
until grep -qs "^EXIT" $R-h200ds42-1025-1700.log; do sleep 60; done
fails=0
bash scripts/queues/h200_dose_1025.sh 0,1 dose:deepseek-v4-flash:dsv4f_:16:40 || fails=$((fails + 1))
band=$(BJ_TARGET=deepseek-v4-flash .venv/bin/python scripts/profile_pick.py dsv4f_jsuite_v2_dev_chat_profile_cand2_v1 2>/dev/null)
mk=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['facts']['paper10/start=all']['contrasts']['M-K']['diff'])" \
  results/ablate_v2/jsuite2_score/dsv4f_jsuite_v2_test_chat_ko_cand2_L${band}_v1.json 2>/dev/null || echo nan)
echo "=== DSDOSE test M-K at L$band: $mk"
if python3 -c "import sys; sys.exit(0 if float(sys.argv[1]) >= 15 else 1)" "$mk" 2>/dev/null; then
  bash scripts/queues/h200_depth_42.sh 0,1 pos:deepseek-v4-flash:dsv4f_:$band:16:question || fails=$((fails + 1))
fi
echo "=== dsdose done, $fails failed $(date -u +%FT%TZ)"
exit $fails
