"""The READMEs' own table-style figures beside exemplars.py's r1-r5: the 2x2 (depth, the 01:58 brief) and the
datasets figure (root README, p0a; Dan 30 Oct: redrawn in the table style, no title inside)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit.dottable import INK, MUTED, C, Col, Row, Table, dot

# (column title, the gap's quantity, its control's quantity). One quantity in all four columns (Dan 30 Oct):
# gap = the recall's loss - the lookup's loss, each as a share of that reader's own answers; 0 = no difference between
# the readers, 1 = the recall loses everything and the lookup nothing; positive = the recall loses more. One layer: the
# share of the whole patch's switches lost without the lens part, beyond a random part of the same size. Band: the share
# of the reader's answers lost beyond a random part (rung 6; Zach's stored M - K for his passages). Verified for the 9B
# from the per-item rows (results/x49_ladder/qwen35_9b_x49_2/outcomes.jsonl): cost(recall) - cost(lookup) = 0.3213 and
# the control's gap 0.0144, the numbers in data.csv; the sign is positive when the recall loses more.
TWO_BY_TWO = [
    ("locker scenes", "our removal, our scenes (main test): gap",
     "our removal, our scenes (main test): the control (a random part of the same size instead), recall minus lookup"),
    ("fact passages", "our removal, his passages: gap",
     "our removal, his passages: the control (a random part of the same size instead), recall minus lookup"),
    ("locker scenes", "Zach's operation, our scenes (rung 6): recall's cost minus the lookup's, every scene",
     "Zach's operation, our scenes (rung 6): the control (a random part of the same size instead), recall minus lookup, "
     "every scene (kept with none minus kept with the random part)"),
    ("fact passages", "Zach's operation, his passages: his stored recall minus lookup",
     "Zach's operation, his passages: his rotated-direction control, recall minus lookup"),
]  # fmt: skip
SWITCHES = "our removal, his passages: lookup switches under the whole change"  # col 2: a lookup with < 30 switches
XLIM, XTICKS = (-0.25, 1.0), [0, 0.5, 1]


def _n(model: str, quantity: str):
    """The n column of a data.csv row (the story cache keeps values only)."""
    import csv

    with (D.REPO / "data/figures/depth/data.csv").open() as f:
        for r in csv.DictReader(f):
            if r["model"] == model and r["quantity"] == quantity:
                return int(float(r["n"])) if r["n"] else None
    return None


def two_by_two():
    """Fig. 12: both operations on both datasets, one unit in every column: recall minus lookup, share lost. The grey dot
    is the same gap with a same-size control; a missing cell says why in the cell."""
    models = X.DAN
    rows = [Row(X.NAME[m]) for m, _ in models]
    LT = "nemotron-3.5-lightning"

    def col(k):
        _t, q, qc = TWO_BY_TWO[k]

        def f(ax, _r):
            for i, (m, _) in enumerate(models):
                v, c = D.s(m, q), D.s(m, qc)
                if not v:
                    if k == 1 and (sw := D.s(m, SWITCHES)):
                        why = f"too few switches ({sw[0]:.0f} of {_n(m, SWITCHES)})"
                    elif k == 2 and m == LT:
                        why = "below gate"
                    else:
                        why = "–"
                    ax.text(0.06 if len(why) > 3 else XLIM[0] + 0.04, i, why, ha="left", va="center", color=MUTED, fontsize=10.5 if len(why) > 3 else 12)
                    continue
                if c:  # a little below the gap's dot, so a control close to the gap is not hidden behind it
                    dot(ax, c[0], i + 0.2, C["control"], size=7, cell=c if c[1] is not None else None)
                cell = v if len(v) == 3 and v[1] is not None else None
                dot(ax, v[0], i - 0.08, C["recall"], D.hollow(m), cell=cell, value=v[0],
                    vside="left" if (cell[2] if cell else v[0]) > 0.8 else "right")  # a high value's label stays in its panel

        return f

    cols = [Col(2.3, t, "", col(k), XLIM, XTICKS, xlabel="recall − lookup, share lost", cue="→ recall depends more")
            for k, (t, _q, _c) in enumerate(TWO_BY_TWO)]
    key = [[("●", C["recall"], "gap: recall − lookup"),
            ("●", C["control"], "grey: the same gap with a same-size control"),
            ("–", MUTED, "no result (the reason is in the cell)")],
           [("", MUTED, "control: a random part (one layer; band · locker scenes), rotated directions (band · fact passages)")],
           [("", MUTED, "the control's interval is drawn in the two band columns; the one-layer controls are drawn without one")]]
    t = Table(rows, cols, label_w=1.45, head=0.93, labels=False, key=key)
    width = t.label_w + sum(c.width for c in cols) + t.pad * (len(cols) + 1)

    def groups(fig):  # a group title over each pair of columns: the operation
        for g, w in enumerate(["one layer", "band of layers"]):
            x = t.label_w + t.pad + (cols[0].width + cols[1].width + 2 * t.pad) * g
            fig.text(x / width, 1 - 0.06 / fig.get_figheight(), w, ha="left", va="top", fontsize=12.5, weight="bold",
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
