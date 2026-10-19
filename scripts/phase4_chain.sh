#!/usr/bin/env bash
# Blocks 4-6 of the overnight plan (Zach, 2026-10-19), all in the chat format with the published J++, after
# phase3_chat.sh (whose exp02 chat gate gives the swap band and whose exp09 map map_chat_v1 gives R's and B's items):
#   4  Phase 2a: contrastive bridge directions (exp21, R and B), then exp09's swaps with them
#   5  Phase 3: the use-vs-answer-source families (data/use_source.json): exp20's competence row first, then the map
#      and parts; each family's reliability (Wilson lower bound >= 85%, README Decisions) reported next to its verdict
#   6  brew's composition misses (exp22)
#   8  (stretch) an arithmetic intermediate (exp23)
#   bash scripts/phase4_chain.sh   (on the GPU box)
set -uo pipefail
cd /workspace/bridge-jspace; export PATH="$HOME/.local/bin:$PATH"; set -a; [ -f .env ] && . ./.env; set +a
PY="uv run python"
stamp() { echo "=== $(date -u +%H:%M:%S) $*"; }
BAND=$(python3 -c "import json; print(json.load(open('results/exp02_swaps/gate_chat_v1/summary.json'))['decision']['band'])" 2>/dev/null || echo 24-40)
stamp "band $BAND (exp02 gate_chat_v1)"

