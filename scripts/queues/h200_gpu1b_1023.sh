#!/bin/bash
# Zach (2026-10-23 ~04:20 UTC): GPU 1 while the 122B queue holds GPU 0.
# (1) the 122B gate, rerun: v1 OOMed at load (removal_textloss built vocab x d lens vectors for all 7 layers; now lazy).
#     Pre-registered layers L21-27; also, descriptive, the two bands its C1 runs at (39-45 from choose_band, 24-30).
# (2) gpt-oss-20b fails the gate at L10-13 (top-10 +4.73 nats, rotated -0.04; logit-lens top-10 +1.37, J++ without sinks
#     +4.50). Descriptive: is a single layer, or two, under the 2-nat line?
# (3) gpt-oss steering on full_v8 (amendment 8), which the gate stop skipped.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=1
PY="uv run --no-sync python"
run() { [ -f "results/$1/summary.json" ] && { echo "=== $1 done already"; return 0; }; echo "=== $1 $(date -u +%T)"; "${@:2}"; }
nll() { python3 -c "import json,sys; n=json.load(open(sys.argv[1]))['mean_nll']; print('=== nll', {k: round(v - n['none'], 2) for k, v in n.items()}, 'none', round(n['none'], 2))" results/removal_textloss/$1/summary.json; }

# (1) the 122B
export BJ_TARGET=qwen3.5-122b-a10b
P=qwen35_122b_
WHY="Zach (2026-10-23): Qwen3.5-122B-A10B (published J++) on the v2 pipeline"
run removal_textloss/${P}textloss_top_v2 $PY scripts/removal_textloss.py --name ${P}textloss_top_v2 --why "$WHY: the gate at L21-27, rerun (v1 OOMed at load before scoring)" \
  --layers $(seq 21 27) --conditions none top1 top1_rot top5 top5_rot top10 top10_rot && nll ${P}textloss_top_v2
for B in 39-45 24-30; do
  run removal_textloss/${P}textloss_L${B}_v1 $PY scripts/removal_textloss.py --name ${P}textloss_L${B}_v1 --why "$WHY: descriptive, plain-text loss at the C1 band $B" \
    --layers $(seq ${B%-*} ${B#*-}) --conditions none top1 top10 top10_rot unembed10 && nll ${P}textloss_L${B}_v1
done

# (2) gpt-oss, fewer layers (descriptive)
export BJ_TARGET=gpt-oss-20b
P=gptoss20_
WHY="Zach (2026-10-23, prereg amendment 8): gpt-oss-20b (our J++), the non-Qwen generality model"
for L in "11" "12" "11 12"; do
  N=${P}textloss_L$(echo $L | tr " " "_")_v1
  run removal_textloss/$N $PY scripts/removal_textloss.py --name $N --why "$WHY: descriptive, plain-text loss with fewer layers (L$L) after the L10-13 gate failed" \
    --layers $L --conditions none top1 top5 top10 top10_rot unembed10 && nll $N
done

# (3) gpt-oss steering, as in scripts/queues/h200_gptoss_1023.sh
CF=${P}full_v8_competence_v1
W2="--tasks full_v8 --tasks-competence $CF --tasks-level all --families PP PM MP MM CP CM"
run write_max/${P}smoke_wm2_1023 env BJ_BATCH=16 $PY scripts/write_max.py --name ${P}smoke_wm2_1023 --why smoke --n 2 --band 12-13 --single-step 1 --early 6 \
  --possets question final $W2 || { echo "steering smoke failed: stop"; exit 1; }
run copy_sweep/${P}copy_sweep_full2_v1 $PY scripts/copy_sweep.py --name ${P}copy_sweep_full2_v1 --why "$WHY: where the question / final positions carry the bridge" \
  --tasks full_v8 --tasks-competence $CF --families PP PM MP MM --n 40 --step 1 --window 4
run write_max/${P}wm2_full2_v1 env BJ_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_full2_v1 --why "$WHY: two-step steering at 10-15 (the 27B's 28-40 scaled)" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band 10-15 --single-step 1 --early 4 6 8 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_v1 | tail -3 && $PY scripts/c2_graded.py ${P}wm2_full2_v1 --drop-guessable > /dev/null \
  && $PY scripts/c2_narrow.py ${P}wm2_full2_v1 ${P}wm2_full2_v1_noguess > /dev/null
AB=$($PY scripts/choose_steer_band.py ${P}copy_sweep_full2_v1) || AB=""
echo "=== aligned band: ${AB:-none}"
[ -n "$AB" ] && run write_max/${P}wm2_full2_aligned_v1 env BJ_BATCH=64 $PY scripts/write_max.py --name ${P}wm2_full2_aligned_v1 --why "$WHY: steering at the aligned band ${AB%% *}" \
  --n 1000 --writes lens_add lens_swap copy early_lens_add early_embed_add --possets question final --band ${AB%% *} --single-step 1 --early 4 6 8 $W2 \
  && $PY scripts/c2_graded.py ${P}wm2_full2_aligned_v1 | tail -3
echo "=== gpu1b done $(date -u +%FT%TZ)"
