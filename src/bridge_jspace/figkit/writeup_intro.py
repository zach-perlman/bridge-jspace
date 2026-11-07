"""The LessWrong write-up's rebuilt opening figures (figures/writeup/, `figkit.tables --target writeup`): the datasets
(p0a), the tools (p0b), the routes (r5), the pointer (r4) and the last token (r3), laid out again at 8.0 in. They read
the same sources as their originals (depth_figs.py, exemplars.py); the originals stay as they are."""

from __future__ import annotations

import re

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import writeup_figs as W
from bridge_jspace.figkit.dottable import INK, MUTED, C, Col, Row, connector, dot, head_label, rich, vrule

OUT = "."  # set by bridge_jspace.figkit.tables
PROBLEMS: list[str] = []
NAME, DAN = W.NAME, W.DAN


def _save(fig, name: str) -> None:
    """A figure drawn without the dot table: the target's lint hook, then the PNG."""
    path = f"{OUT}/{name}.png"
    if T.BEFORE_SAVE is not None:
        T.BEFORE_SAVE(fig, path)
    fig.savefig(path, dpi=W.DPI, facecolor="white")
    plt.close(fig)


# ---- Fig. 2: the datasets (p0a_datasets) ------------------------------------------------------------------------------
def fig02_datasets() -> None:
    """The two kinds of prompt as a table, as p0a: the fact passages (question, the lookup's passage, the recall's) and
    the locker scenes (scene, lookup question, recall question); the bridge in bold. At 8 in a long prompt runs on two
    lines, and the answer (lookup purple, recall ink) sits over its source (grey)."""
    B, N = "bold", "normal"

    def words(*parts):
        return [(t, INK, B if bold else N) for t, bold in parts]

    look, rec = ("lookup", C["lookup"]), ("recall", C["recall"])
    rows = [  # (label, sub-row?, prompt lines, (answer, colour) or None, source)
        ("Fact passages", False, [words(("Question: ", False), ("The composer who wrote The Magic Flute", True)),
                                  words(("was of which nationality?", False))], None, ""),
        (look[0], True, [words(("“… ", False), ("Mozart", True), (" was Austrian by birth. …”", False))],
         ("Austrian", look[1]), "in the passage"),
        (rec[0], True, [words(("“… A reader asked a question about ", False), ("Mozart", True)),
                        words(("in the letters page. …”", False))], ("Austrian", rec[1]), "from memory"),
        ("Locker scenes", False, [words(("The locker of carbon is 3. The locker of helium is 5.", False)),
                                  words(("Eric picked ", False), ("carbon", True), (".", False))], None, ""),
        (look[0], True, [words(("Which locker belongs to Eric's pick?", False))], ("3", look[1]), "in the scene"),
        (rec[0], True, [words(("What is the atomic number of Eric's pick?", False))], ("6", rec[1]), "from memory"),
    ]  # fmt: skip
    head, rh, foot = 0.85, 0.62, 0.15
    x_label, x_prompt, x_answer = 0.12, 1.55, 6.55
    h = head + rh * len(rows) + foot
    fig = plt.figure(figsize=(W.WIDTH, h), dpi=W.DPI)
    fx, fy = (lambda x: x / W.WIDTH), (lambda y: 1 - y / h)  # inches -> figure fraction (y from the top)
    size = W.FS["text"]
    for x, title, sub in ((x_prompt, "Prompt", "the bridge in bold"), (x_answer, "Answer", "and its source")):
        fig.text(fx(x), fy(0.22), title, ha="left", va="top", fontsize=W.FS["title"], weight="bold", color=INK)
        fig.text(fx(x), fy(0.52), sub, ha="left", va="top", fontsize=W.FS["sub"], color=MUTED)
    for i, (label, sub, lines, answer, source) in enumerate(rows):
        top = head + i * rh
        if i % 2 == 0:
            fig.patches.append(Rectangle((0, fy(top + rh)), 1, rh / h, transform=fig.transFigure, color=T.ZEBRA,
                                         zorder=-5))  # fmt: skip
        line_y = [top + rh * 0.33, top + rh * 0.69]
        if sub:
            fig.text(fx(0.3), fy(line_y[0]), label, ha="left", va="center", fontsize=W.FS["subrow"], color=MUTED)
        else:
            fig.text(fx(x_label), fy(line_y[0]), label, ha="left", va="center", fontsize=W.FS["name"], weight=B,
                     color=INK)  # fmt: skip
        for k, parts in enumerate(lines):
            rich(fig, fx(x_prompt), fy(line_y[k]), parts, size=size)
        if answer:
            fig.text(fx(x_answer), fy(line_y[0]), answer[0], ha="left", va="center", fontsize=size, weight=B,
                     color=answer[1])  # fmt: skip
            fig.text(fx(x_answer), fy(line_y[1]), source, ha="left", va="center", fontsize=size, color=MUTED)
    _save(fig, "fig02_datasets")


