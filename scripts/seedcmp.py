"""Amendment 29 A: each start's M - P and K - M on seed 2302 against seed 2301 (within 10 points)."""
import json, sys
a = json.load(open(f"results/ablate_v2/jsuite_score/{sys.argv[1]}.json"))["cells"]
b = json.load(open(f"results/ablate_v2/jsuite_score/{sys.argv[2]}.json"))["cells"]
for s in ("P", "M", "T", "all"):
    for c in ("M-P", "K-M"):
        x, y = a[s + "/paper10"]["contrasts"][c]["diff"], b[s + "/paper10"]["contrasts"][c]["diff"]
        verdict = "within 10" if abs(y - x) <= 10 else "OUTSIDE 10"
        print(f"start {s:3s} {c}: seed 2301 {x:+6.1f}  seed 2302 {y:+6.1f}  diff {y - x:+5.1f}  {verdict}")
