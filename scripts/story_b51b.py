"""51.10's figures, redrawn to Dan's brief (28 Oct ~22:35): "readable but not used" seen at a glance. Two quantities that
shared one cell before (the heat = the probe, the number = the swap) now get one grid each, the same shape, side by side.

  s17_jspace_grid_{9b,27b,muse}  per model (supplement): rows the bridge word, the question's pick token and the last
                                 token, in one block per reader (lookup, recall); columns the layers of the run. Left,
                                 "Can the lens read the entity here?": the through-the-lens probe's accuracy on the
                                 locker-first rows (read.json). Right, "Does writing through the lens change the
                                 answer?": the swap's switches over the whole-state patch's at that position and layer
                                 (verdict.json), hatched where the whole-state patch switches < 0.1. One sequential 0-1
                                 scale on both, dark = 0, bright = 1 (the J++ part's hue of the mark system); no number
                                 in a cell. A line where the answer appears (the verdict's answer layer), greyed after it;
                                 the first layer passing the read bar boxed on both grids; the decisive cell's numbers
                                 in one line beneath.
  fig17_jspace_last_token        the main page: the last token only, per reader one panel, per model two bars (the
                                 probe's accuracy, the swap over the whole-state patch) at the verdict's read peak (the
                                 layer before the answer with the highest through-the-lens accuracy, where the write
                                 rule was read), 95% cluster-bootstrap intervals over the bridge entities (the ratio's
                                 paired, from outcomes.jsonl).

Every plotted number is recorded for figures/story/data.csv with its source file.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from matplotlib import patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from matplotlib.transforms import blended_transform_factory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import story_style as S
from scripts import x0_necessity as X
from scripts.story_b50 import INK, LOOKUP, MODELS, NOT_RUN, SHORT, caption, rel
from scripts.story_b51 import head

TITLE = "At the last token the in-between entity is in the lens, but the answer is not computed through it"
READERS = (("lookup", LOOKUP), ("recall", INK))
CODE = {"lookup": X.LOOKUP, "recall": X.RECALL}  # outcomes.jsonl's reader codes
POS = (("P1", "the bridge word"), ("P2", "the question's\npick token"), ("P3", "the last token"))
POS_TEXT = {p: t.replace("\n", " ") for p, t in POS}
# scripts/x51_jread.py's read bar (THRU_MIN, TOP5_MIN, FULL_MIN; not imported: it loads the model stack); the boxes are
# asserted against the verdict's own first readable layers
THRU_MIN, TOP5_MIN, FULL_MIN, EPS = 0.8, 0.5, 0.9, 1e-9
NOTHING = 0.1  # Dan: where the whole-state patch switches under 0.1 there is nothing to move: hatched, no ratio
DARK = "#1e1e1e"
# one sequential scale, dark (0) to bright (1), through the J++ part's hue (the lens's colour in the mark system)
SEQ = LinearSegmentedColormap.from_list("lens", [DARK, S.MARK_COL["jpp"], "#aee6dc"]).with_extremes(bad="white")
GREYED = {"facecolor": "#cfcfcf", "alpha": 0.9, "lw": 0}
HATCH = {"facecolor": "#f6f6f6", "edgecolor": "#b4b4b4", "hatch": "////", "lw": 0}
BOX_FX = [pe.Stroke(linewidth=3.6, foreground=DARK), pe.Normal()]
LINE_FX = [pe.Stroke(linewidth=3.4, foreground="white"), pe.Normal()]


def readable(c: dict) -> bool:
    """x51_jread's read bar at one cell (read.json): through-the-lens >= 0.8, lens top-5 >= 0.5, full residual >= 0.9."""
    return (c["thru"]["lf"][0] >= THRU_MIN - EPS and (c["lens"]["top5"] or 0.0) >= TOP5_MIN - EPS
            and c["full"]["lf"][0] >= FULL_MIN - EPS)  # fmt: skip


