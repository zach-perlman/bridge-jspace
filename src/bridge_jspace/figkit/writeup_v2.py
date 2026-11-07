"""The write-up's figures in grammar v2 (docs/shared/figure_style.md), the pilot: the key figure, Fig. 1, 4, 9, 12 and
appendix B f17 (with its heads panel as appB_f17b_heads). Every mark goes through figkit/grammar.py (role tag, status
from data/figures/status.csv), every word comes from figkit/terms.py, every number through grammar.num (one precision
per unit). Same file names as v1; the values are the v1 figures' (presentation only)."""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import grammar as G
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit import terms as TM
from bridge_jspace.figkit import writeup_figs as W
from bridge_jspace.figkit.dottable import INK, MUTED, Col, Row
from bridge_jspace.palette import ROLE

OUT = "."
PROBLEMS: list[str] = []
DAN, NAME, ZK = W.DAN, W.NAME, W.ZK
ZK_MODEL = {k: m for m, k in ZK.items()}
U = TM.UNIT
TWIN = W.TWIN_MODELS


def _val(ax, x, y, cell, role, text, i=None, size=9.5):
    """A printed value beside its dot (writeup_figs.value: clear of every line and mark), already formatted."""
    return W.value(ax, x, y, cell, ROLE[role], text.replace("{", "{{").replace("}", "}}"), i=i, size=size)


def _col(width, title, draw, xlim, xticks, unit, sub="", **kw):
    xl = U[unit] if width >= 2.2 else U[unit].replace(" (", "\n(")  # a narrow panel: the unit on its own line
    return Col(width, title, sub, draw, xlim, xticks, xlabel=xl, cue=TM.cue(unit), **kw)


def _render(t: T.Table, fig_id: str) -> None:
    G.begin(fig_id)
    t.key = G.key  # built from what was drawn (the dot table renders twice)
    t.render(f"{OUT}/{fig_id}.png", dpi=W.DPI)


def _stack(tables, fid):
    """Panels one under the other; one key line under the last, naming what every panel draws."""
    from PIL import Image

    G.begin(fid)
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for k, t in enumerate(tables):
            p = Path(tmp) / f"{fid}_{k}.png"
            last = k == len(tables) - 1
            G.FIGURE["defer_key"] = not last
            t.key = G.key if last else []
            t.hollow_key = last
            t.render(str(p), dpi=W.DPI)
            parts.append(Image.open(p).convert("RGB"))
        sheet = Image.new("RGB", (parts[0].width, sum(p.height for p in parts)), "white")
        y = 0
        for p in parts:
            sheet.paste(p, (0, y))
            y += p.height
        sheet.save(f"{OUT}/{fid}.png", dpi=(W.DPI, W.DPI))


def _note(text):
    """One grey line at the top of a panel."""
    return lambda fig: fig.text(0.12 / fig.get_figwidth(), 1 - 0.08 / fig.get_figheight(), text, ha="left", va="top",
                                fontsize=W.FS["sub"], color=MUTED)  # fmt: skip


