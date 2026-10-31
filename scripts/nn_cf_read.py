"""nn_cf_read (Zach, 2026-10-28, prereg amendment 58 note 14): the counterfactual-patching map on jsuite_v4, read (CPU).

Rows from nn_swap runs on v4 (--items v4ok, conditions *_cf: the counterfactual prompt, same passage, the question about
another scene entity D), pooled over the runs given (donor seeds); per site (the run's --site), word (MP lookup / MM
recall twin) and layer window. Classes: donor = D's answer (MP: D's passage value; MM: D's remembered attribute).
Primary rows: pairs whose counterfactual prompt the model answers with D's answer (cf_ok); all pairs beside.
Readings (fixed in note 14):
  the bridge lives here    full_cf moves >= 20% to D's answer, lensrand_cf < 10%, and full - lensrand (paired, 95%
                           bootstrap over bridges) above 0
  the lens part carries it at such a cell: lens >= 2/3 of full and remfix <= 1/3 of full (lensrand < 10): "through";
                           rem >= 2/3 of full: "around"; else "mixed" (each a share moved to D's answer)
Writes results/nn_swap/nn_cf_read/NAME.json, with the cells that meet the first reading (stage 2's targets).

python scripts/nn_cf_read.py NAME RUN [RUN ...] [--all-pairs]
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "nn_swap"


def boot(by: dict[str, list[float]]) -> list[float]:
    rng, keys, out = random.Random(0), sorted(by), []
    for _ in range(1000):
        xs = [x for k in (rng.choice(keys) for _ in keys) for x in by[k]]
        out.append(sum(xs) / len(xs))
    out.sort()
    return [round(out[25], 1), round(out[974], 1)]


def boot_stat(by: dict[str, list[dict]], fn) -> list:
    """Note 15-16: fn over pooled pair dicts, and its 95% cluster bootstrap over bridges (1000, seed 0)."""
    rng, keys, out = random.Random(0), sorted(by), []
    for _ in range(1000):
        v = fn([d for k in (rng.choice(keys) for _ in keys) for d in by[k]])
        if v is not None:
            out.append(v)
    out.sort()
    pt = fn([d for k in keys for d in by[k]])
    return [None if pt is None else round(pt, 3), [round(out[int(0.025 * len(out))], 3), round(out[int(0.975 * len(out)) - 1], 3)] if out else None]


def share_of(ds: list[dict], c: str) -> float:
    return sum(d.get(c) == "donor" for d in ds) / max(1, sum(c in d for d in ds))


def note15(by: dict[str, list[dict]], ranks: list, A: str) -> dict:
    """Note 15, Dan's 51.12 rule: e1 = (remrand - rem) / full, e2 = (remrand - remkeepA) / full, e3 = (noaActl - noaA) /
    full (donor shares); bridge if e2 >= 0.7 e1 and e3 <= 0.10; answer if e2 <= 0.3 e1 and e3 >= 0.5 e1; else mixed;
    e1 <= 0: can't tell. Readout check first: the answer not read at the site if it ranks > 50 for X and D on >= 90%."""
    def e(arm: str, twin: str):
        def f(ds):
            full = share_of(ds, "full_cf")
            return None if full <= 0 else (share_of(ds, twin) - share_of(ds, arm)) / full
        return f

    e1, e2, e3 = boot_stat(by, e("rem_cf", "remrand_cf")), boot_stat(by, e(f"remkeep{A}_cf", "remrand_cf")), boot_stat(by, e(f"noa{A}_cf", f"noa{A}ctl_cf"))
    ok =[r for r in ranks if r[0] is not None and r[1] is not None]
    not_read = sum(a > 50 and d > 50 for a, d in ok) / max(1, len(ok))
    p1, p2, p3 = e1[0], e2[0], e3[0]
    if p1 is None or p1 <= 0:
        arms = "can't tell (arm 1 has no extra loss beyond random)"
    elif p2 >= 0.7 * p1 and p3 <= 0.10:
        arms = "the lens part is the bridge"
    elif p2 <= 0.3 * p1 and p3 >= 0.5 * p1:
        arms = "the lens part is the answer"
    else:
        arms = "mixed"
    return {"e1": e1, "e2": e2, "e3": e3, "e2_over_e1": None if not p1 or p1 <= 0 else round(p2 / p1, 3),
            "e3_over_e1": None if not p1 or p1 <= 0 else round(p3 / p1, 3), "answer_not_read_share": round(not_read, 3), "n_ranked": len(ok),
            "arms": arms, "verdict": f"the answer is not read at the site ({100 * not_read:.0f}% of pairs; arms beside: {arms})" if not_read >= 0.9 else arms}  # fmt: skip


