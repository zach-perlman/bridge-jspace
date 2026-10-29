"""The deck's and the root README's figures as specs: data and words only. To change what a figure shows, edit its
function here; to change how every figure looks, edit src/bridge_jspace/figkit/theme.py; to change a component, render.py.
Each function returns a Figure; SPECS maps id -> function (order = the deck's)."""

from __future__ import annotations

import re

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit.spec import Bars, Curves, Figure, Image, Line, Multiples, Rule, Series, Stacked

NOT_NEEDED = Rule(0.10, "not needed")


def ctrl(m: str) -> float | None:
    """Zach's largest same-size control in M - K: max of rotated, logit lens, PCA (or the size-matched ratio x mk)."""
    pc, pcr, mk = D.b(f"ko.{m}.pc"), D.b(f"ko.{m}.pcr"), D.b(f"ko.{m}.mk")
    vals = [v[0] for v in (D.b(f"ko.{m}.rot"), D.b(f"ko.{m}.u")) if v]
    vals.append(pc[0] if pc else (pcr[0] * mk[0] if pcr and mk else None))
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None


def conflict(m: str, reader: str):
    key = {"recall": "rc", "lookup": "lk"}[reader]
    return D.x(f"{key}_excess_{D.SHORT.get(m, '-')}") or D.s(
        m, f"conflict: {reader}, switches lost beyond a random part"
    )


def lightning_hollow(models) -> set:
    return {m for m, _ in models if D.hollow(m)}


# ---- slides 2, 3 ----------------------------------------------------------------------------------------------------
def setup_datasets() -> Figure:
    return Figure("p0a_datasets", "One question, two kinds of answer, two datasets.",
                  "figures/shared/j0_setup.png, its top half (a diagram, not re-drawn).",
                  [Image("figures/shared/j0_setup.png", (0, 0.5))])  # fmt: skip


def setup_tools() -> Figure:
    return Figure("p0b_tools", "Three tools, one target: the lens part at the bridge.",
                  "figures/shared/j0_setup.png, its bottom half (a diagram, not re-drawn).",
                  [Image("figures/shared/j0_setup.png", (0.5, 1))])  # fmt: skip


# ---- slide 4: C1 ----------------------------------------------------------------------------------------------------
def c1_split() -> Figure:
    zc = [(m, n) for m, n in D.ZACH if m in ("q27", "q9", "nl", "mu", "q122")]
    left = Bars(zc, [Series("recall", "recall", {m: D.b(f"ko.{m}.lostM") for m, _ in zc}),
                     Series("lookup", "lookup", {m: D.b(f"ko.{m}.lostK") for m, _ in zc})],
                "answers that turn wrong (pp)", (-3, 72), "{:.1f}", ticks={m: ctrl(m) for m, _ in zc}, rotate=15)  # fmt: skip
    hol = lightning_hollow(D.DAN)
    rc = {m: conflict(m, "recall") for m, _ in D.DAN}
    lk = {m: conflict(m, "lookup") for m, _ in D.DAN}
    gap = {m: (D.x(f"contrast_{D.SHORT.get(m, '-')}") or (rc[m][0] - lk[m][0],))[0] for m, _ in D.DAN}
    right = Bars(D.DAN, [Series("recall", "recall", rc, hol), Series("lookup", "lookup", lk, hol)],
                 "switches lost beyond a random part", (-0.2, 1.05), gap=gap, rules=[NOT_NEEDED], rotate=15)  # fmt: skip
    return Figure("p1_c1_split", "Recall needs the lens part; lookup does not.",
                  "Left (Zach, pp): the lens part's top-10 J++ directions removed at every token over his band; points "
                  "lost on recalled (M, dark) and stated (K, purple) finals (docs/breadth/data.csv ko.*.lostM / lostK); "
                  "grey tick: the largest same-size control in M − K (rotated, logit lens, PCA). Muse 30B: shared with "
                  "the logit lens; Qwen 122B: gone by probability (Zach's grading). Right (Dan, share): the conflict "
                  "test at L, switches lost beyond a random part (docs/x0_numbers.json rc_excess_* / lk_excess_*; "
                  "Lightning from figures/story/data.csv), 200 scenes per model, 95% whiskers; bold: recall minus "
                  "lookup (contrast_*); dashed: the lookup's 0.10 bar. Lightning hollow (gate chosen after its "
                  "pre-check; pending hand-check, 29 Oct).", [left, right])  # fmt: skip


