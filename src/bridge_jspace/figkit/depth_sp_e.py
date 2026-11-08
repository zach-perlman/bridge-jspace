"""The depth README's figures for the two claims that had none inline (docs pass P2-4, 7 Nov): claim 3, the recall
also reads the item's earlier mention (rule 45p, figure "fig03c" rows of data/figures/depth/data.csv), and claim 7,
the address added by itself brings position answers back (the routes test's keep-only arms, "fig07" rows). Every
number is read from data/figures/depth/data.csv by figure id and quantity.
"""

from __future__ import annotations

import styles_plot as sp

from bridge_jspace import figdata as D
from bridge_jspace.figkit.writeup_sp_base import ZK, est, vocab

DAN = [m for m, _ in D.DAN]
ARM = "45p, {}: recall switches lost against (1)"


def fig03d_earlier_mention() -> sp.Figure:
    """45p: the recall's switches blocked against the base edit (1) when the new item's tokens at its earlier mention
    also lose their own lens part (arm 2), against the same tokens losing a random part of the same share (arm 3) as a
    grey control dot on the same axis (Dan, 8 Nov: it was a tick, whose key word is "the largest same-size control");
    beside it, another item's tokens losing their own lens part (arm 4)."""
    models = [m for m in DAN if D.s(m, ARM.format("a2"), "fig03c")]
    item, other, rand = {}, {}, {}
    for m in models:
        k = ZK[m]
        item[m] = est(D.s(m, ARM.format("a2"), "fig03c"), f"item.{k}", key=f"f03d.item.{k}", label=True)
        other[m] = est(D.s(m, ARM.format("a4"), "fig03c"), f"other.{k}", key=f"f03d.other.{k}", label=True)
        rand[m] = est(D.s(m, ARM.format("a3"), "fig03c"), f"random.{k}", key=f"f03d.random.{k}", label=True,
                      interval=False)
    cols = [sp.DotColumn("without the lens part at the item's earlier mention", "recall_blocked", (-0.1, 0.75),
                         (0, 0.25, 0.5), series=[sp.Series("control", rand, control="a random part"),
                                                 sp.Series("recall", item)], connect=("control", "recall")),
            sp.DotColumn("without another item's lens part there", "recall_blocked", (-0.1, 0.75), (0, 0.25, 0.5),
                         series=[sp.Series("recall", other)])]  # fmt: skip
    return sp.Figure("fig03d_earlier_mention", vocab()).add(sp.DotTable(models, cols))


def fig05e_address_added_alone() -> sp.Figure:
    """The routes test, another item moved: position answers with only the address added at the bridge word, against
    only a random part of its share (grey)."""
    q = "another item moved, {}: position share"
    models = [m for m in DAN if D.s(m, q.format("keep_alf"), "fig07")]
    alone, rand = {}, {}
    for m in models:
        k = ZK[m]
        alone[m] = est(D.s(m, q.format("keep_alf"), "fig07"), f"keep.{k}", key=f"f05e.address.{k}", label=True)
        rand[m] = est(D.s(m, q.format("keep_alf_rand"), "fig07"), f"keep.{k}", key=f"f05e.random.{k}", interval=False)
    col = sp.DotColumn("position answers with only the address", "lookups", (-0.03, 0.55), (0, 0.25, 0.5),
                       series=[sp.Series("control", rand, control="a random part"), sp.Series("address", alone)],
                       connect=("control", "address"))  # fmt: skip
    return sp.Figure("fig05e_address_added_alone", vocab()).add(sp.DotTable(models, [col]))


FIGS = {"fig03d_earlier_mention": fig03d_earlier_mention, "fig05e_address_added_alone": fig05e_address_added_alone}
