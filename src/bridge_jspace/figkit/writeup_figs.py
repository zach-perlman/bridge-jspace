"""The LessWrong write-up's figures (figures/writeup/, built by `figkit.tables --target writeup`): 8.0 in wide at 200 dpi
(1600 px), nothing under 11 pt, no title (the caption lives in the post). The rebuilt figures read the same sources as
their README / slide originals (data/figures/depth/data.csv, docs/breadth/data.csv); the new ones read
data/figures/writeup/data.csv (scripts/writeup_data.py)."""

from __future__ import annotations

import csv
import tempfile
from functools import cache
from pathlib import Path

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import deck_figs as F
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import lint
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit.dottable import BAND, INK, MUTED, C, Col, Row, Table, band, connector, dot, head_label
from bridge_jspace.figkit.theme import WRITEUP, WRITEUP_MIN_ROW

OUT = "."  # set by bridge_jspace.figkit.tables
PROBLEMS: list[str] = []  # lint of the panels stack() draws above the last (tables.build reports them)
DPI = WRITEUP.dpi
WIDTH = WRITEUP.sizes["full"][0]
DAN = D.DAN
ZK = F.ZK
NAME = {m: n.replace(" ○", "") for m, n in DAN}
# the write-up theme's sizes for the dot table's texts (tables.build swaps them in for this target only)
FS = {"name": 12, "title": 12, "sub": WRITEUP.label, "rowsub": WRITEUP.label, "subrow": WRITEUP.label,
      "hollow": WRITEUP.label, "xlabel": WRITEUP.axis, "cue": WRITEUP.label, "key": WRITEUP.label,
      "text": WRITEUP.value, "value": WRITEUP.value, "head": WRITEUP.label, "small": WRITEUP.label}  # fmt: skip


@cache
def writeup_data() -> dict:
    """data/figures/writeup/data.csv (scripts/writeup_data.py) by key: (value, lo, hi)."""
    path = D.REPO / "data" / "figures" / "writeup" / "data.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {r["key"]: (D._f(r["value"]), D._f(r["lo"]), D._f(r["hi"])) for r in csv.DictReader(f)}


def w(key: str):
    """A write-up data cell (value, lo, hi), or None: the figure then says "source missing" in grey."""
    return writeup_data().get(key)


@cache
def _ns() -> dict:
    path = D.REPO / "data" / "figures" / "writeup" / "data.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {r["key"]: int(r["n"]) for r in csv.DictReader(f) if r["n"]}


def writeup_n(key: str) -> int | None:
    return _ns().get(key)


def pad_for(label_w: float, widths: list[float]) -> float:
    """The column gap that makes a table exactly WIDTH inches wide."""
    pad = (WIDTH - label_w - sum(widths)) / (len(widths) + 1)
    assert pad > 0.05, f"columns too wide for {WIDTH} in: {label_w} + {sum(widths)}"
    return pad


def table(rows, cols, label_w: float, **kw) -> Table:
    return Table(rows, cols, label_w=label_w, pad=pad_for(label_w, [c.width for c in cols]), **kw)


VALUE_GAP = 7.0  # points between a dot's edge and its value (tables.build sets dottable.VALUE_GAP for this target)
LOWER = 0.27  # a row's lower line (rows units): notes go there, under dots lifted by LIFT


def lower(ax, x, i, text, ha="center", color=MUTED, zebra=None):
    """A grey note on row i's lower line, its box the row's colour: the lines under it stop there (figkit/lint.py
    crossings exempts it from lines, never from marks)."""
    bg = (T.ZEBRA if i % 2 == 0 else "white") if zebra is None else (T.ZEBRA if zebra else "white")
    if ha == "center":  # kept inside its panel
        r = ax.figure.canvas.get_renderer()
        probe = ax.text(x, i + LOWER, text, ha="center", fontsize=FS["small"])
        bb = probe.get_window_extent(r).transformed(ax.transData.inverted())
        probe.remove()
        lim = ax.get_xlim()
        x += max(0.0, lim[0] - bb.x0) - max(0.0, bb.x1 - lim[1])
    t = ax.text(x, i + LOWER, text, ha=ha, va="center", fontsize=FS["small"], color=color, zorder=6,
                bbox={"boxstyle": "square,pad=0.15", "facecolor": bg, "edgecolor": "none"})  # fmt: skip
    t._masks_lines = True
    return t


