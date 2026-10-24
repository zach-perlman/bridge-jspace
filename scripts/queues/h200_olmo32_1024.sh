#!/bin/bash
# Zach (2026-10-24, prereg amendment 31): OLMo-3 32B base (allenai/Olmo-3-1125-32B@c2b61da; dense, 64 blocks, Apache-2.0)
# with its published J++ (neuronpedia/jacobian-lens@e166deb, by Ayonrinde & Lindsey: rlens, 64 WikiText prompts, target
# layer 63, recall@10 50.0%) on module 1 in raw-text framing (a base model takes no chat template; the 9B's base vs instruct
# result says the dependence is mostly a pretraining property). The plain J-lens of the same repo is the secondary lens
# (target olmo-3-32b-jlens). Steps: reg (pins entries, lens sha256s, BOS from the tokenizer, as the J++ fit prepended it),
# gate (removal_textloss, top10 vs rotated, layers 20-44), dev (competence + band sweep on jsuite_v1_facts_dev_qa, windows
# of 9 by 4 as the 27B, choose_band), test (competence + knock-out at the dev band, paper10 / rot / unembed10 / rot, 12
# words, jsuite_score), testj (the plain J-lens at the same band).
# Usage: h200_olmo32_1024.sh GPU STEP ...   waitq:JOB  reg  gate  dev  test  testj
set -u
G=$1; shift
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-24, prereg amendment 31)"
KEY=olmo-3-32b; P=olmo32_; KEYJ=olmo-3-32b-jlens; PJ=olmo32j_
DEV=jsuite_v1_facts_dev_qa; SET=jsuite_v1_facts_test_qa
WORDS="PP PK PM PA MP MK MM MA TP TK TM TA"
BANDS="0-8 4-12 8-16 12-20 16-24 20-28 24-32 28-36 32-40 36-44 40-48 44-52 48-56 52-60"
BANDFILE=/workspace/scratch/${P}band.txt; GATEFILE=/workspace/scratch/${P}gate.txt
fails=0
fail() { echo "=== $1 FAILED"; tail -3 "$2"; fails=$((fails + 1)); }
for step in "$@"; do
  IFS=: read -r kind a <<< "$step"
  case $kind in
    waitq) until grep -qs "^EXIT" $R-$a.log; do sleep 60; done; echo "=== $a finished $(date -u +%T)";;
    reg)
      grep -q "\"$KEY\": {" src/bridge_jspace/pins.py && { echo "=== $KEY registered already"; continue; }
      .venv/bin/python - <<'PY' || { echo "=== $KEY reg FAILED"; fails=$((fails + 1)); continue; }
