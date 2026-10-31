"""nn_probe_v4 (Zach, 2026-10-29, prereg amendment 58 note 23): how readable is the bridge at the description's end to a
trained read-out, and does it generalise to another description of the same person? A ceiling for the lens readout
(note 14); v3's leave-one-description-out probe is scripts/nn_probe.py (note 9).

Prompts: every v4 MP and MM item (the main question), the state at the description's last token at every 2nd layer.
Split by description, two folds: for a bridge with >= 2 distinct descriptions in the set, the items using its second
description (sorted) are held out and the rest train, then its first (note 23 addendum); every held-out item is scored once
per fold it is held out in; extra sets (--extra-sets, new seeds of the same people and descriptions) only train, and their
items with a held-out description are dropped (note 23 addendum 2). Control: the same read-outs trained on permuted labels (seed 1). 95% bootstrap over bridges. Read-outs per layer, each scored top-1 among the item's relation's bridges (the readout's
candidates, chance 1/k):
  nc   nearest class mean (cosine, train-mean centred)
  lr   multinomial logistic regression over every bridge (standardised; Adam, weight decay, fixed steps, seed 0)
The lens's top-1 on the same held-out gated items and layers comes from the readout run's rows (nn_readout --items v4).

python scripts/nn_probe_v4.py --name N --why W --competence C --cv-h1 CV [--set jsuite_v4_test_chat] [--every 2] [--readout R]
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.model import _forward_hooks, load_model  # noqa: E402
from scripts import jswap as JS  # noqa: E402
from scripts.ablate_v2 import bridge_positions  # noqa: E402

RES = pins.RESULTS_DIR / "nn_probe_v4"


@torch.no_grad()
def states(a, model, tok, items, layers):
    from scripts.nn_swap import build_prompt

    jobs = []
    for set_name in [a.set, *a.extra_sets]:  # note 23 addendum 2: extra passage sets (new seeds) add training examples
        its = items if set_name == a.set else {json.loads(l)["id"]: json.loads(l) for l in (JS.DATA / set_name / "items.jsonl").read_text().splitlines()}
        for i, it in sorted(its.items()):
            if it.get("set_version") != "v4" or it["word"] not in ("MP", "MM"):
                continue
            p = build_prompt(tok, it, set_name)
            pos = bridge_positions(tok, p["ids"], it["start_desc"])
            if pos:
                jid = i if set_name == a.set else f"{set_name}|{i}"
                jobs.append({"id": jid, "ids": p["ids"], "pos": pos[-1], "bridge": it["bridge"], "rel": it["relation"], "desc": it["start_desc"],
                             "word": it["word"], "main": set_name == a.set})  # fmt: skip
    if a.limit:
        jobs = jobs[: a.limit]
    by_len = collections.defaultdict(list)
    for j in jobs:
        by_len[len(j["ids"])].append(j)
    out = {}
    for group in by_len.values():
        for s in range(0, len(group), a.batch):
            chunk = group[s : s + a.batch]
            rec = {}

            def hook_for(la):
                def hook(_m, _a, o):
                    rec[la] = (o[0] if isinstance(o, tuple) else o).float()

                return hook

            ids = torch.tensor([j["ids"] for j in chunk], device="cuda")
            with _forward_hooks([(model.layers[la], hook_for(la)) for la in layers]):
                model.hf(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
            for b, j in enumerate(chunk):
                out[j["id"]] = torch.stack([rec[la][b, j["pos"]] for la in layers]).half().cpu()
    return jobs, out


def main(a) -> None:
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out_dir / "manifest.json").write_text(json.dumps({"run": a.name, "why": a.why, "target": pins.TARGET, "model": pins.model_pin(), "set": a.set,
                                                       "competence": a.competence, "cv_h1": a.cv_h1, "readout": a.readout, "every": a.every,
                                                       "steps": a.steps, "seed": 0, "limit": a.limit, "extra_sets": a.extra_sets, "git_commit": commit, "git_state": pins.git_state()}, indent=2) + "\n")  # fmt: skip
    model = load_model()
    tok = model.tokenizer
    items = {json.loads(line)["id"]: json.loads(line) for line in (JS.DATA / a.set / "items.jsonl").read_text().splitlines()}
    layers = [la for la in range(len(model.layers)) if la % a.every == 0]
    jobs, st = states(a, model, tok, items, layers)
    from scripts.nn_swap import v4_split

    ok = {i for i, s in v4_split(a.competence, a.cv_h1, a.set).items() if s == "ok"}
    descs = collections.defaultdict(set)
    for j in jobs:
        descs[j["bridge"]].add(j["desc"])
    bridges = sorted({j["bridge"] for j in jobs})
    bi = {b: k for k, b in enumerate(bridges)}
    cands = collections.defaultdict(set)
    for j in jobs:
        cands[j["rel"]].add(bi[j["bridge"]])

    def fit_eval(train, test, li, shuffle):  # per-item hits (nc, lr) on test at layer index li
        xtr = torch.stack([st[j["id"]][li] for j in train]).float().cuda()
        xte = torch.stack([st[j["id"]][li] for j in test]).float().cuda()
        y_tr = torch.tensor([bi[j["bridge"]] for j in train], device="cuda")
        if shuffle:  # the shuffled-label control: train labels permuted (seed 1)
            y_tr = y_tr[torch.randperm(len(y_tr), generator=torch.Generator().manual_seed(1)).cuda()]
        y_te = torch.tensor([bi[j["bridge"]] for j in test], device="cuda")
        mask = torch.full((len(test), len(bridges)), float("-inf"), device="cuda")
        for r, j in enumerate(test):
            mask[r, sorted(cands[j["rel"]])] = 0.0
        mu, sd = xtr.mean(0), xtr.std(0) + 1e-4
        ctr, cte = xtr - mu, xte - mu  # nearest class mean (cosine, centred)
        means = torch.zeros(len(bridges), ctr.shape[1], device="cuda").index_add_(0, y_tr, ctr)
        cnt = torch.zeros(len(bridges), device="cuda").index_add_(0, y_tr, torch.ones_like(y_tr, dtype=torch.float))
        means = torch.nn.functional.normalize(means / cnt.clamp_min(1)[:, None], dim=-1)
        nc = (torch.nn.functional.normalize(cte, dim=-1) @ means.T + mask).argmax(-1)
        g = torch.Generator(device="cuda").manual_seed(0)  # logistic regression
        W = (torch.randn(xtr.shape[1], len(bridges), device="cuda", generator=g) * 0.01).requires_grad_()
        bvec = torch.zeros(len(bridges), device="cuda", requires_grad=True)
        opt = torch.optim.Adam([W, bvec], lr=1e-2, weight_decay=1e-2)
        ztr, zte = (xtr - mu) / sd, (xte - mu) / sd
        with torch.enable_grad():
            for _ in range(a.steps):
                opt.zero_grad()
                torch.nn.functional.cross_entropy(ztr @ W + bvec, y_tr).backward()
                opt.step()
        with torch.no_grad():
            lr = (zte @ W + bvec + mask).argmax(-1)
        return (nc == y_te).tolist(), (lr == y_te).tolist()

    # two folds: hold out each bridge's second description (sorted), then its first; every bridge with >= 2 descriptions
    folds = []
    for f in (1, 0):
        held = {b: sorted(d)[f] for b, d in descs.items() if len(d) >= 2}
        folds.append(([j for j in jobs if held.get(j["bridge"]) != j["desc"]], [j for j in jobs if j["main"] and held.get(j["bridge"]) == j["desc"]]))
    tested = [j for _, te in folds for j in te]
    chance = sum(1 / len(cands[j["rel"]]) for j in tested) / max(1, len(tested))
    print(f"{len(jobs)} prompts, {len(bridges)} bridges; folds train/test {[(len(tr), len(te)) for tr, te in folds]}; layers {layers}", flush=True)
    assert tested, "no held-out description: nothing to score"

    def boot(hits_by_bridge):
        rng, keys, out = __import__("random").Random(0), sorted(hits_by_bridge), []
        for _ in range(1000):
            xs = [h for k in (rng.choice(keys) for _ in keys) for h in hits_by_bridge[k]]
            out.append(100 * sum(xs) / len(xs))
        out.sort()
        return [round(out[25], 1), round(out[974], 1)]

    rows, summ = [], {"folds": [(len(tr), len(te)) for tr, te in folds], "n_test": len(tested),
                      "n_test_gated": sum(j["id"] in ok for j in tested), "chance": round(100 * chance, 1), "layers": {}}  # fmt: skip
    for li, la in enumerate(layers):
        hits = collections.defaultdict(list)  # (readout, control) -> [(job, hit)]
        for tr, te in folds:
            for shuffle in (False, True):
                nch, lrh = fit_eval(tr, te, li, shuffle)
                hits[("nc", shuffle)] += list(zip(te, nch))
                hits[("lr", shuffle)] += list(zip(te, lrh))
        rec = {}
        for (nm_, shuffle), hs in sorted(hits.items()):
            key = nm_ + ("_shuffled" if shuffle else "")
            g = [h for j, h in hs if j["id"] in ok]
            byb = collections.defaultdict(list)
            for j, h in hs:
                if j["id"] in ok:
                    byb[j["bridge"]].append(h)
            rec[key] = {"all": round(100 * sum(h for _, h in hs) / len(hs), 1), "gated": round(100 * sum(g) / len(g), 1) if g else None,
                        "gated_ci": boot(byb) if byb else None}  # fmt: skip
            if not shuffle:
                for j, h in hs:
                    rows.append({"id": j["id"], "word": j["word"], "rel": j["rel"], "bridge": j["bridge"], "layer": la, "readout": nm_,
                                 "gated": j["id"] in ok, "hit": bool(h)})  # fmt: skip
        summ["layers"][f"L{la}"] = rec
        print(f"L{la:2d}  " + "  ".join(f"{k} {v['gated']} {v['gated_ci']}" for k, v in rec.items()) + f"  chance {100 * chance:.1f}", flush=True)
    if a.readout:  # the lens's top-1 on the same held-out gated items (the readout's per-item rows)
        test_ok = {j["id"] for j in tested if j["id"] in ok}
        lens = collections.defaultdict(list)
        for line in (pins.RESULTS_DIR / "nn_readout" / a.readout / "rows.jsonl").read_text().splitlines():
            r = json.loads(line)
            if r["id"] in test_ok and r["site"] == "desc_end" and r["what"] == "bridge":
                lens[(r["lens"], r["layer"])].append(r["rank"] == 1)
        for (ln, la), v in sorted(lens.items()):
            summ["layers"].setdefault(f"L{la}", {})[f"lens_{ln}_gated"] = round(100 * sum(v) / len(v), 1)
    (out_dir / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    for k, v in summ["layers"].items():
        print(k, json.dumps(v))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--cv-h1", required=True)
    ap.add_argument("--set", default="jsuite_v4_test_chat")
    ap.add_argument("--readout", default=None, help="the nn_readout --items v4 run for the lens comparison")
    ap.add_argument("--every", type=int, default=2)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--limit", type=int, default=0, help="a smoke: the first N prompts")
    ap.add_argument("--extra-sets", nargs="*", default=[], help="note 23 addendum 2: more v4 passage sets for training (held-out descriptions never trained on)")
    main(ap.parse_args())
