"""The depth README's sweeps on styles-plot (readme target): quantities over the depth, x the layer as a share of the
model's depth. Two lines of one role are named by words at their ends; a gate is a named grey window over the layers
that pass it, never a faded line (Dan, 7 Nov); the points fixed in advance carry their own whiskers. Numbers are the
rows the story builders recorded in data/figures/depth/data.csv. depth_sp.FIGS includes these.
"""

from __future__ import annotations

import re
from itertools import pairwise

import styles_plot as sp

from bridge_jspace.figkit import curve_figs as CV
from bridge_jspace.figkit import data as D
from bridge_jspace.figkit.writeup_sp_base import ZK, est, need, vocab

DAN = [m for m, _ in D.DAN]


def layers(m: str, fig: str, pattern: str) -> list[int]:
    return CV._layers(m, fig, pattern)


def line(m, fig, q, role, cell, word=None, control=None):
    """A line over the layers a quantity was read at, with its interval band when the rows carry one."""
    las = layers(m, fig, "^" + re.escape(q).replace(r"\{\}", r"(\d+)") + "$")
    v = [need(D.s(m, q.format(la), fig), f"{fig} {m} {la}") for la in las]
    band = ([t[1] for t in v], [t[2] for t in v]) if all(t[1] is not None for t in v) else None
    return sp.Line(m, role, [la / CV.DEPTH[m] for la in las], [t[0] for t in v], cell=cell, band=band, word=word,
                   control=control)  # fmt: skip


def windows(m: str, fig: str, q: str, threshold: float) -> list[tuple[float, float, str]]:
    """The runs of consecutive read layers whose value passes the threshold, as grey x-windows (layer share)."""
    las = layers(m, fig, "^" + re.escape(q).replace(r"\{\}", r"(\d+)") + "$")
    ok = [la for la in las if need(D.s(m, q.format(la), fig), q)[0] >= threshold]
    out, run = [], []
    for la in las:
        if la in ok:
            run.append(la)
        elif run:
            out.append(run)
            run = []
    if run:
        out.append(run)
    step = min((b - a for a, b in pairwise(las)), default=1) / 2
    return [((r[0] - step) / CV.DEPTH[m], (r[-1] + step) / CV.DEPTH[m], "gate") for r in out]


XLIM, XTICKS = (-0.04, 1.03), (0, 0.5, 1)  # the depth axis of every sweep


# ---- fig03b: the copy at every locker-sentence token, by layer (45q) ---------------------------------------------------
Q45 = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
BW = "45q, layer {}: the bridge-word change (lookups switched)"


def _arm_points(m, fig, arms):
    L, half = (need(D.s(m, f"45q: {q}", "fig03"), q)[0] for q in ("L, the rule's layer", "L/2, the rule's half layer"))
    pts = []
    for arm, what, which in arms:
        r = need(D.s(m, f"45q, the rule's arm {arm}: {what} (lookups switched)", fig), f"{m} {arm}")
        x = (L if which == "L" else half) / CV.DEPTH[m]
        pts.append((arm, sp.Point(m, "lookup", x, cell=f"arm.{arm}.{ZK[m]}", value=r[0], lo=r[1], hi=r[2]), r))
    return pts


ARMS = (("a", "the bridge-word change at L", "L"), ("c", "copy at L, every locker-sentence token", "L"),
        ("d", "copy at L/2, every locker-sentence token", "L/2"))  # fmt: skip
ARM_HEADER = {"a": "at the bridge word, at L", "c": "copied, at L", "d": "copied, at L/2"}


