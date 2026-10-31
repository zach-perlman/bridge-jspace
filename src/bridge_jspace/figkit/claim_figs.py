"""Three claim figures in the deck's table style (31 Oct), for the slides and the root README: sentence order (claim 10, with the post hoc 2x2), when by depth
(claim 12) and the two removals (post hoc). Numbers come from data/figures/depth/data.csv (the rows scripts/readme_story_figures.py records from the run
files); no caption inside the figure (the deck and the README carry it)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit.dottable import INK, MUTED, C, Col, Row, Table, connector, dot, head_label

OUT = "."  # set by bridge_jspace.figkit.tables
DPI = 160
NAME, DAN = X.NAME, X.DAN
ORDER_Q = "lookups switched by the whole change, locker sentence {}"
BOTH_Q = "post hoc, original locker sentence {} the pick, changed {}: lookups switched by the whole change"  # {}: before / after
OFFSET = 0.0
ZACH_Q = "Zach's passages, L{}: lookups switched by the whole change, fact-{}"  # {}: the model's layer; first / after
ZACH_L = {"qwen3.5-9b": 12, "qwen3.6-27b": 32, "muse-glimmer-30b": 26, "nemotron-3.5-lightning": 14}
SLIDE_W, SLIDE_ROW = 12.0, 0.55  # inches: the deck figures are 2400 px wide at 200 dpi; the row height sets the height


def _render(t: Table, name: str) -> None:
    t.render(f"{OUT}/{name}.png", dpi=DPI)


def f_sentence_order() -> None:
    """Claim 10: the lookup's switches under the whole change by where the locker sentence sits, ours; then the post hoc 2x2 (both orders)."""
    models = [(m, n) for m, n in DAN if D.s(m, ORDER_Q.format("before the pick"), "fig03")]
    rows = [Row(NAME[m]) for m, _ in models]

    def first_after(ax, _rows):
        for i, (m, _) in enumerate(models):
            b, a = D.s(m, ORDER_Q.format("before the pick"), "fig03"), D.s(m, ORDER_Q.format("after the pick"), "fig03")
            hol = D.hollow(m)
            connector(ax, a[0], b[0], i)
            dot(ax, a[0], i, C["lookup_light"], hol, cell=a, value=a[0], vside="left")
            dot(ax, b[0], i, C["lookup"], hol, cell=b, value=b[0])
        head_label(ax, 0.12, "locker after", C["lookup_light"], ha="left")
        head_label(ax, 0.55, "locker first", C["lookup"], ha="left")

    def both(orig: str):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                cb = D.s(m, BOTH_Q.format(orig, "before"), "fig03")
                ca = D.s(m, BOTH_Q.format(orig, "after"), "fig03")
                if not cb or not ca:
                    continue
                connector(ax, ca[0], cb[0], i)
                dot(ax, ca[0], i, C["lookup_light"], True, cell=ca, value=ca[0], vside="left")
                dot(ax, cb[0], i, C["lookup"], True, cell=cb, value=cb[0])
            head_label(ax, 0.0, "after", C["lookup_light"], ha="left")
            head_label(ax, 0.8, "before", C["lookup"], ha="left")

        return f

    t = Table(
        rows,
        [
            Col(3.5, "lookups switched", "the locker sentence first vs after the pick", first_after, (-0.02, 1.0), [0, 0.5, 1],
                xlabel="share of lookups switched", cue="→ more switched"),
            Col(3.0, "original locker first", "post hoc: the changed prompt's", both("before"), (-0.2, 1.3), [0, 0.5, 1],
                xlabel="share of lookups switched", cue="→ more switched"),
            Col(3.0, "original locker after", "post hoc: the changed prompt's", both("after"), (-0.2, 1.3), [0, 0.5, 1],
                xlabel="share of lookups switched", cue="→ more switched"),
        ],
        label_w=1.45,
        labels=True,
    )
    _render(t, "f10_sentence_order")


