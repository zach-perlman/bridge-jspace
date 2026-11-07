"""The breadth README's figures (figures/breadth/, Zach's set) on styles-plot, for the readme target. Every number is a
row of docs/breadth/data.csv (scripts/report_breadth.py, readers in scripts/breadth_data.py), read by key; the old
builder (scripts/fig_neel.py) drew them on the pod. Models are rows in the vocabulary's order (the old figures sorted
them by strength and coloured them by model: here a colour is a role), conditions are columns or lanes, verdict texts
stay in the README (Dan, 7 Nov). fig06_pointer is the README's r4_pointer (the same pointer runs and the probe's
subspace); fig11_scorecard becomes a markdown table and is not drawn.

uv run python -m bridge_jspace.figkit.breadth_sp [ids...]
"""

from __future__ import annotations

import sys

import styles_plot as sp

from bridge_jspace.figkit import data as D
from bridge_jspace.figkit import readme_sp as RS
from bridge_jspace.figkit.writeup_sp_base import REPO, vocab

OUT = REPO / "figures" / "breadth"


def path(fid: str):
    """Where a breadth figure is written (one place, for the folder layout to come)."""
    return OUT / f"{fid}.png"


def ids() -> dict[str, str]:
    """Breadth id (data.csv's model column) -> the vocabulary's model key."""
    return {e.id: e.key for e in vocab().entities("models")}


def b(key: str):
    return D.b(key)


def est(c, cell, key, label=False, interval=True) -> sp.Est:
    lo, hi = (c[1], c[2]) if interval and c[1] is not None else (None, None)
    return sp.Est(c[0], lo, hi, cell=cell, key=key, label=label)


def models_with(pattern: str) -> list[tuple[str, str]]:
    """(breadth id, model key) in the vocabulary's order, for the models whose key `pattern.format(id)` exists."""
    return [(i, m) for i, m in ids().items() if b(pattern.format(i))]


# ---- fig01: needed --------------------------------------------------------------------------------------------------
CONTROLS01 = (("rot", "rotated"), ("u", "logit lens"), ("pc", "PCA"))
FINALS = (("K", "the fact in the passage", "lookup"), ("P", "a new made-up fact in the passage", "lookup"),
          ("A", "the answer word on another entity", "recall"),
          ("N", "nothing in the passage, no lures", "recall"), ("M", "recall, lures present", "recall"))  # fmt: skip


def fig01_needed() -> sp.Figure:
    """(top) Per model, M − K under the lens part's top-10 knock-out at the model's band, against the same knock-out
    rotated, the logit lens's top 10, and the same norm along the top principal directions (grey). (bottom) For the
    three strong models, the points lost by where the answer is (stated facts in the lookup's colour, the rest in the
    recall's)."""
    v = vocab()
    rows = models_with("ko.{}.mk")
    lens = {m: est(b(f"ko.{i}.mk"), f"mk.{i}", f"ko.{i}.mk", label=True) for i, m in rows}
    series = [sp.Series("control", {m: est(c, f"mk.{i}", f"ko.{i}.{k}", interval=True)
                                    for i, m in rows if (c := b(f"ko.{i}.{k}"))}, control=name)
              for k, name in CONTROLS01]  # fmt: skip
    # one column per arm: grey dots of different controls in one column could not be told apart
    top = sp.DotTable([m for _i, m in rows], [
        sp.DotColumn("lens part knocked out", "gap", (-8, 72), (0, 30, 60), series=[sp.Series("neutral", lens)]),
        *(sp.DotColumn(s.control, "gap", (-8, 72), (0, 30, 60), series=[s]) for s in series),
    ])  # fmt: skip
    strong = [(i, m) for i, m in rows if i in ("q9", "q27", "nl")]
    vb = v.with_entities("finals", [(k, name) for k, name, _r in FINALS])
    cols = []
    for i, m in strong:
        cells = {"lookup": {}, "recall": {}}
        for k, _name, role in FINALS:
            c = b(f"ko.{i}.lost{k}")
            if c:
                cells[role][k] = sp.Est(c[0], cell=f"lost.{i}", key=f"ko.{i}.lost{k}", label=True)
        cols.append(sp.DotColumn(v.entity("models", m).name, "drop", (-2, 62), (0, 30, 60),
                                 series=[sp.Series("lookup", cells["lookup"]), sp.Series("recall", cells["recall"])]))  # fmt: skip
    bottom = sp.DotTable([k for k, *_ in FINALS], cols, kind="finals",
                         note="accuracy drop under the lens part's top-10 knock-out, by where the answer is")  # fmt: skip
    return sp.Figure("fig01_needed", vb).add(top, bottom)


# ---- fig03: robust --------------------------------------------------------------------------------------------------
RELATIONS = ("countries", "languages", "people", "cities", "companies", "landmarks", "dishes", "animals")
STARTS = (("startP", "start P (read)"), ("startT", "start T (tracked)"), ("startM", "start M (recalled)"))
REPLICATIONS = (("mk", "run of record"), ("r2", "rendering 2"), ("r3", "rendering 3"), ("halfA", "test half A"),
                ("halfB", "test half B"), ("soft", "scored by probability"))  # fmt: skip


def _by_condition(kind, conds, key, cid, rows, rot=None, lim=(-8, 100)):
    """Rows are conditions, columns the strong models: M − K per condition, the rotated knock-out grey where run."""
    cols = []
    for i, m in rows:
        lens, ctrl = {}, {}
        for c, _name in conds:
            v_ = b(key.format(i, c))
            if v_:
                lens[c] = est(v_, f"{cid}.{i}", key.format(i, c), label=True)
            r = b(rot.format(i, c)) if rot else None
            if r:
                ctrl[c] = est(r, f"{cid}.{i}", rot.format(i, c), interval=False)
        series = [sp.Series("control", ctrl, control="rotated")] if ctrl else []
        cols.append(sp.DotColumn(vocab().entity("models", m).name, "gap", lim, (0, 40, 80),
                                 series=[*series, sp.Series("neutral", lens)]))  # fmt: skip
    return sp.DotTable([c for c, _n in conds], cols, kind=kind)


