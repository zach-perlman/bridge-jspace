"""lens_input_identity: at which layers does the J-lens mostly read the input token itself? (Zach, 2026-10-20.) Defines
ablate_v2's "workspace" whole-depth range: from the first layer where the lens's top-1 token equals the current input
token at fewer than half of the positions, to the last edited layer (removing the J-space below it mostly deletes
the prompt's tokens, decided with Zach 2026-10-20). Per layer, on the whole questions of the depth sweep's families
(25 per family): the share of positions whose lens top-1 is the input token there, and the share where it is the
next input token.

python scripts/lens_input_identity.py --name N --why W [--n 25]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import ablate_v2 as V

RESULTS = pins.RESULTS_DIR / "lens_input_identity"


@torch.no_grad()
def main(name: str, why: str, n: int) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    (out_dir / "manifest.json").write_text(json.dumps({"run": name, "why": why, "model": pins.model_pin(),
        "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "n_per_family": n,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    prompts = V.suite_prompts(tok, ["BL", "BR", "RL", "RR"], ["clean"], n, V.COMPETENCE)
    prompts += V.country_prompts(tok, ["R", "B"], n)
    layers = list(range(pins.N_LAYERS - 1))
    same = {la: [0, 0] for la in layers}
    nxt = {la: [0, 0] for la in layers}
    for p in prompts:
        ids = torch.tensor([p["ids"]], device="cuda")
        _, rec = model.run(ids, record=tuple(layers))
        inp = ids[0]
        for la in layers:
            top = lens.readout(rec[la], la).argmax(-1)
            same[la][0] += int((top == inp).sum())
            same[la][1] += inp.numel()
            nxt[la][0] += int((top[:-1] == inp[1:]).sum())
            nxt[la][1] += inp.numel() - 1
    share = {la: same[la][0] / same[la][1] for la in layers}
    start = next(la for la in layers if share[la] < 0.5)
    summary = {"n_prompts": len(prompts), "workspace_start": start,
               "top1_is_input_token": {la: round(v, 3) for la, v in share.items()},
               "top1_is_next_input_token": {la: round(nxt[la][0] / nxt[la][1], 3) for la in layers}}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("workspace starts at layer", start)
    print(" ".join(f"{la}:{share[la]:.2f}" for la in layers))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=25)
    args = ap.parse_args()
    main(args.name, args.why, args.n)
