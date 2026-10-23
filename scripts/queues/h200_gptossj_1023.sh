#!/bin/bash
# Zach (2026-10-23, prereg amendment 8b): gpt-oss-20b with neuronpedia's published plain J-lens (target gpt-oss-20b-jlens),
# after our LN-rule-only J++ failed the gate. Lens agreement; the gate at L10-13; if testable, the band on ctrl_v8 and C1
# on olmo_big_v8nc with the logit-lens control and a control seed. GPU 1, alongside the gpu1b queue's gpt-oss steps.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1 BJ_TARGET=gpt-oss-20b-jlens
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
# wait for the 122B to leave GPU 1 (gpu1b on to its gpt-oss steps) and >= 60 GB free
until grep -qs "^=== removal_textloss/gptoss20_textloss_L11_v1" $R-h200gpu1b-1023-0420.log \
  && [ "$(nvidia-smi -i 1 --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 60000 ]; do sleep 30; done
echo "=== start $(date -u +%FT%TZ)"
P=gptoss20j_
WHY="Zach (2026-10-23, prereg amendment 8b): gpt-oss-20b with neuronpedia's plain J-lens (a labelled comparison lens)"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }
$PY scripts/lens_agreement.py --name ${P}lens_agreement_v1 --why "$WHY: lens check" > /workspace/scratch/${P}agree.log 2>&1 || echo "=== lens check FAILED"
python3 - results/lens_agreement/${P}lens_agreement_v1/summary.json <<'PY' || true
import json, sys
a = json.load(open(sys.argv[1]))["top10_agreement"]
print("=== agreement (J-lens / logit):", " ".join("L%s %.2f/%.2f" % (l, a[l]["lens"], a[l]["logit"]) for l in ["6", "10", "13", "17", "20", "22"] if l in a))
PY
run removal_textloss/${P}textloss_top_v1 $PY scripts/removal_textloss.py --name ${P}textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L10-13 (the gate)" \
  --layers $(seq 10 13) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot
python3 - results/removal_textloss/${P}textloss_top_v1/summary.json <<'PY' && echo "=== gate: testable" || { echo "=== gpt-oss J-lens untestable: stop"; exit 0; }
import json, sys
n = json.load(open(sys.argv[1]))["mean_nll"]
d, r = n["top10"] - n["none"], n["top10_rot"] - n["none"]
print(f"=== gate: top-10 +{d:.2f} nats, rotated +{r:.2f}")
sys.exit(1 if (d >= 2 and r <= 0.3) else 0)
PY
CC=gptoss20_ctrl_v8_competence_v1
CB=gptoss20_olmo_big_v8nc_competence_v1
run ablate_v2/${P}ctrl_sweep_v1 $PY scripts/ablate_v2.py --name ${P}ctrl_sweep_v1 --why "$WHY: depth sweep on ctrl_v8 to choose the middle band (4-layer windows by 2)" \
  --plan bands --bands 0-3 2-5 4-7 6-9 8-11 10-13 12-15 14-17 16-19 18-21 --conditions paper10 paper10_rot \
  --tasks ctrl_v8 --tasks-competence $CC --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32
MID=$($PY scripts/choose_band.py ${P}ctrl_sweep_v1 "") || MID=""
[ -n "$MID" ] || { MID=12-15; echo "=== no band chosen: the relative-depth band 12-15 instead"; }
echo "=== middle band: $MID"
T2="--tasks olmo_big_v8nc --tasks-competence $CB --tasks-words PP PM MP MM --tasks-level all"
K="--n 1000 --kinds clean --batch 32"
BANDS=$(echo "$MID 12-15" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " ")
run ablate_v2/${P}smoke_big_ko_1023 $PY scripts/ablate_v2.py --name ${P}smoke_big_ko_1023 --why smoke --plan bands --bands $MID --conditions paper10 paper10_rot $T2 --n 2 --kinds clean --batch 8 \
  || { echo "smoke failed: stop"; exit 1; }
run ablate_v2/${P}big2_ko_v1 $PY scripts/ablate_v2.py --name ${P}big2_ko_v1 --why "$WHY: C1 at the band and at 12-15 on olmo_big_v8nc" --plan bands --bands $BANDS \
  --conditions paper10 paper10_rot $T2 $K
$PY scripts/c1_v2.py ${P}big2_ko_v1 --middle L$MID --set olmo_big_v8nc | tail -2
run ablate_v2/${P}big2_ko_unembed_v1 $PY scripts/ablate_v2.py --name ${P}big2_ko_unembed_v1 --why "$WHY: the logit-lens control" --plan bands --bands $MID \
  --conditions unembed10 unembed10_rot $T2 $K
run ablate_v2/${P}big2_ko_rotseed1_v1 $PY scripts/ablate_v2.py --name ${P}big2_ko_rotseed1_v1 --why "$WHY: control seed 1" --plan bands --bands $MID --conditions paper10_rot --seed-offset 1 $T2 $K
echo "=== gpt-oss J-lens done $(date -u +%FT%TZ)"
