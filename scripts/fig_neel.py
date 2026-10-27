"""fig_neel (Zach, 2026-10-26): the breadth half of bridge-jspace as one figure set for Neel, read from result files only
(through scripts/results_digest.py's readers where they exist). Writes /workspace/scratch/neel_figures/F01..F12 and all.pdf.

  F01 dataset        the question, the test (jsuite_v2), one scene across its finals and starts, counts, eligibility
  F02 readable       what the J++ lens and the logit lens read at the bridge mention, by depth (6 models)
  F03 needed         the headline knock-out across models, its controls, and the per-final losses
  F04 settings       the 27B's and 9B's split across every dataset we built (toy, natural, natplus, jsuite v1, v2)
  F05 robust         within v2: relations, starts, the never-named bridge, replications
  F06 where          depth profiles and position splits: mention at mid depth, question late
  F07 carries        J-part swaps across models; the answer-only swap
  F08 pointer        what the J-part carries: context-free entity pointer, not the probe's subspace
  F09 lookup         the answer-position timeline
  F10 dose           effect against removal size, K 1-300 (amendment 54)
  F11 beyond         three hops, numbers, computed bridges
  F12 scorecard      every model x every test: holds / weak / fails / untestable / not run

python scripts/fig_neel.py [F01 F02 ...]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from scripts import results_digest as D  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
OUT = Path("/workspace/scratch/neel_figures")  # Zach (2026-10-26): kept out of the repo, in scratch
# categorical slots in fixed order (validated on the light surface; light hues always carry a label and a shape)
J, LOGIT, ROT, SIZE, COMP, PROBE = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#008300", "#6250d6"
PASTE = "#898781"
INK, INK2, MUTED, GRID, AXIS, SURF, PANEL = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb", "#f3f2ee"
JL = "#9ec5f4"  # a lighter step of J's hue for secondary J conditions
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.edgecolor": AXIS, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.titlelocation": "left"})  # fmt: skip

SHORT = {"Qwen3.6-27B": "Qwen 27B", "Qwen3.5-9B": "Qwen 9B", "Nemotron-3.5-Lightning": "Nemotron Lightning",
         "Nemotron-3.5-Bolt": "Nemotron Bolt", "DeepSeek-V4-Flash": "DeepSeek V4 Flash", "Ministral-3-14B": "Ministral 14B",
         "OLMo-3-32B (base, Q&A)": "OLMo-3 32B base", "Muse-Glimmer-30B": "Muse 30B", "Qwen3.5-122B": "Qwen 122B"}  # fmt: skip
MOD = {m[0]: m for m in D.MODELS}
HEAD = ["Qwen3.6-27B", "Qwen3.5-9B", "Nemotron-3.5-Lightning"]
PREFIX = {"Qwen3.6-27B": "", "Qwen3.5-9B": "qwen35_9b_", "Nemotron-3.5-Lightning": "nem35l_", "Ministral-3-14B": "min14_",
          "DeepSeek-V4-Flash": "dsv4f_", "Nemotron-3.5-Bolt": "nem35b_", "Muse-Glimmer-30B": "muse30_", "Qwen3.5-122B": "qwen35_122b_"}  # fmt: skip
NLAYERS = {"Qwen3.6-27B": 64, "Qwen3.5-9B": 32, "Nemotron-3.5-Lightning": 52, "Ministral-3-14B": 40, "Nemotron-3.5-Bolt": 88}
SET = "jsuite_v2_test_chat"


def load(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def score(run: str) -> dict:
    return load(RES / "ablate_v2" / "jsuite2_score" / f"{run}.json") or {}


def cell(run: str, key: str, contrast: str = "M-K"):
    c = score(run).get("facts", {}).get(key)
    return (c["contrasts"][contrast]["diff"], c["contrasts"][contrast]["ci"]) if c and contrast in c["contrasts"] else None


def style(ax, grid="x"):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    if grid:
        ax.grid(axis=grid, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def header(fig, title: str, sub: str = "") -> float:
    """Title and subtitle at fixed distances (inches) from the top; returns the figure fraction below them."""
    H = fig.get_figheight()
    fig.text(0.01, 1 - 0.16 / H, title, fontsize=12.5, fontweight="bold", va="top", ha="left")
    if sub:
        fig.text(0.01, 1 - 0.47 / H, sub, fontsize=9, color=INK2, va="top", ha="left")
    return 1 - (0.8 if sub else 0.55) / H


def note(fig, text: str) -> float:
    """The footnote, wrapped to the figure's width, at the bottom; returns the figure fraction above it."""
    import textwrap

    W, H = fig.get_figwidth(), fig.get_figheight()
    lines = [ln for para in text.split("\n") for ln in textwrap.wrap(para, int(W * 17.5))]
    fig.text(0.01, 0.06 / H, "\n".join(lines), fontsize=7.5, color=MUTED, va="bottom", ha="left", linespacing=1.35)
    return (0.12 + 0.145 * len(lines)) / H


def dot(ax, x, y, ci, col, mk="o", ms=7, label=None, lab_off=1.2, fmt="{:+.0f}", text=True):
    if ci:
        ax.plot(ci, [y, y], color=col, lw=2, solid_capstyle="round", zorder=2)
    ax.plot(x, y, mk, color=col, ms=ms, mec=SURF, mew=1.5, zorder=3, label=label)
    if text:
        ax.text((ci[1] if ci else x) + lab_off, y, fmt.format(x), va="center", fontsize=7.5, color=INK2)


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.png", dpi=170)
    plt.close(fig)
    print(name, "ok", flush=True)


# ---------------------------------------------------------------------------------------------------------------- F01


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if s.strip()]


def f01() -> None:
    items = {}
    for line in (DATA / "jsuite_v2_test_chat" / "items.jsonl").read_text().splitlines():
        d = json.loads(line)
        items[d["id"]] = d
    r_items = {json.loads(x)["id"]: json.loads(x) for x in (DATA / "jsuite_v2_1_test_chat" / "items.jsonl").read_text().splitlines()}
    ex = {w: items[f"j2:chat:facts:{w}-L0-00635"] for w in ("MK", "MM", "MA", "MN", "MP")}
    ex["RM"] = r_items["j2:chat:facts:RM-L0-00635"]
    sets = {w: sentences(d["context"]) for w, d in ex.items()}
    shared = set.intersection(*(set(v) for w, v in sets.items() if w != "RM"))
    facts = [d for d in items.values() if d["module"] == "facts"]

    fig = plt.figure(figsize=(15, 10.8))
    header(fig, "The test: the same two-hop question, with the bridge's attribute either stated in the passage or left to memory",
           "jsuite_v2 (our dataset, built for this sprint): 8 relations, 179 bridge facts on test, 15 'words' = how the bridge is reached x where the answer comes from")  # fmt: skip
    import textwrap

    # A: one scene across its finals
    ax = fig.add_axes((0.01, 0.40, 0.60, 0.51))
    ax.axis("off")
    ax.set_title("A   One test scene, five finals (Mozart; people -> nationality; start M)", fontsize=10.5)
    ax.add_patch(FancyBboxPatch((0.0, 0.0), 1, 0.96, boxstyle="round,pad=0.005,rounding_size=0.01", fc=PANEL, ec="none", transform=ax.transAxes))
    names = [e if isinstance(e, str) else e.get("name", "") for e in ex["MM"].get("entities", [])]
    frame = [s for s in sets["MN"] if s in shared and any(nm and nm in s for nm in names)]
    other = sum(1 for s in sets["MN"] if s in shared) - len(frame)
    y = 0.93
    ax.text(0.02, y, f"Shared passage frame (every final), plus a header, a sign-off and WikiText filler ({other} sentences):", fontsize=8.5, color=MUTED, transform=ax.transAxes, va="top")
    y -= 0.045
    ax.text(0.03, y, " ".join(frame), fontsize=8, color=INK2, transform=ax.transAxes, va="top", style="italic")
    y -= 0.045
    y -= 0.015
    q = ex["MM"]["question"]
    rows = [("K", "MK", "the fact is stated", J), ("M", "MM", "recall: answer nowhere in the passage", J), ("A", "MA", "answer word present once, on another entity", J),
            ("N", "MN", "no relation sentences at all (no lures)", J), ("P", "MP", "a new made-up fact is stated (different question)", J)]  # fmt: skip
    ax.text(0.02, y, "Final-hop sentences (the only thing that changes):", fontsize=8.5, color=MUTED, transform=ax.transAxes, va="top")
    y -= 0.055
    for code, w, gloss, _c in rows:
        diff = [s for s in sets[w] if s not in shared]
        ax.text(0.02, y, f"{code}", fontsize=11, fontweight="bold", color=INK, transform=ax.transAxes, va="top")
        ax.text(0.055, y, gloss, fontsize=8, color=MUTED, transform=ax.transAxes, va="top")
        ax.text(0.52, y, f"answer: {ex[w]['answer']}", fontsize=8.5, color=INK, transform=ax.transAxes, va="top", fontweight="bold")
        y -= 0.036
        wrapped = textwrap.wrap(" ".join(diff), 128)
        ax.text(0.055, y, "\n".join(wrapped), fontsize=8, color=INK2, transform=ax.transAxes, va="top", style="italic", linespacing=1.3)
        y -= 0.033 * len(wrapped) + 0.022
    ax.text(0.02, y, f"Question (K, M, A, N): “{q}”", fontsize=8.5, color=INK, transform=ax.transAxes, va="top")
    y -= 0.045
    ax.text(0.02, y, f"Question (P): “{ex['MP']['question']}”", fontsize=8.5, color=INK, transform=ax.transAxes, va="top")
    y -= 0.05
    ax.text(0.02, y, "Primary contrast M − K: the same question and answer, recalled vs stated.", fontsize=9, color=J, fontweight="bold", transform=ax.transAxes, va="top")

    # B: the starts
    ax = fig.add_axes((0.63, 0.40, 0.36, 0.50))
    ax.axis("off")
    ax.set_title("B   Four starts: how hop 1 reaches the bridge", fontsize=10.5)
    ax.add_patch(FancyBboxPatch((0.0, 0.0), 1, 0.96, boxstyle="round,pad=0.005,rounding_size=0.01", fc=PANEL, ec="none", transform=ax.transAxes))
    starts = [("P  read", "the passage ties a made-up person to each entity;\nthe question names the bridge only through them",
               "“Last spring, Felix Ward relocated to Kyoto.” ->\n“...the city Felix Ward relocated to last spring...”", "bridge named 2x"),
              ("M  recalled", "the question describes the bridge by a real fact;\nthe passage names it once, in passing",
               "“the composer who wrote The Magic Flute” (Mozart)", "bridge named 1x"),
              ("T  tracked", "two objects move through three places each,\ninterleaved; the bridge is where one went last",
               "“Then the jazz tour stopped in Kyoto...”", "bridge named 2x"),
              ("R  never named", "an M item with its one sentence naming\nthe bridge deleted (dataset v2.1)", "Mozart never appears", "bridge named 0x")]  # fmt: skip
    y = 0.9
    for name, gloss, eg, ment in starts:
        ax.text(0.03, y, name, fontsize=10.5, fontweight="bold", transform=ax.transAxes, va="top")
        ax.text(0.97, y, ment, fontsize=8, color=MUTED, transform=ax.transAxes, va="top", ha="right")
        ax.text(0.03, y - 0.05, gloss, fontsize=8, color=INK2, transform=ax.transAxes, va="top")
        ax.text(0.03, y - 0.135, eg, fontsize=8, color=INK2, transform=ax.transAxes, va="top", style="italic")
        y -= 0.225

    # C: relations
    ax = fig.add_axes((0.13, 0.1, 0.2, 0.23))
    style(ax)
    rels = ["countries", "languages", "people", "cities", "companies", "landmarks", "dishes", "animals"]
    gl = {"countries": "country -> continent", "languages": "country -> language", "people": "person -> nationality", "cities": "city -> country",
          "companies": "company -> country", "landmarks": "landmark -> country", "dishes": "dish -> country", "animals": "animal -> class"}  # fmt: skip
    n_items = [sum(1 for d in facts if d["relation"] == r) for r in rels]
    n_pairs = [len({d["bridge"] for d in facts if d["relation"] == r}) for r in rels]
    n_ans = [len({d["real"] for d in facts if d["relation"] == r and d.get("real")}) for r in rels]
    ax.barh(range(8), n_items, color=J, height=0.6)
    for i, (a, b, c) in enumerate(zip(n_items, n_pairs, n_ans, strict=True)):
        ax.text(a + 15, i, f"{a} items, {b} bridges, {c} answers", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(8), [gl[r] for r in rels])
    ax.set_ylim(7.6, -0.6)
    ax.set_xlim(0, max(n_items) * 2.3)
    ax.set_xlabel("test items (15 words x 2 passage lengths)")
    ax.set_title("C   Eight relations (test split)", fontsize=10, y=1.13)

    # D: eligibility per model
    ax = fig.add_axes((0.46, 0.1, 0.24, 0.23))
    style(ax)
    from scripts import tasks_v2 as T

    elig = []
    words = ["PP", "PK", "PM", "PA", "PN", "MP", "MK", "MM", "MA", "MN", "TP", "TK", "TM", "TA", "TN"]
    for lab, pre in (("Qwen 27B", ""), ("Qwen 122B", "qwen35_122b_"), ("Nemotron Bolt", "nem35b_"), ("Ministral 14B", "min14_"),
                     ("Nemotron Lightning", "nem35l_"), ("Qwen 9B", "qwen35_9b_"), ("Muse 30B", "muse30_"), ("DeepSeek V4 Flash", "dsv4f_")):  # fmt: skip
        comp = f"{pre}{SET}_competence_cand2_v1"
        if not (RES / "tasks_v2" / comp / "items.jsonl").exists():
            continue
        ids = {it["id"] for it in T.eligible(SET, comp, words, 1000, "all")}  # the call ablate_v2 makes (--tasks-level all, --n 1000)
        by = {s: sum(1 for i in ids if items.get(i, {}).get("start") == s) for s in "PMT"}
        elig.append((lab, by))
    left = [0] * len(elig)
    for s, col in (("P", J), ("M", JL), ("T", PASTE)):
        vals = [b[s] for _, b in elig]
        ax.barh(range(len(elig)), vals, left=left, color=col, height=0.6, label=f"start {s}", edgecolor=SURF, lw=1)
        left = [a + b for a, b in zip(left, vals, strict=True)]
    for i, t in enumerate(left):
        ax.text(t + 40, i, f"{t:,}", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(elig)), [lab for lab, _ in elig])
    ax.set_ylim(len(elig) - 0.4, -0.6)
    ax.set_xlim(0, 5370 * 1.08)
    ax.axvline(len(facts), color=AXIS, lw=1, ls=":")
    ax.text(len(facts) - 40, -0.75, f"all {len(facts):,}", fontsize=7, color=MUTED, ha="right")
    ax.set_xlabel("eligible test items: every part right unedited")
    ax.legend(loc="upper left", frameon=False, fontsize=7.5, ncol=3, bbox_to_anchor=(0.0, 1.13))
    ax.set_title("D   What each model can do (eligibility)", fontsize=10, y=1.13)

    # E: the intervention
    ax = fig.add_axes((0.75, 0.07, 0.24, 0.28))
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.0, 0.0), 1, 0.92, boxstyle="round,pad=0.005,rounding_size=0.01", fc=PANEL, ec="none", transform=ax.transAxes))
    ax.set_title("E   The intervention and its controls", fontsize=10)
    txt = [("Knock-out (J++ top 10):", "at every token, at each layer of one\nmid-depth band, project out the 10 directions\nthe J++ lens reads most there", J),
           ("Rotated:", "the same removal, turned in a random\ndirection (same norm)", ROT),
           ("Logit lens:", "the 10 unembedding directions read most", LOGIT),
           ("Size-matched:", "the same norm along the residual's\ntop principal directions", "#b07800"),
           ("Score:", "points lost on items right unedited;\nM − K, 95% bootstrap over bridges", INK)]  # fmt: skip
    y = 0.85
    for a, b, c in txt:
        ax.text(0.04, y, a, fontsize=8.5, fontweight="bold", color=c, transform=ax.transAxes, va="top")
        ax.text(0.04, y - 0.055, b, fontsize=7.8, color=INK2, transform=ax.transAxes, va="top")
        y -= 0.06 + 0.055 * (b.count("\n") + 1)
    note(fig, f"Test split: {len(facts):,} facts items = 179 (relation, bridge) pairs x 15 words x 2 passage lengths (3 or 6 entities, 53-299 words), 4 genres; dev split: 171 disjoint pairs, "
              "used only to choose bands. Three renderings (seeds 2601-2603) redraw passages, distractors and wording over the same facts. "
              "Chat format, thinking off; the answer is read as the top candidate among the relation's answers.")  # fmt: skip
    save(fig, "F01_dataset")


