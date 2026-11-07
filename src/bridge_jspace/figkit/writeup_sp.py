"""The write-up's pilot figures on styles-plot (https://github.com/danorel/styles-plot, pinned in pyproject.toml): the
key figure, Fig. 1, 4, 9, 12 and appendix B f17 / f17b. Same figures and file names as figkit/writeup_v2.py; the
library draws them from declarations, with every word from plotstyle.toml and every status from its registry
(data/figures/status_sp.csv). The numbers are read from the data files by the same accessors as before.

uv run python -m bridge_jspace.figkit.writeup_sp [ids...]
"""

from __future__ import annotations

import csv
import sys
from functools import cache
from pathlib import Path

import styles_plot as sp

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit import terms as TM
from bridge_jspace.figkit import writeup_figs as W

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "figures" / "writeup"
TARGET = "post"
ZK = W.ZK  # model key -> short id (the registry's cell suffix)
MODEL = {k: m for m, k in ZK.items()}
BAND, LAYER = "Band of layers · fact passages", "One layer · locker scenes"


@cache
def vocab() -> sp.Vocab:
    return sp.load(REPO / "plotstyle.toml")


def need(c, what: str):
    """A value every figure must have: a missing one stops the build (it is never drawn as a guess)."""
    if c is None:
        raise ValueError(f"no data for {what}")
    return c


def est(c, cell, key=None, label=False, interval=True, note=None) -> sp.Est:
    """A data cell (value, lo, hi) as an estimate; interval=False draws the dot alone."""
    lo, hi = (c[1], c[2]) if interval and len(c) > 2 and c[1] is not None else (None, None)
    return sp.Est(c[0], lo, hi, cell=cell, key=key, label=label, note=note)


# ---- Fig. 1: the main split --------------------------------------------------------------------------------------------
def _layer_gap(m: str) -> sp.Est:
    k = ZK[m]
    g = D.x(f"contrast_{D.SHORT.get(m, '-')}")
    if g is None:  # aggregate only: the difference of the two shares, no interval (said in the cell)
        rc, lk = need(S.conflict(m, "recall"), m)[0], need(S.conflict(m, "lookup"), m)[0]
        return sp.Est(rc - lk, cell=f"layer.{k}", key=f"contrast.{k}", label=True, note="no interval")
    return est(g, f"layer.{k}", key=f"contrast.{k}", label=True)


def _band_columns(models, label_gap=True) -> list:
    """The band test's two panels: each reader's accuracy drop, and the gap with its whisker and the grey tick."""
    drop = sp.DotColumn(
        "accuracy drop", "drop", (-4, 70), (0, 30, 60),
        series=[sp.Series("lookup", {m: est(D.b(f"ko.{ZK[m]}.lostK"), f"band.{ZK[m]}", interval=False) for m in models}),
                sp.Series("recall", {m: est(D.b(f"ko.{ZK[m]}.lostM"), f"band.{ZK[m]}", interval=False) for m in models})],
        connect=("lookup", "recall"),
    )  # fmt: skip
    gap = sp.DotColumn(
        "gap: recall − lookup", "gap", (-4, 98), (0, 30, 60),
        series=[sp.Series("recall", {m: est(D.b(f"ko.{ZK[m]}.mk"), f"band.{ZK[m]}", key=f"ko.{ZK[m]}.mk",
                                            label=label_gap) for m in models})],
        ticks={m: need(S.ctrl(ZK[m]), f"ctrl {m}") for m in models},
    )  # fmt: skip
    return [drop, gap]


