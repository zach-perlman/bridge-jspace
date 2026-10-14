"""Setup checks on the GPU, before any experiment. Writes results/checks/setup.json (once).

1. Layer convention: J_l should map the output of block l (not its input) to the final block's output.
2. Unembed: model.unembed(final block output) reproduces the model's logits.
3. Vector form: <v_t, h> / rms(J_l h) equals the lens logit of token t.
4. No-op clamp: pinning clean coordinates at every band layer leaves the logits unchanged; the swap does not.
5. Determinism: the same prompt twice gives identical logits.
6. Clean accuracy on the 90 two-hop items (answer at word rank 1), for orientation only.
"""

import json
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.clamp import SwapClamp  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.model import load_model  # noqa: E402

OUT = pins.RESULTS_DIR / "checks" / "setup.json"
BAND = tuple(range(24, 41))


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assert not OUT.exists(), f"{OUT} exists; results are write-once"
    model = load_model()
    lens = JLens(model)
    items = json.loads(pins.PROBE_SWAP_FILE.read_text())["items"]
    final = len(model.layers) - 1
    report = {}

    # 1-3 on the first 10 prompts.
    conv = {l: {"block_output": [], "block_input": []} for l in (20, 40, 62)}
    unembed_err, vector_err, lens_top1_agree = [], [], []
    for item in items[:10]:
        ids = model.encode(item["prompt"])
        logits, h = model.run(ids, record=tuple(range(len(model.layers))))
        target = h[final][1:]
        for l in conv:
            for name, src in (("block_output", h[l]), ("block_input", h[l - 1])):
                cos = torch.nn.functional.cosine_similarity(src[1:] @ lens.J(l).T, target, dim=-1)
                conv[l][name].append(float(cos.mean()))
        unembed_err.append(float((model.unembed(h[final][-1]) - logits).abs().max() / logits.abs().max()))
        lens_top1_agree.append(int(lens.readout(h[62][-1], 62).argmax() == logits.argmax()))
        x = h[40][-1] @ lens.J(40).T
        lens_logits = lens.readout(h[40][-1], 40)
        top = lens_logits.topk(50).indices
        rms = (x.pow(2).mean() + model.hf.model.norm.eps).sqrt()
        vec_logits = lens.vectors(40, top, unit=False) @ h[40][-1] / rms
        vector_err.append(float((vec_logits - lens_logits[top]).abs().max() / lens_logits[top].abs().max()))
    report["layer_convention_mean_cos_to_final"] = {
        l: {k: sum(v) / len(v) for k, v in d.items()} for l, d in conv.items()}
    report["unembed_max_rel_err"] = max(unembed_err)
    report["lens62_top1_agrees_with_model"] = f"{sum(lens_top1_agree)}/{len(lens_top1_agree)}"
    report["vector_form_max_rel_err"] = max(vector_err)

    # 4-5 on the first item: swap/pin the J-lens vectors of its bridge and swap target across BAND.
    item = items[0]
    ids = model.encode(item["prompt"])
    clean_logits, clean_h = model.run(ids, record=BAND)
    tokens = torch.tensor([model.concept_token(item["intermediate"]), model.concept_token(item["swap_to"])],
                          device="cuda")

    def clamps(swap: bool):
        return {l: SwapClamp(lens.vectors(l, tokens), clean_h[l], swap=swap) for l in BAND}

    pinned_logits, _ = model.run(ids, edits=clamps(swap=False))
    swapped_logits, _ = model.run(ids, edits=clamps(swap=True))
    again_logits, _ = model.run(ids)
    report["noop_clamp"] = {
        "item": item["name"],
        "max_abs_logit_change_pinned": float((pinned_logits - clean_logits).abs().max()),
        "max_abs_logit_change_swapped": float((swapped_logits - clean_logits).abs().max()),
        "top_word_clean": model.top_word(clean_logits),
        "top_word_pinned": model.top_word(pinned_logits),
        "top_word_swapped": model.top_word(swapped_logits),
    }
    report["deterministic_rerun"] = bool(torch.equal(again_logits, clean_logits))

    # 6
    correct, scorable = 0, 0
    for item in items:
        answer_ids = model.surface_ids(item["answer"])
        if not answer_ids or not model.surface_ids(item["swap_answer"]):
            continue
        scorable += 1
        logits, _ = model.run(model.encode(item["prompt"]))
        correct += model.word_rank(logits, answer_ids) == 1
    report["clean_accuracy"] = {"correct": correct, "scorable": scorable, "total": len(items)}

    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
