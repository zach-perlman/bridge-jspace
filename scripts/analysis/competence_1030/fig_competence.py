"""fig_competence.png from competence_work/card_data.json (agent 'competence', 2026-10-30)."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

W = "/home/zach/scratch/redteam_1030/next8h/"
d = json.load(open(W + "competence_work/card_data.json"))
MODELS = [("Qwen3.5-9B", "Qwen3.5-9B (J++)"), ("Qwen3.6-27B", "Qwen3.6-27B (J++)"),
          ("Nemotron-3.5-Lightning", "Nemotron-3.5-Lightning (plain J-lens)")]
GROUPS = [("v4_4001", "MP", "v4 twins\nlookup (MP)"), ("v4_4001", "MM", "v4 twins\nrecall (MM)"),
          ("v5al", "MP", "codename\nlookup (MP)"), ("v5al", "MM", "codename\nrecall (MM)"),
          ("v5kn2c", "MC", "capital of X's\ncountry, passage (MC)"), ("v5kn2c", "MC0", "capital of X's\ncountry, closed (MC0)")]
BARS = [("whole", "whole question", "#2a78d6", None), ("step1", "hop 1 alone", "#eb6834", None),
        ("step2", "hop 2 alone (bridge named)", "#1baf7a", None), ("guess", "no-description guess", "#6250d6", "///")]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, axes = plt.subplots(3, 1, figsize=(13, 11.5), sharey=True)
bw, gap = 0.19, 0.02
for ax, (m, title) in zip(axes, MODELS):
    for gi, (tag, w, lab) in enumerate(GROUPS):
        c = d[m][tag][w]
        for bi, (k, _, col, hatch) in enumerate(BARS):
            x = gi + (bi - 1.5) * (bw + gap)
            v = c[k]
            ax.bar(x, v, bw, color=col if not hatch else "white", edgecolor=col, hatch=hatch, linewidth=1.2 if hatch else 0, zorder=2)
            top = max([v] + ([d[m][t2][w]["whole"] for t2 in ("v4_4002", "v4_4003")] if (k == "whole" and tag == "v4_4001") else []))
            if k == "guess":
                top = max(top, 16.7 if w in ("MP", "MC", "MC0") else c["chance_vocab"])
            ax.text(x, top + 2.2, f"{v:.0f}", ha="center", va="bottom", fontsize=7.5, color=INK2)
            if k == "guess":  # chance: 1/6 passage values for MP / MC / MC0, 1/|answer vocab| for MM
                ch = 16.7 if w in ("MP", "MC", "MC0") else c["chance_vocab"]
                ax.plot([x - bw / 2 - 0.02, x + bw / 2 + 0.02], [ch, ch], color=INK, lw=1.6, ls=(0, (2, 1)), zorder=3)
            if k == "whole" and tag == "v4_4001":  # the other two v4 data draws
                for t2 in ("v4_4002", "v4_4003"):
                    ax.plot(x, d[m][t2][w]["whole"], "o", ms=4.5, mfc="white", mec=INK, mew=1.1, zorder=4)
    ax.set_title(title, loc="left", fontsize=11, color=INK, fontweight="bold")
    ax.set_xticks(range(len(GROUPS)))
    ax.set_xticklabels([f"{g[2]}\nknock-out gated n {d[m][g[0]][g[1]]['ko_n_rows']}" for g in GROUPS], fontsize=8.5)
    ax.tick_params(axis="x", length=0, pad=4)
    ax.set_ylim(0, 112); ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("accuracy, % (cand2 read)")
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.axvline(1.5, color=GRID, lw=1); ax.axvline(3.5, color=GRID, lw=1)
handles = [Patch(facecolor=col if not h else "white", edgecolor=col, hatch=h, label=l) for _, l, col, h in BARS]
handles += [Line2D([], [], color=INK, lw=1.6, ls=(0, (2, 1)), label="chance (1/6 passage values; 1/|answer vocab| for MM)"),
            Line2D([], [], marker="o", ls="", mfc="white", mec=INK, label="whole question, v4 draws 4002 / 4003")]
fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 0.995))
fig.text(0.01, 0.005, "Unedited models, all items (v4 n 874 per word and draw; codename n 582; capital n 325). Hop 1 counts as right only if the "
         "candidate read AND the greedy name agree. Codename hop 1 is read from the passage (not latent).\n"
         "Gated n = items in the knock-out (hop-1 control right [closed book; codename: from the passage], hop 1 and hop 2 and whole right, guess wrong). Source: competence_card.md / competence_work/card_data.json.",
         fontsize=7.5, color=INK2, va="bottom")
fig.tight_layout(rect=(0, 0.035, 1, 0.955), h_pad=2.2)
fig.savefig(W + "fig_competence.png", dpi=160, facecolor="#fcfcfb")
print("ok")
