"""paper_ko_read60 (prereg amendment 85 note 60): outputs vs pivots on the paper's own tasks, read (CPU).

Input: one paper_ko_decomp --n60 run (ML and MH at the medium band, MH also at note 39's median-onset window "early"; PO
beside with the label-free keeps only). Analysis set (note 45's): gated items whose unedited strict first-token read is
right. Primary metric: L_X = mean over items of -(delta log p of the target's first token) under condition X (nats);
rescue_X = 1 - (L_X - L_rot) / (L_p10 - L_rot) (undefined if L_p10 <= L_rot). Top-1 K beside: K_X = (loss_X - loss_rot) /
(loss_p10 - loss_rot) on strict top-1 loss (points). Intervals: cluster bootstrap (ML relation, MH answer type, PO T's
spelled rhyme), 2000 draws, seed 0, percentile 95%, every statistic recomputed inside.
  A0: paper10 - max(rot, pcasize) >= 20 points top-1 or >= 0.5 nats, that criterion's interval above 0. Without it the
      keeps read as "which span prevents the damage", not "J-specific".
  O1 (output candidates): rescue(keepT10) >= 0.67 and rescue(keepT10) - rescue(keepRT10E) >= 0.33 with its lower end > 0.
  O2 (a non-output intermediate is needed): X = I (ML) or B (MH, each band): rescue(keep_Xperp) - rescue(keepRE_Xperp)
      >= 0.33 with its lower end > 0.
  O3 (the answer concept across languages; ML): on the items whose E is not in the clean top-10 (no E form token among
      them), rescue(keep_Eperp) - rescue(keepRE_Eperp) >= 0.33 with its lower end > 0.
  Specificity guard (ML): rescue(keep_ctl) <= rescue(keep_E) - 0.33, else "any English word of the relation rescues"
      (keep_ctl = keep_ctlE: another item's E, same relation when possible, count-matched). MH: keep_ctl (ctlB) beside.
  A reading whose statistic's interval has half-width > 0.4 is flagged "underpowered".
  PO (rhyme, beside): A0 and O1 only.
Beside: every condition's L, rescue and top-1 K; energy shares, ranks and matched prefix sizes (and whether they reached).

python scripts/paper_ko_read60.py results/paper_ko_decomp/<run> [--boot 2000]
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

from scripts.paper_ko_read import Read, f  # noqa: E402

NAN = float("nan")


class Read60(Read):
    def L(self, s, names, cond, band) -> float:
        """Mean loss in nats: -(delta log p) of the target's first token."""
        v = [-self.dlogp[(s, n, band, cond)] for n in names if (s, n, band, cond) in self.dlogp]
        return sum(v) / len(v) if v else NAN

    def rescue(self, s, names, cond, band) -> float:
        lp, lr = self.L(s, names, "paper10", band), self.L(s, names, "paper10_rot", band)
        den = lp - lr
        return 1 - (self.L(s, names, cond, band) - lr) / den if den > 0 else NAN

    def K1(self, s, names, cond, band) -> float:
        lp, lr = self.loss(s, names, "paper10", band), self.loss(s, names, "paper10_rot", band)
        den = lp - lr
        return (self.loss(s, names, cond, band) - lr) / den if den > 0 else NAN


def hw(ci: tuple) -> float:
    return (ci[2] - ci[1]) / 2 if not any(isinstance(x, float) and math.isnan(x) for x in ci) else NAN


def under(ci: tuple) -> str:
    h = hw(ci)
    return " [underpowered: CI half-width %.2f > 0.4]" % h if (not math.isnan(h) and h > 0.4) else ""


