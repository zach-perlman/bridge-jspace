"""x0_probe (descriptive, added after data; Dan, 24 Oct evening): what does the bridge's word hold in the org run?
Linear probes on h_org at the asked person's bridge word and the pre-registered layer, X0's scenes, split by whether
the bridge's locker sentence comes before or after the asked pick sentence:
  (a) answer digit: the lookup's answer (the bridge's locker number);
  (b) locker sentence: the index, among the context's sentences, of the sentence holding the bridge's locker;
  (c) bridge identity: the positive control.
(a) and (b) are cross-validated by bridge entity (5 folds, whole entities held out). (c) cannot be (a held-out entity is
an unseen class): 5 folds by item, every entity spread over the folds. Probe: ridge regression on one-hot targets over
the training folds' standardized features (dual form), predicted class = argmax; the penalty (relative to the mean
kernel diagonal, RELS) chosen by an inner 4-fold CV of the same kind on the training folds. Baselines: chance
(1 / classes) and the training folds' majority class; for (b) also a structure-only baseline (the agent's addition, not
specified): the training folds' most frequent locker index given the asked pick's sentence index. Accuracy with 95% CIs
from a cluster bootstrap over bridge entities (10,000 resamples, seed 0), and probe - best baseline on the same draws.
Primary: the X0 items of the source run; secondary: every chat scene of the set.

Pre-stated reading (Dan): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the
word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address (a lookback-style
pointer). In locker-after scenes the locker sentence follows the word, so (a) and (b) cannot be read there from the
locker sentence itself: that stratum is the control by construction.

uv run python scripts/x0_probe.py run --name x0_probe_27b --source x0_necessity_27b_chat --layer 32   # GPU, then fit
uv run python scripts/x0_probe.py fit --name x0_probe_27b                                             # CPU
uv run python scripts/x0_probe.py figures --name x0_probe_27b                                         # CPU
Writes results/x0_probe/<name>/{manifest.json, states.npz, items.jsonl, probe-<UTC>/{probe.md, probe.json, probe.png}}.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x0_strata as ST

EXP = "x0_probe"
RESULTS = pins.RESULTS_DIR / EXP
NOTE = "Descriptive, added after data (Dan, 24 Oct evening); not part of X0's rule."
TARGETS = {"answer digit": "answer", "locker sentence": "locker_index", "bridge identity": "entity"}
GROUPED = {"answer digit": True, "locker sentence": True, "bridge identity": False}
STRATA = ("before", "after", "both")
K_OUTER, K_INNER = 5, 4
RELS = (1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0)  # ridge penalty / mean kernel diagonal
NUMBER_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def positions(case: dict) -> tuple[int, int, int]:
    """(the asked pick sentence's index, the bridge's locker sentence's index, the number of sentences)."""
    sents = [s if s.endswith(".") else s + "." for s in case["context"].split(". ")]
    asked = re.search(r"([A-Z][a-z]+)'s pick", case["readers"][X.LOOKUP]["question"]).group(1)  # type: ignore[union-attr]
    pick = next(i for i, s in enumerate(sents) if s.startswith(f"{asked} picked"))
    locker = next(i for i, s in enumerate(sents)
                  if s.startswith("The locker of") and re.search(rf"\b{case['bridge']}\b", s))  # fmt: skip
    answer = case["readers"][X.LOOKUP]["answer"]
    stated = sents[locker].rsplit(" is ", 1)[1].rstrip(".")
    assert stated in (answer, NUMBER_WORDS[int(answer)]), f"{case['scene']}: {sents[locker]!r} vs answer {answer}"
    return pick, locker, len(sents)


def layout(context: str, pick: int) -> str:
    """What the word can see of the scene's layout, without any binding: which sentences before the asked pick are
    locker sentences (e.g. '.LLL.' for a pick at index 5); the layout baseline's key."""
    return "".join("L" if s.startswith("The locker of") else "." for s in context.split(". ")[:pick])


def item_of(case: dict, x0: bool) -> dict:
    pick, locker, n = positions(case)
    stated = case["context"].split(". ")[locker].rsplit(" is ", 1)[1].rstrip(".")
    return {"scene": case["scene"], "entity": case["bridge"], "domain": case["domain"], "x0": x0,
            "order": ST.features(case)["org locker vs asked pick"], "answer": case["readers"][X.LOOKUP]["answer"],
            "locker_form": "digit" if stated.isdigit() else "word", "pick_index": pick, "locker_index": locker,
            "sentences": n, "pos": case["pos"]}  # fmt: skip


# ---- probes (CPU) -------------------------------------------------------------------------------------------------


def folds(labels: list, groups: list[str], grouped: bool, k: int) -> np.ndarray:
    """Fold index per item. grouped: whole entities per fold (largest entity first, to the smallest fold); else every
    class spread over the folds (round robin in item order, the start shifted per class)."""
    out = np.empty(len(labels), dtype=int)
    if grouped:
        size = [0] * k
        count = collections.Counter(groups)
        for g in sorted(count, key=lambda g: (-count[g], g)):
            f = min(range(k), key=lambda i: (size[i], i))
            out[[i for i, x in enumerate(groups) if x == g]] = f
            size[f] += count[g]
        return out
    start = 0
    for c in sorted(set(labels), key=str):
        idx = [i for i, x in enumerate(labels) if x == c]
        for j, i in enumerate(idx):
            out[i] = (start + j) % k
        start += len(idx)
    return out


def ridge(xtr: np.ndarray, ytr: list, xte: np.ndarray, rels: tuple[float, ...]) -> list[list]:
    """Per relative penalty, the predicted class of each test row: one-hot ridge on standardized features (dual)."""
    classes = sorted(set(ytr), key=str)
    mu, sd = xtr.mean(0), xtr.std(0)
    sd[sd < 1e-6] = 1.0
    a, b = (xtr - mu) / sd, (xte - mu) / sd
    y = np.array([[v == c for c in classes] for v in ytr], dtype=float)
    ym = y.mean(0)
    s, u = np.linalg.eigh(a @ a.T)
    s = np.clip(s, 0.0, None)
    proj, kt = u.T @ (y - ym), b @ a.T
    out = []
    for r in rels:
        alpha = u @ (proj / (s + r * s.sum() / len(s))[:, None])
        out.append([classes[j] for j in (kt @ alpha + ym).argmax(1)])
    return out


def cv_predict(
    x: np.ndarray, y: list, groups: list[str], grouped: bool, resid: list | None = None
) -> tuple[list, np.ndarray, list[float]]:
    """Out-of-fold predictions, the outer fold of each item, and the penalty chosen per outer fold (inner CV; ties go
    to the larger penalty). resid: a label per item whose class means, from the training folds only, are subtracted
    from the states first (the probe then reads only what the label's class means do not carry)."""
    outer = folds(y, groups, grouped, K_OUTER)
    pred: list = [None] * len(y)
    chosen = []
    for f in range(K_OUTER):
        tr, te = np.flatnonzero(outer != f), np.flatnonzero(outer == f)
        if not len(te):
            continue
        if resid is not None:
            means = {c: x[[i for i in tr if resid[i] == c]].mean(0) for c in {resid[i] for i in tr}}
            overall = x[tr].mean(0)
            x = x.copy()
            for i in (*tr, *te):
                x[i] = x[i] - means.get(resid[i], overall)
        ytr, gtr = [y[i] for i in tr], [groups[i] for i in tr]
        inner = folds(ytr, gtr, grouped, K_INNER)
        acc = np.zeros(len(RELS))
        for g in range(K_INNER):
            itr, ite = np.flatnonzero(inner != g), np.flatnonzero(inner == g)
            if not len(ite):
                continue
            for j, p in enumerate(ridge(x[tr][itr], [ytr[i] for i in itr], x[tr][ite], RELS)):
                acc[j] += sum(pi == ytr[i] for pi, i in zip(p, ite, strict=True))
        best = max(range(len(RELS)), key=lambda j: (acc[j], j))
        chosen.append(RELS[best])
        for i, p in zip(te, ridge(x[tr], ytr, x[te], (RELS[best],))[0], strict=True):
            pred[i] = p
    return pred, outer, chosen


def select_penalty(x: np.ndarray, y: list, groups: list[str]) -> float:
    """The relative penalty with the best entity-held-out CV accuracy (K_OUTER folds; ties to the larger)."""
    f = folds(y, groups, True, K_OUTER)
    acc = np.zeros(len(RELS))
    for g in range(K_OUTER):
        tr, te = np.flatnonzero(f != g), np.flatnonzero(f == g)
        for j, p in enumerate(ridge(x[tr], [y[i] for i in tr], x[te], RELS)):
            acc[j] += sum(pi == y[i] for pi, i in zip(p, te, strict=True))
    return RELS[max(range(len(RELS)), key=lambda j: (acc[j], j))]


def subspace(x: np.ndarray, y: list, rel: float) -> np.ndarray:
    """An orthonormal basis [d, classes - 1] of the probe's decision directions in raw state space: the one-hot ridge
    weights over standardized features, divided by the feature scales, centered across classes."""
    classes = sorted(set(y), key=str)
    mu, sd = x.mean(0), x.std(0)
    sd[sd < 1e-6] = 1.0
    a = (x - mu) / sd
    t = np.array([[v == c for c in classes] for v in y], dtype=float)
    s, u = np.linalg.eigh(a @ a.T)
    s = np.clip(s, 0.0, None)
    alpha = u @ ((u.T @ (t - t.mean(0))) / (s + rel * s.sum() / len(s))[:, None])
    w = (a.T @ alpha) / sd[:, None]  # [d, classes]
    w -= w.mean(1, keepdims=True)
    q, sv, _ = np.linalg.svd(w, full_matrices=False)
    return q[:, : int((sv > sv.max() * 1e-6).sum())]


def mode(values: list):
    count = collections.Counter(values)
    return max(sorted(count, key=str), key=lambda v: count[v])


def baseline(y: list, outer: np.ndarray, given: list | None = None) -> list:
    """Out-of-fold: the training folds' majority class, or (given) its majority among items with the same `given`
    value (the overall majority when no training item shares it)."""
    pred: list = [None] * len(y)
    for f in set(outer.tolist()):
        tr = [i for i in range(len(y)) if outer[i] != f]
        overall = mode([y[i] for i in tr])
        for i in np.flatnonzero(outer == f):
            same = [y[j] for j in tr if given is not None and given[j] == given[i]]
            pred[i] = mode(same) if same else overall
    return pred


def score(x: np.ndarray, items: list[dict], target: str, n_boot: int) -> dict:
    y = [it[TARGETS[target]] for it in items]
    ents = [it["entity"] for it in items]
    pred, outer, chosen = cv_predict(x, y, ents, GROUPED[target])
    right = {"probe": [int(p == t) for p, t in zip(pred, y, strict=True)],
             "majority": [int(p == t) for p, t in zip(baseline(y, outer), y, strict=True)]}  # fmt: skip
    if target == "locker sentence":
        right["structure"] = [int(p == t) for p, t in
                              zip(baseline(y, outer, [it["pick_index"] for it in items]), y, strict=True)]  # fmt: skip
        if all("layout" in it for it in items):
            right["layout"] = [int(p == t) for p, t in
                               zip(baseline(y, outer, [it["layout"] for it in items]), y, strict=True)]  # fmt: skip
    chance = 1.0 / len(set(y))
    r = X.resampled_rates(right, ents, n_boot)
    out = {"n": len(y), "entities": len(set(ents)), "classes": len(set(y)), "chance": round(chance, 4),
           "penalties": chosen}  # fmt: skip
    for k, v in right.items():
        out[k] = [float(np.mean(v)), *X.interval(r[k])]
    best = max((k for k in right if k != "probe"), key=lambda k: out[k][0])
    if chance > out[best][0]:
        out["best_baseline"], diff = "chance", r["probe"] - chance
    else:
        out["best_baseline"], diff = best, r["probe"] - r[best]
    base = chance if out["best_baseline"] == "chance" else out[best][0]
    out["probe_minus_best"] = [out["probe"][0] - base, *X.interval(diff)]
    return out


def stage_fit(name: str, n_boot: int) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    z = np.load(src / "states.npz")
    h, scenes = z["h"].astype(np.float64), [str(s) for s in z["scene"]]
    items = X.read_jsonl(src / "items.jsonl")
    assert [it["scene"] for it in items] == scenes, "items.jsonl and states.npz disagree on the scene order"
    if m["source"]:
        contexts = {c["scene"]: c["context"] for c in X.read_jsonl(X.RESULTS / m["source"] / "cases.jsonl")}
    else:  # a fresh set (no X0 run): the items carry their contexts
        contexts = {it["scene"]: it["context"] for it in items}
    for it in items:
        it["layout"] = layout(contexts[it["scene"]], it["pick_index"])
    rows = []
    for subset in ("x0", "all") if m["source"] else ("all",):
        for stratum in STRATA:
            idx = [i for i, it in enumerate(items) if (subset == "all" or it["x0"])
                   and (stratum == "both" or it["order"] == stratum)]  # fmt: skip
            for target in TARGETS:
                sub = [items[i] for i in idx]
                rows.append({"subset": subset, "stratum": stratum, "target": target,
                             **score(h[idx], sub, target, n_boot)})  # fmt: skip
                print(json.dumps(rows[-1]), flush=True)
    out = src / f"probe-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    blob = {"run": name, "manifest": m, "note": NOTE, "rows": rows}
    (out / "probe.json").write_text(json.dumps(blob, indent=1) + "\n")
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# X0 probes: {name} ({m['model']['target']}, layer {m['layer']}, the bridge's word, org run)", "",
             f"{NOTE} Source run {m['source']} (set {m['set']}). Probes cross-validated by bridge entity ((a), (b)) or by "
             f"item ((c)); {n_boot} cluster-bootstrap resamples over entities, seed {X.BOOT_SEED}. 'structure' and "
             "'layout' (b only) are the agent's additions: the training folds' most frequent locker index given the "
             "asked pick's sentence index (structure), or given which sentences before the pick are locker sentences "
             "(layout: what the word can see of the scene, with no binding). UNVERIFIED.", "",
             "Pre-stated reading (Dan): (a) high in locker-before and at chance in locker-after -> the answer value is "
             "stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an "
             "address. Locker-after: the locker sentence follows the word, so the stratum is a control by construction.",
             "", "| subset | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | "
             "layout | probe - best baseline |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for r in rows:
        lines.append(f"| {'X0 items' if r['subset'] == 'x0' else 'every scene'} | {r['stratum']} | {r['target']} | "
                     f"{r['n']} | {r['entities']} | {r['classes']} | {ci(r['probe'])} | {ci(r['majority'])} | "
                     f"{r['chance']:.2f} | {ci(r['structure']) if 'structure' in r else '-'} | "
                     f"{ci(r['layout']) if 'layout' in r else '-'} | {ci(r['probe_minus_best'])} ({r['best_baseline']}) |")  # fmt: skip
    (out / "probe.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def stage_a_given_b(name: str, n_boot: int) -> Path:
    """Probe (a) with the locker index factored out (Dan's audit item 3), locker-before: the answer digit from the locker
    index alone (training folds' most frequent digit per index, entity-held-out), probe (a) on states residualised on
    the locker index (class means from the training folds), and probe (a)'s accuracy within each locker-index class."""
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    h = np.load(src / "states.npz")["h"].astype(np.float64)
    items = X.read_jsonl(src / "items.jsonl")
    out = src / f"a-given-b-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# Probe (a) with the locker index factored out: {name} (layer {m['layer']}, locker-before)", "",
             f"{NOTE} (Dan's audit item 3.) Folds by bridge entity; {n_boot} cluster-bootstrap resamples over entities. "
             "UNVERIFIED.", "",
             "| subset | n | probe (a) | the locker index alone | probe (a), residualised on the index | chance | "
             "residualised - index alone |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    blob: dict = {"run": name, "note": NOTE, "subsets": {}}
    per_class = []
    for subset in ("x0", "all") if m["source"] else ("all",):
        idx = [i for i, it in enumerate(items) if it["order"] == "before" and (subset == "all" or it["x0"])]
        sub = [items[i] for i in idx]
        y, ents, b = [it["answer"] for it in sub], [it["entity"] for it in sub], [it["locker_index"] for it in sub]
        pred, outer, _ = cv_predict(h[idx], y, ents, True)
        pred_r, _, _ = cv_predict(h[idx], y, ents, True, resid=b)
        right = {"probe": [int(p == t) for p, t in zip(pred, y, strict=True)],
                 "index_alone": [int(p == t) for p, t in zip(baseline(y, outer, b), y, strict=True)],
                 "residualised": [int(p == t) for p, t in zip(pred_r, y, strict=True)]}  # fmt: skip
        r = X.resampled_rates(right, ents, n_boot)
        res = {k: [float(np.mean(v)), *X.interval(r[k])] for k, v in right.items()}
        res["residualised_minus_index"] = [res["residualised"][0] - res["index_alone"][0],
                                           *X.interval(r["residualised"] - r["index_alone"])]  # fmt: skip
        res["chance"] = 1 / len(set(y))
        blob["subsets"][subset] = res
        lines.append(f"| {'X0 items' if subset == 'x0' else 'every scene'} | {len(y)} | {ci(res['probe'])} | "
                     f"{ci(res['index_alone'])} | {ci(res['residualised'])} | {res['chance']:.2f} | "
                     f"{ci(res['residualised_minus_index'])} |")  # fmt: skip
        for c in sorted(set(b)):
            k = [j for j, v in enumerate(b) if v == c]
            per_class.append((subset, c, len(k), float(np.mean([right["probe"][j] for j in k])),
                              float(np.mean([right["residualised"][j] for j in k]))))  # fmt: skip
    lines += ["", "Within each locker-index class (point estimates):", "",
              "| subset | locker index | n | probe (a) | residualised |", "|---|---|---|---|---|"]  # fmt: skip
    lines += [f"| {s} | {c} | {n} | {a:.2f} | {r_:.2f} |" for s, c, n, a, r_ in per_class]
    blob["per_class"] = per_class
    (out / "a_given_b.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "a_given_b.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def stage_perclass(name: str, n_boot: int) -> Path:
    """Probe (b) per true locker-sentence index, locker-before (Dan's item 4): accuracy with its entity-bootstrap CI,
    the share predicted per index (the confusion rows), per subset; and how probe (c)'s folds split (by item = scene)."""
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    h = np.load(src / "states.npz")["h"].astype(np.float64)
    items = X.read_jsonl(src / "items.jsonl")
    out = src / f"perclass-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    lines = [f"# Probe (b) by locker-sentence index: {name} (layer {m['layer']}, locker-before)", "",
             f"{NOTE} Out-of-fold predictions of x0_probe's (b) probe (5 folds by bridge entity); accuracy per true index "
             f"with a cluster bootstrap over entities ({n_boot} resamples, seed {X.BOOT_SEED}); the rest of each row is "
             "the share of that index's items predicted as each index. UNVERIFIED.", ""]  # fmt: skip
    blob: dict = {"run": name, "note": NOTE, "subsets": {}}
    for subset in ("x0", "all") if m["source"] else ("all",):
        idx = [i for i, it in enumerate(items) if it["order"] == "before" and (subset == "all" or it["x0"])]
        sub = [items[i] for i in idx]
        y = [it["locker_index"] for it in sub]
        pred, _, _ = cv_predict(h[idx], y, [it["entity"] for it in sub], True)
        classes = sorted(set(y))
        lines += [f"## {'X0 items' if subset == 'x0' else 'every scene'} (n = {len(y)})", "",
                  "| true index | n | accuracy | " + " | ".join(f"predicted {c}" for c in classes) + " |",
                  "|---|---|---|" + "---|" * len(classes)]  # fmt: skip
        rows = {}
        for c in classes:
            k = [j for j, t in enumerate(y) if t == c]
            right = [int(pred[j] == c) for j in k]
            r = X.resampled_rates({"right": right}, [sub[j]["entity"] for j in k], n_boot)["right"]
            share = {p: sum(pred[j] == p for j in k) / len(k) for p in classes}
            rows[str(c)] = {"n": len(k), "accuracy": [float(np.mean(right)), *X.interval(r)], "predicted": share}
            lines.append(f"| {c} | {len(k)} | {X.fmt3(rows[str(c)]['accuracy'])} | "
                         + " | ".join(f"{share[p]:.2f}" for p in classes) + " |")  # fmt: skip
        blob["subsets"][subset] = rows
        lines.append("")
    f = folds([it["entity"] for it in items], [it["entity"] for it in items], False, K_OUTER)
    per_entity = collections.Counter(len({int(f[i]) for i, it in enumerate(items) if it["entity"] == e})
                                     for e in {it["entity"] for it in items})  # fmt: skip
    blob["probe_c_split"] = {"unit": "item (one scene per item)", "folds": K_OUTER,
                             "entities_by_number_of_folds_they_span": dict(per_entity)}  # fmt: skip
    lines += ["## Probe (c)'s split", "",
              f"Probe (c) (bridge identity) uses 5 folds over items; each item is one scene, so the split is by scene. "
              f"Every entity is spread over the folds (an entity-held-out fold has no seen class): entities by the number "
              f"of folds they span: {dict(sorted(per_entity.items()))}.", ""]  # fmt: skip
    (out / "perclass.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "perclass.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def figures(probe_dir: Path) -> Path:
    """Probe accuracy per target and stratum (X0 items) with its CI, beside majority, chance and structure."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle

    from scripts.figs import common as F

    blob = json.loads((probe_dir / "probe.json").read_text())
    subset = "x0" if blob["manifest"]["source"] else "all"
    rows = [r for r in blob["rows"] if r["subset"] == subset]
    fig, axes = plt.subplots(1, len(TARGETS), figsize=(13, 4.6), sharey=True)
    for ax, target in zip(axes, TARGETS, strict=True):
        for j, stratum in enumerate(STRATA):
            r = next(r for r in rows if r["target"] == target and r["stratum"] == stratum)
            p = r["probe"]
            ax.bar(j, p[0], 0.6, color="#4a6fa5", yerr=[[p[0] - p[1]], [p[2] - p[0]]], capsize=4)
            ax.plot([j - 0.3, j + 0.3], [r["chance"]] * 2, color="black", lw=1, ls="--")
            ax.plot(j, r["majority"][0], "D", color=F.CONTROL, ms=7)
            if "structure" in r:
                ax.plot(j, r["structure"][0], "s", color="#c27c0e", ms=7)
            if "layout" in r:
                ax.plot(j, r["layout"][0], "^", color="#7a4ea3", ms=8)
            ax.text(j, 1.02, f"n={r['n']}", ha="center", fontsize=8, color=F.CAPTION_INK)
        ax.set_xticks(range(len(STRATA)), ["locker before", "locker after", "both"])
        ax.set_title(target)
        ax.set_ylim(0, 1.08)
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("cross-validated accuracy")
    h = [Rectangle((0, 0), 1, 1, color="#4a6fa5"), Line2D([], [], color="black", ls="--"),
         Line2D([], [], marker="D", color=F.CONTROL, ls=""), Line2D([], [], marker="s", color="#c27c0e", ls=""),
         Line2D([], [], marker="^", color="#7a4ea3", ls="")]  # fmt: skip
    fig.legend(h, ["probe (95% CI)", "chance", "majority class", "pick index only*", "visible layout only*"], ncol=5,
               loc="upper center", bbox_to_anchor=(0.5, 0.93), frameon=False, fontsize=9)  # fmt: skip
    fig.text(0.5, 0.01, "* agent's additions, (b) only: the most frequent locker index given the pick's sentence index, "
             "or given which earlier sentences are locker sentences (no binding).", ha="center", fontsize=8,
             color=F.CAPTION_INK)  # fmt: skip
    m = blob["manifest"]
    what = "X0 items" if subset == "x0" else f"every scene of {m['set']}"
    fig.suptitle(f"What the bridge's word holds: {m['model']['target']}, layer {m['layer']}, {what} (UNVERIFIED; "
                 "descriptive, added after data)", fontsize=11)  # fmt: skip
    fig.tight_layout(rect=(0, 0.04, 1, 0.86))
    path = probe_dir / "probe.png"
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
    print(path)
    return path


# ---- states (GPU) -------------------------------------------------------------------------------------------------


def stage_run(name: str, source: str | None, layer: int, set_name: str | None = None) -> Path:
    """States at the bridge's word for every chat scene of the source X0 run's set (its items flagged x0), or of a
    fresh set (source None: no X0 items)."""
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress

    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    sm = json.loads((X.RESULTS / source / "manifest.json").read_text()) if source else {"code": None, "set": set_name}
    x0 = {r["scene"] for r in X.read_jsonl(X.RESULTS / source / "outcomes.jsonl") if r["rendering"] == "chat"} if source else set()  # fmt: skip
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "source": source, "source_code": sm["code"], "set": sm["set"], "layer": layer, "x0_items": len(x0),
         "model": pins.model_pin(), "code": git_state(), "position": "the asked person's bridge word, org run, chat",
         "folds": {"outer": K_OUTER, "inner": K_INNER, "penalties": list(RELS)},
         "seeds": {"bootstrap": X.BOOT_SEED}, "targets": {t: TARGETS[t] for t in TARGETS}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    cases, _ = X.build_cases(model.tokenizer, sm["set"])
    cases = [c for c in cases if c["rendering"] == "chat"]
    assert x0 <= {c["scene"] for c in cases}, "X0 items missing from the rebuilt cases"
    states = []
    with torch.no_grad():
        for c in progress(cases, "h_org at the bridge's word (case)"):
            ids = torch.tensor([c["readers"][X.LOOKUP]["ids"]["org"]], device="cuda")
            states.append(model.run(ids, record=(layer,))[1][layer][c["pos"]].float().cpu().numpy())
    h = np.stack(states)
    h = h.astype(np.float16) if np.abs(h).max() < 6e4 else h  # fp16 when it fits (size), else fp32
    np.savez_compressed(out / "states.npz", h=h, scene=np.array([c["scene"] for c in cases]))
    X.write_jsonl(out / "items.jsonl", [{**item_of(c, c["scene"] in x0), "context": c["context"]} for c in cases])
    print("wrote", out / "states.npz", h.shape, h.dtype, flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "fit", "figures", "perclass", "a_given_b"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--source", default="x0_necessity_27b_chat")
    ap.add_argument("--set", default=None, help="run: a fresh tasks_v2 set instead of the source run's (no X0 items)")
    ap.add_argument("--layer", type=int, default=32)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "run":
        stage_run(a.name, None if a.set else a.source, a.layer, a.set)
    if a.stage == "perclass":
        stage_perclass(a.name, a.n_boot)
    elif a.stage == "a_given_b":
        stage_a_given_b(a.name, a.n_boot)
    elif a.stage in ("run", "fit"):
        figures(stage_fit(a.name, a.n_boot))
    else:
        figures(sorted((RESULTS / a.name).glob("probe-*"))[-1])


if __name__ == "__main__":
    main()