# ---- Fig. 1: the main split, the two tests stacked ---------------------------------------------------------------------
def fig01_main_split() -> None:
    """Top, band of layers (fact passages): each reader's accuracy drop under the knock-out; the gap with its 95%
    whisker and the largest same-size control as a grey tick on the gap's axis. Bottom, one layer (locker scenes): each
    reader's switches blocked on the grey band, and the gap. Muse 30B and Qwen 122B in the band test: post hoc
    (hollow), in their role colours, tagged "not claimed: <reason>" on the row's lower line."""
    fid = "fig01_main_split"
    # the band cells the post does not claim say so on the row's grey second line (its box masks the lines it crosses)
    rows = [Row(NAME[m], sub=W.NOT_CLAIMED.get(ZK[m], "")) for m, _ in DAN]

    def lifted(k):  # marks on the upper line where the lower line holds a tag or a note
        return k in W.NOT_CLAIMED or D.x(f"contrast_{D.SHORT.get(ZK_MODEL[k], '-')}") is None

    def drops(ax, _r):
        for i, (m, _) in enumerate(DAN):
            k = ZK[m]
            y = i - (W.LIFT if lifted(k) else 0)
            lk, rc = D.b(f"ko.{k}.lostK"), D.b(f"ko.{k}.lostM")
            G.connector(ax, lk[0], rc[0], y)
            G.mark(ax, lk[0], y, "lookup", f"band.{k}")
            G.mark(ax, rc[0], y, "recall", f"band.{k}")
        G.role_word(ax, 0, "lookup", "lookup", ha="left")
        G.role_word(ax, 70, "recall", "recall", ha="right")

    def gap(ax, _r):
        for i, (m, _) in enumerate(DAN):
            k = ZK[m]
            y = i - (W.LIFT if lifted(k) else 0)
            mk = D.b(f"ko.{k}.mk")
            G.tick(ax, S.ctrl(k), y)
            G.mark(ax, mk[0], y, "recall", f"band.{k}", interval=mk)
            _val(ax, mk[0], y, mk, "recall", G.num(f"ko.{k}.mk", mk[0], "points"), i=i)

    def shares(ax, _r):
        G.band(ax, len(DAN))
        for i, (m, _) in enumerate(DAN):
            k = ZK[m]
            y = i - (W.LIFT if lifted(k) else 0)
            rc, lk = S.conflict(m, "recall"), S.conflict(m, "lookup")
            G.connector(ax, lk[0], rc[0], y)
            G.mark(ax, lk[0], y, "lookup", f"layer.{k}", interval=lk)
            G.mark(ax, rc[0], y, "recall", f"layer.{k}", interval=rc)
        G.role_word(ax, -0.2, "lookup", "lookup", ha="left")
        G.role_word(ax, 1.0, "recall", "recall", ha="right")

    def layer_gap(ax, _r):
        for i, (m, _) in enumerate(DAN):
            k = ZK[m]
            y = i - (W.LIFT if lifted(k) else 0)
            g = D.x(f"contrast_{D.SHORT.get(m, '-')}")
            if g is None:  # aggregate only: the difference of the two shares, no interval
                g = (S.conflict(m, "recall")[0] - S.conflict(m, "lookup")[0], None, None)
                W.lower(ax, ax.get_xlim()[1], i, "no interval", ha="right")
            G.mark(ax, g[0], y, "recall", f"layer.{k}", interval=g if g[1] is not None else None)
            _val(ax, g[0], y, g, "recall", G.num(f"contrast.{k}", g[0], "share"), i=i)

    # the two tests side by side, each in its own two panels with its own units (a gutter between them)
    t = W.table(rows, [
        _col(1.5, "accuracy drop", drops, (-4, 70), [0, 30, 60], "drop"),
        _col(1.45, "gap:\nrecall − lookup", gap, (-4, 98), [0, 30, 60], "gap"),
        Col(0.12, gutter=True),
        _col(1.45, "switches blocked", shares, (-0.25, 1.0), [0, 0.5, 1.0], "switches"),
        _col(1.45, "gap:\nrecall − lookup", layer_gap, (-0.1, 1.1), [0, 0.5, 1.0], "gap_share"),
    ], label_w=1.05, head=1.0, title_top=0.42, sub_lift=True, row_h=0.6)  # fmt: skip

    def tag(fig):  # the registry check reads which cell a "not claimed" line belongs to
        for t_ in fig.texts:
            for m, _ in DAN:
                if t_.get_text() == W.NOT_CLAIMED.get(ZK[m]):
                    G.tag_text(t_, f"band.{ZK[m]}", t_.get_text())

    t.extra.append(tag)
    t.extra.append(W._groups((W._x_of(t, 0), "Band of layers · fact passages"),
                             (W._x_of(t, 3), "One layer · locker scenes")))  # fmt: skip
    _render(t, fid)


