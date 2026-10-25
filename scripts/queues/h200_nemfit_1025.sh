#!/bin/bash
# Zach (2026-10-25, prereg amendment 45): our J++ on Nemotron 3.5 Lightning (Zach: no plain J-lenses anywhere). The
# 9B refit's and Ministral's recipe (safety-research/jpp_lens@93f02cd as patched, scripts/lens_fit/jpp_lens_ministral3.patch
# + NemotronHRMSNorm and NemotronH's layout and no BOS), with the LN rule alone (--lrp-mode ln, as gpt-oss: Nemotron has
# no gated MLPs; its Mamba, attention and MoE layers keep standard gradients, as OLMo-Hybrid's GatedDeltaNet did).
# Router on 64 WikiText prompts, one fit shard of 32 prompts over source layers 0-50 (target the final block), merge,
# grading, readout weights, held-out evaluation, export, sha256 into pins, commit, lens check. The model is loaded from
# its pinned local snapshot (a9904d2) and runs with the HF-hub mamba-ssm kernels (scripts/lens_fit/jpp_cli_hubmamba.py).
# Working directory in /dev/shm (RAM). Usage: h200_nemfit_1025.sh GPU
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$1
PY="uv run --no-sync python"
JP=/workspace/ext/jpp_lens/.venv/bin/python
WRAP="$JP /workspace/bridge-jspace/scripts/lens_fit/jpp_cli_hubmamba.py"
KEY=nemotron-3.5-lightning; PFX=nem35l_; REV=a9904d24bcc1d289a1950fa9d2b978c47cf903b9
STEM=NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
SNAP=/workspace/hf_cache/hub/models--nvidia--NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16/snapshots/$REV
LAYERS=$(seq -s, 0 50)
OUT=/workspace/ext/${KEY}_fit; LOG=/workspace/scratch/${KEY}_jppfit.log
LENS=cache/$KEY/lenses/jpp/${STEM}_jpp_lens.pt
echo "=== start $(date -u +%FT%TZ)"
[ -f "$LENS" ] && { echo "=== $KEY lens exists"; exit 0; }
mkdir -p /dev/shm/${KEY}_fit; [ -e "$OUT" ] || ln -s /dev/shm/${KEY}_fit "$OUT"
M="--hf-model-name $SNAP"; C="$WRAP /workspace/ext/jpp_lens/scripts/jpp_cli.py"
cd /workspace/ext/jpp_lens
echo "=== $KEY router $(date -u +%T)"
[ -f "$OUT/router.pt" ] || { $C fit-router $M --layers "$LAYERS" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 \
  --out "$OUT/router.tmp.pt" > $LOG 2>&1 < /dev/null && mv "$OUT/router.tmp.pt" "$OUT/router.pt" || { echo "=== $KEY router FAILED"; tail -5 $LOG; exit 1; }; }
ok=0
for rows in 32 16; do
  echo "=== $KEY fit-shard (32 prompts), $rows rows per pass $(date -u +%T)"
  $C fit-shard $M --layers "$LAYERS" --router-path "$OUT/router.pt" --shard-idx 0 --num-shards 1 --num-prompts 32 \
    --target-offset -1 --lrp-mode ln --jacobian-rows-per-pass $rows --max-seq-len 128 --skip-first-n-positions 16 \
    --checkpoint-every-n-prompts 32 --artifacts-base-dir "$OUT/artifacts" --checkpoint-name fit32 >> $LOG 2>&1 < /dev/null && { ok=1; break; }
  echo "=== $KEY $rows rows failed ($(tail -40 $LOG | grep -m1 -oiE "out of memory|No space left|[A-Za-z]+Error: [^ ]+ [^ ]+ [^ ]+"))"
  rm -rf "$OUT"/artifacts/*/fit32
done
[ $ok = 1 ] || { echo "=== $KEY fit FAILED"; exit 1; }
echo "=== $KEY merge $(date -u +%T)"
$C merge-experts --checkpoint-dirs $(ls -d "$OUT"/artifacts/*/fit32/shard0of* | tail -1) --out "$OUT/experts.pt" --pooled-lens-out "$OUT/pooled_lens.pt" --device cpu >> $LOG 2>&1 < /dev/null \
  || { echo "=== $KEY merge FAILED"; tail -5 $LOG; exit 1; }
