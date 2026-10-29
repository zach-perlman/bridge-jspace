"""README figures from Dan's figures brief (28 Oct ~18:30), drawn in its one mark system (story_style.MARK_COL / MARK):
colour = who or what, mark = the operation, one panel per model in the order 9B, 27B, Muse; omitted cells are listed in
one caption line under the plot, never drawn as text inside a frame. Every plotted number is recorded for
figures/story/data.csv with its source file.

  fig00b_marks       the mark legend, under Fig. 0
  fig01d_ladder      49.2's removal ladder (x49_2-<UTC>/x49_2.json): E2's figure, replacing fig01c
  fig12_two_by_two   our operation / Zach's x our scenes / his passages: our main-test gap (docs/x0_numbers.json),
                     49.2's rung 6, Z1's gap and his stored M - K rows (x50_zach/z1-<UTC>/z1.json)

The Muse's rung 6 ran at L23-29, not in Zach's band (L36-42): drawn hollow until its rerun lands; likewise the Z1 cell
(our operation on his passages) until it reruns with the P final. Both are said in the caption lines.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

from matplotlib import patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_style as S

MODELS = tuple((t, m, name) for t, m, name in S.MODELS if m != "122b")  # 9B, 27B, Muse
SHORT = {"9b": "9B", "27b": "27B", "muse": "Muse", "lightning": "Lightning"}
INK, LOOKUP, NULL = S.MARK_COL["recall"], S.MARK_COL["lookup"], S.MARK_COL["null"]
RECALL_AFTER = "#9a9a9a"  # the recall's lighter shade (locker after the pick): a grey, so no new hue
CAPTION = "#555555"
CAPTION_CHARS = 110  # caption characters per line at 10 pt in the 8.8 in column
MUSE_BAND = "Muse's rung 6 ran at L23–29; his band is L36–42, where it was not run"
MUSE_DAGGER = "† Muse's rung 6 ran at L23–29, outside his band (L36–42)"  # the one caption line (Dan, 21:55)
ZACH_MUSE_BAND = list(range(36, 43))  # Muse's rerun (r3, muse30_x52_ladder) ran rung 6 here: no dagger then


def muse_outside_band(ladder: dict) -> bool:
    """True when the ladder verdict's Muse rung 6 ran outside Zach's band (the first run), so the dagger is drawn."""
    m = next((x for x in ladder["models"] if x["target"] == "muse-glimmer-30b"), None)
    return m is not None and m.get("band") != ZACH_MUSE_BAND


# the ladder's rungs in words, two lines each: where, then what is added (49.2's rung_text; Dan's round 3, 28 Oct
# 21:10; rungs 5 and 6 are two definitions, not one). Dan (21:55): each rung's full meaning is in the README's Setup,
# so the ticks stay short and leave room for the end labels
RUNGS = {1: "bridge word\none layer", 2: "bridge word\nL to L+3", 3: "+ earlier\nmention",
         4: "+ the\nquestion", 5: "every token\nL to L+3", 6: "Zach's lens\ndirections"}  # fmt: skip
# the rungs' x: rung 6 (Zach's definition) set a little apart, which also gives its longer label room
RUNG_X = {1: 1.0, 2: 2.0, 3: 3.0, 4: 4.0, 5: 5.0, 6: 6.25}
VALID_SWITCHES = F.VALID_SWITCHES  # a lookup extra loss is drawn only on at least 30 switches (X0's validity bar)


def rel(path: Path) -> str:
    return str(path.relative_to(S.REPO))


def caption_lines(lines: list[str]) -> list[str]:
    return [w for line in lines if line for w in textwrap.wrap(line, CAPTION_CHARS)]


def caption(fig, lines: list[str], y_in: float) -> None:
    """The figure's caption lines (omitted cells, hollow marks) under the plot, y_in inches from the bottom."""
    fig.text(0.01, y_in / fig.get_figheight(), "\n".join(caption_lines(lines)), ha="left", va="top",
             fontsize=S.FONT - 1, color=CAPTION, linespacing=1.25)  # fmt: skip