def note16(by: dict[str, list[dict]], shares: list[float]) -> dict:
    """Note 16: in Dan's lens part if jpp - jpprand >= 0.5 full and nojpprand - nojpp >= 1/3 full; outside it if
    jpp - jpprand < 1/3 full and nojpprand - nojpp < 1/3 full; else mixed (donor shares, points)."""
    ds = [d for v in by.values() for d in v]
    full = 100 * share_of(ds, "full_cf")
    alone = 100 * (share_of(ds, "jpp_cf") - share_of(ds, "jpprand_cf"))
    need = 100 * (share_of(ds, "nojpprand_cf") - share_of(ds, "nojpp_cf"))
    verdict = ("not read (full < 20)" if full < 20 else "in Dan's lens part" if alone >= 0.5 * full and need >= full / 3
               else "outside it" if alone < full / 3 and need < full / 3 else "mixed")  # fmt: skip
    return {"full": round(full, 1), "jpp_minus_rand": round(alone, 1), "removal_minus_rand": round(need, 1),
            "jpp_alone_ci": boot_stat(by, lambda x: 100 * (share_of(x, "jpp_cf") - share_of(x, "jpprand_cf"))),
            "removal_ci": boot_stat(by, lambda x: 100 * (share_of(x, "nojpprand_cf") - share_of(x, "nojpp_cf"))),
            "positive_check_pass": alone >= 0.5 * full, "jshare_mean": round(sum(shares) / len(shares), 3) if shares else None, "verdict": verdict}  # fmt: skip


