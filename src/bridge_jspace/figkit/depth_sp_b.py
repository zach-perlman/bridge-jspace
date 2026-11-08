"""The depth README's second batch on styles-plot (readme target): Fig. 8, 9, 10, 15 and the supplementary s01, s02,
s03, s08b. Numbers are the rows the story builders recorded in data/figures/depth/data.csv, read by figure id and
quantity. Verdict texts are not drawn (Dan, 7 Nov). depth_sp.FIGS includes these.
"""

from __future__ import annotations

import styles_plot as sp

from bridge_jspace import figdata as D
from bridge_jspace.figkit.writeup_sp_base import ZK, est, need, vocab

DAN = [m for m, _ in D.DAN]


def cell(fig: str, m: str, q: str):
    return D.s(m, q, fig)


def models_with(fig: str, qs) -> list[str]:
    return [m for m in DAN if any(cell(fig, m, q) for q in qs)]


# ---- Fig. 8: the first locker ------------------------------------------------------------------------------------------
SENTENCES = (("none", "no sentence", "no sentence"), ("neutral", "a neutral sentence", "a neutral sentence"),
             ("first", "a pick naming the first-locker item", "a pick naming the first-locker item"),
             ("another", "a pick naming another locker item", "a pick naming another locker item"),
             ("nolocker", "a pick naming an item with no locker", "a pick naming an item with no locker"))  # fmt: skip


def fig08_first_locker() -> sp.Figure:
    """45a (after the data): per model the lookup's answers on first-locker moves under the whole change, by the
    sentence added before the lockers (lanes): the share by identity with its interval, the share by position beside,
    and the code shift against no sentence (how far the pointer's code moves, in positions)."""
    f = "fig08"
    stem = "45a, first-locker moves, whole change, {}: {} share"
    models = models_with(f, [stem.format("no sentence", "identity")])
    ident, pos, shift = {}, {}, {}
    for m in models:
        k = ZK[m]
        for lane, words, _label in SENTENCES:
            c = need(cell(f, m, stem.format(words, "identity")), f"{f} {m} {words}")
            ident[(m, lane)] = est(c, f"first.{k}", key=f"f08.{lane}.identity.{k}", label=True)
            p = cell(f, m, stem.format(words, "position"))
            if p:
                pos[(m, lane)] = sp.Est(p[0], cell=f"first.{k}", key=f"f08.{lane}.position.{k}")
            b = cell(f, m, f"45a, beta vs no sentence: {words}")
            if b:
                shift[(m, lane)] = est(b, f"first.{k}", key=f"f08.{lane}.shift.{k}")
    cols = [sp.DotColumn("answers by identity", "identity_share", (0.3, 1.08), (0.4, 0.7, 1),
                         series=[sp.Series("identity", ident)]),
            sp.TextColumn("by position", "identity_share", pos, unit_title=False),
            sp.TextColumn("shift against no sentence", "code_shift", shift, unit_title=False)]  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k_, label) for k_, _w, label in SENTENCES])
    return sp.Figure("fig08_first_locker", vocab()).add(t)


# ---- Fig. 9: transfer of the pointer -----------------------------------------------------------------------------------
FORMATS = (("simple", "simple scenes"), ("prose", "prose"), ("json", "JSON"), ("table", "table"),
           ("natural", "natural passages"))  # fmt: skip
GATE = 30  # X0's bar, fixed before the data: a cell with fewer whole-change lookup switches is not counted