def value(ax, x, y, cell, color, vfmt, i=None, size=9.5, zebra=None):
    """A dot's value beside its whisker, VALUE_GAP points clear of its marker, on the first side where it touches no
    line or mark drawn so far (figkit/lint.py hit: draw a row's dots before its values) and stays inside the panel; if
    neither side does, on row i's lower line."""
    fig = ax.figure
    fig.canvas.draw()  # the spines' positions are set on the first draw
    r = fig.canvas.get_renderer()
    obstacles = lint.drawn_obstacles(fig)
    lim = ax.get_xlim()
    text = T.clean(vfmt.format(x))
    tcol = color if color != C["control"] else MUTED
    px_pt = fig.dpi / 72
    cx = ax.transData.transform((x, y))[0]
    for side in ("right", "left"):
        sgn = 1 if side == "right" else -1
        x0 = (cell[2] if side == "right" else cell[1]) if cell and cell[1] is not None else x
        ex = ax.transData.transform((x0, y))[0]
        # from the whisker's end, but never closer to the marker than its edge plus VALUE_GAP
        pts = max(5.0, (size / 2 + VALUE_GAP) - sgn * (ex - cx) / px_pt)
        a = ax.annotate(text, (x0, y), xytext=(sgn * pts, 0), textcoords="offset points",
                        ha="left" if side == "right" else "right", va="center", fontsize=FS["value"], color=tcol,
                        annotation_clip=False, zorder=6)  # fmt: skip
        bb = a.get_window_extent(r)
        d = bb.transformed(ax.transData.inverted())
        if lim[0] <= d.x0 and d.x1 <= lim[1] and not lint.hit(bb, obstacles):
            return a
        a.remove()
    row = y if i is None else i
    for ha in ("center", "right", "left"):  # the lower line: where it crosses no line, else centred with lines stopped
        t = lower(ax, x, row, text, ha=ha, color=tcol, zebra=zebra)
        d = t.get_window_extent(r).transformed(ax.transData.inverted())
        if lim[0] <= d.x0 and d.x1 <= lim[1] and not lint.hit(t.get_window_extent(r), obstacles):
            return t
        t.remove()
    return lower(ax, x, row, text, color=tcol, zebra=zebra)


HOLLOW_NO_KEY = "a hollow mark without the key item 'post hoc'"


def stack(tables: list[Table], name: str) -> None:
    """Tables rendered one under the other into one PNG, each linted as it is drawn. Only the last carries the key, so
    the panels above it may use a hollow mark whose "○ post hoc" item is in the last panel's key."""
    from PIL import Image

    def lint_upper(fig, path):
        PROBLEMS.extend(p for p in lint.table_problems(fig, Path(path).stem, need_xlabel=True, need_cue=True,
                                                       min_pt=FS["small"]) if not p.endswith(HOLLOW_NO_KEY))  # fmt: skip
        PROBLEMS.extend(lint.crossings(fig, Path(path).stem))

    hook = T.BEFORE_SAVE
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for k, t in enumerate(tables):
            p = Path(tmp) / f"{name}_{k}.png"
            last = k == len(tables) - 1
            t.hollow_key = last
            T.BEFORE_SAVE = hook if last else lint_upper
            try:
                t.render(str(p), dpi=DPI)
            finally:
                T.BEFORE_SAVE = hook
            parts.append(Image.open(p).convert("RGB"))
        sheet = Image.new("RGB", (parts[0].width, sum(p.height for p in parts)), "white")
        y = 0
        for p in parts:
            sheet.paste(p, (0, y))
            y += p.height
        sheet.save(f"{OUT}/{name}.png", dpi=(DPI, DPI))


# ---- Fig. 1: the main split (r1_c1_split at the column's width) -----------------------------------------------------
# the band test's two models whose split the post does not claim, and why (docs/breadth: Muse's largest control is the
# logit lens, ko.mu.u; the 122B's gap is gone when scored by probability, ko.q122.soft)
NOT_CLAIMED = {"mu": "not claimed: shared with the logit lens", "q122": "not claimed: gone when scored by probability"}
LIFT = 0.18  # a row with a grey note under its name: its marks move up with the name (0.09 in of a 0.5 in row)


def _groups(*titles: tuple[float, str], top: float = 0.08, notes: tuple[tuple[float, str], ...] = ()):
    """Bold group headers above the column titles, each at an x in inches; notes: grey lines under them, one each."""

    def f(fig):
        w, h = fig.get_figwidth(), fig.get_figheight()
        for x, word in titles:
            fig.text(x / w, 1 - top / h, word, ha="left", va="top", fontsize=FS["title"], weight="bold", color=INK)
        for k, (x, word) in enumerate(notes):
            fig.text(x / w, 1 - (top + 0.30 * (k + 1)) / h, word, ha="left", va="top", fontsize=FS["sub"], color=MUTED)

    return f


def _x_of(t: Table, col: int) -> float:
    """A column's left edge in inches."""
    return t.label_w + t.pad + sum(c.width + t.pad for c in t.cols[:col])


