"""jsuite2_score (Zach, 2026-10-24, prereg amendment 33): a knock-out run on the combined suite v2 (jsuite_v2_*), all
modules from one rows file, each scored by its own design (the module comes from the item):
  facts     per condition, start (P M T all), test half (A B all) and relation: points lost (items right unedited) for
            the finals P K M A N, and the contrasts M - K (primary: same question and answer, recalled vs stated),
            M - P, M - N (lure capture: lures present vs none), A - M; 95% bootstrap over bridges (resampled jointly)
  threehop  points lost per word, and each word minus PPP under the same condition (natural3's design)
  numbers   points lost per word (prefix "n" stripped: SF, S in P K A M, F in R L M), and SM - SL, KR - PR, AR - PR,
            MR - PR (amendment 21's contrasts)
Writes results/ablate_v2/jsuite2_score/RUN.json.

python scripts/jsuite2_score.py RUN --set jsuite_v2_test_chat [--by-relation] [--with RUN2 ...]
(v2.1, 2026-10-24: start R, the never-named recall, is kept out of the start=all cells and scored as RF - MF.
--with: rows of other runs on the same model, band, conditions, lens and read, on other items (a model's R-only run
beside its v2 run; ids are shared across v2 and v2.1), scored as one; written to RUN+RUN2.json)
"""

from __future__ import annotations

import argparse
import collections
import json
import random
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "ablate_v2"
DATA = Path(__file__).resolve().parents[1] / "data" / "tasks_v2"
FACT_CONTRASTS = (("M", "K"), ("M", "P"), ("M", "N"), ("A", "M"))


def boot(sel: dict[str, list[tuple[str, bool]]], contrasts, rng: random.Random, reps: int = 1000) -> dict:
    """sel: final -> [(cluster, correct)]; percentile intervals of loss differences, clusters resampled jointly."""
    loss = {f: 100 * (1 - sum(c for _, c in v) / len(v)) for f, v in sel.items() if v}
    clusters = sorted({b for v in sel.values() for b, _ in v})
    boots = collections.defaultdict(list)
    for _ in range(reps):
        pick = collections.Counter(rng.choice(clusters) for _ in clusters)
        lb = {}
        for f, v in sel.items():
            tot = [(c, pick[b]) for b, c in v if pick[b]]
            n = sum(m for _, m in tot)
            lb[f] = 100 * (1 - sum(c * m for c, m in tot) / n) if n else None
        for a, b in contrasts:
            if lb.get(a) is not None and lb.get(b) is not None:
                boots[f"{a}-{b}"].append(lb[a] - lb[b])
    out = {"loss": {f: round(v, 1) for f, v in loss.items()}, "n": {f: len(v) for f, v in sel.items()}, "contrasts": {}}
    for a, b in contrasts:
        bs = sorted(boots[f"{a}-{b}"])
        if a in loss and b in loss and bs:
            out["contrasts"][f"{a}-{b}"] = {"diff": round(loss[a] - loss[b], 1), "ci": [round(bs[int(0.025 * len(bs))]), round(bs[int(0.975 * len(bs)) - 1])]}
    return out


