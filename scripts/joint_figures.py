"""joint_figures (agent, 27 Oct; Dan ~15:50): the root README's figures, the joint story of both tracks, in
scripts/story_style.py's visual language and the joint vocabulary (check_figure_terms.JOINT_RETIRED): "recalled answer"
(from memory) and "lookup answer" (written in the text); "the lens part" (the directions the J++ lens reads at the
bridge); the tools "remove everywhere" (Zach), "remove from the patch" (Dan) and "swap" (Zach); "order signal" (Dan's
four directions outside the lens); the models Qwen 9B, Qwen 27B, Qwen 122B, Muse 30B, Nemotron Lightning.

  figures/shared/j0_setup.png              one bridge, two answers, in Zach's passage and Dan's scene; the three tools
  figures/shared/j1_recall_needs_lens.png  recalled answers need the lens part, lookup answers do not (both tools)
  figures/shared/j2_swap.png               swapping the lens part moves the recalled answer, not the lookup one
  figures/shared/j3_order_signal.png       the lookup answer uses an order signal outside the lens (Dan's scenes)
  figures/shared/grid_front.png            the README's four findings x five models, from docs/shared/grid.csv
  figures/shared/data.csv                  every plotted number with its source (figures/story/data.csv's columns)
  docs/shared/contact_sheet_joint.png      the five, for one look

Sources: docs/breadth/data.csv (Zach's numbers), figures/story/data.csv (ours, with docs/x0_numbers.json's rows), Zach's
stored knock-out scores and swap runs under results/ (controls and the swap of everything else, not in his report), and
docs/shared/grid.csv. Example texts: Zach's from data/tasks_v2 (his Fig. 0's items), ours from readme_story_figures.f00_setup.

uv run python scripts/joint_figures.py     (CPU only; reads stored results)
"""

from __future__ import annotations

import csv
import io
import json
import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

from scripts import readme_story_figures as F  # noqa: E402
from scripts import results_digest as RD  # noqa: E402
from scripts import shared_grid as G  # noqa: E402
from scripts import story_style as S  # noqa: E402

OUT = REPO / "figures" / "shared"
DATA = OUT / "data.csv"
SHEET = REPO / "docs" / "shared" / "contact_sheet_joint.png"
BREADTH = REPO / "docs" / "breadth" / "data.csv"
DEPTH = REPO / "figures" / "story" / "data.csv"
ITEMS = REPO / "data" / "tasks_v2" / "jsuite_v2_test_chat" / "items.jsonl"
FIELDS = ("figure", "model", "quantity", "value", "lo", "hi", "n", "source")
ROWS: list[dict] = []

# (name on the figures, breadth data.csv model, our data.csv model, our numbers suffix); rows in the README's order
MODELS = (("Qwen 9B", "q9", "qwen3.5-9b", "9b"), ("Qwen 27B", "q27", "qwen3.6-27b", "27b"),
          ("Nemotron Lightning", "nl", None, None), ("Muse 30B", "mu", "muse-glimmer-30b", "muse"),
          ("Qwen 122B", "q122", "qwen3.5-122b-a10b", "122b"))  # fmt: skip
RECALLED, LOOKUP = S.COL["recall"], S.COL["lookup"]  # recalled answers dark grey; lookup answers purple
BRIDGE = "#fde3e3"  # the bridge's highlight (Fig. 0's)
REMOVED, WRITTEN = "#e3a3a3", "#9cc3e4"  # the tool strip: the lens part removed; another entity's lens part written in
SWAP_RUNS = {"q9": "qwen35_9b_jswap_v2_v1", "q27": "jswap_v2_v1"}  # Zach's v2 swaps at the band (data.csv swap.*.swap)
# Zach's Fig. 0 scene (scripts/fig_neel.py f01): the item with the fact stated and the one left to memory
ZACH_ITEMS = {"lookup": "j2:chat:facts:MK-L0-00635", "recalled": "j2:chat:facts:MM-L0-00635"}
ZACH_SENTENCES = {
    "lookup": "Mozart was Austrian by birth.",
    "recalled": "A reader asked a question about Mozart in the letters page.",
}
ZACH_DESCRIPTION, ZACH_BRIDGE = "The composer who wrote The Magic Flute", "Mozart"
# our Fig. 0 (readme_story_figures.f00_setup): the original prompt's three sentences and the two questions
DAN_SCENE = ("The locker of the frog is 5.", "The locker of the tick is 2.", "Iris picked the frog.")
DAN_QUESTIONS = (
    ("Which locker belongs to Iris's pick?", "5", "lookup"),
    ("How many legs does Iris's pick have?", "4", "recalled"),
)


# ---------------------------------------------------------------------------------------------------------- sources


