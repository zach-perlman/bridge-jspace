#!/bin/bash
# Prereg amendment 88 note 67 (2026-10-30, "as decided", and its addendum: the 27B primary): a positive control built from data
# for answer-orthogonal removal. Usage: h200_n67_1030.sh MODEL GPU [WAITJOB ...]
#   MODEL: 27b (primary) | 9b | nem35l (confirmatory). Waits for the WAITJOBs (^EXIT) and the model's known stage and gate.
#   sd stage (scripts/nn_sd67_datactl.py ko; the city-identity fit is made inside its first run, ~6 neutral sentences per city
#   of every person-birthcity-cntry item, dev and test, and saved to /workspace/scratch/n67/{P}fit.pt, not in git): test split,
#   onehop (O), solo (P), ctx2hop (I), every edit from the question's first token; per band (early, note 62's mid): cityRaw,
#   cityRaw_RE, cityClean, cityClean_RE, cityClean_RJ, bridgeJperp; --gen (the unedited 12 tokens, the agreement check).
#   An 8-item smoke first (moved to /workspace/scratch/n67), then the full run, then scripts/nn_sd67_read.py, appended to
#   /workspace/scratch/{P}note67.txt; its reading lines go to this log. Run {P}sd67_ko_test_v1.
#   v4 stage (scripts/nn_sd67_datactl.py v4; run only if the sd stage's R1 holds, or with N67_V4=always): note 37's v4 items
#   (jsuite_v4_test_chat, MP and MM, cand2 read, v4 gate), an entity-identity fit of the set's bridges cleaned of the MM answers'
#   class means and the relation's answer span A (/workspace/scratch/n67/{P}fitv4.pt), every edit from the question's first token;
#   per band: entRaw, entRaw_RE, entClean, entClean_RE, entClean_RJ. Smoke (4 items per word), the full run, the reader (--v4,
#   with the sd reader's json), appended to the same note67 file. Run {P}sd67v4_test_v1.
#   Bands (both stages): 27B L16-24 + L32-40; 9B L6-10 + L12-16; Lightning L14-20 + L27-33. Batches N67_KBATCH (sd: 16 each) and
#   N67_VBATCH (v4: 27B 16, 9B 32, Lightning 16). GPU [E, from the 9B smoke and notes 62 / 37's timings]: 27B sd ~15-20 min,
#   v4 ~20-25 min; 9B sd ~8, v4 ~8; Lightning sd ~12, v4 ~8 (plus model loads).
set -u
M=$1; G=$2; shift 2
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_GRAM_PROJ=1
PY="uv run --no-sync python"
case $M in
  9b) export BJ_TARGET=qwen3.5-9b; P=qwen35_9b_; EB=6-10; MB=12-16; KBATCH=16; GBATCH=64; VBATCH=32 ;;
  27b) export BJ_TARGET=qwen3.6-27b; P=; EB=16-24; MB=32-40; KBATCH=16; GBATCH=32; VBATCH=16 ;;
  nem35l) export BJ_TARGET=nemotron-3.5-lightning; P=nem35l_; EB=14-20; MB=27-33; KBATCH=16; GBATCH=32; VBATCH=16 ;;
  *) echo "=== unknown model $M"; exit 2 ;;
esac
KBATCH=${N67_KBATCH:-$KBATCH}; VBATCH=${N67_VBATCH:-$VBATCH}
W="prereg amendment 88 note 67, data-defined positive control (2026-10-30, $BJ_TARGET)"
for J in "$@"; do
  echo "=== waiting for $J $(date -u +%T)"
  until grep -qsE "^EXIT [0-9]+" /workspace/runs/$J.log; do sleep 60; done
done
KN=${P}sd_known_v1; GT=${P}sd_gate_v1
for r in $KN $GT; do
  echo "=== waiting for $r $(date -u +%T)"
  until [ -f results/sd_necessity/$r/summary.json ]; do sleep 60; done
