#!/bin/bash
# Zach (2026-10-21): the Gemma 4 31B-it every-layer J++ fit on GPU 1 of the 2x H200 NVL box, after its gate (the B200
# went down before its fit ran). gemma_fit_1021.sh's recipe and gate: layers 0-58, 64 WikiText prompts, 32 rows per
# pass where it fits else 16 (a 141 GB H200 may need 16), export, gate (held-out macro pass@10 on layers 24-45 >=
# 0.5284 - 0.05), register gemma-4-31b-it-full, commit.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=1 UV_CACHE_DIR=/workspace/uv-cache
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200gate-*.log; do sleep 60; done
grep -qs "GATE PASSED" $R-h200gate-*.log || { echo "the box's gate did not pass: stop"; exit 1; }
echo "=== start $(date -u +%FT%TZ)"
PIN=842da3794eaa0b77d5f08bae87a17459d91ff475
MAIN=$(.venv/bin/python -c 'from huggingface_hub import model_info; print(model_info("google/gemma-4-31B-it").sha)')
[ "$MAIN" = "$PIN" ] || { echo "HF main $MAIN is not the pinned $PIN: stop"; exit 1; }
LAYERS=$(seq -s, 0 58)
SMOKE=/workspace/scratch/gemma_full_smoke OUT=/workspace/ext/gemma_it_fit_full
echo "=== fit smoke (1 prompt, every layer) $(date -u +%FT%TZ)"
export JPP_ROWS=32  # 2026-10-21 (Zach): 32 rows per pass where it fits; the 1-prompt run decides, 16 as the fallback
JPP_ROWS=32 bash scripts/lens_fit/fit_jpp.sh google/gemma-4-31B-it "$LAYERS" "$SMOKE" 1 > "$SMOKE.log" 2>&1
if ! grep -q FIT_DONE "$SMOKE.log"; then
  echo "=== 32 rows per pass failed ($(grep -m1 -oiE "out of memory|error[^ ]*" "$SMOKE.log")); retrying with 16"
  rm -rf "$SMOKE"; export JPP_ROWS=16
  bash scripts/lens_fit/fit_jpp.sh google/gemma-4-31B-it "$LAYERS" "$SMOKE" 1 > "$SMOKE.log" 2>&1
fi
echo "=== rows per pass: $JPP_ROWS"
grep -q FIT_DONE "$SMOKE.log" || { echo "fit smoke failed:"; tail -20 "$SMOKE.log"; exit 1; }
SEC=$(grep -oE "prompt 1/1 .* [0-9]+s" "$SMOKE.log" | grep -oE "[0-9]+s$" | tr -d s)
echo "=== fit smoke ok: ${SEC:-?}s per prompt; $(df -h /workspace | tail -1)"
[ -n "$SEC" ] && [ "$SEC" -le 300 ] || { echo "a prompt takes ${SEC:-?}s (> 300 or unknown): stop and ask"; exit 1; }
rm -rf "$SMOKE"
echo "=== fit (64 prompts) $(date -u +%FT%TZ)"
bash scripts/lens_fit/fit_jpp.sh google/gemma-4-31B-it "$LAYERS" "$OUT" 64 || { echo "fit failed"; exit 1; }
LENS=cache/gemma-4-31b-it-full/lenses/jpp/gemma-4-31B-it_jpp_lens.pt
mkdir -p "$(dirname $LENS)" results/lens_fit/gemma_it_full
$PY scripts/lens_fit/export_jpp_lens.py "$OUT/gemma-4-31B-it_jpp_lens.pt" "$LENS" \
  --note "J++ on google/gemma-4-31B-it@842da37, safety-research/jpp_lens@93f02cd recipe, 64 wikitext prompts, layers 0-58" || exit 1
SHA=$(sha256sum "$LENS" | cut -d" " -f1)
cp "$OUT"/eval_ranks*.csv "$OUT"/model_correctness.csv results/lens_fit/gemma_it_full/
rm -rf "$OUT"/artifacts  # the shard checkpoint: merged into experts.pt
echo "=== gate $(date -u +%FT%TZ); lens sha256 $SHA"
( cd /workspace/ext/jpp_lens && uv run --no-sync python scripts/jpp_cli.py evaluate --hf-model-name google/gemma-4-31B-it \
    --layers 24,27,30,33,36,39,42,45 --lens "$OUT/gemma-4-31B-it_jpp_lens.pt" --items held-out:0 \
    --correctness-csv "$OUT/model_correctness.csv" --out "$OUT/eval_ranks_shared.csv" ) > /workspace/scratch/gemma_gate_eval.log 2>&1
cp "$OUT"/eval_ranks_shared*.csv results/lens_fit/gemma_it_full/ 2>/dev/null
GATE=$(.venv/bin/python - "$OUT" <<'PY'
import csv, glob, statistics, sys
out = sys.argv[1]
def macro(path):
    rows = [r for r in csv.DictReader(open(path)) if r["k"] == "10" and r["weighting"] == "item" and r["lens"] == "gemma-4-31B-it_jpp_lens"]
    return statistics.mean(float(r["pass_at_k"]) for r in rows) if rows else None
shared = glob.glob(f"{out}/eval_ranks_shared*pass_at_k.csv")
m, which = (macro(shared[0]), "layers 24-45") if shared else (None, None)
if m is None:
    m, which = macro(f"{out}/eval_ranks_pass_at_k.csv"), "ALL layers (the layer-subset evaluation failed)"
print(f"{m:.4f} {'PASS' if m >= 0.5284 - 0.05 else 'FAIL'} {which}")
PY
)
echo "=== gate: macro pass@10 $GATE (old fit 0.5284, threshold 0.4784)"
echo "$GATE" | grep -q PASS || { echo "gate failed: stop"; exit 1; }
.venv/bin/python - "$SHA" "$GATE" <<'PY' || exit 1
import sys
from pathlib import Path
sha, gate = sys.argv[1], sys.argv[2]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
anchor = "    # Qwen3.5-122B-A10B (MoE, 10B active)"
assert anchor in s and '"gemma-4-31b-it-full"' not in s
block = f'''    # Gemma 4 31B-it with a J++ we fit on it at every source layer 0-58 (Zach asked, 2026-10-21: match Qwen3.6-27B's
    # every-layer published lens; the 24-45 every-3rd fit above stays for its runs): the same recipe (64 wikitext texts x
    # 128 tokens, skip 16, target = the final block, LRP rlens, 8 experts, readout weights on fit:0 items graded on this
    # model), scripts/queues/gemma_full_1021.sh. Gate: held-out macro pass@10 {gate}.
    "gemma-4-31b-it-full": {{
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "gemma4itf_",
        "lenses": {{
            "jpp": ("local", "cache/gemma-4-31b-it-full/lenses/jpp/gemma-4-31B-it_jpp_lens.pt", "{sha}"),
        }},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("target gemma-4-31b-it-full registered")
PY
git add src/bridge_jspace/pins.py results/lens_fit/gemma_it_full && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
  commit -q -m "pins: gemma-4-31b-it-full (J++ at every layer 0-58), gate $GATE

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 1
echo "=== registered $(git log --oneline -1)"
echo "=== gemma fit done $(date -u +%FT%TZ)"
