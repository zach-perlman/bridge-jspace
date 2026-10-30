"""paper_ko_read55 (prereg amendment 72 note 55): the paper's strengths, matched for generic damage, read (CPU).

Inputs: one paper_ko_decomp --bands run (the paper's sets ML, MH, OO, PO at its medium and heavy strengths, and the text
stage's text_rows.jsonl), and optionally the model's v4 run of ablate_v2 at the same bands (--v4 RUN).
Task loss (note 45's): the share of the analysis items (gated, unedited strict first-token read right) whose read is wrong
under a condition, in points. Text agreement: plain-text top-1 agreement with the clean model, pooled over the scored
positions of a text set (WikiText primary, v4 passages beside).
Readings:
  G (descriptive): paper10's and paper10_rot's WikiText agreement at medium and heavy against the paper's Fig. 22 values
    (J ablation 0.75 at medium, 0.65 at heavy; its random control 0.96 at medium).
  S (primary; per set and strength; OO descriptive): a* = paper10's agreement; L_PCA(a*) = task loss interpolated linearly
    in agreement between the two PCA dose points (pca3, pca10, pca30) that bracket a*; Delta_sel = L(paper10) - L_PCA(a*),
    cluster bootstrap (note 45's clusters; PO: T's spelled rhyme; 2000 draws, seed 0) with the interpolation inside (the
    text agreements are fixed). "J-selective at matched generic damage" Delta_sel >= 15 with the interval above 0; "not
    selective" Delta_sel < 10 and the interval includes 0; otherwise "partly"; "not matched" if the PCA points do not
    bracket a* (the nearest point is printed, no reading). Beside: the same against the logit-lens dose (unembed10,
    unembed30), the paper's own contrast paper10 - paper10_rot, and the v4-passage agreement version.
  Rhyme (PO): note 45's A0 (paper10 - max(rot, pcasize) >= 20, interval above 0) per strength; then at the keep band
    multihop's rule with S in B's place, on the items whose S is unprotected: "the rhyme word carries it" K(T) <= 1/3 and
    K(S) >= 2/3; "the rhyme source carries it" the reverse; "both carry it" both <= 1/3; "neither" both >= 2/3; else "mixed".
  V (v4, per strength; --v4): "C1 holds at the paper's strength" if paper10's gap (MM - MP loss) >= 20 with its interval
    above 0, paper10_rot's gap <= 1/3 of it, and gap - max(paper10_pcasize gap, unembed10 gap) >= 10; note 37's keepA
    reading (scripts/nn_ko37_read.measures) at each strength.
  Beside (descriptive): note 45's keep readings at the keep band (ML: K(E), K(T); MH: K(T), K(B); its validity spans
    keepR / keep_ctl are not part of note 55), and every dose point (task loss, both agreements, |edit| / |h|).
Reads are first-token strict top-1, not the paper's generation scores.

python scripts/paper_ko_read55.py results/paper_ko_decomp/<run> [--v4 <ablate_v2 run>] [--boot 2000]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

from scripts.paper_ko_read import Read, f, label_pair  # noqa: E402

PCA = ("pca3", "pca10", "pca30")
UNEMBED = ("unembed10", "unembed30")
DOSE = ("top3", "paper10", "top30", "pca3", "pca10", "pca30", "unembed10", "unembed30", "paper10_rot", "paper10_pcasize")
PAPER_G = {"medium": 0.75, "heavy": 0.65}  # Fig. 22, pretraining top-1 match under the J ablation; random at medium 0.96
PAPER_RANDOM = 0.96
V_CONDS = ("paper10", "paper10_rot", "paper10_pcasize", "unembed10", "paper10_keepA", "paper10_keepA_rot")


def text_agreement(run_dir: Path) -> dict:
    """(textset, band, cond) -> (agreement, n texts, n positions, mean nll, mean edit_rel)."""
    p = run_dir / "text_rows.jsonl"
    if not p.exists():
        return {}
    acc: dict = collections.defaultdict(lambda: [0, 0, 0, [], []])
    for line in p.open():
        x = json.loads(line)
        a = acc[(x["textset"], x["band"], x["cond"])]
        a[0] += x["agree"]
        a[1] += x["n"]
        a[2] += 1
        a[3].append(x["nll"])
        a[4].append(x["edit_rel"])
    return {k: (v[0] / v[1], v[2], v[1], statistics.mean(v[3]), statistics.mean(v[4])) for k, v in acc.items()}


def interp(points: list[tuple[float, float]], a: float) -> float:
    """Loss at agreement a, linear between the two points that bracket it (points sorted by agreement); nan if none do."""
    pts = sorted(points)
    for (a0, l0), (a1, l1) in zip(pts, pts[1:], strict=False):
        if a0 <= a <= a1:
            return l0 if a1 == a0 else l0 + (l1 - l0) * (a - a0) / (a1 - a0)
    return math.nan


def matched(R: Read, s: str, names: list[str], band: str, agree: dict, dose: tuple, a_star: float) -> dict:
    """Delta = L(paper10) - L_dose(a*), its cluster bootstrap with the interpolation inside, or the nearest point."""
    pts_a = [(agree[c], c) for c in dose]
    lo_a, hi_a = min(x for x, _ in pts_a), max(x for x, _ in pts_a)
    out = {"a_star": round(a_star, 4), "dose_agreement": {c: round(x, 4) for x, c in pts_a},
           "dose_loss": {c: round(R.loss(s, names, c, band), 1) for c in dose}, "bracketed": lo_a <= a_star <= hi_a}  # fmt: skip
    if not out["bracketed"]:
        x, c = min(pts_a, key=lambda t: abs(t[0] - a_star))
        out["nearest"] = {"cond": c, "agreement": round(x, 4), "loss": round(R.loss(s, names, c, band), 1),
                          "paper10_minus_nearest": R.boot(s, names, lambda ns: R.loss(s, ns, "paper10", band) - R.loss(s, ns, c, band))}  # fmt: skip
        return out

    def stat(ns):
        return R.loss(s, ns, "paper10", band) - interp([(agree[c], R.loss(s, ns, c, band)) for c in dose], a_star)

    out["delta"] = R.boot(s, names, stat)
    out["L_interp"] = round(interp([(agree[c], R.loss(s, names, c, band)) for c in dose], a_star), 1)
    return out


def s_label(m: dict) -> str:
    if not m["bracketed"]:
        return "not matched"
    d, lo, hi = m["delta"]
    if d >= 15 and lo > 0:
        return "J-selective at matched generic damage"
    if d < 10 and lo <= 0 <= hi:
        return "not selective"
    return "partly"


def read_tasks(R: Read, bands: list[str], keep_band: str, ta: dict) -> tuple[dict, list[str]]:
    out: dict = {}
    lines: list[str] = []
    sets = sorted({r["set"] for r in R.items})
    for s in sets:
        names = R.analysis(s)
        o: dict = {"n_analysis": len(names), "n_eligible": sum(r["eligible"] for r in R.items if r["set"] == s), "bands": {}}
        lines.append(f"\n## {s}: analysis n {len(names)} (gated {o['n_eligible']})")
        for b in bands:
            ob: dict = {"loss": {c: round(R.loss(s, names, c, b), 1) for c in DOSE}}
            a0 = R.boot(s, names, lambda ns, b=b: R.loss(s, ns, "paper10", b) - max(R.loss(s, ns, "paper10_rot", b), R.loss(s, ns, "paper10_pcasize", b)))
            ob["A0"] = {"paper10_minus_max_controls": a0, "met": a0[0] >= 20 and a0[1] > 0}
            ob["paper_contrast"] = R.boot(s, names, lambda ns, b=b: R.loss(s, ns, "paper10", b) - R.loss(s, ns, "paper10_rot", b))
            dose_line = []
            for c in DOSE:
                w, v = ta.get(("wiki", b, c)), ta.get(("v4", b, c))
                dose_line.append(f"{c} {ob['loss'][c]}" + (f"/{w[0]:.3f}" if w else "") + (f"/{v[0]:.3f}" if v else ""))
            lines.append(f"  {b}: loss/wiki agreement/v4 agreement: " + "; ".join(dose_line))
            for tset in ("wiki", "v4"):
                agree = {c: ta[(tset, b, c)][0] for c in DOSE if (tset, b, c) in ta}
                if "paper10" not in agree or not all(c in agree for c in PCA + UNEMBED):
                    continue
                a_star = agree["paper10"]
                m_pca = matched(R, s, names, b, agree, PCA, a_star)
                m_une = matched(R, s, names, b, agree, UNEMBED, a_star)
                ob[f"S_{tset}"] = {"pca": m_pca, "unembed": m_une, "label": s_label(m_pca), "label_unembed": s_label(m_une)}
                desc = " (OO descriptive)" if s == "OO" else ""
                tag = "reading" if tset == "wiki" else "beside"
                if m_pca["bracketed"]:
                    lines.append(f"{tag} S {s} {b} [{tset}]: {s_label(m_pca)}{desc} (n {len(names)}; Delta_sel {f(m_pca['delta'])} pts; "
                                 f"a* {a_star:.3f}; L(paper10) {ob['loss']['paper10']}, L_PCA(a*) {m_pca['L_interp']}; PCA agreement "
                                 f"{m_pca['dose_agreement']})")  # fmt: skip
                else:
                    nr = m_pca["nearest"]
                    lines.append(f"{tag} S {s} {b} [{tset}]: not matched{desc} (n {len(names)}; a* {a_star:.3f} outside the PCA agreements "
                                 f"{m_pca['dose_agreement']}; nearest {nr['cond']} at {nr['agreement']}, loss {nr['loss']}; "
                                 f"paper10 - nearest {f(nr['paper10_minus_nearest'])} pts; no reading)")  # fmt: skip
                if m_une["bracketed"]:
                    lines.append(f"  beside S {s} {b} [{tset}] vs logit-lens dose: {s_label(m_une)} (Delta {f(m_une['delta'])} pts; "
                                 f"unembed agreement {m_une['dose_agreement']})")  # fmt: skip
                else:
                    lines.append(f"  beside S {s} {b} [{tset}] vs logit-lens dose: not matched (unembed agreement {m_une['dose_agreement']}; "
                                 f"nearest {m_une['nearest']['cond']} paper10 - it {f(m_une['nearest']['paper10_minus_nearest'])} pts)")  # fmt: skip
            lines.append(f"  beside {s} {b}: the paper's contrast paper10 - rot {f(ob['paper_contrast'])} pts; A0 "
                         f"{'met' if ob['A0']['met'] else 'not met'} ({f(a0)} pts)")  # fmt: skip
            if s == "PO":
                lines.append(f"reading PO A0 {b}: {'the knock-out bites' if ob['A0']['met'] else 'the knock-out does not bite on this set'} "
                             f"(n {len(names)}; paper10 - max(rot, pcasize) {f(a0)} pts)")  # fmt: skip
            o["bands"][b] = ob
        # the keeps at the keep band
        kb = keep_band
        if kb in bands and names:
            met = o["bands"][kb]["A0"]["met"]
            void = "" if met else " [void: A0 not met]"
            if s == "PO":
                sn = R.unprotected(s, names, ["S"])
                kT, kS = R.boot(s, sn, R.K(s, "T", kb)), R.boot(s, sn, R.K(s, "S", kb))
                lab = label_pair(kT[0], kS[0], "the rhyme word carries it", "the rhyme source carries it", "both carry it", "neither") + void
                o["rhyme"] = {"n": len(sn), "K_T": kT, "K_S": kS, "reading": lab}
                lines.append(f"reading PO {kb}: {lab} (n {len(sn)} with S unprotected; K(T) {f(kT)}; K(S) {f(kS)})")
                lines.append(f"  beside PO all items: K(T) {f(R.boot(s, names, R.K(s, 'T', kb)))}; K(S) {f(R.boot(s, names, R.K(s, 'S', kb)))}")
            elif s == "ML":
                pn = [n for n in R.unprotected(s, names, ["E"]) if not R.by[(s, n)].get("cognate")]
                kE, kT = R.boot(s, pn, R.K(s, "E", kb)), R.boot(s, pn, R.K(s, "T", kb))
                lab = label_pair(kE[0], kT[0], "English pivot carries it", "target word carries it", "shared concept", "neither") + void
                o["keep"] = {"n": len(pn), "K_E": kE, "K_T": kT, "label": lab}
                lines.append(f"  beside ML keep {kb} (note 45's pivot rule, descriptive): {lab} (n {len(pn)}; K(E) {f(kE)}; K(T) {f(kT)})")
            elif s == "MH":
                bn = R.unprotected(s, names, ["B"])
                kT, kB = R.boot(s, bn, R.K(s, "T", kb)), R.boot(s, bn, R.K(s, "B", kb))
                lab = label_pair(kT[0], kB[0], "answer", "bridge", "both carry it", "neither") + void
                o["keep"] = {"n": len(bn), "K_T": kT, "K_B": kB, "label": lab}
                lines.append(f"  beside MH keep {kb} (note 45's rule, descriptive): {lab} (n {len(bn)}; K(T) {f(kT)}; K(B) {f(kB)})")
            else:
                kT = R.boot(s, names, R.K(s, "T", kb))
                o["keep"] = {"n": len(names), "K_T": kT}
                lines.append(f"  beside OO keep {kb} (descriptive): K(T) {f(kT)} (n {len(names)})")
            e55 = [r.get("E55") for r in R.items if r["set"] == s and r["name"] in set(names) and r.get("E55")]
            if e55:
                ws = list(e55[0])
                lines.append(f"  {s} keep spans' share of paper10's removal energy at {kb} (median): "
                             + ", ".join(f"E_{w} {statistics.median([x[w] for x in e55 if x[w] is not None]):.3f}" for w in ws))  # fmt: skip
        out[s] = o
    return out, lines


def edit_rel(R: Read) -> dict:
    rows = [json.loads(x) for x in (R.dir / "rows.jsonl").read_text().splitlines() if x.strip()]
    acc = collections.defaultdict(list)
    for r in rows:
        if "edit_rel" in r:
            acc[(r["window"], r["cond"])].append(r["edit_rel"])
    return {f"{w}/{c}": round(statistics.mean(v), 4) for (w, c), v in sorted(acc.items())}


def read_v4(run: str, bands: dict[str, str], prefix_set: str = "jsuite_v4_test_chat") -> tuple[dict, list[str]]:
    from scripts import nn_ko37_read as K37

    p = ROOT / "results" / "ablate_v2" / run / "rows.jsonl"
    if not p.exists():
        return {"run": run, "missing": True}, [f"V: {run} missing"]
    items = {json.loads(x)["id"]: json.loads(x) for x in (ROOT / "data" / "tasks_v2" / prefix_set / "items.jsonl").open()}
    allrows = [json.loads(x) for x in p.open()]
    out: dict = {"run": run}
    lines: list[str] = []
    for bname, blabel in bands.items():
        acc: dict = collections.defaultdict(dict)
        for r in allrows:
            if r.get("kind", "clean") == "clean" and (r["condition"] == "none" or r["band"] == blabel):
                acc[(r["family"], r["condition"])][r["id"]] = (bool(r["correct_cand2"]), r["logp"])
        m = K37.measures(acc, items, lambda it: True, V_CONDS)
        cs = m.get("conditions", {})
        rec: dict = {"band": blabel, "measures": m}
        if all(c in cs for c in ("paper10", "paper10_rot", "paper10_pcasize", "unembed10")):
            g, ci = cs["paper10"]["gap"], cs["paper10"]["gap_ci"]
            rot, ctl = cs["paper10_rot"]["gap"], max(cs["paper10_pcasize"]["gap"], cs["unembed10"]["gap"])
            holds = g >= 20 and ci is not None and ci[0] > 0 and rot <= g / 3 and g - ctl >= 10
            rec["V"] = {"gap": g, "gap_ci": ci, "rot_gap": rot, "pcasize_gap": cs["paper10_pcasize"]["gap"], "unembed10_gap": cs["unembed10"]["gap"],
                        "reading": "C1 holds at the paper's strength" if holds else "C1 not shown at the paper's strength"}  # fmt: skip
            lines.append(f"reading V {bname} ({blabel}): {rec['V']['reading']} (n MP {m['n']['MP']} MM {m['n']['MM']}; gap {g} {ci}; rot gap {rot}; "
                         f"pcasize gap {cs['paper10_pcasize']['gap']}; unembed10 gap {cs['unembed10']['gap']})")  # fmt: skip
        if "reading" in m:
            lines.append(f"reading V keepA {bname} ({blabel}): {m['reading']} (ratio {m['ratio']}; keepA gap {cs['paper10_keepA']['gap']} "
                         f"{cs['paper10_keepA']['gap_ci']})")  # fmt: skip
        lines += ["  " + x for x in K37.table(f"v4 {bname}", m)]
        out[bname] = rec
    return out, lines


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--v4", default=None, help="the model's ablate_v2 v4 run at the same bands")
    ap.add_argument("--v4-stored", default=None, help="note 37's stored v4 run (its unedited rows are checked)")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    R = Read(Path(a.run_dir), a.boot)
    man = json.loads((R.dir / "manifest.json").read_text())
    check = json.loads((R.dir / "check.json").read_text())
    bands = list(man["bands"])
    ta = text_agreement(R.dir)
    res: dict = {"run": str(R.dir), "target": man["target"], "bands": man["bands"], "byte_check_all_equal": check["all_equal"]}
    print(f"# note 55 reading: {R.dir.name} ({man['target']}); bands {man['bands']}; keep band {man['keep_band']}; "
          f"byte-identity check (paper10, rot, top3, top30 vs ablate_v2's recipe, MH): all equal {check['all_equal']}")
    # G
    res["G"] = {}
    for b in bands:
        w = {c: ta.get(("wiki", b, c)) for c in ("paper10", "paper10_rot")}
        v = {c: ta.get(("v4", b, c)) for c in ("paper10", "paper10_rot")}
        if w["paper10"]:
            res["G"][b] = {"wiki": {c: x[0] for c, x in w.items() if x}, "v4": {c: x[0] for c, x in v.items() if x}}
            print(f"reading G {b}: paper10 WikiText top-1 agreement {w['paper10'][0]:.3f} (paper {PAPER_G.get(b)}), paper10_rot "
                  f"{w['paper10_rot'][0]:.3f} (paper's random {PAPER_RANDOM}, at medium) (n {w['paper10'][1]} texts, {w['paper10'][2]} "
                  f"positions); v4 passages paper10 {v['paper10'][0]:.3f}, rot {v['paper10_rot'][0]:.3f} (n {v['paper10'][1]})")  # fmt: skip
    for b in bands:
        print(f"  text dose {b} (wiki agreement / nll / |edit|/|h|): " + "; ".join(
            f"{c} {ta[('wiki', b, c)][0]:.3f}/{ta[('wiki', b, c)][3]:.2f}/{ta[('wiki', b, c)][4]:.3f}" for c in DOSE + ("paper10_noprot",) if ("wiki", b, c) in ta))  # fmt: skip
    if ("wiki", "-", "none") in ta:
        print(f"  text clean nll: wiki {ta[('wiki', '-', 'none')][3]:.3f}, v4 {ta[('v4', '-', 'none')][3]:.3f}")
    tasks, lines = read_tasks(R, bands, man["keep_band"], ta)
    res["sets"] = tasks
    print("\n".join(lines))
    er = edit_rel(R)
    res["edit_rel_tasks"] = er
    print("  task |edit| / |h| (mean over rows): " + json.dumps(er))
    if a.v4:
        v4b = {b: f"L{v.split('-')[0]}-{v.split('-')[1]}" for b, v in man["bands"].items()}
        v4, vl = read_v4(a.v4, v4b)
        res["v4"] = v4
        print("\n## v4\n" + "\n".join(vl))
        if a.v4_stored and not v4.get("missing"):
            from scripts import nn_ko37_read as K37

            new = K37.rows_of(a.v4)
            sc = K37.stored_check({k: v for k, v in new.items() if k[1] == "none"}, a.v4_stored)
            res["v4_stored_check_none"] = {k: v for k, v in sc.items() if k == "stored_run" or k.endswith("/none")}
            print("  stored check of the unedited rows (" + a.v4_stored + "): " + "; ".join(
                f"{k} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']}"
                for k, v in sc.items() if k.endswith("/none")))  # fmt: skip
    (R.dir / "reading55.json").write_text(json.dumps(res, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
