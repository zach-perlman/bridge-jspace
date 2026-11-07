"""The write-up's rebuilds of the claim figures (claim_figs.py) at the post's column: 8.0 in at 200 dpi, nothing under
11 pt, no text over a line or a mark. Same data and encodings as the slide versions; the layouts are new (stacked where
two panel pairs do not fit side by side). fig09_order is f10a_order_main; the appendix keeps the source ids."""

from __future__ import annotations

from bridge_jspace.figkit import claim_figs as CF
from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import writeup_figs as W
from bridge_jspace.figkit.dottable import MUTED, C, Col, Row, connector, dot, head_label

OUT = "."  # set by bridge_jspace.figkit.tables
PROBLEMS: list[str] = []
FS = W.FS


def _cell_note(ax, x, i, text, ha="right"):
    """A grey cell note ("no run", a gate) on the row's middle, its box the row's colour: grid lines stop at it."""
    t = ax.text(x, i, text, ha=ha, va="center", fontsize=FS["small"], color=MUTED, zorder=6,
                bbox={"boxstyle": "square,pad=0.15", "facecolor": T.ZEBRA if round(i) % 2 == 0 else "white",
                      "edgecolor": "none"})  # fmt: skip
    t._masks_lines = True


# ---- Fig. 9: the sentence order (f10a_order_main) ---------------------------------------------------------------------
def fig09_order() -> None:
    """Per model the share of lookups switched by the change at the bridge word, the locker (or fact) sentence after the
    pick (light) against before it (dark); left the locker scenes, right the fact passages (the 122B not run)."""
    models = [(m, n) for m, n in W.DAN if D.s(m, CF.ORDER_Q.format("before the pick"), "fig03")]
    rows = [Row(W.NAME[m]) for m, _ in models]
    lim = (-0.32, 1.2)  # room left of the light dots for their values; no zero line (a share starts at 0)

    def lanes(get):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                got = get(m)
                if got is None:
                    _cell_note(ax, lim[1], i, "no run")
                    continue
                b, a = got
                hol = D.hollow(m)
                connector(ax, a[0], b[0], i)
                dot(ax, a[0], i, C["lookup_light"], hol, size=11, cell=a)
                dot(ax, b[0], i, C["lookup_dark"], hol, size=11, cell=b)
                # the light dot's value in the lookup's purple: the light tint is too pale for text
                W.value(ax, a[0], i, a, C["lookup"], "{:.2f}", size=11)
                W.value(ax, b[0], i, b, C["lookup_dark"], "{:.2f}", size=11)

        return f

    def locker(m):
        return D.s(m, CF.ORDER_Q.format("before the pick"), "fig03"), D.s(m, CF.ORDER_Q.format("after the pick"), "fig03")

    def facts(m):
        if m not in CF.ZACH_L:
            return None
        return (D.s(m, CF.ZACH_Q.format(CF.ZACH_L[m], "first"), "fig03"),
                D.s(m, CF.ZACH_Q.format(CF.ZACH_L[m], "after"), "fig03"))  # fmt: skip

    t = W.table(rows, [
        Col(3.25, "Locker scenes", "", lanes(locker), lim, [0, 0.5, 1], xlabel="lookups switched (share)", zero=False,
            cue="→ more switched"),
        Col(3.25, "Fact passages", "", lanes(facts), lim, [0, 0.5, 1], xlabel="lookups switched (share)", zero=False,
            cue="→ more switched"),
    ], label_w=1.15, labels=False, head=0.5, title_top=0.1, row_h=0.45,
        key=[[("●", C["lookup_dark"], "the locker / fact sentence came before the pick"),
              ("●", C["lookup_light"], "after the pick")]])  # fmt: skip
    t.render(f"{OUT}/fig09_order.png", dpi=W.DPI)