def read_csv(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def breadth() -> dict[tuple[str, str], dict]:
    return {(r["model"], r["key"]): r for r in read_csv(BREADTH)}


def depth() -> dict[tuple[str, str, str], dict]:
    """(figure, model, quantity) -> figures/story/data.csv row; docs/x0_numbers.json's rows are ('numbers', '', key)."""
    return {(r["figure"], r["model"], r["quantity"]): r for r in read_csv(DEPTH)}


def num(x) -> float:
    return float(str(x).replace("−", "-"))


def record(fig: str, model: str, quantity: str, v, lo=None, hi=None, n=None, source: str = "") -> None:
    ROWS.append({"figure": fig, "model": model, "quantity": quantity, "value": v, "lo": "" if lo is None else lo,
                 "hi": "" if hi is None else hi, "n": "" if n is None else n, "source": source})  # fmt: skip


def write_data() -> None:
    DATA.write_text(data_text(ROWS))


def data_text(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(FIELDS), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def ko_control(row: dict) -> tuple[str, float, str]:
    """The larger control of Zach's knock-out on recalled answers (rotated or logit lens): its name, the recalled
    answers it loses (points, his score file beside the data.csv row) and that file."""
    path = row["source"]
    facts = json.loads((REPO / path).read_text())["facts"]
    lost = {
        name: facts[f"{cond}/start=all"]["loss"]["M"]
        for name, cond in (("rotated", "paper10_rot"), ("logit lens", "unembed10"))
    }
    name = max(lost, key=lambda k: lost[k])
    return name, lost[name], path


def zach_texts() -> dict[str, str]:
    """Zach's example: the question and the two passages' sentences, read from the dataset (asserted present)."""
    items = {}
    for line in ITEMS.read_text().splitlines():
        d = json.loads(line)
        if d["id"] in ZACH_ITEMS.values():
            items[d["id"]] = d
    out = {}
    for kind, item_id in ZACH_ITEMS.items():
        d = items[item_id]
        assert ZACH_SENTENCES[kind] in d["context"], item_id
        assert d["answer"] == "Austrian", item_id
        assert d["question"].startswith(ZACH_DESCRIPTION), d["question"]
        out["question"], out["answer"] = d["question"], d["answer"]
    return out


# ---------------------------------------------------------------------------------------------------------- drawing


def highlight(ax, t, word: str, color: str = BRIDGE) -> None:
    """A rounded patch behind the last `word` of the one-line text t, measured with the renderer."""
    r = ax.figure.canvas.get_renderer()
    s = t.get_text()
    i = s.rfind(word)
    probe = ax.text(*t.get_position(), s[: i + len(word)], fontsize=t.get_fontsize(), ha="left", va=t.get_va(),
                    style=t.get_style(), transform=t.get_transform())  # fmt: skip
    x1 = probe.get_window_extent(r).x1
    probe.set_text(word)
    w = probe.get_window_extent(r).width
    probe.remove()
    bb = t.get_window_extent(r)
    inv = ax.transData.inverted()
    (x0d, y0d), (x1d, y1d) = inv.transform([(x1 - w, bb.y0), (x1, bb.y1)])
    ax.add_patch(
        FancyBboxPatch((x0d, y0d), x1d - x0d, y1d - y0d, boxstyle="round,pad=0.25", fc=color, ec="none", zorder=0)
    )


def bar(ax, y: float, v: float, lo, hi, color: str, kind: str = "fixed", h: float = 0.36) -> None:
    """A horizontal bar with its 95% interval; filled = fixed in advance, open = after the data (story_style's code)."""
    face = color if kind == "fixed" else "white"
    ax.barh([y], [v], height=h, color=face, edgecolor=color, lw=1.6, zorder=2)
    if lo not in (None, ""):  # light on a dark bar, dark elsewhere, so the interval shows on every bar
        whisker = "#bdbdbd" if face == RECALLED else "#333333"
        ax.plot([num(lo), num(hi)], [y, y], color=whisker, lw=1.4, zorder=3)


def legend_below(fig, handles, labels, y: float, ncol: int) -> None:
    fig.legend(handles, labels, loc="lower left", bbox_to_anchor=(0.01, y), ncol=ncol, frameon=False,
               handletextpad=0.4, columnspacing=1.2)  # fmt: skip


def j0_setup(plt):
    """Zach's fact passages (one sentence differs) and Dan's locker scene (two questions), the bridge highlighted, each
    answer named; below, the three tools as token x layer sketches with a key."""
    # drawn at the PNG's dpi, so highlight() measures the words as they will be rasterised
    fig = plt.figure(figsize=(S.WIDTH, 8.0), dpi=200)
    ax = fig.add_axes((0, 0, 1, 0.89))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    S.title(fig, "One question, two kinds of answer: looked up or recalled",
            "Each tool tests whether an answer needs the lens part: what a lens reads at the bridge.")  # fmt: skip
    z = zach_texts()
    ans_x, lab_x = 67, 81.5

    def answer(y: float, a: str, kind: str) -> None:
        col = LOOKUP if kind == "lookup" else RECALLED
        ax.text(ans_x, y, f"→ {a}", fontsize=S.FONT, weight="bold", color=col, va="center")
        ax.text(lab_x, y, f"{kind} answer", fontsize=S.FONT, color=col, va="center")

    ax.text(1, 67, "Fact passages (Zach): one sentence differs", fontsize=S.FONT + 1, weight="bold", va="center")
    t = ax.text(3, 62.5, f"Question: {z['question']}", fontsize=S.FONT, va="center")
    highlight(ax, t, ZACH_DESCRIPTION)
    for y, kind in ((58, "lookup"), (53.5, "recalled")):
        t = ax.text(3, y, f"“… {ZACH_SENTENCES[kind]} …”", fontsize=S.FONT, va="center", style="italic")
        highlight(ax, t, ZACH_BRIDGE)
        answer(y, z["answer"], kind)
    ax.text(1, 47, "Locker scene (Dan): two questions", fontsize=S.FONT + 1, weight="bold", va="center")
    t = ax.text(3, 42.5, "“" + " ".join(DAN_SCENE) + "”", fontsize=S.FONT, va="center", style="italic")
    highlight(ax, t, "frog")
    for y, (q, a, kind) in zip((38, 33.5), DAN_QUESTIONS, strict=True):
        ax.text(3, y, q, fontsize=S.FONT, va="center")
        answer(y, a, kind)
    record("j0", "", "Zach's example (lookup / recalled items)", z["answer"],
           source=f"{ITEMS.relative_to(REPO)} | {', '.join(ZACH_ITEMS.values())}")  # fmt: skip
    record("j0", "", "Dan's example", "5 / 4", source="scripts/readme_story_figures.py | f00_setup")

    # the tool strip: tokens across, layers up; the bridge's column marked; a key below
    ax.plot([1, 99], [30, 30], color="#dddddd", lw=1)
    tools = (("remove everywhere", "Zach: takes out the lens part at every token, over a band of layers", "every"),
             ("remove from the patch", "Dan: patches the bridge word in from another prompt at one layer, without its "
              "lens part", "one"),
             ("swap", "Zach: writes another entity's lens part in at the bridge, over the band", "swap"))  # fmt: skip
    ntok, nlay, bridge_col, band = 7, 4, 4, (1, 2)
    for k, (name, cap, kind) in enumerate(tools):
        x0 = 2 + 33 * k
        ax.text(x0, 27.2, name, fontsize=S.FONT + 1, weight="bold", va="center")
        cw, ch = 3.4, 2.0
        for i in range(ntok):
            for j in range(nlay):
                removed = (kind == "every" and j in band) or (kind == "one" and i == bridge_col and j == band[0])
                written = kind == "swap" and i == bridge_col and j in band
                fc = REMOVED if removed else WRITTEN if written else "white"
                ax.add_patch(
                    Rectangle((x0 + 2 + i * cw, 16.6 + j * ch), cw * 0.86, ch * 0.8, fc=fc, ec="#9a9a9a", lw=0.8)
                )
        ax.text(x0 + 2 + bridge_col * cw + cw * 0.43, 16.0, "bridge", fontsize=S.FONT, ha="center", va="top",
                color=S.COL["muted"])  # fmt: skip
        ax.text(x0, 20.6, "layers", fontsize=S.FONT, rotation=90, ha="center", va="center", color=S.COL["muted"])
        ax.text(x0, 8.8, textwrap.fill(cap, 34), fontsize=S.FONT, va="center", linespacing=1.15)
    for x, fc, text in ((2, REMOVED, "lens part taken out"), (30, WRITTEN, "another entity's lens part written in")):
        ax.add_patch(Rectangle((x, 1.2), 2.2, 1.6, fc=fc, ec="#9a9a9a", lw=0.8))
        ax.text(x + 3.2, 2.0, text, fontsize=S.FONT, va="center")
    ax.text(72, 2.0, "columns: tokens", fontsize=S.FONT, va="center", color=S.COL["muted"])
    return fig


def j1_recall_needs_lens(plt):
    """Per model, recalled vs lookup answers lost under each tool; the larger control as a grey tick on recalled answers;
    hollow = after the data; 'not run' where a tool was not run."""
    zb, dp = breadth(), depth()
    fig = plt.figure(figsize=(S.WIDTH, 5.4))
    axes = (fig.add_axes((0.215, 0.31, 0.35, 0.50)), fig.add_axes((0.625, 0.31, 0.35, 0.50)))
    S.title(fig, "Recalled answers need the lens part; lookup answers do not",
            "Left: answers that turn wrong; right: patch switches no longer going through. "
            "Compare patterns, not numbers.")  # fmt: skip
    ys = {name: -i for i, (name, *_) in enumerate(MODELS)}
    for ax, panel in zip(axes, ("everywhere", "change"), strict=True):
        for name, zm, target, m in MODELS:
            y = ys[name]
            if panel == "everywhere":
                rc, st = zb[(zm, f"ko.{zm}.lostM")], zb[(zm, f"ko.{zm}.lostK")]
                kind = "after" if zm in G.AFTER_V2_KNOCKOUT else "fixed"
                cname, cv, cpath = ko_control(rc)
                pts = (num(rc["value"]), num(st["value"]))
                cis: tuple = (None, None)  # Zach's per-answer-kind losses carry no interval in data.csv
                src = (f"docs/breadth/data.csv | ko.{zm}.lostM", f"docs/breadth/data.csv | ko.{zm}.lostK")
                record("j1", name, "remove everywhere: recalled answers that turn wrong (pp)", pts[0], source=src[0])
                record("j1", name, "remove everywhere: lookup answers that turn wrong (pp)", pts[1], source=src[1])
                record("j1", name, f"remove everywhere, largest control ({cname}): recalled answers that turn wrong (pp)", cv,
                       source=f"{cpath} | facts {'paper10_rot' if cname == 'rotated' else 'unembed10'}/start=all loss M")  # fmt: skip
            else:
                if target is None:
                    ax.text(45, y, "not run", ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"])
                    record(
                        "j1",
                        name,
                        "remove from the patch",
                        "not run",
                        source="docs/shared/grid.csv | depth column '-'",
                    )
                    continue
                q = "main test (two people swap picks): {} extra loss"
                rc, st = dp[("fig01", target, q.format("recall"))], dp[("fig01", target, q.format("lookup"))]
                kind = "fixed"  # our main test, fixed in advance on all four (figures/story/scorecard.csv 'main test')
                cv = num(dp[("numbers", "", f"rc_droprand_{m}")]["value"])
                pts = (100 * num(rc["value"]), 100 * num(st["value"]))
                cis = tuple((100 * num(r["lo"]), 100 * num(r["hi"])) for r in (rc, st))
                for label, r, v in (("recalled", rc, pts[0]), ("lookup", st, pts[1])):
                    record("j1", name, f"remove from the patch: share of the {label} answers' switches lost beyond a random part (%)", round(v, 1),
                           round(100 * num(r["lo"]), 1), round(100 * num(r["hi"]), 1),
                           source=f"figures/story/data.csv | fig01 | {r['quantity']}")  # fmt: skip
                record("j1", name, "remove from the patch, control (a random part): share of the recalled answers' switches lost (%)", cv,
                       source=f"figures/story/data.csv | numbers | rc_droprand_{m}")  # fmt: skip
            ax.plot(pts, [y, y], color="#bbbbbb", lw=2.2, zorder=1, solid_capstyle="butt")
            ax.plot([cv], [y], marker="|", ms=15, mew=2.6, color=S.COL["control"], ls="", zorder=2)
            for v, ci, col in zip(pts, cis, (RECALLED, LOOKUP), strict=True):
                if ci is not None:  # the 95% interval
                    ax.plot(ci, [y, y], color=col, lw=1.6, zorder=3, solid_capstyle="butt")
                ax.plot([v], [y], "o", ms=8, mfc=col if kind == "fixed" else "white", mec=col, mew=1.8, zorder=4)
        ax.set_xlim(-15, 100)
        ax.set_ylim(-len(MODELS) + 0.4, 0.6)
        ax.axvline(0, color="#999999", lw=0.8, zorder=0)
        ax.set_xticks([0, 50, 100])
        ax.set_yticks([ys[n] for n, *_ in MODELS], [n for n, *_ in MODELS] if panel == "everywhere" else [])
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[0].set_title("remove everywhere (Zach)", fontsize=S.FONT + 1, loc="left")
    axes[1].set_title("remove from the patch (Dan)", fontsize=S.FONT + 1, loc="left")
    axes[0].set_xlabel("answers that turn wrong (pp)")
    axes[1].set_xlabel("share of the patch's switches lost,\nbeyond a random part (%)")
    hs = [plt.Line2D([], [], marker="o", ls="", color=RECALLED, ms=8), plt.Line2D([], [], marker="o", ls="", color=LOOKUP, ms=8),
          plt.Line2D([], [], marker="|", ls="", color=S.COL["control"], ms=13, mew=2.6),
          plt.Line2D([], [], marker="o", ls="", mfc="white", mec=RECALLED, mew=1.6, ms=8)]  # fmt: skip
    labels = ["recalled answer", "lookup answer", "largest control", "hollow: after the data"]
    legend_below(fig, hs, labels, 0.0, 2)
    return fig


def j2_swap(plt):
    """Two panels (which answer moves) with rows per model (Qwen 9B, Qwen 27B): the lens part swapped, everything else
    swapped; answers that switch to the other entity beyond switches to an unrelated one (pp), with 95% intervals. The
    swap of everything else is after the data (hollow), confirmed by Zach (docs/shared/zach_reply_2026-10-27.md)."""
    zb = breadth()
    fig = plt.figure(figsize=(S.WIDTH, 4.8))
    axes = (fig.add_axes((0.30, 0.26, 0.31, 0.53)), fig.add_axes((0.665, 0.26, 0.31, 0.53)))
    cols = (("recalled answer moves", RECALLED), ("lookup answer moves", LOOKUP))
    rows = ("swap the lens part", "swap everything else")
    ns, ticks, labels, heads = [], [], [], []
    for g, (name, zm, *_) in enumerate([MODELS[0], MODELS[1]]):
        run = SWAP_RUNS[zm]
        summ = json.loads((REPO / "results" / "jswap" / run / "summary.json").read_text())
        pooled = RD.pooled(run)
        assert pooled is not None
        r = zb[(zm, f"swap.{zm}.swap")]
        assert abs(pooled["memory/swap"]["transfer"] - num(r["value"])) < 0.05, (
            "Zach's pooling no longer gives data.csv's swap"
        )
        cells = {  # (row, column) -> (value, lo, hi, n, source, kind)
            (0, 0): (num(r["value"]), r["lo"], r["hi"], r["n"], f"docs/breadth/data.csv | swap.{zm}.swap", "fixed"),
            (0, 1): (summ["PK/swap"]["transfer"], *summ["PK/swap"]["ci"], summ["PK/swap"]["n"],
                     f"results/jswap/{run}/summary.json | PK/swap", "fixed"),
            (1, 0): (pooled["memory/swap_comp"]["transfer"], *pooled["memory/swap_comp"]["ci"], pooled["memory/swap_comp"]["n"],
                     f"results/jswap/{run}/rows.jsonl | memory finals pooled (results_digest.pooled), swap_comp", "after"),
            (1, 1): (summ["PK/swap_comp"]["transfer"], *summ["PK/swap_comp"]["ci"], summ["PK/swap_comp"]["n"],
                     f"results/jswap/{run}/summary.json | PK/swap_comp", "after"),
        }  # fmt: skip
        y0 = -g * 2.9
        heads.append((name, y0 + 0.85))
        for i in range(2):
            ticks.append(y0 - i)
            labels.append(rows[i])
        for c, (ctitle, col) in enumerate(cols):
            for i in range(2):
                v, lo, hi, n, src, kind = cells[(i, c)]
                bar(axes[c], y0 - i, v, lo, hi, col, kind, h=0.7)
                axes[c].text(max(v, num(hi)) + 3, y0 - i, f"{v:+.1f}", va="center", fontsize=S.FONT, color=col)
                record("j2", name, f"{rows[i]}: {ctitle} (pp)", v, lo, hi, n, source=src)
                ns.append(int(n))
    S.title(fig, "Swapping the lens part moves the recalled answer, not the lookup one",
            "Answers that switch to the other entity, beyond switches to an unrelated one (pp); "
            f"n {min(ns)}-{max(ns):,} per bar")  # fmt: skip
    tr = F.blend(fig, axes[0])
    for name, y in heads:
        axes[0].text(0.01, y, name, transform=tr, fontsize=S.FONT + 1, weight="bold", va="center")
    for c, ax in enumerate(axes):
        ax.set_xlim(-5, 100)
        ax.set_ylim(-4.45, 1.25)
        ax.axvline(0, color="#999999", lw=0.8)
        ax.set_xticks([0, 50, 100])
        ax.set_yticks(ticks, labels if c == 0 else [])
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.set_title(cols[c][0], fontsize=S.FONT + 1, color=cols[c][1], loc="left")
        ax.set_xlabel("answers that switch (pp)")
    hs = [Rectangle((0, 0), 1, 1, fc=RECALLED, ec=RECALLED), Rectangle((0, 0), 1, 1, fc="white", ec=RECALLED, lw=1.6)]
    legend_below(fig, hs, ["fixed in advance", "hollow: after the data"], 0.0, 2)
    return fig


def j3_order_signal(plt):
    """Qwen 9B and Muse 30B, Dan's scenes where another item moved: lookup answers that follow the locker's position with
    the whole patch, without the order signal and without a random part of its size (%); beside it, the order signal
    pointed at another locker (written at about a real patch's size) against a random vector (%)."""
    dp = depth()
    card = {(r["claim"], r["model"]): r["flag"] for r in read_csv(G.SCORECARD)}
    fig = plt.figure(figsize=(S.WIDTH, 5.0))
    pair = [MODELS[0], MODELS[3]]
    axl, axr = fig.add_axes((0.17, 0.34, 0.41, 0.43)), fig.add_axes((0.70, 0.34, 0.27, 0.43))
    light = "#b9a6ee"  # the lookup purple, lighter: the patch without the order signal
    arms = (("whole", "whole patch", LOOKUP), ("no_alf", "without the order signal", light),
            ("no_alf_rand", "without a random part (same size)", S.COL["control"]))  # fmt: skip
    ns = set()
    for g, (name, _, target, _m) in enumerate(pair):
        scard = {"Qwen 9B": "Qwen3.5-9B", "Muse 30B": "Muse Glimmer 30B"}[name]
        kind = "after" if "a" in card[("the lookup needs it", scard)] else "fixed"
        for k, (arm, label, col) in enumerate(arms):
            r = dp[("fig05", target, f"another item moved, {arm}: position share")]
            y = -g * 4.2 - k
            v, lo, hi = (round(100 * num(r[c]), 1) for c in ("value", "lo", "hi"))  # a share, drawn in %
            bar(axl, y, v, lo, hi, col, kind, h=0.8)
            axl.text(hi + 2, y, f"{v:.0f}", va="center", fontsize=S.FONT)
            record("j3", name, f"answers by position: {label} (%)", v, lo, hi, r["n"],
                   source=f"figures/story/data.csv | fig05 | {r['quantity']}")  # fmt: skip
            ns.add(r["n"])
        kind_w = "after" if "a" in card[("a write moves the lookup", scard)] else "fixed"
        w = dp[("fig07", target, "lookup target share, mean over locker pairs, s = 2")]
        dose = dp[("fig07", target, "dose (s / mean s*), s = 2")]
        rnd = dp[("fig07", target, "lookup target share, random direction, s = 4")]
        rdose = dp[("fig07", target, "dose (s / mean s*), s = 4")]
        for k, (r, col) in enumerate(((w, LOOKUP), (rnd, S.COL["control"]))):
            y = -g * 2.6 - k
            v = round(100 * num(r["value"]), 1)
            lo, hi = (round(100 * num(r[c]), 1) if r[c] != "" else "" for c in ("lo", "hi"))
            bar(axr, y, v, lo, hi, col, kind_w, h=0.8)
            axr.text((hi if isinstance(hi, float) and hi > v else v) + 2, y, f"{v:.0f}", va="center", fontsize=S.FONT)
            what = "order signal" if r is w else "random vector"
            record("j3", name, f"writes sending the lookup answer to the target locker: {what} (%)", v, lo, hi,
                   source=f"figures/story/data.csv | fig07 | {r['quantity']}")  # fmt: skip
        record("j3", name, "the order signal's write dose (times a real patch's size)", round(num(dose["value"]), 2),
               source=f"figures/story/data.csv | fig07 | {dose['quantity']}")  # fmt: skip
        record("j3", name, "the random vector's dose (times a real patch's size)", round(num(rdose["value"]), 2),
               source=f"figures/story/data.csv | fig07 | {rdose['quantity']}")  # fmt: skip
    S.title(fig, "The lookup answer uses an order signal the lens does not read",
            f"Dan's locker scenes where another item moved; {'/'.join(sorted(ns))} scenes per model (left)")  # fmt: skip
    axl.set_yticks([-g * 4.2 - 1 for g in range(2)], [n for n, *_ in pair])
    axr.set_yticks([-g * 2.6 - 0.5 for g in range(2)], [n for n, *_ in pair])
    for ax, lim in ((axl, (-7.9, 0.7)), (axr, (-4.3, 0.7))):
        ax.set_xlim(0, 100)
        ax.set_ylim(*lim)
        ax.set_xticks([0, 50, 100])
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axl.set_title("lookup answers that follow position", fontsize=S.FONT + 1, loc="left")
    axr.set_title("order signal pointed\nat another locker", fontsize=S.FONT + 1, loc="left")
    axl.set_xlabel("% of lookup answers")
    axr.set_xlabel("% of writes that reach it")
    hs = [Rectangle((0, 0), 1, 1, fc=LOOKUP, ec=LOOKUP), Rectangle((0, 0), 1, 1, fc=light, ec=light),
          Rectangle((0, 0), 1, 1, fc=S.COL["control"], ec=S.COL["control"]),
          Rectangle((0, 0), 1, 1, fc="white", ec=RECALLED, lw=1.6)]  # fmt: skip
    labels = ["whole patch; order signal written", "without the order signal", "random part or vector",
              "hollow: after the data"]  # fmt: skip
    legend_below(fig, hs, labels, 0.0, 2)
    return fig


# the README's findings: (label, grid rows as (study, grid claim)); finding 4 is derived from rows below it
FINDINGS = (
    ("recalled answers need the lens part; lookup ones do not", (("depth", G.RECALL), ("breadth", G.RECALL))),
    ("swapping the lens part moves the recalled answer, not the lookup one",
     (("breadth", "another entity's J++ part moves the answer (≥ 20 points)"),)),
    ("the lookup answer uses an order signal outside the lens", (("depth", "the lookup needs it"),)),
    ("the two methods agree on this model", (("depth", G.RECALL), ("breadth", G.RECALL),
                                              ("breadth", "specific: rotated and logit-lens removals cost < 10"))),
)  # fmt: skip


def agree(d: dict, b: dict, s: dict) -> tuple[str, str]:
    """Finding 4: '-' if either method was not run; 'x' if one grades the recall split held and the other not, or remove
    everywhere fails its rotated and logit-lens control there; '~' if the two grades differ by a partial; else 'ok'.
    'a' if any input is after the data."""
    cells = {d["cell"], b["cell"]}
    flag = "a" if "a" in (d["flag"] + b["flag"] + s["flag"]) else ""
    if "-" in cells:
        return "-", ""
    if {"ok", "x"} <= cells or s["cell"] == "x":
        return "x", flag
    return ("~" if len(cells) > 1 or s["cell"] == "~" else "ok"), flag


def front_cells() -> dict[tuple[int, str], list[dict]]:
    """(finding, model) -> the marks to draw (two for finding 1: Dan's, Zach's), each a grid.csv row or a derived one."""
    grid = read_csv(G.GRID)
    by = {(r["study"], r["claim"], r["model"]): r for r in grid}
    header = {code: h for h, _, code in G.MODELS}
    out = {}
    for name, zm, *_ in MODELS:
        h = header[zm]
        for i, (_label, rows) in enumerate(FINDINGS):
            got = [by[(study, claim, h)] for study, claim in rows]
            if i == 3:
                cell, flag = agree(*got)
                got = [{"cell": cell, "flag": flag, "claim": "derived", "study": "both"}]
            out[(i, name)] = got
    return out


def grid_front(plt):
    """The README's four findings x five models in the full grid's cells (shared_grid: a coloured cell per grade with Fig.
    11's symbol inside, a corner mark for after the data); finding 1 as two strips, Dan's tool above Zach's."""
    cells = front_cells()
    names = [n for n, *_ in MODELS]
    labels = ("recalled answers need the lens part", "swapping it moves the recalled answer",
              "lookup answers use an order signal", "both tools hold, controls included")  # fmt: skip
    strips = [len(cells[(i, names[0])]) for i in range(len(FINDINGS))]
    strip_in, top_in, bottom_in = 0.40, 1.95, 0.62
    h = top_in + strip_in * sum(strips) + bottom_in
    fig = plt.figure(figsize=(S.WIDTH, h))
    ax = fig.add_axes((0.40, bottom_in / h, 0.58, strip_in * sum(strips) / h))
    S.title(fig, "Findings hold on Qwen 9B; Muse 30B and Qwen 122B fail controls",
            "Each finding graded per model; row 1 shows each tool (Dan above, Zach below)")  # fmt: skip
    G.legend_strip(fig, 0.5 + 0.2 + 0.05, h)
    ax.set_xlim(-0.5, len(names) - 0.5)
    ax.set_ylim(sum(strips), 0)
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    for j, name in enumerate(names):
        ax.text(j, -0.15, name.replace("Nemotron ", "Nemotron\n"), ha="center", va="bottom", fontsize=S.FONT,
                weight="bold", linespacing=1.0)  # fmt: skip
    tr = F.blend(fig, ax)
    y = 0.0
    for i, label in enumerate(labels):
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((-20.5, y), len(names) + 20, strips[i], fc="#f7f7f7", ec="none", zorder=0,
                                       clip_on=False))  # fmt: skip
        ax.text(0.01, y + strips[i] / 2, f"{i + 1}. {label}", transform=tr, fontsize=S.FONT, va="center")
        for t in range(strips[i]):
            yc = y + t + 0.5
            if strips[i] == 2:
                ax.text(-0.56, yc, "Dan" if t == 0 else "Zach", ha="right", va="center", fontsize=S.FONT,
                        color=S.COL["muted"])  # fmt: skip
            for j, name in enumerate(names):
                r = cells[(i, name)][t]
                ax.add_patch(G.plt_rect((j - 0.45, yc - 0.42), 0.9, 0.84, G.FILL[r["cell"]]))
                sym, col = F.CELL_SYMBOL[r["cell"]]
                ax.text(j, yc, sym, ha="center", va="center", fontsize=S.FONT + 1, color=col, weight="bold")
                if "a" in r["flag"]:
                    G.corner(ax, j + 0.45, yc - 0.42, 0.22, -0.34)
                record("grid_front", name, f"finding {i + 1} ({r['study']})", r["cell"] + (f" {r['flag']}" if r["flag"] else ""),
                       source=f"docs/shared/grid.csv | {r['claim']}" if r["claim"] != "derived" else
                       "derived (joint_figures.agree) from docs/shared/grid.csv: both studies' recall rows and breadth's 'specific' row")  # fmt: skip
        y += strips[i]
    fig.text(0.01, 0.1 / h, "Row 4: both tools grade row 1 the same, and remove everywhere passes its logit-lens check.\n"
             "Row 2: Nemotron Lightning's swap is not counted in the README; its ceiling check failed.",
             fontsize=S.FONT, color=S.COL["muted"], va="bottom")  # fmt: skip
    return fig


def x45r_score() -> Path:
    """The latest score of the Muse depth test (scripts/x45r_score.py)."""
    return sorted((REPO / "results" / "x45r").glob("score-*/x45r.json"))[-1]


def j5_muse_depth(plt):
    """Muse 30B, Zach's tool only (Dan ~19:50): recalled minus lookup answers lost (pp) at layers 23-29, layer 26 and
    layers 36-42, each with its 95% interval and one grey tick for the logit lens's own directions; the bar of 15 fixed
    in advance; layers 36-42 hollow (after the data). Our layer-26 result in one text line, no second axis. Kept as a
    file for the call and slides; not on the README."""
    path = x45r_score()
    src = str(path.relative_to(REPO))
    sc = json.loads(path.read_text())
    rule = json.loads((REPO / "results/ablate_v2/jsuite2_score" / f"{sc['rule_run']}.json").read_text())
    n = rule["facts"]["paper10/start=all"]["n"]
    sets = (("layers 23-29", "his_L23_29", sc["his_L23_29"], "fixed"),
            ("layer 26", "descriptive.L26", sc["descriptive"]["L26"], "fixed"),
            ("layers 36-42", "descriptive.L36_42_record", sc["descriptive"]["L36_42_record"], "after"))  # fmt: skip
    # the largest rotated or size-matched control over the three layer sets, named in the subtitle with its key
    others = [(c["paper10_rot"]["mk"], f"{key}.paper10_rot.mk") for _, key, c, _ in sets]
    others += [(sc["his_L23_29"]["paper10_pcasize"]["mk"], "his_L23_29.paper10_pcasize.mk"),
               (sc["descriptive"]["L26"]["paper10_pcasize"]["mk"], "descriptive.L26.paper10_pcasize.mk"),
               (sc["descriptive"]["L36_42_size_matched"]["paper10_pcasize"]["mk"],
                "descriptive.L36_42_size_matched.paper10_pcasize.mk")]  # fmt: skip
    worst, worst_key = max(others)
    fig = plt.figure(figsize=(S.WIDTH, 4.6))
    S.title(fig, "Muse 30B: lens-part removal hurts only late; logit lens does over half",
            f"Remove everywhere, {n['M']} items each; rotated and size-matched controls ≤ {worst:.1f} pp")  # fmt: skip
    ax = fig.add_axes((0.17, 0.33, 0.79, 0.47))
    record("j5", "Muse 30B", "remove everywhere: items per answer kind (recalled, lookup)", n["M"], n=n["K"],
           source=f"results/ablate_v2/jsuite2_score/{sc['rule_run']}.json | facts paper10/start=all n")  # fmt: skip
    for i, (label, key, cells, kind) in enumerate(sets):
        y = -i
        lens, u = cells["paper10"], cells["unembed10"]
        ax.plot(lens["ci"], [y, y], color=RECALLED, lw=1.8, zorder=2)
        ax.plot(
            [lens["mk"]], [y], "o", ms=10, mfc=RECALLED if kind == "fixed" else "white", mec=RECALLED, mew=1.8, zorder=3
        )
        ax.plot(u["ci"], [y - 0.16, y - 0.16], color=S.COL["control"], lw=1.6, zorder=2)  # its 95% interval
        ax.plot([u["mk"]], [y - 0.16], marker="|", ms=13, mew=2.6, color=S.COL["control"], ls="", zorder=2)
        ax.text(lens["mk"], y + 0.3, f"{lens['mk']:+.1f}", ha="center", va="center", fontsize=S.FONT + 1)
        if u["mk"] > 10:  # where the logit lens costs something, its value beside it
            ax.text(u["ci"][1] + 1.5, y - 0.16, f"{u['mk']:+.1f}", va="center", fontsize=S.FONT, color="#777777")
        for cond, v in (("paper10", lens), ("unembed10", u)):
            record("j5", "Muse 30B", f"remove everywhere, {label}, {'lens part' if cond == 'paper10' else 'logit lens'}: "
                   "recalled minus lookup answers lost (pp)", v["mk"], v["ci"][0], v["ci"][1], n["M"],
                   source=f"{src} | {key}.{cond}.mk")  # fmt: skip
    record("j5", "Muse 30B", "remove everywhere: rotated and size-matched controls, the largest (pp)", worst,
           source=f"{src} | {worst_key}")  # fmt: skip
    ax.axvline(15, color="#555555", ls="--", lw=1.2, zorder=1)
    ax.text(15.8, 0.52, "bar fixed in advance", fontsize=S.FONT, color=S.COL["muted"], va="center")
    record("j5", "Muse 30B", "remove everywhere: the 'needed' bar (pp)", 15.0,
           source="scripts/x45r_score.py | NOT_NEEDED_MK, NOT_NEEDED_EXCESS, CARRIED = 15.0")  # fmt: skip
    ax.set_xlim(-5, 75)
    ax.set_ylim(-2.5, 0.7)
    ax.set_xticks([0, 15, 30, 45, 60, 75])
    ax.set_yticks([-i for i in range(len(sets))], [s[0] for s in sets])
    ax.axvline(0, color="#999999", lw=0.8, zorder=0)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("recalled minus lookup answers that turn wrong (pp)")
    gap = depth()[("numbers", "", "contrast_muse")]
    g = S.parse(gap["value"])
    assert g is not None
    fig.text(0.01, 0.025, f"Dan's patch at layer 26: the lens part carries the answer ({100 * g[0]:.0f}% of the patch's "
             "switches); a different measure.", fontsize=S.FONT, va="bottom")  # fmt: skip
    record("j5", "Muse 30B", "remove from the patch, layer 26: gap (share of the patch's switches, %)", round(100 * g[0]),
           round(100 * g[1]), round(100 * g[2]), source="figures/story/data.csv | numbers | contrast_muse")  # fmt: skip
    hs = [plt.Line2D([], [], marker="o", ls="", color=RECALLED, ms=9),
          plt.Line2D([], [], marker="|", ls="", color=S.COL["control"], ms=14, mew=2.6),
          plt.Line2D([], [], marker="o", ls="", mfc="white", mec=RECALLED, mew=1.6, ms=9)]  # fmt: skip
    labels = ["lens part taken out", "logit lens's own directions taken out", "hollow: after the data"]
    legend_below(fig, hs, labels, 0.075, 2)
    return fig


FIGURES = (("j0_setup", j0_setup), ("j1_recall_needs_lens", j1_recall_needs_lens), ("j2_swap", j2_swap),
           ("j3_order_signal", j3_order_signal), ("grid_front", grid_front), ("j5_muse_depth", j5_muse_depth))  # fmt: skip


def save(fig, name: str) -> None:
    """As story_style.save, into figures/shared."""
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", facecolor="white")
    fig.savefig(OUT / f"{name}.png", dpi=200, facecolor="white")


def main() -> None:
    ROWS.clear()
    plt = S.setup()
    for name, draw in FIGURES:
        fig = draw(plt)
        save(fig, name)
        plt.close(fig)
    write_data()
    saved = S.OUT
    try:  # readme_story_figures.contact_sheet reads its PNGs from story_style.OUT
        S.OUT = OUT
        F.contact_sheet(plt, [n for n, _ in FIGURES], SHEET, cols=2)
    finally:
        S.OUT = saved
    print(
        f"{len(FIGURES)} figures in {OUT.relative_to(REPO)}; {len(ROWS)} rows in {DATA.relative_to(REPO)}; {SHEET.relative_to(REPO)}"
    )


if __name__ == "__main__":
    main()
