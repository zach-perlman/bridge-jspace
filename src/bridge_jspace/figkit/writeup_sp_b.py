"""The write-up's figures after the pilot, on styles-plot: the dot tables of figkit/writeup_figs.py, writeup_intro.py,
writeup_address.py, writeup_claims.py and writeup_appendix.py declared for the library (same data accessors, same file
names). writeup_sp.FIGS takes them in; the figures the library cannot draw yet stay on figkit (see FIGS' comment)."""

from __future__ import annotations

import re

import styles_plot as sp

from bridge_jspace import figdata as CF
from bridge_jspace import figdata as D
from bridge_jspace import figdata as F
from bridge_jspace import figdata as W
from bridge_jspace.figkit.writeup_sp_base import MODEL, ZK, est, need, vocab

DAN = [m for m, _ in D.DAN]
TWIN = [MODEL[k] for k, _ in W.TWIN_MODELS]


def _missing(c, why="no run"):
    return sp.Missing(why) if c is None else c


# ---- Fig. 5: same-size controls ----------------------------------------------------------------------------------------
def _band_cell(m, key):
    k = ZK[m]
    c = D.b(f"ko.{k}.{key}")
    if key == "pc" and not c:  # the size-matched ratio times the lens part's gap (specs.largest)
        pcr, mk = D.b(f"ko.{k}.pcr"), D.b(f"ko.{k}.mk")
        c = (pcr[0] * mk[0], None, None) if pcr and mk else None
    return c


def fig05_controls() -> sp.Figure:
    """Top, band of layers: the recall − lookup gap under each removal, the lens part (teal) against rotated, logit-lens
    and PCA parts of the same size (grey), and the difference lens part − largest control. Bottom, one layer: the
    recall's switches blocked beyond a random part, the same way, from the earlier runs with a same-size control."""
    v = vocab()

    def col(header, role, data, unit, lim, ticks, cell_id, key, control=None):
        """data: {model: (value, lo, hi) or None}; key(m): the data key printed."""
        cells = {m: sp.Missing("no run") if not data[m] else
                 est(data[m], cell_id(m), key=key(m), label=role != "control", interval=role != "control")
                 for m in DAN}  # fmt: skip
        return sp.DotColumn(header, unit, lim, ticks, series=[sp.Series(role, cells, control=control)])

    def band(m):
        return f"band.{ZK[m]}"

    def layer(m):
        return f"layer.{ZK[m]}"

    pts = ("points", (-4, 70), (0, 30, 60))
    shares = ("share", (-0.08, 1.0), (0, 0.5, 1))

    def band_diff(m):
        k = ZK[m]
        c = W.w(f"fig05.band_diff.{k}")
        return sp.Missing("source missing") if c is None else sp.Est(c[0], c[1], c[2], cell=band(m),
                                                                      key=f"fig05.band_diff.{k}")  # fmt: skip

    def layer_diff(m):
        top_ = F.layer_largest(m)
        if not top_:
            return sp.Missing("no run")
        lens, key, _name, cell = top_
        pair = D.b(f"f2.layer.{ZK[m]}.pca") if key == "pca" else None
        if pair and pair[1] is not None:
            return sp.Est(pair[0], pair[1], pair[2], cell=layer(m), key=f"f2.layer.{ZK[m]}.pca")
        return sp.Est(need(lens, m)[0] - need(cell, m)[0], cell=layer(m), key=f"fig05.layer_diff.{ZK[m]}",
                      note="no interval")  # fmt: skip

    band_cols = [col("lens part", "lens", {m: _band_cell(m, "mk") for m in DAN}, *pts, band,
                     lambda m: f"ko.{ZK[m]}.mk")]  # fmt: skip
    for q, name in (("rot", "rotated"), ("u", "logit lens"), ("pc", "PCA")):
        keys = {m: f"ko.{ZK[m]}.{q}" for m in DAN}
        band_cols.append(col(name, "control", {m: _band_cell(m, q) for m in DAN}, *pts, band, keys.get, control=name))
    top = sp.DotTable(DAN, [sp.ColumnGroup("Band of layers · fact passages", [
        *band_cols, sp.TextColumn("lens part − largest control", "gap_difference", {m: band_diff(m) for m in DAN}),
    ])], note="the recall − lookup gap under each removal")  # fmt: skip

    names = {"rand": "random lens directions"}
    layer_cols = [col("lens part", "lens", {m: D.s(m, "J++ part: recall extra loss", "fig02") for m in DAN}, *shares,
                      layer, lambda m: f"fig05.layer.lens.{ZK[m]}")]  # fmt: skip
    for k, name, q in F.LAYER_CTRL:
        keys = {m: f"fig05.layer.{k}.{ZK[m]}" for m in DAN}
        layer_cols.append(col(names.get(k, name), "control", {m: D.s(m, q, "fig02") for m in DAN}, *shares, layer,
                              keys.get, control=names.get(k, name)))  # fmt: skip
    bottom = sp.DotTable(DAN, [sp.ColumnGroup("One layer · locker scenes", [
        *layer_cols,
        sp.TextColumn("lens part − largest control", "share_difference", {m: layer_diff(m) for m in DAN}),
    ])], note="the recall's switches blocked beyond random · earlier runs with a same-size control")  # fmt: skip
    return sp.Figure("fig05_controls", v).add(top, bottom)


# ---- Fig. 8a: the address, read and removed ------------------------------------------------------------------------------
SHORT = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "qwen3.5-122b-a10b": "122b"}


