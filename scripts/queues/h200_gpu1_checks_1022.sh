#!/bin/bash
# 2026-10-22 ~18:20 UTC (speed-up, Zach asked): the amendment-3 checks moved from GPU 0's queue to GPU 1, run now
# beside the 9B's knock-outs (GPU 1 has ~110 GB free and the 9B's competence runs are CPU-bound). Same commands.
# Zach (2026-10-22 ~17:00 UTC; docs/prereg_replication_1022.md amendment 3): GPU 0 after Muse's steering recovery
# (h200_muse_c2fix_1022.sh, whose full-write C2 re-run is swapped for this scored-writes one; identical verdicts):
# (1) Muse's pre-registered C2 at the current band; (2) Qwen3-32B's late-layer write check (54-62); (3) Qwen3-32B's C1
# with its published J-lens; (4) the 27B's size-matched specificity control; Muse's late-layer write check (amendment 5). (Qwen3-8B dropped, Zach.) The 9B's GPU 0
# part follows.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
S=$( [ "$(cat /workspace/scratch/markers/c1_protocol 2>/dev/null)" = nosink ] && echo _nosink )
TWO="PP PM MP MM CP CM"
K="--n 1000 --kinds clean --batch 32"
TRIM="--writes lens_add lens_swap copy early_lens_add early_embed_add"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
archive() { [ -d "$1" ] && [ ! -f "$1/summary.json" ] && mkdir -p /workspace/runs/archive_cancelled/results && mv "$1" /workspace/runs/archive_cancelled/results/$(basename $1)_$2 && echo "archived $1"; }
echo "=== start $(date -u +%FT%TZ)"
W2M=""
echo "=== 27B size-matched specificity $(date -u +%T)"
BJ_TARGET=qwen3.6-27b $PY scripts/removal_size.py --name removal_size_ks_v1 --why "Zach (2026-10-22, amendment 3): removal size by K, to size-match the unembedding control" \
  --layers 32 36 40 --ks 10 20 30 40 50 || echo "=== removal size by K FAILED"
KU=$(python3 - <<'PY'
import json, statistics
d = json.load(open("results/removal_size/removal_size_ks_v1/summary.json"))["median_share"]
target = statistics.mean(v["jlens_top10"] for v in d.values())
best = min((abs(statistics.mean(v[f"unembed_top{k}"] for v in d.values()) - target), k) for k in (10, 20, 30, 40, 50))
print(best[1])
PY
) || KU=""
echo "=== size-matched unembedding K: ${KU:-none}"
[ -n "$KU" ] && { BJ_TARGET=qwen3.6-27b $PY scripts/ablate_v2.py --name full2_ko_unembed_sized_v1 \
  --why "Zach (2026-10-22, amendment 3): the specificity control size-matched to the J-lens removal (unembed$KU)" --plan bands \
  --bands 32-40 --conditions unembed$KU$S unembed$KU${S}_rot --tasks full_v8 --tasks-competence full_v8_competence_v1 --tasks-words $TWO --tasks-level all $K \
  && python3 - "$KU" <<'PY' || echo "=== size-matched table FAILED"; }
import collections, json, statistics, sys
k = sys.argv[1]
rows = [json.loads(x) for x in open("results/ablate_v2/full2_ko_unembed_sized_v1/rows.jsonl")]
acc = collections.defaultdict(list)
for r in rows:
    if r["kind"] == "clean":
        acc[(r["condition"], r["family"])].append(r["correct"])
a = {c: {w: 100 * statistics.mean(acc[(c, w)]) for w in ("PP", "MP", "PM", "MM", "CP", "CM")} for c in {c for c, _ in acc}}
base = a["none"]
cond = next(c for c in a if c.startswith("unembed") and not c.endswith("_rot"))
loss = {w: base[w] - a[cond][w] for w in base}
gap = (loss["PM"] + loss["MM"]) / 2 - (loss["PP"] + loss["MP"]) / 2
out = {"K": int(k), "accuracy": a, "gap": gap, "holds_size_matched": gap <= 10}
open("results/ablate_v2/c1_specificity/full2_ko_unembed_sized_v1.json", "w").write(json.dumps(out, indent=2) + "\n")
print(f"size-matched unembed{k} at 32-40:", {w: round(v) for w, v in a[cond].items()}, f"gap {gap:.0f} (J-lens 36) ->", "specificity holds size-matched" if gap <= 10 else "specificity does NOT hold size-matched")
PY

echo "=== Qwen3-32B C1 with its published J-lens $(date -u +%T)"
BJ_TARGET=qwen3-32b-jlens $PY scripts/ablate_v2.py --name qwen3_32bj_full2_ko_v1 --why "Zach (2026-10-22, amendment 3): Qwen3-32B's C1 at 44-52 with neuronpedia's published J-lens" \
  --plan bands --bands 44-52 --conditions paper10$S paper10${S}_rot --tasks full_v8 --tasks-competence qwen3_32b_full_v8_competence_v1 --tasks-words $TWO --tasks-level all $K \
  && BJ_TARGET=qwen3-32b-jlens $PY scripts/c1_v2.py qwen3_32bj_full2_ko_v1 --middle L44-52 --set full_v8 --suffix "$S" | tail -2 || echo "=== Qwen3-32B J-lens C1 FAILED"

echo "=== Qwen3-32B late-layer write check $(date -u +%T)"
W2Q="--tasks full_v8 --tasks-competence qwen3_32b_full_v8_competence_v1 --tasks-level all --families $TWO"
BJ_TARGET=qwen3-32b BJ_BATCH=64 $PY scripts/write_max.py --name qwen3_32b_wm2_full2_late_v1 --why "Zach (2026-10-22, amendment 3): lens writes at the final position at layers 54-62 (a direct push on the answer?)" \
  --n 1000 --writes lens_add copy --possets final --band 54-62 --single-step 2 --early 16 $W2Q || echo "=== late-layer check FAILED"
python3 - <<'PY' || echo "=== late-layer table FAILED"
import collections, json
from pathlib import Path
out = {}
for run in ("qwen3_32b_wm2_full2_aligned_v1", "qwen3_32b_wm2_full2_late_v1"):
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
late = [mm[str(la)] for la in (58, 60, 62) if str(la) in mm]
verdict = None if not late or "52" not in mm else ("not a direct output effect" if max(late) < mm["52"] / 2 else "FLAG: possibly a direct output effect")
Path("results/write_max/late_check").mkdir(parents=True, exist_ok=True)
Path("results/write_max/late_check/qwen3_32b.json").write_text(json.dumps({"best_flips_lens_add_final_by_layer": out, "verdict": verdict}, indent=2) + "\n")
for f in ("PP", "MP", "CP", "PM", "MM", "CM"):
    print(f, {la: round(100 * v) for la, v in sorted(out.get(f, {}).items(), key=lambda x: (x[0] == "joint", int(x[0]) if x[0].isdigit() else 0))})
print("late-layer verdict (amendment 3):", verdict)
PY

echo "=== GPU 1 checks done $(date -u +%FT%TZ)"
