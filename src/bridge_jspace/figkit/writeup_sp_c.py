"""The write-up figures styles-plot 0.1.6 can draw (Dan, 7 Nov, grammar decisions 1, 2 and 4): a second estimate of one
role in its own column (fig06), a 100% stack with its numbers in text columns beside it (fig07; stacks carry no
whiskers), a depth sweep whose points fixed in advance carry their own vertical whiskers (appB_f15), and appB_f18 as
the depth README's fig21 (the same cells). Same data accessors as the figkit builders; writeup_sp.FIGS takes them in."""

from __future__ import annotations

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


def fig06_nine_models() -> sp.Figure:
    """Per model: the answers moved by another entity's lens part swapped in (Bolt's run at 100 directions in its own
    column), and the recall − lookup gap with the lens part knocked out against the largest same-size control (the
    122B scored by probability in its own column). The models' grades are verdicts: they stay in the text."""
    swap, swap100, gap, soft = {}, {}, {}, {}
    for m in NINE:
        k = _id(m)
        c = D.b(SWAPKEY.get(k, f"swap.{k}.swap"))
        # Muse and the 122B were swapped only in an earlier protocol, not in this set
        swap[m] = (
            est(c, f"swap.{k}", key=SWAPKEY.get(k, f"swap.{k}.swap"), label=True)
            if c
            else sp.Missing("no comparable run")
        )
        gap[m] = est(need(D.b(f"ko.{k}.mk"), f"ko.{k}.mk"), f"gap.{k}", key=f"ko.{k}.mk", label=True)
    swap100["bolt"] = est(need(D.b("swap.nb.k100.swap"), "swap.nb.k100.swap"), "swap100.nb", key="swap.nb.k100.swap",
                          label=True)  # fmt: skip
    soft["qwen3.5-122b-a10b"] = est(need(D.b("ko.q122.soft"), "ko.q122.soft"), "soft.q122", key="ko.q122.soft",
                                    label=True)  # fmt: skip
    ticks = {m: t for m in NINE if (t := S.ctrl(_id(m))) is not None}
    # the first panel wide enough for "no comparable run" clear of its zero line; the one-model columns narrow
    cols = [
        sp.DotColumn("lens part swapped in", "moved", (-8, 84), (0, 40, 80), width=2.0,
                     series=[sp.Series("lens", swap, word="lens part swapped in")]),
        sp.DotColumn("at 100 directions", "moved", (-8, 84), (0, 40, 80), width=1.1,
                     series=[sp.Series("lens", swap100, word="at 100 directions")]),
        sp.DotColumn(GAP, "gap", (-3, 72), (0, 30, 60), series=[sp.Series("neutral", gap, word=GAP)], ticks=ticks),
        sp.DotColumn("scored by probability", "gap", (-3, 72), (0, 30, 60), width=1.1,
                     series=[sp.Series("neutral", soft, word="scored by probability")]),
    ]  # fmt: skip
    return sp.Figure("fig06_nine_models", vocab()).add(sp.DotTable(list(NINE), cols))


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
    points with their own 95% whiskers; their values, with the intervals, in the table under the sweep (labels on
    the crossing curves would sit on a line)."""
    lines, points, values = [], [], {arm: {} for arm, *_ in ARMS}
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
                                   lo=r[1], hi=r[2]))  # fmt: skip
            values[arm][m] = est(r, cell, key=f"f15.{arm}.{k}")
    sweep = sp.Sweep(list(LINK), "depth_share", "lookups_switched", lines, points=points, panel_h=1.0,
                     xlim=(-0.04, 1.03), ylim=(-0.04, 1.1), xticks=(0, 0.5, 1), yticks=(0, 0.5, 1))  # fmt: skip
    table = sp.DotTable(list(LINK), [sp.TextColumn(ARM_HEADER[arm], "lookups_switched", values[arm], unit_title=False)
                                     for arm, *_ in ARMS])  # fmt: skip
    return sp.Figure("appB_f15_link_crossover", vocab()).add(sweep, table)


# ---- appendix B f18: code and tool output (the depth README's fig21, the same cells) ------------------------------------
def appB_f18_code_tool() -> sp.Figure:
    """The depth README's fig21_code_tool under the write-up's id: the locker probe and the position answers without
    the address and with only it kept, each arm in its own column against a random part of the same size."""
    from bridge_jspace.figkit import depth_sp

    fig = depth_sp.fig21_code_tool()
    fig.id = "appB_f18_code_tool"
    return fig


FIGS = {"fig06_nine_models": fig06_nine_models, "fig07_routes": fig07_routes,
        "appB_f15_link_crossover": appB_f15_link_crossover, "appB_f18_code_tool": appB_f18_code_tool}  # fmt: skip
