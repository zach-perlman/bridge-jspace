#!/bin/bash
# Zach (2026-10-21, the rebalance; replaces h200_q32_shard_1021.sh 0, h200_q32_shard1_gpu0_1021.sh and
# h200_q32_merge_1021.sh before they started): the Qwen3-32B fit on GPU 1 right after the 9B knock-outs (h200_q9_B4 fill),
# instead of on GPU 0 behind Gemma's steering, so GPU 1 does not idle. The same recipe and statistics: 1-prompt smoke,
# router, fit-shard 0 then 1 of 2 (16 prompts each; merge-experts sums them), merge, grading, fit-weights, held-out
# evaluation, export, model entry qwen3-32b (sha256 + held-out readout), commit, competence on full_v8; then the
# competence runs that were in its steering queue (full_v8b; suite_v1 main, first 150 per family), and the marker.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export CUDA_VISIBLE_DEVICES=1 UV_CACHE_DIR=/workspace/uv-cache
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
OUT=/workspace/ext/qwen3_32b_fit M="--hf-model-name Qwen/Qwen3-32B" LAYERS=$(seq -s, 0 62)
MK=/workspace/scratch/markers/q32_competence_done
until grep -qs "^EXIT" $R-h200q9F-*.log; do sleep 60; done
echo "=== GPU 1 free for the Qwen3-32B fit $(date -u +%FT%TZ)"
mkdir -p "$OUT"
cd /workspace/ext/jpp_lens
C="uv run --no-sync python scripts/jpp_cli.py"
if [ ! -f "$OUT/router.pt" ]; then
SMOKE=/workspace/scratch/q32_fit_smoke
bash /workspace/bridge-jspace/scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B 30,31 "$SMOKE" 1 > /workspace/scratch/q32_smoke.log 2>&1 \
  && rm -rf "$SMOKE" || { echo "32B fit smoke failed"; tail -20 /workspace/scratch/q32_smoke.log; exit 1; }
echo "=== router $(date -u +%T)"
$C fit-router $M --layers "$LAYERS" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 --out "$OUT/router.tmp.pt" \
  > /workspace/scratch/q32_router.log 2>&1 && mv "$OUT/router.tmp.pt" "$OUT/router.pt" || { echo "router failed"; exit 1; }
fi
for K in 0 1; do
  [ -f "$OUT/shard$K.done" ] && { echo "=== shard $K done already"; continue; }
  ok=0
  for rows in 32 16; do
    echo "=== fit-shard $K of 2, $rows rows per pass $(date -u +%T)"
    $C fit-shard $M --layers "$LAYERS" --router-path "$OUT/router.pt" --shard-idx $K --num-shards 2 --num-prompts 32 \
      --target-offset -1 --lrp-mode rlens --jacobian-rows-per-pass $rows --max-seq-len 128 --skip-first-n-positions 16 \
      --checkpoint-every-n-prompts 8 --artifacts-base-dir "$OUT/artifacts" --checkpoint-name fit32 > /workspace/scratch/q32_shard$K.log 2>&1 \
      && { touch "$OUT/shard$K.done"; echo "=== shard $K done $(date -u +%T)"; ok=1; break; }
    echo "=== $rows rows failed ($(grep -m1 -oiE "out of memory" /workspace/scratch/q32_shard$K.log))"
    rm -rf "$OUT"/artifacts/*/fit32/shard${K}of2
  done
  [ $ok = 1 ] || { echo "shard $K failed: stop"; exit 1; }
done
cd /workspace/bridge-jspace
echo "=== merge $(date -u +%FT%TZ)"
cd /workspace/ext/jpp_lens
C="uv run --no-sync python scripts/jpp_cli.py"
$C merge-experts --checkpoint-dirs $(ls -d "$OUT"/artifacts/*/fit32/shard0of2 | tail -1) $(ls -d "$OUT"/artifacts/*/fit32/shard1of2 | tail -1) \
  --out "$OUT/experts.pt" --pooled-lens-out "$OUT/pooled_lens.pt" > /workspace/scratch/q32_merge.log 2>&1 || { echo "merge failed"; exit 1; }
uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py Qwen/Qwen3-32B "$LAYERS" "$OUT/model_correctness.csv" >> /workspace/scratch/q32_merge.log 2>&1 || exit 1
$C fit-weights $M --layers "$LAYERS" --experts "$OUT/experts.pt" --items fit:0 --correctness-csv "$OUT/model_correctness.csv" \
  --cache-path "$OUT/readout_cache.pt" --out "$OUT/Qwen3-32B_jpp_lens.pt" >> /workspace/scratch/q32_merge.log 2>&1 || exit 1
$C evaluate $M --layers "$LAYERS" --lens "$OUT/Qwen3-32B_jpp_lens.pt" "$OUT/pooled_lens.pt" --items held-out:0 \
  --correctness-csv "$OUT/model_correctness.csv" --out "$OUT/eval_ranks.csv" >> /workspace/scratch/q32_merge.log 2>&1 || exit 1
cd /workspace/bridge-jspace
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
    # 2x H200 box, scripts/queues/h200_q32_shard_1021.sh + h200_q32_merge_1021.sh (2 shards)); held-out readout {gate}.
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
C3=qwen3_32b_full_v8b_competence_v1
CS=qwen3_32b_competence_v1
WHY="Zach (2026-10-21): Qwen3-32B, every-layer J++ (32 prompts)"
[ -f results/tasks_v2/$C3/summary.json ] || { BJ_TARGET=qwen3-32b $PY scripts/tasks_v2.py competence --set full_v8b --name $C3 --guess \
  --why "$WHY: competence on full_v8b (three-step words), as the 27B and Gemma" > /workspace/scratch/q32_comp3.log 2>&1 \
  && BJ_TARGET=qwen3-32b $PY scripts/competence_full_report.py $C3 | tail -16 || echo "=== full_v8b competence FAILED"; }
[ -f results/suite_v1/$CS/summary.json ] || { BJ_TARGET=qwen3-32b $PY scripts/suite_v1.py manifest --set main --name $CS --limit 150 \
  --why "$WHY: suite competence (first 150 per family) for the steering positive control, as Gemma's" \
  && BJ_TARGET=qwen3-32b $PY scripts/suite_v1.py competence --name $CS > /workspace/scratch/q32_suitecomp.log 2>&1 || echo "=== suite competence FAILED"; }
touch $MK
echo "=== Qwen3-32B fit and competence done $(date -u +%FT%TZ)"