def model_label(ax, m: str, name: str, first: bool) -> None:
    ax.text(0.0, 1.03, name if first else SHORT[m], transform=ax.transAxes, ha="left", va="bottom", fontsize=12,
            weight="bold")  # fmt: skip


def mark(ax, x: float, v: tuple, col: str, op: str, hollow: bool = False, ms: float = 8.0, whisker: bool = True):
    """One estimate in the mark system: the operation's mark in the reader's colour, its 95% whisker; hollow = white
    face."""
    if whisker and v[1] is not None and v[2] is not None:
        ax.plot([x, x], [v[1], v[2]], color=col, lw=1.5, zorder=3, solid_capstyle="butt")
    ax.plot([x], [v[0]], S.MARK[op], color=col, ms=ms, mfc="white" if hollow else col, mec=col, mew=1.6, zorder=4)


# ---- fig00b: the mark legend ---------------------------------------------------------------------------------------


def build_marks(out_name: str = "fig00b_marks") -> str:
    """Fig. 0b: the colours (who or what) and the marks (the operation) once, so later legends name only the arms."""
    plt = S.setup()
    body_in = 1.6  # four lines of 0.4 in
    h = 0.78 + body_in
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, "How to read the figures: colour is who, the mark is what was done",
            "Panels: one per model, always 9B, 27B, Muse. Whiskers and bands: 95% intervals.")  # fmt: skip
    ax = fig.add_axes((0.0, 0.0, 1.0, body_in / h))
    ax.set_xlim(0, S.WIDTH)  # x and y in inches
    ax.set_ylim(0, body_in)
    ax.axis("off")
    r = fig.canvas.get_renderer()
    line = {"y": body_in - 0.25}

    def row(head: str, items) -> None:
        """A heading and its entries, wrapped to a new line where the next entry would pass the right edge."""
        y = line["y"]
        ax.text(0.09, y, head, fontsize=S.FONT, weight="bold", va="center")
        x = 0.95
        for draw, label in items:
            t = ax.text(x + 0.17, y, label, fontsize=S.FONT, va="center")
            w = t.get_window_extent(r).width / fig.dpi
            if x + 0.17 + w > S.WIDTH - 0.08:
                y -= 0.38
                x = 0.95
                t.set_position((x + 0.17, y))
            draw(x, y)
            x += 0.17 + w + 0.30
        line["y"] = y - 0.42

    def dot(col):
        return lambda x, y: ax.plot([x], [y], "o", ms=9, color=col)

    def band(x, y):
        ax.add_patch(plt.Rectangle((x - 0.12, y - 0.09), 0.24, 0.18, fc=NULL, ec="none", alpha=0.6))

    row("colour", [(dot(S.MARK_COL[k]) if k != "null" else band, S.MARK_COL_TEXT[k]) for k in S.MARK_COL])
    row("mark", [(lambda x, y, o=op: ax.plot([x], [y], S.MARK[o], ms=9, color="#555555"), S.MARK_TEXT[op])
                      for op in ("remove", "zero", "add", "swap", "whole")])  # fmt: skip
    S.save(fig, out_name)
    return out_name


# ---- fig01d: the removal ladder ------------------------------------------------------------------------------------


LADDER_BARS = (("recall", "locker-first", INK, -0.27, "recall, locker before the pick"),
               ("recall", "locker-after", RECALL_AFTER, -0.01, "recall, locker after the pick"),
               ("lookup", "all", LOOKUP, 0.27, "lookup, every scene"))  # fmt: skip
LADDER_BAR_W = 0.25
# Lightning's ladder below its gate (exploratory, Dan's morning queue, 29 Oct; rung 6 in Zach's band L27-33), drawn as
# a fourth panel, hollow; and the clean one-pick gate it fails (the recall's read accuracy on the original prompts)
LT_LADDER_BELOW = S.REPO / "results" / "x49_ladder" / "x52_ladder_below-20261029T091146Z"
LT_CLEAN_GATE = S.REPO / "results" / "x0_necessity" / "nem35l_x45s_smoke_clean" / "gate.json"


