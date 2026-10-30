"""Five reference figures in the dot-table style, from the repo's own data (figkit.data). Run from the repo root:
PYTHONPATH=src:/home/claude/figref python3 /home/claude/figref/exemplars.py OUTDIR"""

from __future__ import annotations

import re

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit.dottable import BAND, INK, MUTED, C, Col, Row, Table, band, connector, dot, head_label, vrule

OUT = "."  # set by bridge_jspace.figkit.tables
DAN = D.DAN
ZK = {"qwen3.5-9b": "q9", "qwen3.6-27b": "q27", "muse-glimmer-30b": "mu", "nemotron-3.5-lightning": "nl",
      "qwen3.5-122b-a10b": "q122"}  # fmt: skip
NAME = {m: n.replace(" ○", "") for m, n in DAN}


# ---- R1: C1, two tools, one table ---------------------------------------------------------------------------------
def r1_split():
    rows = [Row(NAME[m]) for m, _ in DAN]
    z_hollow = {"mu", "q122"}  # Zach: post hoc

    def zach(ax, _rows):
        for i, (m, _) in enumerate(DAN):
            k = ZK[m]
            rc, lk = D.b(f"ko.{k}.lostM")[0], D.b(f"ko.{k}.lostK")[0]
            h = k in z_hollow
            connector(ax, lk, rc, i)
            dot(ax, lk, i, C["lookup"], h)
            dot(ax, rc, i, C["recall"], h)
        head_label(ax, D.b("ko.q9.lostK")[0], "lookup", C["lookup"])
        head_label(ax, D.b("ko.q9.lostM")[0], "recall", C["recall"])

    def zach_nums(i, _r):
        k = ZK[DAN[i][0]]
        mk, lo, hi = D.b(f"ko.{k}.mk")  # the gap's 95% interval, the same "[lo, hi]" as the right half's (Dan 30 Oct)
        return [(f"{mk:.0f}", INK, "bold"), (f"  [{lo:.0f}, {hi:.0f}]", MUTED, "normal"),
                (f"  ({S.ctrl(k):.0f})", MUTED, "normal")]

    t = Table(rows, [
        Col(3.0, "Remove everywhere", "answers that turn wrong", zach, (-4, 70), [0, 20, 40, 60], xlabel="points",
            cue="→ lens part needed more"),
        Col(2.25, "gap", "recall − lookup, 95%", zach_nums, text=True),
        *dan_split_cols(),
    ], label_w=1.45, key=[("(n)", MUTED, "the largest same-size control's gap (rotated, logit lens or PCA)"),
                          ("■", BAND, "within 0.10 of a random part")])  # fmt: skip
    t.render(f"{OUT}/r1_c1_split.png")


def dan_split_cols(title="Remove from the patch"):
    """r1's right half: the conflict test's lookup and recall, and the gap with its interval."""

    def dan(ax, _rows):
        n = len(DAN)
        band(ax, -0.1, 0.1, n)
        for i, (m, _) in enumerate(DAN):
            rc, lk = S.conflict(m, "recall"), S.conflict(m, "lookup")
            h = D.hollow(m)
            connector(ax, lk[0], rc[0], i)
            dot(ax, lk[0], i, C["lookup"], h, cell=lk)
            dot(ax, rc[0], i, C["recall"], h, cell=rc)
        head_label(ax, S.conflict("qwen3.5-9b", "lookup")[0], "lookup", C["lookup"])
        head_label(ax, S.conflict("qwen3.5-9b", "recall")[0], "recall", C["recall"])

    def dan_nums(i, _r):
        m = DAN[i][0]
        g = D.x(f"contrast_{D.SHORT.get(m, '-')}")
        if g:
            return [(f"{g[0]:.2f}", INK, "bold"), (f"  [{g[1]:.2f}, {g[2]:.2f}]", MUTED, "normal")]
        rc, lk = S.conflict(m, "recall")[0], S.conflict(m, "lookup")[0]
        return [
            (f"{rc - lk:.2f}", INK, "bold"),
            ("  no interval (aggregate only)", MUTED, "normal"),
        ]  # a paired interval was not computed

    return [Col(3.0, title, "switches lost beyond a random part", dan, (-0.25, 1.0), [0, 0.5, 1.0],
                xlabel="share of switches",
                cue="→ depends more on lens part"),
            Col(3.5, "gap", "recall − lookup, 95%", dan_nums, text=True)]  # fmt: skip


