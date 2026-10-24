#!/bin/bash
# Zach (2026-10-24, prereg amendment 28 note): Kolibri-1 feasibility before any lens fit. (1) pins entry kolibri-1 with
# no lens yet (competence needs none); (2) competence on the jsuite test split (cand2, hop 1 by generation, thinking
# off): can it do the tasks without reasoning?; (3) can a lens be fit on the FP8 weights at all (lens fitting needs
# gradients through every block; the FP8 matmul kernels may have no backward): jlens.fit on 2 prompts at 2 layers, with
# its time per prompt; (4) whether transformers can dequantize the FP8 checkpoint to bf16 (the fallback: 156 GB, two
# GPUs). Usage: h200_kolchk_1024.sh GPU
set -u
G=$1
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$G
KPY=/workspace/ext/kolibri_env/bin/python
W="Zach (2026-10-24, prereg amendment 28 note)"
KEY=kolibri-1; P=kol1_; REPO=Aleph-Alpha/Kolibri-1; REV=5bb7075ba22db733e3834b1c71d2245537cc14ed
if ! grep -q "\"$KEY\": {" src/bridge_jspace/pins.py; then
  python3 - <<'PY' || { echo "=== KOLCHK pins FAILED"; exit 1; }
from pathlib import Path
p = Path("src/bridge_jspace/pins.py"); s = p.read_text()
anchor = '    "qwen3-32b-jlens": {'
assert s.count(anchor) == 1 and '"kolibri-1": {' not in s
block = '''    # Aleph-Alpha/Kolibri-1 (Aleph Alpha, 2026-10-03; MoE, 78B total / 3.46B active, FP8 weights; sliding-window and
    # full attention; prereg amendment 28; Zach, 2026-10-24): needs transformers >= 5.20 (/workspace/ext/kolibri_env).
    # Registered before its lens (competence needs none); the lens is added once fit and checked.
    "kolibri-1": {
        "repo": "Aleph-Alpha/Kolibri-1",
        "revision": "5bb7075ba22db733e3834b1c71d2245537cc14ed",
        "n_layers": 50,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "kol1_",
        "lenses": {},
    },
'''
p.write_text(s.replace(anchor, block + anchor)); print("registered kolibri-1 (no lens yet)")
PY
  git add src/bridge_jspace/pins.py scripts/queues/h200_kolchk_1024.sh && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com \
    commit -q -m "pins: kolibri-1, no lens yet (feasibility first; amendment 28 note)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
fi
export BJ_TARGET=$KEY
SET=jsuite_v1_facts_test_chat; cn=${P}${SET}_competence_cand2_v1
echo "=== competence $cn $(date -u +%T)"
[ -f results/tasks_v2/$cn/summary.json ] || $KPY scripts/natural_v1.py competence --set $SET --name $cn --read cand2 --hop1 gen \
  --why "$W: Kolibri-1, thinking off, can it do module 1" > /workspace/scratch/$cn.log 2>&1 || { echo "=== KOLCHK competence FAILED"; tail -5 /workspace/scratch/$cn.log; }
[ -f results/tasks_v2/$cn/summary.json ] && python3 -c "
import json, sys, collections
s = json.load(open(sys.argv[1]))['by_word_level']
print('=== KOLCOMP whole:', {k: round(v['whole'], 2) for k, v in s.items()})
rows = [json.loads(l) for l in open(sys.argv[2])]
acc = collections.defaultdict(list)
for r in rows: acc[r['part']].append(r['correct'])
print('=== KOLCOMP by part:', {k: round(sum(v) / len(v), 2) for k, v in acc.items()})
" results/tasks_v2/$cn/summary.json results/tasks_v2/$cn/items.jsonl
echo "=== FP8 backward test $(date -u +%T)"
$KPY - <<'PY' 2>&1 | grep -E "^=== |Error|error" | tail -6
import sys, time, traceback
sys.path.insert(0, "src")
import torch, jlens
from transformers import AutoModelForCausalLM, AutoTokenizer
from bridge_jspace import pins
repo, rev = "Aleph-Alpha/Kolibri-1", "5bb7075ba22db733e3834b1c71d2245537cc14ed"
try:
    from transformers import FineGrainedFP8Config
    import inspect
    print("=== KOLFP8 FineGrainedFP8Config params:", [p for p in inspect.signature(FineGrainedFP8Config).parameters])
except Exception as e:
    print("=== KOLFP8 no FineGrainedFP8Config:", type(e).__name__)
tok = AutoTokenizer.from_pretrained(repo, revision=rev)
hf = AutoModelForCausalLM.from_pretrained(repo, revision=rev, dtype=torch.bfloat16, device_map="cuda").eval()
print("=== KOLFP8 loaded; a weight dtype:", next(p.dtype for n, p in hf.named_parameters() if "experts" in n or "mlp" in n),
      "| peak GB", round(torch.cuda.max_memory_allocated() / 1e9, 1))
rows = [r[:2000] for r in pins.wikitext_rows() if len(r.split()) >= 64][:2]
model = jlens.from_hf(hf, tok, force_bos=tok.bos_token_id is not None)
t0 = time.time()
try:
    lens = jlens.fit(model, rows, source_layers=[10, 25], dim_batch=64, max_seq_len=128, skip_first=16)
    J = lens.jacobians[10]
    print("=== KOLFP8 BACKWARD OK: 2 prompts, 2 layers in", round(time.time() - t0, 1), "s; J finite:", bool(torch.isfinite(J).all()),
          "| peak GB", round(torch.cuda.max_memory_allocated() / 1e9, 1))
except Exception as e:
    print("=== KOLFP8 BACKWARD FAILED:", type(e).__name__, str(e)[:300])
    traceback.print_exc(limit=3)
PY
echo "=== kolchk done $(date -u +%FT%TZ)"
