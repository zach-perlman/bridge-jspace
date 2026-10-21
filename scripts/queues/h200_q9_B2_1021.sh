#!/bin/bash
# Zach (2026-10-21; replaces h200_q9_B_1021.sh before it started, decided with Zach: fill GPU 1's idle gap with 9B work):
# Qwen3.5-9B with its published J++, the knock-out set of the other models at matched relative depth (32 layers: 27B's
# 12-20 / 20-28 / 32-40 / whole -> 6-10 / 10-14 / 16-20 / whole): the C1 rule (c1_v2 --middle L16-20), the specificity
# control (unembed10), keep own word, two more control seeds, the position split, each step alone; three-step whole and
# each step. Usage: h200_q9_B2_1021.sh fill|main.
#   fill: on GPU 1 right after the Gemma knock-outs; the 9B's competence (full_v8, full_v8b) first, then the steps in
#         order; before each step it checks whether Qwen3-32B's competence is ready and, if so, hands GPU 1 back
#         (Qwen3-32B keeps its priority; it waits at most one 9B step).
#   main: on GPU 1 after Qwen3-32B's knock-outs; runs whatever the fill did not finish.
# Every step is skipped if its result exists. The whole-depth band is the lens's own layer range (left out if it skips layers).
set -u
MODE=${1:?fill or main}
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
MK9=/workspace/scratch/markers/q9_competence_done
MK32=/workspace/scratch/markers/q32_competence_done
if [ "$MODE" = fill ]; then
  until grep -qs "^EXIT" $R-h200gemmaB3-*.log; do sleep 60; done
else
  until grep -qs "^EXIT" $R-h200q32B-*.log && { [ -f $MK9 ] || grep -qs "^EXIT" $R-h200q9A-*.log; }; do sleep 60; done
fi
export BJ_TARGET=qwen3.5-9b
C2=qwen35_9b_full_v8_competence_v1
C3=qwen35_9b_full_v8b_competence_v1
WHY="Zach (2026-10-21): Qwen3.5-9B on the v2 pipeline (published J++), the same set as the others"
TWO="PP PM MP MM CP CM"
THREE="PPP PPM PMP MPP MPM MMP"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
T3="--tasks full_v8b --tasks-competence $C3 --tasks-words $THREE --tasks-level all --tasks-strata core secondary --tasks-per-word"
K="--n 1000 --kinds clean --batch 32"
run_step() {  # run_step RESULT_PATH FUNCTION: skip if done; in fill mode hand GPU 1 back once Qwen3-32B is ready
  if [ "$MODE" = fill ] && [ -f $MK32 ]; then echo "=== Qwen3-32B competence ready: GPU 1 back to Qwen3-32B $(date -u +%FT%TZ)"; exit 0; fi
  if [ -f "results/$1/summary.json" ]; then echo "=== $1 done already"; return 0; fi
  echo "=== $1 $(date -u +%T)"; "$2"
}
s_comp2() { $PY scripts/tasks_v2.py competence --set full_v8 --name $C2 --guess --why "$WHY: competence on full_v8" > /workspace/scratch/q9_comp2.log 2>&1 \
  && $PY scripts/competence_full_report.py $C2 | tail -16 || echo "=== 9B full_v8 competence FAILED"; }
s_comp3() { $PY scripts/tasks_v2.py competence --set full_v8b --name $C3 --guess --why "$WHY: competence on full_v8b" > /workspace/scratch/q9_comp3.log 2>&1 \
  && $PY scripts/competence_full_report.py $C3 | tail -16 || echo "=== 9B full_v8b competence FAILED"; }
run_step tasks_v2/$C2 s_comp2
run_step tasks_v2/$C3 s_comp3
touch $MK9
[ -f results/tasks_v2/$C2/summary.json ] || { echo "no 9B full_v8 competence: stop"; exit 1; }
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
s_smoke() { $PY scripts/ablate_v2.py --name qwen35_9b_smoke_full_ko_1021 --why smoke --plan bands --bands 16-20 \
  --conditions paper10 paper10_rot unembed10 $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }; }