# 3b, the gate rule's debug step: gate_chat_v1 failed (full probe 1-8%) with probes built at the prefill's ':' while
# the lens's own vectors flipped 45-62%. Probes at the statement's last token in the user turn, then the gate again;
# B1's main, matched and Phase 2c runs (and exp09's R/B swaps) only if this gate passes.
WHY3B="Chosen by the agent under Zach's overnight approval (2026-10-19): the debug step after gate_chat_v1 failed \
(full probe 8% < 30%): exp01's chat probes taken at the statement's last token in the user turn, not the prefill's ':'."
STAG=v4_chat_stmt_jpp
stamp "3b exp01 $STAG"
if $PY scripts/exp01_probes.py manifest --variant more_jpp_chat_stmt \
   && $PY scripts/exp01_probes.py run --variant more_jpp_chat_stmt --tag $STAG \
   && $PY scripts/exp02_swaps.py manifest gate --probes $STAG --name gate_chat_stmt_v1 --prompt-end chat_prefill \
   && $PY scripts/exp02_swaps.py run gate_chat_stmt_v1; then
  GO=$(python3 -c "import json; print(json.load(open('results/exp02_swaps/gate_chat_stmt_v1/summary.json'))['decision']['go'])")
  SBAND=$(python3 -c "import json; print(json.load(open('results/exp02_swaps/gate_chat_stmt_v1/summary.json'))['decision']['band'])")
  stamp "3b gate_chat_stmt_v1: go=$GO band=$SBAND"
  if [ "$GO" = True ]; then
    BAND=$SBAND
    for spec in "main_chat_stmt_v1:" "matched_chat_stmt_v1:jpart jpart_matched" "own_chat_stmt_v1:raw_jlens jpart jpart_minus_own jpart_matched"; do
      name=${spec%%:*}; conds=${spec#*:}
      stamp "3b exp02 $name ($conds)"
      $PY scripts/exp02_swaps.py manifest main --probes $STAG --band $BAND --gate gate_chat_stmt_v1 --prompt-end chat_prefill \
        --name $name ${conds:+--conditions $conds} && $PY scripts/exp02_swaps.py run $name || stamp "3b exp02 $name FAILED"
    done
    stamp "3b exp09 swaps_chat_stmt_v1"
    $PY scripts/exp09_bind_recall.py manifest_swaps --name swaps_chat_stmt_v1 --probes $STAG --swap-map map_chat_v1 \
      --band $BAND --why "$WHY3B" && $PY scripts/exp09_bind_recall.py run_swaps swaps_chat_stmt_v1 || stamp "3b swaps FAILED"
  else
    stamp "3b the gate failed again: B1's chat runs stop here (report and debug further)"
  fi
else
  stamp "3b FAILED"
fi

# Phase 2c in the verified B1 setting (raw text, the B200 probes, band 24-40): own_chat_v1 found the J-part's flips
# carried by the entities' own word directions (jpart_minus_own 0%); this asks the same of the verified result.
stamp "2c exp02 own_v1 (raw, v3_jpp_b200)"
$PY scripts/exp02_swaps.py manifest main --probes v3_jpp_b200 --band 24-40 --gate gate_v4_b200 \
  --conditions raw_jlens jpart jpart_minus_own jpart_matched --name own_v1 --gate-reason "Zach approved Phase 2c on \
the B200 probes (2026-10-19); gate_v4_b200's full probe was 28.6%, as close to 30% as v4's gate, whose main runs B1 rests on." \
  && $PY scripts/exp02_swaps.py run own_v1 || stamp "2c own_v1 FAILED"

stamp "5a exp20 competence rows for LM, RM, BT, RT"
$PY scripts/exp20_competence.py manifest --name use_source_v1 --tasks LM RM BT RT --why "Zach (2026-10-19): Phase 3's \
families get a competence row before any edit (README Decisions: task competence is part of the research)." \
  && $PY scripts/exp20_competence.py run --name use_source_v1 || stamp "5a FAILED"

WHY2A="Chosen by the human (Zach, 2026-10-19): Phase 2a, a stronger lens-free bridge direction than exp01's probes, from \
contrasts on exp09's own question (chat format, fit cities and names exp09's items never use). Prediction: the R \
direction's J-part swap flips R as exp01's did; the B direction moves B where exp01's probes did not (positive \
control), and B's J-part then carries it as B's copy split did (inside)."
for fam in R B; do
  stamp "4 exp21 contrast${fam}_v1"
  $PY scripts/exp21_contrastive.py manifest --tag contrast${fam}_v1 --family $fam --why "$WHY2A" \
    && $PY scripts/exp21_contrastive.py run --tag contrast${fam}_v1 || { stamp "4 exp21 $fam FAILED"; continue; }
  stamp "4 exp09 swaps_contrast${fam}_chat_v1"
  $PY scripts/exp09_bind_recall.py manifest_swaps --name swaps_contrast${fam}_chat_v1 \
    --probes exp21_contrastive/contrast${fam}_v1 --swap-map map_chat_v1 --band $BAND --why "$WHY2A" \
    && $PY scripts/exp09_bind_recall.py run_swaps swaps_contrast${fam}_chat_v1 || stamp "4 swaps $fam FAILED"
done

if [ -f results/exp20_competence/use_source_v1/summary.json ]; then
  # Reliability per family is reported next to its verdict (README Decisions: a task the model does not reliably do is
  # reported as such, not gated into shape); the map's own gate keeps the items each family answers.
  python3 -c "
import json
s = json.load(open('results/exp20_competence/use_source_v1/summary.json'))
for f in ('LM', 'RM', 'BT', 'RT'):
    c = s['cells'][f]['chat_prefill']['clean']
    print('=== 5 reliability', f, c['correct'], '/', c['n'], 'lower bound', round(c['ci'][0], 3), 'reliable' if c['ci'][0] >= 0.85 else 'NOT reliable')"
  WHY3="Chosen by the human (Zach, 2026-10-19): Phase 3, what uses the bridge vs where the answer comes from (L and \
RL confound them). Decision fixed in the manifest (use_source rule); a family below the reliability bar in exp20 \
use_source_v1 is reported, its verdict flagged."
  stamp "5 exp09 map_use_source_chat_v1"
  $PY scripts/exp09_bind_recall.py manifest_map --name map_use_source_chat_v1 --items use_source --format chat_prefill \
    --why "$WHY3" && $PY scripts/exp09_bind_recall.py run_map map_use_source_chat_v1 \
    && $PY scripts/exp09_bind_recall.py manifest_parts --name parts_use_source_chat_v1 --map map_use_source_chat_v1 \
      --lens jpp --why "$WHY3" && $PY scripts/exp09_bind_recall.py run_parts parts_use_source_chat_v1 \
    || stamp "5 map/parts FAILED"
fi

stamp "6 exp22 misses_v1"
$PY scripts/exp22_brew_misses.py manifest --name misses_v1 --why "Zach (2026-10-19): competence as data. On brew items \
the model gets wrong with each step right alone (exp20), is the intermediate formed?" \
  && $PY scripts/exp22_brew_misses.py run misses_v1 || stamp "6 FAILED"
stamp "8 exp23 arith_v1 (stretch)"
$PY scripts/exp23_arith.py manifest --name arith_v1 --why "Zach (2026-10-19, overnight plan, stretch): a computed \
intermediate (arithmetic in the prompt) next to brew's looked-up one. Prediction: outside, as brew." \
  && $PY scripts/exp23_arith.py run arith_v1 || stamp "8 FAILED"
stamp done
