"""joint_figures (agent, 27 Oct; Dan ~15:50): the root README's figures, the joint story of both tracks, in
scripts/story_style.py's visual language and the joint vocabulary (check_figure_terms.JOINT_RETIRED): "recalled answer"
(from memory) and "stated answer" (written in the text); "the lens part" (the directions the J++ lens reads at the
bridge); the tools "remove everywhere" (Zach), "remove from the change" (Dan) and "swap" (Zach); "order signal" (Dan's
four directions outside the lens); the models Qwen 9B, Qwen 27B, Qwen 122B, Muse 30B, Nemotron Lightning.

  figures/shared/j0_setup.png              one bridge, two answers, in Zach's passage and Dan's scene; the three tools
  figures/shared/j1_recall_needs_lens.png  recalled answers need the lens part, stated answers do not (both tools)
  figures/shared/j2_swap.png               swapping the lens part moves the recalled answer, not the stated one
  figures/shared/j3_order_signal.png       the stated answer uses an order signal outside the lens (Dan's scenes)
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
RECALLED, STATED = S.COL["recall"], S.COL["lookup"]  # recalled answers dark grey; stated answers purple (our lookup's)
BRIDGE = "#fde3e3"  # the bridge's highlight (Fig. 0's)
REMOVED, WRITTEN = "#e3a3a3", "#9cc3e4"  # the tool strip: the lens part removed; another entity's lens part written in
SWAP_RUNS = {"q9": "qwen35_9b_jswap_v2_v1", "q27": "jswap_v2_v1"}  # Zach's v2 swaps at the band (data.csv swap.*.swap)
# Zach's Fig. 0 scene (scripts/fig_neel.py f01): the item with the fact stated and the one left to memory
ZACH_ITEMS = {"stated": "j2:chat:facts:MK-L0-00635", "recalled": "j2:chat:facts:MM-L0-00635"}
ZACH_SENTENCES = {
    "stated": "Mozart was Austrian by birth.",
    "recalled": "A reader asked a question about Mozart in the letters page.",
}
ZACH_DESCRIPTION, ZACH_BRIDGE = "The composer who wrote The Magic Flute", "Mozart"
# our Fig. 0 (readme_story_figures.f00_setup): the original prompt's three sentences and the two questions
DAN_SCENE = ("The locker of the frog is 5.", "The locker of the tick is 2.", "Iris picked the frog.")
DAN_QUESTIONS = (
    ("Which locker belongs to Iris's pick?", "5", "stated"),
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
    if lo not in (None, ""):
        ax.plot([num(lo), num(hi)], [y, y], color="#333333", lw=1.2, zorder=3)


def legend_below(fig, handles, labels, y: float, ncol: int) -> None:
    fig.legend(handles, labels, loc="lower left", bbox_to_anchor=(0.01, y), ncol=ncol, frameon=False,
               handletextpad=0.4, columnspacing=1.2)  # fmt: skip


def j0_setup(plt):
    """Zach's passage (one sentence differs) and Dan's scene (two questions), the bridge highlighted, each answer named;
    below, the three tools as token x layer sketches."""
    # drawn at the PNG's dpi, so highlight() measures the words as they will be rasterised
    fig = plt.figure(figsize=(S.WIDTH, 7.6), dpi=200)
    ax = fig.add_axes((0, 0, 1, 0.885))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 66)
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    S.title(fig, "The same bridge, two answers: stated in the text or recalled",
            "Each tool asks whether an answer needs the lens part of the bridge.")  # fmt: skip
    z = zach_texts()
    ans_x, lab_x = 67, 77.5

    def answer(y: float, a: str, kind: str) -> None:
        col = STATED if kind == "stated" else RECALLED
        ax.text(ans_x, y, f"→ {a}", fontsize=S.FONT, weight="bold", color=col, va="center")
        ax.text(lab_x + 4, y, f"{kind} answer", fontsize=S.FONT, color=col, va="center")

    ax.text(1, 63, "Zach's passages: one sentence differs", fontsize=S.FONT + 1, weight="bold", va="center")
    t = ax.text(3, 58.5, f"Question: {z['question']}", fontsize=S.FONT, va="center")
    highlight(ax, t, ZACH_DESCRIPTION)
    for y, kind in ((54, "stated"), (49.5, "recalled")):
        t = ax.text(3, y, f"“… {ZACH_SENTENCES[kind]} …”", fontsize=S.FONT, va="center", style="italic")
        highlight(ax, t, ZACH_BRIDGE)
        answer(y, z["answer"], kind)
    ax.text(1, 43, "Dan's scene: two questions", fontsize=S.FONT + 1, weight="bold", va="center")
    t = ax.text(3, 38.5, "“" + " ".join(DAN_SCENE) + "”", fontsize=S.FONT, va="center", style="italic")
    highlight(ax, t, "frog")
    for y, (q, a, kind) in zip((34, 29.5), DAN_QUESTIONS, strict=True):
        ax.text(3, y, q, fontsize=S.FONT, va="center")
        answer(y, a, kind)
    record(
        "j0",
        "",
        "Zach's example (stated / recalled items)",
        z["answer"],
        source=f"{ITEMS.relative_to(REPO)} | {', '.join(ZACH_ITEMS.values())}",
    )
    record("j0", "", "Dan's example", "5 / 4", source="scripts/readme_story_figures.py | f00_setup")

    # the tool strip: tokens across, layers up; the bridge's column marked
    ax.plot([1, 99], [26, 26], color="#dddddd", lw=1)
    tools = (("remove everywhere", "Zach: takes out the lens part at every token, over a band of layers", "every"),
             ("remove from the change", "Dan: the bridge word's change added at one layer, without its lens part", "one"),
             ("swap", "Zach: another entity's lens part written in at the bridge, over the band", "swap"))  # fmt: skip
    ntok, nlay, bridge_col, band = 7, 4, 4, (1, 2)
    for k, (name, cap, kind) in enumerate(tools):
        x0 = 2 + 33 * k
        ax.text(x0, 23.2, name, fontsize=S.FONT + 1, weight="bold", va="center")
        cw, ch = 3.4, 2.0
        for i in range(ntok):
            for j in range(nlay):
                removed = (kind == "every" and j in band) or (kind == "one" and i == bridge_col and j == band[0])
                written = kind == "swap" and i == bridge_col and j in band
                fc = REMOVED if removed else WRITTEN if written else "white"
                ax.add_patch(
                    Rectangle((x0 + 2 + i * cw, 12.6 + j * ch), cw * 0.86, ch * 0.8, fc=fc, ec="#9a9a9a", lw=0.8)
                )
        ax.text(
            x0 + 2 + bridge_col * cw + cw * 0.43,
            12.0,
            "bridge",
            fontsize=S.FONT,
            ha="center",
            va="top",
            color=S.COL["muted"],
        )
        ax.text(x0, 16.6, "layers", fontsize=S.FONT, rotation=90, ha="center", va="center", color=S.COL["muted"])
        ax.text(x0, 4.6, textwrap.fill(cap, 34), fontsize=S.FONT, va="center", linespacing=1.15)
    return fig


def j1_recall_needs_lens(plt):
    """Per model, recalled vs stated answers lost under each tool; the larger control as a grey tick on recalled answers;
    hollow = after the data; 'not run' where a tool was not run."""
    zb, dp = breadth(), depth()
    fig = plt.figure(figsize=(S.WIDTH, 5.0))
    axes = (fig.add_axes((0.215, 0.27, 0.35, 0.50)), fig.add_axes((0.625, 0.27, 0.35, 0.50)))
    S.title(fig, "Recalled answers need the lens part; stated answers do not",
            "The two tools count losses differently: left, answers lost; right, switches lost beyond\n"
            "a random part. Grey tick: the largest control, on recalled answers.")  # fmt: skip
    ys = {name: -i for i, (name, *_) in enumerate(MODELS)}
    for ax, panel in zip(axes, ("everywhere", "change"), strict=True):
        for name, zm, target, m in MODELS:
            y = ys[name]
            if panel == "everywhere":
                rc, st = zb[(zm, f"ko.{zm}.lostM")], zb[(zm, f"ko.{zm}.lostK")]
                kind = "after" if zm in G.AFTER_V2_KNOCKOUT else "fixed"
                cname, cv, cpath = ko_control(rc)
                pts = (num(rc["value"]), num(st["value"]))
                src = (f"docs/breadth/data.csv | ko.{zm}.lostM", f"docs/breadth/data.csv | ko.{zm}.lostK")
                record("j1", name, "remove everywhere: recalled answers lost (points)", pts[0], source=src[0])
                record("j1", name, "remove everywhere: stated answers lost (points)", pts[1], source=src[1])
                record("j1", name, f"remove everywhere, largest control ({cname}): recalled answers lost (points)", cv,
                       source=f"{cpath} | facts {'paper10_rot' if cname == 'rotated' else 'unembed10'}/start=all loss M")  # fmt: skip
            else:
                if target is None:
                    ax.text(45, y, "not run", ha="center", va="center", fontsize=S.FONT, color=S.COL["muted"])
                    record(
                        "j1",
                        name,
                        "remove from the change",
                        "not run",
                        source="docs/shared/grid.csv | depth column '-'",
                    )
                    continue
                q = "main test (two people swap picks): {} extra loss"
                rc, st = dp[("fig01", target, q.format("recall"))], dp[("fig01", target, q.format("lookup"))]
                kind = "fixed"  # our main test, fixed in advance on all four (figures/story/scorecard.csv 'main test')
                cv = num(dp[("numbers", "", f"rc_droprand_{m}")]["value"])
                pts = (100 * num(rc["value"]), 100 * num(st["value"]))
                for label, r, v in (("recalled", rc, pts[0]), ("stated", st, pts[1])):
                    record("j1", name, f"remove from the change: {label} answers' extra loss (x 100)", round(v, 1),
                           round(100 * num(r["lo"]), 1), round(100 * num(r["hi"]), 1),
                           source=f"figures/story/data.csv | fig01 | {r['quantity']}")  # fmt: skip
                record("j1", name, "remove from the change, control (a random part): recalled switches lost (%)", cv,
                       source=f"figures/story/data.csv | numbers | rc_droprand_{m}")  # fmt: skip
            ax.plot(pts, [y, y], color="#bbbbbb", lw=2.2, zorder=1, solid_capstyle="butt")
            ax.plot([cv], [y], marker="|", ms=15, mew=2.6, color=S.COL["control"], ls="", zorder=2)
            for v, col in zip(pts, (RECALLED, STATED), strict=True):
                ax.plot([v], [y], "o", ms=8, mfc=col if kind == "fixed" else "white", mec=col, mew=1.8, zorder=3)
        ax.set_xlim(-15, 100)
        ax.set_ylim(-len(MODELS) + 0.4, 0.6)
        ax.axvline(0, color="#999999", lw=0.8, zorder=0)
        ax.set_xticks([0, 50, 100])
        ax.set_yticks([ys[n] for n, *_ in MODELS], [n for n, *_ in MODELS] if panel == "everywhere" else [])
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[0].set_title("remove everywhere (Zach)", fontsize=S.FONT + 1, loc="left")
    axes[1].set_title("remove from the change (Dan)", fontsize=S.FONT + 1, loc="left")
    axes[0].set_xlabel("answers lost (points)")
    axes[1].set_xlabel("switches lost beyond a random part (× 100)")
    hs = [plt.Line2D([], [], marker="o", ls="", color=RECALLED, ms=8), plt.Line2D([], [], marker="o", ls="", color=STATED, ms=8),
          plt.Line2D([], [], marker="|", ls="", color=S.COL["control"], ms=13, mew=2.6)]  # fmt: skip
    sh, sl = S.status_handles(("fixed", "after"))
    legend_below(fig, hs + sh, ["recalled answer", "stated answer", "largest control", *sl], 0.0, 3)
    return fig


def j2_swap(plt):
    """Per model, a 2 x 2: which part is swapped (rows) x which answer moves (columns), transfer in points with its 95%
    interval; the swap of everything else is after the data and awaits Zach's confirmation."""
    zb = breadth()
    fig = plt.figure(figsize=(S.WIDTH, 6.0))
    S.title(fig, "Swapping the lens part moves the recalled answer, not the stated one",
            "Transfer: answers that move to the other entity's, minus a third entity's (points).\n"
            "Zach's swaps, written in at the bridge over his band of layers.")  # fmt: skip
    rows = ("swap the lens part", "swap everything else")
    cols = (("recalled answer moves", RECALLED), ("stated answer moves", STATED))
    tops = (0.53, 0.24)
    for (name, zm, *_), top in zip([MODELS[0], MODELS[1]], tops, strict=True):
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
        tk = summ["TK/swap_comp"]
        record("j2", name, "swap everything else: stated answer moves, bridge tracked (points)", tk["transfer"], tk["ci"][0],
               tk["ci"][1], tk["n"], source=f"results/jswap/{run}/summary.json | TK/swap_comp")  # fmt: skip
        for c, (ctitle, col) in enumerate(cols):
            ax = fig.add_axes((0.355 + 0.33 * c, top, 0.29, 0.19))
            for i in range(2):
                v, lo, hi, n, src, kind = cells[(i, c)]
                bar(ax, -i, v, lo, hi, col, kind)
                ax.text(max(v, num(hi)) + 3, -i, f"{v:+.1f}", va="center", fontsize=S.FONT, color=col)
                record("j2", name, f"{rows[i]}: {ctitle} (points)", v, lo, hi, n, source=src)
            ax.set_xlim(-5, 100)
            ax.set_ylim(-1.6, 0.6)
            ax.axvline(0, color="#999999", lw=0.8)
            ax.set_xticks([0, 50, 100])
            ax.tick_params(axis="y", length=0)
            ax.spines["left"].set_visible(False)
            labels = ["swap the lens part", "swap everything else\n(awaiting Zach's\nconfirmation)"]
            ax.set_yticks([0, -1], labels if c == 0 else [])
            if top == tops[0]:
                ax.set_title(ctitle, fontsize=S.FONT + 1, color=col, loc="left")
            if top == tops[-1]:
                ax.set_xlabel("points")
            else:
                ax.set_xticklabels([])
        fig.text(0.01, top + 0.215, name, fontsize=S.FONT + 1, weight="bold", va="bottom")
    tk27, tk9 = (json.loads((REPO / "results" / "jswap" / SWAP_RUNS[m] / "summary.json").read_text())["TK/swap_comp"]["transfer"]
                 for m in ("q27", "q9"))  # fmt: skip
    fig.text(0.01, 0.015, "Stated answers: the bridge read from the passage. With the bridge tracked instead, everything else\n"
             f"moves the stated answer {tk27:+.1f} (Qwen 27B) and {tk9:+.1f} (Qwen 9B). Hollow: after the data.",
             fontsize=S.FONT, color=S.COL["muted"], va="bottom")  # fmt: skip
    return fig


