"""x47_margins (batch 47, test 47.0b; jobs/c3/batch47.yaml; descriptive, CPU only): the margins of the non-switchers.

The cheapest "why not every answer switches": per design (the main test: x0_necessity's two-people swap; the clean
design: 45m's fresh one-pick runs), model and reader, the unedited logit margin, logit(original answer) - logit(changed
answer) = -ld on the arm "none" at the layer fixed in advance (chat), of the items the whole change switches (arm
"whole", X0's top-token read) against those it does not. Means with 95% intervals from a cluster bootstrap over the
bridge items (10,000 resamples, seed 0; the switchers' and the stayers' means on the same draws, so the difference is
paired); medians, the AUC (the chance a random stayer's margin is above a random switcher's; ties 1/2) and the unedited
p_org beside, point estimates. Groups: all scenes, and the scenes whose original bridge's locker sentence comes before
the asked pick (x0_strata's 'org locker vs asked pick', as in x0_split_by_order). 47.4 is the causal test.

uv run python scripts/x47_margins.py        # results/x47_margins/<stamp>/ (manifest.json, margins.json, margins.md)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.utils import git_state
from scripts import x0_necessity as X
from scripts import x0_strata as ST

EXP = "x47_margins"
RESULTS = pins.RESULTS_DIR / EXP
# design -> target -> x0_necessity run (the main test's runs as x0_composition.RUNS / x0_details.MODELS name them)
RUNS = {
    "main test": {"qwen3.5-9b": "qwen35_9b_x0_necessity", "qwen3.6-27b": "x0_necessity_27b_chat",
                  "muse-glimmer-30b": "muse30b_x0_necessity"},
    "clean design": {"qwen3.5-9b": "qwen35_9b_x45m_fresh", "qwen3.6-27b": "x45m_fresh_27b",
                     "muse-glimmer-30b": "muse30b_x45m_fresh"},
}  # fmt: skip
GROUPS = ("all", "before")  # all scenes; the original bridge's locker sentence before the asked pick
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
FEW = 10  # a group with fewer items is marked in the table (its mean and interval are noise)


def items(rows: list[dict], layer: int, reader: str) -> list[dict]:
    """One reader's items at the layer (chat): scene, entity, the unedited margin (-ld on 'none'), p_org, p_alt (on
    'none') and the whole change's switch; asserts one 'none' and one 'whole' row per scene."""
    mine = [r for r in rows if r["rendering"] == "chat" and r["layer"] == layer and r["reader"] == reader
            and r["arm"] in ("none", "whole")]  # fmt: skip
    by: dict[tuple[str, str], dict] = {}
    for r in mine:
        key = (r["scene"], r["arm"])
        assert key not in by, f"two {r['arm']} rows for {r['scene']} ({reader}, layer {layer})"
        by[key] = r
    scenes = sorted({s for s, _ in by})
    out = []
    for s in scenes:
        none, whole = by[(s, "none")], by[(s, "whole")]
        out.append({"scene": s, "entity": none["entity"], "margin": -float(none["ld"]), "p_org": none["p_org"],
                    "p_alt": none["p_alt"], "switched": int(whole["switched"])})  # fmt: skip
    return out


def auc(stay: np.ndarray, switch: np.ndarray) -> float:
    """P(a random stayer's margin > a random switcher's), ties 1/2 (Mann-Whitney); nan if a group is empty."""
    from scipy.stats import rankdata

    if not len(stay) or not len(switch):
        return float("nan")
    r_stay = rankdata(np.concatenate([stay, switch]))[: len(stay)].sum()  # average ranks over ties
    return float((r_stay - len(stay) * (len(stay) + 1) / 2) / (len(stay) * len(switch)))


def margin_cell(
    margin: list[float], switched: list[int], entities: list[str], n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED
) -> dict:
    """Switchers' vs stayers' unedited margins: n, means [point, lo, hi], the difference stayers - switchers [point,
    lo, hi], medians, AUC. Cluster bootstrap over entities with X.resampled_rates' draws (same seed -> same draws);
    a resample without a switcher or a stayer is nan and dropped from the percentiles."""
    m = np.asarray(margin, dtype=float)
    sw = np.asarray(switched, dtype=bool)
    assert len(m) == len(sw) == len(entities)
    keys = sorted(set(entities))
    index = {e: i for i, e in enumerate(keys)}
    ent = np.array([index[e] for e in entities])
    pick = np.random.default_rng(seed).integers(0, len(keys), size=(n_boot, len(keys)))

    def resampled_mean(mask: np.ndarray) -> np.ndarray:
        sums = np.bincount(ent, weights=np.where(mask, m, 0.0), minlength=len(keys))
        cnt = np.bincount(ent, weights=mask.astype(float), minlength=len(keys))
        num, den = sums[pick].sum(1), cnt[pick].sum(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)

    def point(mask: np.ndarray) -> float:
        return float(m[mask].mean()) if mask.any() else float("nan")

    r_sw, r_st = resampled_mean(sw), resampled_mean(~sw)
    p_sw, p_st = point(sw), point(~sw)

    def ci(p: float, r: np.ndarray) -> list[float]:
        if math.isnan(p) or np.isnan(r).all():
            return [p, float("nan"), float("nan")]
        return [p, *X.interval(r)]

    return {"n": len(m), "entities": len(keys), "n_switch": int(sw.sum()), "n_stay": int((~sw).sum()),
            "mean_switch": ci(p_sw, r_sw), "mean_stay": ci(p_st, r_st), "diff": ci(p_st - p_sw, r_st - r_sw),
            "median_switch": float(np.median(m[sw])) if sw.any() else float("nan"),
            "median_stay": float(np.median(m[~sw])) if (~sw).any() else float("nan"),
            "auc": auc(m[~sw], m[sw])}  # fmt: skip