# ---- Fig. 4: the twin set --------------------------------------------------------------------------------------------
LANES = (("paper10", -0.24, None), ("paper10_rot", 0.0, "control"), ("paper10_keepA", 0.24, "answer"))


def fig04_twin_set() -> None:
    """Rows are models (the items, recall / lookup, on the row's second line); columns recall twins, lookup twins, gap.
    In a cell three lanes: the knock-out (the reader's colour), rotated (grey), answer span kept (brick), named by
    coloured words above the first row. The unedited accuracy is one grey line (its range over every model)."""
    fid = "fig04_twin_set"
    rows = []
    for k, name in TWIN:
        nr, nl = W.writeup_n(f"fig04.recall.unedited.{k}"), W.writeup_n(f"fig04.lookup.unedited.{k}")
        rows.append(Row(name, sub=f"{nr} / {nl} items" if nr and nl else ""))
    acc_lim, gap_lim = (-4, 106), (-12, 74)

    def accuracy(reader):
        def f(ax, _r):
            for i, (k, _) in enumerate(TWIN):
                for cond, dy, role in LANES:
                    c = W.w(f"fig04.{reader}.{cond}.{k}")
                    role = role or reader
                    G.mark(ax, c[0], i + dy, role, f"{reader}.{cond}.{k}", size=8.5,
                           name="rotated" if role == "control" else "")  # fmt: skip
                    _val(ax, c[0], i + dy, None, role, G.num(f"fig04.{reader}.{cond}.{k}", c[0], "accuracy"),
                         size=8.5)  # fmt: skip
            G.role_word(ax, -4, "knock-out", reader, ha="left")
            G.role_word(ax, 106, "answer span kept", "answer", ha="right", level=1)

        return f

    def gap(ax, _r):
        for i, (k, _) in enumerate(TWIN):
            for cond, dy, role in LANES[:2]:
                c = W.w(f"fig04.gap.{cond}.{k}")
                role = role or "recall"
                G.mark(ax, c[0], i + dy, role, f"gap.{cond}.{k}", interval=c, size=8.5,
                       name="rotated" if role == "control" else "")  # fmt: skip
                _val(ax, c[0], i + dy, c, role, G.num(f"fig04.gap.{cond}.{k}", c[0], "points"), size=8.5)
        G.role_word(ax, 74, "knock-out", "recall", ha="right")

    t = W.table(rows, [
        _col(2.05, "recall twins", accuracy("recall"), acc_lim, [0, 50, 100], "accuracy"),
        _col(2.05, "lookup twins", accuracy("lookup"), acc_lim, [0, 50, 100], "accuracy"),
        _col(2.05, "gap: recall − lookup", gap, gap_lim, [0, 30, 60], "gap"),
    ], label_w=1.15, row_h=0.8, head=0.95, title_top=0.45)  # fmt: skip
    unedited = [c[0] for r in ("recall", "lookup") for k, _ in TWIN if (c := W.w(f"fig04.{r}.unedited.{k}"))]
    if len(unedited) == 2 * len(TWIN):  # "every model" only when every cell has its source
        lo, hi = round(min(unedited)), round(max(unedited))
        t.extra.append(_note(f"unedited: {lo}–{hi}% right on every model" if lo != hi else
                             f"unedited: {lo}% right on every model"))  # fmt: skip
    _render(t, fid)


