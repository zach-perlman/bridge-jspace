"""nn_ko58_read (Zach, 2026-10-30, prereg amendment 84 note 58): recall and lookup through separable subspaces? A double
dissociation with the unembedding dark space (DarkLens, Kuleshova et al. 2610.23182 §3.2), read (CPU).

Run (scripts/queues/h200_n58_1030.sh), per model prefix P: {P}jsuite_v4_test_chat_ko58_cand2_v1 (v4 draw 4001, note 37's gate,
band, batch and cand2 read; MP lookup and MM recall twins) under paper10 and paper10_rot (rerun, at the main band) and, per
4-layer window W (a: the main band's start; b: DarkLens's depth, ~55-64% of the layers): darkperm_W (the hidden state's components
in W_U's bottom-5% right singular vectors permuted across the non-initial positions, seeded per item, rescaled to the original
norm) and midperm_W (the same in a mid-spectrum block whose dimension matches the dark permutation's WikiText NLL increase; the run's
n58_calib.json). Every row carries edit_rel.
Measures: nn_ko37_read's (loss = 100 x (correct_cand2 unedited - edited) over the gated items; gap = MM - MP; 95% bootstrap over
bridges, 2000 draws, random.Random(0), every gated item of a bridge resampled together).
Readings (per window):
  D1 "lookup needs the dark space": MP loss(dark) - MP loss(mid) >= 15 with the lower end > 0, AND MP loss(dark) - MM loss(dark)
     >= 10 with the lower end > 0. If D1 fails: "no dark-space lookup route on these models".
  Double dissociation: D1 AND C1 in the same run (paper10's MM - MP gap >= 20; its interval and paper10_rot's gap beside).
Writes results/ablate_v2/nn_ko_read/{P}note58.json (or --out-dir) and prints one "reading ..." line per reading and window.

python scripts/nn_ko58_read.py PREFIX [--run-dir DIR] [--out-dir DIR]   (PREFIX "" for the 27B, qwen35_9b_, nem35l_)
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import nn_ko37_read as K  # noqa: E402
from scripts.nn_ko49_read import rows_at  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
SET = "jsuite_v4_test_chat"


def mean100(xs):
    return 100 * sum(xs) / len(xs) if xs else float("nan")


def main(P: str, run_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    items = {json.loads(l)["id"]: json.loads(l) for l in (DATA / SET / "items.jsonl").open()}
    d = run_dir or RES / "ablate_v2" / f"{P}{SET}_ko58_cand2_v1"
    out: dict = {"prefix": P, "run": str(d)}
    if not (d / "rows.jsonl").exists():
        print(f"note 58 {P or '27b_'}: {d} missing")
        return out
    acc = rows_at(d)
    conds = sorted({c for (_, c) in acc if c != "none"}, key=lambda c: (c.startswith(("dark", "mid")), c))
    m = K.measures(acc, items, lambda it: True, tuple(conds))
    cs = m["conditions"]
    out["measures"], out["stored_check"] = m, K.stored_check(acc, f"{P}{SET}_ko37_cand2_v1")
    tag = P or "27b_"
    lines = K.table(f"note 58 {tag}", m)
    calib = json.loads((d / "n58_calib.json").read_text()) if (d / "n58_calib.json").exists() else {}
    out["calibration"] = calib
    base = {f: acc.get((f, "none"), {}) for f in ("MP", "MM")}
    p10 = cs.get("paper10", {})
    c1 = bool(p10) and p10["gap"] >= 20
    out["C1"] = {"met": c1, "gap": p10.get("gap"), "gap_ci": p10.get("gap_ci"), "rot_gap": cs.get("paper10_rot", {}).get("gap")}
    lines.append(f"reading note58 C1 {tag}: {'met' if c1 else 'not met'} | paper10 gap {p10.get('gap')} {p10.get('gap_ci')}, "
                 f"paper10_rot gap {cs.get('paper10_rot', {}).get('gap')} (n MP {m['n'].get('MP')}, MM {m['n'].get('MM')})")
    R = {}
    windows = sorted({mm[1] for c in conds if (mm := re.fullmatch(r"darkperm_(L\d+-\d+)", c))})
    for w in windows:
        dk, md = f"darkperm_{w}", f"midperm_{w}"
        if dk not in cs or md not in cs:
            R[w] = {"label": "not read: conditions missing"}
            continue
        by1, by2 = collections.defaultdict(list), collections.defaultdict(list)
        for i, (ok, _) in base["MP"].items():
            if i in acc[("MP", dk)] and i in acc[("MP", md)]:
                by1[items[i]["bridge"]].append(int(ok) - int(acc[("MP", dk)][i][0]) - (int(ok) - int(acc[("MP", md)][i][0])))
        for f in ("MP", "MM"):
            for i, (ok, _) in base[f].items():
                if i in acc[(f, dk)]:
                    by2[items[i]["bridge"]].append((f, int(ok) - int(acc[(f, dk)][i][0])))
        u1 = [x for v in by1.values() for x in v]
        u2 = [x for v in by2.values() for x in v]
        s1, ci1 = mean100(u1), K.boot(by1, mean100)
        neg_gap = lambda us: -K.gap_fn(us)  # noqa: E731  # MP loss - MM loss
        s2, ci2 = neg_gap(u2), K.boot(by2, neg_gap)
        d1 = s1 >= 15 and bool(ci1) and ci1[0] > 0 and s2 >= 10 and bool(ci2) and ci2[0] > 0
        lab = "lookup needs the dark space" if d1 else "no dark-space lookup route on these models"
        dd = ("double dissociation" if d1 and c1 else "D1 holds, C1 not met in this run" if d1 else "no double dissociation (D1 fails)")
        cw = calib.get("windows", {}).get(w, {})
        R[w] = {"label": lab, "double_dissociation": dd, "MP_dark_minus_mid": round(s1, 1), "ci": ci1, "n_MP": len(u1),
                "MP_minus_MM_dark": round(s2, 1), "ci2": ci2, "n_MP_MM": len(u2),
                "loss": {c: {"MP": cs[c]["loss_MP"], "MM": cs[c]["loss_MM"], "gap": cs[c]["gap"]} for c in (dk, md)},
                "mid_dim": cw.get("mid_dim"), "dnll_dark": cw.get("dnll_dark"), "dnll_mid": cw.get("dnll_mid"),
                "matched_within_10pct": cw.get("matched_within_10pct"), "pct_depth": cw.get("pct_depth")}  # fmt: skip
        lines.append(f"reading note58 D1 {w} {tag}: {lab!r} | MP dark - mid {R[w]['MP_dark_minus_mid']} {ci1} (n MP {len(u1)}); "
                     f"MP - MM under dark {R[w]['MP_minus_MM_dark']} {ci2} (n {len(u2)})")
        lines.append(f"reading note58 DD {w} {tag}: {dd!r} | C1 {'met' if c1 else 'not met'} (paper10 gap {p10.get('gap')}); "
                     f"mid dim {cw.get('mid_dim')} (dNLL dark {cw.get('dnll_dark')}, mid {cw.get('dnll_mid')}, within 10%: {cw.get('matched_within_10pct')}); "
                     f"depth {cw.get('pct_depth')}%")
    out["readings"] = R
    er = collections.defaultdict(list)
    for line in (d / "rows.jsonl").open():
        r = json.loads(line)
        if r.get("edit_rel") is not None:
            er[r["condition"]].append(r["edit_rel"])
    out["edit_rel_mean"] = {c: round(sum(v) / len(v), 6) for c, v in er.items()}
    lines.append(f"  edit_rel (mean |edit|^2 / |h|^2): {json.dumps(out['edit_rel_mean'])}")
    sc = out["stored_check"]
    if not sc.get("missing"):
        lines.append(f"  stored check ({sc['stored_run']}): " + "; ".join(
            f"{c} {v['n_both']}/{v['n_new']} same read {v['same_correct']} same logp {v['same_logp_bits']}" for c, v in sc.items() if c != "stored_run"))
    od = out_dir or RES / "ablate_v2" / "nn_ko_read"
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}note58.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n".join(lines))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix", nargs="?", default="")
    ap.add_argument("--run-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()
    main(a.prefix, a.run_dir, a.out_dir)
