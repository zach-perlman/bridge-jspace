"""nn_priming_read (Zach, 2026-10-29, prereg amendment 58 note 25): at the bridge, does the J-space show what the model
will say, or the person's remembered attribute whatever is asked? Reads an nn_readout --items v4 --priming run.

v4's lookup (MP) and its recall twin (MM) share the passage and the description; only the question's frame differs.
On MP the model says X's made-up passage value, not X's remembered attribute. Per prompt and target: the share of the
window's layers where the target is the top answer. Primary set: scenes whose MP and MM are both v4ok (paired).
  rho = (MP other - MP third) / (MM attr - MM third) at the description's end, J++ lens
  (MP other: X's remembered attribute on the lookup; MM attr: the same word on the recall twin; third: an absent answer)
Readings: void unless MM attr - MM third >= 10 points with its interval above 0; "the person's attribute, whatever will
be said" if rho >= 0.7; "what will be said" if rho <= 0.3; mixed between; unclear if rho's interval holds 0.3 and 0.7.
Final token: "the end shows what will be said" if MP attr (the passage value) - MP other >= 20 points.
Cluster bootstrap over bridges, 2000 draws.

python scripts/nn_priming_read.py PREFIX [RUN [OUT]]   (PREFIX "qwen35_9b_", "" for the 27B, "nem35l_", "muse30_"; OUT names the
       output {PREFIX}{OUT}_n25.json, default v4; amendment 59 notes 27-28)
Windows: WIN below; for a model not in WIN (Muse, note 28), the rule that gives them: the min-max of the bands that are stage 1
hits for both MP and MM, at site last (the description's end) and at site final ({PREFIX}v4_stage1.json).
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "nn_readout"
# stage 1's hits for both words (note 14): the description's end, then the final token
WIN = {"qwen35_9b_": ((4, 16), (21, 30)), "": ((16, 40), (49, 62)), "nem35l_": ((6, 26), (34, 50)), "dsv4f_": ((6, 23), (30, 40))}  # DeepSeek: amendment 62, by relative depth (no stage 1 map)
WHAT = ("attr", "other", "third", "ctx", "bridge")


def windows(P: str) -> dict:
    if P in WIN:
        return dict(zip(("desc_end", "final"), WIN[P]))
    d = json.loads((ROOT / "results" / "nn_swap" / "nn_cf_read" / f"{P}v4_stage1.json").read_text())
    out = {}
    for site, key in (("last", "desc_end"), ("final", "final")):
        both = set.intersection(*({h["band"] for h in d["hits"] if h["site"] == site and h["word"] == w} for w in ("MP", "MM")))
        assert both, f"no band is a stage 1 hit for both words at site {site}"
        out[key] = (min(int(b[1:].split("-")[0]) for b in both), max(int(b.split("-")[1]) for b in both))
    return out


def main(P: str, run_name: str | None = None, out_name: str = "v4") -> None:
    run = RES / (run_name or f"{P}nn_readout_v4prime_v1")
    win = windows(P)
    hits = collections.defaultdict(list)
    fam, bridge = {}, {}
    for line in (run / "rows.jsonl").open():
        r = json.loads(line)
        lo, hi = win[r["site"]]
        if lo <= r["layer"] <= hi:
            hits[(r["site"], r["lens"], r["id"], r["what"])].append(r["rank"] == 1)
        fam[r["id"]], bridge[r["id"]] = r["family"], r["bridge"]
    val = {k: sum(v) / len(v) for k, v in hits.items()}

    def uid(i: str) -> str:  # j3:chat:v4:MP-w0-00000 -> w0-00000
        return i.split(":")[-1].split("-", 1)[1]

    mp = {uid(i): i for i, f in fam.items() if f == "MP_ok"}
    mm = {uid(i): i for i, f in fam.items() if f == "MM_ok"}
    sets = {"paired": [(bridge[mp[u]], mp[u], mm[u]) for u in sorted(set(mp) & set(mm))],
            "all_ok": [(bridge[i], i, None) for i in mp.values()] + [(bridge[i], None, i) for i in mm.values()]}  # fmt: skip

    def rates(site, lens, units):
        out = {}
        for w, col in (("MP", 1), ("MM", 2)):
            ids = [u[col] for u in units if u[col]]
            for t in WHAT:
                xs = [val[(site, lens, i, t)] for i in ids if (site, lens, i, t) in val]
                out[f"{w}/{t}"] = 100 * sum(xs) / len(xs) if xs else float("nan")
        return out

    stats = {"MM_attr_minus_third": lambda r: r["MM/attr"] - r["MM/third"],
             "MP_other_minus_third": lambda r: r["MP/other"] - r["MP/third"],
             "MP_said_minus_other": lambda r: r["MP/attr"] - r["MP/other"],
             "rho": lambda r: (r["MP/other"] - r["MP/third"]) / (r["MM/attr"] - r["MM/third"]) if r["MM/attr"] - r["MM/third"] > 0 else float("nan")}  # fmt: skip

    def boot(site, lens, units, seed=0):
        by = collections.defaultdict(list)
        for u in units:
            by[u[0]].append(u)
        keys, rng, draws = sorted(by), random.Random(seed), collections.defaultdict(list)
        for _ in range(2000):
            r = rates(site, lens, [u for k in (rng.choice(keys) for _ in keys) for u in by[k]])
            for name, fn in stats.items():
                v = fn(r)
                if v == v:
                    draws[name].append(v)
        return {k: [round(sorted(v)[int(0.025 * len(v))], 3), round(sorted(v)[int(0.975 * len(v)) - 1], 3)] for k, v in draws.items()}

    out = {"prefix": P, "run": run.name, "windows": win, "n_paired": len(sets["paired"]), "n_MP_ok": len(mp), "n_MM_ok": len(mm), "cells": {}}
    for label, units in sets.items():
        for site in ("desc_end", "final"):
            for lens in ("jlens", "logit"):
                r = rates(site, lens, units)
                rec = {k: round(v, 1) for k, v in r.items()}
                rec.update({k: round(fn(r), 3) for k, fn in stats.items()})
                rec["ci"] = boot(site, lens, units)
                out["cells"][f"{label}/{site}/{lens}"] = rec
    pr, fi = out["cells"]["paired/desc_end/jlens"], out["cells"]["paired/final/jlens"]
    rho, lo_hi = pr["rho"], pr["ci"].get("rho", [float("nan")] * 2)
    if not (pr["MM_attr_minus_third"] >= 10 and pr["ci"]["MM_attr_minus_third"][0] > 0):
        v = "void (positive check fails)"
    elif lo_hi[0] <= 0.3 and lo_hi[1] >= 0.7:
        v = "unclear"
    elif rho >= 0.7:
        v = "the person's attribute, whatever will be said"
    elif rho <= 0.3:
        v = "what will be said"
    else:
        v = "mixed"
    out["reading"] = {"bridge": v, "rho": rho, "rho_ci": lo_hi,
                      "end_shows_what_will_be_said": fi["MP_said_minus_other"] >= 20, "end_said_minus_other": fi["MP_said_minus_other"]}  # fmt: skip
    d = RES / "nn_priming_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{P}{out_name}_n25.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"n paired {out['n_paired']}, MP ok {len(mp)}, MM ok {len(mm)}; windows {win}")
    for k, rec in out["cells"].items():
        print(k, {t: rec[t] for t in ("MP/attr", "MP/other", "MP/third", "MP/ctx", "MM/attr", "MM/other", "MM/third")}, "rho", rec["rho"], rec["ci"].get("rho"))
    print(json.dumps(out["reading"]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "", sys.argv[2] if len(sys.argv) > 2 else None, sys.argv[3] if len(sys.argv) > 3 else "v4")