# ---- slide 5: controls ----------------------------------------------------------------------------------------------
def controls_zach() -> Figure:
    conds = ["lens\npart", "rotated", "logit\nlens", "PCA"]
    data = {m: dict(zip(conds, (D.b(f"ko.{m}.mk"), D.b(f"ko.{m}.rot"), D.b(f"ko.{m}.u"), D.b(f"ko.{m}.pc")), strict=True))
            for m, _ in D.ZACH[:3]}  # fmt: skip
    colors = {"lens\npart": "lens", "rotated": "control", "logit\nlens": "control", "PCA": "control"}
    return Figure("p2a_controls_zach", "Same-size parts do not do it (Zach).",
                  "Recalled minus stated answers lost when the lens part's top-10 J++ directions are removed over his "
                  "band (teal, 95% whiskers) against rotated directions, the logit lens's top 10 and same-norm PCA "
                  "directions (grey; docs/breadth/data.csv ko.*.rot / u / pc), on the three clean models.",
                  [Multiples(D.ZACH[:3], conds, data, colors, "recalled minus stated answers lost (pp)", (-3, 60), "{:.1f}")])  # fmt: skip


def controls_dan() -> Figure:
    qs = {"lens\npart": "J++ part: recall extra loss", "PCA": "PCA directions (same size): recall extra loss",
          "logit\nlens": "logit-lens directions: recall extra loss", "random\nlens": "random lens directions: recall extra loss"}  # fmt: skip
    models = [(m, n) for m, n in D.DAN if D.s(m, qs["lens\npart"], "fig02")]
    data = {m: {c: D.s(m, q, "fig02") for c, q in qs.items()} for m, _ in models}
    colors = {c: ("lens" if c == "lens\npart" else "control") for c in qs}
    return Figure("p2b_controls_dan", "Same-size parts do not do it (Dan).",
                  "The recall's switches lost beyond a random part without the lens part's 25 directions (teal, 95% "
                  "whiskers) against same-size PCA directions, the logit lens's directions and random lens directions "
                  "(grey), main test at L, 200 scenes (figures/story/data.csv fig02 rows). On the 122B the PCA control "
                  "is close (0.21 vs 0.26). Lightning has no fig02 row.",
                  [Multiples(models, list(qs), data, colors, "recall: switches lost beyond a random part", (-0.1, 0.85))])  # fmt: skip


def graded_nine() -> Figure:
    grade = ["clean", "clean", "clean", "weak", "weak", "not specific", "carried, not needed", "shared with logit lens",
             "by probability"]  # fmt: skip
    p = Bars(D.ZACH, [Series("lens part", "recall", {m: D.b(f"ko.{m}.mk") for m, _ in D.ZACH})],
             "recalled minus stated answers lost (pp)", (-3, 70), "{:.1f}", rules=[Rule(30, "the plan's bar")],
             ticks={m: ctrl(m) for m, _ in D.ZACH}, under=dict(zip([m for m, _ in D.ZACH], grade, strict=True)))  # fmt: skip
    return Figure("p3_graded_nine", "Across nine models it is graded.",
                  "Zach: recalled minus stated answers lost without the lens part's top-10 directions over his band "
                  "(dark, 95% whiskers; ko.*.mk) against the largest same-size control (grey tick); his grade under each "
                  "model; dashed: the plan's +30 bar. The 122B scored by probability: 1.7 (ko.q122.soft). Gemma 4, "
                  "gpt-oss and Kolibri cannot be tested (the removal breaks plain text).", [p])  # fmt: skip


