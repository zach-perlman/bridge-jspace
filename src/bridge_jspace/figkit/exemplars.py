"""Five reference figures in the dot-table style, from the repo's own data (figkit.data). Run from the repo root:
PYTHONPATH=src:/home/claude/figref python3 /home/claude/figref/exemplars.py OUTDIR"""

from __future__ import annotations

import re

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit.dottable import INK, MUTED, C, Col, Row, Table, band, connector, dot, head_label, under, vrule

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
        mk, ct = D.b(f"ko.{k}.mk")[0], S.ctrl(k)
        return [(f"{mk:.0f}", INK, "bold"), (f"   control {ct:.0f}", MUTED, "normal")]

    t = Table(rows, [
        Col(3.0, "Remove everywhere (Zach)", "answers that turn wrong, points", zach, (-4, 70), [0, 20, 40, 60]),
        Col(1.15, "gap", "recall − lookup", zach_nums, text=True),
        *dan_split_cols(),
    ], label_w=1.45)  # fmt: skip
    t.render(f"{OUT}/r1_c1_split.png")


def dan_split_cols(title="Remove from the patch (Dan)"):
    """r1's right half: the conflict test's lookup and recall, and the gap with its interval."""

    def dan(ax, _rows):
        n = len(DAN)
        band(ax, -0.1, 0.1, n)
        under(ax, 0.0, "grey band: not needed")
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
        return [(f"{rc - lk:.2f}", INK, "bold")]

    return [Col(3.0, title, "switches lost beyond a random part", dan, (-0.25, 1.0), [0, 0.5, 1.0]),
            Col(1.35, "gap", "[95% interval]", dan_nums, text=True)]  # fmt: skip


def r1_dan_split():
    """The depth README's Fig. 1: r1's right half alone (the 01:58 brief)."""
    Table([Row(NAME[m]) for m, _ in DAN], dan_split_cols("Remove from the patch"), label_w=1.45).render(
        f"{OUT}/r1_dan_split.png"
    )


# ---- R2: the address, three columns ---------------------------------------------------------------------------------
def r2_address():
    rows = [Row(NAME[m]) for m, _ in DAN]

    def probe(ax, _rows):
        for i, (m, _) in enumerate(DAN):
            v = D.s(m, "the locker probe at the bridge word, locker-first scenes")
            base = D.s(m, "the locker probe's layout baseline, locker-first scenes")[0]
            ax.plot([base, base], [i - 0.26, i + 0.26], color=C["control"], lw=2.2, zorder=3)
            dot(ax, v[0], i, C["address"], D.hollow(m), cell=v, value=v[0], vside="left")
        b0 = D.s("qwen3.5-9b", "the locker probe's layout baseline, locker-first scenes")[0]
        head_label(ax, b0, "layout only", MUTED, weight="normal")
        head_label(ax, 0.97, "probe", C["address"])

    def swap(ax, _rows):
        for i, (m, _) in enumerate(DAN):
            two = D.s(m, "lookup target share, mean over locker pairs, s = 2", "fig07")
            rnd = D.s(m, "lookup target share, random direction, s = 4", "fig07")
            connector(ax, rnd[0], two[0], i)
            dot(ax, rnd[0], i, C["control"], size=8)
            dot(ax, two[0], i, C["lookup"], D.hollow(m, True), value=two[0])
        head_label(ax, 0.0, "random", MUTED, ha="left", weight="normal")
        head_label(ax, D.s("qwen3.5-9b", "lookup target share, mean over locker pairs, s = 2", "fig07")[0],
                   "address swap", C["lookup"])  # fmt: skip

    zq = "47.0 (b) share rebuilt by 25 lens directions: "

    def lens(ax, _rows):
        band(ax, -1, 1, len(DAN))
        for i, (m, _) in enumerate(DAN):
            p, it = D.s(m, zq + "pointer: z", prefix=True), D.s(m, zq + "identity_mean: z", prefix=True)
            if not p:
                ax.text(-2.4, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                continue
            connector(ax, p[0], it[0], i)
            dot(ax, p[0], i, C["address"], D.hollow(m, True))  # the 122B: lookup-only gate, post hoc
            dot(ax, it[0], i, C["identity"], D.hollow(m, True), value=it[0], vfmt="{:.0f}")
        head_label(ax, 0, "address swap", C["address"], ha="left")
        head_label(ax, 20, "item change", C["identity"])

    t = Table(rows, [
        Col(2.75, "A probe reads it", "accuracy at the bridge word", probe, (0.4, 1.02), [0.5, 0.75, 1.0]),
        Col(2.75, "A swap moves it", "lookups sent to the new locker", swap, (-0.03, 0.75), [0, 0.25, 0.5]),
        Col(2.75, "The lens cannot see it", "z above random vectors", lens, (-2.5, 26),
            [0, 10, 20]),
    ], label_w=1.45)  # fmt: skip
    t.render(f"{OUT}/r2_address.png")


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
        Col(3.6, "Readable", "a probe finds the recall's entity in the lens part", read, (0, 1.02), [0, 0.5, 1.0]),
        Col(3.6, "Not used", "recalls that switch when it is written in", used, (-0.25, 1.02), [0, 0.5, 1.0]),
    ], label_w=1.6)  # fmt: skip
    t.render(f"{OUT}/r3_last_token.png")


