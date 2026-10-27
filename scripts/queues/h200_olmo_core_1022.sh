#!/bin/bash
# Zach (2026-10-22, prereg amendment 6B): one Olmo model through every model's pipeline, as the 9B (also 32 blocks), C1
# first. Usage: h200_olmo_core_1022.sh TARGET PREFIX GPU [WAIT_LOG_GLOB]
#   waits for the target's lens (registered by h200_olmo_fit_1022.sh) and, if given, for WAIT_LOG_GLOB's EXIT line.
# Steps: the untestable gate (plain-text loss under the knock-out at L14-18; stop if top-10 adds >= 2 nats with the
# rotated control within 0.3), competence on ctrl_v8 and full_v8 (parallel), the ctrl_v8 depth sweep (5-layer windows by
# 2), the band (scripts/choose_band.py), C1 on full_v8 (6-10, 10-14, the band, whole depth) and its scoring, the
# logit-lens control, keep-own, two more control seeds, plain-text loss at the band, then steering (copy sweep, two-step
# at 14-20 as the 9B, C2-graded / -relative / C2', the aligned band).
set -u
KEY=$1 P=$2 G=$3 WAIT=${4:-}
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
. scripts/queues/lib_competence_parallel.sh
until grep -qs "\"$KEY\": {" src/bridge_jspace/pins.py; do sleep 60; done
[ -n "$WAIT" ] && { until grep -qs "^EXIT" $WAIT; do sleep 60; done; }
export BJ_TARGET=$KEY
WHY="Zach (2026-10-22, prereg amendment 6B): $KEY (our J++), the Olmo architecture pair"
echo "=== start $KEY on GPU $G $(date -u +%FT%TZ)"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }
# 1. the untestable gate
run removal_textloss/${P}textloss_top_v1 $PY scripts/removal_textloss.py --name ${P}textloss_top_v1 --why "$WHY: plain-text loss under the knock-out, L14-18 (the untestable gate)" \
  --layers $(seq 14 18) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot || echo "=== text loss FAILED"
GATE=$(python3 - results/removal_textloss/${P}textloss_top_v1/summary.json <<'PY'
import json, sys
n = json.load(open(sys.argv[1]))["mean_nll"]
d, r = n["top10"] - n["none"], n["top10_rot"] - n["none"]
print(f"top-10 +{d:.2f} nats, rotated +{r:.2f}: " + ("UNTESTABLE" if d >= 2 and r <= 0.3 else "testable"))
PY
)
echo "=== gate: $GATE"
case "$GATE" in *UNTESTABLE*) echo "=== $KEY untestable: stop"; exit 0;; esac
# 2. competence (ctrl_v8 for the band, full_v8 for the test)
CC=${P}ctrl_v8_competence_v1 C2=${P}full_v8_competence_v1
comp_parallel 2 "$WHY" $CC:ctrl_v8 $C2:full_v8
$PY scripts/competence_full_report.py $C2 | tail -10
[ -f results/tasks_v2/$C2/summary.json ] && [ -f results/tasks_v2/$CC/summary.json ] || { echo "no competence: stop"; exit 1; }
# 3. the band, on ctrl_v8
run ablate_v2/${P}ctrl_sweep_v1 $PY scripts/ablate_v2.py --name ${P}ctrl_sweep_v1 \
  --why "$WHY: depth sweep on ctrl_v8 to choose the middle band (every model's procedure; 5-layer windows sliding by 2)" \
  --plan bands --bands 0-4 2-6 4-8 6-10 8-12 10-14 12-16 14-18 16-20 18-22 20-24 22-26 24-28 26-30 --conditions paper10 paper10_rot \
  --tasks ctrl_v8 --tasks-competence $CC --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32 || echo "=== ctrl_v8 sweep FAILED"
MID=$($PY scripts/choose_band.py ${P}ctrl_sweep_v1 "") || MID=""
[ -n "$MID" ] || { MID=16-20; echo "=== no band chosen: the relative-depth band 16-20 instead"; }
echo "=== middle band: $MID"
uniq_bands() { echo "$@" | tr " " "\n" | awk 'NF && !s[$0]++' | tr "\n" " "; }
TWO="PP PM MP MM CP CM"
T2="--tasks full_v8 --tasks-competence $C2 --tasks-words $TWO --tasks-level all"
K="--n 1000 --kinds clean --batch 32"
# 4. C1
run ablate_v2/${P}smoke_full_ko_1022 $PY scripts/ablate_v2.py --name ${P}smoke_full_ko_1022 --why smoke --plan bands --bands $MID \
  --conditions paper10 paper10_rot unembed10 $T2 --n 2 --kinds clean step1 --batch 16 || { echo "smoke failed: stop"; exit 1; }
