"""The depth ledger's figures that had no PNG after the redraw (docs pass P3-3, 7 Nov): one figure per ledger card,
drawn from that card's rows of data/figures/depth/data.csv (figure groups ledger_* and fig01d), read by group and
quantity. The cards are in docs/depth/EXPERIMENTS.md; the figure ids are appended to the depth set (figkit/layout.py)
so no other file is renumbered. depth_sp.FIGS includes these.
"""

from __future__ import annotations

import re

import styles_plot as sp

from bridge_jspace import figdata as D
from bridge_jspace.figkit.writeup_sp_base import ZK, est, vocab

DAN = [m for m, _ in D.DAN]
SHARE = (0, 0.5, 1)


def c(group: str, m: str, q: str):
    return D.s(m, q, group)


def models(group: str, qs) -> list[str]:
    return [m for m in DAN if any(c(group, m, q) for q in qs)]


def cells(group, ms, q, fid, lane=None, label=False, interval=True):
    """{row or (row, lane): Est} for one quantity; a model without the row is left out."""
    out = {}
    for m in ms:
        v = c(group, m, q)
        if v:
            out[(m, lane) if lane else m] = est(v, f"c.{ZK[m]}", key=f"{fid}.{_slug(q)}.{ZK[m]}", label=label,
                                                interval=interval)  # fmt: skip
    return out


def lanes_cells(group, ms, fmt, lanes, fid, label=False):
    """{(row, lane): Est} with the quantity formatted per lane."""
    out = {}
    for lane, words in lanes:
        out.update(cells(group, ms, fmt.format(words), fid, lane=lane, label=label))
    return out


def _num(pattern: str, text: str) -> int:
    """The layer number a quantity names (its rows are written by the run scripts with it)."""
    m = re.search(pattern, text)
    if m is None:
        raise ValueError(f"no layer in {text!r}")
    return int(m.group(1))


