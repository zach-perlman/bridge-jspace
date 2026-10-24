#!/bin/bash
# Zach (2026-10-24, prereg amendment 28 note 2): Kolibri-1's J++ and its module 1 knock-outs.
# Lens. The FP8 matmul kernels have no backward (h200_kolchk_1024.sh), so the Jacobians are fit on the FP8 checkpoint
# dequantized to bf16 on load (jpp_cli --dequantize-fp8, as the J++ authors fit DeepSeek-V4; exact: one expert checked
# against a hand dequantization), sharded over both GPUs (--device-map auto). Everything forward-only (grading, the
# readout weights, the held-out evaluation, the knock-outs) runs the FP8 model on one GPU, as the 122B's published lens
# (fit on its bf16 weights) is used with its FP8 weights. Recipe: our J++ (as for Muse, Qwen3-32B, Gemma and the Olmos;
# amendment 28 note) with the published MoE lens's settings: lrp_mode r+moe, 64 WikiText prompts, 128 tokens, the first
# 16 positions skipped, every block but the last a source (0-48), the final block the target, 8 router clusters;
# /workspace/ext/jpp_lens_kol's Kolibri patchers (Kolibri1RMSNorm: the Qwen2 LN rule; the shared and routed experts:
# identity + half; router weights detached; the ungated shared expert: the backward x4, no gate to detach), CPU-checked
# on a tiny Kolibri and on the real first two blocks (scripts/lens_fit/test_kolibri_lrp*.py). Primary lens: the weighted
# J++ (target kolibri-1); secondary: the same fit's pooled RelP lens, the kind every published neuronpedia "jpp" lens is
# (target kolibri-1-pooled). A 1-prompt smoke first, timed, choosing the rows per pass (exact batching). Shard
# checkpoints go to /dev/shm (disk is short). Then, per amendment 28: the plain-text gate (removal_textloss, top10 vs
# rotated, layers 15-35; untestable if top10 alone adds >= 2 nats while the rotation stays within 0.3), the lens check,
# dev competence + band sweep (windows of 7 by 3; paper10 / rotated; PP PM MP MM; n 100), choose_band, the test
# knock-out at that band (paper10 / rot, unembed10 / rot; 12 words), jsuite_score; the pooled lens at the same band.
# Usage: h200_kolfit_1024.sh STEP ...   waitq:JOB  fit  gate:GPU  check:GPU  dev:GPU  test:GPU  testp:GPU
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY="uv run --no-sync python"
KPY=/workspace/ext/kolibri_env/bin/python
JPPK=/workspace/ext/jpp_lens_kol
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-24, prereg amendment 28 note 2)"
KEY=kolibri-1; P=kol1_; REV=5bb7075ba22db733e3834b1c71d2245537cc14ed
SNAP=/workspace/hf_cache/hub/models--Aleph-Alpha--Kolibri-1/snapshots/$REV
LENS=cache/$KEY/lenses/jpp/Kolibri-1_jpp_lens.pt
LENSP=cache/$KEY-pooled/lenses/jpp/Kolibri-1_pooled_lens.pt
DEV=jsuite_v1_facts_dev_chat; SET=jsuite_v1_facts_test_chat
WORDS="PP PK PM PA MP MK MM MA TP TK TM TA"
BANDS="0-6 3-9 6-12 9-15 12-18 15-21 18-24 21-27 24-30 27-33 30-36 33-39 36-42 39-45 42-48"
BANDFILE=/workspace/scratch/${P}band.txt; GATEFILE=/workspace/scratch/${P}gate.txt
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }

