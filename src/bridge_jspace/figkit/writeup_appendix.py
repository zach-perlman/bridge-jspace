"""The LessWrong write-up's appendix figures (appB_*), rebuilt as is at the write-up's 8.0 in width: the deck's f5_atoms,
f9_where, f8_facts, f8_directions (deck_figs) and its curve figures f15_link_crossover, f17_attention (curve_figs). Same
data and encodings as their originals (data/figures/depth/data.csv, docs/breadth/data.csv); only the layout changes.
The curve figures are not dot tables: they pass the same lint through dottable.BEFORE_SAVE before they are saved."""

from __future__ import annotations

import math
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt

from bridge_jspace.figkit import curve_figs as CV
from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import lint
from bridge_jspace.figkit import writeup_figs as W
from bridge_jspace.figkit.dottable import (
    BAND,
    FAINT,
    INK,
    MUTED,
    C,
    Col,
    Row,
    band,
    clean,
    connector,
    dot,
    head_label,
    rich,
)

OUT = "."  # set by bridge_jspace.figkit.tables
PROBLEMS: list[str] = []
FS = W.FS
BANDKEY = ("■", BAND, "within 0.10 of a random part")


def _save(fig, name: str) -> None:
    path = f"{OUT}/{name}.png"
    if T.BEFORE_SAVE is not None:  # the target's lint (tables.build: table lint at 11 pt, text crossing a line or a mark)
        T.BEFORE_SAVE(fig, path)
    fig.savefig(path, dpi=W.DPI, facecolor="white")
    plt.close(fig)


def _cue(ax, cue: str, offset: float) -> None:
    """The direction cue under an axis title (the table style's rule: say which way is "more"), `offset` points down."""
    ax.annotate(cue, (0.5, 0), xycoords="axes fraction", xytext=(0, -offset), textcoords="offset points", ha="center",
                va="top", fontsize=FS["cue"], color=MUTED, annotation_clip=False)  # fmt: skip
    ax._cue = cue


def _place(ax, text: str, xy, offsets, rules=(), **kw):
    """An annotation at the first offset (points) where it touches no line or mark drawn so far and stays inside the
    axes. If none is free, the first offset that crosses only reference rules (`rules`, e.g. the L/2 and L lines):
    the label then gets a white box and the rule stops at it (figkit/lint.py crossings: `_masks_lines`); else the
    first offset (the lint then names it)."""
    fig = ax.figure
    fig.canvas.draw()  # the spines take their place at the first draw: before it their paths are stale
    r = fig.canvas.get_renderer()
    box = ax.get_window_extent(r)

    def first_free(obstacles):
        for dx, dy in offsets:
            a = ax.annotate(text, xy, xytext=(dx, dy), textcoords="offset points", va="center", annotation_clip=False,
                            ha="center" if dx == 0 else ("left" if dx > 0 else "right"), **kw)  # fmt: skip
            bb = a.get_window_extent(r)
            if box.x0 <= bb.x0 and bb.x1 <= box.x1 and box.y0 <= bb.y0 and bb.y1 <= box.y1 and not lint.hit(bb, obstacles):
                return a
            a.remove()
        return None

    if (a := first_free(lint.drawn_obstacles(fig))) is not None:
        return a
    for ln in rules:
        ln.set_visible(False)
    try:
        a = first_free(lint.drawn_obstacles(fig))
    finally:
        for ln in rules:
            ln.set_visible(True)
    if a is not None:
        a.set_bbox({"boxstyle": "square,pad=0.1", "facecolor": "white", "edgecolor": "none"})
        a._masks_lines = True
        return a
    dx, dy = offsets[0]
    return ax.annotate(text, xy, xytext=(dx, dy), textcoords="offset points", va="center", annotation_clip=False,
                       ha="center" if dx == 0 else ("left" if dx > 0 else "right"), **kw)  # fmt: skip


def _ring() -> list[tuple[float, float]]:
    """Candidate label offsets (points) around a mark: nearest first, sixteen directions (straight up first), out to
    52 points."""
    out = []
    for r in (17, 24, 32, 42, 52):
        for k in range(16):
            a = math.pi / 2 + (k + 1) // 2 * (1 if k % 2 else -1) * math.pi / 8
            out.append((round(r * math.cos(a), 1), round(r * math.sin(a), 1)))
    return list(dict.fromkeys(out))


