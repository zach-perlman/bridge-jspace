"""nn_ko63_read (Zach, 2026-10-30, prereg amendment 86 note 63): the mechanism beyond country answers, read (CPU).

Run (scripts/queues/h200_n63_1030.sh): {P}jsuite_v2_test_chat_ko63_cand2_v1, note 57's battery (paper10, paper10_onlyA,
paper10_onlyRperp, top30 / top100 with keepA and keepRE, ansJ, ansRe, each + _rot) plus note 37's paper10_keepA / _rot, at each
model's main band and batch, on every v2 relation's MP and MM items (gated per word by the v2 competence run, cand2).
Gate (the closest version of note 37's / note 20's on v2): the run's per-word competence gate (whole, hop 1 and hop 2 right) and,
here, v4_split's other rule: the no-description guess prompt answered wrong ({P}jsuite_v2_test_chat_competence_cand2_v1's "guess"
part; an item without one is dropped). v4_split's closed-book H1 check needs a v4 control set that v2 lacks. The per-word gate
alone is printed beside ("gate pw").
Relations (jsuite_v2_test_chat's MP / MM answer_vocab): non-country: animals (6 animal classes), countries (5 continents),
languages (16 languages; 11 share their word with a nationality adjective); country-type, beside: cities, companies, dishes,
landmarks (country names), people (nationality adjectives).
Measures: nn_ko37_read's (loss, MM - MP gap, bridge bootstrap: 2000 draws, random.Random(0), every gated item of a bridge
together), on each relation's items, pooled over the non-country relations, and pooled over the country-type ones (beside).
Readings (per non-country relation with >= 30 gated MM items, and the non-country pool):
  C1 (validity): paper10's MM - MP gap >= 20 with the lower end > 0; without it the relation is "not readable".
  K: note 37's keepA rule (ratio = (keepA - keepA_rot) / (paper10 - paper10_rot) on MM <= 1/3, keepA's gap < 10 and its upper end
     < 15); keepA rescue = 1 - ratio.
  S1: note 57's rule ([(onlyA - onlyA_rot) - (onlyRperp - onlyRperp_rot)] MM loss >= 1/3 of paper10's net, lower end > 0).
  E: note 57's D1: rescue(topK_keepA) - rescue(topK_keepRE) >= 0.33 with the lower end > 0, at K = 30 and K = 100; E is met when
     it is met at both doses (builder's reading of "keepA - keepRE rescue"; each dose is printed).
  Verdict: kill if keepA rescue < 0.5 or S1 < 0.5 on >= 2 readable non-country relations (on the pool if fewer than 2 are
  readable) = "the mechanism is specific to country-type answers"; pass if K, S1 and E are met on the pool and on every readable
  relation = "the answer-direction account holds beyond country answers"; otherwise "partly" (relations named).
  Relations with < 30 gated MM items are read in the pool only (their numbers are printed as descriptive).
Beside: A1 (ansRe's gap vs ansJ's), A's rank and energy share E_A (keeplog), the stored check of none / paper10 / paper10_rot
against {P}jsuite_v2_test_chat_ko_cand2_v1 (same band, batch and positions; scene-gated, so the ids overlap only in part).
Writes results/ablate_v2/nn_ko_read/{P}note63.json (or --out-dir) and prints one "reading ..." line per registered reading.

python scripts/nn_ko63_read.py PREFIX [--run-dir DIR] [--out-dir DIR]   (PREFIX "" for the 27B, qwen35_9b_, nem35l_)
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K  # noqa: E402
from scripts.nn_ko41_read import gap_ratio  # noqa: E402
from scripts.nn_ko49_read import rows_at  # noqa: E402
from scripts.nn_ko57_read import DOSES, contrast  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
SET = "jsuite_v2_test_chat"
NONCOUNTRY = ("animals", "countries", "languages")  # answers: animal classes, continents, languages
COUNTRY = ("cities", "companies", "dishes", "landmarks", "people")  # answers: country names, nationality adjectives (beside)
MIN_MM = 30
CONDS = (("paper10", "paper10_rot", "paper10_keepA", "paper10_keepA_rot")
         + tuple(f"paper10_{x}{s}" for x in ("onlyA", "onlyRperp") for s in ("", "_rot"))
         + tuple(f"top{k}{s}" for k in DOSES for s in ("", "_rot", "_keepA", "_keepA_rot", "_keepRE", "_keepRE_rot"))
         + ("ansJ", "ansJ_rot", "ansRe", "ansRe_rot"))  # fmt: skip
K_MET = "the recall's J-need is its answer's directions"


def guess_wrong(P: str) -> set:
    """Ids whose no-description guess prompt the model answered wrong (v4_split's rule: guess is False)."""
    out = set()
    for line in (RES / "tasks_v2" / f"{P}{SET}_competence_cand2_v1" / "items.jsonl").open():
        r = json.loads(line)
        if r["part"] == "guess" and r["correct"] is False:
            out.add(r["id"])
    return out


def sub(acc: dict, ids: set) -> dict:
    return collections.defaultdict(dict, {k: {i: v for i, v in d.items() if i in ids} for k, d in acc.items()})


def read(acc: dict, items: dict, ids: set, keeplog: dict) -> dict:
    """Every registered measure on the items in ids."""
    a = sub(acc, ids)
    m = K.measures(a, items, lambda it: True, CONDS)
    cs = m.get("conditions", {})
    rec: dict = {"n": m["n"]}
    p = cs.get("paper10")
    rec["C1"] = {"met": bool(p and p["gap"] >= 20 and p["gap_ci"] and p["gap_ci"][0] > 0),
                 "gap": p and p["gap"], "gap_ci": p and p["gap_ci"], "loss_MM": p and p["loss_MM"], "loss_MP": p and p["loss_MP"],
                 "paper10_rot_gap": cs.get("paper10_rot", {}).get("gap")}  # fmt: skip
    rt = m.get("ratio") or {}
    r = rt.get("ratio")
    rec["K"] = {"met": m.get("reading") == K_MET, "note37_label": m.get("reading"), "ratio": r, "ratio_ci": rt.get("ratio_ci"),
                "keepA_rescue": (round(1 - r, 3) if r is not None else None),
                "keepA_rescue_ci": ([round(1 - rt["ratio_ci"][1], 3), round(1 - rt["ratio_ci"][0], 3)] if rt.get("ratio_ci") else None),
                "keepA_gap": cs.get("paper10_keepA", {}).get("gap"), "keepA_gap_ci": cs.get("paper10_keepA", {}).get("gap_ci"),
                "keepA_net_MM": rt.get("keepA_net_MM"), "paper10_net_MM": rt.get("paper10_net_MM")}  # fmt: skip
    s1 = contrast(a, items, ("paper10_onlyA", "paper10_onlyA_rot"), ("paper10_onlyRperp", "paper10_onlyRperp_rot"), ("paper10", "paper10_rot"))
    rec["S1"] = {"met": bool(s1.get("value") is not None and s1["value"] >= 1 / 3 and s1["ci"] and s1["ci"][0] > 0), **s1}
    rec["E"] = {}
    for k in DOSES:  # rescue(A) - rescue(RE) = ratio(RE) - ratio(A): the contrast with a = RE, b = A (as nn_ko57_read)
        dk = contrast(a, items, (f"top{k}_keepRE", f"top{k}_keepRE_rot"), (f"top{k}_keepA", f"top{k}_keepA_rot"), (f"top{k}", f"top{k}_rot"))
        rec["E"][f"K{k}"] = {"met": bool(dk.get("value") is not None and dk["value"] >= 0.33 and dk["ci"] and dk["ci"][0] > 0),
                             "rescue_A_minus_RE": dk.get("value"), "ci": dk.get("ci"), "n_MM": dk.get("n_MM"), "den_points": dk.get("den_points")}  # fmt: skip
    rec["E"]["met"] = all(rec["E"][f"K{k}"]["met"] for k in DOSES)
    if "ansRe" in cs and "ansJ" in cs:  # A1, beside
        gJ, gE = cs["ansJ"]["gap"], cs["ansRe"]["gap"]
        rr = gap_ratio(a, a, items, "ansRe", "ansJ")
        rec["A1_beside"] = {"label": ("not read: ansJ's gap <= 0" if gJ <= 0 else "answer-specific removal at matched energy" if gE <= gJ / 3
                                      else "not answer-specific at matched energy"), "ansJ_gap": gJ, "ansJ_gap_ci": cs["ansJ"]["gap_ci"],
                            "ansRe_gap": gE, "ansRe_gap_ci": cs["ansRe"]["gap_ci"], **rr}  # fmt: skip
    kl = [keeplog[i] for i in ids if i in keeplog and items[i]["word"] == "MM"]
    if kl:
        rec["A_beside"] = {"n_MM": len(kl), "rank_A_median": statistics.median(x[0] for x in kl), "E_A_mean": round(statistics.mean(x[1] for x in kl), 3)}
    rec["fail_kill"] = bool((rec["K"]["keepA_rescue"] is not None and rec["K"]["keepA_rescue"] < 0.5)
                            or (s1.get("value") is not None and s1["value"] < 0.5))  # fmt: skip
    rec["all_met"] = rec["K"]["met"] and rec["S1"]["met"] and rec["E"]["met"]
    rec["measures"] = m
    return rec


def verdict(per: dict, pool: dict) -> dict:
    """Amendment 86's kill / pass / partly over the non-country relations (per: relation -> rec; pool: the pooled rec)."""
    readable = [r for r in NONCOUNTRY if r in per and per[r]["n"].get("MM", 0) >= MIN_MM and per[r]["C1"]["met"]]
    pool_ok = pool["C1"]["met"]
    if len(readable) >= 2:
        failing = [r for r in readable if per[r]["fail_kill"]]
        kill, on = len(failing) >= 2, failing
    else:
        kill, on = pool_ok and pool["fail_kill"], ["pool"]
    if kill:
        return {"label": "the mechanism is specific to country-type answers", "readable": readable, "on": on}
    if not pool_ok and len(readable) < 2:
        return {"label": "not readable: the non-country pool fails C1 and fewer than 2 relations are readable", "readable": readable}
    if pool_ok and pool["all_met"] and all(per[r]["all_met"] for r in readable):
        return {"label": "the answer-direction account holds beyond country answers", "readable": readable}
    short = [x for x in readable + ["pool"] if not (pool if x == "pool" else per[x])["all_met"] or (x == "pool" and not pool_ok)]
    return {"label": "partly", "readable": readable, "not_met": short,
            "detail": {x: {k: (pool if x == "pool" else per[x])[k]["met"] for k in ("C1", "K", "S1", "E")} for x in short}}


def ci(x) -> str:
    return f"[{x[0]}, {x[1]}]" if x else "None"


def lines_of(name: str, rec: dict, tag: str, pooled_only: bool) -> list[str]:
    n = rec["n"]
    pre = f"note63 {{}} {name} {tag} (n MP {n.get('MP')} MM {n.get('MM')})"
    d = " [descriptive: < 30 gated MM, read in the pool only]" if pooled_only else ""
    c1, k, s1, e = rec["C1"], rec["K"], rec["S1"], rec["E"]
    out = [f"{pre.format('C1')}: {'valid' if c1['met'] else 'not readable'}{d} | paper10 gap {c1['gap']} {ci(c1['gap_ci'])} (loss MM {c1['loss_MM']} MP {c1['loss_MP']}; rot gap {c1['paper10_rot_gap']})",
           f"{pre.format('K')}: {'met' if k['met'] else 'not met'} ({k['note37_label']!r}){d} | keepA rescue {k['keepA_rescue']} {ci(k['keepA_rescue_ci'])}; ratio {k['ratio']} {ci(k['ratio_ci'])}; keepA gap {k['keepA_gap']} {ci(k['keepA_gap_ci'])}; nets keepA {k['keepA_net_MM']} paper10 {k['paper10_net_MM']}",
           f"{pre.format('S1')}: {'met' if s1['met'] else 'not met'}{d} | S1 {s1.get('value')} {ci(s1.get('ci'))} (n MM {s1.get('n_MM')}; {s1.get('points')} of {s1.get('den_points')} points)",
           f"{pre.format('E')}: {'met' if e['met'] else 'not met'}{d} | " + "; ".join(
               f"K{kk}: {'met' if e[f'K{kk}']['met'] else 'not met'} rescue A - RE {e[f'K{kk}']['rescue_A_minus_RE']} {ci(e[f'K{kk}']['ci'])} (n MM {e[f'K{kk}']['n_MM']}, topK net {e[f'K{kk}']['den_points']})" for kk in DOSES)]  # fmt: skip
    return out


def beside(name: str, rec: dict) -> str:
    n, c1, k, s1, e = rec["n"], rec["C1"], rec["K"], rec["S1"], rec["E"]
    a1, A = rec.get("A1_beside", {}), rec.get("A_beside", {})
    return (f"  {name:24s} n MP {n.get('MP'):>3} MM {n.get('MM'):>3} | C1 gap {c1['gap']} {ci(c1['gap_ci'])} {'ok' if c1['met'] else 'no'} | keepA rescue "
            f"{k['keepA_rescue']} {ci(k['keepA_rescue_ci'])} K {'ok' if k['met'] else 'no'} | S1 {s1.get('value')} {ci(s1.get('ci'))} {'ok' if s1['met'] else 'no'} | "
            + " ".join(f"E{kk} {e[f'K{kk}']['rescue_A_minus_RE']} {ci(e[f'K{kk}']['ci'])}" for kk in DOSES)
            + f" {'ok' if e['met'] else 'no'} | A1 ansJ gap {a1.get('ansJ_gap')} ansRe gap {a1.get('ansRe_gap')} | A rank {A.get('rank_A_median')} E_A {A.get('E_A_mean')}")  # fmt: skip


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / SET / "items.jsonl").open()}
    d = run_dir or RES / "ablate_v2" / f"{P}{SET}_ko63_cand2_v1"
    tag = P or "27b_"
    out: dict = {"prefix": P, "run": str(d)}
    if not (d / "rows.jsonl").exists():
        print(f"note 63 {tag}: {d} missing")
        return out
    acc = rows_at(d)
    keeplog = {}
    if (d / "keeplog.jsonl").exists():
        for line in (d / "keeplog.jsonl").open():
            r = json.loads(line)
            if r.get("condition") == "paper10" and r.get("kind", "clean") == "clean" and "A" in r.get("E", {}):
                keeplog[r["id"]] = (r["rank"]["A"], r["E"]["A"])
    run_ids = {i for (f, c), v in acc.items() if c == "none" for i in v}
    gw = guess_wrong(P)
    gates = {"gate": run_ids & gw, "gate pw": run_ids}  # registered gate first; the per-word gate alone beside
    out["vocab"] = {r: sorted({v for it in items.values() if it["domain"] == r and it["word"] in ("MP", "MM") for v in it["answer_vocab"]})
                    for r in NONCOUNTRY + COUNTRY}  # fmt: skip
    lines = [f"note 63 {tag}: run {d.name}; items in the run {len(run_ids)}, with the guess-wrong gate {len(run_ids & gw)}"]
    out["stored_check"] = K.stored_check(acc, f"{P}{SET}_ko_cand2_v1")
    for gname, ids in gates.items():
        dom = lambda rs, ids=ids: {i for i in ids if items[i]["domain"] in rs}  # noqa: E731
        per = {r: read(acc, items, dom((r,)), keeplog) for r in NONCOUNTRY if dom((r,))}
        pool = read(acc, items, dom(NONCOUNTRY), keeplog)
        cty = {r: read(acc, items, dom((r,)), keeplog) for r in COUNTRY if dom((r,))}
        cpool = read(acc, items, dom(COUNTRY), keeplog)
        v = verdict(per, pool)
        out[gname] = {"per_relation": per, "pool": pool, "country_type": cty, "country_pool": cpool, "verdict": v}
        lines.append(f"-- {gname} ({'registered: per-word competence + guess wrong' if gname == 'gate' else 'beside: per-word competence only'})")
        lines.append("  gated n per relation (MP / MM): " + "; ".join(f"{r} {x['n'].get('MP')}/{x['n'].get('MM')}" for r, x in {**per, **cty}.items()))
        if gname == "gate":
            for r, x in per.items():
                lines += ["reading " + s for s in lines_of(r, x, tag, x["n"].get("MM", 0) < MIN_MM)]
            lines += ["reading " + s for s in lines_of("non-country pool", pool, tag, False)]
            lines.append(f"reading note63 verdict {tag}: {v['label']!r} | " + json.dumps({kk: vv for kk, vv in v.items() if kk != "label"}))
        else:
            lines.append(f"  beside note63 verdict {tag} ({gname}): {v['label']!r} | " + json.dumps({kk: vv for kk, vv in v.items() if kk != "label"}))
        lines.append("  table (" + gname + "):")
        for r, x in per.items():
            lines.append(beside(r, x))
        lines.append(beside("non-country pool", pool))
        for r, x in cty.items():
            lines.append(beside(f"{r} (country-type)", x))
        lines.append(beside("country-type pool", cpool))
    sc = out["stored_check"]
    if not sc.get("missing"):
        lines.append(f"  stored check ({sc['stored_run']}): " + "; ".join(
            f"{c} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']} max|dlogp| {v['max_abs_dlogp']}" for c, v in sc.items() if c != "stored_run"))
    else:
        lines.append(f"  stored check: {sc['stored_run']} missing")
    od = out_dir or RES / "ablate_v2" / "nn_ko_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}note63.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="qwen35_9b_")
    ap.add_argument("--run-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()
    main(a.prefix, a.run_dir, a.out_dir)
