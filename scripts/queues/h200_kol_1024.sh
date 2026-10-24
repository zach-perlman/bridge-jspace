#!/bin/bash
# Zach (2026-10-24, prereg amendment 28): onboard Kolibri-1 (Aleph-Alpha/Kolibri-1, FP8 MoE, transformers >= 5.20 in
# /workspace/ext/kolibri_env). Steps, each stopping the queue on failure: plain J-lens fit (scripts/lens_fit/fit_jlens.py,
# 500 WikiText rows) -> pins entry "kolibri-1" (lens sha256) + commit -> lens_agreement -> plain-text gate
# (removal_textloss: top10 vs rotated, layers 15-35) -> jsuite dev split: competence + band sweep (windows of 7 by 3,
# PP PM MP MM, paper10 / rotated, n 100) + choose_band -> test split: competence + module 1 knock-out at the chosen band.
# Usage: h200_kol_1024.sh GPU
set -u
G=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
KPY=/workspace/ext/kolibri_env/bin/python
R=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd
W="Zach (2026-10-24, prereg amendment 28)"
REPO=Aleph-Alpha/Kolibri-1; REV=5bb7075ba22db733e3834b1c71d2245537cc14ed; KEY=kolibri-1; P=kol1_
LENS=cache/$KEY/lenses/jlens/Kolibri-1_jacobian_lens_n500.pt
stop() { echo "=== KOL STOP: $1"; [ -n "${2:-}" ] && tail -5 "$2"; exit 1; }
until grep -qs "^EXIT" $R-h200kolprep2-1024-0350.log; do sleep 30; done
grep -qs "=== kolibri prep done" $R-h200kolprep2-1024-0350.log || stop "prep failed" $R-h200kolprep2-1024-0350.log
grep -a "=== KOL" $R-h200kolprep2-1024-0350.log
echo "=== fit $(date -u +%T)"
if [ ! -f "$LENS" ]; then
  $KPY scripts/lens_fit/fit_jlens.py --repo $REPO --revision $REV --out $LENS --n 500 > /workspace/scratch/kol1_fit.log 2>&1 || stop "fit" /workspace/scratch/kol1_fit.log