def fig01_main_split() -> None:
    rows = [Row(NAME[m], sub=NOT_CLAIMED.get(ZK[m], "")) for m, _ in DAN]

    def y_of(i):
        return i - (LIFT if rows[i].sub else 0)

    def remove_band(ax, _rows):
        for i, (m, _) in enumerate(DAN):
            k, y = ZK[m], y_of(i)
            rc, lk = D.b(f"ko.{k}.lostM")[0], D.b(f"ko.{k}.lostK")[0]
            grey = k in NOT_CLAIMED
            connector(ax, lk, rc, y)
            dot(ax, lk, y, C["control"] if grey else C["lookup"], grey, size=8 if grey else 9.5)
            dot(ax, rc, y, C["control"] if grey else C["recall"], grey, size=8 if grey else 9.5)
        head_label(ax, 0, "lookup", C["lookup"], ha="left")
        head_label(ax, D.b("ko.q9.lostM")[0], "recall", C["recall"])

    def band_gap(i, _r):
        k = ZK[DAN[i][0]]
        mk, lo, hi = D.b(f"ko.{k}.mk")
        ink = MUTED if k in NOT_CLAIMED else INK
        return [(f"{mk:.0f}", ink, "bold"), (f"  [{lo:.0f}, {hi:.0f}]", MUTED, "normal"),
                (f"  ({S.ctrl(k):.0f})", MUTED, "normal")]  # fmt: skip

    def remove_patch(ax, _rows):
        band(ax, -0.1, 0.1, len(DAN))
        for i, (m, _) in enumerate(DAN):
            rc, lk = S.conflict(m, "recall"), S.conflict(m, "lookup")
            h, y = D.hollow(m), y_of(i)
            connector(ax, lk[0], rc[0], y)
            dot(ax, lk[0], y, C["lookup"], h, cell=lk)
            dot(ax, rc[0], y, C["recall"], h, cell=rc)
        head_label(ax, -0.2, "lookup", C["lookup"], ha="left")
        head_label(ax, 1.0, "recall", C["recall"], ha="right")

    def patch_gap(i, _r):
        m = DAN[i][0]
        g = D.x(f"contrast_{D.SHORT.get(m, '-')}")
        if g:
            return [(f"{g[0]:.2f}", INK, "bold"), (f"  [{g[1]:.2f}, {g[2]:.2f}]", MUTED, "normal")]
        rc, lk = S.conflict(m, "recall")[0], S.conflict(m, "lookup")[0]
        return [(f"{rc - lk:.2f}", INK, "bold"), ("  no interval", MUTED, "normal")]  # aggregate only

    # the two halves measure different data (fact passages / locker scenes): a gutter between them, the zebra cut there
    t = table(rows, [
        Col(1.75, "", "answers turned wrong", remove_band, (-4, 70), [0, 30, 60],
            xlabel="accuracy drop (points)", cue="→ lens part needed more"),
        Col(1.35, "gap (points)", "recall − lookup", band_gap, text=True),
        Col(0.15, gutter=True),
        Col(1.6, "", "switches blocked", remove_patch, (-0.25, 1.0), [0, 0.5, 1.0],
            xlabel="share of switches", cue="→ depends more on lens part"),
        Col(1.4, "gap (share)", "recall − lookup", patch_gap, text=True),
    ], label_w=1.1, sub_lift=True, foot=0.45, head=1.0, title_top=0.4,
        key=[[("(n)", MUTED, "the largest same-size control's gap: rotated, logit lens or PCA")],
             [("[ ]", MUTED, "95% interval"), ("■", BAND, "within 0.10 of a random part")]])  # fmt: skip
    t.extra.append(_groups((_x_of(t, 0), "Band of layers · fact passages"), (_x_of(t, 3), "One layer · locker scenes")))
    t.render(f"{OUT}/fig01_main_split.png", dpi=DPI)


# ---- Fig. 5: same-size controls (f2_controls as two stacked panels) -------------------------------------------------
COMPACT = {"row_h": 0.34, "labels": False, "foot": 0.25}


