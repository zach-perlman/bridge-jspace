"""fig_story (Zach, 2026-10-25): one-page summary of the breadth half (does the memory-vs-prompt split hold, and where),
for a reader new to the project, from committed results only. Writes figures/archive/day6/story.png.

python scripts/fig_story.py
"""

from __future__ import annotations

import collections
import json
import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from scripts.fig_day6 import AXIS, COMP, GRID, INK, INK2, LOGIT, MODELS, MUTED, SURF, J, load, remove_loss  # noqa: E402
from scripts.jswap import score  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
LOOK = "#9ec5f4"  # the J-lens knock-out on lookup questions: same condition, lighter step of its hue
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK, "axes.edgecolor": AXIS, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})  # fmt: skip


def losses(run: str, set_name: str, finals=("M", "K"), conds=("paper10", "unembed10", "paper10_rot")) -> dict:
    """Points lost per final and condition (facts, all starts; items right unedited), 95% bootstrap over bridges."""
    items = {json.loads(x)["id"]: json.loads(x) for x in (DATA / set_name / "items.jsonl").read_text().splitlines()}
    rows = [json.loads(x) for x in (RES / "ablate_v2" / run / "rows.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] == "clean" and r["id"] in items and items[r["id"]].get("module", "facts") == "facts"]
    ok = {(r["family"], r["id"]) for r in rows if r["condition"] == "none" and r["correct"]}
    out = {}
    for c in conds:
        for f in finals:
            by = collections.defaultdict(list)
            for r in rows:
                it = items[r["id"]]
                if r["condition"] == c and (r["family"], r["id"]) in ok and it["word"][1] == f:
                    by[f"{it.get('relation', '')}:{it['steps'][0]['answer']}"].append(not r["correct"])
            keys, rng = sorted(by), random.Random(0)
            lo = lambda ks: 100 * sum(sum(by[k]) for k in ks) / sum(len(by[k]) for k in ks)  # noqa: E731
            bs = sorted(lo([rng.choice(keys) for _ in keys]) for _ in range(1000))
            out[(c, f)] = (lo(keys), bs[25], bs[974], sum(len(v) for v in by.values()))
    return out


def card(ax, x, y, w, h, fc="#f3f2ee"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.015", fc=fc, ec=GRID, lw=0.8, transform=ax.transAxes))


def panel_a(ax):
    ax.axis("off")
    ax.text(0, 1.0, "A   The test", fontsize=12.5, fontweight="bold", va="top")
    ax.text(0, 0.925, "Two-step questions over a short passage. The model must first work out an intermediate\n"
                      "entity (the 'bridge', here Adidas), then give a fact about it.", fontsize=9.5, color=INK2, va="top")  # fmt: skip
    card(ax, 0.0, 0.47, 1.0, 0.33)
    ax.text(0.03, 0.775, "Passage (shortened)", fontsize=8.5, color=MUTED, va="top")
    ax.text(0.03, 0.72, "“Mark Ellison's business school thesis was about Adidas. Volvo has\n"
                        "announced a new regional office in India. …”", fontsize=9.5, va="top", style="italic")  # fmt: skip
    ax.text(0.03, 0.585, "Question: What is the country of origin of the company\nMark Ellison's thesis was about?", fontsize=9.5, va="top")
    card(ax, 0.0, 0.05, 0.485, 0.36, fc="#e8f1fc")
    card(ax, 0.515, 0.05, 0.485, 0.36, fc="#f1f6fd")
    ax.text(0.025, 0.385, "RECALL version", fontsize=9.5, fontweight="bold", color=J, va="top")
    ax.text(0.025, 0.315, "The passage never says where\nAdidas is from: the model must\nrecall ‘Germany’ from memory.",
            fontsize=9, va="top")  # fmt: skip
    ax.text(0.54, 0.385, "LOOKUP version", fontsize=9.5, fontweight="bold", color="#5a8fd0", va="top")
    ax.text(0.54, 0.315, "Same question, but the passage\nalso says “Adidas was founded\nin Germany”: it can read it off.",
            fontsize=9, va="top")  # fmt: skip
    ax.text(0.0, -0.04, "8 relations (countries, cities, people, companies, landmarks, dishes, animals, languages), 171 bridges;\n"
                        "the bridge is read from the passage, tracked through a story, or recalled from a description.",
            fontsize=8.3, color=MUTED, va="top")  # fmt: skip


def panel_b(ax):
    runs = [("Qwen 27B", "jsuite_v2_test_chat_ko_cand2_v1", "jsuite_v2_test_chat"),
            ("Qwen 9B", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", "jsuite_v2_test_chat"),
            ("Qwen 9B base", "qwen35_9bb_jsuite_v2_test_qa_ko_cand2_v1", "jsuite_v2_test_qa"),
            ("Qwen 122B", "qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1", "jsuite_v2_test_chat"),
            ("Muse 30B", "muse30_jsuite_v2_test_chat_ko_cand2_v1", "jsuite_v2_test_chat"),
            ("OLMo-3 32B*", "olmo32_jsuite_v1_facts_test_qa_ko_cand2_v1", "jsuite_v1_facts_test_qa")]  # fmt: skip
    bars = [(("paper10", "M"), "Recall questions, J-lens directions removed", J),
            (("paper10", "K"), "Lookup questions, J-lens directions removed", LOOK),
            (("unembed10", "M"), "Recall, logit-lens directions removed (control)", LOGIT),
            (("paper10_rot", "M"), "Recall, random directions removed (control)", COMP)]  # fmt: skip
    h = 0.19
    for i, (name, run, s) in enumerate(runs):
        L = losses(run, s)
        for j, (key, lab, col) in enumerate(bars):
            v, lo, hi, n = L[key]
            y = i + (j - 1.5) * (h + 0.015)
            ax.barh(y, max(v, 0.4), height=h, color=col, lw=0, zorder=2, label=lab if i == 0 else None)
            ax.plot([lo, hi], [y, y], color=INK2, lw=0.9, zorder=3)
            ax.text(max(hi, v) + 1.2, y, f"{v:.0f}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(runs)), [n for n, _, _ in runs], fontsize=10)
    ax.set_ylim(len(runs) - 0.45, -0.55)
    ax.set_xlim(0, 75)
    ax.set_xlabel("% of questions the model got right that it gets wrong after the removal")
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="lower right", frameon=False, fontsize=8.3, handlelength=1.2, borderaxespad=0.2)
    ax.set_title("B   Removing 10 J-lens directions breaks recall, not lookup", loc="left", fontsize=12.5, fontweight="bold", pad=24)
    ax.text(0, -0.75, "At each of the model's own layers in a fixed band, the 10 directions the J-lens reads most are projected out.",
            fontsize=9, color=INK2, va="bottom")  # fmt: skip


def panel_c(ax_r, ax_m):
    modes = [("", "every\ntoken"), ("posbridge", "bridge word\nonly (~2 tok.)"), ("posquestion", "question\nonly"), ("posfinal", "answer\nposition only")]
    for ax, start, title in ((ax_r, "P", "Bridge read from the passage"), (ax_m, "M", "Bridge recalled from a description")):
        for k, (m, lab) in enumerate(modes):
            for pre, col, off, mk in (("", J, -0.17, None), ("qwen35_9b_", INK, 0.17, "o")):
                c = load(f"ablate_v2/jsuite_score/{pre}jsuite_v1_facts_test_chat_ko_cand2{'_' + m if m else ''}_v1.json")["cells"]
                d = c[f"{start}/paper10"]["contrasts"]["M-P"]
                v = d["diff"] if not (start == "M" and m == "posbridge") else None
                if v is None:
                    if pre == "":
                        ax.text(k, 3, "not named\nin passage", ha="center", fontsize=7.5, color=MUTED)
                    continue
                if mk is None:
                    ax.bar(k + off, max(v, 0.6), width=0.32, color=col, lw=0, zorder=2, label="27B" if k == 0 else None)
                    ax.plot([k + off] * 2, d["ci"], color=INK2, lw=0.9, zorder=3)
                else:
                    ax.bar(k + off, max(v, 0.6), width=0.32, color=SURF, ec=J, lw=1.3, zorder=2, label="9B" if k == 0 else None)
                    ax.plot([k + off] * 2, d["ci"], color=INK2, lw=0.9, zorder=3)
        ax.set_xticks(range(len(modes)), [lab for _, lab in modes], fontsize=8)
        ax.set_ylim(-12, 72)
        ax.axhline(0, color=AXIS, lw=1)
        ax.set_title(title, loc="left", fontsize=10.5, fontweight="bold")
        for s_ in ("top", "right", "left"):
            ax.spines[s_].set_visible(False)
        ax.tick_params(length=0)
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
    ax_r.set_ylabel("extra % wrong on recall vs\na made-up fact read from the passage", fontsize=8.5)
    ax_m.set_yticklabels([])
    ax_r.legend(loc="upper right", frameon=False, fontsize=8.5)


def panel_d(ax):
    rows, cols = [], ["J-lens reads the\nfact at the bridge\n(% top; chance ~11%)", "Swapping in another\nentity's J-part moves\nthe answer (points)",
                      "Removing the J-part\nat the bridge only\n(points lost)", "Removing directions\neverywhere: recall extra\nlost, J-lens / logit-lens"]  # fmt: skip
    for name, kor, swr, ror, nl, band in MODELS:
        s = load(f"bridge_readout/{ror}/summary.json")
        b = (14, 20) if name.startswith("Muse") else band  # Muse: the readout at its swap band (the mention's band)
        las = [la for la in range(b[0], b[1] + 1) if f"L{la}/jlens/PM" in s]
        rd = sum(s[f"L{la}/jlens/PM"]["top_among_candidates"] for la in las) / len(las)
        rws = [json.loads(x) for x in (RES / "jswap" / swr / "rows.jsonl").read_text().splitlines()]
        sw = score([{**r, "family": "MEM"} for r in rws if r["family"] in ("PM", "TM")])["MEM/swap"]["transfer"]
        rm = remove_loss(swr, ("PM", "TM"))[0]
        c = load(f"ablate_v2/jsuite_score/{kor}.json")["cells"]
        kj, ku = c["all/paper10"]["contrasts"]["M-P"]["diff"], c["all/unembed10"]["contrasts"]["M-P"]["diff"]
        rows.append((name, [rd, sw, rm, kj - ku], f"{kj:+.0f} / {ku:+.0f}"))  # colour: the J-specific part
    import matplotlib.colors as mc

    cmap = mc.LinearSegmentedColormap.from_list("b", ["#f3f2ee", "#cde2fb", "#6da7ec", "#1c5cab"])
    ax.set_xlim(0, len(cols))
    ax.set_ylim(len(rows), -1.15)
    ax.axis("off")
    for j, lab in enumerate(cols):
        ax.text(j + 0.5, -0.12, lab, ha="center", va="bottom", fontsize=8.3, color=INK2)
    for i, (name, vals, kotxt) in enumerate(rows):
        ax.text(-0.06, i + 0.5, name, ha="right", va="center", fontsize=10)
        for j, v in enumerate(vals):
            sc = max(0.0, min(1.0, v / (100 if j == 0 else 75)))
            ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, color=cmap(sc), lw=0))
            txt = f"{v:.0f}%" if j == 0 else (kotxt if j == 3 else f"{v:+.0f}" if j == 1 else f"{v:.0f}")
            ax.text(j + 0.5, i + 0.5, txt, ha="center", va="center", fontsize=10, color="white" if sc > 0.55 else INK, fontweight="bold")
    ax.set_title("D   Same representation everywhere; only the Qwens clearly depend on it", loc="left", fontsize=12.5, fontweight="bold", pad=8, x=-0.25)
    ax.text(-0.95, len(rows) + 0.25, "Earlier facts set (3 relations); the current set gives the same pattern where run (27B, 9B, OLMo). Last column shaded by\n"
            "its J-specific part (J-lens minus logit-lens). Muse: bridge columns at L14-20, where its J-lens reads the fact; removal everywhere at L36-42.",
            fontsize=7.8, color=MUTED, va="top")  # fmt: skip


def main():
    fig = plt.figure(figsize=(16, 12.2))
    fig.text(0.02, 0.975, "When a language model recalls a fact, it runs through a handful of 'J-lens' directions; when it reads the fact, it doesn't",
             fontsize=15.5, fontweight="bold", va="top")  # fmt: skip
    fig.text(0.02, 0.945, "The J-lens (Anthropic's 'global workspace' paper) reads which concepts a model is internally representing at each token. "
                          "We remove its top 10 directions and ask which questions break.\nQwen 3.5/3.6 models (9B, 27B, 122B), Muse 30B and OLMo-3 32B; "
                          "one fixed layer band per model; every comparison has a random-direction and a logit-lens control.",
             fontsize=10, color=INK2, va="top")  # fmt: skip
    ax_a = fig.add_axes([0.03, 0.53, 0.36, 0.33])
    ax_b = fig.add_axes([0.52, 0.53, 0.45, 0.33])
    ax_cr = fig.add_axes([0.06, 0.135, 0.19, 0.25])
    ax_cm = fig.add_axes([0.265, 0.135, 0.19, 0.25])
    ax_d = fig.add_axes([0.62, 0.135, 0.36, 0.3])
    panel_a(ax_a)
    panel_b(ax_b)
    panel_c(ax_cr, ax_cm)
    fig.text(0.03, 0.455, "C   Where the removal has to act (27B and 9B)", fontsize=12.5, fontweight="bold", va="top")
    fig.text(0.03, 0.43, "Applying it only to one part of the prompt: the dependence sits on the bridge's own word when the bridge was read,\n"
                         "and in the question when it had to be recalled. The answer position carries none of it.", fontsize=9, color=INK2, va="top")  # fmt: skip
    panel_d(ax_d)
    fig.text(0.02, 0.07, "What holds", fontsize=10.5, fontweight="bold", va="top")
    fig.text(0.02, 0.05, "Both halves of the facts (disjoint bridges) agree; all 8 relations; chat, prefill and raw text; base vs instruct (the 9B base keeps ~4/5 of it); "
                         "new passages; the 27B headline reproduces exactly from a clean checkout\n(earlier set; the current set's rerun is "
                         "running); wrong answer words in the passage explain only a small part (5-12 of 46-62 points).", fontsize=8.6, color=INK2, va="top")  # fmt: skip
    fig.text(0.02, 0.022, "Caveats: in the 122B (logit-lens control +12) and Muse (+35) part of the effect is shared with plain logit-lens directions; the 122B's dependence sits in the question "
                          "rather than at the bridge word (being checked: its band is deeper);\nOLMo shows no dependence (*its row in B is the earlier facts set); one rendering seed on the "
                          "current set; bands fixed per model; Gemma-4 and gpt-oss could not be tested (any removal breaks them). Intervals: 95% bootstrap over bridges.",
             fontsize=8.3, color=MUTED, va="top")  # fmt: skip
    (ROOT / "figures" / "archive" / "day6").mkdir(parents=True, exist_ok=True)
    fig.savefig(ROOT / "figures" / "archive" / "day6" / "story.png", dpi=150)
    print("ok")


if __name__ == "__main__":
    main()
