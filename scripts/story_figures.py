"""Two figures for the partner update (2026-10-20), from results/ on the box:
  story_2x2.png   the 27B's families under three measures: the J-space part's share of the lens-free copy
                  (concentration), the lens write (best flips over strengths), the J-space knock-out (accuracy)
  story_depth.png lens write by layer, per family, 27B vs 122B (best single-layer flips over 0.5-16x)
python story_figs.py RESULTS OUTDIR"""

import collections
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RES, OUT = Path(sys.argv[1]), Path(sys.argv[2])
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#9aa0a6"
INK, INK2, SURF, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e0"
plt.rcParams.update(
    {"font.size": 9, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK}
)


def load(*p):
    return json.loads(RES.joinpath(*p, "summary.json").read_text())


def style(ax):
    ax.set_facecolor(SURF)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


# ---- figure 1: the 2x2 under three measures (27B) ---------------------------------------------------------------
# rows: (label, use, concentration run/family, write run/family, knock-out family)
ROWS = [
    ("given → looked up (BL)", "lookup", ("suite_split/parts_A8_v1", "BL"), ("dose_v1", "BL"), "BL"),
    ("recalled → looked up (RL)", "lookup", ("suite_split/parts_A8_v1", "RL"), ("dose_v1", "RL"), "RL"),
    ("given → recalled (BR)", "recall", ("suite_split/parts_A8_v1", "BR"), ("dose_v1", "BR"), "BR"),
    ("recalled → recalled (RR)", "recall", ("suite_split/parts_A8_v1", "RR"), ("dose_v1", "RR"), "RR"),
    ("typo fixed → recalled", "recall", ("suite_split/parts_C3_cal_v1", "TYPO"), ("computed_v1", "TYPO"), "TYPO"),
    ("translated → recalled", "recall", ("suite_split/parts_C3_cal_v1", "TRANS"), ("computed_v1", "TRANS"), "TRANS"),
    ("countries (paper-style)", "recall", None, ("dose_v1", "R"), "country-R"),
]
# random-dictionary nulls for the concentration (EXPERIMENTS.md, calib-1020-0038 and computed-1020-0057), and the
# country positive control (control-1019-2340, question tokens, single layer): not stored under one key, so listed
NULL = {"BL": 0.17, "RL": 0.15, "BR": 0.31, "RR": 0.24, "TYPO": 0.52, "TRANS": 0.37}
COUNTRY_CONC = (2.86, 2.70, 3.02)

conc, write, ko = [], [], []
for label, use, c, w, k in ROWS:
    if c:
        d = load(c[0])["families"][c[1]]["frac"]["jspace"]["concentration"]
        conc.append((label, use, d[0], d[1], d[2], NULL[c[1]]))
    else:
        conc.append((label, use, *COUNTRY_CONC, None))
    ws = load("read_write", w[0])["families"][w[1]]["write"]
    lens = max(v["flips"] for kk, v in ws.items() if "/lens_" in kk)
    rnd = max(v["flips"] for kk, v in ws.items() if "/random_" in kk)
    write.append((label, use, lens, rnd))
    a = load("ablate_pilot", "abl_rot_v1")["families"][f"{k}/clean"]["accuracy"]
    ko.append((label, use, a["jspace"], a["random"], a.get("rotated")))

col = {"lookup": ORANGE, "recall": BLUE}
fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.9), facecolor=SURF, sharey=True, gridspec_kw={"wspace": 0.08})
ys = list(range(len(ROWS)))
ax = axes[0]
style(ax)
for y, (_label, use, m, lo, hi, null) in zip(ys, conc, strict=True):
    ax.plot([lo, hi], [y, y], color=col[use], lw=2, alpha=0.45)
    ax.scatter([m], [y], s=46, color=col[use], zorder=3, edgecolors=SURF, linewidths=1.5)
    if null is not None:
        ax.scatter([null], [y], s=40, marker="|", color=GREY, linewidths=2, zorder=2)
ax.axvline(1, color=INK2, lw=0.8, ls=(0, (3, 3)))
ax.text(1.04, len(ROWS) - 0.45, "1× = its fair share", color=INK2, fontsize=7.5, va="center")
ax.set_xlim(0, 3.2)
ax.set_xlabel("J-space part's effect ÷ its share of the copy (95% CI)")
ax.set_title(
    "1. Lens-free copy: is the bridge carried\nin the J-space? (| = random-dictionary null)",
    loc="left",
    fontsize=9.5,
    fontweight="bold",
)
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in ROWS])
ax.invert_yaxis()

ax = axes[1]
style(ax)
for y, (_label, use, lens, rnd) in zip(ys, write, strict=True):
    ax.barh(y, 100 * lens, height=0.55, color=col[use])
    ax.scatter([100 * rnd], [y], s=40, marker="|", color=GREY, linewidths=2, zorder=3)
    ax.text(100 * max(lens, rnd) + 2.5, y, f"{100 * lens:.0f}%", va="center", fontsize=8, color=INK)
ax.set_xlim(0, 112)
ax.set_xlabel("answers flipped, best strength (layers 32/36/40)")
ax.set_title(
    "2. Lens write: does pushing along the lens\ndirection change the bridge? (| = random)",
    loc="left",
    fontsize=9.5,
    fontweight="bold",
)