def _ctrl_col(title, cell_of, xlim, xticks, xlabel, cue, colour, vfmt, width, hollow_of=lambda m: False):
    def draw(ax, _r):
        for i, (m, _) in enumerate(DAN):
            c = cell_of(m)
            if not c:
                ax.text(sum(xlim) / 2, i, "no run", ha="center", va="center", fontsize=FS["small"], color=MUTED,
                        bbox={"boxstyle": "square,pad=0.1", "facecolor": T.ZEBRA if i % 2 == 0 else "white",
                              "edgecolor": "none"})  # fmt: skip
                continue
            ctl = colour == "control"
            # a value on the right half of a narrow column goes left of its whisker, so it stays in its column
            right = ctl or (c[0] - xlim[0]) / (xlim[1] - xlim[0]) < 0.5
            dot(ax, c[0], i, C[colour], hollow=hollow_of(m), cell=None if ctl else c, value=c[0], vfmt=vfmt,
                size=8 if ctl else 9.5, vside="right" if right else "left")  # fmt: skip

    return Col(width, title, "", draw, xlim, xticks, xlabel=xlabel, cue=cue)


def _band_diff(k: str):
    """The lens part minus its largest control, value and interval at one decimal (one precision per column), from
    data/figures/writeup/data.csv (scripts/writeup_data.py; docs/breadth/data.csv rounds the interval to whole points).
    Grey where the band test's split is not claimed (fig01)."""
    c = w(f"fig05.band_diff.{k}")
    if c is None:
        return [("source missing", MUTED, "normal")]
    ink = MUTED if k in NOT_CLAIMED else INK
    return [(f"{c[0]:+.1f}", ink, "bold"), (f"  [{c[1]:.1f}, {c[2]:.1f}]", MUTED, "normal")]


def fig05_controls() -> None:
    rows = [Row(NAME[m]) for m, _ in DAN]
    label_w, w_lens, w_ctl, w_diff = 1.15, 1.2, 1.15, 1.55

    def band_cell(key):
        def f(m):
            k = ZK[m]
            c = D.b(f"ko.{k}.{key}")
            if key == "pc" and not c:  # the size-matched ratio times the lens part's gap (specs.largest)
                pcr, mk = D.b(f"ko.{k}.pcr"), D.b(f"ko.{k}.mk")
                c = (pcr[0] * mk[0], None, None) if pcr and mk else None
            return c

        return f

    zach_post_hoc = lambda m: ZK[m] in ("mu", "q122")  # noqa: E731  the band test's post hoc models (r1, f2)
    pts = dict(xlim=(-4, 70), xticks=[0, 50], xlabel="points", cue="→ needed more", vfmt="{:.0f}")
    top = table(rows, [
        _ctrl_col("lens part", band_cell("mk"), colour="lens", width=w_lens, hollow_of=zach_post_hoc, **pts),
        _ctrl_col("rotated", band_cell("rot"), colour="control", width=w_ctl, hollow_of=zach_post_hoc, **pts),
        _ctrl_col("logit lens", band_cell("u"), colour="control", width=w_ctl, hollow_of=zach_post_hoc, **pts),
        _ctrl_col("PCA", band_cell("pc"), colour="control", width=w_ctl, hollow_of=zach_post_hoc, **pts),
        Col(w_diff, "difference", "", lambda i, _r: _band_diff(ZK[DAN[i][0]]), text=True),
    ], label_w=label_w, head=0.95, title_top=0.68, **COMPACT)  # fmt: skip
    top.extra.append(_groups((0.12, "Band · fact passages"),
                             notes=((0.12, "recall − lookup gap under each removal (points)"),)))

    def layer_cell(q):
        return lambda m: D.s(m, q, "fig02")

    share = dict(xlim=(-0.08, 1.0), xticks=[0, 0.5, 1], xlabel="share", cue="→ more blocked", vfmt="{:.2f}")
    # "random lens directions": not the random part fig01's shares are measured against, so named in full
    layer_name = {"rand": "random lens\ndirections"}
    bottom = table(rows, [
        _ctrl_col("lens part", layer_cell("J++ part: recall extra loss"), colour="lens", width=w_lens, **share),
        *(_ctrl_col(layer_name.get(k, name), layer_cell(q), colour="control", width=w_ctl, **share)
          for k, name, q in F.LAYER_CTRL),
        Col(w_diff, "difference", "", lambda i, _r: F.layer_diff_parts(DAN[i][0]), text=True),
    ], label_w=label_w, head=1.3, title_top=0.94, **COMPACT,
        key=[("●", C["lens"], "lens part"), ("●", C["control"], "same-size control"), ("○", INK, "post hoc"),
             ("", MUTED, "difference: lens part − largest control [95%]")])  # fmt: skip
    # fig01's one-layer shares come from the conflict-test runs, which had no same-size control (0.50 there, 0.37 here
    # for the 9B): this panel's runs are the earlier x0_pcaeq / x0_parts ones
    bottom.extra.append(_groups((0.12, "One layer · locker scenes"),
                                notes=((0.12, "recall's switches blocked beyond a random part (share)"),
                                       (0.12, "earlier runs with a same-size control; Fig. 1's runs had none"))))  # fmt: skip
    stack([top, bottom], "fig05_controls")