# ---------------------------------------------------------------------------------------------------------------- F02

READOUT = [("Qwen3.6-27B", "bridge_readout_v2_v1"), ("Qwen3.5-9B", "qwen35_9b_bridge_readout_v2_v1"),
           ("Nemotron-3.5-Lightning", "nem35l_bridge_readout_v2_v1"), ("Ministral-3-14B", "min14_bridge_readout_v2_v1"),
           ("DeepSeek-V4-Flash", "dsv4f_bridge_readout_v2_v1"), ("Nemotron-3.5-Bolt", "nem35b_bridge_readout_v2_v1")]  # fmt: skip


def nlayers(m: str) -> int:
    if m in NLAYERS:
        return NLAYERS[m]
    s = load(RES / "ablate_v2" / "profile" / "dsv4f_jsuite_v2_dev_chat_profile_cand2_v1.json")
    return s["n_layers"]


def f02() -> None:
    fig, axes = plt.subplots(1, 6, figsize=(16, 4.8), sharey=True)
    for ax, (m, run) in zip(axes, READOUT, strict=True):
        s = load(RES / "bridge_readout" / run / "summary.json")
        n = nlayers(m)
        lays = sorted({int(k.split("/")[0][1:]) for k in s})
        lo, hi = map(int, MOD[m][2][1:].split("-"))
        style(ax, "y")
        ax.axvspan(lo / n, (hi + 1) / n, color=GRID, alpha=0.8, lw=0)
        for kind, col, lab in (("jlens", J, "J++ lens"), ("logit", LOGIT, "logit lens")):
            ys = [s[f"L{la}/{kind}/PM"]["top_among_candidates"] for la in lays]
            ax.plot([la / n for la in lays], ys, color=col, lw=2, label=lab)
        ch = s[f"L{lays[0]}/jlens/PM"]["chance"]
        ax.axhline(ch, color=AXIS, lw=1, ls=":")
        ax.set_title(SHORT[m], fontsize=10)
        ax.set_xlabel("relative depth")
        ax.set_xlim(0, 1)
        ax.text(0.98, 3, f"n {s[f'L{lays[0]}/jlens/PM']['n']}", ha="right", fontsize=7, color=MUTED)
    axes[0].set_ylabel("true attribute ranked first\namong the relation's answers, %")
    axes[1].legend(loc="lower right", frameon=False, fontsize=8)
    axes[0].text(0.98, ch + 2, "chance", fontsize=7, color=MUTED, ha="right")
    top = header(fig, "Readable: at the bridge's mention the J++ lens reads the attribute the model will need, in every model; the logit lens lags in the Qwens and Ministral",
                 "Start P, final M (the passage never states the attribute): what each lens ranks first at the last token of the bridge's mention, every 2nd layer")  # fmt: skip
    bot = note(fig, "jsuite_v2 test, eligible items; shaded: the knock-out band. Readability is not use: the next figures test whether the model needs these directions (F03) and whether they carry the answer (F07-F08). "
                    "Ministral reads the attribute at mid depth (~90%) but neither needs nor carries it there (F06, F07).")  # fmt: skip
    fig.tight_layout(rect=(0, bot, 1, top))
    save(fig, "F02_readable")


# ---------------------------------------------------------------------------------------------------------------- F03


def f03() -> None:
    order = ["Qwen3.6-27B", "Qwen3.5-9B", "Nemotron-3.5-Lightning", "DeepSeek-V4-Flash", "Ministral-3-14B",
             "Nemotron-3.5-Bolt", "OLMo-3-32B (base, Q&A)", "Muse-Glimmer-30B", "Qwen3.5-122B"]  # fmt: skip
    fig = plt.figure(figsize=(16, 8.2))
    ax = fig.add_axes((0.15, 0.14, 0.5, 0.66))
    style(ax)
    series = [("j", "J++ lens, top 10", J, "o"), ("u", "logit lens, top 10", LOGIT, "s"), ("rot", "J++ rotated (same norm)", ROT, "D"),
              ("pc", "same norm, top principal directions", SIZE, "^")]  # fmt: skip
    offs = [-0.27, -0.09, 0.09, 0.27]
    labels = []
    for r, m in enumerate(order):
        lab, ko, band, *_r = MOD[m]
        pc = _r[4]
        vals = {"j": D.mk(ko), "u": D.mk(ko, "unembed10"), "rot": D.mk(ko, "paper10_rot"), "pc": D.mk(pc, "paper10_pcasize") if pc else None}
        for (key, _l, col, mk_), off in zip(series, offs, strict=True):
            v = vals[key]
            if v:
                dot(ax, v["d"], r + off, v["ci"], col, mk_, ms=6.5)
        labels.append(f"{SHORT[m]}  {band}")
    for yy in (2.5, 5.5):
        ax.axhline(yy, color=GRID, lw=1.2)
    ax.text(74, 0.0, "J-specific,\nstrong", fontsize=8, color=MUTED, ha="right", va="top")
    ax.text(74, 3.0, "weak / spread\n(F10)", fontsize=8, color=MUTED, ha="right", va="top")
    ax.text(74, 6.0, "not needed /\nnot J-specific /\nnot robust", fontsize=8, color=MUTED, ha="right", va="top")
    ax.set_yticks(range(len(order)), labels)
    ax.set_ylim(len(order) - 0.5, -0.6)
    ax.set_xlim(-8, 75)
    ax.axvline(0, color=AXIS, lw=1)
    ax.set_xlabel("recall answers lost minus stated-fact answers lost (M − K), points")
    ax.legend(handles=[plt.Line2D([], [], ls="", marker=mk_, color=c, ms=7, label=lab) for _k, lab, c, mk_ in series],
              loc="upper left", bbox_to_anchor=(0.0, 1.1), ncol=4, frameon=False, fontsize=8)  # fmt: skip
    ax.set_title("A   M − K under the top-10 removal at each model's band", y=1.1)
    # B: losses per final for the three strong models
    bx = fig.add_axes((0.72, 0.14, 0.27, 0.66))
    style(bx, "x")
    finals = [("K", "fact stated"), ("P", "new made-up fact stated"), ("A", "answer word present\n(on another entity)"),
              ("N", "nothing stated, no lures"), ("M", "recall (lures present)")]  # fmt: skip
    cols = {"Qwen3.6-27B": J, "Qwen3.5-9B": JL, "Nemotron-3.5-Lightning": "#184f95"}
    for i, m in enumerate(HEAD):
        c = score(MOD[m][1])["facts"]["paper10/start=all"]["loss"]
        for r, (f, _g) in enumerate(finals):
            bx.barh(r + (i - 1) * 0.26, c[f], height=0.24, color=cols[m], label=SHORT[m] if r == 0 else None)
            bx.text(c[f] + 0.8, r + (i - 1) * 0.26, f"{c[f]:.0f}", va="center", fontsize=7, color=INK2)
    bx.set_yticks(range(len(finals)), [f"{f}: {g}" for f, g in finals])
    bx.set_ylim(len(finals) - 0.5, -0.6)
    bx.set_xlim(0, 70)
    bx.set_xlabel("points lost under the J++ top-10 removal")
    bx.legend(loc="upper left", bbox_to_anchor=(0.0, 1.1), ncol=3, frameon=False, fontsize=8)
    bx.set_title("B   What is lost depends on where the answer is", y=1.1)
    header(fig, "Needed: removing 10 J++ directions at one band breaks recalled facts and leaves stated facts, J-specifically, in three models from two families",
           "Test set, all 8 relations, all starts. Each model's band was fixed on dev before the test run (F06).")  # fmt: skip
    note(fig, "95% bootstrap over bridges (seed 0). Size-matched control: same norm along the residual's top-256 principal directions (not run for the last four). "
              "Qwen 122B: by answer probability its M − K is +2 (greedy +48): not robust. OLMo: base model, Q&A format; its J-part swap still carries (F07).\n"
              "Muse: the logit lens's own top 10 removes much of it. Gemma 4 31B, gpt-oss-20b and Kolibri are untestable: any top-10 lens removal wrecks plain text (F12). "
              "B: a stated answer protects; one mention of the answer word on another entity halves the loss; lures add little (M vs N).")  # fmt: skip
    save(fig, "F03_needed")