def fig09_transfer() -> sp.Figure:
    """(a) After the data: per model and setting (columns), the lookup's extra loss without the lens part and without
    the address fit on simple scenes. (b) 45d (fixed in advance): per format (lanes), the lookup's extra loss without
    the address fit on simple scenes and without an address refit on that format; a cell under X0's 30-switch bar is
    not counted."""
    f = "fig09"
    models = models_with(f, ["lookup extra loss without J++: simple"])
    cols = []
    for key, header in FORMATS:
        lens, ptr = {}, {}
        for m in models:
            k = ZK[m]
            a, b = (cell(f, m, f"lookup extra loss without {w}: {key}") for w in ("J++", "the pointer"))
            if a:
                lens[m] = est(a, f"format.{k}", key=f"f09.{key}.lens.{k}")
            if b:
                ptr[m] = est(b, f"format.{k}", key=f"f09.{key}.pointer.{k}")
            if not (a or b):
                lens[m] = sp.Missing("no run")
        cols.append(sp.DotColumn(header, "switches", (-0.1, 0.6), (0, 0.25, 0.5),
                                 series=[sp.Series("lens", lens), sp.Series("address", ptr)]))  # fmt: skip
    top = sp.DotTable(models, cols, note="after the data: the address fit on simple scenes, not refit")
    refit_models = models_with(f, ["(b) prose: lookup switches with the whole change"])
    fit, refit = {}, {}
    for m in refit_models:
        k = ZK[m]
        for key in ("prose", "json", "table"):
            n = cell(f, m, f"(b) {key}: lookup switches with the whole change")
            if not n or n[0] < GATE:
                fit[(m, key)] = sp.Missing("too few switches")
                continue
            for store, w, tag in (
                (fit, "the pointer fit on simple scenes", "fit"),  # data keys (data/figures/depth/data.csv)
                (refit, "the refit pointer", "refit"),
            ):
                store[(m, key)] = est(need(cell(f, m, f"(b) {key}: lookup extra loss without {w}"), w),
                                      f"refit.{k}", key=f"f09.b.{key}.{tag}.{k}")  # fmt: skip
    bottom = sp.DotTable(refit_models, [
        sp.DotColumn("address fit on simple scenes", "switches", (-0.05, 0.33), (0, 0.15, 0.3),
                     series=[sp.Series("address", fit)]),
        sp.DotColumn("address refit on the format", "switches", (-0.05, 0.33), (0, 0.15, 0.3),
                     series=[sp.Series("address", refit)]),
    ], lanes=[sp.Lane(k_, label) for k_, label in FORMATS[1:4]])  # fmt: skip
    return sp.Figure("fig09_transfer", vocab()).add(top, bottom)


# ---- Fig. 10: what is left ---------------------------------------------------------------------------------------------
REMOVALS = (("jpp", "J++ part + pointer", "lens part and address"),
            ("idout", "+ identity outside J++", "+ identity outside the lens part"),
            ("wrong", "+ wrong pair instead (scenes where it reached 0.9 of identity's share)", "+ a wrong pair instead"))  # fmt: skip


def fig10_what_is_left() -> sp.Figure:
    """The sanity swap: per model and removal (lanes), the share of the whole change's lookup switches still switching
    with the part removed, against a random part of the same size removed (grey); the part's share of the change
    beside; on the wrong-pair lane, the routes test's identity answers cut beyond the wrong pair (45e, matched
    scenes)."""
    f = "fig10"
    models = models_with(f, ["sanity swap, lookups still switching without J++ part + pointer: the part"])
    part, rand, share, routes = {}, {}, {}, {}
    for m in models:
        k = ZK[m]
        for lane, words, _label in REMOVALS:
            q = f"sanity swap, lookups still switching without {words}: "
            p = cell(f, m, q + "the part")
            if not p:
                part[(m, lane)] = sp.Missing("no run")
                continue
            part[(m, lane)] = est(p, f"left.{lane}.{k}", key=f"f10.{lane}.part.{k}", label=True)
            rand[(m, lane)] = est(need(cell(f, m, q + "a random part of the same size"), q), f"left.{lane}.{k}",
                                  key=f"f10.{lane}.random.{k}")  # fmt: skip
            s = cell(f, m, f"share of the change: {words}")
            if s:
                share[(m, lane)] = sp.Est(s[0], cell=f"left.{lane}.{k}", key=f"f10.{lane}.share.{k}")
        r = cell(f, m, "routes test: identity answers cut by identity outside J++ beyond the wrong pair (scenes where "
                       "the wrong pair reached 0.9 of its share)")  # fmt: skip
        if r:
            routes[(m, "wrong")] = est(r, f"left.wrong.{k}", key=f"f10.routes.{k}")
    cols = [sp.DotColumn("lookups still switching", "still_switching", (-0.05, 1.15), (0, 0.5, 1),
                         series=[sp.Series("control", rand, control="a random part"), sp.Series("lookup", part)],
                         connect=("control", "lookup")),
            sp.TextColumn("share", "change_share", share),
            sp.TextColumn("identity answers cut", "identity_cut_beyond_wrong_pair", routes)]  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k_, label) for k_, _w, label in REMOVALS])
    return sp.Figure("fig10_what_is_left", vocab()).add(t)


# ---- Fig. 15: the mechanisms that failed their rules ---------------------------------------------------------------------
# each test's bar, fixed in advance with the test (scripts/story_b48.py build_mechanisms' groups)
BARS = {"48.2": 0.40, "48.3": 0.85, "48.5": 0.30}
HEADS_BAR = 3  # 48.4: at least 3 of the five heads


