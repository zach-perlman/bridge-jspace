#!/bin/bash
# Zach (2026-10-21): Qwen3-32B on GPU 1 of the 2x H200 box, after the Gemma knock-outs (the 27B reruns and Gemma first,
# decided with Zach): 1-prompt fit smoke, the every-layer J++ fit (layers 0-62, 32 prompts, 32 rows per pass where it
# fits, else 16), export, model entry qwen3-32b (sha256 + held-out readout), competence on full_v8 and its report.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=1 UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200gemmaB2-*.log; do sleep 120; done  # after the Gemma knock-outs (GPU 1)
echo "=== start $(date -u +%FT%TZ)"
echo "=== Qwen3-32B fit smoke $(date -u +%FT%TZ)"
SMOKE=/workspace/scratch/q32_fit_smoke OUT=/workspace/ext/qwen3_32b_fit
bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 > /workspace/scratch/q32_smoke.log 2>&1 \
  && $PY scripts/lens_fit/export_jpp_lens.py "$SMOKE/Qwen3-32B_jpp_lens.pt" "$SMOKE/export_check.pt" --note smoke > /dev/null \
  && rm -rf "$SMOKE" || { echo "32B fit smoke failed"; tail -20 /workspace/scratch/q32_smoke.log; exit 1; }
echo "=== Qwen3-32B fit $(date -u +%FT%TZ)"
JPP_ROWS=32 bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B "$(seq -s, 0 62)" "$OUT" 32 > /workspace/scratch/q32_fit.log 2>&1 \
  || { echo "=== 32 rows per pass failed ($(grep -m1 -oiE "out of memory" /workspace/scratch/q32_fit.log)); refitting with 16"; rm -rf "$OUT"; \
       JPP_ROWS=16 bash scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B "$(seq -s, 0 62)" "$OUT" 32 > /workspace/scratch/q32_fit.log 2>&1; } \
  || { echo "32B fit failed"; tail -20 /workspace/scratch/q32_fit.log; exit 1; }
mkdir -p cache/qwen3-32b/lenses/jpp results/lens_fit/qwen3_32b
LENS=cache/qwen3-32b/lenses/jpp/Qwen3-32B_jpp_lens.pt
$PY scripts/lens_fit/export_jpp_lens.py "$OUT/Qwen3-32B_jpp_lens.pt" "$LENS" \
  --note "J++ on Qwen/Qwen3-32B@9216db5, safety-research/jpp_lens@93f02cd recipe, 32 wikitext prompts, layers 0-62" || exit 1
cp "$OUT"/eval_ranks*.csv "$OUT"/model_correctness.csv results/lens_fit/qwen3_32b/ 2>/dev/null
rm -rf "$OUT"/artifacts
GATE=$($PY - <<'PY'
import collections, csv
rows = [r for r in csv.DictReader(open("/workspace/ext/qwen3_32b_fit/eval_ranks_pass_at_k.csv")) if r["k"] == "10" and r["weighting"] == "item"]
by = collections.defaultdict(list)
for r in rows:
    by[r["lens"]].append(float(r["pass_at_k"]))
print("macro recall@10:", {k: round(sum(v) / len(v), 3) for k, v in by.items()}, "(gate: J++ >= 0.45)")
PY
)
echo "=== $GATE"
SHA=$(sha256sum "$LENS" | cut -d" " -f1)
.venv/bin/python - "$SHA" "$GATE" <<'PY' || exit 1
import sys
from pathlib import Path
sha, gate = sys.argv[1], sys.argv[2]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
anchor = "    # Qwen3.5-122B-A10B (MoE, 10B active)"
assert anchor in s and '"qwen3-32b"' not in s
block = f'''    # Qwen3-32B (dense, full attention in every layer: separates architecture from family; Zach, 2026-10-20/21): a J++ we
    # fit on it at every source layer 0-62 (32 wikitext prompts, the safety-research/jpp_lens@93f02cd recipe, on the
    # 2x H200 box, scripts/queues/h200_q32_1021.sh); held-out readout {gate}.
    "qwen3-32b": {{
        "repo": "Qwen/Qwen3-32B",
        "revision": "9216db5781bf21249d130ec9da846c4624c16137",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "qwen3_32b_",
        "lenses": {{
            "jpp": ("local", "cache/qwen3-32b/lenses/jpp/Qwen3-32B_jpp_lens.pt", "{sha}"),
        }},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("target qwen3-32b registered")
PY
git add src/bridge_jspace/pins.py results/lens_fit/qwen3_32b && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
  commit -q -m "pins: qwen3-32b (J++ at every layer 0-62); $GATE

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 1
echo "=== Qwen3-32B competence $(date -u +%FT%TZ)"
BJ_TARGET=qwen3-32b $PY scripts/tasks_v2.py competence --set full_v8 --name qwen3_32b_full_v8_competence_v1 --guess \
  --why "Zach (2026-10-21): Qwen3-32B competence on the full v8 set, right after its fit" > /workspace/scratch/q32_comp.log 2>&1 \
  && $PY scripts/competence_full_report.py qwen3_32b_full_v8_competence_v1 | tail -16 || echo "=== 32B competence FAILED"
echo "=== Qwen3-32B done $(date -u +%FT%TZ)"
