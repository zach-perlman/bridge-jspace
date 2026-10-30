"""Every figure of the deck (v2), in the table style of figures/depth/fig00_setup.png, from the repo's data.
Run from the repo root:  PYTHONPATH=src:<this dir> python3 deck_figs.py OUTDIR [--target slide|readme]
Uses dottable.py (the component) and exemplars.py (r1-r5)."""

from __future__ import annotations

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import exemplars as X
from bridge_jspace.figkit import specs as S
from bridge_jspace.figkit.dottable import (
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
    under,
)

OUT = "."  # set by bridge_jspace.figkit.tables
DPI = 160
NAME, DAN, ZK = X.NAME, X.DAN, X.ZK


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

    cols = [Col(1.38, n, "points" if j == 0 else "", zcol(k, c), (-3, 70), [0, 50]) for j, (n, k, c) in enumerate(zach)]
    cols += [
        Col(1.38, n, "share" if j == 0 else "", dcol(q, c), (-0.05, 0.85), [0, 0.5]) for j, (n, q, c) in enumerate(dq)
    ]
    t = Table(rows, cols, label_w=1.45, pad=0.18, labels=False, head=1.25)

    def group_titles(fig):
        w = t.label_w + sum(c.width for c in t.cols) + t.pad * (len(t.cols) + 1)
        x0 = (t.label_w + t.pad) / w
        x1 = (t.label_w + t.pad * 5 + sum(c.width for c in t.cols[:4])) / w
        fig.text(x0, 1 - 0.12 / fig.get_figheight(), "Removed everywhere, over a band (recalled − stated lost)", ha="left", va="top",
                 fontsize=12.5, color=INK, weight="bold")  # fmt: skip
        fig.text(x1, 1 - 0.12 / fig.get_figheight(), "Removed from the patch (recall's switches lost)", ha="left", va="top",
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
    rows = [Row(n) for _, n in D.ZACH]

    def carried(ax, _r):
        for i, (k, _) in enumerate(D.ZACH):
            c = D.b(swapkey.get(k, f"swap.{k}.swap"))
            if not c:
                ax.text(-6, i, "–", ha="left", va="center", fontsize=12, color=MUTED)
                continue
            dot(ax, c[0], i, C["lens"], cell=c, value=c[0], vfmt="{:.0f}")
            if k == "nb":
                c100 = D.b("swap.nb.k100.swap")
                dot(ax, c100[0], i, C["lens"], size=6, value=None)
                ax.text(c100[0], i - 0.32, "100 dirs", ha="center", va="bottom", fontsize=10, color=MUTED)
        head_label(ax, 52, "lens part written in", C["lens"])

    def needed(ax, _r):
        for i, (k, _) in enumerate(D.ZACH):
            mk, ct = D.b(f"ko.{k}.mk"), S.ctrl(k)
            if ct is not None:
                ax.plot([ct, ct], [i - 0.26, i + 0.26], color=C["control"], lw=2.4, zorder=3)
            dot(ax, mk[0], i, C["recall"], cell=mk, value=mk[0], vfmt="{:.0f}")
            if k == "q122":
                soft = D.b("ko.q122.soft")
                dot(ax, soft[0], i, C["recall"], hollow=True, size=7.5)
                ax.text(soft[0], i - 0.32, "by probability", ha="left", va="bottom", fontsize=10, color=MUTED)
        head_label(ax, 52, "lens part removed", C["recall"])
        head_label(ax, 0, "control", MUTED, ha="left", weight="normal")

    def grades(i, _r):
        k = D.ZACH[i][0]
        g = grade[k]
        return [(g, INK if g == "clean" else MUTED, "bold" if g == "clean" else "normal")]

    t = Table(rows, [
        Col(3.4, "Carried", "answers moved to the other entity, points", carried, (-8, 80), [0, 40, 80]),
        Col(3.4, "Needed", "recalled minus stated answers lost, points", needed, (-3, 70), [0, 30, 60]),
        Col(2.3, "Grade", "", grades, text=True),
    ], label_w=1.45)  # fmt: skip
    render(t, "f3_nine_models")


# ---- F5: what the lens part is (Dan's atoms) ------------------------------------------------------------------------
def f_atoms():
    q = "52 A: share of the rebuilt energy, "
    models = [(m, n) for m, n in DAN if D.s(m, q + "the old bridge word")]
    rows = [Row(NAME[m]) for m, _ in models]

    def stack(ax, _r):
        for i, (m, _) in enumerate(models):
            a = 0.45 if D.hollow(m) else 1.0
            segs = [(D.s(m, q + "the old bridge word")[0], C["recall"]), (D.s(m, q + "the new bridge word")[0], C["lens"]),
                    (D.s(m, q + "another scene word or its class")[0], "#9E9E9E"), (D.s(m, q + "no scene word")[0], "#DADADA")]  # fmt: skip
            x = 0
            for j, (v, col) in enumerate(segs):
                ax.barh(i, v, left=x, height=0.62, color=col, alpha=a if j < 2 else 1, zorder=3)
                if v >= 0.08:
                    tc = "white" if (j < 2 and a == 1) else INK
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

    t = Table(rows, [Col(7.2, "What the lens part's 25 directions are", "share of the energy they rebuild, by the word "
                         "each direction decodes to", stack, (0, 1), [0, 0.5, 1]),
                     Col(1.3, "answer word", "share", answer, text=True)], label_w=1.45)  # fmt: skip
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
        head_label(ax, 0.0, "removed", C["address"], ha="left")
        head_label(ax, 0.62, "random", MUTED, ha="right", weight="normal")

    def swap(ax, _r):
        for i, (m, _) in enumerate(DAN):
            two = D.s(m, "lookup target share, mean over locker pairs, s = 2", "fig07")
            rnd = D.s(m, "lookup target share, random direction, s = 4", "fig07")
            connector(ax, rnd[0], two[0], i)
            dot(ax, rnd[0], i, C["control"], size=8)
            dot(ax, two[0], i, C["lookup"], D.hollow(m, True), value=two[0])
        head_label(ax, 0.0, "random", MUTED, ha="left", weight="normal")
        head_label(ax, 0.46, "address swap", C["lookup"])

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
        head_label(ax, 20, "item change", C["identity"])
        under(ax, 0, "grey band: random vectors")

    t = Table(rows, [
        Col(2.35, "A probe reads it", "accuracy at the bridge word", probe, (0.4, 1.03), [0.5, 0.75, 1]),
        Col(2.35, "Removing it", "lookups answering by position", remove, (-0.2, 0.62), [0, 0.25, 0.5]),
        Col(2.35, "A swap moves it", "lookups sent to the new locker", swap, (-0.03, 0.62), [0, 0.25, 0.5]),
        Col(2.35, "The lens misses it", "z above random vectors", lens, (-2.5, 26), [0, 10, 20]),
    ], label_w=1.45, pad=0.22)  # fmt: skip
    render(t, "f6_address")


# ---- F8: where it breaks --------------------------------------------------------------------------------------------
def f_breaks():
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
                strong = c[0] > 0.1
                dot(ax, c[0], i, C["lookup"], value=c[0], size=9.5 if strong else 8)

        return f

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
                dot(ax, mu[0], i, C["control"], D.hollow(m), size=8, cell=None)
            dot(ax, tr[0], i, C["lookup"], D.hollow(m), cell=tr, value=tr[0])
        head_label(ax, 0.12, "made-up facts", MUTED, ha="right", weight="normal")
        head_label(ax, 0.2, "true facts", C["lookup"], ha="left")
        under(ax, 0, "grey band: not needed")

    t = Table(rows, [
        Col(1.75, "25 lens dirs", "the lookup's loss", kcol(25), (-0.3, 0.8), [0, 0.5]),
        Col(1.75, "50", "", kcol(50), (-0.3, 0.8), [0, 0.5]),
        Col(1.75, "100", "", kcol(100), (-0.3, 0.8), [0, 0.5]),
        Col(3.6, "Fact passages", "the lookup's switches lost without the lens part", zach, (-0.3, 0.85), [0, 0.5]),
    ], label_w=1.45, pad=0.22, labels=True)  # fmt: skip
    render(t, "f8_breaks")


# ---- F9: where in the prompt and in depth (Zach) --------------------------------------------------------------------
def f_where():
    models = [("q27", "Qwen 27B"), ("q9", "Qwen 9B"), ("nl", "Lightning"), ("mu", "Muse 30B")]
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
                col_ = C["recall"] if j == 0 else (C["lens"] if j == 1 else C["lookup"])
                dot(ax, c[0], i, col_, cell=c, value=c[0], vfmt="{:.0f}", size=9.5 if c[0] > 15 else 8)

        return f

    names = ["all tokens", "mention", "question"]
    cols = [Col(1.55, f"{n}", "pp" if j == 0 else "", col("mid", j), (-3, 72), [0, 50]) for j, n in enumerate(names)]
    cols += [Col(1.55, f"{n}", "pp" if j == 0 else "", col("late", j), (-3, 72), [0, 50]) for j, n in enumerate(names)]
    t = Table(rows, cols, label_w=1.35, pad=0.2, labels=False, head=1.25)
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
                         kcol(25), (0.4, 1.02), [0.5, 0.75, 1]),
                     Col(4.0, "100 lens directions", "", kcol(100), (0.4, 1.02), [0.5, 0.75, 1])], label_w=1.45, labels=False,
              key=[("●", C["lens"], "the lens part"), ("●", "#7A7A7A", "a random part of the same energy"),
                   ("|", INK, "the full state"), ("○", C["lens"], "post hoc")])  # fmt: skip
    render(t, "f11_monitor")


