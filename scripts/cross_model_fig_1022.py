"""Cross-model C1 and aligned-band C2 (2026-10-22). Run from the box repo root. Unverified; one data seed."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = Path("results")
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
LOOK, MEM = "#2a78d6", "#eb6834"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "font.family": "DejaVu Sans"})
models = [("Qwen3.6-27B\n(hybrid)", "", "wm2_full2_aligned_v1", "L48-60"), ("Qwen3-32B\n(dense)", "qwen3_32b_", "qwen3_32b_wm2_full2_aligned_v1", "L40-52"),
          ("Muse Glimmer 30B\n(Meta)", "muse30_", "muse30_wm2_full2_aligned_v1", "L22-32")]
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.8))
for ax in axes:
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID)
    ax.set_axisbelow(True)
# C1
ax = axes[0]
for i, (lab, p, _, _) in enumerate(models):
    c = json.loads((R / "ablate_v2/c1_v2" / f"{p}full2_ko_v1.json").read_text())
    loss, band = c["rule"]["loss"], c["middle"]
    look = [100 * loss[w] for w in ("PP", "MP", "CP")]
    mem = [100 * loss[w] for w in ("PM", "MM", "CM")]
    x0 = i * 3.2
    ax.bar(x0, sum(look) / 3, 1.1, color=LOOK, label="lookup-final (P→P, M→P, C→P)" if i == 0 else None)
    ax.bar(x0 + 1.25, sum(mem) / 3, 1.1, color=MEM, label="memory-final (P→M, M→M, C→M)" if i == 0 else None)
    for j, v in enumerate(look):
        ax.plot(x0 - 0.3 + 0.3 * j, v, "o", color=INK2, ms=3.5)
    for j, v in enumerate(mem):
        ax.plot(x0 + 0.95 + 0.3 * j, v, "o", color=INK2, ms=3.5)
    gap = 100 * c["rule"]["gap"]
    ax.text(x0 + 0.62, max(mem + look) + 3, f"gap {gap:.0f}\n{'holds' if c['rule']['C1_graded_holds'] else 'fails'}", ha="center", fontsize=9)
    ax.text(x0 + 0.62, -6, f"{lab}\n{band}", ha="center", va="top", fontsize=9)
ax.axhline(0, color=INK2, lw=0.8)
ax.set_xticks([])
ax.set_ylim(-2, 62)
ax.set_ylabel("accuracy lost under the knock-out (points)")
ax.set_title("C1: knocking out the top-10 J-lens directions\nhurts memory steps, not lookups — strongly only on the 27B", loc="left", fontsize=10.5)
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
# C2 aligned
ax = axes[1]
for i, (lab, p, run, band) in enumerate(models):
    n = json.loads((R / "write_max/c2_narrow" / f"{run}.json").read_text())
    g = json.loads((R / "write_max/c2_graded" / f"{run}.json").read_text())["families"]
    cv = {f: 100 * (g[f]["cv_own_direction"] or 0) for f in ("PP", "MP", "CP", "PM", "MM", "CM")}
    x0 = i * 3.2
    ax.bar(x0, sum(cv[w] for w in ("PP", "MP", "CP")) / 3, 1.1, color=LOOK, label="lookup-final" if i == 0 else None)
    ax.bar(x0 + 1.25, sum(cv[w] for w in ("PM", "MM", "CM")) / 3, 1.1, color=MEM, label="memory-final" if i == 0 else None)
    for j, w in enumerate(("PP", "MP", "CP")):
        ax.plot(x0 - 0.3 + 0.3 * j, cv[w], "o", color=INK2, ms=3.5)
    for j, w in enumerate(("PM", "MM", "CM")):
        ax.plot(x0 + 0.95 + 0.3 * j, cv[w], "o", color=INK2, ms=3.5)
    rel = json.loads((R / "write_max/c2_graded" / f"{run}.json").read_text())
    verdicts = f"graded {'✓' if rel['rule']['C2_graded_holds'] else '✗'} · relative {'✓' if rel['rule_relative']['verdict'] == 'HOLDS' else '✗'}\nC2′ {'✓' if n['verdict'] == 'HOLDS' else '✗'}"
    ax.text(x0 + 0.62, -6, f"{lab}\n{band} final\n{verdicts}", ha="center", va="top", fontsize=9)
ax.axhline(0, color=INK2, lw=0.8)
ax.set_xticks([])
ax.set_ylim(-2, 95)
ax.set_ylabel("answers switched by writing the bridge's lens direction (%)")
ax.set_title("C2 at layers where pasting the full state works (≥50% for every word):\nlens writes move memory-final answers more than lookups —\nclearly on Qwen3-32B and Muse, weakly on the 27B", loc="left", fontsize=10.5)
ax.legend(frameon=False, fontsize=8.5, loc="upper left")
fig.text(0.01, 0.01, "Bars: mean over the three words; dots: each word, left to right P-, M-, C-start. C1: test set, full_v8, each model's band chosen on held-out data. C2: cross-validated best "
         "gated lens write (add / swap)\nat the aligned band (copy-sweep rule fixed beforehand). One data seed; unverified; Muse and Qwen3-32B use our own J++ fits, the 27B the published J++.",
         fontsize=7.3, color=INK2)
fig.subplots_adjust(left=0.06, right=0.99, top=0.82, bottom=0.29, wspace=0.18)
out = Path("figures/archive/cross_model"); out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "c1_c2_by_model_1022.png", dpi=180)
print("saved")
