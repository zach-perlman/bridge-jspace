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

from matplotlib.lines import Line2D
from matplotlib.patches import Patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_style as S

MODELS = tuple((t, m, name) for t, m, name in S.MODELS if m != "122b")  # 9B, 27B, Muse
SHORT = {"9b": "9B", "27b": "27B", "muse": "Muse"}
INK, LOOKUP, NULL = S.MARK_COL["recall"], S.MARK_COL["lookup"], S.MARK_COL["null"]
CAPTION = "#555555"
CAPTION_CHARS = 110  # caption characters per line at 10 pt in the 8.8 in column
MUSE_BAND = "Muse's rung 6 ran at L23–29; his band is L36–42 (rerun running)"
# the ladder's rungs in words (49.2's rung_text; rungs 5 and 6 are two definitions, not one)
RUNGS = {1: "bridge word,\none layer", 2: "bridge word,\nfour layers", 3: "+ the earlier\nmention",
         4: "+ the\nquestion", 5: "every token,\nfour layers", 6: "Zach's directions,\nhis band"}  # fmt: skip
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


def build_ladder(verdict_dir: Path, out_name: str = "fig01d_ladder") -> str:
    """Fig. 1d (E2): per model, the answers lost beyond a random part of the same share (pp) when the J++ part's
    directions are taken out of the changed prompt's own state, rung by rung (49.2's six rungs; the 27B ran rungs 1-2).
    Recall: locker before the pick (solid) and after it (dashed); lookup: every scene. The grey bars: what the random
    part itself costs the recall (every scene). Rung 6 (Zach's definition) stands apart from rungs 1-5 (ours)."""
    src_path = verdict_dir / "x49_2.json"
    v = json.loads(src_path.read_text())
    src, fid = rel(src_path), out_name.split("_")[0]
    by = {m["target"]: m for m in v["models"] if m.get("status") == "tested"}
    plt = S.setup()
    panel_in, gap_in, top_in, bottom_in = 1.45, 0.42, 1.75, 1.25
    h = top_in + 3 * panel_in + 2 * gap_in + bottom_in
    fig, axes = plt.subplots(3, 1, figsize=(S.WIDTH, h), sharex=True)
    fig.subplots_adjust(left=0.10, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, hspace=gap_in / panel_in)
    S.title(fig, "Recall needs the J++ part once its other copies go; the lookup never",
            "The J++ part taken out of the changed prompt, rung by rung; answers lost beyond a random part")  # fmt: skip
    series = (("recall", "locker-before", "-", "recall, locker before the pick"),
              ("recall", "locker-after", "--", "recall, locker after the pick"),
              ("lookup", "all", "-", "lookup, every scene"))  # fmt: skip
    group_key = {"locker-before": "locker-first", "locker-after": "locker-after", "all": "all"}
    dx = {"locker-before": -0.13, "locker-after": 0.0, "all": 0.13}
    omitted = []
    for k, (ax, (target, m, name)) in enumerate(zip(axes, MODELS, strict=True)):
        mod = by.get(target)
        model_label(ax, m, name, k == 0)
        ax.axhline(0, color="#999999", lw=0.8, zorder=1)
        ax.axhline(10, color="#555555", lw=1.0, ls=(0, (4, 3)), zorder=1)
        ax.text(6.62, 10, "10 pp", ha="right", va="bottom", fontsize=S.FONT - 1, color="#555555")
        ax.axvline(5.5, color="#cccccc", lw=1.0, zorder=0)
        ax.set_ylim(-12, 55)
        ax.set_yticks([0, 20, 40])
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)
        if mod is None:
            omitted.append(f"{SHORT[m]} (every rung)")
            continue
        rungs = mod["rungs"]
        if len(rungs) < 6:
            omitted.append(f"{SHORT[m]} rungs {len(rungs) + 1}–6")
        rc = mod["cells"]["recall"]["all"]
        own = [100 * (rc["kept"]["none"][0] - rc["kept"][f"rand{r}"][0]) for r in rungs]
        for r, o in zip(rungs, own, strict=True):
            S.record(fid, target, f"rung {r}: the random part's own cost to the recall, every scene (kept with none "
                     "minus kept with the random part)", round(o / 100, 4), n=rc["n"], source=src)  # fmt: skip
        ax.bar(rungs, own, width=0.6, color=NULL, alpha=0.55, lw=0, zorder=1)
        for reader, group, ls, label in series:
            cell = mod["cells"][reader][group_key[group]]
            col = INK if reader == "recall" else LOOKUP
            pts = []
            for r in rungs:
                c = cell["cost"][str(r)]
                pp = tuple(100 * x for x in c)
                S.record(fid, target, f"rung {r}: {label}: answers lost beyond random", *[round(x, 4) for x in c],
                         n=cell["n"], source=src)  # fmt: skip
                pts.append(pp)
                mark(ax, r + dx[group], pp, col, "zero", hollow=m == "muse" and r == 6, ms=7)
            ours = [(r + dx[group], p[0]) for r, p in zip(rungs, pts, strict=True) if r <= 5]  # rung 6 stands apart
            ax.plot(*zip(*ours, strict=True), color=col, ls=ls, lw=1.6, zorder=2)
        S.panel_tag(ax, str(rc["n"]), "fixed", inside=True)
    axes[1].set_ylabel("answers lost beyond random (pp)")
    axes[-1].set_xlim(0.5, 6.7)
    axes[-1].set_xticks(list(RUNGS), list(RUNGS.values()))
    hs = [Line2D([], [], color=INK, lw=1.8), Line2D([], [], color=INK, lw=1.8, ls="--"),
          Line2D([], [], color=LOOKUP, lw=1.8), Patch(fc=NULL, alpha=0.55, ec="none")]  # fmt: skip
    fig.legend(hs, [s[3] for s in series] + ["what a random part costs the recall"], loc="upper left",
               bbox_to_anchor=(0.0, 1 - 0.74 / h), frameon=False, ncol=2, handlelength=2.6, columnspacing=1.6)  # fmt: skip
    caption(fig, [f"Hollow: {MUSE_BAND}."] + ([f"Not run: {'; '.join(omitted)}."] if omitted else []), 0.42)
    S.save(fig, out_name)
    return out_name