RING = _ring()


# ---- appB_f5_atoms: what the lens part is ---------------------------------------------------------------------------
def f5_atoms() -> None:
    q = "52 A: share of the rebuilt energy, "
    models = [(m, n) for m, n in W.DAN if D.s(m, q + "the old bridge word")]
    rows = [Row(W.NAME[m]) for m, _ in models]

    def stack(ax, _r):
        for i, (m, _) in enumerate(models):
            hol = D.hollow(m)  # post hoc: hollow segments, not a tint
            segs = [(D.s(m, q + "the old bridge word")[0], C["recall"]), (D.s(m, q + "the new bridge word")[0], C["lens"]),
                    (D.s(m, q + "another scene word or its class")[0], "#9E9E9E"), (D.s(m, q + "no scene word")[0], "#DADADA")]  # fmt: skip
            x = 0
            for j, (v, col) in enumerate(segs):
                kw = {"facecolor": "white", "edgecolor": col, "linewidth": 2.0} if hol else {"color": col}
                ax.barh(i, v, left=x, height=0.62, zorder=3, **kw)
                if v >= 0.08:
                    ax.text(x + v / 2, i, f"{v:.2f}", ha="center", va="center", fontsize=FS["value"],
                            color="white" if (j < 2 and not hol) else INK, weight="bold", zorder=4)  # fmt: skip
                x += v
        head_label(ax, 0.0, "old bridge word", C["recall"], ha="left")
        head_label(ax, 0.42, "new bridge word", C["lens"], ha="center")
        head_label(ax, 1.0, "no word of the scene", MUTED, ha="right", weight="normal")

    def answer(i, _r):
        v = D.s(models[i][0], q + "an answer word")[0]
        return [(clean(f"{v:.2f}"), INK, "bold")]

    t = W.table(rows, [
        Col(5.4, "share of the rebuilt energy", "of the lens part's 25 directions, by the word each decodes to",
            stack, (0, 1), [0, 0.5, 1], xlabel="share of the rebuilt energy", cue="→ more of the energy"),
        Col(0.95, "answer", "word's share", answer, text=True),
    ], label_w=1.2, key=[("●", "#9E9E9E", "another scene word")])  # fmt: skip
    t.render(f"{OUT}/appB_f5_atoms.png", dpi=W.DPI)


# ---- appB_f9_where: where in the prompt and in depth, two stacked bands ---------------------------------------------
WHERE_MODELS = (("q9", "Qwen 9B"), ("q27", "Qwen 27B"), ("mu", "Muse 30B"), ("nl", "Lightning"))
WHERE_KEYS = {"mid": ("pos.{}.all.all", "pos.{}.all.bridge", "pos.{}.all.question"),
              "late": ("late.{}.all", "late.{}.bridge", "late.{}.question")}  # fmt: skip


def _where_col(band_: str, j: int):
    def f(ax, _r):
        for i, (k, _) in enumerate(WHERE_MODELS):
            key = WHERE_KEYS[band_][j].format(k)
            if k == "mu":  # Muse's deeper band is its knock-out run; its middle band has no position-limited run
                key = {"late": ("ko.mu.mk", "pos.mu.bridge", "pos.mu.question")}.get(band_, ("", "", ""))[j]
            c = D.b(key) if key else None
            if not c:
                ax.text(4, i, "no run", ha="left", va="center", fontsize=FS["small"], color=MUTED)
                continue
            col = C["recall"] if j == 0 else (C["mention"] if j == 1 else C["question"])
            rk = "ko.mu.rot" if (k == "mu" and j == 0) else (key + ".rot" if k == "mu" else WHERE_KEYS[band_][j].format(k) + ".rot")
            rot = D.b(rk)
            if rot:  # under the row's dot, so a control at the same value is not hidden behind it
                dot(ax, rot[0], i + 0.26, C["control"], size=7)
            size = 9.5 if c[0] > 15 else 8
            dot(ax, c[0], i - 0.1, col, cell=c, size=size)
            if not rot:
                W.lower(ax, 4, i, "no control run", ha="left")
            W.value(ax, c[0], i - 0.1, c, col, "{:.0f}", i=i, size=size)

    return f