def model_data(verdict_dir: Path) -> dict[str, dict]:
    """Per tested model: its verdict entry, its read.json (the newest read folder of its run, the one the verdict read:
    its first readable layers and read peaks are asserted equal) and the source paths."""
    vpath = verdict_dir / "verdict.json"
    blob = json.loads(vpath.read_text())
    out = {}
    for m in blob["models"]:
        if m["status"] != "tested":
            continue
        rpath = sorted(verdict_dir.parent.glob(f"read-{m['run']}-*/read.json"))[-1]
        read = json.loads(rpath.read_text())
        assert read["layers"] == m["layers"], m["target"]
        assert read["peaks_P3"] == m["read_folder_peaks"], m["target"]
        for w, _ in READERS:
            ans = m["answer"][w]["layer"]
            for p in ("P2", "P3"):
                assert first_readable(read, w, p, m["layers"], ans) == m["rules"][w][p]["first_readable_before_answer"]
        out[m["target"]] = {"m": m, "read": read, "src_v": rel(vpath), "src_r": rel(rpath),
                            "outcomes": verdict_dir.parent / m["run"] / "outcomes.jsonl"}  # fmt: skip
    return out


def first_readable(read: dict, w: str, p: str, layers: list[int], ans: int | None) -> int | None:
    return next((la for la in layers if (ans is None or la < ans) and readable(read["cells"][f"{w}|{p}|{la}"])), None)


def switch(m: dict, w: str, p: str, la: int, arm: str) -> list[float]:
    return m["readers"][w]["switch"][f"{p}|{la}|{arm}"]["switch"]


def ratio_ci(path: Path, w: str, la: int, swap: float, whole: float) -> tuple[float, float, float, int]:
    """The swap's switches over the whole-state patch's at the last token and layer la: the point, and a paired 95%
    cluster-bootstrap interval over the bridge entities (x0_necessity's resampler, 10,000, seed 0: the verdict's)."""
    rows = [r for r in X.read_jsonl(path) if r["reader"] == CODE[w] and r["pos"] == "P3" and r["layer"] == la
            and r["arm"] in ("swap", "whole")]  # fmt: skip
    by = {a: {r["scene"]: r for r in rows if r["arm"] == a} for a in ("swap", "whole")}
    scenes = sorted(by["swap"])
    assert scenes == sorted(by["whole"]), (w, la)
    s = [by["swap"][k]["switched"] for k in scenes]
    h = [by["whole"][k]["switched"] for k in scenes]
    assert abs(np.mean(s) - swap) < 1e-9, (w, la)
    assert abs(np.mean(h) - whole) < 1e-9, (w, la)
    boot = X.resampled_rates({"swap": s, "whole": h}, [by["swap"][k]["entity"] for k in scenes], X.N_BOOT, X.BOOT_SEED)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(boot["whole"] > 0, boot["swap"] / boot["whole"], np.nan)
    return (swap / whole, *X.interval(r), len(scenes))


def answer_cut(layers: list[int], ans: int | None) -> int:
    """The first column at or after the answer layer (len(layers) when the answer appears after the last one)."""
    return next((j for j, la in enumerate(layers) if ans is not None and la >= ans), len(layers))


# ---- the per-model grids (supplement) ------------------------------------------------------------------------------


def row_of(ri: int, pi: int) -> int:
    return 4 * ri + pi  # three positions per reader, an empty row between the readers


def runs(cols: list[int]) -> list[tuple[int, int]]:
    """Consecutive column indices as (first, count)."""
    out: list[tuple[int, int]] = []
    for j in sorted(cols):
        if out and out[-1][0] + out[-1][1] == j:
            out[-1] = (out[-1][0], out[-1][1] + 1)
        else:
            out.append((j, 1))
    return out