def build_ladder(verdict_dir: Path, out_name: str = "fig01d_ladder", lightning: bool = False) -> str:
    """Fig. 1d (E2), Dan's round 3 (28 Oct 21:10): one panel per model, one column per rung (49.2's six rungs; a run
    without some rungs has those columns greyed), each column the recall's bars (locker before the pick, dark; after
    it, a lighter shade) and the lookup's (every scene, purple): the answers lost beyond a random part of the same
    share (pp) when the J++ part's directions are taken out of the changed prompt's own state, with 95% whiskers; on
    each bar a grey tick at what the random part itself costs that bar's group (kept with none minus kept with the
    random part). Rung 6 (Zach's definition) stands apart from rungs 1-5 (ours); Muse's rung 6 is marked (†) and its
    band said in the caption while it ran outside his band. lightning: a fourth panel from LT_LADDER_BELOW (below its
    gate: white-faced bars with coloured edges, its n tag ○, a caption line), or, without that file, a row under the
    rung labels saying Lightning was not tested (its gate)."""
    src_path = verdict_dir / "x49_2.json"
    v = json.loads(src_path.read_text())
    src, fid = rel(src_path), out_name.split("_")[0]
    by = {m["target"]: m for m in v["models"] if m.get("status") == "tested"}
    srcs = dict.fromkeys(by, src)
    panels = list(MODELS)
    lt_below = lightning and (LT_LADDER_BELOW / "x49_2.json").exists()
    if lt_below:
        p = LT_LADDER_BELOW / "x49_2.json"
        for m in json.loads(p.read_text())["models"]:
            if m.get("status") == "tested" and m["target"] == F.LT[0]:
                by[m["target"]], srcs[m["target"]] = m, rel(p)
        panels.append((F.LT[0], F.LT[1], F.LT[2]))
    lt_row = lightning and not lt_below  # the text row under the rung labels
    plt = S.setup()
    n_p = len(panels)
    panel_in, gap_in, top_in, bottom_in = 1.5, 0.42, 1.75, 1.05 + 0.45 * lt_row + 0.4 * lt_below
    h = top_in + n_p * panel_in + (n_p - 1) * gap_in + bottom_in
    fig, axes = plt.subplots(n_p, 1, figsize=(S.WIDTH, h), sharex=True)
    fig.subplots_adjust(left=0.08, right=0.99, top=1 - top_in / h, bottom=bottom_in / h, hspace=gap_in / panel_in)
    S.title(fig, "Recall needs the J++ part once its other copies go; the lookup never",
            "The J++ part taken out of the changed prompt, rung by rung; answers lost beyond a random part")  # fmt: skip
    omitted, greyed = [], []
    for k, (ax, (target, m, name)) in enumerate(zip(axes, panels, strict=True)):
        mod = by.get(target)
        hollow = m == "lightning"
        src = srcs.get(target, src)
        if hollow:  # below its gate: the panel says so beside the model's name
            ax.text(0.0, 1.03, f"{SHORT[m]}  {S.STATUS_GLYPH['after']} below gate", transform=ax.transAxes, ha="left",
                    va="bottom", fontsize=12, weight="bold")  # fmt: skip
        else:
            model_label(ax, m, name, k == 0)
        ax.axhline(0, color="#999999", lw=0.8, zorder=1)
        ax.axhline(10, color="#555555", lw=1.0, ls=(0, (4, 3)), zorder=1)
        ax.text(0.6, 10.5, "10 pp", ha="left", va="bottom", fontsize=S.FONT - 1, color="#555555")
        ax.axvline((RUNG_X[5] + RUNG_X[6]) / 2, color="#cccccc", lw=1.0, zorder=0)
        ax.set_ylim(-10, 58)
        ax.set_yticks([0, 20, 40])
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)
        rungs = mod["rungs"] if mod else []
        # a rung not run: its column greyed, no text in the frame (the caption says it)
        for r in (r for r in RUNGS if r not in rungs):
            ax.axvspan(RUNG_X[r] - 0.45, RUNG_X[r] + 0.45, color=S.COL["band"], lw=0, zorder=0)
        if mod is None:
            omitted.append(f"{SHORT[m]} (every rung)")
            continue
        if len(rungs) < 6:
            greyed.append(f"{SHORT[m]} rungs {len(rungs) + 1}–6")
        for reader, group, col, dx, label in LADDER_BARS:
            cell = mod["cells"][reader][group]
            for r in rungs:
                c = cell["cost"][str(r)]
                S.record(fid, target, f"rung {r}: {label}: answers lost beyond random", *[round(x, 4) for x in c],
                         n=cell["n"], source=src)  # fmt: skip
                own = cell["kept"]["none"][0] - cell["kept"][f"rand{r}"][0]
                S.record(fid, target, f"rung {r}: {label}: the random part's own cost (kept with none minus kept with "
                         "the random part)", round(own, 4), n=cell["n"], source=src)  # fmt: skip
                x = RUNG_X[r] + dx
                face = {"facecolor": "white", "edgecolor": col, "lw": 1.4} if hollow else {"color": col, "lw": 0}
                ax.bar(x, 100 * c[0], width=LADDER_BAR_W, zorder=2, **face)
                ax.plot([x, x], [100 * c[1], 100 * c[2]], color="#1e1e1e", lw=1.1, zorder=3, solid_capstyle="butt")
                ax.plot([x - LADDER_BAR_W * 0.55, x + LADDER_BAR_W * 0.55], [100 * own] * 2, color=NULL, lw=2.4,
                        zorder=4, solid_capstyle="butt", path_effects=[pe.withStroke(linewidth=3.6, foreground="white")])  # fmt: skip
        if m == "muse" and 6 in rungs and muse_outside_band(v):  # rung 6 outside Zach's band on Muse (the dagger)
            top = max(100 * mod["cells"][w][g]["cost"]["6"][2] for w, g, *_ in LADDER_BARS)
            # above its bars' whiskers and clear of the 10 pp line
            ax.text(RUNG_X[6], max(top, 10) + 4, "†", ha="center", va="bottom", fontsize=S.FONT + 1, color="#1e1e1e")
        # Dan (21:50): every panel names its bars, beside the last rung it ran (the random tick: the lookup bar's)
        last = max(rungs)
        ends = [(100 * mod["cells"][w][g]["cost"][str(last)][0], short, col)
                for (w, g, col, _, _), short in zip(LADDER_BARS, ("recall, before", "recall, after", "lookup"),
                                                    strict=True)]  # fmt: skip
        lk = mod["cells"]["lookup"]["all"]["kept"]
        ends.append((100 * (lk["none"][0] - lk[f"rand{last}"][0]), "random (tick)", S.COL["muted"]))
        S.end_labels(ax, RUNG_X[last] + LADDER_BARS[-1][3] + LADDER_BAR_W / 2, ends, pad=0.08)
        S.panel_tag(ax, str(mod["cells"]["recall"]["all"]["n"]), "after" if hollow else "fixed")
    axes[1].set_ylabel("answers lost beyond random (pp)")
    if n_p == 4:  # the axis label between the middle two panels
        axes[1].yaxis.set_label_coords(-0.06, -gap_in / panel_in / 2)
    axes[-1].set_xlim(0.58, RUNG_X[6] + 1.75)  # the end labels' room right of rung 6
    # half a point under the figures' 11 pt: six two-line labels across the column otherwise touch
    axes[-1].set_xticks(list(RUNG_X.values()), list(RUNGS.values()), fontsize=S.FONT - 0.5)
    hs = [Patch(fc=col, ec="none") for *_, col, _, _ in LADDER_BARS]
    hs.append(Line2D([], [], color=NULL, lw=2.4, solid_capstyle="butt"))
    fig.legend(hs, [b[4] for b in LADDER_BARS] + ["tick: what a random part (same size) costs that bar"],
               loc="upper left", bbox_to_anchor=(0.0, 1 - 0.74 / h), frameon=False, ncol=2, handlelength=1.6,
               columnspacing=1.6)  # fmt: skip
    # Dan (21:55): one caption line; L to L+3 and the rungs' meanings are in the README's Setup
    line = (
        MUSE_DAGGER + "." if muse_outside_band(v) else "Each model's full run; Muse's rung 6 inside his band (L36–42)."
    )
    line += f" Grey columns: not run ({'; '.join(greyed)})." if greyed else ""
    line += f" Omitted: {'; '.join(omitted)}." if omitted else ""
    lines = [line]
    if lt_below:
        gate = json.loads(LT_CLEAN_GATE.read_text())["gate"]["chat"]["org_accuracy"]["PM"]
        band = by[F.LT[0]].get("band") or []
        lines.append(f"Lightning hollow: below gate (its clean one-pick recall {gate:.3f} < 0.80), descriptive only"
                     + (f"; rung 6 in his band (L{band[0]}–{band[-1]})." if band else ".") + " " + F.LT_NOTE)  # fmt: skip
    if lt_row:  # no rung ran on Lightning: one row, its name and why, under the rung labels
        y = (bottom_in - 0.72) / h
        fig.text(0.01, y, F.LT[2], ha="left", va="top", fontsize=12, weight="bold")
        fig.text(0.5, y, F.LT_GATE, ha="center", va="top", color=S.COL["muted"])
    caption(fig, lines, bottom_in - 0.75 - 0.45 * lt_row)
    S.save(fig, out_name)
    return out_name


