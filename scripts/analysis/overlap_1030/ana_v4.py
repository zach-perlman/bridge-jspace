"""overlap agent (post hoc, exploratory; CPU): v4 knock-out results split by bridge-answer overlap and by relation.

Overlap per bridge (from /tmp/ov_v4_<target>.json, ov_v4.py): the bridge's concept-token J++ vector's energy share inside
keepA's span A at the band's middle layer, minus the mean share of 20 random same-size letter spans ("excess").
Readers reused unchanged (scripts/nn_ko37_read, nn_ko41_read, nn_ko49_read, nn_ko57_read): bridge bootstrap, 2000 draws,
random.Random(0). Subsets restrict the rows to items whose bridge is in the subset.
python ana_v4.py  -> /tmp/ana_v4.json
"""

import collections
import json
import statistics as st
import sys

ROOT = "/workspace/bridge-jspace"
sys.path[:0] = [ROOT, ROOT + "/scripts"]
from scripts import nn_ko37_read as K  # noqa: E402
from scripts.nn_ko41_read import gap_ratio  # noqa: E402
from scripts.nn_ko49_read import ratio_of, rows_at  # noqa: E402
from scripts.nn_ko57_read import contrast  # noqa: E402
from pathlib import Path  # noqa: E402

RES = Path(ROOT) / "results" / "ablate_v2"
MODELS = {"qwen35_9b_": "qwen3.5-9b", "": "qwen3.6-27b", "nem35l_": "nemotron-3.5-lightning"}
SET = "jsuite_v4_test_chat"
items = {json.loads(l)["id"]: json.loads(l) for l in open(f"{ROOT}/data/tasks_v2/{SET}/items.jsonl")}
COUNTRY = {"cities", "companies", "landmarks"}


def sub(acc, ids):
    return collections.defaultdict(dict, {k: {i: v for i, v in d.items() if i in ids} for k, d in acc.items()})


def metrics(a37, a49, a57, ids):
    s37, s49, s57 = sub(a37, ids), sub(a49, ids), sub(a57, ids) if a57 else None
    out = {}
    m = K.measures(s37, items, lambda it: True)
    cs = m.get("conditions", {})
    out["n_MM"], out["n_MP"] = m["n"].get("MM"), m["n"].get("MP")
    out["n_bridges"] = len({items[i]["bridge"] for i in s37[("MM", "none")]})
    for c in ("paper10", "paper10_rot", "paper10_keepA", "ansJ"):
        if c in cs:
            out[f"gap_{c}"] = cs[c]["gap"]
            out[f"gap_{c}_ci"] = cs[c]["gap_ci"]
            out[f"lossMM_{c}"] = cs[c]["loss_MM"]
            out[f"lossMP_{c}"] = cs[c]["loss_MP"]
    if "ratio" in m:
        r = m["ratio"]
        out["keepA_rescue"] = None if r["ratio"] is None else round(1 - r["ratio"], 3)
        out["keepA_rescue_ci"] = None if not r["ratio_ci"] else [round(1 - r["ratio_ci"][1], 3), round(1 - r["ratio_ci"][0], 3)]
        out["paper10_net_MM"] = r["paper10_net_MM"]
    oa = ratio_of(s49, items, "paper10_onlyA", "paper10_onlyA_rot")
    if oa:
        out["onlyA_net_share"], out["onlyA_net_share_ci"] = oa["ratio"], oa["ratio_ci"]
        g = gap_ratio(s49, s49, items, "paper10_onlyA", "paper10")
        out["onlyA_gap_share"], out["onlyA_gap_share_ci"] = g["ratio"], g["ratio_ci"]
    if s57 is not None and ("MM", "paper10_onlyRperp") in s57:
        c = contrast(s57, items, ("paper10_onlyA", "paper10_onlyA_rot"), ("paper10_onlyRperp", "paper10_onlyRperp_rot"), ("paper10", "paper10_rot"))
        out["S1_onlyA_minus_onlyRperp"], out["S1_ci"] = c.get("value"), c.get("ci")
        rp = ratio_of(s57, items, "paper10_onlyRperp", "paper10_onlyRperp_rot")
        out["onlyRperp_net_share"], out["onlyRperp_net_share_ci"] = rp.get("ratio"), rp.get("ratio_ci")
        for k in (30, 100):
            d = contrast(s57, items, (f"top{k}_keepRE", f"top{k}_keepRE_rot"), (f"top{k}_keepA", f"top{k}_keepA_rot"), (f"top{k}", f"top{k}_rot"))
            out[f"D1_K{k}"], out[f"D1_K{k}_ci"] = d.get("value"), d.get("ci")
    return out