def grid_frame(ax, nl: int, label: bool) -> None:
    for j in range(nl - 1):
        ax.plot([j + 0.5] * 2, [-0.5, 2.5], color="white", lw=0.7, zorder=1.5)
        ax.plot([j + 0.5] * 2, [3.5, 6.5], color="white", lw=0.7, zorder=1.5)
    for y in (0.5, 1.5, 4.5, 5.5):
        ax.plot([-0.5, nl - 0.5], [y] * 2, color="white", lw=0.7, zorder=1.5)
    ax.set_xlim(-0.5, nl - 0.5)
    ax.set_ylim(6.5, -0.5)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    if label:
        ax.set_yticks([row_of(ri, pi) for ri in range(2) for pi in range(3)], [t for _ in range(2) for _, t in POS])
    else:
        ax.tick_params(labelleft=False)


def answer_marks(ax, layers: list[int], answers: dict[str, int | None]) -> None:
    """Per reader block: grey every column from the answer layer on, a line where the answer appears, labelled above
    the block."""
    nl = len(layers)
    for ri, (w, _) in enumerate(READERS):
        cut, top = answer_cut(layers, answers[w]), row_of(ri, 0) - 0.5
        if cut < nl:
            ax.add_patch(Rectangle((cut - 0.5, top), nl - cut, 3, zorder=3, **GREYED))
        ax.plot([cut - 0.5] * 2, [top - 0.32, top + 3], color=DARK, lw=1.6, zorder=5, solid_capstyle="butt",
                path_effects=LINE_FX, clip_on=False)  # fmt: skip
        ax.text(cut - 0.65, top - 0.1, "the answer appears", ha="right", va="bottom", fontsize=S.LABEL_PT, color=DARK,
                zorder=6, clip_on=False)  # fmt: skip


def box(ax, row: int, col: int) -> None:
    ax.add_patch(Rectangle((col - 0.5, row - 0.5), 1, 1, fill=False, ec="white", lw=1.7, zorder=7, path_effects=BOX_FX,
                           clip_on=False))  # fmt: skip