ax = axes[2]
style(ax)
for y, (_label, use, j, rnd, rot) in zip(ys, ko, strict=True):
    ax.barh(y, 100 * j, height=0.55, color=col[use])
    ax.scatter([100 * rnd], [y], s=40, marker="|", color=GREY, linewidths=2, zorder=3)
    if rot is not None:
        ax.scatter([100 * rot], [y], s=22, marker="D", color=SURF, edgecolors=GREY, linewidths=1.2, zorder=3)
    ax.text(
        100 * j + 2.5 if j < 0.9 else 100 * j - 2.5,
        y,
        f"{100 * j:.0f}%",
        va="center",
        fontsize=8,
        color=INK if j < 0.9 else SURF,
        ha="left" if j < 0.9 else "right",
    )
ax.set_xlim(0, 112)
ax.set_xlabel("accuracy with the J-space removed (unedited: 100%)")
ax.set_title(
    "3. Knock-out: does the model still answer?\n(| = random dictionary, ◇ = same-size random)",
    loc="left",
    fontsize=9.5,
    fontweight="bold",
)
h = [
    plt.Line2D([], [], marker="s", ls="", color=ORANGE, markersize=8, label="bridge used by a lookup in the prompt"),
    plt.Line2D([], [], marker="s", ls="", color=BLUE, markersize=8, label="bridge used to recall a fact from memory"),
]
fig.legend(handles=h, loc="lower left", ncol=2, frameon=False, bbox_to_anchor=(0.005, 0.985))
fig.suptitle(
    "Qwen3.6-27B: the same four families under three different measures",
    x=0.01,
    ha="left",
    fontsize=11,
    fontweight="bold",
    y=1.10,
)
fig.text(
    0.01,
    -0.03,
    "n = 150 scenes (copy), 80 (write), 100 (knock-out) per family; one seed each. Copy split and knock-out "
    "at layers 32-40 on the question tokens; countries' copy value from the country control (125 items).",
    fontsize=7.5,
    color=INK2,
)
fig.savefig(OUT / "story_2x2.png", dpi=170, facecolor=SURF, bbox_inches="tight")
plt.close(fig)


# ---- figure 2: lens write by depth, 27B vs 122B --------------------------------------------------------------------
def per_layer(run):
    """family -> layer -> best single-layer lens flips over scales (and random)"""
    agg = collections.defaultdict(list)
    for line in RES.joinpath("read_write", run, "outcomes.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["null"] or r["layer"] == "band":
            continue
        agg[(r["family"], r["layer"], r["part"])].append(r["role"] == "b")
    best = collections.defaultdict(dict)
    for (fam, la, part), v in agg.items():
        if part.startswith("lens_") or part.startswith("random_"):
            kind = part.split("_")[0]
            rate = sum(v) / len(v)
            key = (la, kind)
            best[fam][key] = max(best[fam].get(key, 0), rate)
    return best


FAMS = [
    ("RL", "recalled → looked up", BLUE, "o"),
    ("RR", "recalled → recalled", ORANGE, "s"),
    ("BR", "given → recalled", AQUA, "^"),
    ("BL", "given → looked up", YELLOW, "v"),
    ("R", "countries", MAGENTA, "D"),
]
MODELS = [
    ("Qwen3.6-27B", 64, ("layers_v1", "dose_v1")),
    ("Qwen3.5-122B", 48, ("qwen35_122b_layers_v1", "qwen35_122b_rw_v1")),
]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=SURF, sharey=True, gridspec_kw={"wspace": 0.06})
for ax, (name, n_layers, runs) in zip(axes, MODELS, strict=True):
    style(ax)
    ax.grid(axis="y", color=GRID, lw=0.8)
    merged = collections.defaultdict(dict)
    for run in runs:
        for fam, d in per_layer(run).items():
            merged[fam].update(d)
    rmax = 0
    for fam, label, c, mk in FAMS:
        d = merged.get(fam, {})
        layers = sorted({la for la, kind in d if kind == "lens"})
        xs = [la / n_layers for la in layers]
        ys_ = [100 * d[(la, "lens")] for la in layers]
        rmax = max([rmax] + [100 * d.get((la, "random"), 0) for la in layers])
        ax.plot(xs, ys_, color=c, lw=2, marker=mk, markersize=6, markeredgecolor=SURF, markeredgewidth=1, label=label)
    all_layers = sorted({la for d in merged.values() for la, kind in d if kind == "random"})
    rnd = [100 * max(merged[f].get((la, "random"), 0) for f in merged) for la in all_layers]
    ax.plot(
        [la / n_layers for la in all_layers],
        rnd,
        color=GREY,
        lw=1.5,
        ls=(0, (4, 3)),
        label="random direction (max over families)",
    )
    ax.set_xlim(0.15, 1.0)
    ax.set_ylim(-3, 105)
    ax.set_xlabel("depth (layer ÷ number of layers)")
    ax.set_title(name, loc="left", fontsize=9.5, fontweight="bold")
axes[0].set_ylabel("answers flipped by the lens push, best of 0.5–16×")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="lower left",
    ncol=6,
    frameon=False,
    bbox_to_anchor=(0.005, 0.93),
    fontsize=8,
    handletextpad=0.4,
    columnspacing=1.2,
)
fig.suptitle(
    "Where can the lens write the bridge? The lookup-used bridge (blue) resists in transit on both models,\n"
    "and at every depth on the 122B; on the 27B, hard early pushes write every family",
    x=0.01,
    ha="left",
    fontsize=10.5,
    fontweight="bold",
    y=1.10,
)
fig.text(
    0.01,
    -0.05,
    "One layer at a time, question tokens; n = 80 (27B) / 60 (122B) per family; one seed. 27B transit "
    "window (bridge carried, answer not yet formed) ≈ 0.5–0.63 depth.",
    fontsize=7.5,
    color=INK2,
)
fig.savefig(OUT / "story_depth.png", dpi=170, facecolor=SURF, bbox_inches="tight")
print("ok")
