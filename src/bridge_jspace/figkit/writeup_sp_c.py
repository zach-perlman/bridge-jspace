"""The write-up figures styles-plot 0.1.6 can draw (Dan, 7 Nov, grammar decisions 1, 2 and 4): a second estimate of one
role in its own column (fig06), a 100% stack with its numbers in text columns beside it (fig07; stacks carry no
whiskers), a depth sweep whose points fixed in advance carry their own vertical whiskers (appB_f15), and appB_f18 as
the depth README's fig21 (the same cells). Same data accessors as the figkit builders; writeup_sp.FIGS takes them in."""

from __future__ import annotations

import dataclasses

import styles_plot as sp

from bridge_jspace import figdata as CV
from bridge_jspace import figdata as D
from bridge_jspace import figdata as S
from bridge_jspace.figkit.writeup_sp_base import ZK, est, need, vocab

DAN = [m for m, _ in D.DAN]
GAP = "gap: recall − lookup"


def _id(m: str) -> str:
    return vocab().entity("models", m).id


# ---- Fig. 6: nine models -------------------------------------------------------------------------------------------------
NINE = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning", "qwen3.5-122b-a10b", "deepseek",
        "ministral", "bolt", "olmo")  # fmt: skip
SWAPKEY = {"ds": "swap.ds.mid.swap", "mi": "swap.mi.mid.swap"}  # (deck_figs.f_nine)


# rows by the bar fixed before the main runs (amendment 33: gap >= 30, rotated and logit-lens controls < 10)
BANDS = (("Passes the bar", ("qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning")),
         ("Fails on a control", ("muse-glimmer-30b", "qwen3.5-122b-a10b")),
         ("Fails on the gap", ("ministral", "deepseek", "bolt", "olmo")))  # fmt: skip
NINE_ROWS = tuple(m for _, ms in BANDS for m in ms)
# docs/breadth/prereg_replication_1022.md, amendment 33: "M - K >= 30 with the logit-lens and rotated controls < 10"
GAP_BAR, CONTROL_BAR = 30, 10


def _nine_cells(key: str, cell: str, label: bool = True) -> dict:
    """One estimate per model from docs/breadth/data.csv (`key` with {k}); "not run" where no run exists."""
    out = {}
    for m in NINE_ROWS:
        k = _id(m)
        c = D.b(key.format(k=k))
        out[m] = sp.Missing("not run") if c is None else est(c, f"{cell}.{k}", key=key.format(k=k), label=label)
    return out


def _verdict(m: str) -> str:
    """The bar's verdict on one model from its data (gap >= 30, both controls < 10), checked against its band."""
    k = _id(m)
    gap = need(D.b(f"ko.{k}.mk"), f"gap {k}")[0] >= GAP_BAR
    ctrl = max(need(D.b(f"ko.{k}.{c}"), f"{c} {k}")[0] for c in ("rot", "u")) < CONTROL_BAR
    word = {(True, True): "passes", (True, False): "fails: control", (False, True): "fails: gap"}.get(
        (gap, ctrl), "fails: gap and control")
    band = next(b for b, ms in BANDS if m in ms)
    assert (word == "passes") == (band == "Passes the bar"), (m, word, band)
    return word


def fig06_nine_models() -> sp.Figure:
    """Nine models in three bands by the bar fixed before the main runs: the recall − lookup gap
    under the knock-out against the bar of 30, and what each same-size control costs against the limit of 10, one
    panel per control (one grey dot per line: the grammar gives a second control its own panel)."""
    gap = sp.DotColumn("Recall minus lookup gap", "nine_gap", (0, 70), (0, 30, 60), weight=1.3,
                       series=[sp.Series("neutral", _nine_cells("ko.{k}.mk", "gap"), word="Recall minus lookup gap")],
                       rules=[sp.Rule(GAP_BAR, "bar: gap ≥ {} points", unit="nine_bar", key="nine.bar.gap")])  # fmt: skip
    limit = [sp.Rule(CONTROL_BAR, "limit: {} points", unit="nine_bar", key="nine.bar.control")]
    rot = sp.DotColumn("rotated part", "nine_control", (0, 40), (0, 20, 40), rules=limit,
                       series=[sp.Series("control", _nine_cells("ko.{k}.rot", "rot"), control="rotated")])
    logit = sp.DotColumn("logit-lens directions", "nine_control", (0, 40), (0, 20, 40), rules=limit,
                         series=[sp.Series("control", _nine_cells("ko.{k}.u", "logit"), control="logit lens")])
    # one verdict per band, under its first model: a verdict under all nine makes the figure taller than wide (SP604)
    assert all(_verdict(m) for m in NINE_ROWS)  # the bands agree with the data
    row_sub = {ms[0]: band for band, ms in BANDS}
    table = sp.DotTable(list(NINE_ROWS), [gap, sp.Gutter(), sp.ColumnGroup("Cost of same-size controls", [rot, logit])],
                        kind="nine", row_sub=row_sub)  # fmt: skip
    return sp.Figure("fig06_nine_models", vocab(), subtitle="known-fact set").add(table)


