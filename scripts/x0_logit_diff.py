"""x0_logit_diff (batch 39, Dan 26 Oct ~10:30 / ~11:55; CPU): the split on the logit difference instead of switches.

The main test (two people swap picks), chat, each model's layer fixed in advance (9B L12, 27B L32, 122B L33, Muse L26),
the J++ part (25 directions, signed) and its random part, the scenes the main test used. An item's logit difference
`ld` = the swapped answer's logit minus the original answer's, at the answer position; its shift under an arm =
ld(arm) - ld(none). The fraction of the shift lost without a part = 1 - mean shift without it / mean shift of the whole
change, over a reader's items; extra loss = without J++ minus without its random part; gap = the recall's minus the
lookup's (point estimate). Cluster bootstrap over bridge entities (10,000 resamples, seed 0, paired across arms).
Q39.1: models with gap >= 0.20 (all four / three / two or fewer). Q39.2 (the 27B): items (scene, reader) in terciles of
the whole change's shift, cut points from both readers pooled; per tercile the switch-based gap (X0's cells); a tercile
counts if each reader has >= 30 items switched by the whole change in it; fewer than two counting terciles: can't tell.
Descriptive: each reader's median whole-change shift per model.
Writes results/x0_logit_diff/<name>/{ld.json, ld.md}. UNVERIFIED.

uv run python scripts/x0_logit_diff.py --name x0_logit_diff_20261026
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
from scripts import x0_necessity as X

RESULTS = pins.RESULTS_DIR / "x0_logit_diff"
RUNS = {"9B": ("qwen35_9b_x0_necessity", 12), "27B": ("x0_necessity_27b_chat", 32),
        "122B": ("qwen35_122b_x0_necessity_r2", 33), "Muse": ("muse30b_x0_necessity", 26)}  # fmt: skip
GAP_BAR, VALID = 0.20, X.VALID_N
ARMS = ("none", "whole", "no_part", "no_rand")


def items(run: str, layer: int) -> dict[str, dict[str, dict]]:
    """reader -> scene -> {entity, ld per arm, switched per arm} for J++ k = 25 signed at the layer."""
    out: dict[str, dict[str, dict]] = {}
    for r in X.read_jsonl(X.RESULTS / run / "outcomes.jsonl"):
        if r["rendering"] != "chat" or r["layer"] != layer or r["arm"] not in ARMS:
            continue
        if r["arm"] in ("no_part", "no_rand") and (r["dict"], r["k"], r["omp"]) != ("jpp", X.K_MAIN, "signed"):
            continue
        it = out.setdefault(r["reader"], {}).setdefault(r["scene"], {"entity": r["entity"], "ld": {}, "sw": {}})
        it["ld"][r["arm"]] = float(r["ld"])
        it["sw"][r["arm"]] = int(r["switched"])
    return {w: {s: it for s, it in by.items() if set(it["ld"]) == set(ARMS)} for w, by in out.items()}


def ld_extra(by: dict[str, dict], n_boot: int) -> dict:
    """One reader: the fraction of the whole change's ld shift lost without J++ and without its random part, and the
    extra loss, with the resamples (for the paired gap)."""
    scenes = sorted(by)
    ents = [by[s]["entity"] for s in scenes]
    shift = {a: [by[s]["ld"][a] - by[s]["ld"]["none"] for s in scenes] for a in ("whole", "no_part", "no_rand")}
    m = {a: float(np.mean(v)) for a, v in shift.items()}
    r = X.resampled_rates(shift, ents, n_boot)
    lost = {a: float(X.dependence(m["whole"], m[a])) for a in ("no_part", "no_rand")}
    ex_r = X.dependence(r["whole"], r["no_part"]) - X.dependence(r["whole"], r["no_rand"])
    return {"n": len(scenes), "entities": len(set(ents)), "mean_shift": m, "median_whole_shift": float(np.median(shift["whole"])),
            "lost_without_jpp": lost["no_part"], "lost_without_rand": lost["no_rand"],
            "extra": [lost["no_part"] - lost["no_rand"], *X.interval(ex_r)], "_r": ex_r}  # fmt: skip


def gap_of(model: dict, n_boot: int) -> dict:
    """The gap on the ld (recall minus lookup), paired resamples over the entities both readers share."""
    lk, rc = model[X.LOOKUP], model[X.RECALL]
    common = sorted(set(lk) & set(rc))
    a = ld_extra({s: lk[s] for s in common}, n_boot)
    b = ld_extra({s: rc[s] for s in common}, n_boot)
    point = b["extra"][0] - a["extra"][0]
    return {"lookup": {k: v for k, v in a.items() if k != "_r"}, "recall": {k: v for k, v in b.items() if k != "_r"},
            "gap": [point, *X.interval(b["_r"] - a["_r"])], "n_common": len(common)}  # fmt: skip


def terciles(model: dict, n_boot: int) -> dict:
    """Q39.2: items (scene, reader) by tercile of the whole change's ld shift (cut points pooled over the readers); per
    tercile each reader's switch-based X0 cell and the gap."""
    pooled = [(w, s, it["ld"]["whole"] - it["ld"]["none"]) for w, by in model.items() for s, it in by.items()]
    cuts = [float(c) for c in np.quantile([v for *_, v in pooled], [1 / 3, 2 / 3])]
    rows = []
    for t, (lo, hi) in enumerate(((-np.inf, cuts[0]), (cuts[0], cuts[1]), (cuts[1], np.inf))):
        cells = {}
        for w in X.READERS:
            mine = [model[w][s] for ww, s, v in pooled if ww == w and lo <= v < hi]
            sw = {"whole": [i["sw"]["whole"] for i in mine], "no_part": [i["sw"]["no_part"] for i in mine],
                  "no_rand": [i["sw"]["no_rand"] for i in mine]}  # fmt: skip
            cells[w] = X.cell(sw, [i["entity"] for i in mine], n_boot) if mine else None
        ok = all(c is not None and c["switched_whole"] >= VALID for c in cells.values())
        gap = (cells[X.RECALL]["excess"][0] - cells[X.LOOKUP]["excess"][0]) if all(cells.values()) else float("nan")
        rows.append({"tercile": t + 1, "shift_range": [lo, hi], "counts": ok, "gap": gap,
                     **{f"{'lookup' if w == X.LOOKUP else 'recall'}": None if c is None else
                        {"n": c["n"], "switched_whole": c["switched_whole"], "excess": c["excess"]}
                        for w, c in cells.items()}})  # fmt: skip
    counted = [r for r in rows if r["counts"]]
    answer = "can't tell" if len(counted) < 2 else ("yes" if all(r["gap"] >= GAP_BAR for r in counted) else "no")
    return {"cut_points": cuts, "terciles": rows, "counted": len(counted), "answer": answer}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    out = RESULTS / a.name
    out.mkdir(parents=True, exist_ok=False)
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    blob: dict = {"run": a.name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "models": {}}
    lines = [f"# Batch 39: the split on the logit difference ({a.name})", "",
             "The main test (two people swap picks), chat, each model's layer fixed in advance, J++ (25, signed) against "
             "its random part. Fraction of the whole change's ld shift lost; extra loss = without J++ minus without "
             f"random; gap = recall minus lookup. Cluster bootstrap over bridge entities ({a.n_boot} resamples, seed 0). "
             "UNVERIFIED.", "",
             "| model | layer | n | lookup extra loss (ld) | recall extra loss (ld) | gap (ld) | median whole shift, lookup / recall |",
             "|---|---|---|---|---|---|---|"]  # fmt: skip
    passing = 0
    for name, (run, layer) in RUNS.items():
        model = items(run, layer)
        g = gap_of(model, a.n_boot)
        passing += g["gap"][0] >= GAP_BAR
        blob["models"][name] = {"run": run, "layer": layer, **g}
        lines.append(f"| {name} | {layer} | {g['n_common']} | {ci(g['lookup']['extra'])} | {ci(g['recall']['extra'])} | "
                     f"{ci(g['gap'])} | {g['lookup']['median_whole_shift']:.2f} / {g['recall']['median_whole_shift']:.2f} |")  # fmt: skip
        if name == "27B":
            blob["q39_2"] = terciles(model, a.n_boot)
    q1 = "(a) all four" if passing == 4 else "(b) three of four" if passing == 3 else "(c) two or fewer"
    blob["q39_1"] = {"models_with_gap_at_least_0.20": passing, "answer": q1}
    q2 = blob["q39_2"]
    lines += ["", f"Q39.1: gap >= {GAP_BAR} on {passing} of 4 models: {q1}.", "",
              f"Q39.2 (the 27B; cut points {q2['cut_points'][0]:.2f}, {q2['cut_points'][1]:.2f} on the pooled whole shift): "
              f"{q2['counted']} terciles count (each reader >= {VALID} switched): {q2['answer']}.", "",
              "| tercile | counts | lookup n / switched / extra loss | recall n / switched / extra loss | gap (switches) |",
              "|---|---|---|---|---|"]  # fmt: skip
    for r in q2["terciles"]:
        cell = lambda c: "-" if c is None else f"{c['n']} / {c['switched_whole']} / {ci(c['excess'])}"  # noqa: E731
        lines.append(f"| {r['tercile']} | {'yes' if r['counts'] else 'no'} | {cell(r['lookup'])} | {cell(r['recall'])} | "
                     f"{r['gap']:.2f} |")  # fmt: skip
    (out / "ld.json").write_text(json.dumps(blob, indent=1, default=float) + "\n")
    (out / "ld.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
