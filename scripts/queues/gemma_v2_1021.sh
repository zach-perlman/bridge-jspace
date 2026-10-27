#!/bin/bash
# Zach (2026-10-21, decided with Zach): Gemma 4 31B-it end to end on tasks_v2 ("v2 replaces v1"), before anything
# Qwen3-32B. Replaces gemma_full_1021.sh (suite-based; cancelled while waiting, before it ran anything).
#  1. J++ at every source layer 0-58 (final block 59 = target), 64 WikiText prompts, the recipe of our layers 24-45
#     fit; a 1-prompt run first (stop if a prompt takes > 300 s); export. 2. Gate (fixed before the fit): held-out macro
#     pass@10 on layers 24-45 >= 0.5284 - 0.05 (full-layer macro if the subset evaluation fails, logged). 3. Register
#     target gemma-4-31b-it-full (prefix gemma4itf_), commit.
#  4. Gemma's competence on ctrl_v8 (which tasks_v2 items Gemma gets right). 5. Smokes.
#  6. Positive control (does Gemma's lens write anything?): write_max v2 on countries (recalled, given) and the suite's
#     M->M, band 26-38; c2_graded's rule: Gemma's steering counts only if each reaches >= 50% with a lens write.
#  7. C1 on v2: paper10 + rotated control on ctrl_v8 at layers 11-19, 19-27, 30-38 and whole depth (the 27B's 12-20,
#     20-28, 32-40, 0-62), whole question and each step; scripts/c1_v2.py --middle L30-38 (rule fixed in b7100e0).
#  8. C2-graded on v2: write_max v2 on ctrl_v8, band 26-38, early 15/19/23; scripts/c2_graded.py.
#  9. Knock-out dose on v2: top-K, K = 1, 2, 5, 10, 25, 50, 100, each with its rotated control, at 30-38 and 11-19.
#  Ends by touching /workspace/scratch/markers/gemma_chain_done (whatever happened); the Qwen3-32B job waits for it.
set -uo pipefail
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
MARK=/workspace/scratch/markers/gemma_chain_done
mkdir -p "$(dirname $MARK)"; rm -f "$MARK"
trap 'touch "$MARK"; echo "=== marker touched $(date -u +%FT%TZ)"' EXIT
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
PY="uv run --no-sync python"
# wait: the 27B's v2 steering and v2 knock-out ended, then >= 170 GB free on 3 checks a minute apart
until grep -q "^EXIT" $R-wm2ctrlall-1021-0325.log && grep -q "^EXIT" $R-tasksko-1021-0413.log; do sleep 120; done
ok=0; while [ $ok -lt 3 ]; do
  [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)" -ge 170000 ] && ok=$((ok + 1)) || ok=0
  sleep 60; done
echo "=== start $(date -u +%FT%TZ)"
PIN=842da3794eaa0b77d5f08bae87a17459d91ff475
MAIN=$(.venv/bin/python -c 'from huggingface_hub import model_info; print(model_info("google/gemma-4-31B-it").sha)')
[ "$MAIN" = "$PIN" ] || { echo "HF main $MAIN is not the pinned $PIN: stop"; exit 1; }
LAYERS=$(seq -s, 0 58)
SMOKE=/workspace/scratch/gemma_full_smoke OUT=/workspace/ext/gemma_it_fit_full
echo "=== fit smoke (1 prompt, every layer) $(date -u +%FT%TZ)"
bash scripts/lens_fit/fit_jpp.sh google/gemma-4-31B-it "$LAYERS" "$SMOKE" 1 > "$SMOKE.log" 2>&1
grep -q FIT_DONE "$SMOKE.log" || { echo "fit smoke failed:"; tail -20 "$SMOKE.log"; exit 1; }
SEC=$(grep -oE "prompt 1/1 .* [0-9]+s" "$SMOKE.log" | grep -oE "[0-9]+s$" | tr -d s)
echo "=== fit smoke ok: ${SEC:-?}s per prompt; $(df -h /workspace | tail -1)"
[ -n "$SEC" ] && [ "$SEC" -le 300 ] || { echo "a prompt takes ${SEC:-?}s (> 300 or unknown): stop and ask"; exit 1; }
rm -rf "$SMOKE"
echo "=== fit (64 prompts) $(date -u +%FT%TZ)"
bash scripts/lens_fit/fit_jpp.sh google/gemma-4-31B-it "$LAYERS" "$OUT" 64 || { echo "fit failed"; exit 1; }
LENS=cache/gemma-4-31b-it-full/lenses/jpp/gemma-4-31B-it_jpp_lens.pt
mkdir -p "$(dirname $LENS)" results/lens_fit/gemma_it_full
$PY scripts/lens_fit/export_jpp_lens.py "$OUT/gemma-4-31B-it_jpp_lens.pt" "$LENS" \
  --note "J++ on google/gemma-4-31B-it@842da37, safety-research/jpp_lens@93f02cd recipe, 64 wikitext prompts, layers 0-58" || exit 1
SHA=$(sha256sum "$LENS" | cut -d" " -f1)
cp "$OUT"/eval_ranks*.csv "$OUT"/model_correctness.csv results/lens_fit/gemma_it_full/
rm -rf "$OUT"/artifacts  # the shard checkpoint: merged into experts.pt
echo "=== gate $(date -u +%FT%TZ); lens sha256 $SHA"
( cd /workspace/ext/jpp_lens && uv run --no-sync python scripts/jpp_cli.py evaluate --hf-model-name google/gemma-4-31B-it \
    --layers 24,27,30,33,36,39,42,45 --lens "$OUT/gemma-4-31B-it_jpp_lens.pt" --items held-out:0 \
    --correctness-csv "$OUT/model_correctness.csv" --out "$OUT/eval_ranks_shared.csv" ) > /workspace/scratch/gemma_gate_eval.log 2>&1