def fig15_mechanisms() -> sp.Figure:
    """Every mechanism test proposed for the split, per model: the test's deciding number against its bar, fixed in
    advance with the test (48.2, 48.3, 48.5 as dots with the bar; 48.4 a count of five heads; 47.6 the identity
    answers kept with the block, beside the rule's per-model bar)."""
    v, f = vocab(), "fig15"
    models = models_with(f, ["48.3, probe at the item, locker after the pick (accuracy)"])

    def col(header, unit, q, test, role, lim, ticks, label=True):
        cells = {}
        for m in models:
            c = cell(f, m, q)
            cells[m] = (est(c, f"{test}.{ZK[m]}", key=f"f15.{test}.{header}.{ZK[m]}", label=label) if c
                        else sp.Missing("no run"))  # fmt: skip
        bar = BARS.get(test)
        rules = [sp.Rule(bar, "bar fixed in advance: {}", unit=unit, key=f"f15.{test}.bar")] if bar is not None else []
        return sp.DotColumn(header, unit, lim, ticks, series=[sp.Series(role, cells)], rules=rules)

    heads = {}
    for m in models:
        c = cell(f, m, "48.4: heads passing the rest at twice the J++ part, share of the five")
        heads[m] = (
            sp.Count(round(c[0] * 5), 5, cell=f"48.4.{ZK[m]}", key=f"f15.48.4.{ZK[m]}") if c else sp.Missing("no run")
        )
    kept, bar476 = {}, {}
    for m in models:
        c = cell(f, m, "47.6 (b) block/sentence/all: lookup identity share")
        kept[m] = est(c, f"47.6.{ZK[m]}", key=f"f15.47.6.{ZK[m]}", label=True) if c else sp.Missing("no run")
        b = cell(f, m, "47.6: the rule's bar (whole change's identity share less 0.10)")
        if b:
            bar476[m] = sp.Est(b[0], cell=f"47.6.{ZK[m]}", key=f"f15.47.6.bar.{ZK[m]}")
    top = sp.DotTable(models, [
        sp.ColumnGroup("48.2: late MLPs carry the recall", [
            col("recall accuracy drop", "mlp_lost", "48.2 B, bridge_late: recall accuracy lost", "48.2", "recall",
                (-0.02, 0.5), (0, 0.2, 0.4))]),
        sp.Gutter(),
        sp.ColumnGroup("48.3: a person mark", [
            col("probe at the item", "probe_accuracy", "48.3, probe at the item, locker after the pick (accuracy)",
                "48.3", "neutral", (0, 1), (0, 0.5, 1), label=False),
            col("probe at the number", "probe_accuracy", "48.3, probe at the number, locker after the pick (accuracy)",
                "48.3", "neutral", (0, 1), (0, 0.5, 1), label=False)]),
    ])  # fmt: skip
    bottom = sp.DotTable(models, [
        # a group, as each other test here: its header wraps over its span, the column header stays short (SP613)
        sp.ColumnGroup("48.4: heads passing the rest", [sp.TextColumn("heads", "heads_of_five", heads,
                                                                      unit_title=False)]),
        sp.ColumnGroup("48.5: the address as a second route", [
            col("recalls naming the target's item", "named",
                "48.5, (ii) (i) and the pointer write: recall names the written locker's item", "48.5", "recall",
                (-0.02, 0.4), (0, 0.15, 0.3))]),
        sp.Gutter(),
        sp.ColumnGroup("47.6: blocking the pick sentence", [
            sp.DotColumn("identity answers kept", "identity_kept", (0, 0.75), (0, 0.3, 0.6),
                         series=[sp.Series("identity", kept)]),
            sp.TextColumn("the bar", "identity_kept", bar476, unit_title=False)]),
    ], note=f"48.4's bar fixed in advance: {HEADS_BAR} of 5")  # fmt: skip
    return sp.Figure("fig15_mechanisms", v).add(top, bottom)


# ---- s01: the split in every setting ------------------------------------------------------------------------------------
S01 = (("main", "main test (two people swap picks)", "main test"),
       ("onepick", "one-pick scenes (only the asked pick changes)", "one-pick scenes"),
       ("matched2", "matched scenes (two people swap picks)", "matched scenes, two people swap"),
       ("matched1", "matched scenes (only the asked pick changes)", "matched scenes, one pick changes"),
       ("varied", "varied scenes: prose / JSON / table", "varied scenes"),
       ("natural", "natural passages", "natural passages"))  # fmt: skip