rm -rf "$OUT"/artifacts
$WRAP /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py $SNAP "$LAYERS" "$OUT/model_correctness.csv" >> $LOG 2>&1 < /dev/null || { echo "=== $KEY grade FAILED"; tail -5 $LOG; exit 1; }
$C fit-weights $M --layers "$LAYERS" --experts "$OUT/experts.pt" --items fit:0 --correctness-csv "$OUT/model_correctness.csv" \
  --cache-path "$OUT/readout_cache.pt" --out "$OUT/${STEM}_jpp_lens.pt" >> $LOG 2>&1 < /dev/null || { echo "=== $KEY fit-weights FAILED"; tail -5 $LOG; exit 1; }
echo "=== $KEY evaluate $(date -u +%T)"
$C evaluate $M --layers "$LAYERS" --lens "$OUT/${STEM}_jpp_lens.pt" "$OUT/pooled_lens.pt" logit --items held-out:0 \
  --correctness-csv "$OUT/model_correctness.csv" --out "$OUT/eval_ranks.csv" >> $LOG 2>&1 < /dev/null || echo "=== $KEY evaluate FAILED"
cd /workspace/bridge-jspace
mkdir -p cache/$KEY/lenses/jpp results/lens_fit/$KEY
$PY scripts/lens_fit/export_jpp_lens.py "$OUT/${STEM}_jpp_lens.pt" "$LENS" \
  --note "J++ (LN rule only) on nvidia/$STEM@$REV, safety-research/jpp_lens@93f02cd recipe (as patched), 32 wikitext prompts, layers 0-50" \
  || { echo "=== $KEY export FAILED"; exit 1; }
cp "$OUT"/eval_ranks*.csv "$OUT"/model_correctness.csv results/lens_fit/$KEY/ 2>/dev/null
gate=$(python3 - "$OUT" <<'PY'
import collections, csv, sys
rows = [r for r in csv.DictReader(open(sys.argv[1] + "/eval_ranks_pass_at_k.csv")) if r["k"] == "10" and r["weighting"] == "item"]
by = collections.defaultdict(list)
for r in rows:
    by[r["lens"]].append(float(r["pass_at_k"]))
print("held-out macro pass@10:", {k: round(sum(v) / len(v), 3) for k, v in by.items()})
PY
)
echo "=== $KEY $gate"
sha=$(sha256sum "$LENS" | cut -d" " -f1)
.venv/bin/python - "$LENS" "$sha" "$gate" <<'PY' || { echo "=== $KEY pins FAILED"; exit 1; }
import sys
from pathlib import Path
lens, sha, gate = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
o1 = f'"lenses": {{"jpp": ("local", "{lens}", None)}},'
o2 = '"frozen_lens_sha256": None,  # set when the Lightning fit is done'
assert s.count(o1) == 1 and s.count(o2) == 1, "the Lightning entry's placeholders"
s = s.replace(o1, f'"lenses": {{"jpp": ("local", "{lens}", "{sha}")}},  # our J++, LN rule only (h200_nemfit_1025.sh); {gate}')
s = s.replace(o2, f'"frozen_lens_sha256": "{sha}",')
p.write_text(s)
print("lens registered", sha[:12])
PY
git add results/lens_fit/$KEY && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com commit -q -m "pins: $KEY, our J++ (LN rule only, 32 prompts, layers 0-50, amendment 45); $gate

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- src/bridge_jspace/pins.py results/lens_fit/$KEY || { echo "=== $KEY commit FAILED"; exit 1; }
BJ_TARGET=$KEY $PY scripts/lens_agreement.py --name ${PFX}lens_agreement_v1 --why "Zach (2026-10-25, amendment 45): $KEY, our J++, lens check" \
  > /workspace/scratch/${KEY}_agree.log 2>&1 < /dev/null || echo "=== $KEY lens check FAILED"
rm -f "$OUT/experts.pt" "$OUT/pooled_lens.pt" "$OUT/${STEM}_jpp_lens.pt"
echo "=== $KEY fit done $(date -u +%T)"