def fig01_main_split() -> sp.Figure:
    """Left, band of layers (fact passages): each reader's accuracy drop under the knock-out; the gap with its 95%
    whisker and the largest same-size control as a grey tick. Right, one layer (locker scenes): each reader's switches
    blocked beyond random on the grey band, and the gap. Hollow, tags and "no interval" come from the registry and
    the data."""
    models = [m for m, _ in D.DAN]
    shares = sp.DotColumn(
        "switches blocked beyond random", "switches", (-0.25, 1.0), (0, 0.5, 1),
        series=[sp.Series("lookup", {m: est(S.conflict(m, "lookup"), f"layer.{ZK[m]}") for m in models}),
                sp.Series("recall", {m: est(S.conflict(m, "recall"), f"layer.{ZK[m]}") for m in models})],
        connect=("lookup", "recall"), band=(-0.1, 0.1),
    )  # fmt: skip
    layer_gap = sp.DotColumn("gap: recall − lookup", "gap_share", (-0.1, 1.1), (0, 0.5, 1),
                             series=[sp.Series("recall", {m: _layer_gap(m) for m in models})])  # fmt: skip
    table = sp.DotTable(models, [sp.ColumnGroup(BAND, _band_columns(models)), sp.Gutter(),
                                 sp.ColumnGroup(LAYER, [shares, layer_gap])])  # fmt: skip
    return sp.Figure("fig01_main_split", vocab()).add(table)


# ---- Fig. 4: the twin set ----------------------------------------------------------------------------------------------
LANES = (("paper10", None), ("paper10_rot", "control"), ("paper10_keepA", "answer"))


def fig04_twin_set() -> sp.Figure:
    """Rows are models (the items, recall / lookup, on the row's second line); columns recall twins, lookup twins, gap.
    Three lanes per row: the knock-out (the reader's colour), rotated (grey), answer span kept (brick). The unedited
    accuracy is one grey line above the table (its range over every model)."""
    v = vocab()
    models = [MODEL[k] for k, _ in W.TWIN_MODELS]
    sub = {}
    for m in models:
        nr, nl = W.writeup_n(f"fig04.recall.unedited.{ZK[m]}"), W.writeup_n(f"fig04.lookup.unedited.{ZK[m]}")
        if nr and nl:
            sub[m] = f"{nr} / {nl} items"

    def series(reader, conds, unit_key, data_key):
        out = []
        for cond, role in conds:
            cells = {}
            for m in models:
                c = W.w(data_key(cond, ZK[m]))
                if c is not None:
                    cells[(m, cond)] = est(c, f"{unit_key}.{cond}.{ZK[m]}", key=data_key(cond, ZK[m]), label=True,
                                           interval=unit_key == "gap")  # fmt: skip
            out.append(sp.Series(role or reader, cells, control="rotated" if role == "control" else None))
        return out

    def accuracy(reader):
        return sp.DotColumn(f"{reader} twins", "accuracy", (-4, 106), (0, 50, 100),
                            series=series(reader, LANES, reader, lambda c, k: f"fig04.{reader}.{c}.{k}"))  # fmt: skip

    gap = sp.DotColumn("gap: recall − lookup", "gap", (-12, 74), (0, 30, 60),
                       series=series("recall", LANES[:2], "gap", lambda c, k: f"fig04.gap.{c}.{k}"))  # fmt: skip
    unedited = [c[0] for r in ("recall", "lookup") for m in models if (c := W.w(f"fig04.{r}.unedited.{ZK[m]}"))]
    note = ""
    if len(unedited) == 2 * len(models):  # "every model" only when every cell has its source
        lo, hi = v.format(min(unedited), "accuracy"), v.format(max(unedited), "accuracy")
        note = f"unedited: {lo}–{hi}% right on every model" if lo != hi else f"unedited: {lo}% right on every model"
    table = sp.DotTable(models, [accuracy("recall"), accuracy("lookup"), gap], row_sub=sub,
                        lanes=[sp.Lane(c) for c, _ in LANES], note=note)  # fmt: skip
    return sp.Figure("fig04_twin_set", v).add(table)