# ---- fig12: the 2 x 2 ----------------------------------------------------------------------------------------------


def n_tag(ax, text: str, after: str = "") -> None:
    """story_style.panel_tag's look ("n = ..." and the status glyph), in the cell's bottom right under the zero line;
    after: an n drawn after the data (Lightning's), with the open glyph."""
    tail = f";  {after}  {S.STATUS_GLYPH['after']}" if after else ""
    ax.text(0.995, 0.03, f"n = {text}  {S.STATUS_GLYPH['fixed']}{tail}", transform=ax.transAxes, ha="right",
            va="bottom", fontsize=S.FONT - 1, color=S.COL["muted"], zorder=8)  # fmt: skip


def main_random_gap(target: str, m: str) -> tuple[float, str]:
    """The main test's control for the 2 x 2's first cell: a random part of the J++ part's share taken out instead,
    the recall's switches lost minus the lookup's (each reader's dependence on the random part at L, the point estimate
    x0_figures.contrast subtracts), from the run's outcomes; checked against docs/x0_numbers.json's rounded rc_rdep /
    lk_rdep. Returns (value, source)."""
    run, la = F.MAIN_RUNS[m], F.X.PREDICTED[target]
    path = F.X.RESULTS / run / "outcomes.jsonl"
    rows = [r for r in F.X.read_jsonl(path) if r["rendering"] == "chat" and r["layer"] == la]
    rdep = {}
    for w in F.X.READERS:
        mine = [r for r in rows if r["reader"] == w]
        whole = [r["switched"] for r in mine if r["arm"] == "whole"]
        rand = [r["switched"] for r in mine if r["arm"] == "no_rand" and (r["dict"], r["k"], r["omp"]) == F.X.MAIN]
        assert whole, (target, w)
        assert len(rand) == len(whole), (target, w, len(whole), len(rand))
        rdep[w] = float(F.X.dependence(sum(whole) / len(whole), sum(rand) / len(rand)))
    for w, key in ((F.X.RECALL, "rc"), (F.X.LOOKUP, "lk")):
        stored = float(F.N[f"{key}_rdep_{m}"].replace("−", "-"))
        assert abs(rdep[w] - stored) <= 0.005 + 1e-9, (target, key, rdep[w], stored)
    return rdep[F.X.RECALL] - rdep[F.X.LOOKUP], str(path.relative_to(S.REPO))


