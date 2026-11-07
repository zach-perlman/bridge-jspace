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


def _groups(*titles: tuple[float, str], top: float = 0.08, note: tuple[float, str] | None = None):
    """Bold group headers above the column titles, each at an x in inches; note: one grey line under them."""

    def f(fig):
        w, h = fig.get_figwidth(), fig.get_figheight()
        for x, word in titles:
            fig.text(x / w, 1 - top / h, word, ha="left", va="top", fontsize=FS["title"], weight="bold", color=INK)
        if note:
            fig.text(note[0] / w, 1 - (top + 0.30) / h, note[1], ha="left", va="top", fontsize=FS["sub"], color=MUTED)

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
    label_w, w_lens, w_ctl, w_diff = 1.0, 1.22, 1.22, 1.55

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
    ], label_w=label_w, head=0.7, title_top=0.4, **COMPACT)  # fmt: skip
    top.extra.append(_groups((0.12, "Band · fact passages")))

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
    ], label_w=label_w, head=1.15, title_top=0.7, **COMPACT,
        key=[("●", C["lens"], "lens part"), ("●", C["control"], "same-size control"), ("○", INK, "post hoc"),
             ("", MUTED, "difference: lens part − largest control [95%]")])  # fmt: skip
    # fig01's one-layer shares come from the conflict-test runs, which had no same-size control (0.50 there, 0.37 here
    # for the 9B): this panel's runs are the earlier x0_pcaeq / x0_parts ones
    bottom.extra.append(_groups((0.12, "One layer · locker scenes"),
                                note=(0.12, "earlier runs with a same-size control; Fig. 1's runs had none")))  # fmt: skip
    stack([top, bottom], "fig05_controls")


# ---- Fig. 4: the twin set (note 41; data/figures/writeup/data.csv fig04.*) -----------------------------------------------
TWIN_MODELS = (("q9", "Qwen 9B"), ("q27", "Qwen 27B"), ("nl", "Lightning"))
TWIN_CONDS = (("unedited", "unedited", INK), ("paper10", "knock-out", None), ("paper10_rot", "rotated", C["control"]),
              ("paper10_keepA", "knock-out, answer span kept", C["lens"]))  # fmt: skip


def _missing(ax, i, xlim):
    ax.text(sum(xlim) / 2, i, "source missing", ha="center", va="center", fontsize=FS["small"], color=MUTED)


def fig04_twin_set() -> None:
    """Per model a header row, then one sub-row per condition: accuracy on the recall twins and on the lookup twins,
    and the recall - lookup gap of the knock-out (and of the rotated control, grey) with its 95% interval. One
    population: the registered one (every gated item, v4 draw 4001)."""
    rows, at = [], []  # at: (model key, condition key or None for the header row)
    for k, name in TWIN_MODELS:
        rows.append(Row(name))
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
                    c = w(f"fig04.{reader}.unedited.{k}")
                    n = writeup_n(f"fig04.{reader}.unedited.{k}")
                    if n:
                        ax.text(acc_lim[0] + 2, i, f"{n} items", ha="left", va="center", fontsize=FS["small"],
                                color=MUTED)  # fmt: skip
                    continue
                c = w(f"fig04.{reader}.{cond}.{k}")
                if c is None:
                    _missing(ax, i, acc_lim)
                    continue
                col = dict((cd, cl) for cd, _l, cl in TWIN_CONDS)[cond] or knock
                dot(ax, c[0], i, col, value=c[0], vfmt="{:.0f}", vside="left" if c[0] > 50 else "right",
                    size=8 if col == C["control"] else 9.5)  # fmt: skip

        return f

    def gap(ax, _r):
        for i, (k, cond) in enumerate(at):
            if cond not in ("paper10", "paper10_rot"):
                continue
            c = w(f"fig04.gap.{cond}.{k}")
            if c is None:
                _missing(ax, i, gap_lim)
                continue
            ctl = cond == "paper10_rot"
            dot(ax, c[0], i, C["control"] if ctl else INK, cell=c, value=c[0], vfmt="{:.1f}",
                size=8 if ctl else 9.5, vside="left" if c[0] > 30 else "right")  # fmt: skip

    t = table(rows, [
        Col(2.15, "Recall twins", "share answered right", accuracy("recall"), acc_lim, [0, 50, 100],
            xlabel="accuracy (%)", cue="→ more answers right"),
        Col(2.15, "Lookup twins", "share answered right", accuracy("lookup"), acc_lim, [0, 50, 100],
            xlabel="accuracy (%)", cue="→ more answers right"),
        Col(2.25, "Gap", "recall − lookup, 95% interval", gap, gap_lim, [0, 30, 60],
            xlabel="accuracy drop (points)", cue="→ recall drops more"),
    ], label_w=1.15, labels=False, row_h=WRITEUP_MIN_ROW, group=5,
        subtitle="one population: every gated item of one draw (the registered one)")  # fmt: skip
    t.render(f"{OUT}/fig04_twin_set.png", dpi=DPI)


