#!/bin/bash
# Zach (2026-10-21, decided with Zach): J++ on Gemma 4 31B-it at every source layer 0-58 (the final block, 59, is the
# fit's target), 64 WikiText prompts: the recipe of our layers 24-45 fit (gemma_it_fit_full.sh), through fit_jpp.sh,
# so Gemma's lens covers what Qwen3.6-27B's published J++ covers (every layer) and the 27B's experiments can run at
# matched relative depth. Replaces gemma_retest_1021.sh (every-3rd-layer lens; cancelled before it ran).
# Steps: wait for tonight's queue and the pooled control run (the fit needs the GPU to itself: 62 GB of weights + ~55
# GB of expert accumulators); check HF main is still the pinned revision (jpp_lens loads by name); a 1-prompt run of
# the whole pipeline (stop if a prompt takes > 300 s: 64 prompts would pass 5 h); the full fit; export to our J format
# (sha256 printed); held-out readout table. The lens becomes its own target (gemma-4-31b-it-full) by hand, after the
# gate fixed now: macro pass@10 on the shared layers 24-45 within 0.05 of the layers 24-45 fit's.
set -euo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -q "^EXIT" $R-resume-1021-0052.log && grep -q "^EXIT" $R-wm2ctrlall-1021-0218.log; do sleep 120; done
until [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 170000 ]; do sleep 60; done
PIN=842da3794eaa0b77d5f08bae87a17459d91ff475
MAIN=$(.venv/bin/python -c 'from huggingface_hub import model_info; print(model_info("google/gemma-4-31B-it").sha)')
[ "$MAIN" = "$PIN" ] || { echo "HF main $MAIN is not the pinned $PIN: stop"; exit 1; }
LAYERS=$(seq -s, 0 58)
SMOKE=/workspace/scratch/gemma_full_smoke OUT=/workspace/ext/gemma_it_fit_full
echo "=== smoke (1 prompt, every layer) $(date -u +%FT%TZ)"
bash scripts/lens_fit/fit_jpp.sh google/gemma-4-31B-it "$LAYERS" "$SMOKE" 1 2>&1 | tee "$SMOKE.log" | grep -E "^===|prompt 1/1|FIT_DONE|Error|error" || true
grep -q FIT_DONE "$SMOKE.log" || { echo "smoke failed"; exit 1; }
SEC=$(grep -oE "prompt 1/1 .* ([0-9]+)s" "$SMOKE.log" | grep -oE "[0-9]+s$" | tr -d s)
echo "=== smoke ok: ${SEC}s per prompt; $(df -h /workspace | tail -1)"
[ "$SEC" -le 300 ] || { echo "a prompt takes ${SEC}s (> 300): stop and ask"; exit 1; }
rm -rf "$SMOKE"
echo "=== full fit (64 prompts) $(date -u +%FT%TZ)"
bash scripts/lens_fit/fit_jpp.sh google/gemma-4-31B-it "$LAYERS" "$OUT" 64
mkdir -p cache/gemma-4-31b-it-full/lenses/jpp results/lens_fit/gemma_it_full
uv run --no-sync python scripts/lens_fit/export_jpp_lens.py "$OUT/gemma-4-31B-it_jpp_lens.pt" \
  cache/gemma-4-31b-it-full/lenses/jpp/gemma-4-31B-it_jpp_lens.pt \
  --note "J++ on google/gemma-4-31B-it@842da37, safety-research/jpp_lens@93f02cd recipe, 64 wikitext prompts, layers 0-58"
cp "$OUT"/eval_ranks*.csv "$OUT"/model_correctness.csv results/lens_fit/gemma_it_full/ 2>/dev/null || true
rm -rf "$OUT"/artifacts  # the shard checkpoint (~50 GB): merged into experts.pt
echo "=== done $(date -u +%FT%TZ); $(df -h /workspace | tail -1)"
