"""The depth README's dot-table figures (figures/depth/) on styles-plot, for the readme target. Their numbers are the
rows scripts/readme_story_figures.py and the story_b* builders recorded in data/figures/depth/data.csv (read by
figure id and quantity, never the newest verdict file); three are write-up figures under the depth README's file
name (ALIAS). Verdict texts ("the rule's reading", clauses) are not drawn (Dan, 7 Nov): they stay in the README.

uv run python -m bridge_jspace.figkit.depth_sp [ids...]
"""

from __future__ import annotations

import sys

import styles_plot as sp

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import readme_sp as RS
from bridge_jspace.figkit.writeup_sp_base import REPO, ZK, est, vocab

OUT = REPO / "figures" / "depth"
DAN = [m for m, _ in D.DAN]

# depth id -> the write-up figure it draws (registry rows copied, as readme_sp.ALIAS)
ALIAS = {"fig13_attention": "appB_f17_attention", "fig09b_six_lockers": "appB_f19_six_lockers",
         "fig24_two_codes": "appB_f14_two_codes"}  # fmt: skip


def path(fid: str):
    """Where a depth figure is written (one place, for the folder layout to come)."""
    return OUT / f"{fid}.png"


def _alias(fid: str):
    def build() -> sp.Figure:
        fig = RS.WRITEUP[ALIAS[fid]]()
        fig.id = fid
        return fig

    build.__doc__ = f"The write-up's {ALIAS[fid]}, as the depth README's {fid}."
    return build


def cell(fig: str, m: str, q: str):
    return D.s(m, q, fig)


def models_with(fig: str, qs) -> list[str]:
    return [m for m in DAN if any(cell(fig, m, q) for q in qs)]


def readers(fig, models, q_lookup, q_recall, cid, key, interval=True):
    """The lookup's and the recall's dots of one condition (a missing cell says "no run")."""
    out = {"lookup": {}, "recall": {}}
    for m in models:
        for reader, q in (("lookup", q_lookup), ("recall", q_recall)):
            c = cell(fig, m, q)
            if c:
                out[reader][m] = est(c, f"{cid}.{ZK[m]}", key=f"{key}.{reader}.{ZK[m]}", interval=interval)
            elif reader == "recall":  # one missing word per row
                out[reader][m] = sp.Missing("no run")
    return out


def reader_column(header, unit, lim, ticks, cells, band=True) -> sp.DotColumn:
    return sp.DotColumn(header, unit, lim, ticks, series=[sp.Series("lookup", cells["lookup"]),
                                                          sp.Series("recall", cells["recall"])],
                        connect=("lookup", "recall"), band=(-0.1, 0.1) if band else None)  # fmt: skip


# ---- fig01b: the split in the other settings -------------------------------------------------------------------------
SETTINGS = (("ld", "main test (two people swap picks), scored on the logit difference", "logit difference", "logit_shift"),
            ("clean", "clean one-pick scenes, locker before the pick", "clean one-pick scenes", "switches"),
            ("varied", "varied scenes: prose / JSON / table", "varied scenes", "switches"),
            ("natural", "natural passages", "natural passages", "switches"))  # fmt: skip


def fig01b_settings() -> sp.Figure:
    """The lookup's and the recall's extra loss without the J++ part in the other settings: the main test scored on
    the logit difference, the clean one-pick scenes (45m, fixed in advance), varied scenes, natural passages."""
    qs = [f"{s}: {r} extra loss" for _k, s, _h, _u in SETTINGS for r in ("lookup", "recall")]
    models = models_with("fig01b", qs)
    cols = []
    for k, stem, header, unit in SETTINGS:
        cells = readers("fig01b", models, f"{stem}: lookup extra loss", f"{stem}: recall extra loss", k, f"f01b.{k}",
                        interval=False)  # fmt: skip
        cols.append(reader_column(header, unit, (-0.2, 1.0), (0, 0.5, 1), cells, band=False))
    return sp.Figure("fig01b_settings", vocab()).add(sp.DotTable(models, cols))