# ---------------------------------------------------------------------------------------------------------------- F05


def f05() -> None:
    fig = plt.figure(figsize=(16, 8.4))
    cols = {"Qwen3.6-27B": J, "Qwen3.5-9B": JL, "Nemotron-3.5-Lightning": "#184f95"}
    mks = {"Qwen3.6-27B": "o", "Qwen3.5-9B": "s", "Nemotron-3.5-Lightning": "D"}
    offs = {"Qwen3.6-27B": -0.22, "Qwen3.5-9B": 0.0, "Nemotron-3.5-Lightning": 0.22}
    # A: relations
    ax = fig.add_axes((0.11, 0.12, 0.27, 0.7))
    style(ax)
    rels = ["countries", "languages", "people", "cities", "companies", "landmarks", "dishes", "animals"]
    for m in HEAD:
        for r, rel in enumerate(rels):
            v = cell(MOD[m][1], f"paper10/relation={rel}")
            rv = cell(MOD[m][1], f"paper10_rot/relation={rel}")
            if v:
                dot(ax, v[0], r + offs[m], v[1], cols[m], mks[m], ms=6, text=False)
            if rv:
                ax.plot(rv[0], r + offs[m], "|", color=ROT, ms=7, mew=1.5)
    ax.set_yticks(range(8), rels)
    ax.set_ylim(7.6, -0.6)
    ax.set_xlim(-10, 100)
    ax.axvline(0, color=AXIS, lw=1)
    ax.set_xlabel("M − K, points (tick: rotated control)")
    ax.set_title("A   Every relation")
    ax.legend(handles=[plt.Line2D([], [], ls="", marker=mks[m], color=cols[m], ms=7, label=SHORT[m]) for m in HEAD],
              loc="upper left", bbox_to_anchor=(0, 1.13), ncol=3, frameon=False, fontsize=8)  # fmt: skip
    # B: starts, and the never-named bridge
    bx = fig.add_axes((0.47, 0.12, 0.2, 0.7))
    style(bx)
    rows = [("start P (read)", "start=P", "M-K"), ("start T (tracked)", "start=T", "M-K"), ("start M (recalled)", "start=M", "M-K")]
    for m in HEAD:
        for r, (_l, key, con) in enumerate(rows):
            v = cell(MOD[m][1], f"paper10/{key}", con)
            if v:
                dot(bx, v[0], r + offs[m], v[1], cols[m], mks[m], ms=6, text=False)
        rr = f"{PREFIX[m]}{SET}_ko_cand2_v1+{PREFIX[m]}jsuite_v2_1_test_chat_R_ko_cand2_v1"
        v = cell(rr, "paper10/never_named", "RM-MM")
        if v:
            dot(bx, v[0], 3 + offs[m], v[1], cols[m], mks[m], ms=6, text=False)
        else:
            bx.text(1, 3 + offs[m], f"{SHORT[m]}: not run", fontsize=7, color=MUTED, va="center")
    bx.set_yticks(range(4), [r[0] for r in rows] + ["never named (R):\nRM − MM, extra loss"])
    bx.set_ylim(3.6, -0.6)
    bx.set_xlim(-10, 80)
    bx.axvline(0, color=AXIS, lw=1)
    bx.set_xlabel("points")
    bx.set_title("B   Every start")
    # C: replications
    cx = fig.add_axes((0.78, 0.12, 0.21, 0.7))
    style(cx)
    reps = []
    for m in HEAD:
        lab, ko, band, _s, *_x = MOD[m]
        renders = MOD[m][-1]
        reps.append((m, "run of record", D.mk(ko)))
        for i, rr in enumerate(renders, 2):
            reps.append((m, f"rendering {i}", D.mk(rr)))
        for h in "AB":
            v = cell(ko, f"paper10/half={h}")
            reps.append((m, f"test half {h}", {"d": v[0], "ci": v[1]} if v else None))
        sv = load(RES / "ablate_v2" / "soft_score" / f"{ko}.json")
        c = (sv or {}).get("paper10")
        reps.append((m, "by probability", {"d": c["soft_M-K"], "ci": c["soft_ci"]} if c else None))
    labs = ["run of record", "rendering 2", "rendering 3", "test half A", "test half B", "by probability"]
    for m, lab, v in reps:
        if v:
            dot(cx, v["d"], labs.index(lab) + offs[m], v["ci"], cols[m], mks[m], ms=6, text=False)
    cx.set_yticks(range(len(labs)), labs)
    cx.set_ylim(len(labs) - 0.4, -0.6)
    cx.set_xlim(0, 75)
    cx.set_xlabel("M − K, points")
    cx.set_title("C   Replications")
    header(fig, "Robust: the split holds on all 8 relations (weakest: animals), every way of reaching the bridge, both test halves, three renderings, by probability",
           "The three strong models (F03). jsuite_v2 test, J++ top-10 removal at each model's band; 95% bootstrap over bridges.")  # fmt: skip
    note(fig, "C: renderings redraw passages, distractors and wording over the same facts (150 random items per word for the 27B and Lightning); halves A/B are disjoint bridge sets. "
              "The 27B and 9B headlines also reproduce row for row from a clean checkout.\nB: R is the M scene with its one sentence naming the bridge deleted; RM − MM is the extra recall loss when the bridge is never named "
              "(Lightning not run). Animals is the weakest relation in every model (6 answers: mammal, bird, ...).")  # fmt: skip
    save(fig, "F05_robust")


# ---------------------------------------------------------------------------------------------------------------- F06

PROFILES = [("Qwen3.6-27B", "jsuite_v2_dev_chat_profile_rs40_cand2_v1"), ("Qwen3.5-9B", "qwen35_9b_jsuite_v2_dev_chat_profile_rs40_cand2_v1"),
            ("Nemotron-3.5-Lightning", "nem35l_jsuite_v2_dev_chat_profile_rs40_cand2_v1"), ("Ministral-3-14B", "min14_jsuite_v2_dev_chat_profile_rs40_cand2_v1"),
            ("Nemotron-3.5-Bolt", "nem35b_jsuite_v2_dev_chat_profile_cand2_v1")]  # fmt: skip