# ---- Fig. 4: the twin set (note 41; data/figures/writeup/data.csv fig04.*) -----------------------------------------------
TWIN_MODELS = (("q9", "Qwen 9B"), ("q27", "Qwen 27B"), ("nl", "Lightning"))
TWIN_CONDS = (("paper10", "knock-out", None), ("paper10_rot", "rotated", C["control"]),
              ("paper10_keepA", "answer span kept", C["answer"]))  # fmt: skip


def _missing(ax, i, xlim):
    """'source missing' at the cell's right end, where no rule runs; its box the row's colour hides the grid lines."""
    t = ax.text(xlim[1], i, "source missing", ha="right", va="center", fontsize=FS["small"], color=MUTED, zorder=6,
                bbox={"boxstyle": "square,pad=0.15", "facecolor": T.ZEBRA if round(i) % 2 == 0 else "white",
                      "edgecolor": "none"})  # fmt: skip
    t._masks_lines = True


def fig04_twin_set() -> None:
    """Per model a header row (its item counts, recall / lookup), then one sub-row per condition: accuracy on the
    recall twins and on the lookup twins, and the recall - lookup gap of the knock-out (and of the rotated control,
    grey) with its 95% interval. The unedited accuracy is one grey line under the column titles (its range over every
    model and reader). One population: the registered one (every gated item, v4 draw 4001)."""
    rows, at, heads = [], [], []  # at: (model key, condition key or None for the header row)
    for k, name in TWIN_MODELS:
        heads.append(len(rows))
        nr, nl = writeup_n(f"fig04.recall.unedited.{k}"), writeup_n(f"fig04.lookup.unedited.{k}")
        rows.append(Row(f"{name} · {nr} / {nl} items" if nr and nl else name))
        at.append((k, None))
        for cond, label, _ in TWIN_CONDS:
            rows.append(Row("", sub=label))
            at.append((k, cond))
    acc_lim, gap_lim = (-4, 104), (-12, 72)

    def accuracy(reader):
        knock = C["recall"] if reader == "recall" else C["lookup"]

        def f(ax, _r):
            for i, (k, cond) in enumerate(at):
                if cond is None:
                    continue
                c = w(f"fig04.{reader}.{cond}.{k}")
                if c is None:
                    _missing(ax, i, acc_lim)
                    continue
                col = dict((cd, cl) for cd, _l, cl in TWIN_CONDS)[cond] or knock
                dot(ax, c[0], i, col, size=8 if col == C["control"] else 9.5)
                value(ax, c[0], i, None, col, "{:.0f}")

        return f

    def gap(ax, _r):
        for i, (k, cond) in enumerate(at):
            if cond not in ("paper10", "paper10_rot"):
                continue
            c = w(f"fig04.gap.{cond}.{k}")
            if c is None:
                _missing(ax, i, gap_lim)
                continue
            col = C["control"] if cond == "paper10_rot" else INK
            dot(ax, c[0], i, col, cell=c, size=8 if col == C["control"] else 9.5)
            value(ax, c[0], i, c, col, "{:.1f}")

    t = table(rows, [
        Col(1.9, "Recall twins", "share answered right", accuracy("recall"), acc_lim, [0, 50, 100],
            xlabel="accuracy (%)", cue="→ more answers right"),
        Col(1.9, "Lookup twins", "share answered right", accuracy("lookup"), acc_lim, [0, 50, 100],
            xlabel="accuracy (%)", cue="→ more answers right"),
        Col(1.9, "Gap", "recall − lookup", gap, gap_lim, [0, 30, 60],
            xlabel="accuracy drop (points)", cue="→ recall drops more"),
    ], label_w=1.75, row_h=WRITEUP_MIN_ROW, group=4, skip_lines=tuple(heads),
        key=[("", MUTED, "whiskers: 95% interval")])  # fmt: skip
    unedited = [c[0] for r in ("recall", "lookup") for k, _ in TWIN_MODELS if (c := w(f"fig04.{r}.unedited.{k}"))]
    if len(unedited) == 2 * len(TWIN_MODELS):  # "every model" only when every cell has its source
        lo, hi = round(min(unedited)), round(max(unedited))
        span = f"{lo}%" if lo == hi else f"{lo}–{hi}%"

        def line(fig):  # in the direct-label row, under the column titles, where no line runs
            y = t.head + T.LABEL_ROW / 2
            fig.text(_x_of(t, 0) / fig.get_figwidth(), 1 - y / fig.get_figheight(),
                     f"unedited: {span} right on every model", ha="left", va="center", fontsize=FS["sub"],
                     color=MUTED)  # fmt: skip

        t.extra.append(line)
    t.render(f"{OUT}/fig04_twin_set.png", dpi=DPI)


