"""Three claim figures in the deck's table style (31 Oct), for the slides and the root README: sentence order (claim 10, with the post hoc 2x2), when by depth
(claim 12) and the two removals (post hoc). Numbers come from data/figures/depth/data.csv (the rows scripts/readme_story_figures.py records from the run
files); no caption inside the figure (the deck and the README carry it)."""

from __future__ import annotations

import csv
import json
from functools import cache
from pathlib import Path

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
    """Deck and README: the same scenes followed one by one (another item moved, lookup; every cell post hoc, so every mark is hollow). Left: of the scenes
    on the position route under the whole change, the share that leave it without the address (orange) against without a same-size random part (grey);
    right: of the scenes on the identity route, the share that go to position without the J++ part (teal) against without its random part; beside each panel
    the paired difference with its 95% interval."""
    models = [(m, n) for m, n in DAN if D.s(m, "post hoc, another item moved, lookup: Position scenes that leave position, without the address", "fig24")]
    rows = [Row(NAME[m]) for m, _ in models]
    qa = "post hoc, another item moved, lookup: Position scenes that leave position, "
    qb = "post hoc, another item moved, lookup: Identity scenes that go to position, "

    def panel(q: str, arm: str, col):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                a, r = D.s(m, q + arm, "fig24"), D.s(m, q + "without a same-size random part", "fig24")
                connector(ax, r[0], a[0], i)
                dot(ax, r[0], i, C["control"], True, size=10, cell=r, value=r[0], vside="left")
                dot(ax, a[0], i, col, True, size=10, cell=a, value=a[0])

        return f

    def forest(q: str, col):
        def f(ax, _rows):
            for i, (m, _) in enumerate(models):
                d = D.s(m, q + "paired difference", "fig24")
                dot(ax, d[0], i, col, True, size=10, cell=d, value=d[0], vfmt="{:+.2f}")

        return f

    def group_titles(fig):
        w = t.label_w + sum(c.width for c in t.cols) + t.pad * (len(t.cols) + 1)
        x0 = (t.label_w + t.pad) / w
        x1 = (t.label_w + t.pad * 3 + t.cols[0].width + t.cols[1].width) / w
        for x, txt in ((x0, "Without the address,\nposition answers disappear"), (x1, "Without the lens part, identity\nanswers turn into position")):
            fig.text(x, 1 - 0.12 / fig.get_figheight(), txt, ha="left", va="top", fontsize=13, color=INK, weight="bold", linespacing=1.2)

    with _slide(0.5):
        t = Table(
            rows,
            [
                Col(2.55, "scenes that leave position", "among position-route scenes", panel(qa, "without the address", C["address"]), (-0.2, 1.1), [0, 0.5, 1],
                    xlabel="share of the scenes", cue="→ more leave"),
                Col(2.25, "difference", "95% interval", forest(qa, C["address"]), (-0.1, 1.25), [0, 0.5, 1], xlabel="difference (share)", cue="0 = no effect, larger →"),
                Col(2.55, "scenes that go to position", "among identity-route scenes", panel(qb, "without the J++ part", C["lens"]), (-0.2, 1.1), [0, 0.5, 1],
                    xlabel="share of the scenes", cue="→ more go"),
                Col(2.25, "difference", "95% interval", forest(qb, C["lens"]), (-0.1, 1.25), [0, 0.5, 1], xlabel="difference (share)", cue="0 = no effect, larger →"),
            ],
            label_w=1.4,
            pad=0.2,
            labels=False,
            head=1.35,
            key=[("●", C["address"], "without the address"), ("●", C["lens"], "without the lens part"), ("●", C["control"], "without a same-size random part")],
        )
        t.extra.append(group_titles)
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


# ---- f18 / f19 (31 Oct): code and tool output; six lockers ------------------------------------------------------------------
REPO = Path(__file__).resolve().parents[3]
_PRINTED: set = set()


@cache
def _csv_rows() -> dict:
    with (REPO / "data/figures/depth/data.csv").open(newline="") as f:
        return {(r["figure"], r["model"], r["quantity"]): r for r in csv.DictReader(f)}


def _num(x: str):
    try:
        return float(x)
    except ValueError:
        return None


def row_value(figure: str, model: str, quantity: str):
    """(value, lo, hi) from data.csv; every row read is printed once with its source, so the plotted numbers can be checked."""
    r = _csv_rows()[(figure, model, quantity)]
    v, lo, hi = _num(r["value"]), _num(r["lo"]), _num(r["hi"])
    if (figure, model, quantity) not in _PRINTED:
        _PRINTED.add((figure, model, quantity))
        print(f"{figure} | {model} | {quantity} = {r['value']}" + (f" [{r['lo']}, {r['hi']}]" if r["lo"] else "") + f" n={r['n']} | {r['source']}")
    return v, lo, hi