# ---- R4: Zach's pointer, conditions as rows, models as columns -----------------------------------------------------
def r4_pointer():
    conds = [("D's own passage", "lens"), ("one neutral sentence about D", "lens"),
             ("without D's own-word directions", "lens"), ("rotated (control)", "control"),
             ("a probe's subspace (reads the fact)", "lookup")]  # fmt: skip
    rows = [Row(c) for c, _ in conds]
    models = [("q27", "Qwen 27B"), ("q9", "Qwen 9B"), ("nl", "Lightning")]

    def cells(k):
        own = D.b(f"ptr.{k}.swap")
        return [own, D.scaled(own, D.b(f"ptr.{k}.neutral")[0]), D.scaled(own, D.b(f"ptr.{k}.noown")[0]),
                D.b(f"ptr.{k}.rot"), D.b(f"probe.{k}.probe")]  # fmt: skip

    def panel(k):
        def f(ax, _rows):
            for i, (cell, (_, col)) in enumerate(zip(cells(k), conds, strict=True)):
                dot(ax, cell[0], i, C[col], cell=cell, value=cell[0], vfmt="{:.0f}")

        return f

    t = Table(rows, [Col(2.35, n, "answers moved to D's fact, points" if j == 0 else "", panel(k), (-8, 92),
                         [0, 40, 80]) for j, (k, n) in enumerate(models)], label_w=3.35, labels=False)  # fmt: skip
    t.render(f"{OUT}/r4_pointer.png")


# ---- R5: routes, 100% stacked as rows -------------------------------------------------------------------------------
def r5_routes():
    models = [(m, n) for m, n in DAN if D.s(m, "another item moved, whole: identity share")]
    rows = [Row(NAME[m]) for m, _ in models]

    def stack(ax, _rows):
        for i, (m, _) in enumerate(models):
            idn = D.s(m, "another item moved, whole: identity share")[0]
            pos = D.s(m, "another item moved, whole: position share")[0]
            a = 0.45 if D.hollow(m, True) else 1.0
            ax.barh(i, idn, left=0, height=0.62, color=C["identity"], alpha=a, zorder=3)
            ax.barh(i, pos, left=idn, height=0.62, color=C["address"], alpha=a, zorder=3)
            ax.barh(i, 1 - idn - pos, left=idn + pos, height=0.62, color=C["other"], zorder=3)
            tc = "white" if a == 1.0 else INK
            ax.text(idn / 2, i, f"{idn:.2f}", ha="center", va="center", fontsize=12, color=tc, weight="bold", zorder=4)
            ax.text(
                idn + pos / 2, i, f"{pos:.2f}", ha="center", va="center", fontsize=12, color=tc, weight="bold", zorder=4
            )
        head_label(ax, 0.0, "by identity", C["identity"], ha="left")
        head_label(ax, 1.0, "by position", C["address"], ha="right")

    def value(i, _r):
        v = D.s(models[i][0], "another item moved, whole: value share")[0]
        return [(f"{v:.2f}", INK, "bold")]

    t = Table(rows, [Col(6.6, "Which locker the lookup names", "identity: the item's own locker · position: the locker now at its old place", stack,
                         (0, 1), [0, 0.5, 1]),
                     Col(1.3, "the number", "itself", value, text=True)], label_w=1.45)  # fmt: skip
    t.render(f"{OUT}/r5_routes.png")


if __name__ == "__main__":
    for f in (r1_split, r2_address, r3_last_token, r4_pointer, r5_routes):
        f()
        print("ok", f.__name__)