# ---- fig12: the 2 x 2 ----------------------------------------------------------------------------------------------


def n_tag(ax, text: str) -> None:
    """story_style.panel_tag's look ("n = ..." and the status glyph), in the cell's bottom right under the zero line."""
    ax.text(0.995, 0.03, f"n = {text}  {S.STATUS_GLYPH['fixed']}", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=S.FONT - 1, color=S.COL["muted"], zorder=8)  # fmt: skip


def build_two_by_two(ladder_dir: Path, z1_dir: Path, out_name: str = "fig12_two_by_two") -> str:
    """Fig. 12: recall minus lookup in four cells, our operation / Zach's x our scenes / his passages, one mark per
    model: our main-test gap (docs/x0_numbers.json, Fig. 1's); rung 6 of the ladder on our clean scenes (recall's cost
    minus the lookup's, every scene; two separate estimates, so no joint interval); Z1's gap on his passages (a lookup
    with fewer than 30 switches is omitted); his stored M - K rows on the same passage ids, with his rotated-direction
    control as the grey band."""
    lad_path, z1_path = ladder_dir / "x49_2.json", z1_dir / "z1.json"
    lad = {m["target"]: m for m in json.loads(lad_path.read_text())["models"] if m.get("status") == "tested"}
    z1 = {m["target"]: m for m in json.loads(z1_path.read_text())["models"] if m.get("status") == "tested"}
    fid = out_name.split("_")[0]
    omitted, hollow = [], [MUSE_BAND.replace(" (rerun running)", "")]
    cells: dict[tuple[int, int], list] = {(0, 0): [], (0, 1): [], (1, 0): [], (1, 1): []}  # (i, v, op, hollow)
    ns: dict[tuple[int, int], list[str]] = {k: [] for k in cells}
    bands = []  # (i, lo, hi): his rotated control
    for i, (target, m, _) in enumerate(MODELS):
        # (0, 0) our removal on our scenes: the main test's gap (Fig. 1)
        v = F.interval(f"contrast_{m}")
        S.record(fid, target, "our removal, our scenes (main test): gap", *v, n=200, source=f"contrast_{m}")
        cells[(0, 0)].append((i, v, "remove", False))
        ns[(0, 0)].append("200")
        # (0, 1) our removal on his passages: Z1's gap at our layer
        mod = z1.get(target)
        lr = mod["layer_results"][str(mod["layers"][0])] if mod else None
        if lr is None:
            omitted.append(f"{SHORT[m]}, our removal on his passages (not run)")
        else:
            sw = lr["lookup"]["switched_whole"]
            S.record(fid, target, "our removal, his passages: lookup switches under the whole change", sw, n=lr["n"],
                     source=rel(z1_path))  # fmt: skip
            if sw < VALID_SWITCHES:
                omitted.append(f"{SHORT[m]} on his passages, too few lookup switches ({sw} of {lr['n']})")
            else:
                v = tuple(round(x, 4) for x in lr["gap"])
                S.record(fid, target, "our removal, his passages: gap", *v, n=lr["n"], source=rel(z1_path))
                cells[(0, 1)].append((i, v, "remove", True))
                ns[(0, 1)].append(str(lr["n"]))
        # (1, 0) Zach's operation on our scenes: rung 6 of the ladder, recall's cost minus the lookup's (every scene)
        mod = lad.get(target)
        if mod is None or 6 not in mod["rungs"]:
            omitted.append(f"{SHORT[m]} under Zach's operation on our scenes, not run")
        else:
            rc, lk = (mod["cells"][w]["all"]["cost"]["6"][0] for w in ("recall", "lookup"))
            n = mod["cells"]["recall"]["all"]["n"]
            S.record(fid, target, "Zach's operation, our scenes (rung 6): recall's cost minus the lookup's, every scene",
                     round(rc - lk, 4), n=n, source=rel(lad_path))  # fmt: skip
            cells[(1, 0)].append((i, (rc - lk, None, None), "zero", m == "muse"))
            ns[(1, 0)].append(str(n))
        # (1, 1) Zach's operation on his passages: his stored M - K rows, his rotated control as the band
        full = (z1.get(target) or {}).get("beside", {}).get("full")
        if not full:
            omitted.append(f"{SHORT[m]}, his rows not stored")
            continue
        rot, mk = full["paper10_rot"], full["paper10"]
        S.record(fid, target, "Zach's operation, his passages: his rotated-direction control, recall minus lookup",
                 *[round(x, 4) for x in rot["m_minus_k"]], n=rot["joined"], source=rel(z1_path))  # fmt: skip
        S.record(fid, target, "Zach's operation, his passages: his stored recall minus lookup",
                 *[round(x, 4) for x in mk["m_minus_k"]], n=mk["joined"], source=rel(z1_path))  # fmt: skip
        bands.append((i, rot["m_minus_k"][1], rot["m_minus_k"][2]))
        cells[(1, 1)].append((i, tuple(mk["m_minus_k"]), "zero", False))
        ns[(1, 1)].append(str(mk["joined"]))

    lines = [f"Hollow: reruns tonight ({hollow[0]}; our removal on his passages, with the P final).",
             (f"Omitted: {'; '.join(omitted)}. " if omitted else "") + "The last rung: two separate estimates, no "
             "joint interval. On his passages the lookup is his K final (the answer read from the passage)."]  # fmt: skip
    plt = S.setup()
    cell_in, gap_in, top_in = 1.75, 0.62, 1.85
    bottom_in = 0.55 + 0.19 * len(caption_lines(lines))
    h = top_in + 2 * cell_in + gap_in + bottom_in
    fig, axes = plt.subplots(2, 2, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.24, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, hspace=gap_in / cell_in,
                        wspace=0.10)  # fmt: skip
    S.title(fig, "Both operations, both datasets, one direction",
            "Recall minus lookup: how much more the recall loses than the lookup when lens directions are taken out")  # fmt: skip
    for i, lo, hi in bands:
        axes[1, 1].fill_between([i - 0.36, i + 0.36], [lo] * 2, [hi] * 2, color=NULL, alpha=0.6, lw=0, zorder=1)
    for (r, c), items in cells.items():
        ax = axes[r, c]
        for i, v, op, holl in items:
            ax.bar(i, v[0], width=0.5, fc="none", ec="#9a9a9a", lw=0.9, zorder=2)
            mark(ax, i, v, INK, op, hollow=holl, ms=8.5)
            ax.text(i + 0.3, v[0], f"{v[0]:.2f}", ha="left", va="center", fontsize=S.FONT - 1, color="#333333",
                    zorder=5)  # fmt: skip
        n = ns[(r, c)]
        n_tag(ax, f"{n[0]} per model" if len(n) == 3 and len(set(n)) == 1 else ", ".join(n))
    for ax in axes.flat:
        ax.axhline(0, color="#999999", lw=0.8, zorder=1)
        ax.set_xlim(-0.55, 2.75)
        ax.set_xticks(range(3), [SHORT[m] for _, m, _ in MODELS])
        ax.tick_params(axis="x", length=0)
        ax.set_ylim(-0.2, 1.05)
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
    for ax, text in ((axes[0, 0], "our scenes"), (axes[0, 1], "Zach's passages")):
        ax.set_title(text, fontsize=12, weight="bold", loc="left", pad=24)
    for ax, text in (
        (axes[0, 0], "our removal\n(from the\nchange)"),
        (axes[1, 0], "Zach's\noperation\n(his lens\ndirections)"),
    ):
        ax.text(-0.56, 0.5, text, transform=ax.transAxes, ha="left", va="center", fontsize=12, weight="bold",
                linespacing=1.05)  # fmt: skip
    for ax, text in ((axes[0, 0], "gap, main test"), (axes[0, 1], "gap"),
                     (axes[1, 0], "last rung of the ladder, clean scenes"),
                     (axes[1, 1], "his stored rows, same passages")):  # fmt: skip
        ax.text(0.0, 1.03, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=S.FONT - 1, color="#555555")
    hs = [
        Line2D([], [], marker=S.MARK["remove"], ls="", color=INK, ms=8),
        Line2D([], [], marker=S.MARK["zero"], ls="", color=INK, ms=8),
        Patch(fc=NULL, alpha=0.6, ec="none"),
    ]
    F.legend(fig, hs, ["our removal", "Zach's operation", "his rotated directions (control)"], 1 - 0.74 / h, ncol=3)
    caption(fig, lines, bottom_in - 0.45)
    S.save(fig, out_name)
    return out_name