def fig03b_layers() -> sp.Figure:
    """45q, by depth: the lookups switched by the change at the bridge word and by the same change copied at every
    locker-sentence token (two lookup lines), the three cells fixed in advance as points with their whiskers, and in
    the table the copy at L's share of the changed prompt's lookup switches (the rule's quantity)."""
    f = "fig03b"
    lines, points, vals, share = [], [], {a: {} for a, *_ in ARMS}, {}
    for m in Q45:
        k = ZK[m]
        lines.append(line(m, f, BW, "lookup", f"sweep.bridge.{k}", word="at the bridge word"))
        lines.append(line(m, f, "45q, layer {}: copy at every locker-sentence token (lookups switched)", "lookup",
                          f"sweep.copy.{k}", word="copied at every locker-sentence token"))  # fmt: skip
        for arm, p, r in _arm_points(m, f, ARMS):
            points.append(p)
            vals[arm][m] = est(r, f"arm.{arm}.{k}", key=f"f03b.{arm}.{k}")
        s = need(D.s(m, "45q, the rule: copy at L's share of the changed prompt's lookup switches", f), m)
        share[m] = est(s, f"arm.c.{k}", key=f"f03b.share.{k}")
    sweep = sp.Sweep(list(Q45), "depth_share", "lookups_switched", lines, points=points, panel_h=1.0,
                     ylim=(-0.04, 1.1), yticks=(0, 0.5, 1), xlim=XLIM, xticks=XTICKS)  # fmt: skip
    cols = [sp.TextColumn(ARM_HEADER[a], "lookups_switched", vals[a], unit_title=False) for a, *_ in ARMS]
    cols.append(sp.TextColumn("copy at L's share of the switches", "change_share", share, unit_title=False))
    return sp.Figure("fig03b_layers", vocab()).add(sweep, sp.DotTable(list(Q45), cols))


# ---- s03d: which tokens of the locker sentences carry the copy (45q) ----------------------------------------------------
S03D = (("every", "copy at every locker-sentence token", "every locker-sentence token"),
        ("item", "copy at the item's own tokens", "the item's own tokens"),
        ("rest", "copy at the other locker-sentence tokens", "the other locker-sentence tokens"),
        ("number", "copy at the number only", "the number only"),
        ("period", "copy at the period only", "the period only"))  # fmt: skip


def s03d_link_copy_variants() -> sp.Figure:
    """45q, by depth: the lookups switched when the change is copied at every locker-sentence token, at the item's
    own tokens, at the other tokens, at the number only and at the period only (five lookup lines named at their
    ends); at L, the copy without the lens part against without a random part of the same size (grey)."""
    f = "s03d"
    lines = [line(m, f, f"45q, layer {{}}: {q} (lookups switched)", "lookup", f"sweep.{key}.{ZK[m]}", word=w)
             for m in Q45 for key, q, w in S03D]  # fmt: skip
    sweep = sp.Sweep(list(Q45), "depth_share", "lookups_switched", lines, panel_h=1.2, ylim=(-0.04, 1.1),
                     yticks=(0, 0.5, 1), xlim=XLIM, xticks=XTICKS)  # fmt: skip
    at = {}
    for key, q in (("c", "the rule's arm c: copy at L, every locker-sentence token"),
                   ("nolens", "copy at L without the J++ part"), ("rand", "copy at L without a random part (same size)")):  # fmt: skip
        at[key] = {m: est(c, f"arm.c.{ZK[m]}", key=f"s03d.{key}.{ZK[m]}", label=True)
                   for m in Q45 if (c := D.s(m, f"45q, {q} (lookups switched)", f))}  # fmt: skip
    cols = [sp.DotColumn("copied, at L", "lookups_switched", (-0.04, 1.1), (0, 0.5, 1), series=[sp.Series("lookup", at["c"])]),
            sp.DotColumn("without the lens part", "lookups_switched", (-0.04, 1.1), (0, 0.5, 1),
                         series=[sp.Series("lens", at["nolens"])]),
            sp.DotColumn("without a random part", "lookups_switched", (-0.04, 1.1), (0, 0.5, 1),
                         series=[sp.Series("control", at["rand"], control="a random part")])]  # fmt: skip
    return sp.Figure("s03d_link_copy_variants", vocab()).add(sweep, sp.DotTable(list(Q45), cols))


# ---- fig06_depth: when, by depth (47.8) --------------------------------------------------------------------------------
F06 = "47.8, layer {}: "


