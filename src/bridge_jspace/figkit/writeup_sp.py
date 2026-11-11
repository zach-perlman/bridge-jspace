"""The write-up's pilot figures on styles-plot (https://github.com/danorel/styles-plot, pinned in pyproject.toml): the
key figure, Fig. 1, 4, 9, 12 and appendix B f17 / f17b. Same figures and file names as figkit/writeup_v2.py; the
library draws them from declarations, with every word from plotstyle.toml and every status from its registry
(data/figures/status_sp.csv). The numbers are read from the data files by the same accessors as before.

uv run python -m bridge_jspace.figkit.writeup_sp [ids...]
"""

from __future__ import annotations

import csv
import dataclasses
import sys
from functools import cache

import styles_plot as sp

from bridge_jspace import figdata as D
from bridge_jspace import figdata as S
from bridge_jspace import figdata as TM
from bridge_jspace import figdata as W
from bridge_jspace.figkit import layout as L
from bridge_jspace.figkit import writeup_sp_b, writeup_sp_c, writeup_sp_d
from bridge_jspace.figkit.writeup_sp_base import MODEL, ZK, est, need, vocab

GROUP = "common/writeup"
OUT = L.folder(GROUP)
TARGET = "post"
BAND, LAYER = "Band of layers · fact passages", "One layer · locker scenes"
GAP = "gap: recall − lookup"


# ---- Fig. 1: the main split --------------------------------------------------------------------------------------------
def _layer_gap(m: str) -> sp.Est:
    k = ZK[m]
    g = D.x(f"contrast_{D.SHORT.get(m, '-')}")
    if g is None:  # aggregate only: the difference of the two shares, no interval (said in the cell)
        rc, lk = need(S.conflict(m, "recall"), m)[0], need(S.conflict(m, "lookup"), m)[0]
        return sp.Est(rc - lk, cell=f"layer.{k}", key=f"contrast.{k}", label=True, note="no interval")
    return est(g, f"layer.{k}", key=f"contrast.{k}", label=True)


def _band_columns(models, label_gap=True, gap_word=GAP) -> list:
    """The band test's two panels: each reader's accuracy drop, and the gap (headed `gap_word`) with its whisker and
    the grey tick."""
    drop = sp.DotColumn(
        "answers turned wrong", "drop", (-4, 70), (0, 30, 60),
        series=[sp.Series("lookup", {m: est(D.b(f"ko.{ZK[m]}.lostK"), f"band.{ZK[m]}", interval=False) for m in models}),
                sp.Series("recall", {m: est(D.b(f"ko.{ZK[m]}.lostM"), f"band.{ZK[m]}", interval=False) for m in models})],
        connect=("lookup", "recall"),
    )  # fmt: skip
    # a gap is a difference: the neutral role, never the recall's black (Dan, 7 Nov, decision 10)
    gap = sp.DotColumn(
        gap_word, "gap", (-4, 98), (0, 30, 60),
        series=[sp.Series("neutral", {m: est(D.b(f"ko.{ZK[m]}.mk"), f"band.{ZK[m]}", key=f"ko.{ZK[m]}.mk",
                                            label=label_gap) for m in models}, word=gap_word)],
        ticks={m: need(S.ctrl(ZK[m]), f"ctrl {m}") for m in models},
    )  # fmt: skip
    return [drop, gap]


def _made_drop(k: str, reader: str) -> sp.Est:
    """A reader's answers turned wrong on the made-up-fact set: unedited minus knock-out accuracy (points)."""
    u, ko = (need(W.w(f"fig04.{reader}.{c}.{k}"), f"{reader} {c} {k}")[0] for c in ("unedited", "paper10"))
    return sp.Est(u - ko, cell=f"made.{k}")