import hashlib, json
from pathlib import Path
from huggingface_hub import hf_hub_download
from transformers import AutoConfig, AutoTokenizer
REPO, REV, LREV = "allenai/Olmo-3-1125-32B", "c2b61dae89a1ad10e4ad5653d0e46b590902607b", "e166deb5ad540932100ef803c8c9bcc2a5453694"
cfg = AutoConfig.from_pretrained(REPO, revision=REV)
tok = AutoTokenizer.from_pretrained(REPO, revision=REV)
bos = tok.bos_token_id is not None
print("config:", cfg.model_type, cfg.num_hidden_layers, cfg.hidden_size, "| bos", tok.bos_token, tok.bos_token_id, "| add_bos", getattr(tok, "add_bos_token", None))
assert cfg.num_hidden_layers == 64
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()
fj = "olmo-3-1125-32b/jpp/Salesforce-wikitext/Olmo-3-1125-32B_jpp_lens.pt"
fl = "olmo-3-1125-32b/jlens/Salesforce-wikitext/Olmo-3-1125-32B_jacobian_lens.pt"
sj, sl = sha(hf_hub_download("neuronpedia/jacobian-lens", fj, revision=LREV)), sha(hf_hub_download("neuronpedia/jacobian-lens", fl, revision=LREV))
p = Path("src/bridge_jspace/pins.py"); s = p.read_text()
anchor = '    "qwen3-32b-jlens": {'
assert s.count(anchor) == 1 and '"olmo-3-32b": {' not in s
block = f'''    # allenai/Olmo-3-1125-32B (OLMo 3 32B base, Ai2, 2025-11; dense, 64 blocks, sliding-window and full attention,
    # post-norm sublayers; Apache-2.0): the non-Qwen dense model with a published J++ by the J++ authors (Ayonrinde &
    # Lindsey; neuronpedia recall@10 50.0%; rlens, 64 WikiText prompts, target layer 63), prereg amendment 31 (Zach,
    # 2026-10-24). A base model: module 1 in raw-text framing. BOS as the tokenizer defines it (the J++ fit prepended it).
    "olmo-3-32b": {{
        "repo": "{REPO}",
        "revision": "{REV}",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": {bos},
        "run_prefix": "olmo32_",
        "lenses": {{"jpp": (LENS_REPO, "{fj}", "{LREV}")}},
        "frozen_lens_sha256": "{sj}",
    }},
    # The same model with the plain J-lens of the same repo (the paper's own lens): the secondary lens (amendment 31).
    "olmo-3-32b-jlens": {{
        "repo": "{REPO}",
        "revision": "{REV}",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": {bos},
        "run_prefix": "olmo32j_",
        "frozen_lens": "jlens",
        "lenses": {{"jlens": (LENS_REPO, "{fl}", "{LREV}")}},
        "frozen_lens_sha256": "{sl}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("=== OLMOREG registered olmo-3-32b and olmo-3-32b-jlens; bos", bos, "jpp", sj[:12], "jlens", sl[:12])
PY
      git add src/bridge_jspace/pins.py scripts/queues/h200_olmo32_1024.sh && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
        commit -q -m "pins: olmo-3-32b (published J++) and olmo-3-32b-jlens (amendment 31)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || echo "=== $KEY commit FAILED";;
    gate)
      export BJ_TARGET=$KEY; t=${P}textloss_top_l20_44_v1
      echo "=== $KEY plain-text gate $(date -u +%T)"
      [ -f results/removal_textloss/$t/summary.json ] || $PY scripts/removal_textloss.py --name $t --why "$W: $KEY plain-text gate" \
        --layers $(seq 20 44) --conditions none top10 top10_rot > /workspace/scratch/$t.log 2>&1 || { fail "$KEY gate" /workspace/scratch/$t.log; continue; }
      python3 - results/removal_textloss/$t/summary.json > $GATEFILE <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))["mean_nll"]
d, dr = m["top10"] - m["none"], m["top10_rot"] - m["none"]
print("UNTESTABLE" if d >= 2 and abs(dr) <= 0.3 else "PASS", f"none {m['none']:.2f} nats, top10 {d:+.2f}, top10_rot {dr:+.2f}")
PY
      echo "=== OLMOGATE $(cat $GATEFILE)";;
    dev)
      export BJ_TARGET=$KEY
      cn=${P}${DEV}_competence_cand2_v1; sw=${P}${DEV}_sweep_cand2_v1
      if [ ! -f results/tasks_v2/$cn/summary.json ]; then
        echo "=== competence $cn $(date -u +%T)"
        $PY scripts/natural_v1.py competence --set $DEV --name $cn --read cand2 --hop1 gen --why "$W: $KEY on $DEV" > /workspace/scratch/$cn.log 2>&1 \
          || { fail "$KEY dev competence" /workspace/scratch/$cn.log; continue; }
      fi
      python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== OLMODEVCOMP whole:', {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$cn/summary.json
      echo "=== ablate_v2/$sw $(date -u +%T)"
      [ -f results/ablate_v2/$sw/summary.json ] || $PY scripts/ablate_v2.py --name $sw --why "$W: $KEY band sweep on the dev split" --plan bands --bands $BANDS \
        --conditions paper10 paper10_rot --tasks $DEV --tasks-competence $cn --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean \
        --batch 32 --read cand2 > /workspace/scratch/$sw.log 2>&1 || { fail "$KEY dev sweep" /workspace/scratch/$sw.log; continue; }
      $PY scripts/choose_band.py $sw > /workspace/scratch/${sw}_band.txt 2>&1 || { fail "$KEY choose_band" /workspace/scratch/${sw}_band.txt; continue; }
      tail -1 /workspace/scratch/${sw}_band.txt > $BANDFILE
      echo "=== DEVBAND $KEY: $(cat $BANDFILE)";;
    test|testj)
      band=$(cat $BANDFILE 2>/dev/null)
      [[ "$band" =~ ^[0-9]+-[0-9]+$ ]] || { echo "=== $KEY $kind: no dev band ('$band')"; fails=$((fails + 1)); continue; }
      if [ $kind = test ]; then export BJ_TARGET=$KEY; p=$P; else export BJ_TARGET=$KEYJ; p=$PJ; fi
      cn=${P}${SET}_competence_cand2_v1; r=${p}${SET}_ko_cand2_v1
      if [ ! -f results/tasks_v2/$cn/summary.json ]; then
        echo "=== competence $cn $(date -u +%T)"
        BJ_TARGET=$KEY $PY scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen --why "$W: $KEY on $SET" > /workspace/scratch/$cn.log 2>&1 \
          || { fail "$KEY test competence" /workspace/scratch/$cn.log; continue; }
      fi
      python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== OLMOCOMP whole:', {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$cn/summary.json
      echo "=== ablate_v2/$r at L$band $(date -u +%T)"
      [ -f results/ablate_v2/$r/summary.json ] || $PY scripts/ablate_v2.py --name $r --why "$W: $BJ_TARGET, fact chains in raw text at L$band (dev-chosen)" --plan bands \
        --bands $band --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $SET --tasks-competence $cn --tasks-words $WORDS \
        --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2 > /workspace/scratch/$r.log 2>&1 || { fail "$BJ_TARGET jsuite KO" /workspace/scratch/$r.log; continue; }
      $PY scripts/jsuite_score.py $r --set $SET | grep -E "^start (all|P |M |T )" | grep -E "paper10 |paper10_rot |unembed10 " | sed "s/^/=== JS $BJ_TARGET: /";;
    *) echo "=== unknown step $step"; fails=$((fails + 1));;
  esac
done
echo "=== olmo32 GPU $G done, $fails failed $(date -u +%FT%TZ)"
exit $fails
