"""nn_probe (Zach, 2026-10-28, prereg amendment 58 note 9, item 4): is the never-named bridge linearly decodable where
it would be computed? A trained linear probe, leave-one-description-out.

collect (GPU): residuals at the last token of the bridge's description in the question, every 4th layer, for
  - training prompts: M and W starts (every final; up to 4 prompts per (bridge, description)) and RM's hop 1 alone
    ("Which novelist wrote Arrow of God?", same passage);
  - test prompts: RM (never named), every item.
  Written to results/nn_probe/NAME/acts_L{layer}.npy (fp16) and meta.jsonl.
fit (CPU): per relation, layer and held-out description d (0 / 1): a multinomial logistic regression over the
  relation's bridges (standardized features, L2 weight 1e-3, L-BFGS), trained on the training prompts that use the
  other description, tested on the RM prompts that use d (so no test description's text is ever seen in training).
  Also tested on the M / W prompts that use d (the named upper bound). Writes per-item predictions (preds.jsonl) and
  top-1 accuracy per relation x layer (summary.json); chance 1/k.

python scripts/nn_probe.py collect --name N --competence C [--set jsuite_v3_test_chat] [--every 4] [--batch 16]
python scripts/nn_probe.py fit --name N
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402

RES = pins.RESULTS_DIR / "nn_probe"
TRAIN_WORDS = ("MP", "MK", "MM", "MA", "MN", "MH", "MC", "MD", "ME", "MF", "MG", "WK", "WM", "WA", "WN")


@torch.no_grad()
def collect(a) -> None:
    from bridge_jspace.model import _forward_hooks, load_model
    from scripts import jswap as JS
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T
    from scripts.ablate_v2 import bridge_positions

    out = RES / a.name
    assert not (out / "meta.jsonl").exists(), f"{out} has activations; runs are written once"
    out.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    layers = list(range(0, pins.TARGETS[pins.TARGET]["n_layers"], a.every))
    (out / "manifest.json").write_text(json.dumps({"run": a.name, "target": pins.TARGET, "model": pins.model_pin(), "set": a.set, "competence": a.competence,
                                                   "layers": layers, "train_words": TRAIN_WORDS, "per_description": a.per_description, "seed": "random.Random(0)",
                                                   "git_commit": commit, "git_state": pins.git_state()}, indent=2) + "\n")  # fmt: skip
    items = [json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()]
    rng = random.Random(0)
    by_desc = collections.defaultdict(list)
    for it in items:
        if it.get("module") == "facts" and it["word"] in TRAIN_WORDS and it.get("desc_index") is not None:
            by_desc[(it["bridge"], it["desc_index"])].append(it)
    jobs = []
    for key in sorted(by_desc):
        for it in rng.sample(by_desc[key], min(a.per_description, len(by_desc[key]))):
            jobs.append(("train_mw", it, it["question"], it["start_desc"]))
    for it in items:
        if it.get("module") == "facts" and it["word"] == "RM":
            jobs.append(("test_rm", it, it["question"], it["start_desc"]))
            clause = re.split(r" (?:who|that) ", it["start_desc"], maxsplit=1)[-1]
            jobs.append(("train_hop1", it, it["steps"][0]["question"], clause))
    if a.limit:  # a smoke: the first N jobs per role
        seen = collections.Counter()
        jobs = [j for j in jobs if (seen.update([j[0]]) or True) and seen[j[0]] <= a.limit]
    rows, prompts = [], []
    for role, it, q, desc in jobs:
        ids = S.ids(tok, T.render(tok, {**it, "_question": q, "_kind": it["kind"] if role != "train_hop1" else it["steps"][0]["kind"]}))
        pos = bridge_positions(tok, ids, desc)
        if not pos:
            continue
        rows.append({"role": role, "id": it["id"], "word": it["word"], "relation": it["relation"], "bridge": it["bridge"], "desc_index": it["desc_index"],
                     "level": it["level"]})  # fmt: skip
        prompts.append((ids, pos[-1]))
    print(f"{len(rows)} prompts: {dict(collections.Counter(r['role'] for r in rows))}; layers {layers}", flush=True)
    d = model.hf.config.hidden_size if hasattr(model.hf.config, "hidden_size") else None
    acts = {la: None for la in layers}
    order = sorted(range(len(prompts)), key=lambda i: len(prompts[i][0]))
    by_len = collections.defaultdict(list)
    for i in order:
        by_len[len(prompts[i][0])].append(i)
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            ids = torch.tensor([prompts[i][0] for i in chunk], device="cuda")
            rec = {}

            def hook_for(la):
                def hook(_m, _a, out_):
                    h = out_[0] if isinstance(out_, tuple) else out_
                    rec[la] = h[torch.arange(len(chunk)), torch.tensor([prompts[i][1] for i in chunk])].float().cpu()

                return hook

            with _forward_hooks([(model.layers[la], hook_for(la)) for la in layers]):
                model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
            for la in layers:
                if acts[la] is None:
                    d = rec[la].shape[1]
                    acts[la] = np.zeros((len(prompts), d), dtype=np.float16)
                acts[la][chunk] = rec[la].numpy().astype(np.float16)
    for la in layers:
        np.save(out / f"acts_L{la}.npy", acts[la])
    (out / "meta.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"wrote {len(rows)} x {d} activations at {len(layers)} layers", flush=True)


def fit_lr(X: torch.Tensor, y: torch.Tensor, k: int, wd: float = 1e-3, iters: int = 200) -> torch.nn.Linear:
    torch.manual_seed(0)
    lin = torch.nn.Linear(X.shape[1], k).double()
    opt = torch.optim.LBFGS(lin.parameters(), lr=1, max_iter=iters, history_size=20, line_search_fn="strong_wolfe")

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(lin(X), y) + wd * lin.weight.pow(2).sum()
        loss.backward()
        return loss

    opt.step(closure)
    return lin


def fit(a) -> None:
    out = RES / a.name
    rows = [json.loads(line) for line in (out / "meta.jsonl").read_text().splitlines()]
    layers = json.loads((out / "manifest.json").read_text())["layers"]
    torch.set_num_threads(16)
    preds, summ = [], {}
    for la in layers:
        A = torch.from_numpy(np.load(out / f"acts_L{la}.npy").astype(np.float64))
        for rel in sorted({r["relation"] for r in rows}):
            classes = sorted({r["bridge"] for r in rows if r["relation"] == rel})
            ci = {b: i for i, b in enumerate(classes)}
            for dd in (0, 1):
                tr = [i for i, r in enumerate(rows) if r["relation"] == rel and r["role"] != "test_rm" and r["desc_index"] != dd]
                te = [i for i, r in enumerate(rows) if r["relation"] == rel and r["role"] == "test_rm" and r["desc_index"] == dd]
                tn = [i for i, r in enumerate(rows) if r["relation"] == rel and r["role"] == "train_mw" and r["desc_index"] == dd]
                if not tr or not te:
                    continue
                mu, sd = A[tr].mean(0), A[tr].std(0) + 1e-6
                lin = fit_lr((A[tr] - mu) / sd, torch.tensor([ci[rows[i]["bridge"]] for i in tr]), len(classes))
                with torch.no_grad():
                    for split, idx in (("rm", te), ("named", tn)):
                        if not idx:
                            continue
                        pr = lin((A[idx] - mu) / sd).softmax(-1)
                        top = pr.argmax(-1).tolist()
                        for i, t, p_true in zip(idx, top, pr[torch.arange(len(idx)), torch.tensor([ci[rows[i]["bridge"]] for i in idx])].tolist(), strict=True):
                            preds.append({"layer": la, "split": split, "id": rows[i]["id"], "relation": rel, "bridge": rows[i]["bridge"],
                                          "pred": classes[t], "right": classes[t] == rows[i]["bridge"], "p_true": round(p_true, 4), "k": len(classes)})  # fmt: skip
        print(f"L{la} done", flush=True)
    cells = collections.defaultdict(list)
    for p in preds:
        cells[(p["split"], p["relation"], p["layer"])].append(p)
        cells[(p["split"], "all", p["layer"])].append(p)
    for (split, rel, la), ps in sorted(cells.items()):
        summ[f"{split}/{rel}/L{la}"] = {"n": len(ps), "top1": round(100 * sum(p["right"] for p in ps) / len(ps), 1),
                                        "chance": round(100 * sum(1 / p["k"] for p in ps) / len(ps), 1)}  # fmt: skip
    (out / "preds.jsonl").write_text("".join(json.dumps(p) + "\n" for p in preds))
    (out / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for split in ("rm", "named"):
        print(split, " ".join(f"L{la} {summ[f'{split}/all/L{la}']['top1']:.0f}" for la in layers if f"{split}/all/L{la}" in summ),
              f"(chance ~{summ.get(f'{split}/all/L{layers[0]}', {}).get('chance')})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["collect", "fit"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--competence", default=None)
    ap.add_argument("--set", default="jsuite_v3_test_chat")
    ap.add_argument("--every", type=int, default=4)
    ap.add_argument("--per-description", type=int, default=4)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0, help="collect: first N prompts per role (a smoke)")
    a = ap.parse_args()
    collect(a) if a.cmd == "collect" else fit(a)