def none_stable(rows: list[dict], reader: str) -> float:
    """Max |ld| difference of the unedited ('none') read across the run's layers per scene: the unedited read has no
    edit, so it should not depend on the layer (a check that the fixed layer's 'none' rows are the unedited run)."""
    ld: dict[str, list[float]] = {}
    for r in rows:
        if r["rendering"] == "chat" and r["reader"] == reader and r["arm"] == "none":
            ld.setdefault(r["scene"], []).append(float(r["ld"]))
    return round(max((max(v) - min(v) for v in ld.values()), default=0.0), 3)


def run_cells(run: str, target: str, n_boot: int) -> dict:
    src = X.RESULTS / run
    layer = X.PREDICTED[target]
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    out: dict = {"run": f"results/x0_necessity/{run}", "layer": layer, "cells": {}, "checks": {}}
    for w in X.READERS:
        its = items(rows, layer, w)
        out["checks"][f"{READER_NAME[w]}: max |ld| spread of 'none' across layers"] = none_stable(rows, w)
        out["checks"][f"{READER_NAME[w]}: unedited margins <= 0 (org not on top)"] = sum(i["margin"] <= 0 for i in its)
        order = {i["scene"]: ST.features(cases[i["scene"]])["org locker vs asked pick"] for i in its}
        for g in GROUPS:
            sub = [i for i in its if g == "all" or order[i["scene"]] == g]
            if not sub:
                continue
            c = margin_cell([i["margin"] for i in sub], [i["switched"] for i in sub], [i["entity"] for i in sub],
                            n_boot)  # fmt: skip
            sw = [i for i in sub if i["switched"]]
            st = [i for i in sub if not i["switched"]]
            c["p_org_switch"] = float(np.mean([i["p_org"] for i in sw])) if sw else float("nan")
            c["p_org_stay"] = float(np.mean([i["p_org"] for i in st])) if st else float("nan")
            out["cells"][f"{READER_NAME[w]}|{g}"] = c
    return out


def fmt(v: list[float]) -> str:
    return "–" if v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−")


def table(blob: dict) -> list[str]:
    """The markdown table (also what scripts/x0_details.py renders into docs/x0_details.md)."""
    name = {"qwen3.5-9b": "Qwen3.5-9B", "qwen3.6-27b": "Qwen3.6-27B", "muse-glimmer-30b": "Muse Glimmer 30B"}
    lines = ["| design | model (layer) | reader | scenes | n switch / stay | margin, switchers | margin, stayers | "
             "stayers − switchers | median switch / stay | AUC |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for design, models in blob["designs"].items():
        for target, r in models.items():
            for key, c in r["cells"].items():
                reader, g = key.split("|")
                f2 = lambda x: "–" if x != x else f"{x:.2f}".replace("-", "−")  # noqa: E731
                few = "°" if min(c["n_switch"], c["n_stay"]) < FEW else ""
                lines.append(f"| {design} | {name[target]} (L{r['layer']}) | {reader} | "
                             f"{'all' if g == 'all' else 'locker before the pick'} | {c['n_switch']} / {c['n_stay']}{few} | "
                             f"{fmt(c['mean_switch'])} | {fmt(c['mean_stay'])} | {fmt(c['diff'])} | "
                             f"{f2(c['median_switch'])} / {f2(c['median_stay'])} | {f2(c['auc'])} |")  # fmt: skip
    return [*lines, "", f"° fewer than {FEW} items in a group: its mean and interval are noise."]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    out = RESULTS / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "test": "47.0b (jobs/c3/batch47.yaml)", "descriptive": True,
         "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "code": git_state(), "n_boot": a.n_boot,
         "seed": X.BOOT_SEED, "inputs": {d: {t: f"results/x0_necessity/{r}/outcomes.jsonl" for t, r in runs.items()}
                                         for d, runs in RUNS.items()},
         "margin": "logit(original answer) - logit(changed answer) = -ld on arm 'none' (unedited), chat, the layer fixed "
                   "in advance; switch = arm 'whole' switched (top token = the changed answer's first token)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    blob = {"manifest": m, "designs": {d: {t: run_cells(r, t, a.n_boot) for t, r in runs.items()}
                                       for d, runs in RUNS.items()}}  # fmt: skip
    (out / "margins.json").write_text(json.dumps(blob, indent=1) + "\n")
    lines = ["# 47.0b: margins of the non-switchers (descriptive)", "",
             "Unedited logit margin, logit(original) − logit(changed), of the items the whole change switches against "
             "those it does not, at the layer fixed in advance (chat). Means with 95% cluster-bootstrap intervals over "
             f"bridge items ({a.n_boot} resamples, seed {X.BOOT_SEED}); the difference on paired draws. AUC: the chance a "
             "random stayer's margin is above a random switcher's (0.5 = the margin does not tell them apart). "
             "UNVERIFIED.", "", *table(blob), "", "Checks:"]  # fmt: skip
    for d, models in blob["designs"].items():
        for t, r in models.items():
            lines.append(f"- {d}, {t}: " + "; ".join(f"{k} = {v}" for k, v in r["checks"].items()))
    (out / "margins.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)


if __name__ == "__main__":
    main()
