"""natural_hops_ablate: J-space removal on each single step of natural_rw v3's items (Zach, 2026-10-20 overnight). In
v3_lookup the removal hurt both versions (NM 98% -> 45%, NL 100% -> 55%), unlike the suite's RL (99%). Is that because
the first step, recalling the person's birth city, itself needs the J-space? For the items of a natural_rw run (its
ablation.jsonl ids), three single-step prompts in natural_rw's format (chat, blank statement, 'Answer:' prefilled):
  hop1         "The city where <person> was born is ___"                  -> the city      (recall)
  hop2_recall  "<city> is in the country of ___" (TwoHopFact's own)       -> its country   (recall)
  hop2_lookup  the v3 colour facts, then "The team colour of <city> is ___" -> its colour  (lookup in the prompt)
Conditions as natural_rw --ablate (ablate_pilot's Remove at the layers, all at once; control: the random dictionary).
Accuracy = top token is the answer's first token; reported over all items and over those right unedited.

python scripts/natural_hops_ablate.py --name N --why W --from RUN
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

from bridge_jspace import chat, pins
from bridge_jspace.run_switches import switches
from bridge_jspace.tokens import raw_encoding
from scripts import natural_rw as N
from scripts import suite_v1 as S
from scripts import twohop_pilot as T
from scripts.ablate_pilot import Remove
from scripts.exp03_brew_swaps import write_jsonl


@torch.no_grad()
def main(name: str, why: str, source: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = N.RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "layers": list(N.LAYERS),
                "items_from": source, "screen_run": N.SCREEN_RUN, "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    keep = {json.loads(line)["id"] for line in (N.RESULTS / source / "ablation.jsonl").read_text().splitlines()}
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    nl = {c["id"]: c for c in N.build(tok, model, ("NL",)) if c["id"] in keep}
    items = {it["id"]: it for it in json.loads((T.DATA / "screen.json").read_text())["items"] if it["id"] in keep}
    assert set(nl) == keep == set(items), "items differ from the source run's"

    def encode(text: str) -> list[int]:
        return list(raw_encoding(tok, chat.chat_text(tok, chat.blank_content(text)))["input_ids"])

    prompts = []
    for i in sorted(keep):
        it, c = items[i], nl[i]
        steps = {"hop1": (it["prompts"]["hop1"], it["e2"]), "hop2_recall": (it["prompts"]["hop2"], it["e3"]),
                 "hop2_lookup": (f"{c['context']} The team colour of {it['e2']} is", c["answer"])}  # fmt: skip
        for step, (text, answer) in steps.items():
            prompts.append({"id": i, "step": step, "ids": encode(text), "tok": S.answer_token(tok, answer, "word")})
    letters = model.letter_token_ids()
    jd = {la: lens.vectors(la, letters) for la in N.LAYERS}
    rd = {}
    for la in N.LAYERS:
        g = torch.Generator(device="cuda").manual_seed(777 + la)
        rd[la] = torch.nn.functional.normalize(torch.randn(jd[la].shape, device="cuda", generator=g), dim=-1)
    conds = {"none": {}, "jspace": {la: Remove(jd[la]) for la in N.LAYERS},
             "random": {la: Remove(rd[la]) for la in N.LAYERS}}  # fmt: skip
    t0 = time.time()
    rows = []
    for p in prompts:
        ids = torch.tensor([p["ids"]], device="cuda")
        for cname, edits in conds.items():
            _, lg = model.generate_batch(ids, 1, [edits], first_logits=True)
            rows.append({"id": p["id"], "step": p["step"], "condition": cname, "correct": int(lg[0].argmax()) == p["tok"],
                         "logp": float(lg[0].log_softmax(-1)[p["tok"]])})  # fmt: skip
    write_jsonl(out_dir / "rows.jsonl", rows)
    summary: dict = {"n_items": len(keep), "seconds": round(time.time() - t0), "steps": {}}
    lines = [f"# natural_hops_ablate / {name}: {len(keep)} items from {source}, layers {list(N.LAYERS)}", "",
             "| step | n right unedited | accuracy: none / J-space removed / random removed (all items) | "
             "same, items right unedited |", "|---|---|---|---|"]  # fmt: skip
    for step in ("hop1", "hop2_recall", "hop2_lookup"):
        sel = {c: {r["id"]: r for r in rows if r["step"] == step and r["condition"] == c} for c in conds}
        ok = [i for i, r in sel["none"].items() if r["correct"]]
        acc_all = {c: statistics.mean(r["correct"] for r in v.values()) for c, v in sel.items()}
        acc_ok = {c: statistics.mean(v[i]["correct"] for i in ok) if ok else None for c, v in sel.items()}
        summary["steps"][step] = {
            "n_right_unedited": len(ok),
            "accuracy_all": acc_all,
            "accuracy_right_unedited": acc_ok,
        }
        fmt = lambda d: " / ".join("-" if v is None else f"{100 * v:.0f}%" for v in d.values())  # noqa: E731
        lines.append(f"| {step} | {len(ok)} | {fmt(acc_all)} | {fmt(acc_ok)} |")
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--from", dest="source", required=True, help="natural_rw run (with --ablate) whose items to use")
    ap.add_argument("--layers", nargs="+", type=int, default=list(N.LAYERS))
    ap.add_argument("--screen-run", default=N.SCREEN_RUN)
    args = ap.parse_args()
    N.LAYERS, N.SCREEN_RUN = tuple(args.layers), args.screen_run
    main(args.name, args.why, args.source)
