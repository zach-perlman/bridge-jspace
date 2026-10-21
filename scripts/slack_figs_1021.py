"""Two figures for the 2026-10-21 Slack update (27B, full_v8, paper10 knock-out vs its rotated control).
Fig 1: C1 by band, the whole question. Fig 2: each step of a chain alone, at L32-40. 95% intervals: bootstrap over
bridge entities. Run from the repo root on the box."""

import collections
import json
import random
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, "src")
sys.path.insert(0, ".")
from scripts import tasks_v2 as T

OUT = Path("figures/slack_1021")
OUT.mkdir(parents=True, exist_ok=True)
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
LOOKUP, MEMORY, COMPUTED, CONTROL = "#2a78d6", "#eb6834", "#1baf7a", "#8d8c88"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "font.family": "DejaVu Sans"})  # fmt: skip
NAME = lambda w: "→".join(w)  # noqa: E731


def rows_of(run):
    return [json.loads(x) for x in Path(f"results/ablate_v2/{run}/rows.jsonl").read_text().splitlines()]


def loss_ci(pairs, reps=2000, seed=0):
    """pairs: (bridge, loss 0/1/-1). Mean and 95% interval, resampling bridge entities."""
    by = collections.defaultdict(list)
    for b, x in pairs:
        by[b].append(x)
    groups, rng = list(by.values()), random.Random(seed)
    stats = sorted(statistics.mean([x for g in (rng.choice(groups) for _ in groups) for x in g]) for _ in range(reps))
    return statistics.mean(x for _, x in pairs), stats[int(0.025 * reps)], stats[int(0.975 * reps) - 1]


def losses(rows, band, cond, kind, word, keep=None):
    base = {(r["family"], r["id"], r["kind"]): r["correct"] for r in rows if r["condition"] == "none"}
    sel = [r for r in rows if r["band"] == band and r["condition"] == cond and r["kind"] == kind and r["family"] == word
           and (keep is None or r["id"] in keep)]  # fmt: skip
    return [(r["bridge"], int(base[(word, r["id"], kind)]) - int(r["correct"])) for r in sel]


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# ---- Fig 1: C1 by band (whole question)
rows = rows_of("full2_ko_v1")
words = [("PP", LOOKUP), ("MP", LOOKUP), ("PM", MEMORY), ("MM", MEMORY)]
bands = [("L12-20", "layers 12–20"), ("L20-28", "layers 20–28"), ("L32-40", "layers 32–40\n(the pre-set rule band)")]
fig, ax = plt.subplots(figsize=(8.2, 4.8))
style(ax)
width, xt, xl = 0.19, [], []
for gi, (band, label) in enumerate(bands):
    vals = {}
    for wi, (w, col) in enumerate(words):
        x = gi + (wi - 1.5) * (width + 0.02)
        m, lo, hi = loss_ci(losses(rows, band, "paper10", "clean", w))
        r = statistics.mean(v for _, v in losses(rows, band, "paper10_rot", "clean", w))
        vals[w] = m
        ax.bar(x, 100 * m, width, color=col, zorder=2)
        ax.errorbar(x, 100 * m, yerr=[[100 * (m - lo)], [100 * (hi - m)]], color=INK, linewidth=1, capsize=2, zorder=3)
        ax.plot(x, 100 * r, marker="o", markersize=5, color=CONTROL, markeredgecolor=SURFACE, zorder=4)
        ax.text(x, -4, NAME(w), ha="center", va="top", fontsize=8.5, color=INK2)
    gap = (vals["PM"] + vals["MM"]) / 2 - (vals["PP"] + vals["MP"]) / 2
    ax.text(gi, 66, f"gap {100 * gap:+.0f}", ha="center", fontsize=10, color=INK, fontweight="bold")
    xt.append(gi)
    xl.append(label)
ax.set_xticks(xt, xl)
ax.tick_params(axis="x", pad=18, length=0)
ax.set_ylim(-1, 72)
ax.set_ylabel("accuracy lost under the knock-out (points)")
ax.set_title("Qwen3.6-27B: at layers 32–40 the J-space knock-out hurts memory-final questions,\n"
             "not lookup-final ones; at layers 12–20 lookups are hit as hard", loc="left", fontsize=11, pad=26)  # fmt: skip
handles = [plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=MEMORY),
           plt.Line2D([], [], marker="o", color=CONTROL, linestyle="", markersize=5)]  # fmt: skip
