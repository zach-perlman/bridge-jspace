"""The depth README's last figures on styles-plot (readme target), drawn as Dan decided on 7 Nov: stacks with sub-rows
or with segments that are not roles become dot tables of shares (segments as columns, arms as lanes); a per-row
reference is its own grey control column; lines over a dose or k become dots per dose or k; a gate is a named grey
window, never a faded line. Numbers are the rows the story builders recorded in data/figures/depth/data.csv, read by
figure id and quantity; verdict rows ("the rule holds") are not drawn. depth_sp.FIGS includes these.
"""

from __future__ import annotations

import re

import styles_plot as sp

from bridge_jspace import figdata as D
from bridge_jspace.figkit.writeup_sp_base import ZK, est, vocab

DAN = [m for m, _ in D.DAN]


def cell(fig: str, m: str, q: str):
    return D.s(m, q, fig)


def models_with(fig: str, qs) -> list[str]:
    return [m for m in DAN if any(cell(fig, m, q) for q in qs)]


def shares(fig, models, lanes, stem, outcome, cid, key, lane_role=None, control=None):
    """{(model, lane): Est} of one outcome share per lane; a lane whose role is "control" is left out (its own series)."""
    out = {}
    for m in models:
        for lane, words, *_ in lanes:
            if lane_role and lane_role.get(lane) == "control":
                continue
            c = cell(fig, m, stem.format(arm=words, outcome=outcome))
            if c:
                out[(m, lane)] = est(c, f"{cid}.{ZK[m]}", key=f"{key}.{lane}.{ZK[m]}")
    return out


def outcome_columns(fig, models, lanes, stem, outcomes, unit, cid, key, lim, ticks, control_lane=None, control=None):
    """One dot column per outcome share: its role, or the neutral role named by the column's header; a control lane
    is a grey series of its own in every column."""
    cols = []
    for out_key, outcome, header, role in outcomes:
        cells = {}
        ctrl = {}
        for m in models:
            for lane, words, *_ in lanes:
                c = cell(fig, m, stem.format(arm=words, outcome=outcome))
                if not c:
                    continue
                e = est(c, f"{cid}.{ZK[m]}", key=f"{key}.{out_key}.{lane}.{ZK[m]}")
                (ctrl if lane == control_lane else cells)[(m, lane)] = e
        series = [sp.Series(role, cells, word=header if role == "neutral" else None)]
        if ctrl:
            series.insert(0, sp.Series("control", ctrl, control=control))
        cols.append(sp.DotColumn(header, unit, lim, ticks, series=series))
    return cols


# ---- fig09c: the pick sentence blocked (47.6 b) ------------------------------------------------------------------------
F09C_LANES = (("none", "none", "the whole change"), ("block", "block/sentence/all", "the pick sentence blocked"),
              ("control", "control/sentence/all", "a control block"))  # fmt: skip
LOOKUP_OUTCOMES = (("identity", "identity", "by identity", "identity"), ("position", "position", "by position", "address"),
                   ("original", "original", "the original answer", "neutral"),
                   ("value", "value", "the number", "neutral"), ("other", "other", "other answers", "neutral"))  # fmt: skip


def fig09c_formation() -> sp.Figure:
    """47.6 (b), fixed in advance: the lookup's answers under the whole change, with the pick sentence's attention
    blocked, and with a control block (grey), as one dot column per outcome share; the recall's switches beside."""
    f = "fig09c_formation"
    stem = "47.6 (b) {arm}: lookup {outcome} share"
    models = models_with(f, [stem.format(arm="none", outcome="identity")])
    cols = outcome_columns(f, models, F09C_LANES, stem, LOOKUP_OUTCOMES, "lookup_answers", "formation", "f09c",
                           (-0.05, 1.05), (0, 0.5, 1), control_lane="control", control="a control block")  # fmt: skip
    rec, rec_ctrl = {}, {}
    for m in models:
        for lane, words, _label in F09C_LANES:
            c = cell(f, m, f"47.6 (b) {words}: recall switched")
            if c:
                e = est(c, f"formation.{ZK[m]}", key=f"f09c.recall.{lane}.{ZK[m]}")
                (rec_ctrl if lane == "control" else rec)[(m, lane)] = e
    cols.append(sp.DotColumn("recalls switched", "recalls", (-0.05, 1.05), (0, 0.5, 1),
                             series=[sp.Series("control", rec_ctrl, control="a control block"),
                                     sp.Series("recall", rec)]))  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k, label) for k, _w, label in F09C_LANES])
    return sp.Figure(f, vocab()).add(t)