def build_grid(verdict_dir: Path, target: str, out_name: str) -> str:
    """One model's two grids (see the module docstring), as a supplementary figure."""
    d = model_data(verdict_dir)[target]
    m, read = d["m"], d["read"]
    layers, nl, n = m["layers"], len(m["layers"]), m["n"]
    answers = {w: m["answer"][w]["layer"] for w, _ in READERS}
    chance = sorted({read["cells"][k]["thru"]["chance_lf"] for k in read["cells"]})
    assert max(chance) - min(chance) < 1e-9, chance  # one chance per model (1 / the family's classes, all families)
    rd = np.full((7, nl), np.nan)
    wr = np.full((7, nl), np.nan)
    hatched: dict[int, list[int]] = {}
    boxes: list[tuple[int, int]] = []
    for ri, (w, _) in enumerate(READERS):
        cut = answer_cut(layers, answers[w])
        for pi, (p, _) in enumerate(POS):
            row = row_of(ri, pi)
            for j, la in enumerate(layers):
                c = read["cells"][f"{w}|{p}|{la}"]
                rd[row, j] = c["thru"]["lf"][0]
                after = " (after the answer appears: greyed)" if j >= cut else ""
                S.record(out_name, target, f"51.10 read grid: {w}, {POS_TEXT[p]}, layer {la}: the probe's accuracy on "
                         f"the lens part of the state, locker-first rows{after}", *c["thru"]["lf"],
                         n=c["thru"]["n_lf"], source=d["src_r"])  # fmt: skip
                sw, wh = switch(m, w, p, la, "swap")[0], switch(m, w, p, la, "whole")[0]
                if wh < NOTHING - EPS:
                    hatched.setdefault(row, []).append(j)
                    S.record(out_name, target, f"51.10 swap grid: {w}, {POS_TEXT[p]}, layer {la}: hatched, the "
                             f"whole-state patch switches under 0.1{after}", wh, n=n, source=d["src_v"])  # fmt: skip
                else:
                    wr[row, j] = min(sw / wh, 1.0)
                    S.record(out_name, target, f"51.10 swap grid: {w}, {POS_TEXT[p]}, layer {la}: the swap's switches "
                             f"over the whole-state patch's ({sw:.4f} / {wh:.4f}){after}", sw / wh, n=n,
                             source=d["src_v"])  # fmt: skip
            fr = first_readable(read, w, p, layers, answers[w])
            if fr is not None:
                boxes.append((row, layers.index(fr)))
            S.record(out_name, target, f"51.10: {w}, {POS_TEXT[p]}: first layer passing the read bar before the answer",
                     fr, source=d["src_r"])  # fmt: skip
        S.record(out_name, target, f"51.10: {w}: the layer where the answer appears (plain logit lens, last token)",
                 answers[w], n=m["answer"][w]["n"], source=d["src_v"])  # fmt: skip
    S.record(out_name, target, "51.10: the read probe's chance (locker-first rows)", chance[0], source=d["src_r"])

    plt = S.setup()
    top_in, row_in, bottom_in, left_in = 1.85, 0.3, 2.1, 1.6
    h = top_in + 7 * row_in + bottom_in
    fig, (a, b) = plt.subplots(1, 2, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=left_in / S.WIDTH, right=0.985, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.07)
    S.title(fig, TITLE, "Left: a probe on the lens part of the state. Right: the lens swap as a share of patching the "
            "whole state", limit=100)  # fmt: skip
    heads = ((a, "Can the lens read\nthe entity here?", "probe accuracy on the lens part of the state"),
             (b, "Does writing through the lens\nchange the answer?", "lens swap's switches ÷ whole-state patch's"))  # fmt: skip
    for ax, bold, sub in heads:
        head(fig, ax.get_position().x0, 1.2, bold, sub)
        fig.text(ax.get_position().x1, 1 - 1.2 / h, f"n = {n}  ●", ha="right", va="bottom", fontsize=S.FONT - 1,
                 color=S.COL["muted"])  # fmt: skip
    for ax, grid in ((a, rd), (b, wr)):
        ax.imshow(np.ma.masked_invalid(grid), cmap=SEQ, vmin=0, vmax=1, aspect="auto", interpolation="nearest",
                  zorder=1)  # fmt: skip
        grid_frame(ax, nl, ax is a)
        answer_marks(ax, layers, answers)
        for row, col in boxes:
            box(ax, row, col)
        ax.set_xticks(range(0, nl, 2), [str(la) for la in layers[::2]])
        ax.set_xlabel("layer")
    for row, cols in hatched.items():
        for j0, k in runs(cols):
            b.add_patch(Rectangle((j0 - 0.5, row - 0.5), k, 1, zorder=2, **HATCH))
    tr = blended_transform_factory(fig.transFigure, a.transData)
    for ri, (w, col) in enumerate(READERS):
        a.text(0.012, row_of(ri, 1), w, transform=tr, rotation=90, ha="left", va="center", fontsize=12, weight="bold",
               color=col)  # fmt: skip
    legend(fig, a, b, h, chance[0], greyed=any(answer_cut(layers, x) < nl for x in answers.values()))
    caption(fig, [decisive_line(m, read, "recall")], 0.48)
    S.save(fig, out_name, supp=True)
    S.record(out_name, target, "51.10: locker-first items (the swap grid's n)", n, source=d["src_v"])
    return out_name


