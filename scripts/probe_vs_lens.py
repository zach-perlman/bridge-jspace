"""probe_vs_lens (Zach, 2026-10-23, prereg amendment 22): how much of an intermediate the J-lens shows, against a linear
probe as the ceiling, layer by layer.

For a tasks_v2 natural set and its competence run: the eligible items of the given words (tasks_v2.eligible, as
ablate_v2), unedited, residual stream at the last prompt position (block outputs) every --every layers. The target is a
number per item (--target x: ctxcomp's X). Per word and layer:
  probe   held-out accuracy of a linear probe for the target (standardise, PCA to --pca dims, multinomial logistic
          regression with L2), 5-fold cross-validation over scenes
  jlens   accuracy of the J-lens read: the class whose surface tokens (digit, " digit", number word in three cases)
          score highest in the lens logits (no training)
  logit   the same read with the logit lens (J = identity)
  jshare  the share of the class means' spread (around their mean) inside the span of the J-lens vectors of every
          class surface token at that layer (rand: the same for a random subspace of equal dimension)
Descriptive. Writes results/probe_vs_lens/NAME.json.

python scripts/probe_vs_lens.py --name N --set ctxcomp_v1_chat --competence C --words PR PP PM ... [--every 2]
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import subprocess
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from scripts import ablate_v2 as AV  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402

RESULTS = pins.RESULTS_DIR / "probe_vs_lens"
WORDS_NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def surface_ids(tok, n: int) -> list[int]:
    """Single-token surfaces of the number n: "5", " 5", "five", " five", "Five", " Five"."""
    out = set()
    for s in (str(n), " " + str(n), WORDS_NUM[n], " " + WORDS_NUM[n], WORDS_NUM[n].capitalize(), " " + WORDS_NUM[n].capitalize()):
        ids = tok(s, add_special_tokens=False).input_ids
        if len(ids) == 1:
            out.add(ids[0])
    return sorted(out)


def probe_acc(X: torch.Tensor, y: torch.Tensor, groups: list[str], pca: int, folds: int = 5, l2: float = 1e-2) -> float:
    """Held-out accuracy of standardise -> PCA -> multinomial logistic regression, folds over groups (scenes)."""
    ug = sorted(set(groups))
    random.Random(0).shuffle(ug)
    fold_of = {g: i % folds for i, g in enumerate(ug)}
    classes = sorted(set(y.tolist()))
    yi = torch.tensor([classes.index(v) for v in y.tolist()])
    right = 0
    for f in range(folds):
        te = torch.tensor([fold_of[g] == f for g in groups])
        tr = ~te
        if te.sum() == 0 or tr.sum() < 10:
            continue
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-6
        Xtr, Xte = (X[tr] - mu) / sd, (X[te] - mu) / sd
        k = min(pca, Xtr.shape[0] - 1)
        U, S, V = torch.pca_lowrank(Xtr, q=k, center=False)
        Ztr, Zte = Xtr @ V[:, :k], Xte @ V[:, :k]
        W = torch.zeros(k, len(classes), requires_grad=True)
        b = torch.zeros(len(classes), requires_grad=True)
        opt = torch.optim.LBFGS([W, b], max_iter=200, line_search_fn="strong_wolfe")

        def closure():
            opt.zero_grad()
            loss = torch.nn.functional.cross_entropy(Ztr @ W + b, yi[tr]) + l2 * (W**2).sum()
            loss.backward()
            return loss

        opt.step(closure)
        right += int(((Zte @ W + b).argmax(1) == yi[te]).sum())
    return right / len(groups)


@torch.no_grad()
def main(args) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(args.name)
    out = RESULTS / f"{args.name}.json"
    assert not out.exists(), f"{out} exists; results are written once"
    torch.backends.cuda.matmul.allow_tf32 = True
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    model = load_model()
    tok = model.tokenizer
    prompts = AV.tasks_prompts(tok, args.set, args.competence, args.words, 10**6, ["clean"], "all")
    items = {it["id"]: it for it in T.load(args.set)}
    layers = list(range(0, pins.N_LAYERS, args.every))
    lens = JLens(model, pins.FROZEN_LENS)
    lens_layers = set(lens.source_layers)
    gain = model.norm_gain()
    classes = sorted({items[p["id"]][args.target] for p in prompts})
    sids = {c: surface_ids(tok, c) for c in classes}
    all_ids = sorted({i for c in classes for i in sids[c]})
    Wc = model.hf.lm_head.weight[all_ids].float() * gain  # [n_ids, d]
    col = {i: j for j, i in enumerate(all_ids)}
    print(len(prompts), "prompts;", len(layers), "layers; classes", classes, {c: len(v) for c, v in sids.items()}, flush=True)

    # residuals at the last prompt position, every chosen layer (block outputs = hidden_states[l + 1])
    acts = {la: [] for la in layers}
    t0 = time.time()
    by_len = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    order = []
    for group in by_len.values():
        for s in range(0, len(group), args.batch):
            chunk = group[s : s + args.batch]
            ids = torch.tensor([p["ids"] for p in chunk], device="cuda")
            hs = model.hf(input_ids=ids, output_hidden_states=True, use_cache=False, logits_to_keep=1).hidden_states
            for la in layers:
                acts[la].append(hs[la + 1][:, -1].float().cpu())
            order += chunk
    acts = {la: torch.cat(v) for la, v in acts.items()}
    print(f"activations {time.time() - t0:.0f}s", flush=True)

    res: dict = {"words": {}}
    rng = torch.Generator().manual_seed(0)
    for w in args.words:
        idx = [i for i, p in enumerate(order) if p["family"] == w]
        if len(idx) < 20:
            continue
        y = torch.tensor([items[order[i]["id"]][args.target] for i in idx])
        groups = [items[order[i]["id"]]["scene"] for i in idx]
        rows = []
        for la in layers:
            X = acts[la][idx]
            row = {"layer": la, "n": len(idx), "probe": round(probe_acc(X, y, groups, args.pca), 3)}
            for name, J in (("jlens", lens.J(la).float() if la in lens_layers else None), ("logit", None)):
                if name == "jlens" and J is None:
                    continue
                H = X.cuda() if J is None else (X.cuda() @ J.T)
                L = H @ Wc.T  # [n, n_ids]
                score = torch.stack([L[:, [col[i] for i in sids[c]]].max(1).values for c in classes], 1)
                row[name] = round(float((torch.tensor(classes, device="cuda")[score.argmax(1)] == y.cuda()).float().mean()), 3)
            if la in lens_layers:
                J = lens.J(la).float()
                U = Wc @ J  # J-lens vectors of the class surface tokens (rows)
                Q, _ = torch.linalg.qr(U.T)  # [d, k] orthonormal basis of their span
                means = torch.stack([X[y == c].mean(0) for c in classes]).cuda()
                M = means - means.mean(0)
                row["jshare"] = round(float((M @ Q).pow(2).sum() / M.pow(2).sum()), 4)
                R, _ = torch.linalg.qr(torch.randn(M.shape[1], Q.shape[1], generator=rng).cuda())
                row["rand"] = round(float((M @ R).pow(2).sum() / M.pow(2).sum()), 4)
            rows.append(row)
        res["words"][w] = rows
        best = max(rows, key=lambda r: r["probe"])
        print(f"{w}: n {len(idx)}; best probe {best['probe']} at L{best['layer']}; " + "; ".join(
            f"L{r['layer']} p {r['probe']:.2f} j {r.get('jlens', float('nan')):.2f} l {r['logit']:.2f} sh {r.get('jshare', float('nan')):.3f}"
            for r in rows if r["layer"] % (4 * args.every) == 0), flush=True)  # fmt: skip
    res.update({"run": args.name, "set": args.set, "competence": args.competence, "target": args.target, "every": args.every,
                "pca": args.pca, "git_commit": commit, "model": pins.model_pin(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256],
                "classes": classes, "surface_ids": {str(c): v for c, v in sids.items()}, "why": args.why,
                "seconds": round(time.time() - t0)})  # fmt: skip
    RESULTS.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--set", required=True)
    ap.add_argument("--competence", required=True)
    ap.add_argument("--words", nargs="+", required=True)
    ap.add_argument("--target", default="x")
    ap.add_argument("--every", type=int, default=2)
    ap.add_argument("--pca", type=int, default=64)
    ap.add_argument("--batch", type=int, default=16)
    main(ap.parse_args())
