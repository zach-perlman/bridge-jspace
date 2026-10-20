#!/usr/bin/env bash
# Overnight queue (Zach, 2026-10-20), after the Gemma-it J++ fit: one model on the GPU at a time; a failed step is
# logged and the queue goes on; the job's exit code is the number of failed steps.
#   G  Gemma 4 31B-it with the J++ fit on it (BJ_TARGET=gemma-4-31b-it-refit): calibrate a gentler J-space removal
#      (decided by the random control alone, rule below), read/write with the countries as positive control, removal
#   Q  Qwen3.6-27B: the chosen gentle removal (does it keep the v1 removal's conclusions?), natural_rw v3 (NM/NL with
#      removal), the tool-output set (competence, read/write, removal)
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
FAILED=0
step() { echo "=== STEP $1 $(date -u +%H:%M:%S)"; shift; "$@" || { echo "=== FAILED (exit $?)"; FAILED=$((FAILED + 1)); }; }
PY="uv run --no-sync python"
WG="Zach (2026-10-20): does the memory-vs-prompt pattern hold on Gemma 4 31B-it with a J++ fit on the chat model itself (the base-model lens failed the positive control)?"
COMP="cases from gemma4itb_competence_v1 (same model and revision; competence does not use a lens)"

# --- G: Gemma with its own lens -------------------------------------------------------------------------------------
export BJ_TARGET=gemma-4-31b-it-refit
CAL="calibration of a gentler removal: chosen by the random control alone, the first of s1, s4, s1c, s4c (skip the first 1 or 4 positions; c = fit to the residual minus its WikiText mean) whose random-dictionary removal keeps every family/step's accuracy within 10 points of unedited; n=20"
for cfg in s1 s4 s1c s4c; do
  k=${cfg:1:1}; c=""; [[ $cfg == *c ]] && c="--center"
  step "gemma cal $cfg" $PY scripts/ablate_pilot.py --name gemma4itr_abl_cal_$cfg --n 20 --layers 30 33 36 --skip-first $k $c \
    --comp-main gemma4itb_competence_v1 --comp-computed gemma4itb_competence_computed_v1 --countries-build --why "$WG ($CAL)"
done
CHOSEN=$($PY - <<'EOF'
import json, pathlib
for cfg in ("s1", "s4", "s1c", "s4c"):
    p = pathlib.Path(f"results/ablate_pilot/gemma4itr_abl_cal_{cfg}/summary.json")
    if not p.exists():
        continue
    fams = json.loads(p.read_text())["families"]
    worst = min(f["accuracy"]["random"] - f["accuracy"]["none"] for f in fams.values())
    print(f"# {cfg}: worst random-minus-unedited accuracy {worst:+.2f}", file=__import__("sys").stderr)
    if worst >= -0.10:
        print(cfg)
        break
EOF
)
echo "=== chosen gentle removal: ${CHOSEN:-none}"
step "gemma rw smoke" $PY scripts/read_write.py --name gemma4itr_smoke_rw_1020 --n 2 --from-competence gemma4itb_competence_v1 \
  --families BL BR RL RR --layers 30 33 36 --scales 1 4 --why "smoke"
step "gemma rw" $PY scripts/read_write.py --name gemma4itr_rw_v1 --n 60 --from-competence gemma4itb_competence_v1 \
  --families BL BR RL RR --layers 30 33 36 --scales 0.5 1 2 4 8 16 --why "$WG (read and write, as gemma4itb_rw_v1; $COMP)"
if [[ -n ${CHOSEN:-} ]]; then
  k=${CHOSEN:1:1}; c=""; [[ $CHOSEN == *c ]] && c="--center"
  step "gemma removal" $PY scripts/ablate_pilot.py --name gemma4itr_abl_v1 --n 100 --layers 30 33 36 --skip-first $k $c \
    --comp-main gemma4itb_competence_v1 --comp-computed gemma4itb_competence_computed_v1 --countries-build \
    --why "$WG (J-space removal, the calibrated setting $CHOSEN; $COMP)"
fi

# --- Q: Qwen3.6-27B ------------------------------------------------------------------------------------------------
unset BJ_TARGET
WQ="Zach (2026-10-20, overnight)"
if [[ -n ${CHOSEN:-} ]]; then
  step "qwen gentle removal" $PY scripts/ablate_pilot.py --name abl_gentle_$CHOSEN --n 100 --skip-first $k $c \
    --why "$WQ: does the gentler removal calibrated on Gemma ($CHOSEN) keep the v1 removal's conclusions on the 27B?"
fi
WN="$WQ: natural lookup, v3: a recalled birth city used by a lookup only the prompt can answer (invented team colours, NL) vs the same context with the recalled country (NM); read, write and J-space removal"
step "natural v3 smoke" $PY scripts/natural_rw.py --name v3_smoke_1020 --n 4 --versions NM NL --ablate --why "smoke"
step "natural v3" $PY scripts/natural_rw.py --name v3_lookup --n 150 --versions NM NL --ablate --why "$WN"
WT="$WQ: tool-output set (TBL, TBR: BL and BR as two JSON tool results), a less toy context"
step "tool manifest smoke" $PY scripts/suite_v1.py manifest --set tool --name tool_smoke_1020 --limit 4 --why "smoke"
step "tool competence smoke" $PY scripts/suite_v1.py competence --name tool_smoke_1020
step "tool manifest" $PY scripts/suite_v1.py manifest --set tool --name competence_tool_v1 --why "$WT (competence, all 400 per family)"
step "tool competence" $PY scripts/suite_v1.py competence --name competence_tool_v1
step "tool rw" $PY scripts/read_write.py --name tool_rw_v1 --n 100 --from-competence competence_tool_v1 --families TBL TBR \
  --scales 0.5 1 2 4 8 16 --why "$WT (read and write; countries as positive control)"
step "tool removal" $PY scripts/ablate_pilot.py --name tool_abl_v1 --n 100 --comp-computed none --comp-tool competence_tool_v1 \
  --why "$WT (J-space removal, the v1 setting; BL-RR rerun alongside)"
echo "=== QUEUE DONE failed=$FAILED"
exit $FAILED
