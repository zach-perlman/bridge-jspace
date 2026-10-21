#!/bin/bash
# Zach (2026-10-21, decided with Zach: the 9B on this pipeline after Qwen3-32B): Qwen3.5-9B with its published J++,
# GPU 1 part, after Qwen3-32B's knock-outs and the 9B's competence (h200_q9_A_1021.sh). The other models' knock-out set
# at matched relative depth (32 layers: 27B's 12-20 / 20-28 / 32-40 / whole -> 6-10 / 10-14 / 16-20 / 0-30): the C1
# rule (c1_v2 --middle L16-20), the specificity control (unembed10), keep own word, two more control seeds, the
# position split, each step alone; three-step whole and each step. The whole-depth band is the lens's own layer range
# (checked below; left out if the lens skips layers).
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK=/workspace/scratch/markers/q9_competence_done
until grep -qs "^EXIT" $R-h200q32B-*.log && { [ -f $MK ] || grep -qs "^EXIT" $R-h200q9A-*.log; }; do sleep 60; done
export BJ_TARGET=qwen3.5-9b
C2=qwen35_9b_full_v8_competence_v1
C3=qwen35_9b_full_v8b_competence_v1
[ -f results/tasks_v2/$C2/summary.json ] || { echo "no 9B full_v8 competence: stop"; exit 1; }
WHY="Zach (2026-10-21): Qwen3.5-9B on the v2 pipeline (published J++), the same set as the others"
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
K="--n 1000 --kinds clean --batch 32"
WHOLE=$($PY - <<'PY'
import hashlib
import torch
from huggingface_hub import hf_hub_download
p = hf_hub_download("neuronpedia/jacobian-lens", "qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt",
                    revision="e166deb5ad540932100ef803c8c9bcc2a5453694")
h = hashlib.sha256(open(p, "rb").read()).hexdigest()
assert h == "8cda12f7ddf11e70fcfc69a47a9574f626fe084c67807a4781f4f67106e739c5", h
L = sorted(int(x) for x in torch.load(p, map_location="cpu", weights_only=False)["source_layers"])
print(f"{L[0]}-{L[-1]}" if L == list(range(L[0], L[-1] + 1)) else "gaps")
PY
)
echo "=== 9B lens layers: $WHOLE"
case "$WHOLE" in gaps|"") BANDS="6-10 10-14 16-20"; echo "=== whole-depth band left out (lens layers: ${WHOLE:-unknown})";; *) BANDS="6-10 10-14 16-20 $WHOLE";; esac
echo "=== start $(date -u +%FT%TZ)"
$PY scripts/ablate_v2.py --name qwen35_9b_smoke_full_ko_1021 --why smoke --plan bands --bands 16-20 \
  --conditions paper10 paper10_rot unembed10 $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
$PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_v1 --middle L16-20 --set full_v8 | tail -2 \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_v1 --middle L16-20 --set full_v8 --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"
$PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands 6-10 10-14 16-20 --conditions unembed10 unembed10_rot $T2 $K \
  && $PY scripts/c1_specificity.py qwen35_9b_full2_ko_v1 qwen35_9b_full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_unembed_v1 --middle L16-20 --set full_v8 > /dev/null || echo "=== unembed knock-out FAILED"
$PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands 16-20 --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_keepown_v1 --middle L16-20 --set full_v8 | tail -3 || echo "=== keep-own FAILED"
for s in 1 2; do
  $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_rotseed${s}_v1 --why "$WHY: rotated control, seed offset $s" --plan bands \
    --bands 16-20 --conditions paper10_rot --seed-offset $s $T2 $K || echo "=== control seed $s FAILED"
done
for pos in context question; do
  $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_pos_${pos}_v1 --why "$WHY: position split, $pos positions only" --plan bands \
    --bands 6-10 16-20 --conditions paper10 paper10_rot --positions $pos $T2 $K \
    && $PY scripts/c1_v2.py qwen35_9b_full2_ko_pos_${pos}_v1 --middle L16-20 --set full_v8 > /dev/null || echo "=== position $pos FAILED"
done
$PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at 16-20" --plan bands \
  --bands 16-20 --conditions paper10 paper10_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_steps_v1 --middle L16-20 --set full_v8 > /dev/null || echo "=== two-step steps FAILED"
if [ -f results/tasks_v2/$C3/summary.json ]; then
  $PY scripts/ablate_v2.py --name qwen35_9b_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
    --bands $BANDS --conditions paper10 paper10_rot $T3 $K \
    && $PY scripts/c1_v2.py qwen35_9b_full3_ko_v1 --middle L16-20 --set full_v8b > /dev/null || echo "=== three-step knock-out FAILED"
  $PY scripts/ablate_v2.py --name qwen35_9b_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at 16-20" --plan bands \
    --bands 16-20 --conditions paper10 paper10_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
    && $PY scripts/c1_v2.py qwen35_9b_full3_ko_steps_v1 --middle L16-20 --set full_v8b > /dev/null || echo "=== three-step steps FAILED"
else
  echo "=== no full_v8b competence: three-step knock-outs skipped"
fi
echo "=== 9B GPU 1 part done $(date -u +%FT%TZ)"
