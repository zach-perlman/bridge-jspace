"""The depth README's own table-style figures (the 01:58 brief, Section 2), beside exemplars.py's r1-r5."""

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

    cols = [Col(2.15, t, u, col(k), (-0.3, 1.0), [0, 0.5, 1]) for k, (t, u, _q, _c) in enumerate(TWO_BY_TWO)]
    key = [("●", C["recall"], "recall minus lookup"),
           ("●", C["control"], "control: the same removal with a random part (a band: rotated directions)"),
           ("○", C["recall"], "post hoc")]  # fmt: skip
    t = Table(rows, cols, label_w=1.45, head=1.25, labels=False, key=key)
    width = t.label_w + sum(c.width for c in cols) + t.pad * (len(cols) + 1)

    def groups(fig):  # a group title over each pair of columns, as f9_where
        for g, w in enumerate(["Removed from the patch (one layer)", "Removed everywhere (a band of layers)"]):
            x = t.label_w + t.pad + (cols[0].width + cols[1].width + 2 * t.pad) * g
            fig.text(x / width, 1 - 0.12 / fig.get_figheight(), w, ha="left", va="top", fontsize=12.5, weight="bold",
                     color=INK)  # fmt: skip

    t.extra.append(groups)
    t.render(f"{X.OUT}/t12_two_by_two.png")