def main(name: str, runs: list[str], all_pairs: bool) -> None:
    cell = collections.defaultdict(lambda: collections.defaultdict(dict))  # (site, word, band) -> key -> cond -> cls
    bridge = {}
    ranks = collections.defaultdict(dict)  # note 15: (site, word, band) -> key -> (rank_ax, rank_ad)
    jsh = collections.defaultdict(list)  # note 16: (site, word, band) -> ||J||^2 / ||Δ||^2 per pair
    for ri, run in enumerate(runs):
        site = json.loads((RES / run / "manifest.json").read_text())["site"]
        for line in (RES / run / "rows.jsonl").read_text().splitlines():
            r = json.loads(line)
            if not all_pairs and r.get("cf_ok") is False:
                continue
            key = f"{ri}:{r['id']}"
            cell[(site, r["family"], r["band"])][key][r["condition"]] = r["cls"]
            bridge[key] = f"{r['rel']}:{r['x']}"
            if r["condition"] == "none" and "rank_ax" in r:
                ranks[(site, r["family"], r["band"])][key] = (r["rank_ax"], r["rank_ad"])
            if "jshare" in r:
                jsh[(site, r["family"], r["band"])].append(r["jshare"])
    out: dict = {"runs": runs, "pairs": "all" if all_pairs else "cf_ok", "cells": {}, "hits": []}
    for (site, word, band), by in sorted(cell.items(), key=lambda kv: (kv[0][0], kv[0][1], int(kv[0][2][1:].split("-")[0]))):
        conds = sorted({c for d in by.values() for c in d})
        share = {c: round(100 * sum(d.get(c) == "donor" for d in by.values() if c in d) / max(1, sum(c in d for d in by.values())), 1) for c in conds}
        kept = {c: round(100 * sum(d.get(c) == "kept" for d in by.values() if c in d) / max(1, sum(c in d for d in by.values())), 1) for c in conds}
        third = {c: round(100 * sum(d.get(c) == "third" for d in by.values() if c in d) / max(1, sum(c in d for d in by.values())), 1) for c in conds}
        rec: dict = {"n": len(by), "donor": share, "kept": kept, "third": third}
        if "full_cf" in conds and "lensrand_cf" in conds:
            b = collections.defaultdict(list)
            for k, d in by.items():
                if "full_cf" in d and "lensrand_cf" in d:
                    b[bridge[k]].append(100.0 * ((d["full_cf"] == "donor") - (d["lensrand_cf"] == "donor")))
            ci = boot(b)
            rec["full_minus_rand_ci"] = ci
            rec["bridge_lives_here"] = share["full_cf"] >= 20 and share["lensrand_cf"] < 10 and ci[0] > 0
            if rec["bridge_lives_here"]:
                out["hits"].append({"site": site, "word": word, "band": band})
        if all(f"{k}_cf" in share for k in ("full", "lens", "rem", "remfix", "lensrand")):
            t = {k: share[f"{k}_cf"] - share.get("none", 0.0) for k in ("full", "lens", "rem", "remfix", "lensrand")}
            full = t["full"]
            rec["decomposition"] = {**{k: round(v, 1) for k, v in t.items()},
                                    "verdict": "not read" if full < 20 else "through" if t["lens"] >= 2 / 3 * full and t["remfix"] <= 1 / 3 * full and t["lensrand"] < 10
                                    else "around" if t["rem"] >= 2 / 3 * full else "mixed"}  # fmt: skip
        bb = collections.defaultdict(list)  # notes 15-16: pairs clustered by bridge
        for k, d in by.items():
            bb[bridge[k]].append(d)
        for A in ("own", "rel", "oth"):
            if all(c in conds for c in ("full_cf", "rem_cf", "remrand_cf", f"remkeep{A}_cf", f"noa{A}_cf", f"noa{A}ctl_cf")):
                rec[f"note15_{A}"] = note15(bb, list(ranks[(site, word, band)].values()), A)
        if "note15_own" in rec and "note15_oth" in rec:  # note 15 addendum 2: this answer, or answer-ness?
            def e3(A: str):
                return lambda ds: None if share_of(ds, "full_cf") <= 0 else (share_of(ds, f"noa{A}ctl_cf") - share_of(ds, f"noa{A}_cf")) / share_of(ds, "full_cf")

            diff = boot_stat(bb, lambda ds: None if e3("own")(ds) is None else e3("own")(ds) - e3("oth")(ds))
            po, pt = rec["note15_own"]["e3"][0], rec["note15_oth"]["e3"][0]
            rec["note15_spec"] = {"e3_own_minus_oth": diff,
                                  "verdict": "can't tell" if po is None or pt is None or po <= 0 else "this item's answer" if diff[0] >= 0.2 and diff[1][0] > 0 and pt <= 0.5 * po
                                  else "answer-ness (any answer of the relation)" if pt >= 0.7 * po else "partly specific"}  # fmt: skip
        if all(c in conds for c in ("full_cf", "lens_cf", "rem_cf", "lensshr_cf", "remshr_cf")):  # note 15 addendum
            def frac(arm: str, twin: str):
                return lambda ds: None if share_of(ds, "full_cf") <= 0 else (share_of(ds, twin) - share_of(ds, arm)) / share_of(ds, "full_cf")

            need, alone = boot_stat(bb, frac("rem_cf", "remshr_cf")), boot_stat(bb, frac("lensshr_cf", "lens_cf"))
            p = need[0]
            rec["note15a"] = {"need_beyond_same_share": need, "alone_beyond_same_share": alone,
                              "verdict": "can't tell" if p is None else "needed beyond a same-share random part" if p >= 0.30 and need[1][0] > 0
                              else "not needed beyond it" if p < 0.10 else "weak"}  # fmt: skip
        if all(c in conds for c in ("full_cf", "lensnp_cf", "remnp_cf", "lensshrnp_cf", "remshrnp_cf")):  # note 21 addendum: no skip rule
            def frac2(arm: str, twin: str):
                return lambda ds: None if share_of(ds, "full_cf") <= 0 else (share_of(ds, twin) - share_of(ds, arm)) / share_of(ds, "full_cf")

            need, alone = boot_stat(bb, frac2("remnp_cf", "remshrnp_cf")), boot_stat(bb, frac2("lensshrnp_cf", "lensnp_cf"))
            rec["note21np"] = {"need_beyond_same_share": need, "alone_beyond_same_share": alone,
                               "verdict": "can't tell" if need[0] is None else "needed" if need[0] >= 1 / 3 else "not needed"}  # fmt: skip
        if all(c in conds for c in ("full_cf", "jpp_cf", "jpprand_cf", "nojpp_cf", "nojpprand_cf")):
            rec["note16"] = note16(bb, jsh[(site, word, band)])
        out["cells"][f"{site}/{word}/{band}"] = rec
        line = f"{site:5s} {word} {band:7s} n {len(by):4d}  " + "  ".join(f"{c} {share[c]:5.1f}" for c in conds if c != "none")
        if "bridge_lives_here" in rec:
            line += f"  full-rand CI {rec['full_minus_rand_ci']}  {'<-- LIVES HERE' if rec['bridge_lives_here'] else ''}"
        if "decomposition" in rec:
            line += f"  decomposition {rec['decomposition']}"
        for k in ("note15_own", "note15_rel", "note15_oth", "note15_spec", "note15a", "note16", "note21np"):
            if k in rec:
                line += f"\n    {k}: {json.dumps(rec[k])}"
        print(line)
    d = RES / "nn_cf_read"
    d.mkdir(exist_ok=True)
    (d / f"{name}.json").write_text(json.dumps(out, indent=1) + "\n")
    print("hits", json.dumps(out["hits"]))


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if x != "--all-pairs"]
    main(args[0], args[1:], "--all-pairs" in sys.argv)
