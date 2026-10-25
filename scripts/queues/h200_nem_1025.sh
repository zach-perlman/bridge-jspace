#!/bin/bash
# Zach (2026-10-25, prereg amendment 40): NVIDIA Nemotron 3.5 Lightning 30B-A3B on v2, at the end of the queue. Download
# once DeepSeek's download and OLMo's cache drop are done (disk); on GPU G once DeepSeek's chain has finished
# (h200nqDS3's nq part; Ministral's chain h200min2 then holds GPU 0): smoke (scripts/new_model_smoke.py + competence
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
[ "$free" -ge 80 ] || [ -d /workspace/hf_cache/hub/models--nvidia--NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16/snapshots/$REV ] || { echo "=== $KEY download: only $free GB free, stopped"; exit 1; }
CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
from huggingface_hub import snapshot_download
print('=== NEMDL done', snapshot_download('$REPO', revision='$REV'))
" 2>&1 | grep -v -E "it/s|Fetching" | tail -2
echo "=== df after: $(df -h /workspace | tail -1 | awk '{print $4}')"
until grep -qs "^EXIT" $R-h200dsdose-1025-1715.log; do sleep 60; done  # 2026-10-25 (amendment 43): after DeepSeek's profile, test, swap and dose chains
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
  ok=0
  for db in 64 32 16; do  # hub kernels (amendment 42); 64 ran out of memory on the torch Mamba scan (amendment 40 note 2)
    echo "=== $KEY J-lens fit, dim_batch $db $(date -u +%T)"
    $PY scripts/lens_fit/fit_jlens.py --repo $REPO --revision $REV --out $LENS --n 200 --no-bos --use-kernels --dim-batch $db > /workspace/scratch/${P}fit.log 2>&1 < /dev/null && { ok=1; break; }
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
o2 = '"frozen_lens_sha256": None,  # set when the Lightning fit is done'
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
# amendment 42: the gate, then the dev depth profile instead of amendment 39's sweep; the test knock-out and swap at the
# profile's pick (written where h200_nq40_1025.sh reads its band), then the swap at mid depth L26-32 (50-62% of 52)
bash scripts/queues/h200_nq40_1025.sh $G $KEY $P gate
bash scripts/queues/h200_profile_1025.sh $G prof:$KEY:$P:16:40
band=$($PY scripts/profile_pick.py ${P}jsuite_v2_dev_chat_profile_cand2_v1 2>/dev/null)
echo "=== NEMPICK $KEY: '$band'"
bash scripts/queues/h200_dose_1025.sh $G dose:$KEY:$P:16:40  # amendment 43: removal sizes at the pick (dev)
[[ "$band" =~ ^[0-9]+-[0-9]+$ ]] && echo "$band" > /workspace/scratch/${P}v2band.txt && bash scripts/queues/h200_nq40_1025.sh $G $KEY $P test swap
r=${P}jswap_v2_L26-32_v1
echo "=== jswap/$r $(date -u +%T)"
[ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "Zach (2026-10-25, prereg amendment 42): $KEY, the swap at mid depth L26-32" \
  --set jsuite_v2_test_chat --band 26-32 --competence ${P}jsuite_v2_test_chat_competence_cand2_v1 --batch 8 > /workspace/scratch/$r.log 2>&1 < /dev/null \
  || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; }
grep -E "^(PM|TM|PN|TN|PK|TK|PP|TP) (swap|remove|swap_rot|swap_u|swap_comp|paste) " /workspace/scratch/$r.log | sed "s/^/=== MIDSWAP $KEY /"
echo "=== nem done $(date -u +%FT%TZ)"
