"""The split by sentence order (Dan, 26 Oct ~18:30, batch-45 brief T0.2; CPU, descriptive, after the data).

For every model and design (two people swap: the main test; only the asked pick changes: the one-pick runs; fresh
scenes: the replication runs, every scene with both locker sentences before the pick, i.e. the README's "matched"
scenes), at the layer fixed in advance, the lookup's and the recall's J++ extra loss (25 signed-OMP directions, against a
random part of the same share) and the gap (recall minus lookup, both readers on the same cluster resamples), for all
scenes, the scenes whose original bridge's locker sentence comes before the asked pick, and those where it comes after.
The pre-registered numbers are the "all" rows of the main test; nothing here replaces them. Cluster bootstrap over bridge
entities, 10,000 resamples, seed 0. Also the lookup's switch rate under the whole change per group (why the lookup is
measurable only where the locker comes first).

uv run python scripts/x0_split_by_order.py          # results/x0_composition/split-by-order-<stamp>/, docs/depth/notes/split_by_order.md
uv run python scripts/x0_split_by_order.py --targets nemotron-3.5-lightning --no-docs   # batch 52 C: Lightning alone
"""

from __future__ import annotations

import argparse
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
from scripts import x0_strata as ST

DESIGN = {"two people swap": "swap", "only the asked pick": "one",
          "only the asked pick (replication, fresh scenes)": "fresh"}  # fmt: skip
GROUPS = ("all", "before", "after")


def coverage_runs() -> dict:
    """Batch 52 C (amendment 3, key row 5): Lightning's conflict run at its committed layer (layer.json at HEAD), the
    main test only (its one-pick and fresh designs never ran there); C.RUNS' shape (layer, [(design, dir)], None)."""
    from scripts import x51_lightning as L6

    return {L6.TARGET: (L6.committed_layer(), [("two people swap", "x0_necessity/nem35l_x52_conflict")], None)}


ARMS = ("whole", "no_part", "no_rand")


def group_cells(
    rows: list[dict], cases: dict[str, dict], layer: int, n_boot: int, rendering: str = "chat"
) -> dict[str, dict]:
    """Per group (all / before / after): each reader's extra loss and switch rate, and the gap, on paired resamples
    (one rendering's rows: chat, or nochat for a run without the chat template)."""
    mine = [r for r in rows if r["rendering"] == rendering and r["layer"] == layer and r["dict"] in ("-", "jpp")
            and (r["arm"] == "whole" or (r["dict"], r["k"], r["omp"]) == ("jpp", X.K_MAIN, "signed"))]  # fmt: skip
    got = {(r["scene"], r["reader"], r["arm"]): r["switched"] for r in mine}
    done = sorted({r["scene"] for r in mine if r["arm"] == "whole"})
    order = {s: ST.features(cases[s])["org locker vs asked pick"] for s in done}
    ent = {r["scene"]: r["entity"] for r in mine}
    out = {}
    for g in GROUPS:
        scenes = [s for s in done if g == "all" or order[s] == g]
        if not scenes:
            continue
        sw = {f"{w}|{a}": [got[(s, w, a)] for s in scenes] for w in X.READERS for a in ARMS}
        r_ = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
        s_ = {k: float(np.mean(v)) for k, v in sw.items()}

        def excess(src, w):
            return X.dependence(src[f"{w}|whole"], src[f"{w}|no_part"]) - X.dependence(
                src[f"{w}|whole"], src[f"{w}|no_rand"]
            )

        cell = {"n": len(scenes)}
        for w, k in ((X.LOOKUP, "lookup"), (X.RECALL, "recall")):
            cell[k] = [float(excess(s_, w)), *X.interval(excess(r_, w))]
            cell[f"{k}_switch"] = s_[f"{w}|whole"]
        gap = excess(r_, X.RECALL) - excess(r_, X.LOOKUP)
        cell["gap"] = [cell["recall"][0] - cell["lookup"][0], *X.interval(gap)]
        out[g] = cell
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--targets", nargs="+", default=None, help="these models only (default: x0_composition.RUNS')")
    ap.add_argument("--no-docs", action="store_true", help="do not rewrite docs/depth/notes/split_by_order.md (batch 52 coverage)")
    a = ap.parse_args()
    runs = dict(C.RUNS)
    if a.targets and any(t not in runs for t in a.targets):
        runs |= coverage_runs()
    runs = {t: v for t, v in runs.items() if not a.targets or t in a.targets}
    assert runs, f"no runs for {a.targets}"
    out = C.RESULTS / f"split-by-order-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    ci = lambda v: "–" if v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = ["# The split by sentence order (descriptive, after the data)", "",
             "J++ extra loss per reader and the gap (recall minus lookup, paired resamples) at the layer fixed in advance, "
             "by where the original bridge's locker sentence sits relative to the asked pick. Fresh scenes are the "
             "README's matched scenes (both locker sentences before the pick by construction). The pre-registered "
             f"numbers are the main test's 'all' rows. Cluster bootstrap over bridge entities ({a.n_boot} resamples, seed "
             "0). Lookup switch: the share of lookups the whole change switches (the lookup's extra loss is a share of "
             "those switches, so it is measurable only where they are many). UNVERIFIED.", "",
             "| model | design | locker vs pick | n | lookup switch | lookup extra loss | recall extra loss | gap |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob = {}
    for target, (layer, designs, _) in runs.items():
        for design, d in designs:
            src = pins.RESULTS_DIR / d
            if not (src / "outcomes.jsonl").exists():
                continue
            cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
            cells = group_cells(X.read_jsonl(src / "outcomes.jsonl"), cases, layer, a.n_boot)
            blob[f"{target}|{DESIGN[design]}"] = {"run": d, "layer": layer, "cells": cells}
            for g, c in cells.items():
                lines.append(f"| {target} | {design} | {g} | {c['n']} | {c['lookup_switch']:.2f} | {ci(c['lookup'])} | "
                             f"{ci(c['recall'])} | {ci(c['gap'])} |")  # fmt: skip
    m = {"run": out.name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "code": git_state(),
         "n_boot": a.n_boot, "inputs": {k: v["run"] for k, v in blob.items()}, "note": "Dan 26 Oct ~18:30, T0.2"}  # fmt: skip
    (out / "split.json").write_text(json.dumps({"manifest": m, "cells": blob}, indent=1) + "\n")
    (out / "split.md").write_text("\n".join(lines) + "\n")
    if not a.no_docs:
        (pins.REPO_ROOT / "docs" / "depth" / "notes" / "split_by_order.md").write_text(
            "\n".join(lines) + f"\n\nSource: {out.relative_to(pins.REPO_ROOT)}.\n"
        )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