# ---- F12: question before or after the scene (Dan) ------------------------------------------------------------------
def f_order():
    models = [(m, n) for m, n in DAN if D.s(m, "question before the scene: lookup, switches lost beyond a random part")]
    rows = [Row(NAME[m]) for m, _ in models]

    def lk(ax, _r):
        band(ax, -0.1, 0.1, len(models))
        for i, (m, _) in enumerate(models):
            a = D.s(m, "question after the scene: lookup, switches lost beyond a random part")
            b = D.s(m, "question before the scene: lookup, switches lost beyond a random part")
            connector(ax, a[0], b[0], i)
            dot(ax, a[0], i, C["control"], size=8)
            dot(ax, b[0], i, C["lookup"], cell=b, value=b[0])
        head_label(ax, 0.13, "question after", MUTED, ha="right", weight="normal")
        head_label(ax, 0.2, "question before", C["lookup"], ha="left")

    def diff(i, _r):
        d = D.s(models[i][0], "the lookup, question before minus after (paired)")
        return [(f"{d[0]:+.2f}", INK, "bold"), (f"  [{d[1]:.2f}, {d[2]:.2f}]", MUTED, "normal")]

    t = Table(rows, [Col(4.5, "The lookup without the lens part", "switches lost beyond a random part", lk, (-0.25, 0.6),
                         [0, 0.25, 0.5]),
                     Col(2.0, "before − after", "paired, 95%", diff, text=True)], label_w=1.45)  # fmt: skip
    render(t, "f12_order")


if __name__ == "__main__":
    X.r1_split()
    X.r2_address()
    X.r3_last_token()
    X.r4_pointer()
    X.r5_routes()
    for f in (f_controls, f_nine, f_atoms, f_address, f_breaks, f_where, f_monitor, f_order):
        f()
        print("ok", f.__name__)
