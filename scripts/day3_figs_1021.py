"""Day 3 figures (Zach, 2026-10-21). Fig A: the knock-out's depth profile on held-out items (ctrl_v8), Qwen3.6-27B vs
Gemma 4 31B-it. Fig B: lens writes on the 27B (write_max wm2_full2_v2, scored by c2_graded). Run from the repo root."""

import collections
import json
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("figures/day3_1021")
OUT.mkdir(parents=True, exist_ok=True)
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
LOOKUP, MEMORY, CONTROL, BAND = "#2a78d6", "#eb6834", "#8d8c88", "#ecebe7"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "font.family": "DejaVu Sans"})  # fmt: skip
WORDS = [("PP", LOOKUP, "-", "o", "P→P"), ("MP", LOOKUP, "--", "s", "M→P"),
         ("PM", MEMORY, "-", "o", "P→M"), ("MM", MEMORY, "--", "s", "M→M")]  # fmt: skip


def profile(run: str):
    rows = [json.loads(x) for x in Path(f"results/ablate_v2/{run}/rows.jsonl").read_text().splitlines()]
    acc, n = collections.defaultdict(list), collections.Counter()
    for r in rows:
        if r["condition"] == "none":
            n[r["family"]] += 1
        elif r["kind"] == "clean":
            acc[(r["band"], r["condition"], r["family"])].append(r["correct"])
    bands = sorted({k[0] for k in acc if k[0].count("-") == 1}, key=lambda b: int(b[1:].split("-")[0]))
    widths = [int(b.split("-")[1]) - int(b[1:].split("-")[0]) + 1 for b in bands]
    bands = [b for b, w in zip(bands, widths, strict=True) if w == max(set(widths), key=widths.count)]
    a = {(b, c, w): 100 * statistics.mean(v) for (b, c, w), v in acc.items()}
    return bands, a, n


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# ---- Fig A: depth profiles, 27B vs Gemma, held-out ctrl_v8
panels = [("Qwen3.6-27B (64 layers)", "ctrl_sweep_v1", 64, (32, 40), "chosen band 32–40"),
          ("Gemma 4 31B-it (60 layers)", "gemma4itf_ctrl_sweep_v1", 60, (48, 56), "chosen band 48–56")]  # fmt: skip
fig, axes = plt.subplots(1, 2, figsize=(11, 4.9), sharey=True)
for ax, (title, run, nl, (lo, hi), blabel) in zip(axes, panels, strict=True):
    style(ax)
    bands, a, n = profile(run)
    x = [(int(b[1:].split("-")[0]) + int(b.split("-")[1])) / 2 / nl for b in bands]
    ax.axvspan(lo / nl, (hi + 1) / nl, color=BAND, zorder=0)
    ax.text((lo + hi + 1) / 2 / nl, 109, blabel, ha="center", fontsize=8.5, color=INK2)
    for w, col, ls, mk, name in WORDS:
        ys = [a.get((b, "paper10", w)) for b in bands]
        ax.plot(x, ys, color=col, linestyle=ls, marker=mk, markersize=4.5, linewidth=2, label=name, zorder=3)
    ctrl = [min(a.get((b, "paper10_rot", w), 100) for w, *_ in WORDS) for b in bands]
    ax.plot(
        x, ctrl, color=CONTROL, linewidth=1.5, marker="o", markersize=3, label="rotated control (lowest word)", zorder=2
    )
    ns = "/".join(str(n[w]) for w, *_ in WORDS)
    ax.set_title(f"{title}   n = {ns} per chain", loc="left", fontsize=10.5, pad=18)
    ax.set_xlim(0, 1)
    ax.set_ylim(-3, 114)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel("depth of the 9-layer window (fraction of the model's layers)")
axes[0].set_ylabel("accuracy under the knock-out (%)")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.01, 0.865), ncol=5, frameon=False, fontsize=9)
fig.suptitle("Held-out items: the 27B keeps lookups (blue) and loses memory steps (orange) in its middle layers;\n"
             "Gemma loses both from ~40% depth on, while the same-size random control is untouched",
             x=0.01, y=0.985, ha="left", fontsize=11.5)  # fmt: skip