def _fig06(fid: str, keep) -> sp.Figure:
    """47.8, by depth: the locker probe's accuracy and the position answers under the whole change when another item
    moves (two address lines), and the lookup's switches blocked without the lens part beyond a random part of the same
    size (the lens part's colour); grey windows: the layers that pass the gate (the whole change switches at least
    0.30 of the lookups: curve_figs.GATE). The recall is not part of claim 12 and is not drawn."""
    f = "fig06"
    models = [m for m in DAN if m in keep and layers(m, f, r"47\.8, layer (\d+): the locker probe's accuracy")]
    lines, wins = [], []
    for m in models:
        k = ZK[m]
        lines += [line(m, f, F06 + "the locker probe's accuracy", "address", f"depth.{k}", word="the locker probe"),
                  line(m, f, F06 + "position answers under the whole change", "address", f"depth.{k}",
                       word="position answers"),
                  line(m, f, F06 + "lookup: switches blocked beyond random without the J++ part", "lens",
                       f"depth.{k}")]  # fmt: skip
        wins.append((m, windows(m, f, F06 + "lookup switches under the whole change", CV.GATE)))
    figs = sp.Figure(fid, vocab())
    for m, w in wins:
        own = [ln for ln in lines if ln.row == m]
        lo = min(min(ln.y) for ln in own)
        lo = min(lo, *(min(ln.band[0]) for ln in own if ln.band))
        deep = lo < -0.5  # outside the gate an interval can run far below 0 (Lightning): every value is drawn
        figs.add(sp.Sweep([m], "depth_share", "depth_share_y", own, windows=w, panel_h=1.5 if deep else 0.9,
                          ylim=(min(-0.04, lo - 0.03), 1.1), yticks=(round(lo), 0, 1) if deep else (0, 0.5, 1),
                          xlim=XLIM, xticks=XTICKS))  # fmt: skip
    return figs


