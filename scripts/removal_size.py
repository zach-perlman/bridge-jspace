"""removal_size: how much of the residual does each knock-out remove? (Zach, 2026-10-22; the caveat on C1's specificity
control: removing the top-10 unembedding directions per position did nothing on the 27B, but those directions may simply
hold less of the mid-layer residual than the top-10 J-lens directions do.) On removal_textloss's 16 WikiText rows, at
each layer: the removed share of the residual's norm, ||h - edit(h)|| / ||h||, per position (position 0 excluded), for
the top-K span removal over the J-lens dictionary (paper10's) and over the unit unembedding rows (unembed10's), K = 1 and
10, and the same-size rotated control (equal norm by construction). Descriptive.

python scripts/removal_size.py --name N --why W --layers L [L ...]
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins
from bridge_jspace.ablate import LensDictionary, RowSettings, removal_edit
from bridge_jspace.tokens import raw_encoding

RESULTS = pins.RESULTS_DIR / "removal_size"


@torch.no_grad()
def main(name: str, why: str, layers: tuple[int, ...]) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    (out_dir / "manifest.json").write_text(json.dumps({"run": name, "why": why, "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
        "layers": list(layers), "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "doc": (__doc__ or "").split("\n\n")[0]}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    d = wg.shape[1]
    eye = torch.eye(d, device="cuda")
    texts = [ids for t in pins.wikitext_rows() if len(ids := raw_encoding(model.tokenizer, t)["input_ids"][:128]) >= 64][:16]
    shares: dict = {la: {f"{kind}{k}": [] for kind in ("jlens_top", "unembed_top") for k in (1, 10)} for la in layers}
    for ids in texts:
        _, rec = model.run(torch.tensor([ids], device="cuda"), record=tuple(layers))
        for la in layers:
            h = rec[la][1:][None]  # [1, T-1, d], position 0 excluded
            norm = h.norm(dim=-1)
            for kind, dic in (("jlens_top", LensDictionary(wg, lens.J(la))), ("unembed_top", LensDictionary(wg, eye))):
                for k in (1, 10):
                    edit = removal_edit("top", dic, [RowSettings()], k=k)
                    removed = (h - edit(h)).norm(dim=-1) / norm
                    shares[la][f"{kind}{k}"] += removed[0].tolist()
    summary = {"n_texts": len(texts), "median_share": {la: {c: statistics.median(v) for c, v in s.items()} for la, s in shares.items()},
               "mean_share": {la: {c: statistics.mean(v) for c, v in s.items()} for la, s in shares.items()}}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"{pins.TARGET}: median share of the residual norm removed (position 0 excluded)")
    for la, s in summary["median_share"].items():
        print(f"  L{la}: " + ", ".join(f"{c} {100 * v:.1f}%" for c, v in s.items()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--layers", nargs="+", type=int, required=True)
    a = ap.parse_args()
    main(a.name, a.why, tuple(a.layers))