# ---- Fig. 9: sentence order ----------------------------------------------------------------------------------------
def fig09_order() -> None:
    """Per model two sub-rows, the sentence (locker or fact) before the pick and after it, both purple: a second
    condition of the lookup is a sub-row named in words, never a shade. Left locker scenes, right fact passages."""
    from bridge_jspace.figkit import claim_figs as CF

    fid = "fig09_order"
    models = [(m, n) for m, n in DAN if D.s(m, CF.ORDER_Q.format("before the pick"), "fig03")]
    rows, at = [], []
    for m, _ in models:
        rows.append(Row(NAME[m]))
        at.append((m, None))
        for when, label in (("first", "sentence before the pick"), ("after", "sentence after the pick")):
            rows.append(Row("", sub=label))
            at.append((m, when))
    heads = tuple(i for i, (_, w) in enumerate(at) if w is None)
    lim = (-0.05, 1.2)

    def cells(ds, m):
        if ds == "locker":
            return {"first": D.s(m, CF.ORDER_Q.format("before the pick"), "fig03"),
                    "after": D.s(m, CF.ORDER_Q.format("after the pick"), "fig03")}  # fmt: skip
        if m not in CF.ZACH_L:
            return None
        return {"first": D.s(m, CF.ZACH_Q.format(CF.ZACH_L[m], "first"), "fig03"),
                "after": D.s(m, CF.ZACH_Q.format(CF.ZACH_L[m], "after"), "fig03")}  # fmt: skip

    def lane(ds):
        def f(ax, _r):
            for i, (m, when) in enumerate(at):
                if when is None:
                    continue
                cs = cells(ds, m)
                if cs is None:
                    if when == "first":
                        W._missing(ax, i + 0.5, lim, "no run")
                    continue
                c = cs[when]
                G.mark(ax, c[0], i, "lookup", f"{ds}.{when}.{ZK[m]}", interval=c)
                _val(ax, c[0], i, c, "lookup", G.num(f"order.{ds}.{when}.{ZK[m]}", c[0], "share"))
            G.role_word(ax, lim[1], "lookup", "lookup", ha="right")

        return f

    t = W.table(rows, [
        _col(2.85, "Locker scenes", lane("locker"), lim, [0, 0.5, 1], "lookups_switched", zero=False),
        _col(2.85, "Fact passages", lane("facts"), lim, [0, 0.5, 1], "lookups_switched", zero=False),
    ], label_w=1.9, row_h=0.34, group=3, skip_lines=heads, head=0.55, title_top=0.12)  # fmt: skip
    _render(t, fid)


# ---- Fig. 12: the pointer, models as rows ------------------------------------------------------------------------------
PTR = (("swap", ("another entity's own passage", ""), "lens"),
       ("neutral", ("one neutral sentence", "about another entity"), "lens"),
       ("noown", ("without own-word\ndirections", ""), "lens"),
       ("rot", ("rotated", ""), "control"))  # fmt: skip
PTR_KEY = {"swap": "swap", "neutral": "neutral_pts", "noown": "noown_pts", "rot": "rot_pts"}


def _ptr_n(k):
    with (D.REPO / "docs/breadth/data.csv").open() as f:
        return next((r["n"] for r in csv.DictReader(f) if r["key"] == f"ptr.{k}.swap"), "")


