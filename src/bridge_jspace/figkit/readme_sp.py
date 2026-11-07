"""The root README's figures (figures/readme/) on styles-plot, for the readme target. Several are write-up figures
under the README's file name (ALIAS: the same declaration, the README's figure id, so the registry has their rows under
both ids); the rest are declared here from the figkit builders' data (exemplars.py, deck_figs.py, claim_figs.py,
depth_figs.py), same accessors, same file names.

uv run python -m bridge_jspace.figkit.readme_sp [ids...]
"""

from __future__ import annotations

import sys

import styles_plot as sp

from bridge_jspace import figdata as CF
from bridge_jspace import figdata as D
from bridge_jspace import figdata as DF
from bridge_jspace import figdata as S
from bridge_jspace.figkit import layout as L
from bridge_jspace.figkit import writeup_sp as WS
from bridge_jspace.figkit import writeup_sp_b as WB
from bridge_jspace.figkit.writeup_sp_base import REPO, ZK, est, need, vocab

OUT = REPO / "figures" / "readme"
TARGET = "readme"
DAN = [m for m, _ in D.DAN]
TWIN = WB.TWIN

# README id -> the write-up figure it draws (the same cells and statuses, scripts/status_registry.py copies them)
ALIAS = {"r3_last_token": "fig13_last_token", "f9_where": "appB_f9_where",
         "f8_facts": "appB_f8_facts", "f8_directions": "appB_f8_directions", "f12_order": "appB_f12_order",
         "f14_two_codes": "appB_f14_two_codes", "p0b_tools": "fig03_tools",
         "f3_nine_models": "fig06_nine_models", "r5_routes": "fig07_routes",
         # f6_address drawn as two figures: one table of four columns needs 2.99 in of colour words over a 2.19 in panel
         # (SP609; Dan, 7 Nov: lanes or split); the README embeds both where it embedded f6_address.png
         "f6a_address_read_remove": "fig08a_address_read_remove", "f6b_address_swap_lens": "fig08b_address_swap_lens"}  # fmt: skip
WRITEUP = {**WS.FIGS, **WB.BLOCKED}
# README figures drawn here from a write-up figure's cells (the registry copies that figure's rows under these ids)
COPIES = {"r1_c1_split": "fig01_main_split", "r1_c1_gaps": "fig01_main_split", "f2_controls": "fig05_controls",
          "f2_controls_layer": "fig05_controls"}


# laid out in inches: drawn for the README's width, not the post's (p0a_datasets is a markdown table in the README)
SCHEMATICS = {"p0b_tools"}


def _alias(fid: str):
    def build() -> sp.Figure:
        src = WRITEUP[ALIAS[fid]]
        fig = src(vocab().target(TARGET).width_in) if fid in SCHEMATICS else src()
        fig.id = fid  # the README's figure id: its registry rows (copies of the write-up figure's)
        return fig

    build.__doc__ = f"The write-up's {ALIAS[fid]}, as the README's {fid}."
    return build


# ---- r1_c1_split: the headline (README brief F2) ----------------------------------------------------------------------
READ_HEADLINE = ("read: on {model}, removing the lens part everywhere costs recall {{recall}} points and lookup "
                 "{{lookup}}; at one layer it blocks {{rc}} of the recall's switches beyond random and {{lk}} of the "
                 "lookup's")  # fmt: skip


