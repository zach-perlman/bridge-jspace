#!/usr/bin/env bash
# 122B follow-up (Zach, 2026-10-20 overnight), after scripts/queues/overnight_1020.sh: the new settings on the larger
# model (Neel: results only matter if they generalise; try larger models early). Qwen3.5-122B-A10B FP8, its published
# J++, layers 36 and 39 (its window, as qwen35_122b_rw_v1). A failed step is logged and the queue goes on.
#   1 the J-space removal (ablate_pilot v1 setting) on the suite's main families, the tool-output set and the countries
#   2 the tool-output set: competence, read/write
#   3 TwoHopFact screening on this model, then natural_rw v3 (NM/NL with removal)
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=qwen3.5-122b-a10b BJ_BATCH=16
FAILED=0
step() { echo "=== STEP $1 $(date -u +%H:%M:%S)"; shift; "$@" || { echo "=== FAILED (exit $?)"; FAILED=$((FAILED + 1)); }; }
PY="uv run --no-sync python"
W="Zach (2026-10-20, overnight): the 27B's new settings on Qwen3.5-122B-A10B (does it generalise to a larger model?)"
step "tool manifest smoke" $PY scripts/suite_v1.py manifest --set tool --name qwen35_122b_tool_smoke_1020 --limit 4 --why "smoke"
step "tool competence smoke" $PY scripts/suite_v1.py competence --name qwen35_122b_tool_smoke_1020
step "tool manifest" $PY scripts/suite_v1.py manifest --set tool --name qwen35_122b_competence_tool_v1 --limit 150 \
  --why "$W (tool-output set competence, first 150 per family)"
step "tool competence" $PY scripts/suite_v1.py competence --name qwen35_122b_competence_tool_v1
step "removal smoke" $PY scripts/ablate_pilot.py --name qwen35_122b_abl_smoke_1020 --n 2 --layers 36 39 \
  --comp-main qwen35_122b_competence_v1 --comp-computed none --comp-tool qwen35_122b_competence_tool_v1 --countries-build --why "smoke"
step "removal" $PY scripts/ablate_pilot.py --name qwen35_122b_abl_v1 --n 100 --layers 36 39 \
  --comp-main qwen35_122b_competence_v1 --comp-computed none --comp-tool qwen35_122b_competence_tool_v1 --countries-build \
  --why "$W (J-space removal, the v1 setting, at its window layers)"
step "tool rw" $PY scripts/read_write.py --name qwen35_122b_tool_rw_v1 --n 100 --from-competence qwen35_122b_competence_tool_v1 \
  --families TBL TBR --layers 36 39 --scales 0.5 1 2 4 8 16 --no-countries --why "$W (tool-output set, read and write)"
step "twohop screen" $PY scripts/twohop_pilot.py competence --screen --name qwen35_122b_screen_v1 \
  --why "$W (TwoHopFact screening: which facts this model knows)"
step "natural v3 smoke" $PY scripts/natural_rw.py --name qwen35_122b_v3_smoke_1020 --n 4 --versions NM NL --ablate \
  --layers 36 39 --screen-run qwen35_122b_screen_v1 --why "smoke"
step "natural v3" $PY scripts/natural_rw.py --name qwen35_122b_v3_lookup --n 150 --versions NM NL --ablate --layers 36 39 \
  --screen-run qwen35_122b_screen_v1 --why "$W (natural lookup v3: read, write and removal)"
echo "=== QUEUE DONE failed=$FAILED"
exit $FAILED