# ---- slide 6: C2 ----------------------------------------------------------------------------------------------------
def pointer_zach() -> Figure:
    conds = ["own\npassage", "neutral\nsentence", "no own-\nword dirs", "rotated", "probe\nsubspace"]
    data = {}
    for m, _ in D.ZACH[:3]:
        own = D.b(f"ptr.{m}.swap")
        data[m] = dict(zip(conds, (own, D.scaled(own, D.b(f"ptr.{m}.neutral")[0]), D.scaled(own, D.b(f"ptr.{m}.noown")[0]),
                                   D.b(f"ptr.{m}.rot"), D.b(f"probe.{m}.probe")), strict=True))  # fmt: skip
    colors = dict(zip(conds, ("lens", "lens", "lens", "control", "lookup"), strict=True))
    return Figure("p4a_pointer_zach", "The lens part says which entity it is: a pointer, from any context.",
                  "Zach: another entity D's lens part written in over his band; answers moved to D's fact when the part "
                  "comes from D's own passage (95% whiskers), one neutral sentence about D, without D's own-word "
                  "directions, the neutral donor rotated (grey), and a probe's subspace that reads the fact (purple; "
                  "probe-valid relations). docs/breadth/data.csv ptr.*, probe.*.probe; the neutral and own-word bars are "
                  "ptr.*.swap times the stored ratios (no interval). Cross-relation and paste rows dropped.",
                  [Multiples(D.ZACH[:3], conds, data, colors, "answers moved to D's fact (points)", (-5, 85), "{:.0f}")])  # fmt: skip


def atoms_dan() -> Figure:
    q = "52 A: share of the rebuilt energy, "
    models = [(m, n) for m, n in D.DAN if D.s(m, q + "the old bridge word")]
    seg = lambda label, color, kind: (label, color, {m: D.s(m, q + kind)[0] for m, _ in models})  # noqa: E731
    segs = [seg("old bridge word", "recall", "the old bridge word"), seg("new bridge word", "lens", "the new bridge word"),
            seg("another scene word", "rule", "another scene word or its class"), seg("no scene word", "control", "no scene word")]  # fmt: skip
    ans = ", ".join(f"{n} {D.s(m, q + 'an answer word')[0]:.2f}" for m, n in models)
    return Figure("p4b_atoms_dan", "The lens part's 25 directions are the bridge words, never the answer.",
                  f"Dan: share of the rebuilt energy by the kind of lens word, main test at L, 50 scenes per model "
                  f"(figures/story/data.csv 52 A rows). The answer word's share: {ans}. Lightning hollow (pending "
                  f"hand-check, 29 Oct); the 122B has no 52 A row in the depth README.",
                  [Stacked(models, segs, "share of the lens part's rebuilt energy", lightning_hollow(models), rotate=20)],
                  size="half")  # fmt: skip


# ---- slide 7: C3 ----------------------------------------------------------------------------------------------------
def probe() -> Figure:
    q = "the locker probe at the bridge word, locker-first scenes"
    cats = list(D.DAN) + [("tool", "27B tool output"), ("code", "27B code")]
    cells = {m: D.s(m, q) for m, _ in D.DAN} | {
        k: D.s("qwen3.6-27b", f"code and tool output, {k}: {q}") for k in ("tool", "code")
    }
    base = D.s("qwen3.5-9b", "the locker probe's layout baseline, locker-first scenes")[0]
    p = Bars(cats, [Series("", "address", cells, lightning_hollow(D.DAN))], "probe accuracy (share of scenes)", (0, 1.08),
             rules=[Rule(base, "layout baseline")], divider=len(D.DAN) - 0.5, rotate=15)  # fmt: skip
    return Figure("p5a_probe", "A probe at the bridge word reads which locker sentence holds the item's locker.",
                  "Locker-first scenes (657-758 per model); dashed: the layout baseline; right of the line: the 27B's "
                  "tool output (1,500 scenes) and code (682), lookup-only gate. Lightning hollow; the 122B's probe ran "
                  "at its gate (filled). Tool output and code: pending hand-check (29 Oct).", [p])  # fmt: skip


def swap_dose() -> Figure:
    panels, rnd = [], 0.0
    for m, name in D.DAN:
        pts = [(D.s(m, f"dose (s / mean s*), s = {s}", "fig07"), D.s(m, f"lookup target share, mean over locker pairs, s = {s}", "fig07"), s)
               for s in (1, 2, 4)]  # fmt: skip
        pts = [(d[0], v[0], s) for d, v, s in pts if d and v]
        two = next(p for p in pts if p[2] == 2)
        panels.append((name, [Line("", "lookup", [p[0] for p in pts], [p[1] for p in pts], thin=D.hollow(m, True),
                                   mark={two[0]: two[1]})]))  # fmt: skip
        r = D.s(m, "lookup target share, random direction, s = 4", "fig07")
        rnd = max(rnd, r[0] if r else 0)
    p = Curves(panels, "dose (a real change = 1)", "lookups to the swapped-in locker", (-0.02, 0.85), band=(-0.02, rnd + 0.02),
               vline=(1, "a real change"))  # fmt: skip
    return Figure("p5b_swap_dose", "The address swap moves the lookup.",
                  "Lookups answering the swapped-in locker by dose (s / the mean real change; figures/story/data.csv "
                  "fig07), 600 swaps per dose and model; dot: s = 2 (about a real change's size) with its value; grey "
                  "band: a random vector at s = 4; dashed: a real change. The swap's rule fixed in advance was read at "
                  "s = 1 and said no on every model (a design error). Lightning and the 122B thinner (after the data; "
                  "the 122B's gate lowered to 0.75).", [p])  # fmt: skip