# ---- fig10e: a second route to the recall (48.5) -----------------------------------------------------------------------
F10E_LANES = (("i", "(i) without the J++ part", "without the lens part"),
              ("ii", "(ii) (i) and the pointer write", "and the address swapped in"),
              ("iii", "(iii) the pointer write only", "the address swapped in only"),
              ("iv", "(iv) (i) and a random direction (same size)", "and a random vector"))  # fmt: skip
RECALL_OUTCOMES = (("written", "the written locker's item", "the target locker's item", "address"),
                   ("changed", "the changed item", "the changed item", "identity"),
                   ("original", "original answer", "the original answer", "neutral"),
                   ("other", "other", "other answers", "neutral"))  # fmt: skip


def fig10e_second_route() -> sp.Figure:
    """48.5, fixed in advance: what the recall names on the informative writes under the four arms (lanes; the arm
    with a random direction is the control, grey), one dot column per outcome share."""
    f = "fig10e"
    stem = "48.5, {arm}: recall names {outcome}"
    models = models_with(f, [stem.format(arm=F10E_LANES[0][1], outcome="the changed item")])
    cols = outcome_columns(f, models, F10E_LANES, stem, RECALL_OUTCOMES, "recall_answers", "route2", "f10e",
                           (-0.05, 1.05), (0, 0.5, 1), control_lane="iv", control="a random vector")  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k, label) for k, _w, label in F10E_LANES])
    return sp.Figure("fig10e_second_route", vocab()).add(t)


# ---- s05: every routes arm ---------------------------------------------------------------------------------------------
S05_ARMS = (("whole", "the whole change"), ("no_jpp", "without the lens part"),
            ("no_jpp_rand", "without a random part"), ("no_alf", "without the address"),
            ("no_alf_rand", "without a random part of the address's size"), ("keep_alf", "the address only"),
            ("keep_alf_rand", "a random part of the address's size only"), ("keep_jpp", "the lens part only"),
            ("keep_jpp_rand", "a random part only"))  # fmt: skip
RANDOM_ARMS = {"no_jpp_rand", "no_alf_rand", "keep_alf_rand", "keep_jpp_rand"}


def _s05(fid: str, arms) -> sp.Figure:
    """The routes test (another item moved): the lookup's answers by identity and by position, and the original
    answer, as dot columns; arms as lanes, the random-part arms grey."""
    f = "s05"
    stem = "another item moved, {arm}: {outcome} share"
    models = models_with(f, [stem.format(arm="whole", outcome="identity")])
    lanes = [(k, k, label) for k, label in arms]
    cols = []
    for out_key, outcome, header, role in LOOKUP_OUTCOMES[:3]:
        cells, ctrl = {}, {}
        for m in models:
            for k, _label in arms:
                c = cell(f, m, stem.format(arm=k, outcome=outcome))
                if c:
                    e = est(c, f"routes.{k}.{ZK[m]}", key=f"s05.{out_key}.{k}.{ZK[m]}")
                    (ctrl if k in RANDOM_ARMS else cells)[(m, k)] = e
        cols.append(sp.DotColumn(header, "lookup_answers", (-0.05, 1.05), (0, 0.5, 1),
                                 series=[sp.Series("control", ctrl, control="a random part"),
                                         sp.Series(role, cells, word=header if role == "neutral" else None)]))  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k, label) for k, _k, label in lanes])
    return sp.Figure(fid, vocab()).add(t)


def s05a_routes_taken_out() -> sp.Figure:
    """The routes test's arms that take a part out of the whole change (and their random parts of the same size)."""
    return _s05("s05a_routes_taken_out", S05_ARMS[:5])


def s05b_routes_kept() -> sp.Figure:
    """The routes test's arms that keep only one part of the change (and their random parts of the same size)."""
    return _s05("s05b_routes_kept", S05_ARMS[5:])


# ---- s03e: where the missing switches sit (47.4), a decomposition --------------------------------------------------------
S03E_TERMS = (("a", "the bridge word at L"), ("before_L", "the bridge word before L"),
              ("propagation", "every layer after L"), ("pick_other", "pick sentence's other tokens"),
              ("outside", "outside the pick sentence"))  # fmt: skip