def _slug(q: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", q.lower()).strip("_")[:60]


def table(fid, ms, cols, lanes=(), note="", kind="models", v=None) -> sp.Figure:
    lane_objs = [sp.Lane(k, label) for k, label in lanes]
    return sp.Figure(fid, v or vocab()).add(sp.DotTable(ms, cols, kind=kind, lanes=lane_objs, note=note))


# ---- t51-12: the recall's drop without the lens part is the item, not its answer --------------------------------------
def fig40_item_not_answer() -> sp.Figure:
    g, fid = "ledger_answer_control", "fig40_item_not_answer"
    q = "main test, recall, switches lost beyond random: {}"
    arms = [("whole", "without the lens part"), ("kept", "lens part out, answer kept"),
            ("answer", "answer directions only")]  # fmt: skip
    ms = models(g, [q.format(a) for _, a in arms])
    col = sp.DotColumn("the recall's switches", "switches", (-0.1, 1.0), SHARE,
                       series=[sp.Series("recall", lanes_cells(g, ms, q, arms, fid))])  # fmt: skip
    return table(fid, ms, [col], lanes=[(k, w) for k, w in arms])


# ---- lightning-layer: Lightning's layer sweep ----------------------------------------------------------------------------
def fig41_lightning_layers() -> sp.Figure:
    g, fid, m = "ledger_lightning_layers", "fig41_lightning_layers", "nemotron-3.5-lightning"
    lines = []
    for role in ("lookup", "recall"):
        pts = sorted((_num(r"L(\d+)", q), v[0]) for q, v in _rows(g, m)
                     if q.startswith("layer sweep") and q.endswith(f"{role} switch rate"))  # fmt: skip
        lines.append(sp.Line(m, role, [x for x, _ in pts], [y for _, y in pts], cell=f"c.{ZK[m]}"))
    v = vocab()
    gate = sp.Rule(0.3, "bar fixed in advance: {}", unit="switched", key=f"{fid}.gate")
    return sp.Figure(fid, v).add(sp.Sweep([m], "layer", "switched", lines, hrules=[gate], ylim=(0, 1.05),
                                          yticks=SHARE))  # fmt: skip


def _rows(group: str, m: str):
    return [(q, v) for (fig, mm, q), v in D.story().items() if fig == group and mm == m]


# ---- t49-2: the ladder, rungs 2 and 3 (the rule compares them) -----------------------------------------------------------
def fig42_ladder() -> sp.Figure:
    g, fid = "fig01d", "fig42_ladder"
    rungs = [("r2", "rung 2"), ("r3", "rung 3")]
    q = "{}: {}: answers lost beyond random"
    ms = models(g, [q.format("rung 2", "recall, locker before the pick")])
    cols = []
    for scene, header, role in (("recall, locker before the pick", "the recall, locker sentence first", "recall"),
                                ("recall, locker after the pick", "the recall, locker sentence after", "recall"),
                                ("lookup, every scene", "the lookup, every scene", "lookup")):  # fmt: skip
        cs = {}
        for lane, r in rungs:
            cs.update(cells(g, ms, q.format(r, scene), fid, lane=lane))
        cols.append(
            sp.DotColumn(header, "drop_beyond_share", (-0.1, 0.6), (0, 0.25, 0.5), series=[sp.Series(role, cs)])
        )
    return table(fid, ms, cols, lanes=rungs)


# ---- b53-6: the lens part's item against the address's item --------------------------------------------------------------
def fig43_follows_both() -> sp.Figure:
    g, fid = "ledger_identity_address", "fig43_follows_both"
    ms = models(g, ["both: B's answer"])
    both = sp.DotColumn("both changed", "recall_answers", (-0.05, 1.0), SHARE,
                        series=[sp.Series("lens", cells(g, ms, "both: B's answer", fid), word="the lens part's item"),
                                sp.Series("address", cells(g, ms, "both: C's answer", fid),
                                          word="the address's item")])  # fmt: skip
    alone = sp.DotColumn("one changed alone", "recall_answers", (-0.05, 1.0), SHARE,
                         series=[sp.Series("lens", cells(g, ms, "lens part alone: B's", fid),
                                           word="the lens part's item"),
                                 sp.Series("address", cells(g, ms, "address alone: C's", fid),
                                           word="the address's item")])  # fmt: skip
    return table(fid, ms, [both, alone])


# ---- b53-1: a number answer, the question before or after the scene ------------------------------------------------------
def fig44_number_answer() -> sp.Figure:
    g, fid = "ledger_twobytwo", "fig44_number_answer"
    order = [("after", "Q after"), ("before", "Q before")]
    lanes = [("after", "question after the scene"), ("before", "question before the scene")]
    ms = models(g, ["Q after, number: recall lost"])
    cols = []
    for reader in ("recall", "lookup"):
        cs = {}
        for lane, words in order:
            cs.update(cells(g, ms, f"{words}, number: {reader} lost", fid, lane=lane))
        cols.append(sp.DotColumn(f"the {reader}", "switches", (-0.2, 1.0), SHARE, series=[sp.Series(reader, cs)]))
    return table(fid, ms, cols, lanes=lanes)


# ---- b52-b: where the answer is readable through the lens, and whether writing it there changes the answer ---------------
def fig45_answer_map() -> sp.Figure:
    g, fid = "ledger_answer_map", "fig45_answer_map"
    sets = [("ours", "ours", "our scenes"), ("facts", "Zach's", "the fact passages")]
    ms = [m for m in DAN if _rows(g, m)]
    read_cols, write_cols = {}, {}
    for reader in ("lookup", "recall"):
        rd, wr = {}, {}
        for lane, key, _label in sets:
            for m in ms:
                r = D.s_match(m, rf"{re.escape(key)}, {reader}: best top-5 share before the answer layer", g)
                w = D.s_match(m, rf"{re.escape(key)}, {reader}: answers changed by the write", g)
                if r:
                    rd[(m, lane)] = est(r[1], f"c.{ZK[m]}", key=f"{fid}.read.{lane}.{reader}.{ZK[m]}")
                if w:
                    wr[(m, lane)] = est(w[1], f"c.{ZK[m]}", key=f"{fid}.write.{lane}.{reader}.{ZK[m]}")
        read_cols[reader], write_cols[reader] = rd, wr
    readable = sp.DotColumn("readable", "readable", (-0.05, 1.05), SHARE,
                            series=[sp.Series(r, read_cols[r]) for r in ("lookup", "recall")])  # fmt: skip
    usable = sp.DotColumn("changed by adding its directions", "changed", (-0.05, 1.05), SHARE,
                          series=[sp.Series(r, write_cols[r]) for r in ("lookup", "recall")])  # fmt: skip
    return table(fid, ms, [readable, usable], lanes=[(k, label) for k, _q, label in sets])


# ---- t47-7c: prose, JSON and tables: the value route stays empty -----------------------------------------------------------
def fig46_value_formats() -> sp.Figure:
    g, fid = "ledger_value_formats", "fig46_value_formats"
    fmts = [("prose", "prose"), ("json", "json"), ("table", "table")]
    lanes = [("prose", "prose"), ("json", "JSON"), ("table", "a table")]
    q = "{}, whole change: {} share"
    ms = models(g, [q.format(f, "position") for f, _ in fmts])
    pos = {k: v for f, _ in fmts for k, v in cells(g, ms, q.format(f, "position"), fid, lane=f).items()}
    val = {k: v for f, _ in fmts for k, v in cells(g, ms, q.format(f, "value"), fid, lane=f).items()}
    cols = [sp.DotColumn("by position", "identity_share", (-0.05, 0.6), (0, 0.25, 0.5), series=[sp.Series("address", pos)]),
            sp.DotColumn("by value", "identity_share", (-0.05, 0.6), (0, 0.25, 0.5),
                         series=[sp.Series("neutral", val, word="by value")])]  # fmt: skip
    return table(fid, ms, cols, lanes=lanes)


# ---- b53-8: the item's identity code at its locker sentence --------------------------------------------------------------
def fig47_identity_code() -> sp.Figure:
    g, fid = "ledger_bindid", "fig47_identity_code"
    lanes = [("pre", "pre-specified"), ("cen", "centered")]
    ms = models(g, ["centered: X's vector"])
    own, other, rnd = {}, {}, {}
    for lane, words in lanes:
        own.update(cells(g, ms, f"{words}: X's vector", fid, lane=lane))
        other.update(cells(g, ms, f"{words}: Y's version", fid, lane=lane))
        rnd.update(cells(g, ms, f"{words}: random", fid, lane=lane))
    col = sp.DotColumn("lookups moved", "lookups", (-0.02, 0.6), (0, 0.25, 0.5),
                       series=[sp.Series("control", rnd, control="a random vector"),
                               sp.Series("neutral", other, word="another item's version"),
                               sp.Series("identity", own, word="the item's own code")])  # fmt: skip
    return table(fid, ms, [col], lanes=[(k, "pre-specified code" if k == "pre" else "centered code") for k, _ in lanes])


# ---- b53-5: the 27B's position scenes ------------------------------------------------------------------------------------
def fig48_subset27b() -> sp.Figure:
    g, fid = "ledger_subset27b", "fig48_subset27b"
    ms = models(g, ["the address alone"])
    without = sp.DotColumn("position answers left", "position_share", (-0.02, 0.6), (0, 0.25, 0.5),
                           series=[sp.Series("control", cells(g, ms, "without a random part", fid), control="a random part"),
                                   sp.Series("address", cells(g, ms, "without the address", fid),
                                             word="without the address")])  # fmt: skip
    alone = sp.DotColumn("position answers brought back", "position_share", (-0.02, 0.6), (0, 0.25, 0.5),
                         series=[sp.Series("control", cells(g, ms, "a random part alone", fid), control="a random part"),
                                 sp.Series("address", cells(g, ms, "the address alone", fid),
                                           word="the address alone")])  # fmt: skip
    return table(fid, ms, [without, alone])


# ---- t49-6: the report, reworded -----------------------------------------------------------------------------------------
def fig49_report_first_position() -> sp.Figure:
    g, fid = "ledger_report_slot1", "fig49_report_first_position"
    lanes = [("earlier", "the earlier report wording"), ("digit", "position wording (a digit)"),
             ("word", "sentence wording (a word)")]  # fmt: skip
    ms = models(g, [w for _, w in lanes])
    cs = {}
    for lane, words in lanes:
        cs.update(cells(g, ms, words, fid, lane=lane))
    col = sp.DotColumn("reports naming the first position", "reports", (-0.02, 1.05), SHARE,
                       series=[sp.Series("neutral", cs, word="reports naming the first position")])  # fmt: skip
    return table(fid, ms, [col], lanes=[("earlier", "the earlier wording"), ("digit", "a digit asked for"),
                                        ("word", "a word asked for")])  # fmt: skip


# ---- t51-4: the bridge-fit swap at the last token -------------------------------------------------------------------------
def fig50_last_token_swap() -> sp.Figure:
    g, fid = "ledger_last_token_address", "fig50_last_token_swap"
    q = "bridge-fit swap at L+4, dose 2: lookups sent to the target"
    ms = models(g, [q])
    col = sp.DotColumn("the address swapped in at the last token", "sent_written", (-0.02, 0.6), (0, 0.25, 0.5),
                       series=[sp.Series("address", cells(g, ms, q, fid, label=True))])  # fmt: skip
    return table(fid, ms, [col])


# ---- b53-3: the conflict test at the last token -----------------------------------------------------------------------------
def _two_layers(g, m, reader, stem):
    """This reader's two tested layers (as run), earlier first, as (layer, cell)."""
    pts = []
    for q, v in _rows(g, m):
        mm = re.match(rf"{reader} L(\d+): {re.escape(stem)}$", q)
        if mm:
            pts.append((int(mm.group(1)), v))
    return sorted(pts)


def fig51_last_conflict() -> sp.Figure:
    g, fid = "ledger_last_conflict", "fig51_last_conflict"
    stem = "switches lost without the lens part beyond random (last token)"
    ms = [m for m in DAN if _two_layers(g, m, "recall", stem)]
    cols = []
    for reader in ("lookup", "recall"):
        cs = {}
        for m in ms:
            for lane, (layer, v) in zip(("first", "second"), _two_layers(g, m, reader, stem), strict=False):
                cs[(m, lane)] = est(v, f"c.{ZK[m]}", key=f"{fid}.{reader}.L{layer}.{ZK[m]}")
        cols.append(sp.DotColumn(f"the {reader}", "switches", (-0.15, 1.0), SHARE, series=[sp.Series(reader, cs)]))
    return table(fid, ms, cols, lanes=[("first", "the earlier layer tested"), ("second", "the later layer tested")])


# ---- b53-3b: the same with words as answers -----------------------------------------------------------------------------------
def fig52_last_conflict_words() -> sp.Figure:
    g, fid = "ledger_last_conflict_words", "fig52_last_conflict_words"
    steps = [("a3", "answer - 3", "three layers before the answer"),
             ("a2", "answer - 2: uninformative", "two layers before the answer"),
             ("a1", "answer - 1: uninformative", "one layer before the answer"),
             ("peak", "read peak", "the read peak")]  # fmt: skip
    ms = models(g, ["words, recall, answer - 3"])
    cols = []
    for reader in ("lookup", "recall"):
        cs = {}
        for lane, words, _label in steps:
            cs.update(cells(g, ms, f"words, {reader}, {words}", fid, lane=lane))
        cols.append(sp.DotColumn(f"the {reader}", "switches", (-0.15, 1.05), SHARE, series=[sp.Series(reader, cs)]))
    return table(fid, ms, cols, lanes=[(k, label) for k, _w, label in steps])


# ---- b53-4: Lightning's attention blocks ------------------------------------------------------------------------------------
BLOCKS = [("i", "(i) block 19", "block 19"), ("ii", "(ii) block 26", "block 26"),
          ("iii", "(iii) blocks 19, 26", "blocks 19 and 26"), ("iv", "(iv) all after L", "every block after L"),
          ("v", "(v) control", "a control block"), ("span", "follow-up: span", "the follow-up span"),
          ("cspan", "follow-up: control span", "a control span")]  # fmt: skip


def fig53_attention_blocks() -> sp.Figure:
    g, fid, m = "ledger_attnblock", "fig53_attention_blocks", "nemotron-3.5-lightning"
    v = vocab().with_entities("blocks", [(k, label) for k, _q, label in BLOCKS])
    cols = []
    for reader in ("lookup", "recall"):
        cs = {}
        for k, q, _label in BLOCKS:
            val = c(g, m, f"{reader}: {q}")
            if val:
                cs[k] = est(val, f"c.{ZK[m]}", key=f"{fid}.{reader}.{k}")
        cols.append(
            sp.DotColumn(f"the {reader}", "switches", (-0.1, 0.7), (0, 0.25, 0.5), series=[sp.Series(reader, cs)])
        )
    return table(fid, [k for k, *_ in BLOCKS], cols, kind="blocks", v=v)


# ---- b53-1b: the fact passages, named bridge: the answer control ------------------------------------------------------------
def fig54_fact_answer_control() -> sp.Figure:
    g, fid = "ledger_jsuite", "fig54_fact_answer_control"
    chains = [("pp", "PP lookup", "lookup"), ("pm", "PM recall", "recall"), ("mp", "MP lookup", "lookup"),
              ("mm", "MM recall", "recall")]  # fmt: skip
    ms = models(g, ["PM recall: without the lens part"])
    cols = []
    for arm, header in (("without the lens part", "without the lens part"),
                        ("answer directions only", "answer directions only")):  # fmt: skip
        by_role = {"lookup": {}, "recall": {}}
        for lane, q, role in chains:
            by_role[role].update(cells(g, ms, f"{q}: {arm}", fid, lane=lane))
        cols.append(sp.DotColumn(header, "switches", (-0.25, 1.0), SHARE,
                                 series=[sp.Series(r, by_role[r]) for r in ("lookup", "recall")]))  # fmt: skip
    return table(fid, ms, cols, lanes=[(k, q.split()[0]) for k, q, _r in chains])


# ---- t51-7: the change at every layer up to L ---------------------------------------------------------------------------------
def fig55_every_layer() -> sp.Figure:
    g, fid = "ledger_full_carrier", "fig55_every_layer"
    orders = [("first", "fact-first", "fact sentence first"), ("after", "fact-after", "fact sentence after")]
    q = "{}, {}, {}: switches lost beyond random"
    ms = models(g, [q.format("fact-first", "recall", "one layer")])
    cols = []
    for span, header in (("one layer", "at one layer"), ("every layer to L", "at every layer up to L")):
        series = []
        for reader in ("lookup", "recall"):
            cs = {}
            for lane, words, _label in orders:
                cs.update(cells(g, ms, q.format(words, reader, span), fid, lane=lane))
            series.append(sp.Series(reader, cs))
        cols.append(sp.DotColumn(header, "switches", (-0.1, 1.0), SHARE, series=series))
    return table(fid, ms, cols, lanes=[(k, label) for k, _w, label in orders])


# ---- z3: the routes on the fact passages --------------------------------------------------------------------------------------
def fig56_fact_routes() -> sp.Figure:
    g, fid = "ledger_zach_routes", "fig56_fact_routes"

    ms = [m for m in DAN if _rows(g, m)]
    cols = {"identity": {}, "position": {}, "value": {}}
    for m in ms:
        layers = sorted({_num(r"^L(\d+)", q) for q, _v in _rows(g, m)})
        for lane, layer in zip(("first", "second"), layers, strict=False):
            for route in cols:
                val = c(g, m, f"L{layer}, whole change: {route} share")
                if val:
                    cols[route][(m, lane)] = est(val, f"c.{ZK[m]}", key=f"{fid}.{route}.L{layer}.{ZK[m]}")
    out = [sp.DotColumn("by identity", "identity_share", (-0.05, 0.8), (0, 0.25, 0.5),
                        series=[sp.Series("identity", cols["identity"])]),
           sp.DotColumn("by position", "identity_share", (-0.05, 0.8), (0, 0.25, 0.5),
                        series=[sp.Series("address", cols["position"])]),
           sp.DotColumn("by value", "identity_share", (-0.05, 0.8), (0, 0.25, 0.5),
                        series=[sp.Series("neutral", cols["value"], word="by value")])]  # fmt: skip
    return table(fid, ms, out, lanes=[("first", "the earlier layer tested"), ("second", "the later layer tested")])


# ---- t51-5: the fact passages' read window --------------------------------------------------------------------------------------
def fig57_read_window() -> sp.Figure:
    g, fid = "ledger_read_window", "fig57_read_window"
    ms = [m for m in DAN if _rows(g, m)]
    lines = []
    for m in ms:
        for role in ("lookup", "recall"):
            pts = sorted((_num(r"layer (\d+)", q), v[0]) for q, v in _rows(g, m)
                         if q.endswith(f": {role} switched"))  # fmt: skip
            lines.append(sp.Line(m, role, [x for x, _ in pts], [y for _, y in pts], cell=f"c.{ZK[m]}"))
    gate = sp.Rule(0.3, "bar fixed in advance: {}", unit="switched", key=f"{fid}.gate")
    return sp.Figure(fid, vocab()).add(sp.Sweep(ms, "layer", "switched", lines, hrules=[gate], ylim=(0, 1.05),
                                                yticks=SHARE))  # fmt: skip


# ---- t49-3: who picked the item, read at its locker sentence ------------------------------------------------------------------
def fig58_person_probe() -> sp.Figure:
    g, fid = "ledger_pooled_probe", "fig58_person_probe"
    ms = [m for m in DAN if _rows(g, m)]
    pooled, single = {}, {}
    for m in ms:
        layers = sorted({_num(r"^L(\d+)", q) for q, _v in _rows(g, m)})
        for lane, layer in zip(("half", "full"), layers, strict=False):
            p = c(g, m, f"L{layer}: who picked it, pooled over the locker sentence")
            s1 = c(g, m, f"L{layer}: who picked it, best single token")
            if p:
                pooled[(m, lane)] = est(p, f"c.{ZK[m]}", key=f"{fid}.pooled.L{layer}.{ZK[m]}")
            if s1:
                single[(m, lane)] = est(s1, f"c.{ZK[m]}", key=f"{fid}.single.L{layer}.{ZK[m]}")
    cols = [sp.DotColumn("pooled over the locker sentence", "probe_accuracy", (0, 1.0), SHARE,
                         series=[sp.Series("neutral", pooled, word="pooled over the locker sentence")]),
            sp.DotColumn("the best single token", "probe_accuracy", (0, 1.0), SHARE,
                         series=[sp.Series("neutral", single, word="the best single token")])]  # fmt: skip
    return table(fid, ms, cols, lanes=[("half", "half the test layer"), ("full", "the test layer")])


# ---- t47-11: the address on other kinds of item ---------------------------------------------------------------------------------
def fig59_any_item() -> sp.Figure:
    g, fid = "ledger_agnostic", "fig59_any_item"
    kinds = [("animals", "animals"), ("fruits", "fruits"), ("names", "names")]
    ms = models(g, ["animals: position lost without the animal-fit address, beyond random"])
    fit, refit = {}, {}
    for lane, k in kinds:
        fit.update(cells(g, ms, f"{k}: position lost without the animal-fit address, beyond random", fid, lane=lane))
        refit.update(cells(g, ms, f"{k}: position lost without the refit address, beyond random", fid, lane=lane))
    cols = [sp.DotColumn("without the address fit on animals", "position_lost", (-0.05, 0.8), (0, 0.25, 0.5),
                         series=[sp.Series("address", fit)]),
            sp.DotColumn("without the address refit on that kind", "position_lost", (-0.05, 0.8), (0, 0.25, 0.5),
                         series=[sp.Series("address", refit)])]  # fmt: skip
    return table(fid, ms, cols, lanes=kinds)


# ---- z2: the described bridge, both operations ------------------------------------------------------------------------------------
def fig60_described_gap() -> sp.Figure:
    g, fid = "ledger_described", "fig60_described_gap"
    ms = [m for m in DAN if _rows(g, m)]
    ours, theirs = {}, {}
    for m in ms:
        o = D.s_match(m, r"L\d+: our gap \(recall minus lookup extra loss\)", g)
        t = c(g, m, "Zach's knock-out, recall minus lookup")
        ours[m] = est(o[1], f"c.{ZK[m]}", key=f"{fid}.ours.{ZK[m]}") if o else sp.Missing("no run")
        if t:
            theirs[m] = est(t, f"c.{ZK[m]}", key=f"{fid}.removal.{ZK[m]}")
    cols = [sp.DotColumn("the change at one layer", "gap_share", (-0.8, 0.8), (-0.5, 0, 0.5),
                         series=[sp.Series("neutral", ours, word="the change at one layer")]),
            sp.DotColumn("removal everywhere", "gap_answers", (-0.8, 0.8), (-0.5, 0, 0.5),
                         series=[sp.Series("neutral", theirs, word="removal everywhere")])]  # fmt: skip
    return table(fid, ms, cols)


FIGS = {f.__name__: f for f in (
    fig40_item_not_answer, fig41_lightning_layers, fig42_ladder, fig43_follows_both, fig44_number_answer,
    fig45_answer_map, fig46_value_formats, fig47_identity_code, fig48_subset27b, fig49_report_first_position,
    fig50_last_token_swap, fig51_last_conflict, fig52_last_conflict_words, fig53_attention_blocks,
    fig54_fact_answer_control, fig55_every_layer, fig56_fact_routes, fig57_read_window, fig58_person_probe,
    fig59_any_item, fig60_described_gap)}  # fmt: skip
# card → figure (docs/depth/EXPERIMENTS.md anchors); x45d's figure already exists (fig09_transfer, panel b is 45d)
CARD = {"t51-12": "fig40_item_not_answer", "lightning-layer": "fig41_lightning_layers", "t49-2": "fig42_ladder",
        "b53-6": "fig43_follows_both", "b53-1": "fig44_number_answer", "b52-b": "fig45_answer_map",
        "t47-7c": "fig46_value_formats", "b53-8": "fig47_identity_code", "b53-5": "fig48_subset27b",
        "t49-6": "fig49_report_first_position", "t51-4": "fig50_last_token_swap", "b53-3": "fig51_last_conflict",
        "b53-3b": "fig52_last_conflict_words", "b53-4": "fig53_attention_blocks", "b53-1b": "fig54_fact_answer_control",
        "t51-7": "fig55_every_layer", "z3": "fig56_fact_routes", "t51-5": "fig57_read_window",
        "t49-3": "fig58_person_probe", "t47-11": "fig59_any_item", "z2": "fig60_described_gap",
        "x45d": "fig09_transfer"}  # fmt: skip
