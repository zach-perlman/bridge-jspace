"""nn_ko49_read (Zach, 2026-10-30, prereg amendment 72 notes 49 and 50): the paper's output protection sealed, and the
orthogonal placebo / exact complement / rank-matched ansR, read (CPU).

Run (scripts/queues/h200_n49_1030.sh), per model prefix P: {P}jsuite_v4_test_chat_ko49_cand2_v1 (note 20's gate, band and batch;
v4 seed 4001; every position) under paper10, paper10_rot and, each + _rot: paper10_protF, protC, keepT10, keepRT10, keepOwn,
keepSib, keepR4perp, keepR8perp, onlyA, and ansRk. Its keeplog.jsonl holds, per item, paper10's removal energy in each kept span
(E_X), alpha_X, the protections' E and still-removed answer part, ranks and |edit| / |h| (scripts/ablate_v2.py, amendment 72).
Stored runs beside: {P}jsuite_v4_test_chat_ko37_cand2_v1 (keepA, ansJ) and {P}jsuite_v4_test_chat_ko41_cand2_v1 (R, R2, R4, ansR).
Measures (note 41's): loss = 100 x (correct_cand2 unedited - edited) over the gated items; gap = MM - MP; ratio(X) = (X - X_rot) /
(paper10 - paper10_rot) on MM's loss within the run; rescue = 1 - ratio; 95% bootstrap over bridges (2000 draws,
random.Random(0); every gated item of a bridge resampled together). rescue_L (amendment 70): the same in the gold answer's
first-token log p (mean MM delta log p, each net of its _rot). E_X = the mean over MM's gated items of the per-item share.
Readings (per model, MM):
  note 49 R1 (primary): protF "the protection leaks through spellings" if ratio <= 1/3 and protF's gap < 15; "not through
    spellings" if ratio >= 2/3; otherwise "partly". protC by the same rule: "leaks through J++ neighbours" / "not through J++
    neighbours" / "partly".
  note 49 R2: "the output candidates' directions" if ratio(keepT10) <= 1/3 and rescue(keepT10) - rescue(keepRT10) >= 0.33 with
    its CI's lower end > 0; "beyond the candidates" if ratio(keepT10) >= 2/3; otherwise "partly".
  note 49 R3: "this item's answer" if rescue(keepOwn) - rescue(keepSib) >= 0.20 with CI > 0; "the category" if |difference| < 0.10
    and rescue(keepOwn) >= 2/3; otherwise "unclear".
  note 50 P1 (primary): the perp keep with E closest to E_A and not below it; "the placebo's rescue is its overlap with the answer
    span" if its rescue <= 1/3, "non-answer J content rescues" if >= 2/3, otherwise "partly"; "not matched" if both perps hold
    E < E_A. P2: P1 in rescue_L (same perp). P3: "the answer part is sufficient for the damage" if onlyA's net MM loss >= 2/3 of
    paper10's and onlyA's gap >= 2/3 of paper10's (otherwise "not shown"). P4: note 41's removal rule with ansRk for ansR:
    "answer-specific removal" if ansRk's gap <= 1/3 of ansJ's (note 37's run; joint bridge bootstrap), otherwise "not
    answer-specific" (note 41's ansR reading reported beside).
  ("not read" where a denominator (paper10 - paper10_rot loss, or ansJ's gap) is <= 0.)
Beside: MP losses; keepA's rescue (note 37's run); the protections' row counts and still-removed answer share. Descriptive:
rescue against alpha for every keep (A from note 37's run, R / R2 / R4 from note 41's, the rest from this run).
Checks: this run's none / paper10 / paper10_rot rows against note 41's stored run (same reads, same log-prob bits).
Writes results/ablate_v2/nn_ko_read/{P}note49_50.json (or --out-dir) and prints one "reading ..." line per registered reading.
Amendment 77 (--set, another v4 draw, e.g. jsuite_v4p4002_test_chat): reads {P}{set}_ko49_cand2_v1; the draw's note 37 / 41 run
{P}{set}_ko37_cand2_v1 (it holds paper10 / paper10_rot, keepA, ansJ and note 41's R / R2 / R4 / ansR) serves as both stored runs
and as the stored check; writes {P}{set}_note49_50.json and, per reading, a "reading replication ..." line: "replicates" if the
label equals draw 4001's ({P}note49_50.json), otherwise "does not replicate" (no pooling across draws). The default call is
unchanged.

python scripts/nn_ko49_read.py PREFIX [--set SET] [--run-dir DIR] [--out-dir DIR]   (PREFIX "" for the 27B, qwen35_9b_, nem35l_)
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K  # noqa: E402
from scripts.nn_ko41_read import gap_ratio, keep_ratio  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
SET = "jsuite_v4_test_chat"
N49 = ("protF", "protC", "keepT10", "keepRT10", "keepOwn", "keepSib")
N50 = ("keepR4perp", "keepR8perp", "onlyA")
CONDS = ("paper10", "paper10_rot") + tuple(f"paper10_{x}{s}" for x in N49 + N50 for s in ("", "_rot")) + ("ansRk", "ansRk_rot")


def rows_at(d: Path) -> dict:
    """(family, condition) -> id -> (correct_cand2, logp), as nn_ko37_read.rows_of, from a run directory."""
    acc: dict = collections.defaultdict(dict)
    for line in (d / "rows.jsonl").open():
        r = json.loads(line)
        if r.get("kind", "clean") == "clean":
            acc[(r["family"], r["condition"])][r["id"]] = (bool(r["correct_cand2"]), r["logp"])
    return acc


def units(acc: dict, items: dict, conds: tuple, logp: bool = False) -> dict:
    """bridge -> per MM item tuple over conds: the loss (unedited - edited correct) or, with logp, the edited - unedited log p."""
    by = collections.defaultdict(list)
    for i, (ok, lp) in acc.get(("MM", "none"), {}).items():
        if all(i in acc.get(("MM", c), {}) for c in conds):
            by[items[i]["bridge"]].append(tuple((acc[("MM", c)][i][1] - lp) if logp else (int(ok) - int(acc[("MM", c)][i][0])) for c in conds))
    return by


def rf(us: list, j: int = 0) -> float:
    """ratio over MM items: (u[j] - u[j+1]) / (u[-2] - u[-1]) summed (for logp the denominator's sign is flipped: losses are
    negative log-prob changes, so the ratio is (dX - dXrot) / (dP - dProt) with dP - dProt < 0 the damage)."""
    den = sum(u[-2] - u[-1] for u in us)
    return sum(u[j] - u[j + 1] for u in us) / den if den != 0 else float("nan")


def ratio_of(acc, items, x: str, xr: str, base=("paper10", "paper10_rot"), logp: bool = False) -> dict:
    by = units(acc, items, (x, xr) + base, logp)
    us = [u for v in by.values() for u in v]
    if not us:
        return {}
    den = sum(u[2] - u[3] for u in us)
    ok = den > 0 if not logp else den < 0  # paper10 must do net damage (loss > 0, or log p change < 0)
    r = rf(us) if ok else float("nan")
    ci = K.boot(by, lambda xs: 100 * rf(xs)) if ok else None
    return {"n_MM": len(us), "net_X": round(sum(u[0] - u[1] for u in us) / len(us) * (1 if logp else 100), 3 if logp else 1),
            "net_paper10": round(den / len(us) * (1 if logp else 100), 3 if logp else 1),
            "ratio": round(r, 3) if r == r else None, "ratio_ci": [v / 100 for v in ci] if ci else None,
            "rescue": round(1 - r, 3) if r == r else None, "rescue_ci": [round(1 - v / 100, 3) for v in reversed(ci)] if ci else None}  # fmt: skip


def rescue_diff(acc, items, x: str, y: str, logp: bool = False) -> dict:
    """rescue(paper10_x) - rescue(paper10_y) = ratio(y) - ratio(x), with a joint bridge bootstrap."""
    c = (f"paper10_{x}", f"paper10_{x}_rot", f"paper10_{y}", f"paper10_{y}_rot", "paper10", "paper10_rot")
    by = units(acc, items, c, logp)

    def fn(us):
        den = sum(u[4] - u[5] for u in us)
        if (den <= 0 and not logp) or (den >= 0 and logp):
            return float("nan")
        return (sum(u[2] - u[3] for u in us) - sum(u[0] - u[1] for u in us)) / den

    us = [u for v in by.values() for u in v]
    v = fn(us) if us else float("nan")
    ci = K.boot(by, lambda xs: 100 * fn(xs)) if us else None
    return {"diff": round(v, 3) if v == v else None, "ci": [w / 100 for w in ci] if ci else None, "n_MM": len(us)}


def energies(d: Path, acc: dict) -> dict:
    """Mean per-item E_X, alpha_X, ranks and the protections' logs over MM's (and MP's) gated items, from keeplog.jsonl."""
    out = {}
    lines = [json.loads(l) for l in (d / "keeplog.jsonl").open()] if (d / "keeplog.jsonl").exists() else []
    for f in ("MM", "MP"):
        xs = [x for x in lines if x["family"] == f and x["condition"] == "paper10" and x["id"] in acc.get((f, "none"), {}) and x["energy"] > 0]
        if not xs:
            continue
        mean = lambda vals: round(sum(vals) / len(vals), 4) if vals else None  # noqa: E731
        out[f] = {"n": len(xs), "E": {k: mean([x["E"][k] for x in xs if x["E"].get(k) is not None]) for k in xs[0]["E"]},
                  "alpha": {k: mean([x["alpha"][k] for x in xs if x["alpha"].get(k) is not None]) for k in xs[0].get("alpha", {})},
                  "rank": {k: mean([x["rank"][k] for x in xs]) for k in xs[0]["rank"]},
                  "edit_rel_paper10": mean([x["edit_rel"] for x in xs if x["edit_rel"] is not None]),
                  "prot": {kp: {k: mean([x["prot"][kp][k] for x in xs if x["prot"][kp][k] is not None]) for k in xs[0]["prot"][kp]}
                           for kp in xs[0].get("prot", {})},
                  "n_rows": {k: mean([x["n_rows"][k] for x in xs]) for k in xs[0].get("n_rows", {})},
                  "sib_count_matched": round(sum(x["sib"]["sib_matched"] for x in xs) / len(xs), 3) if "sib" in xs[0] else None}  # fmt: skip
    return out


def lab3(r: float | None, lo: str, hi: str, extra_lo: bool = True) -> str:
    if r is None:
        return "not read: paper10 - paper10_rot <= 0 (ratio undefined)"
    return lo if r <= 1 / 3 and extra_lo else hi if r >= 2 / 3 else "partly"


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None, set_name: str = SET) -> dict:
    items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / set_name / "items.jsonl").open()}
    run = f"{P}{set_name}_ko49_cand2_v1"
    d = run_dir or RES / "ablate_v2" / run
    n37, n41 = f"{P}{set_name}_ko37_cand2_v1", f"{P}{set_name}_ko41_cand2_v1"
    if set_name != SET:  # amendment 77: a draw's note 37 and note 41 conditions ran in one run (notes 43 / 48)
        n41 = n37
    out: dict = {"prefix": P, "run": str(d), "stored": [n37, n41], **({"set": set_name} if set_name != SET else {})}
    if not (d / "rows.jsonl").exists():
        print(f"note 49/50 {P or '27b_'}: {d} missing")
        return out
    acc = rows_at(d)
    a37 = rows_at(RES / "ablate_v2" / n37) if (RES / "ablate_v2" / n37 / "rows.jsonl").exists() else None
    a41 = rows_at(RES / "ablate_v2" / n41) if (RES / "ablate_v2" / n41 / "rows.jsonl").exists() else None
    every = lambda it: True  # noqa: E731
    m = K.measures(acc, items, every, CONDS)
    out["measures"] = m
    out["stored_check"] = K.stored_check(acc, n41)
    cs = m["conditions"]
    tag = P or "27b_"
    if set_name != SET:
        tag = f"{tag} {set_name}"
    lines = K.table(f"notes 49/50 {tag}", m)
    rat = {x: ratio_of(acc, items, f"paper10_{x}", f"paper10_{x}_rot") for x in N49 + N50}
    ratL = {x: ratio_of(acc, items, f"paper10_{x}", f"paper10_{x}_rot", logp=True) for x in N49 + N50}
    out["ratio"], out["ratio_logp"] = rat, ratL
    E = energies(d, acc)
    out["energy"] = E
    eMM = E.get("MM", {}).get("E", {})
    R: dict = {}
    # note 49 R1
    for x, lo, hi in (("protF", "the protection leaks through spellings", "not through spellings"),
                      ("protC", "the protection leaks through J++ neighbours", "not through J++ neighbours")):
        g = cs.get(f"paper10_{x}", {}).get("gap")
        r = rat[x].get("ratio")
        R[f"49_R1_{x}"] = {"label": lab3(r, lo, hi, g is not None and g < 15), "ratio": r, "ratio_ci": rat[x].get("ratio_ci"),
                           "gap": g, "gap_ci": cs.get(f"paper10_{x}", {}).get("gap_ci"), "n_MM": rat[x].get("n_MM")}  # fmt: skip
    # note 49 R2
    dT = rescue_diff(acc, items, "keepT10", "keepRT10")
    r = rat["keepT10"].get("ratio")
    cand = r is not None and r <= 1 / 3 and dT["diff"] is not None and dT["diff"] >= 0.33 and dT["ci"] and dT["ci"][0] > 0
    R["49_R2"] = {"label": ("not read: paper10 - paper10_rot <= 0" if r is None else "the output candidates' directions" if cand
                            else "beyond the candidates" if r >= 2 / 3 else "partly"),
                  "ratio_keepT10": r, "ratio_ci": rat["keepT10"].get("ratio_ci"), "rescue_T10_minus_RT10": dT["diff"], "diff_ci": dT["ci"],
                  "rescue_RT10": rat["keepRT10"].get("rescue"), "n_MM": dT["n_MM"]}  # fmt: skip
    # note 49 R3
    dO = rescue_diff(acc, items, "keepOwn", "keepSib")
    ro = rat["keepOwn"].get("rescue")
    if dO["diff"] is None or ro is None:
        l3 = "not read: paper10 - paper10_rot <= 0"
    elif dO["diff"] >= 0.20 and dO["ci"] and dO["ci"][0] > 0:
        l3 = "this item's answer"
    elif abs(dO["diff"]) < 0.10 and ro >= 2 / 3:
        l3 = "the category"
    else:
        l3 = "unclear"
    R["49_R3"] = {"label": l3, "rescue_own": ro, "rescue_own_ci": rat["keepOwn"].get("rescue_ci"), "rescue_sib": rat["keepSib"].get("rescue"),
                  "own_minus_sib": dO["diff"], "diff_ci": dO["ci"], "n_MM": dO["n_MM"],
                  "keepA_rescue_n37_beside": (keep_ratio(a37, items, "A").get("rescue") if a37 else None)}  # fmt: skip
    # note 50 P1 / P2
    eA = eMM.get("A")
    perps = {x: eMM.get(x) for x in ("R4perp", "R8perp")}
    above = [x for x, e in perps.items() if e is not None and eA is not None and e >= eA]
    star = min(above, key=lambda x: perps[x] - eA) if above else None
    for key, rr, name in (("50_P1", rat, "rescue"), ("50_P2", ratL, "rescue_L")):
        if star is None:
            lab = "not matched: both perps hold E < E_A" if eA is not None and all(e is not None for e in perps.values()) else "not read: no energy log"
            R[key] = {"label": lab, "E_A": eA, "E_perps": perps}
            continue
        v = rr[f"keep{star}"].get("rescue")
        R[key] = {"label": ("not read: paper10 - paper10_rot <= 0" if v is None else "the placebo's rescue is its overlap with the answer span"
                            if v <= 1 / 3 else "non-answer J content rescues" if v >= 2 / 3 else "partly"),
                  "perp": star, "E_A": eA, "E_perps": perps, name: v, f"{name}_ci": rr[f"keep{star}"].get("rescue_ci"),
                  "n_MM": rr[f"keep{star}"].get("n_MM"), "other_perp": {x: rr[f"keep{x}"].get("rescue") for x in perps}}  # fmt: skip
    # note 50 P3
    p10, p10r = cs.get("paper10", {}), cs.get("paper10_rot", {})
    oa, oar = cs.get("paper10_onlyA", {}), cs.get("paper10_onlyA_rot", {})
    if p10 and oa:
        net_o, net_p = oa["loss_MM"] - oar["loss_MM"], p10["loss_MM"] - p10r["loss_MM"]
        gr = gap_ratio(acc, acc, items, "paper10_onlyA", "paper10")
        suff = net_p > 0 and p10["gap"] > 0 and net_o >= 2 / 3 * net_p and oa["gap"] >= 2 / 3 * p10["gap"]
        R["50_P3"] = {"label": "the answer part is sufficient for the damage" if suff else "not shown",
                      "onlyA_net_MM": round(net_o, 1), "paper10_net_MM": round(net_p, 1), "net_share": rat["onlyA"].get("ratio"),
                      "net_share_ci": rat["onlyA"].get("ratio_ci"), "onlyA_gap": oa["gap"], "paper10_gap": p10["gap"],
                      "gap_share": gr["ratio"], "gap_share_ci": gr["ratio_ci"], "n_MM": rat["onlyA"].get("n_MM")}  # fmt: skip
    # note 50 P4
    if a37 is not None and "ansRk" in cs:
        m37 = K.measures(a37, items, every, ("ansJ", "ansJ_rot"))["conditions"]
        gJ, gK = m37["ansJ"]["gap"], cs["ansRk"]["gap"]
        rr = gap_ratio(acc, a37, items, "ansRk", "ansJ")
        R["50_P4"] = {"label": ("not read: ansJ's gap <= 0" if gJ <= 0 else "answer-specific removal" if gK <= gJ / 3 else "not answer-specific"),
                      "ansRk_gap": gK, "ansRk_gap_ci": cs["ansRk"]["gap_ci"], "ansJ_gap": gJ, "ansJ_gap_ci": m37["ansJ"]["gap_ci"],
                      "ratio": rr["ratio"], "ratio_ci": rr["ratio_ci"], "ansRk_rot_gap": cs.get("ansRk_rot", {}).get("gap"),
                      "ansJ_rot_gap": m37.get("ansJ_rot", {}).get("gap"),
                      "rows": E.get("MM", {}).get("n_rows", {}).get("Rk")}  # fmt: skip
        if a41 is not None:
            m41 = K.measures(a41, items, every, ("ansR", "ansR_rot"))["conditions"]
            if "ansR" in m41:
                r41 = gap_ratio(a41, a37, items, "ansR", "ansJ")
                R["50_P4"]["note41_ansR_beside"] = {"ansR_gap": m41["ansR"]["gap"], "ratio": r41["ratio"], "ratio_ci": r41["ratio_ci"],
                                                    "reading": "answer-specific removal" if gJ > 0 and m41["ansR"]["gap"] <= gJ / 3 else "not answer-specific"}  # fmt: skip
    out["readings"] = R
    # descriptive: rescue against alpha
    al = E.get("MM", {}).get("alpha", {})
    desc = {"A": {"rescue": keep_ratio(a37, items, "A").get("rescue") if a37 else None, "alpha": al.get("A"), "E": eA, "src": n37}}
    for x in ("R", "R2", "R4"):
        desc[x] = {"rescue": keep_ratio(a41, items, x).get("rescue") if a41 else None, "alpha": al.get(x), "E": eMM.get(x), "src": n41}
    for x in ("T10", "RT10", "Own", "Sib", "R4perp", "R8perp"):
        desc[x] = {"rescue": rat[f"keep{x}"].get("rescue"), "rescue_L": ratL[f"keep{x}"].get("rescue"), "alpha": al.get(x), "E": eMM.get(x), "src": "this run"}
    out["rescue_vs_alpha"] = desc
    for k, v in R.items():
        main_v = {kk: vv for kk, vv in v.items() if kk != "label"}
        lines.append(f"reading note{k[:2]} {k[3:]} {tag}: {v['label']!r} | " + json.dumps(main_v)[:600])
    lines.append("  rescue vs alpha (MM): " + "; ".join(f"{x}: rescue {t['rescue']} alpha {t['alpha']} E {t['E']}" for x, t in desc.items()))
    pr = E.get("MM", {}).get("prot", {})
    lines.append(f"  protections (MM means): {json.dumps(pr)}; n_rows {json.dumps(E.get('MM', {}).get('n_rows', {}))}")
    if set_name != SET:  # amendment 77: the same registered label as draw 4001's, per reading
        ref_p = RES / "ablate_v2" / "nn_ko_read" / f"{P}note49_50.json"
        ref = json.loads(ref_p.read_text()).get("readings", {}) if ref_p.exists() else {}
        out["replication"] = {}
        for k, v in R.items():
            base = ref.get(k, {}).get("label")
            rep_ = ("not compared: draw 4001's reading missing" if base is None else "replicates" if base == v["label"] else "does not replicate")
            out["replication"][k] = {"label": rep_, "draw4001": base, "this_draw": v["label"]}
            lines.append(f"reading replication note{k[:2]} {k[3:]} {tag}: {rep_!r} (draw 4001 {base!r}, this draw {v['label']!r})")
    lines.append("  MP losses: " + ", ".join(f"{c} {r['loss_MP']}" for c, r in cs.items()))
    sc = out["stored_check"]
    if not sc.get("missing"):
        lines.append(f"  stored check ({sc['stored_run']}): " + "; ".join(
            f"{c} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']}" for c, v in sc.items() if c != "stored_run"))
    od = out_dir or RES / "ablate_v2" / "nn_ko_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / (f"{P}note49_50.json" if set_name == SET else f"{P}{set_name}_note49_50.json")).write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--set", default=SET, help="amendment 77: another v4 draw (e.g. jsuite_v4p4002_test_chat)")
    ap.add_argument("--run-dir", type=Path, default=None, help="the run's directory (default results/ablate_v2/{P}{set}_ko49_cand2_v1)")
    ap.add_argument("--out-dir", type=Path, default=None, help="where the JSON goes (default results/ablate_v2/nn_ko_read)")
    a = ap.parse_args()
    main(a.prefix, a.run_dir, a.out_dir, a.set)
