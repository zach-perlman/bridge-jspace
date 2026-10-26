#!/bin/bash
# Amendment 40 (2026-10-25): h200_nq_1025.sh as committed in 4d21b30, its --why strings marked amendment 40 (a copy, so the chains
# running h200_nq_1025.sh are not edited under them).
# Zach (2026-10-25, prereg amendment 39): the non-Qwen families on the combined suite v2, OLMo's procedure (amendment 31,
# h200_olmo32_1024.sh) moved to v2: gate (removal_textloss, top10 vs rotated, the middle of the lens's layers), dev
# (competence on the facts words of jsuite_v2_dev_chat + a band sweep, windows 9/64 of the depth wide sliding by 4/64
# inside the lens's layers, PP PM MP MM, choose_band), test (competence on the facts words of jsuite_v2_test_chat + the
# knock-out at the dev band, paper10 / rot / unembed10 / rot, the 15 facts words, jsuite2_score), swap (jswap, its six
# conditions, + bridge_readout + jswap_by_relation at the dev band).
# Usage: h200_nq_1025.sh GPUS KEY PREFIX STEP ...   (GPUS e.g. 0 or 0,1)   STEP: waitq:JOB  mem:GB  gate  dev  test  swap
set -u
G=$1; KEY=$2; P=$3; shift 3
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G BJ_TARGET=$KEY
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-25, prereg amendment 40)"
DEV=jsuite_v2_dev_chat; SET=jsuite_v2_test_chat
FACTS="PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN"
BANDFILE=/workspace/scratch/${P}v2band.txt; GATEFILE=/workspace/scratch/${P}v2gate.txt
# windows inside the lens's source layers: width round(9/64 n), step round(4/64 n); gate layers: the middle 31-69% of them
read -r BANDS GATEL <<< "$($PY - <<'PY'
import sys
sys.path.insert(0, "src")
import torch
from bridge_jspace import pins
from huggingface_hub import hf_hub_download
n = pins.N_LAYERS
s0 = pins.LENS_SOURCES[pins.FROZEN_LENS]
path = pins.REPO_ROOT / s0[1] if s0[0] == "local" else hf_hub_download(s0[0], s0[1], revision=s0[2])
src = sorted(int(x) for x in torch.load(path, map_location="cpu", weights_only=True, mmap=True)["source_layers"])
lo, hi = src[0], src[-1]
w, s = max(2, round(9 / 64 * n)), max(1, round(4 / 64 * n))
bands = [f"{a}-{a + w - 1}" for a in range(lo, hi - w + 2, s)]
g = [x for x in src if 0.31 * n <= x <= 0.69 * n]
print("|".join(bands), f"{g[0]}-{g[-1]}")
PY
)"
BANDS=${BANDS//|/ }
echo "=== $KEY bands: $BANDS | gate layers: $GATEL"
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    mem) for g in ${G//,/ }; do until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge $((a * 1024)) ]; do sleep 60; done; done
      echo "=== GPUs $G have $a GB free each $(date -u +%T)";;
    gate)
      t=${P}textloss_top_v2gate_v1; lo=${GATEL%-*}; hi=${GATEL#*-}
      echo "=== $KEY plain-text gate, layers $GATEL $(date -u +%T)"
      [ -f results/removal_textloss/$t/summary.json ] || $PY scripts/removal_textloss.py --name $t --why "$W: $KEY plain-text gate" \
        --layers $(seq $lo $hi) --conditions none top10 top10_rot > /workspace/scratch/$t.log 2>&1 || { fail "$KEY gate" /workspace/scratch/$t.log; continue; }
      python3 - results/removal_textloss/$t/summary.json > $GATEFILE <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))["mean_nll"]
