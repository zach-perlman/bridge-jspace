#!/bin/bash
# Zach (2026-10-25, prereg amendment 39): our own J++ on Ministral 3 14B Instruct (BF16 repo) with the 9B refit's recipe
# (scripts/queues/h200_q9fit_1024.sh: safety-research/jpp_lens@93f02cd as patched in /workspace/ext/jpp_lens, here also
# Ministral3MLP / Ministral3RMSNorm registered and Mistral tokenizers loaded with fix_mistral_regex,
# scripts/lens_fit/jpp_lens_ministral3.patch): router on 64 WikiText prompts, one fit shard of 32 prompts over every
# source layer 0-38 (target the final block), merge on the CPU, grading, readout weights, held-out evaluation, export,
# the lens's sha256 into the existing pins entry, commit, lens check. Usage: h200_minfit_1025.sh GPU
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$1
PY="uv run --no-sync python"
JP=/workspace/ext/jpp_lens/.venv/bin/python
LAYERS=$(seq -s, 0 38)
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
    --note "J++ on $hf@$rev, safety-research/jpp_lens@93f02cd recipe (as patched), 32 wikitext prompts, layers 0-38" \
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
  .venv/bin/python - "$key" "$lens" "$sha" "$gate" <<'PY' || { echo "=== $key pins FAILED"; return 1; }
import sys
from pathlib import Path
key, lens, sha, gate = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
o1 = f'"lenses": {{"jpp": ("local", "{lens}", None)}},'
o2 = '"frozen_lens_sha256": None,  # set when the fit is done'
assert s.count(o1) == 1 and s.count(o2) == 1, "the ministral entry's placeholders"
s = s.replace(o1, f'"lenses": {{"jpp": ("local", "{lens}", "{sha}")}},  # our J++ (h200_minfit_1025.sh); {gate}')
s = s.replace(o2, f'"frozen_lens_sha256": "{sha}",')
p.write_text(s)
print("target", key, "lens registered", sha[:12])
PY
  git add src/bridge_jspace/pins.py results/lens_fit/$key && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
    commit -q -m "pins: $key, our J++ (layers 0-38, amendment 39); $gate

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || { echo "=== $key commit FAILED"; return 1; }
  BJ_TARGET=$key $PY scripts/lens_agreement.py --name ${pfx}lens_agreement_v1 --why "Zach (2026-10-25, amendment 39): $key, our J++, lens check" > /workspace/scratch/${key}_agree.log 2>&1 \
    || echo "=== $key lens check FAILED"
  rm -f "$out/experts.pt" "$out/pooled_lens.pt" "$out/${stem}_jpp_lens.pt"
  echo "=== $key fit done $(date -u +%T)"
}
fit ministral-3-14b mistralai/Ministral-3-14B-Instruct-2512-BF16 3cea74c1ebaf5ce5f5a2553de470e2ceab825142 Ministral-3-14B-Instruct-2512-BF16 min14_
echo "=== Ministral fit done $(date -u +%FT%TZ)"