def _removal_cells(m):
    """Position answers with the address taken out, and with a random part of the same size (deck_figs.f_address)."""
    if m == "nemotron-3.5-lightning":
        return (D.s(m, "another item moved, no_alf: position share"),
                D.s(m, "another item moved, no_alf_rand: position share"))  # fmt: skip
    pre = "rtg_C2" if m == "qwen3.5-122b-a10b" else "rt_C2"
    return D.x(f"{pre}_no_alf_position_{SHORT[m]}"), D.x(f"{pre}_no_alf_rand_position_{SHORT[m]}")


def fig08a_address_read_remove() -> sp.Figure:
    """Left: the locker probe's accuracy at the bridge word (address) against the layout alone (grey). Right: the lookups
    that follow the position with the address taken out against a random part of the same size taken out (grey)."""
    probe, base, addr, rand = {}, {}, {}, {}
    for m in DAN:
        k = ZK[m]
        probe[m] = est(need(D.s(m, "the locker probe at the bridge word, locker-first scenes"), m), f"probe.{k}",
                       key=f"fig08a.probe.{k}", label=True)  # fmt: skip
        b = need(D.s(m, "the locker probe's layout baseline, locker-first scenes"), m)
        base[m] = est(b, f"probe.{k}", key=f"fig08a.layout.{k}", interval=False)
        a, r = (need(c, m) for c in _removal_cells(m))
        addr[m] = est(a, f"remove.{k}", key=f"fig08a.remove.{k}", label=True)
        rand[m] = est(r, f"remove.{k}", key=f"fig08a.random.{k}", label=True, interval=False)
    read = sp.DotColumn("probe accuracy at the bridge word", "probe_accuracy", (0.4, 1.03), (0.5, 0.75, 1),
                        series=[sp.Series("control", base, control="layout-only probe"),
                                sp.Series("address", probe)])  # fmt: skip
    remove = sp.DotColumn("position answers without the address", "lookups", (-0.12, 0.74), (0, 0.25, 0.5),
                          series=[sp.Series("control", rand, control="a random part"), sp.Series("address", addr)],
                          connect=("control", "address"))  # fmt: skip
    return sp.Figure("fig08a_address_read_remove", vocab()).add(sp.DotTable(DAN, [read, remove]))


def fig08b_address_swap_lens() -> sp.Figure:
    """Left: the lookups sent to the new locker by the address swap at 2x against a random direction at 4x (grey).
    Right: how much of an address swap and of an item change 25 lens directions rebuild, as a z against 200 random
    vectors (the grey band: theirs)."""
    zq = "47.0 (b) share rebuilt by 25 lens directions: "
    two, rnd, ptr, item = {}, {}, {}, {}
    for m in DAN:
        k = ZK[m]
        two[m] = est(need(D.s(m, "lookup target share, mean over locker pairs, s = 2", "fig07"), m), f"swap.{k}",
                     key=f"fig08b.swap.{k}", label=True)  # fmt: skip
        rnd[m] = est(need(D.s(m, "lookup target share, random direction, s = 4", "fig07"), m), f"swap.{k}",
                     key=f"fig08b.random.{k}", interval=False)  # fmt: skip
        p, it = D.s(m, zq + "pointer: z", prefix=True), D.s(m, zq + "identity_mean: z", prefix=True)
        if not p or not it:
            ptr[m] = sp.Missing("no run")
            continue
        ptr[m] = est(p, f"lens.{k}", key=f"fig08b.address_z.{k}", interval=False)
        item[m] = est(it, f"lens.{k}", key=f"fig08b.item_z.{k}", label=True, interval=False)
    swap = sp.DotColumn("lookups sent to the new locker", "lookups", (-0.04, 0.68), (0, 0.25, 0.5),
                        series=[sp.Series("control", rnd, control="a random vector"),
                                sp.Series("address", two, word="address swap")],
                        connect=("control", "address"))  # fmt: skip
    lens = sp.DotColumn("lens rebuild", "z", (-2.5, 31), (0, 10, 20, 30),
                        series=[sp.Series("address", ptr, word="address swap"),
                                sp.Series("identity", item, word="a change of item")],
                        connect=("address", "identity"), band=(-1, 1), band_name="random_vectors")  # fmt: skip
    return sp.Figure("fig08b_address_swap_lens", vocab()).add(sp.DotTable(DAN, [swap, lens]))


# ---- Fig. 10: the answer span --------------------------------------------------------------------------------------------
ALL_OF_IT = 1.0  # "all of it": the full damage (× the full damage = 1), the axis' own reference