def diff_reading(R: Read60, s, names, a, b, band, label_yes: str, label_no: str) -> tuple[str, tuple]:
    d = R.boot(s, names, lambda ns: R.rescue(s, ns, a, band) - R.rescue(s, ns, b, band))
    if math.isnan(d[0]):
        return "undefined (paper10 not above its rotation in log p)", d
    return (label_yes if d[0] >= 0.33 and d[1] > 0 else label_no) + under(d), d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    R = Read60(Path(a.run_dir), a.boot)
    man = json.loads((R.dir / "manifest.json").read_text())
    check = json.loads((R.dir / "check.json").read_text())
    rows = [json.loads(x) for x in (R.dir / "rows.jsonl").read_text().splitlines() if x.strip()]
    conds_by = {}
    for r in rows:
        if r["window"] != "-":
            conds_by.setdefault((r["set"], r["window"]), [])
            if r["cond"] not in conds_by[(r["set"], r["window"])]:
                conds_by[(r["set"], r["window"])].append(r["cond"])
    res: dict = {"run": str(R.dir), "target": man["target"], "bands": man["bands"], "byte_check_all_equal": check["all_equal"], "sets": {}}
    print(f"# note 60 reading: {R.dir.name} ({man['target']}); bands {man['bands']} (early = note 39's median-onset window, MH only); "
          f"byte-identity check (paper10, rot, top3, top30 vs ablate_v2's recipe, MH): all equal {check['all_equal']}")  # fmt: skip
    for s in sorted({r["set"] for r in R.items}):
        names = R.analysis(s)
        out: dict = {"n_analysis": len(names)}
        print(f"\n## {s}: analysis n {len(names)} (gated {sum(r['eligible'] for r in R.items if r['set'] == s)})")
        for band in [b for b in man["bands"] if (s, b) in conds_by]:
            ob: dict = {}
            cs = conds_by[(s, band)]
            ob["L"] = {c: R.L(s, names, c, band) for c in cs}
            ob["rescue"] = {c: R.rescue(s, names, c, band) for c in cs}
            ob["K_top1"] = {c: R.K1(s, names, c, band) for c in cs}
            ob["loss_top1"] = {c: R.loss(s, names, c, band) for c in cs}
            print(f"  {band}: L (nats) / rescue / top-1 loss / top-1 K: " + "; ".join(
                f"{c} {ob['L'][c]:.3f}/{ob['rescue'][c]:.2f}/{ob['loss_top1'][c]:.1f}/{ob['K_top1'][c]:.2f}" for c in cs))  # fmt: skip
            a_pts = R.boot(s, names, lambda ns: R.loss(s, ns, "paper10", band) - max(R.loss(s, ns, "paper10_rot", band), R.loss(s, ns, "paper10_pcasize", band)))
            a_nat = R.boot(s, names, lambda ns: R.L(s, ns, "paper10", band) - max(R.L(s, ns, "paper10_rot", band), R.L(s, ns, "paper10_pcasize", band)))
            met = (a_pts[0] >= 20 and a_pts[1] > 0) or (a_nat[0] >= 0.5 and a_nat[1] > 0)
            ob["A0"] = {"top1_pts": a_pts, "nats": a_nat, "met": met}
            qual = "" if met else " [A0 not met: read as which span prevents the damage, not J-specific]"
            print(f"reading {s} A0 {band}: {'met' if met else 'not met'} (n {len(names)}; paper10 - max(rot, pcasize): top-1 {f(a_pts)} pts, "
                  f"log p {f(a_nat)} nats)")  # fmt: skip
            # O1
            r10 = R.boot(s, names, lambda ns: R.rescue(s, ns, "keepT10", band))
            lab, d = diff_reading(R, s, names, "keepT10", "keepRT10E", band, "x", "x")
            o1 = (not math.isnan(r10[0])) and r10[0] >= 0.67 and d[0] >= 0.33 and d[1] > 0
            o1_lab = ("the output candidates' directions carry the damage" if o1 else "not the output candidates alone") + under(d) + qual
            ob["O1"] = {"rescue_keepT10": r10, "minus_keepRT10E": d, "reading": o1_lab}
            print(f"reading {s} O1 {band}: {o1_lab} (n {len(names)}; rescue(keepT10) {f(r10)}; - rescue(keepRT10E) {f(d)}; "
                  f"onlyT10 rescue {ob['rescue'].get('onlyT10', NAN):.2f}, onlyRT10E {ob['rescue'].get('onlyRT10E', NAN):.2f})")  # fmt: skip
            if s in ("ML", "MH"):
                X = "I" if s == "ML" else "B"
                lab, d = diff_reading(R, s, names, f"keep_{X}perp", f"keepRE_{X}perp", band,
                                      f"a non-output intermediate ({X}) is needed", f"not shown that {X} is needed beyond the outputs")  # fmt: skip
                xn = [n for n in names if not R.by[(s, n)]["protected"].get(X)]
                d2 = R.boot(s, xn, lambda ns: R.rescue(s, ns, f"keep_{X}perp", band) - R.rescue(s, ns, f"keepRE_{X}perp", band))
                ob["O2"] = {"X": X, "diff": d, "reading": lab + qual, f"diff_{X}_not_in_top10": {"n": len(xn), "diff": d2}}
                print(f"reading {s} O2 {band}: {lab}{qual} (n {len(names)}; rescue(keep_{X}perp) - rescue(keepRE_{X}perp) {f(d)}; "
                      f"rescue keep_{X} {ob['rescue'].get('keep_' + X, NAN):.2f}, keep_{X}perp {ob['rescue'].get('keep_' + X + 'perp', NAN):.2f}; "
                      f"beside, {X} not in the clean top-10: n {len(xn)} {f(d2)})")  # fmt: skip
            if s == "ML":
                en = [n for n in names if not R.by[(s, n)]["protected"].get("E")]
                lab, d = diff_reading(R, s, en, "keep_Eperp", "keepRE_Eperp", band,
                                      "the answer concept across languages is needed", "not shown")  # fmt: skip
                ob["O3"] = {"n": len(en), "diff": d, "reading": lab + qual}
                print(f"reading ML O3 {band}: {lab}{qual} (n {len(en)} with E not in the clean top-10; rescue(keep_Eperp) - "
                      f"rescue(keepRE_Eperp) {f(d)})")  # fmt: skip
                g = R.boot(s, names, lambda ns: R.rescue(s, ns, "keep_E", band) - R.rescue(s, ns, "keep_ctl", band))
                ok = not math.isnan(g[0]) and g[0] >= 0.33
                glab = ("specific: the item's own English word rescues more than another English word of the relation" if ok
                        else "any English word of the relation rescues") + under(g)  # fmt: skip
                ob["guard"] = {"E_minus_ctlE": g, "reading": glab}
                print(f"reading ML guard {band}: {glab} (n {len(names)}; rescue(keep_E) {ob['rescue'].get('keep_E', NAN):.2f} - "
                      f"rescue(keep_ctlE) {ob['rescue'].get('keep_ctl', NAN):.2f} = {f(g)})")  # fmt: skip
            if s == "MH":
                g = R.boot(s, names, lambda ns: R.rescue(s, ns, "keep_B", band) - R.rescue(s, ns, "keep_ctl", band))
                ob["ctlB"] = g
                print(f"  beside MH {band}: rescue(keep_B) - rescue(keep_ctlB) {f(g)}")
            # logs: energy shares, ranks, matched prefixes
            logs = [R.by[(s, n)].get("n60", {}).get(band) for n in names]
            logs = [x for x in logs if x]
            if logs:
                med = lambda xs: statistics.median(xs) if xs else NAN  # noqa: E731
                Ek = sorted({k for x in logs for k in x["E"]})
                print(f"  {s} {band} energy shares of paper10's removal (median): " + ", ".join(
                    f"{k} {med([x['E'][k] for x in logs if x['E'].get(k) is not None]):.3f}" for k in Ek)
                    + "; ranks (median): " + ", ".join(f"{k} {med([x['rank'][k] for x in logs])}" for k in sorted(logs[0]["rank"]))
                    + "; matched prefix k (median) / reached: " + ", ".join(
                        f"{k} {med([x['k'][k] for x in logs])}/{sum(x['reached'][k] for x in logs)}of{len(logs)}" for k in sorted(logs[0]["k"])))  # fmt: skip
            out[band] = ob
        res["sets"][s] = out
    er = {}
    for r in rows:
        if "edit_rel" in r:
            er.setdefault(f"{r['set']}/{r['window']}/{r['cond']}", []).append(r["edit_rel"])
    print("  |edit| / |h| (mean): " + json.dumps({k: round(statistics.mean(v), 4) for k, v in sorted(er.items())}))
    (R.dir / "reading60.json").write_text(json.dumps(res, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