S03E_SETS = (("main", "the main test"), ("clean", "the clean one-pick scenes"))


def s03e_cumulative() -> sp.Figure:
    """47.4, fixed in advance: the switches of the locker-first scenes, decomposed (terms may be negative): the bridge
    word's change at L, then the bridge word at the layers before L, every layer after L, the pick sentence's other
    tokens, and what lies outside the pick sentence; one dot column per term with both readers, the main test and the
    clean one-pick scenes as lanes."""
    f = "s03e_cumulative"
    stem = "47.4 {set}, locker-first, {reader}: {term}"
    models = models_with(f, [stem.format(set="main", reader="lookup", term="a")])
    cols = []
    for term, header in S03E_TERMS:
        series = []
        for reader in ("lookup", "recall"):
            cells = {}
            for m in models:
                for s, _label in S03E_SETS:
                    c = cell(f, m, stem.format(set=s, reader=reader, term=term))
                    if c:
                        cells[(m, s)] = est(c, f"cumulative.{s}.{ZK[m]}", key=f"s03e.{reader}.{term}.{s}.{ZK[m]}")
            series.append(sp.Series(reader, cells))
        # the pick sentence's header on two lines (SP613): weight 1.1-1.19 per styles-plot 0.2.1
        cols.append(sp.DotColumn(header, "switch_terms", (-0.2, 1.05), (0, 0.5, 1), series=series,
                                 weight=1.15 if term == "pick_other" else 1.0))  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k, label) for k, label in S03E_SETS])
    return sp.Figure(f, vocab()).add(t)


# ---- fig16: the dose (51.1), dots per dose -----------------------------------------------------------------------------
A_DOSES = ("0.5", "1", "1.5", "2", "3")
B_DOSES = ("0.25", "0.5", "0.75", "1", "1.5")
B_ARMS = (("rest", "the rest by itself", "the rest by itself", None),
          ("no_address", "the rest by itself without the address", "without the address", None),
          ("no_random", "the rest by itself without a random part of the address's share",
           "without a random part of the address's size", "control"))  # fmt: skip


def _fig16() -> tuple:
    """51.1, fixed in advance. Top (A): the recall's and the lookup's switches with the lens part by itself, beyond a
    random part of the same size, per dose (lanes). Bottom (B): the lookups switched with the rest of the change by
    itself, without the address, and without a random part of the address's size (grey), per dose."""
    f = "fig16_dose"
    a_stem = ("51.1 A: {reader} switches with the J++ part by itself at dose {d}, minus a random part (same size) at the "
              "same dose")  # fmt: skip
    models = models_with(f, [a_stem.format(reader="recall", d="1")])
    a_cols = []
    for d in A_DOSES:
        series = [sp.Series(reader, {m: est(c, f"dose.{ZK[m]}", key=f"f16.a.{reader}.{d}.{ZK[m]}")
                                     for m in models if (c := cell(f, m, a_stem.format(reader=reader, d=d)))})
                  for reader in ("lookup", "recall")]  # fmt: skip
        a_cols.append(sp.DotColumn(f"dose {d}", "switches_beyond", (-0.75, 0.6), (-0.5, 0, 0.5), series=series))
    top = sp.DotTable(models, a_cols, note="the lens part by itself")
    b_cols = []
    for d in B_DOSES:
        lk, ctrl = {}, {}
        for key, words, _label, role in B_ARMS:
            for m in models:
                c = cell(f, m, f"51.1 B: lookups switched, {words}, dose {d}")
                if c:
                    e = est(c, f"dose.{ZK[m]}", key=f"f16.b.{key}.{d}.{ZK[m]}")
                    (ctrl if role == "control" else lk)[(m, key)] = e
        b_cols.append(sp.DotColumn(f"dose {d}", "lookups_switched", (-0.05, 1.05), (0, 0.5, 1),
                                   series=[sp.Series("control", ctrl, control="a random part"),
                                           sp.Series("lookup", lk)]))  # fmt: skip
    bottom = sp.DotTable(models, b_cols, lanes=[sp.Lane(k, label) for k, _w, label, _r in B_ARMS],
                         note="the rest of the change by itself")  # fmt: skip
    return top, bottom


def fig16a_dose_lens() -> sp.Figure:
    """51.1 A, fixed in advance: the recall's and the lookup's switches with the lens part by itself, beyond a random
    part of the same size, one column per dose."""
    return sp.Figure("fig16a_dose_lens", vocab()).add(_fig16()[0])


