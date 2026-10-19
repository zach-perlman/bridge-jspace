"""Phone-sized figure: the J-space part's concentration per family, wording A vs B (parts_A8_v1, parts_B8_v1). python scripts/suite_split_mobile_figure.py OUT.png"""

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = "/workspace/bridge-jspace/results/suite_split"
ORDER = [
    ("BL", "lookup"),
    ("RL", "lookup"),
    ("NAMES", "lookup"),
    ("BLR", "lookup → recall"),
    ("BRL", "recall → lookup"),
    ("BR", "recall"),
    ("RR", "recall"),
]
runs = [("parts_A8_v1", "wording A", "#2a78d6", -0.15), ("parts_B8_v1", "wording B", "#eb6834", 0.15)]
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
fig, ax = plt.subplots(figsize=(6, 7.5))
n = len(ORDER)
for run, label, colour, off in runs:
    s = json.load(open(f"{R}/{run}/summary.json"))["families"]
    first = True
    for i, (f, _) in enumerate(ORDER):
        y = n - 1 - i + off
        v = s.get(f, {})
        if "frac" not in v:
            ax.text(0.05, y, "no usable layers", color=MUTED, fontsize=8, va="center")
            continue
        c, lo, hi = v["frac"]["jspace"]["concentration"]
        ax.plot([lo, hi], [y, y], color=colour, lw=2.5, solid_capstyle="round", zorder=2)
        ax.plot([c], [y], "o", color=colour, ms=8, zorder=3, label=label if first else None)
        first = False
ax.axvline(1, color=MUTED, ls="--", lw=1)
ax.axvline(2, color=INK, ls=":", lw=1)
tr = ax.get_xaxis_transform()
ax.text(1.03, 0.005, "its size", color=MUTED, fontsize=9, ha="left", va="bottom", transform=tr)
ax.text(2.03, 0.005, "'inside'\nif above", color=INK, fontsize=9, ha="left", va="bottom", transform=tr)
ax.set_yticks(range(n)[::-1], [f"{f}\n({u})" for f, u in ORDER], color=INK, fontsize=10)
ax.set_xlim(0, 2.4)
ax.set_xlabel("J-space part's effect ÷ effect its size predicts\n(95% CI, 150 scenes per family)", color=MUTED)
ax.set_title(
    "Qwen3.6-27B: lookup-used bridges get under their share,\nrecall-used a bit over; none reach 2×",
    loc="left",
    color=INK,
    fontsize=11,
    pad=12,
)
ax.grid(axis="x", color=GRID, zorder=0)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="upper right", fontsize=10)
fig.tight_layout()
fig.savefig(sys.argv[1], dpi=200)
print("wrote", sys.argv[1])