def r1_c1_split() -> sp.Figure:
    """The headline: two dumbbell panels, lookup → recall per model. Left, the band test (fact passages): each reader's
    answers turned wrong when the lens part is removed everywhere; right, the one-layer test (locker scenes): each reader's
    switches blocked beyond a random part, on the grey band. The gap, recall − lookup, printed at each panel's right
    end; the gaps with their controls are r1_c1_gaps (the Finding 1 fold). One sentence reads the 27B's row."""
    drop = sp.DotColumn(
        "answers turned wrong", "drop", (-4, 70), (0, 30, 60),
        series=[sp.Series("lookup", {m: est(D.b(f"ko.{ZK[m]}.lostK"), f"band.{ZK[m]}", interval=False) for m in DAN}),
                sp.Series("recall", {m: est(D.b(f"ko.{ZK[m]}.lostM"), f"band.{ZK[m]}", interval=False) for m in DAN})],
        connect=("lookup", "recall"),
    )  # fmt: skip
    band_gap = sp.TextColumn(WS.GAP, "gap", {m: est(D.b(f"ko.{ZK[m]}.mk"), f"band.{ZK[m]}", key=f"ko.{ZK[m]}.mk")
                                             for m in DAN}, role="neutral", unit_title=False)  # fmt: skip
    shares = sp.DotColumn(
        "switches blocked beyond random", "switches", (-0.25, 1.0), (0, 0.5, 1),
        series=[sp.Series("lookup", {m: est(S.conflict(m, "lookup"), f"layer.{ZK[m]}", interval=False) for m in DAN}),
                sp.Series("recall", {m: est(S.conflict(m, "recall"), f"layer.{ZK[m]}", interval=False) for m in DAN})],
        connect=("lookup", "recall"), band=(-0.1, 0.1),
    )  # fmt: skip
    layer_gap = sp.TextColumn(WS.GAP, "gap_share", {m: WS._layer_gap(m) for m in DAN}, role="neutral",
                              unit_title=False)  # fmt: skip
    t = sp.DotTable(DAN, [sp.ColumnGroup(WS.BAND, [drop, band_gap]), sp.Gutter(),
                          sp.ColumnGroup(WS.LAYER, [shares, layer_gap])])  # fmt: skip
    m, k = "qwen3.6-27b", ZK["qwen3.6-27b"]
    numbers = {"recall": (need(D.b(f"ko.{k}.lostM"), "lostM")[0], "drop", f"ko.{k}.lostM"),
               "lookup": (need(D.b(f"ko.{k}.lostK"), "lostK")[0], "drop", f"ko.{k}.lostK"),
               "rc": (need(S.conflict(m, "recall"), m)[0], "switches", f"conflict.recall.{k}"),
               "lk": (need(S.conflict(m, "lookup"), m)[0], "switches", f"conflict.lookup.{k}")}  # fmt: skip
    read = READ_HEADLINE.format(model=vocab().entity("models", m).name)
    return sp.Figure("r1_c1_split", vocab(), read=read, numbers=numbers).add(t)


def r1_c1_gaps() -> sp.Figure:
    """The headline's gaps with their controls (the Finding 1 fold): the band test's gap with its 95% whisker and the
    largest same-size control as a grey tick; the one-layer test's gap with its interval."""
    layer_gap = sp.DotColumn(WS.GAP, "gap_share", (-0.1, 1.1), (0, 0.5, 1),
                             series=[sp.Series("neutral", {m: WS._layer_gap(m) for m in DAN}, word=WS.GAP)])  # fmt: skip
    t = sp.DotTable(DAN, [sp.ColumnGroup(WS.BAND, [WS._band_columns(DAN)[1]]), sp.Gutter(),
                          sp.ColumnGroup(WS.LAYER, [layer_gap])])  # fmt: skip
    return sp.Figure("r1_c1_gaps", vocab()).add(t)


# ---- f2_controls (+ f2_controls_layer): every control on the lens part's axis (README brief F3) -----------------------
def _controls_table(models, lens, controls, unit, lim, ticks, diff, diff_unit, group, note) -> sp.DotTable:
    """One axis: per model a lane for the lens part (teal, labelled) and one per same-size control (grey, its name on
    the lane); the lens part − largest control difference printed on the lens part's lane."""
    series = [sp.Series("lens", {(m, "lens"): c for m, c in lens.items()})]
    for lane, name, cells in controls:
        series.append(sp.Series("control", {(m, lane): c for m, c in cells.items()}, control=name))
    col = sp.DotColumn(group, unit, lim, ticks, series=series)  # the lanes name the lens part and each control
    text = sp.TextColumn("lens part − largest control", diff_unit, {(m, "lens"): diff(m) for m in models},
                         unit_title=False)  # fmt: skip
    lanes = [sp.Lane("lens", "lens part"), *(sp.Lane(lane, name) for lane, name, _ in controls)]
    # the test names the panel; what is measured is in the caption (one line fewer: the aspect minimum)
    return sp.DotTable(models, [col, text], lanes=lanes)