def fig16b_dose_rest() -> sp.Figure:
    """51.1 B, fixed in advance: the lookups switched with the rest of the change by itself, without the address, and
    without a random part of the address's size (grey), one column per dose."""
    return sp.Figure("fig16b_dose_rest", vocab()).add(_fig16()[1])


# ---- s12: learned subspaces on Muse and the 27B (48.1), dots per k -------------------------------------------------------
S12_K = ("1", "4", "16", "64")


def s12_das_muse() -> sp.Figure:
    """48.1, fixed in advance: each reader's switches under its own learned subspace of k directions (lanes), against
    a shuffled and a random subspace of the same k (grey)."""
    f = "s12"
    models = models_with(f, ["48.1, lookup's switches under the lookup's subspace, k = 4"])
    cols = []
    for reader in ("lookup", "recall"):
        own: dict = {(m, k): est(c, f"learned.{ZK[m]}", key=f"s12.{reader}.own.{k}.{ZK[m]}")
               for m in models for k in S12_K
               if (c := cell(f, m, f"48.1, {reader}'s switches under the {reader}'s subspace, k = {k}"))}  # fmt: skip
        cols.append(sp.DotColumn(f"the {reader}'s subspace", "own_switches", (-0.05, 1.05), (0, 0.5, 1),
                                 series=[sp.Series(reader, own)]))  # fmt: skip
        for ctl, name in (("shuffled", "shuffled pairs"), ("random", "a random subspace")):
            cc: dict = {(m, k): est(c, f"learned.{ZK[m]}", key=f"s12.{reader}.{ctl}.{k}.{ZK[m]}")
                  for m in models for k in S12_K
                  if (c := cell(f, m, f"48.1, {reader}'s switches under a {ctl} subspace, k = {k}"))}  # fmt: skip
            cols.append(sp.DotColumn(f"a {ctl} subspace", "own_switches", (-0.05, 1.05), (0, 0.5, 1),
                                     series=[sp.Series("control", cc, control=name)]))  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k, f"k = {k}") for k in S12_K])
    return sp.Figure("s12_das_muse", vocab()).add(t)


# ---- fig10c: binding (48.3), the reference as a grey column ------------------------------------------------------------
# 48.3's and 48.4's bars, fixed in advance: 2 × a random direction's share, 2 × the lens part's (story_b48.py)
TWICE = 2


