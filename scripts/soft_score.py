"""soft_score (Zach, 2026-10-25, TA note: sampling): a v2 facts knock-out scored by the model's probability on the right
answer instead of its candidate pick. On items right unedited (cand2, the main scorer's eligibility), points lost =
100 x (mean p unedited - mean p edited), p = exp(logp) of the answer's first token: the expected accuracy of that
token under temperature-1 sampling. Per condition: losses on finals P K M (all starts but R) and M - K, 95% bootstrap
over bridges (seed 0), beside the candidate-pick M - K. CPU only, existing rows.
python scripts/soft_score.py RUN [RUN ...] --set jsuite_v2_test_chat"""
import argparse, collections, json, math, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(runs, set_name):
    items = {json.loads(x)["id"]: json.loads(x) for x in (ROOT / "data" / "tasks_v2" / set_name / "items.jsonl").read_text().splitlines()}
    for run in runs:
        rows = [json.loads(x) for x in (ROOT / "results" / "ablate_v2" / run / "rows.jsonl").read_text().splitlines()]
        rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items and items[r["id"]].get("module") == "facts"
                and items[r["id"]]["start"] in "PMT"]  # fmt: skip
        base = {(r["family"], r["id"]): r for r in rows if r["condition"] == "none"}
        ok = {k for k, r in base.items() if r["correct"]}
        conds = [c for c in dict.fromkeys(r["condition"] for r in rows) if c != "none"]
        out = {}
        for c in conds:
            cell = collections.defaultdict(list)  # final -> [(bridge, soft loss, hard loss)]
            for r in rows:
                k = (r["family"], r["id"])
                if r["condition"] != c or k not in ok:
                    continue
                it = items[r["id"]]
                soft = 100 * (math.exp(base[k]["logp"]) - math.exp(r["logp"]))
                cell[it["final"]].append((f"{it['relation']}:{it['bridge']}", soft, 100 * (1 - r["correct"])))
            if not cell["M"] or not cell["K"]:
                continue
            mean = lambda v, i: sum(x[i] for x in v) / len(v)  # noqa: E731
            rng, clusters = random.Random(0), sorted({b for f in "MK" for b, _, _ in cell[f]})
            bs = []
            for _ in range(1000):
                pick = collections.Counter(rng.choice(clusters) for _ in clusters)
                m = [(s, pick[b]) for b, s, _ in cell["M"] if pick[b]]
                k = [(s, pick[b]) for b, s, _ in cell["K"] if pick[b]]
                if m and k:
                    bs.append(sum(s * w for s, w in m) / sum(w for _, w in m) - sum(s * w for s, w in k) / sum(w for _, w in k))
            bs.sort()
            out[c] = {"soft": {f: round(mean(v, 1), 1) for f, v in cell.items()}, "hard": {f: round(mean(v, 2), 1) for f, v in cell.items()},
                      "soft_M-K": round(mean(cell["M"], 1) - mean(cell["K"], 1), 1), "soft_ci": [round(bs[25]), round(bs[974])],
                      "hard_M-K": round(mean(cell["M"], 2) - mean(cell["K"], 2), 1), "n": {f: len(v) for f, v in cell.items()}}  # fmt: skip
            print(f"{run[:52]:52s} {c:14s} soft M-K {out[c]['soft_M-K']:+6.1f} {out[c]['soft_ci']}  hard M-K {out[c]['hard_M-K']:+6.1f}  "
                  f"soft lost P {out[c]['soft'].get('P', float('nan')):5.1f} K {out[c]['soft']['K']:5.1f} M {out[c]['soft']['M']:5.1f}")  # fmt: skip
        (ROOT / "results" / "ablate_v2" / "soft_score").mkdir(exist_ok=True)
        (ROOT / "results" / "ablate_v2" / "soft_score" / f"{run}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--set", default="jsuite_v2_test_chat")
    a = ap.parse_args()
    main(a.runs, a.set)