def _cell(c, cell, key, label):
    return sp.Missing("no run") if not c else est(c, cell, key=key, label=label, interval=label)


def f2_controls() -> sp.Figure:
    """The band test (fact passages): the recall − lookup gap under the lens part's removal and under each same-size
    control's (rotated, logit lens, PCA), on one axis, and the difference lens part − largest control."""
    band = {m: f"band.{ZK[m]}" for m in DAN}
    lens = {m: _cell(WB._band_cell(m, "mk"), band[m], f"ko.{ZK[m]}.mk", True) for m in DAN}
    controls = [(q, name, {m: _cell(WB._band_cell(m, q), band[m], f"ko.{ZK[m]}.{q}", False) for m in DAN})
                for q, name in (("rot", "rotated"), ("u", "logit lens"), ("pc", "PCA"))]  # fmt: skip

    def diff(m):
        c = D.w(f"fig05.band_diff.{ZK[m]}")
        return sp.Missing("source missing") if c is None else sp.Est(c[0], c[1], c[2], cell=band[m],
                                                                      key=f"fig05.band_diff.{ZK[m]}")  # fmt: skip

    t = _controls_table(DAN, lens, controls, "gap", (-4, 70), (0, 30, 60), diff, "gap_difference",
                        "Band of layers · fact passages", "the recall − lookup gap under each removal")  # fmt: skip
    return sp.Figure("f2_controls", vocab()).add(t)


def f2_controls_layer() -> sp.Figure:
    """The one-layer test (locker scenes, earlier runs with a same-size control): the recall's switches blocked beyond
    a random part without the lens part and without each same-size control (PCA, logit lens, random lens directions),
    on one axis, and the difference lens part − largest control."""
    layer = {m: f"layer.{ZK[m]}" for m in DAN}
    lens = {m: _cell(D.s(m, "J++ part: recall extra loss", "fig02"), layer[m], f"fig05.layer.lens.{ZK[m]}", True)
            for m in DAN}  # fmt: skip
    names = {"rand": "random lens directions"}
    controls = [(k, names.get(k, name), {m: _cell(D.s(m, q, "fig02"), layer[m], f"fig05.layer.{k}.{ZK[m]}", False)
                                         for m in DAN}) for k, name, q in D.LAYER_CTRL]  # fmt: skip

    def diff(m):
        top_ = D.layer_largest(m)
        if not top_:
            return sp.Missing("no run")
        lens_c, key, _name, cell = top_
        pair = D.b(f"f2.layer.{ZK[m]}.pca") if key == "pca" else None
        if pair and pair[1] is not None:
            return sp.Est(pair[0], pair[1], pair[2], cell=layer[m], key=f"f2.layer.{ZK[m]}.pca")
        return sp.Est(need(lens_c, m)[0] - need(cell, m)[0], cell=layer[m], key=f"fig05.layer_diff.{ZK[m]}",
                      note="no interval")  # fmt: skip

    t = _controls_table(DAN, lens, controls, "switches", (-0.08, 1.0), (0, 0.5, 1), diff, "share_difference",
                        "One layer · locker scenes",
                        "the recall's switches blocked beyond random · earlier runs with a same-size control")  # fmt: skip
    return sp.Figure("f2_controls_layer", vocab()).add(t)


# ---- r1_dan_split: the one-layer test alone --------------------------------------------------------------------------
def r1_dan_split() -> sp.Figure:
    """The one-layer test (locker scenes): each reader's switches blocked beyond random on the grey band, and the gap
    recall − lookup with its 95% interval (the depth README's Fig. 1; the write-up Fig. 1's right half)."""
    shares = sp.DotColumn(
        "switches blocked beyond random", "switches", (-0.25, 1.0), (0, 0.5, 1),
        series=[sp.Series("lookup", {m: est(S.conflict(m, "lookup"), f"layer.{ZK[m]}") for m in DAN}),
                sp.Series("recall", {m: est(S.conflict(m, "recall"), f"layer.{ZK[m]}") for m in DAN})],
        connect=("lookup", "recall"), band=(-0.1, 0.1),
    )  # fmt: skip
    gap = sp.DotColumn("gap: recall − lookup", "gap_share", (-0.1, 1.1), (0, 0.5, 1),
                       series=[sp.Series("neutral", {m: WS._layer_gap(m) for m in DAN}, word=WS.GAP)])  # fmt: skip
    t = sp.DotTable(DAN, [sp.ColumnGroup("One layer · locker scenes", [shares, gap])])
    return sp.Figure("r1_dan_split", vocab()).add(t)