def fig03_robust() -> sp.Figure:
    """For the three strong models, M − K under the top-10 knock-out on every relation (the rotated knock-out grey),
    every start, and the replications (renderings, test halves, scored by probability)."""
    rows = [(i, m) for i, m in models_with("ko.{}.mk") if i in ("q9", "q27", "nl")]
    rel = tuple((r, r) for r in RELATIONS)
    v = vocab().with_entities("relations", rel).with_entities("checks", STARTS + REPLICATIONS)
    return sp.Figure("fig03_robust", v).add(
        _by_condition("relations", rel, "ko.{}.rel.{}", "robust", rows, rot="ko.{}.rel.{}.rot"),
        _by_condition("checks", STARTS + REPLICATIONS, "ko.{}.{}", "robust", rows),
    )


# ---- fig05: carries -------------------------------------------------------------------------------------------------
SWAP_CONTROLS = (("paste", "the whole state swapped in"), ("swap_comp", "the rest swapped in"),
                 ("swap_rot", "rotated"), ("swap_u", "logit lens"))  # fmt: skip


def _swap_key(i: str) -> str | None:
    for stem in (f"swap.{i}", f"swap.{i}.mid"):
        if b(f"{stem}.swap"):
            return stem
    return None


def fig05_carries() -> sp.Figure:
    """Per model, the answers moved to another entity's attribute when the lens part at the bridge's mention is
    swapped in from that entity (its top 10 directions), against the whole state pasted, everything but the lens part
    swapped, the swap rotated, and the logit-lens part (grey). Bolt and Ministral at their mid band, K = 10."""
    rows = [(i, m, s) for i, m in ids().items() if (s := _swap_key(i))]
    lens = {m: est(b(f"{s}.swap"), f"swap.{i}", f"{s}.swap", label=True) for i, m, s in rows}
    series = [sp.Series("control", {m: est(c, f"swap.{i}", f"{s}.{k}") for i, m, s in rows if (c := b(f"{s}.{k}"))},
                        control=name) for k, name in SWAP_CONTROLS]  # fmt: skip
    # one column per arm, as fig01
    t = sp.DotTable([m for _i, m, _s in rows], [
        sp.DotColumn("another entity's lens part swapped in", "moved", (-6, 80), (0, 30, 60),
                     series=[sp.Series("lens", lens)]),
        *(sp.DotColumn(s.control, "moved", (-6, 80), (0, 30, 60), series=[s]) for s in series)])  # fmt: skip
    return sp.Figure("fig05_carries", vocab()).add(t)


# ---- fig09: dose ----------------------------------------------------------------------------------------------------
DOSES = (1, 3, 10, 30, 100, 300)


def fig09_dose() -> sp.Figure:
    """Per model and number of lens directions knocked out (columns: 1 to 300), M − K, the rotated knock-out of the
    same size grey (its interval was not kept)."""
    rows = models_with("dose.{}.k10")
    cols = []
    for k in DOSES:
        lens, rot = {}, {}
        for i, m in rows:
            c = b(f"dose.{i}.k{k}")
            if c:
                lens[m] = est(c, f"dose.{i}", f"dose.{i}.k{k}", label=False)
            r = b(f"dose.{i}.k{k}.rot")
            if r:
                rot[m] = est(r, f"dose.{i}", f"dose.{i}.k{k}.rot", interval=False)
        cols.append(sp.DotColumn(f"{k} lens directions", "gap", (-8, 80), (0, 30, 60),
                                 series=[sp.Series("control", rot, control="rotated"), sp.Series("neutral", lens)]))  # fmt: skip
    return sp.Figure("fig09_dose", vocab()).add(sp.DotTable([m for _i, m in rows], cols))


# ---- fig04: where ---------------------------------------------------------------------------------------------------
WHERE = (("all", "every token"), ("bridge", "the bridge's mention"), ("context", "the passage"),
         ("question", "the question"))  # fmt: skip


def fig04_where() -> sp.Figure:
    """Per model, M − K when the knock-out acts only at some tokens (columns): every token, the bridge's mention, the
    passage around it, the question (all starts pooled)."""
    rows = models_with("pos.{}.all.all")
    cols = []
    for w, header in WHERE:
        cells = {m: est(c, f"pos.{i}", f"pos.{i}.all.{w}", label=True) for i, m in rows if (c := b(f"pos.{i}.all.{w}"))}
        cols.append(sp.DotColumn(header, "gap", (-8, 70), (0, 30, 60), series=[sp.Series("neutral", cells)]))
    return sp.Figure("fig04_where", vocab()).add(sp.DotTable([m for _i, m in rows], cols))


def _pointer():
    fig = RS.FIGS["r4_pointer"]()
    fig.id = "fig06_pointer"
    return fig


FIGS = {"fig01_needed": fig01_needed, "fig03_robust": fig03_robust, "fig04_where": fig04_where,
        "fig05_carries": fig05_carries, "fig06_pointer": _pointer, "fig09_dose": fig09_dose}  # fmt: skip


def build(ids_=None) -> list[str]:
    return RS.build(ids_, figs=FIGS, dirs={fid: path(fid).parent for fid in FIGS})


if __name__ == "__main__":
    sys.exit(1 if build(sys.argv[1:] or None) else 0)
