"""The LessWrong write-up's rebuilds of the nine-model grade, the address figures and the question-order appendix
(figures/writeup/, built by `figkit.tables --target writeup`): deck_figs.f_nine, f_address("read_removed"),
f_address("swap_lens") and f_order laid out again at 8.0 in (1600 px at 200 dpi), from the same data the deck reads
(docs/breadth/data.csv, data/figures/depth/data.csv, docs/depth/x0_numbers.json)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import deck_figs as F
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit import writeup_figs as W
from bridge_jspace.figkit.dottable import BAND, INK, MUTED, C, Col, Row, band, connector, dot, head_label

OUT = "."  # set by bridge_jspace.figkit.tables
PROBLEMS: list[str] = []
DAN, NAME = W.DAN, W.NAME


def _note(ax, xlim, y, text, zebra=None):
    """A grey cell note at the cell's right end, where no rule runs; its box the row's colour hides the grid lines
    (zebra: whether the row is striped; None: every other row, as for one row per stripe)."""
    striped = round(y) % 2 == 0 if zebra is None else zebra
    t = ax.text(xlim[1], y, text, ha="right", va="center", fontsize=W.FS["small"], color=MUTED, zorder=6,
                bbox={"boxstyle": "square,pad=0.15", "facecolor": T.ZEBRA if striped else "white",
                      "edgecolor": "none"})  # fmt: skip
    t._masks_lines = True


# ---- Fig. 6: nine models, carried and needed (f3_nine_models) -------------------------------------------------------
def fig06_nine_models() -> None:
    """Per model: the answers moved by the other entity's lens part swapped in (teal; Bolt also at 100 directions, the
    small dot), the recall - lookup accuracy drop with the lens part removed (black) against the largest same-size
    control (grey tick; the 122B scored by probability, grey dot), and the model's grade (deck_figs.f_nine)."""
    grade = {"q27": "clean", "q9": "clean", "nl": "clean", "ds": "weak, not specific", "mi": "weak",
             "nb": "not specific", "ol": "carried, not needed", "mu": "shared with logit lens",
             "q122": "gone by probability"}  # fmt: skip
    swapkey = {"ds": "swap.ds.mid.swap", "mi": "swap.mi.mid.swap"}
    order = F.ZORD
    rows = [Row(n) for _, n in order]
    carry_lim, need_lim = (-8, 84), (-3, 72)

    def carried(ax, _r):
        for i, (k, _) in enumerate(order):
            c = D.b(swapkey.get(k, f"swap.{k}.swap"))
            if not c:  # Muse and the 122B were swapped only in an earlier protocol, not in this set
                _note(ax, carry_lim, i, "no comparable run")
                continue
            dot(ax, c[0], i, C["lens"], cell=c)
            if k == "nb":
                dot(ax, D.b("swap.nb.k100.swap")[0], i, C["lens"], size=6)  # Bolt at 100 directions (the key says so)
            W.value(ax, c[0], i, c, C["lens"], "{:.0f}")
        head_label(ax, carry_lim[1], "lens part swapped in", C["lens"], ha="right")

    def needed(ax, _r):
        for i, (k, _) in enumerate(order):
            mk, ct = D.b(f"ko.{k}.mk"), S.ctrl(k)
            if ct is not None:
                ax.plot([ct, ct], [i - 0.26, i + 0.26], color=C["control"], lw=2.4, zorder=3)
            dot(ax, mk[0], i, C["recall"], cell=mk)
            if k == "q122":
                dot(ax, D.b("ko.q122.soft")[0], i, C["control"], size=7)  # scored by probability (the key says so)
            W.value(ax, mk[0], i, mk, C["recall"], "{:.0f}")
        head_label(ax, need_lim[1], "lens part taken out", C["recall"], ha="right")

    def grades(i, _r):
        g = grade[order[i][0]]
        return [(g, INK if g == "clean" else MUTED, "bold" if g == "clean" else "normal")]

    t = W.table(rows, [
        Col(2.35, "answers moved", "to the other entity's fact", carried, carry_lim, [0, 40, 80], xlabel="points",
            cue="→ carried more"),
        Col(2.35, "accuracy drop", "recall minus lookup", needed, need_lim, [0, 30, 60],
            xlabel="accuracy drop (points)", cue="→ needed more"),
        Col(1.8, "grade", "", grades, text=True),
    ], label_w=1.05, row_h=0.4,
        key=[[("|", C["control"], "largest same-size control"), ("●", C["control"], "the 122B scored by probability")],
             [("●", C["lens"], "small: Bolt at 100 directions"), ("", MUTED, "whiskers: 95% interval")]])  # fmt: skip
    t.render(f"{OUT}/fig06_nine_models.png", dpi=W.DPI)