# ---- Appendix: the two removals (f14_two_codes), stacked ----------------------------------------------------------------
def appB_f14_two_codes() -> None:
    """The same scenes followed one by one (another item moved, lookup; every cell post hoc, so every mark is hollow).
    Top: of the scenes on the position route under the whole change, the share that leave it without the address
    (orange) against without a same-size random part (grey); bottom: of the scenes on the identity route, the share that
    go to position without the J++ part (teal) against without its random part; beside each, the paired difference
    with its 95% interval."""
    qa = "post hoc, another item moved, lookup: Position scenes that leave position, "
    qb = "post hoc, another item moved, lookup: Identity scenes that go to position, "
    models = [(m, n) for m, n in W.DAN if D.s(m, qa + "without the address", "fig24")]
    rows = [Row(W.NAME[m]) for m, _ in models]

    def panel(q: str, arm: str, col):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                a, r = D.s(m, q + arm, "fig24"), D.s(m, q + "without a same-size random part", "fig24")
                connector(ax, r[0], a[0], i)
                dot(ax, r[0], i, C["control"], True, size=10, cell=r)
                dot(ax, a[0], i, col, True, size=10, cell=a)
                W.value(ax, r[0], i, r, C["control"], "{:.2f}", size=10)
                W.value(ax, a[0], i, a, col, "{:.2f}", size=10)

        return f

    def forest(q: str, col):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                d = D.s(m, q + "paired difference", "fig24")
                dot(ax, d[0], i, col, True, size=10, cell=d)
                W.value(ax, d[0], i, d, col, "{:+.2f}", size=10)

        return f

    def half(q, arm, col, title, sub, cue, group, key=()):
        t = W.table(rows, [
            Col(3.6, title, sub, panel(q, arm, col), (-0.3, 1.1), [0, 0.5, 1], xlabel="share of the scenes", cue=cue,
                zero=False),
            Col(2.6, "difference", "95% interval", forest(q, col), (-0.1, 1.25), [0, 0.5, 1],
                xlabel="difference (share)", cue="0 = no effect, larger →"),
        ], label_w=1.15, labels=False, head=0.92, title_top=0.4, row_h=0.34, foot=0.35, key=list(key))  # fmt: skip
        t.extra.append(W._groups((0.12, group)))
        return t

    top = half(qa, "without the address", C["address"], "scenes that leave position", "among position-route scenes",
               "→ more leave", "Without the address, position answers disappear")
    bottom = half(qb, "without the J++ part", C["lens"], "scenes that go to position", "among identity-route scenes",
                  "→ more go", "Without the lens part, identity answers turn into position",
                  key=[[("●", C["address"], "without the address"), ("●", C["lens"], "without the lens part")],
                       [("●", C["control"], "without a same-size random part")]])  # fmt: skip
    W.stack([top, bottom], "appB_f14_two_codes")


# ---- Appendix: code and tool output (f18_code_tool) -----------------------------------------------------------------------
def appB_f18_code_tool() -> None:
    """Does the address carry over to Python code and tool output? Rows: 9B code (the probe below its bar: a grey note in
    the probe panel; its routes test was run), 9B tool output, 27B code, 27B tool output, each with its scene count.
    Left: the probe at the bridge word (dot), the layout-only baseline (grey tick), the same probe in prose (open tick).
    Right: the position answers when another item moves, without the address, only the address (small), a same-size
    random part removed (grey)."""
    fig = "fig21_code_tool"
    rows_def = (("qwen3.5-9b", "code"), ("qwen3.5-9b", "tool"), ("qwen3.6-27b", "code"), ("qwen3.6-27b", "tool"))
    base = "code and tool output, {}: "
    nq = "another item moved, no_alf: position share"

    def n_of(m, c):
        return int(CF._csv_rows()[(fig, m, base.format(c) + nq)]["n"])

    rows = [Row(W.NAME[m], sub=f"{'code' if c == 'code' else 'tool output'} · {n_of(m, c)} scenes") for m, c in rows_def]
    gate = CF._csv_rows()[(fig, "qwen3.5-9b", base.format("code") + "the probe's status")]
    gate_num = gate["value"].split("gate ")[1].split(" <")[0]  # "0.669"
    plim, mlim = (0.4, 1.03), (-0.04, 0.68)

    def probe(ax, _r):
        for i, (m, c) in enumerate(rows_def):
            if m == "qwen3.5-9b" and c == "code":
                _cell_note(ax, plim[1] - 0.02, i, f"probe {gate_num}, below the 0.80 bar")
                continue
            v = CF.row_value(fig, m, base.format(c) + "the locker probe at the bridge word, locker-first scenes")
            b = CF.row_value(fig, m, base.format(c) + "the locker probe's layout baseline, locker-first scenes")[0]
            pr = CF.row_value(fig, m, base.format(c) + "the locker probe in prose, locker-first scenes (stored)")[0]
            ax.plot([b, b], [i - 0.26, i + 0.26], color=C["control"], lw=2.6, zorder=3)
            ax.plot([pr, pr], [i - 0.2, i + 0.2], color=C["address"], lw=3.6, zorder=3, solid_capstyle="butt")
            ax.plot([pr, pr], [i - 0.2, i + 0.2], color="white", lw=1.4, zorder=3.1, solid_capstyle="butt")  # open tick
            dot(ax, v[0], i, C["address"], False, size=11, cell=v)
            W.value(ax, v[0], i, v, C["address"], "{:.2f}", size=11)

    def move(ax, _r):
        for i, (m, c) in enumerate(rows_def):
            no = CF.row_value(fig, m, base.format(c) + nq)
            kp = CF.row_value(fig, m, base.format(c) + "another item moved, keep_alf: position share")
            rd = CF.row_value(fig, m, base.format(c) + "another item moved, no_alf_rand: position share")
            connector(ax, min(no[0], rd[0]), max(no[0], rd[0]), i)
            dot(ax, rd[0], i, C["control"], False, size=10)
            dot(ax, no[0], i, C["address"], False, size=11)
            dot(ax, kp[0], i, C["address"], False, size=6.5, zorder=6)
            W.value(ax, rd[0], i, None, C["control"], "{:.2f}", size=10)
            ax.annotate(f"{no[0]:.2f}", (no[0], i), xytext=(0, 11), textcoords="offset points", ha="center",
                        va="bottom", fontsize=FS["value"], color=C["address"], zorder=6)  # fmt: skip

    t = W.table([*rows], [
        Col(2.8, "probe reads the address", "at the bridge word", probe, plim, [0.5, 0.75, 1], xlabel="accuracy",
            cue="→ more readable"),
        Col(3.3, "position answers", "when another item moves", move, mlim, [0, 0.25, 0.5],
            xlabel="share of lookups on the position route", cue="← the address is needed"),
    ], label_w=1.6, labels=False, head=0.85, row_h=0.62,
        key=[[("●", C["address"], "without the address"), ("●", C["address"], "only the address (small)")],
             [("●", C["control"], "a same-size random part removed")],
             [("▮", C["control"], "layout-only probe"), ("▮", C["address"], "the same probe in prose")]])  # fmt: skip
    t.render(f"{OUT}/appB_f18_code_tool.png", dpi=W.DPI)