# ---- Fig. 3: the tools (p0b_tools) ------------------------------------------------------------------------------------
def fig03_tools() -> None:
    """The three tools as grids (layers x tokens), as p0b: the lens part teal, another entity's part blue; the bridge
    word's column outlined darker. The grids are figure patches (no axes: nothing here is a measurement)."""
    w, h = W.WIDTH, 3.15
    fig = plt.figure(figsize=(w, h), dpi=W.DPI)
    fx, fy = (lambda x: x / w), (lambda y: 1 - y / h)
    nl, nt, bridge, cell = 4, 7, 4, 0.27  # layers, tokens, the bridge word's token, a cell's side (in)
    panels = [("remove everywhere", "a band of layers, every token", {(r, t) for r in (1, 2) for t in range(nt)}, "lens"),
              ("remove from the patch", "one layer, the bridge word", {(2, bridge)}, "lens"),
              ("swap", "the bridge word, over the band", {(1, bridge), (2, bridge)}, "identity")]  # fmt: skip
    for k, (title, sub, cells, role) in enumerate(panels):
        x0 = 0.12 + k * 2.66
        fig.text(fx(x0), fy(0.12), title, ha="left", va="top", fontsize=W.FS["title"], weight="bold", color=INK)
        fig.text(fx(x0), fy(0.42), sub, ha="left", va="top", fontsize=W.FS["sub"], color=MUTED)
        gx, gy = x0 + 0.62, 0.92  # the grid's top-left corner (in)
        for r in range(nl):
            for t in range(nt):
                hit = (r, t) in cells
                edge = C[role] if hit else (MUTED if t == bridge else T.FAINT)
                fig.patches.append(Rectangle((fx(gx + t * cell + 0.015), fy(gy + (r + 1) * cell - 0.015)),
                                             (cell - 0.03) / w, (cell - 0.03) / h, transform=fig.transFigure,
                                             facecolor=C[role] if hit else "white", edgecolor=edge, lw=1.0))  # fmt: skip
        fig.text(fx(gx - 0.08), fy(gy + nl * cell / 2), "layers", ha="right", va="center", fontsize=W.FS["small"],
                 color=MUTED)  # fmt: skip
        fig.text(fx(gx + nt * cell / 2), fy(gy + nl * cell + 0.2), "tokens", ha="center", va="center",
                 fontsize=W.FS["small"], color=MUTED)  # fmt: skip
        fig.text(fx(gx + (bridge + 0.5) * cell), fy(gy - 0.12), "bridge", ha="center", va="center",
                 fontsize=W.FS["small"], color=MUTED)  # fmt: skip
    for k, (col, words) in enumerate([(C["lens"], "the lens part taken out"),
                                      (C["identity"], "another entity's lens part swapped in")]):  # fmt: skip
        x = 0.12 + k * 2.66
        fig.patches.append(Rectangle((fx(x), fy(h - 0.13)), 0.16 / w, 0.16 / h, transform=fig.transFigure,
                                     facecolor=col, edgecolor=col))  # fmt: skip
        fig.text(fx(x + 0.24), fy(h - 0.21), words, ha="left", va="center", fontsize=W.FS["key"], color=col)
    _save(fig, "fig03_tools")


