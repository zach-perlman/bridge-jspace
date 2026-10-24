#!/bin/bash
# Zach (2026-10-24): Kolibri-1 prep, CPU and network only (approved: a separate env, the shared project env untouched).
# A uv env at /workspace/ext/kolibri_env with the project's pins except transformers >= 5.20 (Kolibri1 is native from
# 5.20); the FP8 weights at a pinned revision into the shared HF cache; a CPU check that config and tokenizer load.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
export UV_CACHE_DIR=/workspace/uv-cache CUDA_VISIBLE_DEVICES=
ENV=/workspace/ext/kolibri_env
REV=5bb7075ba22db733e3834b1c71d2245537cc14ed
echo "=== env $(date -u +%T)"
[ -x $ENV/bin/python ] || uv venv $ENV --python 3.12 || { echo "=== kolibri env FAILED"; exit 1; }
uv pip install --python $ENV/bin/python --index-url https://download.pytorch.org/whl/cu128 "torch==2.11.0" > /workspace/scratch/kolibri_env.log 2>&1 \
  && uv pip install --python $ENV/bin/python "transformers[kernels]>=5.20" "accelerate>=1.14" huggingface_hub safetensors "numpy==2.5.3" "scipy==1.18.1" \
     "pydantic>=2.8" "pyyaml>=6.0" "python-dotenv>=1.0" "tqdm>=4.66" "kernels==0.16.2" \
     "jlens @ git+https://github.com/anthropics/jacobian-lens@581d398613e5602a5af361e1c34d3a92ea82ba8e" >> /workspace/scratch/kolibri_env.log 2>&1 \
  || { echo "=== kolibri env install FAILED"; tail -5 /workspace/scratch/kolibri_env.log; exit 1; }
$ENV/bin/python -c "import torch, transformers; print('=== KOLENV torch', torch.__version__, 'transformers', transformers.__version__)"
echo "=== download $(date -u +%T)"
$ENV/bin/python -c "
from huggingface_hub import snapshot_download
p = snapshot_download('Aleph-Alpha/Kolibri-1', revision='$REV')
print('=== KOLDL', p)
" > /workspace/scratch/kolibri_dl.log 2>&1 || { echo "=== kolibri download FAILED"; tail -3 /workspace/scratch/kolibri_dl.log; exit 1; }
tail -1 /workspace/scratch/kolibri_dl.log
$ENV/bin/python -c "
from transformers import AutoConfig, AutoTokenizer
c = AutoConfig.from_pretrained('Aleph-Alpha/Kolibri-1', revision='$REV')
t = AutoTokenizer.from_pretrained('Aleph-Alpha/Kolibri-1', revision='$REV')
print('=== KOLCFG', c.architectures, 'layers', c.num_hidden_layers, 'hidden', c.hidden_size, 'vocab', c.vocab_size, 'tokenizer', type(t).__name__)
msgs = [{'role': 'user', 'content': 'Which country is Lima in? Answer with just the answer, nothing else.'}]
print('=== KOLTPL', repr(t.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)[-120:]))
" 2>&1 | grep -E "^===|Error" | tail -4
df -h /workspace | tail -1
echo "=== kolibri prep done $(date -u +%FT%TZ)"
