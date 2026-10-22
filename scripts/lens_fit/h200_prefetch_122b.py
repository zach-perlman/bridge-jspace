"""Prefetch Qwen3.5-122B-A10B (FP8) and its J++ lens on the 2x H200 box, at the revisions pinned in
src/bridge_jspace/pins.py, while the Qwen3-32B J++ fit still holds the GPUs (Dan, 23 Oct ~00:35: the 122B runs on this
box after the fit). Run on the box with the recipe env's python (it has huggingface_hub):

  nohup ~/work/jpp_lens/.venv/bin/python ~/work/bridge-jspace/scripts/lens_fit/h200_prefetch_122b.py > ~/work/prefetch_122b.log 2>&1 &
"""

import hashlib
import os
import time

os.environ.setdefault("HF_HOME", os.path.expanduser("~/work/hf"))
from huggingface_hub import hf_hub_download, snapshot_download

MODEL, MODEL_REV = "Qwen/Qwen3.5-122B-A10B-FP8", "a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9"
LENS_REPO, LENS_REV = "neuronpedia/jacobian-lens", "e166deb5ad540932100ef803c8c9bcc2a5453694"
LENS_FILE = "qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt"
LENS_SHA = "b771e50244c81a3f315987ca2b8e88a58f670e3fed934dd21e3bfec4a3c05e53"

t = time.time()
lens = hf_hub_download(LENS_REPO, LENS_FILE, revision=LENS_REV)
h = hashlib.sha256()
with open(lens, "rb") as f:
    for chunk in iter(lambda: f.read(1 << 24), b""):
        h.update(chunk)
print("lens", lens, "sha256 ok" if h.hexdigest() == LENS_SHA else f"SHA MISMATCH {h.hexdigest()}", flush=True)
path = snapshot_download(MODEL, revision=MODEL_REV, max_workers=16)
print("model", path, f"{(time.time() - t) / 60:.1f} min", flush=True)
print("PREFETCH_DONE", flush=True)
