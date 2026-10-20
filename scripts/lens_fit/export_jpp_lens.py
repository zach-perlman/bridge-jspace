"""Export a lens written by safety-research/jpp_lens (BaseLens.save: {"parameters": {"jacobians": {layer: [F, N]}},
"source_layers", "config"}) to the J format bridge_jspace.lens.JLens loads ({"J": {layer: [d, d]}, "source_layers",
"d_model", "n_prompts", "provenance"}, fp16, as neuronpedia's published lenses), and print its sha256 (Zach, 2026-10-20,
for the Gemma 4 31B-it fit). Both libraries apply J as h @ J.T (jpp_lens JacobianLens.forward, our JLens.readout), so
the matrices are copied as they are; the fp16 cast's largest relative error (Frobenius, per layer) is printed.

python scripts/lens_fit/export_jpp_lens.py IN OUT --note TEXT
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import torch


def main(src: str, dst: str, note: str) -> None:
    blob = torch.load(src, map_location="cpu", weights_only=True)
    jac = blob["parameters"]["jacobians"]
    layers = sorted(int(k) for k in jac)
    assert layers == sorted(int(k) for k in blob["source_layers"]), "jacobians and source_layers disagree"
    J = {la: jac[la].to(torch.float16).contiguous() for la in layers}
    err = max(float((J[la].float() - jac[la].float()).norm() / jac[la].float().norm()) for la in layers)
    assert all(J[la].shape[0] == J[la].shape[1] for la in layers), "expected square [d, d] jacobians"
    config = blob.get("config", {})
    out = {
        "J": J,
        "source_layers": layers,
        "d_model": int(J[layers[0]].shape[0]),
        "n_prompts": config.get("num_prompts_trained_on"),
        "provenance": {"source": str(src), "method": "jpp", "source_config": config, "note": note},
    }
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    assert not Path(dst).exists(), f"{dst} exists; lens files are written once"
    torch.save(out, dst)
    sha = hashlib.sha256(Path(dst).read_bytes()).hexdigest()
    print(json.dumps({"out": str(dst), "layers": layers, "d": out["d_model"], "max_rel_err_fp16": err, "sha256": sha}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--note", required=True)
    args = ap.parse_args()
    main(args.src, args.dst, args.note)