def _fig10c() -> tuple:
    """48.3, fixed in advance. Left: the probe for who picked the item, at the locker sentence's item and number, in
    locker-after and locker-first scenes (lanes). Middle: the lens part's share of the person direction written there,
    against 2 × a random direction's (grey). Right: the person direction written at strength 1 and 2 (lanes): lookups
    sent to the written item and recalls naming it, against a random direction of the same norm (grey)."""
    f = "fig10c"
    models = models_with(f, ["48.3, J++ part's share of the person direction at the item"])
    probe_lanes = (("after", "locker after the pick", "locker sentence after"),
                   ("before", "locker before the pick", "locker sentence first"))  # fmt: skip
    probe_cols = []
    for at in ("item", "number"):
        cells: dict = {(m, k): est(c, f"binding.{ZK[m]}", key=f"f10c.probe.{at}.{k}.{ZK[m]}")
                 for m in models for k, w, _l in probe_lanes
                 if (c := cell(f, m, f"48.3, probe at the {at}, {w} (accuracy)"))}  # fmt: skip
        header = f"probe at the {at}"  # a probe's accuracy has no role: the neutral colour, named by its header
        probe_cols.append(sp.DotColumn(header, "probe_accuracy", (0, 1.0), (0, 0.5, 1),
                                       series=[sp.Series("neutral", cells, word=header)]))  # fmt: skip
    probe = sp.DotTable(models, probe_cols, lanes=[sp.Lane(k, label) for k, _w, label in probe_lanes],
                        note="who picked the item, read by a probe")  # fmt: skip
    share_cols = []
    for at in ("item", "number"):
        lens, ref = {}, {}
        for m in models:
            a = cell(f, m, f"48.3, J++ part's share of the person direction at the {at}")
            r = cell(f, m, f"48.3, random direction's J++ part share at the {at}")
            if a:
                lens[m] = sp.Est(a[0], cell=f"binding.{ZK[m]}", key=f"f10c.share.{at}.{ZK[m]}", label=True)
            if r:
                ref[m] = sp.Est(TWICE * r[0], cell=f"binding.{ZK[m]}", key=f"f10c.twice_random.{at}.{ZK[m]}")
        share_cols += [sp.DotColumn(f"at the {at}", "lens_share", (0, 0.3), (0, 0.1, 0.2),
                                    series=[sp.Series("lens", lens)]),
                       sp.DotColumn("2 × random", "lens_share", (0, 0.3), (0, 0.1, 0.2),
                                    series=[sp.Series("control", ref, control="2 × a random direction")])]  # fmt: skip
    share = sp.DotTable(models, share_cols, note="the lens part's share of the person direction")
    write_lanes = (("1", "strength 1"), ("2", "strength 2"))
    write_cols = []
    for reader in ("lookup", "recall"):
        w, r = {}, {}
        for m in models:
            for s, _l in write_lanes:
                a = cell(f, m, f"48.3, {reader}: the write, strength {s}, sent to the written item")
                rq = f"48.3, {reader}: a random direction (same norm), strength {s}, sent to the written item"
                b = cell(f, m, rq)
                if a:
                    w[(m, s)] = est(a, f"binding.{ZK[m]}", key=f"f10c.write.{reader}.{s}.{ZK[m]}")
                if b:
                    r[(m, s)] = est(b, f"binding.{ZK[m]}", key=f"f10c.write_random.{reader}.{s}.{ZK[m]}")
        write_cols += [sp.DotColumn(f"{reader}s sent", "sent_written", (-0.02, 0.3), (0, 0.1, 0.2),
                                    series=[sp.Series(reader, w)]),
                       sp.DotColumn("a random vector", "sent_written", (-0.02, 0.3), (0, 0.1, 0.2),
                                    series=[sp.Series("control", r, control="a random vector")])]  # fmt: skip
    write = sp.DotTable(models, write_cols, lanes=[sp.Lane(k, label) for k, label in write_lanes],
                        note="the person direction added")  # fmt: skip
    return probe, share, write


def fig10c_binding() -> sp.Figure:
    """48.3, fixed in advance: who picked the item, read by a probe, and the lens part's share of the person direction
    against 2 × a random direction's (grey)."""
    probe, share, _write = _fig10c()
    return sp.Figure("fig10c_binding", vocab()).add(probe, share)


def fig10c2_binding_added() -> sp.Figure:
    """48.3, fixed in advance: the person direction added at strength 1 and 2 (lanes): lookups sent to the target item
    and recalls naming it, against a random direction of the same norm (grey)."""
    return sp.Figure("fig10c2_binding_added", vocab()).add(_fig10c()[2])


# ---- fig10d: heads (48.4), rows read from the run file ------------------------------------------------------------------
HEAD_PARTS = (("jpp", "J++ part", "the lens part", "lens"), ("rest", "the rest (the change minus its J++ part)",
              "the rest", "neutral"), ("pointer", "pointer", "the address", "address"))  # fmt: skip


def _heads(m: str) -> list[str]:
    """The heads 48.4 read for a model, in the run file's order (data.csv keeps it)."""
    out = []
    for (fig, mm, q), _v in D.story().items():
        h = re.match(r"48\.4, (layer \d+ head \d+): J\+\+ part passed$", q)
        if fig == "fig10d" and mm == m and h:
            out.append(h.group(1))
    return out


def fig10d_heads() -> sp.Figure:
    """48.4, fixed in advance: per model the five heads with the most attention from the last token to the bridge word
    (rows, read from the run): how much of each part of the change the head passes, against a random part of the same
    size (grey) and 2 × the lens part's (grey)."""
    f = "fig10d"
    v = vocab()
    tables = []
    for m in [m for m in DAN if _heads(m)]:
        heads = _heads(m)
        vh = v.with_entities("heads", [(h, h) for h in heads])
        cols = []
        lens = {}
        for key, words, header, role in HEAD_PARTS:
            cells = {h: est(c, f"heads.{ZK[m]}", key=f"f10d.{key}.{h}.{ZK[m]}")
                     for h in heads if (c := cell(f, m, f"48.4, {h}: {words} passed"))}  # fmt: skip
            if key == "jpp":
                lens = cells
            cols.append((header, [sp.Series(role, cells, word=header if role == "neutral" else None)]))
        rand = {h: est(c, f"heads.{ZK[m]}", key=f"f10d.random.{h}.{ZK[m]}")
                for h in heads if (c := cell(f, m, f"48.4, {h}: random part (same size) passed"))}  # fmt: skip
        twice = {h: sp.Est(TWICE * e.value, cell=f"heads.{ZK[m]}", key=f"f10d.twice_lens.{h}.{ZK[m]}")
                 for h, e in lens.items()}  # fmt: skip
        cols += [("a random part", [sp.Series("control", rand, control="a random part")]),
                 ("2 × the lens part", [sp.Series("control", twice, control="2 × the lens part")])]  # fmt: skip
        tables.append((vh, heads, cols, v.entity("models", m).name))
    return _head_figure(tables)


