"""fig_overlap.png (overlap agent, post hoc, exploratory). Reads overlap_work/data/*.json."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

D = Path("/home/zach/scratch/redteam_1030/next8h/overlap_work/data")
OUT = Path("/home/zach/scratch/redteam_1030/next8h/fig_overlap.png")
v4 = json.load(open(D / "ana_v4.json"))
dr = json.load(open(D / "ana_v4draws.json"))
n38 = json.load(open(D / "ana_n38.json"))
n53 = json.load(open(D / "ana_n53.json"))
LOW, HIGH, MUTED = "#2a78d6", "#eb6834", "#52514e"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"
MODELS = [("qwen35_9b_", "9B"), ("27b_", "27B"), ("nem35l_", "Lightning")]
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlecolor": INK, "figure.facecolor": "#fcfcfb",
                     "axes.facecolor": "#fcfcfb"})
fig, axs = plt.subplots(2, 3, figsize=(13, 7.6))


def style(ax, ylab, ref=None):
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_ylabel(ylab)
    if ref is not None:
        ax.axhline(ref, color=MUTED, lw=1, ls=":")


def pair(ax, vals, labels, ylab, ref=None, extra=None, ylim=None):
    """vals: list of ((lo, lo_ci), (hi, hi_ci)) per group."""
    for g, ((a, aci), (b, bci)) in enumerate(vals):
        for off, v, ci, col in ((-0.15, a, aci, LOW), (0.15, b, bci, HIGH)):
            if v is None:
                continue
            yerr = [[v - ci[0]], [ci[1] - v]] if ci else None
            ax.errorbar(g + off, v, yerr=yerr, fmt="o", ms=7, color=col, ecolor=col, elinewidth=2, capsize=0, mec="#fcfcfb", mew=1.5, zorder=3)
        if extra:
            for off, vs, col in ((-0.15, extra[g][0], LOW), (0.15, extra[g][1], HIGH)):
                for k, v in enumerate(vs):
                    if v is not None:
                        ax.plot(g + off + (0.06 if k else -0.06), v, marker="D", ms=4, mfc="none", mec=col, mew=1.2, ls="", zorder=2)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.6, len(labels) - 0.4)
    if ylim:
        ax.set_ylim(*ylim)
    style(ax, ylab, ref)


# (a) C1 gap
vals, extra = [], []
for P, _ in MODELS:
    x = v4[P]["excess_A"]
    vals.append(((x["low"]["gap_paper10"], x["low"]["gap_paper10_ci"]), (x["high"]["gap_paper10"], x["high"]["gap_paper10_ci"])))
    extra.append(([dr.get(f"{P}{d}", {}).get("low", {}).get("gap") for d in ("p4002", "p4003")],
                  [dr.get(f"{P}{d}", {}).get("high", {}).get("gap") for d in ("p4002", "p4003")]))
pair(axs[0, 0], vals, [m for _, m in MODELS], "MM loss - MP loss under paper10 (points)", 0, extra, (0, 90))
axs[0, 0].set_title("v4: recall-vs-lookup gap (C1)")
# (b) keepA rescue
vals, extra = [], []
for P, _ in MODELS:
    x = v4[P]["excess_A"]
    vals.append(((x["low"]["keepA_rescue"], x["low"]["keepA_rescue_ci"]), (x["high"]["keepA_rescue"], x["high"]["keepA_rescue_ci"])))
    extra.append(([dr.get(f"{P}{d}", {}).get("low", {}).get("rescue") for d in ("p4002", "p4003")],
                  [dr.get(f"{P}{d}", {}).get("high", {}).get("rescue") for d in ("p4002", "p4003")]))
pair(axs[0, 1], vals, [m for _, m in MODELS], "keepA rescue (1 = full)", 2 / 3, extra, (0.3, 1.25))
axs[0, 1].set_title("v4: keeping the answer span rescues recall")
# (c) onlyA damage share
vals = []
for P, _ in MODELS:
    x = v4[P]["excess_A"]
    vals.append(((x["low"]["onlyA_net_share"], x["low"]["onlyA_net_share_ci"]), (x["high"]["onlyA_net_share"], x["high"]["onlyA_net_share_ci"])))
pair(axs[0, 2], vals, [m for _, m in MODELS], "onlyA net MM loss / paper10's", 2 / 3, None, (0.3, 1.7))
axs[0, 2].set_title("v4: removing only A does the damage")
# (d) relation split (all bridges, any tokenisation): keepA rescue
ax = axs[1, 0]
rels = [("people", "people\n(nationality)"), ("companies", "companies\n(country)"), ("landmarks", "landmarks\n(country)"), ("cities", "cities\n(country)")]
cols = {"9B": "#2a78d6", "27B": "#1baf7a", "Lightning": "#6250d6"}
for j, (P, m) in enumerate(MODELS):
    for g, (rel, _) in enumerate(rels):
        r = v4[P]["relation"][rel]
        v, ci = r.get("gap_paper10"), r.get("gap_paper10_ci")
        if v is None:
            continue
        ax.errorbar(g + (j - 1) * 0.2, v, yerr=[[v - ci[0]], [ci[1] - v]], fmt="o", ms=6, color=cols[m], elinewidth=1.8, mec="#fcfcfb", mew=1.2,
                    label=m if g == 0 else None, zorder=3)
ax.set_xticks(range(len(rels)))
ax.set_xticklabels([lab for _, lab in rels])
ax.set_ylim(0, 100)
style(ax, "C1 gap under paper10 (points)", 0)
ax.legend(frameon=False, loc="lower left", fontsize=8, ncol=3)
ax.set_title("v4 by relation (all bridges): C1 gap")
# (e) note 38 v3 swap: scrub keeps (matched norm)
vals = []
for P, _ in MODELS:
    x = n38[P]["RM"]
    g = lambda h: (x[h]["table"].get("insert_k10_noansrel_nm", {}).get("share"), x[h]["table"].get("insert_k10_noansrel_nm", {}).get("share_ci"))  # noqa: E731
    vals.append((g("low"), g("high")))
pair(axs[1, 1], vals, [m for _, m in MODELS], "swap kept after answer scrub (share)", 1 / 3, None, (-0.1, 1.0))
axs[1, 1].set_title("v3 swap (note 38, RM): matched-norm answer scrub")
axs[1, 1].annotate("swap < 10 pts:\nnot read", (2 - 0.15, 0.42), ha="center", fontsize=7.5, color=INK2)
# (f) note 53 paper prompts: arm-1 flip rate by half and keep_7E
ax = axs[1, 2]
M53 = [("qwen35_9b_", "9B"), ("27b_", "27B"), ("nem35l_", "Lightning"), ("muse30_", "Muse")]
for g, (P, m) in enumerate(M53):
    for off, h, col in ((-0.15, "low", LOW), (0.15, "high", HIGH)):
        s = n53[P][h]
        rate = s["arm1_flips"] / s["n"]
        ax.bar(g + off, rate, width=0.28, color=col, edgecolor="#fcfcfb", lw=2, zorder=3)
        ax.text(g + off, rate + 0.015, f"{s['arm1_flips']}/{s['n']}", ha="center", va="bottom", fontsize=7.5, color=INK2)
ax.set_xticks(range(len(M53)))
ax.set_xticklabels([m for _, m in M53])
ax.set_ylim(0, 1)
style(ax, "paper swap (arm 1) flip rate")
ax.set_title("paper's 2-hop prompts (note 39/53): swap works\nalmost only on high-overlap items")
from matplotlib.lines import Line2D  # noqa: E402

handles = [Line2D([], [], marker="o", ls="", color=LOW, ms=7, label="low bridge-answer overlap (below median)"),
           Line2D([], [], marker="o", ls="", color=HIGH, ms=7, label="high overlap (above median)"),
           Line2D([], [], marker="D", ls="", mfc="none", mec=MUTED, ms=5, label="v4 draws p4002 / p4003 (same split)"),
           Line2D([], [], ls=":", color=MUTED, label="reference: 0, 2/3 or 1/3 rule")]
fig.legend(handles=handles, loc="upper center", ncol=4, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.995))
fig.suptitle("Do the answer-direction results hold where the bridge's J++ vector is NOT inside the answer span? (post hoc, exploratory; bars = 95% bridge bootstrap; draw 4001)",
             y=0.955, fontsize=9.5, color=INK2)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUT, dpi=150)
print(OUT)