# position runs: (label, all-token run, band, {mode: run})
POSITIONS = [
    ("Qwen 27B, mid L32-40", "jsuite_v2_test_chat_ko_cand2_v1", {m: f"jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
    ("Qwen 9B, mid L12-16", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", {m: f"qwen35_9b_jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
    ("Lightning, mid L27-33", "nem35l_jsuite_v2_test_chat_ko_cand2_v1", {m: f"nem35l_jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
    ("Qwen 27B, late L52-60", None, {m: f"jsuite_v2_test_chat_ko_cand2_L52-60_pos{m}_v1" for m in ("bridge", "question")}),
    ("Ministral, late L32-37", "min14_jsuite_v2_test_chat_ko_cand2_v1", {m: f"min14_jsuite_v2_test_chat_ko_cand2_L32-37_pos{m}_v1" for m in ("bridge", "question")}),
    ("Qwen 122B, late L39-45", "qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1", {m: f"qwen35_122b_jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
]  # fmt: skip


def f06() -> None:
    fig = plt.figure(figsize=(16, 9.6))
    # A: profiles, J++ / logit / rotated
    w = 0.168
    for i, (m, run) in enumerate(PROFILES):
        ax = fig.add_axes((0.05 + i * (w + 0.022), 0.55, w, 0.3))
        s = load(RES / "ablate_v2" / "profile" / f"{run}.json")
        bands = sorted(s["bands"].values(), key=lambda b: b["depth"][0])
        mid = [100 * (b["depth"][0] + b["depth"][1]) / 2 for b in bands]
        style(ax, "y")
        lo, hi = map(int, MOD[m][2][1:].split("-"))
        n = s["n_layers"]
        ax.axvspan(100 * lo / n, 100 * (hi + 1) / n, color=GRID, alpha=0.8, lw=0)
        for c, col, mk_, lab in (("paper10", J, "o", "J++ top 10"), ("unembed10", LOGIT, "s", "logit lens top 10"), ("paper10_rot", ROT, "D", "J++ rotated")):
            y = [b[c]["M-K"] for b in bands]
            ax.plot(mid, y, "-", color=col, lw=1.8, marker=mk_, ms=4, mec=SURF, mew=0.8, label=lab)
            bad = [j for j, b in enumerate(bands) if b[c]["loss"]["K"] >= 20]
            ax.plot([mid[j] for j in bad], [y[j] for j in bad], mk_, color=col, mfc=SURF, ms=5, mew=1.3, ls="")
        ax.axhline(0, color=AXIS, lw=1)
        ax.set_ylim(-8, 66)
        ax.set_xlim(0, 100)
        ax.set_title(f"{SHORT[m]}", fontsize=9.5)
        ax.set_xlabel("depth, % of layers")
        if i == 0:
            ax.set_ylabel("M − K on dev, points")
            ax.legend(loc="upper left", frameon=False, fontsize=7)
        else:
            ax.set_yticklabels([])
    fig.text(0.05, 0.885, "A   Depth: M − K for a 1/8-wide removal window slid through the model (dev, all relations; shaded: the test band)", fontsize=10.5, fontweight="bold")
    # B: positions, by start at the mid bands; pooled at the late bands
    modes = [("all", "every token", J), ("bridge", "bridge mention only", "#184f95"), ("context", "whole passage only", JL), ("question", "question only", LOGIT)]
    for i, (lab, allrun, runs) in enumerate(POSITIONS[:3]):
        bx = fig.add_axes((0.07 + i * 0.205, 0.11, 0.17, 0.3))
        style(bx)
        for r, st in enumerate("PTM"):
            for k, (mode, _ml, col) in enumerate(modes):
                run = allrun if mode == "all" else runs.get(mode)
                v = cell(run, f"paper10/start={st}") if run else None
                y = r + (k - 1.5) * 0.19
                if v:
                    bx.barh(y, v[0], height=0.17, color=col)
                    bx.text(max(v[0], 0) + 1, y, f"{v[0]:+.0f}", va="center", fontsize=6.5, color=INK2)
        bx.set_yticks(range(3), ["read (P)", "tracked (T)", "recalled (M)"] if i == 0 else ["", "", ""])
        bx.set_ylim(2.5, -0.55)
        bx.set_xlim(-5, 85)
        bx.axvline(0, color=AXIS, lw=1)
        bx.set_title(lab, fontsize=9)
        bx.set_xlabel("M \u2212 K, points")
    bx = fig.add_axes((0.77, 0.11, 0.21, 0.3))
    style(bx)
    lates = POSITIONS[3:]
    for r, (lab, allrun, runs) in enumerate(lates):
        for k, (mode, _ml, col) in enumerate(modes):
            run = allrun if mode == "all" else runs.get(mode)
            v = cell(run, "paper10/start=all") if run else None
            y = r + (k - 1.5) * 0.19
            if v:
                bx.barh(y, v[0], height=0.17, color=col)
                bx.text(max(v[0], 0) + 1, y, f"{v[0]:+.0f}", va="center", fontsize=6.5, color=INK2)
    bx.set_yticks(range(len(lates)), [p_[0].replace(", late ", "\n") for p_ in lates])
    bx.set_ylim(len(lates) - 0.5, -0.55)
    bx.set_xlim(-5, 62)
    bx.axvline(0, color=AXIS, lw=1)
    bx.set_title("late bands (all starts)", fontsize=9)
    bx.set_xlabel("M \u2212 K, points")
    bx.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c, label=ml) for _m, ml, c in modes], loc="lower right", bbox_to_anchor=(1.0, 1.1), ncol=2, frameon=False, fontsize=7.5)
    fig.text(0.05, 0.47, "B   Position: the removal applied only to one part of the prompt (mid bands by how the bridge was reached; late bands pooled)", fontsize=10.5, fontweight="bold")
    header(fig, "Where: a bridge read from the passage needs J-space at its own mention in the Qwens (in Lightning, mention and question); late in depth, at the question",
           "The same removal restricted to a window of layers (A) or to a part of the prompt (B). A recalled bridge (start M) needs it at several places at once: no single region carries it")  # fmt: skip
    note(fig, "A: hollow markers: stated facts (K) also lose >= 20 points there (not a split). Windows overlap; no intervals (n ~80 per final per window). Bolt is flat at K = 10 (its effect needs ~100 directions, F10). "
              "The 9B's all-relation pick would be L16-19; its test band L12-16 came from the first facts set.\nB: jsuite_v2 test, all eligible items; 'bridge mention' = the bridge's own tokens (named twice for P and T starts, once in passing for M); the 27B's late band has no all-token run. "
              "Late, the dependence is in the question in the 27B, Ministral and the 122B; Ministral has no mid-depth dependence to localize (A). Bolt's split (at K = 100) is in F12.")  # fmt: skip
    save(fig, "F06_where")


# ---------------------------------------------------------------------------------------------------------------- F07

SWAPS = [("Qwen 27B (L32-40)", "jswap_v2_v1", "pooled"), ("Qwen 9B (L12-16)", "qwen35_9b_jswap_v2_v1", "pooled"),
         ("Lightning (L27-33)", "nem35l_jswap_v2_v1", "pooled"), ("OLMo-3 32B base (L12-20)", "olmo32_jswap_v2_v1", "pooled"),
         ("Bolt, K 10 (L42-53)", "nem35b_jswap_v2_v1", "pooled"), ("Bolt, K 100 (L42-53)", "nem35b_jswap_v2_k100_v1", "pooled"),
         ("DeepSeek, mid (L22-27)", "dsv4f_jswap_v2_L22-27_v1", "pooled"), ("Ministral, mid, K 10 (L20-25)", "min14_jswap_v2_L20-25_v1", "pooled"),
         ("Ministral, mid, K 100 (L20-25)", "min14_jswap_v2_L20-25_k100_v1", "pooled")]  # fmt: skip


def f07() -> None:
    fig = plt.figure(figsize=(16, 8.6))
    ax = fig.add_axes((0.17, 0.13, 0.47, 0.66))
    style(ax)
    conds = [("swap", "J-part of D's mention swapped in", J, "o"), ("paste", "whole residual of D's mention pasted", PASTE, "v"),
             ("swap_comp", "everything but the J-part swapped", COMP, "P"), ("swap_rot", "J-part, rotated", ROT, "D"), ("swap_u", "logit-lens part", LOGIT, "s")]  # fmt: skip
    offs = [-0.3, -0.15, 0.0, 0.15, 0.3]
    for r, (lab, run, _k) in enumerate(SWAPS):
        p = D.pooled(run) or {}
        for (c, _l, col, mk_), off in zip(conds, offs, strict=True):
            v = p.get(f"memory/{c}")
            if v:
                dot(ax, v["transfer"], r + off, v["ci"], col, mk_, ms=6, text=c in ("swap", "paste", "swap_comp"))
    ax.set_yticks(range(len(SWAPS)), [s[0] for s in SWAPS])
    ax.set_ylim(len(SWAPS) - 0.45, -0.6)
    ax.set_xlim(-6, 100)
    ax.axvline(0, color=AXIS, lw=1)
    for yy in (2.5, 3.5):
        ax.axhline(yy, color=GRID, lw=1.2)
    ax.set_xlabel("answers moved to D's attribute (transfer: % donor − % third entity), memory finals pooled")
    ax.legend(handles=[plt.Line2D([], [], ls="", marker=mk_, color=c, ms=7, label=lab) for _c, lab, c, mk_ in conds],
              loc="upper left", bbox_to_anchor=(0, 1.13), ncol=3, frameon=False, fontsize=8)  # fmt: skip
    ax.set_title("A   Swap the bridge mention's J-part with another entity's (D): does the answer follow D?", y=1.13)
    # B: answer-only swaps
    bx = fig.add_axes((0.75, 0.13, 0.23, 0.66))
    style(bx)
    rows = [("swap", "whole J-part (top 10)"), ("swap_noans", "J-part minus D's answer\ndirection"), ("swap_ans", "D's answer direction only"),
            ("swap_ans_rot", "answer direction, rotated")]  # fmt: skip
    for i, (m, run) in enumerate((("Qwen3.6-27B", "jswap_ans_v2_v1"), ("Qwen3.5-9B", "qwen35_9b_jswap_ans_v2_v1"))):
        s = load(RES / "jswap" / run / "summary.json") or {}
        for r, (c, _l) in enumerate(rows):
            v = s.get(f"PM/{c}")
            if v:
                dot(bx, v["transfer"], r + (i - 0.5) * 0.3, v["ci"], [J, JL][i], ["o", "s"][i], ms=6, label=SHORT[m] if r == 0 else None)
    bx.set_yticks(range(len(rows)), [r[1] for r in rows])
    bx.set_ylim(len(rows) - 0.5, -0.6)
    bx.set_xlim(-6, 100)
    bx.axvline(0, color=AXIS, lw=1)
    bx.set_xlabel("transfer, points (PM)")
    bx.legend(loc="lower right", frameon=False, fontsize=8)
    bx.set_title("B   Is it just the answer token?", y=1.13)
    header(fig, "Sufficient: in the strong models the 10 J-directions at the bridge's mention carry which entity it is; the answer follows a swapped J-part",
           "Swaps at the last token of the bridge's mention, across the band; only that token's J-part (the span of its top-10 J++ directions) is replaced")  # fmt: skip
    note(fig, "Transfer subtracts how often a third, unrelated entity's attribute comes out. Paste is not a ceiling: it also overwrites position and binding information (Lightning: J-part +45 vs paste +14). "
              "Stated-fact answers stay >= 92% under every J-part swap.\nThe J-part swap replaced the earlier steering test (C2), whose cells mostly broke > 10% of answers and were withdrawn (24 Oct re-score). "
              "OLMo: the J-part carries the entity though removing it costs only +5 (F03): carried, not needed. Ministral: readable (F02) but not carried, even with 100 directions.")  # fmt: skip
    save(fig, "F07_carries")


# ---------------------------------------------------------------------------------------------------------------- F08


def f08() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 6.4), sharey=True)
    groups = [("one passage, one J-part swap (pointer run, amendment 51)", [("J-part from D's own passage", "p:swap"),
                                              ("J-part from one neutral sentence about D", "p:swap_neutral"),
                                              ("  the same, without the entity's own-word directions", "p:swap_noown"),
                                              ("  the same, randomly rotated", "p:swap_neutral_rot"),
                                              ("  logit-lens part of the neutral sentence", "p:swap_neutral_u"),
                                              ("whole residual of the neutral sentence (paste)", "p:paste_neutral")]),
              ("cross-relation run (amendment 47)", [("J-part from a passage on the same relation", "x:swap_srel"),
                                                     ("J-part from a passage on another relation", "x:swap_xrel")]),
              ("probe run (amendment 48; probe-valid relations)", [("J-part (J++ top 10)", "q:swap"),
                                                                    ("supervised probe's subspace (top <= 10 directions)", "q:swap_probe")])]  # fmt: skip
    look = {"p:swap": (J, "o"), "p:swap_neutral": (J, "o"), "p:swap_noown": (J, "o"), "p:swap_neutral_rot": (ROT, "D"),
            "p:swap_neutral_u": (LOGIT, "s"), "p:paste_neutral": (PASTE, "v"), "x:swap_srel": (J, "o"), "x:swap_xrel": (J, "o"),
            "q:swap": (J, "o"), "q:swap_probe": (PROBE, "P")}  # fmt: skip
    ys, labels, seps, heads, y = {}, [], [], [], 0.0
    for gi, (glab, rows) in enumerate(groups):
        if gi:
            seps.append(y - 0.1)
            y += 0.4
        heads.append((y - 0.55, glab))
        for lab, key in rows:
            ys[key] = y
            labels.append((y, lab))
            y += 1
    for ax, m in zip(axes, HEAD, strict=True):
        src = {"p": (load(RES / "jswap" / dict(D.POINTER)[m] / "summary.json"), "memory"),
               "x": (load(RES / "jswap" / MOD[m][8] / "summary.json"), "memory"),
               "q": (load(RES / "probe_ceiling" / MOD[m][6] / "summary.json"), "memory_valid")}  # fmt: skip
        style(ax)
        for key, yy in ys.items():
            sm, fam = src[key[0]]
            c = sm[f"{fam}/{key[2:]}"]
            col, mk_ = look[key]
            dot(ax, c["transfer"], yy, c["ci"], col, mk_, ms=7, lab_off=1.5)
        for sy in seps:
            ax.axhline(sy, color=GRID, lw=1.2)
        for hy, hl in heads:
            ax.text(-4, hy, hl, fontsize=7.5, color=MUTED, va="center", style="italic")
        ax.axvline(0, color=AXIS, lw=1)
        ax.set_yticks([a for a, _ in labels], [b for _, b in labels])
        ax.set_ylim(y - 0.5, -1.0)
        ax.set_xlim(-5, 100)
        ax.set_title(f"{SHORT[m]}  ({MOD[m][2]})")
        ax.set_xlabel("answers moved to D's attribute (transfer, points)")
    top = header(fig, "What the J-part carries: a pointer to the entity, whatever context it came from, not the attribute a probe reads there",
                 "Three runs, each with its own baseline. Swaps at the last token of the bridge's mention, across the band; memory finals pooled")  # fmt: skip
    bot = note(fig, "Neutral sentence: “A reader asked a question about D in the letters page.” Its J-part moves the answer as much as one from D's own passage, on 8 of 8 relations in the Qwens and 7 of 7 read in Lightning; "
                    "so it is D, not a relation-primed answer (and not Neel's linear answer swap: F07 B). Own-word directions: the lens rows for the entity's own name tokens; "
                    "without them the Qwens keep 0.83-0.84 of the swap, Lightning 0.62 (more name-like).\nProbe: a supervised probe decodes the attribute at the mention about as well as J++ (readout ratio 0.91-1.21) "
                    "but swapping its subspace barely moves the answer: decodable is not carried. Pointer run: 150 random items per word, n 624-898; cross-relation n 198-374; probe n 420-891.")  # fmt: skip
    fig.tight_layout(rect=(0, bot, 1, top))
    save(fig, "F08_pointer")


# ---------------------------------------------------------------------------------------------------------------- F09


def f09() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.9), sharey=True)
    for ax, m in zip(axes, HEAD, strict=True):
        tl = load(RES / "jswap" / dict(D.POINTER)[m] / "summary.json")["timeline_memory"]
        lays = sorted({int(k.split("/L")[1]) for k in tl})
        ser = lambda c, k: [tl[f"{c}/L{la}"][k] for la in lays]  # noqa: E731
        lo, hi = map(int, MOD[m][2][1:].split("-"))
        style(ax, "y")
        ax.axvspan(lo - 0.5, hi + 0.5, color=GRID, alpha=0.8, lw=0)
        ax.text((lo + hi) / 2, 101, "edit band", ha="center", fontsize=7.5, color=MUTED)
        ax.plot(lays, ser("none", "kept"), color=INK2, lw=2, label="unedited: X's own attribute")
        ax.plot(lays, ser("swap_neutral", "donor"), color=J, lw=2, label="J-part from a neutral sentence about D: D's attribute")
        ax.plot(lays, ser("swap", "donor"), color=J, lw=2, ls=(0, (3, 2)), label="J-part from D's passage: D's attribute")
        ax.axhline(50, color=AXIS, lw=0.8, ls=":")
        ax.set_ylim(0, 105)
        ax.set_title(SHORT[m])
        ax.set_xlabel("layer (J++ lens read at the answer position)")
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    axes[0].set_ylabel("% of items whose lens top pick\nis that attribute")
    axes[0].legend(loc="upper left", frameon=False, fontsize=7.5)
    top = header(fig, "When: the edit is at the mention, but the attribute appears at the answer position only later, for the swapped entity as for the original",
                 "The J++ lens at the answer position, layer by layer: the recalled fact is computed after the band, from what the mention points to")  # fmt: skip
    bot = note(fig, "Memory finals pooled, 150 random items per word (amendment 51). Qwens: the attribute appears 7-10 layers past the band (27B ~L49, 9B ~L23). "
                    "Lightning: at the band's end (L30-32), and the swapped entity's attribute plateaus below half. Dan's half asks how this lookup reads the pointer.")  # fmt: skip
    fig.tight_layout(rect=(0, bot, 1, top))
    save(fig, "F09_lookup")