def f9_where() -> None:
    rows = [Row(n) for _, n in WHERE_MODELS]
    names = ["all tokens", "mention", "question"]
    pts = dict(xlim=(-3, 72), xticks=[0, 50], xlabel="points", cue="→ needed more")
    compact = {"row_h": 0.42, "labels": False, "foot": 0.22, "head": 0.95, "title_top": 0.68}
    tables = []
    for g, (band_, title) in enumerate((("mid", "Middle layers (the knock-out band)"), ("late", "Deeper layers"))):
        last = g == 1
        t = W.table(rows, [Col(1.95, n, "", _where_col(band_, j), **pts) for j, n in enumerate(names)], label_w=1.15,
                    key=[[("●", C["recall"], "all tokens"), ("●", C["mention"], "the bridge's mention"),
                          ("●", C["question"], "the question")],
                         [("●", C["control"], "rotated control, same size")]] if last else [], **compact)  # fmt: skip
        t.extra.append(W._groups((0.12, title), notes=((0.12, "accuracy drop when the lens part is removed at"),)))
        tables.append(t)
    W.stack(tables, "appB_f9_where")


# ---- appB_f8_facts: true and made-up facts ----------------------------------------------------------------------------
def f8_facts() -> None:
    rows = [Row(W.NAME[m]) for m, _ in W.DAN]
    q = "Zach's named passages, {} facts, lookup: switches lost beyond random"  # the data's quantity name, not drawn

    def facts(ax, _r):
        band(ax, -0.1, 0.1, len(W.DAN))
        for i, (m, _) in enumerate(W.DAN):
            tr, mu = D.s(m, q.format("true"), "ledger_zach_named"), D.s(m, q.format("made-up"), "ledger_zach_named")
            if not tr or m == "muse-glimmer-30b":  # Muse: under 30 lookup switches (ledger_zach_named)
                ax.text(-0.27, i, "–", ha="left", va="center", fontsize=FS["text"], color=MUTED)
                continue
            if mu:
                connector(ax, mu[0], tr[0], i)
                dot(ax, mu[0], i, C["lookup_light"], D.hollow(m), size=8)
            dot(ax, tr[0], i, C["lookup"], D.hollow(m), cell=tr)
            W.value(ax, tr[0], i, tr, C["lookup"], "{:.2f}")

    t = W.table(rows, [Col(6.3, "fact passages", "the lookup's switches blocked without the lens part", facts,
                           (-0.3, 0.9), [0, 0.25, 0.5, 0.75], xlabel="switches blocked beyond random",
                           cue="→ depends more on lens part")], label_w=1.3, labels=False,
                key=[("●", C["lookup"], "true facts"), ("●", C["lookup_light"], "made-up facts"), BANDKEY])  # fmt: skip
    t.render(f"{OUT}/appB_f8_facts.png", dpi=W.DPI)


# ---- appB_f8_directions: the lookup with more lens directions ---------------------------------------------------------
def f8_directions() -> None:
    rows = [Row(W.NAME[m]) for m, _ in W.DAN]
    lim = (-0.62, 0.95)

    def kcol(k):
        def f(ax, _r):
            band(ax, -0.1, 0.1, len(W.DAN))
            for i, (m, _) in enumerate(W.DAN):
                # the conflict test's direction curve with its 95% interval (data.csv fig02b)
                c = D.s(m, f"(a) main test, {k} directions: lookup extra loss", "fig02b")
                if not c:  # Lightning has no curve: its gate failed
                    ax.text(0.14, i, "below gate", ha="left", va="center", fontsize=FS["small"], color=MUTED)
                    continue
                size = 9.5 if c[0] > 0.1 else 8
                dot(ax, c[0], i, C["lookup"], cell=c, size=size)
                W.value(ax, c[0], i, c, C["lookup"], "{:.2f}", size=size)

        return f

    t = W.table(rows, [Col(2.05, f"{k} lens directions", "", kcol(k), lim, [0, 0.5], xlabel="blocked beyond random",
                           cue="→ more blocked") for k in (25, 50, 100)],
                label_w=1.3, labels=False, key=[BANDKEY],
                subtitle="the lookup's switches blocked when more lens directions are removed")  # fmt: skip
    t.render(f"{OUT}/appB_f8_directions.png", dpi=W.DPI)