# ---- r4_pointer: another entity's lens part, against a probe's subspace ---------------------------------------------
R4 = (("swap", "swap", "another entity's own passage", "lens"),
      ("neutral", "neutral_pts", "one neutral sentence about another entity", "lens"),
      ("noown", "noown_pts", "without another entity's own-word directions", "lens"),
      ("rot", "rot_pts", "rotated", "control"))  # fmt: skip
# F4's rows: the source of the swapped-in part (row key, data key, role, short label)
R4_ROWS = (("swap", "swap", "lens", "its own passage"), ("neutral", "neutral_pts", "lens", "a neutral sentence"),
           ("noown", "noown_pts", "lens", "without its own-word directions"),
           ("probe", "probe_pts", "neutral", "a probe's subspace"), ("rot", "rot_pts", "control", "rotated"))
R4_GROUP = "answers moved to the other entity's fact"

def r4_pointer() -> sp.Figure:
    """Answers moved to another entity's fact (README brief F4): rows are the source of the swapped-in part (its own
    passage, one neutral sentence about it, without its own-word directions: the lens part; a probe's subspace that
    reads the fact, slate; rotated, grey), one panel per model on one shared axis. The paired difference neutral
    sentence − own passage is in the caption, by key."""
    v = vocab().with_entities("sources", [(k, name) for k, *_r, name in R4_ROWS])
    cols = []
    for m in TWIN:
        k = ZK[m]
        by_role: dict[str, dict] = {}
        for row, key, role, _name in R4_ROWS:
            c = D.b(f"probe.{k}.probe_pts" if row == "probe" else f"ptr.{k}.{key}")
            cell = f"probe.{k}" if row == "probe" else f"{row}.{k}"
            dkey = f"probe.{k}.probe_pts" if row == "probe" else f"ptr.{k}.{key}"
            by_role.setdefault(role, {})[row] = (est(c, cell, key=dkey, label=True) if c else sp.Missing("no run"))
        series = [sp.Series("lens", by_role["lens"]), sp.Series("neutral", by_role["neutral"], word="probe"),
                  sp.Series("control", by_role["control"], control="rotated")]  # fmt: skip
        cols.append(sp.DotColumn(v.entity("models", m).name, "moved", (-8, 96), (0, 40, 80), series=series))
    t = sp.DotTable([r for r, *_ in R4_ROWS], [sp.ColumnGroup(R4_GROUP, cols)], kind="sources",
                    note="another entity: one of the same kind · answers moved to its fact")  # fmt: skip
    return sp.Figure("r4_pointer", v).add(t)


# ---- f5_atoms: what the lens part decodes to --------------------------------------------------------------------------
ATOMS = "52 A: share of the rebuilt energy, "


def f5_atoms() -> sp.Figure:
    """Of the lens part's 25 directions, the share of the rebuilt energy by the word each decodes to: the old and the new
    bridge word (both the lens part, named in grey lane words), an answer word (brick); another scene word and no
    scene word as numbers beside (Dan, 7 Nov: no new roles)."""
    models = [m for m in DAN if D.s(m, ATOMS + "the old bridge word")]
    lens, answer, other, none_ = {}, {}, {}, {}
    for m in models:
        k = ZK[m]
        for lane, q in (("old", "the old bridge word"), ("new", "the new bridge word")):
            lens[(m, lane)] = est(need(D.s(m, ATOMS + q), m), f"atoms.{k}", key=f"f5.{lane}.{k}", label=True)
        answer[(m, "answer")] = est(need(D.s(m, ATOMS + "an answer word"), m), f"atoms.{k}", key=f"f5.answer.{k}",
                                    label=True)  # fmt: skip
        other[(m, "old")] = est(need(D.s(m, ATOMS + "another scene word or its class"), m), f"atoms.{k}",
                                key=f"f5.other_scene.{k}")  # fmt: skip
        none_[(m, "old")] = est(need(D.s(m, ATOMS + "no scene word"), m), f"atoms.{k}", key=f"f5.no_scene.{k}")
    col = sp.DotColumn("share of the rebuilt energy", "rebuilt", (-0.03, 1.05), (0, 0.5, 1),
                       series=[sp.Series("lens", lens), sp.Series("answer", answer, word="answer word")])  # fmt: skip
    t = sp.DotTable(models, [col, sp.TextColumn("another scene word", "rebuilt", other, unit_title=False),
                             sp.TextColumn("no scene word", "rebuilt", none_, unit_title=False)],
                    lanes=[sp.Lane("old", "old bridge word"), sp.Lane("new", "new bridge word"),
                           sp.Lane("answer", "answer word")],
                    note="of the lens part's 25 directions, by the word each decodes to")  # fmt: skip
    return sp.Figure("f5_atoms", vocab()).add(t)


