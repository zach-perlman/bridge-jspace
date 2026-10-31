"""nn_v5_mc_read (Zach, 2026-10-30, prereg amendment 63 note 35 and its addendum): one remembered fact, three uses. MC's and
MC0's knock-out contrasts, their readings, and the paired comparisons with MP, on the named key scenes.

python scripts/nn_v5_mc_read.py PREFIX [--mc-run RUN] [--kn-run RUN] [--removed-run RUN] [--margins-run RUN] [--out NAME]
  MC, MC0: results/ablate_v2/{PREFIX}jsuite_v5kn2c_test_chat_ko_cand2_v1 (kinds clean, step2: MC's step 2 is the direct
           capital with the passage, MC0's is C0, the direct capital closed book)
  MP, MM:  the existing v5key2 named run results/ablate_v2/{PREFIX}jsuite_v5kn2_test_chat_ko_cand2_v1, unchanged
  removal record and MC / MC0 margins: {PREFIX}jsuite_v5kn2c_test_chat_removed_v1 (scripts/nn_v5_mc_removed.py)
  MP margins: {PREFIX}jsuite_v5kn2_test_chat_margins_v1 (nn_v5_mc_removed.py --margin-only)
Writes results/ablate_v2/nn_v5_read/{PREFIX}mc35.json and prints the readings.

The contrast is note 29's, computed as scripts/nn_v5_read.key() computes MP's: per item gated ok (an item is in the
knock-out run's unedited rows of both its whole question and its step 2), the whole question's loss (unedited correct
minus edited correct, cand2: 1 / 0 / -1) minus its step 2's loss, in points; the interval is key()'s bootstrap (2000
resamples of bridges, each with all its items, seed 0).
Rules (note 35 and the addendum), per arm:
  "needs": contrast(paper10) >= 15 with its interval above 0; contrast(paper10_rot) < 5; contrast(paper10) minus
    contrast(paper10_pcasize) >= 10.
  "does not need": contrast(paper10) < 10 with its interval's upper end < 15 (the addendum's; note 29's "goes around").
  MP "does not" (note 35): "goes around" or not beyond paper10_pcasize (contrast(paper10) - contrast(paper10_pcasize) < 10).
Readings:
  joint (addendum): "memory computation needs it" (MC0 and MC need); "through the passage" (MC0 needs, MC does not need);
    "only saying needs it" (MC0 does not need); otherwise "unclear".
  note 35 (MC vs MP): "dissociation" (MC needs, MP does not, paired MC - MP paper10 contrast >= 10 with its interval above
    0 on scenes where both are gated ok); "both need" (MC and MP need); "neither" (MC does not need, the addendum's
    definition); otherwise "unclear". MC0 vs MP is read the same way (the addendum: compared with MP the same way).
Strata, each read by the same rules:
  scenes: "all", and "split_ok" (amendment 61 addendum: scenes with split_ok false are left out of the primary);
  answer exclusion (MC and MC0): "none"; "exact" (note 35 and addendum 4: items whose answer's first-token J++ row (the
    read token, as the answer starts the reply) was among paper10's removed top-10 at any edited position at any band
    layer, from the removal record; absent record: not computed); "anyform" (the primary, Zach 30 Oct ~04:45 UTC: the same for any form of that
    first token, either case, with or without a leading space; paper10 protects the clean top-10 output tokens, so "exact" excludes nothing); "top1" (a stand-in from the knock-out rows alone: keep items whose unedited top token is the answer's,
    which paper10 protects everywhere).
  The primary is split_ok/anyform (amendment 63, second addendum).
Margin matching (addendum 3, descriptive): the whole question's unedited cand2 margin (right candidate's logit minus the
  best other's) of each arm's contrast items; 5 quantile bins of the pooled margins (MC, MC0, MP); each arm's contrast
  within bins, averaged with MP's bin weights (renormalised over the bins the arm fills; coverage reported). Not
  computed when a margins record is missing.
MM's loss and unembed10 are reported beside.
"""

from __future__ import annotations

import argparse
import bisect
import collections
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts.nn_v5_read import boot_ci, items_of, ko_rows, mean  # noqa: E402

