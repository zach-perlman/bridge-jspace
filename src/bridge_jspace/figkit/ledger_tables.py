"""The ledger's figures (docs/depth/EXPERIMENTS.md) in the table style, from data/figures/depth/data.csv (morning brief
30 Oct, Section 3: "clean" and "table"): one declarative Spec per figure, drawn by dottable.Table.

A Spec's rows are models (or a model's conditions, grouped: the model's name once, short grey sub-rows); a model with no
number for the figure is not drawn (S1); a missing cell is a grey en dash (S2); hollow is only post hoc (S3, Lightning
everywhere, the 122B where its gate was lowered or lookup-only); colours by meaning (S4); the key is one row under the
axes (S5, Dan 30 Oct); no title or status text inside the image (S2, R7).

uv run python -m bridge_jspace.figkit.ledger_tables [ids]   # figures/depth/ledger/t_<id>.png
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import dottable as T
from bridge_jspace.figkit import lint
from bridge_jspace.figkit.data import REPO
from bridge_jspace.figkit.dottable import INK, MUTED, C, Col, Row, Table, band, connector, dot

OUT = REPO / "figures" / "depth" / "ledger"
SLOTS = REPO / "data" / "figures" / "depth" / "ledger" / "table_slots.json"
NAME = {m: n.replace(" ○", "") for m, n in D.DAN}
SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "muse-glimmer-30b": "Muse", "nemotron-3.5-lightning": "Lightning",
         "qwen3.5-122b-a10b": "122B"}  # fmt: skip


@dataclass
class S:
    """A series: the data.csv quantity ({k}: the row's key), its colour (a dottable.C key) and its word in the key."""

    q: str
    color: str
    word: str = ""
    control: bool = False  # grey and smaller (R8)
    needs: tuple | None = None  # (quantity, minimum): the cell is drawn only if that quantity reaches the minimum
    prefix: bool = False  # the first quantity starting with q (names that carry a model's own layer)


@dataclass
class K:
    """A column: dots for its series on one axis (two main series: a dumbbell), or text (a number or a label)."""

    title: str
    unit: str
    series: list
    xlim: tuple = (-0.2, 1.0)
    xticks: list = field(default_factory=lambda: [0, 0.5, 1])
    width: float = 2.6
    fmt: str = "{:.2f}"
    band: tuple | None = None  # the "not needed" band around zero
    text: bool = False  # a text column: the first series' value as words or a number
    target: str | None = None  # a column for one model (models as columns: the rows are conditions, target None)


@dataclass
class Spec:
    id: str
    figure: str  # the data.csv figure group
    cols: list
    rows: list | None = None  # [(target, key, sub)]; None: one row per model in D.DAN order
    lowered: bool = False  # the 122B hollow (its gate lowered, or the lookup-only gate)
    label_w: float = 1.45


def cell(t: str, q: str, fig: str, k="", prefix: bool = False):
    v = D.s(t, q.format(k=k), fig, prefix=prefix)
    ok = v and v[0] is not None and (not isinstance(v[0], float) or v[0] == v[0])  # NaN: nothing switched
    return v if ok else None


def valid(t: str, s: S, fig: str, k="") -> tuple | None:
    """The series' cell, or None when it is missing or its count is under the rule's minimum (S2: a dash)."""
    v = cell(t, s.q, fig, k, s.prefix)
    if v is None or s.needs is None:
        return v
    n = cell(t, s.needs[0], fig, k)
    return v if n is not None and n[0] >= s.needs[1] else None


def cols_of(spec: Spec) -> list[K]:
    """Models as columns: a column drawn only for a model with data (S1)."""
    return [
        c
        for c in spec.cols
        if c.target is None
        or any(valid(c.target, s, spec.figure, k) for _, k, _ in (spec.rows or []) for s in c.series)
    ]


def rows_of(spec: Spec) -> list[tuple[str, str, str]]:
    rows = spec.rows or [(t, "", "") for t, _ in D.DAN]
    return [r for r in rows if any(valid(c.target or r[0], s, spec.figure, r[1]) for c in spec.cols for s in c.series)]


def table(spec: Spec) -> Table:
    rows = rows_of(spec)
    spec_cols = cols_of(spec)
    hollow = {t: D.hollow(t, spec.lowered) for t in {r[0] for r in rows} | {c.target for c in spec_cols} if t}
    seen, table_rows = set(), []
    for t, _k, sub in rows:
        first = t not in seen
        seen.add(t)
        if t is None or (
            len({r[0] for r in rows}) == 1 and sub
        ):  # conditions as rows (models as columns, or one model)
            table_rows.append(Row(sub))
            continue
        name = NAME[t] if first else ""
        table_rows.append(Row(name, sub if sub else "", hollow=hollow[t] and first and not sub))
    cols = []
    for c in spec_cols:
        if c.text:

            def draw_text(i, _r, c=c):
                t, k, _ = rows[i]
                v = valid(c.target or t, c.series[0], spec.figure, k)
                if v is None:
                    return [("–", MUTED, "normal")]
                x = v[0]
                s = c.fmt.format(x) if isinstance(x, (int, float)) else str(x)
                return [(s, INK, "bold")]

            cols.append(Col(c.width, c.title, c.unit, draw_text, text=True))
            continue

        def draw(ax, _r, c=c):
            if c.band:
                band(ax, c.band[0], c.band[1], len(rows))
            for i, (t, k, _) in enumerate(rows):
                t = c.target or t
                vals = [(s, valid(t, s, spec.figure, k)) for s in c.series]
                have = [(s, v) for s, v in vals if v is not None]
                if not have:
                    ax.text((c.xlim[0] + c.xlim[1]) / 2, i, "–", ha="center", va="center", fontsize=12, color=MUTED)
                    continue
                main = [(s, v) for s, v in have if not s.control]
                if len(main) == 2:
                    connector(ax, main[0][1][0], main[1][1][0], i)
                for s, v in have:
                    if s.control:
                        dot(ax, v[0], i, C["control"], size=7, zorder=7)  # above the value labels' boxes
                for j, (s, v) in enumerate(main):
                    ci = v if len(v) >= 3 and v[1] is not None and v[2] is not None else None
                    last = j == len(main) - 1
                    dot(ax, v[0], i, C[s.color], hollow[t], cell=ci, value=v[0] if last else None, vfmt=c.fmt)

        cols.append(Col(c.width, c.title, c.unit, draw, c.xlim, c.xticks))
    words = {}
    for c in spec_cols:
        for s in c.series:
            if s.word and s.word not in words:
                words[s.word] = C["control"] if s.control else C[s.color]
    key = [("●", col, w) for w, col in words.items()]
    if any(hollow.values()):
        key.append(("○", INK, "post hoc"))
    width = spec.label_w + sum(c.width for c in cols) + 0.25 * (len(cols) + 1)
    if width < MIN_W:  # one page width for every figure: the same text size at 880 px (a narrow image scales up)
        grow = (MIN_W - width) / sum(c.width for c in cols)
        for c in cols:
            c.width *= 1 + grow
    return Table(table_rows, cols, label_w=spec.label_w, labels=False, key=key)


PROBLEMS: list[str] = []
DRAWN: dict[str, dict[str, str]] = {}


def build(ids: list[str] | None = None) -> list[str]:
    T.BEFORE_SAVE = lambda fig, path: PROBLEMS.extend(lint.table_problems(fig, Path(path).stem))
    OUT.mkdir(parents=True, exist_ok=True)
    done = []
    for spec in SPECS:
        if ids and not any(spec.id.startswith(x) for x in ids):
            continue
        table(spec).render(str(OUT / f"t_{spec.id}.png"))
        DRAWN[f"t_{spec.id}"] = {SHORT[t]: "data" for t in {r[0] for r in rows_of(spec)} | {c.target for c in cols_of(spec)}
                                 if t}  # fmt: skip
        done.append(spec.id)
    old = json.loads(SLOTS.read_text()) if SLOTS.exists() else {}
    SLOTS.parent.mkdir(parents=True, exist_ok=True)
    SLOTS.write_text(json.dumps(old | DRAWN, indent=1, sort_keys=True) + "\n")
    return done


# ---- the specs, in the ledger's order ---------------------------------------------------------------------------------
NB = (-0.1, 0.1)  # the "not needed" band
MIN_W = 10.5  # inches
LOST = "switches lost beyond a random part"
LT = "nemotron-3.5-lightning"
Q122 = "qwen3.5-122b-a10b"

SPECS: list[Spec] = [
    Spec("lightning_layers", "ledger_lightning_layers",
         [K("The whole change", "switch rate, 60 scenes", [S("layer sweep, {k}: lookup switch rate", "lookup", "lookup"),
                                                            S("layer sweep, {k}: recall switch rate", "recall", "recall")]),
          K("Without the lens part", "lost beyond a random part",
            [S("conflict test, {k}, lookup: switches lost beyond random", "lookup",
               needs=("conflict test, {k}, lookup: switches under the whole change", 30)),
             S("conflict test, {k}, recall: switches lost beyond random", "recall",
               needs=("conflict test, {k}, recall: switches under the whole change", 30))],
            xlim=(-0.3, 1.0), band=NB, width=2.9)],
         rows=[(LT, f"L{la}", f"L{la}") for la in range(2, 51, 4)] + [(Q122, f"L{la}", f"L{la}") for la in (24, 27, 30, 33, 36)]),
    Spec("answer_control", "ledger_answer_control",
         [K("Without the lens part", "recall, beyond random", [S("main test, recall, switches lost beyond random: without the lens part", "recall", "recall")], xlim=(-0.2, 1.0), band=NB),
          K("Lens part out, answer kept", "the same", [S("main test, recall, switches lost beyond random: lens part out, answer kept", "recall")], xlim=(-0.2, 1.0), band=NB),
          K("Answer directions only", "the same", [S("main test, recall, switches lost beyond random: answer directions only", "recall")], xlim=(-0.2, 1.0), band=NB)]),
    Spec("transfer", "fig09a",
         [K(NAME[t], "", [S("lookup extra loss without the J++ part: {k}", "lookup", "lookup"),
                          S("recall extra loss without the J++ part: {k}", "recall", "recall")],
            xlim=(-0.3, 1.0), band=NB, width=1.9, target=t) for t, _ in D.DAN],
         rows=[(None, f, n) for f, n in (("simple", "simple"), ("prose", "prose"), ("json", "JSON"), ("table", "tables"),
                                         ("natural", "natural"))], label_w=1.1),
    Spec("dose", "fig16_dose",
         [K("The lens part alone", "beyond random, dose 1.5",
            [S("51.1 A: lookup switches with the J++ part by itself at dose 1.5, minus a random part (same size) at the same dose", "lookup", "lookup"),
             S("51.1 A: recall switches with the J++ part by itself at dose 1.5, minus a random part (same size) at the same dose", "recall", "recall")],
            xlim=(-0.3, 1.2), band=NB, width=3.0),
          K("The rest alone", "lookups switched, dose 1.5",
            [S("51.1 B: lookups switched, the rest by itself without the address, dose 1.5", "address", "the rest without the address"),
             S("51.1 B: lookups switched, the rest by itself, dose 1.5", "lookup")], xlim=(0, 1.2), width=3.0)]),
    Spec("ladder_before", "fig01d",
         [K(NAME[t], "", [S("rung {k}: recall, locker before the pick: the random part's own cost (kept with none minus kept with the random part)", "control", "random part's own cost", control=True),
                          S("rung {k}: recall, locker before the pick: answers lost beyond random", "recall", "recall, locker before the pick")],
            xlim=(-0.2, 1.0), width=1.9, target=t) for t, _ in D.DAN],
         rows=[(None, str(r), f"rung {r}") for r in range(1, 7)], label_w=1.1),
    Spec("earlier_mention", "fig03c",
         [K(f"Arm {a}", "lost against (1)", [S(f"45p, a{a}: lookup switches lost against (1)", "lookup", "lookup"),
                                             S(f"45p, a{a}: recall switches lost against (1)", "recall", "recall")],
            xlim=(-0.2, 0.8), xticks=[0, 0.25, 0.5], width=2.3) for a in (2, 3, 4)]),
    Spec("identity_address", "ledger_identity_address",
         [K("Both changed", "recalls answering", [S("both: the original", "control", "the original", control=True),
                                                 S("both: B's answer", "identity", "B's (the lens part's item)"),
                                                 S("both: C's answer", "address", "C's (the address's item)")],
            xlim=(0, 0.6), xticks=[0, 0.25, 0.5], width=3.0),
          K("Lens part alone", "B's answer", [S("lens part alone: B's", "identity")], xlim=(0, 0.6), xticks=[0, 0.25, 0.5], width=2.2),
          K("Address alone", "C's answer", [S("address alone: C's", "address")], xlim=(0, 0.6), xticks=[0, 0.25, 0.5], width=2.2)]),
    Spec("twobytwo", "ledger_twobytwo",
         [K("Question after", "number answers, beyond random", [S("Q after, number: lookup lost", "lookup", "lookup"),
                                                           S("Q after, number: recall lost", "recall", "recall")],
            xlim=(-0.2, 1.0), band=NB, width=3.0),
          K("Question before", "the same", [S("Q before, number: lookup lost", "lookup"), S("Q before, number: recall lost", "recall")],
            xlim=(-0.2, 1.0), band=NB, width=3.0),
          K("before − after", "the lookup, paired", [S("lookup, Q before minus after", "lookup")], text=True, fmt="{:+.2f}", width=1.5)]),
    Spec("das48", "ledger_das48",
         [K("The lookup's subspace", "its lookups switched", [S("lookup's subspace", "lookup")], xlim=(0, 1.25), width=3.2),
          K("The recall's subspace", "its recalls switched", [S("recall's subspace", "recall")], xlim=(0, 1.0), width=3.2)]),
]  # fmt: skip


if __name__ == "__main__":
    import sys

    for i in build(sys.argv[1:] or None):
        print("wrote", OUT / f"t_{i}.png")
    print("\n".join(PROBLEMS) or "lint: clean")