def f_code_tool() -> None:
    """Deck (replaces fig21_code_tool): does the address carry over to Python code and tool output? Rows: 9B code (the probe was below its gate: a grey text row in
    the probe panel; its routes test was run, so the position panel has it), 9B tool output, 27B code, 27B tool output. A: the probe at the bridge word (dot),
    the layout-only baseline (grey tick), the same probe in prose (small open tick). B: the position answers when another item moves, without the address,
    only the address, a same-size random part removed (grey)."""
    fig = "fig21_code_tool"
    rows_def = (("qwen3.5-9b", "code"), ("qwen3.5-9b", "tool"), ("qwen3.6-27b", "code"), ("qwen3.6-27b", "tool"))
    rows = [Row(NAME[m], sub="code" if c == "code" else "tool output") for m, c in rows_def]
    base = "code and tool output, {}: "
    gate = _csv_rows()[(fig, "qwen3.5-9b", base.format("code") + "the probe's status")]
    print(f"{fig} | qwen3.5-9b | code: the probe's status = {gate['value']} | {gate['source']}")
    gate_num = gate["value"].split("gate ")[1].split(" <")[0]  # "0.669"

    def probe(ax, _r):
        for i, (m, c) in enumerate(rows_def):
            if m == "qwen3.5-9b" and c == "code":
                ax.text(0.42, i, f"below gate: probe {gate_num} < 0.80", ha="left", va="center", fontsize=12, color=MUTED)
                continue
            v = row_value(fig, m, base.format(c) + "the locker probe at the bridge word, locker-first scenes")
            b = row_value(fig, m, base.format(c) + "the locker probe's layout baseline, locker-first scenes")[0]
            pr = row_value(fig, m, base.format(c) + "the locker probe in prose, locker-first scenes (stored)")[0]
            ax.plot([b, b], [i - 0.26, i + 0.26], color=C["control"], lw=2.6, zorder=3)
            ax.plot([pr, pr], [i - 0.2, i + 0.2], color=C["address"], lw=3.6, zorder=3, solid_capstyle="butt")
            ax.plot([pr, pr], [i - 0.2, i + 0.2], color="white", lw=1.4, zorder=3.1, solid_capstyle="butt")  # an open tick
            dot(ax, v[0], i, C["address"], False, size=11, cell=v, value=v[0], vside="left")

    def move(ax, _r):
        for i, (m, c) in enumerate(rows_def):
            no = row_value(fig, m, base.format(c) + "another item moved, no_alf: position share")
            kp = row_value(fig, m, base.format(c) + "another item moved, keep_alf: position share")
            rd = row_value(fig, m, base.format(c) + "another item moved, no_alf_rand: position share")
            connector(ax, min(no[0], rd[0]), max(no[0], rd[0]), i)
            dot(ax, rd[0], i, C["control"], False, size=10, value=rd[0], vside="right", box=False)
            dot(ax, no[0], i, C["address"], False, size=11)
            ax.annotate(f"{no[0]:.2f}", (no[0], i), xytext=(0, 11), textcoords="offset points", ha="center", va="bottom", fontsize=11.5, color=C["address"])
            dot(ax, kp[0], i, C["address"], False, size=6.5, zorder=6)

    def n_col(i, _r):
        m, c = rows_def[i]
        n = row_value(fig, m, base.format(c) + "another item moved, no_alf: position share")
        print(f"{fig} | n per row {m} {c} = {_csv_rows()[(fig, m, base.format(c) + 'another item moved, no_alf: position share')]['n']}")
        return [(f"{int(_csv_rows()[(fig, m, base.format(c) + 'another item moved, no_alf: position share')]['n'])}", INK, "bold")]

    def group_titles(fig_):
        pass

    with _slide(0.62):
        t = Table(
            rows,
            [
                Col(3.75, "probe reads the address", "at the bridge word, accuracy", probe, (0.4, 1.03), [0.5, 0.75, 1], xlabel="accuracy", cue="→ more readable"),
                Col(4.45, "position answers when another item moves", "share of lookups on the position route", move, (-0.04, 0.6), [0, 0.25, 0.5],
                    xlabel="share of lookups", cue="← the address is needed"),
                Col(0.9, "scenes", "per row", n_col, text=True),
            ],
            label_w=1.9,
            labels=False,
            head=0.8,
            key=[[("●", C["address"], "without the address"), ("●", C["address"], "only the address (small)"), ("●", C["control"], "a same-size random part removed"),
                  ("▮", C["control"], "layout-only probe"), ("▮", C["address"], "the same probe in prose")]],
        )
        _render(t, "f18_code_tool")


def _shift_cells(path: str, model: str) -> list[tuple[float, float]]:
    """(shift, random) at dose 2 for the five start lockers, from a verdict's cells (the 27B and the 122B have no data.csv rows)."""
    d = json.loads((REPO / path).read_text())
    m = next(x for x in d["models"] if x["target"] == model)
    out = []
    for k in range(1, 6):
        c = m["cells"]["shifts"][f"2|v|{k}"]
        print(f"{path} | {model} | shifts 2|v|{k} (n={c['n']}) shift={c['shift'][0]} random={c['random'][0]}")
        out.append((c["shift"][0], c["random"][0]))
    return out


