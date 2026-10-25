"""profile_pick (Zach, 2026-10-25, amendment 42): a test band from a dev depth profile (scripts/profile_score.py):
among bands where the rotated removal costs <= 10 points on every final (P, K, M), the largest J-specific M - K
(J++ removal's M - K minus the logit-lens removal's), ties to the larger J++ M - K. Prints the band ("A-B").
python scripts/profile_pick.py RUN"""
import json, sys
from pathlib import Path
d = json.loads((Path(__file__).resolve().parents[1] / "results" / "ablate_v2" / "profile" / f"{sys.argv[1]}.json").read_text())
best = None
for b, x in d["bands"].items():
    if not all(c in x for c in ("paper10", "paper10_rot", "unembed10")):
        continue
    if max(x["paper10_rot"]["loss"].values()) > 10:
        continue
    key = (x["paper10"]["M-K"] - x["unembed10"]["M-K"], x["paper10"]["M-K"])
    if best is None or key > best[0]:
        best = (key, b)
print(best[1].lstrip("L") if best else "")