# ---- appB_f15_link_crossover: the change at the bridge word against the same change copied --------------------------
def _axis_x(ax, depth: int, xmax: float = 1.03) -> None:
    ax.set_xlim(-0.04, xmax)
    ax.set_xticks([0, 0.5, 1.0], [f"{t:g}\nL{round(t * depth)}" for t in (0, 0.5, 1.0)])
    ax.tick_params(labelsize=FS["value"], length=3, color=FAINT, colors=MUTED)
    ax.set_xlabel("share of the depth", fontsize=FS["xlabel"], color=MUTED, labelpad=2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(FAINT)
    ax.spines["bottom"].set_color(FAINT)
    ax.grid(axis="y", color=T.GRID)
    ax.set_axisbelow(True)


def f15_link_crossover() -> None:
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
    # two by two, the key in the fourth cell: three panels in a row leave no room for a value between L/2 and L
    w, top, ph, below = W.WIDTH, 0.62, 2.1, 1.08  # inches: over each panel, the panel, under it (ticks, title, cue)
    h = 2 * (top + ph + below)
    left, gap = 1.25, 0.45
    pw = (w - left - gap - 0.15) / 2
    fig = plt.figure(figsize=(w, h))
    at = [(left, h - top - ph), (left + pw + gap, h - top - ph), (left, h - 2 * top - 2 * ph - below)]
    axes = [fig.add_axes((x / w, y / h, pw / w, ph / h)) for x, y in at]
    light, dark = C["lookup_light"], C["lookup_dark"]
    bw = "45q, layer {}: the bridge-word change (lookups switched)"  # the data's quantity names, not drawn
    cp = "45q, layer {}: the copy into the locker sentences (lookups switched)"
    arms = (("a", "the bridge-word change at L", "L", light), ("c", "copy at L, every locker-sentence token", "L", dark),
            ("d", "copy at L/2, every locker-sentence token", "L/2", dark))  # (arm, quantity, which layer, colour)
    for ax, m in zip(axes, models, strict=True):
        depth = CV.DEPTH[m]
        _axis_x(ax, depth)
        ax.set_ylim(-0.04, 1.1)
        ax.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.text(0, 1.13, W.NAME[m], transform=ax.transAxes, ha="left", va="bottom", fontsize=FS["title"],
                weight="bold", color=INK)  # fmt: skip
        layers = CV._layers(m, "fig03", r"45q, layer (\d+): the bridge-word change")
        for name, col, ls in ((bw, light, "--"), (cp, dark, "-")):
            v = [D.s(m, name.format(la), "fig03") for la in layers]
            xs = [la / depth for la in layers]
            ax.fill_between(xs, [t[1] for t in v], [t[2] for t in v], color=col, alpha=0.2, lw=0, zorder=1)
            ax.plot(xs, [t[0] for t in v], color=col, ls=ls, lw=2.2, marker="o", ms=4.5, mfc="white", mec=col,
                    mew=1.2, zorder=2)  # open marks: the sweep, post hoc  # fmt: skip
        L, half = (D.s(m, f"45q: {q}", "fig03")[0] for q in ("L, the rule's layer", "L/2, the rule's half layer"))
        rules = []
        for x, txt in ((half / depth, "L/2"), (L / depth, "L")):
            rules.append(ax.axvline(x, color="#555555", ls=":", lw=1.3, zorder=0))
            ax.text(x, 1.02, txt, transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=FS["small"],
                    color="#555555")  # fmt: skip
        cells = []
        for arm, what, which, col in arms:  # the cells fixed in advance
            r = D.s(m, f"45q, the rule's arm {arm}: {what} (lookups switched)", "fig03")
            x = (L if which == "L" else half) / depth
            ax.plot([x, x], [r[1], r[2]], color=INK, lw=1.6, zorder=5)
            ax.plot([x], [r[0]], "o", ms=11, color=col, mec=INK, mew=1.3, zorder=6)
            cells.append((x, r[0]))
        for x, v in cells:  # every mark drawn first, so each value finds free space
            _place(ax, f"{v:.2f}", (x, v), RING, rules=rules, fontsize=FS["value"], color=INK, zorder=7)
        _cue(ax, "→ deeper", 58)
        if ax is not axes[1]:
            ax.set_ylabel("lookups\nswitched\n(share)", fontsize=FS["xlabel"], color=MUTED, rotation=0, ha="right",
                          va="center", labelpad=6)  # fmt: skip
    key = [[("●", dark, "normal"), (" the cells fixed in advance", MUTED, "normal")],
           [("   (L/2 and L), values printed", MUTED, "normal")],
           [("○", INK, "normal"), (" the layer sweep, post hoc", MUTED, "normal")],
           [("- -", light, "bold"), (" the change at the bridge word", MUTED, "normal")],
           [("—", dark, "bold"), (" the same change copied into", MUTED, "normal")],
           [("   the locker sentences", MUTED, "normal")],
           [("bands and whiskers: 95%", MUTED, "normal")],
           [("Locker sentence after the pick.", MUTED, "normal")],
           [("Not drawn: Lightning (below its", MUTED, "normal")],
           [("gate), the 122B (no run).", MUTED, "normal")]]  # fmt: skip
    kx, ky = at[1][0], at[2][1] + ph + top - 0.1  # the fourth cell, from its top
    for i, parts in enumerate(key):
        rich(fig, kx / w, (ky - i * 0.3) / h, parts, size=FS["key"])
    _save(fig, "appB_f15_link_crossover")


# ---- appB_f17_attention: attention follows the swap; no small set of heads carries it ------------------------------
ATT_PRE = "attention mass on slot {}'s locker sentence, {} (mean of five heads, read half)"
SW, ST, NC, RV = "the swap, answer switched", "the swap, answer stayed", "no change, switched pairs", "a random vector, switched pairs"


def _attention_bars(path: str) -> None:
    """Per model the last token's attention on the old and the new locker sentence: the swap with the answer switched
    (dark) and with it staying (light), no change and a random vector as dashed and dotted reference ticks."""
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
    w, h = W.WIDTH, 4.0
    fig = plt.figure(figsize=(w, h))
    top, bottom = 1.85 / h, 0.92 / h
    left, gap = 0.62 / w, 0.3 / w
    pw = (1 - left - 0.12 / w - 2 * gap) / 3
    for k, m in enumerate(models):
        ax = fig.add_axes((left + k * (pw + gap), bottom, pw, 1 - top - bottom))
        ax.text(0, 1.04, W.NAME[m], transform=ax.transAxes, ha="left", va="bottom", fontsize=FS["title"],
                weight="bold", color=INK)  # fmt: skip
        ax.set_xlim(-0.55, 1.55)
        ax.set_ylim(0, 1.12)
        labels = []
        for gi, slot in enumerate(("j", "k")):
            for q, ls, col in ((NC, "--", C["control"]), (RV, ":", "#8C8C8C")):
                v = D.s(m, ATT_PRE.format(slot, q), "fig13")
                ax.plot([gi - 0.42, gi + 0.42], [v[0]] * 2, color=col, ls=ls, lw=1.6, zorder=1.5)
            for q, col, dx in ((SW, C["lookup_dark"], -0.17), (ST, C["lookup_light"], 0.17)):
                v = D.s(m, ATT_PRE.format(slot, q), "fig13")
                ax.bar(gi + dx, v[0], width=0.3, color=col, lw=0, zorder=2)
                ax.plot([gi + dx] * 2, [v[1], v[2]], color="#1e1e1e", lw=1.2, zorder=3)
                labels.append((gi + dx, v))
        for x, v in labels:  # above its whisker, higher if a reference tick runs there
            _place(ax, f"{v[0]:.2f}".lstrip("0"), (x, v[2]), [(0, 9), (0, 19), (0, 29), (0, 39)],
                   fontsize=FS["value"], color=INK, zorder=6)  # fmt: skip
        ax.set_xticks([0, 1], ["old", "new"])
        ax.set_yticks([0, 0.5] if k == 0 else [], ["0", "0.5"] if k == 0 else [])
        ax.tick_params(labelsize=FS["value"], length=3, color=FAINT, colors=MUTED)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(FAINT)
        ax.grid(axis="y", color=T.GRID)
        ax.set_axisbelow(True)
        ax.set_xlabel("locker sentence", fontsize=FS["xlabel"], color=MUTED, labelpad=2)
        _cue(ax, "↑ more attention", 32)
    rng = lambda q: (min(D.s(m, ATT_PRE.format("k", q), "fig13")[0] for m in models),  # noqa: E731
                     max(D.s(m, ATT_PRE.format("k", q), "fig13")[0] for m in models))  # fmt: skip
    f = lambda t: f"{t[0]:.2f}–{t[1]:.2f}"  # noqa: E731
    y0, dy = 1 - 0.2 / h, 0.3 / h
    key = [[("Last-token attention on each locker sentence", INK, "bold")],
           [("●", C["lookup_dark"], "normal"), (" the swap, answer switched   ", MUTED, "normal"),
            ("●", C["lookup_light"], "normal"), (" the swap, answer stayed   whiskers: 95%", MUTED, "normal")],
           [("- -", C["control"], "bold"), (" no change   ", MUTED, "normal"), ("···", "#8C8C8C", "bold"),
            (" a random vector", MUTED, "normal")],
           [(f"on the new locker: {f(rng(SW))} when the answer switched, {f(rng(ST))} when it stayed,", INK, "normal")],
           [(f"{f(rng(RV))} under a random vector", INK, "normal")]]  # fmt: skip
    for i, parts in enumerate(key):
        rich(fig, 0.12 / w, y0 - i * dy, parts, size=FS["key"])
    if T.BEFORE_SAVE is not None:
        T.BEFORE_SAVE(fig, path)
    fig.savefig(path, dpi=W.DPI, facecolor="white")
    plt.close(fig)


def _heads_table() -> T.Table:
    """Zeroing the top 10 heads against 10 random heads: the share of the swap's switch cut, with the rule's 0.5 bar."""
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
    rows = [Row(W.NAME[m]) for m in models]
    cell = lambda m: D.s(m, "last token, top 10: share of the swap's switch cut", "ledger_heads")  # noqa: E731
    rand = lambda m: D.s(m, "last token, top 10: random sets' mean cut", "ledger_heads")  # noqa: E731

    def heads(ax, _r):
        T.vrule(ax, 0.5, len(models))
        head_label(ax, 0.5, "rule: 0.5", MUTED, weight="normal")
        for i, m in enumerate(models):
            hol = D.hollow(m)
            dot(ax, rand(m)[0], i, C["control"], hol, size=8)
            dot(ax, cell(m)[0], i, C["lookup"], hol, cell=cell(m))

    def numbers(i, _r):
        v, r = cell(models[i]), rand(models[i])
        return [(f"{v[0]:.2f}", C["lookup"], "bold"), (f"  [{v[1]:.2f}, {v[2]:.2f}]", MUTED, "normal"),
                (f"   random {clean(f'{r[0]:.2f}')}", MUTED, "normal")]  # fmt: skip

    t = W.table(rows, [
        Col(3.6, "Zeroing the top 10 heads", "", heads, (-0.15, 0.62), [0, 0.25, 0.5], xfmt="{:g}",
            xlabel="share of the swap's switch cut", cue="→ heads carry more"),
        Col(2.6, "share cut", "top 10 [95%], random 10", numbers, text=True),
    ], label_w=1.2, row_h=0.34, foot=0.2, head=0.7,
        key=[("●", C["lookup"], "the top 10 heads"), ("●", C["control"], "10 random heads")])  # fmt: skip
    return t


def f17_attention() -> None:
    from PIL import Image

    with tempfile.TemporaryDirectory() as tmp:
        top = Path(tmp) / "appB_f17_attention_0.png"
        _attention_bars(str(top))
        bottom = Path(tmp) / "appB_f17_attention_1.png"
        _heads_table().render(str(bottom), dpi=W.DPI)
        parts = [Image.open(p).convert("RGB") for p in (top, bottom)]
        sheet = Image.new("RGB", (parts[0].width, sum(p.height for p in parts)), "white")
        y = 0
        for p in parts:
            sheet.paste(p, (0, y))
            y += p.height
        sheet.save(f"{OUT}/appB_f17_attention.png", dpi=(W.DPI, W.DPI))


FIGS = {"appB_f5_atoms": f5_atoms, "appB_f9_where": f9_where, "appB_f8_facts": f8_facts,
        "appB_f8_directions": f8_directions, "appB_f15_link_crossover": f15_link_crossover,
        "appB_f17_attention": f17_attention}  # the brief's appendix order; fixed names  # fmt: skip
