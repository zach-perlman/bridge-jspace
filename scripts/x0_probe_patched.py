"""x0_probe_patched (Dan's items 2 and 3 of ~18:45, audit item 4; descriptive, added after data): the probe-(b) readout
(which sentence holds the bridge's locker) on the single-change pairs and on patched states.

Probe (b): one-hot ridge on the org states at the bridge's word of d1_topics_v3's locker-before scenes (x0_probe's
states; penalty by entity-held-out CV), cross-fitted: each test item is read by the model of the fold that left its
bridge entity out. Test items: the single-change items whose org and alt bridges both have their locker sentence
before the asked pick (the states saved by x0_amnesic: h_org, Δ, Δ's J++ parts at k = 25 and 100; with --parts, also
x0_parts' word part w and J++-without-the-word part jw).
  Pair test: org state (label: the org bridge's locker sentence) and alt state h_org + Δ (label: the alt bridge's); the
  layout is identical, so a layout-only classifier gets both right in none of the pairs, by construction.
  Patched states: h_org + J(Δ), h_org + (Δ - J(Δ)) at k = 25 and 100 (and h_org + w, h_org + jw): how often the probe
  reads the alt's locker sentence, and how often the org's.
Shares with 95% CIs from a cluster bootstrap over bridge entities (10,000 resamples, seed 0).

uv run python scripts/x0_probe_patched.py --probe x0_probe_27b --single x0_single_27b_r2 --states x0_amnesic_27b
"""

from __future__ import annotations

import argparse
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
from scripts import x0_probe as P
from scripts import x0_strata as ST

NOTE = "Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule."


PICK = re.compile(r"\b([A-Z][a-z]+) picked (?:the )?([\w-]+)\.")


def other_pick(case: dict) -> tuple[str, int]:
    """Where the alt item's original picker's sentence sits relative to the asked person's pick sentence (before /
    after), and its sentence index: in the single-change alt, two people pick the alt item."""
    sents = [s if s.endswith(".") else s + "." for s in case["context"].split(". ")]
    asked = re.search(r"([A-Z][a-z]+)'s pick", case["readers"][X.LOOKUP]["question"]).group(1)  # type: ignore[union-attr]
    picks = [(i, m.group(1), m.group(2)) for i, s in enumerate(sents) if (m := PICK.search(s))]
    mine = next(i for i, who, _ in picks if who == asked)
    other = next(i for i, who, what in picks if who != asked and what == case["cf_bridge"])
    return ("before" if other < mine else "after"), other