def lens_readout() -> Figure:
    zq = "47.0 (b) share rebuilt by 25 lens directions: "
    models = [(m, n) for m, n in D.DAN if D.s(m, zq + "pointer: z", prefix=True)]
    pz = {m: D.s(m, zq + "pointer: z", prefix=True)[:1] + (None, None) for m, _ in models}
    iz = {m: D.s(m, zq + "identity_mean: z", prefix=True)[:1] + (None, None) for m, _ in models}
    hol = lightning_hollow(models)
    p = Bars(models, [Series("address swap", "address", pz, hol), Series("item change", "identity", iz, hol)],
             "lens rebuild above random vectors (z)", (-2, 26), "{:.1f}", band=(-1, 1), rotate=20)  # fmt: skip
    return Figure("p5c_lens_readout", "The lens cannot see the address.",
                  "How far above 200 random vectors of the same size the lens's 25 directions rebuild the address swap "
                  "(orange) and an item change of the same size (blue, the positive control), in z (grey band: the "
                  "random vectors' 95% range); 200 cases per model (figures/story/data.csv fig07b_verbal). Lightning "
                  "hollow; the 122B has no 47.0 run in the depth README.", [p], size="half")  # fmt: skip


# ---- slide 8: C4 ----------------------------------------------------------------------------------------------------
def readable() -> Figure:
    rows = []
    for m, name in D.DAN:
        read = D.s_match(
            m, r"51\.10: recall, last token, read peak layer \d+: the probe's accuracy", "fig17_jspace_last_token"
        )
        swap = D.s_match(
            m,
            r"51\.10: recall, last token, read peak layer \d+: the lens swap's switches over",
            "fig17_jspace_last_token",
        )
        if read and swap:
            rows.append((m, name, re.search(r"layer (\d+)", read[0]).group(1), read[1], swap[1]))
    cats = [(m, n) for m, n, *_ in rows]
    chance = max(D.s(m, "51.10: the read probe's chance (locker-first rows)")[0] for m, *_ in rows)
    hol = lightning_hollow(cats)
    p = Bars(cats, [Series("read", "recall", {m: r for m, _, _, r, _ in rows}, hol),
                    Series("lens swap", "lens", {m: w for m, _, _, _, w in rows}, hol)], "share", (0, 1.1),
             rules=[Rule(chance, "chance")], under={m: f"L{lay}" for m, _, lay, *_ in rows}, rotate=15)  # fmt: skip
    return Figure("p6_c4_readable", "Readable is not used.",
                  "At the last token, at the layer where the read peaks (under each model): read = a probe for the "
                  "recall's bridge entity on the lens part of the state (dark); lens swap = the changed prompt's lens "
                  "part swapped in, its switches as a share of the whole-state patch's, which switches 0.95-1.00 (teal); "
                  "dashed: the probe's chance. Locker-first items (figures/story/data.csv fig17_jspace_last_token). "
                  "Rule: '(b) readable, not used' on all four. Lightning hollow (pending hand-check, 29 Oct); the 122B "
                  "has no 51.10 run in the depth README.", [p], size="half")  # fmt: skip


