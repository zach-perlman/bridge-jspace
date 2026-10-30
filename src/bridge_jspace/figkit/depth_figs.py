"""The READMEs' own table-style figures beside exemplars.py's r1-r5: the 2x2 (depth, the 01:58 brief) and the
datasets figure (root README, p0a; Dan 30 Oct: redrawn in the table style, no title inside)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit.dottable import INK, MUTED, C, Col, Row, Table, dot

# (title, unit, the gap's quantity, its control's quantity); a quantity with no row for a model is a grey en dash
TWO_BY_TWO = [
    ("locker scenes", "share of switches", "our removal, our scenes (main test): gap",
     "our removal, our scenes (main test): the control (a random part of the same size instead), recall minus lookup"),
    ("fact passages", "share of switches", "our removal, his passages: gap",
     "our removal, his passages: the control (a random part of the same size instead), recall minus lookup"),
    ("locker scenes", "share of answers kept", "Zach's operation, our scenes (rung 6): recall's cost minus "
     "the lookup's, every scene", "Zach's operation, our scenes (rung 6): the control (a random part of the same size "
     "instead), recall minus lookup, every scene (kept with none minus kept with the random part)"),
    ("fact passages", "share of answers", "Zach's operation, his passages: his stored recall "
     "minus lookup", "Zach's operation, his passages: his rotated-direction control, recall minus lookup"),
]  # fmt: skip
# the Muse's rung 6 ran at L23-29, outside Zach's band (L36-42): ink vs grey, said in the caption (S3: hollow means
# only "post hoc")
OFF_BAND = {("muse-glimmer-30b", 2)}


def two_by_two():
    """Fig. 12: both operations on both datasets, recall minus lookup per model; the control a small grey dot."""
    models = X.DAN
    rows = [Row(X.NAME[m]) for m, _ in models]

    def col(k):
        _t, _u, q, qc = TWO_BY_TWO[k]

        def f(ax, _r):
            for i, (m, _) in enumerate(models):
                v, c = D.s(m, q), D.s(m, qc)
                if not v:
                    ax.text(0.08, i, "–", ha="left", va="center", color=MUTED, fontsize=12)
                    continue
                if c:
                    dot(ax, c[0], i, C["control"], size=7)
                col_ = MUTED if (m, k) in OFF_BAND else C["recall"]
                cell = v if len(v) == 3 and v[1] is not None else None
                dot(ax, v[0], i, col_, D.hollow(m), cell=cell, value=v[0])

        return f

    xl = ("share of switches lost", "share of switches lost", "share of answers lost", "share of answers lost")
    cols = [
        Col(2.15, t, "recall − lookup", col(k), (-0.3, 1.0), [0, 0.5, 1], xlabel=xl[k])
        for k, (t, _u, _q, _c) in enumerate(TWO_BY_TWO)
    ]
    key = [("●", C["recall"], "recall minus lookup"),
           ("●", C["control"], "control: a random part (rotated directions in a band)"),
           ("●", MUTED, "Muse: L23-29, off the band")]  # fmt: skip
    t = Table(rows, cols, label_w=1.45, head=1.25, labels=False, key=key)
    width = t.label_w + sum(c.width for c in cols) + t.pad * (len(cols) + 1)

    def groups(fig):  # a group title over each pair of columns, as f9_where
        for g, w in enumerate(["Removed from the patch (one layer)", "Removed everywhere (a band of layers)"]):
            x = t.label_w + t.pad + (cols[0].width + cols[1].width + 2 * t.pad) * g
            fig.text(x / width, 1 - 0.12 / fig.get_figheight(), w, ha="left", va="top", fontsize=12.5, weight="bold",
                     color=INK)  # fmt: skip

    t.extra.append(groups)
    t.render(f"{X.OUT}/t12_two_by_two.png")


def datasets():
    """p0a: the two kinds of prompt as a table. Rows: the fact passages (question, the lookup's passage, the recall's)
    and the locker scenes (scene, lookup question, recall question); the bridge in bold; the answer and where it comes
    from in the right column, lookup purple, recall ink."""
    B = "bold"

    def words(*parts):
        return [(t, INK, B if bold else "normal") for t, bold in parts]

    rows = [
        (Row("Fact passages"), words(("Question: ", False), ("The composer who wrote The Magic Flute", True),
                                     (" was of which nationality?", False)), []),
        (Row("", "lookup"), words(("“… ", False), ("Mozart", True), (" was Austrian by birth. …”", False)),
         [("Austrian", C["lookup"], B), ("  in the passage", MUTED, "normal")]),
        (Row("", "recall"), words(("“… A reader asked a question about ", False), ("Mozart", True),
                                  (" in the letters page. …”", False)),
         [("Austrian", C["recall"], B), ("  from memory", MUTED, "normal")]),
        (Row("Locker scenes"), words(("The locker of carbon is 3. The locker of helium is 5. Eric picked ", False),
                                     ("carbon", True), (".", False)), []),
        (Row("", "lookup"), words(("Which locker belongs to Eric's pick?", False)),
         [("3", C["lookup"], B), ("  in the scene", MUTED, "normal")]),
        (Row("", "recall"), words(("What is the atomic number of Eric's pick?", False)),
         [("6", C["recall"], B), ("  from memory", MUTED, "normal")]),
    ]  # fmt: skip
    t = Table([r for r, _, _ in rows],
              [Col(7.6, "Prompt", "the bridge in bold", lambda i, _r: rows[i][1], text=True),
               Col(2.1, "Answer", "and its source", lambda i, _r: rows[i][2] or [("", MUTED, "normal")], text=True)],
              label_w=1.75, labels=False)  # fmt: skip
    t.render(f"{X.OUT}/p0a_datasets.png")


def tools():
    """p0b: the three tools as grids (layers x tokens), no prose inside the image (G9, Dan 30 Oct review); the colours
    are the roles' (the lens part teal, another entity's part blue). Horizontal text only."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    from bridge_jspace.figkit import dottable as T
    from bridge_jspace.figkit import lint

    fig = plt.figure(figsize=(10.5, 3.3), dpi=160)
    nl, nt = 4, 7
    panels = [("remove everywhere", "a band of layers, every token", {(1, t) for t in range(nt)} | {(2, t) for t in range(nt)}, "lens"),
              ("remove from the patch", "one layer, the bridge word", {(2, 4)}, "lens"),
              ("swap", "the bridge word, over the band", {(1, 4), (2, 4)}, "identity")]  # fmt: skip
    for k, (title, sub, cells, role) in enumerate(panels):
        x0 = 0.04 + k * 0.325
        fig.text(x0, 0.93, title, ha="left", va="top", fontsize=13, weight="bold", color=T.INK)
        fig.text(x0, 0.83, sub, ha="left", va="top", fontsize=11.5, color=T.MUTED)
        ax = fig.add_axes((x0 + 0.04, 0.2, 0.25, 0.5))
        ax.set_xlim(0, nt)
        ax.set_ylim(nl, 0)
        ax.axis("off")
        for r in range(nl):
            for t in range(nt):
                hit = (r, t) in cells
                ax.add_patch(
                    Rectangle(
                        (t + 0.06, r + 0.08),
                        0.88,
                        0.84,
                        facecolor=T.C[role] if hit else "white",
                        edgecolor=T.C[role] if hit else T.FAINT,
                        lw=1.0,
                    )
                )
        fig.text(x0 + 0.035, 0.45, "layers", ha="right", va="center", fontsize=11.5, color=T.MUTED)
        fig.text(
            x0 + 0.165, 0.12, "tokens (the bridge word marked)", ha="center", va="center", fontsize=11.5, color=T.MUTED
        )
    for k, (col, words) in enumerate(
        [(T.C["lens"], "the lens part taken out"), (T.C["identity"], "another entity's lens part written in")]
    ):
        x = 0.04 + k * 0.3
        fig.patches.append(Rectangle((x, 0.015), 0.02, 0.06, transform=fig.transFigure, facecolor=col, edgecolor=col))
        fig.text(x + 0.03, 0.045, words, ha="left", va="center", fontsize=11.5, color=col)  # the coloured word is the legend
    probs = lint.table_problems(fig, "p0b_tools")
    from bridge_jspace.figkit import tables

    tables.PROBLEMS.extend(probs)
    fig.savefig(f"{X.OUT}/p0b_tools.png", dpi=160, facecolor="white")
    plt.close(fig)
