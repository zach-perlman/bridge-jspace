"""lens_agreement: does a lens read the model's own next-token prediction from earlier layers? (Zach, 2026-10-21: a
sanity check for third-party lenses, solarkyle's plain J-lenses for Mistral-Small-24B-2501 and the two bridges, before
runs lean on them.) On removal_textloss's 16 WikiText rows (first 128 tokens), the share of positions (from 16 on) where
the model's own top-1 next token (the final block, unembedded) is in the lens's top 10 at each layer, for the target's
frozen lens and for the logit lens (no J). Also the model's mean next-token loss on the rows (from position 4, as
removal_textloss), and greedy answers to a few chat questions. Not jpp_lens's pass@10 (other items and grading); numbers
are comparable across targets run with this script.

python scripts/lens_agreement.py --name N --why W [--layers L ...]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import chat, pins
from bridge_jspace.run_switches import switches
from bridge_jspace.tokens import raw_encoding

RESULTS = pins.RESULTS_DIR / "lens_agreement"
QUESTIONS = [
    ("What is the capital of France?", "Paris"),
    ("In which country is Lyon located?", "France"),
    ("What language is spoken in Brazil?", "Portuguese"),
    ("What is the capital of the country where Munich is located?", "Berlin"),
    ("What currency is used in the country whose capital is Tokyo?", "Yen"),
    ("Emma lives in Kenya. What is the capital of the country where Emma lives?", "Nairobi"),
]


@torch.no_grad()
def main(name: str, why: str, layers: list[int] | None) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "argv": sys.argv,
                "doc": (__doc__ or "").split("\n\n")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    src = sorted(set(lens.source_layers))
    layers = layers or src
    last = pins.N_LAYERS - 1
    texts = [ids for t in pins.wikitext_rows() if len(ids := raw_encoding(tok, t)["input_ids"][:128]) >= 64][:16]
    hits = {la: {"lens": 0, "logit": 0} for la in layers}
    n, nll = 0, []
    for ids in texts:
        x = torch.tensor([ids], device="cuda")
        _, rec = model.run(x, record=(*layers, last))
        final = model.unembed(rec[last])  # [T, vocab]: the model's own logits
        nll.append(float(torch.nn.functional.cross_entropy(final[3:-1], x[0, 4:])))
        target = final[16:].argmax(-1)
        n += len(target)
        for la in layers:
            h = rec[la][16:]
            hits[la]["lens"] += int((lens.readout(h, la).topk(10, -1).indices == target[:, None]).any(-1).sum())
            hits[la]["logit"] += int((model.unembed(h).topk(10, -1).indices == target[:, None]).any(-1).sum())
    answers = []
    for q, gold in QUESTIONS:
        ids = model.encode(chat.chat_text(tok, f"{q} {chat.QUESTION_INSTRUCTION}"))
        out = model.greedy_text(ids, 6)
        answers.append({"q": q, "gold": gold, "out": out, "right": gold.lower() in out.lower()})
    summary = {"n_texts": len(texts), "n_positions": n, "mean_nll": sum(nll) / len(nll), "lens_source_layers": [src[0], src[-1], len(src)],
               "top10_agreement": {la: {k: v / n for k, v in hv.items()} for la, hv in hits.items()},
               "chat": answers, "chat_right": sum(a["right"] for a in answers)}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"{pins.TARGET}: loss {summary['mean_nll']:.2f} nats; chat {summary['chat_right']}/{len(answers)}; lens layers {src[0]}-{src[-1]} ({len(src)})")
    for la, hv in summary["top10_agreement"].items():
        print(f"  layer {la:>2}: lens {hv['lens']:.2f}  logit {hv['logit']:.2f}")
    for a in answers:
        print(f"  {a['right']!s:5} {a['q']} -> {a['out']!r}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--layers", nargs="+", type=int, default=None)
    a = ap.parse_args()
    main(a.name, a.why, a.layers)