def fig10_answer_span() -> sp.Figure:
    """Keep answer span: the share of the recall's damage undone by keeping only the answer span (brick) against a random
    keep orthogonal to the answers with at least as much energy (grey). Remove answer span, beyond energy-matched random,
    as a multiple of the full damage, on the main set and on the codename set."""
    v = vocab()
    keep_span, keep_ctrl = {}, {}
    for m in TWIN:
        k = ZK[m]
        span, ctl = W.w(f"fig10.keep_span.{k}"), W.w(f"fig10.keep_ctrl.{k}")
        keep_span[m] = (sp.Missing("source missing") if span is None else
                        est(span, f"keep.{k}", key=f"fig10.keep_span.{k}", label=True))  # fmt: skip
        if ctl is None:
            keep_ctrl[m] = sp.Missing("source missing")
        elif ctl[0] is not None:
            keep_ctrl[m] = est(ctl, f"keep_ctrl.{k}", key=f"fig10.keep_ctrl.{k}", label=True)
        else:  # the reading's label: neither random keep holds the kept span's energy
            keep_span[m] = sp.Est(span[0], span[1], span[2], cell=f"keep.{k}", key=f"fig10.keep_span.{k}", label=True,
                                  note="no energy-matched control") if span else keep_span[m]  # fmt: skip
    keep = sp.DotColumn("keep the answer span", "undone", (-0.4, 1.12), (0, 0.5, 1),
                        series=[sp.Series("control", keep_ctrl, control="energy-matched random"),
                                sp.Series("answer", keep_span)])  # fmt: skip

    def removal(panel, header):
        cells = {}
        for m in TWIN:
            k = ZK[m]
            c = W.w(f"fig10.span_only.{panel}.{k}")
            if c is None:
                cells[m] = sp.Missing("source missing")
                continue
            s = W.w(f"fig10.span_only_matched.{panel}.{k}")
            note = (f"matched on {v.format(100 * s[0], 'accuracy')}%" if s and s[0] is not None and s[0] < 1
                    else None)  # fmt: skip
            cells[m] = est(c, f"remove.{panel}.{k}", key=f"fig10.span_only.{panel}.{k}", label=True, note=note)
        return sp.DotColumn(header, "damage", (0.6, 1.8), (0.8, 1.2, 1.6), series=[sp.Series("answer", cells)],
                            rules=[sp.Rule(ALL_OF_IT, "all of it")])  # fmt: skip

    t = sp.DotTable(TWIN, [keep, removal("v4", "remove the answer span"),
                           removal("codename", "remove it, codename set")])  # fmt: skip
    return sp.Figure("fig10_answer_span", v).add(t)


# ---- Fig. 11: removals orthogonal to the answers -------------------------------------------------------------------------
BAR11 = 15  # the bar fixed in advance for the cleaned city subspace (writeup_figs.fig11_orthogonal's rule)


def fig11_orthogonal() -> sp.Figure:
    """One-hop question: the city's J++ directions (lens part), the same made orthogonal to the answers (neutral, post
    hoc), the answers' own J++ directions (answer). Right: the cleaned, data-built city subspace beyond energy-matched
    random, with the bar fixed in advance."""
    v = vocab()
    series = []
    for key, role in (("city", "lens"), ("city_perp", "neutral"), ("answers", "answer")):
        cells = {}
        for m in TWIN:
            k = ZK[m]
            c = W.w(f"fig11.onehop.{key}.{k}")
            cells[m] = (sp.Missing("source missing") if c is None else
                        est(c, f"onehop.{key}.{k}", key=f"fig11.onehop.{key}.{k}", label=True))  # fmt: skip
        series.append(sp.Series(role, cells))
    one = sp.DotColumn("one-hop question", "drop", (-4, 96), (0, 40, 80), series=series)
    sub = {}
    for m in TWIN:
        k = ZK[m]
        c = W.w(f"fig11.clean_subspace.{k}")
        sub[m] = (sp.Missing("source missing") if c is None else
                  est(c, f"subspace.{k}", key=f"fig11.clean_subspace.{k}", label=True))  # fmt: skip
    subspace = sp.DotColumn("data-built city subspace", "drop_beyond", (-10, 30), (0, 10, 20), width=2.3,
                            series=[sp.Series("neutral", sub, word="data-built city subspace")],
                            rules=[sp.Rule(BAR11, "bar fixed in advance: {}", unit="drop_beyond", key="fig11.bar")])  # fmt: skip
    t = sp.DotTable(TWIN, [subspace, one], note="one-hop question: “{city} is in the country of”")
    return sp.Figure("fig11_orthogonal", v).add(t)


# ---- Fig. 13: the last token ---------------------------------------------------------------------------------------------
def fig13_last_token() -> sp.Figure:
    """At the recall's last token a probe reads the entity from the lens part (left), yet the lens part swapped in
    switches almost no recalls, against the whole state swapped in (grey, right)."""
    v = vocab()
    rx_r = r"51\.10: recall, last token, read peak layer (\d+): the probe's accuracy"
    models, sub, read, lens, whole, chance = [], {}, {}, {}, {}, []
    for m in DAN:
        r = D.s_match(m, rx_r, "fig17_jspace_last_token")
        if not r:
            continue
        k = ZK[m]
        sw = need(D.s_match(m, r"51\.10: recall, last token, read peak layer \d+: the lens swap's switches over",
                            "fig17_jspace_last_token"), m)  # fmt: skip
        mm = need(re.search(r"\(([\d.]+) / ([\d.]+)\)", sw[0]), f"{m}: the swap's switches")
        models.append(m)
        sub[m] = f"layer {need(re.search(r'layer (\d+)', r[0]), m).group(1)}"
        read[m] = est(r[1], f"last.{k}", key=f"fig13.read.{k}", label=True)
        lens[m] = sp.Est(float(mm.group(1)), cell=f"last.{k}", key=f"fig13.lens.{k}")
        whole[m] = sp.Est(float(mm.group(2)), cell=f"last.{k}", key=f"fig13.whole.{k}")
        chance.append(need(D.s(m, "51.10: the read probe's chance (locker-first rows)"), m)[0])
    probe = sp.DotColumn("probe accuracy on the lens part", "probe_accuracy", (0, 1.02), (0, 0.5, 1),
                         series=[sp.Series("recall", read)], rules=[sp.Rule(max(chance), "chance")])  # fmt: skip
    used = sp.DotColumn("recalls switched", "recalls", (-0.05, 1.05), (0, 0.5, 1),
                        series=[sp.Series("control", whole, control="the whole state swapped in"),
                                sp.Series("lens", lens, word="lens part swapped in")],
                        connect=("lens", "control"))  # fmt: skip
    # the lens part's values in their own column, as the figkit figure printed them apart from the dots
    values = sp.TextColumn("lens part swapped in", "recalls", lens, role="lens", unit_title=False)
    return sp.Figure("fig13_last_token", v).add(sp.DotTable(models, [probe, used, values], row_sub=sub))


