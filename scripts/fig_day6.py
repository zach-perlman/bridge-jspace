"""fig_day6 (Zach, 2026-10-25): the day-6 summary figures, from committed result files only.
  1 v2_split.png      the v2 knock-out per model: recall minus stated (M - K), J-lens vs its controls
  2 mechanism.png     per model (module 1, v1): knock-out at every token; the swap and the removal at the bridge mention
  3 readout.png       per model (module 1, v1): the recalled attribute read at the bridge mention across depth
  4 positions.png     27B and 9B (module 1, v1): where along the prompt the knock-out must act, per start
Colours: J-lens top-10 blue, logit lens orange, the J-part's complement aqua (validated: dataviz validate_palette).
Intervals: 95% bootstrap over bridges (seed 0), as scored; removal-at-mention intervals computed here the same way.

python scripts/fig_day6.py   (writes figures/archive/day6/*.png)
"""

from __future__ import annotations

import collections
import json
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
import sys  # noqa: E402

sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
RES = ROOT / "results"
OUT = ROOT / "figures" / "archive" / "day6"
J, LOGIT, COMP = "#2a78d6", "#eb6834", "#1baf7a"
MARK = {J: "o", LOGIT: "s", COMP: "D"}  # shape as the second channel: identity never by colour alone
INK, INK2, MUTED, GRID, AXIS, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.edgecolor": AXIS, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.titlesize": 10, "axes.titleweight": "bold"})  # fmt: skip


def load(p):
    return json.loads((RES / p).read_text())


def style(ax, xgrid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    if xgrid:
        ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def dots(ax, rows, series, xlabel, xlim):
    """rows: [name, {series_key: (value, [lo, hi]) or None}]; series: [(key, label, colour)] drawn top to bottom."""
    k = len(series)
    offs = [(i - (k - 1) / 2) * 0.22 for i in range(k)]
    for r, (_, vals) in enumerate(rows):
        for (key, lab, col), off in zip(series, offs, strict=True):
            v = vals.get(key)
            if v is None:
                continue
            y = r + off
            ax.plot([v[1][0], v[1][1]], [y, y], color=col, lw=1.4, solid_capstyle="round", zorder=2)
            ax.plot(v[0], y, MARK[col], ms=6.5 if MARK[col] == "o" else 5.5, color=col, mec=SURF, mew=1.2, zorder=3)
            ax.text(v[1][1] + (xlim[1] - xlim[0]) * 0.012, y, f"{v[0]:+.0f}", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(rows)), [n for n, _ in rows])
    ax.set_ylim(len(rows) - 0.5, -0.75)
    ax.axvline(0, color=AXIS, lw=1)
    ax.set_xlim(*xlim)
    ax.set_xlabel(xlabel)
    style(ax)


def legend(fig, series, y=0.9):
    from matplotlib.lines import Line2D

    hs = [Line2D([], [], color=c, marker=MARK[c], ms=6 if MARK[c] == "o" else 5, mec=SURF, lw=1.4, label=lab) for lab, c in series]
    fig.legend(handles=hs, loc="upper left", bbox_to_anchor=(0.01, y), ncol=len(hs), frameon=False, fontsize=8, handlelength=1.8)


def foot(fig, text):
    fig.text(0.01, 0.01, text, fontsize=7, color=MUTED, va="bottom", ha="left", wrap=True)