# ---- Fig. 10: what the recall loses is its answer's own directions (notes 41, 50, 57, 68; fig10.*) ---------------------
def fig10_answer_span() -> None:
    """(a) Keeping only the answer span: the share of the recall's damage undone (brick, the answer span's colour in
    every figure), against a random keep orthogonal to the answers holding at least as much energy (grey). (b) Removing
    only the answer span, beyond energy-matched random, as a multiple of the full damage (dashed: all of it); (c) the
    same on the codename set. A row whose random part fell short of its energy says so on its lower line, with the
    stored shares."""

    def note(ax, i, xlim, text):  # a grey note on the lower line of a row whose marks are lifted
        lower(ax, sum(xlim) / 2, i, text)

    def matched(panel, k):  # the share of items whose random part reached its target energy, if short of all
        s = w(f"fig10.span_only_matched.{panel}.{k}")
        return s[0] if s and s[0] is not None and s[0] < 1 else None

    def lifted(k):
        ctl = w(f"fig10.keep_ctrl.{k}")
        return (ctl is not None and ctl[0] is None) or any(matched(p, k) is not None for p in ("v4", "codename"))

    rows = [Row(n) for _, n in TWIN_MODELS]
    y_of = lambda i: i - (LIFT if lifted(TWIN_MODELS[i][0]) else 0)  # noqa: E731
    keep_lim, mult_lim = (-0.4, 1.12), (0.6, 1.8)

    def keep(ax, _r):
        for i, (k, _) in enumerate(TWIN_MODELS):
            y, ctl, span = y_of(i), w(f"fig10.keep_ctrl.{k}"), w(f"fig10.keep_span.{k}")
            drawn = ctl is not None and ctl[0] is not None
            if ctl is None:
                _missing(ax, y, keep_lim)
            elif not drawn:  # the reading's label: neither random keep holds keepA's energy
                note(ax, i, keep_lim, "no energy-matched control")
            else:
                dot(ax, ctl[0], y, C["control"], cell=ctl, size=8)
            if span is not None:
                dot(ax, span[0], y, C["answer"], cell=span)
                value(ax, span[0], y, span, C["answer"], "{:.2f}", i=i)
            else:
                _missing(ax, y, keep_lim)
            if drawn:
                value(ax, ctl[0], y, ctl, C["control"], "{:.2f}", i=i, size=8)

    def removal(panel):
        def f(ax, _r):
            T.vrule(ax, 1.0, len(rows))
            head_label(ax, 1.0, "all of it", MUTED, weight="normal")
            for i, (k, _) in enumerate(TWIN_MODELS):
                c = w(f"fig10.span_only.{panel}.{k}")
                if c is None:
                    _missing(ax, y_of(i), mult_lim)
                    continue
                dot(ax, c[0], y_of(i), C["answer"], cell=c)
                value(ax, c[0], y_of(i), c, C["answer"], "{:.2f}", i=i)
                if (s := matched(panel, k)) is not None:
                    note(ax, i, mult_lim, f"matched on {s:.0%}")

        return f

    mult = dict(xlim=mult_lim, xticks=[0.8, 1.0, 1.2, 1.4, 1.6], xlabel="× the full damage", cue="→ more of the damage")
    t = table(rows, [
        Col(2.15, "Keep answer span", "share of damage undone", keep, keep_lim, [0, 0.5, 1],
            xlabel="share undone", cue="→ more undone"),
        Col(2.15, "Remove answer span", "beyond matched random", removal("v4"), **mult),
        Col(2.15, "Same, codename set", "independent fact sample", removal("codename"), **mult),
    ], label_w=1.15,
        key=[[("●", C["answer"], "the answer span: kept alone (left), removed alone (middle, right)")],
             [("●", C["control"], "a random keep orthogonal to the answers, at least as much energy")],
             [("", MUTED, "matched on N%: the items whose random part reached its target energy (under-matched)")]])  # fmt: skip
    t.render(f"{OUT}/fig10_answer_span.png", dpi=DPI)