# ---- Fig. A1: inside agent transcripts -----------------------------------------------------------------------------------
AGENT = (("copy", "copy a given answer", "beyond_rotated"), ("pick", "pick the true of two", "beyond_rotated"),
         ("verify", "verify a Yes/No claim", "beyond_harshest"), ("produce", "produce the answer alone", "beyond_rotated"),
         ("derive", "derive from a premise", "beyond_rotated"))  # fmt: skip


def figA1_agents() -> sp.Figure:
    """Per task inside the agent transcripts, the knock-out's accuracy drop minus a control's (points, bridge-clustered
    95%); a task is drawn only when every model has its run. Descriptive cells say so (registry)."""
    cols = []
    for col, header, unit in AGENT:
        if not all(W.w(f"figA1.{col}.{ZK[m]}") for m in TWIN):
            continue
        cells = {m: est(W.w(f"figA1.{col}.{ZK[m]}"), f"{col}.{ZK[m]}", key=f"figA1.{col}.{ZK[m]}", label=True)
                 for m in TWIN}  # fmt: skip
        cols.append(sp.DotColumn(header, unit, (-25, 80), (0, 30, 60), series=[sp.Series("recall", cells)]))
    return sp.Figure("figA1_agents", vocab()).add(sp.DotTable(TWIN, cols))


# ---- appendix B f9: where in the prompt and in depth ---------------------------------------------------------------------
WHERE = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
WHERE_KEYS = {"mid": ("pos.{}.all.all", "pos.{}.all.bridge", "pos.{}.all.question"),
              "late": ("late.{}.all", "late.{}.bridge", "late.{}.question")}  # fmt: skip


def _where_keys(band_, j, k):
    if k == "mu":  # Muse's deeper band is its knock-out run; its middle band has no position-limited run
        key = {"late": ("ko.mu.mk", "pos.mu.bridge", "pos.mu.question")}.get(band_, ("", "", ""))[j]
        rot = "ko.mu.rot" if j == 0 else (f"{key}.rot" if key else "")
        return key, rot
    key = WHERE_KEYS[band_][j].format(k)
    return key, key + ".rot"


def appB_f9_where() -> sp.Figure:
    """The accuracy drop when the lens part is removed at all tokens, at the bridge's mention, or at the question, in
    the middle layers (the knock-out band) and in deeper layers, against a rotated control of the same size."""
    tables = []
    for band_, group in (("mid", "Middle layers · the knock-out band"), ("late", "Deeper layers")):
        cols = []
        for j, header in enumerate(("all tokens", "the bridge's mention", "the question")):
            drop, rot = {}, {}
            for m in WHERE:
                k = ZK[m]
                key, rk = _where_keys(band_, j, k)
                c = D.b(key) if key else None
                if not c:
                    drop[m] = sp.Missing("no run")
                    continue
                r = D.b(rk) if rk else None
                cell = f"{band_}.{j}.{k}"
                drop[m] = est(c, cell, key=key, label=True, note=None if r else "no control run")
                if r:
                    rot[m] = est(r, cell, key=rk, interval=False)
            cols.append(sp.DotColumn(header, "drop", (-3, 92), (0, 30, 60),
                                     series=[sp.Series("control", rot, control="rotated"),
                                             sp.Series("recall", drop)]))  # fmt: skip
        tables.append(sp.DotTable(list(WHERE), [sp.ColumnGroup(group, cols)]))
    return sp.Figure("appB_f9_where", vocab()).add(*tables)


# ---- appendix B f8: true and made-up facts; more lens directions ---------------------------------------------------------
def appB_f8_facts() -> sp.Figure:
    """The lookup's switches blocked without the lens part on fact passages, with true facts and with made-up ones."""
    q = "Zach's named passages, {} facts, lookup: switches lost beyond random"  # the data's quantity name, not drawn
    cells = {}
    for m in DAN:
        k = ZK[m]
        tr, mu = D.s(m, q.format("true"), "ledger_zach_named"), D.s(m, q.format("made-up"), "ledger_zach_named")
        if not tr or m == "muse-glimmer-30b":  # Muse: 25 lookup switches under the whole change, too few to read
            # (results/x50_zach/z1-20261028T161649Z/z1.json, layer_results.26.lookup.switched_whole)
            cells[(m, "true")] = sp.Missing("too few switches" if tr else "no run")
            continue
        cells[(m, "true")] = est(tr, f"facts.{k}", key=f"f8.true.{k}", label=True)
        if mu:
            cells[(m, "made_up")] = est(mu, f"facts.{k}", key=f"f8.made_up.{k}", label=True, interval=False)
    col = sp.DotColumn("fact passages", "switches", (-0.3, 0.9), (0, 0.25, 0.5, 0.75),
                       series=[sp.Series("lookup", cells)], band=(-0.1, 0.1))  # fmt: skip
    t = sp.DotTable(DAN, [col], lanes=[sp.Lane("true", "true facts"), sp.Lane("made_up", "made-up facts")])
    return sp.Figure("appB_f8_facts", vocab()).add(t)


def appB_f8_directions() -> sp.Figure:
    """The lookup's switches blocked when 25, 50 or 100 lens directions are removed (the conflict test's curve)."""
    cols = []
    for n in (25, 50, 100):
        cells = {}
        for m in DAN:
            c = D.s(m, f"(a) main test, {n} directions: lookup extra loss", "fig02b")
            cells[m] = (sp.Missing("below gate") if not c else
                        est(c, f"dirs.{ZK[m]}", key=f"f8.dirs.{n}.{ZK[m]}", label=True))  # fmt: skip
        cols.append(sp.DotColumn(f"{n} lens directions", "switches", (-0.62, 0.95), (0, 0.5),
                                 series=[sp.Series("lookup", cells)], band=(-0.1, 0.1)))  # fmt: skip
    t = sp.DotTable(DAN, cols, note="the lookup's switches blocked when more lens directions are removed")
    return sp.Figure("appB_f8_directions", vocab()).add(t)


