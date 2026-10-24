#!/bin/bash
# Zach (2026-10-24, prereg amendment 27): our own J++ on Qwen3.5-9B-Base and on Qwen3.5-9B (instruct) with one recipe
# (safety-research/jpp_lens@93f02cd as patched in /workspace/ext/jpp_lens, Qwen3.5 natively supported): router on 64
# WikiText prompts, one fit shard of 32 prompts over every source layer 0-30 (target the final block), merge on the CPU,
# grading, readout weights, held-out evaluation, export, model entry, commit, lens check. Base vs instruct on matched
# lenses. Usage: h200_q9fit_1024.sh GPU
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$1
PY="uv run --no-sync python"
JP=/workspace/ext/jpp_lens/.venv/bin/python
LAYERS=$(seq -s, 0 30)
echo "=== start $(date -u +%FT%TZ)"
fit() {  # fit KEY HF_NAME REVISION STEM PREFIX
  local key=$1 hf=$2 rev=$3 stem=$4 pfx=$5 out=/workspace/ext/${1}_fit
  local M="--hf-model-name $hf" C="$JP scripts/jpp_cli.py" log=/workspace/scratch/${1}_fit.log
  local lens=cache/$key/lenses/jpp/${stem}_jpp_lens.pt
  if [ -f "$lens" ]; then echo "=== $key lens exists"; return 0; fi
  mkdir -p "$out"; cd /workspace/ext/jpp_lens
  echo "=== $key router $(date -u +%T)"
  [ -f "$out/router.pt" ] || { $C fit-router $M --layers "$LAYERS" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 \
    --out "$out/router.tmp.pt" > $log 2>&1 && mv "$out/router.tmp.pt" "$out/router.pt" || { echo "=== $key router FAILED"; tail -5 $log; cd /workspace/bridge-jspace; return 1; }; }
  local ok=0 rows
  for rows in 32 16; do
    echo "=== $key fit-shard (32 prompts), $rows rows per pass $(date -u +%T)"
    $C fit-shard $M --layers "$LAYERS" --router-path "$out/router.pt" --shard-idx 0 --num-shards 1 --num-prompts 32 \
      --target-offset -1 --lrp-mode rlens --jacobian-rows-per-pass $rows --max-seq-len 128 --skip-first-n-positions 16 \
      --checkpoint-every-n-prompts 32 --artifacts-base-dir "$out/artifacts" --checkpoint-name fit32 >> $log 2>&1 && { ok=1; break; }
    echo "=== $key $rows rows failed ($(grep -m1 -oiE "out of memory|No space left|RuntimeError: [^ ]+ [^ ]+ [^ ]+" $log))"
    rm -rf "$out"/artifacts/*/fit32
  done
  [ $ok = 1 ] || { echo "=== $key fit FAILED"; cd /workspace/bridge-jspace; return 1; }
  echo "=== $key merge $(date -u +%T)"
  $C merge-experts --checkpoint-dirs $(ls -d "$out"/artifacts/*/fit32/shard0of* | tail -1) --out "$out/experts.pt" --pooled-lens-out "$out/pooled_lens.pt" --device cpu >> $log 2>&1 \
    || { echo "=== $key merge FAILED"; tail -5 $log; cd /workspace/bridge-jspace; return 1; }
  rm -rf "$out"/artifacts
  $JP /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py $hf "$LAYERS" "$out/model_correctness.csv" >> $log 2>&1 || { echo "=== $key grade FAILED"; cd /workspace/bridge-jspace; return 1; }
  $C fit-weights $M --layers "$LAYERS" --experts "$out/experts.pt" --items fit:0 --correctness-csv "$out/model_correctness.csv" \
    --cache-path "$out/readout_cache.pt" --out "$out/${stem}_jpp_lens.pt" >> $log 2>&1 || { echo "=== $key fit-weights FAILED"; cd /workspace/bridge-jspace; return 1; }
  echo "=== $key evaluate $(date -u +%T)"
  $C evaluate $M --layers "$LAYERS" --lens "$out/${stem}_jpp_lens.pt" "$out/pooled_lens.pt" logit --items held-out:0 \
    --correctness-csv "$out/model_correctness.csv" --out "$out/eval_ranks.csv" >> $log 2>&1 || echo "=== $key evaluate FAILED"
  cd /workspace/bridge-jspace
  mkdir -p cache/$key/lenses/jpp results/lens_fit/$key
  $PY scripts/lens_fit/export_jpp_lens.py "$out/${stem}_jpp_lens.pt" "$lens" \
    --note "J++ on $hf@$rev, safety-research/jpp_lens@93f02cd recipe (as patched), 32 wikitext prompts, layers 0-30" \
    || { echo "=== $key export FAILED"; return 1; }
  cp "$out"/eval_ranks*.csv "$out"/model_correctness.csv results/lens_fit/$key/ 2>/dev/null
  local gate sha
  gate=$(python3 - "$out" <<'PY'
import collections, csv, sys
rows = [r for r in csv.DictReader(open(sys.argv[1] + "/eval_ranks_pass_at_k.csv")) if r["k"] == "10" and r["weighting"] == "item"]
by = collections.defaultdict(list)
for r in rows:
    by[r["lens"]].append(float(r["pass_at_k"]))
print("held-out macro pass@10:", {k: round(sum(v) / len(v), 3) for k, v in by.items()})
PY
)
  echo "=== $key $gate"
  sha=$(sha256sum "$lens" | cut -d" " -f1)
  .venv/bin/python - "$key" "$hf" "$rev" "$pfx" "$lens" "$sha" "$gate" <<'PY' || { echo "=== $key pins FAILED"; return 1; }
