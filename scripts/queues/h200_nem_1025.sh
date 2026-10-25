#!/bin/bash
# Zach (2026-10-25, prereg amendment 40): NVIDIA Nemotron 3.5 Lightning 30B-A3B on v2, at the end of the queue. Download
# once DeepSeek's download and OLMo's cache drop are done (disk); on GPU G once DeepSeek's chain has finished
# (h200nqDS's first script; Ministral's test and swap then hold GPU 0): smoke (scripts/new_model_smoke.py + competence
# on the first 120 dev items; stop if the unembed check's top-1 differs or plain-text NLL >= 4 nats); our plain J-lens
# (scripts/lens_fit/fit_jlens.py: Anthropic's jlens, 500 WikiText prompts, --no-bos), its sha256 into pins, commit,
# lens check; then amendment 39's procedure (h200_nq40_1025.sh): gate, dev, test, swap. Usage: h200_nem_1025.sh GPU
set -u
G=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
KEY=nemotron-3.5-lightning; P=nem35l_
REPO=nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16; REV=a9904d24bcc1d289a1950fa9d2b978c47cf903b9
LENS=cache/$KEY/lenses/jlens/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jlens.pt
export BJ_TARGET=$KEY
echo "=== start $(date -u +%FT%TZ)"
for j in dsdisk-1025-0505 olmodrop-1025-0505; do until grep -qs "^EXIT" $R-$j.log; do sleep 60; done; done
free=$(df -BG --output=avail /workspace | tail -1 | tr -dc 0-9)
echo "=== $KEY download, $free GB free $(date -u +%T)"
[ "$free" -ge 80 ] || { echo "=== $KEY download: only $free GB free, stopped"; exit 1; }
CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
from huggingface_hub import snapshot_download
print('=== NEMDL done', snapshot_download('$REPO', revision='$REV'))
" 2>&1 | grep -v -E "it/s|Fetching" | tail -2
echo "=== df after: $(df -h /workspace | tail -1 | awk '{print $4}')"
until grep -qs "=== nq deepseek-v4-flash done\|^EXIT" $R-h200nqDS-1025-0505.log; do sleep 60; done
until [ "$(nvidia-smi -i $G --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 100000 ]; do sleep 60; done
echo "=== GPU $G free after DeepSeek $(date -u +%T)"
$PY scripts/new_model_smoke.py > /workspace/scratch/${P}smoke.log 2>&1 || { echo "=== $KEY smoke FAILED"; tail -5 /workspace/scratch/${P}smoke.log; exit 1; }
verdict=$(python3 - results/checks/${P}smoke.json <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
ok = s["unembed"]["top1_same"] and s["wikitext_nll"]["as_harness"] < 4
print("PASS" if ok else "STOP", json.dumps({k: s[k] for k in ("final_norm", "unembed", "wikitext_nll")}), "greedy:", repr(s["chat"]["greedy"]))
PY
)
echo "=== NEMSMOKE $KEY $verdict"
[[ $verdict == PASS* ]] || exit 1
sm=${P}jsuite_v2_dev_chat_competence_smoke_1025
[ -f results/tasks_v2/$sm/summary.json ] || $PY scripts/natural_v1.py competence --set jsuite_v2_dev_chat --name $sm --read cand2 --hop1 gen --limit 120 \
  --why "Zach (2026-10-25, prereg amendment 40): $KEY smoke, first 120 dev items" > /workspace/scratch/$sm.log 2>&1 || { echo "=== $KEY smoke competence FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== NEMSMOKECOMP', {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$sm/summary.json
if [ ! -f $LENS ]; then
  echo "=== $KEY J-lens fit $(date -u +%T)"
  $PY scripts/lens_fit/fit_jlens.py --repo $REPO --revision $REV --out $LENS --n 500 --no-bos > /workspace/scratch/${P}fit.log 2>&1 \
    || { echo "=== $KEY fit FAILED"; tail -5 /workspace/scratch/${P}fit.log; exit 1; }
  grep FIT_DONE /workspace/scratch/${P}fit.log | sed "s/^/=== /"
  sha=$(sha256sum $LENS | cut -d" " -f1)
  .venv/bin/python - "$LENS" "$sha" <<'PY' || { echo "=== $KEY pins FAILED"; exit 1; }
import sys
from pathlib import Path
lens, sha = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
o1 = f'"lenses": {{"jlens": ("local", "{lens}", None)}},'
o2 = '"frozen_lens_sha256": None,  # set when the fit is done'
assert s.count(o1) == 1 and s.count(o2) == 1, "the Lightning entry's placeholders"
s = s.replace(o1, f'"lenses": {{"jlens": ("local", "{lens}", "{sha}")}},  # our plain J-lens (h200_nem_1025.sh)')
s = s.replace(o2, f'"frozen_lens_sha256": "{sha}",')
p.write_text(s)
print("lens registered", sha[:12])
PY
  git add src/bridge_jspace/pins.py && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com commit -q -m "pins: $KEY, our plain J-lens (500 prompts, amendment 40)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- src/bridge_jspace/pins.py || { echo "=== $KEY commit FAILED"; exit 1; }
  $PY scripts/lens_agreement.py --name ${P}lens_agreement_v1 --why "Zach (2026-10-25, amendment 40): $KEY, our plain J-lens, lens check" \
    > /workspace/scratch/${P}agree.log 2>&1 || echo "=== $KEY lens check FAILED"
  echo "=== $KEY fit done $(date -u +%T)"
fi
bash scripts/queues/h200_nq40_1025.sh $G $KEY $P gate dev test swap
