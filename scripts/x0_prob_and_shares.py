"""Two checks of the batch-45 brief (Dan, 26 Oct ~18:30; CPU, descriptive, after the data).

T0.3, the probability version of the switch (the TA's sampling question): in the main test (two people swap) at the
layer fixed in advance, "switched" replaced by p_alt, the probability of the changed answer's first token, i.e. the
expected switch rate when sampling at T = 1; extra loss = (1 - P_no_part / P_whole) - (1 - P_no_rand / P_whole) per
reader with P the mean p_alt, the gap = recall's minus lookup's, cluster bootstrap over bridge entities (10,000, seed 0).

T0.4, share aggregation: every "% of the change" in the README is the median over items of the per-item ratio
||P Δ||² / ||Δ||² (x6_routes' extra_losses and x0_parts' median_share). Here, for the identity removal of batch 40
(J++ + pointer + identity outside J++, sanity swap, x6_routes norms.jsonl) and for the J++ part of the main test
(shares.jsonl), the three aggregations side by side: pooled sum ||P Δ||² / sum ||Δ||², the mean of per-item ratios, the
median.

uv run python scripts/x0_prob_and_shares.py          # results/x0_composition/prob-shares-<stamp>/
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.utils import git_state
from scripts import x0_composition as C
from scripts import x0_necessity as X

MAIN = {t: runs[0][1] for t, (_, runs, _) in C.RUNS.items()}  # the two-people-swap run per model
LAYER = {t: layer for t, (layer, _, _) in C.RUNS.items()}
D1 = {
    "qwen3.5-9b": "qwen35_9b_x6_routes_d1",
    "qwen3.6-27b": "x6_routes_d1_27b",
    "muse-glimmer-30b": "muse30b_x6_routes_d1_r2",
}
ARMS = ("whole", "no_part", "no_rand")


def prob_cells(rows: list[dict], layer: int, n_boot: int) -> dict:
    """Per reader the extra loss on p_alt (expected switches at T = 1), and on the 0/1 switch for comparison; the gaps."""
    mine = [r for r in rows if r["rendering"] == "chat" and r["layer"] == layer
            and (r["arm"] == "whole" or (r["dict"], r["k"], r["omp"]) == ("jpp", X.K_MAIN, "signed"))]  # fmt: skip
    p = {(r["scene"], r["reader"], r["arm"]): r for r in mine}
    scenes = sorted({r["scene"] for r in mine if r["arm"] == "whole"})
    ent = [next(r["entity"] for r in mine if r["scene"] == s) for s in scenes]
    out = {"n": len(scenes)}
    for field, tag in (("p_alt", "prob"), ("switched", "switch")):
        vals = {f"{w}|{a}": [float(p[(s, w, a)][field]) for s in scenes] for w in X.READERS for a in ARMS}
        r_ = X.resampled_rates(vals, ent, n_boot)
        m_ = {k: float(np.mean(v)) for k, v in vals.items()}

        def ex(src, w):
            return X.dependence(src[f"{w}|whole"], src[f"{w}|no_part"]) - X.dependence(
                src[f"{w}|whole"], src[f"{w}|no_rand"]
            )

        for w, k in ((X.LOOKUP, "lookup"), (X.RECALL, "recall")):
            out[f"{tag}_{k}"] = [float(ex(m_, w)), *X.interval(ex(r_, w))]
            out[f"{tag}_{k}_whole"] = m_[f"{w}|whole"]
        out[f"{tag}_gap"] = [
            float(ex(m_, X.RECALL) - ex(m_, X.LOOKUP)),
            *X.interval(ex(r_, X.RECALL) - ex(r_, X.LOOKUP)),
        ]
    return out


def aggregations(ratio: np.ndarray, norm2: np.ndarray) -> dict:
    """The share of the change three ways: pooled, the mean of per-item ratios, the median."""
    return {"pooled": float((ratio * norm2).sum() / norm2.sum()), "mean": float(ratio.mean()),
            "median": float(np.median(ratio)), "n": int(len(ratio))}  # fmt: skip


def main() -> None:
    out = C.RESULTS / f"prob-shares-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = ["# The switch as a probability, and how shares of the change are aggregated (descriptive, after the data)", "",
             "## T0.3: extra loss with the switch replaced by p_alt (expected switches when sampling at T = 1)", "",
             "Main test (two people swap), the layer fixed in advance, J++ at 25 signed-OMP directions against a random "
             "part of the same share; cluster bootstrap over bridge entities (10,000, seed 0). UNVERIFIED.", "",
             "| model | n | lookup, p_alt | recall, p_alt | gap, p_alt | gap, switches (pre-registered) |",
             "|---|---|---|---|---|---|"]  # fmt: skip
    blob = {"prob": {}, "shares": {}}
    for target, run in MAIN.items():
        c = prob_cells(X.read_jsonl(pins.RESULTS_DIR / run / "outcomes.jsonl"), LAYER[target], X.N_BOOT)
        blob["prob"][target] = {"run": run, **c}
        lines.append(f"| {target} | {c['n']} | {ci(c['prob_lookup'])} | {ci(c['prob_recall'])} | {ci(c['prob_gap'])} | "
                     f"{ci(c['switch_gap'])} |")  # fmt: skip
    lines += ["", "## T0.4: a share of the change, three ways", "",
              "Every '% of the change' in the README is the median over items of ||P Δ||² / ||Δ||². Pooled: sum ||P Δ||² / "
              "sum ||Δ||²; mean: the mean of the per-item ratios.", "",
              "| model | part | scenes | n | median (the README's) | mean of per-item ratios | pooled |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for target, run in D1.items():
        norms = [
            r for r in X.read_jsonl(pins.RESULTS_DIR / "x6_routes" / run / "norms.jsonl") if r["condition"] == "C0"
        ]
        key = "share_jpp+alf+idout"
        if not norms or key not in norms[0]:
            continue
        ag = aggregations(np.array([r[key] for r in norms]), np.array([r["norm"] ** 2 for r in norms]))
        blob["shares"][f"{target}|jpp+alf+idout"] = {"run": run, **ag}
        lines.append(f"| {target} | J++ + pointer + identity outside J++ | sanity swap | {ag['n']} | {100 * ag['median']:.0f}% | "
                     f"{100 * ag['mean']:.0f}% | {100 * ag['pooled']:.0f}% |")  # fmt: skip
    for target, run in MAIN.items():
        sh = [r for r in X.read_jsonl(pins.RESULTS_DIR / run / "shares.jsonl")
              if r["layer"] == LAYER[target] and (r["dict"], r["k"], r["omp"]) == ("jpp", X.K_MAIN, "signed")]  # fmt: skip
        if not sh or "norm" not in sh[0]:
            ag = {"median": float(np.median([r["share"] for r in sh])), "mean": float(np.mean([r["share"] for r in sh])),
                  "pooled": float("nan"), "n": len(sh)}  # fmt: skip
        else:
            ag = aggregations(np.array([r["share"] for r in sh]), np.array([r["norm"] ** 2 for r in sh]))
        blob["shares"][f"{target}|jpp"] = {"run": run, **ag}
        pooled = "–" if ag["pooled"] != ag["pooled"] else f"{100 * ag['pooled']:.0f}%"
        lines.append(f"| {target} | J++ (25 directions) | main test | {ag['n']} | {100 * ag['median']:.0f}% | "
                     f"{100 * ag['mean']:.0f}% | {pooled} |")  # fmt: skip
    m = {"run": out.name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "code": git_state(),
         "note": "Dan 26 Oct ~18:30, T0.3 and T0.4"}  # fmt: skip
    (out / "prob_shares.json").write_text(json.dumps({"manifest": m, **blob}, indent=1) + "\n")
    (out / "prob_shares.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
