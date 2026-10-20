"""Depth figure for ablate_v2 runs (Zach, 2026-10-20): accuracy with the J-space removed, by band, per family, for
paper10 (headline) and omp25, with their controls (rotated removal, rotated dictionary). Reads rows.jsonl, partial or
complete. Colour = what uses the bridge (lookup / recall / countries); line style = where it comes from (given =
solid, recalled = dashed). python depth_fig.py RUN OUT.png"""

import collections
import json
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

run, out = sys.argv[1], sys.argv[2]
rows = [json.loads(line) for line in Path(f"results/ablate_v2/{run}/rows.jsonl").read_text().splitlines()]
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#9aa0a6"
INK, INK2, SURF, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e0"
FAM = {"BL": ("given → looked up (P→P)", BLUE, "-", "o"), "RL": ("recalled → looked up (M→P)", BLUE, "--", "o"),
       "BR": ("given → recalled (P→M)", ORANGE, "-", "s"), "RR": ("recalled → recalled (M→M)", ORANGE, "--", "s"),
       "country-R": ("countries, recalled", AQUA, "--", "D"), "country-B": ("countries, given", AQUA, "-", "D")}  # fmt: skip
acc = collections.defaultdict(list)
for r in rows:
    if r["condition"] != "none":
        acc[(r["band"], r["family"], r["condition"])].append(r["correct"])
n_items = len({(r["family"], r["id"]) for r in rows if r["condition"] == "none"})


def centre(band: str) -> float:
    a, b = band[1:].split("-")
    return (int(a) + int(b)) / 2


bands = sorted({b for b, _, _ in acc if b != "L0-62"}, key=centre)
plt.rcParams.update({"font.size": 9, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK})
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=SURF, sharey=True, gridspec_kw={"wspace": 0.06})
for ax, method in zip(axes, ("paper10", "omp25"), strict=True):
    ax.set_facecolor(SURF)
    for fam, (label, col, ls, mk) in FAM.items():
        xs = [centre(b) for b in bands if acc.get((b, fam, method))]
        ys = [100 * statistics.mean(acc[(b, fam, method)]) for b in bands if acc.get((b, fam, method))]
        if xs:
            ax.plot(xs, ys, color=col, ls=ls, marker=mk, markersize=4, lw=1.8, label=label)
        whole = acc.get(("L0-62", fam, method))
        if whole:
            ax.scatter([66], [100 * statistics.mean(whole)], color=col, marker=mk, s=40, zorder=3)
    ctrl = [k for k in acc if k[2] in (f"{method}_rot", f"{method}_rdict") and k[0] != "L0-62"]
    if ctrl:
        lo = {}
        for b, _, _ in ctrl:
            lo[b] = min(100 * statistics.mean(v) for (bb, _, c), v in acc.items() if bb == b and c in (f"{method}_rot", f"{method}_rdict"))
        xs = sorted(lo, key=centre)
        ax.plot([centre(b) for b in xs], [lo[b] for b in xs], color=GREY, lw=1.4, ls=":", label="controls (lowest family)")
    ax.axvspan(32, 40, color="#f1efe8", zorder=0)
    ax.text(36, 3, "v1 band", ha="center", fontsize=7.5, color=INK2)
    ax.set_xticks([0, 8, 16, 24, 32, 40, 48, 56, 66])
    ax.set_xticklabels(["0", "8", "16", "24", "32", "40", "48", "56", "all"])
    ax.set_xlim(-1, 68)
    ax.set_ylim(-3, 103)
    ax.grid(color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("centre of the 9-layer band removed (layer); 'all' = every layer")
    ax.set_title({"paper10": "paper10: top-10 lens directions (answer kept)",
                  "omp25": "omp25: 25-atom OMP fit"}[method], loc="left", fontsize=9.5, fontweight="bold")  # fmt: skip
axes[0].set_ylabel("accuracy with the J-space removed (%)")
h, lab = axes[0].get_legend_handles_labels()
fig.legend(h, lab, loc="lower left", ncol=4, frameon=False, bbox_to_anchor=(0.005, 0.95), fontsize=8)
fig.suptitle(f"Qwen3.6-27B: where in depth does removing the J-space break each family? ({n_items} items)", x=0.01,
             ha="left", fontsize=11, fontweight="bold", y=1.06)  # fmt: skip
fig.savefig(out, dpi=170, facecolor=SURF, bbox_inches="tight")
print("ok", len(rows), "rows")
