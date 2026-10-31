"""nn_ko41_read (Zach, 2026-10-30, prereg amendment 67 note 41 and its addendum): note 37's random-span placebo and its
output-side check, read (CPU).

Runs (scripts/queues/h200_n41_1030.sh), per model prefix P:
  {P}jsuite_v4_test_chat_ko41_cand2_v1           paper10, paper10_rot, paper10_keepR / R2 / R4 (+ _rot), ansR, ansR_rot (note 20's
                                                 gate, band and batch). Its paper10 rows carry "retained": the share of paper10's
                                                 removal energy lying in A, R, R2 and R4, summed over the edited positions and the
                                                 band's layers (sum |P_X r|^2 / sum |r|^2 per item).
  {P}jsuite_v4_test_chat_ko41_posfinal_cand2_v1  --positions final: paper10, paper10_rot, ansJ, ansJ_rot
  {P}jsuite_v4_test_chat_ko37_cand2_v1           note 37's stored run (keepA, keepA_rot, ansJ at every position, its paper10)
Measures: scripts/nn_ko37_read.measures (loss over the gated items, gap with the bridge bootstrap, paired twins, dlogp).
  ratio_X = MM's (keepX - keepX_rot) loss / MM's (paper10 - paper10_rot) loss, each within its own run (A: note 37's run; R,
  R2, R4: this run), with a bridge bootstrap. Retained energy E_X = the mean over MM's gated items of the per-item share
  (the energy-weighted pooled share and MP's mean beside).
Readings (per model):
  keep (the addendum's primary rule, replacing note 41's keepR rule): X* = the random keep with E_X >= E_A closest to E_A.
    "answer-specific keep" if ratio_X* >= 2/3 while ratio_A <= 1/3; else "energy, not answers" if a random keep with
    E_X <= E_A has ratio_X <= 1/3; otherwise "partly" ("not read" if MM's paper10 - paper10_rot loss is <= 0 in either run).
    Note 41's original keepR rule is reported beside (replaced).
  removal: "answer-specific removal" if ansR's gap <= 1/3 of ansJ's (note 37's run); otherwise "not answer-specific".
  output side: ansJ's final-only gap / its all-position gap (note 37's run): "largely output-side" if >= 1/2, "upstream" if
    <= 1/4, otherwise "mixed". Gap ratios carry a joint bootstrap over bridges (both runs' items of a bridge drawn together).
  ("not read" when the denominator gap is <= 0.)
Descriptive: rescue (1 - ratio) against retained energy, A vs R, R2, R4.
Checks: this run's none / paper10 / paper10_rot rows against note 37's run; the final-only run's against note 33's
  ({P}jsuite_v4_test_chat_ko_posfinal_cand2_v1).
Writes results/ablate_v2/nn_ko_read/{P}note41.json and prints a table.

--matched-energy (amendment 70; registered secondaries beside the keep reading, which stays the primary; post hoc on seed 4001,
  i.e. the default v4 set): Rule E: R_rand(E_A) = the accuracy rescue of keepR, keepR2, keepR4 (each net of its _rot, as above)
  linearly interpolated in retained energy (MM's mean per-item share, as above) at E_A, keepA's share; "not interpolable" if
  E_A lies outside the random keeps' range (no extrapolation). "answer-specific at matched energy" if rescue(keepA) -
  R_rand(E_A) >= 0.33 with the bootstrap's lower end > 0 (note 41's bridge bootstrap, 2000 draws, random.Random(0); rescues,
  energies and the interpolation recomputed per resample; resamples where E_A falls outside the range are dropped and counted);
  otherwise "not shown at matched energy". Rule L: the same with rescue_L(X) = 1 - (mean dlogp under X - mean dlogp under
  X_rot) / (mean dlogp under paper10 - mean dlogp under paper10_rot), dlogp = the drop in the gold answer's first-token log p
  (the rows' "logp") on MM items. Adds "matched_energy" to the JSON. Without the flag the output is unchanged.

python scripts/nn_ko41_read.py PREFIX      (PREFIX "" for the 27B, qwen35_9b_ for the 9B, nem35l_ for Lightning)
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
SET = "jsuite_v4_test_chat"
CONDS_A = ("paper10", "paper10_rot", "paper10_keepR", "paper10_keepR_rot", "paper10_keepR2", "paper10_keepR2_rot",
           "paper10_keepR4", "paper10_keepR4_rot", "ansR", "ansR_rot")  # fmt: skip
CONDS_B = ("paper10", "paper10_rot", "ansJ", "ansJ_rot")
RANDOM = ("R", "R2", "R4")


def keep_ratio(acc: dict, items: dict, x: str) -> dict:
    """MM's net loss under paper10_keepX as a share of paper10's net loss, within one run, with its bridge bootstrap."""
    conds = (f"paper10_keep{x}", f"paper10_keep{x}_rot", "paper10", "paper10_rot")
    if not all(("MM", c) in acc for c in conds):
        return {}
    by = collections.defaultdict(list)
    for i, (ok, _) in acc[("MM", "none")].items():
        if all(i in acc[("MM", c)] for c in conds):
            by[items[i]["bridge"]].append(tuple(int(ok) - int(acc[("MM", c)][i][0]) for c in conds))
    us = [u for v in by.values() for u in v]
    r = K.ratio_fn(us)
    ci = K.boot(by, lambda xs: 100 * K.ratio_fn(xs))
    n = len(us)
    return {"n_MM": n, "net_keep": round(100 * sum(u[0] - u[1] for u in us) / n, 1), "net_paper10": round(100 * sum(u[2] - u[3] for u in us) / n, 1),
            "ratio": round(r, 3) if r == r else None, "ratio_ci": [x / 100 for x in ci] if ci else None,
            "rescue": round(1 - r, 3) if r == r else None}  # fmt: skip


def retained(run: str, acc: dict) -> dict:
    """Per twin: the mean per-item retained share of paper10's removal energy in A, R, R2, R4 (gated items), and the pooled
    (energy-weighted) share."""
    per = {}
    for line in (RES / "ablate_v2" / run / "rows.jsonl").open():
        r = json.loads(line)
        if r["condition"] == "paper10" and "retained" in r:
            per[(r["family"], r["id"])] = r["retained"]
    out = {}
    for f in ("MM", "MP"):
        rs = [per[(f, i)] for i in acc.get((f, "none"), {}) if (f, i) in per and per[(f, i)]["energy"] > 0]
        if not rs:
            continue
        tot = sum(x["energy"] for x in rs)
        out[f] = {"n": len(rs), **{k: round(sum(x[k] for x in rs) / len(rs), 4) for k in ("A",) + RANDOM},
                  "pooled": {k: round(sum(x[k] * x["energy"] for x in rs) / tot, 4) for k in ("A",) + RANDOM}}  # fmt: skip
    return out


def gap_ratio(num: dict, den: dict, items: dict, cond_num: str, cond_den: str) -> dict:
    """gap(num run, cond_num) / gap(den run, cond_den), each over its gated items, with a joint bootstrap over bridges."""
    by = collections.defaultdict(list)
    for src, acc, c in (("num", num, cond_num), ("den", den, cond_den)):
        for f in ("MM", "MP"):
            for i, (ok, _) in acc.get((f, "none"), {}).items():
                if i in acc.get((f, c), {}):
                    by[items[i]["bridge"]].append((src, f, int(ok) - int(acc[(f, c)][i][0])))

    def fn(us):
        g = {s: K.gap_fn([(f, x) for t, f, x in us if t == s]) for s in ("num", "den")}
        return g["num"] / g["den"] if g["den"] > 0 else float("nan")

    us = [u for v in by.values() for u in v]
    v = fn(us)
    ci = K.boot(by, lambda xs: 100 * fn(xs))
    return {"ratio": round(v, 3) if v == v else None, "ratio_ci": [x / 100 for x in ci] if ci else None}


def interp(pts: list, x: float) -> float:
    """Piecewise-linear interpolation of (E, rescue) points at x; nan outside the points' range (no extrapolation)."""
    pts = sorted(pts)
    if not pts or any(v != v for p in pts for v in p) or x != x or x < pts[0][0] or x > pts[-1][0]:
        return float("nan")
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[0][1]  # a single point equal to x