# ---- appendix B f12: question before or after the scene ------------------------------------------------------------------
def appB_f12_order() -> sp.Figure:
    """The lookup and the recall without the lens part, beyond a random part, with the question after the scene (the
    main test) and before it; the lookup's paired difference before − after. Question before ran on the 27B and the
    122B only; the others say their recall gate."""
    v = vocab()
    stem = "question {} the scene: {}, switches lost beyond a random part"
    gate = "question before the scene: the recall's gate (read right on the original prompts)"
    series = {"lookup": {}, "recall": {}}
    diff = {}
    for m in DAN:
        k = ZK[m]
        for reader in ("lookup", "recall"):
            for when in ("after", "before"):
                c = D.s(m, stem.format(when, reader))
                if c:
                    series[reader][(m, when)] = est(c, f"{when}.{k}", key=f"f12.{reader}.{when}.{k}", label=True)
        if (m, "before") not in series["lookup"] and (g := D.s(m, gate)):
            series["lookup"][(m, "before")] = sp.Missing(f"below gate ({v.format(g[0], 'switches')})")
        d = D.s(m, "the lookup, question before minus after (paired)")
        diff[(m, "before")] = (est(d, f"before.{k}", key=f"f12.diff.{k}") if d
                               else sp.Missing("can't tell"))  # fmt: skip
    col = sp.DotColumn("without the lens part", "switches", (-0.3, 1.4), (0, 0.5, 1),
                       series=[sp.Series("lookup", series["lookup"]), sp.Series("recall", series["recall"])],
                       band=(-0.1, 0.1))  # fmt: skip
    before_after = sp.TextColumn("lookup: before − after", "share_difference", diff, unit_title=False)
    t = sp.DotTable(DAN, [col, before_after], lanes=[sp.Lane("after", "question after the scene"),
                                                     sp.Lane("before", "question before the scene")])  # fmt: skip
    return sp.Figure("appB_f12_order", v).add(t)


# ---- appendix B f14: the two removals ------------------------------------------------------------------------------------
def appB_f14_two_codes() -> sp.Figure:
    """The same scenes followed one by one (another item moved, lookup; every cell post hoc). Top: of the scenes on the
    position route, the share that leave it without the address against without a same-size random part; bottom: of
    the scenes on the identity route, the share that go to position without the lens part against its random part;
    beside each, the paired difference with its 95% interval."""
    qa = "post hoc, another item moved, lookup: Position scenes that leave position, "
    qb = "post hoc, another item moved, lookup: Identity scenes that go to position, "
    models = [m for m in DAN if D.s(m, qa + "without the address", "fig24")]

    def half(q, arm, role, note, header):
        a, r, d = {}, {}, {}
        for m in models:
            k = ZK[m]
            a[m] = est(need(D.s(m, q + arm, "fig24"), m), f"{role}.{k}", key=f"f14.{role}.{k}", label=True)
            r[m] = est(need(D.s(m, q + "without a same-size random part", "fig24"), m), f"{role}.{k}",
                       key=f"f14.{role}.random.{k}")  # fmt: skip
            d[m] = est(need(D.s(m, q + "paired difference", "fig24"), m), f"{role}.{k}", key=f"f14.{role}.diff.{k}",
                       label=True)  # fmt: skip
        share = sp.DotColumn(header, "scenes", (-0.3, 1.1), (0, 0.5, 1),
                             series=[sp.Series("control", r, control="a random part"), sp.Series(role, a)],
                             connect=("control", role))  # fmt: skip
        diff = sp.DotColumn("difference", "scenes_difference", (-0.1, 1.25), (0, 0.5, 1), series=[sp.Series(role, d)])
        return sp.DotTable(models, [share, diff], note=note)

    return sp.Figure("appB_f14_two_codes", vocab()).add(
        half(qa, "without the address", "address", "position-route scenes, without the address",
             "scenes that leave position"),
        half(qb, "without the J++ part", "lens", "identity-route scenes, without the lens part",
             "scenes that go to position"))  # fmt: skip


# appB_f14 as two figures (Dan, 7 Nov: tighten, else split): stacked, the pair is 0.98 wide : high, under the post's
# 1.0; side by side, the routes' headers do not fit their groups and the labels meet
def appB_f14a_position_route() -> sp.Figure:
    """The position-route scenes that leave position without the address, against a random part (appB_f14's top)."""
    return sp.Figure("appB_f14a_position_route", vocab()).add(appB_f14_two_codes().blocks[0])


def appB_f14b_identity_route() -> sp.Figure:
    """The identity-route scenes that go to position without the lens part, against a random part (its bottom)."""
    return sp.Figure("appB_f14b_identity_route", vocab()).add(appB_f14_two_codes().blocks[1])


# ---- Fig. 5 as two figures (Dan, 7 Nov): the band test and the one-layer test ---------------------------------------------
def fig05a_controls_band() -> sp.Figure:
    """Fig. 5's band of layers (fact passages): the recall − lookup gap under the lens part's removal against rotated,
    logit-lens and PCA parts of the same size, and the difference lens part − largest control."""
    top = fig05_controls().blocks[0]
    return sp.Figure("fig05a_controls_band", vocab()).add(top)