# ---- fig01c: zeroing the J++ part at one layer -------------------------------------------------------------------------
def fig01c_zeroing() -> sp.Figure:
    """47.5: the answers kept at the layer with the J++ part's 25 directions taken out against a random part of the
    same size taken out, for the recall and the lookup."""
    stem = "47.5: {}'s answers kept at L, {} taken out"
    models = models_with("fig01c", [stem.format("recall", "the J++ part's 25 directions")])
    cols = []
    for reader in ("recall", "lookup"):
        lens, rand = {}, {}
        for m in models:
            k = ZK[m]
            a, r = (cell("fig01c", m, stem.format(reader, w)) for w in ("the J++ part's 25 directions",
                                                                         "a random part (same size)"))  # fmt: skip
            if a:
                lens[m] = est(a, f"zero.{k}", key=f"f01c.{reader}.{k}", label=True)
            if r:
                rand[m] = est(r, f"zero.{k}", key=f"f01c.{reader}.random.{k}", interval=False)
        cols.append(sp.DotColumn(f"{reader}'s answers kept", "kept", (0.8, 1.04), (0.8, 0.9, 1),
                                 series=[sp.Series("control", rand, control="a random part"),
                                         sp.Series(reader, lens)]))  # fmt: skip
    return sp.Figure("fig01c_zeroing", vocab()).add(sp.DotTable(models, cols))


# ---- fig02 and fig05b: parts of the same size, as lanes ----------------------------------------------------------------
def _parts(fig, fid, parts, share: bool) -> sp.Figure:
    first = parts[0][1]
    models = models_with(fig, [f"{first}: recall extra loss", f"{first}: lookup extra loss"])
    lookup, recall, shares = {}, {}, {}
    for key, stem, _label in parts:
        for m in models:
            k = ZK[m]
            for reader, store in (("lookup", lookup), ("recall", recall)):
                c = cell(fig, m, f"{stem}: {reader} extra loss") or cell(fig, m, stem.format(reader))
                if c:
                    store[(m, key)] = est(c, f"{key}.{k}", key=f"{fid}.{key}.{reader}.{k}")
            s = cell(fig, m, f"{stem}: share of the change") if share else None
            if s:
                shares[(m, key)] = sp.Est(s[0], cell=f"{key}.{k}", key=f"{fid}.{key}.share.{k}")
    cols = [sp.DotColumn("switches blocked beyond random", "switches", (-0.15, 0.85), (0, 0.4, 0.8),
                         series=[sp.Series("lookup", lookup), sp.Series("recall", recall)],
                         connect=("lookup", "recall"), band=(-0.1, 0.1))]  # fmt: skip
    if share:
        cols.append(sp.TextColumn("share of the change", "change_share", shares, unit_title=False))
    t = sp.DotTable(models, cols, lanes=[sp.Lane(k, label) for k, _s, label in parts])
    return sp.Figure(fid, vocab()).add(t)


PARTS02 = (("jpp", "J++ part", "lens part"), ("pca", "PCA directions (same size)", "PCA directions (same size)"),
           ("wu", "logit-lens directions", "logit-lens directions"),
           ("rand", "random lens directions", "random lens directions"))  # fmt: skip


def fig02_specificity() -> sp.Figure:
    """Per model and part of the same size, the recall's and the lookup's extra loss; the part's share of the
    change beside (the parts runs: after the data)."""
    return _parts("fig02", "fig02_specificity", PARTS02, share=True)


PARTS05B = (("jpp", "J++ part", "lens part"),
            ("d26", "47.1: {}'s extra loss without directions 26-100 (main test)", "lens directions 26–100"),
            *PARTS02[1:])  # fmt: skip


