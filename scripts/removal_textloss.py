"""removal_textloss: does J-space removal break the model on plain text, or only on our tasks? (Zach, 2026-10-20,
overnight; on Gemma 4 31B-it the J-space removal breaks every task, lookups too, while a size-matched rotated removal
breaks none.) Mean next-token loss (nats) over 16 WikiText rows of 64+ tokens (first 128 tokens, predictions from
position 4 on) under: none, the J-space removal (ablate_pilot's Remove, all positions, the layers at once) and the
size-matched rotated control (ablate_pilot's Rotated). No verdict rule; the comparison is between models.
2026-10-21 (Zach: is Gemma broken by the current knock-out too, or only by the 25-atom one?): --conditions adds topK and
topK_rot, the headline knock-out's removal (the span of the K highest-scoring lens directions at every position,
ablate_v2's removal_edit "top") and its same-size rotated control (seed 888 + layer, as ablate_v2). Plain text has no
single answer, so nothing is protected: harsher than the task knock-out, which keeps the answer's top 10.

python scripts/removal_textloss.py --name N --why W --layers L [L ...] [--conditions none jspace rotated top10 top10_rot]
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
from bridge_jspace.ablate import LensDictionary, RowSettings, removal_edit
from bridge_jspace.ablate import rotation as rotation_v2
from bridge_jspace.model import _forward_hooks
from bridge_jspace.tokens import raw_encoding
from scripts.ablate_pilot import Remove, Rotated, rotation

RESULTS = pins.RESULTS_DIR / "removal_textloss"


@torch.no_grad()
def main(name: str, why: str, layers: tuple[int, ...], conditions: tuple[str, ...]) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "layers": list(layers), "conditions": list(conditions),
                "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    every = {"none": {}}
    if {"jspace", "rotated"} & set(conditions):  # 2026-10-23: only when asked (vocab x d per layer; OOMed the 122B)
        jd = {la: lens.vectors(la, letters) for la in layers}
        every |= {"jspace": {la: Remove(jd[la]) for la in layers},
                  "rotated": {la: Rotated(jd[la], rotation(jd[la].shape[1], 888 + la)) for la in layers}}  # fmt: skip
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    dic = {la: LensDictionary(wg, lens.J(la)) for la in layers}
    for c in conditions:
        if c.startswith("top"):  # topK[_nosink][_rot] (2026-10-21: _nosink leaves attention-sink positions unedited)
            k = int(c[3:].removesuffix("_rot").removesuffix("_nosink"))
            rot = c.endswith("_rot")
            every[c] = {la: _top(dic[la], k, rotation_v2(wg.shape[1], 888 + la) if rot else None, "_nosink" in c)
                        for la in layers}  # fmt: skip
        elif c.startswith("unembed"):  # 2026-10-23: the logit lens top-K (J = identity), as ablate_v2's unembedK
            k = int(c[7:].removesuffix("_rot").removesuffix("_nosink"))
            rot = c.endswith("_rot")
            ud = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
            every[c] = {la: _top(ud, k, rotation_v2(wg.shape[1], 888 + la) if rot else None, "_nosink" in c)
                        for la in layers}  # fmt: skip
    conds = {c: every[c] for c in conditions}
    texts = [ids for t in pins.wikitext_rows() if len(ids := raw_encoding(tok, t)["input_ids"][:128]) >= 64][:16]

    def hook_for(edit):
        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            h = edit(h[0].float()).to(h.dtype)[None]
            return (h, *out[1:]) if isinstance(out, tuple) else h

        return hook

    losses: dict[str, list[float]] = {c: [] for c in conds}
    for ids in texts:
        x = torch.tensor([ids], device="cuda")
        for cname, edits in conds.items():
            with _forward_hooks([(model.layers[la], hook_for(e)) for la, e in edits.items()]):
                logits = model.hf(input_ids=x, use_cache=False).logits[0].float()
            nll = torch.nn.functional.cross_entropy(logits[3:-1], x[0, 4:], reduction="mean")
            losses[cname].append(float(nll))
    summary = {"n_texts": len(texts), "mean_nll": {c: sum(v) / len(v) for c, v in losses.items()}, "per_text": losses}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["mean_nll"]))


def _top(dic, k: int, rot, skip_sinks: bool = False):
    """ablate_v2's top-K removal for one [T, d] residual (no row settings: every position, nothing protected)."""
    edit = removal_edit("top", dic, [RowSettings()], rotation=rot, k=k, skip_sinks=skip_sinks)
    return lambda h: edit(h[None])[0]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--layers", nargs="+", type=int, required=True)
    ap.add_argument("--conditions", nargs="+", default=["none", "jspace", "rotated"])
    args = ap.parse_args()
    main(args.name, args.why, tuple(args.layers), tuple(args.conditions))