def r1_dan_split():
    """The depth README's Fig. 1: r1's right half alone (the 01:58 brief)."""
    Table(
        [Row(NAME[m]) for m, _ in DAN],
        dan_split_cols("Remove from the patch"),
        label_w=1.45,
        key=[("■", BAND, "within 0.10 of a random part")],
    ).render(f"{OUT}/r1_dan_split.png")


# ---- R3: C4, readable vs used at the last token ---------------------------------------------------------------------
def r3_last_token():
    rx_r = r"51\.10: recall, last token, read peak layer (\d+): the probe's accuracy"
    rows, cells = [], []
    for m, _ in DAN:
        r = D.s_match(m, rx_r, "fig17_jspace_last_token")
        if not r:
            continue
        sw = D.s_match(
            m,
            r"51\.10: recall, last token, read peak layer \d+: the lens swap's switches over",
            "fig17_jspace_last_token",
        )
        mm = re.search(r"\(([\d.]+) / ([\d.]+)\)", sw[0])
        lens_abs, whole = float(mm.group(1)), float(mm.group(2))
        layer = re.search(r"layer (\d+)", r[0]).group(1)
        chance = D.s(m, "51.10: the read probe's chance (locker-first rows)")[0]
        rows.append(Row(NAME[m], sub=f"layer {layer}"))
        cells.append((m, r[1], lens_abs, whole, chance))

    def read(ax, _rows):
        ch = max(c[4] for c in cells)
        vrule(ax, ch, len(cells), "chance")
        for i, (m, rd, *_r) in enumerate(cells):
            dot(ax, rd[0], i, C["recall"], D.hollow(m), cell=rd, value=rd[0], vside="left")
        head_label(ax, 0.97, "probe on the lens part", C["recall"], ha="right")

    def used(ax, _rows):
        for i, (m, _rd, la, wh, _c) in enumerate(cells):
            connector(ax, la, wh, i)
            dot(ax, wh, i, C["control"], size=8, value=None)
            dot(ax, la, i, C["lens"], D.hollow(m), value=la, vside="left")
        head_label(ax, -0.2, "lens part written in", C["lens"], ha="left")
        head_label(ax, 0.97, "whole state", MUTED, ha="right", weight="normal")

    t = Table(rows, [
        Col(3.6, "probe accuracy on the lens part", "the recall's entity, at the last token", read, (0, 1.02),
            [0, 0.5, 1.0], xlabel="accuracy", cue="→ more readable"),
        Col(3.6, "recalls switched", "lens part written in, against the whole state", used, (-0.25, 1.02),
            [0, 0.5, 1.0], xlabel="share of recalls switched", cue="→ used more"),
    ], label_w=1.6)  # fmt: skip
    t.render(f"{OUT}/r3_last_token.png")