def fig05b_identity_outside() -> sp.Figure:
    """The extra loss without the J++ part, without the lens directions 26-100 (47.1, fixed in advance), and without
    parts of the same size (after the data)."""
    return _parts("fig05b", "fig05b_identity_outside", PARTS05B, share=False)


# ---- fig05c: the described bridge ---------------------------------------------------------------------------------------
def fig05c_described_bridge() -> sp.Figure:
    """47.3 (fixed in advance): with the bridge described, not named: the extra loss without the J++ part, its gap,
    and the position answers lost without the label-free pointer beyond random; Lightning below its gate."""
    q = "47.3: {}'s extra loss without the J++ part"
    models = [m for m in DAN if cell("fig05c", m, q.format("recall")) or D.s_match(m, r"47\.3: status", "fig05c")]
    lk, rc, gap, pos = {}, {}, {}, {}
    for m in models:
        k = ZK[m]
        if not cell("fig05c", m, q.format("recall")):
            lk[m] = sp.Missing("below gate")
            continue
        lk[m] = est(cell("fig05c", m, q.format("lookup")), f"described.{k}", key=f"f05c.lookup.{k}")
        rc[m] = est(cell("fig05c", m, q.format("recall")), f"described.{k}", key=f"f05c.recall.{k}")
        gap[m] = est(cell("fig05c", m, "47.3: gap (recall's extra loss minus the lookup's)"), f"described.{k}",
                     key=f"f05c.gap.{k}", label=True)  # fmt: skip
        p = cell(
            "fig05c", m, "47.3: position answers lost without the label-free pointer beyond random (held-out half)"
        )
        if p:
            pos[m] = est(p, f"described.{k}", key=f"f05c.position.{k}", label=True)
    cols = [reader_column("without the lens part", "switches", (-0.2, 0.75), (0, 0.25, 0.5), {"lookup": lk, "recall": rc}),
            sp.DotColumn("gap: recall − lookup", "gap_share", (-0.1, 0.7), (0, 0.25, 0.5),
                         series=[sp.Series("neutral", gap)]),
            sp.DotColumn("position answers cut", "position_lost", (-0.02, 0.32), (0, 0.1, 0.2),
                         series=[sp.Series("address", pos)])]  # fmt: skip
    return sp.Figure("fig05c_described_bridge", vocab()).add(sp.DotTable(models, cols))


# ---- fig07c: the probe's errors ----------------------------------------------------------------------------------------
def fig07c_probe_errors() -> sp.Figure:
    """47.13 (fixed in advance): of the wrong answers, the share whose locker the address probe predicts, against the
    most common locker (grey) and chance; the most common locker given the layout and the lens's top item beside.
    Its verdict panel is not drawn (Dan, 7 Nov)."""
    q = "47.13: wrong answers whose locker the {} predicts"
    models = models_with("fig07c", [q.format("address probe")])
    probe, common, layout, lens, chance = {}, {}, {}, {}, []
    for m in models:
        k = ZK[m]
        probe[m] = est(cell("fig07c", m, q.format("address probe")), f"errors.{k}", key=f"f07c.probe.{k}", label=True)
        common[m] = est(cell("fig07c", m, q.format("most common locker")), f"errors.{k}", key=f"f07c.common.{k}",
                        interval=False)  # fmt: skip
        lay = cell("fig07c", m, q.format("most common locker given the layout"))
        layout[m] = est(lay, f"errors.{k}", key=f"f07c.layout.{k}") if lay else sp.Missing("no run")
        top = cell("fig07c", m, "47.13: lens's top item still right, matched wrong answers")
        lens[m] = est(top, f"errors.{k}", key=f"f07c.lens.{k}") if top else sp.Missing("no run")
        ch = cell("fig07c", m, "47.13: chance (1 / lockers)")
        if ch:
            chance.append(ch[0])
    dots = sp.DotColumn("wrong answers' locker predicted", "wrong", (-0.02, 0.45), (0, 0.2, 0.4),
                        series=[sp.Series("control", common, control="most common locker"),
                                sp.Series("address", probe)],
                        rules=[sp.Rule(max(chance), "chance")])  # fmt: skip
    t = sp.DotTable(models, [dots, sp.TextColumn("given the layout", "wrong", layout, unit_title=False),
                             sp.TextColumn("lens's top item right", "wrong", lens, unit_title=False)])  # fmt: skip
    return sp.Figure("fig07c_probe_errors", vocab()).add(t)