# ---- Fig. 8: the address (f6a / f6b) --------------------------------------------------------------------------------
SHORT = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "qwen3.5-122b-a10b": "122b"}


def _removal_cells(m):
    """Position answers with the address taken out, and with a random part of the same size (deck_figs.f_address)."""
    if m == "nemotron-3.5-lightning":
        return (D.s(m, "another item moved, no_alf: position share"),
                D.s(m, "another item moved, no_alf_rand: position share"))  # fmt: skip
    pre = "rtg_C2" if m == "qwen3.5-122b-a10b" else "rt_C2"
    return D.x(f"{pre}_no_alf_position_{SHORT[m]}"), D.x(f"{pre}_no_alf_rand_position_{SHORT[m]}")


def fig08a_address_read_remove() -> None:
    """Left: the locker probe's accuracy at the bridge word (orange) against the layout alone (grey tick). Right: the
    lookups that follow the position with the address taken out (orange) against a random part of the same size taken
    out (grey). Every mark sits on its row's upper line; the address values sit under their dots, on the lower line."""
    rows = [Row(NAME[m]) for m, _ in DAN]
    probe_lim, rem_lim = (0.4, 1.03), (-0.12, 0.74)

    def probe(ax, _r):
        for i, (m, _) in enumerate(DAN):
            y = i - W.LIFT
            v = D.s(m, "the locker probe at the bridge word, locker-first scenes")
            base = D.s(m, "the locker probe's layout baseline, locker-first scenes")[0]
            ax.plot([base, base], [y - 0.24, y + 0.24], color=C["control"], lw=2.4, zorder=3)
            dot(ax, v[0], y, C["address"], D.hollow(m), cell=v)
            W.value(ax, v[0], y, v, C["address"], "{:.2f}", i=i)
        head_label(ax, 0.53, "layout only", MUTED, weight="normal")
        head_label(ax, 1.0, "probe", C["address"], ha="right")

    def remove(ax, _r):
        for i, (m, _) in enumerate(DAN):
            y = i - W.LIFT
            a, r = _removal_cells(m)
            connector(ax, a[0], r[0], y)
            dot(ax, r[0], y, C["control"], size=8)
            dot(ax, a[0], y, C["address"], D.hollow(m, True))
            W.value(ax, r[0], y, None, C["control"], "{:.2f}", i=i, size=8)
            # under its dot: beside it the value would cross the zero line or the connector
            W.lower(ax, a[0], i, T.clean(f"{a[0]:.2f}"), color=C["address"])
        head_label(ax, rem_lim[0], "address removed", C["address"], ha="left")

    t = W.table(rows, [
        Col(3.0, "probe accuracy", "at the bridge word", probe, probe_lim, [0.5, 0.75, 1], xlabel="accuracy",
            cue="→ address more readable"),
        Col(3.0, "position answers", "lookups following the position", remove, rem_lim, [0, 0.25, 0.5],
            xlabel="share of lookups", cue="← address needed"),
    ], label_w=1.3, key=[("●", C["control"], "a random part of the same size taken out (right)"),
                         ("", MUTED, "whiskers: 95% interval")])  # fmt: skip
    t.render(f"{OUT}/fig08a_address_read_remove.png", dpi=W.DPI)


def fig08b_address_swap_lens() -> None:
    """Left: the lookups sent to the new locker by the address swap at 2x (orange) against a random direction at 4x
    (grey). Right: how much of an address swap and of an item change 25 lens directions rebuild, as a z against 200
    random vectors (the band: their range)."""
    rows = [Row(NAME[m]) for m, _ in DAN]
    swap_lim, z_lim = (-0.04, 0.68), (-2.5, 31)
    zq = "47.0 (b) share rebuilt by 25 lens directions: "

    def swap(ax, _r):
        for i, (m, _) in enumerate(DAN):
            two = D.s(m, "lookup target share, mean over locker pairs, s = 2", "fig07")
            rnd = D.s(m, "lookup target share, random direction, s = 4", "fig07")
            connector(ax, rnd[0], two[0], i)
            dot(ax, rnd[0], i, C["control"], size=8)
            dot(ax, two[0], i, C["address"], D.hollow(m, True))
            W.value(ax, two[0], i, None, C["address"], "{:.2f}")
        head_label(ax, swap_lim[1], "address swap", C["address"], ha="right")

    def lens(ax, _r):
        band(ax, -1, 1, len(DAN))
        for i, (m, _) in enumerate(DAN):
            p, it = D.s(m, zq + "pointer: z", prefix=True), D.s(m, zq + "identity_mean: z", prefix=True)
            if not p:
                _note(ax, z_lim, i, "no run")
                continue
            connector(ax, p[0], it[0], i)
            dot(ax, p[0], i, C["address"], D.hollow(m, True))  # the 122B: lookup-only gate, post hoc
            dot(ax, it[0], i, C["identity"], D.hollow(m, True))
            W.value(ax, it[0], i, None, C["identity"], "{:.0f}")
        head_label(ax, z_lim[0], "address swap", C["address"], ha="left")
        head_label(ax, z_lim[1], "item change", C["identity"], ha="right")

    t = W.table(rows, [
        Col(3.0, "lookups sent", "to the new locker", swap, swap_lim, [0, 0.25, 0.5], xlabel="share of lookups",
            cue="→ swap works"),
        Col(3.0, "lens rebuild", "z against 200 random vectors", lens, z_lim, [0, 10, 20, 30],
            xlabel="z (distance from random)", cue="→ lens sees it"),
    ], label_w=1.3, key=[[("●", C["control"], "a random direction swapped in instead (left)")],
                         [("■", BAND, "range of 200 random vectors (right)")]])  # fmt: skip
    t.render(f"{OUT}/fig08b_address_swap_lens.png", dpi=W.DPI)


