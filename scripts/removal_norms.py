"""removal_norms: why does removing the J-space (or a random dictionary's fit) break Gemma 4 31B-it but not Qwen? A
diagnostic, no verdict rule (Zach, 2026-10-20, overnight; after every gentle-removal setting failed its random control
on Gemma). For residuals at the removal layers on 8 WikiText texts (first 128 tokens) and 8 suite prompts (BL's lookup step alone),
per position group (first, 1-3, 4 on), the median of:
  norm          ||h||, and ||h - mean|| (mean: the layer's WikiText mean, ablate_pilot.layer_means)
  removed       ||fit(h)|| / ||h|| for the 25-atom signed OMP over the J-space and over the random dictionary
                (ablate_pilot's), and ||fit(h - mean)|| / ||h - mean|| (the centred removal)
  outliers      the share of ||h||^2 in the residual's top 8 coordinates (massive activations)

python scripts/removal_norms.py --name N --why W --layers L [L ...]
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
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.tokens import raw_encoding
from scripts import suite_v1 as S
from scripts.ablate_pilot import layer_means
from scripts.exp04_brew_parts import K_ATOMS, signed_omp

RESULTS = pins.RESULTS_DIR / "removal_norms"
GROUPS = {"first": slice(0, 1), "1-3": slice(1, 4), "4+": slice(4, None)}


@torch.no_grad()
def main(name: str, why: str, layers: tuple[int, ...]) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "layers": list(layers),
                "k_atoms": K_ATOMS, "random_seed": "777 + layer (ablate_pilot)", "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    jdict = {la: lens.vectors(la, letters) for la in layers}
    rdict = {}
    for la in layers:
        g = torch.Generator(device="cuda").manual_seed(777 + la)
        rdict[la] = torch.nn.functional.normalize(torch.randn(jdict[la].shape, device="cuda", generator=g), dim=-1)
    means = layer_means(model, layers)
    prompts = {"wikitext": [raw_encoding(tok, t)["input_ids"][:128] for t in pins.wikitext_rows()[:8]]}
    items = S.load("BL")[:8]
    prompts["suite_BL_hop"] = [S.ids(tok, S.render(tok, it["context"], it["hop2"]["question"])) for it in items]
    stats: dict = {}
    for source, id_lists in prompts.items():
        for la in layers:
            acc: dict[str, dict[str, list[float]]] = {g: {} for g in GROUPS}
            for ids in id_lists:
                _, rec = model.run(torch.tensor([ids], device="cuda"), record=(la,))
                h = rec[la]
                c = h - means[la]
                parts = {
                    "norm": h.norm(dim=-1),
                    "norm_centred": c.norm(dim=-1),
                    "removed_jspace": signed_omp(jdict[la], h, K_ATOMS).norm(dim=-1) / h.norm(dim=-1),
                    "removed_random": signed_omp(rdict[la], h, K_ATOMS).norm(dim=-1) / h.norm(dim=-1),
                    "removed_jspace_centred": signed_omp(jdict[la], c, K_ATOMS).norm(dim=-1) / c.norm(dim=-1),
                    "removed_random_centred": signed_omp(rdict[la], c, K_ATOMS).norm(dim=-1) / c.norm(dim=-1),
                    "top8_energy_share": (h**2).topk(8, dim=-1).values.sum(-1) / (h**2).sum(-1),
                }
                for g, sl in GROUPS.items():
                    for k, v in parts.items():
                        acc[g].setdefault(k, []).extend(v[sl].tolist())
            stats[f"{source}/L{la}"] = {
                g: {k: round(statistics.median(v), 4) for k, v in d.items()} for g, d in acc.items()
            }
            print(source, la, json.dumps(stats[f"{source}/L{la}"]["4+"]), flush=True)
    (out_dir / "summary.json").write_text(json.dumps({"stats": stats}, indent=2) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--layers", nargs="+", type=int, required=True)
    args = ap.parse_args()
    main(args.name, args.why, tuple(args.layers))
