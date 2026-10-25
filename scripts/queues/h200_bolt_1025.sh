#!/bin/bash
# Zach (2026-10-25, prereg amendments 40 note 1, 42, 44): NVIDIA Nemotron 3.5 Bolt 74B-A9B on v2, on GPUs 0,1, after
# Lightning. Disk (Zach's approval): DeepSeek's cache is dropped only once its profile chain (h200ds42) and its dose
# chain (h200dsdose) have both ended with 0 failures; else it is kept and this chain stops. Then Bolt's download (stop
# if under 160 GB free). Once Lightning's chain, the 9B renderings and the profiles have exited, these steps:
#   - smoke (new_model_smoke; stop if the unembed's top-1 differs, plain-text NLL >= 4 nats, or a no-op edit changes the
#     logits);
#   - the hub-kernel check (scripts/kernel_nll.py with and without kernels: |mean NLL diff| <= 0.01 and top-1 agreement
#     >= 0.95, else stop);
#   - competence on the first 120 dev items;
#   - our plain J-lens on 100 prompts (the jlens README's "usable"; fit_jlens --harness, --no-bos; dim_batch 64, 32, 16
#     on out-of-memory), its sha256 into pins, commit, lens check;
#   - the gate, the dev depth profile, the dose curve at its pick, the test knock-out and swap at the pick
#     (h200_nq40_1025.sh, its band file), and the swap at mid depth L44-55 (50-62% of 88 blocks).
# Usage: h200_bolt_1025.sh
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0,1
PY="uv run --no-sync python"
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
KEY=nemotron-3.5-bolt; P=nem35b_
REPO=nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16; REV=e09a4cedb1787db1760375ee5539f222cae0c672
LENS=cache/$KEY/lenses/jlens/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16_jlens.pt
DS=$R-h200ds42-1025-1700.log; DD=$R-h200dsdose-1025-1715.log
export BJ_TARGET=$KEY
echo "=== start $(date -u +%FT%TZ)"
until grep -qs "^EXIT" $DS && grep -qs "^EXIT" $DD; do sleep 60; done
if grep -qs "=== nq deepseek-v4-flash done, 0 failed" $DS && grep -qs "=== dsdose done, 0 failed" $DD; then
  echo "=== DeepSeek chains done with 0 failures $(date -u +%T); df before: $(df -h /workspace | tail -1 | awk '{print $4}')"
  [ -d /workspace/hf_cache/hub/models--deepseek-ai--DeepSeek-V4-Flash ] && python3 /workspace/scratch/cache_drop.py models--deepseek-ai--DeepSeek-V4-Flash
  echo "=== df after: $(df -h /workspace | tail -1 | awk '{print $4}')"
else
  echo "=== BOLT HOLD: a DeepSeek chain did not end with 0 failures; its cache is kept, Bolt stopped"; exit 1