def _by_model_columns(fig, kind_rows, quantity, cid, key, lim, ticks):
    """Rows are conditions (an entity kind given in code), columns are models: the lookup's and the recall's dots."""
    models = [m for m in DAN if any(cell(fig, m, quantity(stem, "recall")) for _k, stem, _n in kind_rows)]
    cols = []
    for m in models:
        k = ZK[m]
        lk, rc = {}, {}
        for row, stem, _name in kind_rows:
            a, b = cell(fig, m, quantity(stem, "lookup")), cell(fig, m, quantity(stem, "recall"))
            if a:
                lk[row] = est(a, f"{cid}.{row}.{k}", key=f"{key}.{row}.lookup.{k}")
            if b:
                rc[row] = est(b, f"{cid}.{row}.{k}", key=f"{key}.{row}.recall.{k}")
            if not (a or b):
                rc[row] = sp.Missing("no run")
        cols.append(sp.DotColumn(vocab().entity("models", m).name, "switches", lim, ticks,
                                 series=[sp.Series("lookup", lk), sp.Series("recall", rc)],
                                 connect=("lookup", "recall")))  # fmt: skip
    return cols


def s01_split_all_scene_sets() -> sp.Figure:
    """Supplementary to Fig. 1: per setting (rows) and model (columns), the lookup's and the recall's extra loss
    without the lens part, joined (the gap is the joining line)."""
    v = vocab().with_entities("settings", [(k, n) for k, _s, n in S01])
    cols = _by_model_columns("s01", S01, lambda stem, r: f"{stem}: {r} extra loss", "split", "s01", (-0.1, 1.0),
                             (0, 0.5, 1))  # fmt: skip
    return sp.Figure("s01_split_all_scene_sets", v).add(sp.DotTable([k for k, *_ in S01], cols, kind="settings"))


# ---- s02: every part tried ---------------------------------------------------------------------------------------------
S02 = (("jpp", "J++ part", "lens part"), ("jpp_noword", "J++ part without the word's directions",
                                          "lens part without the word's directions"),
       ("word", "the word's directions", "the word's directions"),
       ("pca", "PCA directions (same size)", "PCA directions (same size)"),
       ("other_scene", "J++ part fitted to another scene", "lens part fitted to another scene"),
       ("wu", "logit-lens directions", "logit-lens directions"),
       ("embed", "input-embedding directions", "input-embedding directions"),
       ("rand", "random lens directions", "random lens directions"))  # fmt: skip


def s02_parts_all() -> sp.Figure:
    """Supplementary to Fig. 2: every part tried (rows), per model (columns), the lookup's and the recall's extra
    loss without it, joined."""
    v = vocab().with_entities("parts", [(k, n) for k, _s, n in S02])
    cols = _by_model_columns("s02", S02, lambda stem, r: f"{stem}: {r} extra loss", "part", "s02", (-0.1, 0.9),
                             (0, 0.4, 0.8))  # fmt: skip
    return sp.Figure("s02_parts_all", v).add(sp.DotTable([k for k, *_ in S02], cols, kind="parts"))


# ---- s03: sentence order, split ----------------------------------------------------------------------------------------
S03 = (("main_before", "main test (two people swap picks), locker before the pick", "main test, locker first"),
       ("main_after", "main test (two people swap picks), locker after the pick", "main test, locker after"),
       ("clean_before", "clean one-pick scenes, locker before the pick", "clean scenes, locker first"),
       ("clean_after", "clean one-pick scenes, locker after the pick", "clean scenes, locker after"))  # fmt: skip