# ---- Fig. 10: what the recall loses is its answer's own directions (notes 41, 50, 57, 68; fig10.*) ---------------------
def fig10_answer_span() -> None:
    """(a) Keeping only the answer span: the share of the recall's damage undone (teal), against a random keep
    orthogonal to the answers holding at least as much energy (grey). (b) Removing only the answer span, beyond
    energy-matched random, as a multiple of the full damage (dashed: all of it); (c) the same on the codename set. A row
    whose random part fell short of its energy says so under its name, with the stored shares."""

    def note(ax, i, xlim, text):  # a grey note on the lower line of a row whose marks are lifted
        ax.text(sum(xlim) / 2, i + 0.27, text, ha="center", va="center", fontsize=FS["small"], color=MUTED)

    def matched(panel, k):  # the share of items whose random part reached its target energy, if short of all
        s = w(f"fig10.span_only_matched.{panel}.{k}")
        return s[0] if s and s[0] is not None and s[0] < 1 else None

    def lifted(k):
        ctl = w(f"fig10.keep_ctrl.{k}")
        return (ctl is not None and ctl[0] is None) or any(matched(p, k) is not None for p in ("v4", "codename"))

    rows = [Row(n) for _, n in TWIN_MODELS]
    y_of = lambda i: i - (LIFT if lifted(TWIN_MODELS[i][0]) else 0)  # noqa: E731
    keep_lim, mult_lim = (-0.4, 1.12), (0.6, 1.7)

    def keep(ax, _r):
        for i, (k, _) in enumerate(TWIN_MODELS):
            y, ctl, span = y_of(i), w(f"fig10.keep_ctrl.{k}"), w(f"fig10.keep_span.{k}")
            if ctl is None:
                _missing(ax, y, keep_lim)
            elif ctl[0] is None:  # the reading's label: neither random keep holds keepA's energy
                note(ax, i, keep_lim, "no energy-matched control")
            else:
                dot(ax, ctl[0], y, C["control"], cell=ctl, value=ctl[0], size=8)
            if span is None:
                _missing(ax, y, keep_lim)
                continue
            dot(ax, span[0], y, C["lens"], cell=span, value=span[0], vside="left")

    def removal(panel):
        def f(ax, _r):
            T.vrule(ax, 1.0, len(rows))
            head_label(ax, 1.0, "all of it", MUTED, weight="normal")
            for i, (k, _) in enumerate(TWIN_MODELS):
                c = w(f"fig10.span_only.{panel}.{k}")
                if c is None:
                    _missing(ax, y_of(i), mult_lim)
                    continue
                dot(ax, c[0], y_of(i), C["recall"], cell=c, value=c[0], vside="right" if c[2] < 1.45 else "left")
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
        key=[[("●", C["lens"], "keeping only the answer span"), ("●", C["recall"], "removing only the answer span")],
             [("●", C["control"], "a random keep orthogonal to the answers, at least as much energy")],
             [("", MUTED, "matched on N%: the items whose random part reached its target energy (under-matched)")]])  # fmt: skip
    t.render(f"{OUT}/fig10_answer_span.png", dpi=DPI)


# ---- Fig. 11: removals orthogonal to the answers (notes 62, 67; data/figures/writeup/data.csv fig11.*) ----------------
def fig11_orthogonal() -> None:
    """Panel 1, the one-hop question: the city's J++ directions (teal), the same made orthogonal to the answers (slate,
    hollow: not a registered reading on this question), the answers' own J++ directions (brick). Panel 2: the cleaned,
    data-built city subspace beyond energy-matched random, with the registered bar."""
    rows = [Row(n) for _, n in TWIN_MODELS]
    one_lim, sub_lim = (-4, 96), (-6, 22)
    conds = (("city", C["lens"], False), ("city_perp", C["neutral"], True), ("answers", C["answer"], False))

    def onehop(ax, _r):
        for i, (k, _) in enumerate(TWIN_MODELS):
            for key, col, post_hoc in conds:
                c = w(f"fig11.onehop.{key}.{k}")
                if c is None:
                    _missing(ax, i, one_lim)
                    continue
                dot(ax, c[0], i, col, hollow=post_hoc, cell=c, value=c[0], vfmt="{:.1f}",
                    vside="left" if key == "city" and c[1] is not None and c[1] >= 30 else "right")  # fmt: skip

    def subspace(ax, _r):
        T.vrule(ax, 15, len(rows))
        head_label(ax, 15, "registered bar", MUTED, weight="normal")
        for i, (k, _) in enumerate(TWIN_MODELS):
            c = w(f"fig11.clean_subspace.{k}")
            if c is None:
                _missing(ax, i, sub_lim)
                continue
            dot(ax, c[0], i, C["neutral"], cell=c, value=c[0], vfmt="{:.1f}", vside="left" if c[0] > 5 else "right")

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
    95%), one x scale for all five tasks. A cell whose registered reading is descriptive is grey and says so on its
    lower line (grey, not hollow: hollow means post hoc only)."""
    rows = [Row(n) for _, n in TWIN_MODELS]
    lim = (-25, 70)

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
                y = i - (LIFT if word else 0)
                dot(ax, c[0], y, C["control"] if word else C["recall"], cell=c, value=c[0], vfmt="{:.1f}",
                    vside="left" if c[0] > 25 else "right")  # fmt: skip
                if word:
                    ax.text(sum(lim) / 2, i + 0.27, word, ha="center", va="center", fontsize=FS["small"], color=MUTED)

        return f

    t = table(rows, [Col(1.3, title, sub, task(col), lim, [0, 30, 60], xlabel=xl, cue="→ needed more", zero=False)
                     for col, title, sub, xl in AGENT_COLS], label_w=1.0,
              key=[[("●", C["recall"], "the knock-out's accuracy drop minus a control's, 95% whiskers")],
                   [("●", C["control"], "descriptive: no registered reading for this cell")]])  # fmt: skip
    t.render(f"{OUT}/figA1_agents.png", dpi=DPI)


@cache
def _quantities() -> dict:
    path = D.REPO / "data" / "figures" / "writeup" / "data.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {r["key"]: r["quantity"] for r in csv.DictReader(f)}


FIGS = {"fig01_main_split": fig01_main_split, "fig04_twin_set": fig04_twin_set,
        "fig05_controls": fig05_controls, "fig10_answer_span": fig10_answer_span,
        "fig11_orthogonal": fig11_orthogonal, "figA1_agents": figA1_agents}  # post order; fixed names  # fmt: skip