def legend(fig, a, b, h: float, chance: float, greyed: bool = True) -> None:
    """Under the grids: the shared colour scale with chance marked (under the read grid); the hatch, the greyed columns
    (when a grid has any) and the box (under the swap grid)."""
    x0, w_in = a.get_position().x0, 2.3
    y_bar = 1.12 / h
    cax = S.inset(fig, (x0, y_bar, w_in / S.WIDTH, 0.15 / h))
    cax.imshow(np.linspace(0, 1, 256)[None, :], cmap=SEQ, vmin=0, vmax=1, aspect="auto", extent=(0, 1, 0, 1))
    cax.set_yticks([])
    cax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    cax.tick_params(length=2, pad=2)
    for s in cax.spines.values():
        s.set_visible(False)
    cax.plot([chance] * 2, [0, 1], color="white", lw=1.4, path_effects=BOX_FX, zorder=3)
    cax.text(chance, 1.25, "chance", ha="left", va="bottom", fontsize=S.LABEL_PT, color=DARK, transform=cax.transData,
             clip_on=False)  # fmt: skip
    fig.text(x0 - 0.1 / S.WIDTH, y_bar + 0.075 / h, "both grids", ha="right", va="center", fontsize=S.LABEL_PT,
             color=S.COL["muted"])  # fmt: skip
    xs = b.get_position().x0
    sw, sh = 0.26 / S.WIDTH, 0.15 / h
    items = [(1.32, HATCH, "nothing to move here: the whole-state patch\nswitches under 0.1"),
             (0.98, GREYED, "after the answer appears"), (0.74, None, "first layer passing the read bar")]  # fmt: skip
    if not greyed:
        items = [items[0], (0.98, None, items[2][2])]
    for y_in, style, text in items:
        y = y_in / h
        if style is None:
            p = Rectangle((xs, y - sh / 2), sw, sh, transform=fig.transFigure, fill=False, ec="white", lw=1.7,
                          path_effects=BOX_FX)  # fmt: skip
        else:
            p = Rectangle((xs, y - sh / 2), sw, sh, transform=fig.transFigure, **style)
        fig.add_artist(p)
        fig.text(xs + sw + 0.08 / S.WIDTH, y, text, ha="left", va="center", fontsize=S.LABEL_PT, color=DARK,
                 linespacing=1.1)  # fmt: skip


def decisive_line(m: dict, read: dict, w: str) -> str:
    """Dan's one line for the decisive cell: the reader's last token at its first layer passing the read bar."""
    r = m["rules"][w]["P3"]
    la = r["first_readable_before_answer"]
    if la is None:
        return f"{w}, last token: the lens never passes the read bar before the answer appears."
    c = read["cells"][f"{w}|P3|{la}"]
    sw, wh = switch(m, w, "P3", la, "swap")[0], switch(m, w, "P3", la, "whole")[0]
    return (f"{w}, last token: the probe reads the entity from layer {la} ({c['thru']['lf'][0]:.2f}, lens top-5 "
            f"{c['lens']['top5']:.2f}); the lens swap moves {sw:.2f} of answers there while patching the whole state "
            f"moves {wh:.2f}.")  # fmt: skip


def record_decisive(out_name: str, target: str, d: dict, w: str = "recall") -> None:
    """The decisive line's numbers with their intervals (the line itself prints the points)."""
    m, read = d["m"], d["read"]
    la = m["rules"][w]["P3"]["first_readable_before_answer"]
    S.record(out_name, target, f"51.10 decisive: {w}, last token: first layer passing the read bar", la,
             source=d["src_v"])  # fmt: skip
    if la is None:
        return
    c = read["cells"][f"{w}|P3|{la}"]
    S.record(out_name, target, f"51.10 decisive: {w}, last token, layer {la}: probe accuracy on the lens part",
             *c["thru"]["lf"], n=c["thru"]["n_lf"], source=d["src_r"])  # fmt: skip
    S.record(out_name, target, f"51.10 decisive: {w}, last token, layer {la}: lens top-5", c["lens"]["top5"],
             source=d["src_r"])  # fmt: skip
    for arm, what in (("swap", "the lens swap's switches"), ("whole", "the whole-state patch's switches")):
        S.record(out_name, target, f"51.10 decisive: {w}, last token, layer {la}: {what}", *switch(m, w, "P3", la, arm),
                 n=m["n"], source=d["src_v"])  # fmt: skip


