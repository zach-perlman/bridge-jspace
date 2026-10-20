#!/usr/bin/env bash
# Gemma 4 31B-it with the published base-model J++ (Zach, 2026-10-20): competence, read/write, J-space removal.
set -euo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export BJ_TARGET=gemma-4-31b-it-baselens
S="uv run --no-sync python scripts/suite_v1.py"
R="uv run --no-sync python scripts/read_write.py"
A="uv run --no-sync python scripts/ablate_pilot.py"
W="Zach (2026-10-20): does the memory-vs-prompt pattern hold on Gemma 4 31B-it (another family), with the base model's published J++?"
$S manifest --set main --name gemma4itb_smoke_1020 --limit 4 --why "smoke"
$S competence --name gemma4itb_smoke_1020
$S manifest --set main --name gemma4itb_competence_v1 --limit 150 --why "$W (competence, first 150 per family)"
$S competence --name gemma4itb_competence_v1
$S manifest --set computed --name gemma4itb_competence_computed_v1 --limit 150 --why "$W (computed bridges)"
$S competence --name gemma4itb_competence_computed_v1
$R --name gemma4itb_smoke_rw_1020 --n 2 --from-competence gemma4itb_competence_v1 --families BL BR RL RR --layers 30 33 36 --scales 1 4 --why "smoke"
$R --name gemma4itb_rw_v1 --n 60 --from-competence gemma4itb_competence_v1 --families BL BR RL RR --layers 30 33 36 --scales 0.5 1 2 4 8 16 --why "$W (read and write; layers at the 27B's relative depth)"
$A --name gemma4itb_smoke_abl_1020 --n 2 --layers 30 33 36 --comp-main gemma4itb_competence_v1 --comp-computed gemma4itb_competence_computed_v1 --countries-build --why "smoke"
$A --name gemma4itb_abl_v1 --n 100 --layers 30 33 36 --comp-main gemma4itb_competence_v1 --comp-computed gemma4itb_competence_computed_v1 --countries-build --why "$W (J-space removal)"
