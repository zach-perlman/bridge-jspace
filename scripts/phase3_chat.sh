#!/usr/bin/env bash
# Block 3 of the overnight plan (Zach, 2026-10-19: "Chat with that prefill"): B1 and exp09 re-run in the chat format
# (bridge_jspace.chat: chat template, thinking off, "Answer:" prefilled), with the published J++.
#   bash scripts/phase3_chat.sh   (on the GPU box)
# exp01's probes are rebuilt in the chat format (variant more_jpp_chat), then exp02's gate, main, matched and Phase 2c's
# own-word condition on them, then exp09's R/B, L and RL maps, parts and swaps. A failed block is reported and the next
# independent block still runs.
set -uo pipefail
cd /workspace/bridge-jspace; export PATH="$HOME/.local/bin:$PATH"; set -a; [ -f .env ] && . ./.env; set +a
PY="uv run python"
stamp() { echo "=== $(date -u +%H:%M:%S) $*"; }
WHY="Chosen by the human (Zach, 2026-10-19): part B re-run in the chat format (chat template, thinking off, 'Answer:' \
prefilled), where the model answers every exp09 item and 86% of B1's questions (exp20), with the published J++. \
Prediction: the raw-text verdicts hold (B1: J-part above the remainder and the matched control; exp09: B inside, L and \
RL outside, R's J-part swap above its matched control)."
TAG=v4_chat_jpp

stamp "exp01 chat probes ($TAG)"
if $PY scripts/exp01_probes.py run --variant more_jpp_chat --tag $TAG; then P_OK=1; else P_OK=0; stamp "exp01 FAILED"; fi

if [ $P_OK = 1 ]; then
  stamp "exp02 gate_chat_v1"
  $PY scripts/exp02_swaps.py manifest gate --probes $TAG --name gate_chat_v1 --prompt-end chat_prefill \
    && $PY scripts/exp02_swaps.py run gate_chat_v1 || stamp "exp02 gate FAILED"
  BAND=$(python3 -c "import json; print(json.load(open('results/exp02_swaps/gate_chat_v1/summary.json'))['decision']['band'])" 2>/dev/null || echo 24-40)
  stamp "exp02 band $BAND"
  for spec in "main_chat_v1:" "matched_chat_v1:jpart jpart_matched" "own_chat_v1:raw_jlens jpart jpart_minus_own jpart_matched"; do
    name=${spec%%:*}; conds=${spec#*:}
    stamp "exp02 $name ($conds)"
    $PY scripts/exp02_swaps.py manifest main --probes $TAG --band $BAND --gate gate_chat_v1 --prompt-end chat_prefill \
      --name $name ${conds:+--conditions $conds} && $PY scripts/exp02_swaps.py run $name || stamp "exp02 $name FAILED"
  done
fi

for spec in "map_chat_v1:parts_chat_v1:bind_recall" "map_lookup_chat_v1:parts_lookup_chat_v1:bind_lookup_v2" \
            "map_rl_chat_v1:parts_rl_chat_v1:recall_lookup"; do
  IFS=: read -r map parts items <<< "$spec"
  stamp "exp09 $map ($items)"
  if $PY scripts/exp09_bind_recall.py manifest_map --name $map --items $items --format chat_prefill --why "$WHY" \
      && $PY scripts/exp09_bind_recall.py run_map $map; then
    stamp "exp09 $parts"
    $PY scripts/exp09_bind_recall.py manifest_parts --name $parts --map $map --lens jpp --why "$WHY" \
      && $PY scripts/exp09_bind_recall.py run_parts $parts || stamp "exp09 $parts FAILED"
  else
    stamp "exp09 $map FAILED"
  fi
done

if [ $P_OK = 1 ] && [ -f results/exp09_bind_recall/map_chat_v1/summary.json ]; then
  stamp "exp09 swaps_chat_v1 (probes $TAG, band $BAND)"
  $PY scripts/exp09_bind_recall.py manifest_swaps --name swaps_chat_v1 --probes $TAG --swap-map map_chat_v1 \
    --band $BAND --why "$WHY" && $PY scripts/exp09_bind_recall.py run_swaps swaps_chat_v1 || stamp "exp09 swaps FAILED"
fi
stamp done
