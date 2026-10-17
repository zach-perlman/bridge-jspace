"""exp19_fit_data: J++'s CLI (safety-research/jpp_lens scripts/jpp_cli.py) with the router's PCA and k-means on the
GPU (as neuronpedia's jpp_cli_gpu.py), and with WikiText replaced by the prompt pool in $FIT_POOL_JSON.

J++ draws every fitting prompt from jlens.examples.load_wikitext_prompts: fit-router takes the first 1000, fit-shard
the first --num-prompts. Replacing that loader makes both stages read the condition's pool, so the router and the
expert Jacobians see the same data. Run from the jpp_lens checkout with PYTHONPATH=src and its venv.
"""

import dataclasses
import json
import os
import runpy
import sys
from pathlib import Path

import torch as t

if sys.argv[1:2] == ["fit-shard"]:
    sys.modules["fla"] = None  # RelP surgery needs the torch GatedDeltaNet path (as jpp_cli_gpu.py)

import jlens.examples
from workspace_lens.routing import router as routing

POOL = os.environ.get("FIT_POOL_JSON")
if POOL:
    _pool = json.loads(Path(POOL).read_text())

    def _load_pool(n_prompts: int, *, min_chars: int = 600) -> list[str]:
        assert len(_pool) >= n_prompts, f"{POOL} holds {len(_pool)} prompts; {n_prompts} requested"
        return list(_pool[:n_prompts])

    jlens.examples.load_wikitext_prompts = _load_pool
    print(f"[exp19] fitting prompts from {POOL} ({len(_pool)} texts)", flush=True)

_fit = routing.ActivationRouterCollection.fit


def _fit_on_gpu(self, activations_L_dict_PN):
    for layer, activations_PN in activations_L_dict_PN.items():
        _fit(self, {layer: activations_PN.cuda()})
        fitted = self.layer_routers_L_dict[layer]
        moved = {f.name: getattr(fitted, f.name).cpu() for f in dataclasses.fields(fitted)}
        self.layer_routers_L_dict[layer] = dataclasses.replace(fitted, **moved)
        t.cuda.empty_cache()


routing.ActivationRouterCollection.fit = _fit_on_gpu
sys.argv = ["scripts/jpp_cli.py", *sys.argv[1:]]
runpy.run_path("scripts/jpp_cli.py", run_name="__main__")
