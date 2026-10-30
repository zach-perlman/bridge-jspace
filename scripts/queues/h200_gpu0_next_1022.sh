#!/bin/bash
# Zach (2026-10-22 ~17:00 UTC; docs/breadth/prereg_replication_1022.md amendment 3): GPU 0 after Muse's steering recovery
# (h200_muse_c2fix_1022.sh, whose full-write C2 re-run is swapped for this scored-writes one; identical verdicts):
# 2026-10-22 ~18:20 UTC (speed-up): the Qwen3-32B and 27B checks moved to GPU 1 (h200_gpu1_checks_1022.sh), run
# beside the 9B. Left here: (1) Muse's pre-registered C2 at the current band; (2) Qwen3-32B's late-layer write check (54-62); (3) Qwen3-32B's C1
# with its published J-lens; (4) the 27B's size-matched specificity control; Muse's late-layer write check (amendment 5). (Qwen3-8B dropped, Zach.) The 9B's GPU 0
# part follows.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
until grep -qs "^EXIT" $R-h200musec2-*.log; do sleep 60; done
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )
TWO="PP PM MP MM CP CM"
K="--n 1000 --kinds clean --batch 32"
TRIM="--writes lens_add lens_swap copy early_lens_add early_embed_add"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
archive() { [ -d "$1" ] && [ ! -f "$1/summary.json" ] && mkdir -p /workspace/runs/archive_cancelled/results && mv "$1" /workspace/runs/archive_cancelled/results/$(basename $1)_$2 && echo "archived $1"; }
echo "=== start $(date -u +%FT%TZ)"
echo "=== Muse C2 (current band, scored writes) $(date -u +%T)"
archive results/write_max/muse30_wm2_full2_v1 fullwrites
W2M="--tasks full_v8 --tasks-competence muse30_full_v8_competence_v1 --tasks-level all --families $TWO"
BJ_TARGET=muse-glimmer-30b BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full2_v1 --why "Zach (2026-10-22): Muse Glimmer 30B, our J++: two-step steering, full pools, joint paste ceiling (scored writes)" \
  --n 1000 $TRIM --possets question final --band 23-33 --single-step 2 --early 13 16 20 $W2M \
  && BJ_TARGET=muse-glimmer-30b $PY scripts/c2_graded.py muse30_wm2_full2_v1 | tail -14 \
  && BJ_TARGET=muse-glimmer-30b $PY scripts/c2_graded.py muse30_wm2_full2_v1 --drop-guessable > /dev/null \
  && BJ_TARGET=muse-glimmer-30b $PY scripts/c2_narrow.py muse30_wm2_full2_v1 muse30_wm2_full2_v1_noguess || echo "=== Muse C2 FAILED"

echo "=== Muse late-layer write check $(date -u +%T)"
BJ_TARGET=muse-glimmer-30b BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name muse30_wm2_full2_late_v1 --why "Zach (2026-10-22, amendment 5): lens writes at the final position at layers 34-50 (a direct push on the answer?)" \
  --n 1000 --writes lens_add copy --possets final --band 34-50 --single-step 2 --early 13 $W2M || echo "=== Muse late-layer check FAILED"
python3 - <<'PY2' || echo "=== Muse late-layer table FAILED"
import collections, json
from pathlib import Path
out = {}
for run in ("muse30_wm2_full2_aligned_v1", "muse30_wm2_full2_late_v1"):
    p = Path(f"results/write_max/{run}/outcomes.jsonl")
    if not p.exists():
        continue
    cell = collections.defaultdict(list)
    for line in p.open():
        o = json.loads(line)
        if o["write"] == "lens_add" and not o["control"] and o["pos"] == "final":
            cell[(o["family"], str(o["layer"]), o["strength"])].append(o["role"] == "b")
    for (f, la, s), v in cell.items():
        out.setdefault(f, {}).setdefault(la, 0.0)
        out[f][la] = max(out[f][la], sum(v) / len(v))
mm = out.get("MM", {})
late = [mm[str(la)] for la in (46, 48, 50) if str(la) in mm]
verdict = None if not late or "32" not in mm else ("not a direct output effect" if max(late) < mm["32"] / 2 else "FLAG: possibly a direct output effect")
Path("results/write_max/late_check").mkdir(parents=True, exist_ok=True)
Path("results/write_max/late_check/muse30.json").write_text(json.dumps({"best_flips_lens_add_final_by_layer": out, "verdict": verdict}, indent=2) + "\n")
for f in ("PP", "MP", "CP", "PM", "MM", "CM"):
    print(f, {la: round(100 * v) for la, v in sorted(out.get(f, {}).items(), key=lambda x: (x[0] == "joint", int(x[0]) if x[0].isdigit() else 0))})
print("Muse late-layer verdict (amendment 5):", verdict)
PY2

unset BJ_TARGET
$PY scripts/cross_model_summary.py > /dev/null || echo "=== cross-model summary FAILED"
echo "=== GPU 0 next done $(date -u +%FT%TZ)"