# ---- f6_address: read, remove, swap, rebuild ---------------------------------------------------------------------------
def f6_address() -> sp.Figure:
    """The address in four columns: read by the locker probe, taken out, swapped, and rebuilt by 25 lens directions
    (the write-up's Fig. 8a and 8b side by side)."""
    a, b = WB.fig08a_address_read_remove(), WB.fig08b_address_swap_lens()
    t = sp.DotTable(DAN, [*a.blocks[0].columns, *b.blocks[0].columns])
    return sp.Figure("f6_address", vocab()).add(t)


# ---- f11_monitor: the address at the last token -------------------------------------------------------------------------
def f11_monitor() -> sp.Figure:
    """The locker probe's accuracy for the address at the last token with only the lens part kept (25 or 100 lens
    directions), against a random part of the same energy and the full state (grey)."""
    q = "the address at the last token, main test, {} lens directions: "
    models = [m for m in DAN if D.s(m, q.format(25) + "the J++ part")]
    cols = []
    for n in (25, 100):
        lens, rand, full = {}, {}, {}
        for m in models:
            k = ZK[m]
            lens[m] = est(need(D.s(m, q.format(n) + "the J++ part"), m), f"monitor.{k}", key=f"f11.lens.{n}.{k}")
            rand[m] = est(need(D.s(m, q.format(n) + "a random part (same energy)"), m), f"monitor.{k}",
                          key=f"f11.random.{n}.{k}", interval=False)  # fmt: skip
            full[m] = est(need(D.s(m, q.format(n) + "the full state"), m), f"monitor.{k}", key=f"f11.full.{n}.{k}",
                          interval=False)  # fmt: skip
        # two grey dots in one row could not be told apart: the full state (the figkit figure's black tick) is a number
        # beside, with the lens part's (a label between three marks crosses one)
        dots = sp.DotColumn("probe accuracy", "probe_accuracy", (0.4, 1.02), (0.5, 0.75, 1),
                            series=[sp.Series("control", rand, control="energy-matched random"),
                                    sp.Series("lens", lens)],
                            connect=("control", "lens"))  # fmt: skip
        cols += [sp.ColumnGroup(f"{n} lens directions", [
            dots, sp.TextColumn("lens part", "probe_accuracy", lens, role="lens", unit_title=False),
            sp.TextColumn("the full state", "probe_accuracy", full, unit_title=False)]), sp.Gutter()]  # fmt: skip
    t = sp.DotTable(models, cols[:-1], note="the locker probe's accuracy for the address at the last token")
    return sp.Figure("f11_monitor", vocab()).add(t)


