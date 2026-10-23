#!/bin/bash
# Zach (2026-10-23, prereg amendment 8): gpt-oss-20b on GPU 1, after the Olmo-Hybrid powered run and gpt-oss's competence.
# (1) our J++ (the "ln" preset; scripts/lens_fit/jpp_lens_gptoss_1023.patch, checked by check_gptoss_lrp.py), 32 WikiText
# prompts, source layers 0-22, target the final block; register "gpt-oss-20b"; lens check. (2) every model's procedure:
# the gate (L10-13), the band on ctrl_v8 (4-layer windows by 2), C1 on olmo_big_v8 (amendment 7's powered set) at the band
# and at 12-15 (the 27B's relative depth), the logit-lens control, keep-own, a control seed, steering (10-15 as the 27B's
# 28-40 scaled, then the aligned band).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export HF_HUB_OFFLINE=0 UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200amend7g1-1023-0116.log && grep -qs "^=== gpt-oss competence done" $R-h200gptosscomp-1023-0230.log; do sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
JP=/workspace/ext/jpp_lens/.venv/bin/python
$JP -I scripts/lens_fit/check_gptoss_lrp.py 2>&1 | tail -1 | grep -q '"ok": true' || { echo "LRP check failed: stop"; exit 1; }
KEY=gpt-oss-20b
HF=openai/gpt-oss-20b
REV=6cee5e81ee83917806bbde320786a8fb61efebee
STEM=gpt-oss-20b
P=gptoss20_
OUT=/workspace/ext/gpt-oss-20b_fit
LAYERS=$(seq -s, 0 22)
LENS=cache/$KEY/lenses/jpp/${STEM}_jpp_lens.pt
LOG=/workspace/scratch/${KEY}_fit.log
if [ ! -f "$LENS" ]; then
  mkdir -p "$OUT"; cd /workspace/ext/jpp_lens
  C="$JP scripts/jpp_cli.py"; M="--hf-model-name $HF"
  echo "=== router $(date -u +%T)"
  [ -f "$OUT/router.pt" ] || { $C fit-router $M --layers "$LAYERS" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 --out "$OUT/router.tmp.pt" > $LOG 2>&1 \
    && mv "$OUT/router.tmp.pt" "$OUT/router.pt" || { echo "router FAILED: stop"; tail -5 $LOG; exit 1; }; }
  ok=0
  for rows in 32 16; do
    echo "=== fit-shard (32 prompts), $rows rows per pass $(date -u +%T)"
    $C fit-shard $M --layers "$LAYERS" --router-path "$OUT/router.pt" --shard-idx 0 --num-shards 1 --num-prompts 32 --target-offset -1 --lrp-mode ln \
      --jacobian-rows-per-pass $rows --max-seq-len 128 --skip-first-n-positions 16 --checkpoint-every-n-prompts 32 --artifacts-base-dir "$OUT/artifacts" \
      --checkpoint-name fit32 >> $LOG 2>&1 && { ok=1; break; }
    echo "=== $rows rows failed ($(grep -m1 -oiE "out of memory|No space left|RuntimeError: [^ ]+ [^ ]+ [^ ]+" $LOG))"
    rm -rf "${OUT:?}"/artifacts/*/fit32
  done
  [ $ok = 1 ] || { echo "fit FAILED: stop"; exit 1; }
  echo "=== merge $(date -u +%T)"
  $C merge-experts --checkpoint-dirs $(ls -d "$OUT"/artifacts/*/fit32/shard0of* | tail -1) --out "$OUT/experts.pt" --pooled-lens-out "$OUT/pooled_lens.pt" --device cpu >> $LOG 2>&1 \
    || { echo "merge FAILED: stop"; tail -5 $LOG; exit 1; }
  rm -rf "${OUT:?}"/artifacts
  $JP /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py $HF "$LAYERS" "$OUT/model_correctness.csv" >> $LOG 2>&1 || { echo "grade FAILED: stop"; exit 1; }
  $C fit-weights $M --layers "$LAYERS" --experts "$OUT/experts.pt" --items fit:0 --correctness-csv "$OUT/model_correctness.csv" --cache-path "$OUT/readout_cache.pt" \
    --out "$OUT/${STEM}_jpp_lens.pt" >> $LOG 2>&1 || { echo "fit-weights FAILED: stop"; exit 1; }
  echo "=== evaluate $(date -u +%T)"
  $C evaluate $M --layers "$LAYERS" --lens "$OUT/${STEM}_jpp_lens.pt" "$OUT/pooled_lens.pt" logit --items held-out:0 --correctness-csv "$OUT/model_correctness.csv" \
    --out "$OUT/eval_ranks.csv" >> $LOG 2>&1 || echo "=== evaluate FAILED"
  cd /workspace/bridge-jspace
  mkdir -p cache/$KEY/lenses/jpp results/lens_fit/$KEY
  $PY scripts/lens_fit/export_jpp_lens.py "$OUT/${STEM}_jpp_lens.pt" "$LENS" \
    --note "J++ on $HF@$REV, safety-research/jpp_lens@93f02cd recipe with the LN rule only (+ jpp_lens_gptoss_1023.patch), 32 wikitext prompts, layers 0-22" \
    || { echo "export FAILED: stop"; exit 1; }
  cp "$OUT"/eval_ranks*.csv "$OUT"/model_correctness.csv results/lens_fit/$KEY/ 2>/dev/null
  GATE=$(python3 - "$OUT" <<'PY'
import collections, csv, sys
rows = [r for r in csv.DictReader(open(sys.argv[1] + "/eval_ranks_pass_at_k.csv")) if r["k"] == "10" and r["weighting"] == "item"]
by = collections.defaultdict(list)
for r in rows:
    by[r["lens"]].append(float(r["pass_at_k"]))
print("held-out macro pass@10:", {k: round(sum(v) / len(v), 3) for k, v in by.items()})
PY
)
  echo "=== $GATE"
  SHA=$(sha256sum "$LENS" | cut -d" " -f1)
  .venv/bin/python - "$LENS" "$SHA" "$GATE" <<'PY' || { echo "pins FAILED: stop"; exit 1; }