def build_grids(verdict_dir: Path, prefix: str = "s17_jspace_grid") -> list[str]:
    """The three per-model grids, s17_jspace_grid_{9b,27b,muse}."""
    data = model_data(verdict_dir)
    names = []
    for t, key, _ in MODELS:
        if t in data:
            name = f"{prefix}_{key}"
            build_grid(verdict_dir, t, name)
            record_decisive(name, t, data[t])
            names.append(name)
    return names


# ---- the main page: the last token only (fig17) ---------------------------------------------------------------------


LT_ROW = ("nemotron-3.5-lightning", "lightning")


def build_last_token(verdict_dir: Path, out_name: str = "fig17_jspace_last_token", lightning: Path | None = None,
                     lightning_note: str = "") -> str:  # fmt: skip
    """Fig. 17 (see the module docstring): per reader one panel, per model the probe's accuracy on the lens part of the
    last token's state and the lens swap's switches over the whole-state patch's, both at the verdict's read peak.
    Lightning (batch 52) from its own verdict folder `lightning`, after the data: its read bar hatched, its swap bar's
    edge dashed (filled vs open already tells read from swap here), `lightning_note` in the caption."""
    data = model_data(verdict_dir)
    rows = [(t, k) for t, k, _ in MODELS if t in data]
    if lightning is not None:
        data[LT_ROW[0]] = model_data(lightning)[LT_ROW[0]]
        rows.append(LT_ROW)
    plt = S.setup()
    four = LT_ROW in rows  # four models: the bars spread to their gap, the model's layer under its name
    top_in, ax_in, bottom_in = 1.25, 2.3, 1.25 + 0.45 * four
    h = top_in + ax_in + bottom_in
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.075, right=0.985, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.06)
    S.title(fig, TITLE, "The last token, at the layer before the answer where the lens reads the entity best",
            limit=100)  # fmt: skip
    bw, dx = (0.34, 0.25) if four else (0.34, 0.19)  # read and swap ticks clear of each other
    for ax, (w, col) in zip(axes, READERS, strict=True):
        ax.text(0.0, 1.03, w, transform=ax.transAxes, ha="left", va="bottom", fontsize=12, weight="bold", color=col)
        ticks, labels, chances = [], [], []
        for i, (t, key) in enumerate(rows):
            d = data[t]
            m, read = d["m"], d["read"]
            la = m["rules"][w]["P3"]["peak"]
            c = read["cells"][f"{w}|P3|{la}"]
            rv = c["thru"]["lf"]
            sw, wh = switch(m, w, "P3", la, "swap")[0], switch(m, w, "P3", la, "whole")[0]
            assert abs(m["rules"][w]["P3"]["at_peak"]["whole"] - wh) < 1e-9, (t, w)
            wv = ratio_ci(d["outcomes"], w, la, sw, wh)
            chance = c["thru"]["chance_lf"]
            chances.append(chance)
            if key == LT_ROW[1]:  # after the data
                ax.bar(i - dx, rv[0], width=bw, facecolor="white", edgecolor=col, hatch="////", lw=1.4, zorder=2)
                ax.bar(i + dx, wv[0], width=bw, facecolor="white", edgecolor=col, lw=1.4, ls=(0, (3, 2)), zorder=2)
            else:
                ax.bar(i - dx, rv[0], width=bw, color=col, lw=0, zorder=2)
                ax.bar(i + dx, wv[0], width=bw, facecolor="white", edgecolor=col, lw=1.4, zorder=2)
            for x, v in ((i - dx, rv), (i + dx, wv)):
                ax.plot([x, x], [v[1], v[2]], color="#8c8c8c", lw=1.3, zorder=3, solid_capstyle="butt")
                ax.text(x, max(v[2], v[0]) + 0.025, f"{v[0]:.2f}", ha="center", va="bottom", fontsize=S.LABEL_PT,
                        color=DARK)  # fmt: skip
            ax.plot([i - dx - bw / 2 - 0.04, i - dx + bw / 2 + 0.04], [chance] * 2, color="#bdbdbd", ls=(0, (2, 1.5)),
                    lw=1.5, zorder=4)  # fmt: skip
            ticks += [i - dx, i + dx]
            labels += ["read", "swap"]
            ax.text(i, -0.12, f"{SHORT[key]}{chr(10) if four else ' · '}L{la}", transform=blended_transform_factory(ax.transData, ax.transAxes),
                    ha="center", va="top", fontsize=S.FONT, weight="bold")  # fmt: skip
            S.record(out_name, t, f"51.10: {w}, last token, read peak layer {la}: the probe's accuracy on the lens part "
                     "of the state, locker-first rows", *rv, n=c["thru"]["n_lf"], source=d["src_r"])  # fmt: skip
            S.record(out_name, t, f"51.10: {w}, last token, read peak layer {la}: the lens swap's switches over the "
                     f"whole-state patch's ({sw:.4f} / {wh:.4f}), paired cluster bootstrap", *wv[:3], n=wv[3],
                     source=rel(d["outcomes"]))  # fmt: skip
            S.record(out_name, t, f"51.10: {w}, last token: the read peak layer (the answer appears at layer "
                     f"{m['answer'][w]['layer']})", la, source=d["src_v"])  # fmt: skip
            S.record(out_name, t, "51.10: the read probe's chance (locker-first rows)", chance, source=d["src_r"])
            # the README card's plain keys (no layer or value inside the quantity)
            S.record(out_name, t, f"51.10: {w}, last token, read peak: the probe's accuracy on the lens part", *rv,
                     n=c["thru"]["n_lf"], source=d["src_r"])  # fmt: skip
            for arm, v in (("the lens swap's switches", sw), ("the whole-state patch's switches", wh)):
                S.record(
                    out_name, t, f"51.10: {w}, last token, read peak: {arm}", v, n=wv[3], source=rel(d["outcomes"])
                )
        # the fifth slot (Dan's 11:30): the 122B ran no last-token read, a grey slot after the drawn models
        i = len(rows) - 0.12  # a narrow slot: no bars, only its label (a full slot crowds the read / swap ticks)
        ax.text(i, 0.5, NOT_RUN.replace(" ", "\n"), ha="center", va="center", fontsize=S.LABEL_PT,
                color=S.COL["muted"])  # fmt: skip
        ax.text(i, -0.12, SHORT["122b"], transform=blended_transform_factory(ax.transData, ax.transAxes),
                ha="center", va="top", fontsize=S.FONT, weight="bold")  # fmt: skip
        ax.text(-dx - bw / 2 - 0.06, chances[0], "chance", ha="right", va="center", fontsize=S.LABEL_PT,
                color=S.COL["muted"])  # fmt: skip
        ax.set_xticks(
            ticks, labels, fontsize=S.LABEL_PT - 1
        )  # ten ticks per panel: a point smaller, clear of each other
        ax.tick_params(axis="x", length=0)
        ax.set_xlim(-0.95, len(rows) + 0.2)
        ax.set_ylim(0, 1.12)
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
        ns = [str(data[t]["m"]["n"]) for t, k in rows if k != LT_ROW[1]]
        tag = f"n = {', '.join(ns)}  ●" + (f";  {data[LT_ROW[0]]['m']['n']}  ○" if LT_ROW in rows else "")
        ax.text(1.0, 1.02, tag, transform=ax.transAxes, ha="right", va="bottom", fontsize=S.FONT - 1,
                color=S.COL["muted"])  # fmt: skip
    axes[0].set_ylabel("share")
    lines = ["Read: a probe's accuracy on the lens part of the last token's state (dotted: chance). Swap: the lens "
             "swap's switches as a share of the whole-state patch's at the same layer. Whiskers: 95% intervals."]  # fmt: skip
    lines += [lightning_note] if lightning_note and LT_ROW in rows else []
    caption(fig, lines, 0.48 + 0.25 * four)
    S.save(fig, out_name)
    return out_name