ax.legend(handles, ["last step looks up the prompt", "last step recalls from memory", "same-size rotated control"],
          frameon=False, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, fontsize=9)  # fmt: skip
fig.text(0.01, 0.01, "full_v8, whole question. n = 152 / 101 / 152 / 101 items (P→P, M→P, P→M, M→M); 47 / 35 bridge entities.\n"
         "Top-10 J-lens directions removed at every position (answer's clean top-10 kept). 95% intervals over bridge entities.\n"
         "One knock-out run, one data seed. Gap = memory-final minus lookup-final loss. Unverified.", fontsize=7.5, color=INK2)
fig.tight_layout(rect=(0, 0.1, 1, 1))
fig.savefig(OUT / "fig1_c1_by_band.png", dpi=200)

# ---- Fig 2: each step alone, L32-40
two, three = rows_of("full2_ko_steps_v1"), rows_of("full3_ko_steps_v2")
core3 = {it["id"] for it in T.load("full_v8b") if T.stratum(it) == "core"}
chains = [(w, two, None) for w in ("PP", "PM", "MP", "MM", "CP", "CM")] + \
         [(w, three, core3) for w in ("PPP", "PPM", "PMP", "MPP", "MPM", "MMP")]  # fmt: skip
color = {"P": LOOKUP, "M": MEMORY, "C": COMPUTED}
fig, ax = plt.subplots(figsize=(10, 4.8))
style(ax)
x, centers, out = 0.0, [], {}
for w, rows_, keep in chains:
    xs = []
    for k, letter in enumerate(w):
        pairs = losses(rows_, "L32-40", "paper10", f"step{k + 1}", w, keep)
        if not pairs:
            continue
        m, lo, hi = loss_ci(pairs)
        r = statistics.mean(v for _, v in losses(rows_, "L32-40", "paper10_rot", f"step{k + 1}", w, keep))
        out[f"{w}/step{k + 1}"] = {"loss": m, "ci": [lo, hi], "control": r, "n": len(pairs)}
        ax.bar(x, 100 * m, 0.8, color=color[letter], edgecolor=color[letter], linewidth=1.5, zorder=2)
        ax.errorbar(x, 100 * m, yerr=[[100 * (m - lo)], [100 * (hi - m)]], color=INK, linewidth=1, capsize=2, zorder=3)
        ax.plot(x, 100 * r, marker="o", markersize=4.5, color=CONTROL, markeredgecolor=SURFACE, zorder=4)
        xs.append(x)
        x += 1
    centers.append((statistics.mean(xs), NAME(w)))
    x += 0.8
ax.axvline(centers[5][0] + 1.9, color=GRID, linewidth=1)
ax.text(centers[2][0] + 0.5, 66, "two-step chains", ha="center", color=INK2, fontsize=9)
ax.text(centers[8][0] + 0.5, 66, "three-step chains", ha="center", color=INK2, fontsize=9)
ax.set_xticks([c for c, _ in centers], [n for _, n in centers], fontsize=9)
ax.tick_params(axis="x", length=0)
ax.set_ylim(-3, 70)
ax.set_ylabel("accuracy lost, each step asked alone (points)")
ax.set_title("Qwen3.6-27B, layers 32–40: memory steps after the first lose 14–45 points, lookups ≤ 6;\n"
             "first-step recalls (M→ chains) barely move at this depth", loc="left", fontsize=11, pad=26)  # fmt: skip
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (LOOKUP, MEMORY, COMPUTED)] + \
          [plt.Line2D([], [], marker="o", color=CONTROL, linestyle="", markersize=5)]  # fmt: skip
ax.legend(handles, ["lookup step", "memory step", "computed step", "rotated control"], frameon=False, loc="lower left",
          bbox_to_anchor=(0, 1.0), fontsize=9, ncol=4)  # fmt: skip
fig.text(0.01, 0.01, "Bars in chain order (step 1, 2, 3). full_v8 / full_v8b (three-step: core domains, per-word eligibility); "
         "95% intervals over bridge entities; one run, one data seed. Unverified.", fontsize=7.5, color=INK2)  # fmt: skip
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(OUT / "fig2_steps.png", dpi=200)
(OUT / "numbers.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: {"loss": round(100 * v["loss"]), "ci": [round(100 * c) for c in v["ci"]], "ctrl": round(100 * v["control"]), "n": v["n"]} for k, v in out.items()}))
