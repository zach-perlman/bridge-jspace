"""All task variants across models (2026-10-22): the knock-out at each model's held-out-chosen band, by chain type (two- and
three-step), by prompt format, by difficulty level, and by step (each step asked alone). Loss = accuracy lost beyond the
same-size random control (control accuracy minus knock-out accuracy, on the same items). Run from the box repo root."""
import collections
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, "."); sys.path.insert(0, "src")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from scripts import tasks_v2 as T

R = Path("results/ablate_v2")
MODELS = [("Qwen3.6-27B", "", "#0072B2"), ("Qwen3-32B", "qwen3_32b_", "#009E73"), ("Muse Glimmer 30B", "muse30_", "#CC79A7")]
STEPS = {"": ("full2_ko_steps_v1", "full3_ko_steps_v2"), "qwen3_32b_": ("qwen3_32b_full2_ko_steps_v1", "qwen3_32b_full3_ko_steps_v1"),
         "muse30_": ("muse30_full2_ko_steps_v1", "muse30_full3_ko_steps_v1")}
ITEMS = {it["id"]: it for s in ("full_v8", "full_v8b") for it in T.load(s)}
ROWS_TWO = [("P→P", "PP"), ("M→P", "MP"), ("C→P", "CP"), ("P→M", "PM"), ("M→M", "MM"), ("C→M", "CM")]
ROWS_THREE = [("P→P→P", "PPP"), ("M→P→P", "MPP"), ("P→M→P", "PMP"), ("M→M→P", "MMP"), ("P→P→M", "PPM"), ("M→P→M", "MPM")]
LOOK, MEM = ("PP", "MP", "CP"), ("PM", "MM", "CM")
FORMATS = ["prose", "chat", "document", "json", "table", "code"]


def per_item(run, band, kinds=("clean",)):
    """{(kind, family, id): {condition: correct}} at one band (and the unedited)."""
    out = collections.defaultdict(dict)
    for line in (R / run / "rows.jsonl").open():
        r = json.loads(line)
        if r["kind"] in kinds and (r["band"] == band or r["condition"] == "none"):
            out[(r["kind"], r["family"], r["id"])][r["condition"]] = r["correct"]
    return out


def loss(cells):  # points lost beyond the random control on the same items
    pairs = [(c["paper10_rot"], c["paper10"]) for c in cells if "paper10" in c and "paper10_rot" in c]
    return (100 * (statistics.mean(a for a, _ in pairs) - statistics.mean(b for _, b in pairs)), len(pairs)) if pairs else (None, 0)


data = {}
for name, p, _ in MODELS:
    band = json.loads((R / "c1_v2" / f"{p}full2_ko_v1.json").read_text())["middle"]
    two, three = per_item(f"{p}full2_ko_v1", band), per_item(f"{p}full3_ko_v1", band)
    d = {"band": band, "chain": {}, "format": {}, "level": {}, "steps": {}}
    for _, fam in ROWS_TWO:
        d["chain"][fam] = loss([v for (k, f, i), v in two.items() if f == fam])
    for _, fam in ROWS_THREE:
        d["chain"][fam] = loss([v for (k, f, i), v in three.items() if f == fam])
    for key, groups in (("format", FORMATS), ("level", [0, 1, 2, 3])):
        for g in groups:
            per = {fam: loss([v for (k, f, i), v in two.items() if f == fam and ITEMS[i][key] == g])[0] for fam in LOOK + MEM}
            if all(x is not None for x in per.values()):
                n = sum(1 for (k, f, i) in two if ITEMS[i][key] == g)
                d[key][g] = (statistics.mean(per[f] for f in MEM) - statistics.mean(per[f] for f in LOOK), n)
    cats = collections.defaultdict(list)
    for run in STEPS[p]:
        rows = per_item(run, band, kinds=("step1", "step2", "step3"))
        for (kind, fam, i), v in rows.items():
            k = int(kind[-1])
            src = ITEMS[i]["steps"][k - 1]["source"]
            cat = {"P": "lookup", "C": "computed"}.get(src, "recall, first step" if k == 1 else "recall, later step")
            cats[cat].append(v)
    d["steps"] = {c: loss(v) for c, v in cats.items()}
    data[name] = d
Path("results/cross_model").mkdir(parents=True, exist_ok=True)
Path("results/cross_model/variants_1022.json").write_text(json.dumps(data, indent=2, default=str) + "\n")

# ---------------- figure
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(14.5, 9.8))
gs = fig.add_gridspec(3, 2, width_ratios=[1.05, 1.6], hspace=0.62, wspace=0.22, left=0.1, right=0.98, top=0.79, bottom=0.1)
# A: heatmap
ax = fig.add_subplot(gs[:, 0])
rows = ROWS_TWO + ROWS_THREE
cmap = LinearSegmentedColormap.from_list("o", ["#fcfcfb", "#fbe3d4", "#f5a273", "#e05d1f", "#9c3a0d"])
for r, (lab, fam) in enumerate(rows):
    for c, (name, _, _) in enumerate(MODELS):
        v, n = data[name]["chain"][fam]
        val = 0 if v is None else max(v, 0)
        ax.add_patch(plt.Rectangle((c, r), 0.96, 0.92, color=cmap(min(val, 45) / 45)))
        txt = "–" if v is None else f"{v:.0f}"
        ax.text(c + 0.48, r + 0.42, txt, ha="center", va="center", fontsize=11, color=INK if val < 30 else "white", fontweight="bold")
        ax.text(c + 0.48, r + 0.75, f"n={n}", ha="center", va="center", fontsize=6.5, color=INK2 if val < 30 else "white")