def f_depth() -> None:
    """Claim 12 (deck): per model two markers on one axis, the layer as a share of the model's depth: where the locker probe first reads the address (>= 0.80)
    and where the position answers begin (>= 0.20), the layer printed beside each; no line between them. The 27B row (its full grid) carries the note on the
    lookup's last layer needing the lens part. The lookup's own reading is text in the README, not drawn here."""
    depth = {"qwen3.5-9b": 32, "qwen3.6-27b": 64, "muse-glimmer-30b": 52, "nemotron-3.5-lightning": 52, "qwen3.5-122b-a10b": 48}
    models = [(m, n) for m, n in DAN if D.s(m, "47.8: l_probe", "fig06")]
    rows = [Row(NAME[m] + (" (full grid)" if m == "qwen3.6-27b" else "")) for m, _ in models]

    def depth_col(ax, _rows):
        for i, (m, _) in enumerate(models):
            hol = D.hollow(m, True)
            lp, ls = (D.s(m, f"47.8: {k}", "fig06")[0] for k in ("l_probe", "l_P"))
            for v, col in ((lp, C["control"]), (ls, C["address"])):
                dot(ax, v / depth[m], i, col, hol, size=11, value=v, vfmt="L{:.0f}")
            if m == "qwen3.6-27b":
                lj = D.s(m, "47.8: l_J", "fig06")[0]
                ax.text(0.60, i, f"full grid: the lookup still needs the lens part\nuntil L{lj:.0f}, after position answers begin (L{ls:.0f})", ha="left", va="center", fontsize=11.5,
                        color=C["lookup"], linespacing=1.2)

    with _slide(0.6):
        t = Table(rows, [Col(9.6, "", "", depth_col, (-0.03, 1.02), [0, 0.25, 0.5, 0.75, 1], xlabel="layer, as a share of the model's depth", cue="→ deeper")],
                  label_w=1.9, labels=False, head=0.3,
                  key=[("●", C["control"], "address readable (probe ≥ 0.80)"), ("●", C["address"], "position answers begin (≥ 0.20)")])
        _render(t, "f13_depth_anatomy")


def f_two_codes() -> None:
    """Post hoc: the same scenes followed one by one (another item moved, lookup). Position-route scenes that leave position without the address vs a random part;
    identity-route scenes that go to position without J++ vs a random part; the paired difference beside each."""
    models = [(m, n) for m, n in DAN if D.s(m, "post hoc, another item moved, lookup: Position scenes that leave position, without the address", "fig24")]
    rows = [Row(NAME[m]) for m, _ in models]
    qa = "post hoc, another item moved, lookup: Position scenes that leave position, "
    qb = "post hoc, another item moved, lookup: Identity scenes that go to position, "

    def panel(q: str, arm: str, col, word: str):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                a, r = D.s(m, q + arm, "fig24"), D.s(m, q + "without a same-size random part", "fig24")
                connector(ax, r[0], a[0], i)
                dot(ax, r[0], i, C["control"], True, size=9, value=None)
                dot(ax, a[0], i, col, True, size=9.5)
            head_label(ax, 0.02, "random part", MUTED, ha="left")
            head_label(ax, 0.45, word, col, ha="left")

        return f

    def diff(q: str):
        def f(i, _r):
            d = D.s(models[i][0], q + "paired difference", "fig24")
            return [(f"{d[0]:+.2f}", INK, "bold"), (f"  [{d[1]:+.2f}, {d[2]:+.2f}]", MUTED, "normal")]

        return f

    t = Table(
        rows,
        [
            Col(3.2, "leave position", "position scenes, post hoc", panel(qa, "without the address", C["address"], "without the address"), (-0.02, 1.0), [0, 0.5, 1],
                xlabel="share of the scenes", cue="→ more leave"),
            Col(1.9, "difference", "paired, 95%", diff(qa), text=True),
            Col(3.2, "go to position", "identity scenes, post hoc", panel(qb, "without the J++ part", C["lookup"], "without J++"), (-0.02, 1.0), [0, 0.5, 1],
                xlabel="share of the scenes", cue="→ more go"),
            Col(1.9, "difference", "paired, 95%", diff(qb), text=True),
        ],
        label_w=1.45,
    )
    _render(t, "f14_two_codes")


def _slide(row_h: float = SLIDE_ROW):
    """Context for the deck's wide figures: the row height sets the image height, about 2400 x 1000 px (12 x 5 in at 200 dpi)."""

    class _Ctx:
        def __enter__(self):
            self.old = T.ROW_H
            T.ROW_H = row_h
            return self

        def __exit__(self, *_):
            T.ROW_H = self.old

    return _Ctx()