# ---- Appendix: question before or after the scene (f12_order) ----------------------------------------------------------
def appB_f12_order() -> None:
    """The lookup and the recall without the lens part, with the question after the scene (the main test, lighter) and
    before it (darker), beyond a random part; the lookup's paired difference before - after. Question before ran on the
    27B and the 122B only; the others' cells give the recall's gate value. The 27B's rule was set after its cells
    (post hoc, hollow) (deck_figs.f_order)."""
    stem = "question {} the scene: {}, switches lost beyond a random part"
    gate = "question before the scene: the recall's gate (read right on the original prompts)"
    models = list(DAN)
    rows = []
    for m, _ in models:
        rows += [Row(NAME[m], sub="lookup"), Row("", sub="recall")]
    post_hoc = lambda m: D.hollow(m) or m == "qwen3.6-27b"  # noqa: E731
    reader_col = {"lookup": (C["lookup_light"], C["lookup"]), "recall": (C["recall_light"], C["recall"])}
    lim = (-0.3, 0.95)

    def lk(ax, _r):
        band(ax, -0.1, 0.1, len(rows))
        for i, (m, _) in enumerate(models):
            striped = i % 2 == 0  # two rows (lookup, recall) per stripe
            for j, reader in enumerate(("lookup", "recall")):
                row = 2 * i + j
                y = row - W.LIFT  # the marks on the upper line; a value with no room beside its dot goes under it
                a, b = D.s(m, stem.format("after", reader)), D.s(m, stem.format("before", reader))
                light, dark = reader_col[reader]
                if b:
                    connector(ax, a[0], b[0], y)
                    dot(ax, b[0], y, dark, post_hoc(m), cell=b)
                dot(ax, a[0], y, light, post_hoc(m), size=8.5)
                if b:
                    W.value(ax, b[0], y, b, dark, "{:.2f}", i=row, zebra=striped)
                W.value(ax, a[0], y, None, light, "{:.2f}", i=row, size=8.5, zebra=striped)
                if not b and j == 0 and (g := D.s(m, gate)):
                    _note(ax, lim, y, f"below gate ({g[0]:.2f})", zebra=striped)

    def diff(i, _r):
        m, reader = models[i // 2][0], ("lookup", "recall")[i % 2]
        if reader == "recall":
            return [("", MUTED, "normal")]
        d = D.s(m, "the lookup, question before minus after (paired)")
        if not d:
            return [("can't tell", MUTED, "normal")]
        return [(f"{d[0]:+.2f}", INK, "bold"), (f"  [{d[1]:.2f}, {d[2]:.2f}]", MUTED, "normal")]

    t = W.table(rows, [
        Col(4.3, "without the lens part", "switches blocked beyond a random part", lk, lim, [0, 0.5],
            xlabel="switches blocked beyond random (share)", cue="→ depends more on lens part"),
        Col(1.85, "before − after", "lookup, paired [95%]", diff, text=True),
    ], label_w=1.25, row_h=0.5, group=2, labels=False, foot=0.45, sub_lift=True,
        key=[[("●", C["lookup"], "lookup"), ("●", C["recall"], "recall"),
              ("", MUTED, "lighter: question after · darker: before"), ("■", BAND, "within 0.10 of random")],
             [("○", INK, "post hoc: the 27B's rule set after its cells; Lightning's gate after its pre-check")]])  # fmt: skip
    t.render(f"{OUT}/appB_f12_order.png", dpi=W.DPI)


FIGS = {"fig06_nine_models": fig06_nine_models, "fig08a_address_read_remove": fig08a_address_read_remove,
        "fig08b_address_swap_lens": fig08b_address_swap_lens, "appB_f12_order": appB_f12_order}  # fmt: skip