s_c1() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_v1 --middle L16-20 --set full_v8 | tail -2 \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_v1 --middle L16-20 --set full_v8 --drop-guessable > /dev/null || echo "=== two-step knock-out FAILED"; }
s_unembed() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands 6-10 10-14 16-20 --conditions unembed10 unembed10_rot $T2 $K \
  && $PY scripts/c1_specificity.py qwen35_9b_full2_ko_v1 qwen35_9b_full2_ko_unembed_v1 --set full_v8 | tail -6 \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_unembed_v1 --middle L16-20 --set full_v8 > /dev/null || echo "=== unembed knock-out FAILED"; }
s_keepown() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands 16-20 --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_keepown_v1 --middle L16-20 --set full_v8 | tail -3 || echo "=== keep-own FAILED"; }
s_rot1() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_rotseed1_v1 --why "$WHY: rotated control, seed offset 1" --plan bands \
  --bands 16-20 --conditions paper10_rot --seed-offset 1 $T2 $K || echo "=== control seed 1 FAILED"; }
s_rot2() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_rotseed2_v1 --why "$WHY: rotated control, seed offset 2" --plan bands \
  --bands 16-20 --conditions paper10_rot --seed-offset 2 $T2 $K || echo "=== control seed 2 FAILED"; }
s_posc() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_pos_context_v1 --why "$WHY: position split, context positions only" --plan bands \
  --bands 6-10 16-20 --conditions paper10 paper10_rot --positions context $T2 $K \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_pos_context_v1 --middle L16-20 --set full_v8 > /dev/null || echo "=== position context FAILED"; }
s_posq() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_pos_question_v1 --why "$WHY: position split, question positions only" --plan bands \
  --bands 6-10 16-20 --conditions paper10 paper10_rot --positions question $T2 $K \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_pos_question_v1 --middle L16-20 --set full_v8 > /dev/null || echo "=== position question FAILED"; }
s_steps() { $PY scripts/ablate_v2.py --name qwen35_9b_full2_ko_steps_v1 --why "$WHY: two-step, each step alone at 16-20" --plan bands \
  --bands 16-20 --conditions paper10 paper10_rot $T2 --n 1000 --kinds step1 step2 --batch 32 \
  && $PY scripts/c1_v2.py qwen35_9b_full2_ko_steps_v1 --middle L16-20 --set full_v8 > /dev/null || echo "=== two-step steps FAILED"; }
s_three() { $PY scripts/ablate_v2.py --name qwen35_9b_full3_ko_v1 --why "$WHY: three-step, whole question" --plan bands \
  --bands $BANDS --conditions paper10 paper10_rot $T3 $K \
  && $PY scripts/c1_v2.py qwen35_9b_full3_ko_v1 --middle L16-20 --set full_v8b > /dev/null || echo "=== three-step knock-out FAILED"; }
s_three_steps() { $PY scripts/ablate_v2.py --name qwen35_9b_full3_ko_steps_v1 --why "$WHY: three-step, each step alone at 16-20" --plan bands \
  --bands 16-20 --conditions paper10 paper10_rot $T3 --n 1000 --kinds step1 step2 step3 --batch 32 \
  && $PY scripts/c1_v2.py qwen35_9b_full3_ko_steps_v1 --middle L16-20 --set full_v8b > /dev/null || echo "=== three-step steps FAILED"; }
echo "=== start ($MODE) $(date -u +%FT%TZ)"
run_step ablate_v2/qwen35_9b_smoke_full_ko_1021 s_smoke
run_step ablate_v2/qwen35_9b_full2_ko_v1 s_c1
run_step ablate_v2/qwen35_9b_full2_ko_unembed_v1 s_unembed
run_step ablate_v2/qwen35_9b_full2_ko_keepown_v1 s_keepown
run_step ablate_v2/qwen35_9b_full2_ko_rotseed1_v1 s_rot1
run_step ablate_v2/qwen35_9b_full2_ko_rotseed2_v1 s_rot2
run_step ablate_v2/qwen35_9b_full2_ko_pos_context_v1 s_posc
run_step ablate_v2/qwen35_9b_full2_ko_pos_question_v1 s_posq
run_step ablate_v2/qwen35_9b_full2_ko_steps_v1 s_steps
if [ -f results/tasks_v2/$C3/summary.json ]; then
  run_step ablate_v2/qwen35_9b_full3_ko_v1 s_three
  run_step ablate_v2/qwen35_9b_full3_ko_steps_v1 s_three_steps
else
  echo "=== no full_v8b competence: three-step knock-outs skipped"
fi
echo "=== 9B GPU 1 part ($MODE) done $(date -u +%FT%TZ)"
