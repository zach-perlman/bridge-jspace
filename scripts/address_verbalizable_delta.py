"""address_verbalizable_delta: stage (b) of scripts/address_verbalizable.py, on a GPU box (POST HOC; Dan 30 Oct).

For 30 random C2 lookup scenes of the model's routes run (random.Random(29).sample of the sorted C2 scenes): the real change
Delta = h_S - h_O at the bridge word (the lookup's prompts, the model's fixed layer), its component inside the pointer directions
U U^T Delta (U = Alf of the model's probe states, the subspace no_alf removes), and per scene j = the bridge's locker slot in O, k = the
changed pick's locker slot in S, the locker digits. Writes results/address_verbalizable_delta/<UTC>/deltas.npz (+ manifest).

BJ_TARGET=muse-glimmer-30b uv run python scripts/address_verbalizable_delta.py
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import pins  # noqa: E402
from scripts import x0_massmean as MM  # noqa: E402
from scripts import x6_routes as R  # noqa: E402
from scripts import x8_write as W  # noqa: E402

ROUTES = {"qwen3.5-9b": "qwen35_9b_x6_routes", "qwen3.6-27b": "x6_routes_27b", "muse-glimmer-30b": "muse30b_x6_routes",
          "nemotron-3.5-lightning": "nem35l_x52_routes", "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_g75"}  # fmt: skip
SEED, N = 29, 30


def main() -> Path:
    import torch

    from bridge_jspace.model import load_model
    from scripts import x0_necessity as X

    target = pins.TARGET
    states = R.STATES[target]
    layer = int(json.loads((REPO / "results" / "x0_probe" / states / "manifest.json").read_text())["layer"])
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "address_verbalizable_delta" / f"{target}-{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    cases = {
        c["scene"]: c
        for c in X.read_jsonl(REPO / "results" / "x6_routes" / ROUTES[target] / "cases.jsonl")
        if c["condition"] == "C2"
    }
    scenes = random.Random(SEED).sample(sorted(cases), N)
    (out / "manifest.json").write_text(json.dumps({"exp": "address_verbalizable_delta", "post_hoc": True, "model": target, "layer": layer, "probe_states": states,
                                                   "routes_run": ROUTES[target], "scenes": scenes, "seed": SEED, "written_utc": stamp}, indent=2))  # fmt: skip
    alf = MM.subspaces(states)[0]["Alf"].astype(np.float32)
    R.warm_cusolver()
    model = load_model()
    vecs, meta, norms = [], [], []
    with torch.no_grad():
        for s in scenes:
            c = cases[s]
            rd = c["readers"][X.LOOKUP]
            h = {v: model.run(torch.tensor([rd["ids"][v]], device=model.device), record=(layer,))[1][layer][c["pos"] if "pos" in c else rd["pos"]].float().cpu().numpy()
                 for v in ("org", "alt")}  # fmt: skip
            delta = h["alt"] - h["org"]
            p = alf @ (alf.T @ delta)
            slots_o, slots_s = W.slots_of(c["context"]), W.slots_of(c["cf_context"])
            j = [x for x, _ in slots_o].index(c["bridge"])
            k = [x for x, _ in slots_s].index(c["cf_bridge"])
            vecs.append(p)
            norms.append({"delta": float(np.linalg.norm(delta)), "pointer_part": float(np.linalg.norm(p))})
            meta.append({"scene": s, "j": j, "k": k, "locker_values": sorted({d for _, d in slots_o} | {d for _, d in slots_s}), "bridge": c["bridge"], "cf_bridge": c["cf_bridge"], **norms[-1]})  # fmt: skip
    np.savez(out / "deltas.npz", vec=np.stack(vecs), meta=json.dumps(meta))
    print(out, json.dumps(meta[:3]), flush=True)
    return out


if __name__ == "__main__":
    main()
