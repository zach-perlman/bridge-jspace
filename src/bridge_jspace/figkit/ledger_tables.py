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
    regex: bool = False  # q is a regular expression (a model's own layer or head inside the name)


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
    if s.regex:
        hit = D.s_match(t, s.q.format(k=k), fig)
        v = hit[1] if hit and hit[1][0] == hit[1][0] else None
    else:
        v = cell(t, s.q, fig, k, s.prefix)
    if v is None or s.needs is None:
        return v
    n = cell(t, s.needs[0], fig, k)
    return v if n is not None and n[0] >= s.needs[1] else None


def keyed(fig: str, rx: str, sub: str = "{k}") -> list[tuple[str, str, str]]:
    """Rows (model, key, label) for every key a regex's group captures in a figure's quantities, models in D.DAN
    order, keys in numeric order (a model's own layers)."""
    import re

    pat = re.compile(rx)
    out = []
    for t, _ in D.DAN:
        ks = {m.group(1) for (f, m_, q) in D.story() if f == fig and m_ == t and (m := pat.fullmatch(q))}
        out += [(t, k, sub.format(k=k)) for k in sorted(ks, key=lambda k: (len(k), k))]
    return out


def row_list(spec: Spec) -> list:
    return spec.rows() if callable(spec.rows) else (spec.rows or [])


def cols_of(spec: Spec) -> list[K]:
    """Models as columns: a column drawn only for a model with data (S1)."""
    return [
        c
        for c in spec.cols
        if c.target is None or any(valid(c.target, s, spec.figure, k) for _, k, _ in row_list(spec) for s in c.series)
    ]


def rows_of(spec: Spec) -> list[tuple[str, str, str]]:
    rows = row_list(spec) or [(t, "", "") for t, _ in D.DAN]
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
                span = c.xlim[1] - c.xlim[0]
                for j, (s, v) in enumerate(main):
                    ci = v if len(v) >= 3 and v[1] is not None and v[2] is not None else None
                    last = j == len(main) - 1
                    right = (ci[2] if ci else v[0]) if last else v[0]
                    # the value label goes left when a grey control sits where it would be written
                    blocked = any(s2.control and 0 <= v2[0] - right <= 0.25 * span for s2, v2 in have)
                    side = "left" if blocked and v[0] - c.xlim[0] > 0.2 * span else "right"
                    dot(ax, v[0], i, C[s.color], hollow[t], cell=ci, value=v[0] if last else None, vfmt=c.fmt,
                        vside=side)  # fmt: skip

        xlim = (c.xlim[0], c.xlim[1] + 0.22 * (c.xlim[1] - c.xlim[0])) if c.xlim[1] in (1.0, 0.6, 0.8) else c.xlim
        cols.append(Col(c.width, c.title, c.unit, draw, xlim, c.xticks))
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
LOST = "switches blocked beyond a random part"
LT = "nemotron-3.5-lightning"
Q122 = "qwen3.5-122b-a10b"

