"""The LessWrong write-up's figures (figures/writeup/, built by `figkit.tables --target writeup`): 8.0 in wide at 200 dpi
(1600 px), nothing under 11 pt, no title (the caption lives in the post). The rebuilt figures read the same sources as
their README / slide originals (data/figures/depth/data.csv, docs/breadth/data.csv); the new ones read
data/figures/writeup/data.csv (scripts/writeup_data.py)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import deck_figs as F
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import lint
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit.dottable import BAND, INK, MUTED, C, Col, Row, Table, band, connector, dot, head_label
from bridge_jspace.figkit.theme import WRITEUP

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


def pad_for(label_w: float, widths: list[float]) -> float:
    """The column gap that makes a table exactly WIDTH inches wide."""
    pad = (WIDTH - label_w - sum(widths)) / (len(widths) + 1)
    assert pad > 0.05, f"columns too wide for {WIDTH} in: {label_w} + {sum(widths)}"
    return pad


def table(rows, cols, label_w: float, **kw) -> Table:
    return Table(rows, cols, label_w=label_w, pad=pad_for(label_w, [c.width for c in cols]), **kw)


HOLLOW_NO_KEY = "a hollow mark without the key item 'post hoc'"


def stack(tables: list[Table], name: str) -> None:
    """Tables rendered one under the other into one PNG, each linted as it is drawn. Only the last carries the key, so
    the panels above it may use a hollow mark whose "○ post hoc" item is in the last panel's key."""
    from PIL import Image

    def lint_upper(fig, path):
        PROBLEMS.extend(p for p in lint.table_problems(fig, Path(path).stem, need_xlabel=True, need_cue=True,
                                                       min_pt=FS["small"]) if not p.endswith(HOLLOW_NO_KEY))  # fmt: skip

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

    t = table(rows, [
        Col(1.85, "Band of layers", "answers turned wrong", remove_band, (-4, 70), [0, 30, 60],
            xlabel="accuracy drop (points)", cue="→ lens part needed more"),
        Col(1.45, "gap", "recall − lookup", band_gap, text=True),
        Col(1.75, "One layer", "switches blocked", remove_patch, (-0.25, 1.0), [0, 0.5, 1.0],
            xlabel="share of switches", cue="→ depends more on lens part"),
        Col(1.45, "gap", "recall − lookup", patch_gap, text=True),
    ], label_w=1.15, sub_lift=True, foot=0.45, head=0.72, title_top=0.1,
        key=[[("(n)", MUTED, "the largest same-size control's gap: rotated, logit lens or PCA")],
             [("[ ]", MUTED, "95% interval"), ("■", BAND, "within 0.10 of a random part")]])  # fmt: skip
    t.render(f"{OUT}/fig01_main_split.png", dpi=DPI)


# ---- Fig. 5: same-size controls (f2_controls as two stacked panels) -------------------------------------------------
COMPACT = {"row_h": 0.27, "head": 0.32, "title_top": 0.07, "labels": False, "foot": 0.25}


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
    """deck_figs.band_diff_parts at the source's precision (one decimal): 38.5 printed with :.0f reads 38 (half to
    even), where the post quotes 38.5."""
    top = S.largest(k)
    pair = D.b(f"f2.band.{k}.{top[0]}") if top else None
    if not pair or pair[1] is None:
        return F.band_diff_parts(k)
    return [(f"{pair[0]:+.1f}", INK, "bold"), (f"  [{pair[1]:.0f}, {pair[2]:.0f}]", MUTED, "normal")]


def _group(word: str, top: float):
    def f(fig):
        fig.text(0.12 / fig.get_figwidth(), 1 - top / fig.get_figheight(), word, ha="left", va="top",
                 fontsize=FS["title"], weight="bold", color=INK)  # fmt: skip

    return f


def fig05_controls() -> None:
    rows = [Row(NAME[m]) for m, _ in DAN]
    label_w, w_lens, w_ctl, w_diff = 1.0, 1.15, 1.2, 1.55

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
    ], label_w=label_w, extra=[_group("Band", COMPACT["title_top"])], **COMPACT)  # fmt: skip

    def layer_cell(q):
        return lambda m: D.s(m, q, "fig02")

    share = dict(xlim=(-0.08, 1.0), xticks=[0, 0.5, 1], xlabel="share", cue="→ more blocked", vfmt="{:.2f}")
    bottom = table(rows, [
        _ctrl_col("lens part", layer_cell("J++ part: recall extra loss"), colour="lens", width=w_lens, **share),
        *(_ctrl_col(name, layer_cell(q), colour="control", width=w_ctl, **share) for _k, name, q in F.LAYER_CTRL),
        Col(w_diff, "difference", "", lambda i, _r: F.layer_diff_parts(DAN[i][0]), text=True),
    ], label_w=label_w, extra=[_group("One layer", COMPACT["title_top"])], **COMPACT,
        key=[("●", C["lens"], "lens part"), ("●", C["control"], "same-size control"), ("○", INK, "post hoc"),
             ("", MUTED, "difference: lens part − largest control [95%]")])  # fmt: skip
    stack([top, bottom], "fig05_controls")


FIGS = {"fig01_main_split": fig01_main_split, "fig05_controls": fig05_controls}  # post order; the file names are fixed