def matched_energy(acc: dict, items: dict, runs: dict, set_name: str) -> tuple[dict, list[str]]:
    """Amendment 70's Rules E (accuracy) and L (gold first-token log p): keepA's rescue against the random keeps' rescue
    interpolated at keepA's retained energy, with note 41's bridge bootstrap (interpolation recomputed per resample)."""
    status = "post hoc on seed 4001" if set_name == SET else "registered secondary"
    head = f"(amendment 70, {status}, beside the keep reading)"
    if "A" not in acc or "n37" not in acc:
        return {"reading_E": "not read: a run is missing", "reading_L": "not read: a run is missing"}, [
            f"  reading E matched energy {head}: not read: a run is missing", f"  reading L log-prob {head}: not read: a run is missing"]
    ret = {}
    for line in (RES / "ablate_v2" / runs["A"] / "rows.jsonl").open():
        r = json.loads(line)
        if r["condition"] == "paper10" and "retained" in r and r["family"] == "MM" and r.get("kind", "clean") == "clean":
            ret[r["id"]] = r["retained"]
    src = {"A": acc["n37"], **{x: acc["A"] for x in RANDOM}}
    rec: dict = collections.defaultdict(dict)  # MM id -> {X: ((accuracy losses), (logp drops) or None), "E": retained}
    for x, a in src.items():
        conds = (f"paper10_keep{x}", f"paper10_keep{x}_rot", "paper10", "paper10_rot")
        if not all(("MM", c) in a for c in conds):
            continue
        for i, (ok, lp) in a[("MM", "none")].items():
            if all(i in a[("MM", c)] for c in conds):
                ls = tuple(int(ok) - int(a[("MM", c)][i][0]) for c in conds)
                ok_lp = lp is not None and all(a[("MM", c)][i][1] is not None for c in conds)
                rec[i][x] = (ls, tuple(lp - a[("MM", c)][i][1] for c in conds) if ok_lp else None)
    for i in acc["A"].get(("MM", "none"), {}):
        if i in ret and ret[i]["energy"] > 0:
            rec[i]["E"] = ret[i]
    by = collections.defaultdict(list)
    for i, v in rec.items():
        by[items[i]["bridge"]].append(v)

    def stats(rs: list) -> dict:
        s: dict = {}
        es = [v["E"] for v in rs if "E" in v]
        for x in ("A",) + RANDOM:
            us = [v[x] for v in rs if x in v]
            den = sum(u[0][2] - u[0][3] for u in us)
            s[("acc", x)] = 1 - sum(u[0][0] - u[0][1] for u in us) / den if us and den > 0 else float("nan")
            ul = [u[1] for u in us if u[1] is not None]
            m = [sum(u[j] for u in ul) / len(ul) for j in range(4)] if ul else None
            s[("lp", x)] = 1 - (m[0] - m[1]) / (m[2] - m[3]) if m and m[2] - m[3] > 0 else float("nan")
            s[("E", x)] = sum(e[x] for e in es) / len(es) if es else float("nan")
        for k in ("acc", "lp"):
            s[(k, "rand")] = interp([(s[("E", x)], s[(k, x)]) for x in RANDOM], s[("E", "A")])
            s[(k, "diff")] = s[(k, "A")] - s[(k, "rand")]
        return s

    us = [v for b in by.values() for v in b]
    pt = stats(us)
    n_boot, keys, rng = 2000, sorted(by), random.Random(0)
    draws: dict = {"acc": [], "lp": []}
    dropped = {"acc": 0, "lp": 0}
    for _ in range(n_boot):  # note 41's bootstrap (nn_ko37_read.boot): bridges drawn with replacement, random.Random(0)
        s = stats([u for k in (rng.choice(keys) for _ in keys) for u in by[k]])
        for k in ("acc", "lp"):
            if s[(k, "diff")] == s[(k, "diff")]:
                draws[k].append(s[(k, "diff")])
            else:
                dropped[k] += 1
    out: dict = {"status": status, "n_MM": {x: sum(1 for v in us if x in v) for x in ("A",) + RANDOM},
                 "n_MM_energy": sum(1 for v in us if "E" in v), "n_boot": n_boot}  # fmt: skip
    lines = []
    rnd = lambda v: round(v, 4) if v == v else None  # noqa: E731
    f3 = lambda v: f"{v:.3f}" if v == v else "nan"  # noqa: E731
    for k, rule, name in (("acc", "E", "matched energy (accuracy)"), ("lp", "L", "log-prob (gold first-token log p, MM)")):
        d = sorted(draws[k])
        ci = [d[int(0.025 * len(d))], d[int(0.975 * len(d)) - 1]] if d else None
        es = {x: pt[("E", x)] for x in ("A",) + RANDOM}
        rs = {x: pt[(k, x)] for x in ("A",) + RANDOM}
        if any(v != v for v in list(es.values()) + list(rs.values())):
            lab = "not read: a rescue is undefined (paper10 - paper10_rot <= 0) or no retained energy"
        elif es["A"] < min(es[x] for x in RANDOM) or es["A"] > max(es[x] for x in RANDOM):
            lab = "not interpolable"
        elif pt[(k, "diff")] >= 0.33 and ci is not None and ci[0] > 0:
            lab = "answer-specific at matched energy"
        else:
            lab = "not shown at matched energy"
        out[f"rule_{rule}"] = {"E": {x: rnd(v) for x, v in es.items()}, "rescue": {x: rnd(v) for x, v in rs.items()},
                               "R_rand_at_E_A": rnd(pt[(k, "rand")]), "diff": rnd(pt[(k, "diff")]),
                               "diff_ci": [round(v, 4) for v in ci] if ci else None, "boot_dropped": dropped[k], "reading": lab}  # fmt: skip
        lines.append(f"  reading {rule} {name} {head}: n MM {out['n_MM']['A']} (A) / {out['n_MM']['R']} (R), E_A {f3(es['A'])}, rescue A "
                     f"{f3(rs['A'])}; " + ", ".join(f"{x} E {f3(es[x])} rescue {f3(rs[x])}" for x in RANDOM)
                     + f"; R_rand(E_A) {f3(pt[(k, 'rand')])}; A - R_rand {f3(pt[(k, 'diff')])} "
                     + (f"[{ci[0]:.3f}, {ci[1]:.3f}]" if ci else "[no CI]") + f" ({n_boot} draws, {dropped[k]} dropped) -> {lab}")  # fmt: skip
    return out, lines