def f_six_lockers() -> None:
    """Deck (replaces fig09b_six_lockers): with six lockers, does each locker have its own code? A: the pairs of lockers (of 30) whose address swap reaches the
    25% bar, per model. B: the lookups sent one locker on by the shift vector (purple, mean over the five start lockers, the range as a line) against a random
    direction of the same size (grey), the 25% bar dashed."""
    models = [(m, n) for m, n in DAN]
    rows = [Row(NAME[m]) for m, _ in models]
    six = {"qwen3.6-27b": "results/x47_six/x52_six-20261029T004919Z/x47_2.json", "qwen3.5-122b-a10b": "results/x47_six/x52_six-20261029T231821Z/x47_2.json"}
    pairs = {}
    for m, _ in models:
        pairs[m] = row_value("fig09b", m, "47.2: pairwise writes reaching 25% (dose 2)")[0] if m not in six else row_value("cards", m, "47.2: pairwise writes reaching 25% (dose 2)")[0]
    starts = {}
    ordn = ("1st", "2nd", "3rd", "4th", "5th")
    for m, _ in models:
        if m in six:
            starts[m] = _shift_cells(six[m], m)
        else:
            starts[m] = [(row_value("fig09b", m, f"47.2: lookups sent one locker on from the {o} locker, the shift vector, dose 2")[0],
                          row_value("fig09b", m, f"47.2: lookups sent one locker on from the {o} locker, a random direction (same size), dose 2")[0]) for o in ordn]

    def bars(ax, _r):
        for i, (m, _) in enumerate(models):
            v = int(pairs[m])
            hol = D.hollow(m)
            ax.barh(i, v, height=0.52, color="white" if hol else C["lookup"], edgecolor=C["lookup"], linewidth=2.2, zorder=2)
            ax.text(v + 0.8, i, f"{v} of 30", ha="left", va="center", fontsize=12.5, color=C["lookup"], weight="bold", zorder=6,
                    bbox={"boxstyle": "square,pad=0.15", "fc": "white", "ec": "none"})
        ax.plot([15, 15], [len(models) - 0.5, -0.5], color="#8C8C8C", ls=(0, (4, 3)), lw=1.3, zorder=1)
        ax.text(15.4, -0.45, "half", ha="left", va="bottom", fontsize=11, color=MUTED)

    def shifts(ax, _r):
        for i, (m, _) in enumerate(models):
            sh = [a for a, _b in starts[m]]
            rd = [b for _a, b in starts[m]]
            mean_s, mean_r = sum(sh) / 5, sum(rd) / 5
            print(f"f19 | {m} | mean over the five start lockers: shift {mean_s:.4f} (min {min(sh):.2f}, max {max(sh):.2f}), random {mean_r:.4f}")
            hol = D.hollow(m)
            ax.plot([min(sh), max(sh)], [i, i], color=C["lookup"], lw=2.6, zorder=3, solid_capstyle="butt")
            dot(ax, mean_r, i, C["control"], False, size=9, value=None)
            dot(ax, mean_s, i, C["lookup"], hol, size=11)
            ax.annotate(f"{mean_s:.2f}", (mean_s, i), xytext=(0, 11), textcoords="offset points", ha="center", va="bottom", fontsize=11.5, color=C["lookup"])
        ax.plot([0.25, 0.25], [len(models) - 0.5, -0.5], color="#8C8C8C", ls=(0, (4, 3)), lw=1.3, zorder=1)
        ax.text(0.255, -0.45, "the 25% bar", ha="left", va="bottom", fontsize=11, color=MUTED)

    with _slide(0.54):
        t = Table(
            rows,
            [
                Col(4.95, "", "pairs of lockers (of 30) reaching the 25% bar", bars, (0, 33), [0, 15, 30], xlabel="pairs of lockers",
                    cue="→ more pairs"),
                Col(4.75, "", "lookups sent one locker on: mean, range", shifts, (-0.03, 0.4),
                    [0, 0.25], xlabel="share of lookups", cue="→ the shift works"),
            ],
            label_w=1.45,
            labels=False,
            head=1.2,
            key=[("■", C["lookup"], "pairs reaching the bar; the shift vector (mean, range as a line)"), ("●", C["control"], "a random direction, same size")],
        )

        def titles(fig_):
            w = t.label_w + sum(c.width for c in t.cols) + t.pad * (len(t.cols) + 1)
            x0 = (t.label_w + t.pad) / w
            x1 = (t.label_w + t.pad * 2 + t.cols[0].width) / w
            for x, txt in ((x0, "each locker has\nits own code"), (x1, "no single shift moves the\nlookup one locker on")):
                fig_.text(x, 1 - 0.12 / fig_.get_figheight(), txt, ha="left", va="top", fontsize=13, color=INK, weight="bold", linespacing=1.2)

        t.extra.append(titles)
        _render(t, "f19_six_lockers")