# ---- Fig. 11: removals orthogonal to the answers (notes 62, 67; data/figures/writeup/data.csv fig11.*) ----------------
def fig11_orthogonal() -> None:
    """Panel 1, the one-hop question: the city's J++ directions (teal), the same made orthogonal to the answers (slate,
    hollow: not a registered reading on this question), the answers' own J++ directions (brick). Panel 2: the cleaned,
    data-built city subspace beyond energy-matched random, with the registered bar."""
    rows = [Row(n) for _, n in TWIN_MODELS]
    one_lim, sub_lim = (-4, 96), (-6, 27)
    conds = (("city", C["lens"], False), ("city_perp", C["neutral"], True), ("answers", C["answer"], False))

    def onehop(ax, _r):
        for i, (k, _) in enumerate(TWIN_MODELS):
            cells = [(w(f"fig11.onehop.{key}.{k}"), col, post_hoc) for key, col, post_hoc in conds]
            for c, col, post_hoc in cells:  # a row's dots first, so each value avoids them all
                if c is None:
                    _missing(ax, i, one_lim)
                else:
                    dot(ax, c[0], i, col, hollow=post_hoc, cell=c)
            for c, col, _ in cells:
                if c is not None:
                    value(ax, c[0], i, c, col, "{:.1f}")

    def subspace(ax, _r):
        T.vrule(ax, 15, len(rows))
        head_label(ax, 15, "registered bar", MUTED, weight="normal")
        for i, (k, _) in enumerate(TWIN_MODELS):
            c = w(f"fig11.clean_subspace.{k}")
            if c is None:
                _missing(ax, i, sub_lim)
                continue
            dot(ax, c[0], i, C["neutral"], cell=c)
            value(ax, c[0], i, c, C["neutral"], "{:.1f}")

    t = table(rows, [
        Col(3.45, "One-hop question", "“{city} is in the country of”", onehop, one_lim, [0, 40, 80],
            xlabel="accuracy drop (points)", cue="→ larger drop"),
        Col(2.65, "Data-built city subspace", "cleaned, minus random", subspace, sub_lim, [0, 10, 20],
            xlabel="drop beyond random (points)", cue="→ the removal sees the city"),
    ], label_w=1.15, row_h=0.5,
        key=[[("●", C["lens"], "the city's J++ directions"), ("●", C["answer"], "the answers' own J++ directions")],
             [("○", C["neutral"], "the same city directions, orthogonal to the answers (post hoc; no interval stored)")]])  # fmt: skip
    t.render(f"{OUT}/fig11_orthogonal.png", dpi=DPI)


# ---- Fig. A1: inside agent transcripts (notes 56c, 59, 65; figA1.*) -------------------------------------------------------
AGENT_COLS = (("copy", "copy", "a given answer", "vs rotated (pts)"),
              ("pick", "pick", "true of two", "vs rotated (pts)"),
              ("verify", "verify", "Yes/No claim", "vs harshest (pts)"),
              ("produce", "produce", "answer alone", "vs rotated (pts)"),
              ("derive", "derive", "from a premise", "vs rotated (pts)"))  # fmt: skip


def figA1_agents() -> None:
    """Per task inside the agent transcripts, the knock-out's accuracy drop minus a control's (points, bridge-clustered
    95%), one x scale for every task drawn (a task missing a model's run is left out). A cell whose registered reading
    is descriptive is grey and says so on its lower line (grey, not hollow: hollow means post hoc only)."""
    rows = [Row(n) for _, n in TWIN_MODELS]
    lim = (-25, 80)

    def role(key):
        row = _quantities().get(key, "")
        return "descriptive" if "registered role: descriptive" in row or "role: none" in row else ""

    def task(col):
        def f(ax, _r):
            T.vrule(ax, 0, len(rows))
            for i, (k, _) in enumerate(TWIN_MODELS):
                key = f"figA1.{col}.{k}"
                c = w(key)
                if c is None:
                    _missing(ax, i, lim)
                    continue
                word = role(key)
                y = i - LIFT  # every row lifted: its lower line holds the cell's word or a value with no room beside
                ink = C["control"] if word else C["recall"]
                dot(ax, c[0], y, ink, cell=c)
                value(ax, c[0], y, c, ink, "{:.1f}", i=i)
                if word:  # right of the dashed zero rule, so no line stops at it
                    lower(ax, 4, i, word, ha="left")

        return f

    # a task is drawn only when every model has its run (derive: note 56c ran on the 9B only, so the column is dropped
    # until the 27B and Lightning runs exist; its 9B row stays in data.csv)
    cols = [c for c in AGENT_COLS if all(w(f"figA1.{c[0]}.{k}") for k, _ in TWIN_MODELS)]
    width = (WIDTH - 1.0) / len(cols) - 0.12
    t = table(rows, [Col(width, title, sub, task(col), lim, [0, 30, 60], xlabel=xl, cue="→ needed more", zero=False)
                     for col, title, sub, xl in cols], label_w=1.0, labels=False, head=0.75,
              key=[[("●", C["recall"], "the knock-out's accuracy drop minus a control's, 95% whiskers")],
                   [("●", C["control"], "descriptive: no registered reading for this cell")]])  # fmt: skip
    t.render(f"{OUT}/figA1_agents.png", dpi=DPI)