def nine_tests(fid: str) -> sp.Figure:
    """The README's nine-model figure (f3_nine_models; its text cites the swap): four columns in the bar's order, the
    gap under the knock-out, the larger of the rotated and logit-lens controls, the gap scored by the answer's
    probability, and the answers moved by another entity's lens part swapped in. The write-up draws
    fig06_nine_models instead."""
    rot, logit = {}, {}
    for m in NINE_ROWS:
        k = _id(m)
        r_, u_ = need(D.b(f"ko.{k}.rot"), f"rot {k}"), need(D.b(f"ko.{k}.u"), f"u {k}")
        code, c = ("rot", r_) if r_[0] >= u_[0] else ("u", u_)
        (rot if code == "rot" else logit)[m] = est(c, f"ctrl.{k}", key=f"ko.{k}.{code}", label=True)
    swap = {}
    for m in NINE_ROWS:
        k = _id(m)
        key = SWAPKEY.get(k, f"swap.{k}.swap")
        c = D.b(key)
        swap[m] = sp.Missing("not run") if c is None else est(c, f"swap.{k}", key=key, label=True)
    cols = [
        sp.DotColumn("Gap under the knock-out", "points", (-5, 80), (0, 30, 60), weight=1.15,
                     rules=[sp.Rule(GAP_BAR, "bar: {}", unit="points", key="nine.bar.gap")],
                     series=[sp.Series("neutral", _nine_cells("ko.{k}.mk", "gap"), word="Gap under the knock-out")]),
        sp.DotColumn("Larger control", "points", (-5, 50), (0, 20, 40), weight=1.2,
                     series=[sp.Series("control", rot, control="rotated", word="rotated"),
                             sp.Series("control", logit, control="logit lens", word="logit lens")],
                     rules=[sp.Rule(CONTROL_BAR, "bar: {}", unit="points", key="nine.bar.control")]),
        sp.DotColumn("Gap scored by probability", "points", (-5, 80), (0, 30, 60), weight=1.15,
                     series=[sp.Series("neutral", _nine_cells("ko.{k}.soft", "soft"), word="Gap scored by probability")]),
        sp.DotColumn("Swap", "moved", (-5, 100), (0, 40, 80), series=[sp.Series("lens", swap, word="Swap")]),
    ]  # fmt: skip
    row_sub = {ms[0]: band for band, ms in BANDS}
    return sp.Figure(fid, vocab()).add(sp.DotTable(list(NINE_ROWS), cols, kind="nine", row_sub=row_sub))

# ---- Fig. 7: the two routes ----------------------------------------------------------------------------------------------
ROUTE_Q = "another item moved, whole: {} share"


def routes(fid: str) -> sp.Figure:
    """The lookup's answers when another item's locker moved, a 100% bar per model: by identity, by position, other.
    The position share's 95% interval (the segment the claim rests on) and the number itself in text columns beside."""
    models = [m for m in DAN if D.s(m, ROUTE_Q.format("identity"))]
    ids, pos, oth, pos_ci, num = {}, {}, {}, {}, {}
    for m in models:
        k = ZK[m]
        i_, p_ = need(D.s(m, ROUTE_Q.format("identity")), m), need(D.s(m, ROUTE_Q.format("position")), m)
        cell = f"routes.{k}"
        ids[m] = sp.Est(i_[0], cell=cell)
        pos[m] = sp.Est(p_[0], cell=cell)
        oth[m] = sp.Est(1 - i_[0] - p_[0], cell=cell)
        pos_ci[m] = est(p_, cell, key=f"routes.position.{k}")
        num[m] = est(need(D.s(m, ROUTE_Q.format("value")), m), cell, key=f"routes.number.{k}", interval=False)
    stack = sp.Stack(models, [sp.Segment("by identity", "identity", ids), sp.Segment("by position", "address", pos),
                              sp.Segment("other", "other", oth)], unit="lookups",
                     header="when another item's locker moved",
                     columns=[sp.TextColumn("by position", "lookups", pos_ci, unit_title=False),
                              sp.TextColumn("the number", "lookups", num, unit_title=False)])  # fmt: skip
    return sp.Figure(fid, vocab()).add(stack)