def locker_index(context: str, thing: str) -> int:
    """The index of the thing's locker sentence among the context's sentences."""
    sents = context.split(". ")
    return next(i for i, s in enumerate(sents) if s.startswith("The locker of") and re.search(rf"\b{thing}\b", s))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", required=True, help="x0_probe run (d1_topics_v3 states) to train on")
    ap.add_argument("--single", required=True, help="the single-change X0 run (its cases: contexts and alt bridges)")
    ap.add_argument("--states", required=True, help="x0_amnesic run with h_org, Δ and the J++ parts")
    ap.add_argument("--parts", default=None, help="x0_parts run with the w and jw parts (optional)")
    ap.add_argument("--target", choices=("address", "value"), default="address",
                    help="address: probe (b), the locker sentence; value: probe (a), the locker number")  # fmt: skip
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    key = "locker_index" if a.target == "address" else "answer"
    # the probe: locker-before org states of the probe run's set, folds by entity
    src = P.RESULTS / a.probe
    items = X.read_jsonl(src / "items.jsonl")
    keep = [i for i, it in enumerate(items) if it["order"] == "before"]
    h = np.load(src / "states.npz")["h"].astype(np.float64)[keep]
    y = [items[i][key] for i in keep]
    ents = [items[i]["entity"] for i in keep]
    rel = P.select_penalty(h, y, ents)
    fold = P.folds(y, ents, True, P.K_OUTER)
    fold_of = {e: int(f) for e, f in zip(ents, fold, strict=True)}
    # the test items and their states
    z = np.load(pins.RESULTS_DIR / "x0_amnesic" / a.states / "states.npz")
    scenes = [str(s) for s in z["scene"]]
    h_org, delta = z["h_org"].astype(np.float64), z["delta"].astype(np.float64)
    states = {"org": h_org, "alt (org + Δ)": h_org + delta}
    for k in (25, 100):
        j = z[f"jpp_k{k}"].astype(np.float64)
        states[f"org + J++ part, k = {k}"] = h_org + j
        states[f"org + rest, k = {k}"] = h_org + delta - j
    if a.parts:
        zp = np.load(pins.RESULTS_DIR / "x0_parts" / a.parts / "states.npz")
        assert [str(s) for s in zp["scene"]] == scenes, "the parts run's items differ"
        for d, what in (("w", "word part"), ("jw", "J++ without the word")):
            states[f"org + {what}"] = h_org + zp[f"part_{d}"].astype(np.float64)
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / a.single / "cases.jsonl") if c["rendering"] == "chat"}
    test, labels, others = [], [], []
    for i, s in enumerate(scenes):
        c = cases[s]
        f = ST.features(c)
        if f["org locker vs asked pick"] == "before" and f["alt locker vs asked pick"] == "before":
            test.append(i)
            if a.target == "address":
                org, alt = locker_index(c["context"], c["bridge"]), locker_index(c["context"], c["cf_bridge"])
            else:  # the locker numbers: the lookup's org and alt answers
                org, alt = c["readers"][X.LOOKUP]["answer"], c["readers"][X.LOOKUP]["cf_answer"]
            labels.append((org, alt, c["bridge"]))
            others.append(other_pick(c))
    # cross-fitted predictions: the fold model that left the item's entity out
    pred = {name: [None] * len(test) for name in states}
    for f in range(P.K_OUTER):
        mine = [t for t, (_, _, e) in enumerate(labels) if fold_of.get(e, 0) == f]
        if not mine:
            continue
        tr = np.flatnonzero(fold != f)
        for name, st in states.items():
            out = P.ridge(h[tr], [y[i] for i in tr], st[[test[t] for t in mine]], (rel,))[0]
            for t, p in zip(mine, out, strict=True):
                pred[name][t] = p
    org_lab, alt_lab, ent = [lb[0] for lb in labels], [lb[1] for lb in labels], [lb[2] for lb in labels]
    hits = {"org right": [int(p == o) for p, o in zip(pred["org"], org_lab, strict=True)],
            "alt right": [int(p == al) for p, al in zip(pred["alt (org + Δ)"], alt_lab, strict=True)]}  # fmt: skip
    hits["pair right"] = [a_ * b_ for a_, b_ in zip(hits["org right"], hits["alt right"], strict=True)]
    hits["same prediction"] = [int(p == q) for p, q in zip(pred["org"], pred["alt (org + Δ)"], strict=True)]
    for name in states:
        if name in ("org",):
            continue
        hits[f"{name}: reads the alt's"] = [int(p == al) for p, al in zip(pred[name], alt_lab, strict=True)]
        hits[f"{name}: reads the org's"] = [int(p == o) for p, o in zip(pred[name], org_lab, strict=True)]
    r = X.resampled_rates(hits, ent, a.n_boot)
    res = {k: [float(np.mean(v)), *X.interval(r[k])] for k, v in hits.items()}
    # the duplicate pick: alt right by the other picker's side, and readouts pointing at the other pick sentence
    split = {}
    for side in ("before", "after"):
        k = [t for t, (sd, _) in enumerate(others) if sd == side]
        if not k:
            continue
        sub = {"alt right": [hits["alt right"][t] for t in k], "pair right": [hits["pair right"][t] for t in k],
               "alt state reads the other pick sentence": [int(pred["alt (org + Δ)"][t] == others[t][1]) for t in k]}  # fmt: skip
        rs = X.resampled_rates(sub, [ent[t] for t in k], a.n_boot)
        split[side] = {"n": len(k), **{m: [float(np.mean(v)), *X.interval(rs[m])] for m, v in sub.items()}}
    if a.target == "address":  # among 'before': which earlier mention of the alt item is the most recent one
        for name, keep in (("before, the other pick is the latest earlier mention", lambda t: others[t][1] > alt_lab[t]),
                           ("before, the alt locker is the latest earlier mention", lambda t: others[t][1] < alt_lab[t])):  # fmt: skip
            k = [t for t, (sd, _) in enumerate(others) if sd == "before" and keep(t)]
            if not k:
                continue
            sub = {"alt right": [hits["alt right"][t] for t in k], "pair right": [hits["pair right"][t] for t in k],
                   "alt state reads the other pick sentence": [int(pred["alt (org + Δ)"][t] == others[t][1]) for t in k]}  # fmt: skip
            rs = X.resampled_rates(sub, [ent[t] for t in k], a.n_boot)
            split[name] = {"n": len(k), **{m: [float(np.mean(v)), *X.interval(rs[m])] for m, v in sub.items()}}
    res["duplicate_pick_split"] = split
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    what = "(b), the locker sentence" if a.target == "address" else "(a), the locker number"
    lines = [f"# Probe {what}, on single-change pairs and patched states: {a.states}", "",
             f"{NOTE} Probe trained on {a.probe} (locker-before, n = {len(y)}, penalty {rel}), cross-fitted by entity; "
             f"test: the {len(test)} single-change items of {a.single} with both lockers before the pick. Bootstrap over "
             f"bridge entities ({a.n_boot} resamples). UNVERIFIED.", "",
             "## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)", "",
             "| measure | share |", "|---|---|"]  # fmt: skip
    lines += [f"| {k} | {ci(res[k])} |" for k in ("org right", "alt right", "pair right", "same prediction")]
    lines += ["", "## The duplicate pick: by where the alt item's other picker's sentence sits (Dan ~20:45)", "",
              "In the alt, two people pick the alt item. If the alt state's address pointed to the previous occurrence of "
              "the same word, alt right would be high when the other pick comes after the asked pick and low when it "
              "comes before.", "", "| other pick vs asked pick | n | alt right | pair right | alt state reads the other "
              "pick sentence |", "|---|---|---|---|---|"]  # fmt: skip
    for side, d in split.items():
        lines.append(f"| {side} | {d['n']} | {ci(d['alt right'])} | {ci(d['pair right'])} | "
                     f"{ci(d['alt state reads the other pick sentence'])} |")  # fmt: skip
    lines += ["", f"## Patched states: which {'locker sentence' if a.target == 'address' else 'locker number'} the probe reads", "",
              "| state | reads the alt's | reads the org's |", "|---|---|---|"]  # fmt: skip
    for name in states:
        if name != "org":
            lines.append(f"| {name} | {ci(res[f'{name}: reads the alt' + chr(39) + 's'])} | "
                         f"{ci(res[f'{name}: reads the org' + chr(39) + 's'])} |")  # fmt: skip
    # the norm confound: each part's share of ||Δ||² against its share of Δ's energy in the probe's own subspace (a random
    # part of the same size would carry about its overall share there too)
    q = P.subspace(h, y, rel)  # [d, classes - 1], the probe's decision directions
    energy = {}
    for name, st in states.items():
        if name.startswith("org + "):
            v = (st - h_org)[test]
            dv = delta[test]
            energy[name] = {
                "share_of_delta": float(np.median((v**2).sum(1) / (dv**2).sum(1))),
                "share_in_probe_subspace": float(np.median(((v @ q) ** 2).sum(1) / ((dv @ q) ** 2).sum(1))),
            }
    lines += ["", "## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)", "",
              "| part | share of ||Δ||² | share of Δ's probe-subspace energy |", "|---|---|---|"]  # fmt: skip
    lines += [
        f"| {n[len('org + ') :]} | {e['share_of_delta']:.3f} | {e['share_in_probe_subspace']:.3f} |"
        for n, e in energy.items()
    ]
    res["energy"] = energy
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = (
        pins.RESULTS_DIR / "x0_amnesic" / a.states / f"probe-patched-{'' if a.target == 'address' else 'value-'}{stamp}"
    )
    out.mkdir()
    (out / "probe_patched.json").write_text(json.dumps({"note": NOTE, "target": a.target, "probe": a.probe, "single": a.single, "states": a.states,
                                                        "parts": a.parts, "n": len(test), "penalty": rel, "results": res},
                                                       indent=1) + "\n")  # fmt: skip
    (out / "probe_patched.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