def _head_figure(tables) -> sp.Figure:
    """One table per model, each on its own axis (the heads pass different scales on different models)."""
    vh = tables[0][0]
    for v2, *_ in tables[1:]:
        vh = vh.with_entities("heads", [(e.key, e.name) for v_ in (vh, v2) for e in v_.entities("heads")])
    fig = sp.Figure("fig10d_heads", vh)
    for _v, heads, cols, name in tables:
        hi = max(e.hi if e.hi is not None else e.value for _h, ss in cols for s in ss for e in s.cells.values())
        lim, ticks = _lim(hi)
        fig.add(sp.DotTable(heads, [sp.DotColumn(h, "passed", lim, ticks, series=ss) for h, ss in cols],
                            kind="heads", note=name))  # fmt: skip
    return fig


def _lim(hi: float):
    """An axis from 0 to just above the largest value, ticks at round steps (the heads pass different scales)."""
    for top, ticks in ((0.1, (0, 0.05, 0.1)), (0.2, (0, 0.1, 0.2)), (0.6, (0, 0.25, 0.5)), (1.2, (0, 0.5, 1))):
        if hi <= top * 0.98:
            return (0, top * 1.05), ticks
    return (0, hi * 1.1), (0, round(hi / 2, 1), round(hi, 1))


# ---- s07: the recall follows the swap ----------------------------------------------------------------------------------
S07_OUT = (("written", "the written locker's item", "the target locker's item", "address"),
           ("third", "the third item", "the third item", "neutral"), ("other", "other", "other answers", "neutral"))  # fmt: skip


def s07_recall_follows_swap() -> sp.Figure:
    """The recall's answers that changed under the strongest write (s = 4): the written locker's item, the third item,
    other; one dot column each (no interval recorded)."""
    f = "s07"
    stem = "recall changed under the strongest write (s = 4): {}"
    models = models_with(f, [stem.format("the written locker's item")])
    cols = []
    for key, words, header, role in S07_OUT:
        cells = {m: sp.Est(c[0], cell=f"follows.{ZK[m]}", key=f"s07.{key}.{ZK[m]}", label=True)
                 for m in models if (c := cell(f, m, stem.format(words)))}  # fmt: skip
        cols.append(sp.DotColumn(header, "recall_answers", (0, 1.05), (0, 0.5, 1),
                                 series=[sp.Series(role, cells, word=header if role == "neutral" else None)]))  # fmt: skip
    return sp.Figure("s07_recall_follows_swap", vocab()).add(sp.DotTable(models, cols))


# ---- s07b: the lens readout of the swap (47.0), the null as grey columns -----------------------------------------------
S07B_LANES = (("write", "the address swapped in", "address"), ("identity", "the identity change", "identity"))