fi
free=$(df -BG --output=avail /workspace | tail -1 | tr -dc 0-9)
echo "=== $KEY download, $free GB free $(date -u +%T)"
[ "$free" -ge 160 ] || { echo "=== $KEY download: only $free GB free, stopped"; exit 1; }
CUDA_VISIBLE_DEVICES="" .venv/bin/python -c "
from huggingface_hub import snapshot_download
print('=== BOLTDL done', snapshot_download('$REPO', revision='$REV'))
" 2>&1 | grep -v -E "it/s|Fetching" | tail -2
echo "=== df after: $(df -h /workspace | tail -1 | awk '{print $4}')"
for j in h200nemL7-1025-1715 h200qrend9-1025-1720 h200qprof-1025-1700; do until grep -qs "^EXIT" $R-$j.log; do sleep 60; done; done
for g in 0 1; do until [ "$(nvidia-smi -i $g --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 120000 ]; do sleep 60; done; done
echo "=== GPUs 0,1 free $(date -u +%T)"
$PY scripts/new_model_smoke.py > /workspace/scratch/${P}smoke.log 2>&1 < /dev/null || { echo "=== $KEY smoke FAILED"; tail -5 /workspace/scratch/${P}smoke.log; exit 1; }
verdict=$(python3 - results/checks/${P}smoke.json <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
ok = s["unembed"]["top1_same"] and s["wikitext_nll"]["as_harness"] < 4 and s["noop_edit_max_abs_diff"] == 0
print("PASS" if ok else "STOP", json.dumps({k: s[k] for k in ("final_norm", "unembed", "noop_edit_max_abs_diff", "wikitext_nll", "load_s") if k in s}), "greedy:", repr(s["chat"]["greedy"]))
PY
)
echo "=== NEMSMOKE $KEY $verdict"
[[ $verdict == PASS* ]] || exit 1
$PY scripts/kernel_nll.py /workspace/scratch/${P}knll_kernels.pt > /workspace/scratch/${P}knll.log 2>&1 < /dev/null \
  && BJ_NO_KERNELS=1 $PY scripts/kernel_nll.py /workspace/scratch/${P}knll_torch.pt >> /workspace/scratch/${P}knll.log 2>&1 < /dev/null \
  || { echo "=== $KEY kernel check FAILED"; tail -5 /workspace/scratch/${P}knll.log; exit 1; }
kv=$(.venv/bin/python - /workspace/scratch/${P}knll_kernels.pt /workspace/scratch/${P}knll_torch.pt <<'PY'
import sys, torch
a, b = (torch.load(p) for p in sys.argv[1:])
na, nb = torch.cat(a["nll"]), torch.cat(b["nll"])
agree = (torch.cat(a["top"]) == torch.cat(b["top"])).float().mean().item()
d = na.mean().item() - nb.mean().item()
print("PASS" if abs(d) <= 0.01 and agree >= 0.95 else "STOP", f"nll kernels {na.mean():.4f} torch {nb.mean():.4f} diff {d:+.4f}, top-1 agreement {agree:.4f}")
PY
)
echo "=== KERNELCHECK $KEY $kv"
[[ $kv == PASS* ]] || exit 1
sm=${P}jsuite_v2_dev_chat_competence_smoke_1025
[ -f results/tasks_v2/$sm/summary.json ] || $PY scripts/natural_v1.py competence --set jsuite_v2_dev_chat --name $sm --read cand2 --hop1 gen --limit 120 \
  --why "Zach (2026-10-25, prereg amendment 44): $KEY smoke, first 120 dev items" > /workspace/scratch/$sm.log 2>&1 < /dev/null || { echo "=== $KEY smoke competence FAILED"; tail -5 /workspace/scratch/$sm.log; exit 1; }
python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== NEMSMOKECOMP', {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$sm/summary.json
if [ ! -f $LENS ]; then
  ok=0
  for db in 64 32 16; do
    echo "=== $KEY J-lens fit, dim_batch $db $(date -u +%T)"
    $PY scripts/lens_fit/fit_jlens.py --harness --repo $REPO --revision $REV --out $LENS --n 100 --no-bos --dim-batch $db > /workspace/scratch/${P}fit.log 2>&1 < /dev/null && { ok=1; break; }
    echo "=== $KEY fit at dim_batch $db failed ($(grep -m1 -oiE "out of memory|RuntimeError: [^ ]+ [^ ]+ [^ ]+" /workspace/scratch/${P}fit.log))"
    grep -qi "out of memory" /workspace/scratch/${P}fit.log || break
    rm -f $LENS.ckpt
  done
  [ $ok = 1 ] || { echo "=== $KEY fit FAILED"; tail -5 /workspace/scratch/${P}fit.log; exit 1; }
  grep FIT_DONE /workspace/scratch/${P}fit.log | sed "s/^/=== /"
  grep -a "prompt 100/100" /workspace/scratch/${P}fit.log | sed "s/^/=== FITLAST /"
  sha=$(sha256sum $LENS | cut -d" " -f1)
  .venv/bin/python - "$LENS" "$sha" <<'PY' || { echo "=== $KEY pins FAILED"; exit 1; }
import sys
from pathlib import Path
lens, sha = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
o1 = f'"lenses": {{"jlens": ("local", "{lens}", None)}},'
o2 = '"frozen_lens_sha256": None,  # set when the Bolt fit is done'
assert s.count(o1) == 1 and s.count(o2) == 1, "the Bolt entry's placeholders"
s = s.replace(o1, f'"lenses": {{"jlens": ("local", "{lens}", "{sha}")}},  # our plain J-lens (h200_bolt_1025.sh)')
s = s.replace(o2, f'"frozen_lens_sha256": "{sha}",')
p.write_text(s)
print("lens registered", sha[:12])
PY
  git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com commit -q -m "pins: $KEY, our plain J-lens (100 prompts, amendments 40 note 1 and 44)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- src/bridge_jspace/pins.py || { echo "=== $KEY commit FAILED"; exit 1; }
  $PY scripts/lens_agreement.py --name ${P}lens_agreement_v1 --why "Zach (2026-10-25, amendment 44): $KEY, our plain J-lens, lens check" \
    > /workspace/scratch/${P}agree.log 2>&1 < /dev/null || echo "=== $KEY lens check FAILED"
  echo "=== $KEY fit done $(date -u +%T)"
fi
bash scripts/queues/h200_nq40_1025.sh 0,1 $KEY $P gate
bash scripts/queues/h200_profile_1025.sh 0,1 prof:$KEY:$P:16:40
band=$($PY scripts/profile_pick.py ${P}jsuite_v2_dev_chat_profile_cand2_v1 2>/dev/null)
echo "=== BOLTPICK $KEY: '$band'"
bash scripts/queues/h200_dose_1025.sh 0,1 dose:$KEY:$P:16:40
[[ "$band" =~ ^[0-9]+-[0-9]+$ ]] && echo "$band" > /workspace/scratch/${P}v2band.txt && bash scripts/queues/h200_nq40_1025.sh 0,1 $KEY $P test swap
r=${P}jswap_v2_L44-55_v1
echo "=== jswap/$r $(date -u +%T)"
[ -f results/jswap/$r/summary.json ] || $PY scripts/jswap.py --name $r --why "Zach (2026-10-25, prereg amendment 44): $KEY, the swap at mid depth L44-55" \
  --set jsuite_v2_test_chat --band 44-55 --competence ${P}jsuite_v2_test_chat_competence_cand2_v1 --batch 8 > /workspace/scratch/$r.log 2>&1 < /dev/null \
  || { echo "=== $r FAILED"; tail -3 /workspace/scratch/$r.log; }
grep -E "^(PM|TM|PN|TN|PK|TK|PP|TP) (swap|remove|swap_rot|swap_u|swap_comp|paste) " /workspace/scratch/$r.log | sed "s/^/=== MIDSWAP $KEY /"
echo "=== bolt done $(date -u +%FT%TZ)"
