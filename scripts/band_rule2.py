"""band_rule2 (Zach, 2026-10-25, amendment 41): the lookup-sparing band rule on a dev sweep. Among windows whose rotated
control keeps every word >= 90% (choose_band's rule), also require the J++ removal to keep both lookups (PP and MP)
>= 80%; pick the most broken memory finals (mean of PM and MM kept). Prints every window and the pick.
python scripts/band_rule2.py SWEEP_RUN"""
import collections, json, sys
from pathlib import Path
rows = [json.loads(l) for l in (Path(__file__).resolve().parents[1] / "results" / "ablate_v2" / sys.argv[1] / "rows.jsonl").open()]
ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
acc = collections.defaultdict(lambda: [0, 0])
for r in rows:
    if r["condition"] != "none" and (r["family"], r["id"]) in ok:
        a = acc[(r["band"], r["condition"], r["family"])]
        a[0] += r["correct"]
        a[1] += 1
kept = lambda b, c, w: 100 * acc[(b, c, w)][0] / max(1, acc[(b, c, w)][1])  # noqa: E731
best = None
for b in sorted({k[0] for k in acc}, key=lambda b: int(b.split("-")[0].lstrip("L"))):
    rot = min(kept(b, "paper10_rot", w) for w in ("PP", "MP", "PM", "MM"))
    look = min(kept(b, "paper10", w) for w in ("PP", "MP"))
    mem = (kept(b, "paper10", "PM") + kept(b, "paper10", "MM")) / 2
    ok_ = rot >= 90 and look >= 80
    print(f"{b:8s} rot min {rot:4.0f}  lookups min {look:4.0f}  memory mean {mem:4.0f}  {'eligible' if ok_ else ''}")
    if ok_ and (best is None or mem < best[1]):
        best = (b, mem)
print("PICK", best[0] if best else None)