RES = ROOT / "results"
CONDS = ("paper10", "paper10_rot", "unembed10", "paper10_pcasize")
MC_SET, KN_SET = "jsuite_v5kn2c_test_chat", "jsuite_v5kn2_test_chat"


def suffix(i: str) -> str:
    return i.rsplit("-", 1)[1]


def per_item(acc, fam: str, cond: str, keep, step: str = "step2") -> dict:
    """id -> (whole loss, step 2's loss) for the family's gated items that keep() admits (key()'s per-item terms)."""
    whole, last = acc.get((fam, "clean", "none"), {}), acc.get((fam, step, "none"), {})
    if (fam, "clean", cond) not in acc:
        return {}
    return {i: (whole[i] - acc[(fam, "clean", cond)][i], last[i] - acc[(fam, step, cond)][i]) for i in whole if i in last and keep(i)}


def contrast(acc, items, fam: str, cond: str, keep) -> dict | None:
    xs = per_item(acc, fam, cond, keep)
    if not xs:
        return None
    by = collections.defaultdict(list)
    for i, v in xs.items():
        by[items[i]["bridge"]].append(v)
    vals = list(xs.values())
    return {"n_items": len(vals), "n_bridges": len(by), "loss": round(mean([a for a, _ in vals]), 1),
            "loss_step": round(mean([b for _, b in vals]), 1), "contrast": round(mean([a - b for a, b in vals]), 1),
            "ci": boot_ci(by, lambda us: mean([a - b for a, b in us]))}  # fmt: skip


def status(c: dict) -> dict:
    p, r, s = c.get("paper10"), c.get("paper10_rot"), c.get("paper10_pcasize")
    needs = bool(p and r and s and p["ci"]) and p["contrast"] >= 15 and p["ci"][0] > 0 and r["contrast"] < 5 and p["contrast"] - s["contrast"] >= 10
    dnn = bool(p and p["ci"]) and p["contrast"] < 10 and p["ci"][1] < 15
    flat = bool(p and s) and p["contrast"] - s["contrast"] < 10
    return {"needs": needs, "does_not_need": dnn, "not_beyond_pcasize": flat, "does_not_note35": dnn or flat,
            "minus_pcasize": round(p["contrast"] - s["contrast"], 1) if p and s else None}  # fmt: skip


def paired(acc_a, items_a, fam_a, keep_a, acc_b, items_b, keep_b, cond="paper10") -> dict:
    """Arm a's minus MP's contrast, per scene where both are gated ok (scene suffix), bootstrap over bridges."""
    b_ = {suffix(i): v for i, v in per_item(acc_b, "MP", cond, keep_b).items()}
    by = collections.defaultdict(list)
    for i, (lw, ls) in per_item(acc_a, fam_a, cond, keep_a).items():
        if suffix(i) in b_:
            pw, ps = b_[suffix(i)]
            by[items_a[i]["bridge"]].append((lw - ls) - (pw - ps))
    xs = [x for v in by.values() for x in v]
    return {"n_scenes": len(xs), "n_bridges": len(by), "d": round(mean(xs), 1) if xs else None, "ci": boot_ci(by, lambda us: mean(us)) if xs else None}


def vs_mp(arm: dict, mp: dict, pr: dict) -> str:
    if arm["needs"]:
        if mp["needs"]:
            return "both need"
        if mp["does_not_note35"] and pr["ci"] and pr["d"] >= 10 and pr["ci"][0] > 0:
            return "dissociation"
        return "unclear"
    return "neither" if arm["does_not_need"] else "unclear"


def margins(run: str) -> dict | None:
    p = RES / "ablate_v2" / run / "rows.jsonl"
    if not p.exists():
        return None
    out = {}
    for line in p.open():
        r = json.loads(line)
        if r["kind"] == "clean" and r.get("margin2") is not None:
            out[r["id"]] = r["margin2"]
    return out


