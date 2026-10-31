"""v3_readings (Zach, 2026-10-28, prereg amendment 58 notes 3-5): note 4's fixed readings, and the ports' shares against
the removal matrix, for each model with a scored v3 removal matrix (CPU; reads results/ablate_v2/v3_score/*.json and
results/v3_cards/*). Run scripts/v3_score.py on each run first.

  headline    start P (and P without films, P_strict): paper10 M - K >= 10 and paper10_rot <= 10; unembed10, pcasize beside
  hard read   start P, level all and level 3: H's loss under paper10 minus paper10_rot (within 10 = "recall, not anything
              hard"), with H vs M unedited accuracy / median log p and the log-p-matched M - H gap
  conflict    paper10's shift towards the passage value minus paper10_rot's and paper10_pcasize's (>= 10 in both)
  W vs M      guess-prompt accuracy (competence card) and M - K on W
  X, Q, J     M - K where the card's real-composition share is >= 0.7
  ports       answer-only: ansJ M - K / paper10 M - K (note 3: >= 0.5 with ansJ_rot <= 10 = answer deletion explains it);
              position split: each mode's paper10 M - K / the matrix's (amendment 36's shares)

python scripts/v3_readings.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SC = ROOT / "results" / "ablate_v2" / "v3_score"
MODELS = (("qwen35_9b_", "Qwen3.5-9B", "L12-16", "L26-29", "qwen35_9b_"), ("", "Qwen3.6-27B", "L32-40", "L52-60", "qwen36_27b_"),
          ("nem35l_", "Lightning", "L27-33", "L33-39", "nem35l_"))  # fmt: skip
SET = "jsuite_v3_test_chat"


def load(name: str) -> dict | None:
    f = SC / f"{name}.json"
    return json.loads(f.read_text()) if f.exists() else None


def mk(d: dict, cond: str, st: str, lv: str = "Lall", c: str = "M-K") -> tuple | None:
    cell = d["cells"].get(f"{cond}/{st}/{lv}")
    if not cell or c not in cell["contrasts"]:
        return None
    return cell["contrasts"][c]["diff"], cell["contrasts"][c]["ci"]


def fmt(x) -> str:
    return "-" if x is None else f"{x[0]:+.1f} {x[1]}"


def main() -> None:
    for p, name, band, deep, cardp in MODELS:
        d = load(f"{p}{SET}_ko_cand2_v1")
        print(f"\n===== {name} ({band})" + ("" if d else ": no scored removal matrix yet"))
        if not d:
            continue
        card = json.loads((ROOT / "results" / "v3_cards" / f"{cardp}cards.json").read_text())
        for st in ("P", "P_nofilms", "P_strict"):
            row = {c: mk(d, c, st) for c in ("paper10", "paper10_rot", "unembed10", "paper10_pcasize")}
            ok = row["paper10"] and row["paper10_rot"] and row["paper10"][0] >= 10 and row["paper10_rot"][0] <= 10
            print(f"headline {st:10s} " + "  ".join(f"{c} {fmt(v)}" for c, v in row.items()) + f"  -> {'PASS' if ok else 'fail'}")
        for lv in ("Lall", "L3"):
            hr = d["hard_read"].get(f"P/{lv}")
            if hr:
                b = hr["by_condition"]
                print(f"hard read P/{lv}: H lost paper10 {b['paper10']['H_lost']} rot {b['paper10_rot']['H_lost']} -> H - rot "
                      f"{b['paper10']['H_minus_rot']} ({'within 10' if b['paper10']['H_minus_rot'] is not None and abs(b['paper10']['H_minus_rot']) <= 10 else 'NOT within 10'}); "
                      f"M lost {b['paper10']['M_lost']}; M - H log-p matched {b['paper10']['M_minus_H_logp_matched']} (M items {b['paper10']['matched_M_items']}); "
                      f"unedited acc {hr['unedited_acc']} median log p {hr['median_logp_right']}")  # fmt: skip
        for lv in ("L3",):
            print(f"level 3: K-M {fmt(mk(d, 'paper10', 'P', lv))} (rot {fmt(mk(d, 'paper10_rot', 'P', lv))})")
        c = d["conflict"].get("all")
        if c:
            a, b = c.get("paper10_minus_paper10_rot"), c.get("paper10_minus_paper10_pcasize")
            ok = a and b and a["diff"] >= 10 and b["diff"] >= 10
            print(f"conflict all (n {c['n']}): passage share none {c['share']['none']['passage']} paper10 {c['share']['paper10']['passage']}; "
                  f"paper10 - rot {a}; paper10 - pcasize {b} -> {'PASS' if ok else 'fail'}")  # fmt: skip
            for g in ("P-start", "M-start"):
                cg = d["conflict"].get(g)
                if cg:
                    print(f"   {g}: passage none {cg['share']['none']['passage']} paper10 {cg['share']['paper10']['passage']} rot {cg['share']['paper10_rot']['passage']}")
        cells = card["cells"]
        print(f"W vs M guess: WM-L1 {cells.get('WM-L1', {}).get('guess')} vs MM-L1 {cells.get('MM-L1', {}).get('guess')}; W M - K {fmt(mk(d, 'paper10', 'W'))} rot {fmt(mk(d, 'paper10_rot', 'W'))}")
        for st, w in (("X", "XM-L1"), ("Q", "QM-L1"), ("J", "JM-L1"), ("T", "TM-L1"), ("M", "MM-L1"), ("Y", "YM-L1")):
            share = cells.get(w, {}).get("real_share")
            print(f"start {st}: real share {share} -> " + (f"M - K {fmt(mk(d, 'paper10', st))} rot {fmt(mk(d, 'paper10_rot', st))}" if share is not None and share >= 0.7 else "not read"))
        nn = d["never_named"].get("paper10")
        if nn:
            print(f"never-named RM - MM {nn['contrasts'].get('RM-MM')} (rot {d['never_named'].get('paper10_rot', {}).get('contrasts', {}).get('RM-MM')})")
        ref = mk(d, "paper10", "P")
        ans = load(f"{p}{SET}_ko_cand2_{band}_ans_v1")
        if ans and ref:
            j, jr = mk(ans, "ansJ", "P"), mk(ans, "ansJ_rot", "P")
            ok = j[0] >= 0.5 * ref[0] and jr[0] <= 10
            print(f"answer-only: ansJ {fmt(j)} / paper10 {ref[0]:+.1f} = {j[0] / ref[0]:.2f} (ansJ_rot {fmt(jr)}; ansU {fmt(mk(ans, 'ansU', 'P'))}) "
                  f"-> {'answer deletion explains most (>= 0.5)' if ok else 'not mostly answer deletion'} in this model")  # fmt: skip
        for b_ in (band, deep):
            for mode in ("bridge", "question"):
                pos = load(f"{p}{SET}_ko_cand2_{b_}_pos{mode}_v1")
                if pos and ref:
                    line = []
                    for st in ("P", "T", "M", "W"):
                        x, r = mk(pos, "paper10", st), mk(d, "paper10", st)
                        if x and r and r[0] >= 15:
                            line.append(f"{st} {x[0]:+.0f}/{r[0]:+.0f} = {x[0] / r[0]:.2f}")
                        elif x and r:
                            line.append(f"{st} ref {r[0]:+.0f} < 15, not read")
                    print(f"position {b_} {mode}-only share of the all-position M - K: " + "; ".join(line))


if __name__ == "__main__":
    main()
