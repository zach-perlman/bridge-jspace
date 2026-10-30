"""f2_differences: the lens part minus a same-size control, paired on the same items, with a 95% interval (Dan 30 Oct,
slide-readability brief; f2_controls' right-hand columns and f2_main).

f2 plots the lens part and its controls as separate dots, each with its own interval; the claim is their difference, which
needs the items paired. Two halves, as in the figure:

  band of layers (points, M - K)   the lens part (condition paper10) minus a control, per model. The controls are the
      rotated part (paper10_rot) and the logit lens (unembed10), both in the lens part's own run, and the same-norm PCA
      directions (paper10_pcasize), a run of its own on the same test items. Scored as results/ablate_v2's jsuite2_score does: items
      the unedited model gets right, clusters = relation:bridge resampled jointly, 1000 draws, random.Random(0); here the
      statistic is (M - K) of one condition minus (M - K) of the other on the same resample.
  one layer (share, extra loss)     the lens part minus the PCA directions of the same size, from the parts run that holds
      both (results/x0_parts/<run>), with X0's own cluster bootstrap (x0_necessity.resampled_rates: whole entities,
      the same draws for every arm). The logit lens and the random lens directions of f2's one-layer half come from the
      main test, another run on other scenes: no pairing, so no interval (aggregate only).

Each point estimate is asserted equal to the plotted one (the stored M - K to its 0.1 rounding; the stored excess to 1e-6).
Where the pair has no common per-item rows (a control only known as a ratio of the lens part, Lightning's one-layer half),
the row carries no lo / hi and the figure writes "no interval (aggregate only)".

  band.<m>.<ctrl>   M - K of the lens part minus the control, points [lo, hi]   ctrl: rot | u | pc
  layer.<m>.pca     recall's extra loss of the lens part minus the PCA directions, share [lo, hi]

uv run python scripts/f2_differences.py            # recompute, check, print
uv run python scripts/f2_differences.py --write    # and write the rows into docs/breadth/data.csv
"""

from __future__ import annotations

import collections
import csv
import json
import random
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import x0_necessity as X  # noqa: E402

CSV = REPO / "docs" / "breadth" / "data.csv"
ABLATE = REPO / "results" / "ablate_v2"
BAND_RUNS = {  # model -> (the lens part's run, the PCA run)
    "q27": ("jsuite_v2_test_chat_ko_cand2_v1", "jsuite_v2_test_chat_ko_cand2_L32-40_pca_v1"),
    "q9": ("qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_L12-16_pca_v1"),
    "nl": ("nem35l_jsuite_v2_test_chat_ko_cand2_v1", "nem35l_jsuite_v2_test_chat_ko_cand2_L27-33_pca_v1"),
    "mu": ("muse30_jsuite_v2_test_chat_ko_cand2_v1", None),
    "q122": ("qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1", None),
}  # fmt: skip
CONTROLS = {"rot": ("paper10_rot", "rotated"), "u": ("unembed10", "logit lens"), "pc": ("paper10_pcasize", "PCA")}
LAYER_RUNS = {"q9": "qwen35_9b_x0_pcaeq", "q27": "x0_pcaeq_27b", "q122": "qwen35_122b_x0_parts",
              "mu": "muse30b_x0_parts"}  # fmt: skip
SET = "jsuite_v2_test_chat"
MODEL = {"q9": "qwen3.5-9b", "q27": "qwen3.6-27b", "q122": "qwen3.5-122b-a10b", "mu": "muse-glimmer-30b"}


def _items() -> dict[str, dict]:
    path = REPO / "data" / "tasks_v2" / SET / "items.jsonl"
    return {it["id"]: it for it in map(json.loads, path.read_text().splitlines())}