# ---- slide 9: where it breaks ---------------------------------------------------------------------------------------
def breaks() -> Figure:
    ks = [25, 50, 100]
    lines = [Line(name, col, ks, [D.x(f"lk_excess_k{k}_{m}")[0] for k in ks], values=True)
             for m, name, col in (("27b", "Qwen 27B", "lookup"), ("122b", "Qwen 122B", "rule"))]  # fmt: skip
    left = Curves([("", lines)], "lens directions taken out", "lookup: switches lost beyond a random part", (-0.2, 0.7),
                  xlim=(20, 120), xticks=ks, rules=[NOT_NEEDED])  # fmt: skip
    models = D.DAN[:4]
    q = "Zach's named passages, {} facts, lookup: switches lost beyond random"
    cell = lambda m, w: D.s(m, q.format(w), "ledger_zach_named")  # noqa: E731
    hol = lightning_hollow(models)
    right = Bars(models, [Series("true facts", "lookup", {m: cell(m, "true") for m, _ in models if cell(m, "true")}, hol),
                          Series("made-up facts", "recall", {m: cell(m, "made-up") for m, _ in models if cell(m, "made-up")}, hol)],
                 "lookup: switches lost beyond a random part", (-0.15, 0.7), rules=[NOT_NEEDED], rotate=15)  # fmt: skip
    return Figure("p7_breaks", "Where it breaks: the 27B with more directions; passages whose fact the model knows.",
                  "Left: the lookup's switches lost beyond a random part without 25 / 50 / 100 lens directions, main "
                  "test at L, 200 scenes (docs/x0_numbers.json lk_excess_k*). Right: Zach's named passages through "
                  "Dan's conflict test, the lookup with true facts (purple) and made-up facts (dark) (figures/story/"
                  "data.csv ledger_zach_named). Muse and Lightning missed the made-up-fact gate (descriptive); Lightning "
                  "hollow (pending hand-check, 29 Oct). Dashed: the lookup's 0.10 bar.", [left, right])  # fmt: skip


# ---- backups --------------------------------------------------------------------------------------------------------
def where() -> Figure:
    models = [("q27", "Qwen 27B"), ("q9", "Qwen 9B"), ("nl", "Lightning"), ("mu", "Muse 30B")]
    conds = ["mid\nall", "mid\nmention", "mid\nquestion", "late\nall", "late\nmention", "late\nquestion"]
    data = {}
    for m, _ in models:
        keys = [
            f"pos.{m}.all.all",
            f"pos.{m}.all.bridge",
            f"pos.{m}.all.question",
            f"late.{m}.all",
            f"late.{m}.bridge",
            f"late.{m}.question",
        ]
        if m == "mu":  # Muse: only the deeper band (36-42)
            keys = ["", "", "", "ko.mu.mk", "pos.mu.bridge", "pos.mu.question"]
        data[m] = {c: D.b(k) for c, k in zip(conds, keys, strict=True) if D.b(k)}
    colors = dict(zip(conds, ["recall", "lens", "lookup"] * 2, strict=True))
    return Figure("p8_where", "At middle layers the bridge's mention carries it; deeper, the question does.",
                  "Zach's Finding 5: the lens part removed at all tokens (dark), the bridge's mention only (teal) or the "
                  "question only (purple), over a middle and a deeper band (docs/breadth/data.csv pos.*.all.*, late.*); "
                  "Muse 30B tested only at layers 36-42. Fixed in advance; rotated controls cost at most 2.5 points.",
                  [Multiples(models, conds, data, colors, "recalled minus stated answers lost (pp)", (0, 70), "{:.0f}")])  # fmt: skip


def routes() -> Figure:
    models = [(m, n) for m, n in D.DAN if D.s(m, "another item moved, whole: identity share")]
    segs = [(lab, col, {m: D.s(m, f"another item moved, whole: {lab} share")[0] for m, _ in models})
            for lab, col in (("identity", "identity"), ("position", "address"))]  # fmt: skip
    val = ", ".join(f"{n} {D.s(m, 'another item moved, whole: value share')[0]:.2f}" for m, n in models)
    return Figure("p9_routes", "The lookup goes by identity or position, never the value.",
                  "Routes test (another item moved), the whole change at L: shares of switched lookups naming the "
                  f"item's own locker (identity) or the locker now at its old place (position); the new number (value): "
                  f"{val}. 300 scenes per model (figures/story/data.csv fig05 rows). Lightning hollow; the 122B hollow "
                  "(gate lowered to 0.75 after the data).",
                  [Stacked(models, segs, "lookups switched by the whole change", {m for m, _ in models if D.hollow(m, True)}, rotate=20)],
                  size="half")  # fmt: skip


SPECS = {f().id: f for f in (setup_datasets, setup_tools, c1_split, controls_zach, controls_dan, graded_nine, pointer_zach,
                             atoms_dan, probe, swap_dose, lens_readout, readable, breaks, where, routes)}  # fmt: skip