report = {}
for P, target in MODELS.items():
    ov = json.load(open(f"/tmp/ov_v4_{target}.json"))
    mid = str(ov["mid"])
    res = ov["sets"][SET]
    exc, exc_own, raw = {}, {}, {}
    for key, v in res.items():
        if "skipped" in v:
            continue
        p = v["per_layer"][mid]
        exc[key] = p["A"] - st.mean(p["rand"])
        raw[key] = p["A"]
        if "own" in p:
            exc_own[key] = p["own"] - st.mean(p["rand_own"])
        # band-mean as sensitivity
    exc_band = {}
    for key, v in res.items():
        if "skipped" in v:
            continue
        exc_band[key] = st.mean(v["per_layer"][la]["A"] - st.mean(v["per_layer"][la]["rand"]) for la in v["per_layer"])
    a37 = rows_at(RES / f"{P}{SET}_ko37_cand2_v1")
    a49 = rows_at(RES / f"{P}{SET}_ko49_cand2_v1")
    p57 = RES / f"{P}{SET}_ko57_cand2_v1"
    a57 = rows_at(p57) if (p57 / "rows.jsonl").exists() else None
    key_of = lambda i: f"{items[i]['relation']}|{items[i]['bridge']}"  # noqa: E731
    gated = set(a37[("MM", "none")]) | set(a37[("MP", "none")])
    gated_br = sorted({key_of(i) for i in a37[("MM", "none")]})
    R = {"mid_layer": int(mid), "n_bridges_gated": len(gated_br), "n_bridges_with_overlap": sum(k in exc for k in gated_br)}
    R["all"] = metrics(a37, a49, a57, gated)
    R["no_concept_token"] = metrics(a37, a49, a57, {i for i in gated if key_of(i) not in exc})
    R["with_concept_token"] = metrics(a37, a49, a57, {i for i in gated if key_of(i) in exc})
    for name, ov_ in (("excess_A", exc), ("excess_A_bandmean", exc_band), ("excess_own", exc_own), ("raw_A", raw)):
        brs = [k for k in gated_br if k in ov_]
        vals = sorted(ov_[k] for k in brs)
        cut = st.median(vals)
        lo = {k for k in brs if ov_[k] <= cut}
        hi = {k for k in brs if ov_[k] > cut}
        R[name] = {"cut": round(cut, 4), "low_range": [round(vals[0], 3), round(cut, 3)], "high_range": [round(cut, 3), round(vals[-1], 3)],
                   "low": metrics(a37, a49, a57, {i for i in gated if key_of(i) in lo}),
                   "high": metrics(a37, a49, a57, {i for i in gated if key_of(i) in hi}),
                   "low_relations": dict(collections.Counter(k.split("|")[0] for k in lo)),
                   "high_relations": dict(collections.Counter(k.split("|")[0] for k in hi))}
        if name == "excess_A":
            q1, q2 = vals[len(vals) // 3], vals[2 * len(vals) // 3]
            ter = {"T1": {k for k in brs if ov_[k] < q1}, "T2": {k for k in brs if q1 <= ov_[k] < q2}, "T3": {k for k in brs if ov_[k] >= q2}}
            R["tertiles_excess_A"] = {t: {"n_br": len(s), "relations": dict(collections.Counter(k.split("|")[0] for k in s)),
                                          **metrics(a37, a49, a57, {i for i in gated if key_of(i) in s})} for t, s in ter.items()}
            # within-relation median split (removes relation confound): low = below its relation's median
            wl, wh = set(), set()
            for rel in {k.split("|")[0] for k in brs}:
                rb = [k for k in brs if k.startswith(rel + "|")]
                if len(rb) < 4:
                    continue
                c = st.median(ov_[k] for k in rb)
                wl |= {k for k in rb if ov_[k] <= c}
                wh |= {k for k in rb if ov_[k] > c}
            R["within_relation_split"] = {"low": metrics(a37, a49, a57, {i for i in gated if key_of(i) in wl}),
                                          "high": metrics(a37, a49, a57, {i for i in gated if key_of(i) in wh})}
    rels = {}
    for rel in ("people", "cities", "companies", "landmarks", "films"):
        rels[rel] = metrics(a37, a49, a57, {i for i in gated if items[i]["relation"] == rel})
    rels["country_types"] = metrics(a37, a49, a57, {i for i in gated if items[i]["relation"] in COUNTRY})
    R["relation"] = rels
    R["overlap_by_relation"] = {rel: {"n": sum(1 for k in gated_br if k.startswith(rel + "|") and k in exc),
                                      "median_excess": round(st.median([exc[k] for k in gated_br if k.startswith(rel + "|") and k in exc] or [float("nan")]), 3),
                                      "median_raw": round(st.median([raw[k] for k in gated_br if k.startswith(rel + "|") and k in raw] or [float("nan")]), 3)}
                                for rel in ("people", "cities", "companies", "landmarks", "films")}
    R["per_bridge"] = {k: {"excess": round(exc[k], 4), "raw": round(raw[k], 4), "excess_own": round(exc_own.get(k, float("nan")), 4)} for k in gated_br if k in exc}
    report[P or "27b_"] = R
    print(P or "27b_", "done", flush=True)
json.dump(report, open("/tmp/ana_v4.json", "w"), indent=1)