def fig05b_controls_layer() -> sp.Figure:
    """Fig. 5's one layer (locker scenes): the recall's switches blocked beyond random under the lens part against
    same-size controls from the earlier runs, and the difference lens part − largest control."""
    bottom = fig05_controls().blocks[1]
    return sp.Figure("fig05b_controls_layer", vocab()).add(bottom)


# ---- appendix B f5: what the lens part decodes to -------------------------------------------------------------------------
ATOMS = "52 A: share of the rebuilt energy, "
WORDS = (("old", "the old bridge word", "old bridge word"), ("new", "the new bridge word", "new bridge word"),
         ("other", "another scene word or its class", "another scene word"), ("none", "no scene word", "no scene word"))


def appB_f5_atoms() -> sp.Figure:
    """Of the lens part's 25 directions, the share of the rebuilt energy by the word each decodes to, one column per
    word type (teal: the lens part's energy); an answer word's share beside (Dan, 7 Nov: no stack)."""
    models = [m for m in DAN if D.s(m, ATOMS + WORDS[0][1])]
    cols = []
    for key, q, header in WORDS:
        cells = {m: est(need(D.s(m, ATOMS + q), m), f"atoms.{ZK[m]}", key=f"f5.{key}.{ZK[m]}", label=True)
                 for m in models}  # fmt: skip
        cols.append(sp.DotColumn(header, "rebuilt", (-0.05, 1.1), (0, 0.5, 1), series=[sp.Series("lens", cells)]))
    answer = {m: est(need(D.s(m, ATOMS + "an answer word"), m), f"atoms.{ZK[m]}", key=f"f5.answer.{ZK[m]}")
              for m in models}  # fmt: skip
    cols.append(sp.TextColumn("answer word", "rebuilt", answer, unit_title=False))
    t = sp.DotTable(models, cols, note="of the lens part's 25 directions, by the word each decodes to")
    return sp.Figure("appB_f5_atoms", vocab()).add(t)


# ---- appendix B f19: six lockers -----------------------------------------------------------------------------------------
SIX = {"qwen3.6-27b": "results/x47_six/x52_six-20261029T004919Z/x47_2.json",
       "qwen3.5-122b-a10b": "results/x47_six/x52_six-20261029T231821Z/x47_2.json"}  # fmt: skip
PAIRS, HALF, BAR19 = 30, 15, 0.25  # 30 locker pairs, half of them; the 25% bar fixed in advance (claim_figs f19)


def appB_f19_six_lockers() -> sp.Figure:
    """With six lockers: the pairs of lockers (of 30) whose address swap reaches the 25% bar; and the lookups sent one
    locker on by the shift vector (mean over the five start lockers, the range as its whisker) against a random
    direction of the same size (grey)."""
    v = vocab()
    pq = "47.2: pairwise writes reaching 25% (dose 2)"
    ordn = ("1st", "2nd", "3rd", "4th", "5th")
    sq = "47.2: lookups sent one locker on from the {} locker, {}, dose 2"
    pairs, counts, shift, rand = {}, {}, {}, {}
    for m in DAN:
        k = ZK[m]
        n = int(need(CF.row_value("cards" if m in SIX else "fig09b", m, pq)[0], m))
        pairs[m] = sp.Est(n, cell=f"six.{k}", key=f"f19.pairs.{k}")
        counts[m] = sp.Count(n, PAIRS, cell=f"six.{k}", key=f"f19.pairs_of.{k}")
        starts = (CF._shift_cells(SIX[m], m) if m in SIX else
                  [(CF.row_value("fig09b", m, sq.format(o, "the shift vector"))[0],
                    CF.row_value("fig09b", m, sq.format(o, "a random direction (same size)"))[0]) for o in ordn])  # fmt: skip
        sh = [float(need(a, m)) for a, _b in starts]
        shift[m] = sp.Est(sum(sh) / len(sh), min(sh), max(sh), cell=f"six.{k}", key=f"f19.shift.{k}",
                          interval="range")  # fmt: skip
        rand[m] = sp.Est(
            sum(float(need(b, m)) for _a, b in starts) / len(starts), cell=f"six.{k}", key=f"f19.random.{k}"
        )
    reach = sp.DotColumn("pairs reaching the 25% bar", "pairs", (0, 33), (0, 15, 30),
                         series=[sp.Series("lookup", pairs)], rules=[sp.Rule(HALF, "half")])  # fmt: skip
    sent = sp.DotColumn("sent one locker on", "lookups", (-0.03, 0.42), (0, 0.25),
                        series=[sp.Series("control", rand, control="a random vector"), sp.Series("lookup", shift)],
                        rules=[sp.Rule(BAR19, "the 25% bar")])  # fmt: skip
    # the counts and the shift's mean [range] in text columns, beside the dots
    t = sp.DotTable(
        DAN,
        [
            reach,
            sp.TextColumn("pairs", "pair_count", counts, unit_title=False),
            sent,
            sp.TextColumn("sent one locker on", "lookups", shift, role="lookup", unit_title=False),
        ],
    )
    return sp.Figure("appB_f19_six_lockers", v).add(t)


# ---- Fig. 0: one bridge word, two readers (a schematic, no numbers) ------------------------------------------------------
def _width(text: str, bold: bool = False) -> float:
    """A text's width in inches as the post target prints a schematic sentence (value size; a bold part keeps it)."""
    from matplotlib.backends.backend_agg import RendererAgg
    from matplotlib.font_manager import FontProperties

    th = vocab().target("post")
    size = th.sizes.value
    prop = FontProperties(family=th.font, weight="bold" if bold else "normal", size=size)
    w, _h, _d = RendererAgg(10, 10, 72).get_text_width_height_descent(text, prop, ismath=False)
    return w / 72