SPECS: list[Spec] = [
    Spec("lightning_layers", "ledger_lightning_layers",
         [K("The whole change", "switch rate, 60 scenes", [S("layer sweep, {k}: lookup switch rate", "lookup", "lookup"),
                                                            S("layer sweep, {k}: recall switch rate", "recall", "recall")]),
          K("Without the lens part", "blocked beyond a random part",
            [S("conflict test, {k}, lookup: switches lost beyond random", "lookup",
               needs=("conflict test, {k}, lookup: switches under the whole change", 30)),
             S("conflict test, {k}, recall: switches lost beyond random", "recall",
               needs=("conflict test, {k}, recall: switches under the whole change", 30))],
            xlim=(-0.3, 1.0), band=NB, width=2.9)],
         rows=[(LT, f"L{la}", f"L{la}") for la in range(2, 51, 4)] + [(Q122, f"L{la}", f"L{la}") for la in (24, 27, 30, 33, 36)]),
    Spec("answer_control", "ledger_answer_control",
         [K("Without the lens part", "recall, beyond random", [S("main test, recall, switches lost beyond random: without the lens part", "recall", "recall")], xlim=(-0.2, 1.0), band=NB),
          K("Lens out, answer in", "the same", [S("main test, recall, switches lost beyond random: lens part out, answer kept", "recall")], xlim=(-0.2, 1.0), band=NB),
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
         [K(f"Arm {a}", "blocked against (1)", [S(f"45p, a{a}: lookup switches lost against (1)", "lookup", "lookup"),
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
    # ---- Part II --------------------------------------------------------------------------------------------------
    Spec("routes_lens", "fig05d",
         [K(f"Lens directions {r}", "accuracy drop beyond random",
            [S(f"47.1: identity route: answers lost beyond random without lens directions {r}", "identity", "identity route"),
             S(f"47.1: position route: answers lost beyond random without lens directions {r}", "address", "position route")],
            xlim=(-0.4, 0.8), xticks=[0, 0.25, 0.5], width=2.5) for r in ("1-25", "26-100", "1-100")]),
    Spec("routes", "ledger_routes",
         [K(title, "share of the lookup's answers",
            [S(f"another item moved, {arm}: value share", "recall", "the value"),
             S(f"another item moved, {arm}: identity share", "identity", "identity"),
             S(f"another item moved, {arm}: position share", "address", "position")],
            xlim=(0, 1.0), width=2.5) for arm, title in (("whole", "The whole change"), ("no_alf", "Without the address"),
                                                         ("keep_alf", "The address alone"))],
         lowered=True),
    Spec("value_formats", "ledger_value_formats",
         [K("The whole change", "share of the lookup's answers",
            [S("{k}, whole change: value share", "recall", "the value"), S("{k}, whole change: position share", "address", "position")],
            xlim=(0, 1.0), width=4.0)],
         rows=[(t, f, n) for t, _ in D.DAN for f, n in (("prose", "prose"), ("table", "tables"), ("json", "JSON"))]),
    Spec("learned", "ledger_learned",
         [K(NAME[t], "own-IIA, test half", [S("lookup: test own-IIA at k = {k}", "lookup", "lookup's subspace"),
                                             S("recall: test own-IIA at k = {k}", "recall", "recall's subspace")],
            xlim=(0, 1.0), width=2.4, target=t) for t in ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")],
         rows=[(None, str(k), f"k = {k}") for k in (4, 16, 64, 128)], label_w=1.1),
    Spec("bindid", "ledger_bindid",
         [K(title, "lookups moved", [S(f"{v}: random", "control", "random", control=True),
                                     S(f"{v}: Y's version", "lens", "Y's version"), S(f"{v}: X's vector", "address", "X's vector")],
            xlim=(0, 0.6), xticks=[0, 0.25, 0.5], width=3.2) for v, title in (("pre-specified", "Pre-specified"), ("centered", "Centered"))]),
    # ---- Part III -------------------------------------------------------------------------------------------------
    Spec("distance", "e6_distance",
         [K("Position share", "the lookup, whole change", [S("47.16: position share with 0 neutral sentences", "control", "no neutral sentences", control=True),
                                                            S("47.16: position share with 50 neutral sentences", "address", "50 neutral sentences")],
            xlim=(0, 1.0), width=3.2),
          K("The swap", "lookups sent to the target", [S("47.16: the swap (fit with none) sends lookups to the target, 0 sentences", "control", control=True),
                                                        S("47.16: the swap (fit with none) sends lookups to the target, 50 sentences", "lookup", "the swap, 50 sentences")],
            xlim=(0, 1.0), width=3.2)],
         lowered=True),
    Spec("subset27b", "ledger_subset27b",
         [K("Without the address", "position share", [S("without a random part", "control", "a random part", control=True), S("without the address", "address", "the address")],
            xlim=(0, 1.0), width=2.5),
          K("Alone", "position share", [S("a random part alone", "control", control=True), S("the address alone", "address")], xlim=(0, 1.0), width=2.5),
          K("The swap, dose 2", "to the target", [S("the swap at dose 2: to the target", "lookup")], xlim=(0, 1.0), width=2.5)]),
    Spec("report_slot1", "ledger_report_slot1",
         [K(title, "reads slot 1", [S(q, "lookup")], xlim=(0, 1.0), width=2.4)
          for q, title in (("the earlier report wording", "Earlier wording"), ("position wording (a digit)", "Position (a digit)"),
                           ("sentence wording (a word)", "Sentence (a word)"))]),
    Spec("heads", "ledger_heads",
         [K(n, "swap cut", [S(f"last token, {n}: random sets' mean cut", "control", "random heads", control=True),
                            S(f"last token, {n}: share of the swap's switch cut", "lookup", "the top heads")],
            xlim=(-0.2, 1.0), xticks=[0, 0.5, 1], width=1.7) for n in ("top 1", "top 3", "top 5", "top 10", "best layer")]),
    Spec("attention", "ledger_attention",
         [K("Attention moved", "the best head, last token",
            [S(r"best head L\d+:h\d+, last token: attention moved, a random vector \(switched pairs\)", "control", "a random vector", control=True, regex=True),
             S(r"best head L\d+:h\d+, last token: attention moved, pairs that switched", "lookup", "pairs that switched", regex=True)],
            xlim=(0, 2.4), xticks=[0, 1, 2], width=4.5)]),
    Spec("chain", "fig09d",
         [K("Taken out", "hall answers by position", [S("47.14: hall answers by position, without a random part (same size)", "control", "a random part", control=True),
                                                      S("47.14: hall answers by position, without the hall address", "address", "the hall address")],
            xlim=(0, 1.0), width=3.0),
          K("Only retained", "hall answers by position", [S("47.14: hall answers by position, only a random part (same size) kept", "control", control=True),
                                                      S("47.14: hall answers by position, only the hall address kept", "address")],
            xlim=(0, 1.0), width=3.0),
          K("Probe", "the hall at the locker digit", [S("47.14: hall probe's layout baseline", "control", control=True),
                                                      S("47.14: hall probe at the locker digit", "address")], xlim=(0, 1.0), width=2.6)]),
    Spec("refit", "fig09b_refit",
         [K("Without the pointer", "the lookup, beyond random", [S("(b) {k}: lookup extra loss without the pointer fit on simple scenes", "control", "fit on simple scenes", control=True),
                                                                 S("(b) {k}: lookup extra loss without the refit pointer", "address", "refit on this format")],
            xlim=(-0.2, 1.0), band=NB, width=4.0)],
         rows=[(t, f, n) for t, _ in D.DAN for f, n in (("prose", "prose"), ("json", "JSON"), ("table", "tables"))]),
    Spec("code_tool", "ledger_code_tool",
         [K("Without the address", "position share", [S("{k}, routes: the same, random part out", "control", "a random part", control=True),
                                                      S("{k}, routes: position without the address", "address", "the address")],
            xlim=(0, 1.0), width=2.6),
          K("The address alone", "position share", [S("{k}, routes: position, the address alone", "address")], xlim=(0, 1.0), width=2.4),
          K("Probe", "locker sentence, locker first", [S("{k}, probe: the layout alone", "control", control=True), S("{k}, probe: locker sentence, locker first", "address")],
            xlim=(0, 1.0), width=2.6)],
         rows=[(t, f, n) for t, _ in D.DAN for f, n in (("code", "code"), ("tool", "tool output"))]),
    # ---- Part IV --------------------------------------------------------------------------------------------------
    Spec("order_split", "ledger_order_split",
         [K("Lookups switched", "by the whole change", [S("locker after the pick: lookups switched", "control", "locker after the pick", control=True),
                                                        S("locker before the pick: lookups switched", "lookup", "locker before the pick")],
            xlim=(0, 1.0), width=5.0)],
         lowered=True),
    Spec("copy45q", "fig03",
         [K(title, "lookups switched", [S(q, "lookup")], xlim=(0, 1.0), width=2.5)
          for q, title in (("45q, the rule's arm a: the bridge-word change at L (lookups switched)", "The bridge word at L"),
                           ("45q, the rule's arm c: copy at L, every locker-sentence token (lookups switched)", "Copy at L"),
                           ("45q, the rule's arm d: copy at L/2, every locker-sentence token (lookups switched)", "Copy at L/2"))]),
    Spec("cumulative", "ledger_cumulative",
         [K("Locker first", "missed at L", [S("locker first: missed at L", "lookup")], xlim=(0, 1.0), width=3.2),
          K("Locker after", "carried before L", [S("locker after: carried before L", "lookup")], xlim=(0, 1.0), width=3.2)]),
    Spec("last_token_address", "ledger_last_token_address",
         [K("The bridge-fit swap at L+4", "dose 2: lookups sent to the target", [S("bridge-fit swap at L+4, dose 2: lookups sent to the target", "address")],
            xlim=(0, 1.0), width=5.0)]),
    Spec("last_conflict", "ledger_last_conflict",
         [K(f"The {w}", "blocked beyond random, last token", [S(rf"{w} L{{k}}: switches lost without the lens part beyond random \(last token\)", "lookup" if w == "lookup" else "recall", w, regex=True)],
            xlim=(-0.3, 1.0), band=NB, width=3.0) for w in ("lookup", "recall")],
         rows=lambda: keyed("ledger_last_conflict", r"(?:lookup|recall) L(\d+): switches lost without the lens part beyond random \(last token\)", "L{k}")),
    Spec("last_conflict_words", "ledger_last_conflict_words",
         [K(f"{at.capitalize()}, {w}", "blocked beyond random", [S(f"{{k}}, {w}, {at}", w, w)], xlim=(-0.3, 1.0), band=NB, width=2.3)
          for at in ("answer - 3", "read peak") for w in ("lookup", "recall")],
         rows=[(t, k, n) for t, _ in D.DAN for k, n in (("words", "word answers"), ("locker", "number answers"))]),
    Spec("attnblock", "ledger_attnblock",
         [K("The lookup", "switches cut", [S("lookup: {k}", "lookup", "lookup")], xlim=(-0.2, 1.0), width=3.0),
          K("The recall", "switches cut", [S("recall: {k}", "recall", "recall")], xlim=(-0.2, 1.0), width=3.0)],
         rows=[(LT, k, k) for k in ("(i) block 19", "(ii) block 26", "(iii) blocks 19, 26", "(iv) all after L", "(v) control",
                                    "follow-up: span", "follow-up: control span")], label_w=2.6),
    # ---- Part V ---------------------------------------------------------------------------------------------------
    Spec("zach_named", "ledger_zach_named",
         [K(f"{f.capitalize()} facts", LOST, [S(f"Zach's named passages, {f} facts, lookup: switches lost beyond random", "lookup", "lookup"),
                                              S(f"Zach's named passages, {f} facts, recall: switches lost beyond random", "recall", "recall")],
            xlim=(-0.3, 1.0), band=NB, width=3.2) for f in ("true", "made-up")]),
    Spec("jsuite", "ledger_jsuite",
         [K(title, "blocked beyond random", [S(f"{{k}}P lookup: {arm}", "lookup", "lookup"), S(f"{{k}}M recall: {arm}", "recall", "recall")],
            xlim=(-0.3, 1.0), band=NB, width=3.2) for arm, title in (("without the lens part", "Without the lens part"),
                                                                     ("answer directions only", "Answer directions only"))],
         rows=[(t, k, n) for t, _ in D.DAN for k, n in (("P", "named bridge"), ("M", "described bridge"))]),
    Spec("full_carrier", "ledger_full_carrier",
         [K(title, LOST, [S(f"{{k}}, lookup, {arm}: switches lost beyond random", "lookup", "lookup"),
                          S(f"{{k}}, recall, {arm}: switches lost beyond random", "recall", "recall")],
            xlim=(-0.3, 1.0), band=NB, width=3.2) for arm, title in (("one layer", "One layer"), ("every layer to L", "Every layer to L"))],
         rows=[(t, k, k) for t, _ in D.DAN for k in ("fact-first", "fact-after")]),
    Spec("zach_routes", "ledger_zach_routes",
         [K("The whole change", "share of the lookup's answers",
            [S("L{k}, whole change: value share", "recall", "the value"), S("L{k}, whole change: identity share", "identity", "identity"),
             S("L{k}, whole change: position share", "address", "position")], xlim=(0, 1.0), width=5.0)],
         rows=lambda: keyed("ledger_zach_routes", r"L(\d+), whole change: identity share", "L{k}")),
    Spec("read_window", "ledger_read_window",
         [K(NAME[t], "switched", [S("his named passages, layer {k}: lookup switched", "lookup", "lookup"),
                                  S("his named passages, layer {k}: recall switched", "recall", "recall")],
            xlim=(0, 1.0), width=2.6, target=t) for t in ("qwen3.5-9b", "qwen3.6-27b", LT)],
         rows=[(None, str(k), f"L{k}") for k in range(2, 31, 2)], label_w=1.0),
    # ---- Part VI --------------------------------------------------------------------------------------------------
    Spec("described_bridge", "fig05c",
         [K("Without the lens part", "blocked beyond random", [S("47.3: lookup's extra loss without the J++ part", "lookup", "lookup"),
                                                    S("47.3: recall's extra loss without the J++ part", "recall", "recall")],
            xlim=(-0.3, 1.0), band=NB, width=4.0),
          K("gap", "recall − lookup", [S("47.3: gap (recall's extra loss minus the lookup's)", "recall")], text=True, width=1.4)]),
    Spec("pooled_probe", "ledger_pooled_probe",
         [K("Who picked the item", "probe accuracy", [S(r"L{k}: who picked it, best single token", "control", "best single token", control=True, regex=True),
                                                      S(r"L{k}: who picked it, pooled over the locker sentence", "recall", "pooled over the sentence", regex=True)],
            xlim=(0, 1.0), width=5.0)],
         rows=lambda: keyed("ledger_pooled_probe", r"L(\d+): who picked it, pooled over the locker sentence", "L{k}")),
    Spec("agnostic", "ledger_agnostic",
         [K(kind.capitalize(), "position blocked, beyond random", [S(f"{kind}: position lost without the animal-fit address, beyond random", "control", "fit on animals", control=True)]
            + ([S(f"{kind}: position lost without the refit address, beyond random", "address", "refit")] if kind != "animals" else []),
            xlim=(-0.2, 1.0), width=2.6) for kind in ("animals", "fruits", "names")]),
    Spec("described", "ledger_described",
         [K("Our gap", "recall − lookup, one layer", [S(r"L\d+: our gap \(recall minus lookup extra loss\)", "recall", regex=True)], xlim=(-0.3, 1.0), width=3.2),
          K("The band knock-out", "recall − lookup", [S("Zach's knock-out, recall minus lookup", "recall")], xlim=(-0.3, 1.0), width=3.2)]),
    Spec("answer_map", "ledger_answer_map",
         [K("Readable", "best top-5 share before the answer", [S(r"{k}, lookup: best top-5 share before the answer layer \(T L\d+\)", "lookup", "lookup", regex=True),
                                                                S(r"{k}, recall: best top-5 share before the answer layer \(T L\d+\)", "recall", "recall", regex=True)],
            xlim=(0, 1.0), width=3.2),
          K("Usable", "answers changed by the write, gain 1", [S("{k}, lookup: answers changed by the write, gain 1", "lookup"),
                                                               S("{k}, recall: answers changed by the write, gain 1", "recall")],
            xlim=(0, 1.0), width=3.2)],
         rows=[(t, k, n) for t, _ in D.DAN for k, n in (("ours", "locker scenes"), ("Zach's", "fact passages"))]),
]  # fmt: skip


if __name__ == "__main__":
    import sys

    for i in build(sys.argv[1:] or None):
        print("wrote", OUT / f"t_{i}.png")
    print("\n".join(PROBLEMS) or "lint: clean")