def fig12_pointer() -> None:
    """Models are rows (the pointer run's items on the row's second line); the conditions are columns, two per panel:
    another entity's own passage and one neutral sentence about it on top; without its own-word directions and rotated
    below, beside the paired difference neutral sentence − own passage."""
    fid = "fig12_pointer"
    rows = [Row(n, sub=f"{_ptr_n(k)} items" if _ptr_n(k) else "") for k, n in TWIN]
    lim = (-8, 96)

    def panel(cond, role):
        def f(ax, _r):
            for i, (k, _) in enumerate(TWIN):
                c = D.b(f"ptr.{k}.{PTR_KEY[cond]}")
                if not c:
                    W._missing(ax, i, lim, "no run")
                    continue
                G.mark(ax, c[0], i, role, f"{cond}.{k}", interval=c, name="rotated" if role == "control" else "")
                _val(ax, c[0], i, c, role, G.num(f"ptr.{k}.{PTR_KEY[cond]}", c[0], "points"))
            if role != "control":
                G.role_word(ax, lim[1], "lens part swapped in", "lens", ha="right")

        return f

    def diff(i, _r):
        k = TWIN[i][0]
        d = D.b(f"ptr.{k}.neutral_minus_swap")
        if not d:
            return [("no run", MUTED, "normal")]
        key = f"ptr.{k}.neutral_minus_swap"
        return [(G.num(key, d[0], "points", sign=True), INK, "bold"),
                ("  " + G.interval(key, d[1], d[2], "points"), MUTED, "normal")]  # fmt: skip

    def table(conds, extra_col=False):
        w = 1.95 if extra_col else 3.05
        cols = [_col(w, title, panel(cond, role), lim, [0, 40, 80], "moved", sub=sub)
                for cond, (title, sub), role in conds]  # fmt: skip
        if extra_col:
            cols.append(Col(1.85, "neutral sentence −\nown passage", "", diff, text=True))
        return W.table(rows, cols, label_w=1.15, head=0.8, title_top=0.32, row_h=0.48, foot=0.4)

    top, bottom = table(PTR[:2]), table(PTR[2:], extra_col=True)
    top.extra.append(_note("another entity: one of the same kind · answers moved to its fact"))
    bottom.extra.append(_note("the pointer runs: a different item set from Fig. 6's swap"))
    _stack([top, bottom], fid)


# ---- appendix B f17: attention under the address swap; f17b: the top 10 heads ------------------------------------------
ATT = "attention mass on slot {}'s locker sentence, {} (mean of five heads, read half)"
ATT_Q = (("switched", "the swap, answer switched", "address", "", "answer switched"),
         ("stayed", "the swap, answer stayed", "address", "", "answer stayed"),
         ("nochange", "no change, switched pairs", "control", "no change", "no change"),
         ("random", "a random vector, switched pairs", "control", "a random vector", "a random vector"))  # fmt: skip


def appB_f17_attention() -> None:
    """Per model four sub-rows (the address swap with the answer switched, with it staying; no change; a random
    vector), the last token's attention on the old and the new locker sentence: dots, orange for the swap (the
    intervention whose effect is drawn), grey for the two controls, each named on its sub-row."""
    fid = "appB_f17_attention"
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
    rows, at = [], []
    for m in models:
        rows.append(Row(NAME[m]))
        at.append((m, None))
        for q, *_, label in ATT_Q:
            rows.append(Row("", sub=label))
            at.append((m, q))
    heads = tuple(i for i, (_, q) in enumerate(at) if q is None)
    lim = (-0.04, 1.0)

    def attention(slot):
        def f(ax, _r):
            for i, (m, q) in enumerate(at):
                if q is None:
                    continue
                _, quantity, role, name, _l = next(a for a in ATT_Q if a[0] == q)
                v = D.s(m, ATT.format(slot, quantity), "fig13")
                cell = f"att.{'old' if slot == 'j' else 'new'}.{q}.{ZK[m]}"
                ci = v if role != "control" else None
                G.mark(ax, v[0], i, role, cell, interval=ci, size=8.5, name=name)
                _val(ax, v[0], i, ci, role, G.num(f"att.{slot}.{q}.{ZK[m]}", v[0], "share"), size=8.5)
            G.role_word(ax, lim[1], "address swap", "address", ha="right")

        return f

    t = W.table(rows, [
        _col(2.95, "old locker sentence", attention("j"), lim, [0, 0.5, 1], "attention"),
        _col(2.95, "new locker sentence", attention("k"), lim, [0, 0.5, 1], "attention"),
    ], label_w=1.7, row_h=0.32, group=5, skip_lines=heads, head=0.55, title_top=0.12)  # fmt: skip
    _render(t, fid)


