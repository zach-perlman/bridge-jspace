"""fit_jlens (Zach, 2026-10-24, prereg amendment 28): a plain Jacobian lens with Anthropic's jlens (the paper's own
method, anthropics/jacobian-lens at the project's pinned commit) for a model with no published lens. Neuronpedia's
recipe for its published J-lenses where it applies: texts cut to 2,000 characters, 128 tokens, the first 16 positions
skipped, dim_batch 64, bf16, every layer below the last as a source, the final layer as the target. Texts: the pinned
WikiText rows (pins.wikitext_rows, rows of at least 64 words), the first N (default 500; Neuronpedia used up to 1,000
WikiText-103 train texts with early stopping). Resumable checkpoints every 25 prompts. Writes JacobianLens.save (fp16;
the format bridge_jspace.lens reads: J, n_prompts, source_layers, d_model) and prints the lens's sha256.

Run in the model's env (Kolibri-1 needs transformers >= 5.20: /workspace/ext/kolibri_env):
python scripts/lens_fit/fit_jlens.py --repo R --revision V --out PATH [--n 500] [--no-bos]
(2026-10-25, amendment 40: --no-bos for a model whose tokenizer adds no BOS (Nemotron 3.5: add_bos_token false), so the
lens sees text as the harness feeds it; NemotronH's layout (embeddings, layers, norm_f) is passed to jlens explicitly.
--harness: the model as bridge_jspace loads it for BJ_TARGET (Nemotron 3.5 Bolt: NVIDIA's language model out of the
multimodal checkpoint, split over two GPUs by pins' split_gpus); --repo / --revision must then be BJ_TARGET's.)
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import jlens  # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402

from bridge_jspace import pins  # noqa: E402


def main(a) -> None:
    out = Path(a.out)
    assert not out.exists(), f"{out} exists; lenses are written once"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = [r[:2000] for r in pins.wikitext_rows() if len(r.split()) >= 64]
    assert len(rows) >= a.n, f"only {len(rows)} WikiText rows of >= 64 words"
    rows = rows[: a.n]
    if a.harness:
        from bridge_jspace.model import load_model

        assert (a.repo, a.revision) == (pins.MODEL_REPO, pins.MODEL_REVISION), f"BJ_TARGET={pins.TARGET} is another model"
        m = load_model()
        tok, hf = m.tokenizer, m.hf
    else:
        tok = AutoTokenizer.from_pretrained(a.repo, revision=a.revision)
        hf = AutoModelForCausalLM.from_pretrained(a.repo, revision=a.revision, dtype=torch.bfloat16, device_map="cuda").eval()
    bos = tok.bos_token_id is not None and not a.no_bos
    layout = jlens.hf.Layout("model", norm="norm_f", embed="embeddings") if hasattr(hf.model, "norm_f") else None
    model = jlens.from_hf(hf, tok, layout=layout, force_bos=bos)
    print(f"{a.repo}@{a.revision}: {len(rows)} prompts, bos {bos}, layout {layout}", flush=True)
    t0 = time.time()
    lens = jlens.fit(model, rows, dim_batch=a.dim_batch, max_seq_len=128, skip_first=16,
                     checkpoint_path=str(out) + ".ckpt", checkpoint_every=25)  # fmt: skip
    lens.save(str(out))
    print(f"FIT_DONE {out} {len(lens.source_layers)} source layers, {lens.n_prompts} prompts, {time.time() - t0:.0f}s "
          f"sha256 {pins.sha256_file(out)}", flush=True)  # fmt: skip


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--dim-batch", type=int, default=64)
    ap.add_argument("--no-bos", action="store_true", help="no BOS first, for a tokenizer that adds none")
    ap.add_argument("--harness", action="store_true", help="load BJ_TARGET's model as bridge_jspace does (see above)")
    main(ap.parse_args())