# ---- f10_sentence_order: where the locker sentence sits -----------------------------------------------------------------
def f10_sentence_order() -> sp.Figure:
    """The lookups switched by the whole change with the locker sentence before or after the pick (ours); then the post
    hoc two-by-two: the changed prompt's sentence before or after, with the original sentence first or after."""
    models = [m for m in DAN if D.s(m, CF.ORDER_Q.format("before the pick"), "fig03")]
    lanes = (("first", "before"), ("after", "after"))
    main = {}
    for m in models:
        k = ZK[m]
        for lane, when in lanes:
            main[(m, lane)] = est(need(D.s(m, CF.ORDER_Q.format(f"{when} the pick"), "fig03"), m), f"order.{k}",
                                  key=f"f10.order.{lane}.{k}", label=True)  # fmt: skip
    cols = [sp.DotColumn("lookups switched", "lookups_switched", (0, 1.05), (0, 0.5, 1),
                         series=[sp.Series("lookup", main)])]  # fmt: skip
    for orig, header in (("before", "original locker first"), ("after", "original locker after")):
        cells = {}
        for m in models:
            k = ZK[m]
            for lane, when in lanes:
                c = D.s(m, CF.BOTH_Q.format(orig, when), "fig03")
                if c:
                    cells[(m, lane)] = est(c, f"both.{orig}.{k}", key=f"f10.both.{orig}.{lane}.{k}", label=True)
                elif lane == "first":
                    cells[(m, lane)] = sp.Missing("no run")
        cols.append(sp.DotColumn(header, "lookups_switched", (-0.2, 1.3), (0, 0.5, 1),
                                 series=[sp.Series("lookup", cells)]))  # fmt: skip
    t = sp.DotTable(models, cols, lanes=[sp.Lane("first", "sentence before the pick"),
                                         sp.Lane("after", "sentence after the pick")])  # fmt: skip
    return sp.Figure("f10_sentence_order", vocab()).add(t)


# ---- t12_two_by_two: both operations on both datasets ---------------------------------------------------------------------
LIGHTNING = "nemotron-3.5-lightning"


def t12_two_by_two() -> sp.Figure:
    """Both operations on both datasets in one unit, recall − lookup as a share lost: one layer (ours) and a band of
    layers (Zach's), on locker scenes and on fact passages; grey, the same gap with a same-size control."""
    cols = []
    for j, (header, q, qc) in enumerate(DF.TWO_BY_TWO):
        gap, ctl = {}, {}
        for m in DAN:
            k = ZK[m]
            v, c = D.s(m, q), D.s(m, qc)
            if not v:
                why = ("too few switches" if j == 1 and D.s(m, DF.SWITCHES) else
                       "below gate" if j == 2 and m == LIGHTNING else "no run")  # fmt: skip
                gap[m] = sp.Missing(why)
                continue
            cell = f"t12.{j}.{k}"
            gap[m] = est(v, cell, key=f"t12.{j}.{k}", label=True)
            if c:
                ctl[m] = est(c, cell, key=f"t12.{j}.control.{k}")
        control = "rotated" if j == 3 else "a random part"
        cols.append(sp.DotColumn(header.capitalize(), "gap_effect", (-0.25, 1.0), (0, 0.5, 1),
                                 series=[sp.Series("control", ctl, control=control), sp.Series("neutral", gap, word=header.capitalize())]))  # fmt: skip
    t = sp.DotTable(DAN, [sp.ColumnGroup("One layer", cols[:2]), sp.Gutter(), sp.ColumnGroup("Band of layers", cols[2:])])
    return sp.Figure("t12_two_by_two", vocab()).add(t)


FIGS = {**{fid: _alias(fid) for fid in ALIAS}, "r1_c1_split": r1_c1_split, "r1_c1_gaps": r1_c1_gaps,
        "f2_controls": f2_controls, "f2_controls_layer": f2_controls_layer,
        "r1_dan_split": r1_dan_split, "r4_pointer": r4_pointer,
        "f5_atoms": f5_atoms, "f11_monitor": f11_monitor, "f10_sentence_order": f10_sentence_order,
        "t12_two_by_two": t12_two_by_two}  # fmt: skip
# Declared but refused strict (SP609, see ALIAS): f6_address, drawn as f6a + f6b.
BLOCKED = {"f6_address": f6_address}


def build(ids=None) -> list[str]:
    """Save the README set strict into figures/readme/ (numbered files, figkit/layout.py); r1_dan_split and
    t12_two_by_two belong to the depth set (depth_sp builds them). Returns the failures."""
    # the README links f9_where as "Figure": its claim for the index
    return L.build("readme", FIGS, TARGET, ids, {"f9_where": "Middle layers need the bridge's mention; deeper layers, "
                                                              "the question"})  # fmt: skip


if __name__ == "__main__":
    sys.exit(1 if build(sys.argv[1:] or None) else 0)