def main(P: str, set_name: str = SET, run_a: str | None = None, run_n37: str | None = None, matched: bool = False) -> dict:
    """Defaults: note 41 on v4. Amendment 68 note 43: set_name (another v4-format set) and run_a / run_n37 (both may name one
    run holding note 37's and note 41's conditions); written to {P}{set}_note41.json when set_name is not v4's."""
    items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / set_name / "items.jsonl").open()}
    runs = {"A": run_a or f"{P}{set_name}_ko41_cand2_v1", "B": f"{P}{set_name}_ko41_posfinal_cand2_v1",
            "n37": run_n37 or f"{P}{set_name}_ko37_cand2_v1"}  # fmt: skip
    out: dict = {"prefix": P, "runs": runs, **({"set": set_name} if set_name != SET else {})}
    miss = [k for k, r in runs.items() if not (RES / "ablate_v2" / r / "rows.jsonl").exists()]
    if miss:
        out["missing"] = [runs[k] for k in miss]
        print(f"note 41 {P or '27b_'}: missing {out['missing']}")
    acc = {k: K.rows_of(r) for k, r in runs.items() if k not in miss}
    every = lambda it: True  # noqa: E731
    lines = []
    if "A" in acc:
        out["A"] = K.measures(acc["A"], items, every, CONDS_A)
        out["A"]["stored_check"] = K.stored_check(acc["A"], runs["n37"]) if runs["A"] != runs["n37"] else {"same_run": runs["A"]}
        lines += K.table(f"note 41 run A {P or '27b_'}", out["A"])
    if "B" in acc:
        out["B"] = K.measures(acc["B"], items, every, CONDS_B)
        out["B"]["stored_check"] = K.stored_check(acc["B"], f"{P}{set_name}_ko_posfinal_cand2_v1")
        lines += K.table(f"note 41 run B (final token only) {P or '27b_'}", out["B"])
    if "n37" in acc:
        out["n37"] = K.measures(acc["n37"], items, every)
    # keep: rescue against retained energy
    if "A" in acc and "n37" in acc:
        E = retained(runs["A"], acc["A"])
        keep = {"A": keep_ratio(acc["n37"], items, "A"), **{x: keep_ratio(acc["A"], items, x) for x in RANDOM}}
        e = E.get("MM", {})
        table = {x: {"retained_MM": e.get(x), "retained_MM_pooled": e.get("pooled", {}).get(x), "retained_MP": E.get("MP", {}).get(x), **keep[x]}
                 for x in ("A",) + RANDOM}  # fmt: skip
        out["keep"] = {"table": table, "retained": E}
        rA = keep["A"].get("ratio")
        rx = {x: keep[x].get("ratio") for x in RANDOM}
        if rA is None or any(v is None for v in rx.values()) or e.get("A") is None:
            out["keep"]["reading"] = "not read: a ratio is undefined (MM's paper10 - paper10_rot loss <= 0) or no retained energy"
        else:
            above = [x for x in RANDOM if e[x] >= e["A"]]
            star = min(above, key=lambda x: e[x] - e["A"]) if above else None
            specific = star is not None and rx[star] >= 2 / 3 and rA <= 1 / 3
            energy = [x for x in RANDOM if e[x] <= e["A"] and rx[x] <= 1 / 3]
            out["keep"].update({"matched_random_keep": star, "answer_specific_met": specific, "energy_not_answers_keeps": energy,
                                "reading": "answer-specific keep" if specific else "energy, not answers" if energy else "partly"})  # fmt: skip
            orig = ("answer-specific keep" if rx["R"] >= 2 / 3 and rA <= 1 / 3 else
                    "size, not answers" if rx["R"] <= 1 / 3 and rA <= 1 / 3 else "partly")  # fmt: skip
            out["keep"]["note41_original_keepR_rule_replaced"] = orig
        lines.append("  rescue vs retained energy (MM): " + "; ".join(
            f"{x}: E {t['retained_MM']} ratio {t.get('ratio')} {t.get('ratio_ci')} rescue {t.get('rescue')}" for x, t in table.items()))
        lines.append(f"  keep reading: {out['keep'].get('reading')} (matched random keep {out['keep'].get('matched_random_keep')}; "
                     f"note 41's original keepR rule, replaced: {out['keep'].get('note41_original_keepR_rule_replaced')})")  # fmt: skip
    me = None
    if matched:  # amendment 70: Rules E and L beside the keep reading
        me, me_lines = matched_energy(acc, items, runs, set_name)
        lines += me_lines
    # removal: ansR's gap against ansJ's (note 37's run)
    if "A" in acc and "n37" in acc and "ansR" in out["A"]["conditions"] and "ansJ" in out["n37"]["conditions"]:
        gR, gJ = out["A"]["conditions"]["ansR"]["gap"], out["n37"]["conditions"]["ansJ"]["gap"]
        rr = gap_ratio(acc["A"], acc["n37"], items, "ansR", "ansJ")
        out["removal"] = {"ansR_gap": gR, "ansR_gap_ci": out["A"]["conditions"]["ansR"]["gap_ci"], "ansJ_gap": gJ,
                          "ansJ_gap_ci": out["n37"]["conditions"]["ansJ"]["gap_ci"], **rr,
                          "reading": ("not read: ansJ's gap <= 0" if gJ <= 0 else "answer-specific removal" if gR <= gJ / 3
                                      else "not answer-specific")}  # fmt: skip
        lines.append(f"  removal: ansR gap {gR} vs ansJ gap {gJ} (ratio {rr['ratio']} {rr['ratio_ci']}) -> {out['removal']['reading']}")
    # output side: ansJ at the final token only against every position
    if "B" in acc and "n37" in acc and "ansJ" in out["B"]["conditions"] and "ansJ" in out["n37"]["conditions"]:
        gF, gJ = out["B"]["conditions"]["ansJ"]["gap"], out["n37"]["conditions"]["ansJ"]["gap"]
        rr = gap_ratio(acc["B"], acc["n37"], items, "ansJ", "ansJ")
        v = gF / gJ if gJ > 0 else None
        out["output_side"] = {"ansJ_final_gap": gF, "ansJ_final_gap_ci": out["B"]["conditions"]["ansJ"]["gap_ci"], "ansJ_all_gap": gJ,
                              "share": round(v, 3) if v is not None else None, "share_ci": rr["ratio_ci"],
                              "reading": ("not read: ansJ's all-position gap <= 0" if v is None else "largely output-side" if v >= 0.5
                                          else "upstream" if v <= 0.25 else "mixed")}  # fmt: skip
        lines.append(f"  output side: ansJ final-only gap {gF} / all-position gap {gJ} = {out['output_side']['share']} {rr['ratio_ci']} -> {out['output_side']['reading']}")
    for k in ("A", "B"):
        sc = out.get(k, {}).get("stored_check")
        if sc and not sc.get("missing") and not sc.get("same_run"):
            lines.append(f"  run {k} stored check ({sc['stored_run']}): " + "; ".join(
                f"{c} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']}" for c, v in sc.items() if c != "stored_run"))
    if me is not None:
        out["matched_energy"] = me
    d = RES / "ablate_v2" / "nn_ko_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / (f"{P}note41.json" if set_name == SET else f"{P}{set_name}_note41.json")).write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--set", default=SET, help="note 43: another v4-format set")
    ap.add_argument("--run-a", default=None, help="the run with note 41's conditions (default {P}{set}_ko41_cand2_v1)")
    ap.add_argument("--run-n37", default=None, help="the run with note 37's conditions (default {P}{set}_ko37_cand2_v1)")
    ap.add_argument("--matched-energy", action="store_true", help="amendment 70: Rules E (matched energy) and L (log-prob) beside the keep reading")
    a = ap.parse_args()
    main(a.prefix, a.set, a.run_a, a.run_n37, a.matched_energy)