def fig1():
    runs = [("27B", "jsuite_v2_test_chat_ko_cand2_v1"), ("9B", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1"),
            ("9B base (raw text)", "qwen35_9bb_jsuite_v2_test_qa_ko_cand2_v1"), ("122B", "qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1")]  # fmt: skip
    rows = []
    for name, r in runs:
        f = load(f"ablate_v2/jsuite2_score/{r}.json")["facts"]
        g = lambda c: (f[f"{c}/start=all"]["contrasts"]["M-K"]["diff"], f[f"{c}/start=all"]["contrasts"]["M-K"]["ci"])  # noqa: E731
        rows.append((name, {"j": g("paper10"), "u": g("unembed10"), "r": g("paper10_rot")}))
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    dots(ax, rows, [("j", "", J), ("u", "", LOGIT), ("r", "", COMP)], "recall minus stated (M - K): extra points lost on recall", (-8, 68))
    legend(fig, [("knock out 10 J-lens directions", J), ("10 logit-lens directions (control)", LOGIT), ("10 random directions (control)", COMP)], y=0.9)
    ax.axvline(30, color=MUTED, lw=0.8, ls=(0, (3, 3)))
    ax.text(30.6, len(rows) - 0.62, "pre-registered\nthreshold (30)", fontsize=7, color=MUTED, va="bottom")
    ax.axvline(10, color=MUTED, lw=0.6, ls=(0, (1, 3)))
    ax.text(10.6, len(rows) - 0.62, "controls < 10", fontsize=7, color=MUTED, va="bottom")
    fig.suptitle("v2: removing 10 J-lens directions breaks recall but not lookup, in all four Qwens", x=0.01, ha="left", fontsize=10.5, fontweight="bold")
    foot(fig, "jsuite_v2 test, 8 relations, all starts; n = 515-893 items per final per model; each model's band (27B L32-40, 9B L12-16,\n"
              "122B L39-45). 27B, 9B pre-registered (amendment 33); 9B base, 122B judged post hoc. 95% bootstrap over bridges (seed 0);\n"
              "one rendering seed. The 122B's logit-lens control (+12) fails the < 10 threshold.")  # fmt: skip
    fig.subplots_adjust(left=0.17, right=0.97, top=0.8, bottom=0.27)
    fig.savefig(OUT / "v2_split.png", dpi=200)


def remove_loss(run: str, fam: str | tuple = "PM") -> tuple[float, list[float]]:
    rows = [json.loads(x) for x in (RES / "jswap" / run / "rows.jsonl").read_text().splitlines()]
    ok = {r["id"] for r in rows if r["condition"] == "none" and r["cls"] == "kept"}
    fams = (fam,) if isinstance(fam, str) else fam
    rs = [r for r in rows if r["family"] in fams and r["condition"] == "remove" and r["id"] in ok]
    by = collections.defaultdict(list)
    for r in rs:
        by[r["x"]].append(r["cls"] != "kept")
    keys, rng = sorted(by), random.Random(0)
    loss = lambda ks: 100 * sum(sum(by[k]) for k in ks) / sum(len(by[k]) for k in ks)  # noqa: E731
    bs = sorted(loss([rng.choice(keys) for _ in keys]) for _ in range(1000))
    return round(loss(keys), 1), [round(bs[25], 1), round(bs[974], 1)]


MODELS = [("27B", "jsuite_v1_facts_test_chat_ko_cand2_v1", "jswap_v1", "bridge_readout_v1", 64, (32, 40)),
          ("9B", "qwen35_9b_jsuite_v1_facts_test_chat_ko_cand2_v1", "qwen35_9b_jswap_v1", "qwen35_9b_bridge_readout_v1", 32, (12, 16)),
          ("122B", "qwen35_122b_jsuite_v1_facts_test_chat_ko_cand2_v1", "qwen35_122b_jswap_v1", "qwen35_122b_bridge_readout_v1", 48, (39, 45)),
          ("OLMo-3 32B", "olmo32_jsuite_v1_facts_test_qa_ko_cand2_v1", "olmo32_jswap_v1", "olmo32_bridge_readout_v1", 64, (12, 20)),
          ("Muse 30B", "muse30_jsuite_v1_facts_test_chat_ko_cand2_v1", "muse30_jswap_l14_20_v1", "muse30_bridge_readout_v1", 52, (36, 42))]  # fmt: skip


def fig2():
    ko, sw, rm = [], [], []
    for name, kor, swr, _, _, _ in MODELS:
        c = load(f"ablate_v2/jsuite_score/{kor}.json")["cells"]
        g = lambda k: (c[k]["contrasts"]["M-P"]["diff"], c[k]["contrasts"]["M-P"]["ci"])  # noqa: E731
        ko.append((name, {"j": g("all/paper10"), "u": g("all/unembed10")}))
        from scripts.jswap import score

        rows = [json.loads(x) for x in (RES / "jswap" / swr / "rows.jsonl").read_text().splitlines()]
        s = score([{**r, "family": "MEM"} for r in rows if r["family"] in ("PM", "TM")])
        sw.append((name, {"j": (s["MEM/swap"]["transfer"], s["MEM/swap"]["ci"]), "c": (s["MEM/swap_comp"]["transfer"], s["MEM/swap_comp"]["ci"])}))
        rm.append((name, {"j": remove_loss(swr, ("PM", "TM"))}))
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.6), sharey=True)
    dots(axs[0], ko, [("j", "", J), ("u", "", LOGIT)], "recall minus made-up fact (M - P), points", (-25, 90))
    axs[0].set_title("A  Knock-out at every token:\nis the J-part needed?", loc="left")
    dots(axs[1], sw, [("j", "", J), ("c", "", COMP)], "answers moved to the donor's (transfer, points)", (-10, 100))
    axs[1].set_title("B  Swap it in at the mention:\ndoes the answer follow?", loc="left")
    dots(axs[2], rm, [("j", "", J)], "recall answers lost, points", (-5, 55))
    legend(fig, [("J-lens top-10 directions", J), ("logit-lens top-10 (control)", LOGIT), ("everything but the J-part", COMP)], y=0.9)
    axs[2].set_title("C  Remove it at the mention only:\nis it needed there?", loc="left")
    fig.suptitle("All five models carry the recalled attribute in the J-part at the bridge mention; how much they need it there varies",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold")  # fmt: skip
    foot(fig, "Module 1 (jsuite_v1 facts test; OLMo raw text). A: all starts, n 313-641 items per final. B, C: memory finals of the read and tracked "
              "starts pooled (PM + TM), n 204-438; the last token of each\nbridge mention, across the band. Bands: 27B L32-40, 9B L12-16, 122B L39-45, "
              "OLMo L12-20; Muse knock-out L36-42, its swap and removal L14-20 (exploratory: the third band tried).\nRandom and logit-lens swaps move "
              "answers <= 1 point in every model (not drawn). 95% bootstrap over bridges (seed 0). Muse's knock-out (A) is mostly shared with the logit lens.")  # fmt: skip
    fig.subplots_adjust(left=0.1, right=0.99, top=0.7, bottom=0.25, wspace=0.12)
    fig.savefig(OUT / "mechanism.png", dpi=200)


def fig3():
    fig, axs = plt.subplots(1, 5, figsize=(11, 2.9), sharey=True)
    for ax, (name, _, _, ror, nl, band) in zip(axs, MODELS, strict=True):
        s = load(f"bridge_readout/{ror}/summary.json")
        las = sorted({int(k.split("/")[0][1:]) for k in s})
        x = [la / nl for la in las]
        ax.axvspan(band[0] / nl, band[1] / nl, color=GRID, alpha=0.7, lw=0)
        ax.plot(x, [s[f"L{la}/jlens/PM"]["top_among_candidates"] for la in las], color=J, lw=1.6)
        ax.plot(x, [s[f"L{la}/logit/PM"]["top_among_candidates"] for la in las], color=LOGIT, lw=1.6)
        ax.axhline(s[f"L{las[0]}/jlens/PM"]["chance"], color=MUTED, lw=0.8, ls=(0, (3, 3)))
        ax.set_title(f"{name}", loc="left")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 100)
        ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.text(0.98, 3, f"n {s[f'L{las[0]}/jlens/PM']['n']}", ha="right", fontsize=7, color=MUTED)
        style(ax, xgrid=False)
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.spines["bottom"].set_visible(True)
    axs[0].set_ylabel("true attribute ranked first\namong candidates, %")
    axs[0].text(0.3, 100, "J-lens", color=J, fontsize=8, fontweight="bold", va="bottom")
    axs[0].text(0.5, 30, "logit lens", color=LOGIT, fontsize=8, fontweight="bold")
    axs[1].text(0.55, 13, "chance", color=MUTED, fontsize=7)
    for ax in axs:
        ax.set_xlabel("relative depth")
    fig.suptitle("At the bridge mention every model's J-lens reads the recalled attribute; the logit lens lags in the 27B, 9B and Muse",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold")  # fmt: skip
    foot(fig, "Module 1 (jsuite_v1 facts test; OLMo raw text), read start with a memory final (PM: the passage never states the attribute); the last "
              "token of the bridge's first mention, every 2nd layer.\nShaded: the knock-out band. On v1 the layer-0 logit-lens floor sits above "
              "chance on some models (122B 38%); on v2 (9B, 27B) it is at chance. Descriptive, no prediction.")  # fmt: skip
    fig.subplots_adjust(left=0.08, right=0.99, top=0.78, bottom=0.27, wspace=0.08)
    fig.savefig(OUT / "readout.png", dpi=200)


def fig4():
    modes = [("", "every token"), ("posbridge", "bridge mention\nonly"), ("poscontext", "passage\nonly"),
             ("posquestion", "question\nonly"), ("posfinal", "answer position\nonly")]  # fmt: skip
    starts = [("P", "bridge read from the passage", J), ("T", "bridge tracked through a story", LOGIT), ("M", "bridge recalled from a description", COMP)]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.5), sharey=True)
    for ax, (name, pre) in zip(axs, (("27B (L32-40)", ""), ("9B (L12-16)", "qwen35_9b_")), strict=True):
        for mi, (m, _) in enumerate(modes):
            c = load(f"ablate_v2/jsuite_score/{pre}jsuite_v1_facts_test_chat_ko_cand2{'_' + m if m else ''}_v1.json")["cells"]
            for si, (s, lab, col) in enumerate(starts):
                d = c[f"{s}/paper10"]["contrasts"]["M-P"]
                x = mi + (si - 1) * 0.22
                ax.plot([x, x], d["ci"], color=col, lw=1.4, solid_capstyle="round")
                ax.plot(x, d["diff"], MARK[col], ms=6.5 if MARK[col] == "o" else 5.5, color=col, mec=SURF, mew=1.2, zorder=3)
        ax.axhline(0, color=AXIS, lw=1)
        ax.set_xticks(range(len(modes)), [lab for _, lab in modes], fontsize=8)
        ax.set_title(name, loc="left")
        ax.set_ylim(-20, 105)
        style(ax, xgrid=False)
        ax.grid(axis="y", color=GRID, lw=0.6)
    axs[0].set_ylabel("recall minus made-up fact\n(M - P), points")
    legend(fig, [(lab, col) for _, lab, col in starts], y=0.9)
    fig.suptitle("Where the knock-out must act: on the bridge's own tokens when it was read, in the question when it was recalled",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold")  # fmt: skip
    foot(fig, "Module 1 (jsuite_v1 facts test, chat), the J-lens knock-out restricted to one region (amendment 30); n per start 78-251 items per final; "
              "the bridge-mention edit is ~2 tokens x 5-9 layers.\n95% bootstrap over bridges (seed 0). v1's recalled-start memory passages never name "
              "the bridge, so 'bridge mention only' leaves them unedited (~0 by construction);\nnegative values: the edit hurt the made-up-fact (P) question more.")  # fmt: skip
    fig.subplots_adjust(left=0.09, right=0.99, top=0.72, bottom=0.28, wspace=0.06)
    fig.savefig(OUT / "positions.png", dpi=200)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (fig1, fig2, fig3, fig4):
        f()
        print(f.__name__, "ok")