def s07b_lens_readout() -> sp.Figure:
    """47.0, fixed in advance. (a) The lens readout's rank of the best ordinal word under h + the pointer write, and of
    the new item's name under h + the identity change (median; lower is nearer the top), beside the null's cut and
    median (grey). (b) The share of each change rebuilt by 25 lens directions, beside random draws' 95th percentile
    (grey). (c) The readout's KL under each change, beside the null's median and cut (grey)."""
    f = "s07b_lens_readout"
    rank_q = {
        "write": "47.0 (a) best ordinal word's rank, h + pointer write (median; null cut, null median)",
        "identity": "47.0 (a) new item's name rank, h + identity change (median; null cut, null median)",
    }
    kl_q = {
        "write": "47.0 (c) KL of the readout, h + write (median; null median, null cut)",
        "identity": "47.0 (c) KL of the readout, h + identity (median; null median, null cut)",
    }
    models = models_with(f, list(rank_q.values()))

    def group(qs, unit, lim, ticks, refs, header, label):
        est_cells = {lane: {} for lane, *_ in S07B_LANES}
        ref_cells = [{} for _ in refs]
        for m in models:
            for lane, _l, _r in S07B_LANES:
                c = cell(f, m, qs[lane])
                if not c:
                    continue
                cid = f"readout.{ZK[m]}"
                est_cells[lane][(m, lane)] = sp.Est(c[0], cell=cid, key=f"s07b.{unit}.{lane}.{ZK[m]}", label=label)
                for i, (pos, _h, _c) in enumerate(refs):
                    ref_cells[i][(m, lane)] = sp.Est(c[pos], cell=cid, key=f"s07b.{unit}.{lane}.ref{i}.{ZK[m]}")
        cols = [
            sp.DotColumn(
                "the change",
                unit,
                lim,
                ticks,
                width=1.8,
                series=[sp.Series(role, est_cells[lane]) for lane, _l, role in S07B_LANES],
            )
        ]
        cols += [sp.DotColumn(h, unit, lim, ticks, series=[sp.Series("control", ref_cells[i], control=ctl)])
                 for i, (_pos, h, ctl) in enumerate(refs)]  # fmt: skip
        return sp.ColumnGroup(header, cols)

    top = _top(f, models, rank_q)
    rank = group(rank_q, "readout_rank", (0, top), (0, float(f"{0.8 * top:.0g}")), ((1, "the null's cut", "the null's cut"),
                 (2, "the null's median", "the null's median")), "rank in the lens readout", False)  # fmt: skip
    kl = group(kl_q, "readout_kl", (0, 4.2), (0, 2, 4), ((1, "the null's median", "the null's median"),
               (2, "the null's cut", "the null's cut")), "KL of the readout", False)  # fmt: skip
    rebuilt, rnd = {}, {}
    for m in models:
        cid = f"readout.{ZK[m]}"
        p = cell(f, m, "47.0 (b) share rebuilt by 25 lens directions: pointer")
        i = cell(f, m, "47.0 (b) share rebuilt by 25 lens directions: identity_mean")
        r = cell(f, m, "47.0 (b) share rebuilt by 25 lens directions: random draws (mean; mean, 95th pct)")
        if p:
            rebuilt[(m, "write")] = sp.Est(p[0], cell=cid, key=f"s07b.rebuilt.write.{ZK[m]}")
        if i:
            rebuilt[(m, "identity")] = sp.Est(i[0], cell=cid, key=f"s07b.rebuilt.identity.{ZK[m]}")
        if r:
            rnd[(m, "write")] = sp.Est(r[2], cell=cid, key=f"s07b.rebuilt.random95.{ZK[m]}")
    rb = sp.ColumnGroup("rebuilt by 25 lens directions", [
        sp.DotColumn("the change", "rebuilt", (0, 0.3), (0, 0.1, 0.2), width=1.8,
                     series=[sp.Series("address", {k: e for k, e in rebuilt.items() if k[1] == "write"}),
                             sp.Series("identity", {k: e for k, e in rebuilt.items() if k[1] == "identity"})]),
        sp.DotColumn("random draws' 95th percentile", "rebuilt", (0, 0.3), (0, 0.1, 0.2),
                     series=[sp.Series("control", rnd, control="random lens directions")]),
    ])  # fmt: skip
    lanes = [sp.Lane(k) for k, _label, _r in S07B_LANES]  # named by the colour words: address (the pointer), identity
    return sp.Figure(f, vocab()).add(
        sp.DotTable(models, [rank, sp.Gutter(), rb], lanes=lanes), sp.DotTable(models, [kl], lanes=lanes)
    )


def _top(f, models, qs) -> float:
    """Just above the largest value or reference a rank panel draws."""
    return 1.08 * max(
        max(v for v in c[:3] if v is not None) for m in models for q in qs.values() if (c := cell(f, m, q))
    )


# ---- fig02b: the 27B with more directions -----------------------------------------------------------------------------
F02B_K = (("25", "25 directions"), ("50", "50 directions"), ("100", "100 directions"))
F02B_B = (("no_jpp", "25 directions"), ("no_jpp50", "50 directions"), ("no_jpp100", "100 directions"))


