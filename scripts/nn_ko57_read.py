"""nn_ko57_read (Zach, 2026-10-30, prereg amendment 78 note 57): the controls the 9B's mechanism claims lacked, read (CPU).

Run (scripts/queues/h200_n57_1030.sh): {P}jsuite_v4_test_chat_ko57_cand2_v1 (9B, v4 draw 4001, note 49's settings: note 20's gate,
band and batch, every position) under paper10, paper10_rot, paper10_onlyA, paper10_onlyRperp, top30, top30_keepA, top30_keepRE,
top100, top100_keepA, top100_keepRE, ansJ, ansRe, paper10_keepRivals, paper10_keepRandRivals (each + _rot). n57_log.jsonl: the
energy-matched sizes (onlyRperp's in paper10's forward, keepRE's in topK's, ansRe's in ansJ's); n57_rows.jsonl: the rivals.
Measures: nn_ko37_read's (loss, gap, bridge bootstrap: 2000 draws, random.Random(0), every gated item of a bridge together).
Readings (9B; MM):
  S1: [(onlyA - onlyA_rot) - (onlyRperp - onlyRperp_rot)] MM loss >= 1/3 of (paper10 - paper10_rot), with the interval's lower end
      > 0: "sufficiency is answer-specific"; otherwise "sufficiency not shown specific".
  D1 (each K): rescue(topK_keepA) - rescue(topK_keepRE) >= 0.33 with the lower end > 0, rescue(X) = 1 - (X - X_rot) / (topK -
      topK_rot): "answer-specific at dose K"; otherwise "not shown at dose K".
  A1: ansRe's gap <= 1/3 of ansJ's (joint bridge bootstrap beside): "answer-specific removal at matched energy"; otherwise "not
      answer-specific at matched energy" ("not read" if ansJ's gap <= 0).
  T1 (descriptive): on MM items with at least one rival, the share whose output (the cand2 pick) is a kept rival under keepRivals,
      against the share whose output is a kept random answer under keepRandRivals; the gold answer's survival under each (and
      under paper10 and unedited, beside).
Writes results/ablate_v2/nn_ko_read/{P}note57.json (or --out-dir) and prints one "reading ..." line per registered reading.

python scripts/nn_ko57_read.py PREFIX [--run-dir DIR] [--out-dir DIR]
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
from scripts.nn_ko41_read import gap_ratio  # noqa: E402
from scripts.nn_ko49_read import rows_at, units  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
SET = "jsuite_v4_test_chat"
DOSES = (30, 100)
CONDS = (("paper10", "paper10_rot") + tuple(f"paper10_{x}{s}" for x in ("onlyA", "onlyRperp", "keepRivals", "keepRandRivals") for s in ("", "_rot"))
         + tuple(f"top{k}{s}" for k in DOSES for s in ("", "_rot", "_keepA", "_keepA_rot", "_keepRE", "_keepRE_rot"))
         + ("ansJ", "ansJ_rot", "ansRe", "ansRe_rot"))  # fmt: skip


def contrast(acc, items, a: tuple, b: tuple, base: tuple) -> dict:
    """[(a0 - a1) - (b0 - b1)] / (base0 - base1) over MM items, with its bridge bootstrap; also the numerator in points."""
    by = units(acc, items, a + b + base)

    def fn(us):
        den = sum(u[4] - u[5] for u in us)
        return (sum(u[0] - u[1] for u in us) - sum(u[2] - u[3] for u in us)) / den if den > 0 else float("nan")

    def pts(us):
        return 100 * (sum(u[0] - u[1] for u in us) - sum(u[2] - u[3] for u in us)) / len(us)

    us = [u for v in by.values() for u in v]
    if not us:
        return {}
    v = fn(us)
    ci = K.boot(by, lambda xs: 100 * fn(xs))
    return {"n_MM": len(us), "value": round(v, 3) if v == v else None, "ci": [x / 100 for x in ci] if ci else None,
            "points": round(pts(us), 1), "points_ci": K.boot(by, pts), "den_points": round(100 * sum(u[4] - u[5] for u in us) / len(us), 1)}  # fmt: skip


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / SET / "items.jsonl").open()}
    d = run_dir or RES / "ablate_v2" / f"{P}{SET}_ko57_cand2_v1"
    out: dict = {"prefix": P, "run": str(d)}
    if not (d / "rows.jsonl").exists():
        print(f"note 57 {P or '27b_'}: {d} missing")
        return out
    acc = rows_at(d)
    m = K.measures(acc, items, lambda it: True, CONDS)
    cs = m["conditions"]
    out["measures"] = m
    out["stored_check"] = K.stored_check(acc, f"{P}{SET}_ko41_cand2_v1")
    tag = P or "27b_"
    lines = K.table(f"note 57 {tag}", m)
    R: dict = {}
    s1 = contrast(acc, items, ("paper10_onlyA", "paper10_onlyA_rot"), ("paper10_onlyRperp", "paper10_onlyRperp_rot"), ("paper10", "paper10_rot"))
    met = s1.get("value") is not None and s1["value"] >= 1 / 3 and s1["ci"] and s1["ci"][0] > 0
    R["S1"] = {"label": ("not read: paper10 - paper10_rot <= 0" if s1.get("value") is None else "sufficiency is answer-specific" if met
                         else "sufficiency not shown specific"), **s1}  # fmt: skip
    for k in DOSES:
        # rescue(A) - rescue(RE) = ratio(RE) - ratio(A): the contrast with a = RE, b = A
        dk = contrast(acc, items, (f"top{k}_keepRE", f"top{k}_keepRE_rot"), (f"top{k}_keepA", f"top{k}_keepA_rot"), (f"top{k}", f"top{k}_rot"))
        met = dk.get("value") is not None and dk["value"] >= 0.33 and dk["ci"] and dk["ci"][0] > 0
        R[f"D1_K{k}"] = {"label": (f"not read: top{k} - top{k}_rot <= 0" if dk.get("value") is None else f"answer-specific at dose {k}" if met
                                   else f"not shown at dose {k}"), "rescue_A_minus_RE": dk.get("value"), "ci": dk.get("ci"), "n_MM": dk.get("n_MM")}  # fmt: skip
    if "ansRe" in cs and "ansJ" in cs:
        gJ, gE = cs["ansJ"]["gap"], cs["ansRe"]["gap"]
        rr = gap_ratio(acc, acc, items, "ansRe", "ansJ")
        R["A1"] = {"label": ("not read: ansJ's gap <= 0" if gJ <= 0 else "answer-specific removal at matched energy" if gE <= gJ / 3
                             else "not answer-specific at matched energy"), "ansRe_gap": gE, "ansRe_gap_ci": cs["ansRe"]["gap_ci"],
                   "ansJ_gap": gJ, "ansJ_gap_ci": cs["ansJ"]["gap_ci"], "ratio": rr["ratio"], "ratio_ci": rr["ratio_ci"],
                   "ansRe_rot_gap": cs.get("ansRe_rot", {}).get("gap"), "ansJ_rot_gap": cs.get("ansJ_rot", {}).get("gap")}  # fmt: skip
    # T1 (descriptive)
    riv = {json.loads(l)["id"]: json.loads(l) for l in (d / "n57_rows.jsonl").open()} if (d / "n57_rows.jsonl").exists() else {}
    raw = collections.defaultdict(dict)
    for line in (d / "rows.jsonl").open():
        r = json.loads(line)
        if r["family"] == "MM" and r.get("kind", "clean") == "clean":
            raw[r["condition"]][r["id"]] = r
    ids = [i for i in raw.get("none", {}) if riv.get(i, {}).get("riv")]
    t1 = {"n_MM_with_rivals": len(ids), "n_MM": len(raw.get("none", {}))}
    for c in ("none", "paper10", "paper10_keepRivals", "paper10_keepRandRivals"):
        if c not in raw:
            continue
        by = collections.defaultdict(list)
        for i in ids:
            if i in raw[c]:
                r = raw[c][i]
                by[items[i]["bridge"]].append((r["pick2"] in riv[i]["riv_tok"], r["pick2"] in riv[i]["rand_tok"], bool(r["correct_cand2"])))
        us = [u for v in by.values() for u in v]
        if not us:
            continue
        f = lambda j: (lambda xs: 100 * sum(x[j] for x in xs) / len(xs))  # noqa: E731
        t1[c] = {"n": len(us), "says_rival": round(f(0)(us), 1), "says_rival_ci": K.boot(by, f(0)), "says_rand_answer": round(f(1)(us), 1),
                 "says_rand_answer_ci": K.boot(by, f(1)), "gold_survives": round(f(2)(us), 1), "gold_survives_ci": K.boot(by, f(2))}  # fmt: skip
    R["T1"] = {"label": "descriptive", **t1}
    out["readings"] = R
    lg = [json.loads(l) for l in (d / "n57_log.jsonl").open()] if (d / "n57_log.jsonl").exists() else []
    out["matching"] = {}
    for fw in sorted({x["forward"] for x in lg}):
        v = [x for x in lg if x["forward"] == fw and x["family"] == "MM"]
        if v:
            out["matching"][fw] = {"n": len(v), "reached_share": round(sum(x["reached"] for x in v) / len(v), 3),
                                   "k_mean": round(sum(x["k"] for x in v) / len(v), 1), "E_target_mean": round(sum(x["E_target"] for x in v) / len(v), 4),
                                   "E_match_mean": round(sum(x["E_match"] for x in v) / len(v), 4)}  # fmt: skip
    for k, v in R.items():
        lines.append(f"reading note57 {k} {tag}: {v['label']!r} | " + json.dumps({kk: vv for kk, vv in v.items() if kk != "label"})[:700])
    lines.append(f"  energy matching (MM): {json.dumps(out['matching'])}")
    sc = out["stored_check"]
    if not sc.get("missing"):
        lines.append(f"  stored check ({sc['stored_run']}): " + "; ".join(
            f"{c} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']}" for c, v in sc.items() if c != "stored_run"))
    od = out_dir or RES / "ablate_v2" / "nn_ko_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}note57.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="qwen35_9b_")
    ap.add_argument("--run-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()
    main(a.prefix, a.run_dir, a.out_dir)