# ---- Fig. 7: the routes (r5_routes) -------------------------------------------------------------------------------
def fig07_routes() -> None:
    """As r5: the lookup's answers when another item's locker moved, a 100% bar per model: by identity (blue), by
    position (orange), other (grey), 95% whiskers under each segment; the number itself in its own column. A post hoc
    row is hollow (its bars outlined)."""
    models = [(m, n) for m, n in DAN if D.s(m, "another item moved, whole: identity share")]
    rows = [Row(NAME[m], hollow=D.hollow(m, True)) for m, _ in models]

    def stack(ax, _rows):
        for i, (m, _) in enumerate(models):
            ids = D.s(m, "another item moved, whole: identity share")
            ps = D.s(m, "another item moved, whole: position share")
            idn, pos = ids[0], ps[0]
            hol = D.hollow(m, True)  # post hoc: hollow bars, not a tint
            for left, v, col in ((0, idn, C["identity"]), (idn, pos, C["address"]), (idn + pos, 1 - idn - pos, C["other"])):
                kw = ({"facecolor": "white", "edgecolor": col if col != C["other"] else C["control"], "linewidth": 2.2}
                      if hol else {"color": col})  # fmt: skip
                ax.barh(i, v, left=left, height=0.62, zorder=3, **kw)
            tc = INK if hol else "white"
            for x, v in ((idn / 2, idn), (idn + pos / 2, pos)):
                ax.text(x, i - 0.04, f"{v:.2f}", ha="center", va="center", fontsize=W.FS["value"] + 1, color=tc,
                        weight="bold", zorder=4)  # fmt: skip
            for (_v, lo, hi), x0 in ((ids, 0.0), (ps, idn)):  # 95% intervals: thin whiskers under each segment
                if lo is not None:
                    ax.plot([x0 + lo, x0 + hi], [i + 0.42] * 2, color=INK, lw=1.2, zorder=5)
                    for e in (x0 + lo, x0 + hi):  # end caps
                        ax.plot([e, e], [i + 0.37, i + 0.47], color=INK, lw=1.2, zorder=5)
        head_label(ax, 0.0, "by identity", C["identity"], ha="left")
        head_label(ax, 0.5, "by position", C["address"], ha="center")

    def number(i, _r):
        v = D.s(models[i][0], "another item moved, whole: value share")[0]
        return [(f"{v:.2f}", INK, "bold")]

    t = W.table(rows, [
        Col(5.25, "share of the lookup's answers", "after another item's locker moved", stack, (0, 1), [0, 0.5, 1],
            xlabel="share of the lookup's answers", cue="→ larger share"),
        Col(1.05, "the number", "itself", number, text=True),
    ], label_w=1.3, row_h=0.55,
        key=[[("●", C["other"], "other"), ("", MUTED, "whiskers: 95% interval")],
             [("", MUTED, "identity: the item's own locker · position: the locker now at its old place")]])  # fmt: skip
    t.render(f"{OUT}/fig07_routes.png", dpi=W.DPI)


# ---- Fig. 12: the pointer (r4_pointer) ----------------------------------------------------------------------------
def fig12_pointer() -> None:
    """As r4: conditions as rows, models as columns, every cell in points with its 95% interval (docs/breadth/data.csv
    ptr.*, probe.*). The paired difference "neutral sentence minus own passage" is a row of its own, in text, where no
    line runs (r4 printed it inside the panel)."""
    conds = [(("another entity D's", "own passage"), "lens"), (("one neutral sentence", "about D"), "lens"),
             (("without D's", "own-word directions"), "lens"), (("rotated (control)",), "control"),
             (("a probe's subspace", "(reads the fact)"), "neutral")]  # fmt: skip
    diff_label = ("neutral − own passage", "paired, points")
    labels = [c for c, _ in conds] + [diff_label]
    rows = [Row("") for _ in labels]
    n_dots = len(conds)
    models = [("q9", "Qwen 9B"), ("q27", "Qwen 27B"), ("nl", "Lightning")]
    lim = (-8, 92)

    def cells(k):
        return [D.b(f"ptr.{k}.swap"), D.b(f"ptr.{k}.neutral_pts"), D.b(f"ptr.{k}.noown_pts"), D.b(f"ptr.{k}.rot_pts"),
                D.b(f"probe.{k}.probe_pts")]  # fmt: skip

    def panel(k):
        def f(ax, _rows):
            cs = cells(k)
            for i, (cell, (_, col)) in enumerate(zip(cs, conds, strict=True)):
                if not cell:
                    W._missing(ax, i, lim)
                    continue
                dot(ax, cell[0], i, C[col], cell=cell, size=8 if col == "control" else 9.5)
            for i, (cell, (_, col)) in enumerate(zip(cs, conds, strict=True)):
                if cell:
                    W.value(ax, cell[0], i, cell, C[col], "{:.0f}", size=8 if col == "control" else 9.5)
            d = D.b(f"ptr.{k}.neutral_minus_swap")  # row 2 minus row 1 on the same items (scripts/ptr_intervals.py)
            if d:
                ax.text(sum(lim) / 2, n_dots, f"{d[0]:+.1f} [{d[1]:.1f}, {d[2]:.1f}]", ha="center", va="center",
                        fontsize=W.FS["value"], color=INK)  # fmt: skip
            else:
                W._missing(ax, n_dots, lim)

        return f

    t = W.table(rows, [Col(1.86, n, "", panel(k), lim, [0, 40, 80], xlabel="points", cue="→ more follow D")
                       for k, n in models], label_w=1.95, labels=False, row_h=0.56, skip_lines=(n_dots,), head=0.6, title_top=0.45,
                subtitle="D: another entity of the same kind · answers moved to D's fact",
                key=[[("●", C["lens"], "the lens part, from D"), ("●", C["control"], "rotated control")],
                     [("●", C["neutral"], "a probe's subspace: supervised comparison"),
                      ("", MUTED, "whiskers: 95% interval")]])  # fmt: skip

    def row_labels(fig):  # two-line labels in ink, regular weight (a bold name would not fit the column)
        top = t.head + T.SUBTITLE_H + 0.12
        for i, lines in enumerate(labels):
            y = top + (i + 0.5) * t.row_h
            for k, s in enumerate(lines):
                dy = (k - (len(lines) - 1) / 2) * 0.19
                fig.text(0.12 / fig.get_figwidth(), 1 - (y + dy) / fig.get_figheight(), s, ha="left", va="center",
                         fontsize=W.FS["text"], color=INK if i < n_dots else MUTED)  # fmt: skip

    t.extra.append(row_labels)
    t.render(f"{OUT}/fig12_pointer.png", dpi=W.DPI)