def f_order_main() -> None:
    """Deck: the claim fixed in advance. Per model the share of lookups switched by the change at the bridge word, the sentence after the pick (light) against
    before it (dark); left the locker scenes, right Zach's fact passages (the 122B not run)."""
    models = [(m, n) for m, n in DAN if D.s(m, ORDER_Q.format("before the pick"), "fig03")]
    rows = [Row(NAME[m]) for m, _ in models]

    def lanes(get):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                got = get(m)
                if got is None:
                    ax.text(0.5, i, "no run", ha="center", va="center", fontsize=12.5, color=MUTED)
                    continue
                b, a = got
                hol = D.hollow(m)
                connector(ax, a[0], b[0], i)
                dot(ax, a[0], i, C["lookup_light"], hol, size=11, cell=a, vside="left")
                ax.annotate(f"{a[0]:.2f}", (a[1], i), xytext=(-5, 0), textcoords="offset points", ha="right", va="center", fontsize=11.5, color=C["lookup"], zorder=6)
                dot(ax, b[0], i, C["lookup_dark"], hol, size=11, cell=b, value=b[0])

        return f

    def locker(m):
        return D.s(m, ORDER_Q.format("before the pick"), "fig03"), D.s(m, ORDER_Q.format("after the pick"), "fig03")

    def zach(m):
        if m not in ZACH_L:
            return None
        return D.s(m, ZACH_Q.format(ZACH_L[m], "first"), "fig03"), D.s(m, ZACH_Q.format(ZACH_L[m], "after"), "fig03")

    with _slide(0.5):
        t = Table(
            rows,
            [
                Col(4.85, "Locker scenes", "", lanes(locker), (-0.2, 1.15), [0, 0.5, 1], xlabel="lookups switched (share)", cue="→ more switched"),
                Col(4.85, "Zach's fact passages", "", lanes(zach), (-0.2, 1.15), [0, 0.5, 1], xlabel="lookups switched (share)", cue="→ more switched"),
            ],
            label_w=1.55,
            labels=False,
            head=0.8,
            key=[("●", C["lookup_dark"], "the locker / fact sentence came before the pick"), ("●", C["lookup_light"], "after the pick")],
        )
        _render(t, "f10a_order_main")


def f_order_2x2() -> None:
    """Deck, appendix (post hoc): the 2 x 2 in the encoding of f10a. Left the scenes whose original prompt has the locker sentence before the pick, right those
    with it after; in each, the lookups switched when the changed prompt's locker sentence comes after the pick (light) against before it (dark)."""
    models = [(m, n) for m, n in DAN if D.s(m, BOTH_Q.format("before", "before"), "fig03")]
    rows = [Row(NAME[m]) for m, _ in models]

    def lanes(orig: str):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                b, a = D.s(m, BOTH_Q.format(orig, "before"), "fig03"), D.s(m, BOTH_Q.format(orig, "after"), "fig03")
                connector(ax, a[0], b[0], i)
                dot(ax, a[0], i, C["lookup_light"], True, size=11, cell=a, vside="left")
                ax.annotate(f"{a[0]:.2f}", (a[1], i), xytext=(-5, 0), textcoords="offset points", ha="right", va="center", fontsize=11.5, color=C["lookup"], zorder=6)
                dot(ax, b[0], i, C["lookup_dark"], True, size=11, cell=b, value=b[0])

        return f

    with _slide(0.5):
        t = Table(
            rows,
            [
                Col(4.85, "Original prompt: locker first", "", lanes("before"), (-0.2, 1.15), [0, 0.5, 1], xlabel="lookups switched (share)", cue="→ more switched"),
                Col(4.85, "Original prompt: locker after the pick", "", lanes("after"), (-0.2, 1.15), [0, 0.5, 1], xlabel="lookups switched (share)", cue="→ more switched"),
            ],
            label_w=1.55,
            labels=False,
            head=0.8,
            key=[("●", C["lookup_dark"], "the changed prompt's locker sentence came before the pick"), ("●", C["lookup_light"], "after the pick")],
        )
        _render(t, "f10b_order_2x2")