run ablate_v2/${P}full2_ko_v1 $PY scripts/ablate_v2.py --name ${P}full2_ko_v1 --why "$WHY: two-step, C1, whole question" --plan bands \
  --bands $(uniq_bands 6-10 10-14 $MID 0-30) --conditions paper10 paper10_rot $T2 $K || echo "=== two-step knock-out FAILED"
$PY scripts/c1_v2.py ${P}full2_ko_v1 --middle L$MID --set full_v8 | tail -2
$PY scripts/c1_v2.py ${P}full2_ko_v1 --middle L$MID --set full_v8 --drop-guessable > /dev/null
# 5. checks
run ablate_v2/${P}full2_ko_unembed_v1 $PY scripts/ablate_v2.py --name ${P}full2_ko_unembed_v1 --why "$WHY: the specificity control (the logit lens's directions)" \
  --plan bands --bands $(uniq_bands 6-10 10-14 $MID) --conditions unembed10 unembed10_rot $T2 $K \
  && $PY scripts/c1_specificity.py ${P}full2_ko_v1 ${P}full2_ko_unembed_v1 --set full_v8 | tail -4
run ablate_v2/${P}full2_ko_keepown_v1 $PY scripts/ablate_v2.py --name ${P}full2_ko_keepown_v1 --why "$WHY: C1's second kill test (keep own word)" --plan bands \
  --bands $MID --conditions paper10 paper10_rot paper10_keepown paper10_keepown_rot $T2 $K \
  && $PY scripts/c1_v2.py ${P}full2_ko_keepown_v1 --middle L$MID --set full_v8 | tail -3
run ablate_v2/${P}full2_ko_rotseed1_v1 $PY scripts/ablate_v2.py --name ${P}full2_ko_rotseed1_v1 --why "$WHY: rotated control, seed offset 1" --plan bands \
  --bands $MID --conditions paper10_rot --seed-offset 1 $T2 $K
run ablate_v2/${P}full2_ko_rotseed2_v1 $PY scripts/ablate_v2.py --name ${P}full2_ko_rotseed2_v1 --why "$WHY: rotated control, seed offset 2" --plan bands \
  --bands $MID --conditions paper10_rot --seed-offset 2 $T2 $K
[ "$MID" != 14-18 ] && run removal_textloss/${P}textloss_top_l${MID%-*}_${MID#*-}_v1 $PY scripts/removal_textloss.py --name ${P}textloss_top_l${MID%-*}_${MID#*-}_v1 \
  --why "$WHY: plain-text loss under the knock-out at the chosen band" --layers $(seq ${MID%-*} ${MID#*-}) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot
# 6. steering
W2="--tasks full_v8 --tasks-competence $C2 --tasks-level all --families $TWO"
run write_max/${P}smoke_wm2_full_1022 env BJ_SUITE_BATCH=32 $PY scripts/write_max.py --name ${P}smoke_wm2_full_1022 --why smoke --n 2 --band 16-17 --single-step 1 --early 12 \
  --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
run copy_sweep/${P}copy_sweep_full2_v1 $PY scripts/copy_sweep.py --name ${P}copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $C2 --families PP PM MP MM --n 40 --step 1 --window 6 || echo "=== copy sweep FAILED"
run write_max/${P}wm2_full2_v1 env BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_full2_v1 --why "$WHY: two-step steering, full pools (band 14-20, as the 9B)" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band 14-20 --single-step 1 --early 8 10 12 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_v1 | tail -3 && $PY scripts/c2_graded.py ${P}wm2_full2_v1 --drop-guessable > /dev/null \
  && $PY scripts/c2_narrow.py ${P}wm2_full2_v1 ${P}wm2_full2_v1_noguess | head -1
AB=$($PY scripts/choose_steer_band.py ${P}copy_sweep_full2_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
[ -n "$AB" ] && run write_max/${P}wm2_full2_aligned_v1 env BJ_SUITE_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_full2_aligned_v1 \
  --why "$WHY: two-step steering at the aligned band ${AB%% *} (scripts/choose_steer_band.py)" --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add \
  --possets question final --band ${AB%% *} --single-step 1 --early 8 10 12 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_aligned_v1 | tail -3 && $PY scripts/c2_graded.py ${P}wm2_full2_aligned_v1 --drop-guessable > /dev/null \
  && $PY scripts/c2_narrow.py ${P}wm2_full2_aligned_v1 ${P}wm2_full2_aligned_v1_noguess | head -1
echo "=== $KEY core done $(date -u +%FT%TZ)"
