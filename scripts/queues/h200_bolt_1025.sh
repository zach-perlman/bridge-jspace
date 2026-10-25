#!/bin/bash
# Zach (2026-10-25, prereg amendment 40 note 1): NVIDIA Nemotron 3.5 Bolt 74B-A9B on v2, last in the queue, on GPUs 0,1.
# Disk (Zach's approval): once DeepSeek's chain (h200nqDS's first script) has finished with 0 failures, DeepSeek's cache
# is dropped (scratch/cache_drop.py; its lens is kept); with failures, the cache is kept and the chain stops. Then Bolt's
# download (stop if under 160 GB free); once DeepSeek's, Ministral's and Lightning's chains have
# exited: smoke (new_model_smoke + competence on the first 120 dev items; stop if the unembed's top-1 differs or plain-text
# NLL >= 4 nats), our plain J-lens (fit_jlens --harness: NVIDIA's language model as the harness loads it, over two GPUs;
# 500 WikiText prompts, --no-bos; dim_batch 64, else 32), its sha256 into pins, commit, lens check; then h200_nq40_1025.sh
# gate, dev, test, swap. Usage: h200_bolt_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
KEY=nemotron-3.5-bolt; P=nem35b_
REPO=nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16; REV=e09a4cedb1787db1760375ee5539f222cae0c672
LENS=cache/$KEY/lenses/jlens/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16_jlens.pt
DS=$R-h200nqDS3-1025-0900.log
export BJ_TARGET=$KEY
echo "=== start $(date -u +%FT%TZ)"
until grep -qs "=== nq deepseek-v4-flash done\|^EXIT" $DS; do sleep 60; done
if grep -qs "=== nq deepseek-v4-flash done, 0 failed" $DS; then
  echo "=== DeepSeek chain done with 0 failures $(date -u +%T); df before: $(df -h /workspace | tail -1 | awk '{print $4}')"
  [ -d /workspace/hf_cache/hub/models--deepseek-ai--DeepSeek-V4-Flash ] && python3 /workspace/scratch/cache_drop.py models--deepseek-ai--DeepSeek-V4-Flash
  echo "=== df after: $(df -h /workspace | tail -1 | awk '{print $4}')"
else
  echo "=== BOLT HOLD: DeepSeek's chain did not finish with 0 failures ($(grep -a "=== nq deepseek-v4-flash done" $DS | tail -1)); its cache is kept, Bolt stopped"
  exit 1
fi
free=$(df -BG --output=avail /workspace | tail -1 | tr -dc 0-9)
echo "=== $KEY download, $free GB free $(date -u +%T)"
[ "$free" -ge 160 ] || { echo "=== $KEY download: only $free GB free, stopped"; exit 1; }
CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
from huggingface_hub import snapshot_download
print('=== BOLTDL done', snapshot_download('$REPO', revision='$REV'))
" 2>&1 | grep -v -E "it/s|Fetching" | tail -2
echo "=== df after: $(df -h /workspace | tail -1 | awk '{print $4}')"
for j in h200nqDS3-1025-0900 h200min3-1025-0920 h200nemL5-1025-1600; do until grep -qs "^EXIT" $R-$j.log; do sleep 60; done; done
for g in 0 1; do until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 120000 ]; do sleep 60; done; done
echo "=== GPUs 0,1 free $(date -u +%T)"
$PY scripts/new_model_smoke.py > /workspace/scratch/${P}smoke.log 2>&1 < /dev/null || { echo "=== $KEY smoke FAILED"; tail -5 /workspace/scratch/${P}smoke.log; exit 1; }
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
  --why "Zach (2026-10-25, prereg amendment 40 note 1): $KEY smoke, first 120 dev items" > /workspace/scratch/$sm.log 2>&1 < /dev/null || { echo "=== $KEY smoke competence FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== NEMSMOKECOMP', {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$sm/summary.json
if [ ! -f $LENS ]; then
  ok=0
  for db in 64 32; do
    echo "=== $KEY J-lens fit, dim_batch $db $(date -u +%T)"
    $PY scripts/lens_fit/fit_jlens.py --harness --repo $REPO --revision $REV --out $LENS --n 500 --no-bos --dim-batch $db > /workspace/scratch/${P}fit.log 2>&1 < /dev/null && { ok=1; break; }
    echo "=== $KEY fit at dim_batch $db failed ($(grep -m1 -oiE "out of memory|RuntimeError: [^ ]+ [^ ]+ [^ ]+" /workspace/scratch/${P}fit.log))"
    grep -qi "out of memory" /workspace/scratch/${P}fit.log || break
    rm -f $LENS.ckpt
  done
  [ $ok = 1 ] || { echo "=== $KEY fit FAILED"; tail -5 /workspace/scratch/${P}fit.log; exit 1; }
  grep FIT_DONE /workspace/scratch/${P}fit.log | sed "s/^/=== /"
  sha=$(sha256sum $LENS | cut -d" " -f1)
  .venv/bin/python - "$LENS" "$sha" <<'PY' || { echo "=== $KEY pins FAILED"; exit 1; }
import sys
from pathlib import Path
lens, sha = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
o1 = f'"lenses": {{"jlens": ("local", "{lens}", None)}},'
o2 = '"frozen_lens_sha256": None,  # set when the Bolt fit is done'
i = s.index('TARGETS["nemotron-3.5-bolt"]')
head, tail = s[:i], s[i:]
assert tail.count(o1) == 1, "the Bolt entry's lens placeholder"
j = tail.index(o2)
assert j > tail.index(o1), "the Bolt entry's sha placeholder"
tail = tail.replace(o1, f'"lenses": {{"jlens": ("local", "{lens}", "{sha}")}},  # our plain J-lens (h200_bolt_1025.sh)', 1)
tail = tail.replace(o2, f'"frozen_lens_sha256": "{sha}",', 1)
p.write_text(head + tail)
print("lens registered", sha[:12])
PY
  git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com commit -q -m "pins: $KEY, our plain J-lens (500 prompts, amendment 40 note 1)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- src/bridge_jspace/pins.py || { echo "=== $KEY commit FAILED"; exit 1; }
  $PY scripts/lens_agreement.py --name ${P}lens_agreement_v1 --why "Zach (2026-10-25, amendment 40 note 1): $KEY, our plain J-lens, lens check" \
    > /workspace/scratch/${P}agree.log 2>&1 < /dev/null || echo "=== $KEY lens check FAILED"
  echo "=== $KEY fit done $(date -u +%T)"
fi
bash scripts/queues/h200_nq40_1025.sh 0,1 $KEY $P gate dev test swap