def appB_f17b_heads() -> None:
    """Zeroing the top 10 heads against 10 random heads (the share of the address swap's switches cut), with the bar
    fixed in advance; the numbers beside."""
    fid = "appB_f17b_heads"
    hm = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
    cut = lambda m: D.s(m, "last token, top 10: share of the swap's switch cut", "ledger_heads")  # noqa: E731
    rnd = lambda m: D.s(m, "last token, top 10: random sets' mean cut", "ledger_heads")  # noqa: E731
    bar = 0.5  # the rule fixed in advance (curve_figs.f_attention's "rule: 0.5")

    def heads(ax, _r):
        G.rule(ax, bar, len(hm))
        T.head_label(ax, bar, TM.RULE_BAR.format(G.num("heads.bar", bar, "share")), MUTED, ha="center", weight="normal")
        for i, m in enumerate(hm):
            G.mark(ax, rnd(m)[0], i, "control", f"heads.random10.{ZK[m]}", size=8, name="10 random heads")
            G.mark(ax, cut(m)[0], i, "address", f"heads.top10.{ZK[m]}", interval=cut(m))
        G.role_word(ax, -0.15, "the top 10 heads", "address", ha="left", level=1)

    def numbers(i, _r):
        m = hm[i]
        v, r = cut(m), rnd(m)
        key = f"heads.top10.{ZK[m]}"
        return [(G.num(key, v[0], "share"), INK, "bold"), ("  " + G.interval(key, v[1], v[2], "share"), MUTED, "normal"),
                ("   ", MUTED, "normal"), (G.num(f"heads.random10.{ZK[m]}", r[0], "share"), MUTED, "normal")]  # fmt: skip

    t = W.table([Row(NAME[m]) for m in hm], [
        _col(3.6, "zeroing the top 10 heads", heads, (-0.15, 0.66), [0, 0.25, 0.5], "cut", sub="under the address swap"),
        Col(2.5, "share cut", "top 10 [95%] · 10 random", numbers, text=True),
    ], label_w=1.15, row_h=0.4, head=0.95)  # fmt: skip
    _render(t, fid)


