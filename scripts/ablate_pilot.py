"""ablate_pilot: the paper's own kind of test, removing the J-space, as a check that does not depend on the copy split
(Zach, 2026-10-20, cheap experiment before the sprint plan).

At layers 32, 36 and 40 at once, at every position, each residual loses its 25-atom J-space part (signed OMP over the
frozen J++'s letter-token vectors, the split's J-space part, here of the state itself); the control loses the same
fit over a random dictionary of the same size (seeded per layer). On unedited-correct items, read at the answer's
first token (suite_split's read):
  clean   the whole question                      hop     the last step alone (suite_v1's hop2 / hop3: a lookup in the
                                                          prompt for BL, RL; a recalled fact for BR, RR, TYPO, TRANS)
Reported per family: accuracy (top token = the answer's) and the mean change in the answer token's log-probability.
Families: BL, BR, RL, RR (suite main set), TYPO, TRANS (computed set), countries R, B (bind_recall, clean only).
Prediction from the read/write results (not a decision rule): removing the J-space hurts the recall chains more than
the lookup chains, beyond what the step alone loses.

python scripts/ablate_pilot.py --name N --why W [--n K]
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import control_split as C
from scripts import exp09_bind_recall as E
from scripts import suite_split as P
from scripts import suite_v1 as S
from scripts.exp03_brew_swaps import write_jsonl
from scripts.exp04_brew_parts import K_ATOMS, signed_omp

RESULTS = pins.RESULTS_DIR / "ablate_pilot"
LAYERS = (32, 36, 40)
BATCH = 16


class Remove:
    """Edit: every position loses its K_ATOMS-atom OMP fit over `dictionary`."""

    def __init__(self, dictionary: torch.Tensor):
        self.dictionary = dictionary

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        return h - signed_omp(self.dictionary, h, K_ATOMS).to(h.dtype)


def eligible_ids(run: str, wording_set_families: tuple[str, ...]) -> dict[str, set[str]]:
    ok: dict[str, dict[str, list[bool]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for line in (S.RESULTS / run / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["family"] in wording_set_families:
            ok[r["family"]][r["id"]].append(r["correct"])
    return {f: {i for i, v in d.items() if all(v)} for f, d in ok.items()}


def prompts(tok, n: int) -> list[dict]:
    out = []
    sets = (("A", "competence_v2", ("BL", "BR", "RL", "RR")), ("C", "competence_computed_v1", ("TYPO", "TRANS")))
    for wording, run, fams in sets:
        good = eligible_ids(run, fams)
        for fam in fams:
            items = [it for it in S.load(fam, wording) if it["id"] in good[fam]][:n]
            for it in items:
                prep = P.prepare(it, tok)
                out.append({"family": fam, "id": it["id"], "kind": "clean", "ids": prep["read_ids"]["clean"],
                            "tok": prep["tok_A"]})  # fmt: skip
                hop = it.get("hop3") or it["hop2"]
                text = S.render(tok, hop.get("context", it["context"]), hop["question"])
                ids = S.ids(tok, text) + (S.ids(tok, " ") if hop["kind"] == "digit" else [])
                out.append({"family": fam, "id": it["id"], "kind": "hop", "ids": ids,
                            "tok": S.answer_token(tok, hop["answer"], hop["kind"])})  # fmt: skip
    picked = [json.loads(line)["id"] for line in (C.RESULTS / "map_v1" / "cases.jsonl").read_text().splitlines()]
    items = E.ITEM_SETS["bind_recall"][2]()
    by_uid = {E.uid(it, i): (i, it) for i, it in enumerate(items)}
    seen: collections.Counter = collections.Counter()
    for uid in picked:
        index, item = by_uid[uid]
        if seen[item["family"]] >= n:
            continue
        seen[item["family"]] += 1
        prep = E.prepare(item, index, tok, "chat_prefill")
        out.append({"family": f"country-{item['family']}", "id": uid, "kind": "clean", "ids": prep["ids"]["clean"],
                    "tok": S.answer_token(tok, item["answer"], "word")})  # fmt: skip
    return out


@torch.no_grad()
def main(name: str, why: str, n: int) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    manifest = {"run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "layers": list(LAYERS),
                "k_atoms": K_ATOMS, "n_per_family": n, "doc": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    jdict = {la: lens.vectors(la, letters) for la in LAYERS}
    rdict = {}
    for la in LAYERS:
        g = torch.Generator(device="cuda").manual_seed(777 + la)
        rdict[la] = torch.nn.functional.normalize(torch.randn(jdict[la].shape, device="cuda", generator=g), dim=-1)
    conditions = {"none": {}, "jspace": {la: Remove(jdict[la]) for la in LAYERS},
                  "random": {la: Remove(rdict[la]) for la in LAYERS}}  # fmt: skip
    t0 = time.time()
    ps = prompts(tok, n)
    print(len(ps), "prompts", flush=True)
    rows = []
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in ps:
        by_len[len(p["ids"])].append(p)
    for group in by_len.values():
        for start in range(0, len(group), BATCH):
            chunk = group[start : start + BATCH]
            ids = torch.tensor([p["ids"] for p in chunk], device="cuda")
            for cname, edits in conditions.items():
                _, logits = model.generate_batch(ids, 1, [edits] * len(chunk), first_logits=True)
                logp = logits.log_softmax(-1)
                for row, p in enumerate(chunk):
                    rows.append({"family": p["family"], "id": p["id"], "kind": p["kind"], "condition": cname,
                                 "correct": int(logits[row].argmax()) == p["tok"], "logp": float(logp[row, p["tok"]])})  # fmt: skip
    write_jsonl(out_dir / "rows.jsonl", rows)
    summary: dict = {"seconds": round(time.time() - t0), "families": {}}
    lines = ["| family | step | n | accuracy: none / J-space removed / random removed | log p change: J-space / random |",
             "|---|---|---|---|---|"]  # fmt: skip
    for fam in dict.fromkeys(r["family"] for r in rows):
        for kind in ("clean", "hop"):
            sel = {
                c: [r for r in rows if r["family"] == fam and r["kind"] == kind and r["condition"] == c]
                for c in conditions
            }
            if not sel["none"]:
                continue
            base = {r["id"]: r["logp"] for r in sel["none"]}
            acc = {c: statistics.mean(r["correct"] for r in v) for c, v in sel.items()}
            dlp = {c: statistics.mean(r["logp"] - base[r["id"]] for r in v) for c, v in sel.items() if c != "none"}
            summary["families"][f"{fam}/{kind}"] = {"n": len(sel["none"]), "accuracy": acc, "dlogp": dlp}
            lines.append(f"| {fam} | {kind} | {len(sel['none'])} | {100 * acc['none']:.0f}% / {100 * acc['jspace']:.0f}% / "
                         f"{100 * acc['random']:.0f}% | {dlp['jspace']:+.2f} / {dlp['random']:+.2f} |")  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--n", type=int, default=100)
    args = ap.parse_args()
    main(args.name, args.why, args.n)