def fig01_main_split() -> sp.Figure:
    """Band of layers, both fact sets as lanes of each model's row: each reader's answers turned wrong under the
    knock-out (lookup joined to recall) and the gap with its 95% whisker. The known-fact set (docs/breadth/data.csv
    ko.*) has three same-size controls (rotated, logit lens, PCA); the made-up-fact set (fig04_twin_set's rows:
    unedited minus knock-out accuracy, the registered gap) ran only the rotated part. One grey tick per lane: the
    largest same-size control run on that set (Dan, 11 Nov), said so in this figure's key. Muse and the 122B have no
    made-up-fact run. The one-layer half is the post's Figure 3A (patch_split); the README's r1_c1_split /
    r1_c1_gaps keep both halves."""
    models = [m for m, _ in D.DAN]
    lk, rc, gap, tick = {}, {}, {}, {}
    for m in models:
        k = ZK[m]
        known, made = (m, "known"), (m, "made")
        lk[known] = est(need(D.b(f"ko.{k}.lostK"), f"lostK {k}"), f"band.{k}", interval=False)
        rc[known] = est(need(D.b(f"ko.{k}.lostM"), f"lostM {k}"), f"band.{k}", interval=False)
        gap[known] = est(need(D.b(f"ko.{k}.mk"), f"mk {k}"), f"band.{k}", key=f"ko.{k}.mk", label=True)
        tick[known] = need(S.ctrl(k), f"ctrl {m}")
        g = W.w(f"fig04.gap.paper10.{k}")
        if g is None:  # no run on the made-up-fact set
            rc[made], gap[made] = sp.Missing("not run"), sp.Missing("not run")
            continue
        lk[made], rc[made] = _made_drop(k, "lookup"), _made_drop(k, "recall")
        gap[made] = est(g, f"made_gap.{k}", key=f"fig04.gap.paper10.{k}", label=True)
        tick[made] = need(W.w(f"fig04.gap.paper10_rot.{k}"), f"rot {k}")[0]  # its only same-size control
    drop_col = sp.DotColumn("answers turned wrong", "drop", (-4, 82), (0, 30, 60), connect=("lookup", "recall"),
                            series=[sp.Series("lookup", lk), sp.Series("recall", rc)])  # fmt: skip
    gap_col = sp.DotColumn("gap", "gap", (-6, 98), (0, 30, 60), ticks=tick,
                           series=[sp.Series("neutral", gap, word="gap")])
    lanes = [sp.Lane("known", "known-fact set"), sp.Lane("made", "made-up-fact set")]
    table = sp.DotTable(models, [drop_col, gap_col], lanes=lanes)
    v = dataclasses.replace(vocab(), key_tick=RUN_TICK)
    return sp.Figure("fig01_main_split", v, subtitle="method: knock-out, band of middle layers · data: fact passages").add(table)


# fig01's tick: the known-fact set ran three same-size controls, the made-up-fact set one (the rotated part)
RUN_TICK = "the largest same-size control run on that set"


# ---- Fig. 4: the made-up-fact set ----------------------------------------------------------------------------------------------
LANES = (("paper10", None), ("paper10_rot", "control"), ("paper10_keepA", "answer"))
# the conditions named in grey under each model; the colours stay roles (Dan, 7 Nov: labelled lanes)
LANE_WORD = {"paper10": "knock-out", "paper10_rot": "rotated", "paper10_keepA": "answer span kept"}
# each lane's own colour word ("knock-out", "answer span kept") does not fit one line over a post-width accuracy panel
# (SP606, by design), so the lanes keep their roles' words


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

    def series(reader, conds, unit_key, data_key, word=None):
        out = []
        for cond, role in conds:
            cells = {}
            for m in models:
                c = W.w(data_key(cond, ZK[m]))
                if c is not None:
                    cells[(m, cond)] = est(c, f"{unit_key}.{cond}.{ZK[m]}", key=data_key(cond, ZK[m]), label=True,
                                           interval=unit_key == "gap")  # fmt: skip
            out.append(sp.Series(role or reader, cells, control="rotated" if role == "control" else None,
                                 word=None if role else word))  # fmt: skip
        return out

    def accuracy(reader):
        return sp.DotColumn(f"{reader} twins", "accuracy", (-4, 106), (0, 50, 100),
                            series=series(reader, LANES, reader, lambda c, k: f"fig04.{reader}.{c}.{k}"))  # fmt: skip

    # the gap's header is its colour word (styles-plot 0.1.6: no word above the rows); wide enough for one line
    gap = sp.DotColumn(GAP, "gap", (-12, 74), (0, 30, 60), width=2.3,
                       series=series("neutral", LANES[:2], "gap", lambda c, k: f"fig04.gap.{c}.{k}", word=GAP))  # fmt: skip
    unedited = [c[0] for r in ("recall", "lookup") for m in models if (c := W.w(f"fig04.{r}.unedited.{ZK[m]}"))]
    note = ""
    if len(unedited) == 2 * len(models):  # "every model" only when every cell has its source
        lo, hi = v.format(min(unedited), "accuracy"), v.format(max(unedited), "accuracy")
        note = f"unedited: {lo}–{hi}% right on every model" if lo != hi else f"unedited: {lo}% right on every model"
    table = sp.DotTable(models, [accuracy("recall"), accuracy("lookup"), gap], row_sub=sub,
                        lanes=[sp.Lane(c, LANE_WORD[c]) for c, _ in LANES], note=note)  # fmt: skip
    return sp.Figure("fig04_twin_set", v).add(table)