def margin_matched(arms: dict, mar: dict) -> dict:
    """arms: name -> {id: (lw, ls)} per condition-free item set (paper10's items); mar: id -> margin. MP's bin weights."""
    pooled = [mar[i] for xs in arms.values() for i in xs if i in mar]
    if len(pooled) < 10 or "MP" not in arms:
        return {"available": False, "why": "too few items with a margin"}
    cuts = statistics.quantiles(pooled, n=5)
    binof = lambda i: bisect.bisect_right(cuts, mar[i])  # noqa: E731
    w = collections.Counter(binof(i) for i in arms["MP"] if i in mar)
    tot = sum(w.values())
    out = {"available": True, "cuts": [round(c, 3) for c in cuts], "MP_bin_weights": {b: round(w[b] / tot, 3) for b in range(5)}}
    for name, xs in arms.items():
        bins = collections.defaultdict(list)
        for i, (lw, ls) in xs.items():
            if i in mar:
                bins[binof(i)].append(lw - ls)
        cov = sum(w[b] for b in bins) / tot if tot else 0
        val = sum(w[b] * mean(v) for b, v in bins.items()) / sum(w[b] for b in bins) if any(w[b] for b in bins) else None
        out[name] = {"matched_contrast": round(val, 1) if val is not None else None, "MP_weight_covered": round(cov, 3),
                     "n": len(xs), "n_with_margin": sum(i in mar for i in xs),
                     "unmatched_contrast": round(mean([lw - ls for lw, ls in xs.values()]), 1) if xs else None,
                     "bins": {b: {"n": len(bins[b]), "contrast": round(mean(bins[b]), 1)} for b in sorted(bins)}}  # fmt: skip
    return out