def _selected(run: str, cond: str, items: dict) -> dict[str, dict[str, bool]]:
    """final (K or M) -> {item id: correct under cond}, over the items the unedited model gets right (start all, facts)."""
    rows = [json.loads(line) for line in (ABLATE / run / "rows.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    out: dict[str, dict[str, bool]] = {"K": {}, "M": {}}
    for r in rows:
        it = items[r["id"]]
        if r["condition"] != cond or (r["family"], r["id"]) not in ok or it["module"] != "facts" or it["start"] == "R":
            continue
        if it["final"] in out:
            out[it["final"]][r["id"]] = r["correct"]
    return out


def band_difference(lens_run: str, cond_a: str, other_run: str, cond_b: str, draws: int = 1000) -> list[float] | None:
    """(M - K lost, in points) of cond_a minus that of cond_b on the same items, [point, lo, hi]; None when the two do
    not share their items."""
    items = _items()
    a, b = _selected(lens_run, cond_a, items), _selected(other_run, cond_b, items)
    if any(set(a[f]) != set(b[f]) for f in "KM"):
        return None
    cluster = {i: f"{it['relation']}:{it['bridge']}" for i, it in items.items() if it.get("module") == "facts"}
    clusters = sorted({cluster[i] for f in "KM" for i in a[f]})

    def lost(sel: dict[str, bool], pick: collections.Counter) -> float:
        tot = [(c, pick[cluster[i]]) for i, c in sel.items() if pick[cluster[i]]]
        n = sum(m for _, m in tot)
        return 100 * (1 - sum(c * m for c, m in tot) / n)

    def stat(pick: collections.Counter) -> float:
        return (lost(a["M"], pick) - lost(a["K"], pick)) - (lost(b["M"], pick) - lost(b["K"], pick))

    point = stat(collections.Counter({c: 1 for c in clusters}))  # every cluster once: every item weighs one
    rng = random.Random(0)
    boots = sorted(stat(collections.Counter(rng.choice(clusters) for _ in clusters)) for _ in range(draws))
    return [point, boots[int(0.025 * draws)], boots[int(0.975 * draws) - 1]]


def _loss_mk(run: str, cond: str) -> float:
    items = _items()
    s = _selected(run, cond, items)
    loss = {f: 100 * (1 - sum(v.values()) / len(v)) for f, v in s.items()}
    return loss["M"] - loss["K"]


def _plotted(key: str) -> float:
    with CSV.open() as f:
        return next(float(r["value"]) for r in csv.DictReader(f) if r["key"] == key)


def band() -> dict[str, dict[str, dict]]:
    """model -> control -> {v, ci, src, run, ctrl_v}: the lens part minus the control, points."""
    out: dict[str, dict[str, dict]] = {}
    for m, (run, pca_run) in BAND_RUNS.items():
        mk = _loss_mk(run, "paper10")
        for key, (cond, _) in CONTROLS.items():
            other = pca_run if key == "pc" else run
            if other is None:
                continue
            ctrl_v = _loss_mk(other, cond)
            iv = band_difference(run, "paper10", other, cond)
            if iv is None:
                continue
            assert abs(iv[0] - (mk - ctrl_v)) < 1e-6, (m, key)
            plotted = _plotted(f"ko.{m}.mk"), _plotted(f"ko.{m}.{key}")
            assert abs((plotted[0] - plotted[1]) - iv[0]) <= 0.35, (m, key, plotted, iv[0])  # two roundings to 0.1 or 1
            out.setdefault(m, {})[key] = {"v": iv[0], "ci": iv[1:], "mk": mk, "ctrl": ctrl_v,
                                          "src": f"results/ablate_v2/{run}/rows.jsonl" + (f" + {other}" if other != run else "")}  # fmt: skip
    return out


def layer() -> dict[str, dict]:
    """model -> {v, ci, n, src}: the recall's extra loss of the lens part minus the PCA directions (same run), shares."""
    out = {}
    for m, run in LAYER_RUNS.items():
        d = REPO / "results" / "x0_parts" / run
        rows = [json.loads(line) for line in (d / "outcomes.jsonl").read_text().splitlines()]
        rows = [r for r in rows if r["reader"] == X.RECALL]
        sw: dict[str, dict[str, int]] = collections.defaultdict(dict)
        ent: dict[str, str] = {}
        for r in rows:
            key = f"{r['dict']}.{r['arm']}"
            sw[key][r["scene"]] = int(r["switched"])
            ent[r["scene"]] = r["entity"]
        scenes = list(ent)
        arms = {k: [v[s] for s in scenes] for k, v in sw.items() if k in ("-.whole", "jpp.no_part", "jpp.no_rand", "pca_eq.no_part", "pca_eq.no_rand")}
        boot = X.resampled_rates(arms, [ent[s] for s in scenes])
        mean = {k: sum(v) / len(v) for k, v in arms.items()}

        def excess(part: str, g) -> object:
            whole = g["-.whole"]
            return X.dependence(whole, g[f"{part}.no_part"]) - X.dependence(whole, g[f"{part}.no_rand"])

        diff = excess("jpp", mean) - excess("pca_eq", mean)
        lo, hi = X.interval(excess("jpp", boot) - excess("pca_eq", boot))
        stored = {r["quantity"]: float(r["value"]) for r in csv.DictReader((REPO / "data/figures/depth/data.csv").open())
                  if r["figure"] == "fig02" and r["model"] == MODEL[m] and r["quantity"].endswith("recall extra loss")}
        assert abs(float(excess("jpp", mean)) - stored["J++ part: recall extra loss"]) < 1e-6, m
        assert abs(float(excess("pca_eq", mean)) - stored["PCA directions (same size): recall extra loss"]) < 1e-6, m
        out[m] = {"v": float(diff), "ci": [lo, hi], "n": len(scenes), "jpp": float(excess("jpp", mean)),
                  "pca": float(excess("pca_eq", mean)), "src": f"results/x0_parts/{run}/outcomes.jsonl"}
    return out


KEYS = {"band": "f2.band.{m}.{c}", "layer": "f2.layer.{m}.pca"}


def rows() -> list[dict]:
    """The CSV rows (key, figure, model, quantity, value, lo, hi, n, unit, source) for docs/breadth/data.csv."""
    new = []
    for m, per in band().items():
        for c, v in per.items():
            new.append({"key": KEYS["band"].format(m=m, c=c), "figure": "f2", "model": m,
                        "quantity": f"M - K, lens part minus {CONTROLS[c][1]} (paired)", "value": round(v["v"], 1),
                        "lo": round(v["ci"][0]), "hi": round(v["ci"][1]), "n": "", "unit": "points", "source": v["src"]})  # fmt: skip
    for m, v in layer().items():
        new.append({"key": KEYS["layer"].format(m=m), "figure": "f2", "model": m,
                    "quantity": "recall extra loss, lens part minus PCA directions (paired)", "value": round(v["v"], 4),
                    "lo": round(v["ci"][0], 4), "hi": round(v["ci"][1], 4), "n": v["n"], "unit": "share", "source": v["src"]})  # fmt: skip
    return new


def write(new: list[dict]) -> None:
    with CSV.open() as f:
        reader = csv.DictReader(f)
        head, old = reader.fieldnames, list(reader)
    drop = {r["key"] for r in new}
    old = [r for r in old if r["key"] not in drop]
    with CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=head, lineterminator="\r\n")
        w.writeheader()
        w.writerows([*old, *new])


if __name__ == "__main__":
    new = rows()
    for r in new:
        print(f"{r['key']:22s} {r['value']:>8} [{r['lo']}, {r['hi']}]  n={r['n']}")
    if "--write" in sys.argv:
        write(new)
        print(f"wrote {len(new)} rows to {CSV.relative_to(REPO)}")