def fig07_routes() -> sp.Figure:
    return routes("fig07_routes")


# ---- appendix B f15: the change at the bridge word against the same change copied --------------------------------------
BW = "45q, layer {}: the bridge-word change (lookups switched)"
CP = "45q, layer {}: the copy into the locker sentences (lookups switched)"
ARMS = (("a", "the bridge-word change at L", "L"), ("c", "copy at L, every locker-sentence token", "L"),
        ("d", "copy at L/2, every locker-sentence token", "L/2"))  # fmt: skip
ARM_HEADER = {"a": "at the bridge word, at L", "c": "copied, at L", "d": "copied, at L/2"}
LINK = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")  # Lightning below its gate, the 122B no run


def appB_f15_link_crossover() -> sp.Figure:
    """Per model, the lookups switched over the depth by the change at the bridge word and by the same change copied
    into the locker sentences (two lookup lines, named in words), and the three cells fixed in advance at L and L/2 as
    points with their own 95% whiskers and their values beside them."""
    lines, points = [], []
    for m in LINK:
        k, depth = ZK[m], CV.DEPTH[m]
        layers = CV._layers(m, "fig03", r"45q, layer (\d+): the bridge-word change")
        for q, tag, word in ((BW, "bridge", "at the bridge word"), (CP, "copy", "copied into the locker sentences")):
            v = [need(D.s(m, q.format(la), "fig03"), f"{m} {la}") for la in layers]
            lines.append(sp.Line(m, "lookup", [la / depth for la in layers], [t[0] for t in v], cell=f"sweep.{tag}.{k}",
                                 band=([t[1] for t in v], [t[2] for t in v]), word=word))  # fmt: skip
        L, half = (
            need(D.s(m, f"45q: {q}", "fig03"), q)[0] for q in ("L, the rule's layer", "L/2, the rule's half layer")
        )
        for arm, what, which in ARMS:
            r = need(D.s(m, f"45q, the rule's arm {arm}: {what} (lookups switched)", "fig03"), f"{m} {arm}")
            cell = f"arm.{arm}.{k}"
            points.append(sp.Point(m, "lookup", (L if which == "L" else half) / depth, cell=cell, value=r[0],
                                   lo=r[1], hi=r[2], key=f"f15.{arm}.{k}", label=True))  # fmt: skip
    sweep = sp.Sweep(list(LINK), "depth_share", "lookups_switched", lines, points=points, panel_h=1.0,
                     xlim=(-0.04, 1.03), ylim=(-0.04, 1.1), xticks=(0, 0.5, 1), yticks=(0, 0.5, 1))  # fmt: skip
    return sp.Figure("appB_f15_link_crossover", vocab()).add(sweep)


# ---- appendix B f18: code and tool output (the depth README's fig21, the same cells) ------------------------------------
def appB_f18_code_tool() -> sp.Figure:
    """The depth README's fig21_code_tool under the write-up's id: the locker probe and the position answers without
    the address and with only it kept, each arm in its own column against a random part of the same size."""
    from bridge_jspace.figkit import depth_sp

    fig = depth_sp.fig21_code_tool()
    fig.id = "appB_f18_code_tool"
    return fig


# ---- Result 1: one patch at the bridge, two answers ----------------------------------------------------------------------
ANSWER_KEPT = "main test, recall: share of its loss kept when the lens part keeps the answer words' directions"
# the rules fixed in advance: the conflict test's (scripts/x0_necessity.py docstring: lookup excess <= 0.10,
# recall >= 0.30) and the answer-word check's (docs/depth/EXPERIMENTS.md t51-12: arm 2 keeps >= 0.7)
LOOKUP_AT_MOST, RECALL_AT_LEAST, ANSWER_BAR = 0.10, 0.30, 0.7


