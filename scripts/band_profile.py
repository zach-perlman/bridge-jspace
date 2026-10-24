# Zach (2026-10-24): python scripts/band_profile.py SWEEP_RUN (descriptive; the pre-registered band stays the confirmatory test).
"""Per-band gap profile from an ablate_v2 dev sweep (paper10 / paper10_rot on PP MP PM MM): points lost per word, the
memory-final minus prompt-final gap, the same under the rotation, and their difference."""
import json, sys
s = json.load(open(f"results/ablate_v2/{sys.argv[1]}/summary.json"))
cells = s.get("cells") or s
W = ("PP", "MP", "PM", "MM")
print("band    | lost PP  MP  PM  MM |  gap | rot PP  MP  PM  MM | rot gap | J-specific")
for b, f in cells.items():
    p = {w: 100 * (1 - f[w + "/clean"]["paper10"]["accuracy"]) for w in W}
    r = {w: 100 * (1 - f[w + "/clean"]["paper10_rot"]["accuracy"]) for w in W}
    g = (p["PM"] + p["MM"]) / 2 - (p["PP"] + p["MP"]) / 2
    gr = (r["PM"] + r["MM"]) / 2 - (r["PP"] + r["MP"]) / 2
    print(f"{b:7s} | " + " ".join(f"{p[w]:3.0f}" for w in W) + f" | {g:+4.0f} |    " + " ".join(f"{r[w]:3.0f}" for w in W) + f" |  {gr:+4.0f}  |  {g - gr:+4.0f}")
f0 = cells[next(iter(cells))]
print("n per word per band:", {w: f0[w + "/clean"]["paper10"]["n"] for w in W})