# ---- fig09d: the hall chain --------------------------------------------------------------------------------------------
def fig09d_chain() -> sp.Figure:
    """47.14 (fixed in advance): the hall probe at the locker digit against its layout baseline; the hall answers by
    position without the hall address and with only it kept, each against a random part of the same size (grey);
    the whole change's share beside. Lightning not tested."""
    q = "47.14: hall answers by position, {}"
    models = [
        m
        for m in DAN
        if cell("fig09d", m, q.format("the whole change"))
        or cell("fig09d", m, "47.14: the gate's lowest read accuracy on the original prompts")
    ]  # gated, not tested
    cols = []
    probe, base = {}, {}
    for m in models:
        k = ZK[m]
        p = cell("fig09d", m, "47.14: hall probe at the locker digit")
        if not p:
            probe[m] = sp.Missing("not tested")
            continue
        probe[m] = est(p, f"hall.{k}", key=f"f09d.probe.{k}", label=True)
        base[m] = est(cell("fig09d", m, "47.14: hall probe's layout baseline"), f"hall.{k}", key=f"f09d.layout.{k}",
                      interval=False)  # fmt: skip
    cols.append(sp.DotColumn("hall probe", "probe_accuracy", (0, 1.05), (0, 0.5, 1),
                             series=[sp.Series("control", base, control="layout-only probe"),
                                     sp.Series("address", probe)]))  # fmt: skip
    whole = {}
    for header, arm, rand in (("without the hall address", "without the hall address",
                               "without a random part (same size)"),
                              ("only the hall address kept", "only the hall address kept",
                               "only a random part (same size) kept")):  # fmt: skip
        a, r = {}, {}
        for m in models:
            k = ZK[m]
            c = cell("fig09d", m, q.format(arm))
            if not c:
                a[m] = sp.Missing("not tested")
                continue
            a[m] = est(c, f"hall.{k}", key=f"f09d.{arm}.{k}", label=True)
            r[m] = est(cell("fig09d", m, q.format(rand)), f"hall.{k}", key=f"f09d.{rand}.{k}", interval=False)
        cols.append(
            sp.DotColumn(
                header,
                "hall",
                (-0.03, 0.6),
                (0, 0.25, 0.5),
                series=[sp.Series("control", r, control="a random part"), sp.Series("address", a)],
            )
        )
    for m in models:
        c = cell("fig09d", m, q.format("the whole change"))
        if c:
            whole[m] = est(c, f"hall.{ZK[m]}", key=f"f09d.whole.{ZK[m]}")
    cols.append(sp.TextColumn("the whole change", "hall", whole, unit_title=False))
    return sp.Figure("fig09d_chain", vocab()).add(sp.DotTable(models, cols))


FIGS = {**{fid: _alias(fid) for fid in ALIAS}, "fig01b_settings": fig01b_settings, "fig01c_zeroing": fig01c_zeroing,
        "fig02_specificity": fig02_specificity, "fig05b_identity_outside": fig05b_identity_outside,
        "fig05c_described_bridge": fig05c_described_bridge, "fig07c_probe_errors": fig07c_probe_errors,
        "fig09d_chain": fig09d_chain}  # fmt: skip


def build(ids=None) -> list[str]:
    return RS.build(ids, figs=FIGS, dirs={fid: path(fid).parent for fid in FIGS})


if __name__ == "__main__":
    sys.exit(1 if build(sys.argv[1:] or None) else 0)