fi
grep -a FIT_DONE /workspace/scratch/kol1_fit.log | sed "s/^/=== KOLFIT /"
SHA=$(sha256sum $LENS | cut -d" " -f1)
if ! grep -q "\"$KEY\": {" src/bridge_jspace/pins.py; then
  BOS=$($KPY -c "
from transformers import AutoTokenizer
t = AutoTokenizer.from_pretrained('$REPO', revision='$REV')
s = t.apply_chat_template([{'role': 'user', 'content': 'x'}], tokenize=False, add_generation_prompt=True, enable_thinking=False)
print('True' if t.bos_token and s.startswith(t.bos_token) else 'False')")
  python3 - "$KEY" "$REPO" "$REV" "$P" "$LENS" "$SHA" "$BOS" <<'PY' || stop "pins"
import sys
from pathlib import Path
key, repo, rev, pfx, lens, sha, bos = sys.argv[1:]
p = Path("src/bridge_jspace/pins.py"); s = p.read_text()
anchor = '    "qwen3-32b-jlens": {'
assert s.count(anchor) == 1 and f'"{key}": {{' not in s
block = f'''    # {repo} (Aleph Alpha, 2026-10-03; MoE, 78B total / 3.46B active, FP8 weights; sliding-window and full attention;
    # prereg amendment 28; Zach, 2026-10-24): our plain J-lens with Anthropic's jlens (scripts/lens_fit/fit_jlens.py,
    # 500 WikiText rows, Neuronpedia's recipe otherwise); needs transformers >= 5.20 (/workspace/ext/kolibri_env).
    "{key}": {{
        "repo": "{repo}",
        "revision": "{rev}",
        "n_layers": 50,
        "norm_gain": "weight",
        "bos": {bos},
        "run_prefix": "{pfx}",
        "frozen_lens": "jlens",
        "lenses": {{"jlens": ("local", "{lens}", "{sha}")}},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor)); print("registered", key, "bos", bos)
PY
  git add src/bridge_jspace/pins.py scripts/lens_fit/fit_jlens.py && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
    commit -q -m "pins: $KEY (our plain J-lens via jlens, 500 WikiText rows; amendment 28)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || stop "commit"
fi
export BJ_TARGET=$KEY
echo "=== lens check $(date -u +%T)"
[ -f results/lens_agreement/${P}lens_agreement_v1.json ] || $KPY scripts/lens_agreement.py --name ${P}lens_agreement_v1 --why "$W: lens check" > /workspace/scratch/kol1_agree.log 2>&1 || echo "=== KOL lens check FAILED (continuing)"
tail -4 /workspace/scratch/kol1_agree.log | sed "s/^/=== KOLAGREE /"
echo "=== text gate $(date -u +%T)"
$KPY scripts/removal_textloss.py --name ${P}textloss_v1 --why "$W: plain-text gate" --layers $(seq 15 35) --conditions none top10 top10_rot \
  > /workspace/scratch/kol1_textloss.log 2>&1 || echo "=== KOL text gate FAILED (continuing)"
tail -4 /workspace/scratch/kol1_textloss.log | sed "s/^/=== KOLGATE /"
DEV=jsuite_v1_facts_dev_chat; TEST=jsuite_v1_facts_test_chat
for SET in $DEV $TEST; do
  cn=${P}${SET}_competence_cand2_v1
  [ -f results/tasks_v2/$cn/summary.json ] && continue
  echo "=== competence $cn $(date -u +%T)"
  $KPY scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen --why "$W: Kolibri-1 on $SET" > /workspace/scratch/$cn.log 2>&1 || stop "competence $SET" /workspace/scratch/$cn.log
  python3 -c "import json,sys; s=json.load(open(sys.argv[1]))['by_word_level']; print('=== KOLCOMP', sys.argv[2], {k: round(v['whole'], 2) for k, v in s.items()})" results/tasks_v2/$cn/summary.json $SET
done
sw=${P}${DEV}_sweep_cand2_v1
echo "=== sweep $(date -u +%T)"
[ -f results/ablate_v2/$sw/summary.json ] || $KPY scripts/ablate_v2.py --name $sw --why "$W: band sweep on the dev split" --plan bands \
  --bands 0-6 3-9 6-12 9-15 12-18 15-21 18-24 21-27 24-30 27-33 30-36 33-39 36-42 39-45 42-48 --conditions paper10 paper10_rot \
  --tasks $DEV --tasks-competence ${P}${DEV}_competence_cand2_v1 --tasks-words PP PM MP MM --tasks-level all --n 100 --kinds clean --batch 32 --read cand2 \
  > /workspace/scratch/$sw.log 2>&1 || stop "sweep" /workspace/scratch/$sw.log
BAND=$($KPY scripts/choose_band.py $sw 2>/dev/null | tail -1 | grep -oE "[0-9]+-[0-9]+" | head -1)
echo "=== KOLBAND $BAND"
[ -n "$BAND" ] || stop "no band passes the rotated control"
r=${P}${TEST}_ko_cand2_v1
echo "=== ablate_v2/$r $(date -u +%T)"
[ -f results/ablate_v2/$r/summary.json ] || $KPY scripts/ablate_v2.py --name $r --why "$W: Kolibri-1, module 1 at its dev band L$BAND" --plan bands --bands $BAND \
  --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks $TEST --tasks-competence ${P}${TEST}_competence_cand2_v1 \
  --tasks-words PP PK PM PA MP MK MM MA TP TK TM TA --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2 > /workspace/scratch/$r.log 2>&1 || stop "module 1" /workspace/scratch/$r.log
$KPY scripts/jsuite_score.py $r | grep -E "^start (all|P |M |T )" | grep -E "paper10 |paper10_rot |unembed10 " | sed "s/^/=== KOLJS /"
echo "=== kolibri done $(date -u +%FT%TZ)"
