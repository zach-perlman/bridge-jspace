"""overlap agent (post hoc, exploratory; CPU): note 38 (v3 swaps: insert the donor's top-10 J++ part at the description's
last token) split by the swap edit's overlap with the asked relation's answer span: share_rel = ||P_Arel e||^2 / ||e||^2
(logged by nn_swap.py on every note 38 row of an item; e = Jk(h_D) - Jk(h_X)). Median split per word (RM, PM) over the
items kept unedited (ties to low). The reader's own table() (nn_swap38_read: transfer = donor - third, beyond insert_k10_rot,
share of insert_k10's beyond; paired bridge bootstrap, 1000 draws, random.Random(0)) on each half.
"""

import collections
import json
import statistics as st
import sys

ROOT = "/workspace/bridge-jspace"
sys.path[:0] = [ROOT, ROOT + "/scripts"]
from scripts import nn_swap38_read as N  # noqa: E402

out = {}
for P, band in (("qwen35_9b_", "L12-16"), ("", "L32-40"), ("nem35l_", "L27-33")):
    rows = N.load(f"{P}nn38_{band}_v1")
    share = {}
    for r in rows:
        if r.get("share_rel") is not None:
            share.setdefault(r["id"], r["share_rel"])
    kept_ok = {r["id"] for r in rows if r["condition"] == "none" and r["cls"] == "kept"}
    rec = {}
    for word in N.WORDS:
        ids = sorted({r["id"] for r in rows if r["family"] == word and r["id"] in kept_ok and r["id"] in share})
        vals = [share[i] for i in ids]
        if not vals:
            continue
        cut = st.median(vals)
        halves = {"all": set(ids), "low": {i for i in ids if share[i] <= cut}, "high": {i for i in ids if share[i] > cut}}
        rw = {"cut": round(cut, 4), "share_rel_range": [round(min(vals), 3), round(max(vals), 3)]}
        for h, s in halves.items():
            cells = N.Cells([r for r in rows if r["id"] in s])
            tab = N.table(cells, band, word, N.INSERT, N.SWAP, N.ROT)
            rels = collections.Counter(r["rel"] for r in rows if r["id"] in s and r["condition"] == "none" and r["family"] == word)
            rw[h] = {"n": len(s), "relations": dict(rels), "readings": N.readings(tab),
                     "table": {c: {k: v for k, v in tab[c].items()} for c in (N.SWAP, N.ROT, N.REL, N.NM, N.OFF, N.RELANS) if c in tab}}
        # relation split (beside)
        for rel in sorted({r["rel"] for r in rows if r["id"] in halves["all"]}):
            s = halves["all"] & {r["id"] for r in rows if r["rel"] == rel}
            cells = N.Cells([r for r in rows if r["id"] in s])
            tab = N.table(cells, band, word, N.INSERT, N.SWAP, N.ROT)
            rw[f"rel:{rel}"] = {"n": len(s), "readings": N.readings(tab),
                                "median_share_rel": round(st.median(share[i] for i in s), 3) if s else None}
        rec[word] = rw
    out[P or "27b_"] = rec
    for word, rw in rec.items():
        print(f"== {P or '27b_'} {word} cut share_rel {rw['cut']} range {rw['share_rel_range']}")
        for h in ("all", "low", "high"):
            t, rd = rw[h]["table"], rw[h]["readings"]
            sw = t.get(N.SWAP, {})
            print(f"  {h:4s} n {rw[h]['n']:3d} swap transfer {sw.get('transfer')} beyond rot {sw.get('beyond')} {sw.get('beyond_ci')} | "
                  f"share noansrel {t.get(N.REL, {}).get('share')} {t.get(N.REL, {}).get('share_ci')} | nm {t.get(N.NM, {}).get('share')} {t.get(N.NM, {}).get('share_ci')} | "
                  f"off {t.get(N.OFF, {}).get('share')} | relans {t.get(N.RELANS, {}).get('share')} {t.get(N.RELANS, {}).get('share_ci')} | {rd.get('B1')}; {rd.get('B3')}")
        for k, v in rw.items():
            if k.startswith("rel:"):
                rd = v["readings"]
                print(f"  {k:16s} n {v['n']:3d} med share_rel {v['median_share_rel']} swap beyond {rd.get('swap_beyond_rot')} nm {rd.get('share_nm')} rel {rd.get('share_rel')} relans {rd.get('share_relans')}")
json.dump(out, open("/tmp/ana_n38.json", "w"), indent=1)
