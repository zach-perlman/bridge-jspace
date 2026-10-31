"""nn_ko44_read (Zach, 2026-10-30, prereg amendment 68 note 44): answer or intermediate on the closed-book capital question,
read (CPU).

Runs (scripts/queues/h200_n44_1030.sh), per model prefix P, note 35's gate, band and batch:
  {P}jsuite_v5kn2c_test_chat_ko44_cand2_v1   MC and MC0, kinds clean and step2, under paper10, paper10_rot, paper10_keepCap,
                                             paper10_keepCty, paper10_keepCapCty, paper10_keepRcap, ansCap, ansCty, ansCty_rot
  {P}jsuite_v5kn2_test_chat_ko44_cand2_v1    the kn2 say twin (MM, kind clean), the same conditions
  {P}jsuite_v5kn2c_test_chat_removed_v1      note 35's removal record (the anyform stratum, beside)
Spans (scripts/ablate_v2.py, every form = either case, with or without a leading space): Cap = every capital of note 35's
  table (jsuite_v5key.CAPITAL and CAPITAL_ALIASES); Cty = every country of kn2's say vocabulary, count-matched to Cap's rows
  (Random("n44:" + item)); CapCty = their union; Rcap = a random letter-token span whose share of paper10's removal energy is
  the smallest not below Cap's (note 41's machinery, per item).
Contrast: note 35's (scripts/nn_v5_mc_read.contrast): per gated item, the whole question's loss minus its step 2's (MC0: C0,
  the direct capital closed book), in points, bootstrap over bridges (2000, seed 0).
Rescue(X) = 1 - contrast(keepX) / contrast(paper10) on MC0's items (beside: the version net of paper10_rot,
  1 - (c(keepX) - c(rot)) / (c(paper10) - c(rot)), and MC's). A rescue "counts" (>= 2/3) only if it also beats keepRcap's by
  >= 0.33.
Readings (primary stratum: all gated MC0 items; anyform beside; 27B and Lightning primary, the 9B descriptive), in this order:
  "answer only": keepCap counts and rescue(keepCty) <= 1/3;
  "both": keepCapCty counts with rescue(keepCap) <= 1/3 and rescue(keepCty) <= 1/3;
  "intermediate needed": keepCty counts, or rescue(keepCap) <= 1/3 while keepCapCty counts;
  otherwise "unclear" ("not read" if MC0's paper10 contrast is <= 0). ("both" is tested before "intermediate needed", whose
  second clause contains it.)
Amendment 71 (checked before the registered rules; the registered label is printed beside it, unchanged): "either span suffices
  (the spans overlap)" if rescue(keepCap) >= 2/3 and rescue(keepCty) >= 2/3, each beating keepRcap's by >= 0.33 (MC0, per
  stratum), with the spans' cross-overlap and each span's retained energy (paper10 rows' retained44); post hoc on the 9B. One
  added "reading either-suffices" line before each stratum's line, and "either_suffices" in the JSON.
Beside: ansCap / ansCty / ansCty_rot on MC0 (loss and contrast) next to the say twin's loss under each condition; the
  retained shares of paper10's removal energy (Cap, Cty, CapCty, Rcap and Rcap's size); the cross-overlap of the two spans
  (shared rows; mean squared cosine of their principal angles over the band's layers).
Writes results/ablate_v2/nn_v5_read/{P}note44.json and prints the readings.

python scripts/nn_ko44_read.py PREFIX      (PREFIX "" for the 27B, qwen35_9b_ for the 9B, nem35l_ for Lightning)
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts.nn_v5_mc_read import contrast, per_item  # noqa: E402
from scripts.nn_v5_read import boot_ci, items_of, ko_rows, mean  # noqa: E402

RES = ROOT / "results"
MC_SET, KN_SET = "jsuite_v5kn2c_test_chat", "jsuite_v5kn2_test_chat"
CONDS = ("paper10", "paper10_rot", "paper10_keepCap", "paper10_keepCty", "paper10_keepCapCty", "paper10_keepRcap", "ansCap", "ansCty", "ansCty_rot")
KEEPS = ("Cap", "Cty", "CapCty", "Rcap")


def rescue(acc, items, fam: str, x: str, keep) -> dict:
    """1 - contrast(keepX) / contrast(paper10) on the items with all three conditions, its bridge bootstrap, and the
    version net of paper10_rot."""
    p, k, r = (per_item(acc, fam, c, keep) for c in ("paper10", f"paper10_keep{x}", "paper10_rot"))
    by = collections.defaultdict(list)
    for i in p:
        if i in k and i in r:
            by[items[i]["bridge"]].append(((p[i][0] - p[i][1]), (k[i][0] - k[i][1]), (r[i][0] - r[i][1])))
    us = [u for v in by.values() for u in v]
    if not us:
        return {}

    def f(xs):
        cp = sum(u[0] for u in xs) / len(xs)
        return 1 - (sum(u[1] for u in xs) / len(xs)) / cp if cp > 0 else float("nan")

    def fnet(xs):
        cp, cr = (sum(u[j] for u in xs) / len(xs) for j in (0, 2))
        return 1 - (sum(u[1] for u in xs) / len(xs) - cr) / (cp - cr) if cp - cr > 0 else float("nan")

    v, vn = f(us), fnet(us)
    return {"n": len(us), "contrast_paper10": round(mean([u[0] for u in us]), 1), "contrast_keep": round(mean([u[1] for u in us]), 1),
            "rescue": round(v, 3) if v == v else None, "rescue_ci": boot_ci(by, f),
            "rescue_net_rot": round(vn, 3) if vn == vn else None, "rescue_net_rot_ci": boot_ci(by, fnet)}  # fmt: skip


def reading(r: dict) -> dict:
    if any(r.get(x, {}).get("rescue") is None for x in KEEPS):
        return {"reading": "not read: a rescue is undefined (MC0's paper10 contrast <= 0) or missing"}
    v = {x: r[x]["rescue"] for x in KEEPS}
    counts = {x: v[x] >= 2 / 3 and v[x] - v["Rcap"] >= 0.33 for x in ("Cap", "Cty", "CapCty")}
    flags = {"answer only": counts["Cap"] and v["Cty"] <= 1 / 3,
             "both": counts["CapCty"] and v["Cap"] <= 1 / 3 and v["Cty"] <= 1 / 3,
             "intermediate needed": counts["Cty"] or (v["Cap"] <= 1 / 3 and counts["CapCty"])}  # fmt: skip
    lab = next((k for k in ("answer only", "both", "intermediate needed") if flags[k]), "unclear")
    return {"reading": lab, "rescues": v, "counts_vs_Rcap": counts, "flags": flags}


def main(P: str) -> dict:
    mc_run, kn_run, rem_run = f"{P}{MC_SET}_ko44_cand2_v1", f"{P}{KN_SET}_ko44_cand2_v1", f"{P}{MC_SET}_removed_v1"
    out: dict = {"prefix": P, "role": "descriptive" if P == "qwen35_9b_" else "primary", "runs": [mc_run, kn_run, rem_run], "strata": {}}
    if not (RES / "ablate_v2" / mc_run / "rows.jsonl").exists():
        out["missing"] = mc_run
        print(f"note 44 {P or '27b_'}: {mc_run} missing")
        return out
    mc_items = items_of(MC_SET)
    acc = ko_rows(mc_run)
    removed_any = None
    rp = RES / "ablate_v2" / rem_run / "rows.jsonl"
    if rp.exists():
        removed_any = {r["id"] for r in map(json.loads, rp.open()) if r["kind"] == "clean" and r.get("any_form_removed")}
    strata = {"all": lambda i: True}
    if removed_any is not None:
        strata["anyform"] = lambda i: i not in removed_any
    lines = []
    at: dict = {}  # amendment 71: where each stratum's registered line starts (the either-suffices line goes before it)
    for sname, keep in strata.items():
        at[sname] = len(lines)
        rec: dict = {}
        for fam in ("MC0", "MC"):
            rec[fam] = {"contrast": {c: v for c in CONDS if (v := contrast(acc, mc_items, fam, c, keep))},
                        "rescue": {x: rescue(acc, mc_items, fam, x, keep) for x in KEEPS}}  # fmt: skip
        rec["reading"] = reading(rec["MC0"]["rescue"])
        rec["MC_reading_beside"] = reading(rec["MC"]["rescue"])
        out["strata"][sname] = rec
        rs = rec["MC0"]["rescue"]
        lines.append(f"note 44 {P or '27b_'} [{out['role']}] {sname}: MC0 reading {rec['reading']['reading']!r}; rescue "
                     + ", ".join(f"{x} {rs[x].get('rescue')} {rs[x].get('rescue_ci')}" for x in KEEPS)
                     + f"; MC beside {rec['MC_reading_beside']['reading']!r}")  # fmt: skip
    # beside: ansCap / ansCty / ansCty_rot on MC0 next to the say twin's loss
    c0 = out["strata"]["all"]["MC0"]["contrast"]
    say = {}
    if (RES / "ablate_v2" / kn_run / "rows.jsonl").exists():
        kacc, kitems = ko_rows(kn_run), items_of(KN_SET)
        base = kacc.get(("MM", "clean", "none"), {})
        for c in CONDS:
            ed = kacc.get(("MM", "clean", c))
            if not ed:
                continue
            by = collections.defaultdict(list)
            for i, ok in base.items():
                if i in ed:
                    by[kitems[i]["bridge"]].append(int(ok) - int(ed[i]))
            xs = [x for v in by.values() for x in v]
            say[c] = {"n": len(xs), "loss": round(mean(xs), 1), "ci": boot_ci(by, mean)}
    out["beside"] = {"MC0": {c: {k: c0[c][k] for k in ("n_items", "loss", "loss_step", "contrast", "ci")} for c in CONDS if c in c0},
                     "say_twin_MM_loss": say}  # fmt: skip
    lines.append("  ans* on MC0 (contrast / whole loss) vs the say twin's loss: " + "; ".join(
        f"{c}: MC0 {c0[c]['contrast']} / {c0[c]['loss']}, say {say.get(c, {}).get('loss')}" for c in ("paper10", "ansCap", "ansCty", "ansCty_rot") if c in c0))
    # retained energy and the spans' cross-overlap (paper10 rows' retained44; the run's n44_spans.json)
    ret = collections.defaultdict(list)
    for r in map(json.loads, (RES / "ablate_v2" / mc_run / "rows.jsonl").open()):
        if r["condition"] == "paper10" and "retained44" in r and r["id"] in acc.get((r["family"], r["kind"], "none"), {}):
            ret[f"{r['family']}/{r['kind']}"].append(r["retained44"])
    keys = ("Cap", "Cty", "CapCty", "Rcap", "k_Rcap", "span_overlap", "shared_rows")
    out["retained"] = {g: {"n": len(v), **{k: round(sum(x[k] for x in v if x[k] is not None) / len(v), 4) for k in keys},
                           "Rcap_reached_share": round(sum(x["Rcap_reached"] for x in v) / len(v), 3)} for g, v in ret.items()}  # fmt: skip
    sp = RES / "ablate_v2" / mc_run / "n44_spans.json"
    if sp.exists():
        s = json.loads(sp.read_text())
        out["spans"] = {"n_cap_rows": len(s["cap_rows"]), "n_cty_rows": len(s["cty_rows"]), "shared_rows": len(s["shared_rows"]),
                        "shared_tokens": s["shared_tokens"]}  # fmt: skip
    g = out["retained"].get("MC0/clean", {})
    lines.append(f"  retained (MC0 whole question): {json.dumps(g)}; spans {json.dumps(out.get('spans', {}))[:300]}")
    # amendment 71: "either span suffices (the spans overlap)", checked before the registered rules on MC0 (point rescues, as the
    # registered rules), printed before each stratum's registered line, with the spans' cross-overlap and retained energy
    per44 = {}
    for r in map(json.loads, (RES / "ablate_v2" / mc_run / "rows.jsonl").open()):
        if (r["condition"] == "paper10" and r["family"] == "MC0" and r["kind"] == "clean" and "retained44" in r
                and r["id"] in acc.get(("MC0", "clean", "none"), {})):  # fmt: skip
            per44[r["id"]] = r["retained44"]
    out["either_suffices"], new = {}, {}
    tag = f"[{out['role']}{', post hoc' if P == 'qwen35_9b_' else ''}]"
    for sname, keep in strata.items():
        rec = out["strata"][sname]
        v = {x: rec["MC0"]["rescue"].get(x, {}).get("rescue") for x in ("Cap", "Cty", "Rcap")}
        vs = [per44[i] for i in per44 if keep(i)]
        geo: dict = {"n_items": len(vs)}
        for k in ("Cap", "Cty", "span_overlap", "shared_rows"):
            xs = [x[k] for x in vs if x.get(k) is not None]
            geo[k] = round(sum(xs) / len(xs), 4) if xs else None
        if all(geo[k] is not None for k in ("Cap", "Cty", "span_overlap", "shared_rows")):
            gtxt = (f"cross-overlap: mean squared cosine of the principal angles {geo['span_overlap']}, shared rows {geo['shared_rows']}; "
                    f"retained energy (share of paper10's removal): Cap {geo['Cap']}, Cty {geo['Cty']} (per-item means, MC0 whole question, "
                    f"n {geo['n_items']})")  # fmt: skip
        else:
            gtxt = "cross-overlap and retained energy: not computable from stored rows (no retained44 on this stratum's paper10 rows)"
        if any(x is None for x in v.values()):
            met, lab = None, "not read: a rescue is undefined or missing"
        else:
            met = all(v[x] >= 2 / 3 and v[x] - v["Rcap"] >= 0.33 for x in ("Cap", "Cty"))
            lab = "either span suffices (the spans overlap)" if met else "not met"
        out["either_suffices"][sname] = {"met": met, "reading": lab, "rescues": v, "geometry": geo,
                                         "registered_label": rec["reading"]["reading"]}  # fmt: skip
        dif = ", ".join(f"{x} - Rcap {round(v[x] - v['Rcap'], 3)}" for x in ("Cap", "Cty")) if met is not None else "n/a"
        new[sname] = (f"reading either-suffices (amendment 71) note 44 {P or '27b_'} {tag} {sname}: {lab}; MC0 rescue Cap {v['Cap']}, "
                      f"Cty {v['Cty']}, Rcap {v['Rcap']} ({dif}); {gtxt}; registered label beside: {rec['reading']['reading']!r}")  # fmt: skip
    for sname in reversed(list(strata)):  # insert from the last stratum so the earlier positions stay valid
        lines.insert(at[sname], new[sname])
    d = RES / "ablate_v2" / "nn_v5_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{P}note44.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    main(ap.parse_args().prefix)