cp "$OUT"/eval_ranks_shared*.csv results/lens_fit/gemma_it_full/ 2>/dev/null
GATE=$(.venv/bin/python - "$OUT" <<'PY'
import csv, glob, statistics, sys
out = sys.argv[1]
def macro(path):
    rows = [r for r in csv.DictReader(open(path)) if r["k"] == "10" and r["weighting"] == "item" and r["lens"] == "gemma-4-31B-it_jpp_lens"]
    return statistics.mean(float(r["pass_at_k"]) for r in rows) if rows else None
shared = glob.glob(f"{out}/eval_ranks_shared*pass_at_k.csv")
m, which = (macro(shared[0]), "layers 24-45") if shared else (None, None)
if m is None:
    m, which = macro(f"{out}/eval_ranks_pass_at_k.csv"), "ALL layers (the layer-subset evaluation failed)"
print(f"{m:.4f} {'PASS' if m >= 0.5284 - 0.05 else 'FAIL'} {which}")
PY
)
echo "=== gate: macro pass@10 $GATE (old fit 0.5284, threshold 0.4784)"
echo "$GATE" | grep -q PASS || { echo "gate failed: stop"; exit 1; }
.venv/bin/python - "$SHA" "$GATE" <<'PY' || exit 1
import sys
from pathlib import Path
sha, gate = sys.argv[1], sys.argv[2]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
anchor = "    # Qwen3.5-122B-A10B (MoE, 10B active)"
assert anchor in s and '"gemma-4-31b-it-full"' not in s
block = f'''    # Gemma 4 31B-it with a J++ we fit on it at every source layer 0-58 (Zach asked, 2026-10-21: match Qwen3.6-27B's
    # every-layer published lens; the 24-45 every-3rd fit above stays for its runs): the same recipe (64 wikitext texts x
    # 128 tokens, skip 16, target = the final block, LRP rlens, 8 experts, readout weights on fit:0 items graded on this
    # model), scripts/queues/gemma_full_1021.sh. Gate: held-out macro pass@10 {gate}.
    "gemma-4-31b-it-full": {{
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "gemma4itf_",
        "lenses": {{
            "jpp": ("local", "cache/gemma-4-31b-it-full/lenses/jpp/gemma-4-31B-it_jpp_lens.pt", "{sha}"),
        }},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("target gemma-4-31b-it-full registered")
PY
git add src/bridge_jspace/pins.py results/lens_fit/gemma_it_full && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
  commit -q -m "pins: gemma-4-31b-it-full (J++ at every layer 0-58), gate $GATE

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 1
echo "=== registered $(git log --oneline -1)"
export BJ_TARGET=gemma-4-31b-it-full BJ_SUITE_BATCH=64 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
WHY="Zach (2026-10-21): Gemma 4 31B-it with its every-layer J++ on tasks_v2, at the 27B's relative depths"
COMP=gemma4itf_ctrl_v8_competence_v1
$PY scripts/tasks_v2.py competence --set ctrl_v8 --name $COMP --guess --why "$WHY: which ctrl_v8 items Gemma gets right" \
  || { echo "competence failed: stop"; exit 1; }
T="--tasks ctrl_v8 --tasks-competence $COMP --tasks-words PP PM MP MM --tasks-level all"
W="--tasks ctrl_v8 --tasks-competence $COMP --tasks-level all"
$PY scripts/ablate_v2.py --name gemma4itf_smoke_tasks_ko_1021 --why smoke --plan bands --bands 30-38 \
    --conditions paper10 paper10_rot $T --n 2 --kinds clean step1 step2 --batch 16 \
  && $PY scripts/write_max.py --name gemma4itf_smoke_wm2_1021 --why smoke --n 2 --band 30-32 --single-step 1 --early 23 \
    --possets question final $W || { echo "smokes failed: stop"; exit 1; }
echo "=== smokes ok $(date -u +%FT%TZ)"
$PY scripts/write_max.py --name gemma4itf_wm2_posctrl_v1 --why "$WHY: positive control (countries, the suite's M->M)" \
  --n 60 --families RR --band 26-38 --single-step 2 --early 15 19 23 --from-competence gemma4itb_competence_v1 \
  && $PY scripts/c2_graded.py gemma4itf_wm2_posctrl_v1 || echo "=== positive control FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_tasks_ko_v1 --why "$WHY: C1 on tasks_v2" --plan bands \
  --bands 11-19 19-27 30-38 0-58 --conditions paper10 paper10_rot $T --n 1000 --kinds clean step1 step2 --batch 16 \
  && $PY scripts/c1_v2.py gemma4itf_tasks_ko_v1 --middle L30-38 || echo "=== v2 knock-out FAILED"
$PY scripts/write_max.py --name gemma4itf_wm2_tasks_v1 --why "$WHY: C2-graded on tasks_v2" --n 1000 --band 26-38 \
  --single-step 2 --early 15 19 23 $W && $PY scripts/c2_graded.py gemma4itf_wm2_tasks_v1 || echo "=== v2 steering FAILED"
$PY scripts/ablate_v2.py --name gemma4itf_tasks_dose_v1 --why "$WHY: knock-out dose curve on tasks_v2" --plan bands \
  --bands 30-38 11-19 $T --n 1000 --kinds clean --batch 16 \
  --conditions top1 top1_rot top2 top2_rot top5 top5_rot top10 top10_rot top25 top25_rot top50 top50_rot top100 top100_rot \
  || echo "=== v2 dose FAILED"
echo "=== gemma chain done $(date -u +%FT%TZ)"