# ---------------------------------------------------------------------------------------------------------------- F10

DOSE54 = [("Qwen3.6-27B", "", "L32-40"), ("Qwen3.5-9B", "qwen35_9b_", "L12-16"), ("Nemotron-3.5-Lightning", "nem35l_", "L27-33"),
          ("Ministral-3-14B", "min14_", "L32-37"), ("Nemotron-3.5-Bolt", "nem35b_", "L42-53"), ("DeepSeek-V4-Flash", "dsv4f_", "L18-23")]  # fmt: skip
KS = [1, 3, 10, 30, 100, 300]
DCOL = {"Qwen3.6-27B": J, "Qwen3.5-9B": JL, "Nemotron-3.5-Lightning": "#184f95", "Ministral-3-14B": LOGIT, "Nemotron-3.5-Bolt": PROBE, "DeepSeek-V4-Flash": COMP}
DMK = {"Qwen3.6-27B": "o", "Qwen3.5-9B": "s", "Nemotron-3.5-Lightning": "D", "Ministral-3-14B": "^", "Nemotron-3.5-Bolt": "v"}


def dose_data(m: str, pre: str, band: str) -> list[dict] | None:
    run = f"{pre}{SET}_ko_cand2_{band}_dose54_s150_v1"
    sc = score(run).get("facts")
    size = load(RES / "removal_size" / f"{pre}removal_size_{band}_dose54_v1" / "summary.json")
    soft = load(A2 / "soft_score" / f"{run}.json") or {}
    if not sc or not size:
        return None
    med = lambda key: sorted(v[key] for v in size["median_share"].values())[len(size["median_share"]) // 2] * 100  # noqa: E731
    out = []
    for k in KS:
        c = sc.get(f"top{k}/start=all")
        if not c:
            continue
        g = lambda cond: (sc.get(f"{cond}/start=all") or {}).get("contrasts", {}).get("M-K", {}).get("diff")  # noqa: E731
        so = soft.get(f"top{k}", {})
        out.append({"k": k, "share": med(f"jlens_top{k}"), "mk": c["contrasts"]["M-K"]["diff"], "ci": c["contrasts"]["M-K"]["ci"],
                    "K": c["loss"]["K"], "rot": g(f"top{k}_rot"), "pc": g(f"top{k}_pcasize"), "u": g(f"unembed{k}"),
                    "smk": so.get("soft_M-K"), "sK": so.get("soft", {}).get("K"), "spc": soft.get(f"top{k}_pcasize", {}).get("soft_M-K")})  # fmt: skip
        r = out[-1]
        ctrl = [v for v in (r["rot"], r["pc"]) if v is not None]
        r["exc"] = r["mk"] - max(ctrl) if ctrl else None
    return out


def dose_readings(d: list[dict]) -> dict:
    """Amendment 54's readings (as written) and note 1's secondary readings."""
    cls = lambda k: "concentrated" if k <= 10 else "distributed" if k >= 100 else "intermediate"  # noqa: E731
    lim = next((r["k"] for r in d if r["K"] > 10 or (r["pc"] is not None and r["pc"] > r["mk"] / 2)), None)
    under = [r for r in d if lim is None or r["k"] < lim] or d[:1]
    top = max(r["mk"] for r in under)
    kstar = next(r["k"] for r in under if r["mk"] >= 0.9 * top)
    eu = [r for r in under if r["exc"] is not None]
    etop = max(r["exc"] for r in eu) if eu else None
    ekstar = next((r["k"] for r in eu if r["exc"] >= 0.9 * etop), None) if eu else None
    plim = next((r["k"] for r in d if r["sK"] is not None and r["sK"] > 10), None)
    return {"limit": lim, "kstar": kstar, "cls": cls(kstar), "ekstar": ekstar, "ecls": cls(ekstar) if ekstar else None, "plim": plim}


def f10() -> None:
    n = len(DOSE54)
    fig = plt.figure(figsize=(3.4 * n, 9.4))
    gap, x0 = 0.11 / n, 0.06
    w = (0.928 - (n - 1) * gap) / n
    top_ax = [fig.add_axes((x0 + i * (w + gap), 0.43, w, 0.33)) for i in range(n)]
    bot_ax = [fig.add_axes((x0 + i * (w + gap), 0.12, w, 0.2)) for i in range(n)]
    for i, (m, pre, band) in enumerate(DOSE54):
        ax, bx = top_ax[i], bot_ax[i]
        style(ax, "both")
        style(bx, "both")
        ax.set_ylim(-5, 80)
        bx.set_ylim(-3, 96)
        for a_ in (ax, bx):
            a_.set_xlim(0, 40)
            a_.axhline(0, color=AXIS, lw=1)
        ax.set_title(f"{SHORT[m]}  ({band})", fontsize=10, y=1.13)
        d = dose_data(m, pre, band)
        if not d:
            ax.text(20, 38, "running", ha="center", fontsize=9, color=MUTED)
            bx.text(20, 30, "running", ha="center", fontsize=9, color=MUTED)
        else:
            x = [r["share"] for r in d]
            ser = lambda key: [(r["share"], r[key]) for r in d if r.get(key) is not None]  # noqa: E731
            def line(axx, key, col, ls, mk_, mfc=None, lw=2):
                pts = ser(key)
                axx.plot([p_[0] for p_ in pts], [p_[1] for p_ in pts], ls=ls, color=col, lw=lw, marker=mk_, ms=5, mfc=mfc or col, mec=col if mfc else SURF, mew=1.2)
            line(ax, "mk", J, "-", "o")
            line(ax, "smk", J, "--", "o", mfc=SURF)
            line(ax, "pc", SIZE, "-", "^", lw=1.6)
            line(ax, "rot", ROT, "-", "D", lw=1.6)
            line(ax, "u", LOGIT, "-", "s", lw=1.6)
            for r in d:
                ax.annotate(f"{r['k']}", (r["share"], r["mk"]), xytext=(0, 6), textcoords="offset points", fontsize=6.5, color=INK2, ha="center")
            line(bx, "K", INK2, "-", "o")
            line(bx, "sK", INK2, "--", "o", mfc=SURF)
            rd = dose_readings(d)
            sks = [r["sK"] for r in d if r["sK"] is not None]
            ax.text(0.0, 1.015, f"plateau K* {rd['kstar']} as pre-registered ({rd['cls']}; limit K {rd['limit'] or '>300'});\n"
                                f"K* {rd['ekstar']} on the J-specific excess ({rd['ecls']});\n"
                                f"probability limit K {rd['plim'] or '>300'} (stated facts lose {min(sks):.0f}-{max(sks):.0f})",
                    transform=ax.transAxes, fontsize=7.3, color=INK2, va="bottom")  # fmt: skip
        bx.axhline(10, color=AXIS, lw=1, ls=":")
        bx.set_xlabel("residual removed, % (median over the band)", fontsize=8)
        if i == 0:
            ax.set_ylabel("recall minus stated-fact loss (M − K),\npoints", fontsize=9)
            bx.set_ylabel("stated facts lost,\npoints", fontsize=9)
            bx.text(1, 11, "10-point limit", fontsize=7, color=MUTED)
        else:
            ax.set_yticklabels([])
            bx.set_yticklabels([])
    h1 = [plt.Line2D([], [], color=J, lw=2, marker="o", ms=5, mec=SURF, label="J++ top K, greedy"),
          plt.Line2D([], [], color=J, lw=2, ls="--", marker="o", ms=5, mfc=SURF, mec=J, label="J++ top K, by probability"),
          plt.Line2D([], [], color=ROT, lw=1.6, marker="D", ms=5, mec=SURF, label="same norm, random direction"),
          plt.Line2D([], [], color=SIZE, lw=1.6, marker="^", ms=5, mec=SURF, label="same norm, top principal directions"),
          plt.Line2D([], [], color=LOGIT, lw=1.6, marker="s", ms=5, mec=SURF, label="logit lens, top K")]  # fmt: skip
    fig.legend(handles=h1, loc="upper left", bbox_to_anchor=(0.055, 0.905), ncol=5, frameon=False, fontsize=8.5, title="Top row (numbers at points: K directions)", title_fontsize=8.5, alignment="left")
    h2 = [plt.Line2D([], [], color=INK2, lw=2, marker="o", ms=5, mec=SURF, label="greedy (top answer wrong)"),
          plt.Line2D([], [], color=INK2, lw=2, ls="--", marker="o", ms=5, mfc=SURF, mec=INK2, label="by probability (answer probability lost)")]  # fmt: skip
    fig.legend(handles=h2, loc="upper left", bbox_to_anchor=(0.055, 0.38), ncol=2, frameon=False, fontsize=8.5, title="Bottom row: stated facts lost", title_fontsize=8.5, alignment="left")
    header(fig, "How much J-space: the J-specific part sits in the first 1-30 directions; past that, and in Bolt throughout, same-size removals cost about as much",
           "Each model at its band; test set, 150 random items per word (seed 0). The gap between the blue line and the others is the J-specific part")  # fmt: skip
    note(fig, "Readings (amendment 54, as pre-registered): plateau K* = smallest K reaching 90% of the largest J++ M − K below the specificity limit (stated facts lose > 10 greedy, or the size-matched control exceeds half "
              "the J++ M − K); <= 10 concentrated, >= 100 distributed. Note 1 (written after Lightning, before the others): the same rule on the J-specific excess (J++ minus the larger of the random-direction and "
              "size-matched controls), and specificity judged by probability, since greedy accuracy hides that large removals also drain the stated answer's probability. "
              "The per-word sample draws M and K items from partly different scenes: noise, not bias.")  # fmt: skip
    save(fig, "F10_dose")


# ---------------------------------------------------------------------------------------------------------------- F04
A2 = RES / "ablate_v2"


def c1gap(run: str):
    s = load(A2 / "c1_v2" / f"{run}.json")
    return (100 * s["rule"]["gap"], None) if s else None


def c1unembed(run: str):
    s = load(A2 / "c1_specificity" / f"{run}.json")
    if not s:
        return None
    b = next(iter(s["bands"].values()))
    return (100 * b["unembed10"]["gap"], None) if "unembed10" in b else None


def natplus(run: str, cond: str = "paper10", grp: str = "all/all"):
    s = load(A2 / "natplus_split" / f"{run}.json")
    c = (s or {}).get("cells", {}).get(f"{grp}/{cond}")
    return (c["gap"], c.get("gap_ci")) if c else None


def v1(run: str, cond: str = "paper10"):
    s = load(A2 / "jsuite_score" / f"{run}.json")
    c = (s or {}).get("cells", {}).get(f"all/{cond}")
    return (c["contrasts"]["M-P"]["diff"], c["contrasts"]["M-P"]["ci"]) if c else None


def v2(run: str, cond: str = "paper10"):
    x = D.mk(run, cond)
    return (x["d"], x["ci"]) if x else None


def f04() -> None:
    fig = plt.figure(figsize=(16, 9.8))
    # A: the 27B and 9B across every dataset
    ax = fig.add_axes((0.2, 0.12, 0.33, 0.72))
    style(ax)
    rows = [("toy puzzles (full_v8), data seed 1", "full2_ko_v1", c1gap, "full2_ko_unembed_v1", c1unembed),
            ("   seed 2", "fresh2_ko_v1", c1gap, None, None), ("   seed 3", "fresh3_ko_v1", c1gap, None, None),
            ("natural fact chains, seed 1", "natural_v1_chat_ko_v1", c1gap, "natural_v1_chat_ko_unembed_v1", c1unembed),
            ("   seed 2", "natural_v2_chat_ko_v1", c1gap, None, None), ("   seed 3", "natural_v3_chat_ko_v1", c1gap, None, None),
            ("natplus (rare + popular bridges)", "natplus_v1_chat_ko_cand2_v1", natplus, "natplus_v1_chat_ko_cand2_v1", lambda r: natplus(r, "unembed10")),
            ("jsuite v1 (3 relations; M − P)", "jsuite_v1_facts_test_chat_ko_cand2_v1", v1, "jsuite_v1_facts_test_chat_ko_cand2_v1", lambda r: v1(r, "unembed10")),
            ("   rendering 2", "jsuite_v1_facts_s2_test_chat_ko_cand2_v1", v1, None, None),
            ("jsuite v2 (8 relations; M − K)", "jsuite_v2_test_chat_ko_cand2_v1", v2, "jsuite_v2_test_chat_ko_cand2_v1", lambda r: v2(r, "unembed10")),
            ("   rendering 2", "jsuite_v2r2_test_chat_ko_cand2_s150_v1", v2, None, None), ("   rendering 3", "jsuite_v2r3_test_chat_ko_cand2_s150_v1", v2, None, None)]  # fmt: skip
    pre9 = {"jsuite_v2r2_test_chat_ko_cand2_s150_v1": "qwen35_9b_jsuite_v2r2_test_chat_ko_cand2_v1", "jsuite_v2r3_test_chat_ko_cand2_s150_v1": "qwen35_9b_jsuite_v2r3_test_chat_ko_cand2_v1"}
    for r, (_lab, run, fn, urun, ufn) in enumerate(rows):
        for i, (pre, col, mk_) in enumerate((("", J, "o"), ("qwen35_9b_", JL, "s"))):
            rr = pre9.get(run, pre + run) if pre else run
            v = fn(rr)
            if v:
                dot(ax, v[0], r + (i - 0.5) * 0.3, v[1], col, mk_, ms=6.5, text=False)
            if ufn:
                u = ufn(pre + urun)
                if u:
                    ax.plot(u[0], r + (i - 0.5) * 0.3, "s", color=LOGIT, ms=5, mfc=SURF, mew=1.4)
    for yy in (2.5, 5.5, 6.5, 8.5):
        ax.axhline(yy, color=GRID, lw=1.2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_ylim(len(rows) - 0.5, -0.6)
    ax.set_xlim(-8, 70)
    ax.axvline(0, color=AXIS, lw=1)
    ax.axvline(30, color=AXIS, lw=0.8, ls=":")
    ax.set_xlabel("recall loss minus read loss under the J++ top-10 removal, points")
    ax.legend(handles=[plt.Line2D([], [], ls="", marker="o", color=J, ms=7, label="Qwen 27B (L32-40)"),
                       plt.Line2D([], [], ls="", marker="s", color=JL, ms=7, label="Qwen 9B (L12-16)"),
                       plt.Line2D([], [], ls="", marker="s", color=LOGIT, mfc=SURF, mew=1.4, ms=6, label="logit-lens top 10 (control)")],
              loc="upper left", bbox_to_anchor=(0, 1.1), ncol=3, frameon=False, fontsize=8)  # fmt: skip
    ax.set_title("A   The two Qwens on every dataset we built (same bands throughout)", y=1.1)
    # B: other models on the earlier datasets
    bx = fig.add_axes((0.66, 0.5, 0.33, 0.34))
    style(bx)
    others = [("Qwen3-32B", [("toy", c1gap("qwen3_32b_full2_ko_v1")), ("toy s2", c1gap("qwen3_32b_fresh2_ko_v1"))]),
              ("Qwen 122B", [("toy", c1gap("qwen35_122b_full2_ko_v1")), ("v1", v1("qwen35_122b_jsuite_v1_facts_test_chat_ko_cand2_v1")), ("v2", v2("qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1"))]),
              ("Muse 30B", [("toy", c1gap("muse30_full2_ko_v1")), ("natplus", natplus("muse30_natplus_v1_chat_ko_cand2_v1")), ("v1", v1("muse30_jsuite_v1_facts_test_chat_ko_cand2_v1")), ("v2", v2("muse30_jsuite_v2_test_chat_ko_cand2_v1"))]),
              ("Olmo-Hybrid 7B", [("toy", c1gap("olmoh7_big2_ko_v1")), ("natural", c1gap("olmoh7_natural_v1_chat_ko_v1"))]),
              ("Olmo-3 7B", [("toy", c1gap("olmo3d7_big2_ko_v1")), ("natural", c1gap("olmo3d7_natural_v1_chat_ko_v1"))]),
              ("OLMo-3 32B base", [("v1", v1("olmo32_jsuite_v1_facts_test_qa_ko_cand2_v1")), ("v2", v2("olmo32_jsuite_v2_test_qa_ko_cand2_L12-20_v1"))])]  # fmt: skip
    dmk = {"toy": "o", "toy s2": "o", "natural": "s", "natplus": "D", "v1": "^", "v2": "v"}
    for r, (_m, vals) in enumerate(others):
        for q, (lab, v) in enumerate(vals):
            if v:
                bx.plot(v[0], r, dmk[lab], color=INK2, ms=7, mfc=SURF if lab == "toy s2" else INK2, mew=1.3)
                bx.annotate(lab, (v[0], r), xytext=(0, 7 if q % 2 == 0 else -13), textcoords="offset points", fontsize=6.5, color=MUTED, ha="center")
    bx.set_yticks(range(len(others)), [o[0] for o in others])
    bx.set_ylim(len(others) - 0.5, -0.7)
    bx.set_xlim(-10, 90)
    bx.axvline(0, color=AXIS, lw=1)
    bx.axvline(30, color=AXIS, lw=0.8, ls=":")
    bx.set_xlabel("J++ gap, points (marker: dataset)")
    bx.set_title("B   Other models on the datasets they ran (J++ only; Muse and 122B: see F03)")
    # C: what moves the number
    cx = fig.add_axes((0.66, 0.12, 0.33, 0.27))
    style(cx)
    checks = [("natplus popular bridges", natplus("natplus_v1_chat_ko_cand2_v1", grp="popularity/popular"), natplus("qwen35_9b_natplus_v1_chat_ko_cand2_v1", grp="popularity/popular")),
              ("natplus rare bridges", natplus("natplus_v1_chat_ko_cand2_v1", grp="popularity/rare"), natplus("qwen35_9b_natplus_v1_chat_ko_cand2_v1", grp="popularity/rare")),
              ("v1, prefilled answer", v1("jsuite_v1_facts_test_prefill_ko_cand2_v1"), v1("qwen35_9b_jsuite_v1_facts_test_prefill_ko_cand2_v1")),
              ("v1, raw Q&A (9B)", None, v1("qwen35_9b_jsuite_v1_facts_test_qa_ko_cand2_v1")),
              ("v1, Q&A: base model (9B)", None, v1("qwen35_9bb_jsuite_v1_facts_test_qa_ko_cand2_v1")),
              ("v1, plain J-lens, not J++ (27B)", v1("q27jlens_jsuite_v1_facts_test_chat_ko_cand2_v1"), None)]  # fmt: skip
    for r, (_l, a, b) in enumerate(checks):
        for i, (v, col, mk_) in enumerate(((a, J, "o"), (b, JL, "s"))):
            if v:
                dot(cx, v[0], r + (i - 0.5) * 0.3, v[1], col, mk_, ms=6, text=False)
    cx.set_yticks(range(len(checks)), [c[0] for c in checks])
    cx.set_ylim(len(checks) - 0.5, -0.6)
    cx.set_xlim(-8, 70)
    cx.axvline(0, color=AXIS, lw=1)
    cx.set_xlabel("recall minus read, points")
    cx.set_title("C   What moves it, and what doesn't")
    top = header(fig, "Not one dataset: the Qwens' recall-vs-read split replicates on every dataset we built since day 1; in other models it is absent, shared with the logit lens, or not robust",
                 "Each dataset's own contrast (toy: memory-final minus prompt-final words; natural/natplus: the same; v1: M − P; v2: M − K); J++ top-10 removal at the same band per model")  # fmt: skip
    bot = note(fig, "Toy puzzles (10/20-22): made-up pick/locker/partner chains; natural (10/23): real fact chains over 3 relations, 81 bridges; natplus: + rare bridges, 4 relations; jsuite v1 (10/24): passages, 3 relations, 65 bridges; v2 (10/25): F01. "
                    "Dotted line: the plan's pre-registered 30-point bar (the 9B's toy seed 2 missed it at 23; pooled 31). Intervals where stored (natplus, v1, v2); toy and natural gaps have none in the files.\n"
                    "C: Neel's narrow-concept prediction (rare bridges use the shared directions less) is not supported: rare bridges lose as much or more. About 4/5 of the 9B's dependence is already in the base model "
                    "(Q&A, same lens; instruct on the same Q&A format: 41). The lens matters: the plain J-lens finds half the J++ effect.")  # fmt: skip
    save(fig, "F04_settings")


# ---------------------------------------------------------------------------------------------------------------- F11


def f11() -> None:
    fig = plt.figure(figsize=(16, 7.6))
    NLC = "#184f95"

    def v2mod(run, mod):
        s = score(run).get(mod, {})
        return {c: {k.split("-")[0]: (v["diff"], v["ci"]) for k, v in s.get(c, {}).get("contrasts", {}).items()} | {"_s": s.get(c, {})} for c in ("paper10", "paper10_rot", "unembed10")}

    def nat3(run):
        c = (load(A2 / "nat3_score" / f"{run}.json") or {}).get("cells", {})
        return {cond: {w: (v["excess_over_PPP"], v["ci"]) for w, v in c.get(f"all/{cond}", {}).items()} for cond in ("paper10", "paper10_rot", "unembed10")}

    def mark(ax, x, y, ci, col, mk, hollow=False):
        ax.plot(ci, [y, y], color=col, lw=2, solid_capstyle="round", zorder=2)
        ax.plot(x, y, mk, ms=6, zorder=3, color=col, mec=col if hollow else SURF, mfc=SURF if hollow else col, mew=1.5)
        ax.text(ci[1] + 1.5, y, f"{x:+.0f}", va="center", fontsize=7, color=INK2)

    def ticks(ax, d, w, y):
        for cond, col in (("paper10_rot", ROT), ("unembed10", LOGIT)):
            if w in d[cond]:
                ax.plot(d[cond][w][0], y, "|", color=col, ms=8, mew=1.6, zorder=4)

    # A: three hops
    ax = fig.add_axes((0.075, 0.2, 0.235, 0.56))
    style(ax)
    order = ["MMM", "PMM", "MPM", "PPM", "MMP", "MPP", "PMP"]
    q9 = v2mod("qwen35_9b_" + SET + "_threehop_ko_cand2_v1", "threehop")
    series = [("Qwen 27B (v2)", J, "o", False, v2mod(SET + "_threehop_ko_cand2_v1", "threehop")),
              ("Nemotron Lightning (v2)", NLC, "D", False, v2mod("nem35l_" + SET + "_threehop_ko_cand2_v1", "threehop")),
              ("Nemotron Lightning (natural three-hop set)", NLC, "D", True, nat3("nem35l_nat3_v1_chat_ko_cand2_v1_drop"))]  # fmt: skip
    for i, (_lab, col, mk, hol, d) in enumerate(series):
        for r, w in enumerate(order):
            if w in d["paper10"]:
                y = r + (i - 1) * 0.26
                mark(ax, d["paper10"][w][0], y, d["paper10"][w][1], col, mk, hol)
                ticks(ax, d, w, y)
    ax.set_yticks(range(len(order)), [f"{w[0]} → {w[1]} → {w[2]}" for w in order])
    ax.set_ylim(len(order) - 0.5, -0.6)
    ax.set_xlim(-25, 90)
    ax.axvline(0, color=AXIS, lw=1)
    ax.axhline(3.5, color=GRID, lw=1, ls="--")
    ax.set_xlabel("points lost beyond the all-passage chain (P → P → P)")
    ax.set_title("A   Three hops: which chains need J++?", y=1.2)
    hs = [plt.Line2D([], [], ls="", marker=mk, color=col, mfc=SURF if hol else col, mec=col, mew=1.5, ms=7, label=lab) for lab, col, mk, hol, _d in series]
    hs += [plt.Line2D([], [], ls="", marker="|", color=ROT, ms=8, mew=1.6, label="rotated"), plt.Line2D([], [], ls="", marker="|", color=LOGIT, ms=8, mew=1.6, label="logit lens")]
    ax.legend(handles=hs, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=7.5)
    # B: numbers
    bx = fig.add_axes((0.47, 0.2, 0.2, 0.56))
    style(bx)
    rows = [("KR", "counted, then reported"), ("AR", "computed by arithmetic,\nthen reported"), ("MR", "recalled, then reported"), ("MM", "recalled, then used to\nrecall (vs to look up)")]
    nser = [("Qwen 27B", J, "o", v2mod(SET + "_numbers_ko_cand2_dd_v1", "numbers")), ("Qwen 9B", JL, "s", v2mod("qwen35_9b_" + SET + "_numbers_ko_cand2_dd_v1", "numbers")),
            ("Nemotron Lightning", NLC, "D", v2mod("nem35l_" + SET + "_numbers_ko_cand2_dd_v1", "numbers"))]  # fmt: skip
    for i, (_lab, col, mk, d) in enumerate(nser):
        for r, (w, _l) in enumerate(rows):
            if w in d["paper10"]:
                y = r + (i - 1) * 0.26
                mark(bx, d["paper10"][w][0], y, d["paper10"][w][1], col, mk)
                ticks(bx, d, w, y)
    bx.set_yticks(range(len(rows)), [r[1] for r in rows])
    bx.set_ylim(len(rows) - 0.5, -0.6)
    bx.set_xlim(-35, 90)
    bx.axvline(0, color=AXIS, lw=1)
    bx.axhline(2.5, color=GRID, lw=1, ls="--")
    bx.set_xlabel("points lost, minus a number read from the passage\n(last row: minus the same number used in a lookup)")
    bx.legend(handles=[plt.Line2D([], [], ls="", marker=mk, color=col, ms=7, label=lab) for lab, col, mk, _d in nser], loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=7.5)
    bx.set_title("B   Numbers: computed vs recalled", y=1.2)
    # C: what the model says instead
    cx = fig.add_axes((0.775, 0.2, 0.21, 0.56))
    style(cx)
    classes = [("answer", "still right", J), ("lure", "a lure in the passage", LOGIT), ("other_cand", "another valid answer", SIZE), ("other", "something else", PASTE), ("bridge", "the bridge's name", PROBE)]
    runs = [("Qwen 27B", "natplus_v1_chat_genspot_cand2_v1"), ("Qwen 9B", "qwen35_9b_natplus_v1_chat_genspot_cand2_strat_v1"), ("Lightning", "nem35l_natplus_v1_chat_genspot_cand2_v1"), ("Muse 30B", "muse30_natplus_v1_chat_genspot_cand2_v1")]
    r = 0
    labels = []
    for lab, run in runs:
        cells = load(RES / "gen_spot" / run / "summary.json")["cells"]
        for w in ("PM", "MM"):
            cl = cells[f"{w}/paper10"]["class"]
            n = sum(cl.values())
            left = 0
            for k, _l, col in classes:
                v = 100 * cl.get(k, 0) / n
                cx.barh(r, v, left=left, color=col, height=0.6, edgecolor=SURF, lw=1)
                left += v
            labels.append(f"{lab}, {w} (n {n})")
            r += 1
    cx.set_yticks(range(r), labels)
    cx.set_ylim(r - 0.5, -0.6)
    cx.set_xlim(0, 100)
    cx.set_xlabel("generated replies under the knock-out, %")
    cx.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c_, label=l) for _k, l, c_ in classes], loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=7.5)
    cx.set_title("C   What the model says instead (natplus)", y=1.2)
    s9 = q9["paper10"]["_s"]
    r9 = q9["paper10_rot"]["_s"]
    header(fig, "Beyond two hops: chains ending in a recall need J++; a number computed from the passage does not need it to be reported",
           "jsuite v2 three-hop and numbers modules (and Lightning's natural three-hop set), J++ top-10 removal at each model's band; ticks: the same removal rotated (green) and the logit lens's top 10 (orange)")  # fmt: skip
    note(fig, "A: each letter is one hop's source (P: stated in the passage, M: recalled); above the dashed line the last hop is a recall. "
              f"The 9B is left out: its all-passage chain alone loses {s9['loss']['PPP']:.0f} points (rotated {r9['loss']['PPP']:.0f}; n {s9['n']['PPP']}), so its excess cannot be read. "
              "Pre-registered (amendment 56): chains ending in a recall lose more than P → P → P; M → P → P and P → M → P do not. "
              "B: the passage states the number, lists items to count, gives two numbers to add, or says nothing (recall); numbers use the digit dictionary. Pre-registered: counted and computed within 10 of read; recalled at least 10 above. "
              "C: generated replies; the Qwens and Lightning rarely name the bridge (Muse often does): the entity is still known, its attribute is not.")  # fmt: skip
    save(fig, "F11_beyond")