# ---- Appendix: six lockers (f19_six_lockers) --------------------------------------------------------------------------------
def appB_f19_six_lockers() -> None:
    """With six lockers, does each locker have its own code? Left: the pairs of lockers (of 30) whose address swap
    reaches the 25% bar, per model. Right: the lookups sent one locker on by the shift vector (purple, mean over the
    five start lockers, the range as a line) against a random direction of the same size (grey), the 25% bar dashed."""
    six = {"qwen3.6-27b": "results/x47_six/x52_six-20261029T004919Z/x47_2.json",
           "qwen3.5-122b-a10b": "results/x47_six/x52_six-20261029T231821Z/x47_2.json"}  # fmt: skip
    models = list(W.DAN)
    rows = [Row(W.NAME[m]) for m, _ in models]
    pq = "47.2: pairwise writes reaching 25% (dose 2)"
    pairs = {m: CF.row_value("cards" if m in six else "fig09b", m, pq)[0] for m, _ in models}
    ordn = ("1st", "2nd", "3rd", "4th", "5th")
    sq = "47.2: lookups sent one locker on from the {} locker, {}, dose 2"
    starts = {m: CF._shift_cells(six[m], m) if m in six else
              [(CF.row_value("fig09b", m, sq.format(o, "the shift vector"))[0],
                CF.row_value("fig09b", m, sq.format(o, "a random direction (same size)"))[0]) for o in ordn]
              for m, _ in models}  # fmt: skip

    def bars(ax, _r):
        T.vrule(ax, 15, len(models))
        head_label(ax, 15, "half", MUTED, weight="normal")
        for i, (m, _) in enumerate(models):
            v = int(pairs[m])
            hol = D.hollow(m)
            ax.barh(i, v, height=0.56, color="white" if hol else C["lookup"], edgecolor=C["lookup"], linewidth=2.2,
                    zorder=2)  # fmt: skip
            # the count inside its bar, left: clear of the dashed half line
            ax.text(0.8, i, f"{v} of 30", ha="left", va="center", fontsize=FS["text"], weight="bold", zorder=6,
                    color=C["lookup"] if hol else "white")  # fmt: skip

    def shifts(ax, _r):
        T.vrule(ax, 0.25, len(models))
        head_label(ax, 0.25, "the 25% bar", MUTED, weight="normal")
        for i, (m, _) in enumerate(models):
            sh = [a for a, _b in starts[m]]
            mean_s, mean_r = sum(sh) / 5, sum(b for _a, b in starts[m]) / 5
            ax.plot([min(sh), max(sh)], [i, i], color=C["lookup"], lw=2.6, zorder=3, solid_capstyle="butt")
            dot(ax, mean_r, i, C["control"], False, size=9)
            dot(ax, mean_s, i, C["lookup"], D.hollow(m), size=11)
            W.value(ax, mean_s, i, (mean_s, min(sh), max(sh)), C["lookup"], "{:.2f}", size=11)

    t = W.table(rows, [
        Col(3.25, "", "pairs (of 30) reaching the 25% bar", bars, (0, 33), [0, 15, 30],
            xlabel="pairs of lockers", cue="→ more pairs"),
        Col(3.25, "", "sent one locker on: mean, range", shifts, (-0.03, 0.42), [0, 0.25],
            xlabel="share of lookups", cue="→ the shift works"),
    ], label_w=1.15, head=0.9, title_top=0.3, row_h=0.42,
        key=[[("■", C["lookup"], "pairs reaching the bar; the shift vector (mean, range as a line)")],
             [("●", C["control"], "a random direction, same size")]])  # fmt: skip
    t.extra.append(W._groups((W._x_of(t, 0), "Each locker has its own code"),
                             (W._x_of(t, 1), "No single shift moves the\nlookup one locker on")))  # fmt: skip
    t.render(f"{OUT}/appB_f19_six_lockers.png", dpi=W.DPI)


FIGS = {"fig09_order": fig09_order, "appB_f14_two_codes": appB_f14_two_codes, "appB_f18_code_tool": appB_f18_code_tool,
        "appB_f19_six_lockers": appB_f19_six_lockers}  # fmt: skip