def s03_order_split() -> sp.Figure:
    """Supplementary to the order test: per model and order (lanes), the lookups and the recalls the whole change
    switches in the main test (95% Wilson), and the recall's and the lookup's extra loss without the lens part (the
    lookup's only where it has 30 switches or more); the gap on the main test's locker-first lane."""
    f = "s03"
    models = models_with(f, ["lookups switched by the whole change, locker sentence before the pick"])
    sw_l, sw_r, lk, rc, gap = {}, {}, {}, {}, {}
    for m in models:
        k = ZK[m]
        for when in ("before", "after"):
            lane = f"main_{when}"
            for store, who in ((sw_l, "lookups"), (sw_r, "recalls")):
                c = cell(f, m, f"{who} switched by the whole change, locker sentence {when} the pick")
                if c:
                    store[(m, lane)] = sp.Est(c[0], c[1], c[2], cell=f"order.{lane}.{k}", interval="wilson95",
                                              key=f"s03.{lane}.{who}.{k}")  # fmt: skip
        for lane, stem, _label in S03:
            r = cell(f, m, f"(b) {stem}: recall extra loss")
            if not r:
                rc[(m, lane)] = sp.Missing("no run")
                continue
            rc[(m, lane)] = est(r, f"order.{lane}.{k}", key=f"s03.{lane}.recall.{k}")
            a = cell(f, m, f"(b) {stem}: lookup extra loss")
            lk[(m, lane)] = (
                est(a, f"order.{lane}.{k}", key=f"s03.{lane}.lookup.{k}") if a else sp.Missing("too few switches")
            )
        g = cell(f, m, "main test (two people swap picks), locker before the pick: gap")
        if g:
            gap[(m, "main_before")] = est(g, f"order.main_before.{k}", key=f"s03.gap.{k}")
    cols = [sp.DotColumn("switched by the whole change", "switched", (0, 1.05), (0, 0.5, 1),
                         series=[sp.Series("lookup", sw_l), sp.Series("recall", sw_r)]),
            # the lookup and the recall in their own columns: a lookup under 30 switches says so in an empty cell
            sp.ColumnGroup("switches blocked beyond random", [
                sp.DotColumn("lookup", "switches", (-0.15, 0.4), (0, 0.2), series=[sp.Series("lookup", lk)]),
                sp.DotColumn("recall", "switches", (-0.1, 1.0), (0, 0.5, 1), series=[sp.Series("recall", rc)])]),
            sp.TextColumn("gap: recall − lookup", "gap_share", gap, unit_title=False)]  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k_, label) for k_, _s, label in S03],
                    note="switched by the whole change: the main test only")  # fmt: skip
    return sp.Figure("s03_order_split", vocab()).add(t)


# ---- s08b: the pointer's moves and the neutral sentence --------------------------------------------------------------------
MOVES = (("first", "moves with the first", "moves to or from the first locker"),
         ("second_third", "moves second ↔ third", "moves between the second and third"))  # fmt: skip


def s08b_pointer_moves_and_neutral_sentence() -> sp.Figure:
    """Supplementary to Fig. 8 (after the data): (top) the routes test's position answers with only the pointer kept,
    by the move (lanes), the whole change's beside; (bottom) the neutral-sentence test: the code's shift in positions
    with a sentence before the first locker or between the lockers and the picks."""
    f = "s08b"
    models = models_with(f, ["(b) routes, position share, whole, moves with the first"])
    keep, whole = {}, {}
    for m in models:
        k = ZK[m]
        for lane, words, _label in MOVES:
            c = need(cell(f, m, f"(b) routes, position share, keep_alf, {words}"), words)
            keep[(m, lane)] = sp.Est(c[0], cell=f"moves.{k}", key=f"s08b.{lane}.keep.{k}", label=True)
            w = need(cell(f, m, f"(b) routes, position share, whole, {words}"), words)
            whole[(m, lane)] = sp.Est(w[0], cell=f"moves.{k}", key=f"s08b.{lane}.whole.{k}")
    top = sp.DotTable(models, [
        sp.DotColumn("position answers, only the address kept", "position_share", (-0.03, 0.75), (0, 0.3, 0.6),
                     series=[sp.Series("address", keep)]),
        sp.TextColumn("whole change", "position_share", whole, unit_title=False),
    ], lanes=[sp.Lane(k_, label) for k_, _w, label in MOVES])  # fmt: skip
    shift = {}
    cols = []
    for key, header in (("B1", "a sentence before the first locker"),
                        ("B2", "a sentence between the lockers and the picks")):  # fmt: skip
        for m in models:
            c = cell(f, m, f"(c) neutral sentence {key}: the code's shift in positions")
            shift[m] = est(c, f"shift.{ZK[m]}", key=f"s08b.{key}.{ZK[m]}", label=True) if c else sp.Missing("no run")
        cols.append(sp.DotColumn(header, "code_shift", (0, 0.35), (0, 0.15, 0.3),
                                 series=[sp.Series("address", dict(shift))]))  # fmt: skip
    bottom = sp.DotTable(models, cols)
    return sp.Figure("s08b_pointer_moves_and_neutral_sentence", vocab()).add(top, bottom)


FIGS = {"fig08_first_locker": fig08_first_locker, "fig09_transfer": fig09_transfer,
        "fig10_what_is_left": fig10_what_is_left, "fig15_mechanisms": fig15_mechanisms,
        "s01_split_all_scene_sets": s01_split_all_scene_sets, "s02_parts_all": s02_parts_all,
        "s03_order_split": s03_order_split,
        "s08b_pointer_moves_and_neutral_sentence": s08b_pointer_moves_and_neutral_sentence}  # fmt: skip
SUPP = {"s01_split_all_scene_sets", "s02_parts_all", "s03_order_split", "s08b_pointer_moves_and_neutral_sentence"}
