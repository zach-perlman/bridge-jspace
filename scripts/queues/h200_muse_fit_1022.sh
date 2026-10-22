#!/bin/bash
# Zach (2026-10-22): Muse Glimmer 30B gets our own J++ (its lens of record, as every other model's is a J++); its published
# plain J-lens stays as a comparison (target muse-glimmer-30b-jlens). GPU 0. Steps:
# (1) after the Qwen3-32B fit has exported its lens (disk): remove that fit's leftover intermediates (experts.pt,
#     pooled_lens.pt, the fp32 J++, readout_cache.pt; Zach approved; the exported lens and eval CSVs stay) and download
#     Muse's weights (pinned revision);
# (2) the untestable gate with the published J-lens (lens check + plain-text loss at 26-32), cheap, before the fit;
# (3) the J++ fit, Qwen3-32B's recipe (safety-research/jpp_lens@93f02cd + scripts/lens_fit/jpp_lens_muse_1022.patch, run in
#     /workspace/ext/jpp_muse/.venv for transformers 5.17's Muse classes): router on 64 WikiText prompts, one fit shard of
#     32 prompts (rows per pass 32, else 16; one checkpoint at the end: disk), merge, grading, readout weights, held-out
#     evaluation (J++, pooled, logit lens), export, model entry muse-glimmer-30b (prefix muse30_), commit.
# 2026-10-22 ~03:20 UTC: relaunched after the router failed offline (no cached 'main' ref); finished steps skip.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
REV=cec94fcfd6512f2cfe708138c32533b346ea4f69
until grep -qs "^=== Qwen3-32B competence\|^EXIT" $R-h200q32fit-*.log; do sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
rm -f /workspace/ext/qwen3_32b_fit/experts.pt /workspace/ext/qwen3_32b_fit/pooled_lens.pt /workspace/ext/qwen3_32b_fit/Qwen3-32B_jpp_lens.pt /workspace/ext/qwen3_32b_fit/readout_cache.pt
df -h /workspace | tail -1
uv tool run --from huggingface_hub hf download meta-models/Muse-Glimmer-30B --revision $REV > /dev/null 2>&1 || { echo "Muse download failed: stop"; exit 1; }
echo "=== Muse downloaded $(date -u +%T)"; df -h /workspace | tail -1
WHY="Zach (2026-10-22): Muse Glimmer 30B"
echo "=== J-lens gate $(date -u +%T)"
[ -f results/lens_agreement/muse30j_lens_agreement_v1/summary.json ] || BJ_TARGET=muse-glimmer-30b-jlens $PY scripts/lens_agreement.py --name muse30j_lens_agreement_v1 --why "$WHY: the published J-lens, lens check" \
  || { echo "J-lens check failed: stop"; exit 1; }
[ -f results/removal_textloss/muse30j_textloss_top_v1/summary.json ] || BJ_TARGET=muse-glimmer-30b-jlens $PY scripts/removal_textloss.py --name muse30j_textloss_top_v1 \
  --why "$WHY: the published J-lens, plain-text loss under the knock-out at L26-32 (the untestable gate)" \
  --layers $(seq 26 32) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== J-lens text loss FAILED"
OUT=/workspace/ext/muse30_fit LAYERS=$(seq -s, 0 50)
# (no HF_HUB_OFFLINE: the fitter loads the model by name, which needs the hub's 'main' ref; main = cec94fc as pinned)
M="--hf-model-name meta-models/Muse-Glimmer-30B"
MP=/workspace/ext/jpp_muse/.venv/bin/python
mkdir -p "$OUT"
cd /workspace/ext/jpp_lens
C="$MP scripts/jpp_cli.py"
echo "=== router $(date -u +%T)"
[ -f "$OUT/router.pt" ] || { $C fit-router $M --layers "$LAYERS" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 \
  --out "$OUT/router.tmp.pt" > /workspace/scratch/muse_router.log 2>&1 && mv "$OUT/router.tmp.pt" "$OUT/router.pt" || { echo "router failed: stop"; tail -5 /workspace/scratch/muse_router.log; exit 1; }; }
ok=0
for rows in 32 16; do
  echo "=== fit-shard (32 prompts, one shard), $rows rows per pass $(date -u +%T)"
  $C fit-shard $M --layers "$LAYERS" --router-path "$OUT/router.pt" --shard-idx 0 --num-shards 1 --num-prompts 32 \
    --target-offset -1 --lrp-mode rlens --jacobian-rows-per-pass $rows --max-seq-len 128 --skip-first-n-positions 16 \
    --checkpoint-every-n-prompts 32 --artifacts-base-dir "$OUT/artifacts" --checkpoint-name fit32 > /workspace/scratch/muse_shard.log 2>&1 \
    && { ok=1; echo "=== shard done $(date -u +%T)"; break; }
  echo "=== $rows rows failed ($(grep -m1 -oiE "out of memory|No space left|RuntimeError: [^ ]+ [^ ]+ [^ ]+" /workspace/scratch/muse_shard.log))"
  cp /workspace/scratch/muse_shard.log /workspace/scratch/muse_shard_${rows}rows_failed.log
  rm -rf "$OUT"/artifacts/*/fit32
done
[ $ok = 1 ] || { echo "fit failed: stop"; exit 1; }
echo "=== merge $(date -u +%T)"
$C merge-experts --checkpoint-dirs $(ls -d "$OUT"/artifacts/*/fit32/shard0of* | tail -1) --out "$OUT/experts.pt" --pooled-lens-out "$OUT/pooled_lens.pt" \
  > /workspace/scratch/muse_merge.log 2>&1 || { echo "merge failed: stop"; tail -5 /workspace/scratch/muse_merge.log; exit 1; }