import sys
from pathlib import Path
key, hf, rev, pfx, lens, sha, gate = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
anchor = '    "qwen3-32b-jlens": {'
assert s.count(anchor) == 1 and f'"{key}": {{' not in s
arch = "Qwen3.5 hybrid: Gated DeltaNet linear attention and full attention, " + ("base, pre-trained only" if "Base" in hf else "instruct")
block = f'''    # {hf} ({arch}; base vs instruct on matched lenses, prereg amendment 27; Zach, 2026-10-24): our own J++, the
    # safety-research/jpp_lens@93f02cd recipe (as patched in /workspace/ext/jpp_lens), 32 WikiText prompts, one shard,
    # source layers 0-30, target the final block; scripts/queues/h200_q9fit_1024.sh. {gate}.
    "{key}": {{
        "repo": "{hf}",
        "revision": "{rev}",
        "n_layers": 32,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "{pfx}",
        "lenses": {{"jpp": ("local", "{lens}", "{sha}")}},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("target", key, "registered")
PY
  git add src/bridge_jspace/pins.py results/lens_fit/$key && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
    commit -q -m "pins: $key (our J++, layers 0-30, amendment 27); $gate

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || { echo "=== $key commit FAILED"; return 1; }
  BJ_TARGET=$key $PY scripts/lens_agreement.py --name ${pfx}lens_agreement_v1 --why "Zach (2026-10-24, amendment 27): $key, our J++, lens check" > /workspace/scratch/${key}_agree.log 2>&1 \
    || echo "=== $key lens check FAILED"
  rm -f "$out/experts.pt" "$out/pooled_lens.pt" "$out/${stem}_jpp_lens.pt"
  echo "=== $key fit done $(date -u +%T)"
}
fit qwen3.5-9b-base Qwen/Qwen3.5-9B-Base 68c46c4b3498877f3ef123c856ecfde50c39f404 Qwen3.5-9B-Base qwen35_9bb_
fit qwen3.5-9b-ourjpp Qwen/Qwen3.5-9B c202236235762e1c871ad0ccb60c8ee5ba337b9a Qwen3.5-9B qwen35_9boj_
echo "=== 9B fits done $(date -u +%FT%TZ)"