fig.text(0.01, 0.01, "ctrl_v8 (the band-selection set; never the test set). Top-10 J-lens directions removed at every position "
         "(the answer's clean top-10 kept), 9-layer windows sliding by 4. One run, one data seed, unverified.\n"
         "Gemma's breakdown is under diagnosis tonight: the knock-out also edits position 0 (Gemma's BOS attention sink).",
         fontsize=7.5, color=INK2)  # fmt: skip
fig.subplots_adjust(left=0.06, right=0.99, top=0.70, bottom=0.17, wspace=0.08)
fig.savefig(OUT / "figA_depth_27b_vs_gemma.png", dpi=200)

# ---- Fig B: lens writes on the 27B, by where the bridge comes from and what the last step does
c2 = json.loads(Path("results/write_max/c2_graded/wm2_full2_v2.json").read_text())["families"]
groups = [("stated in the prompt", [("PP", "P→P"), ("PM", "P→M")]), ("computed", [("CP", "C→P"), ("CM", "C→M")]),
          ("recalled from memory", [("MP", "M→P"), ("MM", "M→M")])]  # fmt: skip
fig, ax = plt.subplots(figsize=(8.4, 5.0))
style(ax)
x, ticks = 0.0, []
for gname, members in groups:
    xs = []
    for fam, name in members:
        d = c2[fam]
        cv = 100 * (d.get("cv_own_direction") or 0)
        best = d.get("own_direction") or {}
        col = LOOKUP if fam.endswith("P") else MEMORY
        ax.bar(x, cv, 0.75, color=col, edgecolor=col, linewidth=1.5, zorder=2)
        if best:
            ax.errorbar(x + 0.27, 100 * best["flips"], yerr=[[100 * (best["flips"] - best["ci"][0])], [100 * (best["ci"][1] - best["flips"])]],
                        fmt="D", color=INK2, markersize=4, linewidth=1, capsize=2, zorder=3)  # fmt: skip
        ax.text(x, -2.5, name, ha="center", va="top", fontsize=9.5, color=INK2)
        ax.text(x, cv + 1.2, f"{cv:.0f}", ha="center", fontsize=9, color=INK)
        xs.append(x)
        x += 1
    ticks.append((statistics.mean(xs), gname))
    x += 0.7
ax.set_xticks([t for t, _ in ticks], [g for _, g in ticks])
ax.tick_params(axis="x", pad=24, length=0)
for lab in ax.get_xticklabels():
    lab.set_fontweight("bold")
ax.set_ylim(-1, 62)
ax.set_ylabel("answers switched by the bridge's own lens direction (%)")
handles = [plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=MEMORY),
           plt.Line2D([], [], marker="D", color=INK2, linestyle="", markersize=4)]  # fmt: skip
ax.legend(handles, ["last step looks it up in the prompt", "last step recalls from memory",
                    "best single cell, 95% CI (inflated by selection)"], frameon=False, loc="upper left", fontsize=9)  # fmt: skip
ax.set_title("Lens writes (Qwen3.6-27B): a stated or computed bridge is written only when a recall uses it;\n"
             "a recalled bridge is written either way, so C2 as pre-registered (M→M ≥ 3× M→P) fails", loc="left", fontsize=10.5)  # fmt: skip
fig.text(0.01, 0.01, "Bars: the best gated write of the bridge's own lens direction (add / swap; layers 28–40; question or final positions),\n"
         "chosen on half the bridge entities and scored on the other half (mean of 200 halvings). Full v8 pools (482 cases, 72–87 per word);\n"
         "random-direction controls keep the clean answer on ≥95%. One run, one data seed, unverified.", fontsize=7.5, color=INK2)  # fmt: skip
fig.tight_layout(rect=(0, 0.11, 1, 1))
fig.savefig(OUT / "figB_lens_writes_27b.png", dpi=200)
print("saved", sorted(p.name for p in OUT.iterdir()))
