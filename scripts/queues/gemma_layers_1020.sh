#!/usr/bin/env bash
# Gemma 4 31B-it, own lens: can the lens write at other depths? (Zach, 2026-10-20 overnight; at layers 30/33/36 the
# countries, the positive control, flip <= 9% at any strength, Qwen ~100%.) Layers 24, 27, 39, 42, 45 (the rest of the
# fitted ones), scales 0.5-4.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=gemma-4-31b-it-refit
uv run --no-sync python scripts/read_write.py --name gemma4itr_rw_layers_v1 --n 60 --from-competence gemma4itb_competence_v1 \
  --families BL BR RL RR --layers 24 27 39 42 45 --scales 0.5 1 2 4 \
  --why "Zach (2026-10-20, overnight): Gemma 4 31B-it with its own J++: can the lens write (countries, the positive control) at depths other than 30-36? (cases from gemma4itb_competence_v1, same model and revision)"
