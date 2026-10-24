"""x0_descriptive: descriptive tables beside an X0 run's verdict (critic's requests, 24 Oct; added after data, not part
of the rule). Writes results/x0_necessity/<run>/descriptive-<UTC>/{tables.md, cells.json}; never touches the run's files.

- Every cell (rendering, layer, reader, dictionary, k, fit), on all items and on the asked-first subset: n, S_whole,
  S_noD, S_noRand, the absolute drops S_whole - S_noD and S_whole - S_noRand with 95% cluster-bootstrap CIs, Jdep,
  Rdep, excess with CIs, the median share of ||Δ||² removed, the label.
- Per rendering and reader, across layers: Pearson and Spearman correlation of the J++ share (median) with Jdep and
  with excess (J++, k = 25).
- The rule at the predicted layer as written (X0.md section 2) and its D3 consequence.
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x0_necessity as X

NOTE = "Added after data, not part of the rule."
D3 = {"confirmed": "X1-X4 run on this model",
      "killed": "this model leaves X1-X4",
      "not confirmed": "README says \"not confirmed\"; X1-X4 run only where the lookup is \"around\" at the predicted layer",
      "can't tell": "treated as \"not confirmed\" for the stop rule (D3c): this model's X1-X4 legs do not run"}  # fmt: skip


def drops(switched: dict[str, list[int]], entities: list[str], n_boot: int) -> dict[str, list[float]]:
    """S_whole - S_noD and S_whole - S_noRand, point and 95% interval from the same paired cluster bootstrap as cell()."""
    r = X.resampled_rates(switched, entities, n_boot)
    n = len(entities)
    s = {a: sum(switched[a]) / n for a in X.ARMS}
    return {key: [s["whole"] - s[arm], *X.interval(r["whole"] - r[arm])]
            for key, arm in (("drop_noD", "no_part"), ("drop_noRand", "no_rand"))}  # fmt: skip


def all_cells(rows: list[dict], n_boot: int) -> dict[tuple, dict]:
    """cells_of() plus the absolute drops, keyed (rendering, layer, reader, dict, k, fit)."""
    cells = X.cells_of(rows, n_boot)
    whole: dict[tuple, dict[str, int]] = collections.defaultdict(dict)
    part: dict[tuple, dict[str, dict[str, int]]] = collections.defaultdict(lambda: collections.defaultdict(dict))
    entity = {}
    for r in rows:
        entity[r["scene"]] = r["entity"]
        at = (r["rendering"], r["layer"], r["reader"])
        if r["arm"] == "whole":
            whole[at][r["scene"]] = r["switched"]
        elif r["arm"] in ("no_part", "no_rand"):
            part[(*at, r["dict"], r["k"], r["omp"])][r["arm"]][r["scene"]] = r["switched"]
    for key, c in cells.items():
        scenes = sorted(whole[key[:3]])
        sw = {"whole": [whole[key[:3]][s] for s in scenes], **{a: [part[key][a][s] for s in scenes] for a in part[key]}}
        c.update(drops(sw, [entity[s] for s in scenes], n_boot))
    return cells


def correlations(cells: dict[tuple, dict], med: dict[tuple, float], rend: str) -> dict[str, dict]:
    """Per reader, across layers: Pearson and Spearman r of the J++ share with Jdep and with excess (J++, k = 25)."""
    out = {}
    rank = lambda v: np.argsort(np.argsort(v))  # noqa: E731
    for w in X.READERS:
        layers = sorted(k[1] for k, c in cells.items() if k[0] == rend and k[2] == w and k[3:] == X.MAIN and c["valid"])
        share = np.array([med[(rend, la, *X.MAIN)] for la in layers])
        for what in ("Jdep", "excess"):
            y = np.array([cells[(rend, la, w, *X.MAIN)][what][0] for la in layers])
            ok = len(layers) >= 3
            out[f"{w} {what}"] = {"layers": layers, "n_layers": len(layers),
                                  "pearson": round(float(np.corrcoef(share, y)[0, 1]), 3) if ok else None,
                                  "spearman": round(float(np.corrcoef(rank(share), rank(y))[0, 1]), 3) if ok else None}  # fmt: skip
    return out


def fmt(v: list[float]) -> str:
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def table(cells: dict[tuple, dict], med: dict[tuple, float], rend: str, keep) -> list[str]:
    lines = ["| layer | reader | dict | k | fit | n | S_whole | S_noD | S_noRand | S_whole − S_noD | S_whole − S_noRand | "
             "Jdep | Rdep | excess | share | label |", "|" + "---|" * 16]  # fmt: skip
    order = lambda kv: (kv[0][1], kv[0][3] != "jpp", kv[0][3], kv[0][4], kv[0][5], kv[0][2] != X.LOOKUP)  # noqa: E731
    for (rr, la, w, d, k, omp), c in sorted(cells.items(), key=order):
        if rr != rend or not keep(la, d, k, omp):
            continue
        lines.append(f"| {la} | {'lookup' if w == X.LOOKUP else 'recall'} | {d} | {k} | {omp} | {c['n']} | "
                     f"{c['S_whole'][0]:.2f} | {c['S_no_part'][0]:.2f} | {c['S_no_rand'][0]:.2f} | {fmt(c['drop_noD'])} | "
                     f"{fmt(c['drop_noRand'])} | {fmt(c['Jdep'])} | {fmt(c['Rdep'])} | {fmt(c['excess'])} | "
                     f"{med.get((rr, la, d, k, omp), float('nan')):.3f} | {c['label']} |")  # fmt: skip
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="X0 run (results/x0_necessity/<name>/)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    src = X.RESULTS / a.name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    share = collections.defaultdict(list)
    for r in X.read_jsonl(src / "shares.jsonl"):
        share[(r["rendering"], r["layer"], r["dict"], r["k"], r["omp"])].append(r["share"])
    med = {k: statistics.median(v) for k, v in share.items()}
    pred = m["predicted"]
    blob: dict = {"run": a.name, "predicted": pred, "note": NOTE, "renderings": {}}
    lines = [f"# X0 descriptive tables: {a.name} ({m['model']['target']})", "",
             f"{NOTE} Requested 24 Oct after the first results. Run commit {m['code'].get('sha', '?')[:8]}; "
             f"bootstrap over the org bridge entity, {a.n_boot} resamples, seed {X.BOOT_SEED}. UNVERIFIED. The "
             "lookup-vs-recall difference is called a graded contrast; \"split\" is used only where the labels say "
             "around (lookup) and through (recall) at the same layer.", ""]  # fmt: skip
    for rend in [r for r in X.RENDERINGS if any(row["rendering"] == r for row in rows)]:
        mine = [r for r in rows if r["rendering"] == rend]
        full, first = all_cells(mine, a.n_boot), all_cells([r for r in mine if not r["upstream"]], a.n_boot)
        v = X.verdict_of(full, pred, (rend,))[rend]
        corr = correlations(full, med, rend)
        blob["renderings"][rend] = {"verdict": v, "d3": D3.get(v["verdict"]), "correlations": corr,
                                    "cells": [{"subset": s, "layer": k[1], "reader": k[2], "dict": k[3], "k": k[4],
                                               "omp": k[5], **c} for s, cs in (("all", full), ("asked_first", first))
                                              for k, c in sorted(cs.items())]}  # fmt: skip
        lines += [f"## {rend}", "",
                  f"**The rule at layer {pred}, as written (X0.md section 2):** {v['verdict'].upper()} (lookup "
                  f"{v['lookup_label']}, recall {v['recall_label']}). D3: {D3.get(v['verdict'], '-')}. Split layers "
                  f"(labels): {v['split_layers'] or 'none'}.", "",
                  "### J++ (k = 25, signed), every layer, all items", "",
                  *table(full, med, rend, lambda la, d, k, omp: (d, k, omp) == X.MAIN), "",
                  f"### Every dictionary, k and fit at layer {pred}, all items", "",
                  *table(full, med, rend, lambda la, d, k, omp: la == pred), "",
                  f"### Asked-first subset (the asked person's pick comes first; no upstream change in Δ). {NOTE}", "",
                  *table(first, med, rend, lambda la, d, k, omp: (d, k, omp) == X.MAIN or la == pred), "",
                  f"### J++ share of ||Δ||² against Jdep and excess, across layers (J++, k = 25). {NOTE}", "",
                  "| reader, quantity | valid layers | Pearson r | Spearman r |", "|---|---|---|---|",
                  *[f"| {k} | {c['layers']} | {c['pearson']} | {c['spearman']} |" for k, c in corr.items()], ""]  # fmt: skip
    out = src / f"descriptive-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "tables.md").write_text("\n".join(lines) + "\n")
    (out / "cells.json").write_text(json.dumps(blob, indent=1) + "\n")
    print(out)


if __name__ == "__main__":
    main()
