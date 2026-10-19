#!/usr/bin/env bash
# Step A on the H200 box (after the B200 box was lost): rebuild the user-turn chat probes, re-run B1's chat gate, main,
# matched and own-word runs (named _h200: re-runs of the lost _chat_stmt_v1 runs), for the own-word test by bridge kind
# and as a reproduction of the overnight numbers. A one-minute smoke test first.
#   bash scripts/recovery_A.sh   (on the GPU box)
set -uo pipefail
cd /workspace/bridge-jspace; export PATH="$HOME/.local/bin:$PATH"; set -a; [ -f .env ] && . ./.env; set +a
PY="uv run python"
stamp() { echo "=== $(date -u +%H:%M:%S) $*"; }
stamp "smoke: load the model, one chat answer"
$PY - <<'PY' || { stamp "smoke FAILED"; exit 1; }
import sys, torch
sys.path.insert(0, "src")
from bridge_jspace import chat
from bridge_jspace.model import load_model
m = load_model()
ids = m.encode(chat.chat_text(m.tokenizer, chat.blank_content("Fact: The capital of the country where Lyon is located is")))
print("smoke:", repr(m.generate_batch(ids, 8, [{}])[0]))
PY
TAG=v4_chat_stmt_jpp_h200
stamp "exp01 $TAG"
$PY scripts/exp01_probes.py manifest --variant more_jpp_chat_stmt \
  && $PY scripts/exp01_probes.py run --variant more_jpp_chat_stmt --tag $TAG || { stamp "exp01 FAILED"; exit 1; }
stamp "exp02 gate_chat_stmt_h200"
$PY scripts/exp02_swaps.py manifest gate --probes $TAG --name gate_chat_stmt_h200 --prompt-end chat_prefill \
  && $PY scripts/exp02_swaps.py run gate_chat_stmt_h200 || { stamp "gate FAILED"; exit 1; }
BAND=$(python3 -c "import json; print(json.load(open('results/exp02_swaps/gate_chat_stmt_h200/summary.json'))['decision']['band'])")
GO=$(python3 -c "import json; print(json.load(open('results/exp02_swaps/gate_chat_stmt_h200/summary.json'))['decision']['go'])")
stamp "gate: go=$GO band=$BAND"
REASON=""
[ "$GO" = True ] || REASON="Re-run of the lost gate_chat_stmt_v1 (it passed at 33% on the B200 box); run anyway to compare, by the agent under Zach's approval to continue on the new box (2026-10-19)."
for spec in "main_chat_stmt_h200:" "matched_chat_stmt_h200:jpart jpart_matched" "own_chat_stmt_h200:raw_jlens jpart jpart_minus_own jpart_matched"; do
  name=${spec%%:*}; conds=${spec#*:}
  stamp "exp02 $name"
  $PY scripts/exp02_swaps.py manifest main --probes $TAG --band $BAND --gate gate_chat_stmt_h200 --prompt-end chat_prefill \
    --name $name ${conds:+--conditions $conds} ${REASON:+--gate-reason "$REASON"} \
    && $PY scripts/exp02_swaps.py run $name || stamp "$name FAILED"
done
stamp done