ax.set_xlim(-0.05, 3)
ax.set_ylim(len(rows) + 0.05, -0.15)
ax.set_xticks([c + 0.48 for c in range(3)], [f"{n}\n{data[n]['band'].replace('L', 'layers ')}" for n, _, _ in MODELS], fontsize=9)
ax.xaxis.tick_top()
ax.set_yticks([r + 0.46 for r in range(len(rows))], [lab for lab, _ in rows], fontsize=10)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
for y, txt in ((0, "2 steps, ends in a lookup"), (3, "2 steps, ends in a recall"), (6, "3 steps, ends in a lookup"), (10, "3 steps, ends in a recall")):
    ax.text(-0.98, y + 0.06, txt, fontsize=8.3, color=INK2, style="italic", va="bottom", transform=ax.transData, bbox=dict(facecolor=SURFACE, edgecolor="none", pad=0.5))
    if y:
        ax.axhline(y - 0.04, color=INK2, lw=0.8, xmin=0, xmax=1)
ax.set_title("A. Accuracy lost to the knock-out, beyond the\nrandom control (points), by chain type", loc="left", fontsize=10.5, pad=42)


def dots(ax, key, groups, labels, title):
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID)
    ax.set_axisbelow(True)
    for m, (name, _, col) in enumerate(MODELS):
        xs, ys = [], []
        for gi, g in enumerate(groups):
            v = data[name][key].get(g) if key != "level" else data[name][key].get(g)
            if v is None:
                continue
            xs.append(gi + (m - 1) * 0.17)
            ys.append(v[0])
        ax.plot(xs, ys, "o-", color=col, lw=1.2, ms=6.5, label=name, alpha=0.95)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.axhline(30, color=INK2, lw=0.8, ls="--")
    ax.text(len(groups) - 0.55, 31, "C1 bar (30)", fontsize=7.5, color=INK2, ha="right")
    ax.set_xticks(range(len(groups)), labels)
    ax.set_ylim(-15, 62)
    ax.set_ylabel("memory minus lookup\n(points)", fontsize=8.5)
    ax.set_title(title, loc="left", fontsize=10.5)


ax = fig.add_subplot(gs[0, 1])
dots(ax, "format", FORMATS, FORMATS, "B. The memory-vs-lookup gap by prompt format (two-step chains)")
ax.legend(frameon=False, ncol=3, fontsize=8.5, loc="upper right", bbox_to_anchor=(1.0, 1.36))
ax = fig.add_subplot(gs[1, 1])
dots(ax, "level", [0, 1, 2, 3], ["level 0 (easiest)", "level 1", "level 2", "level 3 (hardest)"], "C. The memory-vs-lookup gap by difficulty level (two-step chains)")
# D: steps
ax = fig.add_subplot(gs[2, 1])
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID)
ax.set_axisbelow(True)
CATS = [("lookup", "prompt lookup", "#2a78d6"), ("computed", "computed (typo, translation)", "#8d8c88"),
        ("recall, first step", "recall, first step", "#f5a273"), ("recall, later step", "recall, later step", "#e05d1f")]
for m, (name, _, _) in enumerate(MODELS):
    for j, (cat, lab, col) in enumerate(CATS):
        v, n = data[name]["steps"].get(cat, (None, 0))
        if v is None:
            continue
        x = m * 5 + j
        ax.bar(x, v, 0.85, color=col, label=lab if m == 0 else None)
        ax.text(x, max(v, 0) + 1.2, f"{v:.0f}", ha="center", fontsize=8)
ax.axhline(0, color=INK2, lw=0.8)
ax.set_xticks([m * 5 + 1.5 for m in range(3)], [n for n, _, _ in MODELS])
ax.set_ylabel("lost beyond control\n(points)", fontsize=8.5)
ax.set_ylim(-5, 55)
ax.set_title("D. Each step asked on its own (two- and three-step chains), by what the step does", loc="left", fontsize=10.5)
ax.legend(frameon=False, ncol=4, fontsize=8, loc="upper right")
fig.suptitle("The knock-out across every task variant: the 27B separates memory recalls from lookups everywhere,\n"
             "Qwen3-32B does so more weakly, and Muse barely at all", x=0.01, y=0.99, ha="left", fontsize=12.5)
fig.text(0.01, 0.012, "Top-10 J-lens directions removed at every position at each model's middle band (chosen on held-out data), the answer protected; "
         "loss = random-control accuracy minus knock-out accuracy on the same items.\nB, C: mean loss of P→M, M→M, C→M minus mean loss of P→P, M→P, C→P "
         "within each format / level (20-60 items per word per cell). Our J++ for Qwen3-32B and Muse, the published J++ for the 27B. One data seed; unverified.",
         fontsize=7.5, color=INK2)
out = Path("figures/cross_model"); out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "variants_by_model_1022.png", dpi=170)
print(json.dumps({n: {"steps": d["steps"], "format": d["format"], "level": d["level"]} for n, d in data.items()}, default=str)[:1500])