def _kept(key, cell, label=False):
    return {m: est(need(CV.w(key.format(k=ZK[m])), key.format(k=ZK[m])), f"{cell}.{ZK[m]}", key=key.format(k=ZK[m]),
                   label=label) for m in DAN}


def patch_split() -> sp.Figure:
    """One patch at the bridge, two answers (locker scenes). (A) the patch's switches the lens part's removal blocks
    beyond a random part of the same size, lookup and recall, against the pass rule fixed in advance (grey). (B) the
    share of the recall's drop that remains when the removal keeps the answer words' directions, against its bar fixed
    in advance. The answer word's share of the lens part's energy is in the post's text, not on the figure."""
    rows = DAN

    def layer(m, reader):
        # the recall printed; a lookup printed only where it misses the rule (the others sit inside the rule's line)
        c = need(S.conflict(m, reader), f"{reader} {m}")
        miss = reader == "lookup" and c[0] > LOOKUP_AT_MOST
        return est(c, f"layer.{ZK[m]}", key=f"patch.layer.{reader}.{ZK[m]}", label=reader == "recall" or miss)

    remove = sp.DotColumn(
        "(A) Patch, lens part removed", "switches_share", (-0.2, 1.2), (0, 0.5, 1),
        series=[sp.Series("lookup", {m: layer(m, "lookup") for m in rows}),
                sp.Series("recall", {m: layer(m, "recall") for m in rows})],
        # the recall's rule is on its switches before the random part is subtracted (scripts/x0_necessity.py); the
        # post's text says so
        rules=[sp.Rule(LOOKUP_AT_MOST, "rule ≤ {}", unit="switches", key="patch.rule.lookup"),
               sp.Rule(RECALL_AT_LEAST, "rule ≥ {}", unit="switches", key="patch.rule.recall")])  # fmt: skip
    header_b = "(B) Patch, lens part removed, answer words kept"
    answer = sp.DotColumn(
        header_b, "drop_kept", (0, 1.3), (0, 0.5, 1),  # room right of the 122B's whisker (1.18) for its value
        series=[sp.Series("recall", {m: est(need(D.s(m, ANSWER_KEPT, "conflict_answer"), f"kept {m}"), f"answer.{ZK[m]}",
                                            key=f"patch.answer_kept.{ZK[m]}", label=True) for m in rows},
                          word=header_b)],  # one series: the header names it, no colour word
        rules=[sp.Rule(ANSWER_BAR, "bar {}", unit="drop_kept", key="patch.rule.answer")])  # fmt: skip
    table = sp.DotTable(rows, [remove, sp.Gutter(), answer])
    return sp.Figure("patch_split", vocab(), subtitle="locker scenes · patch").add(table)


def patch_layers() -> sp.Figure:
    """One layer is not essential (locker scenes, no patch, the ladder's own scenes in every column): the answers
    kept when the lens part is removed from a prompt's own state at the bridge word at one layer, at the bridge word
    over four layers, and at every token over four layers; lookup and recall dots, grey tick: the recall's answers kept
    with a random part of the same share removed instead."""
    cols = []
    for rung, header in ((1, "bridge word, 1 layer"), (2, "bridge word, 4 layers"), (5, "every token, 4 layers")):
        cols.append(sp.DotColumn(header, "kept_bridge", (0, 1.15), (0, 0.5, 1),
                                 series=[sp.Series("lookup", _kept(f"patch.rung{rung}.zero.lookup.{{k}}", f"rung{rung}")),
                                         sp.Series("recall", _kept(f"patch.rung{rung}.zero.recall.{{k}}", f"rung{rung}"))],
                                 ticks={m: need(CV.w(f"patch.rung{rung}.rand.recall.{ZK[m]}"), m)[0] for m in DAN}))
    table = sp.DotTable(DAN, cols)  # the claim is in the caption
    # this figure's grey tick is the recall's random part, not the largest same-size control ([key].tick)
    return sp.Figure("patch_layers", dataclasses.replace(vocab(), key_tick=RANDOM_TICK),
                     subtitle="locker scenes · no patch").add(table)


RANDOM_TICK = "random part, same size"

FIGS = {"patch_split": patch_split, "patch_layers": patch_layers, "fig06_nine_models": fig06_nine_models,
        "fig07_routes": fig07_routes,
        "appB_f15_link_crossover": appB_f15_link_crossover, "appB_f18_code_tool": appB_f18_code_tool}  # fmt: skip
