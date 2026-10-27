"""x0_dup_nearest (Dan, 25 Oct morning item 3; descriptive, after data): on the single-change duplicate-pick pairs, does
the alt state at the bridge word point at the alt's locker sentence or at the alt item's first mention, read by the
nearest class mean in the mass-mean address space (A) and in its layout-free version (Alf)?

Class means: the fresh scenes' locker-before org states at the bridge word (x0_probe_v4 states, d1_topics_v4, disjoint
from the test items), one class per locker-sentence index; A and Alf as in x0_massmean.subspaces (Alf: each layout
group's mean subtracted before the class means). Test: x0_amnesic's single-change items whose org and alt locker
sentences both come before the asked pick; the org state h_org and the alt state h_org + Δ. In A: project the states
and the class means on A, nearest by Euclidean distance. In Alf: subtract the test item's layout-group mean (from the
fresh states; items whose layout has no fresh group are left out and counted), then the same on Alf.
Reported as x0_probe_patched's duplicate-pick split: by where the alt item's other picker's sentence sits, and among
'before' by which earlier mention of the alt item comes first; shares with 95% CIs from a cluster bootstrap over bridge
entities (10,000 resamples, seed 0).

uv run python scripts/x0_dup_nearest.py --fresh x0_probe_v4_27b --single x0_single_27b_r2 --states x0_amnesic_27b \
    --out x0_massmean_lf_27b
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_massmean as MM
from scripts import x0_necessity as X
from scripts import x0_probe as P
from scripts import x0_probe_patched as PP
from scripts import x0_strata as ST

NOTE = "Descriptive, added after data (Dan, 25 Oct morning, item 3); not part of X0's rule."
SPLITS = (("after", "the other pick comes after the asked pick"),
          ("lockerfirst", "before; the alt's locker sentence is the alt item's first mention"),
          ("otherfirst", "before; the other person's pick is the alt item's first mention"))  # fmt: skip


def nearest(x: np.ndarray, means: dict, basis: np.ndarray) -> list:
    """The class whose mean is nearest to each row of x, both projected on the basis' columns."""
    keys = sorted(means, key=str)
    m = np.stack([means[k] @ basis for k in keys])  # [classes, r]
    d = (((x @ basis)[:, None, :] - m[None]) ** 2).sum(-1)
    return [keys[i] for i in d.argmin(1)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fresh", required=True, help="x0_probe run with the fresh scenes' states (A, Alf, class means)")
    ap.add_argument("--single", required=True)
    ap.add_argument("--states", required=True, help="x0_amnesic run with h_org and Δ")
    ap.add_argument("--out", required=True, help="x0_massmean run folder to write into (the layout-free run)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    basis, info = MM.subspaces(a.fresh)
    src = P.RESULTS / a.fresh
    items = X.read_jsonl(src / "items.jsonl")
    keep = [i for i, it in enumerate(items) if it["order"] == "before"]
    h = np.load(src / "states.npz")["h"].astype(np.float64)[keep]
    lab = [items[i]["locker_index"] for i in keep]
    group = [P.layout(items[i]["context"], items[i]["pick_index"]) for i in keep]
    gmean = {g: h[[j for j, x in enumerate(group) if x == g]].mean(0) for g in set(group)}
    res_h = h - np.stack([gmean[g] for g in group])
    means = {"A": {c: h[[j for j, x in enumerate(lab) if x == c]].mean(0) for c in set(lab)},
             "Alf": {c: res_h[[j for j, x in enumerate(lab) if x == c]].mean(0) for c in set(lab)}}  # fmt: skip

    z = np.load(pins.RESULTS_DIR / "x0_amnesic" / a.states / "states.npz")
    scenes = [str(s) for s in z["scene"]]
    h_org, delta = z["h_org"].astype(np.float64), z["delta"].astype(np.float64)
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / a.single / "cases.jsonl") if c["rendering"] == "chat"}
    test, rows, missing = [], [], 0
    for i, s in enumerate(scenes):
        c = cases[s]
        f = ST.features(c)
        if f["org locker vs asked pick"] != "before" or f["alt locker vs asked pick"] != "before":
            continue
        g = P.layout(c["context"], P.positions(c)[0])  # the layout the word sees (identical for org and alt)
        if g not in gmean:
            missing += 1
            continue
        side, other = PP.other_pick(c)
        alt = PP.locker_index(c["context"], c["cf_bridge"])
        split = "after" if side == "after" else ("otherfirst" if other < alt else "lockerfirst")
        test.append(i)
        rows.append({"scene": s, "entity": c["bridge"], "split": split, "org": PP.locker_index(c["context"], c["bridge"]),
                     "alt": alt, "other": other, "layout": g})  # fmt: skip
    idx = np.array(test)
    states = {"org": h_org[idx], "alt": h_org[idx] + delta[idx]}
    lay = np.stack([gmean[r["layout"]] for r in rows])
    pred = {(sp, st): nearest(x - (lay if sp == "Alf" else 0), means[sp], basis[sp])
            for sp in ("A", "Alf") for st, x in states.items()}  # fmt: skip

    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    out_json, lines = {}, []
    for sp in ("A", "Alf"):
        hits = {
            "org state: org's locker sentence": [
                int(p == r["org"]) for p, r in zip(pred[(sp, "org")], rows, strict=True)
            ]
        }
        for key, _ in SPLITS:
            k = [t for t, r in enumerate(rows) if r["split"] == key]
            hits[f"{key}: alt's locker sentence"] = [int(pred[(sp, "alt")][t] == rows[t]["alt"]) for t in k]
            hits[f"{key}: other pick sentence"] = [int(pred[(sp, "alt")][t] == rows[t]["other"]) for t in k]
            hits[f"{key}: org's locker sentence"] = [int(pred[(sp, "alt")][t] == rows[t]["org"]) for t in k]
        res = {}
        for name, v in hits.items():
            ents = ([r["entity"] for r in rows] if name.startswith("org state") else
                    [rows[t]["entity"] for t, r in enumerate(rows) if r["split"] == name.split(":")[0]])  # fmt: skip
            rr = X.resampled_rates({name: v}, ents, a.n_boot)
            res[name] = {"n": len(v), "share": [float(np.mean(v)), *X.interval(rr[name])]}
        out_json[sp] = res
        lines += [f"## Nearest class mean in {sp}", "", "| alt-state subset | n | points at the alt's locker sentence | "
                  "points at the other pick sentence | points at the org's locker sentence |", "|---|---|---|---|---|"]  # fmt: skip
        for key, label in SPLITS:
            lines.append(f"| {label} | {res[f'{key}: other pick sentence']['n']} | "
                         f"{ci(res[f'{key}: alt' + chr(39) + 's locker sentence']['share'])} | "
                         f"{ci(res[f'{key}: other pick sentence']['share'])} | "
                         f"{ci(res[f'{key}: org' + chr(39) + 's locker sentence']['share'])} |")  # fmt: skip
        o = res["org state: org's locker sentence"]
        lines += ["", f"Sanity: the org state's nearest class mean is the org's locker sentence in {ci(o['share'])} of "
                  f"{o['n']} items.", ""]  # fmt: skip
    counts = collections.Counter(r["split"] for r in rows)
    head = [f"# Duplicate-pick pairs, nearest class mean in A and Alf: {a.states}", "",
            f"{NOTE} Class means and subspaces from {a.fresh} (locker-before, n = {len(keep)}; {info['layout_groups']['groups']} "
            f"layout groups); test: {len(rows)} single-change items of {a.single} with both lockers before the pick "
            f"({dict(counts)}; {missing} left out, their layout has no fresh group). Bootstrap over bridge entities "
            f"({a.n_boot} resamples). UNVERIFIED.", ""]  # fmt: skip
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = MM.RESULTS / a.out / f"dup-nearest-{stamp}"
    out.mkdir()
    (out / "dup_nearest.json").write_text(json.dumps({"note": NOTE, "fresh": a.fresh, "single": a.single, "states": a.states,
                                                      "n": len(rows), "missing_layout": missing, "splits": dict(counts),
                                                      "results": out_json}, indent=1) + "\n")  # fmt: skip
    (out / "dup_nearest.md").write_text("\n".join(head + lines) + "\n")
    print("\n".join(head + lines))


if __name__ == "__main__":
    main()
