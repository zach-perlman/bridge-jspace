"""Cross-model figures for the Day 4 plan (Zach, 2026-10-22). Run from the box repo root (.venv); re-run as results land:
a model whose run is missing is drawn as "running". Figures show trends only; the pre-registered rules and verdicts are
in the text (results/cross_model/summary.md).
Fig 1  remove vs write, per model (C1 knock-out on the test set; C2 lens write at the aligned band)
Fig 2  the knock-out by depth on held-out ctrl_v8 (the band-selection data)
Fig 3  what the knock-out effect is specific to (logit-lens, random, keep-the-bridge-word) and how it grows with dose
Fig 4  two- and three-step chains together, grouped by where the recall sits; each step asked alone
Fig 5  the recall-vs-lookup gap by prompt format and difficulty
Fig 6  the lens write by single layer, through and past the band (direct-output check)
"""

import collections
import json
import statistics
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

from scripts import tasks_v2 as T

OUT = Path("figures/cross_model")
OUT.mkdir(parents=True, exist_ok=True)
AB, WM = Path("results/ablate_v2"), Path("results/write_max")
SURFACE, INK, INK2, INK3, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8d8c88", "#e4e3df"
LOOKUP, MEMORY, CONTROL, BAND = "#2a78d6", "#eb6834", "#a3a29d", "#ecebe7"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "font.family": "DejaVu Sans"})  # fmt: skip
MODELS = [
    dict(name="Qwen3.6-27B", kind="Qwen · hybrid", p="", nl=64, three_steps="full3_ko_steps_v2", late=None),
    dict(name="Qwen3.5-9B", kind="Qwen · hybrid", p="qwen35_9b_", nl=32, late=None),
    dict(name="Qwen3-32B", kind="Qwen · dense", p="qwen3_32b_", nl=64, late="qwen3_32b"),
    dict(name="Muse Glimmer 30B", kind="Meta · dense", p="muse30_", nl=52, late="muse30"),
]  # fmt: skip
GEMMA = dict(name="Gemma 4 31B-it", kind="Google · dense", p="gemma4itf_", nl=60)
LOOK, MEM = ("PP", "MP", "CP"), ("PM", "MM", "CM")
RLOOK, RMEM = ("PP", "MP"), ("PM", "MM")  # the pre-registered C1 rule's chain types: every gap and mean uses these
RUNNING = {}
FOOT = "Unverified; one data seed unless labeled \"fresh data seed\". J++ lenses: published for the 27B and 9B, our own fits for Qwen3-32B and Muse."


def foot(fig, text, size=7.4):
    width = int(fig.get_figwidth() * (17.8 if size < 7.4 else 17.1))  # characters per line at this font size
    fig.text(0.01, 0.012, "\n".join(textwrap.wrap(text, width)), fontsize=size, color=INK2, va="bottom")