def main(a) -> dict:
    P = a.prefix
    mc_run, kn_run = a.mc_run or f"{P}{MC_SET}_ko_cand2_v1", a.kn_run or f"{P}{KN_SET}_ko_cand2_v1"
    rem_run = a.removed_run or f"{P}{MC_SET}_removed_v1"
    mar_run = a.margins_run or f"{P}{KN_SET}_margins_v1"
    mc_items, kn_items = items_of(MC_SET), items_of(KN_SET)
    mc_acc, kn_acc = ko_rows(mc_run), ko_rows(kn_run)
    top1 = set()  # MC / MC0 items whose unedited top token is the answer's first token (its row protected by paper10)
    for line in (RES / "ablate_v2" / mc_run / "rows.jsonl").open():
        r = json.loads(line)
        if r.get("kind", "clean") == "clean" and r["condition"] == "none" and r.get("correct_top"):
            top1.add(r["id"])
    removed, removed_any, rem_path = None, None, RES / "ablate_v2" / rem_run / "rows.jsonl"
    if rem_path.exists():
        rr = [json.loads(line) for line in rem_path.open()]
        removed = {r["id"] for r in rr if r["kind"] == "clean" and r.get("answer_row_removed")}
        removed_any = {r["id"] for r in rr if r["kind"] == "clean" and r.get("any_form_removed")}
    mar = {}
    for run in (rem_run, mar_run):
        m = margins(run)
        if m:
            mar.update(m)
    out: dict = {"mc_run": mc_run, "kn_run": kn_run, "removed_run": rem_run if removed is not None else None,
                 "margins_runs": [r for r in (rem_run, mar_run) if margins(r)],
                 "n_gated": {f: len((mc_acc if f.startswith("MC") else kn_acc).get((f, "clean", "none"), {})) for f in ("MC", "MC0", "MP", "MM")},
                 "n_top1": {f: sum(i in top1 for i in mc_acc.get((f, "clean", "none"), {})) for f in ("MC", "MC0")},
                 "n_answer_row_removed": {f: sum(i in removed for i in mc_acc.get((f, "clean", "none"), {})) for f in ("MC", "MC0")} if removed is not None else None,
                 "n_any_form_removed": {f: sum(i in removed_any for i in mc_acc.get((f, "clean", "none"), {})) for f in ("MC", "MC0")} if removed is not None else None,
                 "strata": {}}  # fmt: skip
    scenes = {"all": lambda it: True, "split_ok": lambda it: bool(it.get("split_ok"))}
    excl = {"none": lambda i: True, "top1": lambda i: i in top1}
    if removed is not None:
        excl["exact"] = lambda i: i not in removed
        excl["anyform"] = lambda i: i not in removed_any  # the primary: any form of the first token (case, leading space)
    mm = kn_acc.get(("MM", "clean", "none"), {})
    for sname, sk in scenes.items():
        kn_keep = lambda i, sk=sk: sk(kn_items[i])  # noqa: E731
        mp = {c: v for c in CONDS if (v := contrast(kn_acc, kn_items, "MP", c, kn_keep))}
        mp_st = status(mp)
        mm_loss = {c: round(mean([mm[i] - kn_acc[("MM", "clean", c)][i] for i in mm if sk(kn_items[i])]), 1) for c in CONDS if ("MM", "clean", c) in kn_acc}
        for ename, ek in excl.items():
            keep = lambda i, sk=sk, ek=ek: sk(mc_items[i]) and ek(i)  # noqa: E731
            rec: dict = {"MP": mp, "MP_status": mp_st, "MM_loss": mm_loss}
            for fam in ("MC", "MC0"):
                c = {cd: v for cd in CONDS if (v := contrast(mc_acc, mc_items, fam, cd, keep))}
                rec[fam], rec[f"{fam}_status"] = c, status(c)
                rec[f"paired_{fam}_minus_MP"] = paired(mc_acc, mc_items, fam, keep, kn_acc, kn_items, kn_keep)
                rec[f"reading_{fam}_vs_MP"] = vs_mp(rec[f"{fam}_status"], mp_st, rec[f"paired_{fam}_minus_MP"])
            s0, s1 = rec["MC0_status"], rec["MC_status"]
            rec["reading_joint"] = ("memory computation needs it" if s0["needs"] and s1["needs"] else
                                    "through the passage" if s0["needs"] and s1["does_not_need"] else
                                    "only saying needs it" if s0["does_not_need"] else "unclear")  # fmt: skip
            if mar and any(i in mar for i in per_item(kn_acc, "MP", "paper10", kn_keep)):
                rec["margin_matched"] = {cd: margin_matched({"MC": per_item(mc_acc, "MC", cd, keep), "MC0": per_item(mc_acc, "MC0", cd, keep),
                                                             "MP": per_item(kn_acc, "MP", cd, kn_keep)}, mar) for cd in CONDS}  # fmt: skip
            else:
                rec["margin_matched"] = {"available": False, "why": "no margins record (MP's and MC / MC0's unedited cand2 margins)"}
            out["strata"][f"{sname}/{ename}"] = rec
    out["primary"] = "split_ok/anyform" if removed is not None else "split_ok/anyform: not computable (no removal record); split_ok/top1 beside"
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prefix", nargs="?", default="", help="the model's run prefix: qwen35_9b_, '' (27B), nem35l_")
    ap.add_argument("--mc-run", default=None, help="the MC / MC0 knock-out run (default {prefix}jsuite_v5kn2c_test_chat_ko_cand2_v1)")
    ap.add_argument("--kn-run", default=None, help="the named key run (default {prefix}jsuite_v5kn2_test_chat_ko_cand2_v1)")
    ap.add_argument("--removed-run", default=None, help="the removal record (default {prefix}jsuite_v5kn2c_test_chat_removed_v1)")
    ap.add_argument("--margins-run", default=None, help="MP's margins (default {prefix}jsuite_v5kn2_test_chat_margins_v1)")
    ap.add_argument("--out", default=None, help="output name under results/ablate_v2/nn_v5_read/ (default {prefix}mc35)")
    a = ap.parse_args()
    res = main(a)
    d = RES / "ablate_v2" / "nn_v5_read"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{a.out or a.prefix + 'mc35'}.json").write_text(json.dumps(res, indent=1) + "\n")
    for k, rec in res["strata"].items():

        def f(fam, rec=rec):
            c = rec[fam].get("paper10") or {}
            return f"{fam} n={c.get('n_items')} c={c.get('contrast')} ci={c.get('ci')}"

        print(f"reading {k}: joint={rec['reading_joint']} | MC-vs-MP={rec['reading_MC_vs_MP']} | MC0-vs-MP={rec['reading_MC0_vs_MP']} | "
              f"{f('MC')} | {f('MC0')} | {f('MP')}")  # fmt: skip
    print(json.dumps({k: v for k, v in res.items() if k != "strata"}, indent=1))