def fig00_schematic() -> sp.Figure:
    """The carbon locker scene: the bridge word's state holds the lens part, the identity and the address; the recall
    reads the lens part, the lookup reads the identity and the address."""
    scene = ("The locker of carbon is 3. The locker of helium is 5. Eric picked ", "carbon", ".")
    x0, y0 = 0.2, 0.3
    bridge_x = x0 + _width(scene[0]) + _width(scene[1], bold=True) / 2
    sx, sy, sw, sh = 3.1, 1.0, 1.8, 1.25  # the bridge word's state
    parts = (("lens", "lens part"), ("identity", "identity"), ("address", "address"))
    part_y = {r: sy + 0.45 + j * 0.3 for j, (r, _w) in enumerate(parts)}
    rw, rh, ry = 2.5, 1.15, 2.75  # the readers' boxes
    readers = (("lookup", 0.2, "Which locker belongs to", "Eric's pick?", "→ 3, read in the scene"),
               ("recall", 8.0 - 0.2 - rw, "What is the atomic number", "of Eric's pick?", "→ 6, from memory"))  # fmt: skip
    el: list = [
        sp.Words(x0, y0, [(scene[0], None, False), (scene[1], None, True), (scene[2], None, False)], verbatim=True),
        sp.Words(bridge_x + 0.1, y0 + 0.35, [("the bridge word", None)]),
        sp.Arrow((bridge_x, y0 + 0.15), (sx + sw / 2, sy)),
        sp.Box(sx, sy, sw, sh),
        sp.Words(sx + 0.12, sy + 0.18, [("its state", None)]),
    ]
    for role, word in parts:
        el += [sp.Mark(sx + 0.2, part_y[role], role), sp.Words(sx + 0.38, part_y[role], [(word, role)], bold=True)]
    for role, x, q1, q2, answer in readers:
        el += [sp.Box(x, ry, rw, rh, role=role), sp.Words(x + 0.12, ry + 0.2, [(role, role)], bold=True),
               sp.Words(x + 0.12, ry + 0.5, [(q1, None)], verbatim=True),
               sp.Words(x + 0.12, ry + 0.72, [(q2, None)], verbatim=True),
               sp.Words(x + 0.12, ry + 0.97, [(answer, role)], verbatim=True)]  # fmt: skip
    lookup_x, recall_x = readers[0][1] + rw / 2, readers[1][1] + rw / 2
    el += [sp.Arrow((sx, part_y["identity"]), (lookup_x - 0.6, ry), role="identity", label="identity"),
           sp.Arrow((sx + 0.35, sy + sh), (lookup_x + 1.0, ry), role="address", label="address"),
           sp.Arrow((sx + sw, part_y["lens"]), (recall_x, ry), role="lens", label="lens part")]  # fmt: skip
    return sp.Figure("fig00_schematic", vocab(), direct_labels=True).add(sp.Schematic(ry + rh + 0.15, el))


def _sentence(x: float, y: float, parts) -> list:
    """Verbatim prompt text with its bridge word in bold."""
    return [sp.Words(x, y, [(text, None, bold) for text, bold in parts], verbatim=True)]


# ---- Fig. 2: the datasets (a schematic of real prompts) ------------------------------------------------------------------
def fig02_datasets(width: float | None = None) -> sp.Figure:
    """The two kinds of prompt: the fact passages (question, the lookup's passage, the recall's) and the locker scenes
    (scene, lookup question, recall question); the bridge in bold; each answer in its reader's colour, over its
    source. The answer column follows the target's width (the README draws it at 11 in, the post at 8 in)."""
    width = width or vocab().target("post").width_in
    rows = (  # (label, reader role or None, prompt lines [(text, bold)], answer, source)
        ("Fact passages", None, [[("Question: ", False), ("The composer who wrote The Magic Flute", True)],
                                 [("was of which nationality?", False)]], "", ""),
        ("lookup", "lookup", [[("“… ", False), ("Mozart", True), (" was Austrian by birth. …”", False)]], "Austrian",
         "in the passage"),
        ("recall", "recall", [[("“… A reader asked a question about ", False), ("Mozart", True)],
                              [("in the letters page. …”", False)]], "Austrian", "from memory"),
        ("Locker scenes", None, [[("The locker of carbon is 3. The locker of helium is 5.", False)],
                                 [("Eric picked ", False), ("carbon", True), (".", False)]], "", ""),
        ("lookup", "lookup", [[("Which locker belongs to Eric's pick?", False)]], "3", "in the scene"),
        ("recall", "recall", [[("What is the atomic number of Eric's pick?", False)]], "6", "from memory"),
    )  # fmt: skip
    x_label, x_prompt, top, rh = 0.12, 1.55, 0.75, 0.62
    longest = max(sum(_width(t, bold=b) for t, b in parts) for *_, lines, _a, _s in rows for parts in lines)
    # the answer column right after the longest prompt line (a gap in the middle splits the prompt from its answer)
    x_answer = min(x_prompt + longest + 0.5, width - 1.45 - 0.12)  # the answers and their sources need ~1.45 in
    el: list = [sp.Words(x_prompt, 0.25, [("Prompt", None)], bold=True),
                sp.Words(x_prompt, 0.52, [("the bridge in bold", None)]),
                sp.Words(x_answer, 0.25, [("Answer", None)], bold=True),
                sp.Words(x_answer, 0.52, [("and its source", None)])]  # fmt: skip
    for i, (label, role, lines, answer, source) in enumerate(rows):
        y0 = top + i * rh
        line_y = (y0 + rh * 0.33, y0 + rh * 0.69)
        el.append(sp.Words(x_label + (0.2 if role else 0), line_y[0], [(label, role)], bold=True))
        for k, parts in enumerate(lines):
            el += _sentence(x_prompt, line_y[k], parts)
        if answer:
            el += [sp.Words(x_answer, line_y[0], [(answer, role)], verbatim=True, bold=True),
                   sp.Words(x_answer, line_y[1], [(source, None)])]  # fmt: skip
    return sp.Figure("fig02_datasets", vocab(), direct_labels=True).add(sp.Schematic(top + rh * len(rows) + 0.1, el))