# ---- Fig. 9: sentence order --------------------------------------------------------------------------------------------
def fig09_order() -> sp.Figure:
    """Per model two lanes, the sentence (locker or fact) before the pick and after it, both in the lookup's colour: a
    second condition of the lookup is a lane named in words, never a shade. Left locker scenes, right fact passages."""
    from bridge_jspace.figkit import claim_figs as CF

    models = [m for m, _ in D.DAN if D.s(m, CF.ORDER_Q.format("before the pick"), "fig03")]
    when = (("first", "before the pick"), ("after", "after the pick"))

    def column(ds, header):
        cells = {}
        for m in models:
            k = ZK[m]
            if ds == "facts" and m not in CF.ZACH_L:
                cells[(m, "first")] = sp.Missing("no run")
                continue
            for w, pick in when:
                q = CF.ORDER_Q.format(pick) if ds == "locker" else CF.ZACH_Q.format(CF.ZACH_L[m], w)
                cells[(m, w)] = est(D.s(m, q, "fig03"), f"{ds}.{w}.{k}", key=f"order.{ds}.{w}.{k}", label=True)
        return sp.DotColumn(header, "lookups_switched", (0, 1.2), (0, 0.5, 1), series=[sp.Series("lookup", cells)])

    table = sp.DotTable(models, [column("locker", "Locker scenes"), column("facts", "Fact passages")],
                        lanes=[sp.Lane("first", "sentence before the pick"),
                               sp.Lane("after", "sentence after the pick")])  # fmt: skip
    return sp.Figure("fig09_order", vocab()).add(table)


# ---- Fig. 12: the pointer ----------------------------------------------------------------------------------------------
PTR_KEY = {"swap": "swap", "neutral": "neutral_pts", "noown": "noown_pts", "rot": "rot_pts"}


@cache
def _ptr_n(k: str) -> str:
    with (D.REPO / "docs/breadth/data.csv").open() as f:
        return next((r["n"] for r in csv.DictReader(f) if r["key"] == f"ptr.{k}.swap"), "")


def fig12_pointer() -> sp.Figure:
    """Models are rows (the pointer run's items on the row's second line); the conditions are columns, two per table:
    another entity's own passage and one neutral sentence about it on top; without its own-word directions and rotated
    below, beside the paired difference neutral sentence − own passage."""
    models = [MODEL[k] for k, _ in W.TWIN_MODELS]
    sub = {m: f"{_ptr_n(ZK[m])} items" for m in models if _ptr_n(ZK[m])}

    def cells(cond):
        out = {}
        for m in models:
            c = D.b(f"ptr.{ZK[m]}.{PTR_KEY[cond]}")
            out[m] = (est(c, f"{cond}.{ZK[m]}", key=f"ptr.{ZK[m]}.{PTR_KEY[cond]}", label=True) if c
                      else sp.Missing("no run"))  # fmt: skip
        return out

    def panel(cond, header):
        role = "control" if cond == "rot" else "lens"
        return sp.DotColumn(header, "moved", (-8, 96), (0, 40, 80),
                            series=[sp.Series(role, cells(cond), control="rotated" if role == "control" else None)])  # fmt: skip

    def diff(m):
        key = f"ptr.{ZK[m]}.neutral_minus_swap"
        d = D.b(key)
        return sp.Est(d[0], d[1], d[2], key=key) if d else sp.Missing("no run")

    top = sp.DotTable(models, [panel("swap", "another entity's own passage"),
                               panel("neutral", "one neutral sentence about another entity")], row_sub=sub,
                      note="another entity: one of the same kind · answers moved to its fact")  # fmt: skip
    bottom = sp.DotTable(models, [panel("noown", "without another entity's own-word directions"),
                                  panel("rot", "rotated"),
                                  sp.TextColumn("neutral sentence − own passage", "moved_difference",
                                                {m: diff(m) for m in models})],
                         note="the pointer runs: a different item set from Fig. 6's swap")  # fmt: skip
    return sp.Figure("fig12_pointer", vocab()).add(top, bottom)


# ---- appendix B f17: attention under the address swap; f17b: the top 10 heads --------------------------------------------
ATT = "attention mass on slot {}'s locker sentence, {} (mean of five heads, read half)"
ATT_Q = (("switched", "the swap, answer switched", "address", "answer switched"),
         ("stayed", "the swap, answer stayed", "address", "answer stayed"),
         ("nochange", "no change, switched pairs", "no change", "no change"),
         ("random", "a random vector, switched pairs", "a random vector", "a random vector"))  # fmt: skip