# one gate window per model needs its own sweep block (a Sweep's windows hold for every row): too tall as one figure
def fig06_depth() -> sp.Figure:
    """47.8 by depth on the three models whose gate was fixed in advance (see _fig06)."""
    return _fig06("fig06_depth", ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b"))


def fig06d_depth_more() -> sp.Figure:
    """47.8 by depth on Lightning and the 122B, whose gates were chosen after the data (see _fig06)."""
    return _fig06("fig06d_depth_more", ("nemotron-3.5-lightning", "qwen3.5-122b-a10b"))


# ---- fig06c: the address across depth (D4) ------------------------------------------------------------------------------
def fig06c_address_depth() -> sp.Figure:
    """D4: the address's overlap (mean cos²) between neighbouring windows of layers, over the depth
    (x: the middle of the two windows), per model; the mean over every pair of window layers in the table."""
    f = "fig06c"
    q = "D4: the address's overlap (mean cos^2), layers "
    models = [m for m in DAN if any(fi == f and mo == m for fi, mo, _ in D.story())]
    lines, mean = [], {}
    for m in models:
        pts = sorted(((int(a) + int(b)) / 2, v[0]) for (fi, mo, qq), v in D.story().items()
                     if fi == f and mo == m and (g := re.match(re.escape(q) + r"(\d+)-(\d+)$", qq))
                     for a, b in [g.groups()])  # fmt: skip
        lines.append(
            sp.Line(m, "address", [x / CV.DEPTH[m] for x, _ in pts], [y for _, y in pts], cell=f"overlap.{ZK[m]}")
        )
        c = need(D.s(m, "D4: the address's mean overlap over every pair of window layers", f), m)
        mean[m] = est(c, f"overlap.{ZK[m]}", key=f"f06c.mean.{ZK[m]}")
    # ticks at 0 and 0.5 only: a 1 on one panel touches the 0 of the panel under it (library spacing, reported)
    sweep = sp.Sweep(
        models, "depth_share", "overlap", lines, panel_h=1.0, ylim=(0, 1.0), yticks=(0, 0.5), xlim=XLIM, xticks=XTICKS
    )
    table = sp.DotTable(models, [sp.TextColumn("mean overlap, every pair of window layers", "overlap", mean,
                                               unit_title=False)])  # fmt: skip
    return sp.Figure("fig06c_address_depth", vocab()).add(sweep, table)


# ---- fig10b: enrichment (48.2) -----------------------------------------------------------------------------------------
F10B_A = "48.2 A, layer {}: probe moved toward the changed item, "
F10B_B = (("bridge_late", "the bridge word, late layers"), ("person_late", "the person word, late layers"),
          ("bridge_early", "the bridge word, early layers"))  # fmt: skip


def fig10b_enrichment() -> sp.Figure:
    """48.2, fixed in advance. (A) By depth: how far the attribute probe moves from the original item's attribute toward
    the changed item's under the whole change and without the lens part, and without a random
    part of the same size (grey), and the probe's held-out accuracy: lines of no role, named at their ends. (B) The accuracy drop when MLP
    writes are replaced by their mean, per reader, at the bridge word late and early and at the person word late."""
    f = "fig10b"
    models = [m for m in DAN if layers(m, f, r"48\.2 A, layer (\d+): probe moved")]
    lines = []
    for m in models:
        k = ZK[m]
        lines += [line(m, f, F10B_A + "whole change", "neutral", f"enrich.{k}", word="the whole change"),
                  line(m, f, F10B_A + "without the J++ part", "neutral", f"enrich.{k}", word="without the lens part"),
                  line(m, f, F10B_A + "without a random part (same size)", "control", f"enrich.{k}",
                       control="a random part"),
                  line(m, f, "48.2 A, layer {}: probe held-out accuracy at the bridge token", "neutral", f"enrich.{k}",
                       word="probe accuracy")]  # fmt: skip
    sweep = sp.Sweep(models, "depth_share", "probe_moved", lines, panel_h=1.1, ylim=(-0.1, 1.05), yticks=(0, 0.5, 1),
                     xlim=XLIM, xticks=XTICKS)  # fmt: skip
    cols = []
    for key, header in F10B_B:
        series = [sp.Series(reader, {m: est(c, f"enrich.{ZK[m]}", key=f"f10b.{key}.{reader}.{ZK[m]}")
                                     for m in models if (c := D.s(m, f"48.2 B, {key}: {reader} accuracy lost", f))})
                  for reader in ("lookup", "recall")]  # fmt: skip
        cols.append(sp.DotColumn(header, "accuracy_drop_share", (-0.1, 1.0), (0, 0.5, 1), series=series))
    return sp.Figure("fig10b_enrichment", vocab()).add(
        sweep, sp.DotTable(models, cols, note="MLP outputs replaced by their mean")
    )


# ---- the depth README's schematics, laid out from the readme target's width ---------------------------------------------
def _w(text: str, bold: bool = False) -> float:
    from bridge_jspace.figkit.writeup_sp_b import _width

    return _width(text, bold)


SCENES = (("original prompt", None, "oxygen", "carbon"), ("changed prompt", "the two picks swap", "carbon", "oxygen"),
          ("original prompt + Δ", None, "oxygen", "carbon"))  # fmt: skip


def fig00_setup() -> sp.Figure:
    """The setup: the original prompt, the changed prompt (the two picks swap), and the original prompt with Δ added
    at the bridge word at one layer (Δ: the bridge word's state in the changed prompt minus the original's); both
    questions read the same patched state: the lookup's answer moves in the prompt, the recall's from memory."""
    W = vocab().target("readme").width_in
    x_box, line_h, box_h, gap = 2.6, 0.32, 1.12, 0.3
    lines = ("The locker of carbon is 3. The locker of helium is 5.", "The locker of oxygen is 7. Hugo picked {h}. Eric picked ",
             "Eva picked helium.")  # fmt: skip
    box_w = max(_w(lines[0]), _w(lines[1].format(h="carbon")) + _w("oxygen", True) + _w(".")) + 0.4
    dx = x_box + box_w + 0.9  # the Δ box
    el: list = []
    ends = []
    for i, (label, sub, hugo, eric) in enumerate(SCENES):
        y = 0.25 + i * (box_h + gap)
        el += [sp.Words(0.15, y + 0.3, [(label, None)], bold=True), sp.Box(x_box, y, box_w, box_h)]
        if sub:
            el.append(sp.Words(0.15, y + 0.62, [(sub, None)]))
        first = lines[1].format(h=hugo)
        el += [sp.Words(x_box + 0.15, y + 0.25, [(lines[0], None, False)], verbatim=True),
               sp.Words(x_box + 0.15, y + 0.25 + line_h, [(first, None, False), (eric, None, True), (".", None, False)],
                        verbatim=True),
               sp.Words(x_box + 0.15, y + 0.25 + 2 * line_h, [(lines[2], None, False)], verbatim=True)]  # fmt: skip
        ends.append((x_box + box_w, y + 0.25 + line_h))
    dy = (ends[0][1] + ends[1][1]) / 2
    el += [sp.Box(dx, dy - 0.25, 0.5, 0.5, "Δ", verbatim=True),
           sp.Arrow((ends[0][0] + 0.1, ends[0][1]), (dx, dy - 0.1)), sp.Arrow((ends[1][0] + 0.1, ends[1][1]), (dx, dy + 0.1)),
           sp.Arrow((dx + 0.25, dy + 0.25), (dx + 0.25, ends[2][1])),
           sp.Arrow((dx + 0.25, ends[2][1]), (ends[2][0] + 0.1, ends[2][1])),
           sp.Words(ends[2][0] + 0.15, ends[2][1] + 0.3, [("added at one layer", None)])]  # fmt: skip
    y = 0.25 + 3 * (box_h + gap) - 0.1
    xa = W - 2.6  # the answers' column
    el += [sp.Words(x_box, y, [("both questions read this same patched state", None)]),
           sp.Words(xa, y, [("original → after the patch", None)])]  # fmt: skip
    for j, (role, q, a, src) in enumerate((("lookup", "Which locker belongs to Eric's pick?", "3 → 7", "in the prompt"),
                                           ("recall", "What is the atomic number of Eric's pick?", "6 → 8", "from memory"))):  # fmt: skip
        yy = y + 0.45 + j * 0.4
        el += [sp.Words(0.15, yy, [(role, role)], bold=True), sp.Words(x_box, yy, [(q, None)], verbatim=True),
               sp.Words(xa, yy, [(a, role, True), ("   " + src, role, False)], verbatim=True)]  # fmt: skip
    el.append(
        sp.Words(
            0.15,
            y + 1.35,
            [("Δ: the bridge word's state in the changed prompt minus the original's, at one layer", None)],
        )
    )
    return sp.Figure("fig00_setup", vocab(), direct_labels=True).add(sp.Schematic(y + 1.6, el))


def s04_routes_design() -> sp.Figure:
    """Each route predicts a different locker: on the original prompt the original answer, the position route's
    locker (now at the item's old place) and the identity route's (the item's own); on the changed prompt the moved
    sentence carries the value (a new number at helium's place)."""
    bw, bh, x0, gap = 1.9, 0.5, 2.9, 0.12
    cols = ((None, "the original answer"), ("address", "position route"), ("identity", "identity route"))
    rows = (("original prompt", ("carbon: 3", "helium: 5", "oxygen: 7"), "Eric picked carbon."),
            ("changed prompt", ("carbon: 3", "oxygen: 4", "helium: 5"), "Eric picked oxygen."))  # fmt: skip
    el: list = []
    for j, (role, word) in enumerate(cols):
        el.append(sp.Words(x0 + j * (bw + gap) + 0.15, 0.35, [(word, role)], bold=True))
    for i, (label, cells, pick) in enumerate(rows):
        y = 0.75 + i * 1.35
        el.append(sp.Words(0.2, y + bh / 2, [(label, None)], bold=True))
        for j, text in enumerate(cells):
            role = cols[j][0] if i == 0 else ("neutral" if j == 1 else None)
            el.append(sp.Box(x0 + j * (bw + gap), y, bw, bh, text, role=role, verbatim=True))
        el.append(sp.Words(x0 + 2 * (bw + gap), y + bh + 0.28, [(pick, None)], verbatim=True))
    el += [sp.Words(x0 + (bw + gap) + 0.15, 0.75 + 1.35 + bh + 0.3, [("value", "neutral")], bold=True),
           sp.Words(0.2, 3.25, [("identity route: the item's own locker; position route: the locker now at the item's old "
                                 "place; value: the new number", None)])]  # fmt: skip
    return sp.Figure("s04_routes_design", vocab(), direct_labels=True).add(sp.Schematic(3.55, el))


FIGS = {"fig03b_layers": fig03b_layers, "s03d_link_copy_variants": s03d_link_copy_variants,
        "fig06_depth": fig06_depth, "fig06d_depth_more": fig06d_depth_more, "fig06c_address_depth": fig06c_address_depth, "fig10b_enrichment": fig10b_enrichment, "fig00_setup": fig00_setup, "s04_routes_design": s04_routes_design}  # fmt: skip
SUPP = {"s03d_link_copy_variants", "s04_routes_design"}
