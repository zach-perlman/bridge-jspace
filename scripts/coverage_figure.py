"""Evidence by model (2026-10-20): which claims each model supports, contradicts, or cannot test. Values are
transcribed from EXPERIMENTS.md (one line per run; the run names are in the CELLS comments).
python coverage_fig.py OUT.png"""

import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BLUE, AQUA, ORANGE, GREY = "#2a78d6", "#1baf7a", "#eb6834", "#d9d8d2"
INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
STATUS = {  # fill, text colour, symbol, legend label
    "yes": (BLUE, SURF, "✓", "supports"),
    "part": (AQUA, INK, "~", "partly / weakly"),
    "no": (ORANGE, INK, "✗", "against"),
    "na": (GREY, INK, "?", "can't tell (control failed or not run)"),
}
COLS = [
    "does the\ntasks",
    "lens reads\nthe bridge",
    "lens can write\nanything\n(countries)",
    "read, not written\n(RL ≤ random,\nRR written)",
    "knock-out:\nlookups survive,\nrecall breaks",
    "copy split:\nrecall-used >\nlookup-used",
]
ROWS = [
    "Qwen3.6-27B\nhybrid attn",
    "Qwen3.5-122B-A10B\nhybrid attn, MoE",
    "Qwen3.5-9B\nhybrid attn",
    "Gemma 4 31B-it\nstandard attn, own J++",
]
CELLS = [  # (status, text)
    [
        ("yes", "99.5–100%"),
        ("yes", "RL 95%"),
        ("yes", "95–100%"),
        ("yes", "RL ≤3%\nRR 36%"),  # suitecomp, dose_v1
        ("yes", "99% vs 19–22%\nctrl 98–100%"),
        ("yes", "0.3–0.4×\nvs 1.4–1.9×"),
    ],  # abl_rot_v1, parts_A8/B8
    [
        ("yes", "98–100%"),
        ("yes", "RL 98%"),
        ("yes", "86–100%"),
        ("yes", "RL ≤8% at\nevery depth"),  # l5big2, layers sweep
        ("part", "94–100% vs\n77–87%"),
        ("part", "0.24–0.48×\nvs 0.78–1.02×"),
    ],  # abl_v1/depth_v2, cap42
    [
        ("yes", "97–100%"),
        ("yes", "RL 98%"),
        ("na", "countries not run\n(BR 12–18%)"),
        ("na", "RL 0%, but\nRR ~1% too"),  # comp9b, qwen35_9b_rw_v1
        ("na", "not run"),
        ("no", "gap absent at\nmatched depth"),
    ],  # splitq
    [
        ("yes", "97–100%"),
        ("part", "RL 2% (30–36),\n97% elsewhere"),
        ("na", "≤9%\n(Qwen ~100%)"),
        ("na", "untestable"),  # gemma4itr
        ("na", "breaks plain\ntext too"),
        ("na", "not run"),
    ],  # abl_rot, textloss
]

fig, ax = plt.subplots(figsize=(11.2, 4.6), facecolor=SURF)
ax.set_facecolor(SURF)
cw, rh, x0 = 1.0, 1.0, 0.0
for i, row in enumerate(CELLS):
    for j, (st, txt) in enumerate(row):
        fill, tc, sym, _ = STATUS[st]
        ax.add_patch(
            Rectangle(
                (x0 + j * cw + 0.03, -i * rh - 0.97),
                cw - 0.06,
                rh - 0.06,
                facecolor=fill,
                edgecolor=SURF,
                hatch="///" if st == "na" else None,
                linewidth=0,
            )
        )
        ax.text(x0 + j * cw + 0.09, -i * rh - 0.13, sym, ha="left", va="top", fontsize=9, color=tc, fontweight="bold")
        ax.text(
            x0 + j * cw + 0.5,
            -i * rh - 0.53,
            txt,
            ha="center",
            va="center",
            fontsize=7.8,
            color=tc,
            fontweight="bold" if st != "na" else "normal",
        )
for j, c in enumerate(COLS):
    ax.text(x0 + j * cw + 0.5, 0.12, c, ha="center", va="bottom", fontsize=8.5, color=INK)
for i, r in enumerate(ROWS):
    ax.text(-0.08, -i * rh - 0.5, r, ha="right", va="center", fontsize=9, color=INK)
ax.set_xlim(-1.9, len(COLS) * cw + 0.05)
ax.set_ylim(-len(ROWS) * rh - 0.15, 1.15)
ax.axis("off")
handles = [
    Rectangle((0, 0), 1, 1, facecolor=v[0], hatch="///" if k == "na" else None, edgecolor=SURF, label=f"{v[2]} {v[3]}")
    for k, v in STATUS.items()
]
fig.legend(handles=handles, loc="lower left", ncol=4, frameon=False, bbox_to_anchor=(0.01, -0.02), fontsize=8.5)
fig.suptitle(
    "Evidence by model: positive results come from two Qwen hybrid-attention models; the 9B and Gemma mostly can't tell us",
    x=0.01,
    ha="left",
    fontsize=10.5,
    fontweight="bold",
    y=0.99,
)
fig.savefig(sys.argv[1], dpi=170, facecolor=SURF, bbox_inches="tight")
print("ok")