def load(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def gap(L: dict) -> float:
    return statistics.mean(L[w] for w in RMEM) - statistics.mean(L[w] for w in RLOOK)


_rows: dict = {}


def rows_of(run: str):
    if run not in _rows:
        p = AB / run / "rows.jsonl"
        _rows[run] = [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else None
    return _rows[run]


def losses(run: str, band: str | None) -> dict:
    """{condition: {word: points lost}} at one band: unedited accuracy minus edited accuracy on the clean prompts, as in
    scripts/c1_v2.py (the run's items are those the model answers right on every step, so unedited is ~100%)."""
    rows = rows_of(run)
    if rows is None or band is None:
        return {}
    base, acc = collections.defaultdict(list), collections.defaultdict(list)
    for r in rows:
        if r["kind"] == "clean" and r["condition"] == "none":
            base[r["family"]].append(r["correct"])
        elif r["kind"] == "clean" and r["band"] == band:
            acc[(r["condition"], r["family"])].append(r["correct"])
    out = collections.defaultdict(dict)
    for (c, w), v in acc.items():
        out[c][w] = 100 * (statistics.mean(base[w]) - statistics.mean(v))
    return out


def c2(m):
    g = load(WM / "c2_graded" / f"{m['p']}wm2_full2_aligned_v1.json")
    if not g:
        return None
    band = (load(WM / f"{m['p']}wm2_full2_aligned_v1" / "manifest.json") or {}).get("band") or [0]
    return {"flips": {w: 100 * (g["families"].get(w, {}).get("cv_own_direction") or 0) for w in LOOK + MEM},
            "band": f"L{band[0]}-{band[-1]}"}  # fmt: skip


def style(ax, grid="x"):
    ax.spines[["top", "right"]].set_visible(False)
    (ax.xaxis if grid == "x" else ax.yaxis).grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


summary = {d["model"]: d for d in json.loads(Path("results/cross_model/summary.json").read_text())}
gemma_txt = summary.get(GEMMA["name"], {}).get("plain_text", {})
for m in MODELS:
    m["band"] = (load(AB / "c1_v2" / f"{m['p']}full2_ko_v1.json") or {}).get("middle")
    fr = load(AB / "c1_v2" / f"{m['p']}fresh2_ko_v1.json")
    m["fresh_gap"] = 100 * fr["rule"]["gap"] if fr else None
    m["ko"] = losses(f"{m['p']}full2_ko_v1", m["band"])
    m["c2"] = c2(m)
ys = [len(MODELS) - i for i in range(len(MODELS))]


def row_labels(ax, size=10.5):
    for y, m in zip(ys, MODELS, strict=True):
        ax.text(-0.03, y + 0.13, m["name"], transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=size, fontweight="bold")
        ax.text(-0.03, y - 0.2, m["kind"], transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=size - 1.5, color=INK2)


# ---------------------------------------------------------------- Fig 1: remove vs write
def dumbbell(ax, y, vals, extra=""):
    ml, mm = statistics.mean(vals[w] for w in RLOOK), statistics.mean(vals[w] for w in RMEM)
    ax.plot([ml, mm], [y, y], color="#dcdad5", linewidth=7, solid_capstyle="round", zorder=1)
    for w in LOOK + MEM:
        col = LOOKUP if w in LOOK else MEMORY
        ax.plot(vals[w], y, "o", color=col, markersize=5.5, alpha=0.5 if w[0] != "C" else 1, markeredgewidth=1.2 if w[0] == "C" else 0,
                markerfacecolor=SURFACE if w[0] == "C" else col, markeredgecolor=col, zorder=2)  # fmt: skip
    for v, col in ((ml, LOOKUP), (mm, MEMORY)):
        ax.plot(v, y, "o", color=col, markersize=11, markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=4)
    ax.text((ml + mm) / 2, y + 0.3, f"gap {mm - ml:.0f}{extra}", ha="center", va="center", fontsize=9.5, color=INK2)


fig = plt.figure(figsize=(11, 5.7))
gs = fig.add_gridspec(1, 2, left=0.165, right=0.985, top=0.75, bottom=0.17, wspace=0.1)
axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]
for ax, key, xmax in ((axes[0], "ko", 62), (axes[1], "c2", 92)):
    style(ax)
    ax.set_xlim(-3, xmax)
    ax.set_ylim(0.0, len(MODELS) + 0.55)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.axvline(0, color=INK2, linewidth=0.8)
    for y, m in zip(ys, MODELS, strict=True):
        if key == "ko":
            vals, sub = m["ko"].get("paper10"), m["band"]
            if vals:
                ax.plot(max(m["ko"]["paper10_rot"].values()), y, "|", color=INK3, markersize=12, markeredgewidth=2, zorder=3)
        else:
            vals, sub = (m["c2"] or {}).get("flips"), (m["c2"] or {}).get("band")
        if not vals:
            ax.text(1.5, y, RUNNING.get(m["name"], "not run"), va="center", fontsize=9, color=INK3, style="italic")
            continue
        dumbbell(ax, y, vals, f"   (fresh data seed: {m['fresh_gap']:.0f})" if key == "ko" and m.get("fresh_gap") is not None else "")
        ax.text(xmax, y + 0.33, sub, ha="right", va="center", fontsize=7.5, color=INK3)
axes[0].text(-0.03, 0.35, "Gemma 4 31B-it", transform=axes[0].get_yaxis_transform(), ha="right", va="center", fontsize=10.5, fontweight="bold", color=INK3)
axes[0].text(1.5, 0.35, "can't be read: the knock-out alone breaks it on plain text (+%.1f nats)" % gemma_txt.get("top10", 0),
             va="center", fontsize=8.5, color=INK3, style="italic")  # fmt: skip
row_labels(axes[0])
axes[0].set_xlabel("accuracy lost (points)")
axes[1].set_xlabel("answers switched to the written bridge's answer (%)")
axes[0].set_title("Remove the J-space: top-10 lens directions knocked out\nat the model's middle band (test set)", loc="left", fontsize=10)
axes[1].set_title("Write to it: the bridge's own lens direction added,\nat the layers where pasting the whole state works", loc="left", fontsize=10)
fig.legend([Line2D([], [], color=LOOKUP, marker="o", linestyle="", markersize=9), Line2D([], [], color=MEMORY, marker="o", linestyle="", markersize=9),
            Line2D([], [], color=INK3, marker="o", linestyle="", markersize=5, alpha=0.6), Line2D([], [], color=INK3, marker="|", linestyle="", markersize=10, markeredgewidth=2)],
           ["last step looks the answer up in the prompt (mean)", "last step recalls the answer from memory (mean)", "each chain type (hollow: computed bridge, not in the mean)",
            "same-size random removal (worst chain type)"], loc="upper left", bbox_to_anchor=(0.01, 0.905), ncol=2, frameon=False, fontsize=9)  # fmt: skip
fig.suptitle("Lookups respond little to the J-space in every model; memory recalls respond more, by an amount that varies by model",
             x=0.01, y=0.975, ha="left", fontsize=12)  # fmt: skip
foot(fig, "Big dots: means of the chain types the pre-registered rule uses, ending in a lookup (P→P, M→P) or a recall (P→M, M→M); gap = recall minus lookup. "
     "Computed-bridge chains (C→P, C→M) are shown hollow. Left: accuracy unedited "
     "minus knocked out, on items the model gets right (43-152 per chain type); band chosen on held-out items. Right: cross-validated best gated lens write "
     "(add or swap). " + FOOT)  # fmt: skip
fig.savefig(OUT / "story_fig1_remove_write_1022.png", dpi=200)
plt.close(fig)


# ---------------------------------------------------------------- Fig 2: depth on held-out ctrl_v8
def sweep(m):
    rows = rows_of(f"{m['p']}ctrl_sweep_v1")
    if not rows:
        return None
    bands = sorted({r["band"] for r in rows if r["band"].count("-") == 1 and r["band"][0] == "L"}, key=lambda b: int(b[1:].split("-")[0]))
    out = []
    for b in bands:
        lo, hi = (int(x) for x in b[1:].split("-"))
        if hi - lo + 1 > m["nl"] // 2:
            continue
        L = losses(f"{m['p']}ctrl_sweep_v1", b)
        out.append({"x": (lo + hi + 1) / 2 / m["nl"], "look": statistics.mean(L["paper10"][w] for w in ("PP", "MP")),
                    "mem": statistics.mean(L["paper10"][w] for w in ("PM", "MM")), "ctrl": max(L["paper10_rot"].values())})  # fmt: skip
    return out


fig, axs = plt.subplots(2, 3, figsize=(11, 6.4), sharey=True)
panels = MODELS + [dict(GEMMA, band="L48-56", ko=None)]
for ax, m in zip(axs.flat, panels, strict=False):
    style(ax, "y")
    ax.set_xlim(0, 1)
    ax.set_ylim(-3, 103)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0", "¼", "½", "¾", "1"])
    if m.get("band"):
        lo, hi = (int(x) for x in m["band"][1:].split("-"))
        ax.axvspan(lo / m["nl"], (hi + 1) / m["nl"], color=BAND, zorder=0)
    s = sweep(m)
    if s:
        xs = [b["x"] for b in s]
        ax.plot(xs, [b["ctrl"] for b in s], color=CONTROL, linewidth=1.3, zorder=2)
        ax.plot(xs, [b["look"] for b in s], color=LOOKUP, linewidth=2.2, marker="o", markersize=3.5, zorder=3)
        ax.plot(xs, [b["mem"] for b in s], color=MEMORY, linewidth=2.2, marker="o", markersize=3.5, zorder=3)
    ax.set_title(m["name"], loc="left", fontsize=10.5, fontweight="bold", pad=17)
    if m["name"] == GEMMA["name"]:
        note = f"dense, 60 layers · knock-out breaks plain text (+{gemma_txt.get('top10', 0):.1f} nats)"
    else:
        note = f"{m['kind'].split(' · ')[1]}, {m['nl']} layers · test-set gap at {m['band']}: {gap(m['ko']['paper10']):.0f}" + (
            f" (fresh seed {m['fresh_gap']:.0f})" if m.get("fresh_gap") is not None else "")
    ax.text(0, 1.035, note, transform=ax.transAxes, fontsize=8.3, color=INK2)
for ax in axs[1]:
    ax.set_xlabel("window depth (fraction of layers)")
for ax in axs[:, 0]:
    ax.set_ylabel("accuracy lost (points)")
leg = axs.flat[-1]
leg.axis("off")
leg.legend([Line2D([], [], color=MEMORY, linewidth=2.2), Line2D([], [], color=LOOKUP, linewidth=2.2), Line2D([], [], color=CONTROL, linewidth=1.3),
            plt.Rectangle((0, 0), 1, 1, color=BAND)],
           ["last step recalls from memory\n(P→M, M→M)", "last step looks up in the prompt\n(P→P, M→P)",
            "same-size random removal\n(worst of the four)", "middle band, chosen on these\nitems before the test set"],
           loc="center left", frameon=False, fontsize=9.5, labelspacing=1.4)  # fmt: skip
fig.suptitle("The knock-out by depth on held-out items: the hybrid Qwens separate recalls from lookups in their middle layers;\n"
             "Qwen3-32B does so weakly and late, Muse barely anywhere, and Gemma breaks on every chain type",
             x=0.01, y=0.985, ha="left", fontsize=11.5)  # fmt: skip
foot(fig, "ctrl_v8: same generator, another seed, no prompts shared with the test set (40-100 items per chain type). Top-10 lens directions removed "
     "at every position in a sliding window (9 layers on the 64-layer models and Gemma, 7 on Muse, 5 on the 9B), the answer's own directions kept. " + FOOT)  # fmt: skip
fig.subplots_adjust(left=0.07, right=0.99, top=0.83, bottom=0.13, hspace=0.6, wspace=0.12)
fig.savefig(OUT / "story_fig2_depth_1022.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- Fig 3: specificity and dose
CONDS = [("J++ top-10 (the knock-out)", "full2_ko_v1", "paper10", "o", MEMORY, True),
         ("J++ top-10, the bridge's own word kept", "full2_ko_keepown_v1", "paper10_keepown", "o", MEMORY, False),
         ("logit-lens top-10", "full2_ko_unembed_v1", "unembed10", "D", INK2, True),
         ("logit-lens top-K matching the J++ share of the residual (K = 50 on the 27B, 40 on the 9B)", "full2_ko_unembed_sized_v1", "unembedK", "D", INK2, False),
         ("same-size random (one mark per seed)", None, "paper10_rot", "|", INK3, True)]  # fmt: skip
fig = plt.figure(figsize=(11, 5.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1], left=0.15, right=0.975, top=0.7, bottom=0.18, wspace=0.27)
ax = fig.add_subplot(gs[0, 0])
style(ax)
ax.spines["left"].set_visible(False)
ax.set_yticks([])
ax.axvline(0, color=INK2, linewidth=0.8)
row_labels(ax, size=10)
for y, m in zip(ys, MODELS, strict=True):
    ax.axhline(y, color=GRID, linewidth=0.6, zorder=0)
    for label, run, cond, mk, col, filled in CONDS:
        runs = [f"{m['p']}{r}" for r in ("full2_ko_v1", "full2_ko_rotseed1_v1", "full2_ko_rotseed2_v1")] if run is None else [f"{m['p']}{run}"]
        for r in runs:
            LL = losses(r, m["band"])
            L = LL.get(cond) if cond != "unembedK" else next((v for c, v in LL.items() if c.startswith("unembed") and not c.endswith("_rot")), None)
            if L and len(L) == 6:
                ax.plot(gap(L), y, mk, color=col, markersize=12 if mk == "|" else 8, markeredgewidth=2 if mk == "|" else 1.6,
                        markerfacecolor=col if filled else SURFACE, zorder=3)  # fmt: skip
ax.set_xlim(-6, 42)
ax.set_ylim(0.45, len(MODELS) + 0.5)
ax.set_xlabel("recall-final minus lookup-final accuracy loss (points)")
ax.set_title("A. What the effect is specific to (test set, each model's band)", loc="left", fontsize=10)
fig.legend([Line2D([], [], color=c, marker=mk, linestyle="", markersize=10 if mk == "|" else 7, markeredgewidth=2 if mk == "|" else 1.5,
                   markerfacecolor=c if f else SURFACE) for _, _, _, mk, c, f in CONDS], [c[0] for c in CONDS],
           loc="upper left", bbox_to_anchor=(0.01, 0.885), ncol=2, frameon=False, fontsize=8.6)  # fmt: skip
ax2 = fig.add_subplot(gs[0, 1])
style(ax2, "y")
KS = [1, 2, 5, 10, 25, 50, 100]
DOSE = [("27B", [("full2_ko_v1", "L32-40"), ("full2_dose_v1", "L32-40")], "#0f766e"),
        ("9B", [("qwen35_9b_full2_ko_v1", "L12-16"), ("qwen35_9b_full2_dose_v1", "L12-16")], "#b45309"),
        ("Qwen3-32B", [("qwen3_32b_full_dose_v1", "L44-52")], "#3b3a37"),
        ("Muse", [("muse30_full2_ko_v1", "L36-42"), ("muse30_full2_dose_v1", "L36-42")], "#8a5cc2")]  # fmt: skip
ymax_dose = 10.0
for name, srcs, col in DOSE:
    if not all((AB / run / "summary.json").exists() for run, _ in srcs):
        continue  # a dose run still in progress is never drawn
    for rot in (False, True):
        pts = {}
        for run, b in srcs:
            for c, L in losses(run, b).items():
                base = c[:-4] if c.endswith("_rot") else c
                if c.endswith("_rot") != rot or not (base == "paper10" or (base.startswith("top") and base[3:].isdigit())):
                    continue
                pts[10 if base == "paper10" else int(base[3:])] = gap(L)
        if pts:
            ks = sorted(pts)
            ymax_dose = max(ymax_dose, max(pts.values()))
            ax2.plot(ks, [pts[k] for k in ks], "--" if rot else "-", color=col, marker=None if rot else "o", markersize=4, linewidth=1.3 if rot else 2.2)
            if not rot:
                ax2.text(ks[-1] * 1.15, pts[ks[-1]], name, va="center", fontsize=9.5, color=col, fontweight="bold")
ax2.set_xscale("log")
ax2.set_xticks(KS, [str(k) for k in KS])
ax2.minorticks_off()
ax2.set_xlim(0.8, 330)
ax2.set_ylim(-5, ymax_dose + 6)
ax2.set_xlabel("lens directions removed per position")
ax2.set_ylabel("recall minus lookup loss (points)")
ax2.set_title("B. More directions removed (dashed: random)", loc="left", fontsize=10)
fig.suptitle("In the hybrid Qwens the effect is specific to the J++ lens: logit-lens and random removals do almost nothing, keeping the\n"
             "bridge's word restores only a quarter, and even one lens direction opens a 20-31 point gap; Qwen3-32B and Muse stay low",
             x=0.01, y=0.985, ha="left", fontsize=11)  # fmt: skip
foot(fig, "Gap: mean accuracy lost by P→M, M→M minus P→P, M→P (the pre-registered rule's chain types). Not run: keep-own on Muse; the "
     "share-matched logit lens on Qwen3-32B and Muse (their J++ and logit-lens top-10 take the same share). " + FOOT, 7.3)  # fmt: skip
fig.savefig(OUT / "story_fig3_specificity_1022.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- Fig 4: task variants (loss beyond the random control)
ITEMS = {it["id"]: it for s in ("full_v8", "full_v8b") for it in T.load(s)}
FORMATS = ["prose", "chat", "document", "json", "table", "code"]
LEVELS = ["level 0 (easiest)", "level 1", "level 2", "level 3 (hardest)"]
TWO = [("P→P", "PP"), ("M→P", "MP"), ("C→P", "CP"), ("P→M", "PM"), ("M→M", "MM"), ("C→M", "CM")]
THREE = [("P→P→P", "PPP"), ("M→P→P", "MPP"), ("P→M→P", "PMP"), ("M→M→P", "MMP"), ("P→P→M", "PPM"), ("M→P→M", "MPM")]


def per_item(run, band, kinds=("clean",)):
    rows = rows_of(run)
    if rows is None or not band:
        return None
    out = collections.defaultdict(dict)
    for r in rows:
        if r["kind"] in kinds and (r["band"] == band or r["condition"] == "none"):
            out[(r["kind"], r["family"], r["id"])][r["condition"]] = r["correct"]
    return out


def net(cells):
    pairs = [(c["paper10_rot"], c["paper10"]) for c in cells if "paper10" in c and "paper10_rot" in c and c.get("none", 1)]  # items right unedited
    return (100 * (statistics.mean(a for a, _ in pairs) - statistics.mean(b for _, b in pairs)), len(pairs)) if pairs else (None, 0)


V = {}
for m in MODELS:
    two, three = per_item(f"{m['p']}full2_ko_v1", m["band"]), per_item(f"{m['p']}full3_ko_v1", m["band"])
    d = {}
    for lab, fam in TWO:
        d[lab] = net([v for (k, f, i), v in two.items() if f == fam]) if two else (None, 0)
    for lab, fam in THREE:
        d[lab] = net([v for (k, f, i), v in three.items() if f == fam]) if three else (None, 0)
    for key, groups, labs in (("format", FORMATS, FORMATS), ("level", [0, 1, 2, 3], LEVELS)):
        for g, lab in zip(groups, labs, strict=True):
            per = {fam: net([v for (k, f, i), v in two.items() if f == fam and ITEMS[i][key] == g])[0] for fam in RLOOK + RMEM} if two else {}
            ok = bool(per) and all(x is not None for x in per.values())
            d[lab] = (statistics.mean(per[f] for f in RMEM) - statistics.mean(per[f] for f in RLOOK) if ok else None,
                      sum(1 for (k, f, i) in two if ITEMS[i][key] == g) if two else 0)  # fmt: skip
    cats = collections.defaultdict(list)
    for run in (f"{m['p']}full2_ko_steps_v1", f"{m['p']}{m.get('three_steps', 'full3_ko_steps_v1')}"):
        for (kind, fam, i), v in (per_item(run, m["band"], kinds=("step1", "step2", "step3")) or {}).items():
            k = int(kind[-1])
            src = ITEMS[i]["steps"][k - 1]["source"]
            cats[{"P": "lookup", "C": "computed"}.get(src, "first" if k == 1 else "later")].append(v)
    lk = net(cats["lookup"]) if cats.get("lookup") else (None, 0)
    for c, lab in (("later", "a later recall step"), ("first", "a first-step recall")):
        r = net(cats[c]) if cats.get(c) else (None, 0)
        d[lab] = (r[0] - lk[0] if r[0] is not None and lk[0] is not None else None, r[1])
    V[m["name"]] = d
Path("results/cross_model/variants_story_1022.json").write_text(json.dumps(V, indent=2) + "\n")
cmap = LinearSegmentedColormap.from_list("mem", [SURFACE, "#fbd9c4", "#f4a172", MEMORY, "#a8410f"])
fig = plt.figure(figsize=(8.2, 6.4))
gs = fig.add_gridspec(1, 1, left=0.2, right=0.985, top=0.78, bottom=0.11)
blocks = [(fig.add_subplot(gs[0, 0]), "Recall-final minus lookup-final loss (points)",
           [("two-step chains, by prompt format", FORMATS), ("two-step chains, by difficulty", LEVELS)])]  # fmt: skip
for ax, title, groups in blocks:
    labels, heads, y = [], [], 0.0
    for head, rs in groups:
        heads.append((y, head))
        for r in rs:
            y += 1
            labels.append((y, r))
        y += 0.9
    ax.set_xlim(-0.5, len(MODELS) - 0.5)
    ax.set_ylim(y - 0.4, -0.3)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(range(len(MODELS)), [m["name"].replace(" Glimmer 30B", "\nGlimmer 30B").replace("-", "-​") if False else
                                       f"{m['name'].split(' ')[0]}\n{m['kind'].split(' · ')[1]}" for m in MODELS], fontsize=8.8)  # fmt: skip
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    ax.set_yticks([yy for yy, _ in labels], [lab for _, lab in labels], fontsize=9)
    for yy, head in heads:
        ax.text(-0.5, yy + 0.25, head, ha="left", va="center", fontsize=8.5, color=INK2, style="italic")
    for c, m in enumerate(MODELS):
        for yy, lab in labels:
            v, n = V[m["name"]].get(lab, (None, 0))
            if v is None:
                ax.add_patch(plt.Rectangle((c - 0.47, yy - 0.45), 0.94, 0.9, facecolor=SURFACE, edgecolor=GRID, hatch="///", linewidth=0.6))
                ax.text(c, yy, "running" if m["name"] in RUNNING else "–", ha="center", va="center", fontsize=7.5, color=INK3)
                continue
            dark = v > 33
            ax.add_patch(plt.Rectangle((c - 0.47, yy - 0.45), 0.94, 0.9, facecolor=cmap(min(max(v, 0), 50) / 50), edgecolor=SURFACE, linewidth=1.5))
            ax.text(c, yy - 0.07, f"{v:.0f}", ha="center", va="center", fontsize=9.5, color="white" if dark else INK, fontweight="bold")
            ax.text(c, yy + 0.29, f"n={n}", ha="center", va="center", fontsize=6, color="white" if dark else INK3)
    ax.set_title(title, loc="left", fontsize=10, pad=30)
fig.suptitle("By prompt format and difficulty: the hybrid Qwens show the split in every format\nand level; Qwen3-32B unevenly and at about half the size; Muse barely",
             x=0.01, y=0.985, ha="left", fontsize=11.5)  # fmt: skip
foot(fig, "Points lost beyond the same-size random removal (random-control accuracy minus knock-out accuracy, same items, items right unedited), at each model's middle band. "
     "Each cell: mean of P→M, M→M minus mean of P→P, M→P (20-60 items per type per cell). " + FOOT, 7.3)  # fmt: skip
fig.savefig(OUT / "story_fig5_formats_1022.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- Fig 5: lens write by single layer (direct-output check)
LATE = [m for m in MODELS if m["late"] and (WM / "late_check" / f"{m['late']}.json").exists()]
fig, axs = plt.subplots(1, len(LATE), figsize=(11, 3.9), sharey=True, squeeze=False)
for ax, m in zip(axs[0], LATE, strict=True):
    style(ax, "y")
    d = load(WM / "late_check" / f"{m['late']}.json")["best_flips_lens_add_final_by_layer"]
    layers = sorted(int(k) for k in d["MM"] if k.isdigit())
    lo, hi = (int(x) for x in m["c2"]["band"][1:].split("-"))
    ax.axvspan(lo / m["nl"], (hi + 1) / m["nl"], color=BAND, zorder=0)
    xs = [la / m["nl"] for la in layers]
    for words, col in ((RMEM, MEMORY), (RLOOK, LOOKUP)):
        ax.plot(xs, [100 * statistics.mean(d[w][str(la)] for w in words) for la in layers], color=col, linewidth=2.2, marker="o", markersize=3.5)
    ax.plot(xs, [100 * d["MM"][str(la)] for la in layers], color=MEMORY, linewidth=1.2, linestyle="--")
    ax.set_xlim(0.4, 1)
    ax.set_ylim(-3, 80)
    ax.set_title(f"{m['name']} ({m['nl']} layers)", loc="left", fontsize=10.5, fontweight="bold")
    ax.set_xlabel("layer written (fraction of layers)")
axs[0][0].set_ylabel("answers switched (%)")
axs[0][-1].legend([Line2D([], [], color=MEMORY, linewidth=2.2), Line2D([], [], color=MEMORY, linewidth=1.2, linestyle="--"),
                   Line2D([], [], color=LOOKUP, linewidth=2.2), plt.Rectangle((0, 0), 1, 1, color=BAND)],
                  ["last step recalls (P→M, M→M)", "M→M alone", "last step looks up (P→P, M→P)", "band used for C2"],
                  loc="upper right", frameon=False, fontsize=8.5)  # fmt: skip
fig.suptitle("The lens write works up to about ⅔-⅘ of the depth and stops before the output, so it isn't a direct push on the answer",
             x=0.01, y=0.98, ha="left", fontsize=11.5)  # fmt: skip
foot(fig, "Best gated add of the bridge's own lens direction at the final position, one layer at a time (best cell per layer, not cross-validated). "
     "Qwen3-32B and Muse; the 27B's writes already vanish by L56-60 of its own band. " + FOOT)  # fmt: skip
fig.subplots_adjust(left=0.07, right=0.99, top=0.82, bottom=0.2, wspace=0.08)
fig.savefig(OUT / "story_fig6_late_1022.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- Fig 6: two- and three-step chains together
from matplotlib.patches import FancyBboxPatch  # noqa: E402

GROUPS = [("no recall after the first step", ["P→P", "C→P", "M→P", "P→P→P", "M→P→P"], CONTROL),
          ("a later recall, then a lookup", ["P→M→P", "M→M→P"], "#f4a172"),
          ("the last step recalls", ["P→M", "C→M", "M→M", "P→P→M", "M→P→M"], MEMORY)]  # fmt: skip
STEPCATS = [("lookup", "a lookup step", LOOKUP), ("computed", "a computed step", CONTROL),
            ("first", "a recall as the first step", "#f4a172"), ("later", "a recall after the first step", MEMORY)]  # fmt: skip
SV = {}
for m in MODELS:
    cats = collections.defaultdict(list)
    for run, n in ((f"{m['p']}full2_ko_steps_v1", 2), (f"{m['p']}{m.get('three_steps', 'full3_ko_steps_v1')}", 3)):
        for (kind, fam, i), v in (per_item(run, m["band"], kinds=("step1", "step2", "step3")) or {}).items():
            k = int(kind[-1])
            src = ITEMS[i]["steps"][k - 1]["source"]
            cats[({"P": "lookup", "C": "computed"}.get(src, "first" if k == 1 else "later"), n)].append(v)
    SV[m["name"]] = {key: net(v) for key, v in cats.items()}
CHIP = {"P": LOOKUP, "M": MEMORY, "C": CONTROL}
rows = []  # (y, kind, payload)
y = 0.0
for head, chains, col in GROUPS:
    rows.append((y, "head", head))
    y += 0.85
    for ch in chains:
        rows.append((y, "chain", (ch, col)))
        y += 1
    y += 0.35
rows.append((y + 0.25, "head2", "the same knock-out on one step asked on its own (two-step chains / three-step chains)"))
y += 1.1
for key, lab, col in STEPCATS:
    rows.append((y, "step", (key, lab, col)))
    y += 1.15
H = y
FH = 0.33 * H + 2.4
fig = plt.figure(figsize=(11, FH))
gs = fig.add_gridspec(1, 1 + len(MODELS), width_ratios=[1.55] + [1] * len(MODELS), left=0.015, right=0.985,
                      top=1 - 1.75 / FH, bottom=0.75 / FH, wspace=0.12)  # fmt: skip
axL = fig.add_subplot(gs[0, 0])
axL.set_xlim(0, 10)
axL.set_ylim(H - 0.3, -0.6)
axL.axis("off")
XMAX = 50
for c, m in enumerate(MODELS):
    ax = fig.add_subplot(gs[0, c + 1])
    ax.set_xlim(-12, XMAX + 8)
    ax.set_ylim(H - 0.3, -0.6)
    ax.axis("off")
    ax.text((XMAX - 12) / 2, -1.5, f"{m['name']}\n{m['kind'].split(' · ')[1]}", ha="center", va="bottom", fontsize=9.5, fontweight="bold")
    for yy, kind, pl in rows:
        if kind in ("head", "head2"):
            continue
        ax.plot([0, 0], [yy - 0.45, yy + 0.45], color=INK2, linewidth=0.8)
        if kind == "chain":
            ch, col = pl
            v, n = V[m["name"]].get(ch, (None, 0))
            bars = [(v, n, col, yy, 0.62)]
        else:
            key, lab, col = pl
            bars = [(SV[m["name"]].get((key, k), (None, 0))[0], SV[m["name"]].get((key, k), (None, 0))[1], col, yy + off, 0.38)
                    for k, off in ((2, -0.22), (3, 0.22))]  # fmt: skip
        for i, (v, n, col, yb, h) in enumerate(bars):
            if v is None and kind == "step":
                continue  # three-step chains have no computed step
            if v is None:
                ax.text(1, yb, "running" if m["name"] in RUNNING else "–", va="center", fontsize=7.5, color=INK3)
                continue
            shade = col if (kind == "chain" or i == 0) else col + "99"
            ax.barh(yb, max(min(v, XMAX), -12), height=h, color=shade, edgecolor="none")
            ax.text(max(v, 0) + 1.5, yb, f"{round(v) + 0}", va="center", fontsize=8 if kind == "chain" else 7, color=INK)
            if kind == "chain" and n < 30:
                ax.text(max(v, 0) + 9, yb, f"n={n}", va="center", fontsize=6.5, color=INK3)
for yy, kind, pl in rows:
    if kind == "head":
        axL.text(0, yy, pl, fontsize=8.8, color=INK2, style="italic", va="center")
    elif kind == "head2":
        axL.text(0, yy, pl, fontsize=8.8, color=INK2, style="italic", va="center")
    elif kind == "chain":
        ch, _ = pl
        steps = ch.split("→")
        x = 3.2 if len(steps) == 2 else 1.6
        for j, st in enumerate(steps):
            axL.add_patch(FancyBboxPatch((x, yy - 0.32), 1.0, 0.64, boxstyle="round,pad=0.02,rounding_size=0.15", facecolor=CHIP[st], edgecolor="none"))
            axL.text(x + 0.5, yy, st, ha="center", va="center", fontsize=8.5, color="white", fontweight="bold")
            if j < len(steps) - 1:
                axL.annotate("", xy=(x + 1.55, yy), xytext=(x + 1.05, yy), arrowprops=dict(arrowstyle="-|>", color=INK3, lw=1))
            x += 1.6
    else:
        key, lab, col = pl
        axL.text(9.9, yy, lab, ha="right", va="center", fontsize=8.8)
fig.suptitle("Two- and three-step chains together: the knock-out hurts a chain when a recall from memory comes after the first step,\n"
             "most when the recall is the last step, in every model; how much depends on the model", x=0.01, y=0.995, ha="left", fontsize=11.5)  # fmt: skip
fig.legend([plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=MEMORY), plt.Rectangle((0, 0), 1, 1, color=CONTROL)],
           ["P: looked up in the prompt", "M: recalled from memory", "C: computed (misspelling repaired, name reversed, name from its letters)"],
           loc="upper left", bbox_to_anchor=(0.01, 1 - 0.62 / FH), ncol=3, frameon=False, fontsize=8.8)  # fmt: skip
foot(fig, "Points lost beyond the same-size random removal (random-control minus knock-out accuracy, same items, items right unedited) at each "
     "model's middle band; whole question for the chains, one step asked on its own below (darker bar: steps of two-step chains, lighter: of "
     "three-step chains). 15-152 items per chain type (n shown below 30). " + FOOT, 7.2)  # fmt: skip
fig.savefig(OUT / "story_fig4_chains_1022.png", dpi=200)
plt.close(fig)
print("saved", sorted(p.name for p in OUT.glob("story_fig*_1022.png")))
