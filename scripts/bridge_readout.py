"""bridge_readout (Zach, 2026-10-24; descriptive, beside amendment 32): can the J-lens read an entity's recalled attribute
at the entity's own mention? Module 1, read and tracked starts with a memory final (PM, TM: the passage never states the
attribute), the knock-out's eligibility; at the last token of the bridge's first mention, at every 2nd lens layer, the
J-lens and the logit lens scored over the relation's candidate answers: the share of items whose true attribute is the
top candidate (chance 1/k for k candidates), and the median rank of the true attribute among all letter tokens.

python scripts/bridge_readout.py --name N --competence C [--set jsuite_v1_facts_test_chat] [--every 2] [--batch 16]
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import subprocess
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.lens import JLens  # noqa: E402
from bridge_jspace.model import _forward_hooks, load_model  # noqa: E402
from scripts import suite_v1 as S  # noqa: E402
from scripts.ablate_v2 import bridge_positions, tasks_prompts  # noqa: E402

RES = pins.RESULTS_DIR / "bridge_readout"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
ALL_WORDS = ("PP", "PK", "PM", "PA", "MP", "MK", "MM", "MA", "TP", "TK", "TM", "TA")
ALL_WORDS_V2 = tuple(s + f for s in "PMT" for f in "PKMAN")  # v2 (amendment 34 B): memory finals PM TM PN TN read


@torch.no_grad()
def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    layers = [la for la in lens.layers if la % a.every == 0] if hasattr(lens, "layers") else list(range(0, pins.TARGETS[pins.TARGET]["n_layers"] - 1, a.every))
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "target": pins.TARGET, "set": a.set, "competence": a.competence,
                                                       "layers": layers, "git_commit": commit}, indent=2) + "\n")  # fmt: skip
    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / a.set / "items.jsonl").read_text().splitlines()}
    v2 = a.set.startswith("jsuite_v2")
    fams = ("PM", "TM", "PN", "TN") if v2 else ("PM", "TM")
    prompts = [p for p in tasks_prompts(tok, a.set, a.competence, list(ALL_WORDS_V2 if v2 else ALL_WORDS), 1000, ["clean"], "all") if p["family"] in fams]
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    jobs = []
    for p in prompts:
        it = items[p["id"]]
        pos = bridge_positions(tok, p["ids"], it["bridge"])
        if not pos:
            continue
        first = pos[0]
        while first + 1 in pos:
            first += 1
        vocab = it["answer_vocab"]
        rows = []
        for v in vocab:
            r = [int(row_of[t]) for t in {S.ids(tok, " " + v)[0], S.ids(tok, v)[0]} if int(row_of[t]) >= 0]
            rows.append(r)
        if not all(rows) or it["real"] not in vocab:
            continue
        jobs.append({**p, "pos": first, "vocab_rows": rows, "true": vocab.index(it["real"]), "k": len(vocab)})
    print(f"{len(jobs)} items (PM, TM) with a named bridge; layers {layers}", flush=True)
    stats = collections.defaultdict(lambda: collections.defaultdict(list))
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            rec = {}

            def hook_for(la):
                def hook(_m, _a, out):
                    h = out[0] if isinstance(out, tuple) else out
                    rec[la] = h[torch.arange(len(chunk)), torch.tensor([j["pos"] for j in chunk])].float()

                return hook

            with _forward_hooks([(model.layers[la], hook_for(la)) for la in layers]):
                model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
            for la in layers:
                for lens_name, M in (("jlens", lens.J(la)), ("logit", None)):
                    x = rec[la] if M is None else rec[la] @ M.T
                    lg = x @ wg.T  # [b, n letters]: lens logits up to the final norm's positive factor
                    for b, j in enumerate(chunk):
                        cand = torch.stack([lg[b, r].max() for r in j["vocab_rows"]])
                        true_row = max(j["vocab_rows"][j["true"]], key=lambda r: float(lg[b, r]))
                        rank = int((lg[b] > lg[b, true_row]).sum()) + 1
                        stats[(la, lens_name)][j["family"]].append((int(cand.argmax()) == j["true"], rank, 1 / j["k"]))
    summ = {}
    for (la, ln), fam in sorted(stats.items()):
        for f, xs in fam.items():
            summ[f"L{la}/{ln}/{f}"] = {"n": len(xs), "top_among_candidates": round(100 * sum(t for t, _, _ in xs) / len(xs), 1),
                                       "chance": round(100 * sum(c for _, _, c in xs) / len(xs), 1),
                                       "median_rank": statistics.median(r for _, r, _ in xs)}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for la in layers:
        line = f"L{la:>2}"
        for f in fams:
            for ln in ("jlens", "logit"):
                c = summ.get(f"L{la}/{ln}/{f}")
                if c:
                    line += f"  {f} {ln} top {c['top_among_candidates']:5.1f} (chance {c['chance']:4.1f}) rank {c['median_rank']:>6}"
        print(line, flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--set", default="jsuite_v1_facts_test_chat")
    ap.add_argument("--every", type=int, default=2)
    ap.add_argument("--batch", type=int, default=16)
    main(ap.parse_args())