# ---- Fig. 9: sentence order --------------------------------------------------------------------------------------------
def fig09_order() -> sp.Figure:
    """Per model two lanes, the sentence (locker or fact) before the pick and after it, both in the lookup's colour: a
    second condition of the lookup is a lane named in words, never a shade. Left locker scenes, right fact passages."""
    from bridge_jspace import figdata as CF

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
                            series=[sp.Series(role, cells(cond), control="rotated" if role == "control" else None,
                                              word=None if role == "control" else "lens part swapped in")])  # fmt: skip

    def diff(m):
        key = f"ptr.{ZK[m]}.neutral_minus_swap"
        d = D.b(key)
        return sp.Est(d[0], d[1], d[2], key=key) if d else sp.Missing("no run")

    top = sp.DotTable(models, [panel("swap", "another entity's own passage"),
                               panel("neutral", "one neutral sentence about another entity")], row_sub=sub,
                      note="another entity: one of the same kind · answers moved to its fact")  # fmt: skip
    bottom = sp.DotTable(models, [panel("noown", "without another entity's own-word directions"),
                                  panel("rot", "rotated"),
                                  sp.TextColumn("neutral − own passage", "moved_difference",
                                                {m: diff(m) for m in models}, unit_title=False)],
                         note="the lens-part swap runs: a different item set from Fig. 6's swap")  # fmt: skip
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
            series.append(sp.Series("control" if control else "address", cells, control=control,
                                    word=None if control else "address swap"))  # fmt: skip
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
        series=[sp.Series("control", ran, control="10 random heads"), sp.Series("address", top, word="the top 10 heads")],
        rules=[sp.Rule(BAR, TM.RULE_BAR, unit="cut", key="heads.bar")],
    )  # fmt: skip
    table = sp.DotTable(list(models), [heads, sp.TextColumn("top 10 heads", "cut", top, unit_title=False),
                                       sp.TextColumn("random heads", "cut", ran, unit_title=False)],
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
    names = ("recall", "lookup", "gap", "ctrl")
    read = TM.READ_ALOUD.format(model=v.entity("models", m).name, **{n: f"{{{n}}}" for n in names})
    numbers = {"recall": (rc[0], "drop", f"ko.{k}.lostM"), "lookup": (lk[0], "drop", f"ko.{k}.lostK"),
               "gap": (mk[0], "gap", f"ko.{k}.mk"), "ctrl": (ctrl, "gap", f"ko.{k}.ctrl")}  # fmt: skip
    return sp.key_figure(v, example=sp.DotTable([m], _band_columns([m])), read_aloud=read, numbers=numbers)


FIGS = {"key": key, "fig01_main_split": fig01_main_split, "fig04_twin_set": fig04_twin_set, "fig09_order": fig09_order,
        "fig12_pointer": fig12_pointer, "appB_f17_attention": appB_f17_attention,
        "appB_f17b_heads": appB_f17b_heads}  # fmt: skip
FIGS.update(writeup_sp_b.FIGS)
FIGS.update(writeup_sp_c.FIGS)
FIGS.update(writeup_sp_d.FIGS)


# the post's sentence for each figure (the index's "what it shows"); the appendix: its builder's first sentence
TAKEAWAY = {
    "key": "How to read the figures: each colour's role, the marks, one row read aloud",
    "fig00_schematic": "One bridge word, two readers",
    "fig01_main_split": "Taking the lens part out breaks recalled answers, not lookup ones",
    "fig02_datasets": "One question, two kinds of answer, two datasets",
    "fig03_tools": "Three tools, one target: the lens part at the bridge",
    "fig04_twin_set": "On matched twins the knock-out breaks the recall, the lookup much less",
    "fig05a_controls_band": "Same-size removals cost a fraction of what the lens part costs (band of layers)",
    "fig05b_controls_layer": "Same-size removals cost a fraction of what the lens part costs (one layer)",
    "fig06_nine_models": "Carried and needed come apart across models",
    "fig07_routes": "The lookup goes by identity or position, never by the number",
    "fig08a_address_read_remove": "A probe reads the address; removing it stops position answers",
    "fig08b_address_swap_lens": "Swapping the address moves the lookup; the lens does not rebuild it",
    "fig09_order": "The bridge word moves the lookup only when the locker sentence came first",
    "fig10_answer_span": "What recall loses is its answer's own directions",
    "fig11_orthogonal": "Removals made orthogonal to the answers cannot see even the subject",
    "fig12_pointer": "Another entity's lens part moves the recall, even from one neutral sentence",
    "fig13_last_token": "At the last token the lens part reads the entity, yet a 1× swap barely moves the answer",
    "figA1_agents": "Inside agent transcripts, copying and picking survive the knock-out; producing does not",
}  # fmt: skip


def shows() -> dict[str, str]:
    """Each figure's line in the index: its takeaway in bold, then its caption from the caption store
    (figures/common/writeup/_meta/captions.toml); a figure without a caption falls back to its builder's first sentence."""
    from bridge_jspace.figkit import captions

    names = L.names(GROUP)
    out = {}
    for fid, f in FIGS.items():
        stored = captions.load(GROUP).get(names.get(fid, ""), "")
        first = " ".join((f.__doc__ or "").split()).split(". ")[0].rstrip(".")
        lead = f"**{TAKEAWAY[fid]}.** " if fid in TAKEAWAY else ""
        out[fid] = lead + (stored or first)
    return out


def build(ids=None) -> list[str]:
    """Save each figure strict for the post into figures/common/writeup/ (numbered files, figkit/layout.py); returns the
    failures (a failed figure writes nothing)."""
    return L.build(GROUP, FIGS, TARGET, ids, shows())


if __name__ == "__main__":
    sys.exit(1 if build(sys.argv[1:] or None) else 0)