def j3_order_signal(plt):
    """Qwen 9B and Muse 30B, scenes where another item moved: answers by the locker's position with the whole change,
    without the order signal and without a random part of its size; beside it, writes of the order signal at about a
    real change's size against a random vector."""
    dp = depth()
    card = {(r["claim"], r["model"]): r["flag"] for r in read_csv(G.SCORECARD)}
    fig = plt.figure(figsize=(S.WIDTH, 4.9))
    S.title(fig, "The stated answer uses an order signal the lens does not read",
            "Dan's scenes where another item moved. Left: stated answers that follow the locker's\n"
            "position. Right: writes of the order signal that send it to the target locker.")  # fmt: skip
    pair = [MODELS[0], MODELS[3]]
    axl, axr = fig.add_axes((0.17, 0.30, 0.40, 0.48)), fig.add_axes((0.70, 0.30, 0.27, 0.48))
    arms = (("whole", "whole change", S.COL["position"]), ("no_alf", "without the order signal", "#f4c48a"),
            ("no_alf_rand", "without a random part (same size)", S.COL["control"]))  # fmt: skip
    for g, (name, _, target, _m) in enumerate(pair):
        scard = {"Qwen 9B": "Qwen3.5-9B", "Muse 30B": "Muse Glimmer 30B"}[name]
        kind = "after" if "a" in card[("the lookup needs it", scard)] else "fixed"
        for k, (arm, label, col) in enumerate(arms):
            r = dp[("fig05", target, f"another item moved, {arm}: position share")]
            y = -g * 4.2 - k
            bar(axl, y, num(r["value"]), r["lo"], r["hi"], col, kind, h=0.8)
            axl.text(num(r["hi"]) + 0.02, y, f"{num(r['value']):.2f}", va="center", fontsize=S.FONT)
            record("j3", name, f"answers by position: {label} (share)", round(num(r["value"]), 3), round(num(r["lo"]), 3),
                   round(num(r["hi"]), 3), r["n"], source=f"figures/story/data.csv | fig05 | {r['quantity']}")  # fmt: skip
        kind_w = "after" if "a" in card[("a write moves the lookup", scard)] else "fixed"
        w = dp[("fig07", target, "lookup target share, mean over locker pairs, s = 2")]
        dose = dp[("fig07", target, "dose (s / mean s*), s = 2")]
        rnd = dp[("fig07", target, "lookup target share, random direction, s = 4")]
        rdose = dp[("fig07", target, "dose (s / mean s*), s = 4")]
        for k, (r, col) in enumerate(((w, S.COL["position"]), (rnd, S.COL["control"]))):
            y = -g * 2.6 - k
            bar(axr, y, num(r["value"]), r["lo"], r["hi"], col, kind_w, h=0.8)
            axr.text(
                max(num(r["value"]), num(r["hi"] or 0)) + 0.02,
                y,
                f"{num(r['value']):.2f}",
                va="center",
                fontsize=S.FONT,
            )
        record("j3", name, "writes sending the stated answer to the target locker: order signal (share)", num(w["value"]),
               source=f"figures/story/data.csv | fig07 | {w['quantity']}")  # fmt: skip
        record("j3", name, "the order signal's write dose (x a real change's size)", round(num(dose["value"]), 2),
               source=f"figures/story/data.csv | fig07 | {dose['quantity']}")  # fmt: skip
        record("j3", name, "writes sending the stated answer to the target locker: random vector (share)", num(rnd["value"]),
               rnd["lo"], rnd["hi"], source=f"figures/story/data.csv | fig07 | {rnd['quantity']}")  # fmt: skip
        record("j3", name, "the random vector's dose (x a real change's size)", round(num(rdose["value"]), 2),
               source=f"figures/story/data.csv | fig07 | {rdose['quantity']}")  # fmt: skip
    axl.set_yticks([-g * 4.2 - 1 for g in range(2)], [n for n, *_ in pair])
    axr.set_yticks([-g * 2.6 - 0.5 for g in range(2)], [n for n, *_ in pair])
    for ax, lim in ((axl, (-7.9, 0.7)), (axr, (-4.3, 0.7))):
        ax.set_xlim(0, 1)
        ax.set_ylim(*lim)
        ax.set_xticks([0, 0.5, 1])
        ax.set_xticklabels(["0", "0.5", "1"])
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axl.set_xlabel("share of stated answers")
    axr.set_xlabel("share of writes")
    hs = [Rectangle((0, 0), 1, 1, fc=c, ec=c) for _, _, c in arms]
    hs += [
        Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["position"], lw=1.6),
        Rectangle((0, 0), 1, 1, fc="white", ec=S.COL["control"], lw=1.6),
    ]
    labels = [label for _, label, _ in arms] + [
        "order signal written,\nabout a real change's size",
        "random vector,\nabout twice that size",
    ]
    sh, sl = S.status_handles(("fixed", "after"))
    legend_below(fig, hs + sh, labels + sl, 0.0, 3)
    return fig


