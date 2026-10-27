"""pointer_probe (D3b, batch 3): can "which statement is asked" be read from the tokens after the question?

Background (UNVERIFIED): d3b_slot_direction_main_27b fitted per-token class means of the hidden states at the tokens
after the question (the pointer direction is the difference of two of them) on 197 fit items, and read the asked
statement back with a nearest-class-mean classifier at only 39% [33, 46] at layer 48 (5 statements, chance 20%),
although pushing along the same means steers the lookup (37%). "Steers but is hardly readable" may be a small-sample
effect: 197 items, ~40 per class, 5120 dimensions per token.

Design: pointer_v1's fit set (memory → prompt; animals and elements; all 200 scenes per domain, no filter): the hidden
states at every token after the question (instruction, template, 'Answer:'), layers 40-52, labelled by the asked
statement (1-5); the unedited answer read is recorded (right or wrong). Classifier: the nearest per-token class mean
(squared distance summed over the tokens), i.e. the means the pointer direction is built from.
  cv           5-fold cross-validated over items (seed 0): all items, answered-right items, per domain; the same with
               shuffled labels (seed 1) as the null
  same means   the class means of d3b_slot_direction_main_27b itself (cache/pointer_fit/<run>/fits.pt, if present),
               applied to the fit items whose queried entity was held out of that fit (never seen by those means)
Decision rule (fixed before the run): at layer 48, cross-validated accuracy on all items (n ~ 400): "readable" iff its
Wilson 95% lower bound >= 0.60 (the threshold d3b_slot_direction_main_27b's H-slot predicted); "hardly readable"
(the first run's 39% survives) iff its upper bound < 0.60; otherwise in between. Valid only if the shuffled-label null
stays within 10 points of chance (20%). Per domain, per layer, answered-right only and the same-means check are
reported, with an entity-cluster bootstrap (queried entities resampled within domain).

Stages:  run --name N --why W [--fit-limit K] [--layers ...] [--same-means RUN]   figures --name N   examples --name N
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from scripts import pointer_fit as PF
from scripts import pointer_swap as PS
from scripts import suite_v1 as S

EXP = "pointer_probe"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {"domains": ["animals", "elements"], "layers": [40, 42, 44, 46, 48, 50, 52],
                            "primary_layer": 48, "fit_limit": None, "same_means": "d3b_slot_direction_main_27b"}  # fmt: skip
FOLDS, CV_SEED, SHUFFLE_SEED, BOOT_SEED, N_BOOT, EXAMPLE_SEED = 5, 0, 1, 0, 2000, 0
READABLE, NULL_TOL = 0.60, 0.10
BATCH = PS.BATCH


# ---- pure helpers (tests/test_pointer_probe.py) ---------------------------------------------------------------------


def nearest_mean(x: torch.Tensor, mu: torch.Tensor, present: torch.Tensor | None = None) -> torch.Tensor:
    """Predicted class per item: x [N, P, d], class means mu [C, P, d] (absent classes masked out); chunked over items."""
    out = []
    for s in range(0, x.shape[0], 32):
        dist = ((x[s : s + 32, None] - mu[None]) ** 2).sum((2, 3))
        if present is not None:
            dist[:, ~present] = float("inf")
        out.append(dist.argmin(1))
    return torch.cat(out) if out else torch.empty(0, dtype=torch.long, device=x.device)


def cv_predictions(x: torch.Tensor, y: torch.Tensor, folds: int = FOLDS, seed: int = CV_SEED) -> torch.Tensor:
    """Out-of-fold nearest-class-mean predictions for every item (folds over a seeded shuffle)."""
    n = x.shape[0]
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    pred = torch.full((n,), -1, dtype=torch.long, device=x.device)
    for f in range(folds):
        test = idx[f::folds]
        train = torch.tensor(sorted(set(idx) - set(test)), device=x.device)
        if not test or train.numel() == 0:
            continue
        mu, _ = PF.class_means(x[train], y[train])
        present = torch.tensor([bool((y[train] == c).any()) for c in range(mu.shape[0])], device=x.device)
        t = torch.tensor(test, device=x.device)
        pred[t] = nearest_mean(x[t], mu, present)
    return pred


def entity_boot(hits, domains, entities, n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> list[float]:
    """Mean of per-item hits with a cluster bootstrap: queried entities resampled within each domain. [mean, lo, hi]."""
    hits = np.asarray(hits, float)
    if hits.size == 0:
        return [float("nan")] * 3
    groups: dict[str, dict[str, list[int]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for i, (d, e) in enumerate(zip(domains, entities, strict=True)):
        groups[d][e].append(i)
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        idx: list[int] = []
        for ents in groups.values():
            keys = list(ents)
            for k in rng.choice(len(keys), size=len(keys)):
                idx += ents[keys[k]]
        vals.append(hits[idx].mean())
    return [float(hits.mean()), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


# ---- run --------------------------------------------------------------------------------------------------------------


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.early_push import forward_rows

    pins.check_run_name(name)
    assert cfg["primary_layer"] in cfg["layers"], "the primary layer must be collected"
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    fit_cfg = {"domains": cfg["domains"], "fit_limit": cfg["fit_limit"]}
    files = [PF.PV.DATA / "fit" / f"{d}_RL_e5f0.json" for d in cfg["domains"]]
    means_path = pins.CACHE_DIR / "pointer_fit" / cfg["same_means"] / "fits.pt" if cfg["same_means"] else None
    doc = __doc__ or ""
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "config": cfg,
                "inputs": {str(p.relative_to(pins.REPO_ROOT)): sha256_of(p) for p in files},
                "same_means_file": str(means_path) if means_path else None,
                "same_means_sha256": sha256_of(means_path) if means_path and means_path.exists() else None,
                "seeds": {"cv": CV_SEED, "shuffle": SHUFFLE_SEED, "bootstrap": BOOT_SEED, "examples": EXAMPLE_SEED},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    split = PF.pools(cfg["domains"])
    layers = tuple(cfg["layers"])
    preps = [(it, PS.prepare(it, tok)) for it in PF.fit_items(fit_cfg)]
    by_len: dict[int, list[tuple[dict, dict]]] = collections.defaultdict(list)
    for it, p in preps:
        by_len[len(p["read_ids"]["base"])].append((it, p))
    feats: dict[int, list[torch.Tensor]] = {la: [] for la in layers}
    items: list[dict] = []
    for chunk in progress([g[i : i + BATCH] for g in by_len.values() for i in range(0, len(g), BATCH)], "collect"):
        logits, rec = forward_rows(model, torch.tensor([p["read_ids"]["base"] for _, p in chunk], device="cuda"),
                                   [{}] * len(chunk), layers)  # fmt: skip
        for ri, (it, p) in enumerate(chunk):
            for la in layers:
                feats[la].append(rec[la][ri, p["groups"]["final"]].half().cpu())
            items.append({"id": it["id"], "domain": it["domain"], "label": it["slots"]["query"], "query": it["query"],
                          "right": digit_tok.get(int(logits[ri].argmax())) == it["answer"],
                          "held_out_entity": it["query"] in split[it["domain"]][1], "text": p["text"],
                          "context": it["context"], "final_chars": [list(p["offsets"][i]) for i in p["groups"]["final"]]})  # fmt: skip
    y = torch.tensor([it["label"] for it in items], device="cuda")
    y_shuf = y[torch.randperm(len(y), generator=torch.Generator().manual_seed(SHUFFLE_SEED)).to(y.device)]
    same = torch.load(means_path, map_location="cpu") if means_path and means_path.exists() else None
    preds: list[dict] = []
    for la in layers:
        x = torch.stack(feats[la]).cuda().float()
        cv, cv_s = cv_predictions(x, y), cv_predictions(x, y_shuf)
        right = torch.tensor([it["right"] for it in items], device="cuda")
        cv_r = torch.full_like(y, -1)
        if bool(right.any()):
            cv_r[right] = cv_predictions(x[right], y[right])
        sm = nearest_mean(x, same[la]["mu"].cuda().float()) if same is not None and la in same else None
        for i, it in enumerate(items):
            preds.append({"id": it["id"], "layer": la, "label": it["label"], "cv": int(cv[i]), "cv_shuffled": int(cv_s[i]),
                          "shuffled_label": int(y_shuf[i]), "cv_right_only": int(cv_r[i]),
                          "same_means": int(sm[i]) if sm is not None else None})  # fmt: skip
        del x
    PF.write_rows(out_dir / "items.jsonl", items)
    PF.write_rows(out_dir / "preds.jsonl", preds)
    sm_ = summarise(items, preds, cfg)
    sm_["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(sm_, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(sm_))
    print((out_dir / "summary.md").read_text())


def acc(rows: list[dict], key: str, items: dict[str, dict], label_key: str = "label") -> dict[str, Any]:
    rows = [r for r in rows if r[key] is not None and r[key] >= 0]
    hits = [float(r[key] == r[label_key]) for r in rows]
    k = int(sum(hits))
    w = wilson(k, len(rows)) if rows else (float("nan"),) * 3
    b = entity_boot(hits, [items[r["id"]]["domain"] for r in rows], [items[r["id"]]["query"] for r in rows])
    return {"n": len(rows), "k_entities": len({(items[r["id"]]["domain"], items[r["id"]]["query"]) for r in rows}),
            "wilson": [round(v, 4) for v in w], "entity_boot": [round(v, 4) for v in b]}  # fmt: skip


def summarise(items: list[dict], preds: list[dict], cfg: dict) -> dict:
    by_id = {it["id"]: it for it in items}
    out: dict[str, Any] = {"layers": {}}
    for la in cfg["layers"]:
        rows = [r for r in preds if r["layer"] == la]
        cell = {"all": acc(rows, "cv", by_id), "shuffled": acc(rows, "cv_shuffled", by_id, "shuffled_label"),
                "right_only": acc([r for r in rows if by_id[r["id"]]["right"]], "cv_right_only", by_id)}  # fmt: skip
        for d in cfg["domains"]:
            cell[f"domain:{d}"] = acc([r for r in rows if by_id[r["id"]]["domain"] == d], "cv", by_id)
        if any(r["same_means"] is not None for r in rows):
            cell["same_means_held_out_entities"] = acc(
                [r for r in rows if by_id[r["id"]]["held_out_entity"]], "same_means", by_id
            )
        out["layers"][str(la)] = cell
    p = out["layers"][str(cfg["primary_layer"])]
    lo, hi = p["all"]["wilson"][1], p["all"]["wilson"][2]
    valid = abs(p["shuffled"]["wilson"][0] - 0.2) <= NULL_TOL
    out["verdict"] = ("readable" if lo >= READABLE else "hardly readable (the first run's 39% survives)" if hi < READABLE
                      else "in between") + ("" if valid else " (shuffled null off chance: not interpretable)")  # fmt: skip
    out["n_items"], out["n_right"] = len(items), sum(it["right"] for it in items)
    return out


def summary_md(sm: dict) -> str:
    lines = [f"# {EXP}", "", f"Verdict: **{sm['verdict']}** ({sm['n_items']} items, {sm['n_right']} answered right)", "",
             "| layer | all (CV) | shuffled | answered right only | " + " | ".join(k for k in next(iter(sm["layers"].values())) if k.startswith(("domain", "same"))) + " |",
             "|---" * (4 + sum(1 for k in next(iter(sm["layers"].values())) if k.startswith(("domain", "same")))) + "|"]  # fmt: skip
    for la, c in sm["layers"].items():

        def f(x):
            w = x["wilson"]
            return f"{100 * w[0]:.0f}% [{100 * w[1]:.0f}, {100 * w[2]:.0f}] (n={x['n']}, k={x['k_entities']})"

        extra = [f(v) for k, v in c.items() if k.startswith(("domain", "same"))]
        lines.append(
            f"| {la} | {f(c['all'])} | {f(c['shuffled'])} | {f(c['right_only'])} | " + " | ".join(extra) + " |"
        )
    return "\n".join(lines) + "\n"


# ---- figures and examples ---------------------------------------------------------------------------------------------


def stage_figures(name: str) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from bridge_jspace import plotting as PL

    d = RESULTS / name
    m = json.loads((d / "manifest.json").read_text())
    for old in d.glob("analysis-*-figures"):
        for f_ in old.iterdir():
            f_.unlink()
        old.rmdir()
    out = d / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    items = [json.loads(x) for x in (d / "items.jsonl").read_text().splitlines()]
    preds = [json.loads(x) for x in (d / "preds.jsonl").read_text().splitlines()]
    sm = summarise(items, preds, m["config"])
    lay = [int(k) for k in sm["layers"]]
    fig, ax = plt.subplots(figsize=(12, 4.6))
    PL.style_axes(ax)
    PL.percent_axis(ax)
    series = [("all", "#2a78d6", "-", "all fit scenes (cross-validated)"),
              ("right_only", "#1baf7a", "-", "scenes answered right only"),
              *[(f"domain:{dm}", c, "--", f"{dm} only") for dm, c in zip(m["config"]["domains"], ("#eb6834", "#eda100"), strict=False)],
              ("same_means_held_out_entities", "#6250d6", "-", "the first run's own means, entities it never saw"),
              ("shuffled", PL.MUTED, ":", "control: shuffled labels")]  # fmt: skip
    for key, colour, ls, label in series:
        if key not in next(iter(sm["layers"].values())):
            continue
        v = np.array([sm["layers"][str(la)][key]["entity_boot"] for la in lay], float)
        ax.errorbar(lay, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None), color=colour, ls=ls,
                    lw=2, marker="o", ms=5, elinewidth=1, capsize=0, label=label)  # fmt: skip
    ax.axhline(0.2, color=PL.MUTED, lw=1)
    ax.axhline(READABLE, color=PL.MUTED, ls="--", lw=1)
    ax.set_xticks(lay, [str(la) for la in lay])
    ax.set_ylim(0, 1.04)
    ax.set_xlabel("layer", fontsize=9, color=PL.MUTED)
    ax.set_ylabel("which statement is asked: % read right\n(5 statements, chance 20%)", fontsize=9, color=PL.INK)
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    c0 = items[0]
    sents = c0["context"].split(". ")
    explain = [("What we did", "Read which of the 5 statements the question asks about from the tokens after the question, "
                               "by the nearest per-statement mean (the means the pointer direction is built from), "
                               "cross-validated over scenes."),
               ("Example", f"\"{sents[c0['label']].rstrip('.')}. ... {c0['text'][c0['text'].rindex('Which'):].split('?')[0]}?\" "
                           f"-> the asked statement is number {c0['label'] + 1}."),
               ("How to read", f"Each dot: share of scenes read right. Dashed line: the {int(100 * READABLE)}% bar the rule "
                               f"calls readable. Verdict: '{sm['verdict']}'."),
               ("Control", "Dotted: the same classifier on shuffled labels (should sit at chance, 20%).")]  # fmt: skip
    model_name = m["model"]["repo"].split("/")[-1]
    figs: list[str] = []
    PF.save_fig(fig, out, "fig1_slot_readable", "Can the last tokens tell which statement the question asks about?", explain,
                f"{model_name}; {sm['n_items']} fit scenes ({sm['n_right']} answered right); error bars: bootstrap over "
                "the asked entities within each topic.", figs=figs)  # fmt: skip
    (out / "summary.json").write_text(
        json.dumps({"run": name, "verdict": sm["verdict"], "summary": sm, "figures": figs}, indent=2) + "\n"
    )
    print(out)
    return out


def stage_examples(name: str, k: int = 3, seed: int = EXAMPLE_SEED) -> None:
    d = RESULTS / name
    path = d / "examples.json"
    assert not path.exists(), f"{path} exists; written once"
    m = json.loads((d / "manifest.json").read_text())
    la = m["config"]["primary_layer"]
    items = {it["id"]: it for it in (json.loads(x) for x in (d / "items.jsonl").read_text().splitlines())}
    preds = [p for p in (json.loads(x) for x in (d / "preds.jsonl").read_text().splitlines()) if p["layer"] == la]
    groups = {"read_right": "the classifier names the asked statement", "read_wrong": "it names another statement"}
    members = {g: [p for p in preds if (p["cv"] == p["label"]) == (g == "read_right")] for g in groups}
    rng = np.random.default_rng(seed)
    examples = []
    for g, ps in members.items():
        for p in [ps[i] for i in sorted(rng.choice(len(ps), size=min(k, len(ps)), replace=False))] if ps else []:
            it = items[p["id"]]
            spans = PF.statement_spans(it["text"], it["context"])
            examples.append({"group": g, "family": "RL", "item_id": p["id"], "prompt": it["text"] + " ",
                             "spans": [{"start": spans[p["label"]][0], "end": spans[p["label"]][1], "role": "asked statement"},
                                       {"start": spans[p["cv"]][0], "end": spans[p["cv"]][1], "role": "statement read"},
                                       {"start": it["final_chars"][0][0], "end": it["final_chars"][-1][1], "role": "tokens read"}],
                             "condition": f"no edit; nearest statement mean at layer {la} (cross-validated)",
                             "answers": {"clean": f"statement {p['label'] + 1}", "edited": f"statement {p['cv'] + 1}",
                                         "expected": {"H-readable": f"statement {p['label'] + 1}", "H-hardly-readable": "any of 5"}},
                             "numbers": {"answered_right": it["right"]},
                             "why": groups[g]})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k,
            "groups": [{"key": g, "title": g.replace("_", " "), "definition": t, "n_total": len(members[g])} for g, t in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "figures", "examples"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--domains", nargs="+", default=DEFAULTS["domains"])
    ap.add_argument("--layers", nargs="+", type=int, default=DEFAULTS["layers"])
    ap.add_argument("--primary-layer", type=int, default=DEFAULTS["primary_layer"])
    ap.add_argument("--fit-limit", type=int, default=None, help="fit scenes per domain (a smoke: few)")
    ap.add_argument(
        "--same-means",
        default=DEFAULTS["same_means"],
        help="pointer_fit run whose cached class means to apply ('' for none)",
    )
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        stage_run(args.name, args.why, {"domains": args.domains, "layers": args.layers, "primary_layer": args.primary_layer,
                                        "fit_limit": args.fit_limit, "same_means": args.same_means or None})  # fmt: skip
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k)