def main(run: str, set_name: str, by_relation: bool, withs: list[str] | None = None) -> None:
    items = {json.loads(line)["id"]: json.loads(line) for line in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(line) for line in (RES / run / "rows.jsonl").read_text().splitlines()]
    same = ("model", "lens", "bands", "conditions", "read", "positions")
    man = json.loads((RES / run / "manifest.json").read_text())
    for w in withs or []:
        m2 = json.loads((RES / w / "manifest.json").read_text())
        assert all(man.get(k) == m2.get(k) for k in same), f"{w} differs from {run} in {[k for k in same if man.get(k) != m2.get(k)]}"
        r2 = [json.loads(line) for line in (RES / w / "rows.jsonl").read_text().splitlines()]
        assert not {r["id"] for r in rows} & {r["id"] for r in r2}, f"{w} shares items with {run}"
        rows += r2
    rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    conds = list(dict.fromkeys(r["condition"] for r in rows if r["condition"] != "none"))
    rng = random.Random(0)
    out: dict = {"run": run, "with": withs or [], "set": set_name, "facts": {}, "threehop": {}, "numbers": {}}
    for cond in conds:
        rs = [r for r in rows if r["condition"] == cond and (r["family"], r["id"]) in ok]
        fr = [r for r in rs if items[r["id"]]["module"] == "facts"]
        if fr:
            keys = [("start", s) for s in ("P", "M", "T", "all")] + [("half", h) for h in ("A", "B")]
            if by_relation:
                keys += [("relation", x) for x in sorted({items[r["id"]]["relation"] for r in fr})]
            for kind, val in keys:
                sel = collections.defaultdict(list)
                for r in fr:
                    it = items[r["id"]]
                    if kind == "start" and val != "all" and it["start"] != val:
                        continue
                    if it["start"] == "R":  # v2.1's never-named recall (memory finals only) is scored apart, below
                        continue
                    if kind == "half" and it.get("half") != val:
                        continue
                    if kind == "relation" and it["relation"] != val:
                        continue
                    sel[it["final"]].append((f"{it['relation']}:{it['bridge']}", r["correct"]))
                if all(sel[f] for f in "KM"):
                    cell = boot(sel, FACT_CONTRASTS, rng)
                    out["facts"][f"{cond}/{kind}={val}"] = cell
                    print(f"facts {cond:14s} {kind}={val:9s} lost " + " ".join(f"{f} {cell['loss'].get(f, float('nan')):4.0f}" for f in "PKMAN")
                          + f"  n {[cell['n'].get(f, 0) for f in 'PKMAN']}  " + "  ".join(f"{k} {v['diff']:+.0f} {v['ci']}" for k, v in cell["contrasts"].items()))  # fmt: skip
        rr = [r for r in fr if items[r["id"]]["start"] in "MR"]
        if any(items[r["id"]]["start"] == "R" for r in rr):  # v2.1 (amendment 35): RF - MF, the bridge never named vs named once
            sel = collections.defaultdict(list)
            for r in rr:
                it = items[r["id"]]
                if it["final"] in "MAN":
                    sel[it["start"] + it["final"]].append((f"{it['relation']}:{it['bridge']}", r["correct"]))
            cell = boot(sel, [("R" + f, "M" + f) for f in "MAN"], rng)
            out["facts"][f"{cond}/never_named"] = cell
            print(f"facts {cond:14s} never-named lost " + " ".join(f"{w} {v:.0f}" for w, v in sorted(cell["loss"].items()))
                  + "  " + "  ".join(f"{k} {v['diff']:+.0f} {v['ci']}" for k, v in cell["contrasts"].items()))  # fmt: skip
        tr = [r for r in rs if items[r["id"]]["module"] == "threehop"]
        if tr:
            sel = collections.defaultdict(list)
            for r in tr:
                sel[r["family"]].append((items[r["id"]].get("scene", r["id"]), r["correct"]))
            cell = boot(sel, [(w, "PPP") for w in sorted(sel) if w != "PPP"], rng)
            out["threehop"][cond] = cell
            print(f"threehop {cond:14s} lost " + " ".join(f"{w} {v:.0f}" for w, v in sorted(cell["loss"].items())) + "  vs PPP "
                  + " ".join(f"{k.split('-')[0]} {v['diff']:+.0f} {v['ci']}" for k, v in cell["contrasts"].items()))  # fmt: skip
        nr = [r for r in rs if items[r["id"]]["module"] == "numbers"]
        if nr:
            sel = collections.defaultdict(list)
            for r in nr:
                sel[r["family"].lstrip("n")].append((items[r["id"]].get("scene", r["id"]), r["correct"]))
            cs = [(f"{s}M", f"{s}L") for s in "PKAM"] + [("KR", "PR"), ("AR", "PR"), ("MR", "PR")]
            cs += [("KM", "PM"), ("AM", "PM"), ("KL", "PL"), ("AL", "PL")]  # amendment 57: computed vs read numbers that key a recall / lookup
            cell = boot(sel, cs, rng)
            out["numbers"][cond] = cell
            print(f"numbers {cond:14s} lost " + " ".join(f"{w} {v:.0f}" for w, v in sorted(cell["loss"].items())) + "  "
                  + " ".join(f"{k} {v['diff']:+.0f} {v['ci']}" for k, v in cell["contrasts"].items()))  # fmt: skip
    (RES / "jsuite2_score").mkdir(exist_ok=True)
    (RES / "jsuite2_score" / ("+".join([run, *(withs or [])]) + ".json")).write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--set", required=True)
    ap.add_argument("--by-relation", action="store_true")
    ap.add_argument("--with", dest="withs", nargs="+", help="other runs' rows scored with RUN's (see above)")
    a = ap.parse_args()
    main(a.run, a.set, a.by_relation, a.withs)
