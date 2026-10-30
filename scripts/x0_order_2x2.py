"""x0_order_2x2: claim 10 (sentence order) with both orders (POST HOC; Dan 30 Oct; CPU, saved x0_necessity runs, report only).

The lookup's switch rate under the whole change at the model's layer, by two features of the scene (x0_strata.features): the ORIGINAL prompt's bridge locker
sentence before / after the asked person's pick sentence ("org locker vs asked pick"), and the CHANGED prompt's bridge locker sentence before / after it ("alt
locker vs asked pick": the changed pick names the new bridge; the locker sentences stay where they are, so this is the new bridge's locker sentence against the
same pick sentence). Per model and cell: n and the switch rate with a 95% cluster-bootstrap interval over the original bridge entity
(x0_necessity.resampled_rates, seed 0; each cell a ratio of resampled sums). Scenes where a bridge has no locker sentence in the context ("none") are left out and
counted.

Effects (rate differences on the same draws): the changed order's effect = the mean over the original orders of [rate(changed before) - rate(changed after)];
the original order's effect = the mean over the changed orders of [rate(original before) - rate(original after)].

Pre-set (Dan 30 Oct): if the changed order's effect is larger than the original order's on at least 3 of 5 models, with the two effects' intervals not overlapping,
draft a reworded claim 10 naming the order that matters (or both); otherwise keep claim 10 and add the 2x2 as a caveat table.

uv run python scripts/x0_order_2x2.py        # writes results/x0_order_2x2/<UTC>/
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import x0_figures as XF  # noqa: E402
from scripts import x0_necessity as X  # noqa: E402
from scripts import x0_strata as ST  # noqa: E402

RUNS = {"qwen3.5-9b": ("qwen35_9b_x0_necessity", 12), "qwen3.6-27b": ("x0_necessity_27b_chat", 32), "muse-glimmer-30b": ("muse30b_x0_necessity", 26),
        "nemotron-3.5-lightning": ("nem35l_x52_conflict", 14), "qwen3.5-122b-a10b": ("qwen35_122b_x0_necessity_r2", 33)}  # fmt: skip
ORDERS = ("before", "after")
EXAMPLES = {"muse-glimmer-30b": ["P2-L0-0208", "P2-L0-0041", "P2-L0-0040"], "qwen3.6-27b": ["P2-L0-0152"]}


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / "x0_order_2x2" / stamp
    out.mkdir(parents=True, exist_ok=False)
    (out / "manifest.json").write_text(json.dumps({"exp": "x0_order_2x2", "post_hoc": True, "cpu": True, "runs": RUNS, "preset": __doc__.split("Pre-set")[1].strip().split("\n\n")[0], "written_utc": stamp}, indent=2) + "\n")  # fmt: skip
    res: dict = {}
    for model, (run, la) in RUNS.items():
        r = XF.Run(run)
        cases = {c["scene"]: c for c in X.read_jsonl(r.dir / "cases.jsonl") if c["rendering"] == "chat"}
        whole = [
            x
            for x in r.rows
            if x["rendering"] == "chat" and x["layer"] == la and x["reader"] == X.LOOKUP and x["arm"] == "whole"
        ]
        feats = {x["scene"]: ST.features(cases[x["scene"]]) for x in whole}
        keep = [
            x
            for x in whole
            if feats[x["scene"]]["org locker vs asked pick"] in ORDERS
            and feats[x["scene"]]["alt locker vs asked pick"] in ORDERS
        ]
        ents = [x["entity"] for x in keep]
        arrays: dict[str, list[float]] = {}
        for o in ORDERS:
            for a in ORDERS:
                inside = [
                    feats[x["scene"]]["org locker vs asked pick"] == o
                    and feats[x["scene"]]["alt locker vs asked pick"] == a
                    for x in keep
                ]
                arrays[f"n_{o}_{a}"] = [float(i) for i in inside]
                arrays[f"s_{o}_{a}"] = [float(i and x["switched"]) for i, x in zip(inside, keep, strict=True)]
        rr = X.resampled_rates(arrays, ents, X.N_BOOT, X.BOOT_SEED)
        pts = {k: float(np.sum(v)) for k, v in arrays.items()}

        def cell(o: str, a: str, rr=rr, pts=pts) -> dict:
            n, s = pts[f"n_{o}_{a}"], pts[f"s_{o}_{a}"]
            with np.errstate(divide="ignore", invalid="ignore"):
                d = rr[f"s_{o}_{a}"] / rr[f"n_{o}_{a}"]
            return {
                "n": int(n),
                "switched": int(s),
                "rate": [round(s / n, 4) if n else None, *(round(v, 4) for v in X.interval(d))],
            }

        def rate(o: str, a: str, rr=rr):
            with np.errstate(divide="ignore", invalid="ignore"):
                return rr[f"s_{o}_{a}"] / rr[f"n_{o}_{a}"]

        def point(o: str, a: str, pts=pts):
            n = pts[f"n_{o}_{a}"]
            return pts[f"s_{o}_{a}"] / n if n else float("nan")

        eff_alt_d = np.mean(
            [rate("before", "before") - rate("before", "after"), rate("after", "before") - rate("after", "after")],
            axis=0,
        )
        eff_org_d = np.mean(
            [rate("before", "before") - rate("after", "before"), rate("before", "after") - rate("after", "after")],
            axis=0,
        )
        eff_alt = float(
            np.mean(
                [
                    point("before", "before") - point("before", "after"),
                    point("after", "before") - point("after", "after"),
                ]
            )
        )
        eff_org = float(
            np.mean(
                [
                    point("before", "before") - point("after", "before"),
                    point("before", "after") - point("after", "after"),
                ]
            )
        )
        ci_alt, ci_org = [round(v, 4) for v in X.interval(eff_alt_d)], [round(v, 4) for v in X.interval(eff_org_d)]
        larger = abs(eff_alt) > abs(eff_org)
        separate = (ci_alt[0] > max(ci_org[1], 0)) if eff_alt > 0 else (ci_alt[1] < min(ci_org[0], 0))
        ex = []
        for sc in EXAMPLES.get(model, []):
            row = next((x for x in whole if x["scene"] == sc), None)
            if row:
                ex.append(
                    {
                        "scene": sc,
                        "original": feats[sc]["org locker vs asked pick"],
                        "changed": feats[sc]["alt locker vs asked pick"],
                        "switched": int(row["switched"]),
                    }
                )
        res[model] = {"run": run, "layer": la, "lookups": len(whole), "in_2x2": len(keep), "left_out_no_locker_sentence": len(whole) - len(keep),
                      "cells": {f"original {o} / changed {a}": cell(o, a) for o in ORDERS for a in ORDERS},
                      "changed_order_effect": [round(eff_alt, 4), *ci_alt], "original_order_effect": [round(eff_org, 4), *ci_org],
                      "changed_larger_than_original": bool(larger), "intervals_separate_in_changed_favour": bool(larger and separate), "examples": ex}  # fmt: skip
    n_ok = sum(m["intervals_separate_in_changed_favour"] for m in res.values())
    res["_rule"] = {
        "models_where_the_changed_order_matters_more": n_ok,
        "of": len(RUNS),
        "outcome": "draft a reworded claim 10" if n_ok >= 3 else "keep claim 10; the 2x2 is a caveat table",
    }
    (out / "tables.json").write_text(json.dumps(res, indent=1) + "\n")
    L = [
        "# Claim 10: the lookup's switch rate under the whole change by both orders (post hoc)\n",
        f"Rule: {res['_rule']}\n",
    ]
    f = lambda v: "-" if v[0] is None else f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]"  # noqa: E731
    for m, d in res.items():
        if m == "_rule":
            continue
        L.append(f"## {m} (L{d['layer']}; {d['in_2x2']} of {d['lookups']} lookups in the 2x2)\n")
        L.append("| | changed before | changed after |\n|---|---|---|")
        for o in ORDERS:
            L.append(
                f"| original {o} | "
                + " | ".join(
                    f"{d['cells'][f'original {o} / changed {a}']['n']}: {f(d['cells'][f'original {o} / changed {a}']['rate'])}"
                    for a in ORDERS
                )
                + " |"
            )
        L.append(
            f"\nchanged order's effect {f(d['changed_order_effect'])}; original order's effect {f(d['original_order_effect'])}; examples {d['examples']}\n"
        )
    (out / "tables.md").write_text("\n".join(L) + "\n")
    print(out)
    return out


if __name__ == "__main__":
    main()
