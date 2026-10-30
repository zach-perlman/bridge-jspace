"""Every figure of the deck (v2), in the table style of figures/depth/fig00_setup.png, from the repo's data.
Run from the repo root:  PYTHONPATH=src:<this dir> python3 deck_figs.py OUTDIR [--target slide|readme]
Uses dottable.py (the component) and exemplars.py (r1-r5)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit.dottable import (
    BAND,
    INK,
    MUTED,
    C,
    Col,
    Row,
    Table,
    band,
    clean,
    connector,
    dot,
    head_label,
)

OUT = "."  # set by bridge_jspace.figkit.tables
DPI = 160
NAME, DAN, ZK = X.NAME, X.DAN, X.ZK
# one model order everywhere (G8): the depth models, then the breadth-only ones
ZORD = [(k, dict(D.ZACH)[k]) for k in ("q9", "q27", "mu", "nl", "q122", "ds", "mi", "nb", "ol")]
BANDKEY = ("■", BAND, "within 0.10 of a random part")


def render(t: Table, name: str) -> None:
    t.render(f"{X.OUT}/{name}.png", dpi=DPI)


# ---- F2: same-size parts do not do it (both tracks, one column per part) --------------------------------------------
def f_controls():
    zach = [("lens part", "mk", "lens"), ("rotated", "rot", "control"), ("logit lens", "u", "control"),
            ("PCA", "pc", "control")]  # fmt: skip
    dq = [("lens part", "J++ part: recall extra loss", "lens"),
          ("PCA", "PCA directions (same size): recall extra loss", "control"),
          ("logit lens", "logit-lens directions: recall extra loss", "control"),
          ("random", "random lens directions: recall extra loss", "control")]  # fmt: skip
    rows = [Row(NAME[m]) for m, _ in DAN]

    def zcol(key, col):
        def f(ax, _r):
            for i, (m, _) in enumerate(DAN):
                k = ZK[m]
                c = D.b(f"ko.{k}.{key}")
                if key == "pc" and not c:
                    pcr, mk = D.b(f"ko.{k}.pcr"), D.b(f"ko.{k}.mk")
                    c = (pcr[0] * mk[0], None, None) if pcr and mk else None
                if not c:
                    ax.text(2, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                    continue
                dot(ax, c[0], i, C[col], hollow=k in ("mu", "q122"), cell=c if col != "control" else None,
                    value=c[0], vfmt="{:.0f}", size=9.5 if col != "control" else 8)  # fmt: skip

        return f

    def dcol(q, col):
        def f(ax, _r):
            for i, (m, _) in enumerate(DAN):
                c = D.s(m, q, "fig02")
                if not c:
                    ax.text(0.02, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                    continue
                dot(ax, c[0], i, C[col], cell=c if col != "control" else None, value=c[0],
                    size=9.5 if col != "control" else 8)  # fmt: skip

        return f

    cols = [Col(1.38, n, "", zcol(k, c), (-3, 70), [0, 50], xlabel="points") for n, k, c in zach]
    cols += [Col(1.38, n, "", dcol(q, c), (-0.05, 0.85), [0, 0.5], xlabel="share") for n, q, c in dq]
    t = Table(rows, cols, label_w=1.45, pad=0.18, labels=False, head=1.25)

    def group_titles(fig):
        w = t.label_w + sum(c.width for c in t.cols) + t.pad * (len(t.cols) + 1)
        x0 = (t.label_w + t.pad) / w
        x1 = (t.label_w + t.pad * 5 + sum(c.width for c in t.cols[:4])) / w
        fig.text(x0, 1 - 0.12 / fig.get_figheight(), "Band of layers: recall − lookup answers lost", ha="left", va="top",
                 fontsize=12.5, color=INK, weight="bold")  # fmt: skip
        fig.text(x1, 1 - 0.12 / fig.get_figheight(), "One layer: recall's switches lost beyond random", ha="left", va="top",
                 fontsize=12.5, color=INK, weight="bold")  # fmt: skip

    t.extra.append(group_titles)
    for c in t.cols:  # push the column titles below the group titles
        c.title, c.sub = c.title, c.sub
    render(t, "f2_controls")


# ---- F3: nine models, carried vs needed (Zach) ----------------------------------------------------------------------
def f_nine():
    grade = {"q27": "clean", "q9": "clean", "nl": "clean", "ds": "weak, not specific", "mi": "weak",
             "nb": "not specific", "ol": "carried, not needed", "mu": "shared with logit lens", "q122": "gone by probability"}  # fmt: skip
    swapkey = {"ds": "swap.ds.mid.swap", "mi": "swap.mi.mid.swap"}
    rows = [Row(n) for _, n in ZORD]

    def carried(ax, _r):
        for i, (k, _) in enumerate(ZORD):
            c = D.b(swapkey.get(k, f"swap.{k}.swap"))
            if not c:
                ax.text(-6, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                continue
            dot(ax, c[0], i, C["lens"], cell=c, value=c[0], vfmt="{:.0f}")
            if k == "nb":
                c100 = D.b("swap.nb.k100.swap")
                dot(ax, c100[0], i, C["lens"], size=6, value=None)  # Bolt at 100 directions (the key says so)
        head_label(ax, 52, "lens part written in", C["lens"])

    def needed(ax, _r):
        for i, (k, _) in enumerate(ZORD):
            mk, ct = D.b(f"ko.{k}.mk"), S.ctrl(k)
            if ct is not None:
                ax.plot([ct, ct], [i - 0.26, i + 0.26], color=C["control"], lw=2.4, zorder=3)
            dot(ax, mk[0], i, C["recall"], cell=mk, value=mk[0], vfmt="{:.0f}")
            if k == "q122":
                soft = D.b("ko.q122.soft")
                dot(
                    ax, soft[0], i, C["control"], size=7
                )  # the 122B scored by probability (a grey dot, the key says so)
        head_label(ax, 52, "lens part removed", C["recall"])

    def grades(i, _r):
        k = ZORD[i][0]
        g = grade[k]
        return [(g, INK if g == "clean" else MUTED, "bold" if g == "clean" else "normal")]

    t = Table(rows, [
        Col(3.4, "answers moved", "to the other entity's fact", carried, (-8, 80), [0, 40, 80], xlabel="points"),
        Col(3.4, "answers lost", "recall minus lookup", needed, (-3, 70), [0, 30, 60], xlabel="points"),
        Col(2.3, "Grade", "", grades, text=True),
    ], label_w=1.45, key=[("|", C["control"], "largest same-size control"), ("●", C["lens"], "at 100 directions"),
                          ("●", C["control"], "122B: scored by probability")])  # fmt: skip
    render(t, "f3_nine_models")


# ---- F5: what the lens part is (Dan's atoms) ------------------------------------------------------------------------
def f_atoms():
    q = "52 A: share of the rebuilt energy, "
    models = [(m, n) for m, n in DAN if D.s(m, q + "the old bridge word")]
    rows = [Row(NAME[m]) for m, _ in models]

    def stack(ax, _r):
        for i, (m, _) in enumerate(models):
            hol = D.hollow(m)  # post hoc: hollow segments (G1), not a tint
            segs = [(D.s(m, q + "the old bridge word")[0], C["recall"]), (D.s(m, q + "the new bridge word")[0], C["lens"]),
                    (D.s(m, q + "another scene word or its class")[0], "#9E9E9E"), (D.s(m, q + "no scene word")[0], "#DADADA")]  # fmt: skip
            x = 0
            for j, (v, col) in enumerate(segs):
                kw = {"facecolor": "white", "edgecolor": col, "linewidth": 2.0} if hol else {"color": col}
                ax.barh(i, v, left=x, height=0.62, zorder=3, **kw)
                if v >= 0.08:
                    tc = "white" if (j < 2 and not hol) else INK
                    ax.text(
                        x + v / 2,
                        i,
                        f"{v:.2f}",
                        ha="center",
                        va="center",
                        fontsize=12,
                        color=tc,
                        weight="bold",
                        zorder=4,
                    )
                x += v
        head_label(ax, 0.0, "old bridge word", C["recall"], ha="left")
        head_label(ax, 0.42, "new bridge word", C["lens"], ha="center")
        head_label(ax, 1.0, "no word of the scene", MUTED, ha="right", weight="normal")

    def answer(i, _r):
        v = D.s(models[i][0], q + "an answer word")[0]
        return [(clean(f"{v:.2f}"), INK, "bold")]

    t = Table(rows, [Col(7.2, "share of the rebuilt energy", "of the lens part's 25 directions, by the word each decodes to",
                         stack, (0, 1), [0, 0.5, 1], xlabel="share of the rebuilt energy"),
                     Col(1.3, "answer word", "share", answer, text=True)], label_w=1.45,
              key=[("●", "#9E9E9E", "another scene word")])  # fmt: skip
    render(t, "f5_atoms")


# ---- F6: the address, four columns (read / remove / swap / lens) ---------------------------------------------------
def f_address():
    rows = [Row(NAME[m]) for m, _ in DAN]
    short = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "qwen3.5-122b-a10b": "122b"}

    def removal_cells(m):
        if m == "nemotron-3.5-lightning":
            return (
                D.s(m, "another item moved, no_alf: position share"),
                D.s(m, "another item moved, no_alf_rand: position share"),
            )
        pre = "rtg_C2" if m == "qwen3.5-122b-a10b" else "rt_C2"
        return (D.x(f"{pre}_no_alf_position_{short[m]}"), D.x(f"{pre}_no_alf_rand_position_{short[m]}"))

    def probe(ax, _r):
        for i, (m, _) in enumerate(DAN):
            v = D.s(m, "the locker probe at the bridge word, locker-first scenes")
            base = D.s(m, "the locker probe's layout baseline, locker-first scenes")[0]
            ax.plot([base, base], [i - 0.26, i + 0.26], color=C["control"], lw=2.4, zorder=3)
            dot(ax, v[0], i, C["address"], D.hollow(m), cell=v, value=v[0], vside="left")
        head_label(ax, 0.53, "layout only", MUTED, weight="normal")
        head_label(ax, 0.96, "probe", C["address"])

    def remove(ax, _r):
        for i, (m, _) in enumerate(DAN):
            a, r = removal_cells(m)
            connector(ax, a[0], r[0], i)
            dot(ax, r[0], i, C["control"], size=8)
            dot(ax, a[0], i, C["address"], D.hollow(m, True), value=a[0], vside="left")
        head_label(ax, 0.0, "address removed", C["address"], ha="left")

    def swap(ax, _r):
        for i, (m, _) in enumerate(DAN):
            two = D.s(m, "lookup target share, mean over locker pairs, s = 2", "fig07")
            rnd = D.s(m, "lookup target share, random direction, s = 4", "fig07")
            connector(ax, rnd[0], two[0], i)
            dot(ax, rnd[0], i, C["control"], size=8)
            dot(ax, two[0], i, C["address"], D.hollow(m, True), value=two[0])
        head_label(ax, 0.62, "address swap", C["address"], ha="right")

    zq = "47.0 (b) share rebuilt by 25 lens directions: "

    def lens(ax, _r):
        band(ax, -1, 1, len(DAN))
        for i, (m, _) in enumerate(DAN):
            p, it = D.s(m, zq + "pointer: z", prefix=True), D.s(m, zq + "identity_mean: z", prefix=True)
            if not p:
                ax.text(-2.4, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                continue
            connector(ax, p[0], it[0], i)
            dot(ax, p[0], i, C["address"], D.hollow(m, True))  # the 122B: lookup-only gate, post hoc
            dot(ax, it[0], i, C["identity"], D.hollow(m, True), value=it[0], vfmt="{:.0f}")
        head_label(ax, 0, "swap", C["address"], ha="left")
        head_label(ax, 31, "item change", C["identity"], ha="right")

    t = Table(rows, [
        Col(2.35, "probe accuracy", "at the bridge word", probe, (0.4, 1.03), [0.5, 0.75, 1], xlabel="accuracy"),
        Col(2.35, "position answers", "lookups following the position", remove, (-0.2, 0.62), [0, 0.25, 0.5],
            xlabel="share of lookups"),
        Col(2.35, "lookups sent", "to the new locker", swap, (-0.03, 0.66), [0, 0.25, 0.5],
            xlabel="share of lookups"),
        Col(2.35, "lens rebuild", "z from 200 random vectors", lens, (-2.5, 34), [0, 10, 20],
            xlabel="z (distance from random)"),
    ], label_w=1.45, pad=0.22, key=[("●", C["control"], "a random part taken out (column 2), a random vector written in (column 3)"),
                                                  ("■", BAND, "range of the random vectors (column 4)")])  # fmt: skip
    render(t, "f6_address")


# ---- F8: where it breaks, two figures (review v3: two different findings) -------------------------------------------
def f_directions():
    """The 27B's lookup with more lens directions (the x-range reaches 0.95 so the 0.60 label stays inside, G10)."""
    short = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "qwen3.5-122b-a10b": "122b"}
    rows = [Row(NAME[m]) for m, _ in DAN]

    def kcol(k):
        def f(ax, _r):
            band(ax, -0.1, 0.1, len(DAN))
            for i, (m, _) in enumerate(DAN):
                c = D.x(f"lk_excess_k{k}_{short[m]}") if m in short else None
                if not c:
                    ax.text(-0.27, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                    continue
                dot(ax, c[0], i, C["lookup"], value=c[0], size=9.5 if c[0] > 0.1 else 8)

        return f

    t = Table(rows, [
        Col(2.45, "25 lens directions", "the lookup's loss", kcol(25), (-0.3, 0.95), [0, 0.5], xlabel="switches lost beyond random"),
        Col(2.45, "50 lens directions", "", kcol(50), (-0.3, 0.95), [0, 0.5], xlabel="switches lost beyond random"),
        Col(2.45, "100 lens directions", "", kcol(100), (-0.3, 0.95), [0, 0.5], xlabel="switches lost beyond random"),
    ], label_w=1.45, pad=0.22, labels=False, key=[BANDKEY])  # fmt: skip
    render(t, "f8_directions")


def f_facts():
    """The lookup on Zach's passages with true and with made-up facts."""
    rows = [Row(NAME[m]) for m, _ in DAN]
    q = "Zach's named passages, {} facts, lookup: switches lost beyond random"

    def zach(ax, _r):
        band(ax, -0.1, 0.1, len(DAN))
        for i, (m, _) in enumerate(DAN):
            tr, mu = D.s(m, q.format("true"), "ledger_zach_named"), D.s(m, q.format("made-up"), "ledger_zach_named")
            if not tr or m == "muse-glimmer-30b":  # Muse: under 30 lookup switches (ledger_zach_named)
                ax.text(-0.27, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                continue
            if mu:
                connector(ax, mu[0], tr[0], i)
                dot(ax, mu[0], i, C["lookup_light"], D.hollow(m), size=8)
            dot(ax, tr[0], i, C["lookup"], D.hollow(m), cell=tr, value=tr[0])

    t = Table(rows, [Col(7.0, "fact passages", "the lookup's switches lost without the lens part", zach, (-0.3, 0.9),
                         [0, 0.25, 0.5, 0.75], xlabel="switches lost beyond random")],
              label_w=1.45, labels=False,
              key=[("●", C["lookup"], "true facts"), ("●", C["lookup_light"], "made-up facts"), BANDKEY])  # fmt: skip
    render(t, "f8_facts")


# ---- F9: where in the prompt and in depth (Zach) --------------------------------------------------------------------
def f_where():
    models = [("q9", "Qwen 9B"), ("q27", "Qwen 27B"), ("mu", "Muse 30B"), ("nl", "Lightning")]
    rows = [Row(n) for _, n in models]
    keys = {"mid": ("pos.{}.all.all", "pos.{}.all.bridge", "pos.{}.all.question"),
            "late": ("late.{}.all", "late.{}.bridge", "late.{}.question")}  # fmt: skip

    def col(band_, j):
        def f(ax, _r):
            for i, (k, _) in enumerate(models):
                key = keys[band_][j].format(k)
                if k == "mu":
                    key = {"late": ("ko.mu.mk", "pos.mu.bridge", "pos.mu.question")}.get(band_, ("", "", ""))[j]
                c = D.b(key) if key else None
                if not c:
                    ax.text(2, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                    continue
                col_ = C["recall"] if j == 0 else (C["mention"] if j == 1 else C["question"])
                if band_ == "late" and j:  # the rotated control (at most 2.5 points), where it was run
                    rot = D.b(keys[band_][j].format(k) + ".rot")
                    if rot:
                        dot(ax, rot[0], i, C["control"], size=7)
                dot(ax, c[0], i, col_, cell=c, value=c[0], vfmt="{:.0f}", size=9.5 if c[0] > 15 else 8)

        return f

    names = ["all tokens", "mention", "question"]
    cols = [
        Col(1.55, f"{n}", "removed at", col("mid", j), (-3, 72), [0, 50], xlabel="points") for j, n in enumerate(names)
    ]
    cols += [
        Col(1.55, f"{n}", "removed at", col("late", j), (-3, 72), [0, 50], xlabel="points") for j, n in enumerate(names)
    ]
    t = Table(
        rows,
        cols,
        label_w=1.35,
        pad=0.2,
        labels=False,
        head=1.25,
        key=[
            ("●", C["recall"], "all tokens"),
            ("●", C["mention"], "the bridge's mention"),
            ("●", C["question"], "the question"),
            ("●", C["control"], "rotated control (deeper layers)"),
        ],
    )
    t.extra.append(
        lambda fig: [
            fig.text(
                (t.label_w + t.pad + (sum(c.width for c in t.cols[:3]) + 3 * t.pad) * g)
                / (t.label_w + sum(c.width for c in t.cols) + t.pad * 7),
                1 - 0.12 / fig.get_figheight(),
                w,
                ha="left",
                va="top",
                fontsize=12.5,
                weight="bold",
                color=INK,
            )
            for g, w in enumerate(["Middle layers (the knock-out band)", "Deeper layers"])
        ]
    )
    render(t, "f9_where")


# ---- F11: the monitor probe (Dan) ----------------------------------------------------------------------------------
def f_monitor():
    models = [
        (m, n) for m, n in DAN if D.s(m, "the address at the last token, main test, 25 lens directions: the J++ part")
    ]
    rows = [Row(NAME[m]) for m, _ in models]

    def kcol(k):
        q = f"the address at the last token, main test, {k} lens directions: "

        def f(ax, _r):
            for i, (m, _) in enumerate(models):
                full, jpp = D.s(m, q + "the full state"), D.s(m, q + "the J++ part")
                _rsz, ren = D.s(m, q + "a random part (same size)"), D.s(m, q + "a random part (same energy)")
                ax.plot([full[0], full[0]], [i - 0.26, i + 0.26], color=INK, lw=2.2, zorder=3)
                connector(ax, jpp[0], ren[0], i)
                dot(ax, ren[0], i, "#7A7A7A", size=8)
                dot(ax, jpp[0], i, C["lens"], D.hollow(m), cell=jpp, value=jpp[0], vside="left")

        return f

    t = Table(rows, [Col(4.0, "25 lens directions", "probe accuracy for the address at the last token",
                         kcol(25), (0.4, 1.02), [0.5, 0.75, 1], xlabel="accuracy"),
                     Col(4.0, "100 lens directions", "", kcol(100), (0.4, 1.02), [0.5, 0.75, 1], xlabel="accuracy")], label_w=1.45, labels=False,
              key=[("●", C["lens"], "the lens part"), ("●", "#7A7A7A", "a random part of the same energy"),
                   ("|", INK, "the full state")])  # fmt: skip
    render(t, "f11_monitor")


# ---- F12: question before or after the scene (Dan), all five models --------------------------------------------------
def f_order():
    """The lookup and the recall without the lens part, with the question after the scene (the main test) and before it.
    Question before ran on the 27B and the 122B only (its gate: the recall must read the original prompts right); the
    others say so in the cell. The 27B's rule was set after its cells (post hoc, hollow)."""
    stem = "question {} the scene: {}, switches lost beyond a random part"
    gate = "question before the scene: the recall's gate (read right on the original prompts)"
    models = list(DAN)
    rows = []
    for m, _ in models:
        rows += [Row(NAME[m], sub="lookup"), Row("", sub="recall")]
    post_hoc = lambda m: D.hollow(m) or m == "qwen3.6-27b"  # noqa: E731
    reader_col = {"lookup": (C["lookup_light"], C["lookup"]), "recall": (C["recall_light"], C["recall"])}

    def lk(ax, _r):
        band(ax, -0.1, 0.1, len(rows))
        for i, (m, _) in enumerate(models):
            for j, reader in enumerate(("lookup", "recall")):
                y = 2 * i + j
                a, b = D.s(m, stem.format("after", reader)), D.s(m, stem.format("before", reader))
                light, dark = reader_col[reader]
                if b:
                    connector(ax, a[0], b[0], y)
                before_right = bool(b) and b[0] >= a[0]  # each dot's label on the side away from the other dot
                dot(ax, a[0], y, light, post_hoc(m), size=8.5, value=a[0], vside="left" if before_right else "right")
                if b:
                    dot(ax, b[0], y, dark, post_hoc(m), cell=b, value=b[0], vside="right" if before_right else "left")
                elif j == 0 and (g := D.s(m, gate)):
                    ax.text(0.3, y, f"below gate ({g[0]:.2f})", ha="left", va="center", fontsize=10.5, color=MUTED)

    def diff(i, _r):
        m, reader = models[i // 2][0], ("lookup", "recall")[i % 2]
        if reader == "recall":
            return [("", MUTED, "normal")]
        d = D.s(m, "the lookup, question before minus after (paired)")
        if not d:
            return [("can't tell", MUTED, "normal")]
        return [(f"{d[0]:+.2f}", INK, "bold"), (f"  [{d[1]:.2f}, {d[2]:.2f}]", MUTED, "normal")]

    t = Table(rows, [Col(5.0, "without the lens part", "switches lost beyond a random part", lk, (-0.25, 0.95), [0, 0.5],
                         xlabel="switches lost beyond random (share)"),
                     Col(2.1, "before − after", "paired, 95% interval", diff, text=True)], label_w=1.45,
              group=2, key=[[("●", C["lookup"], "lookup"), ("●", C["recall"], "recall"),
                             ("", MUTED, "lighter: question after · darker: question before"),
                             ("■", BAND, "within 0.10 of a random part")],
                            [("○", INK, "post hoc: the 27B's rule was set after its cells; Lightning's gate after its pre-check")]])  # fmt: skip
    render(t, "f12_order")


if __name__ == "__main__":
    X.r1_split()
    X.r3_last_token()
    X.r4_pointer()
    X.r5_routes()
    for f in (f_controls, f_nine, f_atoms, f_address, f_directions, f_facts, f_where, f_monitor, f_order):
        f()
        print("ok", f.__name__)