# ---- Fig. 0: one bridge word, two readers (a schematic, no numbers) ---------------------------------------------------
# the locker scene of the datasets figure (depth_figs.datasets, p0a): the scene, its two questions and their answers
SCENE = (("The locker of carbon is 3. The locker of helium is 5. Eric picked ", "normal"), ("carbon", "bold"), (".", "normal"))
READERS = (("lookup", C["lookup"], "Which locker belongs to\nEric's pick?", "3, read in the scene"),
           ("recall", C["recall"], "What is the atomic number\nof Eric's pick?", "6, from memory"))  # fmt: skip
PARTS = (("lens part", C["lens"]), ("identity", C["identity"]), ("address", C["address"]))


def fig00_schematic() -> None:
    """The carbon locker scene: the bridge word's state holds the lens part (teal), the identity (blue) and the
    address (orange); the recall reads the lens part, the lookup reads the identity and the address."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

    fw, fh = WIDTH, 3.6
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    r = fig.canvas.get_renderer()

    def box(x0, y0, x1, y1, edge):
        fig.patches.append(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=0.015",
                                          transform=fig.transFigure, facecolor="white", edgecolor=edge, lw=1.2))  # fmt: skip

    def arrow(a, b, col, rad=0.0):
        fig.patches.append(FancyArrowPatch(a, b, transform=fig.transFigure, arrowstyle="-|>,head_length=6,head_width=3.5",
                                           color=col, lw=1.8, connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=2))  # fmt: skip

    x, bridge = 0.03, None  # the scene, its bridge word in bold
    for text, weight in SCENE:
        t = fig.text(x, 0.9, text, ha="left", va="center", fontsize=FS["title"], weight=weight, color=INK)
        bb = t.get_window_extent(r)
        if weight == "bold":
            bridge = (bb.x0 + bb.x1) / 2 / fig.bbox.width
        x += bb.width / fig.bbox.width
    fig.text(bridge, 0.80, "the bridge word", ha="center", va="center", fontsize=FS["small"], color=MUTED)

    sx0, sx1, sy0, sy1 = 0.40, 0.60, 0.38, 0.72  # the bridge word's state: its three parts
    box(sx0, sy0, sx1, sy1, T.FAINT)
    fig.text(sx0 + 0.02, sy1 - 0.05, "its state", ha="left", va="center", fontsize=FS["small"], color=MUTED)
    ys = {}
    for k, (word, col) in enumerate(PARTS):
        y = sy1 - 0.125 - k * 0.075
        ys[word] = y
        fig.patches.append(Rectangle((sx0 + 0.02, y - 0.022), 0.022, 0.044, transform=fig.transFigure, color=col))
        fig.text(sx0 + 0.055, y, word, ha="left", va="center", fontsize=FS["text"], weight="bold", color=col)
    arrow((bridge, 0.76), (sx1 - 0.03, sy1 + 0.005), MUTED, rad=-0.2)

    for k, (name, col, question, answer) in enumerate(READERS):
        x0 = 0.03 if k == 0 else 0.67
        x1 = x0 + 0.30
        box(x0, 0.05, x1, 0.40, col)
        fig.text(x0 + 0.02, 0.35, name, ha="left", va="center", fontsize=FS["title"], weight="bold", color=col)
        fig.text(x0 + 0.02, 0.235, question, ha="left", va="center", fontsize=FS["text"], color=INK, linespacing=1.15)
        fig.text(x0 + 0.02, 0.10, f"→ {answer}", ha="left", va="center", fontsize=FS["text"], weight="bold", color=col)
    for word in ("identity", "address"):  # the lookup reads these two
        arrow((sx0 - 0.005, ys[word]), (0.33 - 0.005, 0.40), C[word], rad=0.12 if word == "identity" else 0.05)
    arrow((sx1 + 0.005, ys["lens part"]), (0.67 + 0.005, 0.40), C["lens"], rad=-0.15)

    path = f"{OUT}/fig00_schematic.png"
    if T.BEFORE_SAVE is not None:
        T.BEFORE_SAVE(fig, path)
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)


@cache
def _quantities() -> dict:
    path = D.REPO / "data" / "figures" / "writeup" / "data.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {r["key"]: r["quantity"] for r in csv.DictReader(f)}


FIGS = {"fig00_schematic": fig00_schematic, "fig01_main_split": fig01_main_split, "fig04_twin_set": fig04_twin_set,
        "fig05_controls": fig05_controls, "fig10_answer_span": fig10_answer_span,
        "fig11_orthogonal": fig11_orthogonal, "figA1_agents": figA1_agents}  # post order; fixed names  # fmt: skip