def appB_f17_attention() -> sp.Figure:
    """Per model four lanes (the address swap with the answer switched, with it staying; no change; a random vector),
    the last token's attention on the old and the new locker sentence: the swap in the address colour, the two
    controls grey, each lane named in words."""
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")

    def column(slot, header):
        series = []
        for q, quantity, who, _label in ATT_Q:
            control = who if who != "address" else None
            cells = {}
            for m in models:
                v = D.s(m, ATT.format(slot, quantity), "fig13")
                cells[(m, q)] = est(v, f"att.{'old' if slot == 'j' else 'new'}.{q}.{ZK[m]}",
                                    key=f"att.{slot}.{q}.{ZK[m]}", label=True, interval=control is None)  # fmt: skip
            series.append(sp.Series("control" if control else "address", cells, control=control))
        return sp.DotColumn(header, "attention", (-0.04, 1.0), (0, 0.5, 1), series=series)

    table = sp.DotTable(models, [column("j", "old locker sentence"), column("k", "new locker sentence")],
                        lanes=[sp.Lane(q, label) for q, *_, label in ATT_Q])  # fmt: skip
    return sp.Figure("appB_f17_attention", vocab()).add(table)


BAR = 0.5  # the rule fixed in advance (curve_figs.f_attention's "rule: 0.5")


def appB_f17b_heads() -> sp.Figure:
    """Zeroing the top 10 heads against 10 random heads (the share of the address swap's switches cut), with the bar
    fixed in advance; the numbers beside."""
    v = vocab()
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
    cut = {m: D.s(m, "last token, top 10: share of the swap's switch cut", "ledger_heads") for m in models}
    rnd = {m: D.s(m, "last token, top 10: random sets' mean cut", "ledger_heads") for m in models}
    top = {m: est(cut[m], f"heads.top10.{ZK[m]}", key=f"heads.top10.{ZK[m]}") for m in models}
    ran = {m: est(rnd[m], f"heads.random10.{ZK[m]}", key=f"heads.random10.{ZK[m]}", interval=False) for m in models}
    heads = sp.DotColumn(
        "zeroing the top 10 heads", "cut", (-0.15, 0.66), (0, 0.25, 0.5),
        series=[sp.Series("control", ran, control="10 random heads"), sp.Series("address", top)],
        rules=[sp.Rule(BAR, TM.RULE_BAR.format(v.format(BAR, "cut")))],
    )  # fmt: skip
    table = sp.DotTable(list(models), [heads, sp.TextColumn("top 10 heads", "cut", top),
                                       sp.TextColumn("10 random heads", "cut", ran)],
                        note="under the address swap")  # fmt: skip
    return sp.Figure("appB_f17b_heads", v).add(table)


# ---- the key figure ----------------------------------------------------------------------------------------------------
def key() -> sp.Figure:
    """The grammar on one image (roles, controls, marks, missing words), with one example row from Fig. 1's data (the
    27B's band test: both readers' drops, the gap with its whisker and the grey tick) read aloud."""
    v, m = vocab(), "qwen3.6-27b"
    k = ZK[m]
    lk, rc, mk = (need(D.b(f"ko.{k}.{q}"), f"ko.{k}.{q}") for q in ("lostK", "lostM", "mk"))
    ctrl = need(S.ctrl(k), f"ctrl {k}")
    read = TM.READ_ALOUD.format(model=v.entity("models", m).name, recall=v.format(rc[0], "drop"),
                                lookup=v.format(lk[0], "drop"), gap=v.format(mk[0], "gap"),
                                ctrl=v.format(ctrl, "gap"))  # fmt: skip
    return sp.key_figure(v, example=sp.DotTable([m], _band_columns([m])), read_aloud=read)


FIGS = {"key": key, "fig01_main_split": fig01_main_split, "fig04_twin_set": fig04_twin_set, "fig09_order": fig09_order,
        "fig12_pointer": fig12_pointer, "appB_f17_attention": appB_f17_attention,
        "appB_f17b_heads": appB_f17b_heads}  # fmt: skip


def build(ids=None, out: Path = OUT) -> list[str]:
    """Save each figure strict for the post; returns the failures (a failed figure writes nothing)."""
    failed = []
    for fid in ids or FIGS:
        try:
            sp.save(FIGS[fid](), out / f"{fid}.png", target=TARGET)
            print(f"ok    {fid}")
        except (sp.StyleError, sp.BuildError) as e:
            failed.append(fid)
            print(f"FAIL  {fid}\n{e}")
    return failed


if __name__ == "__main__":
    sys.exit(1 if build(sys.argv[1:] or None) else 0)