rm -rf "$OUT"/artifacts
echo "=== grade $(date -u +%T)"
$MP /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py meta-models/Muse-Glimmer-30B "$LAYERS" "$OUT/model_correctness.csv" >> /workspace/scratch/muse_merge.log 2>&1 || { echo "grade failed: stop"; exit 1; }
echo "=== fit-weights $(date -u +%T)"
$C fit-weights $M --layers "$LAYERS" --experts "$OUT/experts.pt" --items fit:0 --correctness-csv "$OUT/model_correctness.csv" \
  --cache-path "$OUT/readout_cache.pt" --out "$OUT/Muse-Glimmer-30B_jpp_lens.pt" >> /workspace/scratch/muse_merge.log 2>&1 || { echo "fit-weights failed: stop"; exit 1; }
echo "=== evaluate $(date -u +%T)"
$C evaluate $M --layers "$LAYERS" --lens "$OUT/Muse-Glimmer-30B_jpp_lens.pt" "$OUT/pooled_lens.pt" logit --items held-out:0 \
  --correctness-csv "$OUT/model_correctness.csv" --out "$OUT/eval_ranks.csv" >> /workspace/scratch/muse_merge.log 2>&1 || echo "=== evaluate FAILED"
cd /workspace/bridge-jspace
mkdir -p cache/muse-glimmer-30b/lenses/jpp results/lens_fit/muse30
LENS=cache/muse-glimmer-30b/lenses/jpp/Muse-Glimmer-30B_jpp_lens.pt
$PY scripts/lens_fit/export_jpp_lens.py "$OUT/Muse-Glimmer-30B_jpp_lens.pt" "$LENS" \
  --note "J++ on meta-models/Muse-Glimmer-30B@$REV, safety-research/jpp_lens@93f02cd recipe (+ jpp_lens_muse_1022.patch), 32 wikitext prompts, layers 0-50" || { echo "export failed: stop"; exit 1; }
cp "$OUT"/eval_ranks*.csv "$OUT"/model_correctness.csv results/lens_fit/muse30/ 2>/dev/null
GATE=$(python3 - <<'PY'
import collections, csv
rows = [r for r in csv.DictReader(open("/workspace/ext/muse30_fit/eval_ranks_pass_at_k.csv")) if r["k"] == "10" and r["weighting"] == "item"]
by = collections.defaultdict(list)
for r in rows:
    by[r["lens"]].append(float(r["pass_at_k"]))
print("held-out macro pass@10:", {k: round(sum(v) / len(v), 3) for k, v in by.items()})
PY
)
echo "=== $GATE"
SHA=$(sha256sum "$LENS" | cut -d" " -f1)
.venv/bin/python - "$SHA" "$GATE" <<'PY' || { echo "pins failed: stop"; exit 1; }
import sys
from pathlib import Path
sha, gate = sys.argv[1], sys.argv[2]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
anchor = '    "muse-glimmer-30b-jlens": {'
assert s.count(anchor) == 1 and '"muse-glimmer-30b": {' not in s
block = f'''    # Muse Glimmer 30B with our own J++ (Zach, 2026-10-22; its lens of record): the safety-research/jpp_lens@93f02cd recipe
    # (+ scripts/lens_fit/jpp_lens_muse_1022.patch), 32 WikiText prompts, one shard, source layers 0-50, target the final
    # block; scripts/queues/h200_muse_fit_1022.sh. {gate}.
    "muse-glimmer-30b": {{
        "repo": "meta-models/Muse-Glimmer-30B",
        "revision": "cec94fcfd6512f2cfe708138c32533b346ea4f69",
        "n_layers": 52,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "muse30_",
        "chat_template_edits": MUSE_TEMPLATE_EDITS,
        "lenses": {{"jpp": ("local", "cache/muse-glimmer-30b/lenses/jpp/Muse-Glimmer-30B_jpp_lens.pt", "{sha}")}},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("target muse-glimmer-30b registered")
PY
git add src/bridge_jspace/pins.py results/lens_fit/muse30 && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
  commit -q -m "pins: muse-glimmer-30b (our J++, layers 0-50); $GATE

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || { echo "commit failed: stop"; exit 1; }
BJ_TARGET=muse-glimmer-30b $PY scripts/lens_agreement.py --name muse30_lens_agreement_v1 --why "$WHY: our J++, lens check" || echo "=== J++ lens check FAILED"
echo "=== Muse fit done $(date -u +%FT%TZ)"