# ---- R4: Zach's pointer, conditions as rows, models as columns -----------------------------------------------------
def r4_pointer():
    conds = [("another entity D's own passage", "lens"), ("one neutral sentence about D", "lens"),
             ("without D's own-word directions", "lens"), ("rotated (control)", "control"),
             ("a probe's subspace (reads the fact)", "neutral")]  # fmt: skip
    rows = [Row(c) for c, _ in conds]
    models = [("q9", "Qwen 9B"), ("q27", "Qwen 27B"), ("nl", "Lightning")]

    def cells(k):
        # every row in points with its 95% interval (scripts/ptr_intervals.py recomputes rows 2-5 from the runs' per-item rows)
        return [D.b(f"ptr.{k}.swap"), D.b(f"ptr.{k}.neutral_pts"), D.b(f"ptr.{k}.noown_pts"), D.b(f"ptr.{k}.rot_pts"),
                D.b(f"probe.{k}.probe_pts")]  # fmt: skip

    def panel(k):
        def f(ax, _rows):
            for i, (cell, (_, col)) in enumerate(zip(cells(k), conds, strict=True)):
                dot(ax, cell[0], i, C[col], cell=cell, value=cell[0], vfmt="{:.0f}")

        return f

    t = Table(rows, [Col(2.35, n, "answers moved to D's fact" if j == 0 else "", panel(k), (-8, 92), [0, 40, 80],
                         xlabel="points", cue="→ more answers follow D") for j, (k, n) in enumerate(models)], label_w=3.55, labels=False)  # fmt: skip
    t.render(f"{OUT}/r4_pointer.png")


# ---- R5: routes, 100% stacked as rows -------------------------------------------------------------------------------
def r5_routes():
    models = [(m, n) for m, n in DAN if D.s(m, "another item moved, whole: identity share")]
    rows = [Row(NAME[m]) for m, _ in models]

    def stack(ax, _rows):
        for i, (m, _) in enumerate(models):
            idn = D.s(m, "another item moved, whole: identity share")[0]
            pos = D.s(m, "another item moved, whole: position share")[0]
            hol = D.hollow(m, True)  # post hoc: hollow bars (G1), not a tint
            ids, ps = (
                D.s(m, "another item moved, whole: identity share"),
                D.s(m, "another item moved, whole: position share"),
            )
            for left, v, col in (
                (0, idn, C["identity"]),
                (idn, pos, C["address"]),
                (idn + pos, 1 - idn - pos, C["other"]),
            ):
                kw = (
                    {"facecolor": "white", "edgecolor": col if col != C["other"] else C["control"], "linewidth": 2.2}
                    if hol
                    else {"color": col}
                )
                ax.barh(i, v, left=left, height=0.62, zorder=3, **kw)
            tc = INK if hol else "white"
            ax.text(idn / 2, i, f"{idn:.2f}", ha="center", va="center", fontsize=12, color=tc, weight="bold", zorder=4)
            ax.text(
                idn + pos / 2, i, f"{pos:.2f}", ha="center", va="center", fontsize=12, color=tc, weight="bold", zorder=4
            )
            for (_v, lo, hi), x0 in ((ids, 0.0), (ps, idn)):  # 95% intervals: thin whiskers under each segment (G7)
                if lo is not None:
                    ax.plot([x0 + lo, x0 + hi], [i + 0.42] * 2, color=INK, lw=1.2, zorder=5)
                    for e in (x0 + lo, x0 + hi):  # end caps
                        ax.plot([e, e], [i + 0.37, i + 0.47], color=INK, lw=1.2, zorder=5)
        head_label(ax, 0.0, "by identity", C["identity"], ha="left")
        head_label(ax, 0.5, "by position", C["address"], ha="center")

    def value(i, _r):
        v = D.s(models[i][0], "another item moved, whole: value share")[0]
        return [(f"{v:.2f}", INK, "bold")]

    t = Table(rows, [Col(6.6, "share of the lookup's answers", "identity: the item's own locker · position: the locker now at its old place", stack,
                         (0, 1), [0, 0.5, 1], xlabel="share of the lookup's answers", cue="→ larger share"),
                     Col(1.3, "the number", "itself", value, text=True)], label_w=1.45,
              key=[("●", C["other"], "other")])  # fmt: skip
    t.render(f"{OUT}/r5_routes.png")


if __name__ == "__main__":
    for f in (r1_split, r3_last_token, r4_pointer, r5_routes):
        f()
        print("ok", f.__name__)