# ---------------------------------------------------------------------------------------------------------------- F12

STATUS = {"good": ("#0ca30c", "✓"), "warn": ("#fab219", "~"), "bad": ("#d03b3b", "✗"), "untest": ("#898781", "⊘"), "none": (None, "·"), "pend": (None, "…"), "info": (None, "")}


def f12() -> None:
    def tl(run):
        s = load(RES / "removal_textloss" / run / "summary.json")
        if not s:
            return None
        m = s["mean_nll"]
        return m["top10"] - m["none"], m["top10_rot"] - m["none"]

    def ko(m):
        return D.mk(MOD[m][1]) if m in MOD else None

    def ratio(a, b):
        return a / b if a is not None and b else None

    cols = ["plain-text cost\nof the removal", "recall needs J\n(M − K, top 10)", "J-specific\n(rotated, logit)", "not just variance\n(size-matched)",
            "robust\n(probability,\nrenderings)", "other datasets", "J-part carries\nthe entity", "context-free\npointer", "probe reads,\ndoesn't carry",
            "where (positions)", "dose in K\n(F10)"]  # fmt: skip
    rows = []

    def v2row(m, label, tlrun, swap_run=None, pointer=False, other=("none", "-"), where=("none", "-"), dose=("pend", "amendment 54")):
        cells = []
        t = tl(tlrun) if tlrun else None
        cells.append(("good" if t and t[0] < 2 else "untest" if t else "none", f"{t[0]:+.2f} nats\n(rot {t[1]:+.2f})" if t else "-"))
        j = ko(m)
        cells.append(("good" if j["d"] >= 30 else "warn" if j["d"] >= 15 else "bad", f"{j['d']:+.0f} [{j['ci'][0]}, {j['ci'][1]}]"))
        r, u = D.mk(MOD[m][1], "paper10_rot"), D.mk(MOD[m][1], "unembed10")
        spec = max(r["d"], u["d"])
        cells.append(("good" if spec < 10 else "bad", f"rot {r['d']:+.0f}, logit {u['d']:+.0f}"))
        pc = D.mk(MOD[m][7], "paper10_pcasize") if MOD[m][7] else None
        rr = ratio(pc["d"], j["d"]) if pc else None
        cells.append((("good" if rr <= 1 / 3 else "bad" if rr >= 2 / 3 else "warn"), f"{rr:.2f} of J++") if rr is not None else ("none", "not run"))
        sv = load(RES / "ablate_v2" / "soft_score" / f"{MOD[m][1]}.json")
        sm = (sv or {}).get("paper10", {}).get("soft_M-K")
        nren = len(MOD[m][-1])
        cells.append((("good" if sm and sm >= 0.6 * j["d"] else "bad") if sm is not None else "none",
                      (f"prob. {sm:+.0f}" if sm is not None else "") + (f"\n{nren + 1} renderings" if nren else "")))  # fmt: skip
        cells.append(other)
        if swap_run:
            p = D.pooled(swap_run) or {}
            sw, pa = p.get("memory/swap", {}).get("transfer"), p.get("memory/paste", {}).get("transfer")
            cells.append(("good" if sw >= 20 else "warn" if sw >= 10 else "bad", f"swap {sw:+.0f}\n(paste {pa:+.0f})"))
        else:
            cells.append(("none", "not run"))
        if pointer:
            s = load(RES / "jswap" / dict(D.POINTER)[m] / "summary.json")
            rn = s["memory/swap_neutral"]["transfer"] / s["memory/swap"]["transfer"]
            no = s["memory/swap_noown"]["transfer"] / s["memory/swap"]["transfer"]
            cells.append(("good" if rn >= 2 / 3 else "bad", f"neutral {rn:.2f}\nno-name {no:.2f}"))
        else:
            cells.append(("none", "not run"))
        pr = load(RES / "probe_ceiling" / MOD[m][6] / "summary.json") if MOD[m][6] else None
        if pr and "memory_valid/swap" in pr:
            a, b = pr["memory_valid/swap"]["transfer"], pr["memory_valid/swap_probe"]["transfer"]
            cells.append((("good" if b <= a / 3 and a >= 20 else "warn"), f"J++ {a:+.0f}\nprobe {b:+.0f}"))
        else:
            cells.append(("none", "not run"))
        cells.append(where)
        dz = {mm: (pp, bb) for mm, pp, bb in DOSE54}.get(m)
        d = dose_data(m, *dz) if dz else None
        if d:
            rd = dose_readings(d)
            cells.append(("info", f"K* {rd['kstar']} (as written)\nexcess K* {rd['ekstar']}; prob. limit {rd['plim'] or '>300'}"))
        else:
            cells.append(dose)
        rows.append((label, cells))

    v2row("Qwen3.6-27B", "Qwen 27B (hybrid)", "textloss_top_l32_40_v1", "jswap_v2_v1", True, ("good", "toy x3, natural x3,\nnatplus, v1"),
          ("good", "mention (mid),\nquestion (late)"))  # fmt: skip
    v2row("Qwen3.5-9B", "Qwen 9B (hybrid)", "qwen35_9b_textloss_top_l12_16_v1", "qwen35_9b_jswap_v2_v1", True, ("good", "toy x3 (one < 30), natural\nx3, natplus, v1, base"),
          ("good", "mention (mid)"))  # fmt: skip
    lp = [cell(f"nem35l_{SET}_ko_cand2{m_}_v1", "paper10/start=P") for m_ in ("", "_posbridge", "_posquestion")]
    lwhere = (("warn", f"read: mention {lp[1][0]:+.0f},\nquestion {lp[2][0]:+.0f} of {lp[0][0]:+.0f}") if all(lp) else ("pend", "running tonight"))
    lnp = natplus("nem35l_natplus_v1_chat_ko_cand2_v1")
    lother = ("good", f"natplus {lnp[0]:+.0f},\nnatural three-hop") if lnp else ("none", "v2 only")
    v2row("Nemotron-3.5-Lightning", "Nemotron Lightning", "nem35l_textloss_top_v2gate_v1", "nem35l_jswap_v2_v1", True, lother, lwhere)
    v2row("DeepSeek-V4-Flash", "DeepSeek V4 Flash", "dsv4f_textloss_top_v2gate_v1", "dsv4f_jswap_v2_L22-27_v1", False, ("none", "v2 only"), ("warn", "question: about half"),
          ("warn", "rising at 30 (dev);\ncache dropped"))  # fmt: skip
    v2row("Ministral-3-14B", "Ministral 14B", "min14_textloss_top_v2gate_v1", "min14_jswap_v2_L20-25_v1", False, ("none", "v2 only"), ("good", "question (late only)"))
    bp = [cell(f"nem35b_{SET}_ko_cand2_L42-53_k100_pos{w}_s150_v1", "top100/start=all") for w in ("bridge", "question")]
    bd = {r["k"]: r for r in (dose_data("Nemotron-3.5-Bolt", "nem35b_", "L42-53") or [])}
    bwhere = (("warn", f"K 100: mention {bp[0][0]:+.0f},\nquestion {bp[1][0]:+.0f} of {bd[100]['mk']:+.0f}") if all(bp) and 100 in bd else ("pend", "running"))
    v2row("Nemotron-3.5-Bolt", "Nemotron Bolt", "nem35b_textloss_top_v2gate_v1", "nem35b_jswap_v2_k100_v1",
          (RES / "jswap" / dict(D.POINTER)["Nemotron-3.5-Bolt"] / "summary.json").exists(), ("none", "v2 only"), bwhere)  # fmt: skip
    v2row("OLMo-3-32B (base, Q&A)", "OLMo-3 32B base", "olmo32_textloss_top_l20_44_v1", "olmo32_jswap_v2_v1", False, ("bad", "v1 −3"), ("none", "-"), ("none", "-"))
    v2row("Muse-Glimmer-30B", "Muse 30B", "muse30_textloss_top_l36_42_v1", None, False, ("bad", "toy 7; natural/natplus\nmostly logit lens"), ("none", "-"), ("none", "-"))
    v2row("Qwen3.5-122B", "Qwen 122B (FP8)", "qwen35_122b_textloss_L39-45_v1", None, False, ("bad", "toy 9; natural null"), ("good", "question (late only)"), ("none", "-"))
    # models without a v2 run
    for label, run, txt in (("Qwen3-32B", "qwen3_32b_textloss_top_l44_52_v1", "toy 22, 17 (< 30);\nweights deleted"),
                            ("Olmo-Hybrid 7B", "olmoh7_textloss_top_l4_8_v1", "toy 1; natural 1"), ("Olmo-3 7B", "olmo3d7_textloss_top_l10_14_v1", "toy 4; natural 17"),
                            ("Gemma 4 31B-it", "gemma4itf_sink_textloss_v1", ""), ("gpt-oss-20b", "gptoss20_textloss_top_v1", ""), ("Kolibri-1", "kol1_textloss_top_l15_35_v1", "")):  # fmt: skip
        t = tl(run)
        unt = t and (t[0] >= 2)
        cells = [(("untest" if unt else "good") if t else "none", f"{t[0]:+.2f} nats\n(rot {t[1]:+.2f})" if t else "-")]
        cells += [("untest", "untestable")] if unt else [("none", "no v2 run")]
        cells += [("none", "")] * 3
        cells += [("bad", txt) if txt else ("none", "")]
        cells += [("none", "")] * 5
        rows.append((label, cells))
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_axes((0.11, 0.09, 0.885, 0.78))
    ax.axis("off")
    nR, nC = len(rows), len(cols)
    ax.set_xlim(0, nC)
    ax.set_ylim(nR + 0.9, 0)
    for j, c in enumerate(cols):
        ax.text(j + 0.5, 0.45, c, ha="center", va="center", fontsize=8, fontweight="bold", color=INK)
    for i, (label, cells) in enumerate(rows):
        y = i + 1
        ax.text(-0.05, y + 0.5, label, ha="right", va="center", fontsize=9, color=INK)
        for j, (st, txt) in enumerate(cells):
            col, icon = STATUS[st]
            ax.add_patch(plt.Rectangle((j + 0.03, y + 0.05), 0.94, 0.9, color=col if col else PANEL, alpha=0.22 if col else 1.0, lw=0))
            ax.text(j + 0.1, y + 0.5, icon, ha="left", va="center", fontsize=10, color=col or MUTED, fontweight="bold")
            ax.text(j + 0.55, y + 0.5, txt, ha="center", va="center", fontsize=7, color=INK2)
    ax.axhline(10, xmin=0, xmax=1, color=AXIS, lw=1.2)
    leg = [plt.Rectangle((0, 0), 1, 1, color=c or PANEL, alpha=0.4 if c else 1, label=f"{i}  {lab}") for (c, i), lab in zip(list(STATUS.values())[:6], ("holds", "weak / partial", "fails", "untestable", "not run", "running tonight"), strict=True)]
    ax.legend(handles=leg, loc="upper left", bbox_to_anchor=(0, -0.0), ncol=6, frameon=False, fontsize=8.5)
    top = header(fig, "Scorecard: every model we tried, every test; the gaps (·) are what is left for days 9-12",
                 "Above the line: models run on jsuite v2 at their band; below: models stopped earlier (untestable, failed on the earlier datasets, or weights deleted)")  # fmt: skip
    note(fig, "Rules (pre-registered where they exist): untestable if the top-10 removal adds >= 2 nats of plain-text loss; recall needs J at M − K >= 30 (15-30 weak); J-specific if rotated and logit-lens M − K < 10; "
              "size-matched M − K <= 1/3 of J++ (>= 2/3 fails); robust if the by-probability M − K keeps >= 60% of the greedy one; swap carries at >= 20 transfer (10-20 partial); "
              "pointer if the neutral-sentence donor keeps >= 2/3 of the swap; probe: its subspace's swap <= 1/3 of J++'s.\n"
              "Swaps: Bolt at K = 100 (K = 10: +3); DeepSeek and Ministral at mid depth (their knock-out bands are late or broke lookups). Text loss is measured at each model's gate band. "
              "Not on this card: the old steering test (C2), mostly withdrawn on 10/24; keep-own-word (C1's kill test) passed on the toy suite (27B restores 20%, kill bar 75%).")  # fmt: skip
    save(fig, "F12_scorecard")


FIGS = {"F01": f01, "F02": f02, "F03": f03, "F04": f04, "F05": f05, "F06": f06, "F07": f07, "F08": f08, "F09": f09, "F10": f10,
        "F11": f11, "F12": f12}

def pdf() -> None:
    """Every PNG in order, one per page, into all.pdf."""
    with PdfPages(OUT / "all.pdf") as pp:
        for png in sorted(OUT.glob("F*.png")):
            img = plt.imread(png)
            h, w = img.shape[:2]
            fig = plt.figure(figsize=(w / 170, h / 170))
            fig.add_axes((0, 0, 1, 1)).imshow(img)
            fig.axes[0].axis("off")
            pp.savefig(fig, dpi=170)
            plt.close(fig)
    print("all.pdf ok")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for k in sys.argv[1:] or list(FIGS):
        FIGS[k]()
    if not sys.argv[1:]:
        pdf()