d, dr = m["top10"] - m["none"], m["top10_rot"] - m["none"]
print("UNTESTABLE" if d >= 2 and abs(dr) <= 0.3 else "PASS", f"none {m['none']:.2f} nats, top10 {d:+.2f}, top10_rot {dr:+.2f}")
PY
      echo "=== NQGATE $KEY $(cat $GATEFILE)";;
    dev)
      grep -q "^UNTESTABLE" $GATEFILE 2>/dev/null && { echo "=== $KEY untestable by the gate; dev skipped"; continue; }
      cn=${P}${DEV}_competence_cand2_v1; sw=${P}${DEV}_sweep_cand2_v1
      echo "=== competence $cn $(date -u +%T)"
      [ -f results/tasks_v2/$cn/summary.json ] || $PY scripts/natural_v1.py competence --set $DEV --name $cn --read cand2 --hop1 gen --words $FACTS \
        --why "$W: $KEY on $DEV" > /workspace/scratch/$cn.log 2>&1 || { fail "$KEY dev competence" /workspace/scratch/$cn.log; continue; }
      python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== NQDEVCOMP', sys.argv[2], {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$cn/summary.json $KEY
      echo "=== ablate_v2/$sw $(date -u +%T)"
      [ -f results/ablate_v2/$sw/summary.json ] || $PY scripts/ablate_v2.py --name $sw --why "$W: $KEY band sweep on the dev split" --plan bands --bands $BANDS \
        --conditions paper10 paper10_rot --tasks $DEV --tasks-competence $cn --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean \
        --batch 16 --read cand2 > /workspace/scratch/$sw.log 2>&1 || { fail "$KEY dev sweep" /workspace/scratch/$sw.log; continue; }
      $PY scripts/choose_band.py $sw > /workspace/scratch/${sw}_band.txt 2>&1 || { fail "$KEY choose_band" /workspace/scratch/${sw}_band.txt; continue; }
      tail -1 /workspace/scratch/${sw}_band.txt > $BANDFILE
      echo "=== NQDEVBAND $KEY: $(cat $BANDFILE)";;
    test|swap)
      band=$(cat $BANDFILE 2>/dev/null)
      [[ "$band" =~ ^[0-9]+-[0-9]+$ ]] || { echo "=== $KEY $kind: no dev band ('$band')"; fails=$((fails + 1)); continue; }
      cn=${P}${SET}_competence_cand2_v1
      if [ ! -f results/tasks_v2/$cn/summary.json ]; then
        echo "=== competence $cn $(date -u +%T)"
        $PY scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen --words $FACTS --why "$W: $KEY on $SET" > /workspace/scratch/$cn.log 2>&1 \
          || { fail "$KEY test competence" /workspace/scratch/$cn.log; continue; }
        python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== NQCOMP', sys.argv[2], {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$cn/summary.json $KEY
      fi
      S=$(cat /workspace/scratch/${P}sample.txt 2>/dev/null); SA=""  # amendment 49: a seeded random N per word if the file holds N
      [[ "$S" =~ ^[0-9]+$ ]] && SA="--sample-per-word $S --sample-seed 0" && echo "=== $KEY $kind: $S items per word (seed 0)"
      if [ $kind = test ]; then
        r=${P}${SET}_ko_cand2_v1
        echo "=== ablate_v2/$r at L$band $(date -u +%T)"
        [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $KEY, v2 facts at L$band (dev-chosen)" --plan bands \
          --bands $band --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn --tasks-words $FACTS \
          --tasks-level all --n 1000 --kinds clean --batch 16 --read cand2 $SA > /workspace/scratch/$r.log 2>&1 || { fail "$KEY v2 KO" /workspace/scratch/$r.log; continue; }
        $PY scripts/jsuite2_score.py $r --set $SET --by-relation | grep -E "^facts (paper10|unembed10|paper10_rot|unembed10_rot) +(start=|half=)" | sed "s/^/=== NQV2 $KEY: /"
      else
        r=${P}jswap_v2_v1; rb=${P}bridge_readout_v2_v1
        echo "=== jswap/$r at L$band $(date -u +%T)"
        [ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "$W: $KEY on v2 at L$band (dev-chosen)" --set $SET --band $band \
          --competence $cn --batch 8 $SA > /workspace/scratch/$r.log 2>&1 || { fail "$KEY jswap" /workspace/scratch/$r.log; continue; }
        grep -E "^(PM|TM|PN|TN|PK|TK|PP|TP) (swap|remove|swap_rot|swap_u|swap_comp|paste) " /workspace/scratch/$r.log | sed "s/^/=== NQSWAP $KEY /"
        $PY scripts/jswap_by_relation.py $r --set $SET | grep -v -i warn | sed "s/^/=== NQSWAPREL $KEY /"
        [ -f results/bridge_readout/$rb/summary.json ] || $PY scripts/bridge_readout.py --name $rb --set $SET --competence $cn --batch 8 \
          > /workspace/scratch/$rb.log 2>&1 || { fail "$KEY readout" /workspace/scratch/$rb.log; continue; }
        grep -E "^L" /workspace/scratch/$rb.log | sed "s/^/=== NQREAD $KEY /"
      fi;;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== nq $KEY done, $fails failed $(date -u +%FT%TZ)"
exit $fails
