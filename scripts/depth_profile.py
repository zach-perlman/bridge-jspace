"""depth_profile (Zach, 2026-10-25): from a dev band sweep (paper10 / rot on PP MP PM MM), per window: relative depth,
lookups kept (mean of PP, MP), memory finals kept (mean of PM, MM), their gap (lookups - memory = the sweep's
specificity), and the rotation's worst word. python scripts/depth_profile.py SWEEP_RUN N_LAYERS"""
import collections, json, sys
from pathlib import Path
run, n = sys.argv[1], int(sys.argv[2])
rows = [json.loads(l) for l in (Path(__file__).resolve().parents[1] / "results" / "ablate_v2" / run / "rows.jsonl").open()]
ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
acc = collections.defaultdict(lambda: [0, 0])
for r in rows:
    if r["condition"] != "none" and (r["family"], r["id"]) in ok:
        a = acc[(r["band"], r["condition"], r["family"])]; a[0] += r["correct"]; a[1] += 1
k = lambda b, c, w: 100 * acc[(b, c, w)][0] / max(1, acc[(b, c, w)][1])  # noqa: E731
for b in sorted({x[0] for x in acc}, key=lambda b: int(b.split("-")[0].lstrip("L"))):
    lo, hi = (int(x) for x in b.lstrip("L").split("-"))
    look, mem = (k(b, "paper10", "PP") + k(b, "paper10", "MP")) / 2, (k(b, "paper10", "PM") + k(b, "paper10", "MM")) / 2
    rot = min(k(b, "paper10_rot", w) for w in ("PP", "MP", "PM", "MM"))
    print(f"{b:8s} depth {100 * lo / n:3.0f}-{100 * hi / n:3.0f}%  lookups {look:4.0f}  memory {mem:4.0f}  gap {look - mem:+4.0f}  rot min {rot:4.0f}")