fitk() {
  [ -f "$LENS" ] && { echo "=== $KEY lens exists"; return 0; }
  local g out=/workspace/ext/${KEY}_fit log=/workspace/scratch/${KEY}_fit.log rows ok=0 t0 sha shap ROWS=""
  local L; L=$(seq -s, 0 48)
  local C="env PYTHONPATH=$JPPK/src $KPY scripts/jpp_cli.py"
  local M="--hf-model-name $SNAP --device-map auto --dequantize-fp8 --attn-implementation sdpa"  # bf16, both GPUs
  local MF="--hf-model-name $SNAP --attn-implementation sdpa"                                   # FP8, one GPU
  local S="--layers $L --router-path $out/router.pt --shard-idx 0 --num-shards 1 --target-offset -1 --lrp-mode r+moe --max-seq-len 128 --skip-first-n-positions 16"
  if [ ! -f "$out/experts.pt" ]; then
    for g in 0 1; do
      until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((125 * 1024)) ]; do sleep 60; done
    done
    echo "=== both GPUs have 125 GB free $(date -u +%T)"
    export CUDA_VISIBLE_DEVICES=0,1
    mkdir -p "$out" /dev/shm/${KEY}_artifacts
    [ -e "$out/artifacts" ] || ln -s /dev/shm/${KEY}_artifacts "$out/artifacts"
    cd $JPPK
    echo "=== $KEY router $(date -u +%T)"
    [ -f "$out/router.pt" ] || { $C fit-router $M --layers "$L" --num-prompts 64 --skip-first-n-positions 16 --max-seq-len 128 --seed 0 \
      --out "$out/router.tmp.pt" > $log 2>&1 && mv "$out/router.tmp.pt" "$out/router.pt" || { echo "=== $KEY router FAILED"; tail -5 $log; cd /workspace/bridge-jspace; return 1; }; }
    # Rows per pass only batches the Jacobian's rows (the prompt replicated along the batch axis): same result, other
    # memory and speed (each backward walks the per-expert loop's whole graph once, so fewer, wider passes are faster).
    for rows in 128 64 32; do
      echo "=== $KEY smoke: 1 prompt, $rows rows per pass $(date -u +%T)"
      t0=$(date +%s)
      if $C fit-shard $M $S --num-prompts 1 --jacobian-rows-per-pass $rows --checkpoint-every-n-prompts 1 --artifacts-base-dir "$out/artifacts" \
        --checkpoint-name smoke$rows >> $log 2>&1; then
        echo "=== $KEY smoke $rows rows: $(( $(date +%s) - t0 )) s with the load, $(grep -a "prompt 1/1" $log | tail -1 | grep -oE "[0-9]+s$") for the prompt"
        ROWS=$rows; rm -rf "$out"/artifacts/*/smoke$rows; break
      fi
      echo "=== $KEY smoke $rows rows failed ($(grep -a -oiE "out of memory|RuntimeError: [^ ]+ [^ ]+ [^ ]+" $log | tail -1))"
      rm -rf "$out"/artifacts/*/smoke$rows
    done
    [ -n "$ROWS" ] || { echo "=== $KEY smoke FAILED at every width"; cd /workspace/bridge-jspace; return 1; }
    for rows in $ROWS $(( ROWS / 2 )); do
      [ $rows -ge 16 ] || continue
      echo "=== $KEY fit-shard (64 prompts), $rows rows per pass $(date -u +%T)"
      $C fit-shard $M $S --num-prompts 64 --jacobian-rows-per-pass $rows --checkpoint-every-n-prompts 8 --artifacts-base-dir "$out/artifacts" \
        --checkpoint-name fit64 >> $log 2>&1 && { ok=1; break; }
      echo "=== $KEY $rows rows failed ($(grep -a -oiE "out of memory|No space left|RuntimeError: [^ ]+ [^ ]+ [^ ]+" $log | tail -1))"
      rm -rf "$out"/artifacts/*/fit64
    done
    [ $ok = 1 ] || { echo "=== $KEY fit FAILED"; cd /workspace/bridge-jspace; return 1; }
    echo "=== $KEY merge $(date -u +%T)"
    $C merge-experts --checkpoint-dirs $(ls -d "$out"/artifacts/*/fit64/shard0of* | tail -1) --out "$out/experts.pt" --pooled-lens-out "$out/pooled_lens.pt" \
      --device cpu >> $log 2>&1 || { echo "=== $KEY merge FAILED"; tail -5 $log; cd /workspace/bridge-jspace; return 1; }
    rm -rf "$out"/artifacts/*/fit64
    cd /workspace/bridge-jspace
  fi
  touch /workspace/scratch/${P}gpu1_free  # the bf16 part is over: GPU 1 is free for the next queue
  export CUDA_VISIBLE_DEVICES=0
  cd $JPPK
  echo "=== $KEY grade, readout weights, held-out evaluation (FP8, GPU 0) $(date -u +%T)"
  [ -f "$out/model_correctness.csv" ] || env PYTHONPATH=$JPPK/src $KPY /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py $SNAP "$L" "$out/model_correctness.csv" >> $log 2>&1 \
    || { echo "=== $KEY grade FAILED"; tail -5 $log; cd /workspace/bridge-jspace; return 1; }
  [ -f "$out/Kolibri-1_jpp_lens.pt" ] || $C fit-weights $MF --layers "$L" --experts "$out/experts.pt" --items fit:0 --correctness-csv "$out/model_correctness.csv" \
    --cache-path "$out/readout_cache.pt" --out "$out/Kolibri-1_jpp_lens.pt" >> $log 2>&1 || { echo "=== $KEY fit-weights FAILED"; tail -5 $log; cd /workspace/bridge-jspace; return 1; }
  $C evaluate $MF --layers "$L" --lens "$out/Kolibri-1_jpp_lens.pt" "$out/pooled_lens.pt" logit --items held-out:0 \
    --correctness-csv "$out/model_correctness.csv" --out "$out/eval_ranks.csv" >> $log 2>&1 || echo "=== $KEY evaluate FAILED"
  cd /workspace/bridge-jspace
  mkdir -p cache/$KEY/lenses/jpp cache/$KEY-pooled/lenses/jpp results/lens_fit/$KEY
  local note="on $SNAP (Jacobians on the FP8 checkpoint dequantized to bf16; readout weights on the FP8 model), safety-research/jpp_lens@93f02cd recipe as patched for Kolibri-1 (/workspace/ext/jpp_lens_kol), lrp_mode r+moe, 64 WikiText prompts, layers 0-48, target the final block"
  $PY scripts/lens_fit/export_jpp_lens.py "$out/Kolibri-1_jpp_lens.pt" "$LENS" --note "J++ (weighted) $note" || { echo "=== $KEY export FAILED"; return 1; }
  $PY scripts/lens_fit/export_jpp_lens.py "$out/pooled_lens.pt" "$LENSP" --note "Pooled RelP lens (R-Lens) $note" || { echo "=== $KEY pooled export FAILED"; return 1; }
  cp "$out"/eval_ranks*.csv "$out"/model_correctness.csv "$out"/*stamp*.json results/lens_fit/$KEY/ 2>/dev/null
  local gate
  gate=$(python3 - "$out" <<'PY'
import collections, csv, sys
rows = [r for r in csv.DictReader(open(sys.argv[1] + "/eval_ranks_pass_at_k.csv")) if r["k"] == "10" and r["weighting"] == "item"]
by = collections.defaultdict(list)
for r in rows:
    by[r["lens"]].append(float(r["pass_at_k"]))
print("held-out macro pass@10:", {k: round(sum(v) / len(v), 3) for k, v in by.items()})
PY
)
  echo "=== $KEY $gate"
  sha=$(sha256sum "$LENS" | cut -d" " -f1); shap=$(sha256sum "$LENSP" | cut -d" " -f1)
  .venv/bin/python - "$LENS" "$sha" "$LENSP" "$shap" "$gate" <<'PY' || { echo "=== $KEY pins FAILED"; return 1; }
import sys
from pathlib import Path
lens, sha, lensp, shap, gate = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
i = s.index("    # Aleph-Alpha/Kolibri-1 (Aleph Alpha, 2026-10-03;")
k = s.index('    "kolibri-1": {', i)
j = s.index("\n    },\n", k) + len("\n    },\n")
block, body = s[i:j], s[k:j]
assert body.count('"lenses": {},') == 1 and '"kolibri-1-pooled": {' not in s, block
note = "Registered before its lens (competence needs none); the lens is added once fit and checked."
assert block.count(note) == 1
lensnote = ("Lens: our J++ (Jacobians on the FP8 checkpoint dequantized to bf16, r+moe, 64 WikiText prompts, layers 0-48;\n"
            f"    # readout weights on the FP8 model; scripts/queues/h200_kolfit_1024.sh, amendment 28 note 2). {gate}.")
main = block.replace(note, lensnote).replace(
    '"lenses": {},', f'"lenses": {{"jpp": ("local", "{lens}", "{sha}")}},\n        "frozen_lens_sha256": "{sha}",')
pooled = ("    # Kolibri-1 with the same fit's pooled RelP lens (no expert weighting; the kind of every published neuronpedia\n"
          "    # jpp lens): its secondary lens (amendment 28 note 2).\n"
          + body.replace('"kolibri-1": {', '"kolibri-1-pooled": {').replace('"run_prefix": "kol1_"', '"run_prefix": "kol1p_"')
          .replace('"lenses": {},', f'"lenses": {{"jpp": ("local", "{lensp}", "{shap}")}},\n        "frozen_lens_sha256": "{shap}",'))
assert '"run_prefix": "kol1p_"' in pooled
p.write_text(s[:i] + main + pooled + s[j:])
print("kolibri-1 and kolibri-1-pooled registered", sha, shap)
PY
  git add src/bridge_jspace/pins.py results/lens_fit/$KEY && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
    commit -q -m "pins: kolibri-1 J++ and kolibri-1-pooled (r+moe, 64 prompts, layers 0-48; amendment 28 note 2); $gate

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || { echo "=== $KEY commit FAILED"; return 1; }
  rm -f "$out/experts.pt"
  echo "=== $KEY fit done $(date -u +%T) sha256 $sha (pooled $shap)"
}

for step in "$@"; do
  IFS=: read -r kind a <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    fit) fitk || fails=$((fails + 1)); touch /workspace/scratch/${P}gpu1_free;;
    gate)
      export CUDA_VISIBLE_DEVICES=$a BJ_TARGET=$KEY; t=${P}textloss_top_l15_35_v1
      echo "=== $KEY plain-text gate $(date -u +%T)"
      [ -f results/removal_textloss/$t/summary.json ] || $KPY scripts/removal_textloss.py --name $t --why "$W: $KEY plain-text gate (amendment 28)" \
        --layers $(seq 15 35) --conditions none top10 top10_rot > /workspace/scratch/$t.log 2>&1 || { fail "$KEY gate" /workspace/scratch/$t.log; continue; }
      python3 - results/removal_textloss/$t/summary.json > $GATEFILE <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))["mean_nll"]
d, dr = m["top10"] - m["none"], m["top10_rot"] - m["none"]
print("UNTESTABLE" if d >= 2 and abs(dr) <= 0.3 else "PASS", f"none {m['none']:.2f} nats, top10 {d:+.2f}, top10_rot {dr:+.2f}")
PY
      echo "=== KOLGATE $(cat $GATEFILE)";;
    check)
      export CUDA_VISIBLE_DEVICES=$a BJ_TARGET=$KEY
      echo "=== $KEY lens check $(date -u +%T)"
      $KPY scripts/lens_agreement.py --name ${P}lens_agreement_v1 --why "$W: $KEY, our J++, lens check" > /workspace/scratch/${KEY}_agree.log 2>&1 \
        || fail "$KEY lens check" /workspace/scratch/${KEY}_agree.log
      grep -a -E "nats; chat|^  layer (12|24|36|42|48):" /workspace/scratch/${KEY}_agree.log | sed "s/^/=== KOLAGREE /";;
    dev)
      export CUDA_VISIBLE_DEVICES=$a BJ_TARGET=$KEY
      grep -qs "^UNTESTABLE" $GATEFILE && { echo "=== $KEY dev: skipped, untestable by the gate"; continue; }
      cn=${P}${DEV}_competence_cand2_v1; sw=${P}${DEV}_sweep_cand2_v1
      if [ ! -f results/tasks_v2/$cn/summary.json ]; then
        echo "=== competence $cn $(date -u +%T)"
        $KPY scripts/natural_v1.py competence --set $DEV --name $cn --read cand2 --hop1 gen --why "$W: $KEY on $DEV" > /workspace/scratch/$cn.log 2>&1 \
          || { fail "$KEY dev competence" /workspace/scratch/$cn.log; continue; }
      fi
      echo "=== ablate_v2/$sw $(date -u +%T)"
      [ -f results/ablate_v2/$sw/summary.json ] || $KPY scripts/ablate_v2.py --name $sw --why "$W: $KEY band sweep on the dev split" --plan bands --bands $BANDS \
        --conditions paper10 paper10_rot --tasks $DEV --tasks-competence $cn --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean \
        --batch 32 --read cand2 > /workspace/scratch/$sw.log 2>&1 || { fail "$KEY dev sweep" /workspace/scratch/$sw.log; continue; }
      $KPY scripts/choose_band.py $sw > /workspace/scratch/${sw}_band.txt 2>&1 || { fail "$KEY choose_band" /workspace/scratch/${sw}_band.txt; continue; }
      tail -1 /workspace/scratch/${sw}_band.txt > $BANDFILE
      echo "=== DEVBAND $KEY: $(cat $BANDFILE)";;
    test|testp)
      export CUDA_VISIBLE_DEVICES=$a
      grep -qs "^UNTESTABLE" $GATEFILE && { echo "=== $KEY $kind: skipped, untestable by the gate"; continue; }
      band=$(cat $BANDFILE 2>/dev/null)
      [[ "$band" =~ ^[0-9]+-[0-9]+$ ]] || { echo "=== $KEY $kind: no dev band ('$band')"; fails=$((fails + 1)); continue; }
      if [ $kind = test ]; then export BJ_TARGET=$KEY; p=$P; else export BJ_TARGET=$KEY-pooled; p=kol1p_; fi
      cn=${P}${SET}_competence_cand2_v1; r=${p}${SET}_ko_cand2_v1
      [ -f results/tasks_v2/$cn/summary.json ] || { echo "=== $KEY $kind: no test competence"; fails=$((fails + 1)); continue; }
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $KPY scripts/ablate_v2.py --name $r --why "$W: $BJ_TARGET, fact chains at L$band (dev-chosen)" --plan bands --bands $band \
        --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn --tasks-words $WORDS \
        --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$BJ_TARGET jsuite KO" /workspace/scratch/$r.log; continue; }
      $KPY scripts/jsuite_score.py $r | grep -E "^start (all|P |M |T )" | grep -E "paper10 |paper10_rot |unembed10 " | sed "s/^/=== JS $BJ_TARGET: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== kolfit done, $fails failed $(date -u +%FT%TZ)"
exit $fails