# ---- Fig. 3: the tools (layers x tokens grids) ---------------------------------------------------------------------------
def fig03_tools(width: float | None = None) -> sp.Figure:
    """The three tools as grids (layers x tokens): the cells a tool changes are one box in its colour (the lens part
    teal, another entity's part blue) with its words centred right under it (Dan, 7 Nov: a word beside every coloured
    element); the bridge word's column is labelled. The grid is an illustration: its band is the bottom rows. The
    layout follows the target's width (the README draws it at 11 in, the post at 8 in)."""
    width = width or vocab().target("post").width_in
    nl, nt, bridge = 4, 7, 4  # layers, tokens, the bridge word's token
    panels = (("remove everywhere", "a band of layers, every token", (2, 4, 0, nt), "lens", "lens part removed"),
              ("removed from the patch", "one layer, the bridge word", (3, 4, bridge, bridge + 1), "lens",
               "lens part removed"),
              ("swap", "the bridge word, over the band", (2, 4, bridge, bridge + 1), "identity",
               ("another entity's", "lens part swapped in")))  # fmt: skip
    panel_w, label_w = (width - 0.24) / 3, 0.62
    cell = min((panel_w - label_w - 0.12) / nt, 0.42)
    gy, line = 0.95, 0.22
    words_n = max(1 if isinstance(w, str) else len(w) for *_, w in panels)
    el: list = []
    for k, (title, sub, (r0, r1, t0, t1), role, word) in enumerate(panels):
        x0 = 0.12 + k * panel_w
        gx = x0 + label_w
        grid_bottom = gy + nl * cell
        el += [sp.Words(x0, 0.2, [(title, None)], bold=True), sp.Words(x0, 0.47, [(sub, None)]),
               sp.Words(gx + (bridge + 0.5) * cell - _width("bridge") / 2, gy - 0.14, [("bridge", None)]),
               sp.Words(x0, gy + nl * cell / 2, [("layers", None)]),
               sp.Words(gx + nt * cell / 2 - _width("tokens") / 2, grid_bottom + 0.17 + line * words_n + 0.12,
                        [("tokens", None)])]  # fmt: skip
        el += [sp.Box(gx + t * cell + 0.015, gy + r * cell + 0.015, cell - 0.03, cell - 0.03)
               for r in range(nl) for t in range(nt) if not (r0 <= r < r1 and t0 <= t < t1)]  # fmt: skip
        box_mid = gx + (t0 + t1) / 2 * cell
        el.append(sp.Box(gx + t0 * cell + 0.015, gy + r0 * cell + 0.015, (t1 - t0) * cell - 0.03,
                         (r1 - r0) * cell - 0.03, role=role))  # fmt: skip
        for j, w in enumerate((word,) if isinstance(word, str) else word):  # centred under the box, inside the panel
            x = min(max(box_mid - _width(w, bold=True) / 2, gx), x0 + panel_w - 0.1 - _width(w, bold=True))
            el.append(sp.Words(x, grid_bottom + 0.17 + line * j, [(w, role)], bold=True))
    height = gy + nl * cell + 0.17 + line * words_n + 0.12 + 0.3
    return sp.Figure("fig03_tools", vocab(), direct_labels=True).add(sp.Schematic(height, el))


# Declared, but styles-plot refuses them in strict mode (they stay on figkit until a decision):
# fig05 (two five-panel tables: 0.80 wide : high, under the post's 1.0; labels cross lines), appB_f14 (two five-row
# tables: 0.98)
# fig05 and appB_f14 are drawn as their splits (SPLIT).
BLOCKED = {"fig05_controls": fig05_controls, "appB_f14_two_codes": appB_f14_two_codes}
FIGS = {"fig00_schematic": fig00_schematic, "fig02_datasets": fig02_datasets,
        "fig08b_address_swap_lens": fig08b_address_swap_lens, "fig11_orthogonal": fig11_orthogonal,
        "fig13_last_token": fig13_last_token, "figA1_agents": figA1_agents, "appB_f9_where": appB_f9_where,
        "appB_f12_order": appB_f12_order, "appB_f8_facts": appB_f8_facts, "appB_f8_directions": appB_f8_directions,
        "appB_f19_six_lockers": appB_f19_six_lockers, "fig08a_address_read_remove": fig08a_address_read_remove,
        "fig05a_controls_band": fig05a_controls_band, "fig05b_controls_layer": fig05b_controls_layer,
        "appB_f5_atoms": appB_f5_atoms, "appB_f14a_position_route": appB_f14a_position_route,
        "appB_f14b_identity_route": appB_f14b_identity_route, "fig03_tools": fig03_tools,
        "fig10_answer_span": fig10_answer_span}  # fmt: skip
# Fig. 5 is drawn as two new files; the post embeds both where it embedded fig05_controls.png
SPLIT = {"fig05_controls": ("fig05a_controls_band", "fig05b_controls_layer"),
         "appB_f14_two_codes": ("appB_f14a_position_route", "appB_f14b_identity_route")}
