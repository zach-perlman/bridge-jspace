"""Morning figure: read vs write per setting and model, and the J-space knock-out. Reads results/*/summary.json pulled
to RES; rows whose run is missing are skipped. python make_fig.py RES OUT.png"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RES, OUT = Path(sys.argv[1]), sys.argv[2]
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#9aa0a6"
INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
NAMES = {
    "BL": "given → looked up",
    "BR": "given → recalled",
    "RL": "recalled → looked up",
    "RR": "recalled → recalled",
    "R": "countries, recalled",
    "B": "countries, given",
    "TBL": "tool JSON: given → looked up",
    "TBR": "tool JSON: given → recalled",
    "NM": "real facts: recalled → recalled",
    "NL": "real facts: recalled → looked up",
}


def load(*parts):
    p = RES.joinpath(*parts, "summary.json")
    return json.loads(p.read_text()) if p.exists() else None


def rw_rows(model, run, fams):
    s = load("read_write", run)
    if not s:
        return []
    out = []
    for f in fams:
        if f not in s["families"]:
            continue
        d = s["families"][f]
        lens = max((v["flips"] for k, v in d["write"].items() if "/lens_" in k), default=0)
        rand = max((v["flips"] for k, v in d["write"].items() if "/random_" in k), default=0)
        out.append((model, NAMES[f], d["read_top10"], lens, rand, d["n"]))
    return out


def nat_rows(model, run):
    s = load("natural_rw", run)
    if not s:
        return []
    out = []
    for ver in ("NM", "NL"):
        d = s["versions"].get(ver)
        if d:
            lens = max(v["flips"] for k, v in d["write"].items() if k.startswith("lens_"))
            rand = max(v["flips"] for k, v in d["write"].items() if k.startswith("random_"))
            out.append(
                (
                    model,
                    NAMES[ver],
                    d["read_top10"],
                    lens,
                    rand,
                    s["n_items"] if isinstance(s["n_items"], int) else s["n_items"].get(ver),
                )
            )
    return out


core = ["BL", "BR", "RL", "RR", "R", "B"]
rows = []
M27 = "Qwen3.6-27B (layers 32/36/40)"
rows += rw_rows(M27, "dose_v1", core)
rows += rw_rows(M27, "tool_rw_v1", ["TBL", "TBR"])
rows += nat_rows(M27, "v3_lookup")
rows += rw_rows("Qwen3.5-122B (layers 36/39)", "qwen35_122b_rw_v1", core)
rows += rw_rows("Qwen3.5-122B (layers 36/39)", "qwen35_122b_tool_rw_v1", ["TBL", "TBR"])
rows += nat_rows("Qwen3.5-122B (layers 36/39)", "qwen35_122b_v3_lookup")
rows += rw_rows("Qwen3.5-9B (layers 16/18/20)", "qwen35_9b_rw_v1", core)
rows += rw_rows("Gemma 4 31B-it, own lens (layers 30/33/36)", "gemma4itr_rw_v1", core)

abl = []
for model, run in (
    ("Qwen3.6-27B (layers 32/36/40)", "v1"),
    ("Qwen3.6-27B (layers 32/36/40)", "tool_abl_v1"),
    ("Qwen3.6-27B (layers 32/36/40)", "natural:v3_lookup"),
    ("Qwen3.5-122B (layers 24/27/30)", "qwen35_122b_abl_depth_v2"),
    ("Qwen3.5-122B (layers 36/39)", "qwen35_122b_abl_v1"),
    ("Qwen3.5-122B (layers 36/39)", "natural:qwen35_122b_v3_lookup"),
):
    if run.startswith("natural:"):
        s = load("natural_rw", run.split(":")[1])
        for ver, d in ((s or {}).get("ablation") or {}).items():
            abl.append((model, NAMES[ver], d["none"], d["jspace"], d["random"], s["n_items"]))
        continue
    s = load("ablate_pilot", run)
    if not s:
        continue
    for key, d in s["families"].items():
        fam, kind = key.split("/")
        if kind != "clean" or (run == "tool_abl_v1" and not fam.startswith("TB")):
            continue
        fam = fam.replace("country-", "")
        name = NAMES.get(fam, {"TYPO": "typo fix → recalled", "TRANS": "translation → recalled"}.get(fam, fam))
        abl.append((model, name, d["accuracy"]["none"], d["accuracy"]["jspace"], d["accuracy"]["random"], d["n"]))

plt.rcParams.update(
    {"font.size": 9, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK}
)


def groups(d):
    return len({r[0] for r in d})


h_a, h_b = len(rows) + 0.6 * groups(rows) + 2.5, len(abl) + 0.6 * groups(abl) + 2.5
fig, axes = plt.subplots(
    2, 1, figsize=(8.6, 0.24 * (h_a + h_b) + 1.0), facecolor=SURF, gridspec_kw={"height_ratios": [h_a, h_b]}
)


def draw(ax, data, title, a_label, b_label, a_col, b_col, ctrl_label):
    ax.set_facecolor(SURF)
    y, labels, last = 0, [], None
    ys = []
    for model, name, a, b, ctrl, n in data:
        if model != last:
            if last is not None:
                y += 0.6
            labels.append((y, model))
            y += 1
            last = model
        ys.append((y, name, a, b, ctrl, n))
        y += 1
    for yy, _name, a, b, ctrl, _n in ys:
        ax.plot([100 * a, 100 * b], [yy, yy], color="#d5d4cf", lw=2, zorder=1)
        ax.scatter([100 * ctrl], [yy], s=40, color=GREY, marker="|", zorder=4, linewidths=2)
        ax.scatter([100 * a], [yy], s=36, color=a_col, zorder=3, edgecolors=SURF, linewidths=1.5)
        ax.scatter([100 * b], [yy], s=36, color=b_col, zorder=3, edgecolors=SURF, linewidths=1.5)
    ax.set_yticks([v[0] for v in ys] + [v[0] for v in labels])
    ax.set_yticklabels([f"{v[1]} (n={v[5]})" for v in ys] + [v[1] for v in labels])
    for t in ax.get_yticklabels()[len(ys) :]:
        t.set_fontweight("bold")
    ax.invert_yaxis()
    ax.set_xlim(-3, 103)
    ax.set_xlabel("%")
    ax.grid(axis="x", color="#e6e5e0", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title(title, loc="left", fontsize=10, fontweight="bold", pad=24)
    h = [
        plt.Line2D([], [], marker="o", ls="", color=a_col, label=a_label),
        plt.Line2D([], [], marker="o", ls="", color=b_col, label=b_label),
        plt.Line2D([], [], marker="|", ls="", color=GREY, markersize=8, mew=2, label=ctrl_label),
    ]
    ax.legend(
        handles=h,
        loc="lower left",
        bbox_to_anchor=(-0.02, 0.995),
        ncol=3,
        frameon=False,
        fontsize=8,
        borderaxespad=0.2,
        handletextpad=0.3,
        columnspacing=1.0,
    )


draw(
    axes[0],
    [(m, n, r, w, c, k) for m, n, r, w, c, k in rows],
    "A. Read vs write (one set of layers per model)",
    "read: bridge in lens top 10",
    "write: flips at best strength",
    BLUE,
    ORANGE,
    "random",
)
draw(
    axes[1],
    [(m, n, j, a, r, k) for m, n, a, j, r, k in abl],
    "B. Knock-out (Qwen): accuracy with the J-space removed",
    "J-space removed",
    "unedited",
    ORANGE,
    BLUE,
    "random removed",
)
fig.tight_layout()
fig.savefig(OUT, dpi=170, facecolor=SURF)
print("rows", len(rows), "ablation rows", len(abl))