def lightning_main_gap() -> tuple[tuple, float, int, str, str]:
    """Lightning's main-test cell: the gap of its split by sentence order (all rows; Fig. 1's), the control (each
    reader's dependence on the random part at L14, recall minus lookup) from its conflict verdict, n, both sources."""
    c = json.loads(F.LT_SPLIT.read_text())["cells"][f"{F.LT[0]}|swap"]["cells"]["all"]
    v = json.loads(F.LT_CONFLICT.read_text())
    rdep = {x["reader"]: x["Rdep"][0] for x in v["cells"]
            if x["layer"] == F.LT_L and (x["dict"], x["k"], x["omp"]) == F.X.MAIN}  # fmt: skip
    return tuple(c["gap"]), rdep[F.X.RECALL] - rdep[F.X.LOOKUP], c["n"], rel(F.LT_SPLIT), rel(F.LT_CONFLICT)


def build_two_by_two(
    ladder_dir: Path, z1_dir: Path, out_name: str = "fig12_two_by_two", lightning: bool = False
) -> str:
    """Fig. 12: recall minus lookup in four cells, our operation / Zach's x our scenes / his passages, one mark for
    every cell and one scale (Dan's round 3, 28 Oct 21:10): our main-test gap (docs/x0_numbers.json, Fig. 1's); rung 6
    of the ladder on our clean scenes (recall's cost minus the lookup's, every scene; two separate estimates, so no
    joint interval); Z1's gap on his passages (a lookup with fewer than 30 switches is omitted); his stored M - K rows
    on the same passage ids. In every cell a grey tick: the same operation with a random part of the same size (his:
    his rotated directions), recall minus lookup. The units differ by row (said in the subtitle and the row labels).
    lightning: Lightning the fourth column, hollow, from its coverage folders (readme_story_figures.LT_*); the ladder
    did not run on it (its gate), so its (1, 0) cell is empty."""
    lad_path, z1_path = ladder_dir / "x49_2.json", z1_dir / "z1.json"
    lad_v = json.loads(lad_path.read_text())
    lad = {m["target"]: m for m in lad_v["models"] if m.get("status") == "tested"}
    dagger = muse_outside_band(lad_v)
    z1 = {m["target"]: m for m in json.loads(z1_path.read_text())["models"] if m.get("status") == "tested"}
    z1_src = dict.fromkeys(z1, rel(z1_path))
    columns = MODELS
    if lightning:
        z1 |= {m["target"]: m for m in json.loads(F.LT_Z1.read_text())["models"]
               if m.get("status") == "tested" and m["target"] == F.LT[0]}  # fmt: skip
        z1_src[F.LT[0]] = rel(F.LT_Z1)
        columns = (*MODELS, F.LT)
    fid = out_name.split("_")[0]
    omitted = []
    cells: dict[tuple[int, int], list] = {(0, 0): [], (0, 1): [], (1, 0): [], (1, 1): []}  # (i, v, control)
    ns: dict[tuple[int, int], list[str]] = {k: [] for k in cells}
    lt_n: dict[tuple[int, int], str] = {}
    control = "the control (a random part of the same size instead), recall minus lookup"
    for i, (target, m, _) in enumerate(columns):
        lt = m == "lightning"
        # (0, 0) our removal on our scenes: the main test's gap (Fig. 1)
        if lt:
            v, ctl, n0, gsrc, src = lightning_main_gap()
            v = tuple(round(x, 4) for x in v)
            S.record(fid, target, "our removal, our scenes (main test): gap", *v, n=n0, source=gsrc)
            S.record(fid, target, f"our removal, our scenes (main test): {control}", round(ctl, 4), n=n0, source=src)
            lt_n[(0, 0)] = str(n0)
        else:
            v = F.interval(f"contrast_{m}")
            S.record(fid, target, "our removal, our scenes (main test): gap", *v, n=200, source=f"contrast_{m}")
            ctl, src = main_random_gap(target, m)
            S.record(fid, target, f"our removal, our scenes (main test): {control}", round(ctl, 4), n=200, source=src)
            ns[(0, 0)].append("200")
        cells[(0, 0)].append((i, v, ctl))
        # (0, 1) our removal on his passages: Z1's gap at our layer
        mod = z1.get(target)
        lr = mod["layer_results"][str(mod["layers"][0])] if mod else None
        if lr is None:
            omitted.append(f"{SHORT[m]} not run")
        else:
            sw = lr["lookup"]["switched_whole"]
            S.record(fid, target, "our removal, his passages: lookup switches under the whole change", sw, n=lr["n"],
                     source=z1_src[target])  # fmt: skip
            if sw < VALID_SWITCHES:
                omitted.append(f"{SHORT[m]} too few switches")
            else:
                v = tuple(round(x, 4) for x in lr["gap"])
                ctl = lr["recall"]["Rdep"][0] - lr["lookup"]["Rdep"][0]
                S.record(fid, target, "our removal, his passages: gap", *v, n=lr["n"], source=z1_src[target])
                S.record(fid, target, f"our removal, his passages: {control}", round(ctl, 4), n=lr["n"],
                         source=z1_src[target])  # fmt: skip
                cells[(0, 1)].append((i, v, ctl))
                if lt:
                    lt_n[(0, 1)] = str(lr["n"])
                else:
                    ns[(0, 1)].append(str(lr["n"]))
        # (1, 0) Zach's operation on our scenes: rung 6 of the ladder, recall's cost minus the lookup's (every scene)
        mod = lad.get(target)
        if lt:
            omitted.append(f"{SHORT[m]} {F.LT_GATE}")
        elif mod is None or 6 not in mod["rungs"]:
            omitted.append(f"{SHORT[m]} not run")
        else:
            rc, lk = (mod["cells"][w]["all"]["cost"]["6"][0] for w in ("recall", "lookup"))
            own = {w: mod["cells"][w]["all"]["kept"]["none"][0] - mod["cells"][w]["all"]["kept"]["rand6"][0]
                   for w in ("recall", "lookup")}  # fmt: skip
            n = mod["cells"]["recall"]["all"]["n"]
            S.record(fid, target, "Zach's operation, our scenes (rung 6): recall's cost minus the lookup's, every scene",
                     round(rc - lk, 4), n=n, source=rel(lad_path))  # fmt: skip
            S.record(fid, target, f"Zach's operation, our scenes (rung 6): {control}, every scene (kept with none "
                     "minus kept with the random part)", round(own["recall"] - own["lookup"], 4), n=n,
                     source=rel(lad_path))  # fmt: skip
            cells[(1, 0)].append((i, (rc - lk, None, None), own["recall"] - own["lookup"]))
            ns[(1, 0)].append(str(n))
        # (1, 1) Zach's operation on his passages: his stored M - K rows, his rotated control
        full = (z1.get(target) or {}).get("beside", {}).get("full")
        if not full:
            omitted.append(f"{SHORT[m]} rows not stored")
            continue
        rot, mk = full["paper10_rot"], full["paper10"]
        S.record(fid, target, "Zach's operation, his passages: his rotated-direction control, recall minus lookup",
                 *[round(x, 4) for x in rot["m_minus_k"]], n=rot["joined"], source=z1_src[target])  # fmt: skip
        S.record(fid, target, "Zach's operation, his passages: his stored recall minus lookup",
                 *[round(x, 4) for x in mk["m_minus_k"]], n=mk["joined"], source=z1_src[target])  # fmt: skip
        cells[(1, 1)].append((i, tuple(mk["m_minus_k"]), rot["m_minus_k"][0]))
        if lt:
            lt_n[(1, 1)] = str(mk["joined"])
        else:
            ns[(1, 1)].append(str(mk["joined"]))

    # Dan (21:55): one caption line, Muse's dagger and the empty cells; the grey tick's meaning is the legend's and the
    # README's Setup, the K items and the two scopes are E1's card and Zach's report
    lines = [
        (MUSE_DAGGER + ". " if dagger else "") + "Empty cells: " + ("; ".join(omitted) if omitted else "none") + "."
    ]
    lines += [F.LT_NOTE] if lightning else []
    plt = S.setup()
    cell_in, gap_in, top_in = 1.75, 0.62, 1.85
    bottom_in = 0.55 + 0.19 * len(caption_lines(lines))
    h = top_in + 2 * cell_in + gap_in + bottom_in
    fig, axes = plt.subplots(2, 2, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.26, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, hspace=gap_in / cell_in,
                        wspace=0.10)  # fmt: skip
    S.title(fig, "Both operations, both datasets, one direction",
            "The units differ: ours in share of switches, Zach's in points. Read the sign and the order, not the size.")  # fmt: skip
    for (r, c), items in cells.items():
        ax = axes[r, c]
        for i, v, ctl in items:
            ax.bar(i, v[0], width=0.5, fc="none", ec="#9a9a9a", lw=0.9, zorder=2)
            ax.plot([i - 0.3, i + 0.3], [ctl] * 2, color=NULL, lw=2.6, solid_capstyle="butt", zorder=3,
                    path_effects=[pe.withStroke(linewidth=3.8, foreground="white")])  # fmt: skip
            mark(ax, i, v, INK, "remove", ms=8.5, hollow=columns[i][1] == "lightning")
            ax.text(i + 0.3, v[0], f"{v[0]:.2f}", ha="left", va="center", fontsize=S.FONT - 1, color="#333333",
                    zorder=5)  # fmt: skip
            if (r, c) == (1, 0) and columns[i][1] == "muse" and dagger:  # the caption line's dagger
                ax.text(i, max(v[0], ctl) + 0.12, "†", ha="center", va="bottom", fontsize=S.FONT + 1, color="#1e1e1e")
        if items:  # Dan (21:50): each cell names its grey tick, under the first one
            i, _, ctl = items[0]
            ax.text(i, ctl - 0.05, "rotated" if (r, c) == (1, 1) else "random", ha="center", va="top",
                    fontsize=S.LABEL_PT, color=S.COL["muted"], zorder=5)  # fmt: skip
        n = ns[(r, c)]
        n_tag(ax, f"{n[0]} per model" if len(n) == 3 and len(set(n)) == 1 else ", ".join(n), lt_n.get((r, c), ""))
    for ax in axes.flat:
        ax.axhline(0, color="#999999", lw=0.8, zorder=1)
        ax.set_xlim(-0.55, len(columns) - 0.25)
        ax.set_xticks(range(len(columns)), [SHORT[m] for _, m, _ in columns])
        ax.tick_params(axis="x", length=0)
        ax.set_ylim(-0.36, 1.05)
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
    for ax, text in ((axes[0, 0], "our scenes"), (axes[0, 1], "Zach's passages")):
        ax.set_title(text, fontsize=12, weight="bold", loc="left", pad=24)
    # the row: the operation in bold, then what it counts in Dan's words (the units)
    for ax, head, unit in (
        (axes[0, 0], "our removal\n(from the\nchange)", "the recall's extra loss\nminus the lookup's\n(share of switches)"),
        (axes[1, 0], "Zach's operation\n(his lens\ndirections)", "recall answers lost\nminus lookup answers\nlost (points)"),
    ):  # fmt: skip
        ax.text(-0.72, 0.5, head, transform=ax.transAxes, ha="left", va="bottom", fontsize=12, weight="bold",
                linespacing=1.05)  # fmt: skip
        ax.text(-0.72, 0.43, unit, transform=ax.transAxes, ha="left", va="top", fontsize=S.FONT - 1,
                color=S.COL["muted"], linespacing=1.1)  # fmt: skip
    for ax, text in ((axes[0, 0], "gap, main test"), (axes[0, 1], "gap"),
                     (axes[1, 0], "last rung of the ladder, clean scenes"),
                     (axes[1, 1], "his stored rows, same passages")):  # fmt: skip
        ax.text(0.0, 1.03, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=S.FONT - 1, color="#555555")
    hs = [Line2D([], [], marker=S.MARK["remove"], ls="", color=INK, ms=8),
          Line2D([], [], color=NULL, lw=2.6, solid_capstyle="butt")]  # fmt: skip
    F.legend(fig, hs, ["recall minus lookup (95% whisker)", "control: a random part (same size); his: rotated directions"],
             1 - 0.74 / h, ncol=2)  # fmt: skip
    caption(fig, lines, bottom_in - 0.45)
    S.save(fig, out_name)
    return out_name