def _fig02b() -> tuple:
    """(a) The main test with 25, 50 and 100 lens directions taken out (lanes): each reader's extra loss. (b) Another
    item moved without the lens part's 25, 50 and 100 directions (lanes): the lookup's answers by identity and by
    position, against a random part of the same size (grey, identity)."""
    f = "fig02b"
    models = models_with(f, ["(a) main test, 25 directions: recall extra loss"])
    a_cols = []
    for k, label in F02B_K:
        series = [sp.Series(reader, {m: est(c, f"kcurve.{ZK[m]}", key=f"f02b.a.{reader}.{k}.{ZK[m]}")
                                     for m in models
                                     if (c := cell(f, m, f"(a) main test, {k} directions: {reader} extra loss"))})
                  for reader in ("lookup", "recall")]  # fmt: skip
        a_cols.append(sp.DotColumn(label, "extra_loss_share", (-0.2, 1.0), (0, 0.5, 1), series=series,
                                   connect=("lookup", "recall")))  # fmt: skip
    top = sp.DotTable(models, a_cols, note="the main test, extra drop without the lens part")
    models_b = models_with(f, ["(b) another item moved, no_jpp: identity share"])
    ident, pos, rnd = {}, {}, {}
    for m in models_b:
        for arm, label in F02B_B:
            k = label.split()[0]
            i = cell(f, m, f"(b) another item moved, {arm}: identity share")
            p = cell(f, m, f"(b) another item moved, {arm}: position share")
            r = cell(f, m, f"(b) another item moved, {arm}_rand: identity share")
            if i:
                ident[(m, k)] = est(i, f"kcurve.{ZK[m]}", key=f"f02b.b.identity.{k}.{ZK[m]}")
            if p:
                pos[(m, k)] = est(p, f"kcurve.{ZK[m]}", key=f"f02b.b.position.{k}.{ZK[m]}")
            if r:
                rnd[(m, k)] = est(r, f"kcurve.{ZK[m]}", key=f"f02b.b.random.{k}.{ZK[m]}")
    bottom = sp.DotTable(models_b, [
        sp.DotColumn("by identity", "lookup_answers", (-0.05, 1.05), (0, 0.5, 1), series=[sp.Series("identity", ident)]),
        sp.DotColumn("a random part", "lookup_answers", (-0.05, 1.05), (0, 0.5, 1),
                     series=[sp.Series("control", rnd, control="a random part")]),
        sp.DotColumn("by position", "lookup_answers", (-0.05, 1.05), (0, 0.5, 1), series=[sp.Series("address", pos)]),
    ], lanes=[sp.Lane(k, label) for k, label in F02B_K], note="another item moved, without the lens part")  # fmt: skip
    return top, bottom


def fig02b_k_curve() -> sp.Figure:
    """The main test with 25, 50 and 100 lens directions taken out (columns): each reader's extra drop."""
    return sp.Figure("fig02b_k_curve", vocab()).add(_fig02b()[0])


def fig02c_k_routes() -> sp.Figure:
    """Another item moved without the lens part's 25, 50 and 100 directions (lanes): the lookup's answers by identity
    and by position, against a random part of the same size (grey). Apart from fig02b: blue and violet may not share a
    figure."""
    return sp.Figure("fig02c_k_routes", vocab()).add(_fig02b()[1])


FIGS = {"fig09c_formation": fig09c_formation, "fig10e_second_route": fig10e_second_route,
        "s05a_routes_taken_out": s05a_routes_taken_out, "s05b_routes_kept": s05b_routes_kept, "s03e_cumulative": s03e_cumulative, "fig16a_dose_lens": fig16a_dose_lens, "fig16b_dose_rest": fig16b_dose_rest,
        "s12_das_muse": s12_das_muse, "fig10c_binding": fig10c_binding, "fig10c2_binding_added": fig10c2_binding_added, "fig10d_heads": fig10d_heads,
        "s07_recall_follows_swap": s07_recall_follows_swap, "s07b_lens_readout": s07b_lens_readout,
        "fig02b_k_curve": fig02b_k_curve, "fig02c_k_routes": fig02c_k_routes}  # fmt: skip
SUPP = {
    "s05a_routes_taken_out",
    "s05b_routes_kept",
    "s03e_cumulative",
    "s12_das_muse",
    "s07_recall_follows_swap",
    "s07b_lens_readout",
}
