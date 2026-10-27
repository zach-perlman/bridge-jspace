"""tool_answer_type: is the J-space removal's 30% hit on the JSON lookup (tool_abl_v1: TBL 100% -> 70%, the suite's
prose lookups 99%) about the JSON lookup or about its answer being a name? (Zach, 2026-10-20 overnight.) Every suite
family answers a digit; TBL answers a vet's name, a word inside the span of the J-space's letter-token dictionary.

Each scene is one context of three JSON tool results, get_profiles (three people's pets), get_vets (each pet's vet)
and get_lockers (each pet's locker, a digit 1-9), and gets four questions on that same context:
  name_clean   "Which vet looks after <person>'s pet?"       a lookup, name answer   (as TBL)
  digit_clean  "Which locker belongs to <person>'s pet?"     a lookup, digit answer  (as the suite's BL)
  name_hop / digit_hop   the same about "the <animal>" (the lookup step alone)
Removal as ablate_pilot v1 (25-atom J-space OMP at every position, layers all at once; control: the random dictionary).
Accuracy on the scenes each question gets right unedited. Prediction (not a decision rule): if the hit is the answer
type, digit_clean stays near 100% while name_clean drops as TBL did; if it is the JSON lookup, both drop.

python scripts/tool_answer_type.py --name N --why W [--n K]
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import suite_v1 as S
from scripts.ablate_pilot import LAYERS, Remove
from scripts.exp03_brew_swaps import write_jsonl

RESULTS = pins.RESULTS_DIR / "tool_answer_type"
SEED = 602
BATCH = 16


def scenes(tok, n: int) -> list[dict]:
    rng = random.Random(SEED)
    animals = [a for a in S.ANIMALS if len(S.ids(tok, a)) == 1]  # inside JSON quotes: no leading space
    out, seen = [], set()
    while len(out) < n:
        bridge = S.pick_bridge(rng)
        if bridge not in animals:
            continue
        x, z = rng.sample([a for a in animals if a != bridge], 2)
        names = rng.sample(S.PEOPLE, 6)
        people, vets = names[:3], names[3:]
        pets = [bridge, x, z]
        rng.shuffle(pets)
        vet_of = dict(zip([bridge, x, z], vets, strict=True))
        locker_of = dict(zip([bridge, x, z], rng.sample(S.DIGITS, 3), strict=True))
        holder = people[pets.index(bridge)]
        prof = ", ".join(f'{{"name": "{p}", "pet": "{a}"}}' for p, a in zip(people, pets, strict=True))
        vt = ", ".join(f'{{"pet": "{a}", "vet": "{vet_of[a]}"}}' for a in rng.sample(pets, 3))
        lk = ", ".join(f'{{"pet": "{a}", "locker": {locker_of[a]}}}' for a in rng.sample(pets, 3))
        order = [("get_vets", vt), ("get_lockers", lk)]
        rng.shuffle(order)
        ctx = f"Tool output from get_profiles:\n[{prof}]\n" + "\n".join(
            f"Tool output from {f}:\n[{v}]" for f, v in order
        )
        if ctx in seen:
            continue
        seen.add(ctx)
        out.append({"scene": f"TAT-{len(out):04d}", "context": ctx, "bridge": bridge, "holder": holder,
                    "questions": {
                        "name_clean": (f"Which vet looks after {holder}'s pet?", vet_of[bridge], "name"),
                        "digit_clean": (f"Which locker belongs to {holder}'s pet?", str(locker_of[bridge]), "digit"),
                        "name_hop": (f"Which vet looks after the {bridge}?", vet_of[bridge], "name"),
                        "digit_hop": (f"Which locker belongs to the {bridge}?", str(locker_of[bridge]), "digit")}})  # fmt: skip
    return out


@torch.no_grad()
def main(name: str, why: str, n: int) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "layers": list(LAYERS),
                "seed": SEED, "n_scenes": n, "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    items = scenes(tok, n)
    write_jsonl(out_dir / "scenes.jsonl", items)
    letters = model.letter_token_ids()
    jd = {la: lens.vectors(la, letters) for la in LAYERS}
    rd = {}
    for la in LAYERS:
        g = torch.Generator(device="cuda").manual_seed(777 + la)
        rd[la] = torch.nn.functional.normalize(torch.randn(jd[la].shape, device="cuda", generator=g), dim=-1)
    conds = {"none": {}, "jspace": {la: Remove(jd[la]) for la in LAYERS},
             "random": {la: Remove(rd[la]) for la in LAYERS}}  # fmt: skip
    prompts = []
    for it in items:
        for q, (question, answer, kind) in it["questions"].items():
            ids = S.ids(tok, S.render(tok, it["context"], question)) + (S.ids(tok, " ") if kind == "digit" else [])
            prompts.append({"scene": it["scene"], "q": q, "ids": ids, "tok": S.answer_token(tok, answer, kind)})
    t0 = time.time()
    rows = []
    by_len: dict[int, list[dict]] = {}
    for p in prompts:
        by_len.setdefault(len(p["ids"]), []).append(p)
    for group in by_len.values():
        for start in range(0, len(group), BATCH):
            chunk = group[start : start + BATCH]
            ids = torch.tensor([p["ids"] for p in chunk], device="cuda")
            for cname, edits in conds.items():
                _, logits = model.generate_batch(ids, 1, [edits] * len(chunk), first_logits=True)
                for row, p in enumerate(chunk):
                    rows.append({"scene": p["scene"], "q": p["q"], "condition": cname,
                                 "correct": int(logits[row].argmax()) == p["tok"]})  # fmt: skip
    write_jsonl(out_dir / "rows.jsonl", rows)
    summary: dict = {"seconds": round(time.time() - t0), "questions": {}}
    lines = [
        "| question | n right unedited (of all) | accuracy on those: J-space removed / random removed |",
        "|---|---|---|",
    ]
    for q in ("name_clean", "digit_clean", "name_hop", "digit_hop"):
        sel = {c: {r["scene"]: r["correct"] for r in rows if r["q"] == q and r["condition"] == c} for c in conds}
        ok = [s for s, v in sel["none"].items() if v]
        acc = {c: statistics.mean(sel[c][s] for s in ok) if ok else None for c in ("jspace", "random")}
        summary["questions"][q] = {"n": len(sel["none"]), "n_right_unedited": len(ok), "accuracy": acc}
        lines.append(
            f"| {q} | {len(ok)} ({len(sel['none'])}) | {100 * acc['jspace']:.0f}% / {100 * acc['random']:.0f}% |"
        )
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=150)
    args = ap.parse_args()
    main(args.name, args.why, args.n)