done
[ -f scripts/nn_sd67_datactl.py ] && [ -f scripts/nn_sd67_read.py ] || { echo "=== the note 67 code is missing"; exit 1; }
S=/workspace/scratch/n67
mkdir -p $S
fails=0
go() {  # go RUN ARGS...: skip a run whose summary exists; set a partial one aside; log to scratch
  local r=$1; shift
  echo "=== sd_necessity/$r $(date -u +%T)"
  if [ -f results/sd_necessity/$r/summary.json ]; then echo "=== $r exists"; return 0; fi
  if [ -d results/sd_necessity/$r ]; then mv results/sd_necessity/$r $S/$r.partial.$(date -u +%H%M%S) && echo "=== moved a partial $r to $S"; fi
  "$@" > $S/$r.log 2>&1 < /dev/null || { echo "=== $r FAILED"; tail -3 $S/$r.log; fails=$((fails + 1)); return 1; }
  echo "=== done $r $(date -u +%T)"
}
CONDS="cityRaw,cityRaw_RE,cityClean,cityClean_RE,cityClean_RJ,bridgeJperp"
FIT=$S/${P}fit.pt
ko() {  # ko RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  go $r $PY scripts/nn_sd67_datactl.py ko --name $r --why "$W: $why" --items-run $KN --fit $FIT --split test \
    --edits "$EB:$CONDS" "$MB:$CONDS" --batch $KBATCH --gen --gen-batch $GBATCH "$@"
}
rd() { .venv/bin/python scripts/nn_sd67_read.py $1 --gate $GT > $2 2>&1; }
SO=${P}sd67_ko_testsmoke1030; KO=${P}sd67_ko_test_v1
if [ ! -f results/sd_necessity/$KO/summary.json ]; then
  ko $SO "smoke" --n 8 || { echo "=== smoke FAILED"; exit 1; }
  rd $SO $S/${SO}_read.txt || { echo "=== smoke read FAILED"; tail -5 $S/${SO}_read.txt; exit 1; }
  grep -h "fit ranks\|fit check\|agreement" $S/${SO}_read.txt | cut -c1-400
  rm -rf $S/$SO; mv results/sd_necessity/$SO $S/ 2>/dev/null
  mv results/sd_necessity/nn_sd_read/${SO}_note67.json $S/ 2>/dev/null
  echo "=== smoke ok $(date -u +%T)"
fi
ko $KO "O, P and I (test split, person-birthcity-cntry; edits from the question's first token)" || { echo "=== $KO FAILED"; exit 1; }
# the sd reader's json stays in results/sd_necessity/nn_sd_read (the v4 reader reads R1 from it)
OUT=/workspace/scratch/${P}note67.txt
if rd $KO $S/${KO}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $KO (scripts/nn_sd67_read.py, commit $(git rev-parse --short HEAD))"; cat $S/${KO}_read.txt; echo; } >> $OUT
  grep -h "^reading" $S/${KO}_read.txt | cut -c1-400
else
  echo "=== read FAILED"; tail -5 $S/${KO}_read.txt; fails=$((fails + 1))
fi
echo "=== n67 $M sd stage done, $fails failed $(date -u +%FT%TZ)"
# ---- v4 stage (amendment 88 note 67: read only if R1 holds)
SDJ=results/sd_necessity/nn_sd_read/${KO}_note67.json
r1=$(.venv/bin/python -c "import json,sys; print(len(json.load(open(sys.argv[1]))['readings']['R1']['bands']))" $SDJ 2>/dev/null || echo x)
echo "=== sd stage R1 bands: $r1"
if [ "$r1" = 0 ] || [ "$r1" = x ]; then
  if [ "${N67_V4:-}" != always ]; then echo "=== v4 stage skipped (R1 not met; N67_V4=always runs it)"; echo "=== n67 $M done, $fails failed $(date -u +%FT%TZ)"; [ "$fails" = 0 ]; exit; fi
fi
V4C="entRaw,entRaw_RE,entClean,entClean_RE,entClean_RJ"
SET=jsuite_v4_test_chat
v4() {  # v4 RUN WHY [EXTRA...]
  local r=$1 why=$2; shift 2
  go $r $PY scripts/nn_sd67_datactl.py v4 --name $r --why "$W: $why" --tasks $SET --tasks-competence ${P}${SET}_competence_cand2_v1 \
    --tasks-v4-h1 ${P}jsuite_v4_cv_v1 --n 1000 --fit $S/${P}fitv4.pt --edits "$EB:$V4C" "$MB:$V4C" --batch $VBATCH "$@"
}
rd4() { .venv/bin/python scripts/nn_sd67_read.py $1 --v4 --sd-json $SDJ > $2 2>&1; }
S4=${P}sd67v4_testsmoke1030; K4=${P}sd67v4_test_v1
if [ ! -f results/sd_necessity/$K4/summary.json ]; then
  v4 $S4 "v4 smoke" --n-smoke 4 || { echo "=== v4 smoke FAILED"; exit 1; }
  rd4 $S4 $S/${S4}_read.txt || { echo "=== v4 smoke read FAILED"; tail -5 $S/${S4}_read.txt; exit 1; }
  rm -rf $S/$S4; mv results/sd_necessity/$S4 $S/ 2>/dev/null
  mv results/sd_necessity/nn_sd_read/${S4}_note67v4.json $S/ 2>/dev/null
  echo "=== v4 smoke ok $(date -u +%T)"
fi
v4 $K4 "v4 stage (MP, MM; edits from the question's first token)" || { echo "=== $K4 FAILED"; exit 1; }
if rd4 $K4 $S/${K4}_read.txt; then
  { echo "##### $(date -u +%FT%TZ) $K4 (scripts/nn_sd67_read.py --v4, commit $(git rev-parse --short HEAD))"; cat $S/${K4}_read.txt; echo; } >> $OUT
  grep -h "^reading" $S/${K4}_read.txt | cut -c1-400
else
  echo "=== v4 read FAILED"; tail -5 $S/${K4}_read.txt; fails=$((fails + 1))
fi
echo "=== n67 $M done, $fails failed $(date -u +%FT%TZ)"
[ "$fails" = 0 ]
