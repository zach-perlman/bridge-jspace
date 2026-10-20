#!/usr/bin/env bash
# Qwen/Qwen3-32B J++ fit and export (Zach, 2026-10-20; decided the same day: 32 WikiText prompts, every layer in the
# middle of the model, 16-51 = 25-80% depth of 64, in one pass). fit_jpp.sh runs the official recipe (router, fit,
# merge, grade, fit-weights, held-out evaluate); export writes the J file our JLens loads and prints its sha256 for the
# pins target. Expected ~1-1.5 GPU-h (Gemma's 64-prompt fit of 8 layers took 77 min; the Jacobian passes scale with
# prompts, not layers). Needs the GPU to itself (64 GB of weights + the 36 layers' expert accumulators, ~29 GB) and
# ~55 GB of disk (scaled from Gemma's 8-layer fit: checkpoint 7 GB, experts 4 GB, lens and pooled lens 0.9 GB each).
set -euo pipefail
OUT=/workspace/ext/qwen3_32b_fit
bash /workspace/bridge-jspace/scripts/lens_fit/fit_jpp.sh Qwen/Qwen3-32B "$(seq -s, 16 51)" "$OUT" 32
cd /workspace/bridge-jspace
mkdir -p cache/qwen3-32b/lenses/jpp
uv run --no-sync python scripts/lens_fit/export_jpp_lens.py "$OUT/Qwen3-32B_jpp_lens.pt" \
  cache/qwen3-32b/lenses/jpp/Qwen3-32B_jpp_lens.pt \
  --note "J++ on Qwen/Qwen3-32B@9216db5, safety-research/jpp_lens@93f02cd recipe, 32 wikitext prompts, layers 16-51"
uv run --no-sync python - <<'PY'
import pandas as pd
df = pd.read_csv("/workspace/ext/qwen3_32b_fit/eval_ranks_pass_at_k.csv")
df = df[(df.k == 10) & (df.weighting == "item")]
print(df.pivot(index="eval", columns="lens", values="pass_at_k").round(3).to_string())
print("macro recall@10:", df.groupby("lens").pass_at_k.mean().round(3).to_dict(), "(gate: J++ >= 0.45)")
PY
