"""Which J++ atoms does the 25-atom OMP pick for a country copy (control_split R, layer 36), and does barring the words
work? A debug on the first 3 R cases of control_split/map_v1. python scripts/debug_omp_atoms.py"""

import json
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.lens import JLens
from bridge_jspace.model import load_model
from scripts import control_split as C
from scripts import exp09_bind_recall as E

LAYER = 36


@torch.no_grad()
def main() -> None:
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    row_of = {int(t): i for i, t in enumerate(letters.tolist())}
    dictionary = lens.vectors(LAYER, letters)
    items = E.ITEM_SETS["bind_recall"][2]()
    lines = (C.RESULTS / "map_v1" / "cases.jsonl").read_text().splitlines()
    picked = {json.loads(line)["id"] for line in lines[:200]}
    done = 0
    for index, item in enumerate(items):
        uid = E.uid(item, index)
        if uid not in picked or item["family"] != "R":
            continue
        prep = E.prepare(item, index, tok, "chat_prefill")
        pos = prep["groups"]["question"]
        h = {
            s: model.run(torch.tensor([prep["ids"][s]], device="cuda"), record=(LAYER,))[1][LAYER]
            for s in ("clean", "cf")
        }
        delta = (h["cf"] - h["clean"])[pos]
        words = {
            i
            for w in (item["bridge"], item["target"], item["answer"], item["target_answer"])
            for i in model.surface_ids(w)
        }
        banned = sorted(row_of[i] for i in words if i in row_of)
        print("==", uid, item["bridge"], "->", item["target"], "| banned rows", len(banned))
        r = int(delta.norm(dim=-1).argmax())
        x = delta[r : r + 1].float()
        approx = torch.zeros_like(x)
        chosen: list[int] = []
        for _ in range(C.K_ATOMS):
            scores = ((x - approx) @ dictionary.T).abs()[0]
            if chosen:
                scores[chosen] = -1
            chosen.append(int(scores.argmax()))
            atoms = dictionary[chosen].double()
            eye = torch.eye(len(chosen), device="cuda", dtype=torch.float64)
            coef = torch.linalg.solve(atoms @ atoms.T + 1e-8 * eye, atoms @ x[0].double())
            approx = (coef @ atoms).float()[None]
        print("   position", r, "of", len(pos), "| top atoms:", [tok.decode([int(letters[j])]) for j in chosen[:15]])
        share = float(approx.norm() ** 2 / x.norm() ** 2)
        print("   any word among the 25:", any(j in banned for j in chosen), "| share", round(share, 3))
        pair = torch.tensor([model.concept_token(item["bridge"]), model.concept_token(item["target"])], device="cuda")
        own = C.lens2_part(delta, lens.vectors(LAYER, pair))
        cos = float(torch.nn.functional.cosine_similarity(own[r : r + 1], approx))
        print(
            "   own-word share",
            round(float(own.norm() ** 2 / delta.norm() ** 2), 4),
            "| cos with J-part",
            round(cos, 3),
        )
        done += 1
        if done == 3:
            break


if __name__ == "__main__":
    main()