import sys
from pathlib import Path
lens, sha, gate = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py"); s = p.read_text()
anchor = '    "gpt-oss-20b-prefit": {'
assert s.count(anchor) == 1 and '"gpt-oss-20b": {' not in s
block = f'''    # gpt-oss-20b with our own J++ (Zach, 2026-10-23, prereg amendment 8): the safety-research/jpp_lens@93f02cd recipe with the
    # LN rule only (+ scripts/lens_fit/jpp_lens_gptoss_1023.patch), 32 WikiText prompts, source layers 0-22, target the final
    # block; scripts/queues/h200_gptoss_1023.sh. {gate}.
    "gpt-oss-20b": {{
        "repo": "openai/gpt-oss-20b",
        "revision": "6cee5e81ee83917806bbde320786a8fb61efebee",
        "n_layers": 24,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "gptoss20_",
        "snapshot_ignore": ["metal/*", "original/*"],
        "chat_template_edits": GPTOSS_TEMPLATE_EDITS,
        "attn": "eager",
        "dequantize_mxfp4": True,
        "lenses": {{"jpp": ("local", "{lens}", "{sha}")}},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("target gpt-oss-20b registered")
PY
  git add src/bridge_jspace/pins.py results/lens_fit/$KEY scripts/lens_fit/jpp_lens_gptoss_1023.patch scripts/lens_fit/check_gptoss_lrp.py && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
    commit -q -m "pins: gpt-oss-20b (our J++, LN rule only, layers 0-22); $GATE

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || echo "=== commit FAILED"
  BJ_TARGET=$KEY $PY scripts/lens_agreement.py --name ${P}lens_agreement_v1 --why "Zach (2026-10-23, amendment 8): gpt-oss-20b, our J++, lens check" > /workspace/scratch/${KEY}_agree.log 2>&1 || echo "=== lens check FAILED"
  rm -f "${OUT:?}/experts.pt" "${OUT:?}/pooled_lens.pt" "${OUT:?}/${STEM:?}_jpp_lens.pt"
  echo "=== fit done $(date -u +%T)"
fi
# (2) the pipeline
export BJ_TARGET=$KEY
WHY="Zach (2026-10-23, prereg amendment 8): gpt-oss-20b (our J++), the non-Qwen generality model"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }
run removal_textloss/${P}textloss_top_v1 $PY scripts/removal_textloss.py --name ${P}textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L10-13 (the gate)" \
  --layers $(seq 10 13) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot
python3 - results/removal_textloss/${P}textloss_top_v1/summary.json <<'PY' && echo "=== gate: testable" || { echo "=== gpt-oss untestable: stop"; exit 0; }
import json, sys
n = json.load(open(sys.argv[1]))["mean_nll"]
d, r = n["top10"] - n["none"], n["top10_rot"] - n["none"]
print(f"=== gate: top-10 +{d:.2f} nats, rotated +{r:.2f}")
sys.exit(1 if (d >= 2 and r <= 0.3) else 0)
PY
CC=${P}ctrl_v8_competence_v1
CB=${P}olmo_big_v8_competence_v1
run ablate_v2/${P}ctrl_sweep_v1 $PY scripts/ablate_v2.py --name ${P}ctrl_sweep_v1 --why "$WHY: depth sweep on ctrl_v8 to choose the middle band (4-layer windows by 2)" \
  --plan bands --bands 0-3 2-5 4-7 6-9 8-11 10-13 12-15 14-17 16-19 18-21 --conditions paper10 paper10_rot \
  --tasks ctrl_v8 --tasks-competence $CC --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32
MID=$($PY scripts/choose_band.py ${P}ctrl_sweep_v1 "") || MID=""
[ -n "$MID" ] || { MID=12-15; echo "=== no band chosen: the relative-depth band 12-15 instead"; }
echo "=== middle band: $MID"
T2="--tasks olmo_big_v8 --tasks-competence $CB --tasks-words PP PM MP MM --tasks-level all"
K="--n 1000 --kinds clean --batch 32"
BANDS=$(echo "$MID 12-15" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " ")
run ablate_v2/${P}smoke_big_ko_1023 $PY scripts/ablate_v2.py --name ${P}smoke_big_ko_1023 --why smoke --plan bands --bands $MID --conditions paper10 paper10_rot $T2 --n 2 --kinds clean --batch 8 \
  || { echo "smoke failed: stop"; exit 1; }
run ablate_v2/${P}big2_ko_v1 $PY scripts/ablate_v2.py --name ${P}big2_ko_v1 --why "$WHY: C1 at the band and at 12-15 on olmo_big_v8" --plan bands --bands $BANDS \
  --conditions paper10 paper10_rot $T2 $K
$PY scripts/c1_v2.py ${P}big2_ko_v1 --middle L$MID --set olmo_big_v8 | tail -2
run ablate_v2/${P}big2_ko_unembed_v1 $PY scripts/ablate_v2.py --name ${P}big2_ko_unembed_v1 --why "$WHY: the logit-lens control" --plan bands --bands $MID \
  --conditions unembed10 unembed10_rot $T2 $K
run ablate_v2/${P}big2_ko_keepown_v1 $PY scripts/ablate_v2.py --name ${P}big2_ko_keepown_v1 --why "$WHY: keep-own" --plan bands --bands $MID \
  --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K && $PY scripts/c1_v2.py ${P}big2_ko_keepown_v1 --middle L$MID --set olmo_big_v8 | tail -3
run ablate_v2/${P}big2_ko_rotseed1_v1 $PY scripts/ablate_v2.py --name ${P}big2_ko_rotseed1_v1 --why "$WHY: control seed 1" --plan bands --bands $MID --conditions paper10_rot --seed-offset 1 $T2 $K
W2="--tasks olmo_big_v8 --tasks-competence $CB --tasks-level all --families PP PM MP MM"
run write_max/${P}smoke_wm2_1023 env BJ_BATCH=16 $PY scripts/write_max.py --name ${P}smoke_wm2_1023 --why smoke --n 2 --band 12-13 --single-step 1 --early 6 \
  --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
run copy_sweep/${P}copy_sweep_big_v1 $PY scripts/copy_sweep.py --name ${P}copy_sweep_big_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks olmo_big_v8 --tasks-competence $CB --families PP PM MP MM --n 40 --step 1 --window 4
run write_max/${P}wm2_big_v1 env BJ_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_big_v1 --why "$WHY: two-step steering at 10-15 (the 27B's 28-40 scaled)" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band 10-15 --single-step 1 --early 4 6 8 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_big_v1 | tail -3
AB=$($PY scripts/choose_steer_band.py ${P}copy_sweep_big_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
[ -n "$AB" ] && run write_max/${P}wm2_big_aligned_v1 env BJ_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_big_aligned_v1 --why "$WHY: steering at the aligned band ${AB%% *}" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB%% *} --single-step 1 --early 4 6 8 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_big_aligned_v1 | tail -3
echo "=== gpt-oss done $(date -u +%FT%TZ)"