# ---- the key figure (I) --------------------------------------------------------------------------------------------------
def key() -> None:
    """The whole grammar on one image: each role colour and what it stands for; then the marks, drawn by the grammar
    from Fig. 1's data (the 27B's band row: lookup and recall drops; its gap with the whisker and the grey tick of the
    largest same-size control; Muse 30B's post hoc recall drop, hollow; the 27B's one-layer row on the grey band), the
    key line, the missing-cell words, and the 27B's row read aloud (its numbers from the data)."""
    import matplotlib.pyplot as plt

    fid = "key"
    G.begin(fid)
    roles = list(TM.ROLE_MEANING)
    step = 0.29
    h = 0.45 + (len(roles) + 1) * step + 0.3 + 5.6 * step + 4.2 * step + 0.3
    fig = plt.figure(figsize=(W.WIDTH, h), dpi=W.DPI)
    fw = fig.get_figwidth()

    def fy(inch):
        return 1 - inch / h

    x0 = 0.12 / fw
    y = 0.3
    fig.text(x0, fy(y), TM.KEY_TITLES[0], fontsize=W.FS["title"], weight="bold", color=INK, va="center")
    for j, r in enumerate(roles):
        yy = fy(y + (1 + j) * step)
        fig.text(x0, yy, "●", color=ROLE[r], fontsize=W.FS["text"], va="center")
        fig.text(x0 + 0.3 / fw, yy, TM.ROLE_WORD[r], color=ROLE[r] if r != "other" else MUTED, va="center",
                 fontsize=W.FS["text"], weight="bold")  # fmt: skip
        fig.text(x0 + 1.6 / fw, yy, TM.ROLE_MEANING[r], color=MUTED, va="center", fontsize=W.FS["small"])
    y += (len(roles) + 1) * step + 0.3
    fig.text(x0, fy(y), TM.KEY_TITLES[1], fontsize=W.FS["title"], weight="bold", color=INK, va="center")
    k, mu = "q27", "mu"
    lk, rc, mk = D.b(f"ko.{k}.lostK"), D.b(f"ko.{k}.lostM"), D.b(f"ko.{k}.mk")
    lr, ll = S.conflict("qwen3.6-27b", "recall"), S.conflict("qwen3.6-27b", "lookup")
    labels = [f"{NAME['qwen3.6-27b']}: {TM.KEY_ROWS[0]}", f"{NAME['qwen3.6-27b']}: {TM.KEY_ROWS[1]}",
              f"{NAME['muse-glimmer-30b']}: {TM.KEY_ROWS[2]}", f"{NAME['qwen3.6-27b']}: {TM.KEY_ROWS[3]}"]  # fmt: skip
    ax_l = 5.0  # the marks' axes start here (inches), right of the longest row label
    for j, lab in enumerate(labels):
        fig.text(x0, fy(y + (1 + j) * step), lab, fontsize=W.FS["small"], color=INK, va="center")

    def axes(j, xlim):
        yy = y + (1 + j) * step
        ax = fig.add_axes((ax_l / fw, fy(yy + step / 2), (W.WIDTH - ax_l - 0.15) / fw, step / h))
        ax.set_xlim(*xlim)
        ax.set_ylim(0.5, -0.5)
        ax.axis("off")
        return ax

    a = axes(0, (-4, 70))
    G.connector(a, lk[0], rc[0], 0)
    G.mark(a, lk[0], 0, "lookup", f"band.{k}")
    G.mark(a, rc[0], 0, "recall", f"band.{k}")
    a = axes(1, (-4, 70))
    G.tick(a, S.ctrl(k), 0, half=0.4)
    G.mark(a, mk[0], 0, "recall", f"band.{k}", interval=mk)
    a = axes(2, (-4, 70))
    G.mark(a, D.b(f"ko.{mu}.lostM")[0], 0, "recall", f"band.{mu}")
    a = axes(3, (-0.25, 1.0))
    G.band(a, 1)
    G.connector(a, ll[0], lr[0], 0)
    G.mark(a, ll[0], 0, "lookup", "layer.q27", interval=ll)
    G.mark(a, lr[0], 0, "recall", "layer.q27", interval=lr)
    y += 5.6 * step
    for j, row in enumerate(G.key()):
        parts = []
        for n, (mark_, col, words) in enumerate(row):
            parts += [("     " if n else "", MUTED, "normal"), (mark_ + " " if mark_ else "", col, "normal"),
                      (words, MUTED, "normal")]  # fmt: skip
        T.rich(fig, x0, fy(y + j * step), parts, size=W.FS["key"])
    y += len(G.key()) * step
    fig.text(x0, fy(y), TM.MISSING_LINE, fontsize=W.FS["small"], color=MUTED, va="center")
    read = TM.READ_ALOUD.format(model=NAME["qwen3.6-27b"], recall=G.num(f"ko.{k}.lostM", rc[0], "points"),
                                lookup=G.num(f"ko.{k}.lostK", lk[0], "points"), gap=G.num(f"ko.{k}.mk", mk[0], "points"),
                                ctrl=G.num(f"ko.{k}.ctrl", S.ctrl(k), "points"))  # fmt: skip
    for j, line in enumerate(read.split("; ")):  # two lines: what drops, then the gap against its control
        fig.text(x0, fy(y + (1 + j) * step), line + (";" if j == 0 else ""), fontsize=W.FS["small"], color=INK,
                 va="center")  # fmt: skip
    path = f"{OUT}/key.png"
    if T.BEFORE_SAVE is not None:
        T.BEFORE_SAVE(fig, path)
    fig.savefig(path, dpi=W.DPI, facecolor="white")
    plt.close(fig)


FIGS = {"key": key, "fig01_main_split": fig01_main_split, "fig04_twin_set": fig04_twin_set, "fig09_order": fig09_order,
        "fig12_pointer": fig12_pointer, "appB_f17_attention": appB_f17_attention,
        "appB_f17b_heads": appB_f17b_heads}  # fmt: skip