# ---- Fig. 13: the last token (r3_last_token) ----------------------------------------------------------------------
def fig13_last_token() -> None:
    """As r3: at the recall's last token, a probe reads the entity from the lens part (left), yet the lens part swapped
    in switches almost no recalls, against the whole state swapped in (grey, right). A post hoc row is hollow."""
    rx_r = r"51\.10: recall, last token, read peak layer (\d+): the probe's accuracy"
    rows, cells = [], []
    for m, _ in DAN:
        r = D.s_match(m, rx_r, "fig17_jspace_last_token")
        if not r:
            continue
        sw = D.s_match(m, r"51\.10: recall, last token, read peak layer \d+: the lens swap's switches over",
                       "fig17_jspace_last_token")  # fmt: skip
        mm = re.search(r"\(([\d.]+) / ([\d.]+)\)", sw[0])
        lens_abs, whole = float(mm.group(1)), float(mm.group(2))
        layer = re.search(r"layer (\d+)", r[0]).group(1)
        chance = D.s(m, "51.10: the read probe's chance (locker-first rows)")[0]
        rows.append(Row(NAME[m], sub=f"layer {layer}"))
        cells.append((m, r[1], lens_abs, whole, chance))

    def read(ax, _rows):
        vrule(ax, max(c[4] for c in cells), len(cells), "chance")
        for i, (m, rd, *_r) in enumerate(cells):
            dot(ax, rd[0], i, C["recall"], D.hollow(m), cell=rd)
        for i, (_m, rd, *_r) in enumerate(cells):
            W.value(ax, rd[0], i, rd, C["recall"], "{:.2f}")
        head_label(ax, 1.02, "probe on the lens part", C["recall"], ha="right")

    def used(ax, _rows):
        for i, (m, _rd, la, wh, _c) in enumerate(cells):
            connector(ax, la, wh, i)
            dot(ax, wh, i, C["control"], D.hollow(m), size=8)
            dot(ax, la, i, C["lens"], D.hollow(m))
        for i, (_m, _rd, la, _wh, _c) in enumerate(cells):  # the values in a column left of the zero line
            ax.text(-0.06, i, f"{la:.2f}", ha="right", va="center", fontsize=W.FS["value"], color=C["lens"])
        head_label(ax, -0.2, "lens part swapped in", C["lens"], ha="left")
        head_label(ax, 1.02, "whole state", MUTED, ha="right", weight="normal")

    t = W.table(rows, [
        Col(3.05, "probe accuracy on the lens part", "the recall's entity, at the last token", read, (0, 1.02),
            [0, 0.5, 1.0], xlabel="accuracy", cue="→ more readable"),
        Col(3.05, "recalls switched", "swapped in: lens part vs whole state", used, (-0.25, 1.05),
            [0, 0.5, 1.0], xlabel="share of recalls switched", cue="→ used more"),
    ], label_w=1.35)  # fmt: skip
    t.render(f"{OUT}/fig13_last_token.png", dpi=W.DPI)


FIGS = {"fig02_datasets": fig02_datasets, "fig03_tools": fig03_tools, "fig07_routes": fig07_routes,
        "fig12_pointer": fig12_pointer, "fig13_last_token": fig13_last_token}  # post order; fixed names  # fmt: skip