# the README's findings: (label, grid rows as (study, grid claim)); finding 4 is derived from rows below it
FINDINGS = (
    ("recalled answers need the lens part; stated ones do not", (("depth", G.RECALL), ("breadth", G.RECALL))),
    ("swapping the lens part moves the recalled answer, not the stated one",
     (("breadth", "another entity's J++ part moves the answer (≥ 20 points)"),)),
    ("the stated answer uses an order signal outside the lens", (("depth", "the lookup needs it"),)),
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
    """The README's four findings x five models in Fig. 11's symbols; finding 1 split (Dan | Zach)."""
    cells = front_cells()
    fig = plt.figure(figsize=(S.WIDTH, 5.3))
    ax = fig.add_axes((0.40, 0.25, 0.59, 0.45))
    S.title(fig, "The methods agree on the Qwen 9B and split on Muse 30B and Qwen 122B",
            "✓ held   ~ partial   ✗ no   – not tested   a: after the data\n"
            "Row 1: two marks per cell, Dan's tool (left) and Zach's (right).")  # fmt: skip
    names = [n for n, *_ in MODELS]
    for j, name in enumerate(names):
        ax.text(j, -0.6, name.replace("Nemotron ", "Nemotron\n"), ha="center", va="bottom", fontsize=S.FONT, weight="bold",
                linespacing=1.0)  # fmt: skip
        for i in range(len(FINDINGS)):
            marks = cells[(i, name)]
            xs = (j,) if len(marks) == 1 else (j - 0.2, j + 0.16)
            size = S.FONT + 5 if len(marks) == 1 else S.FONT + 3
            if len(marks) == 2:
                ax.plot([j - 0.02, j - 0.02], [i - 0.32, i + 0.32], color="#c8c8c8", lw=0.9)
            for x, r in zip(xs, marks, strict=True):
                sym, col = F.CELL_SYMBOL[r["cell"]]
                ax.text(x, i, sym, ha="center", va="center", fontsize=size, color=col, weight="bold")
                if r["flag"]:
                    ax.annotate(r["flag"], (x, i), xytext=(size * 0.42 + 3, 3), textcoords="offset points", ha="left",
                                va="center", fontsize=S.FONT, color=S.COL["muted"])  # fmt: skip
                record("grid_front", name, f"finding {i + 1} ({r['study']})", r["cell"] + (f" {r['flag']}" if r["flag"] else ""),
                       source=f"docs/shared/grid.csv | {r['claim']}" if r["claim"] != "derived" else
                       "derived (joint_figures.agree) from docs/shared/grid.csv: both studies' recall rows and breadth's 'specific' row")  # fmt: skip
    for i in range(0, len(FINDINGS), 2):
        ax.axhspan(i - 0.5, i + 0.5, color="#f6f6f6", lw=0, zorder=0)
    ax.set_xlim(-0.5, len(names) - 0.5)
    ax.set_ylim(len(FINDINGS) - 0.5, -0.5)
    ax.set_yticks(
        range(len(FINDINGS)), [textwrap.fill(f"{i + 1}. {label}", 34) for i, (label, _) in enumerate(FINDINGS)]
    )
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    fig.text(0.01, 0.015, textwrap.fill(
        "From docs/shared/grid.csv: 1 both tools' recall rows; 2 Zach's swap row; 3 Dan's removal of the order signal; "
        "4 row 1's two grades match and remove everywhere passes its rotated and logit-lens control. Nemotron Lightning's "
        "swap is not counted in the README: pasting the whole residual moves only +13.8, below 20.", 100),
        fontsize=S.FONT, color=S.COL["muted"], va="bottom")  # fmt: skip
    return fig


FIGURES = (("j0_setup", j0_setup), ("j1_recall_needs_lens", j1_recall_needs_lens), ("j2_swap", j2_swap),
           ("j3_order_signal", j3_order_signal), ("grid_front", grid_front))  # fmt: skip


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
